#!/usr/bin/env python3
"""M1 Plus: review sheets of the portrait iPod Home (ipod-ui 4.5), captured under qemu. Not a test: it checks
nothing; boot.py's walks do. For each theme (Minimal, Classic) one sheet, a row per Home layout (Split, Full,
Carousel), each row the same steps: Home, the knob three rows or cards on (Folder), three more and its press
(Settings), Centre (Playback), and the chevron twice, back to Settings and back to the row or card it left.

usage: home_sheets.py BUILD OUT_DIR   (ImageMagick's montage; six runs, about a minute each)"""
import argparse, json, pathlib, shutil, subprocess, sys, tempfile, time

sys.path[:0] = [str(pathlib.Path(__file__).resolve().parent), str(pathlib.Path(__file__).resolve().parents[2]/'tools')]
import boot
from build import symbols, source_sha256

THEMES = {0: 'minimal', 1: 'classic'}
LAYOUTS = {0: 'Split', 1: 'Full', 2: 'Carousel'}
STEPS = [('knob3', [boot.KNOB_DOWN] * 3), ('settings', [boot.KNOB_DOWN] * 3 + [boot.PRESS]), ('playback', [boot.PRESS]),
         ('playback_back', boot.CHEVRON), ('settings_back', boot.CHEVRON)]
BOOT_S, STEP_S = 45, 4  # Home is up well inside boot.py's 60 s startup budget

ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument('build', type=pathlib.Path)
ap.add_argument('out', type=pathlib.Path)
args = ap.parse_args()
if json.loads((args.build/'manifest.json').read_text()).get('source_sha256') != source_sha256():
    raise SystemExit(f'{args.build}/manifest.json does not match the current sources; rebuild into a fresh directory')
montage = shutil.which('montage')
if not montage: raise SystemExit('ImageMagick (montage) is required')
sn, net = symbols(args.build/'stock-demo')['product_sncode'], boot.net_address(args.build)
args.out.mkdir(parents=True, exist_ok=True)
for t in THEMES:
    for m in LAYOUTS:  # one run at a time: side by side, qemu falls behind the step budget
        name = f't{t}-m{m}'
        with tempfile.TemporaryDirectory(prefix='m1-sheets-') as tmp, \
             tempfile.TemporaryDirectory(prefix='m1-card-', dir='/dev/shm') as cards:
            run, card = pathlib.Path(tmp)/'p', pathlib.Path(cards)/'p'
            run.mkdir(); card.mkdir()
            boot.media_card(card)  # with a card the run starts in Knob: Navigation (boot.start)
            boot.IPOD_CLASSIC = f'[IPOD]\nTHEME={t}\nACCENT=1\n'  # read by start's config.ini
            p = boot.start(args.build/'rootfs.squashfs', run, BOOT_S + STEP_S * (len(STEPS) + 2), sn, net, '', '', card, f'HOME={m}\n')
            time.sleep(BOOT_S)
            (args.out/name).mkdir(exist_ok=True)
            for i, (step, lines) in enumerate([('home', [])] + STEPS):
                if lines:
                    boot.send(run, lines)
                    time.sleep(STEP_S)
                if b'uncaught target signal' in (run/'demo.err').read_bytes(): raise SystemExit(f'{name}: the demo crashed')
                boot.png(boot.screen(run), args.out/name/f'{i:02d}-{step}.png')
            p.kill()
font = next(iter(subprocess.run(['fc-match', '-f', '%{file}', 'sans'], capture_output=True, text=True).stdout.split()), '') \
    if shutil.which('fc-match') else ''
for t, theme in THEMES.items():
    tiles = []
    for m, layout in LAYOUTS.items():
        for shot in sorted((args.out/f't{t}-m{m}').glob('*.png')):
            tiles += ['-label', f'{layout}: {shot.stem[3:]}', str(shot)]
    subprocess.run([montage, *(['-font', font] if font else []), *tiles, '-tile', f'{len(STEPS) + 1}x{len(LAYOUTS)}',
                    '-geometry', '200x+6+6', '-pointsize', '13', str(args.out/f'home-{theme}.png')], check=True)
    print(args.out/f'home-{theme}.png')
