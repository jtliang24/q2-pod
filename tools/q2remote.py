#!/usr/bin/env python3
"""Drive a --dev Q2 over Wi-Fi (Q2_HOST, and Q2_KEY or a key file; see docs/remote.md).

usage: q2remote.py {sh [--timeout S] COMMAND|shot [--settle] OUT.png|state|wake|key NAME [MS]|wheel N [--step-ms MS]|knob N|tap X Y [MS]|swipe X1 Y1 X2 Y2 [MS]|peek NAME...|push LOCAL REMOTE|pull REMOTE LOCAL|install UPDATE.TAR|log [LINES|-f|--clear]|events EVENT [S]|devices|find|reboot [--wait]|prof S [--all] [--build DIR]}"""
import concurrent.futures
import contextlib
import hashlib
import ipaddress
import json
import os
import pathlib
import posixpath
import re
import secrets
import shlex
import socket
import struct
import subprocess
import sys
import tarfile
import tempfile
import time
import zlib

PORT = 2302
W, H = 320, 375
# md-gpio-keys codes; Centre is KEY_POWER (hold 5 s for the shutdown prompt), Return is KEY_UP.
KEYS = {"centre": 116, "center": 116, "return": 103, "play": 108, "next": 163, "prev": 165}
# The M1 Plus (told by its md-rotary-knob): an upright 320x480 screen; its md-gpio-keys have the
# knob's press as Centre and Play/Pause as KEY_PLAYPAUSE, and no Return. The knob turns clockwise as
# KEY_VOLUMEUP, anticlockwise as KEY_VOLUMEDOWN. Goodix-CTP reports screen pixels.
M1_W, M1_H = 320, 480
M1_KEYS = {"centre": 116, "center": 116, "play": 164, "next": 163, "prev": 165}
M1_KNOB = "md-rotary-knob"
KEY_VOLUMEUP, KEY_VOLUMEDOWN = 115, 114
# Goodix-CTP's timing, as recorded on the device: its second down frame and its move frames come
# about 12 ms apart. A tap holds TAP_HOLD_MS unless told otherwise; a swipe takes SWIPE_MS.
M1_FRAME_US = 12000
USLEEP_US = 2500  # busybox usleep's own start-up on the M1 Plus, taken off each delay
TAP_HOLD_MS, SWIPE_MS = 100, 300
EV_SYN, EV_KEY, EV_ABS = 0, 1, 3
BTN_TOUCH, ABS_X, ABS_Y, ABS_PRESSURE = 0x14a, 0, 1, 0x18
WHEEL_UNITS, WHEEL_STEP, WHEEL_SETTLE, SAMPLE_US = 28, 11, 4, 20000
TIMEOUT = 30
KEY_FILE = pathlib.Path(__file__).resolve().parents[1] / "q2remote.key"  # git-ignored
CARD = "/mnt/mmc"
LOG = "/tmp/q2-demo.log"  # --dev builds' demo output (tools/build.py LOG_HOOK)
TRAILER = re.compile(rb"\n\0q2rc=(\d+)\n\Z")  # run()'s last line: the exit status
SETTLE_S, SETTLE_POLL_S, REBOOT_WAIT_S = 5, .15, 360
# demo's byte globals at stock V1.32's addresses, as build/*/peq_platform.h has them; test/remote.py checks them.
GLOBALS = {"backlight": ("g_backlight_status", 0x99f5b0), "usb": ("g_usblink_status", 0xa38aef),
           "keylock": ("g_keylock_flag", 0xa38c32), "lockscreen": ("g_lockscreen_pageflag", 0xa38b0f),
           "volume": ("g_volume", 0xa38c41)}
# The same bytes in V2.1's demo (an M1 Plus build's peq_platform.h: backlight_status, usblink_status, keylock_flag,
# lockscreen_pageflag, volume), read on a Q2 with an md-rotary-knob.
M1_GLOBALS = {"backlight": 0x97cae4, "usb": 0xa059f4, "keylock": 0xa05aa0, "lockscreen": 0xa059fc, "volume": 0x97cb10}


def event(kind, code, value):
    return struct.pack("<IIHHi", 0, 0, kind, code, value)


def load_key():
    if key := os.environ.get("Q2_KEY"):
        return key
    try:
        return pathlib.Path(os.environ.get("Q2_KEY_FILE") or KEY_FILE).read_text().strip()
    except FileNotFoundError:
        raise ValueError("set Q2_KEY or Q2_KEY_FILE, or put q2remote.key in the repo root") from None


def shell(cmd, data=b"", timeout=TIMEOUT, host=None, sink=None, done=None):
    """Run cmd with data on its stdin; its output, or streamed to sink. timeout=None waits forever.

    done(reply) ends the read early: a backgrounded job may keep the connection open."""
    host = host or os.environ.get("Q2_HOST")
    if not host:
        raise ValueError("set Q2_HOST (`find` lists the Q2s on this network)")
    key = load_key()
    try:
        with socket.create_connection((host, PORT), timeout or TIMEOUT) as s:
            s.settimeout(timeout)
            s.sendall(key.encode() + b"\n" + cmd.encode() + b"\n" + data)
            s.shutdown(socket.SHUT_WR)
            out = bytearray()
            while part := s.recv(65536):
                out.extend(part)
                if sink and len(out) >= 3:
                    if out[:3] != b"OK\n":
                        break
                    sink.write(out[3:]); sink.flush(); del out[3:]
                if done and done(out):
                    break
    except socket.timeout as e:
        raise TimeoutError(f"no answer from the Q2 for {timeout or TIMEOUT:g} s") from e
    except OSError as e:
        raise ConnectionError(f"cannot reach Q2 at {host}:{PORT}: {e}") from e
    # The helper answers ERR and closes, or OK and then the output.
    if not out:
        raise ConnectionError("no reply from q2remote")
    if not out.startswith(b"OK\n"):
        raise PermissionError("authentication rejected (check Q2_KEY and /mnt/mmc/q2remote.key)")
    return bytes(out[3:])


