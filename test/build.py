#!/usr/bin/env python3
"""JPEG and boot script checks; --build BUILD audits a build (Q2 or M1 Plus), and a stock firmware ZIP
also tests packaging with a custom logo and quoted paths."""
import io, sys; sys.path.insert(0, sys.path[0] + '/../tools')  # tools/ first: test/build.py must import tools/build.py
from build import CAROUSEL, ICONS, LABELS, relabel, ROOT, STOCK_EQ, VERSIONS, dev_tag, jpeg_size, FONT, TAG_C, patch_m4b_cover

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
tags = [dev_tag(n, 'I') for n in range(1, 36**3)]
assert tags[:2] == ['V001i', 'V002i'] and tags[35] == 'V010i' and tags[-1] == 'VZZZi'
assert len(set(tags)) == len(tags) and all(len(t) == 5 for t in tags) and VERSIONS['ipod'] not in tags
assert dev_tag(36**3, 'S') == 'V001s'
print('Dev build tag checks passed.')

def boot_check(s90play=None):
    """S90play's dual boot under the host sh, with stand-in programs: build.py's BOOT_HOOK, or a
    built rootfs's whole S90play (its dbus start stubbed), run as init runs it."""
    import subprocess, tempfile, pathlib
    from build import BOOT_HOOK, ROCKBOX_FLAG
    with tempfile.TemporaryDirectory(prefix='q2-boot-') as tmp:
        r = pathlib.Path(tmp)
        script = (s90play or BOOT_HOOK[1]).decode().replace(' &\n', '\n')
        if s90play:
            stubs = ('/usr/bin/dbus-daemon --config-file=/etc/dbus-1/system.conf', '/usr/bin/q2remote')
            assert script.count(stubs[0]) == 1, 'S90play: no dbus start'
            for stub in stubs: script = script.replace(stub, ':')
            script = script.replace('/bin/mkdir', 'mkdir').replace('/var/run/', f'{r}/var/run/')
        for old in ('/mnt/', '/tmp/mmc_add', ROCKBOX_FLAG, '/usr/bin/q2boot', '/release/bin/demo'):
            script = script.replace(old, f'{r}{old}')
        script = script.replace('usleep 200000', ':')
        for d in ('mnt/data', 'mnt/mmc/.rockbox', 'tmp', 'usr/bin', 'release/bin'): (r/d).mkdir(parents=True)
        def exe(path, body): (r/path).write_text('#!/bin/sh\n' + body + '\n'); (r/path).chmod(0o755)
        # demo takes Home's Rockbox row (leaves the flag) as many times as the shortcuts file says
        flag, shortcuts = f'{r}{ROCKBOX_FLAG}', r/'shortcuts'
        exe('release/bin/demo', f'echo demo >> {r}/ran; n=$(cat {shortcuts}); '
            f'[ "$n" -gt 0 ] && echo $((n - 1)) > {shortcuts} && : > {flag}; exit 137')
        rb, target = r/'mnt/mmc/.rockbox/rockbox', r/'mnt/data/boot-target'
        def boot(held, card, code=81, shortcut=0):
            shortcuts.write_text(f'{shortcut}\n')
            exe('usr/bin/q2boot', 'exit ' + ('0' if held else '1'))
            if card: exe('mnt/mmc/.rockbox/rockbox', f'pwd >> {r}/ran; exit {code}')
            else: rb.unlink(missing_ok=True)
            (r/'ran').write_text('')
            subprocess.run(['sh', '-c', script, 'S90play', 'start'], check=True)
            return (r/'ran').read_text().split(), target.exists() and target.read_text().strip()
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
    print(f'Dual boot ({"built S90play" if s90play else "BOOT_HOOK"}): Rockbox by default, one-session Q2 Pod, stale choice ignored, card fallback and Home Rockbox row passed.')
boot_check()

