/* tstop: stop ONE thread of a process with ptrace, hold it, let it go.
 *
 * kill -STOP stops a whole process, so it stops demo's stall thread (patch/system.c stall_watch)
 * along with the UI loop, and the stall record the thread would write at 20 s is never produced.
 * PTRACE_SEIZE and PTRACE_INTERRUPT stop only the thread asked: the others run on. The hardware
 * watchdog is fed by the UI loop alone (wdt_poll), so stopping demo's main thread (tid == pid)
 * starves it, and the stall thread, still running, writes /mnt/data/q2-stall after STALL_MS (20 s).
 *
 *   tstop -l PID           list PID's threads: tid and comm (the main thread's tid is PID)
 *   tstop TID [SECONDS]    stop thread TID for SECONDS (default 30; 0 = until tstop is killed),
 *                          then detach it. A tstop that is killed (Ctrl-C, SIGTERM, SIGKILL) or
 *                          that crashes lets go as well: the kernel detaches a tracer's tracees
 *                          when it exits.
 *
 * Exit 0 after a hold and a detach, 1 on a failed ptrace call or a thread that ended, 2 for usage.
 *
 * Freestanding on purpose: raw syscalls, no libc, no startup files, so one static ELF runs on the
 * M1 Plus's userland whatever its C library is. mipsel o32 for the device, x86-64 to test on a
 * host:
 *
 *   clang --target=mipsel-linux-gnu -march=mips32r2 -mnan=2008 -mno-abicalls -G0 -fno-pic -msoft-float -Os \
 *         -ffreestanding -fno-builtin -fno-stack-protector -fno-unwind-tables -c tools/tstop.c -o
 * tstop.o ld.lld -m elf32ltsmip -static -e _start --gc-sections tstop.o -o tstop
 *
 * test/tstop.py builds the host one and tries it on a dummy threaded process; see
 * docs/remote.md ("Stopping one thread") for a device pass. */

#define PTRACE_DETACH 17
#define PTRACE_SEIZE 0x4206
#define PTRACE_INTERRUPT 0x4207
#define WNOHANG 1
#define WALL 0x40000000
#define O_DIRECTORY 0x10000 /* the same on MIPS and x86 */
#define DEFAULT_S 30

#if defined(__mips__)
#define NR_read 4003
#define NR_write 4004
#define NR_open 4005
#define NR_close 4006
#define NR_ptrace 4026
#define NR_wait4 4114
#define NR_nanosleep 4166
#define NR_getdents64 4219
#define NR_exit_group 4246
/* o32: number in $2, args in $4-$7; the kernel sets $7 when $2 is an errno. */
static long sys(long n, long a, long b, long c, long d) {
    register long v0 __asm__("$2") = n;
    register long a0 __asm__("$4") = a, a1 __asm__("$5") = b, a2 __asm__("$6") = c;
    register long a3 __asm__("$7") = d;
    __asm__ volatile("syscall"
                     : "+r"(v0), "+r"(a3)
                     : "r"(a0), "r"(a1), "r"(a2)
                     : "$1", "$3", "$8", "$9", "$10", "$11", "$12", "$13", "$14", "$15", "$24",
                       "$25", "hi", "lo", "memory");
    return a3 ? -v0 : v0;
}
/* argc at 0($sp), argv after it. The o32 frame wants 16 bytes below the call, and a nop in the
 * delay slot. */
__asm__(".text\n.globl _start\n.ent _start\n_start:\n.set noreorder\n"
        "move $4, $29\n"
        "addiu $29, $29, -16\n"
        "jal start_c\n"
        "nop\n"
        ".set reorder\n.end _start\n");
#elif defined(__x86_64__)
#define NR_read 0
#define NR_write 1
#define NR_open 2
#define NR_close 3
#define NR_nanosleep 35
#define NR_ptrace 101
#define NR_wait4 61
#define NR_getdents64 217
#define NR_exit_group 231
static long sys(long n, long a, long b, long c, long d) {
    register long r10 __asm__("r10") = d;
    long r;
    __asm__ volatile("syscall"
                     : "=a"(r)
                     : "0"(n), "D"(a), "S"(b), "d"(c), "r"(r10)
                     : "rcx", "r11", "memory");
    return r;
}
__asm__(".text\n.globl _start\n_start:\n"
        "mov %rsp, %rdi\n"
        "and $-16, %rsp\n"
        "call start_c\n");
#else
#error "tstop: add this architecture's syscall numbers, sys() and _start"
#endif

