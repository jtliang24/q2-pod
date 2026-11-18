#!/usr/bin/env python3
"""Host transport and pure q2remote protocol checks."""
import json
import os
import contextlib
import hashlib
import io
import pathlib
import re
import shlex
import signal
import socket
import struct
import subprocess
import tempfile
import time
import zlib

import sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))
import q2remote as q

# Preloaded into the host build of q2remote: /dev/fb0 is the file $Q2_FB, and its two screeninfo ioctls
# read $Q2_FB_INFO, the Q2 kernel's fb_var_screeninfo (160 bytes) then its 32-bit MIPS fb_fix_screeninfo (68).
# A counted build (test/coverage/cc) writes its gcov counts in exit(), but the server's forked children end
# in _exit and the test stops the server with SIGTERM: both end through exit() here. LD_PRELOAD goes at load,
# so the shells the server starts run without the shim.
SHIM = r'''
#define _GNU_SOURCE
#include <dlfcn.h>
#include <errno.h>
#include <fcntl.h>
#include <signal.h>
#include <stdarg.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/ioctl.h>
#include <unistd.h>

static int fb = -1;

int open(const char *path, int flags, ...) {
    int (*real)(const char *, int, ...) = (int (*)(const char *, int, ...))dlsym(RTLD_NEXT, "open");
    mode_t mode = 0;
    if (flags & O_CREAT) { va_list ap; va_start(ap, flags); mode = va_arg(ap, mode_t); va_end(ap); }
    if (strcmp(path, "/dev/fb0")) return real(path, flags, mode);
    const char *mem = getenv("Q2_FB");
    if (!mem) { errno = ENOENT; return -1; }
    return fb = real(mem, flags, mode);
}

int ioctl(int fd, unsigned long request, ...) {
    va_list ap; va_start(ap, request); void *arg = va_arg(ap, void *); va_end(ap);
    if (fd < 0 || fd != fb) return ((int (*)(int, unsigned long, ...))dlsym(RTLD_NEXT, "ioctl"))(fd, request, arg);
    long at = request == 0x4600 ? 0 : request == 0x4602 ? 160 : -1; /* FBIOGET_VSCREENINFO, _FSCREENINFO */
    size_t n = at ? 68 : 160;
    const char *info = getenv("Q2_FB_INFO");
    FILE *f = at < 0 || !info ? 0 : fopen(info, "rb");
    int ok = f && !fseek(f, at, SEEK_SET) && fread(arg, 1, n, f) == n;
    if (f) fclose(f);
    if (!ok) errno = EINVAL;
    return ok ? 0 : -1;
}

void _exit(int status) { exit(status); }
static void term(int sig) { (void)sig; exit(0); }
__attribute__((constructor)) static void init(void) { unsetenv("LD_PRELOAD"); signal(SIGTERM, term); }
'''

# --prof's target. It lets any process trace it (Yama's ptrace_scope 1 allows only ancestors) and says
# ready; then it pauses, or with an argument signals itself without a break. SIGUSR2 ends it, printing
# how many SIGUSR1 it sent and how many reached its handler.
TARGET = r'''
#include <signal.h>
#include <stdio.h>
#include <sys/prctl.h>
#include <unistd.h>
static volatile sig_atomic_t handled, stop;
static void on_usr1(int sig) { (void)sig; ++handled; }
static void on_usr2(int sig) { (void)sig; stop = 1; }
int main(int argc, char **argv) {
    (void)argv;
    prctl(PR_SET_PTRACER, PR_SET_PTRACER_ANY, 0, 0, 0);
    signal(SIGUSR1, on_usr1);
    signal(SIGUSR2, on_usr2);
    puts("ready");
    fflush(stdout);
    long sent = 0;
    while (!stop)
        if (argc > 1) { kill(getpid(), SIGUSR1); ++sent; }
        else pause();
    printf("%ld %ld\n", sent, (long)handled);
    return 0;
}
'''


def fb_info(w=320, h=375, vh=750, y=375, bpp=32, stride=1280, length=None):
    """What the Q2's kernel answers for its panel: fb_var_screeninfo's 40 words (xres, yres, xres_virtual,
    yres_virtual, xoffset, yoffset, bits_per_pixel, ...), then the 32-bit fb_fix_screeninfo: id, smem_start,
    smem_len (the mapped bytes), type, type_aux, visual, x/y pan and wrap steps, line_length (the stride), ..."""
    var = struct.pack("<40I", w, h, w, vh, 0, y, bpp, *[0] * 33)
    fix = struct.pack("<16s5I3H2x4IH6x", b"fake", 0, vh * stride if length is None else length, 0, 0, 2, 0, 1, 0,
                      stride, 0, 0, 0, 0)
    assert len(var) == 160 and len(fix) == 68
    return var + fix


def corners(stride):
    """A 320x375 page of BGRA pixels, stride bytes a row: red, green, blue and white in its corners."""
    page = bytearray(stride * 375)
    for x, y, bgra in ((0, 0, bytes((0, 0, 255, 255))), (319, 0, bytes((0, 255, 0, 255))),
                       (0, 374, bytes((255, 0, 0, 255))), (319, 374, bytes((255, 255, 255, 255)))):
        page[y * stride + x * 4:y * stride + x * 4 + 4] = bgra
    return page


def upright_corners(png):
    """The RGBA corners of framebuffer_png's upright 375x320 image: top left, top right, bottom left, bottom right."""
    assert png[:8] == b"\x89PNG\r\n\x1a\n"
    assert struct.unpack_from(">II", png, 16) == (375, 320)
    at, compressed = 8, bytearray()
    while at < len(png):
        n = struct.unpack_from(">I", png, at)[0]; tag = png[at + 4:at + 8]; body = png[at + 8:at + 8 + n]
        if tag == b"IDAT": compressed.extend(body)
        at += n + 12
    decoded = zlib.decompress(compressed)
    def pixel(x, y): return decoded[y * (1 + 375 * 4) + 1 + x * 4:y * (1 + 375 * 4) + 1 + x * 4 + 4]
    return [pixel(0, 0), pixel(374, 0), pixel(0, 319), pixel(374, 319)]