def run(script, timeout=TIMEOUT):
    """(output, exit status) of script, run with sh in its own process group.

    Ctrl-C kills that group; a timeout leaves it running (a silent cp may still be writing) and names it."""
    pid = f"/tmp/q2remote-{secrets.token_hex(4)}.pid"
    # As a script on stdin: newlines and over 4 KB (or the 128 KB an exported variable may hold).
    inner = (f'q2remote_script=$(cat); echo $$ >{pid}; (eval "$q2remote_script") </dev/null; r=$?; rm -f {pid}; '
             'printf "\\n\\0q2rc=%d\\n" $r')
    try:
        out = shell(f"exec setsid sh -c {shlex.quote(inner)}", script.encode(), timeout,
                    done=lambda reply: TRAILER.search(reply))
    except KeyboardInterrupt:
        with contextlib.suppress(OSError):
            shell(f"p=$(cat {pid} 2>/dev/null) && kill -- -$p; rm -f {pid}", timeout=5)
        raise
    except TimeoutError as e:
        group = ""
        with contextlib.suppress(OSError):
            group = shell(f"cat {pid} 2>/dev/null", timeout=5).strip().decode()
        if group:
            raise TimeoutError(f"{e}; still running as process group {group} (`sh 'kill -- -{group}'` stops it)") from None
        raise
    m = TRAILER.search(out)
    if not m:
        raise ConnectionError("the Q2 closed the connection before the command finished")
    return out[:m.start()], int(m.group(1))


def parse_devices(text):
    """Parse /proc/bus/input/devices; each result includes name, handlers, and capability bitsets."""
    result = []
    for block in re.split(r"\n\s*\n", text.strip()):
        name = re.search(r'^N: Name="(.*)"$', block, re.M)
        handlers = re.search(r"^H: Handlers=(.*)$", block, re.M)
        if not name or not handlers:
            continue
        caps = {}
        for kind in ("KEY", "ABS"):
            m = re.search(rf"^B: {kind}=(.*)$", block, re.M)
            # Kernel prints unpadded words, most significant first; the Q2 kernel's long is 32-bit.
            caps[kind] = sum(int(w, 16) << 32 * i for i, w in enumerate(reversed(m.group(1).split()))) if m else 0
        events = re.findall(r"event(\d+)", handlers.group(1))
        if events:
            result.append({"name": name.group(1), "event": int(events[0]), "handlers": handlers.group(1), **caps})
    return result


def bits(bitmap):
    return {n for n in range(bitmap.bit_length()) if bitmap >> n & 1}


def decode_events(data):
    if len(data) % 16:
        raise ValueError("truncated input-event stream")
    return list(struct.iter_unpack("<IIHHi", data))


def key_events(code):
    return [event(EV_KEY, code, 1) + event(EV_SYN, 0, 0),
            event(EV_KEY, code, 0) + event(EV_SYN, 0, 0)]


def touch_xy(x, y):
    if not 0 <= x < H or not 0 <= y < W:
        raise ValueError(f"coordinates must be x=0..{H-1}, y=0..{W-1}")
    return W - 1 - y, x


def touch_batches(points):
    """Press at the first upright point, move through the rest, then lift."""
    (px, py), *moves = [touch_xy(x, y) for x, y in points]
    # The touchscreen axes follow the 320x375 portrait panel, while CLI coordinates are upright.
    return ([event(EV_ABS, ABS_X, px) + event(EV_ABS, ABS_Y, py) + event(EV_ABS, ABS_PRESSURE, 1) + event(EV_KEY, BTN_TOUCH, 1) + event(EV_SYN, 0, 0)] +
            [event(EV_ABS, ABS_X, x) + event(EV_ABS, ABS_Y, y) + event(EV_SYN, 0, 0) for x, y in moves] +
            [event(EV_ABS, ABS_PRESSURE, 0) + event(EV_KEY, BTN_TOUCH, 0) + event(EV_SYN, 0, 0)])


