#!/usr/bin/env python3
"""Start an M1 Plus build's demo and V2.1's own, side by side, under qemu-mipsel: the patched one must
come up as stock does. Usage: python3 test/boot.py BUILD [--seconds N] [--captures DIR]

Each runs in a bwrap sandbox (no network, no host files but the Nix store qemu needs) whose root is
that build's rootfs, with V2.1's own dbus-daemon. A preloaded shim (SHIM) gives demo a 320x480
framebuffer backed by a file, and the device's serial; config.ini has the first-boot language set.
So both reach Home. The patched demo must stay up as long as stock, draw the same Home (but the
status bar's clock and battery), and enter the payload through the hooks startup reaches.
Not covered: input (no key or touch arrives), the card, the DAC, GPIO and battery, and the X2000 CPU.
"""
import argparse, bisect, collections, json, pathlib, re, shutil, subprocess, sys, tempfile, time
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]/'tools'))
from build import M1PLUS_HOOKS, WM_PAINT_LEAF_M1PLUS, BASE, SCRATCH, source_sha256, symbols, run

W, H = 320, 480
# The hooks V2.1's startup reaches with no input: Home, the paint and dispatch paths, the UI loop and
# the boot play mode. A payload whose startup never enters them proves nothing.
STARTUP = {'home_page_init', 'widget_dispatch', 'widget_on_paint_border', 'window_manager_paint',
           'main_loop_sleep_default', 'mclSetPlayMode'}

SHIM = r'''
/* /dev/fb0 is FB_FILE, which mmap maps as the device would, answering the fb ioctls for a 32-bit
 * double-buffered W x H screen. The serial (home_page_init: strlen(product_sncode) == 14, else "SN
 * Error" and an early return) is written at SN_ADDR: demo is not PIE. Everything else passes. */
#define RTLD_NEXT ((void *)-1l)
void *dlsym(void *, const char *);
int strcmp(const char *, const char *), ftruncate(int, long);
void *memset(void *, int, unsigned);
static int fb = -1;
static int (*real_open)(const char *, int, int);
static int (*real_ioctl)(int, unsigned long, void *);
enum { LINE = W * 4, SIZE = LINE * H * 2 };
int open(const char *path, int flags, int mode) {
    if (!real_open) real_open = (int (*)(const char *, int, int))dlsym(RTLD_NEXT, "open");
    if (path && !strcmp(path, "/dev/fb0")) {
        fb = real_open(FB_FILE, 0x102 /* MIPS O_RDWR | O_CREAT */, 0644);
        if (fb >= 0) ftruncate(fb, SIZE);
        return fb;
    }
    return real_open(path, flags, mode);
}
int open64(const char *path, int flags, int mode) { return open(path, flags, mode); }
int ioctl(int fd, unsigned long req, void *arg) {
    if (!real_ioctl) real_ioctl = (int (*)(int, unsigned long, void *))dlsym(RTLD_NEXT, "ioctl");
    if (fd != fb || fb < 0) return real_ioctl(fd, req, arg);
    unsigned *u = arg;
    if (req == 0x4600) {  /* FBIOGET_VSCREENINFO: geometry, then the BGRA bitfields */
        memset(arg, 0, 160);
        u[0] = W; u[1] = H; u[2] = W; u[3] = H * 2; u[6] = 32;
        u[8] = 16; u[9] = 8; u[11] = 8; u[12] = 8; u[15] = 8; u[17] = 24; u[18] = 8;
        return 0;
    }
    if (req == 0x4602) {  /* FBIOGET_FSCREENINFO: smem_len, TRUECOLOR, ypanstep, line_length */
        memset(arg, 0, 68);
        u[5] = SIZE; u[8] = 2; ((unsigned short *)arg)[19] = 1; u[11] = LINE;
        return 0;
    }
    if ((req & 0xff00) == 0x4600 || (req & 0xffff) == 0x4620) return 0;  /* put var, pan, blank, vsync */
    return real_ioctl(fd, req, arg);
}
__attribute__((constructor)) static void serial(void) {
    const char sn[] = "EMU0M1PLUS0001";
    for (unsigned i = 0; i < sizeof sn; i++) ((volatile char *)SN_ADDR)[i] = sn[i];
}
'''