# The portrait panel turned counterclockwise: its top right is the shot's top left, its top left the bottom left.
UPRIGHT = [bytes((0, 255, 0, 255)), bytes((255, 255, 255, 255)), bytes((255, 0, 0, 255)), bytes((0, 0, 255, 255))]

assert q.event(1, 30, 1) == struct.pack("<IIHHi", 0, 0, 1, 30, 1)
press, release = q.key_events(108)
assert q.decode_events(press)[0][2:] == (q.EV_KEY, 108, 1)
assert q.decode_events(release)[0][2:] == (q.EV_KEY, 108, 0)
assert q.decode_events(press)[-1][2:4] == (q.EV_SYN, 0) and q.decode_events(release)[-1][2:4] == (q.EV_SYN, 0)
assert q.touch_xy(0, 0) == (319, 0) and q.touch_xy(374, 319) == (0, 374)
# One tick is 28 units: overshoot half a tick, steps of at most 11, then the settle frames.
one = q.wheel_positions(1)
assert one[-1] == 58 and one[-1 - q.WHEEL_SETTLE:] == [58] * (q.WHEEL_SETTLE + 1)
assert all(0 < a - b <= q.WHEEL_STEP for a, b in zip([100] + one, one[:-q.WHEEL_SETTLE]))
assert q.wheel_positions(-1)[-1] == 142 and q.wheel_positions(1, start=5)[0] == 195  # x wraps 1-200
assert q.wheel_positions(-3, 7)[-1] == 100 + round(3.5 * 7)
assert [q.wheel_units(c) for c in ("WHEELSENSITIVITY=200\n", "x\nWHEELSENSITIVITY=100\n", "WHEELSENSITIVITY=55\n",
                                   "WHEELSENSITIVITY=050\n", "WHEELSENSITIVITY=210\n", "")] == [7, 14, 28, 28, 28, 28]
saved = {k: os.environ.pop(k, None) for k in ("Q2_HOST", "Q2_KEY", "Q2_KEY_FILE")}
try: q.shell("true")
except ValueError as e: assert "Q2_HOST" in str(e)
else: raise AssertionError("missing host accepted")
with tempfile.NamedTemporaryFile("w") as f:
    f.write("filekey0123456789\n"); f.flush()
    os.environ["Q2_KEY_FILE"] = f.name
    assert q.load_key() == "filekey0123456789"
    os.environ["Q2_KEY_FILE"] = f.name + ".missing"
    try: q.load_key()
    except ValueError as e: assert "Q2_KEY" in str(e)
    else: raise AssertionError("missing key file accepted")
    os.environ["Q2_KEY"] = "envkey0123456789"
    assert q.load_key() == "envkey0123456789"
for k, v in saved.items():
    if v is None: os.environ.pop(k, None)
    else: os.environ[k] = v
# Touch: a tap is press and lift; a swipe moves every SAMPLE_US between its ends; 0 ms writes a gesture at once.
assert len(q.touch_batches([(10, 20)])) == 2
swipe = q.swipe_points(0, 0, 100, 300, 100)
assert swipe[0] == (0, 0) and swipe[-1] == (100, 300) and len(swipe) == 100 * 1000 // q.SAMPLE_US + 1
assert q.decode_events(q.touch_batches(swipe)[-2])[:2] == [(0, 0, q.EV_ABS, q.ABS_X, 19), (0, 0, q.EV_ABS, q.ABS_Y, 100)]
for bad in ((375, 0), (0, 320), (-1, 0)):
    try: q.touch_xy(*bad)
    except ValueError: pass
    else: raise AssertionError("off-screen point accepted")
assert q.event_writer("/x", [b"a", b"b"], 0).count("printf") == 1 and q.event_writer("/x", [b"a", b"b"]).count("printf") == 2
assert q.parse_state("1072\n92.41\n00\n01\n-\n00\n1e\n") == {
    "demo": 1072, "uptime": 92.41, "backlight": 0, "usb": 1, "keylock": None, "lockscreen": 0, "volume": 30}
assert q.M1_GLOBALS.keys() == q.GLOBALS.keys()  # parse_state names the M1's bytes alike
try: q.parse_state("")
except ValueError: pass
else: raise AssertionError("missing demo accepted")
# demo's global addresses match every generated platform header in build/ that has them.
for header in pathlib.Path(__file__).resolve().parents[1].glob("build/*/peq_platform.h"):
    for symbol, addr in q.GLOBALS.values():
        for found in re.findall(rf"^#define {symbol} \(\*\(volatile unsigned char \*\)(0x[0-9a-f]+)u\)$", header.read_text(), re.M):
            assert int(found, 16) == addr, (header, symbol)
gpio = q.parse_devices('''I: Bus=0019 Vendor=0001 Product=0001 Version=0100
N: Name="md-gpio-keys"
H: Handlers=kbd event1
B: EV=3
B: KEY=28 0 101080 0 0 0
''')[0]
assert gpio["event"] == 1 and q.bits(gpio["KEY"]) == {103, 108, 116, 163, 165}
assert q.bits(1 << 116) == {116}
# The M1 Plus's devices as its kernel lists them (V00A): the buttons, the knob and the touch panel.
m1 = {d["name"]: d for d in q.parse_devices('''N: Name="md-gpio-keys"
H: Handlers=kbd event1
B: KEY=38 0 100000 0 0 0

N: Name="md-rotary-knob"
H: Handlers=kbd event2
B: KEY=c0000 0 0 0

N: Name="Goodix-CTP"
H: Handlers=kbd event3
B: KEY=20 0 0 0 0 0 0 100000 0 0 0
B: ABS=2008000 1000003
''')}
assert q.bits(m1["md-gpio-keys"]["KEY"]) == set(q.M1_KEYS.values()) == {116, 163, 164, 165}
assert q.bits(m1[q.M1_KNOB]["KEY"]) == {q.KEY_VOLUMEUP, q.KEY_VOLUMEDOWN}
assert {q.ABS_X, q.ABS_Y, q.ABS_PRESSURE} <= q.bits(m1["Goodix-CTP"]["ABS"]) and 330 not in q.bits(m1["Goodix-CTP"]["KEY"])
# The device answers once whether it is an M1 Plus (its knob); input then goes to the M1's own nodes:
# Goodix-CTP for tap and swipe, the knob for knob, and tap X Y MS holds. A Q2 keeps upstream's paths.
M1_DEVICES = """N: Name="md-gpio-keys"\nH: Handlers=kbd event1\n\nN: Name="md-rotary-knob"\nH: Handlers=kbd event2\n
N: Name="Goodix-CTP"\nH: Handlers=kbd event3\n"""
real_shell, sent = q.shell, []
def fake_shell(cmd, data=b"", *a, **k):
    sent.append((cmd, data)); return M1_DEVICES.encode() if "input/devices" in cmd else b""
