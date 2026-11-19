#!/usr/bin/env python3
"""tools/tstop.c on the host: built for x86-64 (the Q2's mipsel build can't ptrace under qemu-user), run
against a dummy two-thread process. Checks that it stops only the thread asked, that the other keeps
running, that a hold ends with the thread running again, and that killing tstop lets the thread go."""
import os
import pathlib
import shutil
import signal
import subprocess
import sys
import tempfile
import time

ROOT = pathlib.Path(__file__).resolve().parents[1]
CC = ["clang", "-Os", "-Wall", "-Wextra", "-Werror", "-ffreestanding", "-fno-builtin", "-fno-stack-protector",
      "-fno-unwind-tables", "-fno-asynchronous-unwind-tables", "-ffunction-sections"]
# Two threads that sleep a millisecond in a loop: the main one (tid = pid) and a worker named
# stall_dummy, whose tid it prints.
DUMMY = r"""
#define _GNU_SOURCE
#include <linux/prctl.h>
#include <pthread.h>
#include <stdio.h>
#include <sys/syscall.h>
#include <sys/prctl.h>
#include <unistd.h>
static void *worker(void *a) {
    pthread_setname_np(pthread_self(), "stall_dummy");
    printf("%ld\n", syscall(SYS_gettid)), fflush(stdout);
    for (;;) usleep(1000);
    return a;
}
int main(void) {
    pthread_t t;
    prctl(PR_SET_PTRACER, PR_SET_PTRACER_ANY); /* Yama's scope 1: tstop is not this process's parent */
    pthread_create(&t, 0, worker, 0);
    for (;;) usleep(1000);
}
"""


def run(*cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def state(pid, tid):
    return pathlib.Path(f"/proc/{pid}/task/{tid}/stat").read_text().rsplit(")", 1)[1].split()[0]


def switches(pid, tid):  # voluntary context switches: each usleep(1000) of a running thread adds one
    for line in pathlib.Path(f"/proc/{pid}/task/{tid}/status").read_text().splitlines():
        if line.startswith("voluntary_ctxt_switches"):
            return int(line.split()[1])


def wait_state(pid, tid, want, secs=3):
    end = time.time() + secs
    while time.time() < end:
        if state(pid, tid) in want:
            return True
        time.sleep(0.02)
    return False


def main():
    with tempfile.TemporaryDirectory() as d:
        d = pathlib.Path(d)
        tstop, dummy = d / "tstop", d / "dummy"
        r = run(*CC, "--target=x86_64-linux-gnu", "-c", ROOT / "tools/tstop.c", "-o", d / "t.o")
        assert r.returncode == 0, r.stderr
        r = run("ld.lld", "-static", "-e", "_start", "--gc-sections", d / "t.o", "-o", tstop)
        assert r.returncode == 0, r.stderr
        # the Q2's build: o32 mipsel, no libc. qemu-user has no ptrace, so it can only list and refuse
        r = run(*CC, "--target=mipsel-linux-gnu", "-march=mips32r2", "-mno-abicalls", "-G0", "-fno-pic",
                "-msoft-float", "-c", ROOT / "tools/tstop.c", "-o", d / "m.o")
        assert r.returncode == 0, r.stderr
        mips = d / "tstop-mipsel"
        r = run("ld.lld", "-m", "elf32ltsmip", "-static", "-e", "_start", "--gc-sections", d / "m.o", "-o", mips)
        assert r.returncode == 0, r.stderr
        elf = mips.read_bytes()
        assert elf[:4] == b"\x7fELF" and elf[4:6] == b"\x01\x01" and elf[16:20] == b"\x02\x00\x08\x00", "ELF32 LE EXEC MIPS"
        heads = run("llvm-readelf", "-l", mips).stdout
        assert "INTERP" not in heads and "DYNAMIC" not in heads, "static"
        assert "U " not in run("llvm-nm", mips).stdout, "no undefined symbols"
        if (qemu := shutil.which("qemu-mipsel")):
            assert run(qemu, mips).returncode == 2
            r = run(qemu, mips, "-l", str(os.getpid()))
            assert r.returncode == 0 and "main thread" in r.stdout, r
            assert run(qemu, mips, "-l", "99999999").returncode == 1

        (d / "dummy.c").write_text(DUMMY)
        r = run("gcc", "-O1", "-pthread", d / "dummy.c", "-o", dummy)
        assert r.returncode == 0, r.stderr

        r = run(tstop)
        assert r.returncode == 2 and "usage" in r.stderr
        for bad in (["x"], ["0"], ["5", "x"], ["-l"], ["-l", "x"], ["1", "2", "3"]):
            assert run(tstop, *bad).returncode == 2, bad
        assert run(tstop, "-l", "99999999").returncode == 1

        proc = subprocess.Popen([dummy], stdout=subprocess.PIPE, text=True)
        try:
            worker = int(proc.stdout.readline())
            pid = proc.pid
            lines = run(tstop, "-l", str(pid)).stdout.splitlines()
            assert f"{pid} dummy" in lines and f"{worker} stall_dummy" in lines, lines
            assert any("main thread" in line for line in lines)

            # stop the main thread for 3 s: it is traced-stopped, the worker runs, then both run
            held = subprocess.Popen([str(tstop), str(pid), "3"], stdout=subprocess.PIPE, text=True)
            assert wait_state(pid, pid, "t"), state(pid, pid)
            n = switches(pid, worker)
            time.sleep(0.3)
            assert switches(pid, worker) > n + 20  # the worker ran on while the main thread was held
            assert held.wait(timeout=10) == 0
            assert held.stdout.read() == f"stopped {pid} dummy\ndetached {pid}\n"
            assert wait_state(pid, pid, "SR"), state(pid, pid)

            # the worker thread alone, held until tstop is killed: the process's other thread runs on
            held = subprocess.Popen([str(tstop), str(worker), "0"], stdout=subprocess.PIPE, text=True)
            assert wait_state(pid, worker, "t")
            assert state(pid, pid) in "SR"
            time.sleep(1.2)
            assert held.poll() is None and state(pid, worker) == "t"
            n = switches(pid, pid)
            time.sleep(0.3)
            assert switches(pid, pid) > n + 20  # and the main thread ran on while the worker was held
            held.send_signal(signal.SIGTERM)  # the kernel detaches it
            held.wait(timeout=5)
            assert wait_state(pid, worker, "SR"), state(pid, worker)

            # a thread that is gone
            r = run(tstop, "99999999", "1")
            assert r.returncode == 1 and "errno" in r.stderr
        finally:
            proc.kill()
            proc.wait()
    print("tstop: -l lists the threads, a hold stops only the thread asked, detach and a killed tstop resume it.")


if __name__ == "__main__":
    sys.exit(main())
