#!/usr/bin/env python3
"""Host transport and pure q2remote protocol checks."""
import json
import os
import contextlib
import io
import pathlib
import re
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
saved_host, saved_key = os.environ.pop("Q2_HOST", None), os.environ.pop("Q2_KEY", None)
try: q.shell("true")
except ValueError as e: assert "Q2_HOST and Q2_KEY" in str(e)
else: raise AssertionError("missing configuration accepted")
os.environ.update({k: v for k, v in (("Q2_HOST", saved_host), ("Q2_KEY", saved_key)) if v is not None})
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

# A padded framebuffer page with four distinct corners validates metadata, orientation and BGRA conversion.
w, h, stride = 320, 375, 320 * 4 + 8
page = bytearray(stride * h)
for x, y, bgra in ((0, 0, bytes((0, 0, 255, 255))), (319, 0, bytes((0, 255, 0, 255))),
                   (0, 374, bytes((255, 0, 0, 255))), (319, 374, bytes((255, 255, 255, 255)))):
    page[y * stride + x * 4:y * stride + x * 4 + 4] = bgra
frame = b"Q2FB\0" + struct.pack("<IIII", w, h, stride, len(page)) + page
png = q.framebuffer_png(frame)
assert png[:8] == b"\x89PNG\r\n\x1a\n"
assert struct.unpack_from(">II", png, 16) == (375, 320)
at, compressed = 8, bytearray()
while at < len(png):
    n = struct.unpack_from(">I", png, at)[0]; tag = png[at + 4:at + 8]; body = png[at + 8:at + 8 + n]
    if tag == b"IDAT": compressed.extend(body)
    at += n + 12
decoded = zlib.decompress(compressed)
def pixel(x, y): return decoded[y * (1 + 375 * 4) + 1 + x * 4:y * (1 + 375 * 4) + 1 + x * 4 + 4]
assert pixel(0, 0) == bytes((0, 255, 0, 255))
assert pixel(374, 0) == bytes((255, 255, 255, 255))
assert pixel(0, 319) == bytes((255, 0, 0, 255))
assert pixel(374, 319) == bytes((0, 0, 255, 255))
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
    card = lambda on: mounts.write_text(f"/dev/mmcblk4p1 {root} vfat rw 0 0\n" if on else "")
    card(True)
    port = 32000 + os.getpid() % 20000
    q.PORT = port
    exe = root / "q2remote"
    subprocess.run(["cc", "-DREMOTE_HOST", f'-DKEY_FILE="{keyfile}"', f'-DCARD="{root}"', f'-DMOUNTS="{mounts}"',
                    f'-DCACHE_FILE="{cache}"', f"-DPORT={port}",
                    str(pathlib.Path(__file__).resolve().parents[1] / "patch/remote.c"), "-o", str(exe)], check=True)
    proc = subprocess.Popen([exe], start_new_session=True)  # its own group: forked children die with it
    try:
        for _ in range(100):  # a forked child writes it: up to 5 s on a loaded host
            if cache.exists() and cache.read_text(): break
            time.sleep(.05)
        assert cache.read_text() == "0123456789abcdef\n"  # kept at start, before any client
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

        os.environ["Q2_KEY"] = "ffffffffffffffff"
        try: q.shell("printf should-not-run")
        except PermissionError: pass
        else: raise AssertionError("wrong key accepted")
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
        with socket.create_connection(("127.0.0.1", port), 2) as s:
            s.sendall(b"fedcba9876543210\n")
            s.settimeout(12)
            assert s.recv(16) == b""  # 10-second handshake timeout
    finally:
        with contextlib.suppress(ProcessLookupError): os.killpg(proc.pid, signal.SIGTERM)
        proc.wait(timeout=2)
print("Remote auth, rotation/removal, USB-storage key cache, fragmented requests, binary stdin/output, timeout, devices, framebuffer and peek checks passed.")