def swipe_points(x1, y1, x2, y2, ms):
    """One point every SAMPLE_US from (x1, y1) to (x2, y2) over ms."""
    n = max(1, ms * 1000 // SAMPLE_US)
    return [(x1 + (x2 - x1) * i // n, y1 + (y2 - y1) * i // n) for i in range(n + 1)]


def m1_tap(x, y):
    """A tap as the M1 Plus's Goodix-CTP sends one: the point with pressure 1 then 0 in one frame,
    pressure 1 alone, then 0 at the release (no BTN_TOUCH)."""
    return [event(EV_ABS, ABS_X, x) + event(EV_ABS, ABS_Y, y) + event(EV_ABS, ABS_PRESSURE, 1) +
            event(EV_ABS, ABS_PRESSURE, 0) + event(EV_SYN, 0, 0),
            event(EV_ABS, ABS_PRESSURE, 1) + event(EV_SYN, 0, 0),
            event(EV_ABS, ABS_PRESSURE, 0) + event(EV_SYN, 0, 0)]


def m1_swipe(x0, y0, x1, y1, ms=SWIPE_MS):
    """A drag as Goodix-CTP sends one: the tap's two down frames, a move frame every M1_FRAME_US
    with only the axes that changed (the input core drops the rest), then the release."""
    n = max(1, round(ms * 1000 / M1_FRAME_US))
    moves, at = [], (x0, y0)
    for i in range(1, n + 1):
        x, y = round(x0 + (x1 - x0) * i / n), round(y0 + (y1 - y0) * i / n)
        frame = (event(EV_ABS, ABS_X, x) if x != at[0] else b"") + (event(EV_ABS, ABS_Y, y) if y != at[1] else b"")
        if frame:
            moves.append(frame + event(EV_SYN, 0, 0))
            at = (x, y)
    down, release = m1_tap(x0, y0)[:2], m1_tap(x0, y0)[2:]
    return down + moves + release


def knob_events(ticks):
    """One press and release a detent: positive turns clockwise."""
    code = KEY_VOLUMEUP if ticks > 0 else KEY_VOLUMEDOWN
    return [batch for _ in range(abs(ticks)) for batch in key_events(code)]


def wheel_positions(ticks, units=WHEEL_UNITS, start=100):
    """x samples (1-200 a turn) for `ticks` firmware ticks; positive falls, which is next/down.

    Travel overshoots by half a tick so rounding never loses one, and the final x repeats
    WHEEL_SETTLE times: tslib's dejitter averages small moves, so a gesture that lifts straight
    after its last step lands short."""
    travel = round((abs(ticks) + .5) * units)
    n = -(-travel // WHEEL_STEP)
    sign = -1 if ticks > 0 else 1
    points = [(start + sign * (travel * i // n) - 1) % 200 + 1 for i in range(1, n + 1)]
    return points + points[-1:] * WHEEL_SETTLE


def wheel_units(config):
    """Travel per tick from config.ini's Q2POD WHEELSENSITIVITY, as playback.c reads it."""
    m = re.search(r"^WHEELSENSITIVITY=(\d+)\s*$", config, re.M)
    pct = int(m.group(1)) if m and m.group(1) == str(int(m.group(1))) else 50
    return WHEEL_UNITS * 50 / (pct if 50 <= pct <= 200 and pct % 10 == 0 else 50)


def event_writer(path, batches, delay_us=SAMPLE_US, once=False):
    """A script writing each batch to path delay_us apart, or a list of delays, one per gap; 0 writes
    them all at once. With once, path is opened once for all of them: on the M1 Plus, opening
    Goodix-CTP's device costs about 45 ms, which made a 12 ms move period 60 ms. (The Q2's wheel timing
    was tuned reopening it.)"""
    if delay_us == 0:
        batches = [b"".join(batches)]
    delays = delay_us if isinstance(delay_us, list) else [delay_us] * len(batches)
    commands = [f"exec 3> {shlex.quote(path)}"] if once else []
    for i, batch in enumerate(batches):
        if i:
            commands.append(f"usleep {delays[i - 1]}")
        octets = "".join(f"\\{byte:03o}" for byte in batch)
        commands.append(f"printf '%b' {shlex.quote(octets)} " + (">&3" if once else f"> {shlex.quote(path)}"))
    return "; ".join(commands)


def devices():
    return parse_devices(shell("cat /proc/bus/input/devices").decode("utf-8", "replace"))


def input_path(kind):
    need = {"key": "md-gpio-keys", "tap": "hyn_ts", "wheel": "hyn_sliderbar"}[kind]
    for d in devices():
        if d["name"] == need:
            return f"/dev/input/event{d['event']}"
    raise ValueError(f"no {need} input device; inspect `devices`")


def config():
    return shell("cat /mnt/data/config.ini 2>/dev/null").decode("utf-8", "replace")


def parse_state(text):
    lines = text.split()
    if len(lines) != 2 + len(GLOBALS):
        raise ValueError("demo is not running")
    values = {k: None if v == "-" else int(v, 16) for k, v in zip(GLOBALS, lines[2:])}
    return {"demo": int(lines[0]), "uptime": float(lines[1]), **values}


def state():
    """demo's pid, the uptime and GLOBALS, read from demo's memory: M1_GLOBALS' on an M1 Plus."""
    def reads(addresses):
        return "".join(f'v=$(dd if=/proc/$p/mem bs=1 skip={addr} count=1 2>/dev/null | xxd -p); echo "${{v:--}}"; '
                       for addr in addresses)
    return parse_state(shell(f'p=$(pidof -s demo) && echo $p && cut -d" " -f1 /proc/uptime && '
                             f'if grep -q {M1_KNOB} /proc/bus/input/devices; then {reads(M1_GLOBALS.values())}'
                             f'else {reads(addr for _, addr in GLOBALS.values())}fi').decode())


def wake():
    """Light the screen with Centre unless it is already on, twice with Wake: Double Press; False if it was on."""
    lit = state()["backlight"]
    if lit is None:
        raise RuntimeError("cannot read the backlight byte; see `state`")
    if lit:
        return False
    presses = 2 if re.search(r"^WAKEDOUBLE=1\s*$", config(), re.M) else 1
    shell("sh", event_writer(input_path("key"), key_events(KEYS["centre"]) * presses, 80000).encode())
    for _ in range(20):
        time.sleep(.1)
        if state()["backlight"]:
            return True
    raise RuntimeError("the screen stayed off")


def framebuffer_png(data):
    # helper emits Q2FB\0, little-endian width/height/stride/size, then the displayed page.
    if len(data) < 21 or data[:5] != b"Q2FB\0":
        raise ValueError("invalid framebuffer response")
    w, h, stride, size = struct.unpack_from("<IIII", data, 5)
    pixels = data[21:]
    if (w, h) not in ((W, H), (M1_W, M1_H)) or stride < w * 4 or size != stride * h or len(pixels) != size:
        raise ValueError("invalid or truncated framebuffer data")
    rows = [pixels[y * stride:y * stride + w * 4] for y in range(h)]
    # FB pixels are BGRA. The Q2's portrait framebuffer rotates counterclockwise to upright 375x320;
    # the M1 Plus's is upright already.
    if h == M1_H:
        out_w, out_h = w, h
        raw = b"".join(bytes((p[2], p[1], p[0], p[3])) for row in rows for p in (row[i:i + 4] for i in range(0, w * 4, 4)))
    else:
        out_w, out_h = h, w
        raw = b"".join(bytes((p[2], p[1], p[0], p[3])) for y in range(w) for x in range(h)
                        for p in (rows[x][(w - 1 - y) * 4:(w - y) * 4],))
    png = bytearray(b"\x89PNG\r\n\x1a\n")
    def chunk(tag, body):
        payload = tag + body
        png.extend(struct.pack(">I", len(body)) + payload + struct.pack(">I", zlib.crc32(payload) & 0xffffffff))
    chunk(b"IHDR", struct.pack(">2I5B", out_w, out_h, 8, 6, 0, 0, 0))
    chunk(b"IDAT", zlib.compress(b"".join(b"\0" + raw[y * out_w * 4:(y + 1) * out_w * 4] for y in range(out_h))))
    chunk(b"IEND", b"")
    return bytes(png)


def frame():
    try:  # gzip: about 16 KB instead of 480 KB on the network
        return zlib.decompress(shell("/usr/bin/q2remote --shot | gzip -1"), 31)
    except zlib.error as e:
        raise ValueError("invalid framebuffer response") from e


def screenshot(out, settle=False):
    """Save the displayed frame; with settle, once two frames SETTLE_POLL_S apart match (SETTLE_S at most)."""
    shown, end = frame(), time.monotonic() + SETTLE_S
    while settle:
        time.sleep(SETTLE_POLL_S)
        shown, last = frame(), shown
        if shown == last:
            break
        if time.monotonic() > end:
            print(f"q2remote: the screen kept changing for {SETTLE_S} s", file=sys.stderr)
            break
    png = framebuffer_png(shown)  # no empty file left on an error
    with open(out, "wb") as f:
        f.write(png)
    with contextlib.suppress(ValueError, OSError):
        if state()["backlight"] == 0:
            print("q2remote: the screen is off, so this is the last frame it showed; `wake` first", file=sys.stderr)


def card_mounted():
    if run(f"mountpoint -q {CARD}")[1]:
        raise ValueError(f"{CARD} is not mounted: USB storage has the card (`key return` ends it)")


def push(local, remote, timeout=120):
    """Copy local to remote through remote.part, synced; its MD5."""
    data = pathlib.Path(local).read_bytes()
    md5 = hashlib.md5(data).hexdigest()
    remote = posixpath.normpath(remote)
    q, part = shlex.quote(remote), shlex.quote(remote + ".part")
    # Under USB storage the card is unmounted, and a write would land in the bare mount point. Checked
    # first: a command that exits without reading the upload resets the connection, losing its reply.
    if (remote + "/").startswith(CARD + "/"):
        card_mounted()
    out = shell(f"cat >{part} && sync && mv {part} {q} && sync && md5sum {q} || {{ rm -f {part}; echo failed; }}", data, timeout)
    if out.split()[:1] != [md5.encode()]:
        raise ValueError(f"push failed: {out.decode('utf-8', 'replace').strip()}")
    return md5


def pull(remote, local):
    out, rc = run(f"cat {shlex.quote(remote)}")
    if rc:
        raise ValueError(out.decode("utf-8", "replace").strip())
    with open(local + ".part", "wb") as f:
        f.write(out)
    os.replace(local + ".part", local)


def install(tar):
    if not tarfile.is_tarfile(tar):
        raise ValueError(f"{tar} is not a tar file")
    md5 = push(tar, f"{CARD}/update.tar")
    # Read back from the card, not the page cache.
    out, _ = run(f"sync; echo 3 >/proc/sys/vm/drop_caches; md5sum {CARD}/update.tar", 120)
    if out.split()[:1] != [md5.encode()]:
        raise ValueError("update.tar reads back differently from the card; check the card")


def find(hosts=None):
    """Addresses of this PC's /24 (by its default route) where q2remote answers. The probe sends no key:
    a q2remote answers ERR to any wrong one."""
    if hosts is None:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))  # picks the route's local address; sends nothing
            hosts = [str(h) for h in ipaddress.ip_network(f"{s.getsockname()[0]}/24", strict=False).hosts()]
    def probe(host):
        try:
            with socket.create_connection((host, PORT), 2) as s:
                s.sendall(b"q2remote-find\n\n")
                return host if s.recv(4) == b"ERR\n" else None
        except OSError:
            return None
    with concurrent.futures.ThreadPoolExecutor(64) as pool:
        return [h for h in pool.map(probe, hosts) if h]


def reboot(wait):
    boot = shell("cat /proc/sys/kernel/random/boot_id") if wait else None
    # Detached so the reply arrives before the network drops; the PMIC's 10-15 s Centre reset can't be injected.
    shell("(sleep 1; sync; reboot) </dev/null >/dev/null 2>&1 &")
    if not wait:
        return
    start = time.monotonic()
    for _ in range(REBOOT_WAIT_S // 5):
        time.sleep(5)
        with contextlib.suppress(ConnectionError, TimeoutError):
            if shell("cat /proc/sys/kernel/random/boot_id", timeout=5) != boot:
                print(f"back after {time.monotonic() - start:.0f} s")
                return
    raise TimeoutError(f"the Q2 did not answer within {REBOOT_WAIT_S} s")


def symbol_table(path):
    """(sorted addresses, names) of path's defined functions, dynamic and static."""
    import bisect, subprocess
    table = {}
    for flags in (["-D"], []):
        out = subprocess.run(["llvm-nm", *flags, "--defined-only", path], capture_output=True, text=True).stdout
        for line in out.splitlines():
            w = line.split()
            if len(w) == 3 and w[1] in "tTwW":
                table[int(w[0], 16)] = w[2]
    keys = sorted(table)
    return keys, [table[k] for k in keys], bisect.bisect_right


def profile(seconds, all_threads, build):
    """Sample demo's threads with q2remote --prof; the most frequent functions by thread state."""
    import collections
    out, rc = run("p=$(pidof demo); echo $p; ls /proc/$p/task; cat /proc/$p/maps")
    if rc: raise RuntimeError(out.decode())
    lines = out.decode().split("\n")
    pid = lines[0].strip()
    tids = [l for l in lines[1:] if l.strip().isdigit()]
    maps = []
    for l in lines:
        w = l.split()
        if len(w) >= 6 and "x" in w[1] and "-" in w[0] and w[5].startswith("/"):
            lo, hi = (int(x, 16) for x in w[0].split("-"))
            maps.append((lo, hi, int(w[2], 16), w[5]))
    if not all_threads: tids = [pid]
    hz = 100 if not all_threads else 20
    n = int(seconds * hz)
    raw, rc = run(f"{os.environ.get('Q2_PROF_BIN', 'q2remote')} --prof {1000 // hz} {n} {' '.join(tids)}", timeout=TIMEOUT + seconds * 3)
    cache = pathlib.Path.home() / ".cache/q2-prof"
    cache.mkdir(parents=True, exist_ok=True)
    tables = {}
    def name(addr):
        for lo, hi, off, path in maps:
            if lo <= addr < hi:
                base = posixpath.basename(path)
                cands = []
                if base == "demo" and build:
                    cands = [(pathlib.Path(build) / "patch.elf", 0), (pathlib.Path(build) / "demo", 0)]
                else:
                    local = cache / base
                    if not local.exists(): pull(path, str(local))
                    cands = [(local, lo - off)]
                for f, bias in cands:
                    if f not in tables: tables[f] = symbol_table(str(f))
                    keys, names, bis = tables[f]
                    i = bis(keys, addr - bias) - 1
                    if i >= 0 and addr - bias - keys[i] < 0x20000:
                        return f"{names[i]}+{addr - bias - keys[i]:#x}"[:60]
                return f"{base}+{addr - lo + off:#x}"
        return f"{addr:#x}"
    counts = collections.defaultdict(collections.Counter)
    total = collections.Counter()
    for l in raw.decode().split("\n"):
        w = l.split()
        if len(w) < 4: continue
        tid, state = w[0], w[1]
        key = "running" if state == "R" else "blocked" if state == "D" else "sleeping"
        total[(tid, key)] += 1
        # pc, ra, then the stack's words that fall in code: a heuristic, so a stale word may show
        frames = []
        for x in w[2:]:
            a = int(x, 16)
            if not any(lo <= a < hi for lo, hi, _, _ in maps): continue
            f = name(a).split("+")[0]
            if not frames or frames[-1] != f: frames.append(f)
            if len(frames) == 6: break
        counts[(tid, key)]["  <- ".join(frames)] += 1
    for (tid, key), c in sorted(counts.items(), key=lambda kv: -sum(kv[1].values())):
        print(f"== thread {tid} {key}: {total[(tid, key)]} of {n} samples")
        for k, v in c.most_common(15):
            print(f"{v:6d}  {k}")


def input_action(kind, args):
    devs = {d["name"]: f"/dev/input/event{d['event']}" for d in devices()}
    m1 = M1_KNOB in devs
    if kind == "wheel" and m1: raise ValueError("the M1 Plus has a knob: use knob N")
    if kind == "knob" and not m1: raise ValueError("the Q2 has a wheel: use wheel N")
    need = {"key": "md-gpio-keys", "tap": "Goodix-CTP" if m1 else "hyn_ts", "swipe": "Goodix-CTP" if m1 else "hyn_ts",
            "wheel": "hyn_sliderbar", "knob": M1_KNOB}[kind]
    if need not in devs: raise ValueError(f"no {need} input device; inspect `devices`")
    path = devs[need]
    if kind == "key":
        keys = M1_KEYS if m1 else KEYS
        code = keys.get(args[0].lower())
        if code is None: raise ValueError(f"key must be one of {', '.join(keys)}")
        try: ms = int(args[1]) if len(args) > 1 else 80
        except ValueError: raise ValueError("key duration must be an integer number of milliseconds")
        if not 1 <= ms <= 60000: raise ValueError("key duration must be 1..60000 ms")
        shell("sh", event_writer(path, key_events(code), ms * 1000).encode())
    elif kind == "tap" and m1:
        try: x, y = map(int, args[:2]); hold = int(args[2]) if len(args) > 2 else TAP_HOLD_MS
        except ValueError: raise ValueError("tap coordinates and hold must be integers")
        if not 0 <= x < M1_W or not 0 <= y < M1_H: raise ValueError(f"coordinates must be x=0..{M1_W-1}, y=0..{M1_H-1}")
        if not 1 <= hold <= 10000: raise ValueError("tap hold must be 1..10000 ms")
        shell("sh", event_writer(path, m1_tap(x, y), [M1_FRAME_US - USLEEP_US, max(0, hold * 1000 - USLEEP_US)], once=True).encode())
    elif kind == "swipe" and m1:
        try: x0, y0, x1, y1 = map(int, args[:4]); ms = int(args[4]) if len(args) > 4 else SWIPE_MS
        except ValueError: raise ValueError("swipe coordinates and duration must be integers")
        if not all(0 <= x < M1_W for x in (x0, x1)) or not all(0 <= y < M1_H for y in (y0, y1)):
            raise ValueError(f"coordinates must be x=0..{M1_W-1}, y=0..{M1_H-1}")
        if not 50 <= ms <= 5000: raise ValueError("swipe duration must be 50..5000 ms")
        batches = m1_swipe(x0, y0, x1, y1, ms)
        # stdin: a slow swipe's frames outgrow the 4 KB command line
        shell("sh", event_writer(path, batches, [M1_FRAME_US - USLEEP_US] * (len(batches) - 1), once=True).encode())
    elif kind == "knob":
        try: ticks = int(args[0])
        except ValueError: raise ValueError("knob turn must be an integer")
        if not -100 <= ticks <= 100 or not ticks: raise ValueError("knob turn must be -100..100 detents, not 0")
        shell("sh", event_writer(path, knob_events(ticks), once=True).encode())
    elif kind == "tap":
        try: x, y = map(int, args[:2]); hold = int(args[2]) if len(args) > 2 else SAMPLE_US // 1000
        except ValueError: raise ValueError("tap coordinates and hold must be integers")
        if not 1 <= hold <= 10000: raise ValueError("tap hold must be 1..10000 ms")
        shell("sh", event_writer(path, touch_batches([(x, y)]), hold * 1000).encode())
    elif kind == "swipe":
        try: x1, y1, x2, y2, ms = map(int, args + ["300"] * (len(args) == 4))
        except ValueError: raise ValueError("swipe coordinates and duration must be integers")
        if not 20 <= ms <= 10000: raise ValueError("swipe duration must be 20..10000 ms")
        shell("sh", event_writer(path, touch_batches(swipe_points(x1, y1, x2, y2, ms))).encode())
    elif kind == "wheel":
        if args[1:2] not in ([], ["--step-ms"]): raise ValueError("usage: wheel N [--step-ms MS]")
        try: ticks, step_ms = int(args[0]), int(args[2]) if len(args) == 3 else SAMPLE_US // 1000
        except ValueError: raise ValueError("wheel travel and --step-ms must be integers")
        if not 0 <= step_ms <= 1000: raise ValueError("--step-ms must be 0..1000")
        if not -1000 <= ticks <= 1000: raise ValueError("wheel travel must be -1000..1000 ticks")
        if ticks == 0: return
        path, units = input_path(kind), wheel_units(config())
        # Settle frames alternate y so the input core does not drop them as unchanged.
        batches = [event(EV_ABS, ABS_X, 100) + event(EV_ABS, ABS_Y, 100) +
                   event(EV_ABS, ABS_PRESSURE, 1) + event(EV_KEY, BTN_TOUCH, 1) + event(EV_SYN, 0, 0)]
        batches.extend(event(EV_ABS, ABS_X, x) + event(EV_ABS, ABS_Y, 100 + i % 2) + event(EV_SYN, 0, 0)
                       for i, x in enumerate(wheel_positions(ticks, units)))
        batches.append(event(EV_ABS, ABS_PRESSURE, 0) + event(EV_KEY, BTN_TOUCH, 0) + event(EV_SYN, 0, 0))
        shell("sh", event_writer(path, batches, step_ms * 1000).encode())  # stdin: a long turn outgrows the 4 KB command line


# peek: read payload and demo variables by name from the running demo. The build's patch.elf gives a
# payload variable's address and its source file; a demo global's address is its #define in the
# build's headers. clang compiles a probe that includes that file with the build's flags, for the
# offsets and sizes, and dumps the value's record layout, which names and types each field.
ROOT = pathlib.Path(__file__).resolve().parents[1]
PEEK_NAME = re.compile(r"(?:([\w-]+\.c):)?([A-Za-z_]\w*)((?:\.[A-Za-z_]\w*|\[\d+\]|->[A-Za-z_]\w*)*)")
PEEK_LAYOUT = re.compile(r"\s*(\d+)(?::(\d+)-(\d+))? \|( +)(.*)")
PEEK_SOURCE = "navigation.c"  # declares the payload's shared globals and includes the demo globals' header
PEEK_SHOWN, PEEK_HEX = 16, 32  # array elements, and bytes of a hex dump, printed in full
SCALARS = {"char": "b", "signed char": "b", "unsigned char": "B", "_Bool": "B", "short": "h",
           "unsigned short": "H", "int": "i", "unsigned int": "I", "long": "i", "unsigned long": "I",
           "long long": "q", "unsigned long long": "Q", "float": "f", "double": "d", "long double": "d"}


def elf_sections(data):
    """A 32-bit little-endian ELF's sections, in order: (name, type, flags, addr, offset, size, link)."""
    if data[:6] != b"\x7fELF\x01\x01":
        raise ValueError("not a 32-bit little-endian ELF")
    shoff = struct.unpack_from("<I", data, 32)[0]
    size, num, names = struct.unpack_from("<HHH", data, 46)
    rows = [struct.unpack_from("<7I", data, shoff + i * size) for i in range(num)]
    strings = rows[names][4]
    return [(data[strings + r[0]:data.index(b"\0", strings + r[0])].decode(),) + r[1:] for r in rows]


def elf_symbols(data):
    """{name: [(source file, address, size)]} for the defined objects, functions and labels (the M1's
    stubbed globals are untyped). A local follows its file's STT_FILE symbol; a global's file isn't
    recorded (None)."""
    sections = elf_sections(data)
    symtab = next(s for s in sections if s[1] == 2)
    strings = sections[symtab[6]][4]
    out, file = {}, None
    for at in range(symtab[4], symtab[4] + symtab[5], 16):
        name_at, address, size, info, _, index = struct.unpack_from("<IIIBBH", data, at)
        name = data[strings + name_at:data.index(b"\0", strings + name_at)].decode()
        if info & 15 == 4:
            file = name
        elif info & 15 in (0, 1, 2) and index and name:
            out.setdefault(name, []).append((file if info >> 4 == 0 else None, address, size))
    return out


def peek_parse(name):
    """FILE.c:NAME.FIELD[N]->FIELD as (file or None, NAME, the path before any ->, the paths after each)."""
    m = PEEK_NAME.fullmatch(name)
    if not m:
        raise ValueError(f"{name!r}: expected NAME, NAME.FIELD, NAME[N] or NAME->FIELD, optionally FILE.c:NAME")
    file, base, path = m.groups()
    first, *rest = path.split("->")
    return file, base, first, rest


def peek_probe(source, entries):
    """C that includes source, for entries [(i, NAME, first, rest)]: struct peek_v<i>, whose layout
    is the value's, and in .peek per entry sizeof(NAME), the value's size, its offset in NAME, and
    each -> field's offset in what the pointer before it points to."""
    lines, words = [f'#include "{source}"'], []
    offset = lambda t, path: f"(unsigned)(unsigned long)&(*(__typeof__({t}) *)0){path}" if path else "0u"
    for i, base, first, rest in entries:
        expr = base + first + "".join("->" + r for r in rest)
        lines.append(f"struct peek_v{i} {{ __typeof__({expr}) v; }};")
        words += [f"sizeof({base})", f"sizeof(struct peek_v{i})", offset(base, first)]
        prefix = base + first
        for r in rest:
            words.append(offset(f"*({prefix})", "." + r))
            prefix += "->" + r
    lines.append('__attribute__((used, section(".peek"))) static const unsigned peek_probe[] = {' + ", ".join(words) + "};")
    return "\n".join(lines) + "\n"


def peek_layouts(dump):
    """{i: struct peek_v<i>'s v} from clang's -fdump-record-layouts, as nodes {type, name, offset,
    bits, children}. Offsets are from the value's start; name is None for an anonymous member."""
    out, lines = {}, dump.splitlines()
    for at, line in enumerate(lines):
        m = re.fullmatch(r"\s*0 \| struct peek_v(\d+)", line)
        if not m:
            continue
        root = {"children": []}
        stack = [(0, root)]
        for line in lines[at + 1:]:
            f = PEEK_LAYOUT.fullmatch(line)
            if not f:
                break  # [sizeof=…]
            offset, lo, hi, indent, text = f.groups()
            depth = (len(indent) - 1) // 2
            # an anonymous member's type ends its line: "union (anonymous at …) "
            typ, name = (text.strip(), None) if text.endswith((")", " ")) else text.rsplit(" ", 1)
            if name:  # peq_platform.h's #define read peq_lib_read renames a field called read
                name = re.sub(r"^peq_lib_", "", name)
            node = {"type": typ, "name": name, "offset": int(offset),
                    "bits": (int(lo), int(hi)) if lo else None, "children": []}
            while stack[-1][0] >= depth:
                stack.pop()
            stack[-1][1]["children"].append(node)
            stack.append((depth, node))
        out[int(m.group(1))] = root["children"][0]
    return out


def plain(t):
    return re.sub(r"\b(?:const|volatile|restrict)\b ?", "", t).strip()


def short_type(t):
    """t with clang's "(unnamed at /path/file.c:L:C)" shortened to "(unnamed at file.c:L)"."""
    return re.sub(r"\((unnamed|anonymous)( struct| union)? at (?:[^():]*/)?([^/():]+):(\d+):\d+\)", r"(\1 at \3:\4)", t)


def type_size(t):
    """A scalar's or a scalar array's size, else None (a record)."""
    t = plain(t)
    if "(*)" in t or t.endswith("*"):
        return 4
    m = re.fullmatch(r"(.*?)\[(\d+)\](.*)", t)
    if m:
        size = type_size(m.group(1) + m.group(3))
        return size and size * int(m.group(2))
    code = "i" if t.startswith("enum ") else SCALARS.get(t)
    return struct.calcsize("<" + code) if code else None


def number(v):
    return f"{v} (0x{v:x})" if v >= 10 else str(v)


def hexdump(raw):
    return raw[:PEEK_HEX].hex(" ") + (f" … ({len(raw)} bytes)" if len(raw) > PEEK_HEX else "") if raw else "(0 bytes)"


def peek_value(t, raw, bits=None):
    """raw shown as type t: a number, a pointer, a string, a list, or else hex."""
    t = plain(t)
    if "(*)" in t or t.endswith("*"):
        return f"0x{struct.unpack_from('<I', raw)[0]:08x}"
    code = "i" if t.startswith("enum ") else SCALARS.get(t)
    if code and bits:
        lo, hi = bits
        width = hi - lo + 1
        v = int.from_bytes(raw[:hi // 8 + 1], "little") >> lo & (1 << width) - 1
        return number(v - (1 << width) if code.islower() and v >> width - 1 else v)
    if code:
        v = struct.unpack_from("<" + code, raw)[0]
        return repr(v) if code in "fd" else number(v)
    m = re.fullmatch(r"(.*?)\[(\d+)\](.*)", t)
    if m:
        elem, n = (m.group(1) + m.group(3)).strip(), int(m.group(2))
        size = type_size(elem)
        if size == 1 and SCALARS.get(elem) in ("b", "B") and elem != "_Bool":
            return '"' + raw[:n].split(b"\0", 1)[0].decode("utf-8", "backslashreplace").replace('"', '\\"') + '"'
        if size and len(raw) >= n * size:
            items = [peek_value(elem, raw[k * size:(k + 1) * size]) for k in range(min(n, PEEK_SHOWN))]
            if n > PEEK_SHOWN:
                items.append(f"… {n - PEEK_SHOWN} more" + (", all 0" if not any(raw[PEEK_SHOWN * size:n * size]) else ""))
            return "[" + ", ".join(items) + "]"
    return hexdump(raw)


def peek_lines(label, address, node, raw):
    """A scalar as one line; a record as a header and a line per field, nested records indented and
    an anonymous member's fields shown as its parent's, as C names them."""
    if not node["children"]:
        return [f"{label} = {peek_value(node['type'], raw)}  ({short_type(node['type'])} @ 0x{address:08x})"]
    lines = [f"{label} @ 0x{address:08x}  ({short_type(node['type'])}, {len(raw)} bytes)"]
    def walk(children, end, indent):
        for k, c in enumerate(children):
            # a field runs to the next one after it (union members share an offset), or its parent's end
            stop = min((d["offset"] for d in children[k + 1:] if d["offset"] > c["offset"]), default=end)
            if c["children"] and c["name"]:
                lines.append(f"{indent}{c['name']}:")
                walk(c["children"], stop, indent + "  ")
            elif c["children"]:
                walk(c["children"], stop, indent)
            else:
                shown = peek_value(c["type"], raw[c["offset"]:stop], c["bits"])
                # a hex dump names its type: an array of records, which st.pos[0] would show field by field
                lines.append(f"{indent}{c['name']} = {shown}" + (f"  ({short_type(c['type'])})" if type_size(c["type"]) is None else ""))
    walk(node["children"], len(raw), "  ")
    return lines


def peek_source(file, base, symbols):
    """The patch/ file that defines base: the one named, a local's own, else PEEK_SOURCE."""
    if file:
        return file
    files = sorted({f for f, _, _ in symbols.get(base, []) if f})
    if len(files) > 1:
        raise ValueError(f"{base} is defined in {', '.join(files)}: name one, as {files[0]}:{base}")
    return files[0] if files and files[0].endswith(".c") else PEEK_SOURCE


def peek_address(base, source, symbols, macros, size, out):
    """base's address: its symbol in patch.elf (checked against the probe's size, which tells a
    source changed since the build), or a demo global's #define (*(T *)0x…u), followed through
    defines that rename it."""
    name, seen = base, set()
    while name not in seen:
        seen.add(name)
        found = [s for s in symbols.get(name, []) if s[0] in (source, None)]
        if found:
            _, address, elf_size = found[0]
            if elf_size and elf_size != size:
                raise ValueError(f"{name} is {size} bytes in patch/{source} but {elf_size} in {out}/patch.elf: "
                                 "the source has changed since that build")
            return address
        body = macros.get(name, "")
        m = re.fullmatch(r"\(\*\((?:volatile |const )*[\w ]+\*\)(0x[0-9a-fA-F]+)u?\)", body)
        if m:
            return int(m.group(1), 16)
        if not re.fullmatch(r"[A-Za-z_]\w*", body):
            break
        name = body
    raise ValueError(f"{base} is neither a payload symbol in {out}/patch.elf nor a demo global")


def peek_compile(source, entries, flags, defines=False):
    """Run the probe: (the .peek words, the layouts, and with defines source's #defines)."""
    with tempfile.TemporaryDirectory(prefix="q2-peek-") as td:
        probe, obj = pathlib.Path(td) / "probe.c", pathlib.Path(td) / "probe.o"
        probe.write_text(peek_probe(ROOT / "patch" / source, entries))
        try:
            run = subprocess.run(["clang", *flags, "-c", probe, "-o", obj, "-Xclang", "-fdump-record-layouts-canonical",
                                  "-Xclang", "-fdump-record-layouts-complete"], capture_output=True, text=True)
            text = subprocess.run(["clang", *flags, "-E", "-dM", ROOT / "patch" / source],
                                  capture_output=True, text=True).stdout if defines else ""
        except FileNotFoundError:
            raise ValueError("peek needs clang: run it inside nix develop")
        if run.returncode:
            errors = dict.fromkeys(line.split("error: ", 1)[1] for line in run.stderr.splitlines() if "error: " in line)
            raise ValueError(f"probing patch/{source}: " + ("; ".join(list(errors)[:3]) or run.stderr.strip()))
        data = obj.read_bytes()
    section = next(s for s in elf_sections(data) if s[0] == ".peek")
    words = list(struct.unpack_from(f"<{section[5] // 4}I", data, section[4]))
    macros = dict(re.findall(r"^#define (\w+) (.*)$", text, re.M))
    return words, peek_layouts(run.stdout), macros


def peek_device(reads, payload=None):
    """The bytes at each (address, size) of demo's memory, short where it isn't mapped; and the
    sha256 of the payload's (address, size) as demo holds it, when asked."""
    script = ["p=$(pidof demo)", '[ -n "$p" ] || { echo none; exit; }', "m=/proc/$p/mem"]
    if payload:
        skip, lead = divmod(payload[0], 4096)
        script.append(f"dd if=$m bs=4096 skip={skip} count={-(-(lead + payload[1]) // 4096)} 2>/dev/null | "
                      f"tail -c +{lead + 1} | head -c {payload[1]} | sha256sum")
    script += [f"dd if=$m bs=1 skip={at} count={n} 2>/dev/null | xxd -p | tr -d '\\n'; echo" for at, n in reads]
    out = shell("sh", ("\n".join(script) + "\n").encode()).decode().splitlines()  # stdin: many reads outgrow 4 KB
    if out[:1] == ["none"]:
        raise ValueError("demo isn't running")
    digest = out.pop(0).split()[0] if payload else None
    if len(out) != len(reads):
        raise ValueError("unexpected reply reading demo's memory")
    return digest, [bytes.fromhex(line) for line in out]


def peek(names, out=None, device=peek_device):
    """Each name's lines, or its error as "name: why", read from demo with out (Q2_BUILD) the build it runs."""
    out = out or os.environ.get("Q2_BUILD")
    if not out:
        raise ValueError("set Q2_BUILD to the --out directory of the build the device runs")
    out = pathlib.Path(out)
    try:
        manifest = json.loads((out / "manifest.json").read_text())
        elf = (out / "patch.elf").read_bytes()
    except (OSError, ValueError) as e:
        raise ValueError(f"{out} isn't a build directory: {e}")
    from build import FLAGS
    flags = [f for f in FLAGS if f not in ("-Oz", "-Wall", "-Wextra", "-Werror")] + [
        "-O0", "-w", f"-DIPOD={int(manifest.get('variant') == 'ipod')}", "-I", str(out)]
    if manifest.get("model") == "Shanling M1 Plus":
        flags.append("-DM1PLUS=1")
    symbols = elf_symbols(elf)
    groups = {}
    for i, name in enumerate(names):
        file, base, first, rest = peek_parse(name)
        groups.setdefault(peek_source(file, base, symbols), []).append((i, base, first, rest))
    plan = {}  # i: [address, -> offsets, size, layout]
    for source, entries in groups.items():
        if not (ROOT / "patch" / source).is_file():
            raise ValueError(f"no patch/{source}")
        words, layouts, macros = peek_compile(source, entries, flags, any(b not in symbols for _, b, _, _ in entries))
        for i, base, first, rest in entries:
            base_size, size, offset, *chain = words[:3 + len(rest)]
            del words[:3 + len(rest)]
            plan[i] = [peek_address(base, source, symbols, macros, base_size, out) + offset, chain, size, layouts[i]]
    loaded = [s for s in elf_sections(elf) if s[1] == 1 and s[2] & 2 and s[5]]  # PROGBITS, SHF_ALLOC
    payload = [min(s[3] for s in loaded), manifest["patch_bytes"]]
    errors = {}
    def fetch(reads):
        digest, data = device(reads, payload)
        if payload:
            if digest != manifest["patch_sha256"]:
                raise ValueError(f"the device doesn't run {out}: its payload differs from that build's")
            payload.clear()
        return data
    level = 0
    while chase := [i for i in plan if i not in errors and len(plan[i][1]) > level]:
        for i, raw in zip(chase, fetch([(plan[i][0], 4) for i in chase])):
            pointer = struct.unpack("<I", raw)[0] if len(raw) == 4 else 0
            if not pointer:
                errors[i] = f"{'NULL' if len(raw) == 4 else 'unreadable'} pointer at 0x{plan[i][0]:08x}"
            plan[i][0] = pointer + plan[i][1][level]
        level += 1
    good = [i for i in sorted(plan) if i not in errors]
    lines = []
    for i, raw in zip(good, fetch([(plan[i][0], plan[i][2]) for i in good]) if good else []):
        address, _, size, node = plan[i]
        if len(raw) < size:
            errors[i] = f"can't read {size} bytes at 0x{address:08x}"
        else:
            plan[i].append(raw)
    for i, name in enumerate(names):
        lines += [f"{name}: {errors[i]}"] if i in errors else peek_lines(name, plan[i][0], plan[i][3], plan[i][4])
    return lines, len(errors)


def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    cmd, a = argv[0], argv[1:]
    timeout = TIMEOUT
    if cmd == "sh" and a[:1] == ["--timeout"] and len(a) == 3:
        timeout, a = float(a[1]), a[2:]
        if timeout <= 0: raise ValueError("--timeout must be positive")
    if cmd == "sh" and len(a) == 1:
        if not a[0]: raise ValueError("sh requires a non-empty command")
        out, rc = run(a[0], timeout)
        sys.stdout.buffer.write(out); return rc
    if cmd == "shot" and len(a) in (1, 2) and a[:-1] in ([], ["--settle"]):
        screenshot(a[-1], len(a) == 2); return 0
    if cmd == "state" and not a:
        print(" ".join(f"{k}={v}" for k, v in state().items())); return 0
    if cmd == "wake" and not a:
        print("woke the screen" if wake() else "the screen is already on"); return 0
    if cmd == "devices" and not a:
        for d in devices():
            print(f"event{d['event']} {d['name']} handlers={d['handlers']} keys={sorted(bits(d['KEY']))} abs={sorted(bits(d['ABS']))}")
        return 0
    if cmd in ("key", "tap", "swipe", "wheel", "knob"):
        if len(a) not in {"key": (1, 2), "wheel": (1, 3), "knob": (1,), "tap": (2, 3), "swipe": (4, 5)}[cmd]:
            raise ValueError(f"invalid arguments for {cmd}")
        input_action(cmd, a); return 0
    if cmd == "peek" and a:
        lines, failed = peek(a)
        print("\n".join(lines))
        return 1 if failed else 0
    if cmd == "push" and len(a) == 2:
        print(push(*a)); return 0
    if cmd == "pull" and len(a) == 2:
        pull(*a); return 0
    if cmd == "install" and len(a) == 1:
        install(a[0])
        print("update.tar is on the card: System settings → System Update → TF card update"); return 0
    if cmd == "log" and len(a) <= 1:
        if a == ["-f"]:
            shell(f"tail -f {LOG}", timeout=None, sink=sys.stdout.buffer); return 0
        if a == ["--clear"]:
            shell(f": >{LOG}"); return 0
        if a and not a[0].isdigit(): raise ValueError("usage: log [LINES|-f|--clear]")
        out, rc = run(f"tail -n {a[0] if a else 100} {LOG}")
        sys.stdout.buffer.write(out); return rc
    if cmd == "find" and not a:
        print("\n".join(find())); return 0
    if cmd == "reboot" and a in ([], ["--wait"]):
        reboot(bool(a)); return 0
    if cmd == "prof" and a and a[0].replace(".", "", 1).isdigit():
        rest, build = a[1:], os.environ.get("Q2_BUILD")
        if "--build" in rest:
            i = rest.index("--build"); build = rest[i + 1]; del rest[i:i + 2]
        profile(float(a[0]), rest == ["--all"], build); return 0
    if cmd == "events" and 1 <= len(a) <= 2:
        try: n = int(a[0]); seconds = float(a[1]) if len(a) > 1 else 5
        except ValueError: raise ValueError("events requires an integer event number and seconds")
        if n < 0 or seconds <= 0 or seconds > 3600: raise ValueError("events requires EVENT>=0 and 0<S<=3600")
        # Device busybox has no timeout(1); the stream may be silent for the whole window.
        out = shell(f"cat /dev/input/event{n} 2>/dev/null & p=$!; sleep {seconds:g}; kill $p", timeout=TIMEOUT + seconds)
        for sec, usec, typ, code, value in decode_events(out):
            print(f"{sec}.{usec:06d} type={typ} code={code} value={value}")
        return 0
    raise ValueError(__doc__[__doc__.index("usage:"):])


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except KeyboardInterrupt:
        sys.exit(130)
    except (ValueError, OSError, RuntimeError) as e:
        print(f"q2remote: {e}", file=sys.stderr)
        sys.exit(2)
