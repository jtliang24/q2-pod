#!/usr/bin/env python3
"""JPEG and boot script checks; --build BUILD audits a build (Q2 or M1 Plus), and a stock firmware ZIP
also tests packaging with a custom logo and quoted paths."""
import io, math, re, sys; sys.path[1:1] = [sys.path[0] + '/..']; sys.path.insert(0, sys.path[0] + '/../../tools')  # tools/ first: test/m1plus/build.py must import tools/build.py
from build import TAG, jal, j, ICONS, LABELS, relabel, ROOT, STOCK_EQ, dev_tag, jpeg_size, FONT, TAG_C, patch_m4b_cover, WEB, patch_web, DEFAULT_CONFIG, COVERMODE

logo = (ROOT/'assets/boot-logo.jpg').read_bytes()
assert jpeg_size(logo) == (320, 375)
# JPEG permits extra FF fill bytes before a marker.
assert jpeg_size(logo[:2] + b'\xff' + logo[2:]) == (320, 375)
frame = b'\xff\xd8\xff\xc0\x00\x11\x08\x01\x77\x01\x40'
# The stock display_logo reads three bytes per pixel without converting grayscale/CMYK.
# It also requires the documented 8-bit baseline format.
def sof(marker=0xc0, precision=8, components=3, height=375):
    return (b'\xff\xd8\xff' + bytes([marker]) + (8+3*components).to_bytes(2,'big') +
            bytes([precision]) + height.to_bytes(2,'big') + b'\x01\x40' + bytes([components]) +
            b''.join(bytes([i+1,0x11,0]) for i in range(components)))
assert jpeg_size(sof()) == (320,375) and jpeg_size(sof(height=480)) == (320,480)  # Q2's splash, M1 Plus's
for data in (b'', b'not a JPEG', frame, frame + bytes(8),
             b'\xff\xd8\xff', b'\xff\xd8\xff\xe0\x00',
             b'\xff\xd8\xff\xe0\x00\x01', b'\xff\xd8\xff\xd9' + logo[2:],
             sof(components=1), sof(components=4), sof(precision=12),
             sof(marker=0xc2), sof(marker=0xc3)):
    try:
        jpeg_size(data)
    except ValueError:
        continue
    raise AssertionError(f'Accepted malformed JPEG header: {data!r}')
print('JPEG header regression checks passed.')

# --dev tags: five characters, one per build number, never a release's.
tags = [dev_tag(n) for n in range(1, 36**3)]
assert tags[:2] == ['V001i', 'V002i'] and tags[35] == 'V010i' and tags[-1] == 'VZZZi'
assert len(set(tags)) == len(tags) and all(len(t) == 5 for t in tags) and TAG not in tags
assert dev_tag(36**3) == 'V001i'
from m1plus import M1_TAG, m1_dev_tag
assert m1_dev_tag(1) == 'V001m' and M1_TAG not in [m1_dev_tag(n) for n in range(1, 36**3)]
print('Dev build tag checks passed.')

# tools/ipod.py's screen (docs/m1plus-ipod-ui.md Phase 2): the Q2's by default, as patch/m1plus_q2.inc gives
# the payload, and tools/m1plus_ipod.py's second copy with the M1's, every other name still the Q2's.
import re, ipod, m1plus_ipod
def defines(name):
    text = (ROOT/'patch'/name).read_text()
    found = {m[1]: int(m[2], 0) for m in re.finditer(r'^#define\s+(\w+)\s+(0x[0-9A-Fa-f]+|\d+)\b', text, re.M)}
    # SPOT_* name Now Playing's (m1plus_offsets.inc)
    return {**found, **{m[1]: found[m[2]] for m in re.finditer(r'^#define\s+(SPOT_\w+)\s+(NP_\w+)\b', text, re.M)}}
q2, m1 = defines('m1plus_q2.inc'), defines('m1plus_offsets.inc')
SCREEN = ('UI_W', 'UI_H', 'STATUS_H', 'BOTTOM')
assert [getattr(ipod, n) for n in SCREEN] == [q2[n] for n in SCREEN] == [375, 320, 30, 290]
assert all(d['BOTTOM'] == d['UI_H'] - d['STATUS_H'] for d in (q2, m1))
# The Q2 values the screen's names replaced literals in: its update.tar is byte-identical (test/q2compare.py).
assert [ipod.CORNER_R, ipod.BC_ART, ipod.HOME_LIST_W, ipod.STATUS_MARGIN, ipod.NP_POS_X, ipod.NP_ICONS_END,
        ipod.NP_ART, ipod.NP_BAR, ipod.NP_TIME_X] == [80, 292, 375, 54, 22, 353, 166, [21, 253, 333, 4], 46]
m1ipod = m1plus_ipod.ipod
assert [getattr(m1ipod, n) for n in SCREEN] == [m1[n] for n in SCREEN] == [320, 480, 30, 450]
assert m1ipod.CORNER_R == m1['GLASS_R'] == 0 and m1ipod.HOME_LIST_W == 320
# ... and the layout names a Phase 4 item has given V2.1's (4.2: the bar's battery room, which the 320 px bar fits; 4.5:
# Home's rows and their labels' insets; 4.7: the confirm pop-up's rows).
assert {k for k in m1ipod.O if m1ipod.O[k] != ipod.O.get(k)} == {'UI_W', 'UI_H', 'GLASS_R', 'BATT_ROOM', 'SET_ROW', 'SET_ROWS',
                                                                'SET_STOCK_ROW', 'LIB_PITCH', 'LIB_BODY', 'LIB_ART', 'HOME_ROW',
                                                                'HOME_DOT_X', 'HOME_LABEL_END', 'CONFIRM_TOP'} == set(m1plus_ipod.PROFILE) - {'STATUS_H', 'SET_TOP'}
assert (m1ipod.HOME_ROW, m1ipod.HOME_TEXT_X, ipod.HOME_ROW, ipod.HOME_TEXT_X) == (64, 26, 39, 39)  # the Q2's unchanged
# 4.4: LIB_ROWS complete library rows from the top of the screen under the bar, on a body inside each row, the art inside
# the body; ipod.py's names take the M1's (the Q2's stay 72, 68 and 52).
assert (m1ipod.PITCH, m1ipod.BODY, m1ipod.ART, m1ipod.ART_INSET) == (m1['LIB_PITCH'], m1['LIB_BODY'], m1['LIB_ART'], m1['LIB_ART_INSET']) == (64, 60, 40, 10)
assert m1['LIB_ROWS'] * m1ipod.PITCH <= m1ipod.BOTTOM < (m1['LIB_ROWS'] + 1) * m1ipod.PITCH and m1ipod.ART + 2 * m1ipod.ART_INSET == m1ipod.BODY < m1ipod.PITCH
assert (ipod.PITCH, ipod.BODY, ipod.ART) == (72, 68, 52) and 'LIB_PITCH' not in ipod.O
# 4.3: six complete settings rows fit under the bar, each row's 60 px body inside it.
assert m1ipod.SET_TOP + m1ipod.SET_ROWS * m1ipod.SET_ROW <= m1ipod.BOTTOM and m1['SET_STOCK_BODY'] <= m1ipod.SET_ROW
assert (m1ipod.SET_ROW, m1ipod.SET_ROWS, m1ipod.SET_TOP, m1ipod.SET_STOCK_ROW) == (72, 6, 8, 64)
assert m1ipod.BATT_ROOM == m1['BATT_ROOM'] == 115 and m1['STATUS_MARGIN'] == m1ipod.STATUS_MARGIN == 6 and m1['BAR_BACK_W'] == m1plus_ipod.BACK_W
# 4.6's fixes: the chevron's tap, beside the play state's icon, is the chevron and its gap; Spotify's page has Now Playing's places.
assert m1['BAR_BACK_W'] == 32 and m1['BAR_BACK_HIT_W'] == 64
assert all(m1[f'SPOT_{n}'] == m1[f'NP_{n}'] for n in ('TEXT_X', 'TEXT_W', 'TITLE_Y', 'ARTIST_Y', 'ALBUM_Y', 'BAR_X', 'BAR_W', 'TIMES_Y', 'ART_X', 'ART_Y'))
assert sys.modules['ipod'] is ipod and m1ipod is not ipod
print('iPod screen profile checks passed.')

# patch/m1plus_ipod.json (Phase 3): each of V1.32's 54 audited iPod pages is mapped onto V2.1's, or is a null row
# that names the Phase 4 item deciding it. A sync that adds a page to patch/ipod.json fails here until it is mapped.
import json
AUDIT, M1_AUDIT = (json.loads((ROOT/'patch'/f).read_text()) for f in ('ipod.json', 'm1plus_ipod.json'))
SECTIONS = ('assets', 'navbar_only', 'slide_only')
assert set(M1_AUDIT['pages']) == {p for s in SECTIONS for p in AUDIT[s]} and len(M1_AUDIT['pages']) == 54
MAPPED = {p: r for p, r in M1_AUDIT['pages'].items() if r['v21']}
assert len({r['v21'] for r in MAPPED.values()}) == len(MAPPED), 'two V1.32 pages map to one V2.1 page'
for section in SECTIONS:  # each V2.1 page sits in the section of the V1.32 page it replaces
    assert set(M1_AUDIT[section]) == {r['v21'] for p, r in MAPPED.items() if p in AUDIT[section]}, section
for p, r in M1_AUDIT['pages'].items():
    assert bool(r['v21']) == bool(r['opener']) and r['why'], p
    assert r['v21'] or re.search(r'Phase 4\.\d ', r['why']), f'{p}: a null row names its Phase 4 item'
print('V2.1 iPod page inventory checks passed.')

def boot_check(s90play=None):
    """S90play's dual boot under the host sh, with stand-in programs: build.py's BOOT_HOOK, or a
    built rootfs's whole S90play (its dbus start stubbed), run as init runs it."""
    import subprocess, tempfile, pathlib
    from build import BOOT_HOOK, ROCKBOX_FLAG, WIFI_OFF
    with tempfile.TemporaryDirectory(prefix='q2-boot-') as tmp:
        r = pathlib.Path(tmp)
        script = (s90play or BOOT_HOOK[1]).decode().replace(' &\n', '\n')
        if s90play:
            stubs = ('/usr/bin/dbus-daemon --config-file=/etc/dbus-1/system.conf', '/usr/bin/q2remote')
            assert script.count(stubs[0]) == 1, 'S90play: no dbus start'
            for stub in stubs: script = script.replace(stub, ':')
            script = script.replace('/bin/mkdir', 'mkdir').replace('/var/run/', f'{r}/var/run/')
        for old in ('/mnt/', '/tmp/mmc_add', ROCKBOX_FLAG, '/usr/bin/q2boot', '/release/bin/demo', '/proc/mounts', '/tmp/q2-demo.log',
                    '/tmp/q2-scan-file', '/tmp/q2-scan.log', '/tmp/q2-art-file', '/tmp/q2-art.log'):
            script = script.replace(old, f'{r}{old}')
        script = script.replace('usleep 200000\n', ':\n').replace('usleep 500000', ':')
        # This script runs under the PC's own sh: the real killall -9 and ifconfig would take down the PC's network,
        # not a Q2's. So they never run here: a log line stands in, and the text must be gone before anything starts.
        assert script.count(WIFI_OFF) == 2  # before Rockbox, and the hand-over's late pass
        script = script.replace(WIFI_OFF, f'echo wifi >> {r}/order')
        assert 'usleep 300000' in script  # Home's hand-over pauses before Rockbox: logged, its place is the point
        script = script.replace('usleep 300000', f'echo settle >> {r}/order')
        assert 'usleep 2000000' in script and '\n            rockbox\n            kill $! 2>/dev/null\n' in script  # called off once Rockbox is gone
        script = script.replace('usleep 2000000', f'echo late >> {r}/order')  # runs in line here: & is stripped above
        for real in ('killall -9', 'ifconfig', 'wlan0', 'wpa_supplicant', 'udhcpc', 'wifi_connect'): assert real not in script, real
        for d in ('proc', 'mnt/data', 'mnt/mmc/.rockbox', 'tmp', 'usr/bin', 'release/bin'): (r/d).mkdir(parents=True)
        def exe(path, body): (r/path).write_text('#!/bin/sh\n' + body + '\n'); (r/path).chmod(0o755)
        # demo takes Home's Rockbox row (leaves the flag) as many times as the shortcuts file says
        flag, shortcuts = f'{r}{ROCKBOX_FLAG}', r/'shortcuts'
        # a demo that leaves q2-state (r/keep): it ended without ringnav_clean_end
        exe('release/bin/demo', f'echo demo >> {r}/ran; echo demo >> {r}/order; n=$(cat {shortcuts}); '
            f'[ -f {r}/keep ] && echo running > {r}/mnt/data/q2-state; '
            f'[ "$n" -gt 0 ] && echo $((n - 1)) > {shortcuts} && : > {flag}; '
            f's=$(head -n1 {r}/code); [ $(wc -l < {r}/code) -gt 1 ] && sed -i 1d {r}/code; exit $s')  # one status per run, the last repeats
        rb, target = r/'mnt/mmc/.rockbox/rockbox', r/'mnt/data/boot-target'
        def boot(held, card, code=81, shortcut=0, status=137):
            shortcuts.write_text(f'{shortcut}\n')
            (r/'code').write_text(''.join(f'{c}\n' for c in (status if isinstance(status, (list, tuple)) else [status])))
            exe('usr/bin/q2boot', 'exit ' + ('0' if held else '1'))
            if card: exe('mnt/mmc/.rockbox/rockbox', f'pwd >> {r}/ran; echo rockbox >> {r}/order; exit {code}')
            else: rb.unlink(missing_ok=True)
            (r/'ran').write_text(''); (r/'order').write_text('')
            subprocess.run(['sh', '-c', script, 'S90play', 'start'], check=True)
            return (r/'ran').read_text().split(), target.exists() and target.read_text().strip()
        (r/'proc/mounts').write_text('')
        rockbox = [str(rb.parent), 'demo']
        assert boot(False, False) == (['demo'], False)          # no Rockbox on the card: Q2 Pod
        assert boot(False, True, 1) == (rockbox, False)         # Rockbox by default; a crash starts Q2 Pod
        assert (r/'mnt/mmc/.rockbox/rockbox.log').read_text() == 'exit 1\n'
        assert boot(False, True) == (rockbox, False)            # Boot stock OS (0x51): Q2 Pod starts, nothing saved
        assert boot(True, True, 1) == (['demo'], False)         # Play/Pause held: Q2 Pod, this session
        assert boot(False, True, 1) == (rockbox, False)         # the next power-on is Rockbox again
        target.write_text('stock\n')                            # a stale V8.4 choice is ignored
        assert boot(False, True, 1) == (rockbox, 'stock')
        assert boot(True, True, 1) == (['demo'], 'stock')
        for value in ('q2pod', 'rockbox', 'bad', '', 'q2pod\n', 'q2pod-extra'):
            target.write_text(value)
            expected = ['demo'] if value.rstrip('\n') == 'q2pod' else rockbox
            assert boot(False, True, 0) == (expected, value.strip())
            assert boot(False, True, 1) == (expected, value.strip())  # restart preserves choice
            assert boot(True, True) == (['demo'], value.strip())
            assert boot(False, False) == (['demo'], value.strip())
            assert boot(True, True, 81, 1) == (['demo', *rockbox], value.strip())
        target.unlink()
        # Home's Rockbox row: Rockbox, then Q2 Pod again, as often as it is taken; the flag is gone after
        assert boot(True, True, 81, 1) == (['demo', *rockbox], False)
        assert boot(False, True, 81, 2) == (rockbox * 3, False) and not pathlib.Path(flag).exists()
        assert boot(True, False, 81, 1) == (['demo', 'demo'], False)  # no Rockbox on the card: Q2 Pod again
        # Wi-Fi goes off before every start of Rockbox and at no other time; demo follows Rockbox whatever its status
        def order(*args): boot(*args); return (r/'order').read_text().split()
        session = ['wifi', 'rockbox', 'demo']
        for code in (0, 1, 81, 137, 255): assert order(False, True, code) == session
        handover = ['settle', 'late', 'wifi']
        assert order(True, True, 81, 1) == ['demo', *handover, *session]  # Home's Rockbox row waits for what demo launched
        assert order(False, True, 81, 2) == session + [*handover, *session] * 2  # power-on doesn't wait, the row twice does
        assert order(False, False) == ['demo']                  # no Rockbox on the card
        assert order(True, False, 81, 1) == ['demo', *handover, 'demo']  # nor when the row is taken
        assert order(True, True) == ['demo']                    # Play/Pause held
        target.write_text('q2pod'); assert order(False, True) == ['demo']; target.unlink()
        # an abnormal end of demo leaves its status on /mnt/data, which the next boot copies to a mounted card;
        # 0, 143 and the Rockbox hand-over leave nothing
        crash, copy, mounts = r/'mnt/data/q2-crash.log', r/'mnt/mmc/q2-crash.log', r/'proc/mounts'
        def logged(status, card, shortcut=0):
            for f in (crash, copy): f.unlink(missing_ok=True)
            mounts.write_text(f'tmpfs /tmp tmpfs rw 0 0\n/dev/mmcblk0p1 {r}/mnt/mmc vfat rw 0 0\n' if card else '')
            boot(True, False, shortcut=shortcut, status=status)
            return crash.exists() and crash.read_text(), copy.exists() and copy.read_text()
        out, cp = logged(137, True)
        assert 'demo exit 137' in out and '== dmesg' in out and '== meminfo' in out and '== ps' in out and cp is False  # no card write while dying
        assert not crash.with_name('q2-crash.log.tmp').exists()  # written whole, then renamed
        mounts.write_text(''); boot(True, False, status=0); assert not copy.exists() and crash.exists()  # no card: kept for a later boot
        mounts.write_text(f'/dev/mmcblk0p1 {r}/mnt/mmc vfat rw 0 0\n'); boot(True, False, status=0)
        assert copy.read_text() == out and not crash.exists()  # the next boot with a card moves it there
        copy.write_text('kept'); boot(True, False, status=0); assert copy.read_text() == 'kept'  # and never brings it back
        out, cp = logged(139, False)
        assert 'demo exit 139' in out and cp is False
        assert logged(0, True) == (False, False) and logged(143, True) == (False, False)
        assert logged([137, 0], True, 1) == (False, False)  # the Rockbox hand-over's kill, then a clean demo
        # 0 or 143 with q2-state still there was no clean end (ringnav_clean_end removes it first): logged as a crash
        keep, state = r/'keep', r/'mnt/data/q2-state'
        keep.write_text('')
        for status in (0, 143):
            out, cp = logged(status, False)
            assert f'== demo exit {status}\n' in out and '== dmesg' in out and cp is False and state.exists()
        keep.unlink(); state.unlink()
        # a library scan's and Coverflow's art build's records (navigation.c crash_note): the file in progress and
        # the last 60 memory lines
        for name, last, every in (('scan', 'last scanned', 500), ('art', 'last art', 50)):
            note_file, note_log = r/f'tmp/q2-{name}-file', r/f'tmp/q2-{name}.log'
            note_file.write_text('/mnt/mmc/Music/a.opus\n')
            note_log.write_text(''.join(f'{n * every} {91000 + n} /mnt/mmc/{n}.opus\n' for n in range(1, 71)))
            out, cp = logged(137, False)
            assert f'== {last}\n/mnt/mmc/Music/a.opus\n' in out
            lines = out.split(f'== {name}\n')[1].split('== ')[0].splitlines()
            assert len(lines) == 60 and lines[0].startswith(f'{11 * every} 91011 ') and lines[-1] == f'{70 * every} 91070 /mnt/mmc/70.opus'
            note_file.unlink(); note_log.unlink()
            out, cp = logged(137, False)
            assert f'== {last}' not in out and f'== {name}\n' not in out
        # /mnt/data/q2-state (navigation.c state_poll) still there at boot: the last session ended in a forced
        # restart, or the battery. It goes into q2-crash.log, a new one that says so or the crash's, and goes.
        state, line = r/'mnt/data/q2-state', 'screen:off power:suspending cable:out battery:57 play:paused out:jack\n'
        state.write_text(line); out, cp = logged(0, False)
        assert 'did not end' in out and '== last state' in out and line in out and not state.exists() and cp is False
        # a Coverflow open that never finished (coverflow.c cf_trace) goes in after the state, and goes
        trace = r/'mnt/data/q2-cf-trace'
        state.write_text(line); trace.write_text('start albums=0 0 ms\nstaged albums=20000 900 ms\n'); out, cp = logged(0, False)
        assert '== last state' in out and out.endswith('== cover flow\nstart albums=0 0 ms\nstaged albums=20000 900 ms\n') and not trace.exists()
        trace.write_text('stale\n'); out, cp = logged(0, False)
        assert out is False and not trace.exists()  # no forced restart: dropped, not reported
        for f in (crash, copy): f.unlink(missing_ok=True)
        crash.write_text('== demo exit 137\n'); state.write_text(line); boot(True, False, status=0)
        assert crash.read_text().startswith('== demo exit 137\n== last state\n') and line in crash.read_text() and not state.exists()
        for f in (crash, copy): f.unlink(missing_ok=True)
    print(f'Dual boot ({"built S90play" if s90play else "BOOT_HOOK"}): Rockbox by default, one-session Q2 Pod, stale choice ignored, card fallback, Home Rockbox row and Wi-Fi off before Rockbox passed.')
boot_check()

