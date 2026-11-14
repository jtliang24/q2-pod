#!/usr/bin/env python3
"""M1 Plus: review sheets of the iPod UI, captured under qemu. Not gates: boot.py's walks check the UI; these draw it
for a reviewer (theme also checks Theme's real renderer, as its pass did).

    sheets.py BUILD OUT_DIR [bar|home|np|theme|settings|all ...]   (default all; ImageMagick's montage)

Each sheet writes into OUT_DIR/<sheet>/:
  bar    the status bar at its busiest (Wi-Fi, Bluetooth, the battery's percent), each theme in dark and Light Mode: Now
         Playing playing and paused, a list and Home; prints where the bar's ink lies (four runs of about two minutes)
  home   Home in each theme, a row per layout (Split, Full, Carousel): the knob three rows or cards on, Settings,
         Playback, and the chevron twice (six runs, about a minute each)
  np     Now Playing in each theme, a row per layout (the iPod's, Centred): the art, lyrics, info, the visualizer, the
         volume band, the big cover, the panel over the list and V2.1's VOLUME; then the local page and Spotify's on
         boot.py's fake Soloify side by side (four runs of about two minutes, two of about five)
  theme  Theme and Appearance with V2.1's real renderer and input: the picker's marks, the preset tap's saved keys, the
         focus pills (one run of about three minutes; --record-only keeps the captures without the checks)
  settings  the settings pages in each theme, dark and Light: System, Display and its end, Controls, Screen Rotation's
         and Theme's pickers, Configuration and Erase's armed confirm, and Coverflow (four runs of about two minutes)"""
import argparse, collections, configparser, contextlib, json, pathlib, shutil, subprocess, sys, tempfile, time

sys.path[:0] = [str(pathlib.Path(__file__).resolve().parent), str(pathlib.Path(__file__).resolve().parents[2]/'tools')]
import boot
from build import symbols, source_sha256

THEMES = {0: 'minimal', 1: 'classic'}
BOOT_S, STEP_S = 45, 4  # Home is up well inside boot.py's 60 s startup budget


class Sheets:
    """What every sheet shares: the build, its serial and network addresses, montage and its font."""
    def __init__(self, build, out, args):
        self.build, self.out, self.args = build, out, args
        self.sn, self.net = symbols(build/'stock-demo')['product_sncode'], boot.net_address(build)
        self.montage = shutil.which('montage')
        if not self.montage: raise SystemExit('ImageMagick (montage) is required')
        self.font = next(iter(subprocess.run(['fc-match', '-f', '%{file}', 'sans'], capture_output=True, text=True).stdout.split()), '') \
            if shutil.which('fc-match') else ''

    @contextlib.contextmanager
    def run(self, name, seconds, home, media=True, boot_s=BOOT_S):
        """A patched demo booted with Home's layout (home) and a card (Knob: Navigation), with media boot.py's media;
        it yields (run directory, shot), shot(path) writing the screen after checking the demo is still up."""
        with tempfile.TemporaryDirectory(prefix='m1-sheets-') as tmp, \
             tempfile.TemporaryDirectory(prefix='m1-card-', dir='/dev/shm') as cards:
            run, card = pathlib.Path(tmp)/'p', pathlib.Path(cards)/'p'
            run.mkdir(); card.mkdir()
            if media: boot.media_card(card)
            p = boot.start(self.build/'rootfs.squashfs', run, seconds, self.sn, self.net, '', '', card, home)
            def shot(path):
                if b'uncaught target signal' in (run/'demo.err').read_bytes(): raise SystemExit(f'{name}: the demo crashed')
                pixels = boot.screen(run)
                boot.png(pixels, path)
                return pixels
            try:
                time.sleep(boot_s)
                yield run, shot
            finally:
                p.kill(); p.wait()

    def sheet(self, tiles, tile, geometry, out):
        subprocess.run([self.montage, *(['-font', self.font] if self.font else []), *tiles, '-tile', tile, '-geometry', geometry,
                        '-pointsize', '13', str(out)], check=True)
        print(out, flush=True)


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