def logo_check(s11logo=None):
    """S11logo_display_shell's splash choice under the host sh: build.py's LOGO_HOOK, or a built
    rootfs's whole script (its /dev/fb0 wait and ROTATEMODE choice included)."""
    import subprocess, tempfile, pathlib
    from build import LOGO_HOOK
    with tempfile.TemporaryDirectory(prefix='q2-logo-') as tmp:
        user, config = pathlib.Path(tmp)/'boot-logo.jpg', pathlib.Path(tmp)/'config.ini'
        script = (s11logo or LOGO_HOOK[1]).decode()
        if s11logo:
            assert script.count('"/dev/fb0"') <= 1
            script = script.replace(' &\n', '\n').replace('"/dev/fb0"', '/').replace('/mnt/data/config.ini', str(config))
        script = script.replace('/mnt/data/boot-logo.jpg', str(user)).replace('display_logo', 'echo')
        def shown(rotate=0):
            config.write_text(f'ROTATEMODE={rotate}\n')
            return subprocess.run(['sh', '-c', script, 'S11logo', 'start'], check=True, capture_output=True, text=True).stdout.strip()
        assert shown() == '/release/assets/default/raw/images/xx/logo.jpg'  # no card logo: the built-in splash
        user.write_bytes(b'')
        assert shown() == str(user)
        if 'logo180.jpg' in script:  # M1 Plus: a flipped screen keeps the stock flipped splash
            assert shown(1) == '/release/assets/default/raw/images/xx/logo180.jpg'
    print(f'Boot logo ({"built S11logo" if s11logo else "LOGO_HOOK"}): the saved card logo, else the built-in splash, passed.')
logo_check()