q.shell, q._M1 = fake_shell, None
try:
    assert q.is_m1() and q.is_m1() and len(sent) == 1  # asked once
    for argv, node in ((["tap", "10", "20", "500"], 3), (["swipe", "1", "2", "3", "400"], 3), (["knob", "-2"], 2),
                       (["key", "play"], 1)):
        del sent[:]; assert q.main(argv) == 0
        assert f"/dev/input/event{node}".encode() in sent[-1][1] and sent[-1][0] == "sh", argv
    for argv, why in ((["wheel", "1"], "use knob N"), (["key", "return"], "key must be one of")):
        try: q.main(argv)
        except ValueError as e: assert why in str(e), e
        else: raise AssertionError(argv)
    q._M1 = False
    try: q.main(["tap", "1", "2", "3"])
    except ValueError as e: assert str(e) == "invalid arguments for tap"
    else: raise AssertionError("a Q2 tap took a hold")
finally:
    q.shell, q._M1 = real_shell, None
# Goodix-CTP's Phys can hold junk, blank lines too (the 1.5.8 pass): the block stays whole.
junk = q.parse_devices('N: Name="Goodix-CTP"\nP: Phys=\x01\x7f\n\n\x02junk\n\nS: Sysfs=/devices/virtual/input/input3\n'
                       'H: Handlers=kbd event3\nB: ABS=2008000 1000003\n\nN: Name="md-rotary-knob"\nP: Phys=\nH: Handlers=kbd event2\n')
assert [(d["name"], d["event"]) for d in junk] == [("Goodix-CTP", 3), ("md-rotary-knob", 2)] and junk[0]["ABS"]
# A tap as the panel sent the user's: point, pressure 1 then 0, pressure 1, then 0 at the release.
tap = [q.decode_events(b) for b in q.m1_tap(29, 462)]
assert [[e[2:] for e in b] for b in tap] == [
    [(q.EV_ABS, q.ABS_X, 29), (q.EV_ABS, q.ABS_Y, 462), (q.EV_ABS, q.ABS_PRESSURE, 1), (q.EV_ABS, q.ABS_PRESSURE, 0), (q.EV_SYN, 0, 0)],
    [(q.EV_ABS, q.ABS_PRESSURE, 1), (q.EV_SYN, 0, 0)], [(q.EV_ABS, q.ABS_PRESSURE, 0), (q.EV_SYN, 0, 0)]]
# A swipe: the tap's two down frames, moves with only the axes that changed, then the release. A
# vertical drag's moves carry Y alone, as the panel's did; 120 ms is ten 12 ms frames.
swipe = [q.decode_events(b) for b in q.m1_swipe(160, 400, 160, 100, 120)]
assert swipe[:2] == tap[:2] or [[e[2:] for e in b] for b in swipe[:2]] == [
    [(q.EV_ABS, q.ABS_X, 160), (q.EV_ABS, q.ABS_Y, 400), (q.EV_ABS, q.ABS_PRESSURE, 1), (q.EV_ABS, q.ABS_PRESSURE, 0), (q.EV_SYN, 0, 0)],
    [(q.EV_ABS, q.ABS_PRESSURE, 1), (q.EV_SYN, 0, 0)]]
moves = [[e[2:] for e in b] for b in swipe[2:-1]]
assert len(moves) == 10 and all(m[0][:2] == (q.EV_ABS, q.ABS_Y) and len(m) == 2 for m in moves)
assert [m[0][2] for m in moves] == [400 - 30 * i for i in range(1, 11)]
assert [e[2:] for e in swipe[-1]] == [(q.EV_ABS, q.ABS_PRESSURE, 0), (q.EV_SYN, 0, 0)]
diagonal = [[e[2:] for e in q.decode_events(b)] for b in q.m1_swipe(0, 0, 3, 30, 120)[2:-1]]
end = {}
for m in diagonal: end.update({code: value for _, code, value in m[:-1]})
assert all(m[-1] == (q.EV_SYN, 0, 0) for m in diagonal) and end == {q.ABS_X: 3, q.ABS_Y: 30}
assert sum(1 for m in diagonal if m[0][1] == q.ABS_X) == 3  # X changes three times, Y every frame
# Per-gap delays: a held tap waits the hold before its release.
writer = q.event_writer("/dev/input/event3", q.m1_tap(1, 2), [12000, 1000000])
assert writer.count("usleep") == 2 and "usleep 12000" in writer and writer.index("usleep 1000000") > writer.index("usleep 12000")
assert q.event_writer("/dev/null", q.key_events(116), 5).count("usleep 5;") == 1
# Opened once: one exec, every frame to fd 3; otherwise each frame reopens the path, as the Q2's did.
once = q.event_writer("/dev/input/event3", q.m1_swipe(0, 0, 0, 100, 120), q.M1_FRAME_US, once=True)
assert once.startswith("exec 3> /dev/input/event3;") and once.count(">&3") == 13 and once.count("/dev/input/event3") == 1
assert q.event_writer("/dev/input/event1", q.key_events(116)).count("> /dev/input/event1") == 2
# Two detents clockwise, one back: a press and a release each.
assert [q.decode_events(b)[0][2:] for b in q.knob_events(2)] == [(q.EV_KEY, 115, 1), (q.EV_KEY, 115, 0)] * 2
assert [q.decode_events(b)[0][2:] for b in q.knob_events(-1)] == [(q.EV_KEY, 114, 1), (q.EV_KEY, 114, 0)]
# Paced (--step-ms): a gap between each of the turn's batches, a detent every step with its release half way, each
# less usleep's start-up; the default is the 20 ms press and 20 ms gap knob always sent; 0 is one write.
assert q.knob_delays(3, 80) == [40000 - q.USLEEP_US] * 5 and len(q.knob_delays(-3, 80)) == len(q.knob_events(-3)) - 1
assert q.knob_delays(1) == [20000 - q.USLEEP_US] and q.knob_delays(2, 3) == [0, 0, 0] and q.knob_delays(2, 0) == 0
paced = q.event_writer("/dev/input/event2", q.knob_events(5), q.knob_delays(5, 150), once=True)
assert paced.count("usleep 72500") == 9 and paced.count(">&3") == 10
assert q.event_writer("/dev/input/event2", q.knob_events(5), q.knob_delays(5, 0), once=True).count(">&3") == 1