def bar(s, out):
    themes = {s.args.theme: THEMES[s.args.theme]} if s.args.theme is not None else THEMES
    opened = [boot.home_row(boot.LIBRARY, True), boot.page_row(2), boot.lib_row(0), boot.tap(160, 160)]  # the album page's first track
    back = boot.tap(10, 15)  # the bar's chevron
    for t, theme in themes.items():
        tiles = []
        for light in (0, 1):
            name = f'{theme}-{"light" if light else "dark"}'
            # V2.1's level holds steady with a battery voltage file, where the sandbox's garbage moves the slot between frames
            boot.BATTERY_UV = s.args.uv
            boot.IPOD_CLASSIC = f'[IPOD]\nTHEME={t}\nACCENT=1\nBATTERY=2\nLIGHT={light}\n'
            with s.run(name, BOOT_S + 16 * STEP_S, 'HOME=0\n') as (run, shot):
                boot.send(run, ['bar 1'])
                for lines in opened:
                    boot.send(run, lines)
                    time.sleep(STEP_S + 2)
                for step, lines in [('playing', []), ('paused', [boot.PLAY_KEY]), ('list', boot.NP_BACK), ('home', (back + ['wait 2500']) * 3)]:
                    if lines:
                        boot.send(run, lines)
                        time.sleep(STEP_S + (8 if step == 'home' else 1))  # the taps' waits run in the shim
                    path = out/f'{name}-{step}.png'
                    print(name, step, ink(shot(path)), flush=True)
                    tiles += ['-label', f'{name}: {step}', str(path)]
        s.sheet(tiles, '4x2', '320x+6+6', out/f'bar-{theme}.png')


def home(s, out):
    layouts = {0: 'Split', 1: 'Full', 2: 'Carousel'}
    steps = [('knob3', [boot.KNOB_DOWN] * 3), ('settings', [boot.KNOB_DOWN] * 3 + [boot.PRESS]), ('playback', [boot.PRESS]),
             ('playback_back', boot.CHEVRON), ('settings_back', boot.CHEVRON)]
    for t in THEMES:
        for m in layouts:  # one run at a time: side by side, qemu falls behind the step budget
            name = f't{t}-m{m}'
            boot.IPOD_CLASSIC = f'[IPOD]\nTHEME={t}\nACCENT=1\n'  # read by start's config.ini
            with s.run(name, BOOT_S + STEP_S * (len(steps) + 2), f'HOME={m}\n') as (run, shot):
                (out/name).mkdir(exist_ok=True)
                for i, (step, lines) in enumerate([('home', [])] + steps):
                    if lines:
                        boot.send(run, lines)
                        time.sleep(STEP_S)
                    shot(out/name/f'{i:02d}-{step}.png')
    for t, theme in THEMES.items():
        tiles = [a for m, layout in layouts.items() for shot in sorted((out/f't{t}-m{m}').glob('*.png'))
                 for a in ('-label', f'{layout}: {shot.stem[3:]}', str(shot))]
        s.sheet(tiles, f'{len(steps) + 1}x{len(layouts)}', '200x+6+6', out/f'home-{theme}.png')