INNER = '''cd /
exec 2> /out/inner.err  # bash's notice of the deadline's kill
{qemu} -cpu P5600 -U LD_LIBRARY_PATH /usr/bin/dbus-daemon --config-file=/etc/dbus-1/sandbox.conf --nofork --nopidfile > /out/dbus.log 2>&1 &
for i in $(seq 100); do [ -S /var/run/dbus/system_bus_socket ] && break; sleep 0.1; done
timeout -s KILL {seconds} {qemu} -cpu P5600 {trace} -U LD_LIBRARY_PATH -E LD_PRELOAD=/out/shim.so \\
  -E TSLIB_TSDEVICE=/dev/input/event2 -E TSLIB_CONFFILE=/etc/ts.conf -E TSLIB_PLUGINDIR=/usr/lib/ts \\
  /release/bin/demo > /out/demo.out 2> /out/demo.err
echo $? > /out/exit
'''

def tool(name):
    path = shutil.which(name)
    if not path: raise SystemExit(f'{name} not found: run inside the flake devShell (nix develop)')
    return str(pathlib.Path(path).resolve())

def shim(out, root, sn_addr):
    """SHIM, compiled for V2.1's ABI (o32, nan2008, FR=1) against its own glibc 2.28."""
    src = out/'shim.c'
    src.write_text(f'#define W {W}\n#define H {H}\n#define FB_FILE "/out/fb.raw"\n#define SN_ADDR {sn_addr:#x}u\n' + SHIM)
    run('clang', '--target=mipsel-linux-gnu', '-march=mips32r2', '-mabi=32', '-mfp64', '-mnan=2008', '-mabs=2008', '-fPIC',
        '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-O2', '-Wall', '-Werror', '-c', src, '-o', out/'shim.o')
    run('ld.lld', '-m', 'elf32ltsmip', '-shared', '--hash-style=sysv', '-soname', 'shim.so', out/'shim.o',
        root/'lib/libc-2.28.so', root/'lib/libdl-2.28.so', '-o', out/'shim.so')

def start(image, out, seconds, sn_addr, trace=''):
    """Unpack image as a sandbox root and start dbus-daemon, then demo for seconds; returns the bwrap."""
    root = out/'root'
    run('unsquashfs', '-q', '-no-xattrs', '-d', root, image)
    for d in ('mnt/data', 'mnt/mmc', 'var/run/dbus'): (root/d).mkdir(parents=True, exist_ok=True)
    (root/'mnt/data/config.ini').write_text('[SYSSET]\nLANGUAGE=2\n')  # past the first-boot language choice
    conf = (root/'etc/dbus-1/system.conf').read_text()
    # No other users exist in the sandbox: the bus runs as its caller.
    (root/'etc/dbus-1/sandbox.conf').write_text(re.sub(r'\s*<(user|servicehelper)>[^<]*</\1>', '', conf))
    shim(out, root, sn_addr)
    qemu = tool('qemu-mipsel')
    (out/'inner.sh').write_text(INNER.format(qemu=qemu, seconds=seconds, trace=trace))
    return subprocess.Popen([tool('bwrap'), '--bind', root, '/', '--bind', out, '/out', '--ro-bind', '/nix/store', '/nix/store',
                             '--dev', '/dev', '--proc', '/proc', '--tmpfs', '/tmp', '--unshare-all', '--uid', '0', '--gid', '0',
                             '--die-with-parent', '--new-session', tool('bash'), '/out/inner.sh'])

def screen(out):
    """The page demo shows (the framebuffer's first), as W x H BGRA rows."""
    raw = (out/'fb.raw').read_bytes()
    assert len(raw) == W*H*4*2, f'{out.name}: demo never mapped the framebuffer'
    return raw[:W*H*4]