# A padded framebuffer page with four distinct corners validates metadata, orientation and BGRA conversion.
w, h, stride = 320, 375, 320 * 4 + 8
page = corners(stride)
frame = b"Q2FB\0" + struct.pack("<IIII", w, h, stride, len(page)) + page
assert upright_corners(q.framebuffer_png(frame)) == UPRIGHT
# The M1 Plus's 320x480 page stays upright: the same corners where they were.
w1, h1, stride1 = 320, 480, 320 * 4
page1 = bytearray(stride1 * h1)
for x, y, bgra in ((0, 0, bytes((0, 0, 255, 255))), (319, 0, bytes((0, 255, 0, 255))),
                   (0, 479, bytes((255, 0, 0, 255))), (319, 479, bytes((255, 255, 255, 255)))):
    page1[y * stride1 + x * 4:y * stride1 + x * 4 + 4] = bgra
png1 = q.framebuffer_png(b"Q2FB\0" + struct.pack("<IIII", w1, h1, stride1, len(page1)) + page1)
assert struct.unpack_from(">II", png1, 16) == (320, 480)
at, compressed = 8, bytearray()
while at < len(png1):
    n = struct.unpack_from(">I", png1, at)[0]; tag = png1[at + 4:at + 8]; body = png1[at + 8:at + 8 + n]
    if tag == b"IDAT": compressed.extend(body)
    at += n + 12
decoded1 = zlib.decompress(compressed)
def pixel1(x, y): return decoded1[y * (1 + 320 * 4) + 1 + x * 4:y * (1 + 320 * 4) + 1 + x * 4 + 4]
assert pixel1(0, 0) == bytes((255, 0, 0, 255)) and pixel1(319, 0) == bytes((0, 255, 0, 255))
assert pixel1(0, 479) == bytes((0, 0, 255, 255)) and pixel1(319, 479) == bytes((255, 255, 255, 255))
for bad in (frame[:20], frame[:-1], frame[:5] + struct.pack("<IIII", w + 1, h, stride, len(page)) + page):
    try: q.framebuffer_png(bad)
    except ValueError: pass
    else: raise AssertionError("bad framebuffer accepted")

# peek: names parse into the base, the path before ->, and each path after one.
assert q.peek_parse("st.qm_timer") == (None, "st", ".qm_timer", [])
assert q.peek_parse("coverflow.c:cf.jobs->key") == ("coverflow.c", "cf", ".jobs", ["key"])
assert q.peek_parse("g_menu.at[3]->a.b[2]->c") == (None, "g_menu", ".at[3]", ["a.b[2]", "c"])
for bad in ("st.", "st->", "1st", "st.a-b", "st[x]", "st;rm"):
    try: q.peek_parse(bad)
    except ValueError: pass
    else: raise AssertionError(f"peek accepted {bad!r}")
assert q.short_type("struct (unnamed at /a/b/navigation.c:4799:8)") == "struct (unnamed at navigation.c:4799)"
assert q.peek_value("unsigned char", b"\xff") == "255 (0xff)" and q.peek_value("char", b"\xff") == "-1"
assert q.peek_value("unsigned int", b"\x07\0\0\0") == "7" and q.peek_value("struct x *", b"\x10\0\xb5\0") == "0x00b50010"
assert q.peek_value("int[20]", bytes(80)) == "[" + ", ".join(["0"] * 16) + ", … 4 more, all 0]"