def np(s, out):
    themes = {s.args.theme: THEMES[s.args.theme]} if s.args.theme is not None else THEMES
    layouts = {0: 'iPod', 1: 'Centred'}
    if s.args.layout is not None: layouts = {s.args.layout: layouts[s.args.layout]}
    opened = [boot.home_row(boot.LIBRARY, True), boot.page_row(2), boot.lib_row(0), boot.tap(160, 160)]  # the album page's first track, under its head
    slide, unslide = boot.swipe(260, 150, 60, 150), boot.swipe(60, 150, 260, 150)
    steps = [('art', []), ('lyrics', slide), ('info', slide), ('visualizer', slide), ('art_again', unslide + ['wait 800'] + unslide + ['wait 800'] + unslide),
             ('volume', [boot.KNOB_UP]), ('bigcover', ['wait 3500'] + boot.tap(160, 150)), ('bigcover_title', ['wait 4000']), ('closed', boot.tap(160, 150)),
             ('back', boot.NP_BACK), ('panel', [boot.KNOB_UP]), ('volume_page', ['wait 3500'] + boot.tap(160, 15)), ('volume_page_back', boot.tap(30, 55))]
    wait = {'volume': 1, 'panel': 1, 'bigcover': 2, 'volume_page': 1}  # V2.1's volume closes itself after 3 s; the big cover's title fades after 3 s
    for t in themes:
        for c in layouts:
            name = f't{t}-c{c}'
            boot.CARD_KNOB = 0  # the knob's volume everywhere: its band here, its panel over the list
            boot.IPOD_CLASSIC = f'[IPOD]\nTHEME={t}\nACCENT=1\nNPCENTRED={c}\nLIGHT={int(s.args.light)}\n'
            with s.run(name, BOOT_S + STEP_S * (len(steps) + len(opened) + 6), 'HOME=0\n') as (run, shot):
                (out/name).mkdir(exist_ok=True)
                for lines in opened:
                    boot.send(run, lines)
                    time.sleep(STEP_S + 2)
                for i, (step, lines) in enumerate(steps):
                    if lines:
                        boot.send(run, lines)
                        time.sleep(wait.get(step, STEP_S))
                    shot(out/name/f'{i:02d}-{step}.png')
    for t, theme in themes.items():
        tiles = [a for c, layout in layouts.items() for shot in sorted((out/f't{t}-c{c}').glob('*.png'))
                 for a in ('-label', f'{layout}: {shot.stem[3:]}', str(shot))]
        s.sheet(tiles, f'{len(steps)}x{len(layouts)}', '200x+6+6', out/f'np-{theme}.png')
    if not s.args.light and 0 in layouts:  # boot.py's checks of the fake Soloify's page don't know Light Mode's
        boot.soloify(s.build, out/'soloify', tuple(themes))
        for t, theme in themes.items():
            shots = [out/f't{t}-c0/00-art.png', out/f't{t}-c0/05-volume.png', *(out/f'soloify/t{t}-{k}.png' for k in ('page', 'volume', 'scrub', 'message'))]
            labels = ('local', 'local: volume', 'Soloify', 'Soloify: volume', 'Soloify: scrub', 'Soloify: no track')
            s.sheet([a for label, path in zip(labels, shots) for a in ('-label', label, str(path))], f'{len(shots)}x1', '240x+6+6', out/f'pages-{theme}.png')


def pill(shot, y, height=72):
    """Compare top and bottom scanline widths through the actual focus fill."""
    # Graphite's solid card: read its width at each scanline, excluding icons and labels.
    if y is None:
        colors = collections.Counter(shot[i:i + 3] for i in range(30 * 320 * 4, len(shot), 4)
                                     if 48 <= shot[i] <= 128 and shot[i] == shot[i + 1] == shot[i + 2])
        color = colors.most_common(1)[0][0]
        y = next(row for row in range(30, 480)
                 if sum(shot[4 * (row * 320 + x):4 * (row * 320 + x) + 3] == color
                        for x in range(6, 314)) >= 200)
    else:
        color = shot[4 * ((y + 2) * 320 + 160):4 * ((y + 2) * 320 + 160) + 3]
    assert color != b'\0\0\0', 'no focus pill at the expected row'
    widths = []
    for row in range(y, y + height):
        widths.append(sum(shot[4 * (row * 320 + x):4 * (row * 320 + x) + 3] == color
                          for x in range(6, 314)))
    assert min(widths[:4]) > 0 and min(widths[-4:]) > 0, widths
    assert all(abs(a - b) <= 2 for a, b in zip(widths[:8], reversed(widths[-8:]))), widths