def executed(log, elf):
    """Payload functions qemu executed, by name, from its -d exec log of the payload's range."""
    funcs = sorted((a, n) for n, a in symbols(elf).items() if BASE <= a < SCRATCH)
    starts = [a for a, _ in funcs]
    hits = collections.Counter()
    for m in re.finditer(rb'Trace \d+: \S+ \[[0-9a-f]+/([0-9a-f]+)/', log.read_bytes()):
        i = bisect.bisect_right(starts, int(m[1], 16)) - 1
        if i >= 0: hits[funcs[i][1]] += 1
    return hits

def png(pixels, path):
    from ipod import imagemagick
    path.write_bytes(imagemagick('-size', f'{W}x{H}', '-depth', '8', 'bgra:-', '-alpha', 'off', 'png:-', data=pixels))

if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('build', type=pathlib.Path)
    ap.add_argument('--seconds', type=int, default=60)
    ap.add_argument('--captures', type=pathlib.Path, help='write stock.png and patched.png here')
    args = ap.parse_args()
    manifest = json.loads((args.build/'manifest.json').read_text())
    if manifest.get('source_sha256') != source_sha256():
        raise SystemExit(f'{args.build}/manifest.json does not match the current sources; rebuild into a fresh directory')
    if manifest['model'] != 'Shanling M1 Plus':
        raise SystemExit('test/boot.py emulates M1 Plus builds only')
    sn_addr = symbols(args.build/'stock-demo')['product_sncode']
    with tempfile.TemporaryDirectory(prefix='m1-boot-') as tmp:
        tmp = pathlib.Path(tmp)
        runs = {}
        for name, image, trace in (('stock', 'stock.squashfs', ''),
                                   ('patched', 'rootfs.squashfs', f'-d exec,nochain -dfilter {BASE:#x}+{SCRATCH-BASE:#x} -D /out/exec.log')):
            (tmp/name).mkdir()
            runs[name] = start(args.build/image, tmp/name, args.seconds, sn_addr, trace)
        for p in runs.values(): p.wait(timeout=args.seconds + 120)
        for name in runs:
            out = tmp/name
            status = int((out/'exit').read_text())
            err = (out/'demo.err').read_bytes()
            # Killed at the deadline (137) is the only good end: demo never returns by itself on the device.
            assert status == 137 and b'uncaught target signal' not in err, (
                f'{name} demo ended early ({status}): {err[-600:].decode("latin-1")}')
        stock, patched = screen(tmp/'stock'), screen(tmp/'patched')
        if args.captures:
            args.captures.mkdir(parents=True, exist_ok=True)
            png(stock, args.captures/'stock.png'); png(patched, args.captures/'patched.png')
        # Stock reached Home (not a blank page, "SN Error" or the language guide): its pages' dots.
        assert len(set(stock[i:i+4] for i in range(0, len(stock), 4))) > 50, 'stock demo drew no Home'
        bar = 30 * W * 4  # the status bar, whose clock and battery change from run to run
        differ = [i // 4 for i in range(bar, len(stock), 4) if stock[i:i+4] != patched[i:i+4]]
        assert not differ, f'patched Home differs from stock at {len(differ)} pixels, first (x, y) {divmod(differ[0], W)[::-1]}'
        hits = executed(tmp/'patched'/'exec.log', args.build/'patch.elf')
        hooks = {stock_name: replacement for stock_name, (_, replacement, _) in M1PLUS_HOOKS.items()}
        hooks[WM_PAINT_LEAF_M1PLUS[0]] = WM_PAINT_LEAF_M1PLUS[2]
        reached = {n for n, r in hooks.items() if hits[r]}
        assert STARTUP <= reached, f'startup never entered {sorted(STARTUP - reached)}'
    print(f'M1 Plus startup under qemu: both demos up for {args.seconds} s, the same Home below the status bar; '
          f'the payload entered through {len(reached)} hooks ({", ".join(sorted(reached))}), {len(hits)} payload functions ran.')