# A payload of two files, linked where the M1's is: peek reads it as patch.elf and patch.bin, and a
# stand-in device serves patch.bin's bytes as demo's memory.
with tempfile.TemporaryDirectory(prefix="q2-peek-") as td:
    root = pathlib.Path(td); (root / "patch").mkdir(); out = root / "build"; out.mkdir()
    (root / "patch/main.c").write_text('''#define g_flag (*(volatile unsigned char *)0x97cae4u)
#define g_stub m1stub_g_stub
#define read peq_lib_read
extern volatile unsigned char m1stub_g_stub;
typedef struct node { struct node *next; int v; } node_t;
typedef struct { int ctx, id; } pos_t;
static node_t tail = { 0, 7 }, head = { &tail, 5 };
static int fx = 1;
static struct {
    unsigned char flag; unsigned hi : 3, lo : 5; signed s : 4;
    union { int i; float f; };
    struct { short x, y; } pt;
    pos_t at[3]; char name[8]; double d; long long q; _Bool b; unsigned read; node_t *list, *none;
} st = { 200, 5, 17, -3, { 12 }, { -2, 9 }, { { 1, 2 } }, "hello", 1.5, -40, 1, 3, &head, 0 };
int main_use(void) { return st.flag + fx + g_flag + g_stub; }
''')
    (root / "patch/other.c").write_text("static int fx = 2;\nint other_use(void) { return fx; }\n")
    (root / "stub.S").write_text(".data\n.globl m1stub_g_stub\nm1stub_g_stub:\n.byte 9\n")
    flags = ["--target=mipsel-linux-gnu", "-mabi=32", "-mno-abicalls", "-fno-pic", "-G0", "-O0", "-w", "-c"]
    for src in ("patch/main.c", "patch/other.c", "stub.S"):
        subprocess.run(["clang", *flags, str(root / src), "-o", str(root / (pathlib.Path(src).stem + ".o"))], check=True)
    subprocess.run(["ld.lld", "-m", "elf32ltsmip", "-e", "0", "-Ttext=0xb00000", *(str(root / f"{n}.o") for n in ("main", "other", "stub")),
                    "-o", str(out / "patch.elf")], check=True)
    subprocess.run(["llvm-objcopy", "-O", "binary", str(out / "patch.elf"), str(root / "patch.bin")], check=True)
    image = (root / "patch.bin").read_bytes()
    base = min(s[3] for s in q.elf_sections((out / "patch.elf").read_bytes()) if s[1] == 1 and s[2] & 2 and s[5])
    import hashlib
    manifest = {"model": "Shanling M1 Plus", "variant": "stock", "patch_bytes": len(image), "patch_sha256": hashlib.sha256(image).hexdigest()}
    (out / "manifest.json").write_text(json.dumps(manifest))
    memory = {base + i: b for i, b in enumerate(image)} | {0x97cae4: 4}
    calls = []
    def device(reads, payload=None):
        calls.append((list(reads), payload and list(payload)))
        digest = hashlib.sha256(bytes(memory[a] for a in range(payload[0], payload[0] + payload[1]))).hexdigest() if payload else None
        return digest, [bytes(memory[a] for a in range(at, at + n) if a in memory) for at, n in reads]
    q.ROOT, q.PEEK_SOURCE = root, "main.c"
    symbols = q.elf_symbols((out / "patch.elf").read_bytes())
    assert [f for f, _, _ in symbols["fx"]] == ["main.c", "other.c"] and symbols["m1stub_g_stub"][0][0] is None
    lines, failed = q.peek(["st", "st.name", "st.at[1].id", "st.list->v", "st.list->next->v", "st.list->next->next->v",
                            "g_flag", "g_stub", "other.c:fx", "main.c:fx"], out, device)
    assert failed == 1, lines
    text = "\n".join(lines)
    st_line = next(l for l in lines if l.startswith("st @ "))
    assert re.fullmatch(r"st @ 0x00b[0-9a-f]{5}  \(struct \(unnamed at main\.c:9\), \d+ bytes\)", st_line), st_line
    for want in ("  flag = 200 (0xc8)", "  hi = 5", "  lo = 17 (0x11)", "  s = -3", "  i = 12 (0xc)", "  f = 1.6815581571897805e-44",
                 "  pt:\n    x = -2\n    y = 9", '  name = "hello"', "  d = 1.5", "  q = -40", "  b = 1", "  read = 3",
                 "  none = 0x00000000"):
        assert want in text, want
    assert "\n  at = 01 00 00 00 02 00 00 00" + " 00" * 16 + "  (pos_t[3])\n" in text, text  # records: hex and the type
    assert re.search(r'^st\.name = "hello"  \(char\[8\] @ 0x00b', text, re.M)
    assert re.search(r"^st\.at\[1\]\.id = 0  \(int @ ", text, re.M)
    assert re.search(r"^st\.list->v = 5  \(int @ ", text, re.M) and re.search(r"^st\.list->next->v = 7  \(int @ ", text, re.M)
    assert re.search(r"^st\.list->next->next->v: NULL pointer at 0x00b", text, re.M)
    assert "g_flag = 4  (volatile unsigned char @ 0x0097cae4)" in text
    assert re.search(r"^g_stub = 9  \(volatile unsigned char @ 0x00b", text, re.M)
    assert re.search(r"^other\.c:fx = 2  ", text, re.M) and re.search(r"^main\.c:fx = 1  ", text, re.M)
    # One round per -> level; the first also checks the payload, and only the first.
    assert [len(r) for r, _ in calls] == [3, 2, 1, 9] and calls[0][1] == [base, len(image)] and not any(p for _, p in calls[1:])
    def refuses(names, why, build=out, dev=device):
        try: q.peek(names, build, dev)
        except ValueError as e: assert why in str(e), e
        else: raise AssertionError(f"peek {names} accepted")
    refuses(["fx"], "fx is defined in main.c, other.c: name one, as main.c:fx")
    refuses(["st.nope"], "probing patch/main.c: no member named 'nope'")
    refuses(["nothing"], "probing patch/main.c: use of undeclared identifier 'nothing'")
    refuses(["main_use"], "field 'v' declared as a function")
    refuses(["st"], "the device doesn't run", dev=lambda reads, payload=None: ("0" * 64, [b""] * len(reads)))
    memory.pop(0x97cae4)
    assert q.peek(["g_flag"], out, device)[0] == ["g_flag: can't read 1 bytes at 0x0097cae4"]
    # The source changed since the build: st's size in the probe no longer matches patch.elf's.
    (root / "patch/main.c").write_text((root / "patch/main.c").read_text().replace("*none;", "*none; int added;"))
    refuses(["st.flag"], "st is ")
    saved_build = os.environ.pop("Q2_BUILD", None)
    refuses(["st"], "set Q2_BUILD", build=None)
    if saved_build is not None: os.environ["Q2_BUILD"] = saved_build
    q.ROOT, q.PEEK_SOURCE = pathlib.Path(__file__).resolve().parents[1], "navigation.c"