def shared_checks(directory, manifest, stock, demo, read):
    """What both models' builds share: the identity strings in demo, the M4B cover dispatcher, the
    helpers and init scripts, bluealsa, the watchdog and hciplayer."""
    import hashlib, pathlib, re, struct, subprocess, tarfile, tempfile
    from build import (sha, run, fileoff, segments, symbols, ROOT, TAG_C, patch_m4b_cover, HELPER, HELPER_LIKE, BOOT, BOOT_HOOK,
                       REMOTE, REMOTE_HOOK, S90PLAY, S11LOGO, LOGO_HOOK, RTC_WRITE, LOCK_CLOCK_12H, WATCHDOG,
                       WATCHDOG_SLEEP, BLUEALSA, AAC_44K1, STOCK_EQ)
    from peq import PLAYER_PROFILES
    m1plus = manifest['model'] == 'Shanling M1 Plus'
    assert manifest['version'].encode()+b'\0' in demo
    # Each of the model's call sites (build.py CALL_SITES) holds stock's word, now its replacement; the
    # manifest lists the M4B extension checks among them.
    from build import call_site_words
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
    assert tag_new == patch_m4b_cover(tag_old, m1plus=m1plus)
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
    else:
        assert 'q2remote_sha256' not in manifest
        assert not (directory/'q2remote').exists()
        absent = subprocess.run(['unsquashfs', '-cat', str(directory/'rootfs.squashfs'), REMOTE],
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        assert absent.returncode != 0, 'release rootfs contains q2remote'
    assert read('rootfs.squashfs', S90PLAY) == expected_start
    assert read('rootfs.squashfs', S11LOGO) == read('stock.squashfs', S11LOGO).replace(*LOGO_HOOK)  # the card's logo, if saved
    # bluealsa: AAC capability, the two DROP jumps, and one appended LOAD payload.
    from build import BT_DROP, BT_DROP_HANDLER, BT_DROP_PAYLOAD, patch_bluealsa, segments
    old, new = read('stock.squashfs', BLUEALSA), read('rootfs.squashfs', BLUEALSA)
    header = segments(old)[-1][0]
    allowed = {AAC_44K1, *range(header, header+32)}
    for address in (BT_DROP, BT_DROP_HANDLER):
        off = fileoff(old, address)
        allowed.update(range(off, off+8))
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
    # The crash watchdog only sleeps longer.
    old, new = read('stock.squashfs', WATCHDOG), read('rootfs.squashfs', WATCHDOG)
    assert new == old.replace(*WATCHDOG_SLEEP) and new != old
    # hciplayer's code (.text) differs from stock only in the VBR scan branch, now a nop, the 48 kHz EQ gates
    # and the ID3v2 walker calls, now id3_gain (MP3 ReplayGain); each model's at its own addresses.
    old, new = read('stock.squashfs', 'usr/bin/hciplayer'), read('rootfs.squashfs', 'usr/bin/hciplayer')
    profile = PLAYER_PROFILES[sha(old)]
    assert manifest['peq']['stock_sha256'] == sha(old) and manifest['peq']['sha256'] == sha(new)
    assert (directory/'peq'/'stock-hciplayer').read_bytes() == old
    text = re.search(r'\.text +PROGBITS +[0-9a-f]+ ([0-9a-f]+) ([0-9a-f]+) ', run('readelf', '-SW', directory/'peq'/'stock-hciplayer'))
    start, size = int(text[1], 16), int(text[2], 16)
    off = fileoff(old, profile['vbr_scan'])
    gates = [fileoff(old, a) for a in (*(a for a, _, _ in profile['eq_rate_gates']), *profile['id3_calls'])]
    differ = [i for i in range(start, start+size) if old[i] != new[i]]
    assert set(differ) <= {*range(off, off+4), *(i for g in gates for i in range(g, g+4))} and not any(new[off:off+4])
    assert [struct.unpack_from('<I', new, fileoff(old, a))[0] for a, _, _ in profile['eq_rate_gates']] == [p for _, _, p in profile['eq_rate_gates']]
    id3_gain = symbols(directory/'peq'/'peq.elf')['id3_gain']
    assert {struct.unpack_from('<I', new, fileoff(old, a))[0] for a in profile['id3_calls']} == {0x0c000000 | id3_gain >> 2}
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
    assert info == f"{manifest['model']}\n{manifest['version']}\n{hashlib.md5(kernel).hexdigest()}  recovery-update/xImage\n" \
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
    from build import (sha, run, fileoff, segments, symbols, pic_gp, BASE, M1PLUS_HOOKS, M1PLUS_GP, WM_PAINT_LEAF_M1PLUS,
                       PDR_M1PLUS, RTC_WRITE, RTC_READ_M1PLUS, LOCK_CLOCK_12H, TAG_C, ICONS, STOCK_EQ, OBSOLETE, HELPER,
                       BOOT, REMOTE, SCROBBLE_CA, BLUEALSA, WATCHDOG, S90PLAY, S11LOGO, call_site_words,
                       M1PLUS_PRIVATE_FUNCTIONS)
    ps = symbols(directory/'patch.elf')
    payload = (directory/'patch.bin').read_bytes()
    assert (sha(stock), sha(demo), sha(payload)) == (manifest['stock_demo_sha256'], manifest['demo_sha256'], manifest['patch_sha256'])
    # Only the Stock UI exists for M1 Plus so far.
    assert manifest['variant'] == 'stock' and manifest['compact_code'] == []
    assert set(manifest['changed_assets']) == {TAG_C}
    stock_syms = symbols(directory/'stock-demo')
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
    name, address, replacement, words = WM_PAINT_LEAF_M1PLUS
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
    # The Q2 Pod Home card (coverflow.c home_card) copies V2.1's Home grid. Its builder (0x534064)
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
    # the card comes back from its own to-foreground handler. Nothing loaded points to the builder
    # (.pdr, which isn't loaded, describes it).
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
    for old, new in (RTC_WRITE, RTC_READ_M1PLUS, LOCK_CLOCK_12H):  # same-length literals in place
        at = stock.index(old)
        assert stock.count(old) == 1 and len(new) == len(old) and demo[at:at+len(old)] == new, old
        allowed.update(range(at, at+len(old)))
    off, size = PDR_M1PLUS  # .pdr, past every LOAD segment, ships zeroed
    assert demo[off:off+size] == bytes(size) and any(stock[off:off+size])
    assert all(p[1]+p[4] <= off for _, p in segments(stock) if p[0] == 1)
    allowed.update(range(off, off+size))
    # The payload: stock's final PT_NULL header becomes its LOAD segment, R/W/X at BASE, after stock's bytes.
    old_segs, new_segs = segments(stock), segments(demo)
    assert [h for h, _ in old_segs] == [h for h, _ in new_segs] and [p for _, p in old_segs[:-1]] == [p for _, p in new_segs[:-1]]
    assert old_segs[-1][1][0] == 0
    start = (len(stock) + 65535) & ~65535
    assert new_segs[-1][1] == (1, start, BASE, BASE, len(payload), ps['__scratch_end'] - BASE, 7, 65536)
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
                                                                    'books', 'videos', 'longsongs')} | {
             xx+f'stream_{n}.png' for n in ('spotify', 'radio', 'airplay')} | {HELPER, SCROBBLE_CA, BOOT} | ({REMOTE} if manifest['dev'] else set())
    # The Q2 Pod Home card's pair, and the Q2 Pod page's Coverflow, Ratings and Most Played row icons.
    added |= {xx+f'{n}.png' for n in ('home_q2pod', 'home_q2pod_down', 'local_coverflow', 'local_fav', 'local_frequentplay')}
    replaced = {'release/bin/demo', 'usr/bin/hciplayer', BLUEALSA, WATCHDOG, S90PLAY, S11LOGO, TAG_C}
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
        # slide menus have nothing to act on (test/patch.py, Q2 only).
        pages = [p for p in old if '/raw/ui/' in p and p.endswith('.bin')]
        assert len(pages) > 100 and not [p for p in pages if b'slide_menu' in pathlib.Path(old[p]).read_bytes()]
        removed = {p for p in STOCK_EQ + OBSOLETE if p in old}
        assert set(new) == (set(old) - removed) | added, (set(new) ^ ((set(old) - removed) | added))
        differ = {p for p in set(old) & set(new) if os.path.isfile(old[p]) and not os.path.islink(old[p])
                  and not filecmp.cmp(old[p], new[p], shallow=False)}
        assert differ - {logo} == replaced, differ ^ replaced
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
    from build import sha, run, fileoff, symbols, BLUEALSA, AAC_44K1, IPOD_HOOKS, IPOD_LEAF, WM_PAINT_LEAF, HELPER, HELPER_LIKE, BOOT, BOOT_HOOK, REMOTE, REMOTE_HOOK, S90PLAY, S11LOGO, LOGO_HOOK, RTC_WRITE, LOCK_CLOCK_12H, WATCHDOG, WATCHDOG_SLEEP, PDR
    from ipod import (ART_PLACEHOLDERS, sized_art, AUDIT, TOOLBAR_SWITCHES, BOTTOM, CHEVRON_W, CONFIRM, VOLUME, QUICK_SETTINGS, QS_TOP, QS_LABEL_GAP, QS_LABEL_H,
                      QS_LABEL_W, QS_ROW_GAP, QS_PITCH, QS_BAR, QS_TOUCH, QS_EDGE, QS_SUN, HOME_LABEL_END, HOME_LIST_W, HOME_TEXT_X, HOME_TOP, PITCH, ARTIST_PAGE, HOME_PAGE, HOME_ROW, HOME_ROWS, NAVBAR_ONLY, PLAYING_PAGE, SET_ROW, SET_ROWS, SET_TOP, UI_ASSETS,
                      NP_BAR, NP_MARGIN, NP_POS_X, NP_TOP, STATUS_BAR, STATUS_HIDDEN, STATUS_LEFT, STATUS_MARGIN, STATUS_RIGHT, CLOCK_MIN, CLOCK_TEXT, corner_inset, corner_x,
                      STATUS_ICONS, status_icon, QUIET_ICONS, quiet_icon, SET_ICON, SET_STOCK_ICON, SETTINGS_ICONS, SETTINGS_SLIDERS, decode, slider_plain, imagemagick, inc, png_header, settings_icon, walk,
                      patch_asset, patch_code, patch_style, style_props, SLIDE)
    from build import source_sha256
    manifest = json.loads((directory/'manifest.json').read_text())
    assert manifest['source_sha256'] == source_sha256(), f'{directory} was built from other sources; rebuild into a fresh directory'
    ipod = manifest['variant'] == 'ipod'
    stock = (directory/'stock-demo').read_bytes()
    demo = (directory/'demo').read_bytes()
    def read(image, rel):
        return subprocess.check_output(['unsquashfs', '-cat', str(directory/image), rel])
    shared_checks(directory, manifest, stock, demo, read)
    if manifest['model'] == 'Shanling M1 Plus':
        m1plus_checks(directory, manifest, stock, demo, read)
        print(f'M1 Plus {manifest["variant"]}: hook jumps, demo diff, rootfs file parity and boot scripts passed.')
        return
    # All original executable bytes outside the reviewed hooks, version and compact sites
    # must remain stock; the payload and ELF mapping are independently hashed by the runner.
    if not ipod:
        for group in [*AUDIT['immediates'], AUDIT['row_layout_calls'],
                      {'sites': [('0x522410', '0x0320f809'), ('0x523de0', '0x0320f809')]}]:
            for address, _ in group['sites']:
                off = fileoff(stock, int(address, 16))
                assert demo[off:off+4] == stock[off:off+4]
    # .pdr (build.py PDR), past every LOAD segment, ships zeroed.
    assert demo[PDR[0]:PDR[0]+PDR[1]] == bytes(PDR[1]) and any(stock[PDR[0]:PDR[0]+PDR[1]])
    # The slide hint names a stock animator and gives it a duration (a missing one means stock's 500 ms).
    assert re.fullmatch(r'htranslate\(duration=\d+\)', SLIDE) and b'\0htranslate\0' in stock
    # Only iPod's animated lookup pages need synchronous unwind; Stock keeps its Back calls.
    for address, slot in ((0x4a6250, 0x468), (0x4ad458, 0x468), (0x526e70, 0x420)):
        off = fileoff(stock, address)
        want = struct.pack('<III', 0x8f99a8f8, 0x0320f809, 0x8fa40000 | slot) if ipod else stock[off:off+12]
        assert demo[off:off+12] == want
    # iPod alone jumps from these entry points to its payload (build.py pins the leaf's words);
    # Stock keeps all of them stock.
    for address, name in [*(h[:2] for h in IPOD_HOOKS.values()), IPOD_LEAF[1:3]]:
        off = fileoff(stock, address)
        want = stock[off:off+8]
        if ipod: want = (0x08000000 | symbols(directory/'patch.elf')[name] >> 2).to_bytes(4, 'little') + bytes(4)
        assert demo[off:off+8] == want
    # Both jump from window_manager_paint (Videos).
    off = fileoff(stock, WM_PAINT_LEAF[1])
    assert demo[off:off+8] == (0x08000000 | symbols(directory/'patch.elf')[WM_PAINT_LEAF[2]] >> 2).to_bytes(4, 'little') + bytes(4)
    changed = manifest['changed_assets']
    xx = 'release/assets/default/raw/images/xx/'
    assert set(changed) == {'release/assets/default/raw/ui/'+p for p in (UI_ASSETS if ipod else [ARTIST_PAGE, HOME_PAGE])} | {
        'release/assets/default/raw/styles/'+p for p in (AUDIT['styles'] if ipod else [])} | {
        xx+n for n in (SETTINGS_ICONS | QUIET_ICONS | STATUS_ICONS | ART_PLACEHOLDERS if ipod else [])} | {'release/assets/default/raw/strings/en_US.bin', FONT, TAG_C}
    master = (ROOT/'assets/icons/default_album_home.png').read_bytes()
    for name, size in ART_PLACEHOLDERS.items():
        old, new = read('stock.squashfs', xx+name), read('rootfs.squashfs', xx+name)
        if ipod: assert png_header(new)[:2] == (size if isinstance(size, tuple) else (size, size)), name
        assert new == (sized_art(master, size) if ipod else old), name
        if ipod:
            assert changed[xx+name] == dict(original_sha256=sha(old), sha256=sha(new))
            if not isinstance(size, tuple):  # transparent corners, not black, over a selected row
                assert imagemagick('png:-', '-format', '%[fx:p{0,0}.a]', 'info:', data=new) == b'0', name
    if ipod:
        flow = read('rootfs.squashfs', xx+'default_album_flow.png')
        assert flow == sized_art(master, 160) and png_header(flow) == (160, 160, 8, 6)
        assert read('rootfs.squashfs', xx+'default_album_home.png') == master
    if ipod:
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
    # iPod settings icons: the audited 52px artwork, packaged as SET_ICON RGBA with the same transparency
    # and, on a plain background, the same average colour; Stock keeps them stock. Minimal greys them
    # as they load (navigation.c ringnav_image_add: every disc MINIMAL_CHEVRON, glyphs white).
    def mean(png, bg):
        cmd = ['png:-', '-background', bg, '-flatten', '-format', '%[fx:mean.r],%[fx:mean.g],%[fx:mean.b]', 'info:']
        return [float(v) for v in imagemagick(*cmd, data=png).split(b',')]
    for name, digest in SETTINGS_ICONS.items():
        old, new = read('stock.squashfs', xx+name), read('rootfs.squashfs', xx+name)
        assert sha(old) == digest and png_header(old) == (SET_STOCK_ICON, SET_STOCK_ICON, 8, 6), name
        if not ipod:
            assert new == old, name
            continue
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
    # iPod drops the carousel images and adds no Coverflow icons; Stock keeps both.
    icons = {'squashfs-root/release/assets/default/raw/images/xx/'+n for n in ICONS}
    carousel = {'squashfs-root/'+rel for rel in CAROUSEL}
    assert (carousel & names == (set() if ipod else carousel)) and (icons & names == (set() if ipod else icons))
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
            # iPod rows are transparent, so a light list container stock hid behind them would show.
            bad += [c for c in now if ipod and c[2] == 'bg_color' and jarring(c)
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
        assert new == patch_asset(short, original, ipod), short
        root = decode(new)
        if ipod and short in SETTINGS_SLIDERS:
            before = {n[2].get('name'): n for n in walk(decode(original))}
            assert not [n for n in walk(root) if n[0] == 'image' and n[2].get('image')]  # no endpoint glyphs
            gone = [n for n in walk(root) if n[2].get('name') in before and before[n[2]['name']][2].get('image')]
            assert len(gone) == 2 and all(n[1][2:] == [0, 0] and n[1][:2] == before[n[2]['name']][1][:2] for n in gone)
            for n in walk(root):
                if n[0] == 'slider' or n[2].get('name') in ('img_add', 'img_dec'):
                    assert n == before[n[2]['name']]  # ranges, touch and wheel controls stay stock
        if short == VOLUME:  # Hidden before the first paint, including transition snapshots.
            plain = decode(original); del plain[2]['highlight']
            for child in plain[3]: child[2]['visible'] = 'false'
            assert root == plain
            continue
        # iPod: browsing, settings and the PEQ editor slide; Home, Now Playing, the bar and dialogs don't.
        slides = ipod and short not in (HOME_PAGE, STATUS_BAR, PLAYING_PAGE, QUICK_SETTINGS, CONFIRM)
        assert root[2].get('anim_hint') == (SLIDE if slides else None), short
        if ipod:  # screen coordinates: the bar, full-screen dialogs (quick settings slides down from -320), windows
            origin, window = {STATUS_BAR: (0, (0, 30)), QUICK_SETTINGS: (320, (0, 320)), CONFIRM: (0, (0, 320))}.get(short, (30, (30, 320)))
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
        if short == HOME_PAGE and not ipod:  # only the Coverflow card is added
            cards = [n[2]['name'] for n in root[3][0][3]]
            assert cards[:3] == ['btn_playing', 'btn_localmusic', 'btn_coverflow'] and len(cards) == 7, cards
            assert root[3][0][3][1][3][1][2]['text'] == 'Library'  # literal: stock skips label_library
            continue
        if short == HOME_PAGE:  # seven rows with the stock names, beside the art; bytes equal patch_asset above
            art, (lv, lg, _, [sv]), (sl, sg, sp, [ss]) = root[3]
            assert lv == 'list_view' and sv[0] == 'scroll_view' and art[2]['name'] == 'img_homeart'
            # The Settings list: stock's Playback and System setting rows (stock binds them; their
            # labels are literal), hidden in the list's place until Home's Settings row slides it in.
            assert sl == 'list_view' and sp['name'] == 'list_view_homeset' and sp['visible'] == 'false'
            assert sg == [0, HOME_TOP, HOME_LIST_W, 2*HOME_ROW] and [r[2]['name'] for r in ss[3]] == ['btn_playset', 'btn_sysset']
            assert [r[3][1][2]['name'] for r in ss[3]] == ['img_playset', 'img_sysset'] and [r[3][0][2]['text'] for r in ss[3]] == ['Playback', 'System']
            # The art fills the right panel below the status bar; the payload fits and crops it.
            assert art[0] == 'image' and art[1] == [0, 0, 375, 290] and art[2]['draw_type'] == 'fill' and HOME_LIST_W == 375
            assert all(v == '#00000000' for k,v in root[3][1][2].items() if k.startswith('style:'))
            assert [r[2]['name'] for r in sv[3]] == ['btn_'+n for n in HOME_ROWS] and HOME_ROWS[2] == 'coverflow'
            for name, (_, _, _, (label, image)) in zip(HOME_ROWS, sv[3]):
                assert label[2]['name'] == ('label_library' if name == 'localmusic' else 'label_'+name)
                assert image[2] == {'name': 'img_'+name, 'clickable': 'true'}
                # Labels end before the chevron's glyph; longer ones scroll (only_focus) or end in an ellipsis.
                assert label[1][0] + label[1][2] == image[1][2] - HOME_LABEL_END and label[1][2] >= 100
                assert label[2]['only_focus'] == 'true' and label[2]['ellipses'] == 'true'
            assert [r[3][0][2].get('text') for r in sv[3]] == [None, 'Library', 'Coverflow', None, 'Rockbox', None, 'Settings']
            assert lg == [0, HOME_TOP, HOME_LIST_W, 7*HOME_ROW] and HOME_TOP + 7*HOME_ROW <= BOTTOM - HOME_TOP
            assert b'menu_' not in new and b'slide_menu' not in new
            dot = inc('HOME_DOT_X'), inc('HOME_DOT')
            assert HOME_TEXT_X == sum(dot) + inc('HOME_DOT_GAP')
            # The dot and the labels clear the bottom row's corner.
            assert dot[0] >= corner_x(30 + HOME_TOP + 6*HOME_ROW + (HOME_ROW - dot[1])//2, dot[1])
            assert HOME_TEXT_X >= corner_x(30 + HOME_TOP + 6*HOME_ROW + 9, 20)
            # Split (coverflow_home_layout) gives Minimal's menu 45% of the screen, Classic's half, the art the rest;
            # Full's rows end at HOME_CLASSIC_ROW, so the chevron's glyph (x 20 to 31, y 16 to 34 of
            # list_into, centred on the row) mirrors the labels' margin and, on the last row, clears
            # the bottom-right corner as the label clears the bottom-left.
            assert inc('HOME_SPLIT_W') == 375 // 2
            glyph_end = inc('HOME_CLASSIC_ROW') - CHEVRON_W + 31
            glyph_y = 30 + HOME_TOP + 6*HOME_ROW + (HOME_ROW - 50) // 2 + 16
            assert 375 - glyph_end == inc('HOME_CLASSIC_TEXT_X') >= corner_x(glyph_y, 34 - 16)
            assert inc('HOME_CLASSIC_TEXT_X') >= corner_x(30 + HOME_TOP + 6*HOME_ROW + 9, 20)
            continue
        if short == STATUS_BAR:  # iPod only: play state left, title between, four icons right
            left, right, *rest = root[3]
            assert [n[2]['name'] for n in left[3]] == STATUS_LEFT and [n[2]['name'] for n in right[3]] == STATUS_RIGHT
            title = rest.pop()
            assert title[0] == 'hscroll_label' and title[2]['name'] == 'label_clock'
            x, _, w, _ = title[1]
            assert x + w/2 == 375/2 and w >= CLOCK_MIN  # centred on the screen, clear of both groups (corners below)
            assert inc('CLOCK_EDGE') >= corner_x((30 - 20) // 2, 20) and x >= inc('CLOCK_EDGE')
            assert title[2]['style:normal:font_size'] == '16'
            assert all(v[2]['children_layout'].endswith(f'xm={STATUS_MARGIN},s={inc("STATUS_GAP")})') for v in (left, right))
            idle = rest.pop()
            assert idle[1] == [STATUS_MARGIN, 0, 28, 30] and idle[2]['text'] == 'Q2' and idle[2]['visible'] == 'false'
            assert idle[2]['style:normal:font_size'] == '18' and STATUS_MARGIN >= corner_x(6, 18)
            assert STATUS_MARGIN + 28 < x
            assert [n[2]['name'] for n in rest] == STATUS_HIDDEN and all(n[1][0] + n[1][2] < 0 for n in rest)
            # The Battery setting's percentage and payload battery start hidden (navigation.c bar_sync).
            pct, slot = right[3][2:4]
            assert pct[1][2] == inc('BATT_PCT_W') and pct[2]['visible'] == 'false' and pct[2]['style:normal:text_align_h'] == 'right' and pct[2]['style:normal:font_size'] == str(inc('BATT_PCT_PX'))
            assert slot == ['view', [0, 0, inc('BATT_BODY_W') + inc('BATT_NUB_W') + inc('BATT_GAP') + inc('BATT_PCT_W'), 0], {'name': 'view_battery', 'visible': 'false'}, []]
            continue
        if short == PLAYING_PAGE:  # iPod only: see the sketch in docs/ipod.md
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
            # Order and favourite at the page's foot; favourite centred below More.
            assert [n[1] for n in album] == [[16, 10, 166, 166], [39, 33, 120, 120], [194, 31, 165, 28], [194, 65, 165, 22], [194, 93, 165, 22],
                                             [247, 136, 50, 50], [303, 136, 50, 50]]
            assert album[-1][1][0] == named['img_more'][1][0] and album[-1][1][2] == named['img_more'][1][2] == 50
            assert album[-1][1][0] - (album[-2][1][0] + album[-2][1][2]) == 6 and 93 + 22 < 136 + 13
            assert album[1][2]['opacity'] == '0'  # playback gestures retain their original target
            assert album[2][2]['style:normal:font_size'] == '22' and album[3][2]['style:normal:font_size'] == '18'
            for node, color in ((album[3], '#CCCCCC'), (album[4], '#BBBBBB')):
                assert {v for k, v in node[2].items() if k.endswith(':text_color')} == {color}
            assert pos[0] == NP_POS_X and album[0][1][0] == NP_MARGIN and 375 - 16 == album[2][1][0] + album[2][1][2]
            # Distinct bands: top row, art, page dots, bar (A-B markers y 250 to 260), then the times.
            dots = named['slide_indicator1'][1]
            assert NP_TOP + 10 + 166 < NP_TOP + dots[1] and NP_TOP + dots[1] + 10 < NP_BAR[1] - 1
            assert named['slide_view'][1] == [0, 0, 375, 186] and named['view_lrc'][2]['self_layout'].startswith('default(x=75,')
            slider = named['slider_play']
            assert slider[1] == [NP_BAR[0], 240, NP_BAR[2], 30] and slider[2]['bar_size'] == '4' and slider[2]['slide_with_bar'] == 'true'
            assert not [k for k in slider[2] if k.endswith((':bg_image', ':fg_image', ':icon'))]
            assert {v for k, v in slider[2].items() if k.endswith('_color')} == {'#1c1c1c', '#6e6e6e'}
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
            # nothing but the hint changes (and Startup volume's slider glyphs go)
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
            assert gif[1] == [375 - corner_x(30, old[1][3]) - old[1][2], *old[1][1:]]
            assert nav[2].get('visible') != 'false' and nav[2].get('enable') != 'false'
            gif[1][0] = old[1][0]
            assert nav == old_nav, 'only the right button keeps clear of the glass'
        else:
            assert not ipod or nav[2]['visible'] == 'false' and nav[2]['enable'] == 'false'
        assert not ipod or not [v for n in walk(root) if n[0] in ('button', 'list_item', 'table_row')
                                for k, v in n[2].items() if k.endswith(':bg_color') and v == '#000000'], 'Opaque inline row background'
        old_nodes, new_nodes = list(walk(decode(original))), list(walk(root))
        assert len(old_nodes) == len(new_nodes)
        for old, node in zip(old_nodes, new_nodes):
            for key, value in old[2].items():
                if 'font' in key or key == 'style': assert node[2][key] == value
        if short in ('folder_page.bin', 'localmusic_page.bin', 'localmusic/localclass_page.bin', 'localmusic/playlist_page.bin'):
            surface = next(n for n in root[3] if n[0] in ('list_view', 'table_view'))
            top = 50 if short == 'localmusic/playlist_page.bin' else 0
            assert surface[1][1:] == [top, 375, BOTTOM-top], 'Lists must fill the client area'
            assert 4*PITCH <= BOTTOM, 'Four complete rows must fit'
        # Corrupt inputs must be rejected, never silently patched.
        try: patch_asset(short, original[:-1]+b'x', ipod)
        except ValueError: pass
        else: raise AssertionError('Accepted a changed asset')
    if ipod:
        payload_symbols = symbols(directory/'patch.elf')
        for address in [AUDIT['immediates'][0]['sites'][0][0], '0x522410', '0x523de0', '0x4b3130', AUDIT['row_layout_calls']['sites'][0][0],
                        hex(inc('LIST_VIEW_LAYOUT_SLOT'))]:
            damaged = bytearray(stock)
            damaged[fileoff(stock, int(address, 16))] ^= 1
            try: patch_code(damaged, payload_symbols)
            except ValueError: pass
            else: raise AssertionError(f'Accepted a changed instruction at {address}')
    print(f'{manifest["variant"]}: asset geometry, exclusion parity and mismatch rejection passed.')

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
        from build import INPUTS, M1PLUS_BIN_SHA
        assert sha(args.zip.read_bytes()) in INPUTS, f'{args.zip}: not an audited firmware'
        m1plus = INPUTS[sha(args.zip.read_bytes())][1] == M1PLUS_BIN_SHA
        card_logo = logo
        if m1plus:  # its splash is 320x480: a stand-in in the stock baseline RGB format
            from ipod import imagemagick
            card_logo = imagemagick('-size', '320x480', 'gradient:#335-#c96', '-type', 'TrueColor', '-strip', 'jpg:-', data=b'')
            assert jpeg_size(card_logo) == (320, 480)
        for ipod in (False,) if m1plus else (False, True):
          with tempfile.TemporaryDirectory(prefix='q2-package-') as tmp:
              root=pathlib.Path(tmp)
              custom=root/"custom ' logo.jpg"
              custom.write_bytes(card_logo)
              def change_source(*command):
                  if command[0]=='mksquashfs': custom.write_bytes(b'edited during compression')
                  return run(*command)
              a=root/"build ' a"
              with patch('build.run',side_effect=change_source):
                  build(args.zip,a,custom,ipod)
              validate_assets(a)
              manifest=json.loads((a/'manifest.json').read_text())
              assert manifest['logo_sha256']==sha(card_logo) and manifest['logo_source']=='custom'
              for rel,expected in [('release/assets/default/raw/images/xx/logo.jpg',card_logo),
                                   ('release/bin/demo',(a/'demo').read_bytes())]:
                  assert subprocess.check_output(['unsquashfs','-cat',str(a/'rootfs.squashfs'),rel])==expected
              if m1plus:  # no iPod UI for M1 Plus yet, so no build may claim one
                  try: build(args.zip, root/'ipod', custom, True)
                  except ValueError as e: assert 'no iPod build' in str(e), e
                  else: raise AssertionError('Built an M1 Plus iPod variant')
              print('Packaging, mutable logo and quoted paths checks passed.')
