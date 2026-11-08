#!/usr/bin/env python3
"""M1 Plus: review sheets of Now Playing (ipod-ui 4.6), captured under qemu. Not a test: it checks nothing; boot.py's
walks do. For each theme (Minimal, Classic) one sheet, a row per layout (the iPod's, Centred), each row the same steps:
the art, lyrics, info, the visualizer, back on the art, the knob's volume band, the big cover and its close, the panel
over the list after Back, and V2.1's VOLUME page from a tap on the status bar. A third sheet per theme sets the local page and
Spotify's side by side, Spotify's on boot.py's fake Soloify (the walk's own shots: it checks them; not with --light, whose
page its checks don't know).

usage: np_sheets.py BUILD OUT_DIR   (ImageMagick's montage; four runs of about two minutes, two of about five)"""
import argparse, json, pathlib, shutil, subprocess, sys, tempfile, time

sys.path[:0] = [str(pathlib.Path(__file__).resolve().parent), str(pathlib.Path(__file__).resolve().parents[2]/'tools')]
import boot
from build import symbols, source_sha256

THEMES = {0: 'minimal', 1: 'classic'}
LAYOUTS = {0: 'iPod', 1: 'Centred'}
OPEN = [('library', boot.home_row(boot.LIBRARY, True)), ('albums', boot.page_row(2)), ('album', boot.lib_row(0)), ('track', boot.tap(160, 160))]  # the album page's first track, under its head
SLIDE = boot.swipe(260, 150, 60, 150)
UNSLIDE = boot.swipe(60, 150, 260, 150)
STEPS = [('art', []), ('lyrics', SLIDE), ('info', SLIDE), ('visualizer', SLIDE), ('art_again', UNSLIDE + ['wait 800'] + UNSLIDE + ['wait 800'] + UNSLIDE),
         ('volume', [boot.KNOB_UP]), ('bigcover', ['wait 3500'] + boot.tap(160, 150)), ('bigcover_title', ['wait 4000']), ('closed', boot.tap(160, 150)),
         ('back', boot.NP_BACK), ('panel', [boot.KNOB_UP]), ('volume_page', ['wait 3500'] + boot.tap(160, 15)), ('volume_page_back', boot.tap(30, 55))]
BOOT_S, STEP_S = 45, 4
WAIT = {'volume': 1, 'panel': 1, 'bigcover': 2}  # V2.1's volume closes itself after 3 s; the big cover's title fades after 3 s

ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument('build', type=pathlib.Path)
ap.add_argument('out', type=pathlib.Path)
ap.add_argument('--theme', type=int, choices=THEMES, help='this theme only')
ap.add_argument('--layout', type=int, choices=LAYOUTS, help='this layout only')
ap.add_argument('--light', action='store_true', help='in Light Mode')
args = ap.parse_args()
if args.theme is not None: THEMES = {args.theme: THEMES[args.theme]}
if args.layout is not None: LAYOUTS = {args.layout: LAYOUTS[args.layout]}
if json.loads((args.build/'manifest.json').read_text()).get('source_sha256') != source_sha256():
    raise SystemExit(f'{args.build}/manifest.json does not match the current sources; rebuild into a fresh directory')
montage = shutil.which('montage')
if not montage: raise SystemExit('ImageMagick (montage) is required')
sn, net = symbols(args.build/'stock-demo')['product_sncode'], boot.net_address(args.build)
args.out.mkdir(parents=True, exist_ok=True)
for t in THEMES:
    for c in LAYOUTS:
        name = f't{t}-c{c}'
        with tempfile.TemporaryDirectory(prefix='m1-sheets-') as tmp, \
             tempfile.TemporaryDirectory(prefix='m1-card-', dir='/dev/shm') as cards:
            run, card = pathlib.Path(tmp)/'p', pathlib.Path(cards)/'p'
            run.mkdir(); card.mkdir()
            boot.media_card(card)
            boot.CARD_KNOB = 0  # the knob's volume everywhere: its band here, its panel over the list
            boot.IPOD_CLASSIC = f'[IPOD]\nTHEME={t}\nACCENT=1\nNPCENTRED={c}\nLIGHT={int(args.light)}\n'
            p = boot.start(args.build/'rootfs.squashfs', run, BOOT_S + STEP_S * (len(STEPS) + len(OPEN) + 6), sn, net, '', '', card, 'HOME=0\n')
            time.sleep(BOOT_S)
            (args.out/name).mkdir(exist_ok=True)
            for _, lines in OPEN:
                boot.send(run, lines)
                time.sleep(STEP_S + 2)
            for i, (step, lines) in enumerate(STEPS):
                if lines:
                    boot.send(run, lines)
                    time.sleep(WAIT.get(step, STEP_S))
                if b'uncaught target signal' in (run/'demo.err').read_bytes(): raise SystemExit(f'{name}: the demo crashed')
                boot.png(boot.screen(run), args.out/name/f'{i:02d}-{step}.png')
            p.kill()
font = next(iter(subprocess.run(['fc-match', '-f', '%{file}', 'sans'], capture_output=True, text=True).stdout.split()), '') \
    if shutil.which('fc-match') else ''
for t, theme in THEMES.items():
    tiles = []
    for c, layout in LAYOUTS.items():
        for shot in sorted((args.out/f't{t}-c{c}').glob('*.png')):
            tiles += ['-label', f'{layout}: {shot.stem[3:]}', str(shot)]
    subprocess.run([montage, *(['-font', font] if font else []), *tiles, '-tile', f'{len(STEPS)}x{len(LAYOUTS)}',
                    '-geometry', '200x+6+6', '-pointsize', '13', str(args.out/f'np-{theme}.png')], check=True)
    print(args.out/f'np-{theme}.png')
if not args.light and args.layout in (None, 0):
    boot.soloify(args.build, args.out/'soloify', tuple(THEMES))
    for t, theme in THEMES.items():
        tiles = [str(args.out/f't{t}-c0/00-art.png'), str(args.out/f't{t}-c0/05-volume.png'), str(args.out/f'soloify/t{t}-page.png'),
                 str(args.out/f'soloify/t{t}-volume.png'), str(args.out/f'soloify/t{t}-scrub.png'), str(args.out/f'soloify/t{t}-message.png')]
        labels = ('local', 'local: volume', 'Soloify', 'Soloify: volume', 'Soloify: scrub', 'Soloify: no track')
        subprocess.run([montage, *(['-font', font] if font else []), *[a for label, tile in zip(labels, tiles) for a in ('-label', label, tile)],
                        '-tile', f'{len(tiles)}x1', '-geometry', '240x+6+6', '-pointsize', '13', str(args.out/f'pages-{theme}.png')], check=True)
        print(args.out/f'pages-{theme}.png')