def logo_check(s11logo=None):
    """S11logo_display_shell's splash choice under the host sh: build.py's LOGO_HOOK, or a built
    rootfs's whole script (its /dev/fb0 wait and ROTATEMODE choice included)."""
    import subprocess, tempfile, pathlib
    from build import LOGO_HOOK, LOGO, LOGO_LIGHT, TIMEZONES
    with tempfile.TemporaryDirectory(prefix='q2-logo-') as tmp:
        tmp = pathlib.Path(tmp)
        user, config, dark, light = tmp/'boot-logo.jpg', tmp/'config.ini', tmp/'logo.jpg', tmp/'logo-light.jpg'
        script = (s11logo or LOGO_HOOK[1]).decode()
        if s11logo:
            assert script.count('"/dev/fb0"') <= 1
            script = script.replace(' &\n', '\n').replace('"/dev/fb0"', '/')
        script = (script.replace('/mnt/data/boot-logo.jpg', str(user)).replace('/mnt/data/config.ini', str(config))
                  .replace('/'+LOGO_LIGHT, str(light)).replace('/'+LOGO, str(dark)).replace('display_logo', 'echo'))
        def shown(rotate=0, ipod=''):
            config.write_text(f'ROTATEMODE={rotate}\n' + ipod)
            return subprocess.run(['sh', '-c', script, 'S11logo', 'start'], check=True, capture_output=True, text=True).stdout.strip()
        assert shown() == str(dark)  # no card logo, no config: the built-in splash
        assert shown(ipod='[IPOD]\nLIGHT=1\n') == str(dark)  # Light Mode, but no light twin (custom --logo)
        light.write_bytes(b'')
        assert shown(ipod='[IPOD]\nLIGHT=1\n') == str(light)
        assert shown(ipod='[IPOD]\nLIGHT=0\nBACKLIGHT=1\n') == str(dark)
        user.write_bytes(b'')
        assert shown() == str(user)
        assert shown(ipod='[IPOD]\nLIGHT=1\n') == str(user)  # the card's logo wins in either mode
        user.unlink()
        config.write_text('[IPOD]\nLIGHT=2\n')
        def at(hour): return subprocess.run(['sh', '-c', script.replace('$(TZ=$z date +%H)', hour), 'S11logo', 'start'], check=True, capture_output=True, text=True).stdout.strip()
        assert at('06') == str(dark) and at('07') == str(light) and at('18') == str(light) and at('19') == str(dark)
        # Auto reads the hour in the saved zone: only the zone's own TZ gets a light hour. V2.1's 27 stock zones
        # are the Q2's first 27, in order (its select_timezone table at 0x97c810).
        for i, (_, zone) in enumerate(TIMEZONES):
            config.write_text(f'[SYSSET]\nTIMEZONE={i}\n[IPOD]\nLIGHT=2\n')
            fake = f'''date() {{ [ "$TZ" = '{zone}' ] && echo 12 || echo 22; }}; '''
            assert subprocess.run(['sh', '-c', fake + script, 'S11logo', 'start'], check=True, capture_output=True, text=True).stdout.strip() == str(light), zone
        # No saved zone, or one past the list: stock's default, as the player reads it (config_init)
        for text in ('[IPOD]\nLIGHT=2\n', f'[SYSSET]\nTIMEZONE={len(TIMEZONES)}\n[IPOD]\nLIGHT=2\n'):
            config.write_text(text)
            fake = f'''date() {{ [ "$TZ" = '{TIMEZONES[22][1]}' ] && echo 12 || echo 22; }}; '''
            assert subprocess.run(['sh', '-c', fake + script, 'S11logo', 'start'], check=True, capture_output=True, text=True).stdout.strip() == str(light)
        user.write_bytes(b'')
        if 'logo180.jpg' in script:  # M1 Plus: a flipped screen keeps the stock flipped splash
            assert shown(1) == '/release/assets/default/raw/images/xx/logo180.jpg'
    print(f'Boot logo ({"built S11logo" if s11logo else "LOGO_HOOK"}): the saved card logo, else the light splash under '
          'Light Mode, else the built-in one, passed.')
logo_check()

