#!/usr/bin/env python3
"""M1 Plus: review sheets of the status bar (ipod-ui 4.2), captured under qemu with Wi-Fi, Bluetooth and the battery's
percent all showing, the bar's widest. Not a test: it checks nothing, and prints where the bar's ink lies. One sheet per
theme, in dark and Light Mode: Now Playing playing and paused, a list, and Home.

usage: bar_sheets.py BUILD OUT_DIR   (ImageMagick's montage; four runs of about two minutes)"""
import argparse, json, pathlib, shutil, subprocess, sys, tempfile, time

sys.path[:0] = [str(pathlib.Path(__file__).resolve().parent), str(pathlib.Path(__file__).resolve().parents[2]/'tools')]
import boot
from build import symbols, source_sha256

THEMES = {0: 'minimal', 1: 'classic'}
OPEN = [boot.home_row(boot.LIBRARY, True), boot.page_row(2), boot.lib_row(0), boot.tap(160, 160)]  # the album page's first track
BACK = boot.tap(10, 15)  # the bar's chevron
PLAY = 'keys 164'  # KEY_PLAYPAUSE
BOOT_S, STEP_S = 45, 4


def ink(pixels):
    """The bar's runs of ink, by column: what differs from its top-left corner's colour, in the bar's rows."""
    W, bg = boot.W, pixels[:4]
    cols = [any(pixels[4 * (W * y + x):4 * (W * y + x) + 4] != bg for y in range(30)) for x in range(W)]
    runs, x = [], 0
    while x < W:
        if cols[x]:
            end = x
            while end < W and cols[end]: end += 1
            runs.append((x, end - 1)); x = end
        else: x += 1
    return runs


ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument('build', type=pathlib.Path)
ap.add_argument('out', type=pathlib.Path)
ap.add_argument('--theme', type=int, choices=THEMES, help='this theme only')
ap.add_argument('--uv', type=int, default=4300000, help="the battery's voltage file: V2.1's level holds steady with one, where the sandbox's garbage moves the slot between frames")
args = ap.parse_args()
if args.theme is not None: THEMES = {args.theme: THEMES[args.theme]}
if json.loads((args.build/'manifest.json').read_text()).get('source_sha256') != source_sha256():
    raise SystemExit(f'{args.build}/manifest.json does not match the current sources; rebuild into a fresh directory')
montage = shutil.which('montage')
if not montage: raise SystemExit('ImageMagick (montage) is required')
font = next(iter(subprocess.run(['fc-match', '-f', '%{file}', 'sans'], capture_output=True, text=True).stdout.split()), '') \
    if shutil.which('fc-match') else ''
sn, net = symbols(args.build/'stock-demo')['product_sncode'], boot.net_address(args.build)
args.out.mkdir(parents=True, exist_ok=True)
for t, theme in THEMES.items():
    tiles = []
    for light in (0, 1):
        name = f'{theme}-{"light" if light else "dark"}'
        with tempfile.TemporaryDirectory(prefix='m1-bar-') as tmp, tempfile.TemporaryDirectory(prefix='m1-card-', dir='/dev/shm') as cards:
            run, card = pathlib.Path(tmp)/'p', pathlib.Path(cards)/'p'
            run.mkdir(); card.mkdir()
            boot.media_card(card)
            boot.BATTERY_UV = args.uv
            boot.IPOD_CLASSIC = f'[IPOD]\nTHEME={t}\nACCENT=1\nBATTERY=2\nLIGHT={light}\n'
            p = boot.start(args.build/'rootfs.squashfs', run, BOOT_S + 16 * STEP_S, sn, net, '', '', card, 'HOME=0\n')
            time.sleep(BOOT_S)
            boot.send(run, ['bar 1'])
            for lines in OPEN:
                boot.send(run, lines)
                time.sleep(STEP_S + 2)
            shots = [('playing', [])] + [('paused', [PLAY])] + [('list', boot.NP_BACK), ('home', (BACK + ['wait 2500']) * 4)]
            for step, lines in shots:
                if lines:
                    boot.send(run, lines)
                    time.sleep(STEP_S + 1)
                if b'uncaught target signal' in (run/'demo.err').read_bytes(): raise SystemExit(f'{name}: the demo crashed')
                shot = args.out/f'{name}-{step}.png'
                pixels = boot.screen(run)
                boot.png(pixels, shot)
                print(name, step, ink(pixels), flush=True)
                tiles += ['-label', f'{name}: {step}', str(shot)]
            p.kill()
    subprocess.run([montage, *(['-font', font] if font else []), *tiles, '-tile', '4x2', '-geometry', '320x+6+6', '-pointsize', '13', str(args.out/f'bar-{theme}.png')], check=True)
    print(args.out/f'bar-{theme}.png')
