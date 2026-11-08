#!/usr/bin/env python3
"""Start an M1 Plus build's demo and V2.1's own, side by side, under qemu-mipsel: the patched one must
come up as stock does. Usage: python3 test/m1plus/boot.py BUILD [--seconds N] [--captures DIR]

Each runs in a bwrap sandbox (no network, no host files but the Nix store qemu needs) whose root is
that build's rootfs, with V2.1's own dbus-daemon. A preloaded shim (SHIM) gives demo a 320x480
framebuffer backed by a file, and the device's serial; config.ini has the first-boot language set.
So both reach Home: stock its grid, the patched demo the iPod Home (ipod-ui 4.5), which the harness checks for itself:
the art panel and the list's rows in Split, the rows from the top in Full, the selection on Now Playing. The patched
demo must stay up as long as stock and enter the payload through the hooks startup reaches; stock is the control.

Then the patched demo takes the input of WALK: touches (the shim stands in for tslib, as the touchscreen's samples)
and keys (the buttons' and knob's devices, /dev/input/event1 and event2, are FIFOs the harness writes Linux key events
to): Home's Settings list, System Setting, About, Playback Setting and its EQ, Display and the slider pages, where the
chevron (and Previous, in Knob: Navigation) goes back, and the payload's back button must close its EQ and Previous
must not; the Library and Streaming from Home's rows, by touch and by the knob. With --home-menu, a saved V2.1 Home
card selection must change nothing: the control is the same build without it.
Not covered: the card, the DAC, GPIO and battery, and the X2000 CPU.
"""
import argparse, bisect, collections, json, os, pathlib, re, shutil, struct, subprocess, sys, tempfile, time
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]/'tools'))
from build import BASE, SCRATCH, fileoff, source_sha256, symbols, run
from m1plus import M1PLUS_GP, M1PLUS_HOOKS, WM_PAINT_LEAF_M1PLUS
from m1plus_ipod import M1
# Each accent's selection top (patch/m1plus_offsets.inc ACCENTS, { top, bottom, light, red, highlight } a row)
ACCENT_TOPS = [int(r, 16) for r in re.findall(r'\{ 0x([0-9a-fA-F]{6}),', (pathlib.Path(__file__).resolve().parents[2]/'patch/m1plus_offsets.inc')
                                                    .read_text().split('#define ACCENTS', 1)[1].split('\n\n', 1)[0])]
BAR_BACK_W, BAR_BACK_HIT_W, STATUS_H = M1['BAR_BACK_W'], M1['BAR_BACK_HIT_W'], M1['STATUS_H']

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
static int (*real_access)(const char *, int);
/* The buttons' (md-gpio-keys) and knob's (md-rotary-knob) devices, as main_loop_init names them:
 * FIFOs the harness writes struct input_event to. The readers only read() them (0x637870, 0x637e70). */