def shared_checks(directory, manifest, stock, demo, read):
    """What both models' builds share: the identity strings in demo, the M4B cover dispatcher, the
    helpers and init scripts, bluealsa, the watchdog and hciplayer."""
    import hashlib, pathlib, re, struct, subprocess, tarfile, tempfile
    from build import (sha, run, fileoff, segments, symbols, ROOT, TAG_C, HELPER, HELPER_LIKE, BOOT, BOOT_HOOK,
                       REMOTE, REMOTE_HOOK, LOG_HOOK, S90PLAY, S11LOGO, LOGO_HOOK, RTC_WRITE, LOCK_CLOCK_12H, WATCHDOG,
                       WATCHDOG_SLEEP, BLUEALSA, BLUEALSA2, BT_KEEPALIVE, AAC_44K1, STOCK_EQ)
    import build as q2, m1plus as m1, peq
    m1plus = manifest.get('model') == 'Shanling M1 Plus'  # upstream's Q2 manifest has no model
    patch_m4b_cover = (m1 if m1plus else q2).patch_m4b_cover
    assert manifest['version'].encode()+b'\0' in demo
    # Each of the model's call sites (m1plus.py CALL_SITES) holds stock's word, now its replacement; the
    # manifest lists the M4B extension checks among them.
    from m1plus import call_site_words
    words = call_site_words(m1plus, symbols(directory/'patch.elf'))
    for name, address, old, new in words:
        off = fileoff(stock, address)
        assert struct.unpack_from('<I', stock, off)[0] == old, f'{name}: {address:#x} is not stock\'s'
        assert struct.unpack_from('<I', demo, off)[0] == new, f'{name}: {address:#x} not patched'
    assert manifest['audio_extension_calls'] == [dict(address=hex(a), original=f'{o:#010x}', replacement=hex(n))
                                                 for name, a, o, n in words if name == 'AUDIO_EXTENSION_CALLS' and n != o]
    # The RTC is written in UTC: the one hwclock -w literal gains -u in its own padding.
    assert demo.index(RTC_WRITE[1]) == stock.index(RTC_WRITE[0])
    # The lock window's 12-hour clock reads hour:minutes (H:mm), in stock HH:TT's slot after its 24-hour hh:mm.
    assert demo.index(LOCK_CLOCK_12H[1]) == stock.index(LOCK_CLOCK_12H[0]) and LOCK_CLOCK_12H[0] not in demo
    tag_old, tag_new = read('stock.squashfs', TAG_C), read('rootfs.squashfs', TAG_C)
    assert tag_new == patch_m4b_cover(tag_old)
    assert manifest['changed_assets'][TAG_C] == dict(original_sha256=sha(tag_old), sha256=sha(tag_new))
    tag_segment = segments(tag_new)[-1][1]
    assert tag_segment[0] == 1 and tag_segment[2] == 0x30000 and tag_segment[4:7] == (48, 48, 5)
    # Videos' player: an ELF with the stock binaries' ABI flags (nan2008, o32, mips32r2).
    helper = read('rootfs.squashfs', HELPER)
    assert sha(helper) == manifest['q2video_sha256'] and helper[:4] == b'\x7fELF'
    assert helper[36:40] == read('stock.squashfs', HELPER_LIKE)[36:40]
    # Rockbox's dual boot: q2boot likewise, and S90play differs from stock only in starting demo.
    boot = read('rootfs.squashfs', BOOT)
    assert sha(boot) == manifest['q2boot_sha256'] and boot[:4] == b'\x7fELF' and boot[36:40] == helper[36:40]
    expected_start = read('stock.squashfs', S90PLAY).replace(*BOOT_HOOK)
    if manifest['dev']:
        remote = read('rootfs.squashfs', REMOTE)
        assert sha(remote) == manifest['q2remote_sha256'] and remote[:4] == b'\x7fELF'
        assert remote[36:40] == helper[36:40]
        expected_start = expected_start.replace(*REMOTE_HOOK)
        if not m1plus:  # M1 Plus: demo's output isn't kept (LOG_HOOK, m1plus-unported.md)
            expected_start = expected_start.replace(*LOG_HOOK)
    else:
        assert 'q2remote_sha256' not in manifest
        assert not (directory/'q2remote').exists()
        absent = subprocess.run(['unsquashfs', '-cat', str(directory/'rootfs.squashfs'), REMOTE],
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        assert absent.returncode != 0, 'release rootfs contains q2remote'
    assert read('rootfs.squashfs', S90PLAY) == expected_start
    assert read('rootfs.squashfs', S11LOGO) == read('stock.squashfs', S11LOGO).replace(*LOGO_HOOK)  # the card's logo, if saved
    assert read('rootfs.squashfs', BLUEALSA2) == read('stock.squashfs', BLUEALSA2).replace(*BT_KEEPALIVE)  # keep-alive 5 s
    # bluealsa: AAC capability, DROP jumps, silence sites and one appended LOAD payload.
    from build import BT_DROP, BT_DROP_HANDLER, BT_DROP_PAYLOAD, BT_SILENCE_SITES, patch_bluealsa, segments
    old, new = read('stock.squashfs', BLUEALSA), read('rootfs.squashfs', BLUEALSA)
    header = segments(old)[-1][0]
    allowed = {AAC_44K1, *range(header, header+32)}
    for address, size in ((BT_DROP, 8), (BT_DROP_HANDLER, 8), *((a, 4) for a, *_ in BT_SILENCE_SITES)):
        off = fileoff(old, address)
        allowed.update(range(off, off+size))
    assert {i for i in range(len(old)) if old[i] != new[i]} <= allowed
    assert new == patch_bluealsa(old)
    assert segments(new)[-1][1][2] == BT_DROP_PAYLOAD
    assert new[AAC_44K1] == 0 and manifest['bluealsa_sha256'] == sha(new)
    from bluealsa import check as check_bluetooth_drop
    check_bluetooth_drop(directory)
    from build import SCROBBLE_CA
    assert read('rootfs.squashfs', SCROBBLE_CA) == (ROOT/'assets/scrobble-ca.pem').read_bytes()
    if m1plus:
        # The Q2 Pod page's Photos row: V2.1's 40 px cover-mode badge, as the Q2 uses V1.32's. It was
        # a frame of the 54 px loading spinner (scover_wait0) through dev 11.
        xx = 'release/assets/default/raw/images/xx/'
        photos = read('rootfs.squashfs', xx+'local_photos.png')
        assert photos == read('stock.squashfs', xx+'pset_covermode.png') and struct.unpack('>II', photos[16:24]) == (40, 40)
        # Its Streaming rows' Spotify and Internet Radio icons at that size too; the 52 px originals stay
        # for the radio's Now Playing art.
        for n in ('spotify', 'radio'):
            assert struct.unpack('>II', read('rootfs.squashfs', xx+f'row_{n}.png')[16:24]) == (40, 40)
            assert struct.unpack('>II', read('rootfs.squashfs', xx+f'stream_{n}.png')[16:24]) == (52, 52)
    # The crash watchdog only sleeps longer.
    old, new = read('stock.squashfs', WATCHDOG), read('rootfs.squashfs', WATCHDOG)
    assert new == old.replace(*WATCHDOG_SLEEP) and new != old
    # hciplayer's code (.text) differs from stock only in the VBR scan branch, now a nop, the 48 kHz EQ gates,
    # the ID3v2 walker calls, now id3_gain (MP3 ReplayGain), and the pause loop's sleep (PAUSE_SLEEP);
    # each model's at its own addresses.
    old, new = read('stock.squashfs', 'usr/bin/hciplayer'), read('rootfs.squashfs', 'usr/bin/hciplayer')
    profile = m1.PLAYER_PROFILE if m1plus else dict(vbr_scan=peq.VBR_SCAN, eq_rate_gates=peq.EQ_RATE_GATES,
                                                    id3_calls=peq.ID3_CALLS)
    assert manifest['peq']['stock_sha256'] == sha(old) and manifest['peq']['sha256'] == sha(new)
    assert (directory/'peq'/'stock-hciplayer').read_bytes() == old
    text = re.search(r'\.text +PROGBITS +[0-9a-f]+ ([0-9a-f]+) ([0-9a-f]+) ', run('readelf', '-SW', directory/'peq'/'stock-hciplayer'))
    start, size = int(text[1], 16), int(text[2], 16)
    off = fileoff(old, profile['vbr_scan'])
    if m1plus: profile = dict(profile, eq_rate_gates=(*profile['eq_rate_gates'], profile['pause_sleep']))
    gates = [fileoff(old, a) for a in (*(a for a, _, _ in profile['eq_rate_gates']), *profile['id3_calls'])]
    if not m1plus:
        from peq import IDLE_WAIT, PAUSE_WAIT, CMD_DONE, MP3_ALLOC, MP3_FILTER, MP3_CLOSE, MP3_READ
        gates += [fileoff(old, a) for a in (IDLE_WAIT[0], PAUSE_WAIT[0], CMD_DONE[0], MP3_ALLOC, MP3_FILTER, MP3_READ)]
        ps = symbols(directory/'peq'/'peq.elf')
        for address, value in ((IDLE_WAIT[0], jal(ps['hci_idle_wait'])),
                               (PAUSE_WAIT[0], jal(ps['hci_pause_wait'])), (CMD_DONE[0], jal(ps['hci_command'])),
                               (MP3_ALLOC, jal(ps['mp3_private_alloc'])),
                               (MP3_FILTER, jal(ps['mp3_filter_entry'])), (MP3_CLOSE, ps['mp3_close'])):
            assert struct.unpack_from('<I', new, fileoff(old, address))[0] == value
    # The Q2's FLAC fast paths (tools/flac.py, on by default) patch hciplayer's sync calls and LPC/output
    # pointers; unported on M1.
    from flac import patch_words as flac_words
    flac = () if m1plus else flac_words('sync,lpc,output', symbols(directory/'peq'/'peq.elf'))
    gates += [fileoff(old, a) for a, _, _ in flac]
    differ = [i for i in range(start, start+size) if old[i] != new[i]]
    assert set(differ) <= {*range(off, off+4), *(i for g in gates for i in range(g, g+4))} and not any(new[off:off+4])
    assert [struct.unpack_from('<I', new, fileoff(old, a))[0] for a, _, _ in profile['eq_rate_gates']] == [p for _, _, p in profile['eq_rate_gates']]
    assert [struct.unpack_from('<I', new, fileoff(old, a))[0] for a, _, _ in flac] == [p for _, _, p in flac]
    id3_gain = symbols(directory/'peq'/'peq.elf')['id3_gain']
    assert {struct.unpack_from('<I', new, fileoff(old, a))[0] for a in profile['id3_calls']} == {0x0c000000 | id3_gain >> 2}
    if m1plus:  # the second gate branches to the EQ's insert (a jal), as peq.py's 0x42fd84, not past scaletempo's
        insert, _, _ = next(g for g in profile['eq_rate_gates'] if g[2])  # the loads and first gate are nops
        target = insert + 4 + (struct.unpack_from('<h', old, fileoff(old, insert))[0] << 2)
        assert struct.unpack_from('<I', old, fileoff(old, target))[0] >> 26 == 3, hex(target)
    if m1plus:  # the filter's decoded() calls written_audio_pts(sh, ds) on every block: a leaf, as V1.32's 0x44641c
        words = struct.unpack_from('<64I', old, fileoff(old, profile['written_audio_pts']))
        body = words[:words.index(0x03e00008)]  # up to its first jr $ra
        assert not [w for w in body if w >> 26 == 3 or w & 0xfc00003f == 9], 'written_audio_pts calls out (jal/jalr)'
    names = set(run('unsquashfs', '-l', directory/'rootfs.squashfs').splitlines())
    assert not {'squashfs-root/'+rel for rel in STOCK_EQ} & names, 'Stock EQ assets remain'
    # The kernel mounts the rootfs as it does stock's: build.py's mksquashfs options are stock's own.
    def superblock(image):
        text = run('unsquashfs', '-s', directory/image)
        return re.search(r'^Compression (\w+)$', text, re.M)[1], re.search(r'^Block size (\d+)$', text, re.M)[1]
    assert superblock('rootfs.squashfs') == superblock('stock.squashfs'), (superblock('rootfs.squashfs'), superblock('stock.squashfs'))
    # The update archive: stock's members and GNU tar headers, and the MD5s recovery checks.
    archive = directory/('update.bin' if m1plus else 'update.tar')
    assert archive.read_bytes()[257:265] == b'ustar  \0' and sha(archive.read_bytes()) == manifest['update_sha256']
    with tarfile.open(archive) as t:
        assert [(m.name, m.type) for m in t.getmembers()] == [('firmware_v20.info', tarfile.REGTYPE), ('recovery-update', tarfile.DIRTYPE),
            ('recovery-update/xImage', tarfile.REGTYPE), ('recovery-update/rootfs.squashfs', tarfile.REGTYPE)]
        kernel, rootfs = (t.extractfile('recovery-update/'+n).read() for n in ('xImage', 'rootfs.squashfs'))
        info = t.extractfile('firmware_v20.info').read().decode()
    assert rootfs == (directory/'rootfs.squashfs').read_bytes() and sha(kernel) == manifest['kernel_sha256']
    assert info == f"{manifest.get('model', 'Shanling Q2')}\n{manifest['version']}\n{hashlib.md5(kernel).hexdigest()}  recovery-update/xImage\n" \
                   f"{hashlib.md5(rootfs).hexdigest()}  recovery-update/rootfs.squashfs\n"
    # The helpers can start: their loader and every library they name are in the rootfs.
    libs = {n.rsplit('/', 1)[-1] for n in names if n.startswith(('squashfs-root/lib/', 'squashfs-root/usr/lib/'))}
    with tempfile.TemporaryDirectory(prefix='helpers-') as tmp:
        for rel in (HELPER, BOOT, *([REMOTE] if manifest['dev'] else [])):
            elf = pathlib.Path(tmp)/rel.rsplit('/', 1)[-1]
            elf.write_bytes(read('rootfs.squashfs', rel))
            interp = re.search(r'\[Requesting program interpreter: (\S+)\]', run('readelf', '-lW', elf))[1]
            needed = re.findall(r'\(NEEDED\)\s+Shared library: \[(\S+)\]', run('readelf', '-dW', elf))
            assert 'squashfs-root'+interp in names and needed and set(needed) <= libs, (rel, interp, set(needed) - libs)
    # The init scripts as the device runs them, not only build.py's fragments.
    boot_check(read('rootfs.squashfs', S90PLAY))
    logo_check(read('rootfs.squashfs', S11LOGO))

def m1plus_checks(directory, manifest, stock, demo, read):
    """An M1 Plus build changes V2.1's demo only at M1PLUS_HOOKS, window_manager_paint and the
    identity strings, and its rootfs only in the files build.py names; and V2.1 still provides
    what the boot hook relies on."""
    import filecmp, os, pathlib, re, struct, subprocess, tarfile, tempfile
    from build import (sha, run, fileoff, segments, symbols, BASE, RTC_WRITE, WIFI_LPS, LOCK_CLOCK_12H, TAG_C, ICONS, STOCK_EQ,
                       OBSOLETE, HELPER, BOOT, REMOTE, SCROBBLE_CA, BLUEALSA, BLUEALSA2, WATCHDOG, S90PLAY, S11LOGO)
    from m1plus import (pic_gp, M1PLUS_HOOKS, M1PLUS_GP, WM_PAINT_LEAF_M1PLUS, GRADIENT_LEAF_M1PLUS, PDR_M1PLUS, RTC_READ_M1PLUS,
                        call_site_words, M1PLUS_PRIVATE_FUNCTIONS, M1PLUS_SHIMS, M1PLUS_UNRESOLVED, m1plus_inc)
    ps = symbols(directory/'patch.elf')
    # One Now Playing for the local page and Spotify's (m1plus_np_view.c): navigation.c takes the file under M1PLUS where the Q2 has its
    # np_sync, and the file guards itself, so the Q2 never compiles it. Both pages' painters and the one scrub are in the payload, and the
    # Q2's scrub isn't.
    assert '#if M1PLUS\n#include "m1plus_np_view.c"\n#else\n' in (ROOT/'patch/navigation.c').read_text()
    view_c = (ROOT/'patch/m1plus_np_view.c').read_text()
    assert re.fullmatch(r'/\*.*?\*/\n#if M1PLUS\n.*\n#endif\n', view_c, re.S) and view_c.count('#endif') == view_c.count('#if ')
    assert {'np_write', 'np_view_theme', 'np_bar_fill', 'np_scrub_start', 'np_scrub_drag', 'np_scrub_end', 'np_scrub_gone', 'np_scrubbing',
            'np_scrub_shown', 'np_repaint', 'settle_poll', 'spot_np_page', 'spot_now_playing', 'radio_now_playing'} <= set(ps)
    assert not {'scrub_start', 'scrub_end', 'scrub_commit'} & set(ps)
    # A shim is a stand-in some payload source calls (a row nothing uses is dropped), and the stand-in is defined once.
    nav = (ROOT/'patch/m1plus_nav.h').read_text()
    users = ''.join(f.read_text() for f in (ROOT/'patch').glob('*.[ch]') if f.name != 'm1plus_nav.h')
    for name in M1PLUS_SHIMS:
        assert len(re.findall(rf'^\w[\w *]* {name}\(', nav, re.M)) == 1, f'{name}: no stand-in in m1plus_nav.h'
        assert re.search(rf'\b{name}\(', users), f'{name}: no payload source calls it; drop its M1PLUS_SHIMS row'
    assert not any(name in ps for name in M1PLUS_UNRESOLVED)
    payload = (directory/'patch.bin').read_bytes()
    assert (sha(stock), sha(demo), sha(payload)) == (manifest['stock_demo_sha256'], manifest['demo_sha256'], manifest['patch_sha256'])
    # The iPod UI is the only UI. Its code edits and page rewrites (tools/m1plus_ipod.py) are what each Phase 4
    # item has audited so far: the TagLib cover library, the style files (4.1) and the pages in REWRITES.
    import m1plus_ipod
    # 4.3's one code edit: V2.1's list_view layout slot is ipod_list_layout.
    slot = dict(address=hex(0x9047a8), original=hex(0x60abb0), patched=hex(ps['ipod_list_layout']),
                purpose='settings lists stack SET_ROW rows and map their children')
    # 4.4's: the library rows' immediates (pitch and body, the text re-centred by half the body's growth), each row
    # constructor's layout call made compact_set_row_layout, and the two rebinds' resizes gone (pinned below).
    edits = [dict(address=a, original=hex(int(w, 16)), patched=hex(int(w, 16) & 0xffff0000 | {'pitch': m1ipod.PITCH, 'body': m1ipod.BODY}.get(g['value'], g['value'])),
                  purpose=g['purpose']) for g in M1_AUDIT['immediates'] for a, w in g['sites']]
    grown = (m1ipod.BODY - m1plus_ipod.M1['LIB_STOCK_BODY']) // 2
    assert [g['value'] for g in M1_AUDIT['immediates']] == ['pitch', 'body', 10 + grown, 30 + grown, 32 + grown]
    edits += [dict(address=a, original='0x320f809', patched=hex(m1ipod.jal(ps['compact_set_row_layout'])), purpose=M1_AUDIT['row_layout_calls']['purpose'])
              for a, _ in M1_AUDIT['row_layout_calls']['sites']]
    edits += [dict(address=hex(a), original='0x320f809', patched='0x0', purpose='library rebind retains the width owned by its row layouter')
              for a in (0x532f6c, 0x527918)]
    # 4.5's: Home's playing strip's tap is not bound, and its boot resume is ringnav_boot's; the init and refresh's
    # returns with the grid's widgets gone are pinned as they are (m1plus_ipod.json home).
    home = M1_AUDIT['home']
    home_edits = [dict(address=a, original=hex(int(w, 16)), patched='0x0', purpose=why) for _, _, a, w, why in home['unbound']]
    a, w, why = home['boot_resume']
    home_edits.append(dict(address=a, original=hex(int(w, 16)), patched=hex(m1ipod.jal(ps['ringnav_boot'])), purpose=why))
    # 4.6's: the status bar's tap opens the VOLUME page within the bar's 30 px, not 42 (the top row's first 12 px); V2.1's
    # Now Playing lookups all recurse, and the A-B dots' arithmetic is the bar's x, width and row, pinned as they are.
    playing = M1_AUDIT['playing']
    np_edits = [dict(address=a, original=w, patched=n, purpose=why) for a, w, n, why in playing['status_tap']]
    assert 'variant' not in manifest and manifest['compact_code'] == edits + [slot] + np_edits + home_edits, manifest['compact_code']
    assert len(playing['recursive_lookups']) == 38 and all(w == '0x24060001' for _, w, _ in playing['recursive_lookups'])
    assert [int(w, 16) & 0xffff for _, w, _ in playing['ab_dots']] == [
        m1plus_ipod.M1['NP_BAR_W'], m1plus_ipod.M1['NP_BAR_X'], *[m1plus_ipod.M1['NP_AB_Y']] * 3]
    for a, w, why in playing['recursive_lookups'] + playing['ab_dots']:
        assert struct.unpack_from('<I', demo, fileoff(demo, int(a, 16)))[0] == int(w, 16), why
    for a, w, why in home['safe_returns'] + [r[:2] + ['the pointer-up event id'] for r in home['unbound']]:
        assert struct.unpack_from('<I', demo, fileoff(demo, int(a, 16)))[0] == int(w, 16), why
    # 4.7's: V2.1's pull-down (dropdown_dialog) keeps V1.32's states (1 and 2 dragged or sliding, 3 open, 0 shut) and
    # opens from QUICK_EDGE_PX; the confirm's prompts and checks end above CONFIRM_TOP; the playlist page's rows are one
    # rebuild, called with any widget of its window, and it binds no key-up of its own.
    quick, confirm, playlist = M1_AUDIT['quick'], M1_AUDIT['confirm'], M1_AUDIT['playlist']
    def word_at(a): return struct.unpack_from('<I', demo, fileoff(demo, int(a, 16)))[0]
    assert symbols(directory/'stock-demo')['dialog_dropdown_dialog_init'] == int(quick['init'][0], 16)
    assert [word_at(a) & 0xffff for a, _, _ in quick['edge']] == [m1plus_ipod.M1['QUICK_EDGE_PX']]
    assert [word_at(a) & 0xffff for a, _, _ in quick['events']] == [0x103, 0xff, 0x101, m1plus_ipod.M1['EVT_WINDOW_CLOSE']]
    rows = [(word_at(y) & 0xffff, word_at(h) & 0xffff) for y, _, h, _, _ in confirm['prompt_rows']]
    assert max(y + h for y, h in rows) == m1plus_ipod.CONFIRM_PROMPTS_END < m1plus_ipod.M1['CONFIRM_TOP'], rows
    demo_syms = symbols(directory/'stock-demo')
    rebuild = int(playlist['rebuild'], 16)
    assert all(word_at(a) == 0x04110000 | ((rebuild - int(a, 16) - 4) >> 2) & 0xffff for a, _, _ in playlist['calls'])
    assert word_at(playlist['add_mode'][0]) & 0xffff == m1plus_ipod.M1['PLAYLIST_ADD_MODE'] & 0xffff
    # Add to Playlist from a hold menu (qm_run) opens V2.1's playlist_page in add mode 1, whose row click adds
    # the batch selection from pdeq_showlist as the context's class, as V1.32's does (the payload's names).
    import m1plus
    got = lambda a: word_at(hex(m1plus.M1PLUS_GP - (0x10000 - (word_at(a) & 0xffff))))
    assert [got(a) for a, _, _ in playlist['add_rows'][3:5]] == [demo_syms[m1plus.M1PLUS_CONTEXT_ALIASES.get(n, n)] for n in
                                                                ('p_vector_select_record', 'p_deque_showlist')]
    # V2.1 has no localmusic/ pages: the payload names none (V063m's hold menu opened a localmusic/playlist_page).
    assert b'localmusic/' not in payload, 'patch.bin names a localmusic/ page'
    for a, w, why in (quick['edge'] + quick['states'] + quick['events'] + playlist['calls'] + playlist['events'] +
                      playlist['add_rows'] + [playlist['add_mode']] + [r[:2] + [r[4]] for r in confirm['prompt_rows']] +
                      [r[2:] for r in confirm['prompt_rows']]):
        assert word_at(a) == int(w, 16), why
    raw_styles = 'release/assets/default/raw/styles/'
    assert set(manifest['changed_assets']) == {TAG_C} | {'release/assets/default/raw/ui/' + p for p in m1plus_ipod.REWRITES} | {
        raw_styles + p for p in M1_AUDIT['styles']} | {
        'release/assets/default/raw/images/xx/' + p for p in {**M1_AUDIT['status_icons'], **M1_AUDIT['quiet_icons']}}
    stock_syms = symbols(directory/'stock-demo')
    # Each V2.1 iPod page is the stock page the inventory hashed, decodes and re-encodes exactly, and its init
    # function is in V2.1's demo.
    from ipod import decode, encode, walk
    for section in SECTIONS:
        for page, digest in M1_AUDIT[section].items():
            data = read('stock.squashfs', f'release/assets/default/raw/ui/{page}')
            assert sha(data) == digest and encode(decode(data)) == data, page
    for page, row in MAPPED.items():
        assert row['opener'] in stock_syms, f"{page}: no {row['opener']} in V2.1"
    # patch_asset returns every page no rewrite touches as the stock bytes, and refuses what the audit didn't hash,
    # bytes the codec rejects, and a page of the wrong kind (every page's round trip is checked above).
    for page in m1plus_ipod.UI_ASSETS:
        data = read('stock.squashfs', f'release/assets/default/raw/ui/{page}')
        assert page in m1plus_ipod.REWRITES or m1plus_ipod.patch_asset(page, data) == data, page
    # 4.7: Quick Settings, the built pull-down: each switch and its label on the 320 px screen and clear of the others,
    # the label under its icon; the brightness row exactly under the volume panel (vol_paint), inside the dialog; the
    # sysbar's unused widgets transparent in place, never off screen (docs/m1plus-progress.md section 63).
    qs = decode(read('rootfs.squashfs', 'release/assets/default/raw/ui/' + m1plus_ipod.QUICK))
    qs_named = {n[2].get('name'): n for n in walk(qs)}
    boxes = [qs_named[f'{k}_{v}'][1] for i, l in zip(m1plus_ipod.QS_ICONS, m1plus_ipod.QS_LABELS) for k, v in (('img', i), ('label', l))]
    assert all(x >= 0 and x + w <= m1plus_ipod.M1['UI_W'] for x, _, w, _ in boxes)
    assert not any(a[0] < b[0] + b[2] and b[0] < a[0] + a[2] and a[1] < b[1] + b[3] and b[1] < a[1] + a[3]
                   for i, a in enumerate(boxes) for b in boxes[i + 1:]), boxes
    menu, light = qs_named['view_switchs'][1], qs_named['view_backlight'][1]
    assert light[1::2] == [m1plus_ipod.M1['VOL_PANEL_Y'], m1plus_ipod.M1['VOL_PANEL_H']] and light[1] + light[3] <= qs[1][3] and menu[1] + menu[3] < light[1]
    assert all(qs_named[k][2].get('opacity') == '0' and qs_named[k][1][0] >= 0 for k in ('img_volume', 'label_volume', 'img_digital', 'img_synclink'))
    assert qs_named['slider_backlight'][2]['style'] == 's_ipod_progress' and qs_named['label_wifi'][2]['style:normal:font_size'] == '16'
    # 4.7: the confirm pop-up, the built sheet: full width from the top, Cancel and OK rows from CONFIRM_TOP to its foot,
    # under every prompt V2.1 adds; stock's names, which its init binds.
    cf = decode(read('rootfs.squashfs', 'release/assets/default/raw/ui/' + m1plus_ipod.CONFIRM))
    top, row = m1plus_ipod.M1['CONFIRM_TOP'], 48
    assert cf[1] == [0, 0, m1plus_ipod.M1['UI_W'], top + 2 * row] and cf[2]['self_layout'] == f'default(x=0,y=0,w=100%,h={top + 2 * row})'
    assert [(n[2]['name'], n[2]['text'], n[1]) for n in cf[3]] == [
        ('btn_cancel', 'Cancel', [0, top, m1plus_ipod.M1['UI_W'], row]), ('btn_enter', 'OK', [0, top + row, m1plus_ipod.M1['UI_W'], row])]
    assert not any(k.endswith(('bg_image', 'round_radius')) for k in cf[2])
    # ipod-ui 4.1, the styles: V2.1's default.bin is the file the audit hashed, each edit's old value is in exactly its
    # audited number of states, and the build's file differs from it in those states and nowhere else. Each edited style
    # is one a V2.1 page or its code names (a style nothing uses would edit nothing that paints).
    from ipod import style_props
    with tempfile.TemporaryDirectory(prefix='m1-ui-') as tmp:
        run('unsquashfs', '-q', '-no-xattrs', '-d', f'{tmp}/ui', directory/'stock.squashfs', 'release/assets/default/raw/ui')
        used = {n[2].get('style') for q in pathlib.Path(tmp, 'ui').rglob('*.bin') for n in walk(decode(q.read_bytes()))}
    for rel, audit in M1_AUDIT['styles'].items():
        raw = read('stock.squashfs', raw_styles + rel)
        done = m1plus_ipod.patch_style(rel, raw)
        assert sha(raw) == audit['sha256'] and len(done) == len(raw) and done != raw
        assert sha(done) == manifest['changed_assets'][raw_styles + rel]['sha256'] == sha(read('rootfs.squashfs', raw_styles + rel))
        sites, props = set(), list(style_props(raw))
        for widget, style, prop, old, new, n in audit['edits']:
            at = [a for w, st, _, p, a, v in props if (w, st, p, v) == (widget, style, prop, bytes.fromhex(old))]
            assert len(at) == n and all(done[a:a + 4] == bytes.fromhex(new) for a in at), (style, prop)
            assert style in used or b'\0' + style.encode() + b'\0' in stock, f'{style}: no page or code of V2.1 names it'
            sites.update(i for a in at for i in range(a, a + 4))
        assert {i for i in range(len(raw)) if raw[i] != done[i]} <= sites
        # Every row style of V2.1's lists, settings pages, tables and the hold menu is clear at rest, its press 333333
        # or clear: an opaque row hides the selection bar behind it, and Light Mode turns it to paper (the hold menu's,
        # 4.1's device pass).
        rows = [(st, state, v.hex()) for _, st, state, p, _, v in style_props(done) if p == 'bg_color' and st in (
            'list_item_style', 'list_item_black_style', 'list_itemsort_style', 'btn_tablerow_style')]
        assert len(rows) == 20 and all(v == '00000000' or state == 'pressed' and v == '333333ff' for _, state, v in rows), rows
        # a wrong state count and an unaudited file are refused (patch_style's own checks)
        for bad, why in (({**audit, 'edits': [[*audit['edits'][0][:5], audit['edits'][0][5] + 1], *audit['edits'][1:]]}, 'expected'),
                         ({**audit, 'sha256': '0' * 64}, 'Unaudited')):
            try:
                m1plus_ipod.ipod.patch_style(raw, bad)
            except ValueError as e:
                assert why in str(e), e
            else:
                raise AssertionError(f'{rel}: patch_style took {why!r}')
    page = next(iter(M1_AUDIT['assets']))
    data = read('stock.squashfs', f'release/assets/default/raw/ui/{page}')
    def refuses(path, bad, message):
        try:
            m1plus_ipod.patch_asset(path, bad)
        except ValueError as e:
            assert message in str(e), e
        else:
            raise AssertionError(f'{path}: patch_asset took {message!r}')
    refuses(page, bytes([data[0] ^ 1]) + data[1:], 'unaudited')
    hashed = dict(m1plus_ipod.UI_ASSETS)
    try:  # audited, but not a UI page the codec takes (trailing bytes), or not the kind the path names
        m1plus_ipod.UI_ASSETS[page] = sha(data + bytes(4))
        refuses(page, data + bytes(4), 'Trailing UI data')
        dialog = read('stock.squashfs', 'release/assets/default/raw/ui/dialog/confirminfo_dialog.bin')
        m1plus_ipod.UI_ASSETS[page] = sha(dialog)
        refuses(page, dialog, 'expected a window')
    finally:
        m1plus_ipod.UI_ASSETS.clear(); m1plus_ipod.UI_ASSETS.update(hashed)
    assert m1plus_ipod.patch_code(bytearray(stock), ps) == edits + [slot] + np_edits + home_edits
    # the slot as audited, or nothing; and Home's pinned returns (4.5) and its edits' words likewise
    for at, what in ((0x9047a8, 'a changed layout slot'), (0x4cd938, "a changed status bar tap's limit"),
                     (0x53b8d4, "a changed A-B dots' width"), (0x53cd14, "a changed Now Playing lookup"), (0x5340dc, "a changed Home builder's return"),
                     (0x534e2c, "a changed Home pointer-up binding"), (0x534f04, 'a changed boot resume call')):
        try:
            damaged = bytearray(stock); damaged[fileoff(stock, at)] ^= 1
            m1plus_ipod.patch_code(damaged, ps)
        except ValueError as e:
            assert 'unexpected instruction' in str(e), e
        else:
            raise AssertionError(f'patch_code took {what}')
    # Native evidence for this batch: options are asset rows, not V1.32's kind table;
    # Tidal creates its URL worker on demand, and check_cpumem does only drop_caches work.
    more = list(walk(decode(read('stock.squashfs', 'release/assets/default/raw/ui/dialog/playmore_dialog.bin'))))
    assert [n[2]['name'] for n in more if n[0] == 'list_item'] == [f'listitem{i}' for i in range(7)]
    assert next(n for n in more if n[2].get('name') == 'image3')[2]['image'] == 'p_onlinesearch'
    assert next(n for n in more if n[2].get('name') == 'playmore_listview')[2]['item_height'] == '50'
    pins = {0x512f98: 0x0320f809, 0x512fac: 0x0320f809, 0x512fd0: 0x0320f809,
            0x512fd4: 0x24c6c288, 0x512fe0: 0x0320f809, 0x51c2f8: 0xa1230000,
            0x50b844: 0x0320f809, 0x50b878: 0x0320f809, 0x50b894: 0x0320f809,
            0x5d1818: 0x24840d40,
            # V2.1 animator easing callback, not Q2's 0x38 field.
            0x673548: 0xae120044}
    assert all(struct.unpack_from('<I', stock, fileoff(stock, a))[0] == word for a, word in pins.items())
    for n in ('local_era', 'row_stream_config'):
        assert struct.unpack('>II', read('rootfs.squashfs', f'release/assets/default/raw/images/xx/{n}.png')[16:24]) == (40,40)
    # Every page m1plus_contexts.inc lets ringnav navigate is a window V2.1's assets name, as build.py
    # checks contexts.inc's against V1.32's.
    listing = subprocess.run(['unsquashfs', '-l', str(directory/'stock.squashfs')], capture_output=True, text=True).stdout
    windows = set()
    for rel in re.findall(r'squashfs-root/(release/assets/default/raw/ui/\S+\.bin)', listing):
        data = read('stock.squashfs', rel); i = data.find(b'name\0')
        if i >= 0: windows.add(data[i+5:data.index(b'\0', i+5)].decode('utf-8', 'replace'))
    m1_contexts = re.findall(r'"([^"]+)"', (ROOT/'patch/m1plus_contexts.inc').read_text())
    assert m1_contexts and not set(m1_contexts) - windows, set(m1_contexts) - windows
    allowed = set()  # demo file offsets the build may change
    def jumped(address, name):
        off = fileoff(stock, address)
        assert demo[off:off+8] == struct.pack('<II', 0x08000000 | ps[name] >> 2, 0), f'{name}: no jump at {address:#x}'
        allowed.update(range(off, off+8))
    # Each hook: V2.1's own symbol, or a private routine M1PLUS_PRIVATE_FUNCTIONS names (the gapless
    # pick and open), a PIC entry resolving V2.1's GOT base (the trampoline restores it), now a jump
    # to its payload replacement.
    for name, (address, replacement, _) in M1PLUS_HOOKS.items():
        assert stock_syms.get(name, M1PLUS_PRIVATE_FUNCTIONS.get(name)) == address and pic_gp(stock, address) == M1PLUS_GP, name
        jumped(address, replacement)
    # The call sites in V2.1's own code (CALL_SITES['m1plus']); shared_checks checks their words.
    for _, address, _, _ in call_site_words(True, ps):
        off = fileoff(stock, address)
        allowed.update(range(off, off+4))
    for name, address, replacement, words in (WM_PAINT_LEAF_M1PLUS, GRADIENT_LEAF_M1PLUS):
        assert stock_syms[name] == address and struct.unpack_from('<III', stock, fileoff(stock, address)) == words
        jumped(address, replacement)
    # The one version literal takes the 5-character tag; the byte past V2.1's NUL is padding.
    at, n = stock.index(b'V2.1\0'), len(manifest['version']) + 1
    assert stock.count(b'V2.1\0') == 1 and stock[at+5:at+n] == bytes(n-5) and demo[at:at+n] == manifest['version'].encode()+b'\0'
    allowed.update(range(at, at+n))
    # V2.1's updater (update_firmware, 0x4e0e34) takes a card's update.bin only if firmware_v20.info's
    # first line is demo's model string and its second has a V and differs from demo's version
    # literal: strcmp, strchr(line, 'V'), strcmp, each string a GOT page plus an addiu.
    updater = fileoff(stock, 0x4e10e4)
    assert stock[updater:updater+0x44].hex() == ('08a7858f6cf5998f09f820031877a524a2ff40141800bc8fecf4998f5600052409f82003'
                                                '252080029cff40101800bc8f08a7858f252080026cf5998f09f820033c77a524'), 'update_firmware: not the audited checks'
    def compared(lw, addiu):
        page = struct.unpack_from('<I', stock, fileoff(stock, M1PLUS_GP + struct.unpack_from('<h', stock, fileoff(stock, lw))[0]))[0]
        o = fileoff(stock, page + struct.unpack_from('<h', stock, fileoff(stock, addiu))[0])
        return o, stock[o:stock.index(b'\0', o)]
    (_, model), (version_at, version) = compared(0x4e10e4, 0x4e10f0), compared(0x4e1114, 0x4e1124)
    assert model == manifest['model'].encode() and (version_at, version) == (at, b'V2.1')
    with tarfile.open(directory/'update.bin') as t:
        info = t.extractfile('firmware_v20.info').read().decode().splitlines()
    # This build installs over stock (and stock back over it), and the same build is refused once installed.
    assert info[0].encode() == model and 'V' in info[1] and info[1].encode() != version and info[1] == manifest['version']
    # Knob Navigation Mode remaps the knob on its release (navigation.c knob_nav_active), which is
    # enough because V2.1 turns the volume there: home_page_init binds the window manager's key-up
    # to on_wm_keyup_fun and no key-down at all, and on_wm_keyup_fun opens the volume dialog for
    # 220/221 (key - 220 < 2). V2.1 has no Key Tone (no buzzer command) to port.
    def got(lw): return struct.unpack_from('<I', stock, fileoff(stock, M1PLUS_GP + struct.unpack_from('<h', stock, fileoff(stock, lw))[0]))[0]
    def words(address, n): return struct.unpack_from(f'<{n}I', stock, fileoff(stock, address))
    # ipod-ui 4.1, the paint backbone: V2.1's own code for what the four hooks and the gradient leaf read.
    # style_get_gradient is a leaf: a null style, vtable or slot returns 0, else it tail-calls the style
    # vtable's get_gradient (+0x18), as the Q2's does. style_get_color asks it first (a bal, which returns to
    # STYLE_COLOR_GRADIENT_RET) and takes a gradient's first stop; with none it calls the vtable's get_color (+0x14).
    from ipod import branch
    gradient, color = stock_syms['style_get_gradient'], stock_syms['style_get_color']
    assert words(gradient, 11) == (0x10800009, 0, 0x8c820000, 0x10400006, 0, 0x8c590018, 0x13200003, 0, 0x03200008, 0,
                                   0x03e00008), 'style_get_gradient: not the audited leaf'  # ... lw t9, 0x18(v0); jr t9
    assert words(gradient + 0x2c, 1) == (0x00001025,)  # the null paths return 0
    assert words(color + 0x34, 2) == (0x8ca20000, 0x10400004) and words(color + 0x40, 1) == (0x8c420014,)  # the slot @0x14
    assert words(color + 0xb4, 2) == (0x8c590014, 0x0320f809), 'style_get_color: get_color slot'
    ret = m1plus_inc('STYLE_COLOR_GRADIENT_RET')
    assert ret == color + 0x84 and words(ret - 8, 1) == (branch(0x04110000, ret - 8, gradient),), 'style_get_color: gradient call'
    # gradient_t: the stop count at +8, then 8-byte {color, offset} stops from +0xc (the first stop's color is +0xc,
    # the last's is 8 * nr + 4)
    first, last = stock_syms['gradient_get_first_color'], stock_syms['gradient_get_last_color']
    assert words(first + 0x14, 2) == (0x8ca30008, 0x14600011) and words(first + 0x60, 1) == (0x8ca3000c,)
    assert words(last + 0x14, 2) == (0x8ca30008, 0x14600011) and words(last + 0x60, 2) == (0x00a32821, 0x8ca30004)
    # bitmap_t: w @0, h @4, line length @8, flags u16 @0xc, format u16 @0xe (bitmap_init); formats 1 to 4 are the
    # 4-byte ones (bitmap_get_bpp_of_format's table, whose address is a GOT page plus an addiu).
    init = stock_syms['bitmap_init']
    assert (words(init + 0x7c, 1), words(init + 0x84, 1), words(init + 0x90, 1), words(init + 0xa0, 1)) == (
        (0xae130000,), (0xae140004,), (0xa611000e,), (0xa602000c,)), 'bitmap_init: bitmap_t layout'
    assert words(stock_syms['bitmap_get_line_length'] + 0x18, 1) == (0x8c820008,)
    table = got(0x63fefc) + struct.unpack_from('<h', stock, fileoff(stock, 0x63ff00))[0]
    assert words(0x63fefc, 1) == (0x8f828054,) and stock[fileoff(stock, table):][:9] == bytes((4, 4, 4, 4, 2, 2, 3, 3, 1)), 'bpp table'
    # image_manager_add(manager, name, bitmap_t *): the name in a1, copied by the cache, and the bitmap in a2, whose
    # first 0x48 bytes it copies
    add = stock_syms['image_manager_add']
    assert words(add + 0x20, 1) == (0x00a09825,) and words(add + 0x40, 1) == (0x00c09025,)  # move s3, a1; move s2, a2
    assert words(add + 0x74, 2) == (0x24060048, 0x02402825) and words(add + 0x98, 1) == (0x02602025,)
    # widget_on_paint_background(widget, canvas): the widget's vtable @0x70, whose on_paint_background (+0x58) it tail-calls
    paint_bg = stock_syms['widget_on_paint_background']
    assert words(paint_bg + 0x30, 1) == (0x8c820070,) and words(paint_bg + 0x3c, 1) == (0x8c590058,)
    # ui_loader_load_widget_with_parent(name, parent): both kept in registers for the load
    load = stock_syms['ui_loader_load_widget_with_parent']
    assert words(load + 0x24, 1) == (0x00808825,) and words(load + 0x30, 1) == (0x00a0a025,)
    # ipod-ui 4.2, the status bar. systembar_timer_start (0x5453c8) arms a 1000 ms timer (addiu a2, zero, 0x3e8) on the
    # callback at 0x545394: `bal show_sysbar_face; move a0, zero`. The face (systembar_showface, the payload's hook)
    # reads the system_bar global, not its argument, and finds each widget by name; the battery's level is power_capacity
    # and its icon names are bar_charge and bar_lowpower.
    face = stock_syms['show_sysbar_face']
    assert M1PLUS_PRIVATE_FUNCTIONS['systembar_showface'] == face == M1PLUS_HOOKS['systembar_showface'][0]
    assert words(0x545414, 1) == (0x240603e8,) and words(0x5453b0, 2) == (branch(0x04110000, 0x5453b0, face), 0x00002025)
    assert got(0x544b98) == stock_syms['system_bar'] and got(0x545120) == stock_syms['power_capacity']
    for addiu, name in ((0x544bd8, b'img_playstate'), (0x544c98, b'img_btclass'), (0x544cb8, b'img_wifi'), (0x544cd8, b'img_battery'),
                        (0x544cf8, b'pgbar_battery')):
        assert compared(addiu - 0xc, addiu)[1] == name, name
    assert compared(0x54535c, 0x545360)[1] == b'bar_charge' and compared(0x545160, 0x545168)[1] == b'bar_lowpower'
    # V2.1's system_bar.bin as the rewrite takes it (its names are the audit's) and as the build ships it: the payload's
    # names are in it (label_eq and label_idle are not: V2.1 has neither, and a null lookup is tolerated), the chevron is
    # a hidden BAR_BACK_W x STATUS_H image at the far left, the clock stays centred, the groups clear it, and what the
    # iPod doesn't draw is off-screen. A bar whose widgets differ is refused.
    bar_path = 'release/assets/default/raw/ui/system_bar.bin'
    bar_raw = read('stock.squashfs', bar_path)
    bar_new = m1plus_ipod.patch_asset('system_bar.bin', bar_raw)
    assert bar_new == read('rootfs.squashfs', bar_path) != bar_raw
    named = {n[2].get('name'): n for n in walk(decode(bar_new))}
    want = dict(re.findall(r'^#define STATUSW_(\w+) "([^"]+)"', (ROOT/'patch/m1plus_offsets.inc').read_text(), re.M))
    assert {n for k, n in want.items() if k not in ('IDLE', 'EQ')} <= set(named) and not {want['IDLE'], want['EQ']} & set(named)
    assert named['img_back'][1] == [0, 0, 32, 30] and named['img_back'][2]['visible'] == 'false' and named['img_back'][2]['image'] == 'bar_back'
    # The chevron has the left group to itself; the play state sits right of Bluetooth's canvas, whose ink is at its right edge.
    assert named['view_bar_left'][3] == [named['img_back']]
    assert named['view_bar_right'][3] == [named[n] for n in ('img_btclass', 'img_playstate', 'img_wifi', 'view_battery')]
    assert [n for n in m1plus_ipod.STATUS_SHOWN if n != 'img_back'] == [n[2]['name'] for n in named['view_bar_right'][3]]
    clock = named['bar_dclock'][1]
    assert clock[0] + clock[2] // 2 == 160
    # The widgets the iPod doesn't draw stay inside the bar, transparent: on V2.1 an invalidate off the screen's left
    # loses the frame's flush (boot.py's walk saw the page stay as it was after a tap, about 9 runs in 10).
    assert all(named[n][1][0] >= 0 and named[n][1][0] + named[n][1][2] <= 320 and named[n][2].get('opacity') == '0'
               for n in m1plus_ipod.STATUS_HIDDEN)
    left, right = named['view_bar_left'][1], named['view_bar_right'][1]
    assert left[0] == 0 and left[0] + left[2] <= clock[0] and clock[0] + clock[2] <= right[0] and right[0] + right[2] == 320
    broken = decode(bar_raw); broken[3][0][2]['name'] = 'view_left'
    try:
        m1plus_ipod.status_bar(broken)
    except ValueError as e:
        assert 'Unexpected status bar' in str(e)
    else:
        raise AssertionError('status_bar took a bar with other names')
    # The status images: V2.1's own (hashed), as the iPod's slim glyphs, at the Q2's sizes (Wi-Fi 14, Bluetooth 42, 12).
    from ipod import png_header
    for icon, digest in M1_AUDIT['status_icons'].items():
        path = 'release/assets/default/raw/images/xx/' + icon
        shipped = read('rootfs.squashfs', path)
        assert sha(read('stock.squashfs', path)) == digest and sha(shipped) == manifest['changed_assets'][path]['sha256']
        assert png_header(shipped) == (14 if icon.startswith('bar_wifi') else 42 if icon.startswith('bar_bt') else 12, 16, 8, 6), icon
    assert png_header(read('rootfs.squashfs', 'release/assets/default/raw/images/xx/bar_back.png')) == (32, 30, 8, 6)
    # The play state shows the tap's action: V2.1 picks bar_play while playing (status 2, its faces' only users; no UI file names them), which ships pause's glyph.
    xx = 'release/assets/default/raw/images/xx/'
    m1ipod.STATUS_ICONS = M1_AUDIT['status_icons']
    pause_glyph, play_glyph = (m1ipod.status_icon(n, read('stock.squashfs', xx + n)) for n in ('bar_pause.png', 'bar_play.png'))
    assert play_glyph != pause_glyph and read('rootfs.squashfs', xx + 'bar_play.png') == pause_glyph and read('rootfs.squashfs', xx + 'bar_pause.png') == play_glyph
    for addiu, name in ((0x47589c, b'bar_play'), (0x475934, b'bar_pause'), (0x544d54, b'bar_play'), (0x544dec, b'bar_pause')):
        assert stock[fileoff(stock, 0x744678 if name == b'bar_play' else 0x744684):][:len(name) + 1] == name + b'\0'
        assert struct.unpack_from('<h', stock, fileoff(stock, addiu))[0] == (0x4678 if name == b'bar_play' else 0x4684)
    # ipod-ui 4.6, Now Playing's controls: V2.1's own (hashed), as the iPod's quiet glyphs, 28 px.
    assert set(M1_AUDIT['quiet_icons']) == {f'p_{n}.png' for n in ('fav', 'unfav', 'favdown', 'unfavdown', 'cycle', 'cycle1', 'order', 'random',
                                                                   'more', 'moredown', 'playqueue', 'playqueuedown')}
    for icon, digest in M1_AUDIT['quiet_icons'].items():
        path = 'release/assets/default/raw/images/xx/' + icon
        shipped = read('rootfs.squashfs', path)
        assert sha(read('stock.squashfs', path)) == digest and sha(shipped) == manifest['changed_assets'][path]['sha256']
        assert png_header(shipped) == (28, 28, 8, 6), icon
    # ... and its page: V2.1's tree with the top row, the art slide's text, the dots, the bar, the times and the transport
    # at the layout's places. view_buttons and view_dlna are V2.1's inside.
    np_stock, np_page = (decode(read(i, 'release/assets/default/raw/ui/playing_page.bin')) for i in ('stock.squashfs', 'rootfs.squashfs'))
    np = {n[2].get('name'): n for n in walk(np_page)}
    L = m1plus_ipod.M1
    assert [n[2]['name'] for n in np['view_local'][3]] == ['slide_view_view', 'label_ipod_pos', 'img_hr', 'btn_fav', 'btn_more', 'btn_return', 'slider_play',
                                                           'img_repeata', 'img_repeatb', 'label_playtime', 'label_ipod_remain', 'view_buttons']
    for name, box in {'app_gesture': [0, 0, 320, 450], 'view_local': [0, 0, 320, 450], 'view_dlna': [0, 0, 320, 450],
                      'slide_view_view': [0, L['NP_SLIDE_Y'], 320, L['NP_DOTS_Y'] - L['NP_SLIDE_Y'] + 10],
                      'btn_return': [0, 0, L['NP_BACK_W'], L['NP_TOP_H']], 'btn_more': [320 - L['NP_ICON_W'], 0, L['NP_ICON_W'], L['NP_TOP_H']],
                      'btn_fav': [320 - 2 * L['NP_ICON_W'], 0, L['NP_ICON_W'], L['NP_TOP_H']],
                      'img_playcover': [L['NP_ART_X'], L['NP_ART_Y'] - L['NP_SLIDE_Y'], L['NP_ART'], L['NP_ART']],
                      'scrlabel_title': [L['NP_TEXT_X'], L['NP_TITLE_Y'] - L['NP_SLIDE_Y'], L['NP_TEXT_W'], 28],
                      'scrlabel_artist': [L['NP_TEXT_X'], L['NP_ARTIST_Y'] - L['NP_SLIDE_Y'], L['NP_TEXT_W'], 22],
                      'label_ipod_album': [L['NP_TEXT_X'], L['NP_ALBUM_Y'] - L['NP_SLIDE_Y'], L['NP_TEXT_W'], 22],
                      'slider_play': [L['NP_BAR_X'], L['NP_BAR_CY'] - L['NP_BAR_TOUCH'] // 2, L['NP_BAR_W'], L['NP_BAR_TOUCH']],
                      'label_playtime': [L['NP_BAR_X'], L['NP_TIMES_Y'], 80, 16], 'label_ipod_remain': [320 - L['NP_BAR_X'] - 80, L['NP_TIMES_Y'], 80, 16],
                      'view_buttons': [0, L['NP_BUTTONS_Y'], 320, 66]}.items():
        assert np[name][1] == box, (name, np[name][1])
    assert np[name][1][1] + np[name][1][3] == m1ipod.BOTTOM and L['NP_TOP_H'] <= L['NP_SLIDE_Y'] and L['NP_TIMES_Y'] + 16 == L['NP_BUTTONS_Y']
    assert [n[2]['name'] for n in np['view'][3]] == ['img_playcover', 'scrlabel_title', 'scrlabel_artist', 'label_ipod_album']
    assert np['label_index'][2]['visible'] == np['label_playlen'][2]['visible'] == 'false'
    assert np['slider_play'][2]['style'] == 's_ipod_progress' and all(np['slider_play'][2][f'style:{st}:icon'] == '' for st in ('normal', 'pressed', 'over', 'disable', 'focused'))
    np_old = {n[2].get('name'): n for n in walk(np_stock)}
    assert np['view_buttons'][3] == np_old['view_buttons'][3] and np['view_dlna'][3] == np_old['view_dlna'][3]
    # Centred Now Playing's page: V2.1's, named playing_page, its layout and transport, the iPod's bar and lyrics across their column.
    centred_page = decode(read('rootfs.squashfs', 'release/assets/default/raw/ui/' + m1plus_ipod.PLAYING_STOCK))
    assert centred_page[2]['name'] == 'playing_page' and centred_page[3][0][1] == np_stock[3][0][1]
    centred = {n[2].get('name'): n for n in walk(centred_page)}
    for name in ('slide_view_view', 'img_playcover', 'btn_return', 'scrlabel_title', 'label_playtime', 'view_buttons', 'btn_fav', 'btn_more'):
        assert centred[name][1] == np_old[name][1], name
    assert centred['slider_play'][1] == np_old['slider_play'][1] and centred['slider_play'][2]['style'] == 's_ipod_progress'
    assert centred['view_lrc'][2]['self_layout'] == 'default(x=0,y=0,w=100%,h=-20)' and centred['label_lyricmsg'][2]['self_layout'] == 'default(x=0,y=100,w=100%,h=28)'
    assert m1plus_ipod.playing_stock(read('stock.squashfs', 'release/assets/default/raw/ui/playing_page.bin')) == read('rootfs.squashfs', 'release/assets/default/raw/ui/' + m1plus_ipod.PLAYING_STOCK)
    # Spotify's page shares Now Playing's layout, and Radio keeps its stack.
    S = defines('m1plus_offsets.inc')
    assert [S[f'SPOT_{n}'] for n in 'ART_X ART_Y ART_PX TEXT_X TEXT_W TITLE_Y ARTIST_Y ALBUM_Y BAR_X BAR_W TIMES_Y TIME_X TAG_X'.split()] == [
        L[f'NP_{n}'] for n in 'ART_X ART_Y ART TEXT_X TEXT_W TITLE_Y ARTIST_Y ALBUM_Y BAR_X BAR_W TIMES_Y BAR_X'.split()] + [L['NP_BACK_W'] + 8]
    assert S['SPOT_BAR_Y'] == L['NP_BAR_CY'] - S['SPOT_BAR_H'] // 2 and S['SPOT_BAR_H'] == L['NP_BAR_CLASSIC']
    assert [L[f'RADIO_{n}'] for n in 'ART_X ART_Y ART_PX TITLE_Y TIMES_Y'.split()] == [50, 50, 220, 280, 392]
    # ipod-ui 4.6, the big cover: V2.1's page, full screen, the art a centred square with the shade and title on its foot; the
    # artist transparent, as its refresh (0x52958c) shows it. V2.1 opens it only from Enlarged Art's countdown, whose word and reset
    # are BC_IDLE and BC_IDLE_FULL, and its image names are the ones the payload reads.
    big = decode(read('rootfs.squashfs', 'release/assets/default/raw/ui/bigcover_page.bin'))
    assert big[2]['fullscreen'] == 'true' and [n[2]['name'] for n in big[3]] == ['img_playcover', 'view_shade', 'scrlabel_title', 'scrlabel_artist']
    art_y = (m1ipod.UI_H - m1plus_ipod.BC_ART) // 2
    foot = art_y + m1plus_ipod.BC_ART - m1plus_ipod.BC_SHADE_H
    assert big[3][0][1] == [0, art_y, 320, 320] and big[3][1][1] == [0, foot, 320, m1plus_ipod.BC_SHADE_H] and foot <= big[3][2][1][1] < art_y + 320
    assert big[3][3][2]['opacity'] == '0' and m1plus_ipod.BC_ART == m1ipod.UI_W
    assert words(0x53d0f4, 1) == (0x24020014,) and words(0x53d0fc, 1) == (0xae22ccd0,) and L['BC_IDLE'] == 0x97ccd0 and L['BC_IDLE_FULL'] == 20
    # ... and the volume dialog: clear and full screen for vol_paint, the strip's children hidden; view_page2, V2.1's VOLUME page, as V2.1 has it.
    vol_old, vol = (decode(read(i, 'release/assets/default/raw/ui/dialog/volume_dialog.bin')) for i in ('stock.squashfs', 'rootfs.squashfs'))
    assert 'highlight' not in vol[2] and vol[1] == [0, 0, m1ipod.UI_W, m1ipod.UI_H] and vol[3][1] == vol_old[3][1]
    assert all(vol[2][f'style:{st}:bg_color'] == vol[3][0][2][f'style:{st}:bg_color'] == '#00000000' for st in ('normal', 'disable', 'focused'))
    assert vol[3][0][2]['self_layout'] == 'default(x=0,y=0,w=100%,h=100%)'
    assert [(n[2].get('visible'), n[2].get('opacity')) for n in vol[3][0][3]] == [(None, '0'), ('false', None), ('false', None)]
    for a, w, why in playing['volume_init']:
        assert struct.unpack_from('<I', demo, fileoff(demo, int(a, 16)))[0] == int(w, 16), why
    try:
        m1plus_ipod.playing_page(['window', [0, 0, 0, 0], {'name': 'playing_page'}, []])
    except ValueError as e:
        assert 'Unexpected Now Playing' in str(e)
    else:
        raise AssertionError('playing_page took a page with other names')
    # ipod-ui 4.3, the settings pages. V2.1's list_view layouter (children_layouter_list_view_create) uses the vtable at
    # 0x9047a0: its type name, then the layout slot ipod_list_layout takes (LIST_VIEW_LAYOUT_SLOT) holding
    # LIST_VIEW_LAYOUT.
    assert stock_syms['children_layouter_list_view_create'] == 0x60b79c and words(0x9047a8, 1) == (0x60abb0,)
    vtable_name = words(0x9047a0, 1)[0]
    assert stock[fileoff(stock, vtable_name):fileoff(stock, vtable_name) + 10] == b'list_view\0'
    # V2.1's settings rows have no inner button: a list_item_style list_item holds its children directly, centred on a
    # 60 px body in a 64 px row: a 40 px icon at 12,10, the label at 60,20 (at 12 without an icon), and trailing
    # images that end at x 308 (a 57x28 switch at 251,16, right_arrow 13 px at 295, a 26 px tick at 282,17). Each
    # pinned word is an `li` of one argument (a1 x, a2 y, a3 w) at System Setting's, Playback Setting's, Display's,
    # Bluetooth's, Time zone's and Language's builders.
    def li(reg, value): return 0x24000000 | reg << 16 | value
    shape = {0x4adbcc: li(5, 12), 0x4adbc4: li(6, 10), 0x4adbc0: li(7, 40),  # sysset icon
             0x4adc10: li(5, 60), 0x4adc00: li(6, 20),  # sysset label
             0x4adcdc: li(5, 251), 0x4adcd4: li(6, 16), 0x4adcd0: li(7, 57),  # sysset switch
             0x4a0680: li(5, 12), 0x4a0678: li(6, 10), 0x4a0674: li(7, 40),  # playset icon
             0x4a0778: li(5, 251), 0x4a0770: li(6, 16), 0x4a076c: li(7, 57),  # playset switch
             0x4a5d88: li(5, 12), 0x4a5d80: li(6, 20),  # display's label, no icon
             0x4a30e4: li(5, 295), 0x4a30d8: li(7, 13),  # bluetooth quality's right_arrow
             0x4a2310: li(5, 282), 0x4a2308: li(6, 17), 0x4a2304: li(7, 26),  # time zone's tick
             0x4a7fa0: li(5, 282), 0x4a7f98: li(6, 17), 0x4a7f94: li(7, 26)}  # language's tick
    assert all(words(a, 1) == (w,) for a, w in shape.items()), [hex(a) for a, w in shape.items() if words(a, 1) != (w,)]
    # Its row icons (settings_icons): every 40 px pset_, sset_, system_ and playset_ image, hashed; already SET_ICON
    # square RGBA, so the build ships them as they are, and the image hook leaves their category colours alone.
    import fnmatch
    images = [p for p in re.findall(r'squashfs-root/release/assets/default/raw/images/xx/(\S+\.png)',
                                    subprocess.run(['unsquashfs', '-l', str(directory/'stock.squashfs')], capture_output=True, text=True).stdout)
              if any(fnmatch.fnmatch(p, f'{k}_*') for k in ('pset', 'sset', 'system', 'playset'))]
    square = {p for p in images if png_header(read('stock.squashfs', 'release/assets/default/raw/images/xx/' + p))[:2] == (40, 40)}
    assert set(M1_AUDIT['settings_icons']) == square and len(square) == 43
    for icon, digest in M1_AUDIT['settings_icons'].items():
        path = 'release/assets/default/raw/images/xx/' + icon
        assert sha(read('stock.squashfs', path)) == digest and png_header(read('stock.squashfs', path)) == (40, 40, 8, 6), icon
    # The settings pages as built: each navigationbar_view hidden and disabled, its return button still enabled (back_of
    # and previous_back click it); each list SET_TOP from the bar, its rows SET_ROW, as many complete ones as fit (the
    # Power page's standby slide stops at 434, over its slide indicator). The Lock Screen page keeps its toolbar.
    m1 = m1plus_ipod.M1
    for page in M1_AUDIT['navbar_only']:
        built = decode(read('rootfs.squashfs', 'release/assets/default/raw/ui/' + page))
        navs = [n for n in walk(built) if n[2].get('name', '').startswith('navigationbar_view')]
        lists = [n for n in walk(built) if n[0] == 'list_view']
        if page in m1plus_ipod.SETTINGS_TOOLBAR_SWITCHES:
            assert page not in m1plus_ipod.REWRITES and all(n[2].get('visible') != 'false' for n in navs), page
            continue
        assert navs and all(n[2]['visible'] == n[2]['enable'] == 'false' for n in navs), page
        backs = [b for n in navs for b in n[3] if b[2].get('style') == 'navbar_btnreturn_style']
        assert len(backs) == len(navs) and all(b[2].get('enable') == 'true' for b in backs), page
        for n in lists:
            rows = 5 if n[2]['name'] == 'standby_listview' else m1['SET_ROWS']
            assert n[1][1] == m1['SET_TOP'] and n[1][3] == rows * m1['SET_ROW'] and n[2]['default_item_height'] == str(m1['SET_ROW']), page
            assert [c[1][3] for c in n[3]] == [n[1][3]] * 2, page  # its scroll view and bar, as tall
    assert sum(1 for p in M1_AUDIT['navbar_only'] if p in m1plus_ipod.REWRITES) == 32
    # 4.4: the library pages as built: the title bar hidden and disabled (Playlists keeps its own, as the Q2's does), the
    # list from the top to BOTTOM (Playlists' under its bar), its children as tall (or following it, h=100%), rows
    # LIB_PITCH (an album's 154 px header default aside) and the table clients the screen's width.
    for page in m1plus_ipod.LIBRARY_PAGES:
        built = decode(read('rootfs.squashfs', 'release/assets/default/raw/ui/' + page))
        nav, = [n for n in built[3] if n[2].get('name') == 'navigationbar_view']
        lst, = [n for n in built[3] if n[0] in ('list_view', 'table_view')]
        top = 50 if page == 'playlist_page.bin' else 0
        assert (nav[2].get('visible') == nav[2].get('enable') == 'false') == (page != 'playlist_page.bin'), page
        assert lst[1][1] == top and lst[1][3] == m1ipod.BOTTOM - top, page
        assert lst[2].get('self_layout') in (None, f'default(x=0,y={top},w=100%,h={m1ipod.BOTTOM - top})'), page  # Folders' places itself
        assert all(c[1][3] == lst[1][3] or 'h=100%' in c[2].get('self_layout', '') for c in lst[3]), page
        assert {n[2][k] for n in walk(built) for k in ('row_height', 'default_item_height') if k in n[2]} <= {str(m1ipod.PITCH), '154'}, page
        assert all(n[1][2] == m1ipod.UI_W for n in walk(built) if n[0] == 'table_client'), page
        assert all(n[1][3] == m1ipod.PITCH and n[2].get('self_layout') == f'default(w=100%,h={m1ipod.PITCH})'
                   for n in walk(built) if n[0] == 'table_row'), page
    # System Setting in the iPod order (m1plus_nav_sysset.c sysset_ipod_order). V2.1's builder makes a row per
    # syssetMenu entry (0..14, or 15 with sset_prove), names it by its index and draws get_systemset_showinfo's icon:
    # one of two tables, memcpy'd by a GPIO, which differ only in Double Tap's. The rows' click
    # (on_syssetback_onclick) reads the name back with atoi and indexes syssetMenu, so a restacked row keeps its click.
    def cstr(a): return stock[fileoff(stock, a):stock.index(b'\0', fileoff(stock, a))].decode()
    tables = [[cstr(p) for p in words(t, 16)] for t in (0x97c988, 0x97c9c8)]
    assert words(stock_syms['syssetMenu'], 16) == tuple(range(16))
    assert tables[0] == ['system_language', 'sset_wifiset', 'sset_netservice', 'sset_display', 'sset_powermanager', 'system_time',
                         'sset_carmode', 'sset_tswake', 'sset_keylock', 'system_scrotate', 'sset_theme', 'system_update',
                         'system_formatcard', 'system_reset', 'sset_about', 'sset_prove']
    assert tables[1] == tables[0][:7] + ['sset_doublewake'] + tables[0][8:]
    showinfo = stock_syms['get_systemset_showinfo']
    assert words(showinfo + 0x70, 1)[0] & 0xffff == 0x10000 - 0x3678 and words(showinfo + 0xb4, 1)[0] & 0xffff == 0x10000 - 0x3638
    assert got(showinfo + 0x80) == 0x743570  # strcpy(buf, table[id])
    click = stock_syms['on_syssetback_onclick'] + 0x260  # the row click (0x4ad7b0), bound at 0x4adde0
    assert click == 0x4ad7b0 and words(0x4adde8, 1)[0] & 0xffff == 0x10000 - 0x2850 and got(0x4adddc) == 0x4b0000
    assert got(0x4ad7c0) == 0x7435b0 and words(0x4ad7e0, 1) == (0x8c840010,) and got(0x4ad7f0) == stock_syms['syssetMenu']  # atoi(name)
    sysset_c = (ROOT/'patch/m1plus_nav_sysset.c').read_text()
    roles = re.findall(r'"(\w+)"', sysset_c[sysset_c.index('sysset_roles[]'):sysset_c.index('#define SYSSET_ROLES')])
    assert set(roles) == set(tables[0] + tables[1]) - {'sset_prove'} and len(roles) == 16, roles
    # ipod-ui 4.4, the Library. V2.1's library rows: each builder's own constructor makes a row 60 high (Folders' 64), and
    # All Songs' and the class lists' an inner button 56 high (Folders' 60) that holds the row's children. Each row's
    # children are laid out by its own default(r=1,c=0,...) layouter (one row, every child its height), set by a jalr
    # widget_set_children_layout with the params a GOT page plus an addiu: All Songs (music_create_tablerow), the class
    # lists (localclass_create_tablerow), Folders (folder_create_tablerow), Albums (album_listitem_layout, x=0, the cover
    # flush left), an album's tracks (albumdeinfo_listitem_layout) and Playlists (playlist_listitem_layout). All Songs'
    # title and its artist line, and Albums' two lines, sit in a text view at fixed y: 10 and 30, and 10 and 32.
    def li(reg, value): return 0x24000000 | reg << 16 | value
    library = {'music_create_tablerow': {0x528570: li(2, 60), 0x5285a0: li(17, 56), 0x528734: li(6, 10), 0x5287b8: li(6, 30)},
               'localclass_create_tablerow': {0x5368bc: li(2, 60), 0x5368e8: li(17, 56)},
               'folder_create_tablerow': {0x53320c: li(2, 64), 0x533238: li(17, 60)},
               'album_listitem_layout': {0x5245f0: li(2, 60)},  # list_item_create's h, for album_listitem_layout's row
               'airplay_page_init': {0x522918: li(6, 10), 0x5229c0: li(6, 32)},  # Albums' text view (0x52289c)
               'albumdeinfo_listitem_layout': {0x52667c: li(2, 60)}}
    for fn, sites in library.items():
        start = stock_syms[fn]
        for a, w in sites.items():
            assert start < a < start + 0x1000 and words(a, 1) == (w,), (fn, hex(a))
    layouts = {0x528624: 'default(r=1,c=0,x=12,s=8)', 0x53696c: 'default(r=1,c=0,x=12,s=8)', 0x5332bc: 'default(r=1,c=0,x=12,s=8)',
               0x524494: 'default(r=1,c=0,x=0,s=8)', 0x52651c: 'default(r=1,c=0,x=12,s=8)', 0x53e6ec: 'default(r=1,c=0,x=12,s=8)'}
    for call, params in layouts.items():
        assert words(call, 1) == (0x0320f809,) and got(call - 4) == stock_syms['widget_set_children_layout'] and \
            compared(call - 8, call + 4)[1] == params.encode(), hex(call)
    # V2.1's default children layouter: a 0x1c-byte children_layouter_default_t whose children_layouter_t holds a 12-byte
    # str_t, so the vtable (0x904924, "default", its layout at [2]) is at 0xc, rows and cols at 0x10 and 0x12, and the x,
    # y and spacing bytes at 0x14, 0x15 and 0x16 (set_param's switch on the key's letter, its jump table at 0x75c420).
    create = stock_syms['children_layouter_default_create']
    assert words(create + 0x1c, 1) == (0x2405001c,) and words(create + 0x6c, 2) == (0x24424924, 0xae02000c)  # calloc 0x1c; vt @0xc
    assert m1plus_inc('DEFAULT_LAYOUT_VTABLE') == 0x904924 and cstr(words(0x904924, 1)[0]) == 'default' and words(0x904924 + 8, 1) == (0x63a444,)
    assert m1plus_inc('CHILDREN_LAYOUT_VTABLE') == 0xc and m1plus_inc('DEFAULT_LAYOUT_X_MARGIN') == 0x14 and m1plus_inc('DEFAULT_LAYOUT_SPACING') == 0x16
    params = {chr(97 + i): (w + M1PLUS_GP) & 0xffffffff for i, w in enumerate(struct.unpack_from('<25i', stock, fileoff(stock, 0x75c420)))}
    assert words(params['x'], 2) == (0x1000fff0, 0xa2020014) and words(params['y'], 2) == (0x1000ffec, 0xa2020015)
    assert words(params['s'], 2) == (0x1000ffea, 0xa2020016)  # b out; sb v0, 0x14/0x15/0x16(s0)
    # The rows' rebinds: Folders' (0x532f6c) and an album's tracks' (0x527918) resize the row's label each time (200 or
    # 220, and 200 or 250, by multi-select), as the Q2's folder rebind does (0x522410).
    for call in (0x532f6c, 0x527918):
        assert words(call, 1) == (0x0320f809,) and got(call - 8) == stock_syms['widget_resize'], hex(call)
    # Search: the library title bar's Search button (search_style, at 183) opens V2.1's search_page; its click
    # (0x523304) is navigator_to("search_page"), which pull to search calls (stock_search).
    assert M1PLUS_PRIVATE_FUNCTIONS['stock_search'] == 0x523304 and got(0x523318) == stock_syms['navigator_to'] and compared(0x523314, 0x523328)[1] == b'search_page'
    assert compared(0x52307c, 0x523088)[1] == b'search_style' and got(0x5230a0) == stock_syms['widget_on'] and \
        words(0x52308c, 1) == (0x2405010c,) and words(0x5230a8, 1)[0] & 0xffff == 0x3304 and got(0x52309c) == 0x520000
    # Hold: AWTK's key-down arms a 1000 ms timer (0x6a48a0) for every key; it sends EVT_KEY_LONG (0x110) for a key held
    # 1000 ms or more. on_wm_keylong_fun (ringnav_keylong) acts on the power key's (0xd2) alone, so Previous's
    # (KEY_BACK_BTN, or KEY_FWD_BTN rotated) does nothing in stock.
    assert words(0x6a4778, 1) == (0x240603e8,) and got(0x6a4780) == stock_syms['timer_add'] and words(0x6a4964, 1) == (0x2c4203e8,)
    assert words(0x6a497c, 1) == (0x24050110,) and m1plus_inc('EVT_KEY_LONG') == 0x110
    keylong = stock_syms['on_wm_keylong_fun']
    assert [w & 0xffff for w in words(keylong, 0x10c // 4) if w >> 16 == 0x2403] == [2, 0xd2, 1, 10]  # standby and car mode 2, the key 0xd2
    assert words(0x534fbc, 1) == (0x24050113,) and got(0x534fc0) == stock_syms['widget_on'] and got(0x534fc4) == stock_syms['on_wm_keyup_fun']
    bound = {w & 0xffff for w in words(stock_syms['home_page_init'], 984 // 4) if w >> 16 == 0x2405}  # li $a1, event
    assert {0x10f, 0x111, 0x113} & bound == {0x113}, 'home_page_init binds a key-down handler'
    assert words(0x4cdbf4, 2) == (0x2443ff24, 0x2c630002) and compared(0x4cdc34, 0x4cdc44)[1] == b'dialog/volume_dialog'
    assert b'buzzer' not in stock and b'cmd_mcu' not in stock
    # Coverflow's worker (coverflow.c build_art) holds parse_cover_mutex alone on M1: V2.1 has no
    # player cover lock. Its toolsGetAlbumCover calls (lw $t9 from its GOT slot) are the three in
    # parse_albumcovertask_thd and the one in parseplaycover_thd, which locks parse_cover_mutex first.
    text = next(p for _, p in segments(stock) if p[0] == 1 and p[6] & 1)  # the executable LOAD segment
    calls = [text[2] + i for i in range(0, text[4], 4) if struct.unpack_from('<I', stock, text[1] + i)[0] == 0x8f99b87c]
    assert got(0x4df1e8) == stock_syms['toolsGetAlbumCover'] and calls == [0x4dd6a4, 0x4de894, 0x4de95c, 0x4df1e8]
    assert all(stock_syms['parse_albumcovertask_thd'] <= c < stock_syms['parseplaycover_thd'] for c in calls[:3])
    assert words(0x4df1c4, 3) == (0x8f99f8b4, 0x8f84b878, 0x0320f809) and got(0x4df1c8) == stock_syms['parse_cover_mutex']
    assert got(0x4df1c4) == stock_syms['pthread_mutex_lock@GLIBC_2.0'] and stock_syms['parseplaycover_thd'] < 0x4df1c4 < 0x4df1e8
    # now_tag's ID3_ALBUM_ARTIST (coverflow.c): toolsGetMusicInfo fixes id3 field 6 (li $v1, 6) and
    # copies it to info+0x580 (addiu $a0, $s2, 0x580), MUSIC_INFO_ALBUM_ARTIST, as V1.32 does.
    assert stock_syms['toolsGetMusicInfo'] < 0x5ecba0 and words(0x5ecba0, 1) == (0x24030006,) and words(0x5ecbc4, 1) == (0x26440580,)
    # The online searches (onlinematch.c) read stock's keyinfo as online_setkeyword_info fills it: the
    # title at +0x200, the album at +0x400 and the artist at +0x500 (addiu $a0, $s0, ...; $s0 keyinfo).
    assert got(0x50b49c) == stock_syms['keyinfo'] and words(0x50b4d4, 1) == (0x26040200,)
    assert words(0x50b4f0, 1) == (0x26040400,) and words(0x50b50c, 1) == (0x26040500,)
    # radio.c's and spotify.c's Search take the keyboard's OK as EVT_IM_ACTION: V2.1's
    # input_method_dispatch_action dispatches 0x13c (li $a1), V1.32's 0x13a.
    assert words(stock_syms['input_method_dispatch_action'] + 0x14, 1) == (0x2405013c,)
    # V2.1's names for two V1.32 routines (M1PLUS_FUNCTION_ALIASES), each called where V1.32 calls its
    # twin: folder_back's bal clear_foldervariate (folder_reset_variable) and delete_playqueue_file's
    # bal start_playqueue (player_start_queue).
    def bal(site, name): return words(site, 1)[0] == 0x04110000 | ((stock_syms[name] - site - 4) >> 2) & 0xffff
    # 1.7.0's oversized-Ogg tag path uses V2.1's own converter. Its six native tag reads
    # load the same GOT entry before passing the Latin-1 flag, both strings, output and field kind.
    assert stock_syms['toolsFixId3ErrorCode'] == 0x5ec460
    for site in (0x5ec8c0, 0x5ec958, 0x5ec9f0, 0x5eca88, 0x5ecb20, 0x5ecbb8):
        assert words(site, 1) == (0x8f99c770,) and got(site) == stock_syms['toolsFixId3ErrorCode']
    # usbmode_page_init branches to DAC handling on usb_mode == 1 (lb; li 1; bne).
    assert got(0x545e64) == stock_syms['usb_mode'] == 0xa05aa8
    assert words(0x545e68, 3) == (0x80430000, 0x24020001, 0x14620067)
    assert bal(0x4dbf0c, 'clear_foldervariate') and stock_syms['folder_back'] < 0x4dbf0c
    assert bal(0x4e4a80, 'start_playqueue') and stock_syms['delete_playqueue_file'] < 0x4e4a80
    # Library -> Songs (songs_load, 1.6.3): loadLocalClassList's default branch calls getAllMusic, then
    # musicNagvationTitle (music_nagvation_title) with 0xf001 (ori $a0); V2.1's getAllMusic reads sort_flag
    # (g_sort_flag) itself, so the payload's argument is ignored.
    assert bal(0x4ee5c0, 'getAllMusic') and bal(0x4ee5d4, 'musicNagvationTitle') and words(0x4ee5c8, 1) == (0x3404f001,)
    assert stock_syms['loadLocalClassList'] < 0x4ee5c0 and got(0x4ea374) == stock_syms['sort_flag']
    # MQA_ACCEPT (1.6.3): mclWaitAccept's jalr is accept's, and a positive descriptor goes to MCL_FD's
    # word (sw $v0, -0x5414($s4)) after it, as V1.32's does.
    assert got(0x5d0020) == stock_syms['accept@GLIBC_2.0'] and stock_syms['mclWaitAccept'] < 0x5d0030
    assert words(0x5d0038, 3) == (0x18400002, 0x8fbc0010, 0xae82abec)
    # online_lyricthd: the hooked search (kugou_obtainlyric), NetEase's com163_obtainlyric on a miss and
    # again after either; LYRIC_SOURCES branches a find to the thread's end (li $v1, 1), past both.
    assert bal(0x50a1b8, 'kugou_obtainlyric') and bal(0x50a1d0, 'com163_obtainlyric') and bal(0x50a1e4, 'com163_obtainlyric')
    assert stock_syms['online_lyricthd'] < 0x50a1b8 and words(0x50a1ec, 1) == (0x24030001,)
    # ringnav_localclass takes an artist's albums by CLASS_ARTIST_ALBUMS (artist_tab): V2.1's loadAlbumList
    # stores 0xff01 in classinfo_save (ori $v0, 0xff01; sw $v0, 0($s0)) and branches to loadLocalClassList.
    assert words(0x4ee930, 1) == (0x3402ff01,) and words(0x4ee93c, 1) == (0xae020000,)
    assert words(0x4ee9a8, 1)[0] == 0x10000000 | ((stock_syms['loadLocalClassList'] - 0x4ee9ac) >> 2) & 0xffff
    # SCAN_REFRESH: toolsLoadAllFile's bal toolsCheckItemExist, V1.32's word.
    assert bal(0x5eff54, 'toolsCheckItemExist') and stock_syms['toolsLoadAllFile'] < 0x5eff54
    # FOLDER_NAME: the folder row's text (0x532e34, a PIC entry bal'd from 0x533124, V1.32's 0x522304):
    # tk_snprintf at -0x5798, tk_strncpy at -0x3300 from V2.1's GOT base.
    def slot(offset): return struct.unpack_from('<I', stock, fileoff(stock, M1PLUS_GP + offset))[0]
    assert got(0x532ec0) == stock_syms['tk_snprintf'] and slot(-0x3300) == stock_syms['tk_strncpy']
    assert words(0x533124, 1)[0] == 0x04110000 | ((0x532e34 - 0x533128) >> 2) & 0xffff
    assert words(0x532e34, 3) == (0x3c1c004d, 0x279c109c, 0x0399e021)  # gp = 0xa03ed0
    # ID3_PATH: get_id3info's strcpy(playsong_id3info, record->path), the id3 info ringnav_id3_path fills.
    assert got(0x4dff40) == stock_syms['strcpy@GLIBC_2.0'] and got(0x4dff44) == stock_syms['playsong_id3info']
    assert stock_syms['get_id3info'] < 0x4dff4c and words(0x4dff50, 1) == (0x8e05000c,)  # lw $a1, REC_PATH($s0)
    # GRID_COVER: the Albums grid's toolsGetAlbumCover (0x4dd6a4's lw) goes on to toolsGetExternCover, Folder view's don't.
    assert got(0x4dd6c0) == stock_syms['toolsGetExternCover'] and words(0x4de8a4, 1) == words(0x4de960, 1) == (0x0320f809,)
    # PLAYER_COVER: parseplaycover_thd's toolsGetExternCover after its toolsGetAlbumCover (0x4df1e8) missed.
    assert got(0x4df218) == stock_syms['toolsGetExternCover'] and stock_syms['parseplaycover_thd'] < 0x4df1e8 < 0x4df218
    # LYRIC_FOLLOW: Now Playing's timer's scroll_view_scroll_to(scroll_lrc, 0, y, 10).
    assert got(0x53ad54) == stock_syms['scroll_view_scroll_to'] and words(0x53ad58, 1) == (0x2407000a,)  # li $a3, 10
    # LYRIC_ROWS: show_player_face's bal to the lyric row builder, a PIC entry that zeroes scroll_lrc's
    # offset (scroll_view_set_offset) before it reads the lyrics.
    assert words(0x53bed0, 1)[0] == 0x04110000 | ((0x53a240 - 0x53bed4) >> 2) & 0xffff and stock_syms['show_player_face'] < 0x53bed0
    assert pic_gp(stock, 0x53a240) == M1PLUS_GP and got(0x53a3e4) == stock_syms['scroll_view_set_offset']
    assert got(0x53a42c) == stock_syms['mclGetLyricBuffer'] and got(0x53a568) == stock_syms['mclGetLyricTime']
    # BT_INIT, BT_PARAMS, BT_STATUS and BT_AUTOLINK: V1.32's calls in V2.1's platform_init, config_bt_init,
    # openBluetooth (its two callbacks PIC entries, the a2dp one btrecvA2dpFunc) and autoLinkBluetooth.
    assert got(0x50be24) == stock_syms['btctl_create_daemon_thread'] and stock_syms['platform_init'] < 0x50be28
    assert bal(0x4d6ae4, 'initBluetoothParam') and stock_syms['config_bt_init'] < 0x4d6ae4
    assert got(0x4d2cec) == stock_syms['btctl_device_status_callback'] and got(0x4d2cd4) == stock_syms['btctl_set_prompt_callback']
    assert slot(-0x4d4c) + 0x4738 == 0x4d4738 and words(0x4d2cdc, 1) == (0x24842310,) and stock_syms['openBluetooth'] < 0x4d2cd8
    assert pic_gp(stock, 0x4d4738) == pic_gp(stock, 0x4d2310) == M1PLUS_GP and got(0x4d2d04) == stock_syms['btrecvA2dpFunc']
    assert bal(0x4d44e4, 'checkPairDev') and stock_syms['autoLinkBluetooth'] < 0x4d44e4
    # BTLINKMAC: readBtLinkMac's buffer, its GOT page and offset
    assert words(0x4d2800, 1) == (0x8f9082c0,) and slot(-0x7d40) == 0xa00000 and words(0x4d280c, 1) == (0x261041d0,)
    # FOLDER_PLAY: the Folder file click's navigator_to_with_context("playing_page", ...), after its loadSongList.
    def cstr(at): return stock[fileoff(stock, at):stock.index(b'\0', fileoff(stock, at))]
    assert got(0x531e7c) == stock_syms['navigator_to_with_context'] and got(0x531e48) == stock_syms['loadSongList']
    assert words(0x531e88, 1) == (0x24845b14,) and cstr(slot(-0x58f8) + 0x5b14) == b'playing_page'  # $a0 from -0x58f8's page
    # Coverflow's covers and the photo viewer take the touch on their own view (navigation.c
    # slide_swipe): V2.1's slide_menu steps by its height, not an item and a spacer. Its scroll-done
    # (0x6123f4, through 0x612360) commits round(xoffset @0x88 / h @0xc); its own drag stores
    # xdown (@0x84) on the press and sets xoffset to x - xdown, the finger's px one for one, once it
    # has moved 10 px.
    assert words(0x6123a0, 4) == (0x8c620088, 0x44820000, 0x8e02000c, 0x44820800)
    assert words(0x6125c8, 1) == (0xae020084,) and words(0x612970, 1) == (0x2842000a,)
    assert words(0x6128f0, 3) == (0x8e030084, 0x8e220018, 0x00431023) and words(0x612914, 1) == (0xae020088,)
    # The payload readies the headphone DAC (books.c dac_take) through set_outputchannel, whose third
    # argument V1.32's lacks: on the output path it calls mclSetDacPwr(a2 ? 100 : 1) (0x4d6fd4), and
    # only 1 powers the DAC on in full, its FPGA loaded (0x4d1a 1, toolsDownFpgafirmware, 0x4d1a 2).
    # start_player passes 0 (0x4e4688).
    assert words(0x4d6fd4, 3) == (0x24040064, 0x16000002, 0x8fbc0010) and words(0x4d6fe0, 1) == (0x24040001,)
    assert got(0x4d6fe4) == stock_syms['mclSetDacPwr'] and words(0x4e4688, 1) == (0x00003025,)
    assert words(0x5d5c74, 3) == (0x24030001, 0x24a54d1a, 0x14430034) and got(0x5d5cb0) == stock_syms['toolsDownFpgafirmware']
    # Bluetooth absolute volume hooks mclSetVol (navigation.c ringnav_btvol): V2.1 has no
    # mclSetLocalVol or mclSetBtVol, and its mclSetVol issues the DAC's volume ioctl (0xc0044d00)
    # and sends hciplayer {mcl-setvol%d}. set_devicevolume calls it with 0-100 (its clamps); the
    # private routine mclStartPlayer and mcl_tidalStartPlayer call (0x5d4e00) sends 255, 255,
    # which the hook passes to stock. Bluetooth's end stops the player, changes the output and
    # resets the volume before playing again, so the DAC is never left at 100 for the jack.
    assert 'mclSetLocalVol' not in stock_syms and 'mclSetBtVol' not in stock_syms
    assert words(0x5d4cf4, 1) == (0x3c05c004,) and words(0x5d4d04, 1) == (0x24a54d00,)
    assert compared(0x5d4d48, 0x5d4d54)[1] == b'{mcl-setvol\\%d}'
    assert got(0x4d6d40) == got(0x4d6e8c) == got(0x5d50bc) == stock_syms['mclSetVol']
    # V2.1's Home grid, which the iPod Home (ipod-ui 4.5) replaces: its pages are gone, but its init and refresh still
    # run its builder (pinned in m1plus_ipod.json home.safe_returns, returning with no home_sview). Its builder (0x534064)
    # lays pdeq_choicemenu's ids six to a page (li $s0, 6), each page a view_create(home_sview, 0, 0,
    # 320, 364) and home_sindicator's max set to the pages; each card (0x533d8c) a 154x118 view, two
    # columns from x 6, rows 0, 118 and 236, holding a 66 px image at 44, 20 and a 154x36 label at 0,
    # 92 in label_centerwhitehome_white. A card's click (0x533b80) reads atoi(name) as one of 18 ids.
    assert got(0x534100) == stock_syms['pdeq_choicemenu'] and words(0x5340f0, 1) == (0x24100006,)
    assert compared(0x5340a8, 0x5340b0)[1] == b'home_sview' and compared(0x5340c4, 0x5340d0)[1] == b'home_sindicator'
    assert words(0x534168, 2) == (0x2402016c, 0x24070140) and got(0x534140) == stock_syms['view_create']
    assert got(0x534144) == stock_syms['slide_indicator_set_max']
    assert words(0x533dc0, 1) == (0x24140006,) and words(0x534010, 1) == (0x2694009a,)  # x 6, + 154 a column
    assert words(0x533e14, 2) == (0x24020076, 0x2407009a) and got(0x533e10) == stock_syms['view_create']
    assert words(0x534058, 1) == (0x24030076,) and words(0x534008, 1) == (0x240300ec,)  # rows at 118, 236
    assert words(0x533e8c, 1) == (0x24020042,) and words(0x533e94, 2) == (0x24070042, 0x24060014)
    assert words(0x533ea0, 1) == (0x2405002c,) and got(0x533ea4) == stock_syms['image_create']
    assert words(0x533f80, 1) == (0x24020024,) and words(0x533f88, 2) == (0x2407009a, 0x2406005c)
    assert got(0x533f98) == stock_syms['label_create'] and compared(0x533fb0, 0x533fbc)[1] == b'label_centerwhitehome_white'
    assert words(0x533f60, 1) == (0x2405010c,) and got(0x533b90) == stock_syms['atoi@GLIBC_2.0'] and words(0x533ba8, 1) == (0x2c430012,)
    # The grid is rebuilt only from home_page_init and from Home's refresh (0x534858, when
    # homemenu_changeflag is 2), which its to-foreground handler (0x534b88, bound to 0x12d) runs:
    # Nothing loaded points to the builder (.pdr, which isn't loaded, describes it).
    def bal(i):
        x = struct.unpack_from('<I', stock, text[1] + i)[0]
        return x >> 16 == 0x0411 and text[2] + i + 4 + 4 * struct.unpack_from('<h', stock, text[1] + i)[0] == 0x534064
    assert [text[2] + i for i in range(0, text[4], 4) if bal(i)] == [0x5348d0, 0x534de4]
    loaded = [stock[o:o + f] for _, (t, o, _, _, f, *_) in segments(stock) if t == 1]
    assert stock_syms['home_page_init'] <= 0x534de4 and not any(struct.pack('<I', 0x534064) in p for p in loaded)
    assert words(0x534e0c, 1) == (0x2405012d,) and words(0x534c40, 1) == (0x27394858,)  # 0x12d; the refresh
    assert words(0x4d6e64, 1) == (0x28820065,) and words(0x4d6e7c, 1) == (0x28a20065,)  # slti 101
    assert words(0x5d50c0, 3) == (0x240400ff, 0x0411fefa, 0x240500ff)  # li $a0, 255; bal mclSetVol; li $a1, 255
    order = [stock_syms[n] for n in ('save_stop_player', 'set_outputchannel', 'set_devicevolume', 'save_start_player')]
    for name, size, times in (('checkBluetoothStatus', 2800, 3), ('switchBluetooth', 412, 1)):
        start = stock_syms[name]
        callees = [got(a) for a in range(start, start + size, 4) if words(a, 1)[0] >> 16 == 0x8f99]  # lw $t9, GOT
        assert [c for c in callees if c in order] == order * times, name
    # Bluetooth keeps its own level (navigation.c BT_VOLUME): on headset_output 2 the volume dialog
    # (on_volume_tsup_fun) steps btsource_volume and saves it as [PLAYSET] BTVOLUME, the jacks' volume
    # as VOLUME. Its refresh (volume_refresh) and the status bar show the output's level.
    volume, bt = stock_syms['volume'], stock_syms['btsource_volume']
    assert got(0x47df18) == got(0x47d698) == stock_syms['headset_output'] and words(0x47df30, 1) == words(0x47d6a0, 1) == (0x24020002,)
    assert got(0x47df3c) == bt and words(0x47df5c, 1) == (0xae240000,) and got(0x47df70) == stock_syms['write_int_config']  # sw $a0, 0($s1)
    assert compared(0x47df64, 0x47df68)[1] == b'BTVOLUME' and compared(0x47df6c, 0x47df7c)[1] == b'PLAYSET'
    assert got(0x47dff0) == volume and compared(0x47e028, 0x47e030)[1] == b'VOLUME'
    assert got(0x47d674) == volume and got(0x47d6ac) == bt and got(0x544db0) == bt
    assert got(0x47d768) == stock_syms['progress_bar_set_value'] and got(0x47d8a8) == stock_syms['slider_set_value']
    # The hold menu is V2.1's sortselect_dialog (navigation.c qm_sortselect_init). V2.1's navigator
    # (0x4d00c0, navigator_to's) runs its init, and when that returns 0 tail-calls dialog_modal for a
    # dialog whose to_modal reads set, by default: V2.1's init sets no property, and the asset has
    # none, so without the hook navigator_to would return only once the menu had closed. The popup is
    # 260 px wide (offsets.inc SORTSELECT_W).
    sortselect = stock_syms['dialog_sortselect_dialog_init']
    assert got(0x4d0200) == sortselect and words(0x4d0214, 2) == (0x1040ffda, 0x8f99b494)  # beqz $v0 to the check
    assert got(0x4d0198) == stock_syms['widget_get_prop_bool'] and words(0x4d0194, 1) == (0x24060001,)  # default 1
    assert compared(0x4d0190, 0x4d01a4)[1] == b'to_modal' and got(0x4d01b4) == stock_syms['dialog_modal']
    setters = {stock_syms[n] for n in ('widget_set_prop', 'widget_set_prop_int', 'widget_set_prop_bool') if n in stock_syms}
    assert not setters & {got(a) for a in range(sortselect, sortselect + 720, 4) if words(a, 1)[0] >> 16 == 0x8f99}
    asset = read('rootfs.squashfs', 'release/assets/default/raw/ui/dialog/sortselect_dialog.bin')
    assert b'to_modal' not in asset and b'default(x=c,y=m,w=260,h=360)' in asset
    for old, new in (RTC_WRITE, RTC_READ_M1PLUS, LOCK_CLOCK_12H, WIFI_LPS):  # same-length literals in place
        at = stock.index(old)
        assert stock.count(old) == 1 and len(new) == len(old) and demo[at:at+len(old)] == new, old
        allowed.update(range(at, at+len(old)))
    off, size = PDR_M1PLUS  # .pdr, past every LOAD segment, ships zeroed
    assert demo[off:off+size] == bytes(size) and any(stock[off:off+size])
    assert all(p[1]+p[4] <= off for _, p in segments(stock) if p[0] == 1)
    allowed.update(range(off, off+size))
    off = fileoff(stock, 0x9047a8)  # the list_view layout slot (patch_code)
    assert demo[off:off+4] == struct.pack('<I', ps['ipod_list_layout'])
    allowed.update(range(off, off+4))
    for edit in manifest['compact_code']:  # 4.4's library words (patch_code), each as the manifest lists it
        off = fileoff(stock, int(edit['address'], 16))
        assert struct.unpack_from('<I', stock, off)[0] == int(edit['original'], 16) and struct.unpack_from('<I', demo, off)[0] == int(edit['patched'], 16)
        allowed.update(range(off, off+4))
    # The payload: stock's final PT_NULL header becomes its LOAD segment, R/W/X at BASE, after stock's bytes.
    old_segs, new_segs = segments(stock), segments(demo)
    assert [h for h, _ in old_segs] == [h for h, _ in new_segs] and [p for _, p in old_segs[:-1]] == [p for _, p in new_segs[:-1]]
    assert old_segs[-1][1][0] == 0
    start = (len(stock) + 65535) & ~65535
    # mapped to the payload ELF's end, past __scratch_end: link.ld leaves orphan .bss after .scratch (m1plus.build)
    payload_end = max(v + m for _, (t, _, v, _, _, m, _, _) in segments((directory/'patch.elf').read_bytes()) if t == 1)
    assert payload_end >= ps['__scratch_end']
    assert new_segs[-1][1] == (1, start, BASE, BASE, len(payload), payload_end - BASE, 7, 65536)
    assert demo[len(stock):start] == bytes(start - len(stock)) and demo[start:] == payload
    allowed.update(range(new_segs[-1][0], new_segs[-1][0] + 32))
    def stray(image):
        changed = set()
        for block in range(0, len(stock), 4096):
            if stock[block:block+4096] != image[block:block+4096]:
                changed.update(i for i in range(block, min(block+4096, len(stock))) if stock[i] != image[i])
        return sorted(changed - allowed)
    assert not stray(demo), f'demo differs from V2.1 outside the audited sites: {[hex(i) for i in stray(demo)[:8]]}'
    damaged = bytearray(demo)  # one changed .text word next to a hook is caught
    damaged[fileoff(stock, M1PLUS_HOOKS['on_wm_keyup_fun'][0]) + 8] ^= 1
    assert stray(damaged), 'The demo audit accepted an unaudited change'
    # rootfs: the same files as V2.1 but for the ones build.py replaces, adds and removes.
    xx = 'release/assets/default/raw/images/xx/'
    added = {xx+n for n in ICONS} | {xx+f'local_{n}.png' for n in ('shuffle', 'scrobble', 'podcasts', 'audiobooks', 'photos',
                                                                    'books', 'videos', 'longsongs', 'era')} | {
             xx+f'stream_{n}.png' for n in ('spotify', 'radio', 'airplay')} | {HELPER, SCROBBLE_CA, BOOT} | ({REMOTE} if manifest['dev'] else set())
    added |= {xx+'bar_back.png'}  # the status bar's back chevron (ipod-ui 4.2)
    added |= {xx+f'row_{n}.png' for n in ('spotify', 'radio', 'stream_config')}  # the Q2 Pod page's Streaming rows, at 40 px
    added |= {xx+'stream_app.png'}  # its card apps' rows (addon.c), at 40 px too
    # The Library's Ratings and Most Played row icons; the iPod Home's (ipod-ui 4.5) Carousel card art, pressed too, its
    # arrows, and Split's placeholder.
    added |= {xx+f'{n}.png' for n in ('local_fav', 'local_frequentplay', 'home_left', 'home_right', 'default_album_home')}
    added |= {xx+f'home_card_{row}{s}.png' for row in m1ipod.HOME_ROWS for s in ('', '_down')}
    added.add('release/assets/default/raw/ui/' + m1plus_ipod.PLAYING_STOCK)  # Centred Now Playing (4.6)
    replaced = {'release/bin/demo', 'usr/bin/hciplayer', BLUEALSA, BLUEALSA2, WATCHDOG, S90PLAY, S11LOGO, TAG_C} | {
        'release/assets/default/raw/' + p for p in [*('ui/' + q for q in m1plus_ipod.REWRITES), *('styles/' + q for q in M1_AUDIT['styles']),
                                                                      *('images/xx/' + q for q in {**M1_AUDIT['status_icons'], **M1_AUDIT['quiet_icons']})]}
    logo = xx+'logo.jpg'
    with tempfile.TemporaryDirectory(prefix='m1-rootfs-') as tmp:
        trees = {}
        for image in ('stock.squashfs', 'rootfs.squashfs'):
            run('unsquashfs', '-q', '-no-xattrs', '-d', f'{tmp}/{image}', directory/image)
            files = trees[image] = {}
            for root, dirs, names in os.walk(f'{tmp}/{image}'):
                for name in dirs + names:
                    path = os.path.join(root, name)
                    files[os.path.relpath(path, f'{tmp}/{image}')] = path
        old, new = trees['stock.squashfs'], trees['rootfs.squashfs']
        # No V2.1 page holds a slide_menu (V1.32's Home and settings menus did): the payload's
        # Coverflow and photo viewer are the M1's only ones, so the Q2's next and previous on other
        # slide menus have nothing to act on (test/m1plus/patch.py, Q2 only).
        pages = [p for p in old if '/raw/ui/' in p and p.endswith('.bin')]
        assert len(pages) > 100 and not [p for p in pages if b'slide_menu' in pathlib.Path(old[p]).read_bytes()]
        removed = {p for p in STOCK_EQ + OBSOLETE if p in old}
        assert set(new) == (set(old) - removed) | added, (set(new) ^ ((set(old) - removed) | added))
        differ = {p for p in set(old) & set(new) if os.path.isfile(old[p]) and not os.path.islink(old[p])
                  and not filecmp.cmp(old[p], new[p], shallow=False)}
        assert differ - {logo} == replaced, differ ^ replaced
        # The Carousel's card art (ipod-ui 4.5): each role's V2.1 Home card art at CARD_ART, pressed too; the Shortcut's
        # its own (Phase 4.5 fixes, item 3: not Favorites' heart, whatever the Shortcut's target).
        card = lambda n: pathlib.Path(new[xx+f'home_card_{n}.png']).read_bytes()
        art_of = lambda n: m1ipod.sized_art(pathlib.Path(old[xx+n]).read_bytes(), m1plus_ipod.CARD_ART)
        assert set(m1ipod.HOME_ROWS) == {*m1plus_ipod.HOME_CARD_ART, 'rockbox'}
        for s in ('', '_down'):
            for row, art in m1plus_ipod.HOME_CARD_ART.items():
                assert card(row+s) == art_of(f'{art}{s}.png'), row+s
            assert card('rockbox'+s) == m1plus_ipod.home_card_shortcut(down=bool(s))
            assert all(m1ipod.png_header(card(row+s)) == (m1plus_ipod.CARD_ART,)*2 + (8, 6) for row in m1ipod.HOME_ROWS)
        assert card('rockbox') != card('rockbox_down') and card('rockbox') != art_of('fav.png')
        logo_new = pathlib.Path(new[logo]).read_bytes()
        assert sha(logo_new) == manifest['logo_sha256'] and (logo not in differ) == (manifest['logo_source'] == 'stock')
        # The boot hook's assumptions about V2.1: the card script announces a mounted card, and
        # q2boot's Play/Pause (KEY_PLAYPAUSE) is on the "md-gpio-keys" device.
        stock_file = lambda rel: pathlib.Path(old[rel]).read_bytes()
        assert re.search(rb'^\s*touch +/tmp/mmc_add$', stock_file('etc/mdev/add_removesd.sh'), re.M)
        assert re.search(rb'mmcblk\[0-9\]p\[0-9\] .* /etc/mdev/add_removesd\.sh', stock_file('etc/mdev.conf'))
        assert re.search(rb'^echo gpio="\w+" key_code=164 tag="KEY_PLAYPAUSE"', stock_file('module_driver/keyboard_gpio_add.sh'), re.M)
        assert b'md-gpio-keys\0' in stock_file('module_driver/keyboard_gpio_add.ko')
        assert b'sh keyboard_gpio_add.sh' in stock_file('module_driver/driver_default_init_script.sh')

def validate_assets(directory):
    import functools, json, re, struct, subprocess
    from build import sha, run, fileoff, symbols, BLUEALSA, AAC_44K1, GRADIENT_LEAF, WM_PAINT_LEAF, QUEUE_LEAF, HELPER, HELPER_LIKE, BOOT, BOOT_HOOK, REMOTE, REMOTE_HOOK, LOG_HOOK, WHEEL_LOG_HOOK, S90PLAY, S11LOGO, LOGO_HOOK, LOGO_LIGHT, BLUEALSA2, BT_KEEPALIVE, RTC_WRITE, WIFI_LPS, HOOKS, LOCK_CLOCK_12H, WATCHDOG, WATCHDOG_SLEEP, DROP_CACHES, STREAM_POLL_CALLS, DARK_POLLS, WHEEL_TS_READ, PDR
    from ipod import (ART_PLACEHOLDERS, sized_art, AUDIT, TOOLBAR_SWITCHES, BOTTOM, CONFIRM, VOLUME, BIGCOVER, BC_ART, BC_TITLE_PAD, QUICK_SETTINGS, QS_TOP, QS_LABEL_GAP, QS_LABEL_H,
                      QS_LABEL_W, QS_ROW_GAP, QS_PITCH, QS_BAR, QS_TOUCH, QS_EDGE, QS_SUN, HOME_LABEL_END, HOME_LIST_W, HOME_TEXT_X, HOME_TOP, PITCH, ARTIST_PAGE, HOME_PAGE, HOME_ROW, HOME_ROWS, NAVBAR_ONLY, PLAYING_PAGE, SET_ROW, SET_ROWS, SET_TOP, UI_ASSETS,
                      NP_BAR, NP_TOUCH, NP_MARGIN, NP_POS_X, NP_TOP, STATUS_BAR, STATUS_HIDDEN, STATUS_LEFT, STATUS_MARGIN, STATUS_RIGHT, CLOCK_MIN, CLOCK_TEXT, corner_inset, corner_x,
                      STATUS_ICONS, status_icon, QUIET_ICONS, quiet_icon, SET_ICON, SET_STOCK_ICON, SETTINGS_ICONS, SETTINGS_SLIDERS, decode, slider_plain, imagemagick, inc, png_header, settings_icon, walk,
                      patch_asset, patch_code, patch_style, style_props, SLIDE, SET0, status_metrics, CLASSIC_LIGHT_FONT_SRC, NP_IPOD_TIME_WS)
    from build import source_sha256
    manifest = json.loads((directory/'manifest.json').read_text())
    assert manifest['source_sha256'] == source_sha256(), f'{directory} was built from other sources; rebuild into a fresh directory'
    stock = (directory/'stock-demo').read_bytes()
    demo = (directory/'demo').read_bytes()
    def read(image, rel):
        return subprocess.check_output(['unsquashfs', '-cat', str(directory/image), rel])
    shared_checks(directory, manifest, stock, demo, read)
    if manifest.get('model') == 'Shanling M1 Plus':
        m1plus_checks(directory, manifest, stock, demo, read)
        print(f'M1 Plus: hook jumps, demo diff, rootfs file parity and boot scripts passed.')
        return
    # A widget's style, as stock's widget_update_style passes it to the style's notify: lw $4, W_ASTYLE($16).
    astyle = int(re.search(r'#define W_ASTYLE (0x[0-9a-f]+)', (ROOT/'patch/offsets.inc').read_text())[1], 16)
    off = fileoff(stock, 0x65e268)
    assert int.from_bytes(stock[off:off+4], 'little') == 0x8e040000 | astyle
    # .pdr (build.py PDR), past every LOAD segment, ships zeroed.
    assert demo[PDR[0]:PDR[0]+PDR[1]] == bytes(PDR[1]) and any(stock[PDR[0]:PDR[0]+PDR[1]])
    # The slide hint names a stock animator and gives it a duration (a missing one means stock's 500 ms).
    assert re.fullmatch(r'htranslate\(duration=\d+\)', SLIDE) and b'\0htranslate\0' in stock
    # The animated lookup pages need synchronous unwind.
    for address, slot in ((0x4a6250, 0x468), (0x4ad458, 0x468), (0x526e70, 0x420)):
        off = fileoff(stock, address)
        want = struct.pack('<III', 0x8f99a8f8, 0x0320f809, 0x8fa40000 | slot)
        assert demo[off:off+12] == want
    # Every hook and leaf jumps to its payload function (build.py pins the leaves' words): the
    # leaves are window_manager_paint (Videos), style_get_gradient and main_loop_queue_event.
    for address, name in [*(h[:2] for h in HOOKS.values()), WM_PAINT_LEAF[1:3], GRADIENT_LEAF[1:3], QUEUE_LEAF[1:3]]:
        off = fileoff(stock, address)
        assert demo[off:off+8] == j(symbols(directory/'patch.elf')[name]).to_bytes(4, 'little') + bytes(4)
    changed = manifest['changed_assets']
    xx = 'release/assets/default/raw/images/xx/'
    # Every stock UI asset with Chinese text is given in English (english_ui), the edited ones after their edit.
    from build import CJK, english_ui
    ui = 'release/assets/default/raw/ui/'
    chinese = {l.removeprefix('squashfs-root/'+ui) for l in run('unsquashfs', '-l', directory/'stock.squashfs').splitlines()
               if l.startswith('squashfs-root/'+ui) and l.endswith('.bin') and l.removeprefix('squashfs-root/') not in STOCK_EQ}
    chinese = {rel for rel in chinese if CJK.search(read('stock.squashfs', ui+rel).decode('utf-8', 'replace'))}
    assert chinese and {'testmode/test_key.bin', 'kb_default_t9.bin', 'dialog/search_dialog.bin'} <= chinese
    patched_ui = set(UI_ASSETS)
    assert set(changed) == {ui+p for p in patched_ui | chinese} | {
        'release/assets/default/raw/styles/'+p for p in AUDIT['styles']} | {
        xx+n for n in SETTINGS_ICONS | QUIET_ICONS | STATUS_ICONS | ART_PLACEHOLDERS} | {'release/assets/default/raw/strings/en_US.bin', FONT, TAG_C}
    master = (ROOT/'assets/icons/default_album_home.png').read_bytes()
    for name, size in ART_PLACEHOLDERS.items():
        old, new = read('stock.squashfs', xx+name), read('rootfs.squashfs', xx+name)
        assert png_header(new)[:2] == (size if isinstance(size, tuple) else (size, size)), name
        assert new == sized_art(master, size), name
        assert changed[xx+name] == dict(original_sha256=sha(old), sha256=sha(new))
        if not isinstance(size, tuple):  # transparent corners, not black, over a selected row
            assert imagemagick('png:-', '-format', '%[fx:p{0,0}.a]', 'info:', data=new) == b'0', name
    games = read('rootfs.squashfs', xx+'local_games.png')
    assert games == (ROOT/'assets/icons/local_games.png').read_bytes()
    assert png_header(games) == (52, 52, 8, 6)
    assert imagemagick('png:-', '-format', '%[fx:p{0,0}.a]', 'info:', data=games) == b'0'
    flow = read('rootfs.squashfs', xx+'default_album_flow.png')
    assert flow == sized_art(master, 160) and png_header(flow) == (160, 160, 8, 6)
    assert read('rootfs.squashfs', xx+'default_album_home.png') == master
    # Home: Carousel's cards in their own colours, stock's untouched, Coverflow's and the Shortcut's added.
    for name in ICONS:
        assert read('rootfs.squashfs', xx+name) == (ROOT/'assets/icons'/name).read_bytes(), name
    import tempfile
    with tempfile.NamedTemporaryFile(suffix='.ttf') as font:
        font.write(read('stock.squashfs','release/assets/default/raw/fonts/default.ttf')); font.flush()
        for text,size,room in [('Q2',16,28),('12:59 PM',16,CLOCK_TEXT),('100%',inc('BATT_PCT_PX'),inc('BATT_PCT_W'))]:
            rendered=imagemagick('-font',font.name,'-pointsize',str(size),'label:'+text,'png:-',data=b'')
            assert png_header(rendered)[0]-1<=room,(text,size,room,png_header(rendered))
    # Now Playing's queue reads "Queue", Idle "Power" and standby/shutdown "Standby" (LABELS); the table's later offsets move with them and nothing else changes.
    strings = 'release/assets/default/raw/strings/en_US.bin'
    old, new = read('stock.squashfs', strings), read('rootfs.squashfs', strings)
    assert new == relabel(old)
    n = 2 * struct.unpack_from('<H', new, 2)[0]
    table = dict(zip(*[iter(new[o:new.index(b'\0', o)] for o in struct.unpack_from(f'<{n}I', new, 4))] * 2))
    assert [table[k] for k, _, _ in LABELS] == [v for _, _, v in LABELS] and table[b'powerm_sleep'] == b'Sleep Timer'
    # Settings icons: the audited 52px artwork, packaged as SET_ICON RGBA with the same transparency
    # and, on a plain background, the same average colour. Minimal greys them
    # as they load (navigation.c ringnav_image_add: every disc MINIMAL_CHEVRON, glyphs white).
    def mean(png, bg):
        cmd = ['png:-', '-background', bg, '-flatten', '-format', '%[fx:mean.r],%[fx:mean.g],%[fx:mean.b]', 'info:']
        return [float(v) for v in imagemagick(*cmd, data=png).split(b',')]
    for name, digest in SETTINGS_ICONS.items():
        old, new = read('stock.squashfs', xx+name), read('rootfs.squashfs', xx+name)
        assert sha(old) == digest and png_header(old) == (SET_STOCK_ICON, SET_STOCK_ICON, 8, 6), name
        assert changed[xx+name] == dict(original_sha256=digest, sha256=sha(new)) and new == settings_icon(name, old), name
        assert png_header(new) == (SET_ICON, SET_ICON, 8, 6), name
        try: settings_icon(name, old[:-1] + b'x')
        except ValueError: pass
        else: raise AssertionError(f'{name}: accepted a changed icon')
        for bg in ('#000000', '#6e6e6e'):  # the list, and Classic's Graphite selection bar
            assert max(abs(a - b) for a, b in zip(mean(old, bg), mean(new, bg))) < 0.02, (name, bg)
        px = bytearray(imagemagick('png:-', '-depth', '8', 'rgba:-', data=new))
        sat = lambda i: max(px[i:i+3]) - min(px[i:i+3])
        disc = max([1] + [sat(i) for i in range(0, len(px), 4)])
        assert disc > 100, name  # a coloured disc to grey
        for i in range(0, len(px), 4): px[i:i+3] = bytes([255 - (255 - 0x77)*min(sat(i), disc)//disc])*3
        runtime = imagemagick('-size', f'{SET_ICON}x{SET_ICON}', '-depth', '8', 'rgba:-', '-define', 'png:color-type=6', 'png:-', data=bytes(px))
        values = mean(runtime, '#000000')  # Minimal's black list: neutral grey
        assert max(values) - min(values) < 0.001, name
    # Classic's bold ships, cut to what BOLD_RANGES lists
    from build import BOLD_TTF, CLASSIC_LIGHT_TTF, CLASSIC_LIGHT_NOTICE, FONT_NOTICES, bold_font, subset_font
    assert read('rootfs.squashfs', BOLD_TTF) == bold_font()[0]
    assert read('rootfs.squashfs', CLASSIC_LIGHT_TTF) == subset_font(ROOT/'assets/fonts/texgyreheros-bold.otf', 'Q2 Pod Classic Light', 'CLASSIC_LIGHT_RANGES', CLASSIC_LIGHT_NOTICE)[0]
    for name in FONT_NOTICES:
        assert read('rootfs.squashfs', 'release/assets/default/raw/fonts/' + name) == (ROOT/'assets/fonts'/name).read_bytes()
    # Centred Now Playing's page is English, as the iPod page is (english_ui)
    from build import CJK
    from ipod import PLAYING_STOCK
    stock_page = decode(read('rootfs.squashfs', 'release/assets/default/raw/ui/' + PLAYING_STOCK))
    assert not any(CJK.search(n[2].get('text', '')) for n in walk(stock_page))
    # its lyrics page follows the page's size, for full-screen lyrics (navigation.c np_full)
    named = {n[2].get('name'): n[2] for n in walk(stock_page)}
    assert named['view_lrc']['self_layout'] == 'default(x=0,y=0,w=100%,h=-20)'
    assert named['label_lyricmsg']['self_layout'] == 'default(x=0,y=73,w=100%,h=28)'
    # Curly quotes draw the straight glyphs and ♡ takes ♥'s box and advance; other tables keep their
    # stock bytes (head: its checksum).
    from build import QUOTES
    from fontTools.ttLib import TTFont
    old, new = (TTFont(io.BytesIO(read(i, FONT))) for i in ('stock.squashfs', 'rootfs.squashfs'))
    assert all(new.getBestCmap()[c] == old.getBestCmap()[q] for c, q in QUOTES.items())
    full, empty = (new.getBestCmap()[c] for c in (0x2665, 0x2661))
    g = new['glyf']
    assert new['hmtx'][empty] == new['hmtx'][full] == (old['hmtx'][full][0] + 32, g[full].xMin)
    assert abs(g[empty].xMin - g[full].xMin) <= 1 and abs(g[empty].xMax - g[full].xMax) <= 1
    assert abs(g[empty].yMin - g[full].yMin) <= 1 and abs(g[empty].yMax - g[full].yMax) <= 1
    assert all(new.reader[t] == old.reader[t] for t in old.reader.keys() if t not in ('cmap', 'head', 'glyf', 'loca', 'hmtx'))
    # Include every excluded UI screen and saved-preference defaults in byte parity checks.
    paths = [l.removeprefix('squashfs-root/') for l in run('unsquashfs', '-l', directory/'stock.squashfs').splitlines()
             if ('/raw/ui/' in l or '/raw/styles/' in l) and l.endswith('.bin') or l.endswith('/config.ini')]
    names = set(run('unsquashfs', '-l', directory/'rootfs.squashfs').splitlines())
    # Light Mode's splash ships with the default logo only (build.py LOGO_HOOK)
    light = (ROOT/'assets/boot-logo-light.jpg').read_bytes()
    default = manifest['logo_sha256'] == sha((ROOT/'assets/boot-logo.jpg').read_bytes())
    assert ('squashfs-root/'+LOGO_LIGHT in names) == default and (not default or read('rootfs.squashfs', LOGO_LIGHT) == light)
    # The carousel's images stay (and its arrows); the Coverflow and Shortcut cards' are added.
    assert {'squashfs-root/release/assets/default/raw/images/xx/'+n for n in ICONS + ['menu_music.png', 'menu_left.png', 'menu_right.png']} <= names
    # Colours the firmware will paint (inline style props, else the theme entry for the widget's style):
    # no screen may gain a light background or border, or dark text, that stock did not already paint.
    def palette(path):
        return {(w, s, p): v.hex() for w, s, state, p, _, v in style_props(read(path, 'release/assets/default/raw/styles/default.bin'))
                if state == 'normal' and p in ('bg_color', 'border_color', 'text_color')}
    themes = palette('stock.squashfs'), palette('rootfs.squashfs')
    def painted(root, theme):
        out = set()
        for kind, _, props, _ in walk(root):
            style = props.get('style', 'default')
            for p in ('bg_color', 'border_color', 'text_color'):
                v = props.get('style:normal:'+p, '').lstrip('#').lower() or theme.get((kind, style, p))
                if v: out.add((kind, props.get('name', ''), p, v if len(v) == 8 else v+'ff'))
        return out
    def luma(v): return sum(k*int(v[i:i+2], 16) for k, i in ((0.2126, 0), (0.7152, 2), (0.0722, 4))) / 255
    def jarring(c):
        kind, _, p, v = c
        if int(v[6:], 16) <= 0x40: return False
        return luma(v) < 0.25 if p == 'text_color' else luma(v) > 0.35 and kind != 'image'
    # iPod: text and icons must clear the glass's rounded corners (ipod.CORNER_R); backgrounds,
    # bars and full-bleed art may reach into them. Content is a label's font-high band, an image drawn centred at its
    # size, a slider's bar, else the widget; the window clips it, and row layouts place their children.
    # List rows scroll, so only fixed widgets are checked.
    fonts = {(w, s): int.from_bytes(v, 'little') for w, s, state, p, _, v in style_props(
        read('rootfs.squashfs', 'release/assets/default/raw/styles/default.bin')) if state == 'normal' and p == 'font_size'}
    @functools.cache
    def image_size(name):
        try: return struct.unpack('>II', read('rootfs.squashfs', f'release/assets/default/raw/images/xx/{name}.png')[16:24])
        except subprocess.CalledProcessError: return None
    def content(kind, props, x, y, w, h):
        if kind in ('label', 'hscroll_label'):
            size = int(props.get('style:normal:font_size') or fonts.get((kind, props.get('style', 'default')), 18))
            return x, y if props.get('style:normal:text_align_v') == 'top' else y + (h - size) // 2, w, size
        if kind == 'slider':
            bar = int(props.get('bar_size', h))
            return x, y + (h - bar) // 2, w, bar
        if kind == 'progress_bar': return x, y, w, h
        name = props.get('image') or props.get('style:normal:bg_image')
        if kind not in ('image', 'gif', 'image_animation') or not name: return None
        draw = props.get('draw_type') if 'image' in props else props.get('style:normal:bg_image_draw_type', 'center')
        if draw == 'fill': return None  # full-bleed art, like a background: the glass rounds its corners
        size = image_size(name) if draw == 'center' else None
        return (x + (w - size[0]) // 2, y + (h - size[1]) // 2, *size) if size else (x, y, w, h)
    def corners(short, n, x0, y0, window, slot=None):
        kind, (x, y, w, h), props, children = n
        if props.get('visible') == 'false' or kind in ('list_item', 'table_row'): return  # hidden, or rows that scroll
        x, y, w, h = slot or (x, y, w, h)
        if at := re.match(r'default\(x=(-?\d+),y=(-?\d+),', props.get('self_layout', '')):
            x, y = int(at[1]), int(at[2])
        x, y = x0 + x, y0 + y
        if box := content(kind, props, x, y, w, h):
            bx, by, bw, bh = box
            top, bottom = max(by, window[0]), min(by + bh, window[1])
            inset = max(corner_inset(top), corner_inset(bottom))
            assert bx + bw <= 0 or bx >= 375 or top >= bottom or inset <= bx and min(bx + bw, 375) <= 375 - inset, (
                short, props.get('name'), box, inset)
        slots, row = {}, re.fullmatch(r'default\(r=1,c=0,(a=right,)?xm=(\d+),s=(\d+)\)', props.get('children_layout', ''))
        if row:  # AWTK's row layout, every child shown
            gap, cx = int(row[3]), int(row[2])
            if row[1]: cx = w - cx - sum(c[1][2] for c in children) - gap * (len(children) - 1)
            for c in children:
                slots[id(c)] = (cx, 0, c[1][2], h)
                cx += c[1][2] + gap
        for c in children: corners(short, c, x, y, window, slots.get(id(c)))
    for rel in paths:
        if rel in STOCK_EQ: continue
        original, new = read('stock.squashfs', rel), read('rootfs.squashfs', rel)
        if '/raw/ui/' in rel and new[:4] == bytes.fromhex('12122211'):
            now = painted(decode(new), themes[1])
            bad = [c for c in now - painted(decode(original), themes[0]) if jarring(c)
                   and (c[2] != 'text_color' or c[0] in ('label', 'hscroll_label', 'button', 'edit', 'tab_button'))]
            # The rows are transparent, so a light list container stock hid behind them would show.
            bad += [c for c in now if c[2] == 'bg_color' and jarring(c)
                    and c[0] in ('list_view', 'list_item', 'scroll_view', 'table_view', 'table_client', 'view')]
            assert not bad, (rel, bad)
        if rel not in changed:
            assert new == original, rel
            continue
        assert changed[rel] == dict(original_sha256=sha(original), sha256=sha(new))
        if '/raw/styles/' in rel:
            audit = AUDIT['styles'][rel.split('/raw/styles/')[1]]
            assert new == patch_style(original, audit) and len(new) == len(original)
            wrong = [*audit['edits'][0][:3], 'ffffffff', *audit['edits'][0][4:]]
            try:
                patch_style(original, dict(audit, edits=[wrong]))
                raise AssertionError('Accepted a wrong old style value')
            except ValueError:
                pass
            continue
        if '/raw/images/' in rel:
            name=rel.rsplit('/',1)[-1]
            if name in STATUS_ICONS:
                assert new == status_icon(name, original)
                assert png_header(new) == (14 if name.startswith('bar_wifi') else 42 if name.startswith('bar_bt') else 12, 16, 8, 6)
            elif name in QUIET_ICONS:
                assert sha(original)==QUIET_ICONS[name] and new==quiet_icon(name,original)
                assert png_header(new)==(28,28,8,6)
            else: assert name in SETTINGS_ICONS and new==settings_icon(name,original)
            continue
        short = rel.split('/raw/ui/')[1]
        edited = patch_asset(short, original) if short in patched_ui else original
        assert new == (english_ui(short, edited) if short in chinese else edited), short
        if short not in patched_ui:
            continue
        if short in chinese:  # the checks below are of the edits: compare with stock given in English
            original = english_ui(short, original)
        if short == 'dialog/addplaylist_dialog.bin':
            expected = decode(original)
            expected[3][0][3][0][2]['sensitive'] = 'true'
            assert decode(new) == expected
            continue
        root = decode(new)
        if short in SETTINGS_SLIDERS:
            before = {n[2].get('name'): n for n in walk(decode(original))}
            assert not [n for n in walk(root) if n[0] == 'image' and n[2].get('image')]  # no endpoint glyphs
            gone = [n for n in walk(root) if n[2].get('name') in before and before[n[2]['name']][2].get('image')]
            assert len(gone) == 2 and all(n[1][2:] == [0, 0] and n[1][:2] == before[n[2]['name']][1][:2] for n in gone)
            for n in walk(root):
                if n[0] == 'slider':
                    props = n[2]
                    old = before[props['name']]
                    assert n[1] == old[1] and props['bar_size'] == '8'
                    assert not [k for k in props if k.endswith((':bg_image', ':fg_image', ':icon', ':y_offset'))]
                    assert props['style'] == 's_ipod_progress'
                    for state in ('normal', 'pressed', 'over', 'disable', 'focused'):
                        assert props[f'style:{state}:bg_color'] == '#1c1c1c'
                        assert props[f'style:{state}:fg_color'] == '#6e6e6e'
                        assert props[f'style:{state}:round_radius'] == '4'
                        assert props[f'style:{state}:border_color'] == '#00000000'
                    assert {k: v for k, v in props.items() if not k.startswith('style') and k != 'bar_size'} == {
                        k: v for k, v in old[2].items() if not k.startswith('style') and k != 'bar_size'}
                    continue
                if n[2].get('name') in ('img_add', 'img_dec'):
                    assert n == before[n[2]['name']]  # ranges, touch and wheel controls stay stock
        if short == VOLUME:  # Hidden before the first paint, including transition snapshots.
            plain = decode(original); del plain[2]['highlight']
            for child in plain[3]: child[2]['visible'] = 'false'
            assert root == plain
            continue
        # Browsing, settings and the PEQ editor slide; Home, Now Playing, the bar and dialogs don't.
        slides = short not in (HOME_PAGE, STATUS_BAR, PLAYING_PAGE, QUICK_SETTINGS, CONFIRM, BIGCOVER)
        assert root[2].get('anim_hint') == (SLIDE if slides else None), short
        # screen coordinates: the bar, full-screen dialogs (quick settings slides down from -320), windows
        origin, window = {STATUS_BAR: (0, (0, SET0.bar)), QUICK_SETTINGS: (320, (0, 320)), CONFIRM: (0, (0, 320)),
                          BIGCOVER: (0, (0, 320))}.get(short, (SET0.bar, (SET0.bar, 320)))
        corners(short, root, 0, origin, window)
        if short == QUICK_SETTINGS:  # iPod only: the stock 4x2 grid, even label areas, a slim brightness track
            menu, light = root[3]
            icons = [n for n in menu[3] if n[0] == 'image']; labels = [n for n in menu[3] if n[0] == 'label']
            assert len(icons) == len(labels) == 8 and menu[1][1] >= QS_TOP
            assert sorted({n[1][0] for n in icons}) == sorted({n[1][0] for n in decode(original)[3][0][3] if n[0] == 'image'})
            for icon, label in zip(icons, labels):
                x, y, w, h = icon[1]
                # The same 16px two-line area, top-aligned, centred under its icon and clear of the next row.
                assert label[1] == [x + (w - QS_LABEL_W) // 2, y + h + QS_LABEL_GAP, QS_LABEL_W, QS_LABEL_H]
                assert label[2]['style'] == 's_label_white16c' and label[2]['style:normal:text_align_v'] == 'top'
                assert 2 * (16 + 2) <= QS_LABEL_H and label[2]['line_wrap'] == label[2]['word_wrap'] == 'true'
            assert {n[1][1] for n in icons} == {0, QS_PITCH}
            slider, dim, bright = light[3]
            assert light[1][1] == menu[1][1] + menu[1][3] + QS_ROW_GAP and light[1][1] + light[1][3] <= 320 - 16
            assert slider[2]['bar_size'] == str(QS_BAR) and slider[1][3] == QS_TOUCH >= 44 and slider[2]['slide_with_bar'] == 'true'
            assert not [k for k in slider[2] if k.endswith((':bg_image', ':fg_image', ':icon'))]
            assert slider[2]['style'].encode() not in read('rootfs.squashfs', 'release/assets/default/raw/styles/default.bin')
            assert dim[1][0] == QS_EDGE and bright[1][0] + bright[1][2] == 375 - QS_EDGE and dim[2]['image'] == 'drop_lighleft'
            assert dim[1][0] + QS_SUN < slider[1][0] and slider[1][0] + slider[1][2] < bright[1][0]
            continue
        if short == CONFIRM:  # iPod only: the stock pair as two full-width text rows under the prompt
            cancel, enter = root[3]
            assert [n[0] for n in root[3]] == ['button', 'button'] and [n[2]['name'] for n in root[3]] == ['img_cancel', 'img_enter']
            assert cancel[1] == [0, 208, 375, 48] and enter[1] == [0, 256, 375, 48] and enter[1][1] + enter[1][3] <= 320
            assert [n[2]['text'] for n in root[3]] == ['Cancel', 'OK']
            continue
        if short == BIGCOVER:  # iPod only: a centred square of art clear of the glass (corners above), the name on its foot
            art, shade, title = root[3]
            x, y = (375 - BC_ART) // 2, (320 - BC_ART) // 2
            assert root[2] == decode(original)[2] and art[2]['image'] == 'default_bigcover' and art[2]['draw_type'] == 'scale_auto'
            assert art[1] == [x, y, BC_ART, BC_ART] and art[2]['self_layout'] == f'default(x={x},y={y},w={BC_ART},h={BC_ART})'
            assert abs((375 - x - BC_ART) - x) <= 1 and 320 - y - BC_ART == y and BC_ART > 280  # centred, and still most of the height
            assert (375 - BC_ART - 2) // 2 < corner_x((320 - BC_ART - 2) // 2, BC_ART + 2)  # the largest that clears
            assert shade[1] == [x, y + BC_ART - 50, BC_ART, 50] and shade[2] == decode(original)[3][1][2]
            assert title[1] == [x + BC_TITLE_PAD, y + BC_ART - 50 + 11, BC_ART - 2 * BC_TITLE_PAD, 28] and title[2] == decode(original)[3][2][2]
            continue
        if short == HOME_PAGE:  # seven rows with the stock names, beside the art; bytes equal patch_asset above
            art, (lv, lg, _, [sv]), (sl, sg, sp, [ss]), *carousel = root[3]
            assert lv == 'list_view' and sv[0] == 'scroll_view' and art[2]['name'] == 'img_homeart'
            # The Settings list: stock's Playback and System setting rows (stock binds them; their
            # labels are literal), hidden in the list's place until Home's Settings row slides it in.
            assert sl == 'list_view' and sp['name'] == 'list_view_homeset' and sp['visible'] == 'false'
            assert sg == [0, HOME_TOP, HOME_LIST_W, 2*HOME_ROW] and [r[2]['name'] for r in ss[3]] == ['btn_playset', 'btn_sysset']
            assert [r[3][1][2]['name'] for r in ss[3]] == ['img_playset', 'img_sysset'] and [r[3][0][2]['text'] for r in ss[3]] == ['Playback', 'System']
            # The art fills the right panel below the status bar; the payload fits and crops it.
            assert art[0] == 'image' and art[1] == [0, 0, 375, BOTTOM] and art[2]['draw_type'] == 'fill' and HOME_LIST_W == 375
            assert all(v == '#00000000' for k,v in root[3][1][2].items() if k.startswith('style:'))
            assert [r[2]['name'] for r in sv[3]] == ['btn_'+n for n in HOME_ROWS] and HOME_ROWS[2] == 'coverflow'
            for name, (_, _, _, (label, image)) in zip(HOME_ROWS, sv[3]):
                assert label[2]['name'] == ('label_library' if name == 'localmusic' else 'label_'+name)
                assert image[2] == {'name': 'img_'+name, 'clickable': 'true'}
                # Labels end before the chevron's glyph; longer ones scroll (only_focus) or end in an ellipsis.
                assert label[1][0] + label[1][2] == image[1][2] - HOME_LABEL_END and label[1][2] >= 100
                assert label[2]['only_focus'] == 'true' and label[2]['ellipses'] == 'true'
            assert [r[3][0][2].get('text') for r in sv[3]] == [None, 'Library', 'Cover Flow', None, 'Rockbox', None, 'Settings']
            assert lg == [0, HOME_TOP, HOME_LIST_W, 7*HOME_ROW] and HOME_TOP + 7*HOME_ROW <= BOTTOM - HOME_TOP
            # Home: Carousel's: stock's carousel and arrows after the lists, hidden and taking no taps
            # until chosen (coverflow_home_layout); its cards stock's in their places, Library's label
            # literal, Coverflow's after it and the Shortcut's after Folder on their own images.
            stock_root = decode(original)
            assert [n[2]['name'] for n in carousel] == ['slide_menu', 'img_left', 'img_right']
            for n, old in zip(carousel, stock_root[3]):
                assert n[:2] == old[:2] and n[2] == {**old[2], 'visible': 'false', 'sensitive': 'false'}
            slide = carousel[0]
            assert [c[2]['name'] for c in slide[3]] == ['btn_'+n for n in ('playing', 'localmusic', 'coverflow', 'folder', 'rockbox', 'stream', 'playset', 'sysset')]
            assert [c[3][1][2].get('text') for c in slide[3]] == [stock_root[3][0][3][0][3][1][2]['text'], 'Library', 'Cover Flow', None, 'Rockbox', None, None, None]
            for card in slide[3]:
                image = card[3][0][2]
                assert {v for k, v in image.items() if k.endswith(':bg_image')} == {'menu_' + image['name'][4:].replace('localmusic', 'music'),
                                                                                  'menu_' + image['name'][4:].replace('localmusic', 'music') + 'down'}
            dot = inc('HOME_DOT_X'), inc('HOME_DOT')
            assert HOME_TEXT_X == sum(dot) + inc('HOME_DOT_GAP')
            # The dot and the labels clear the bottom row's corner.
            assert dot[0] >= corner_x(SET0.bar + HOME_TOP + 6*HOME_ROW + (HOME_ROW - dot[1])//2, dot[1])
            assert HOME_TEXT_X >= corner_x(SET0.bar + HOME_TOP + 6*HOME_ROW + 9, 20)
            # Split (coverflow_home_layout) gives the menu half the screen, the art the rest;
            # Split's glyph ends 13px before the art, as in the Home concept.
            assert inc('HOME_SPLIT_W') == 375 // 2
            assert inc('CHEVRON_W') - 30 - inc('HOME_CHEVRON_SHIFT') == 13
            assert inc('HOME_MODERN_TEXT_X') >= corner_x(SET0.bar + HOME_TOP + 6*HOME_ROW + 9, 20)
            # Modern's labels stop short of Split's glyph (x 20 to 30 of list_into) and Full's.
            for row, shift in ((inc('HOME_SPLIT_W'), inc('HOME_CHEVRON_SHIFT')), (inc('HOME_MODERN_ROW'), inc('HOME_FULL_CHEVRON_SHIFT'))):
                assert row - inc('HOME_MODERN_LABEL_END') + 5 <= row - inc('CHEVRON_W') + shift + 20
            continue
        if short == STATUS_BAR:  # iPod only: play state left, title between, four icons right
            left, right, *rest = root[3]
            assert all(root[2][f'style:{s}:border_color'] == '#00000000' for s in ('normal', 'disable', 'focused'))  # Light Mode: no paper line
            assert [n[2]['name'] for n in left[3]] == STATUS_LEFT and [n[2]['name'] for n in right[3]] == STATUS_RIGHT
            title = rest.pop()
            assert title[0] == 'hscroll_label' and title[2]['name'] == 'label_clock'
            x, _, w, _ = title[1]
            assert x + w/2 == 375/2 and w >= CLOCK_MIN  # centred on the screen, clear of both groups (corners below)
            assert inc('CLOCK_EDGE') >= corner_x((SET0.bar - 20) // 2, 20) and x >= inc('CLOCK_EDGE')
            assert title[2]['style:normal:font_size'] == '16'
            assert all(v[2]['children_layout'].endswith(f'xm={STATUS_MARGIN},s={inc("STATUS_GAP")})') for v in (left, right))
            idle = rest.pop()
            assert idle[1] == [STATUS_MARGIN, 0, 28, SET0.bar] and idle[2]['text'] == 'Q2' and idle[2]['visible'] == 'false'
            assert idle[2]['style:normal:font_size'] == '18' and STATUS_MARGIN >= corner_x(6, 18)
            assert STATUS_MARGIN + 28 < x
            assert [n[2]['name'] for n in rest] == STATUS_HIDDEN and all(n[1][0] + n[1][2] < 0 for n in rest)
            # The Battery setting's percentage and payload battery start hidden (navigation.c bar_sync).
            pct, slot = right[3][2:4]
            assert pct[1][2] == inc('BATT_PCT_W') and pct[2]['visible'] == 'false' and pct[2]['style:normal:text_align_h'] == 'right' and pct[2]['style:normal:font_size'] == str(inc('BATT_PCT_PX'))
            assert slot == ['view', [0, 0, inc('BATT_BODY_W') + inc('BATT_NUB_W') + inc('BATT_GAP') + inc('BATT_PCT_W'), 0], {'name': 'view_battery', 'visible': 'false'}, []]
            continue
        if short == PLAYING_PAGE:  # see the sketch in docs/ipod.md
            named = {n[2].get('name'): n for n in walk(root)}
            assert {n[2].get('name') for n in walk(decode(original))} < set(named)  # stock names kept
            assert [n[2].get('name') for n in root[3]] == ['view_buttons', 'label_playtime', 'label_playlen', 'label_ipod_remain',
                                                           'slide_view_view', 'slider_play', 'img_repeata', 'img_repeatb', 'image_wait']
            pos = named['label_ipod_pos'][1]
            assert pos[0] + pos[2] == named['img_more'][1][0] and named['img_return'][1][0] < 0
            assert not {'img_fav', 'img_playmode'} & {n[2].get('name') for n in named['view_buttons'][3]}
            assert named['img_more'][1][1:] == [0, 50, 40]
            album = named['view_album'][3]
            assert [n[2]['name'] for n in album] == ['img_cover', 'img_playstate', 'scrlabel_title', 'scrlabel_artist', 'label_ipod_album',
                                                     'img_playmode', 'img_fav']
            # 16px outer margins, 12px from the art to the text, the text column 165px wide; the title larger.
            # Order and favourite glyphs level with the art's foot (frames NP_ICON_PAD lower); favourite centred below More. The art's gap to
            # the dots below (y 182) matches its gap to "3 of 12"'s text above.
            assert [n[1] for n in album] == [[16, 2, 166, 166], [39, 25, 120, 120], [194, 18, 165, 28], [194, 52, 165, 22], [194, 80, 165, 22],
                                             [247, 133, 50, 50], [303, 133, 50, 50]]
            assert album[-1][1][0] == named['img_more'][1][0] and album[-1][1][2] == named['img_more'][1][2] == 50
            assert album[-1][1][0] - (album[-2][1][0] + album[-2][1][2]) == 6 and 80 + 22 < 118 + 13
            assert album[1][2]['opacity'] == '0'  # playback gestures retain their original target
            assert album[2][2]['style:normal:font_size'] == '22' and album[3][2]['style:normal:font_size'] == '18'
            for node, color in ((album[3], '#CCCCCC'), (album[4], '#BBBBBB')):
                assert {v for k, v in node[2].items() if k.endswith(':text_color')} == {color}
            assert pos[0] == NP_POS_X and album[0][1][0] == NP_MARGIN and 375 - 16 == album[2][1][0] + album[2][1][2]
            # Distinct bands: top row, art, page dots, bar (A-B markers y 250 to 260), then the times.
            dots = named['slide_indicator1'][1]
            assert NP_TOP + 10 + 166 < NP_TOP + dots[1] and NP_TOP + dots[1] + 10 < NP_BAR[1] - 1
            # The dots' own anchor, the slide_view's centre: stock's, with none, followed a swipe's offset.
            anchor = named['slide_indicator1'][2]
            assert anchor['anchor_x'] == f'{375 // 2 - dots[0]}px' and anchor['anchor_y'] == '0px' and 0 < dots[3] // 2
            assert named['slide_view'][1] == [0, 0, 375, 186]
            # The lyrics page (patch/lyrics.c): its rows span the page, a LYRIC_SLOT each after a blank one,
            # three to its 178px; the text, LYRIC_X in, clears the glass's corners, as the art does.
            lrc, slot = named['view_lrc'][3][0][2], inc('LYRIC_SLOT')
            assert named['view_lrc'][2]['self_layout'] == 'default(x=0,y=0,w=375,h=178)' and 3 * slot <= 178 < 4 * slot
            assert lrc['self_layout'] == 'default(x=0,y=0,w=100%,h=100%)' and lrc['children_layout'] == f'list_view(x=0,y={slot},s=0)'
            assert inc('LYRIC_X') == NP_MARGIN >= corner_x(SET0.bar + NP_TOP, 178)
            slider = named['slider_play']
            assert slider[1] == [NP_BAR[0], 233, NP_BAR[2], NP_TOUCH] and NP_TOUCH >= 44
            assert slider[2]['bar_size'] == '4' and slider[2]['slide_with_bar'] == 'true'
            assert slider[1][1] + (slider[1][3] - int(slider[2]['bar_size'])) // 2 == NP_BAR[1]
            assert NP_TOP + dots[1] + dots[3] < slider[1][1]  # page swipes and seeking have separate targets
            assert not [k for k in slider[2] if k.endswith((':bg_image', ':fg_image', ':icon'))]
            assert {v for k, v in slider[2].items() if k.endswith('_color')} == {'#1c1c1c', '#6e6e6e', '#00000000'}
            assert all(slider[2][f'style:{s}:border_color'] == '#00000000' for s in ('normal','pressed','over','disable','focused'))
            assert {v for k, v in slider[2].items() if k.endswith(':round_radius')} == {'2'}  # a slim line
            # No theme style of that name, so no thumb icon: stock fills exactly to the value.
            assert slider[2]['style'].encode() not in read('rootfs.squashfs', 'release/assets/default/raw/styles/default.bin')
            played, remain = (named[n][1] for n in ('label_playtime', 'label_ipod_remain'))
            assert played[1:] == remain[1:] == [265, 80, 16] and played[0] == 375 - remain[0] - 80 and 250 + 10 < 265
            assert named['label_playlen'][2]['visible'] == 'false'
            assert {v for n in ('label_playtime', 'label_ipod_remain') for k, v in named[n][2].items() if k.endswith(':text_color')} == {'#AAAAAA'}
            # Stock places the A-B markers at y 250 and x = 50 + t * 290 / length; iPod's follow its bar.
            assert [int.from_bytes(demo[fileoff(demo, a):fileoff(demo, a)+4], 'little') for a in (0x52a318, 0x52a330)] == [
                0x24020000 | NP_BAR[2], 0x24420000 | NP_BAR[0]]
            continue
        if short == ARTIST_PAGE:
            assert [n[2]['value'] for n in walk(root) if n[0] == 'pages'] == ['1'], 'Artist page must show Albums'
        if short in AUDIT['slide_only'] or short in TOOLBAR_SWITCHES:
            # Only the hint and settings slider styling change.
            root[2].pop('anim_hint')
            kept = decode(original)
            slider_plain(short, kept)
            assert root == kept, short
            continue
        nav = next(n for n in root[3] if n[2].get('name') == 'view_navbar')
        if short in NAVBAR_ONLY:  # content moves up 50; lists hold four whole SET_ROW rows from SET_TOP
            for old, node in zip(decode(original)[3], root[3]):
                if node is nav: continue
                if node[0] == 'list_view':
                    assert node[1] == [0, SET_TOP, 375, SET_ROWS * SET_ROW] and SET_TOP + SET_ROWS * SET_ROW <= BOTTOM, short
                    assert node[2] == {**old[2], 'default_item_height': str(SET_ROW)} and node[3] == old[3], short
                    continue
                assert node[1][1] == old[1][1] - 50 and node[1][3] == old[1][3] and node[2] == old[2], short
        if short == 'localmusic/playlist_page.bin':
            old_nav = next(n for n in decode(original)[3] if n[2].get('name') == 'view_navbar')
            gif, old = (next(n for n in p[3] if n[2].get('name') == 'gif_returnplay') for p in (nav, old_nav))
            assert gif[1] == [375 - corner_x(SET0.bar, old[1][3]) - old[1][2], *old[1][1:]]
            assert nav[2].get('visible') != 'false' and nav[2].get('enable') != 'false'
            gif[1][0] = old[1][0]
            assert nav == old_nav, 'only the right button keeps clear of the glass'
        else:
            assert nav[2]['visible'] == 'false' and nav[2]['enable'] == 'false'
        assert not [v for n in walk(root) if n[0] in ('button', 'list_item', 'table_row')
                    for k, v in n[2].items() if k.endswith(':bg_color') and v == '#000000'], 'Opaque inline row background'
        old_nodes, new_nodes = list(walk(decode(original))), list(walk(root))
        assert len(old_nodes) == len(new_nodes)
        for old, node in zip(old_nodes, new_nodes):
            for key, value in old[2].items():
                if short in SETTINGS_SLIDERS and node[0] == 'slider' and key == 'style':
                    value = 's_ipod_progress'
                if 'font' in key or key == 'style': assert node[2][key] == value
        if short in ('folder_page.bin', 'localmusic_page.bin', 'localmusic/localclass_page.bin', 'localmusic/playlist_page.bin'):
            surface = next(n for n in root[3] if n[0] in ('list_view', 'table_view'))
            top = 50 if short == 'localmusic/playlist_page.bin' else 0
            assert surface[1][1:] == [top, 375, BOTTOM-top], 'Lists must fill the client area'
            assert 4*PITCH <= BOTTOM, 'Four complete rows must fit'
        # Corrupt inputs must be rejected, never silently patched.
        try: patch_asset(short, original[:-1]+b'x')
        except ValueError: pass
        else: raise AssertionError('Accepted a changed asset')
    # Every geometry set's built list windows take the row height of the page's pitch
    # immediates (art pages take art_pitch), and its rows fit.
    from theme import builtins, geometry_sets, SCHEMA
    from ipod import CLASSIC_LIGHT_FONT_SRC, PAGE_KIND as page_kind, page_rows
    built = set(run('unsquashfs', '-l', directory/'rootfs.squashfs').split())
    # Classic's Playlists rows (pl_row) are the theme's page_detail high in a list pitched at song_pitch: one height.
    for t in builtins():
        for g in geometry_sets([t]):
            if not g.toolbar: assert g.song_pitch == t['page_detail'], (t['name'], g.name)
    for g in geometry_sets(builtins()):
        assert g.body <= g.pitch and g.art_body <= g.art_pitch and g.song_body <= g.song_pitch, g.name
        assert g.art + 2*g.art_inset <= g.art_body, g.name
        assert g.text_art + 2*g.text_art_inset <= g.body or not g.text_art, g.name   # text rows' artwork fits, or none
        for y, h, body in ((g.title24_y, 24, g.body), (g.title_y, 20, g.body), (g.meta_y, 16, g.body), (g.count_y, 16, g.body),
                           (g.art_title24_y, 24, g.art_body), (g.art_meta_y, 16, g.art_body),
                           (g.song_title24_y, 24, g.song_body), (g.song_meta_y, 16, g.song_body)):
            assert 0 <= y and y + h <= body, (g.name, y, h, body)                    # every stock row label inside its body
        checked = set()
        for short, kind in page_kind.items():
            folder, _, base = short.rpartition('/')
            mine = ui + (folder and folder + '/') + f'{g.name}_{base}'
            new = decode(read('rootfs.squashfs', mine if 'squashfs-root/' + mine in built else ui + short))
            old = {n[2].get('name'): n[2] for n in walk(decode(read('stock.squashfs', ui + short)))}
            for n in walk(new):
                for prop in ('row_height', 'default_item_height'):
                    if old.get(n[2].get('name'), {}).get(prop) == '78':
                        assert n[2][prop] == str(page_rows(g, kind)[0]), (g.name, short, prop)
                        checked.add(short)
        assert checked == set(page_kind) - {'localmusic/album_page.bin'}, checked  # album_page's grid keeps 160
        # A set without toolbars: Playlists' toolbar hides, stock's widgets alive for its rows' clicks, its list takes the
        # bar's room with rows of their own heights (no item_height forces them); More's rows start at the top.
        if not g.toolbar:
            for short in ('localmusic/playlist_page.bin', 'localmusic/playlistsmore_page.bin'):
                folder, _, base = short.rpartition('/')
                new = decode(read('rootfs.squashfs', ui + f'{folder}/{g.name}_{base}'))
                nav = next(n for n in new[3] if n[2].get('name') == 'view_navbar')
                assert nav[2]['visible'] == 'false' and nav[2]['enable'] == 'false', short
                if short == 'localmusic/playlist_page.bin':
                    surface = next(n for n in new[3] if n[0] == 'list_view')
                    assert surface[1][1] == 0 and surface[2]['default_item_height'] == str(g.song_pitch) and 'item_height' not in surface[2]
                else:
                    assert [n[1][1] for n in new[3] if n[0] == 'list_item'] == [0, g.pitch]
        assert g.set_top + g.set_rows*g.set_row <= 320 - g.bar, g.name
        # Home's rows are the set's and fit; a theme with Home's chevron ends its labels short of the
        # glyph (x 20 of list_into) in both widths, as Classic's below.
        mine = ui + f'{g.name}_{HOME_PAGE}'
        listed = {n[2].get('name'): n for n in walk(decode(read('rootfs.squashfs', mine if 'squashfs-root/' + mine in built else ui + HOME_PAGE)))}['list_view_home']
        assert listed[2]['item_height'] == str(g.home_row) and HOME_TOP + 7*g.home_row <= 320 - g.bar, g.name
        for t in builtins():
            if g in geometry_sets([t]) and t['chevron_home']:
                # a theme's own chevron in Split: the label ends at it
                assert t['home_label_end[0]'] >= (inc('HOME_SPLIT_W') - t['home_chevron_x'] if t['home_chevron_x']
                                                  else inc('CHEVRON_W') - inc('HOME_CHEVRON_SHIFT') - 15), t['id']
                assert t['home_label_end[1]'] >= inc('CHEVRON_W') - inc('HOME_FULL_CHEVRON_SHIFT') - 15, t['id']
        for rel in UI_ASSETS:
            folder, _, base = rel.rpartition('/')
            mine = ui + (folder and folder + '/') + f'{g.name}_{base}'
            if 'squashfs-root/' + mine not in built: continue
            for n in walk(decode(read('rootfs.squashfs', mine))):
                if n[0] != 'list_view' or n[2].get('default_item_height') != str(g.set_row): continue
                if rel in NAVBAR_ONLY:  # settings lists: the set's rows from its top
                    h = 320 - g.bar - g.set_top if g.list_end else g.set_rows*g.set_row
                    assert n[1] == [0, g.set_top, 375, h] and 'item_height' not in n[2], (g.name, rel)
                else:                   # any other list with that row height is not one (settings_list)
                    assert n[2].get('item_height') == str(g.set_row), (g.name, rel)
        if g.text_x:  # text from text_x clears the glass at the first row and at list_end's last; the lists take the window
            assert g.text_x >= corner_x(g.bar + 6, g.pitch - 12) and g.list_end % g.pitch == 0, g.name
            assert corner_x(g.bar + g.list_end - g.pitch + 6, g.pitch - 12) <= g.text_x < corner_x(g.bar + g.list_end + 6, g.pitch - 12), g.name
            ends = {}
            for rel in UI_ASSETS:  # every list box the transform resizes ends at the window's end
                folder, _, base = rel.rpartition('/')
                mine = ui + (folder and folder + '/') + f'{g.name}_{base}'
                if 'squashfs-root/' + mine not in built or rel in NAVBAR_ONLY: continue
                was = {n[2].get('name'): n[1] for n in decode(read('stock.squashfs', ui + rel))[3]}
                for n in decode(read('rootfs.squashfs', mine))[3]:
                    old = was.get(n[2].get('name'))
                    if n[0] in ('list_view', 'table_view') and old and old[1] in (50, 100) and n[1] != old:
                        ends[rel] = n[1][1] + n[1][3]
            assert ends and set(ends.values()) == {320 - g.bar}, (g.name, ends)
        if g.bar_px:  # Classic's bar: one cap centre, the title clear of the glass, the clock centred, no idle mark
            m = status_metrics(g, CLASSIC_LIGHT_FONT_SRC)
            bar = {n[2].get('name'): n for n in walk(decode(read('rootfs.squashfs', ui + f'{g.name}_system_bar.bin')))}
            assert bar['label_title'][1] == m['title'] and bar['label_title'][2]['ellipses'] == 'true' and bar['label_clock'][1] == m['clock'] and 'label_idle' not in bar, g.name
            assert 2 * m['cap_top'] + m['cap'] in (g.bar - 3, g.bar - 2) and m['inset'] >= corner_inset(m['cap_top']), g.name
            assert 2 * m['clock'][0] + m['clock'][2] == 375, g.name
            # the battery's nub ends clear of the glass, at its top row, above the bar's two lines
            xm = g.bar_right
            assert xm >= corner_inset((g.bar - 2 - g.batt_h) // 2) and g.batt_h <= g.bar - 1 and bar['view_right'][2]['children_layout'].endswith(f'xm={xm},s={inc("STATUS_GAP")})'), g.name
            size = SCHEMA['bar.title.font_size'].field
            assert {t[size] for t in builtins() if g in geometry_sets([t])} == {g.bar_px}, g.name  # the theme's bar text is the set's
        if g.np_ipod:  # Classic's Now Playing: its text fits, in status_metrics' model (stb scales ascent - descent to the size)
            from fontTools.ttLib import TTFont
            face = TTFont(CLASSIC_LIGHT_FONT_SRC, lazy=True)
            cmap = face.getBestCmap()
            ink = lambda text, px: math.ceil(sum(face['hmtx'][cmap[ord(c)]][0] for c in text) * px / (face['hhea'].ascent - face['hhea'].descent))
            page = {n[2].get('name'): n for n in walk(decode(read('rootfs.squashfs', ui + f'{g.name}_{PLAYING_PAGE}')))}
            # the times beside the bar in "-9:59"'s boxes (the build's class, the widest bar) hold their font's line, their outer
            # edges and the bar's ends clear of the glass; so in every length class navigation.c ipod_times fits them to: each class's longest times, any digit, the outer
            # edges where the build put them, the gap kept, the bar between
            for name in ('label_playtime', 'label_ipod_remain'):
                x, y, w, h = page[name][1]
                assert w == NP_IPOD_TIME_WS[0] and inc('NP_IPOD_TIME_PX') <= h, (g.name, name)
                assert min(x, 375 - x - w) >= corner_x(g.bar + y, h), (g.name, name)
            (ex, ey, _, eh), (sx, sy, _, sh) = page['label_playtime'][1], page['slider_play'][1]
            for tw, longest in zip(NP_IPOD_TIME_WS, ('9:59', '59:59', '9:59:59')):
                bx = ex + tw + inc('NP_IPOD_TIME_GAP')
                for d in '0123456789':
                    assert ink('-' + re.sub(r'\d', d, longest), inc('NP_IPOD_TIME_PX')) <= tw, (g.name, tw, d)
                top = sy + (sh - inc('NP_BAR_IPOD')) // 2
                assert bx - inc('NP_IPOD_TIME_GAP') - tw == ex and bx >= corner_x(g.bar + top, inc('NP_BAR_IPOD') + inc('SCRUB_REFLECT_ROWS')), (g.name, tw)
                assert 375 - 2 * bx < page['slider_play'][1][2] or tw == NP_IPOD_TIME_WS[0], (g.name, tw)
            # the info page's rows (navigation.c ringnav_np_info): each holds the info role's size, its name fits, the rows end above
            # the dots and both columns clear the glass
            px = {t['font_px[ROLE_INFO]'] for t in builtins() if g in geometry_sets([t])}
            assert len(px) == 1, g.name
            px = px.pop()
            info = page['view_info'][3]
            dy = g.bar + page['slide_view_view'][1][1]
            for key, n in zip((b'album', b'genre', b'player_filesize', b'player_era', b'player_encoding', b'player_bitdepth', b'player_bitrate', b'player_samplerate', b'player_location'), info):
                value = page[n[2]['name'] + '_value']
                assert n[1][3] == value[1][3] >= px and ink(table[key].decode(), px) <= n[1][2] and value[1][0] == n[1][0] + n[1][2], (g.name, table[key])
                assert min(n[1][0], 375 - value[1][0] - value[1][2]) >= corner_x(dy + n[1][1], n[1][3]), (g.name, table[key])
            assert len(info) == 18 and info[8][1][1] + info[8][1][3] <= page['slide_indicator1'][1][1], g.name
    payload_symbols = symbols(directory/'patch.elf')
    for address in [AUDIT['immediates'][0]['sites'][0][0], '0x522410', '0x523de0', '0x4b3130', AUDIT['row_layout_calls']['sites'][0][0],
                    hex(inc('LIST_VIEW_LAYOUT_SLOT'))]:
        damaged = bytearray(stock)
        damaged[fileoff(stock, int(address, 16))] ^= 1
        try: patch_code(damaged, payload_symbols)
        except ValueError: pass
        else: raise AssertionError(f'Accepted a changed instruction at {address}')
    print('Asset geometry, exclusion parity and mismatch rejection passed.')

if __name__ == '__main__':
    import argparse, json, pathlib, subprocess, tempfile
    from unittest.mock import patch
    from build import build, run, sha
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('zip',type=pathlib.Path,nargs='?')
    ap.add_argument('--build', type=pathlib.Path)
    args=ap.parse_args()
    if args.build: validate_assets(args.build)
    if args.zip:
        # Reproducibility and update.tar's MD5s are release.py package's; this covers the logo and quoting.
        from build import ZIP_SHA, Q2_TAR_SHA
        import m1plus as m1
        m1plus = m1.takes(args.zip)
        assert m1plus or sha(args.zip.read_bytes()) in (ZIP_SHA, Q2_TAR_SHA), f'{args.zip}: not an audited firmware'
        card_logo = logo
        if m1plus:  # its splash is 320x480: a stand-in in the stock baseline RGB format
            from ipod import imagemagick
            card_logo = imagemagick('-size', '320x480', 'gradient:#335-#c96', '-type', 'TrueColor', '-strip', 'jpg:-', data=b'')
            assert jpeg_size(card_logo) == (320, 480)
        with tempfile.TemporaryDirectory(prefix='q2-package-') as tmp:
            root=pathlib.Path(tmp)
            custom=root/"custom ' logo.jpg"
            custom.write_bytes(card_logo)
            def change_source(*command):
                if command[0]=='mksquashfs': custom.write_bytes(b'edited during compression')
                return run(*command)
            a=root/"build ' a"
            with patch('build.run',side_effect=change_source), patch('m1plus.run',side_effect=change_source):
                build(args.zip,a,custom)
            validate_assets(a)
            manifest=json.loads((a/'manifest.json').read_text())
            assert manifest['logo_sha256']==sha(card_logo) and manifest.get('logo_source', 'custom')=='custom'
            for rel,expected in [('release/assets/default/raw/images/xx/logo.jpg',card_logo),
                                 ('release/bin/demo',(a/'demo').read_bytes())]:
                assert subprocess.check_output(['unsquashfs','-cat',str(a/'rootfs.squashfs'),rel])==expected
            if m1plus: assert manifest['version'] == M1_TAG, manifest['version']
            print('Packaging, mutable logo and quoted paths checks passed.')