with tempfile.TemporaryDirectory(prefix="q2-remote-") as td:
    root = pathlib.Path(td); keyfile = root / "key"; keyfile.write_text("0123456789abcdef\n")
    mounts, cache = root / "mounts", root / "cache"
    # Away, only a mount whose path starts with the card's is left: it isn't the card.
    card = lambda on: mounts.write_text(f"/dev/mmcblk4p1 {root} vfat rw 0 0\n" if on else f"tmpfs {root}-x tmpfs rw 0 0\n")
    card(False)
    port = 32000 + os.getpid() % 20000
    q.PORT = port
    exe = root / "q2remote"
    subprocess.run(["cc", "-DREMOTE_HOST", f'-DKEY_FILE="{keyfile}"', f'-DCARD="{root}"', f'-DMOUNTS="{mounts}"',
                    f'-DCACHE_FILE="{cache}"', f"-DPORT={port}",
                    str(pathlib.Path(__file__).resolve().parents[1] / "patch/remote.c"), "-o", str(exe)], check=True)
    shim = root / "shim.so"; (root / "shim.c").write_text(SHIM)
    subprocess.run(["cc", "-shared", "-fPIC", str(root / "shim.c"), "-o", str(shim), "-ldl"], check=True)

    # --shot writes Q2FB\0, the width, height, stride and size, little-endian, then the page the panel
    # shows: yoffset rows into its double-buffered framebuffer (docs/remote.md, Protocol).
    fb, info = root / "fb", root / "fb.info"
    def shot(geometry, memory=fb, stdout=subprocess.PIPE):
        info.write_bytes(geometry)
        env = {**os.environ, "LD_PRELOAD": str(shim), "Q2_FB_INFO": str(info)}
        if memory: env["Q2_FB"] = str(memory)
        r = subprocess.run([exe, "--shot"], env=env, stdout=stdout, timeout=10)
        return r.returncode, r.stdout
    for stride, y in ((1280, 375), (1288, 0)):  # unpadded rows showing the second page; padded, the first
        fb.write_bytes(bytes(stride * 375) + corners(stride))  # a black page, then the corners
        shown = fb.read_bytes()[y * stride:(y + 375) * stride]
        assert shot(fb_info(y=y, stride=stride)) == (0, b"Q2FB\0" + struct.pack("<4I", 320, 375, stride, len(shown)) + shown)
    assert upright_corners(q.framebuffer_png(shot(fb_info(y=375, stride=1288))[1])) == UPRIGHT
    # Only the Q2's panel is taken: 320x375 at 32 bits in two pages or more, rows of whole pixels, the shown
    # page inside them and the mapped memory. Anything else, or a framebuffer missing, silent or unmappable,
    # fails with nothing written for the client to decode; so does a shot that can't be written out.
    for geometry in (fb_info(w=321, stride=1284), fb_info(h=376, vh=752), fb_info(bpp=16), fb_info(vh=749, y=0),
                     fb_info(stride=1279), fb_info(y=376), fb_info(length=750 * 1280 - 1), fb_info()[:160], b""):
        assert shot(geometry) == (1, b""), geometry[:28]
    assert shot(fb_info(), memory=None) == shot(fb_info(), memory=pathlib.Path("/dev/null")) == (1, b"")
    with open("/dev/full", "wb") as full:
        assert shot(fb_info(), stdout=full)[0] == 1

    # --prof MS N TID...: N rounds, MS ms apart, of a line per thread, "TID STATE PC RA [STACK...]" in hex,
    # as tools/q2remote.py profile reads them. A thread that's gone or can't be traced (the helper itself)
    # has none; one sampled is left as it was, sleeping, untraced and answering signals.
    target = root / "target"; (root / "target.c").write_text(TARGET)
    subprocess.run(["cc", str(root / "target.c"), "-o", str(target)], check=True)
    sleeper = subprocess.Popen([target], stdout=subprocess.PIPE)
    raiser = subprocess.Popen([target, "raise"], stdout=subprocess.PIPE)
    gone = subprocess.Popen(["true"]); gone.wait()
    try:
        assert sleeper.stdout.readline() == raiser.stdout.readline() == b"ready\n"
        # q2remote traces threads it didn't start, and prints nothing for one it can't trace. That takes Yama's
        # ptrace_scope 0, or 1 with the target's PR_SET_PTRACER_ANY, and no container rule against ptrace: a
        # sibling seizes the sleeper (its exit detaches it) to tell this host apart from a broken --prof.
        probe = ("import ctypes, sys; libc = ctypes.CDLL(None, use_errno=True); "
                 "sys.exit(libc.ptrace(0x4206, int(sys.argv[1]), None, None) and (ctypes.get_errno() or 255))")
        denied = subprocess.run([sys.executable, "-c", probe, str(sleeper.pid)], timeout=10).returncode
        scope = pathlib.Path("/proc/sys/kernel/yama/ptrace_scope")
        assert not denied, (f"this host can't run --prof: PTRACE_SEIZE of a sibling fails ({os.strerror(denied)}); "
                            f"kernel.yama.ptrace_scope is {scope.read_text().strip() if scope.exists() else 'absent'} "
                            "(it has to be 0 or 1) and a container has to allow ptrace")
        started = time.monotonic()
        out = subprocess.run(["sh", "-c", f'exec "$0" --prof 30 3 {sleeper.pid} {gone.pid} $$', exe],
                             capture_output=True, timeout=20, check=True).stdout.decode()
        assert time.monotonic() - started >= .09
        lines = [line.split() for line in out.splitlines()]
        assert [line[:2] for line in lines] == [[str(sleeper.pid), "S"]] * 3, out
        assert all(len(line) >= 4 and all(re.fullmatch("[0-9a-f]+", v) for v in line[2:]) for line in lines), out
        status = pathlib.Path(f"/proc/{sleeper.pid}/status").read_text()
        assert re.search(r"^State:\s+S ", status, re.M) and re.search(r"^TracerPid:\s+0$", status, re.M), status
        # A signal that arrives while a thread is held goes on to it: sampling loses none. On CPUs of their
        # own, the target signals itself during a good share of the instants the sampler holds it.
        cpus = sorted(os.sched_getaffinity(0))[:2]
        os.sched_setaffinity(raiser.pid, cpus[:1])
        out = subprocess.run([exe, "--prof", "0", "1000", str(raiser.pid)], capture_output=True, timeout=20, check=True,
                             preexec_fn=lambda: os.sched_setaffinity(0, cpus[-1:])).stdout.decode()
        assert [line.split()[0] for line in out.splitlines()] == [str(raiser.pid)] * 1000
        for p in (sleeper, raiser): p.send_signal(signal.SIGUSR2)
        assert sleeper.communicate(timeout=5)[0] == b"0 0\n"
        sent, handled = map(int, raiser.communicate(timeout=5)[0].split())
        assert sent == handled > 0, (sent, handled)
    finally:
        for p in (sleeper, raiser): p.kill(); p.wait()

    proc = subprocess.Popen([exe], start_new_session=True, env={**os.environ, "LD_PRELOAD": str(shim)})  # forked children die with its group
    try:
        # The card mounts after q2remote starts at boot: its key is kept once it does, before any client.
        time.sleep(.5)
        assert not cache.exists()
        card(True)
        for _ in range(100):  # a forked child writes it: up to 5 s on a loaded host
            if cache.exists() and cache.read_text(): break
            time.sleep(.05)
        assert cache.read_text() == "0123456789abcdef\n"
        # A second copy can't have the port and exits; the first still answers.
        assert subprocess.run([exe], timeout=10).returncode == 1
        os.environ.update(Q2_HOST="127.0.0.1", Q2_KEY="0123456789abcdef")
        assert q.shell("cat", b"\x00binary\xff") == b"\x00binary\xff"
        for _ in range(3): assert q.shell("printf repeated") == b"repeated"
        # The CLI transports long/multiline scripts without sharing script text as command stdin.
        for command, expected in (("printf first; read x; printf done", b"firstdone"),
                                  ("read x\nprintf done", b"done"),
                                  ("#" + "x" * 5000 + "\nprintf long", b"long")):
            output = io.TextIOWrapper(io.BytesIO())
            with contextlib.redirect_stdout(output): assert q.main(["sh", command]) == 0
            assert output.buffer.getvalue() == expected
        # sh reports the exit status, keeps output without a trailing newline, and kills what outlives its timeout.
        assert q.run("false") == (b"", 1) and q.run("printf x; exit 3") == (b"x", 3) and q.run("printf '\\0a'") == (b"\0a", 0)
        assert q.main(["sh", "--timeout", "5", "exit 4"]) == 4
        try: q.run("sleep 37", timeout=1)
        except TimeoutError as e: group = re.search(r"process group (\d+)", str(e)).group(1)
        else: raise AssertionError("timeout ignored")
        # A timeout leaves the command running (it may be writing a file); kill stops its group.
        assert subprocess.run(["pgrep", "-f", "sleep 37"], capture_output=True).returncode == 0, "timed-out command killed"
        assert q.run(f"kill -- -{group}")[1] == 0; time.sleep(.3)
        assert subprocess.run(["pgrep", "-f", "sleep 37"], capture_output=True).returncode == 1, "process group survived kill"
        # A job left in the background holding the output doesn't hold the reply; nor is a big script too big.
        started = time.monotonic()
        assert q.run("sleep 38 & printf bg") == (b"bg", 0) and time.monotonic() - started < 5
        subprocess.run(["pkill", "-f", "sleep 38"])
        assert q.run("#" + "x" * 200000 + "\nprintf big") == (b"big", 0)
        # push and pull: binary data, a checked MD5, and no write to an unmounted card.
        blob = root / "blob"; blob.write_bytes(b"\0" + bytes(range(256)) * 300)
        assert q.push(blob, str(root / "pushed")) == hashlib.md5(blob.read_bytes()).hexdigest()
        assert (root / "pushed").read_bytes() == blob.read_bytes() and not (root / "pushed.part").exists()
        q.pull(str(root / "pushed"), str(root / "pulled"))
        assert (root / "pulled").read_bytes() == blob.read_bytes()
        try: q.pull(str(root / "absent"), str(root / "pulled"))
        except ValueError: pass
        else: raise AssertionError("missing file pulled")
        try: q.push(blob, q.CARD + "/x")
        except ValueError as e: assert "not mounted" in str(e)
        else: raise AssertionError("pushed to an unmounted card")
        assert q.find(["127.0.0.1", "192.0.2.1"]) == ["127.0.0.1"]
        # End to end, the client's shot: --shot through the server's shell and gzip, saved upright. The
        # client runs the Q2's /usr/bin/q2remote; here it is the host build on the fake panel.
        fb.write_bytes(bytes(1280 * 375) + corners(1280)); info.write_bytes(fb_info())
        helper = (f"Q2_FB={shlex.quote(str(fb))} Q2_FB_INFO={shlex.quote(str(info))} "
                  f"LD_PRELOAD={shlex.quote(str(shim))} {shlex.quote(str(exe))}")
        device_shell = q.shell
        q.shell = lambda cmd, *a, **k: device_shell(cmd.replace("/usr/bin/q2remote", helper), *a, **k)
        try: q.screenshot(root / "shot.png", settle=True)
        finally: q.shell = device_shell
        assert upright_corners((root / "shot.png").read_bytes()) == UPRIGHT

        os.environ["Q2_KEY"] = "ffffffffffffffff"
        try: q.shell("printf should-not-run")
        except PermissionError: pass
        else: raise AssertionError("wrong key accepted")
        # Strict xfail. BUG: q2remote refuses with the request's stdin unread, so closing resets the connection
        # after its ERR, and the client reports the reset as a network failure: a wrong key with sh, push or
        # pull says "cannot reach Q2", which docs/remote.md reads as the Q2 off the network. The errno it names
        # depends on where the reset lands: ENOTCONN at the client's shutdown, ECONNRESET at a read.
        try: q.run("true")
        except PermissionError: raise AssertionError("XPASS: a wrong key with stdin now reads as rejected; make it a plain check")
        except ConnectionError: pass
        else: raise AssertionError("wrong key accepted with stdin")
        os.environ["Q2_KEY"] = "0123456789abcdef"
        keyfile.write_text("fedcba9876543210\n")
        try: q.shell("printf stale")
        except PermissionError: pass
        else: raise AssertionError("rotated key accepted old key")
        os.environ["Q2_KEY"] = "fedcba9876543210"
        assert q.shell("printf rotated") == b"rotated"
        for invalid_key in ("short\n", "bad key with spaces\n", "x" * 128):
            keyfile.write_text(invalid_key)
            try: q.shell("printf invalid")
            except PermissionError: pass
            else: raise AssertionError("malformed card key accepted")
        keyfile.write_text("fedcba9876543210\n")
        keyfile.unlink()
        try: q.shell("printf removed")
        except PermissionError: pass
        else: raise AssertionError("missing key accepted")
        keyfile.write_text("fedcba9876543210\n")
        # Partial and malformed request lines are rejected without running the command; split reads still work.
        with socket.create_connection(("127.0.0.1", port), 2) as s:
            s.sendall(b"fedcba98")
        with socket.create_connection(("127.0.0.1", port), 2) as s:
            for part in (b"fedcba98", b"76543210\n", b"\n"):
                s.sendall(part); time.sleep(.01)
            assert s.recv(16) == b"ERR\n"
        with socket.create_connection(("127.0.0.1", port), 2) as s:
            for part in (b"fedcba98", b"76543210\n", b"true\n"):
                s.sendall(part); time.sleep(.01)
            assert s.recv(16).startswith(b"OK\n")
        # The whole key has to match, and the command line hold no NUL or CR and fit q2remote's 4 KB line.
        def ask(request):
            with socket.create_connection(("127.0.0.1", port), 2) as s:
                s.sendall(request)
                with contextlib.suppress(OSError): s.shutdown(socket.SHUT_WR)
                reply = bytearray()
                with contextlib.suppress(ConnectionResetError):  # what it didn't read resets the connection
                    while part := s.recv(4096): reply += part
            return bytes(reply)
        marker = root / "ran"; touch = f"touch {marker}".encode()
        for request in (b"fedcba987654321\n" + touch + b"\n", b"fedcba98765432100\n" + touch + b"\n",
                        b"fedcba9876543210\n" + touch + b"\0\n", b"fedcba9876543210\n" + touch + b"\r\n",
                        b"fedcba9876543210\n" + touch + b" #" + b"x" * 5000 + b"\n"):
            assert ask(request) == b"ERR\n" and not marker.exists(), request[:40]
        assert ask(b"fedcba9876543210\n" + touch + b" #" + b"x" * 4000 + b"\n") == b"OK\n" and marker.exists()
        # The card's key: 16-126 characters from A-Z a-z 0-9 _ -, on a line of its own (docs/remote.md). One
        # malformed on the card revokes the copy, as a missing one does.
        def accepted(key): return ask(f"{key}\nprintf in\n".encode()) == b"OK\nin"
        for text, key in (("azAZ09_-" * 2 + "\n", "azAZ09_-" * 2), ("k" * 126 + "\n", "k" * 126),
                          ("0123456789abcdef\r\n", "0123456789abcdef")):
            keyfile.write_text(text)
            assert accepted(key) and cache.read_text() == key + "\n", text
        keyfile.write_text("k" * 127)
        assert not accepted("k" * 127)
        for key in ("0123456789abcde", *(f"0123456789abcde{c}" for c in "`{@[/:")):
            keyfile.write_text("fedcba9876543210\n")
            assert accepted("fedcba9876543210") and cache.exists()
            keyfile.write_text(key + "\n")
            assert not accepted(key) and not cache.exists(), key
        keyfile.write_text("fedcba9876543210\n")
        # Shared over USB storage the card is unmounted: the last key read from it still works, until
        # the card is back without its key.
        assert q.shell("printf cached") == b"cached" and cache.read_text() == "fedcba9876543210\n"
        card(False); keyfile.unlink()
        assert q.shell("printf away") == b"away"
        card(True)
        try: q.shell("printf revoked")
        except PermissionError: pass
        else: raise AssertionError("key removed from the card still accepted")
        card(False)
        try: q.shell("printf revoked-away")
        except PermissionError: pass
        else: raise AssertionError("revoked cache accepted")
        assert not cache.exists()
        card(True); keyfile.write_text("fedcba9876543210\n")
        # The copy follows the card's key at the first connection that reads it, through a temporary file:
        # one that can't be written, as on a full disk, leaves the last copy whole and the card's key working.
        tmp = pathlib.Path(f"{cache}.tmp")
        assert q.shell("printf copied") == b"copied" and cache.read_text() == "fedcba9876543210\n"
        keyfile.write_text("rotated_key-0123\n"); tmp.symlink_to("/dev/full")
        os.environ["Q2_KEY"] = "rotated_key-0123"
        assert q.shell("printf full") == b"full"
        assert cache.read_text() == "fedcba9876543210\n" and not os.path.lexists(tmp)
        assert q.shell("printf follows") == b"follows" and cache.read_text() == "rotated_key-0123\n"
        with socket.create_connection(("127.0.0.1", port), 2) as s:
            s.sendall(b"fedcba9876543210\n")
            s.settimeout(12)
            assert s.recv(16) == b""  # 10-second handshake timeout
    finally:
        with contextlib.suppress(ProcessLookupError): os.killpg(proc.pid, signal.SIGTERM)
        proc.wait(timeout=2)
print("Remote auth and key format, rotation/removal, USB-storage key cache and its writes, request limits, binary stdin/output, "
      "timeout, devices, --shot, --prof, framebuffer and peek checks passed.")