static const char *key_file(const char *path) {
    if (!path) return 0;
    if (!strcmp(path, "/dev/input/event1")) return KEYS_FILE;
    if (!strcmp(path, "/dev/input/event2")) return KNOB_FILE;
    return 0;
}
int access(const char *path, int mode) {
    if (!real_access) real_access = (int (*)(const char *, int))dlsym(RTLD_NEXT, "access");
    return key_file(path) ? 0 : real_access(path, mode);
}
static int (*real_ioctl)(int, unsigned long, void *);
enum { LINE = W * 4, SIZE = LINE * H * 2 };
int open(const char *path, int flags, int mode) {
    if (!real_open) real_open = (int (*)(const char *, int, int))dlsym(RTLD_NEXT, "open");
    if (path && !strcmp(path, "/dev/fb0")) {
        fb = real_open(FB_FILE, 0x102 /* MIPS O_RDWR | O_CREAT */, 0644);
        if (fb >= 0) ftruncate(fb, SIZE);
        return fb;
    }
    if (key_file(path)) return real_open(key_file(path), 2 /* O_RDWR: a FIFO's open never waits */, 0);
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
/* tslib (V2.1's 0.0 API; tslib_run reads one sample at a time): samples from TOUCH_FILE, which the
 * harness appends to. Lines: "x y pressure" (0 lifts the finger), or "wait ms". ts_read blocks for one. */
struct ts_sample { int x, y; unsigned pressure; struct { long sec, usec; } tv; };
int gettimeofday(void *, void *), nanosleep(const void *, void *), read(int, void *, unsigned);
static int touch_fd = -1;
static char tbuf[256];
static unsigned tlen;
/* "net 1" holds V2.1's network status (the word networkGetConnectStatus returns, NET_ADDR) at connected, as the
 * touch thread waits, until "net 0" clears it: the sandbox has no network, and Tidal and HiFi Music open only with one. */
static int net;
static void nap(long ms) { long t[2] = { ms / 1000, ms % 1000 * 1000000 }; nanosleep(t, 0); }
void *ts_open(const char *dev, int nonblock) { (void)dev; (void)nonblock; static int ts; return &ts; }
int ts_config(void *ts) { (void)ts; return 0; }
int ts_close(void *ts) { (void)ts; return 0; }
static void next_line(char *line) {
    for (;;) {
        if (net) *(volatile int *)NET_ADDR = 1;
        for (unsigned i = 0; i < tlen; i++)
            if (tbuf[i] == '\n') {
                for (unsigned j = 0; j < i; j++) line[j] = tbuf[j];
                line[i] = 0;
                for (unsigned j = i + 1; j < tlen; j++) tbuf[j - i - 1] = tbuf[j];
                tlen -= i + 1;
                return;
            }
        if (touch_fd < 0) {
            if (!real_open) real_open = (int (*)(const char *, int, int))dlsym(RTLD_NEXT, "open");
            touch_fd = real_open(TOUCH_FILE, 0, 0);
        }
        int n = touch_fd >= 0 && tlen < sizeof tbuf ? read(touch_fd, tbuf + tlen, sizeof tbuf - tlen) : 0;
        if (n > 0) tlen += n;
        else nap(20);
    }
}
static int num(const char **p) {
    int v = 0, sign = 1;
    while (**p == ' ') ++*p;
    if (**p == '-') sign = -1, ++*p;
    while (**p >= '0' && **p <= '9') v = v * 10 + *(*p)++ - '0';
    return sign * v;
}
int ts_read(void *ts, struct ts_sample *s, int nr) {
    (void)ts, (void)nr;
    char line[256];
    for (;;) {
        next_line(line);
        const char *p = line;
        if (line[0] == 'w') { p += 4; nap(num(&p)); continue; }
        if (line[0] == 'n') { p += 4; net = num(&p); *(volatile int *)NET_ADDR = net; continue; }
        s->x = num(&p); s->y = num(&p); s->pressure = num(&p);
        gettimeofday(&s->tv, 0);
        return 1;
    }
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

def shim(out, root, sn_addr, net_addr):
    """SHIM, compiled for V2.1's ABI (o32, nan2008, FR=1) against its own glibc 2.28."""
    src = out/'shim.c'
    src.write_text(f'#define W {W}\n#define H {H}\n#define FB_FILE "/out/fb.raw"\n#define TOUCH_FILE "/out/touch"\n'
                   f'#define KEYS_FILE "/out/keys"\n#define KNOB_FILE "/out/knob"\n#define SN_ADDR {sn_addr:#x}u\n'
                   f'#define NET_ADDR {net_addr:#x}u\n' + SHIM)
    run('clang', '--target=mipsel-linux-gnu', '-march=mips32r2', '-mabi=32', '-mfp64', '-mnan=2008', '-mabs=2008', '-fPIC',
        '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-O2', '-Wall', '-Werror', '-c', src, '-o', out/'shim.o')
    run('ld.lld', '-m', 'elf32ltsmip', '-shared', '--hash-style=sysv', '-soname', 'shim.so', out/'shim.o',
        root/'lib/libc-2.28.so', root/'lib/libdl-2.28.so', '-o', out/'shim.so')

# The iPod theme's default is Minimal, whose greys recolour the icons' edges: both runs use Classic with Crimson (the
# stock red), which leaves a stock colour as it was, so a page that differs from stock differs by a change of layout.
IPOD_CLASSIC = '[IPOD]\nTHEME=1\nACCENT=1\n'
# The iPod Home (ipod-ui 4.5): the plain and --home-menu walks lay it out Full (HOME=1), the media walk Split (0).
HOME_FULL, HOME_SPLIT = 'HOME=1\n', 'HOME=0\n'

CARD_KNOB = 1  # Knob: Navigation with a card (start); a review sheet may want the volume
def net_address(build):
    """The word the shim's "net" lines set: V2.1's network flag, as networkGetConnectStatus reads it
    (lw v0, -0x7f4c(gp); jr ra; lw v0, -0x53c8(v0))."""
    stock_demo = (build/'stock-demo').read_bytes()
    at = fileoff(stock_demo, symbols(build/'stock-demo')['networkGetConnectStatus'])
    assert struct.unpack_from('<3I', stock_demo, at + 12) == (0x8f8280b4, 0x03e00008, 0x8c42ac38), 'networkGetConnectStatus'
    return struct.unpack_from('<I', stock_demo, fileoff(stock_demo, M1PLUS_GP - 0x7f4c))[0] - 0x53c8


def start(image, out, seconds, sn_addr, net_addr, trace='', home_menu='', card=None, home=HOME_FULL):
    """Unpack image as a sandbox root and start dbus-daemon, then demo for seconds; returns the bwrap.
    With card, a directory mounted as the card, and V2.1's library database listing its songs."""
    root = out/'root'
    run('unsquashfs', '-q', '-no-xattrs', '-d', root, image)
    for d in ('mnt/data', 'mnt/mmc', 'var/run/dbus'): (root/d).mkdir(parents=True, exist_ok=True)
    if card: media_db(root/'mnt/data/database.db')
    # Past the first-boot language choice; with home_menu, V2.1's Home cards ([MAIN] HOMEMENU, ids each
    # followed by |, as saveHomemenu 0x4d7940 writes them).
    # Knob: Volume, so the walk starts on V2.1's own knob; it turns Knob: Navigation on itself (patch.py has the default).
    # The media walk's Library steps go back and hold with Previous, so it starts in Navigation (the M1's default).
    (root/'mnt/data/config.ini').write_text(f'[SYSSET]\nLANGUAGE=2\n[Q2POD]\nKNOB={CARD_KNOB if card else 0}\n' + IPOD_CLASSIC + home + (f'[MAIN]\nHOMEMENU={home_menu}\n' if home_menu else ''))
    conf = (root/'etc/dbus-1/system.conf').read_text()
    # No other users exist in the sandbox: the bus runs as its caller.
    (root/'etc/dbus-1/sandbox.conf').write_text(re.sub(r'\s*<(user|servicehelper)>[^<]*</\1>', '', conf))
    shim(out, root, sn_addr, net_addr)
    (out/'touch').write_text('')
    for fifo in ('keys', 'knob'): os.mkfifo(out/fifo)
    qemu = tool('qemu-mipsel')
    (out/'inner.sh').write_text(INNER.format(qemu=qemu, seconds=seconds, trace=trace))
    return subprocess.Popen([tool('bwrap'), '--bind', root, '/', *(['--bind', card, '/mnt/mmc'] if card else []),
                             '--bind', out, '/out', '--ro-bind', '/nix/store', '/nix/store',
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

WALK_SECONDS = 260  # the walk's budget after startup, inside the same run

def tap(x, y): return [f'{x} {y} 200', 'wait 80', f'{x} {y} 0']
def swipe(x0, y0, x1, y1, steps=10):
    return [line for i in range(steps + 1) for line in (f'{x0 + (x1 - x0) * i // steps} {y0 + (y1 - y0) * i // steps} 200', 'wait 16')] + [f'{x1} {y1} 0']
NEXT_PAGE = swipe(280, 250, 40, 250)  # Home's carousel, a page right
DOWN_LIST = swipe(160, 420, 160, 60)  # a list scrolled towards its end
UP_LIST = swipe(160, 100, 160, 460)    # and back towards its start
# The iPod settings rows (ipod-ui 4.3): SET_ROWS rows of SET_ROW, in Classic (the walk's theme) flush under the bar, the
# same whether the list is at its start or scrolled to its end. V2.1's title bar is hidden there: the chevron and
# Previous are the backs.
def set_row(i): return tap(160, STATUS_H + M1['SET_ROW'] * i + M1['SET_ROW'] // 2)
def set_band(i): return (STATUS_H + M1['SET_ROW'] * i, STATUS_H + M1['SET_ROW'] * (i + 1))
CHEVRON_EDGE = tap(BAR_BACK_HIT_W - 4, STATUS_H // 2)  # its tap's far edge, past the image (BAR_BACK_W)
NP_BACK = tap(M1['NP_BACK_W'] // 2, STATUS_H + M1['NP_TOP_H'] // 2)  # Now Playing's large back (ipod-ui 4.6): the page has no chevron
CHEVRON = tap(BAR_BACK_W // 2, STATUS_H // 2)  # the status bar's back chevron: the payload's pages' only back (ipod-ui 4.2),
                                               # and V2.1's pages' too, which previous_back clicks the button of
# Keys, as Linux reports them (keyboard_gpio_add.sh, keyboard_encoder): "keys CODE" on the buttons'
# device, "knob CODE" on the knob's; each a press and a release.
PREVIOUS, KNOB_UP = 'keys 165', 'knob 115'  # KEY_PREVIOUSSONG, KEY_VOLUMEUP
KNOB_DOWN, PRESS = 'knob 114', 'keys 116'   # KEY_VOLUMEDOWN, and the knob's press, KEY_POWER
# (name, touches for both, seconds to settle, expectation): 'same', stock's below the status bar;
# ('rows', same, differ), the y bands that match stock's and that must not; 'differs'; ('as', step),
# the patched screen as it was at that step; ('not', step, ...), unlike it at each of those steps;
# ('as', step, same, differ), as at that step in the y band same and unlike it in differ; or ('kept',
# step, box): unlike that step, but the box (x0, y0, x1, y1, the status bar's included) as it was then;
# ('still', step, box): as at that step, the box too.
# Positions are V2.1's 320x480 layout, the settings pages' the iPod rows' (set_row).
# The iPod Home (ipod-ui 4.5) in Classic: its rows HOME_ROW apart from the window's top in Full, under the art
# (HOME_ART_H) in Split; Home's Settings list takes the menu's place, its rows where the menu's are.
HOME_ROW, HOME_ART_H = M1['HOME_ROW'], M1['HOME_ART_H']
NOW, LIBRARY, COVERFLOW, FOLDER, SHORTCUT, STREAMING, SETTINGS = range(7)
PLAYBACK, SYSTEM = range(2)
def home_y(i, split=False, scroll=0): return STATUS_H + (HOME_ART_H if split else 0) + HOME_ROW * i - scroll + HOME_ROW // 2
def home_row(i, split=False, scroll=0): return tap(160, home_y(i, split, scroll))
WALK = [('settings', home_row(SETTINGS), 4, ('not', 'home')),  # its Playback and System rows, the chevron shown
        ('sysset', home_row(SYSTEM), 4, ('not', 'settings')),  # the iPod settings rows
        # System Setting in the iPod order (m1plus_nav_sysset.c): its end is System Update, Reset, Formatting Card and
        # About, the last row.
        ('sysset_end', DOWN_LIST + ['wait 800'] + DOWN_LIST, 4, ('not', 'sysset')),
        ('about', set_row(5), 4, ('not', 'sysset_end')),
        # Back twice, Home's Settings list again, System (tapped) chosen.
        ('settings_again', CHEVRON + ['wait 2500'] + CHEVRON, 5, ('not', 'settings', 'about')),
        ('playset', home_row(PLAYBACK), 4, ('not', 'settings_again')),
        # The knob turns the volume (Knob: Volume): the iPod bar draws no figure (V2.1's img_volume and label_volume
        # stay transparent), the chevron and the play state as they were.
        ('knob', [KNOB_UP, KNOB_UP], 3, ('still', 'playset', (0, 0, 60, 30))),
        ('eq', set_row(2), 5, ('not', 'playset')),  # the PEQ editor in stock's EQ page
        ('eq_closed', CHEVRON, 4, ('as', 'playset')),  # the PEQ's back: the chevron; stock's EQ page has its own button
        ('eq_again', set_row(2), 5, ('as', 'eq')),
        ('eq_previous', [PREVIOUS], 4, ('as', 'eq')),  # Previous is a media key, not Back: the PEQ stays
        # Back steps back one screen: Advanced's Preamp row, then Back to Advanced, then out.
        ('advanced', tap(250, 53), 4, ('not', 'eq')),           # the tab bar's right half
        ('preamp', tap(160, 414), 4, ('not', 'advanced')),      # the fifth row, after 1.3.8's Reset to defaults
        ('preamp_back', CHEVRON, 4, ('not', 'preamp', 'playset')),
        ('advanced_back', CHEVRON, 4, ('as', 'playset')),
        ('playset_end', (DOWN_LIST + ['wait 800']) * 3 + DOWN_LIST, 4, ('not', 'playset')),
        ('crossfade', set_row(0), 4, ('not', 'playset_end')),  # the first row at the end, MQA the last
        ('crossfade_slid', tap(230, 197), 4, ('not', 'crossfade')),  # its slider, up the hidden title bar's 50 px
        # Back: the list as before (the rows V2.1 rebuilds, then ours again), Crossfade's row now 11 s. Resume Songs'
        # label (row 2) is wider than its row and scrolls, so the rows compared are the last three.
        ('crossfade_back', CHEVRON, 4, ('as', 'playset_end', (set_band(3)[0], 480), set_band(0))),
        # Back at its top before leaving, so Playback Setting's reopening (which glides to its remembered row) starts there.
        ('playset_top', (UP_LIST + ['wait 800']) * 4, 4, ('not', 'crossfade_back')),
        # Display's Knob: Navigation. The knob's turns then move System Setting's selection
        # (its outline drawn), and the volume, in the status bar, stays as it was.
        ('knob_home', CHEVRON, 5, ('as', 'settings')),  # Playback Setting closes to Home's Settings list
        ('knob_sysset', home_row(SYSTEM) + ['wait 2000'] + (UP_LIST + ['wait 800']) * 2, 4, ('as', 'sysset')),
        ('display', set_row(2), 4, ('not', 'knob_sysset')),  # Wireless, Network Service, then Display
        # Lock screen: switched on, V2.1's grid shows its pictures, the built-ins drawn, in
        # the payload's scroll view; scrolled to its end, Time show, Clock and About. Switched
        # off again, then the chevron returns to Display: on V2.1's pages it clicks their own back
        # button (previous_back), which knob_home and display_back tap.
        ('lockscreen', set_row(2), 4, ('not', 'display')),  # it keeps its title bar, which holds its switch
        ('lockscreen_on', tap(221, 53), 4, ('not', 'lockscreen')),
        ('lockscreen_end', DOWN_LIST, 4, ('not', 'lockscreen_on')),
        ('lockscreen_off', tap(221, 53), 4, ('as', 'lockscreen')),
        ('lockscreen_back', CHEVRON, 4, ('as', 'display')),
        # Display's end: V2.1's rows, then Appearance, Coverflow and Controls (ipod-ui 4.3), the last row. Controls
        # holds Shortcut (4.5), Smart Awake, Hold Return, then the knob's two rows; Knob becomes Navigation once tapped.
        ('display_end', DOWN_LIST + ['wait 800'], 4, ('not', 'lockscreen_back')),
        ('controls', set_row(5), 4, ('not', 'display_end')),
        ('knob_row', set_row(3), 3, ('as', 'controls', (30, set_band(3)[0]), set_band(3))),
        ('controls_back', CHEVRON, 4, ('as', 'display_end')),
        ('display_back', CHEVRON_EDGE, 4, ('as', 'knob_sysset')),
        ('knob_nav', [KNOB_UP, KNOB_UP], 3, ('kept', 'display_back', (0, 0, 60, 30))),
        # With Knob: Navigation, Previous is Back: System Setting closes to Home's Settings list, Previous closes that
        # (ipod-ui 4.5) to the main list, the chevron gone, and there it stays Previous track (nothing plays).
        ('previous_back', [PREVIOUS], 4, ('as', 'settings_again')),
        ('previous_settings', [PREVIOUS], 4, ('not', 'previous_back')),
        ('previous_home', [PREVIOUS], 4, ('as', 'previous_settings')),
        # V2.1's slider pages keep the knob's volume (no context) but Previous goes back there too: Max
        # Volume and Default Vol (bootvol_page, Crossfade's page too). On V039m it stayed a media key there.
        # Playback Setting reopens where its list was left (playset_top): at its start, Max Volume the fifth row.
        ('slider_playset', home_row(SETTINGS) + ['wait 1500'] + home_row(PLAYBACK) + ['wait 2000'],
         4, ('not', 'previous_home')),
        ('maxvol', set_row(4), 4, ('not', 'slider_playset')),
        ('maxvol_previous', [PREVIOUS], 4, ('as', 'slider_playset')),
        ('bootvol', set_row(5), 4, ('not', 'slider_playset', 'maxvol')),
        ('bootvol_previous', [PREVIOUS], 4, ('as', 'slider_playset')),
        ('slider_home', [PREVIOUS] + ['wait 1500'] + [PREVIOUS], 4, ('as', 'previous_home')),
        # Home's Library row opens the Library (rows of 64 px under the 48 px title bar); its Shuffle row opens Shuffle,
        # which the chevron closes. Previous (Knob: Navigation) closes the Library, and so does the chevron.
        ('library', home_row(LIBRARY), 4, ('not', 'previous_home')),
        ('library_shuffle', tap(160, 110), 4, ('not', 'library')),
        ('library_shuffle_back', CHEVRON, 4, ('as', 'library')),
        ('library_previous', [PREVIOUS], 4, ('not', 'library')),
        ('library_again', home_row(LIBRARY), 4, ('as', 'library')),
        ('library_back', CHEVRON, 4, ('as', 'library_previous')),
        # Knob: Navigation on Home's rows: four turns from Library to Streaming, the press opens it, Previous closes it.
        ('home_knob', [KNOB_DOWN] * 4, 3, ('not', 'library_back')),
        ('home_knob_open', [PRESS], 4, ('not', 'home_knob')),
        ('home_knob_back', [PREVIOUS], 4, ('as', 'home_knob'))]
# --home-menu: V2.1's Home cards saved ([MAIN] HOMEMENU, six cards from My Music to Composer), which the iPod Home
# replaces: the control is the same build without them, and both must draw the same Home and pages: the Library from
# Home's row, closed by the chevron; Home's Settings list, closed by its chevron.
HOME_MENU = '3|4|5|6|7|8|'
MENU_WALK = [('menu_library', home_row(LIBRARY), 4, 'same'),
             ('menu_back', CHEVRON, 4, 'same'),
             ('menu_settings', home_row(SETTINGS), 4, 'same'),
             ('menu_settings_back', CHEVRON, 4, 'same')]

# --media: a card with two 11-minute songs, a book and two photos, and V2.1's songtable listing the
# songs as its scan writes them (time and time_end 0: not CUE tracks). The card is on a tmpfs: on
# ext4, a 32-bit guest's readdir under qemu-user fails on 64-bit directory offsets (EOVERFLOW), so
# the payload would find it empty. The walk, patched only: Long Songs measures and lists both songs;
# a tap opens the book and the photo (a hidden reader or viewer must not take it); a swipe moves to
# the next photo and back; Spotify and Internet Radio open from their rows; Coverflow's covers (each song an album
# of its own: since 1.4.5 the ring is the albums alone) turn by swipe and open by a tap on the centre cover;
# Shuffle Songs saves stock's Shuffle play mode.
LONG_S = 660
MEDIA_SONGS = ('long.flac', 'long.mp3')
def media_card(card):
    """The card's files. TagLib reads a length from the headers alone: a FLAC STREAMINFO counting
    LONG_S of samples, and an MP3 whose Xing frame counts LONG_S of frames."""
    rate = 44100
    info = struct.pack('>HH', 4096, 4096) + bytes(6) + ((rate << 44) | (1 << 41) | (15 << 36) | LONG_S * rate).to_bytes(8, 'big') + bytes(16)
    (card/'Music').mkdir()
    (card/'Music/long.flac').write_bytes(b'fLaC\x80' + len(info).to_bytes(3, 'big') + info + bytes(8192))
    frames, size, head = LONG_S * rate // 1152, 144 * 128000 // rate, bytes((0xff, 0xfb, 0x90, 0x64))
    xing = head + bytes(32) + b'Xing' + struct.pack('>III', 3, frames, frames * size)
    (card/'Music/long.mp3').write_bytes(xing + bytes(size - len(xing)) + (head + bytes(size - 4)) * 50)
    (card/'Books').mkdir()
    (card/'Books/Alpha.txt').write_text('A short book.\n' * 200)
    (card/'Photos').mkdir()
    from ipod import imagemagick
    (card/'Photos/one.jpg').write_bytes(imagemagick('-size', '200x150', 'gradient:red-blue', 'jpg:-', data=b''))
    (card/'Photos/two.jpg').write_bytes(imagemagick('-size', '200x150', 'gradient:green-yellow', 'jpg:-', data=b''))

def media_db(path):
    import sqlite3
    db = sqlite3.connect(path)
    # V2.1's own create statement (its demo's strings)
    db.execute('create table songtable(id INTEGER PRIMARY KEY, filename VARCHAR(512), fileurl VARCHAR(1024), '
               'album VARCHAR(512), songer VARCHAR(256), style VARCHAR(128), name VARCHAR(512), composer VARCHAR(256), '
               'albumsonger VARCHAR(256), year INTEGER, track INTEGER, cd_num INTEGER, time INTEGER, time_end INTEGER, '
               'time_create INTEGER, Initial INTEGER, bitdepth INTEGER, samprate INTEGER)')
    for i, n in enumerate(MEDIA_SONGS):
        db.execute('insert into songtable values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
                   (i + 1, n, f'/mnt/mmc/Music/{n}', ('Long', 'Longer')[i], 'Tester', '', f'Long {n}', '', 'Tester', 2024, i + 1, 1,
                    0, 0, 0, 0, 16, 44100))
    db.commit()
    db.close()

# The Library page's rows (patch/m1plus_nav_library.c), 64 px under the 48 px title, upstream's order with V2.1's
# categories: Shuffle, Artists, Albums, All Songs, Genres, Era, Playlists, Ratings, Recently Added, Recently Played,
# Most Played, Frequent, Hi-Res, Long Songs, then the card's Photos and Books, Composers, CD Ripper and Update Local
# Music: 19 rows, six showing. A slow drag held before its release scrolls by its length (no fling), from y 420 (a touch
# lower is V2.1's swipe up to Home): two of DRAG_PX bring Most Played to the top. Tap row centres: a settling scroll
# must not pick the row above.
LIB_ROWS, LIB_LIST_Y, LIB_LIST_H, DRAG_PX = 19, STATUS_H + 48, H - STATUS_H - 48, 320
def drag(x, y0, y1, steps=20):
    return [line for i in range(steps + 1) for line in (f'{x} {y0 + (y1 - y0) * i // steps} 200', 'wait 24')] + ['wait 600', f'{x} {y1} 0']
def page_row(i, scroll=0): return tap(160, LIB_LIST_Y + 64 * i - scroll + 32)
MID = 2 * DRAG_PX
# The Library (ipod-ui 4.4) and V2.1's library lists, from Home's rows in Split (the art above them): V2.1's lists
# without their title bar, in LIB_PITCH rows from the top; each closes by the chevron or Previous (Knob: Navigation, the
# M1's default). On an album's tracks, Previous held (V2.1's key-long, after 1000 ms) opens Now Playing, and so does
# the chevron held (LONG_PRESS_MS); Now Playing's own back button goes back to the list. Home's list shows four rows under the
# art: a fling to its end (HOME_END px on) brings Streaming and Settings up.
LIB_PITCH = M1['LIB_PITCH']
HOME_END = 7 * HOME_ROW - (H - STATUS_H - HOME_ART_H)
def lib_row(i): return tap(160, STATUS_H + LIB_PITCH * i + LIB_PITCH // 2)
CHEVRON_HOLD = [f'{BAR_BACK_W // 2} {STATUS_H // 2} 200', f'wait {M1["LONG_PRESS_MS"] + 400}', f'{BAR_BACK_W // 2} {STATUS_H // 2} 0']
LIBRARY_WALK = [('lib', home_row(LIBRARY, True), 5, ('not', 'home')),
                ('lib_songs', page_row(3), 5, ('not', 'lib')),
                ('lib_songs_back', CHEVRON, 4, ('as', 'lib')),
                ('lib_artists', page_row(1), 5, ('not', 'lib')),
                ('lib_artists_back', CHEVRON, 4, ('as', 'lib')),
                ('lib_albums', page_row(2), 5, ('not', 'lib')),
                ('lib_album', lib_row(0), 5, ('not', 'lib_albums')),  # the first album's tracks
                ('lib_hold', [f'hold {PREVIOUS} 1400'], 5, ('not', 'lib_album')),
                ('lib_hold_back', NP_BACK, 5, ('as', 'lib_album')),
                ('lib_chevron_hold', CHEVRON_HOLD, 5, ('not', 'lib_album')),
                ('lib_chevron_back', NP_BACK, 5, ('as', 'lib_album')),
                ('lib_album_back', [PREVIOUS], 4, ('as', 'lib_albums')),
                ('lib_albums_back', CHEVRON, 4, ('as', 'lib'))]
LOGIN_BACK = tap(50, STATUS_H + 25)  # V2.1's login pages' back button, its title bar's first 80 px, clear of the edge
# Streaming's logins, from its page (MEDIA_WALK): with the network up (the shim's "net 1") and no login stored, Tidal's
# row opens its login page in its main page's place, and HiFi Music's page replaces itself with its own, its account
# field focused under AWTK's keyboard. Back from either, by the chevron, Previous or the page's own back button, is
# Streaming again (V04Hm's went Home; on HiFi's, the chevron and Previous were a Return in the keyboard).
LOGIN_WALK = [('tidal', ['net 1'] + page_row(0), 6, ('not', 'streaming')),
              ('tidal_back', CHEVRON, 4, ('as', 'streaming')),
              ('tidal_again', page_row(0), 6, ('not', 'streaming')),
              ('tidal_previous', [PREVIOUS], 4, ('as', 'streaming')),
              ('tidal_third', page_row(0), 6, ('not', 'streaming')),
              ('tidal_button', LOGIN_BACK, 4, ('as', 'streaming')),
              ('hifi', page_row(1), 8, ('not', 'streaming', 'tidal')),
              ('hifi_back', CHEVRON, 4, ('as', 'streaming')),
              ('hifi_again', page_row(1), 8, ('not', 'streaming')),
              ('hifi_previous', [PREVIOUS], 4, ('as', 'streaming')),
              ('hifi_third', page_row(1), 8, ('not', 'streaming')),
              ('hifi_button', LOGIN_BACK + ['net 0'], 4, ('as', 'streaming'))]
MEDIA_WALK = LIBRARY_WALK + [
              # At the Library's top, a pull opens V2.1's search (4.4).
              ('lib_search', UP_LIST, 4, ('not', 'lib')),
              ('lib_search_back', CHEVRON, 4, ('as', 'lib')),
              ('era', page_row(5), 4, ('not', 'lib')),
              ('era_decade', tap(160, 110), 4, ('not', 'era')),
              ('era_decade_back', CHEVRON, 4, ('as', 'era')),
              ('era_back', CHEVRON, 4, ('as', 'lib')),
              ('shuffle', page_row(0), 4, ('not', 'lib')),
              ('shuffle_back', CHEVRON, 4, ('as', 'lib')),
              ('lib_mid', drag(160, 420, 420 - DRAG_PX) + ['wait 800'] + drag(160, 420, 420 - DRAG_PX), 4, ('not', 'lib')),
              ('long_songs', page_row(13, MID), 12, ('not', 'lib_mid')),  # measures, then lists
              ('long_songs_back', CHEVRON, 4, ('as', 'lib_mid')),
              ('photos', page_row(14, MID), 6, ('not', 'lib_mid')),
              ('photo', tap(56, 126), 5, ('not', 'photos')),         # the first tile
              # qemu's demo decodes neither photo ("Can't open this photo"), so the move to the
              # second and back shows only in the trace (photos.c moved); the viewer stays open.
              ('photo_swipes', swipe(240, 250, 60, 250) + ['wait 1500'] + swipe(60, 250, 240, 250), 4, ('as', 'photo')),
              ('photo_back', CHEVRON, 4, ('not', 'photo')),
              ('photos_back', CHEVRON, 4, ('as', 'lib_mid')),
              ('books', page_row(15, MID), 4, ('not', 'lib_mid')),
              ('book', tap(160, 110), 5, ('not', 'books')),          # the first book's row
              ('book_back', CHEVRON, 4, ('not', 'book')),
              ('books_back', CHEVRON, 4, ('as', 'lib_mid')),
              ('lib_closed', CHEVRON, 4, ('not', 'lib_mid', 'home')),  # Home, its Library row chosen
              # Home's Folder row: V2.1's Folder view, closed by Previous.
              ('folder', home_row(FOLDER, True), 5, ('not', 'lib_closed')),
              ('folder_back', [PREVIOUS], 4, ('not', 'folder', 'lib_closed')),
              ('coverflow', home_row(COVERFLOW, True), 10, ('not', 'folder_back')),
              ('cover_next', swipe(220, 150, 120, 150), 4, ('not', 'coverflow')),  # one cover: the second album
              ('cover_prev', swipe(120, 150, 220, 150), 4, ('as', 'coverflow')),
              ('cover_open', tap(160, 120), 5, ('not', 'coverflow')),               # the centre cover's tracks
              ('cover_back', CHEVRON, 4, ('as', 'coverflow')),
              ('coverflow_back', CHEVRON, 4, ('not', 'coverflow', 'folder_back')),
              # Home's list, flung to its end: Streaming's row opens its page: native Tidal and HiFi Music, Spotify,
              # Internet Radio, AirPlay and Configuration. Spotify, not on the card, says so on its Now Playing page;
              # Internet Radio opens its menu. Each closes with the chevron.
              ('home_end', DOWN_LIST, 4, ('not', 'coverflow_back')),
              ('streaming', home_row(STREAMING, True, HOME_END), 4, ('not', 'home_end')),
              ('spotify', page_row(2), 4, ('not', 'streaming')),
              ('spotify_back', NP_BACK, 4, ('as', 'streaming')),
              ('radio', page_row(3), 5, ('not', 'streaming')),
              ('radio_back', CHEVRON, 4, ('as', 'streaming')),
              ('configuration', page_row(5), 4, ('not', 'streaming')),
              ('configuration_back', CHEVRON, 4, ('as', 'streaming')),
             ] + LOGIN_WALK + [
              # Back at Home's end, Streaming chosen (the fling chose the visible row nearest the list's middle).
              ('streaming_back', CHEVRON, 4, ('as', 'home_end')),
              # Settings, the last row: its list in the menu's place, under the art; its chevron goes back.
              ('settings', home_row(SETTINGS, True, HOME_END), 4, ('not', 'streaming_back')),
              ('settings_back', CHEVRON, 4, ('not', 'settings')),
              # A fling from the art (which takes no touch) released over the Settings row clicks nothing: V2.1's
              # image kept its press after its click, and on V04Fm the release opened Settings again (home_click).
              ('art_fling', swipe(160, 100, 160, home_y(SETTINGS, True, HOME_END)), 4, ('as', 'settings_back')),
              # Opened again, the Library glides back to its last row (Books', 15). The knob (Knob: Navigation) walks it
              # nine rows up to Playlists (Home id 14: V2.1's playlist_page), which Previous closes, then six more to
              # Shuffle at its top; the press opens Shuffle, its first row chosen (the tap that opened it before chose
              # none), and that row shuffles the songs.
              ('home_top', swipe(160, 260, 160, 450), 4, ('not', 'settings_back')),
              ('lib_again', home_row(LIBRARY, True), 4, ('not', 'home_top', 'lib')),
              ('playlists', [KNOB_UP] * 9 + [PRESS], 5, ('not', 'lib_again')),
              ('playlists_back', [PREVIOUS], 4, ('not', 'playlists')),
              ('lib_top', [KNOB_UP] * 6, 4, ('not', 'playlists_back')),
              ('shuffle_again', [PRESS], 4, ('not', 'lib_top')),
              ('shuffle_songs', tap(160, 110), 5, ('not', 'shuffle_again'))]  # Shuffle's first row

def send(out, lines):
    """A step's input: key lines to their device's FIFO, as a press and a release each with its
    EV_SYN (a "hold" line holds the key MS before its release); the rest to the touch file."""
    touch = [l for l in lines if not l.startswith(('keys ', 'knob ', 'hold '))]
    if touch:
        with open(out/'touch', 'a') as f: f.write(''.join(l + '\n' for l in touch))
    for line in lines:
        if not line.startswith(('keys ', 'knob ', 'hold ')): continue
        held = line.startswith('hold ')
        device, code, *ms = line.split()[1:] if held else line.split()
        fd = os.open(out/device, os.O_RDWR)  # never waits, as the reader's own open
        try:
            for value in (1, 0):
                now = time.time()
                event = lambda kind, code, value: struct.pack('<IIHHi', int(now), int(now % 1 * 1e6), kind, code, value)
                os.write(fd, event(1, int(code), value) + event(0, 0, 0))  # EV_KEY, then EV_SYN
                time.sleep(int(ms[0]) / 1000 if held and value else 0.12)
        finally:
            os.close(fd)
        time.sleep(0.4)

def png(pixels, path):
    from ipod import imagemagick
    path.write_bytes(imagemagick('-size', f'{W}x{H}', '-depth', '8', 'bgra:-', '-alpha', 'off', 'png:-', data=pixels))

if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('build', type=pathlib.Path)
    ap.add_argument('--seconds', type=int, default=60)
    ap.add_argument('--captures', type=pathlib.Path, help='write stock.png and patched.png here')
    ap.add_argument('--home-menu', action='store_true',
                    help=f'V2.1 Home cards saved ({HOME_MENU}): the iPod Home and its pages as without them')
    ap.add_argument('--media', action='store_true',
                    help='Home in Split, a card with long songs, a book and two photos: the Library, Long Songs, Books, Photos, '
                         'Folder, Coverflow and Streaming by touch, Shuffle Songs')
    args = ap.parse_args()
    if args.home_menu and args.media: raise SystemExit('--home-menu and --media are separate runs')
    # The Library walk precedes the original media walk, and the logins' follow Streaming's: give their steps their
    # settling budget too, and the logins' their waits.
    waits = lambda walk: sum(int(line.split()[1]) / 1000 for step in walk for line in step[1] if line.startswith('wait '))
    walk_seconds = WALK_SECONDS + (sum(step[2] for step in LIBRARY_WALK + LOGIN_WALK) + waits(LOGIN_WALK) if args.media else 0)
    manifest = json.loads((args.build/'manifest.json').read_text())
    if manifest.get('source_sha256') != source_sha256():
        raise SystemExit(f'{args.build}/manifest.json does not match the current sources; rebuild into a fresh directory')
    if manifest.get('model') != 'Shanling M1 Plus':
        raise SystemExit('test/m1plus/boot.py emulates M1 Plus builds only')
    stock_syms = symbols(args.build/'stock-demo')
    sn_addr = stock_syms['product_sncode']
    net_addr = net_address(args.build)
    with tempfile.TemporaryDirectory(prefix='m1-boot-') as tmp, \
         tempfile.TemporaryDirectory(prefix='m1-card-', dir='/dev/shm') as cards:
        tmp = pathlib.Path(tmp)
        runs = {}
        # With --home-menu, the control ('stock') is the same build without the saved cards.
        for name, image, trace in (('stock', 'rootfs.squashfs' if args.home_menu else 'stock.squashfs', ''),
                                   ('patched', 'rootfs.squashfs', f'-d exec,nochain -dfilter {BASE:#x}+{SCRATCH-BASE:#x} -D /out/exec.log')):
            (tmp/name).mkdir()
            card = None
            if args.media:
                card = pathlib.Path(cards)/name
                card.mkdir()
                media_card(card)
            runs[name] = start(args.build/image, tmp/name, args.seconds + walk_seconds, sn_addr, net_addr, trace,
                               HOME_MENU if args.home_menu and name == 'patched' else '', card,
                               HOME_SPLIT if args.media else HOME_FULL)
        deadline = time.monotonic() + args.seconds
        while time.monotonic() < deadline:  # startup: either demo dying early fails below
            if any(p.poll() is not None for p in runs.values()): break
            time.sleep(1)
        def alive(name):
            err = (tmp/name/'demo.err').read_bytes()
            assert (tmp/name/'exit').exists() is False and b'uncaught target signal' not in err, (
                f'{name} demo ended early: {err[-600:].decode("latin-1")}')
        for name in runs: alive(name)
        stock, patched = screen(tmp/'stock'), screen(tmp/'patched')
        if args.captures:
            args.captures.mkdir(parents=True, exist_ok=True)
            png(stock, args.captures/'stock.png'); png(patched, args.captures/'patched.png')
        # Stock reached Home (not a blank page, "SN Error" or the language guide): its pages' dots.
        assert len(set(stock[i:i+4] for i in range(0, len(stock), 4))) > 50, 'stock demo drew no Home'
        bar = 30 * W * 4  # the status bar, whose clock and battery change from run to run
        # The style audit's colours (patch/m1plus_ipod.json): V2.1's list rows are 0x131313 in stock and transparent
        # (black) patched, and their press 0x362221 is 0x333333. A screen is stock's but for those (edits=True): a pixel
        # of one colour is the other, and an icon's soft edge, blended over the row, is darker by at most the row's 0x13.
        edited = {bytes((0x13, 0x13, 0x13)): bytes((0, 0, 0)), bytes((0x36, 0x22, 0x21)): bytes((0x33, 0x33, 0x33))}
        def edit(x, y): return edited.get(x) == y or all(0 <= p - q <= 0x13 for p, q in zip(x, y))
        def differing(a, b, y0=30, y1=H, edits=False):
            return [i // 4 for i in range(y0 * W * 4, y1 * W * 4, 4) if a[i:i+4] != b[i:i+4]
                    and not (edits and edit(a[i:i+3], b[i:i+3]))]
        # The iPod Home, Classic (ACCENT 1): Now Playing chosen, the accent's bar behind its label, the next row black;
        # in Split the art's panel above them (the placeholder, no track playing), in Full the rows from the top.
        def px(shot, x, y): return shot[(y * W + x) * 4:(y * W + x) * 4 + 3]
        split = args.media
        bar_rgb = ACCENT_TOPS[1].to_bytes(3, 'big')[::-1]  # BGRA's first three
        assert px(patched, 200, home_y(NOW, split)) == bar_rgb, f'Home: no accent bar on Now Playing ({px(patched, 200, home_y(NOW, split)).hex()})'
        assert px(patched, 200, home_y(LIBRARY, split)) == b'\0\0\0', 'Home: the second row is not black'
        if split: assert px(patched, 160, STATUS_H + HOME_ART_H // 2) != b'\0\0\0', 'Home: no art panel in Split'
        if args.home_menu:  # the saved cards change nothing
            differ = differing(stock, patched)
            assert not differ, f'Home with saved cards differs at {len(differ)} pixels, first (x, y) {divmod(differ[0], W)[::-1]}'
        else:
            assert differing(stock, patched), 'patched Home is stock\'s grid'
        # The walk: the patched demo's, and with --home-menu the control's too, a screen each step.
        seen = {'home': patched}
        walk, patched_only = ((MENU_WALK, []) if args.home_menu else (MEDIA_WALK, MEDIA_WALK) if args.media
                              else (WALK, WALK))
        for name, touches, settle, want in walk:
            targets = ['patched'] if (name, touches, settle, want) in patched_only else ['stock', 'patched']
            for t in targets:
                send(tmp/t, touches)
            time.sleep(settle)
            for t in runs: alive(t)
            shots = {t: screen(tmp/t) for t in targets}
            seen[name] = shots['patched']
            if args.captures:
                for t, px in shots.items(): png(px, args.captures/f'{name}-{t}.png')
            if want == 'same':
                differ = differing(shots['stock'], shots['patched'], edits=True)
                assert not differ, f'{name}: patched differs from stock at {len(differ)} pixels, first (x, y) {divmod(differ[0], W)[::-1]}'
            elif want == 'differs':
                assert differing(shots['stock'], shots['patched'], edits=True), f'{name}: the payload left stock\'s page as it was'
            elif want[0] == 'rows':
                assert not differing(shots['stock'], shots['patched'], *want[1], edits=True), f'{name}: rows {want[1]} differ from stock'
                assert differing(shots['stock'], shots['patched'], *want[2], edits=True), f'{name}: rows {want[2]} are stock\'s'
            elif want[0] in ('kept', 'still'):
                x0, y0, x1, y1 = want[2]
                box = lambda px: [px[(y * W + x0) * 4:(y * W + x1) * 4] for y in range(y0, y1)]
                assert bool(differing(seen[want[1]], shots['patched'])) == (want[0] == 'kept'), f'{name}: {want[0]} at {want[1]}?'
                assert box(shots['patched']) == box(seen[want[1]]), f'{name}: {want[2]} changed since {want[1]}'
            elif want[0] == 'not':
                for step in want[1:]:
                    assert differing(seen[step], shots['patched']), f'{name}: still as at {step}'
            elif len(want) == 4:
                assert not differing(seen[want[1]], shots['patched'], *want[2]), f'{name}: rows {want[2]} differ from {want[1]}'
                assert differing(seen[want[1]], shots['patched'], *want[3]), f'{name}: rows {want[3]} are as at {want[1]}'
            else:
                differ = differing(seen[want[1]], shots['patched'])
                assert not differ, f'{name}: not back at {want[1]} ({len(differ)} pixels differ)'
        if 'advanced' in seen:
            # The PEQ's tab tap with Knob: Volume: no focus card over Simple, which nothing could move (peq_focus_shown;
            # V039m's grey box). The card would be 0x333333 at (56, 40).
            px = seen['advanced'][(40 * W + 56) * 4:(40 * W + 56) * 4 + 3]
            assert px == b'\0\0\0', f'advanced: the focus card shows over Simple ({px.hex()}) with Knob: Volume'
        for p in runs.values(): p.wait(timeout=args.seconds + walk_seconds + 120)
        for name in runs:
            out = tmp/name
            status = int((out/'exit').read_text())
            err = (out/'demo.err').read_bytes()
            # Killed at the deadline (137) is the only good end: demo never returns by itself on the device.
            assert status == 137 and b'uncaught target signal' not in err, (
                f'{name} demo ended early ({status}): {err[-600:].decode("latin-1")}')
        hits = executed(tmp/'patched'/'exec.log', args.build/'patch.elf')
        hooks = {stock_name: replacement for stock_name, (_, replacement, _) in M1PLUS_HOOKS.items()}
        hooks[WM_PAINT_LEAF_M1PLUS[0]] = WM_PAINT_LEAF_M1PLUS[2]
        reached = {n for n, r in hooks.items() if hits[r]}
        assert STARTUP <= reached, f'startup never entered {sorted(STARTUP - reached)}'
        # crossfade's tap opened crossfade.c's page: its row was there again after EQ, when V2.1
        # rebuilt the list (a tap on a stock row there would change the screens as well).
        assert args.home_menu or args.media or hits['xfade_open'], 'crossfade: the Crossfade row was not there to open its page'
        assert hits['library_open'], "library: Home's row did not open the Library"
        assert args.home_menu or hits['streaming_open'], "streaming: Home's row did not open the Streaming page"
        assert args.home_menu or hits['coverflow_home_back'], "settings: Home's Settings list never went back"
        if args.media:
            data = tmp/'patched/root/mnt/data'
            lengths = (data/'ringnav-lengths').read_bytes() if (data/'ringnav-lengths').exists() else b''
            secs = sorted(struct.unpack_from('<2I', lengths, i)[1] for i in range(0, len(lengths), 8))
            # TagLib rounds the MP3's frames down a second
            assert len(secs) == len(MEDIA_SONGS) and all(LONG_S - 1 <= x <= LONG_S for x in secs), (
                f'long_songs: lengths cached as {secs}, not {LONG_S} s each')
            assert hits['to_reader'], 'book: the tap on the book\'s row never opened the reader'
            assert hits['to_viewer'], 'photo: the tap on the tile never opened the viewer'
            assert hits['swiped'] and hits['moved'], 'photo_swipes: the swipes never moved the viewer to another photo'
            assert hits['touched'], 'cover_next: no touch reached the covers'
            assert hits['to_tracks'], 'cover_open: the tap on the centre cover never opened its tracks'
            assert hits['era_menu'] and hits['era_open_decade'] and hits['stream_config']
            assert hits['spot_np'] and hits['radio_open'], 'spotify, radio: the rows never opened their pages'
            assert hits['coverflow_open'] and hits['home_page'], "coverflow, folder: Home's rows never opened them"
            config = (data/'config.ini').read_text(errors='replace')
            assert re.search(r'^PLAYMODE=2$', config, re.M), 'shuffle_songs: Shuffle (2) not saved as the play mode'
    print(f'M1 Plus under qemu: both demos up, {"the same iPod Home with saved V2.1 cards and without" if args.home_menu else "the iPod Home"}; the walk ({", ".join(n for n, *_ in walk)}) '
          f'as expected; the payload entered through {len(reached)} hooks ({", ".join(sorted(reached))}), {len(hits)} payload functions ran.')
