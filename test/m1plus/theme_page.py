#!/usr/bin/env python3
"""Exercise Theme and Appearance with V2.1's real renderer and input dispatch.

Usage: theme_page.py BUILD CAPTURES [--record-only]
The optional record-only pass retains the original renderer's broken pill for comparison.
"""
import argparse
import collections
import json
import pathlib
import sys
import tempfile
import time

sys.path[:0] = [str(pathlib.Path(__file__).resolve().parent),
               str(pathlib.Path(__file__).resolve().parents[2] / 'tools')]
import boot
from build import symbols


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


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('build', type=pathlib.Path)
    ap.add_argument('captures', type=pathlib.Path)
    ap.add_argument('--record-only', action='store_true')
    args = ap.parse_args()
    args.captures.mkdir(parents=True, exist_ok=True)
    sn = symbols(args.build / 'stock-demo')['product_sncode']
    boot.IPOD_CLASSIC = '[IPOD]\nTHEME=0\nMINIMAL_ACCENT=7\nLIGHT=0\n'
    with tempfile.TemporaryDirectory(prefix='m1-theme-') as tmp:
        out, card = pathlib.Path(tmp) / 'run', pathlib.Path(tmp) / 'card'
        out.mkdir(); card.mkdir()
        # A card enables Knob: Navigation in boot.start; no media is needed for these pages.
        p = boot.start(args.build / 'rootfs.squashfs', out, 180, sn, boot.net_address(args.build),
                       card=card, home='HOME=1\n')
        try:
            time.sleep(40)
            def step(name, lines):
                boot.send(out, lines); time.sleep(3)
                shot = boot.screen(out)
                boot.png(shot, args.captures / (name + '.png'))
                assert b'uncaught target signal' not in (out / 'demo.err').read_bytes()
                return shot
            step('settings', boot.home_row(boot.SETTINGS))
            step('system', boot.home_row(boot.SYSTEM))
            step('display', boot.set_row(2))
            step('display-end', boot.DOWN_LIST)
            step('appearance', boot.set_row(3))
            initial = step('theme', boot.set_row(0))
            if not args.record_only: marks(initial, 0)
            # Modern's preset enables Light Mode. A real tap must write only these expected keys.
            config = out / 'root/mnt/data/config.ini'
            before = config.read_text()
            modern_shot = step('modern', boot.set_row(1))
            if not args.record_only: marks(modern_shot, 1)
            modern = config.read_text()
            minimal_shot = step('minimal', boot.set_row(0))
            if not args.record_only: marks(minimal_shot, 0)
            minimal = config.read_text()
            (args.captures / 'config.json').write_text(json.dumps(
                dict(before=before, modern=modern, minimal=minimal), indent=2) + '\n')
            def values(text):
                import configparser
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
            if not args.record_only:
                for shot, y in shots: pill(shot, y)
        finally:
            p.kill(); p.wait()
    print(f'Theme renderer and preset tap evidence: {args.captures}')


if __name__ == '__main__':
    main()
