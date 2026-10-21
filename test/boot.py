#!/usr/bin/env python3
"""Start an M1 Plus build's demo and V2.1's own, side by side, under qemu-mipsel: the patched one must
come up as stock does. Usage: python3 test/boot.py BUILD [--seconds N] [--captures DIR]

Each runs in a bwrap sandbox (no network, no host files but the Nix store qemu needs) whose root is
that build's rootfs, with V2.1's own dbus-daemon. A preloaded shim (SHIM) gives demo a 320x480
framebuffer backed by a file, and the device's serial; config.ini has the first-boot language set.
So both reach Home. The patched demo must stay up as long as stock, draw the same Home (but the
status bar's clock and battery), and enter the payload through the hooks startup reaches.

Then both take the same input through WALK: touches (the shim stands in for tslib, as the
touchscreen's samples) and keys (the buttons' and knob's devices, /dev/input/event1 and event2, are
FIFOs the harness writes Linux key events to). Home's pages, System Setting, About, Playback Setting
and its EQ: each screen must match stock's, or differ where the payload changes it, and the payload's
back button must close its EQ and Previous must not.
Not covered: the card, the DAC, GPIO and battery, and the X2000 CPU.
"""
import argparse, bisect, collections, json, os, pathlib, re, shutil, struct, subprocess, sys, tempfile, time
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
static void nap(long ms) { long t[2] = { ms / 1000, ms % 1000 * 1000000 }; nanosleep(t, 0); }
void *ts_open(const char *dev, int nonblock) { (void)dev; (void)nonblock; static int ts; return &ts; }
int ts_config(void *ts) { (void)ts; return 0; }
int ts_close(void *ts) { (void)ts; return 0; }
static void next_line(char *line) {
    for (;;) {
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

def shim(out, root, sn_addr):
    """SHIM, compiled for V2.1's ABI (o32, nan2008, FR=1) against its own glibc 2.28."""
    src = out/'shim.c'
    src.write_text(f'#define W {W}\n#define H {H}\n#define FB_FILE "/out/fb.raw"\n#define TOUCH_FILE "/out/touch"\n'
                   f'#define KEYS_FILE "/out/keys"\n#define KNOB_FILE "/out/knob"\n#define SN_ADDR {sn_addr:#x}u\n' + SHIM)
    run('clang', '--target=mipsel-linux-gnu', '-march=mips32r2', '-mabi=32', '-mfp64', '-mnan=2008', '-mabs=2008', '-fPIC',
        '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-O2', '-Wall', '-Werror', '-c', src, '-o', out/'shim.o')
    run('ld.lld', '-m', 'elf32ltsmip', '-shared', '--hash-style=sysv', '-soname', 'shim.so', out/'shim.o',
        root/'lib/libc-2.28.so', root/'lib/libdl-2.28.so', '-o', out/'shim.so')

def start(image, out, seconds, sn_addr, trace='', home_menu='', card=None):
    """Unpack image as a sandbox root and start dbus-daemon, then demo for seconds; returns the bwrap.
    With card, a directory mounted as the card, and V2.1's library database listing its songs."""
    root = out/'root'
    run('unsquashfs', '-q', '-no-xattrs', '-d', root, image)
    for d in ('mnt/data', 'mnt/mmc', 'var/run/dbus'): (root/d).mkdir(parents=True, exist_ok=True)
    if card: media_db(root/'mnt/data/database.db')
    # Past the first-boot language choice; with home_menu, V2.1's Home cards ([MAIN] HOMEMENU, ids each
    # followed by |, as saveHomemenu 0x4d7940 writes them).
    (root/'mnt/data/config.ini').write_text('[SYSSET]\nLANGUAGE=2\n' + (f'[MAIN]\nHOMEMENU={home_menu}\n' if home_menu else ''))
    conf = (root/'etc/dbus-1/system.conf').read_text()
    # No other users exist in the sandbox: the bus runs as its caller.
    (root/'etc/dbus-1/sandbox.conf').write_text(re.sub(r'\s*<(user|servicehelper)>[^<]*</\1>', '', conf))
    shim(out, root, sn_addr)
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

WALK_SECONDS = 180  # the walk's budget after startup, inside the same run

def tap(x, y): return [f'{x} {y} 200', 'wait 80', f'{x} {y} 0']
def swipe(x0, y0, x1, y1, steps=10):
    return [line for i in range(steps + 1) for line in (f'{x0 + (x1 - x0) * i // steps} {y0 + (y1 - y0) * i // steps} 200', 'wait 16')] + [f'{x1} {y1} 0']
NEXT_PAGE = swipe(280, 250, 40, 250)  # Home's carousel, a page right
DOWN_LIST = swipe(160, 420, 160, 60)  # a list scrolled towards its end
UP_LIST = swipe(160, 100, 160, 460)    # and back towards its start
BACK = tap(18, 53)                    # V2.1's title-bar back button, and the payload's (back_button)
# Keys, as Linux reports them (keyboard_gpio_add.sh, keyboard_encoder): "keys CODE" on the buttons'
# device, "knob CODE" on the knob's; each a press and a release.
PREVIOUS, KNOB_UP = 'keys 165', 'knob 115'  # KEY_PREVIOUSSONG, KEY_VOLUMEUP
# (name, touches for both, seconds to settle, expectation): 'same', stock's below the status bar;
# ('rows', same, differ), the y bands that match stock's and that must not; 'differs'; ('as', step),
# the patched screen as it was at that step; ('not', step, ...), unlike it at each of those steps; or
# ('same', 'moved', step, box): same, and the box (x0, y0, x1, y1, the status bar's included) changed
# on both since that step; ('as', step, same, differ), as at that step in the y band same and unlike
# it in differ; ('kept', step, box): unlike that step, but the box as it was then. Positions are
# V2.1's 320x480 layout.
# Home's last page: V2.1's five cards (seventeen in all), then, patched, the Q2 Pod card in the
# sixth slot (its row's right half, y 266 to 394 with its label); stock's slot is empty.
Q2POD_CARD = (237, 318)
HOME3_ROWS = ('rows', (30, 266), (266, 394))
WALK = [
    ('home3', NEXT_PAGE + ['wait 1500'] + NEXT_PAGE, 4, HOME3_ROWS),
    ('sysset', tap(82, 318), 4, 'same'),
    ('sysset_end', DOWN_LIST + ['wait 800'] + DOWN_LIST, 4, 'same'),
    # About: Model and FW. Version (the stock firmware's, ringnav_about) as stock's, then CFW. Version.
    ('about', tap(160, 446), 4, ('rows', (30, 208), (208, 272))),
    ('home3_again', BACK + ['wait 2500'] + BACK, 5, HOME3_ROWS),
    ('playset', tap(237, 230), 4, 'same'),
    ('knob', [KNOB_UP, KNOB_UP], 3, ('same', 'moved', 'playset', (0, 0, 60, 30))),  # the volume, as stock's, and its figure up
    ('eq', tap(160, 238), 5, 'differs'),  # the PEQ editor in stock's EQ page
]
PATCHED_ONLY = [('eq_closed', BACK, 4, ('as', 'playset')),  # the PEQ's back button; stock's EQ page has its own
                ('eq_again', tap(160, 238), 5, ('as', 'eq')),
                ('eq_previous', [PREVIOUS], 4, ('as', 'eq')),  # Previous is a media key, not Back: the PEQ stays
                # Back steps back one screen: Advanced's Preamp row, then Back to Advanced, then out.
                ('advanced', tap(250, 53), 4, ('not', 'eq')),           # the tab bar's right half
                ('preamp', tap(160, 318), 4, ('not', 'advanced')),      # the third row, under the graph
                ('preamp_back', BACK, 4, ('not', 'preamp', 'playset')),
                ('advanced_back', BACK, 4, ('as', 'playset')),
                ('playset_end', (DOWN_LIST + ['wait 800']) * 3 + DOWN_LIST, 4, ('not', 'playset')),
                ('crossfade', tap(160, 446), 4, ('not', 'playset_end')),
                ('crossfade_slid', tap(230, 247), 4, ('not', 'crossfade')),
                # Back: the list as before (the rows V2.1 rebuilds, then ours again), Crossfade's row now 8 s.
                ('crossfade_back', BACK, 4, ('as', 'playset_end', (30, 414), (414, 480))),
                # Display's Knob: Navigation. The knob's turns then move System Setting's selection
                # (its outline drawn), and the volume, in the status bar, stays as it was.
                ('knob_home', BACK, 5, ('not', 'crossfade_back')),
                ('knob_sysset', tap(82, 318) + ['wait 2000'] + (UP_LIST + ['wait 800']) * 2, 4, ('as', 'sysset')),
                ('display', tap(160, 302), 4, ('not', 'knob_sysset')),
                ('knob_row', tap(160, 430), 3, ('as', 'display', (30, 398), (398, 462))),  # Knob: Navigation
                ('display_back', BACK, 4, ('as', 'knob_sysset')),
                ('knob_nav', [KNOB_UP, KNOB_UP], 3, ('kept', 'display_back', (0, 0, 60, 30))),
                # With Knob: Navigation, Previous is Back: System Setting closes to Home, where it
                # stays Previous track (nothing plays) and Home stays.
                ('previous_back', [PREVIOUS], 4, ('as', 'knob_home')),
                ('previous_home', [PREVIOUS], 4, ('as', 'previous_back')),
                # The Q2 Pod card opens its page (rows of 64 px under the 48 px title bar); its
                # Shuffle row opens Shuffle, which the back button closes. Previous (Knob:
                # Navigation) closes the page, and so does the back button.
                ('q2pod', tap(*Q2POD_CARD), 4, ('not', 'previous_home')),
                ('q2pod_shuffle', tap(160, 110), 4, ('not', 'q2pod')),
                ('q2pod_shuffle_back', BACK, 4, ('as', 'q2pod')),
                ('q2pod_previous', [PREVIOUS], 4, ('as', 'previous_home')),
                ('q2pod_again', tap(*Q2POD_CARD), 4, ('as', 'q2pod')),
                ('q2pod_back', BACK, 4, ('as', 'previous_home'))]
# --home-menu: V2.1's Home with six cards (My Music to Composer), a full page, so the Q2 Pod card starts a
# second page and the dots count it: Home is stock's but for the dots (y 390 to 404). The walk goes to
# the second page, opens the card (its first slot) and closes the page with the back button.
HOME_MENU = '3|4|5|6|7|8|'
HOME_DOTS = (390, 404)
MENU_WALK = [('menu_page2', NEXT_PAGE, 4, ('not', 'home')),
             ('menu_q2pod', tap(83, 83), 4, ('not', 'menu_page2')),
             # Back on Home, V2.1's refresh retitles the bottom bar (y 414 on) without the asset's full
             # stop ("Life is short,Play more", 0x53438c): the rest is as before.
             ('menu_back', BACK, 4, ('as', 'menu_page2', (30, 414), (414, 480)))]

# --media: a card with two 11-minute songs, a book and two photos, and V2.1's songtable listing the
# songs as its scan writes them (time and time_end 0: not CUE tracks). The card is on a tmpfs: on
# ext4, a 32-bit guest's readdir under qemu-user fails on 64-bit directory offsets (EOVERFLOW), so
# the payload would find it empty. The walk, patched only: Long Songs measures and lists both songs;
# a tap opens the book and the photo (a hidden reader or viewer must not take it); a swipe moves to
# the next photo and back; Spotify and Internet Radio open from their rows; Coverflow's covers (one album, then the Sort
# and Refresh cards) turn by swipe and open by a tap on the centre cover; Shuffle Songs saves stock's
# Shuffle play mode.
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
                   (i + 1, n, f'/mnt/mmc/Music/{n}', 'Long', 'Tester', '', f'Long {n}', '', 'Tester', 2024, i + 1, 1,
                    0, 0, 0, 0, 16, 44100))
    db.commit()
    db.close()

# The Q2 Pod page's rows, 64 px under the 48 px title: Shuffle, Ratings, Most Played, Long Songs,
# Photos, Books (with their folders), Coverflow, Spotify, Internet Radio, AirPlay; six show. Scrolled
# to its end (four rows on), Coverflow is the third showing.
def q2pod_row(i): return tap(160, 80 + 64 * i)
def q2pod_end_row(i): return tap(160, 80 + 64 * (i - 4))
MEDIA_WALK = [('media_home3', NEXT_PAGE + ['wait 1500'] + NEXT_PAGE, 4, ('not', 'home')),
              ('media_q2pod', tap(*Q2POD_CARD), 4, ('not', 'media_home3')),
              ('long_songs', q2pod_row(3), 12, ('not', 'media_q2pod')),  # measures, then lists
              ('long_songs_back', BACK, 4, ('as', 'media_q2pod')),
              ('books', q2pod_row(5), 4, ('not', 'media_q2pod')),
              ('book', tap(160, 102), 5, ('not', 'books')),          # the first book's row
              ('book_back', BACK, 4, ('not', 'book')),
              ('books_back', BACK, 4, ('as', 'media_q2pod')),
              ('photos', q2pod_row(4), 6, ('not', 'media_q2pod')),
              ('photo', tap(56, 126), 5, ('not', 'photos')),         # the first tile
              # qemu's demo decodes neither photo ("Can't open this photo"), so the move to the
              # second and back shows only in the trace (photos.c moved); the viewer stays open.
              ('photo_swipes', swipe(240, 250, 60, 250) + ['wait 1500'] + swipe(60, 250, 240, 250), 4, ('as', 'photo')),
              ('photo_back', BACK, 4, ('not', 'photo')),
              ('photos_back', BACK, 4, ('as', 'media_q2pod')),
              ('q2pod_end', DOWN_LIST, 4, ('not', 'media_q2pod')),
              ('coverflow', q2pod_end_row(6), 10, ('not', 'q2pod_end')),
              ('cover_next', swipe(220, 150, 120, 150), 4, ('not', 'coverflow')),  # one cover: the Sort card
              ('cover_prev', swipe(120, 150, 220, 150), 4, ('as', 'coverflow')),
              ('cover_open', tap(160, 120), 5, ('not', 'coverflow')),               # the centre cover's tracks
              ('cover_back', BACK, 4, ('as', 'coverflow')),
              ('coverflow_back', BACK, 4, ('as', 'q2pod_end')),
              # Streaming's rows (V2.1 has no Streaming page): Spotify, not on the card, says so on its
              # Now Playing page; Internet Radio opens its menu. Each closes with its back button.
              ('spotify', q2pod_end_row(7), 4, ('not', 'q2pod_end')),
              ('spotify_back', BACK, 4, ('as', 'q2pod_end')),
              ('radio', q2pod_end_row(8), 5, ('not', 'q2pod_end')),
              ('radio_back', BACK, 4, ('as', 'q2pod_end')),
              ('q2pod_top', UP_LIST, 4, ('as', 'media_q2pod')),
              ('shuffle', q2pod_row(0), 4, ('not', 'media_q2pod')),
              ('shuffle_songs', tap(160, 101), 5, ('not', 'media_q2pod'))]  # Shuffle's first row

def send(out, lines):
    """A step's input: key lines to their device's FIFO, as a press and a release each with its
    EV_SYN; the rest to the touch file."""
    touch = [l for l in lines if not l.startswith(('keys ', 'knob '))]
    if touch:
        with open(out/'touch', 'a') as f: f.write(''.join(l + '\n' for l in touch))
    for line in lines:
        if not line.startswith(('keys ', 'knob ')): continue
        device, code = line.split()
        fd = os.open(out/device, os.O_RDWR)  # never waits, as the reader's own open
        try:
            for value in (1, 0):
                now = time.time()
                event = lambda kind, code, value: struct.pack('<IIHHi', int(now), int(now % 1 * 1e6), kind, code, value)
                os.write(fd, event(1, int(code), value) + event(0, 0, 0))  # EV_KEY, then EV_SYN
                time.sleep(0.12)
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
                    help=f'V2.1 Home with six cards ({HOME_MENU}): the Q2 Pod card on a page of its own, and a short walk to it')
    ap.add_argument('--media', action='store_true',
                    help='a card with long songs, a book and two photos: Long Songs, Books, Photos and Coverflow by touch, Shuffle Songs')
    args = ap.parse_args()
    if args.home_menu and args.media: raise SystemExit('--home-menu and --media are separate runs')
    manifest = json.loads((args.build/'manifest.json').read_text())
    if manifest.get('source_sha256') != source_sha256():
        raise SystemExit(f'{args.build}/manifest.json does not match the current sources; rebuild into a fresh directory')
    if manifest['model'] != 'Shanling M1 Plus':
        raise SystemExit('test/boot.py emulates M1 Plus builds only')
    sn_addr = symbols(args.build/'stock-demo')['product_sncode']
    with tempfile.TemporaryDirectory(prefix='m1-boot-') as tmp, \
         tempfile.TemporaryDirectory(prefix='m1-card-', dir='/dev/shm') as cards:
        tmp = pathlib.Path(tmp)
        runs = {}
        for name, image, trace in (('stock', 'stock.squashfs', ''),
                                   ('patched', 'rootfs.squashfs', f'-d exec,nochain -dfilter {BASE:#x}+{SCRATCH-BASE:#x} -D /out/exec.log')):
            (tmp/name).mkdir()
            card = None
            if args.media:
                card = pathlib.Path(cards)/name
                card.mkdir()
                media_card(card)
            runs[name] = start(args.build/image, tmp/name, args.seconds + WALK_SECONDS, sn_addr, trace,
                               HOME_MENU if args.home_menu else '', card)
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
        def differing(a, b, y0=30, y1=H):
            return [i // 4 for i in range(y0 * W * 4, y1 * W * 4, 4) if a[i:i+4] != b[i:i+4]]
        if args.home_menu:
            differ = differing(stock, patched, 30, HOME_DOTS[0]) + differing(stock, patched, HOME_DOTS[1])
            assert differing(stock, patched, *HOME_DOTS), 'six cards: the dots show no page for the Q2 Pod card'
        else:
            differ = differing(stock, patched)
        assert not differ, f'patched Home differs from stock at {len(differ)} pixels, first (x, y) {divmod(differ[0], W)[::-1]}'
        # The walk: the same touches to both, a screen each step.
        seen, seen_all = {'home': patched}, {}
        walk, patched_only = ((MENU_WALK, MENU_WALK) if args.home_menu else (MEDIA_WALK, MEDIA_WALK) if args.media
                              else (WALK + PATCHED_ONLY, PATCHED_ONLY))
        for name, touches, settle, want in walk:
            targets = ['patched'] if (name, touches, settle, want) in patched_only else ['stock', 'patched']
            for t in targets:
                send(tmp/t, touches)
            time.sleep(settle)
            for t in runs: alive(t)
            shots = {t: screen(tmp/t) for t in targets}
            seen[name] = shots['patched']
            for t, px in shots.items(): seen_all.setdefault(t, {})[name] = px
            if args.captures:
                for t, px in shots.items(): png(px, args.captures/f'{name}-{t}.png')
            if isinstance(want, tuple) and want[:2] == ('same', 'moved'):
                differ = differing(shots['stock'], shots['patched'])
                assert not differ, f'{name}: patched differs from stock at {len(differ)} pixels'
                x0, y0, x1, y1 = want[3]
                box = lambda px: [px[(y * W + x0) * 4:(y * W + x1) * 4] for y in range(y0, y1)]
                for t in ('stock', 'patched'):
                    assert box(shots[t]) != box(seen_all[t][want[2]]), f'{name}: {t} showed no change in {want[3]}'
            elif want == 'same':
                differ = differing(shots['stock'], shots['patched'])
                assert not differ, f'{name}: patched differs from stock at {len(differ)} pixels, first (x, y) {divmod(differ[0], W)[::-1]}'
            elif want == 'differs':
                assert differing(shots['stock'], shots['patched']), f'{name}: the payload left stock\'s page as it was'
            elif want[0] == 'rows':
                assert not differing(shots['stock'], shots['patched'], *want[1]), f'{name}: rows {want[1]} differ from stock'
                assert differing(shots['stock'], shots['patched'], *want[2]), f'{name}: rows {want[2]} are stock\'s'
            elif want[0] == 'kept':
                x0, y0, x1, y1 = want[2]
                box = lambda px: [px[(y * W + x0) * 4:(y * W + x1) * 4] for y in range(y0, y1)]
                assert differing(seen[want[1]], shots['patched']), f'{name}: still as at {want[1]}'
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
        for p in runs.values(): p.wait(timeout=args.seconds + WALK_SECONDS + 120)
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
        assert hits['library_open'], 'q2pod: the card was not there to open its page'
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
            assert hits['spot_np'] and hits['radio_open'], 'spotify, radio: the rows never opened their pages'
            config = (data/'config.ini').read_text(errors='replace')
            assert re.search(r'^PLAYMODE=2$', config, re.M), 'shuffle_songs: Shuffle (2) not saved as the play mode'
    print(f'M1 Plus under qemu: both demos up, the same Home below the status bar{" but for the dots" if args.home_menu else ""}; the walk ({", ".join(n for n, *_ in walk)}) '
          f'as expected; the payload entered through {len(reached)} hooks ({", ".join(sorted(reached))}), {len(hits)} payload functions ran.')