static long slen(const char *s) {
    long n = 0;
    while (s[n]) ++n;
    return n;
}
static void out(int fd, const char *s) { sys(NR_write, fd, (long)s, slen(s), 0); }
static void num(int fd, long v) {
    char b[24], *p = b + sizeof b;
    int neg = v < 0;
    unsigned long u = neg ? -(unsigned long)v : (unsigned long)v;
    *--p = 0;
    do *--p = '0' + u % 10, u /= 10;
    while (u);
    if (neg) *--p = '-';
    out(fd, p);
}
static long parse(const char *s) { /* a non-negative decimal, or -1 */
    long v = 0;
    if (!*s) return -1;
    for (; *s; ++s) {
        if (*s < '0' || *s > '9' || v > 100000000) return -1;
        v = v * 10 + (*s - '0');
    }
    return v;
}
static void proc_path(char *p, long id, const char *tail) { /* "/proc/ID" + tail */
    char d[12];
    long k = 0;
    for (const char *s = "/proc/"; (*p = *s++); ++p) {}
    do d[k++] = '0' + id % 10, id /= 10;
    while (id);
    while (k) *p++ = d[--k];
    while ((*p++ = *tail++)) {}
}
static void ident(int fd, long tid) { /* "TID comm", the comm as /proc/TID/comm has it */
    char path[40], name[32];
    long n, i = 0;
    int f;
    proc_path(path, tid, "/comm");
    num(fd, tid);
    out(fd, " ");
    f = (int)sys(NR_open, (long)path, 0, 0, 0);
    n = f < 0 ? f : sys(NR_read, f, (long)name, sizeof name - 1, 0);
    if (f >= 0) sys(NR_close, f, 0, 0, 0);
    if (n <= 0) {
        out(fd, "?\n");
        return;
    }
    while (i < n && name[i] != '\n') ++i;
    name[i] = 0;
    out(fd, name);
    out(fd, "\n");
}
static int list(long pid) {
    char path[40], buf[2048];
    long n;
    int f;
    proc_path(path, pid, "/task");
    f = (int)sys(NR_open, (long)path, O_DIRECTORY, 0, 0);
    if (f < 0) {
        out(2, "tstop: no such process\n");
        return 1;
    }
    while ((n = sys(NR_getdents64, f, (long)buf, sizeof buf, 0)) > 0) {
        for (long o = 0; o < n;) {
            /* linux_dirent64: ino u64, off s64, reclen u16, type u8, name at 19 */
            unsigned short len = (unsigned char)buf[o + 16] | (unsigned char)buf[o + 17] << 8;
            long tid = parse(buf + o + 19);
            if (tid >= 0) {
                ident(1, tid);
                if (tid == pid) out(1, "  ^ main thread (demo's UI loop)\n");
            }
            o += len;
        }
    }
    sys(NR_close, f, 0, 0, 0);
    return 0;
}
static void sleep_s(long s) {
    long ts[2] = { s, 0 };
    sys(NR_nanosleep, (long)ts, 0, 0, 0);
}
static int hold(long tid, long secs) {
    int st = 0;
    long r = sys(NR_ptrace, PTRACE_SEIZE, tid, 0, 0);
    if (r < 0) {
        out(2, "tstop: PTRACE_SEIZE failed, errno ");
        num(2, -r);
        out(2, "\n");
        return 1;
    }
    r = sys(NR_ptrace, PTRACE_INTERRUPT, tid, 0, 0);
    if (r < 0) {
        out(2, "tstop: PTRACE_INTERRUPT failed, errno ");
        num(2, -r);
        out(2, "\n");
        return 1;
    }
    for (;;) { /* until it reports the stop (an exit or a kill ends it first) */
        r = sys(NR_wait4, tid, (long)&st, WALL, 0);
        if (r < 0) {
            out(2, "tstop: wait4 failed, errno ");
            num(2, -r);
            out(2, "\n");
            return 1;
        }
        if ((st & 0xff) == 0x7f) break; /* WIFSTOPPED */
        out(2, "tstop: thread ended\n");
        return 1;
    }
    out(1, "stopped ");
    ident(1, tid);
    for (long i = 0; !secs || i < secs; ++i) {
        sleep_s(1);
        if (sys(NR_wait4, tid, (long)&st, WALL | WNOHANG, 0) == tid && (st & 0xff) != 0x7f) {
            out(2, "tstop: thread ended while held\n");
            return 1;
        }
    }
    r = sys(NR_ptrace, PTRACE_DETACH, tid, 0, 0);
    if (r < 0) {
        out(2, "tstop: PTRACE_DETACH failed, errno ");
        num(2, -r);
        out(2, "\n");
        return 1;
    }
    out(1, "detached ");
    num(1, tid);
    out(1, "\n");
    return 0;
}
static void usage(void) {
    out(2, "usage: tstop -l PID | tstop TID [SECONDS]  (default 30; 0 = until killed)\n");
    sys(NR_exit_group, 2, 0, 0, 0);
}
__attribute__((used)) void start_c(long *sp) {
    long argc = sp[0], rc = 2;
    char **argv = (char **)(sp + 1);
    if (argc == 3 && argv[1][0] == '-' && argv[1][1] == 'l' && !argv[1][2]) {
        long pid = parse(argv[2]);
        if (pid > 0)
            rc = list(pid);
        else
            usage();
    } else if (argc == 2 || argc == 3) {
        long tid = parse(argv[1]), secs = argc == 3 ? parse(argv[2]) : DEFAULT_S;
        if (tid > 0 && secs >= 0)
            rc = hold(tid, secs);
        else
            usage();
    } else
        usage();
    sys(NR_exit_group, rc, 0, 0, 0);
    for (;;) {}
}