def marks(shot, active):
    """A filled centre differs from the ring's empty interior, including on the focus card."""
    def pixel(x, y): return shot[4 * (y * 320 + x):4 * (y * 320 + x) + 3]
    filled = [pixel(48, y) != pixel(48, y - 8) for y in (74, 146)]
    assert filled == [i == active for i in range(2)], filled


def theme(s, out):
    check = not s.args.record_only  # the record-only pass keeps the original renderer's broken pill for comparison
    boot.IPOD_CLASSIC = '[IPOD]\nTHEME=0\nMINIMAL_ACCENT=7\nLIGHT=0\n'
    # A card enables Knob: Navigation in boot.start; no media is needed for these pages.
    with s.run('theme', 180, 'HOME=1\n', media=False, boot_s=40) as (run, shot):
        def step(name, lines):
            boot.send(run, lines); time.sleep(3)
            return shot(out/(name + '.png'))
        step('settings', boot.home_row(boot.SETTINGS))
        step('system', boot.home_row(boot.SYSTEM))
        step('display', boot.set_row(2))
        step('display-end', boot.DOWN_LIST)
        step('appearance', boot.set_row(3))
        initial = step('theme', boot.set_row(0))
        if check: marks(initial, 0)
        # Modern's preset enables Light Mode. A real tap must write only these expected keys.
        config = run/'root/mnt/data/config.ini'
        before = config.read_text()
        modern_shot = step('modern', boot.set_row(1))
        if check: marks(modern_shot, 1)
        modern = config.read_text()
        minimal_shot = step('minimal', boot.set_row(0))
        if check: marks(minimal_shot, 0)
        minimal = config.read_text()
        (out/'config.json').write_text(json.dumps(dict(before=before, modern=modern, minimal=minimal), indent=2) + '\n')
        def values(text):
            c = configparser.ConfigParser(); c.read_string(text)
            return dict(c['IPOD'])
        a, b, c = map(values, (before, modern, minimal))
        assert {k: v for k, v in b.items() if a.get(k) != v} == {
            'theme': '1', 'light': '1', 'home': '0', 'accent': '4', 'timetitle': '0'}
        assert {k: v for k, v in c.items() if b.get(k) != v} == {
            'theme': '0', 'light': '0', 'minimal_accent': '0', 'timetitle': '1', 'rounded': '1'}
        # Touch hides focus: one knob turn brings it back. Test both rows, then Appearance.
        shots = [(step('theme-focus', [boot.KNOB_UP]), 38)]
        shots.append((step('theme-second', [boot.KNOB_DOWN]), 110))
        step('appearance-back', boot.CHEVRON)
        shots.append((step('appearance-focus', [boot.KNOB_UP]), 38))
        shots.append((step('appearance-end', [boot.KNOB_DOWN] * 6), 398))
        # Theme and Appearance fit in their viewport. System's longer list exercises the
        # same mapped rows after an actual scroll, with its final row fully in view.
        step('display-back', boot.CHEVRON)
        step('system-back', boot.CHEVRON)
        step('system-scroll', (boot.DOWN_LIST + ['wait 800']) * 3)
        shots.append((step('system-scrolled', [boot.KNOB_UP]), None))
        if check:
            for pixels, y in shots: pill(pixels, y)
    print(f'Theme renderer and preset tap evidence: {out}')


def settings(s, out):
    """The settings pages and V2.1's pickers in each theme, dark and Light: System (and its selection bar after a knob
    turn), Display, Controls, Screen Rotation and Theme (and their focus frames), Streaming's Configuration with Erase's
    confirm armed, and Coverflow (the aesthetics pass's review sheet)."""
    themes = {s.args.theme: THEMES[s.args.theme]} if s.args.theme is not None else THEMES
    steps = [('system', boot.home_row(boot.SETTINGS) + ['wait 1500'] + boot.home_row(boot.SYSTEM)),
             ('system_knob', [boot.KNOB_DOWN]),  # the selection bar, its row's arrow
             ('display', boot.set_row(2)), ('display_end', boot.DOWN_LIST + ['wait 800']), ('controls', boot.set_row(5)),
             ('system_end', boot.CHEVRON + ['wait 2000'] + boot.CHEVRON + ['wait 2000'] + (boot.DOWN_LIST + ['wait 800']) * 2),
             ('rotation', boot.set_row(0)), ('rotation_knob', [boot.KNOB_DOWN]),  # the picker's frame
             ('theme', boot.CHEVRON + ['wait 2000'] + boot.set_row(1)), ('theme_knob', [boot.KNOB_DOWN]),
             ('configuration', boot.CHEVRON + ['wait 2000'] + boot.CHEVRON + ['wait 2000'] + boot.CHEVRON + ['wait 2000'] +
              boot.home_row(boot.STREAMING) + ['wait 2000'] + boot.page_row(5)),
             ('erase_armed', boot.page_row(2)),  # one tap arms the confirm; only a second erases
             ('coverflow', boot.CHEVRON + ['wait 2000'] + boot.CHEVRON + ['wait 2000'] + boot.home_row(boot.COVERFLOW))]
    wait = {'system': 6, 'system_end': 9, 'theme': 6, 'configuration': 12, 'coverflow': 12}
    for t, theme in themes.items():
        for light in (0, 1):
            name = f'{theme}-{"light" if light else "dark"}'
            boot.IPOD_CLASSIC = f'[IPOD]\nTHEME={t}\nACCENT=1\nLIGHT={light}\n'
            with s.run(name, BOOT_S + sum(wait.get(k, STEP_S) for k, _ in steps) + 20, boot.HOME_FULL) as (run, shot):
                (out/name).mkdir(exist_ok=True)
                for i, (step, lines) in enumerate(steps):
                    boot.send(run, lines)
                    time.sleep(wait.get(step, STEP_S))
                    shot(out/name/f'{i:02d}-{step}.png')
        tiles = [a for light in ('dark', 'light') for shot in sorted((out/f'{theme}-{light}').glob('*.png'))
                 for a in ('-label', f'{light}: {shot.stem[3:]}', str(shot))]
        s.sheet(tiles, f'{len(steps)}x2', '200x+6+6', out/f'settings-{theme}.png')


SHEETS = {'bar': bar, 'home': home, 'np': np, 'theme': theme, 'settings': settings}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('build', type=pathlib.Path)
    ap.add_argument('out', type=pathlib.Path)
    ap.add_argument('which', nargs='*', choices=[*SHEETS, 'all'], default=['all'])
    ap.add_argument('--theme', type=int, choices=THEMES, help='bar, np, settings: this theme only')
    ap.add_argument('--layout', type=int, choices=(0, 1), help="np: this layout only (0 the iPod's, 1 Centred)")
    ap.add_argument('--light', action='store_true', help='np: in Light Mode')
    ap.add_argument('--uv', type=int, default=4300000, help="bar: the battery's voltage file, which steadies V2.1's level")
    ap.add_argument('--record-only', action='store_true', help="theme: capture without the renderer's checks")
    args = ap.parse_args()
    if json.loads((args.build/'manifest.json').read_text()).get('source_sha256') != source_sha256():
        raise SystemExit(f'{args.build}/manifest.json does not match the current sources; rebuild into a fresh directory')
    s = Sheets(args.build, args.out, args)
    for name in (SHEETS if 'all' in args.which else dict.fromkeys(args.which)):
        out = args.out/name
        out.mkdir(parents=True, exist_ok=True)
        SHEETS[name](s, out)


if __name__ == '__main__':
    main()
