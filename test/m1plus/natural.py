#!/usr/bin/env python3
"""test/hci_natural.py's natural changes on V2.1's hciplayer, at V2.1's addresses (m1plus.PLAYER_PROFILE): the fixes
tools/m1plus.py patch_player ports from tools/peq.py, run in the real player on test/hci_emu.py as on the Q2.

A next file no demuxer knows leaves the song playing to its last frame, then reports (PROBE_STOP, STOP_SITES,
STOP_FILL); a stop landing in that open still stops. A next file that ends as it starts sends its exit no sooner than
300 ms after the song's (EXIT_HOLD): the FLAC cut inside its metadata reached by a natural change, G3, is one. A header
that understates the length cuts nothing, and an MP3's frame count ends the junk after it (FORCED_EOF). A preload the
song outran or the queue closed is dropped (PRELOAD_*, COLD_CLEAR). A FLAC seek near the end keeps that end
(FLAC_GATE, SEEK_NOSYNC, SEEK_WORDS).
Usage: test/m1plus/natural.py BUILD_DIR [PLAYER]  (PLAYER: another V2.1 hciplayer, e.g. BUILD_DIR/peq/stock-hciplayer,
to see stock fail). CASES=name,... runs only those (hci_natural.py's function names). Needs ffmpeg and flac on PATH,
as test/hci_natural.py: gates.py's natural step puts nixpkgs' there."""
import os, pathlib, random, shutil, struct, sys, traceback
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]/'tools'))
from build import sha
from m1plus import M1PLUS_PLAYER_SHA, PLAYER_PROFILE as P
import hci_natural as n

# V2.1's twins of hci_natural.py's V1.32 addresses: the profile's where it has them; the rest found as the first checks
# found the sites (work/unported/r2/2.1a), a 49-word window matched at the same delta as the code around them
n.AUTH = 0x43050c                         # the licence check, as player_faults.py's
n.STOP, n.NEXT, n.LENGTH = P['stop_flag'], P['preload_state'], P['length_addr']
n.COLD_PATH, n.FREE_PRELOAD = P['cold_clear'][0], P['preload_free']
n.LAVF_CHECK, n.LAVF_PREFERRED = 0x4ae124, 0x4aeafc  # V1.32's less 0x540
n.STOP_READ = 0x4223dc                    # lw $a1, 0xe54($s1), V1.32's 0x4223c8
n.FORCED = (0x4855ac, 0x4855b4)           # the probe loop's, V1.32's less 0x540
n.ISO_STOP, n.AAC_STOP, n.ASF_STOP = (a for a, _, _ in P['stop_sites'])
n.ISO_TOC, n.ISO_ZEROS = 0x469c00, (0x46b908, 0x469a80)  # V1.32's 0x46a010 (less 0x410); its two jal targets
n.DAC_HELPER = 0x43ae74                   # V1.32's 0x43b280
# V2.1's list tries lavf ahead of the DSD checks (stock's order): a thread that gives up at one has met lavf first.
# A junk .iso or .dff its forced check (0x4855ac) let by meets lavf, too, and the thread gives up there
n.LAVF_LAST = False
# mp3_gapless.c isn't in V2.1's player yet (step 3 of .plan/unported-r2.md): each MP3 keeps LAME's delay and padding,
# 1836 frames on x.mp3 here, and the two joined files ran 0.11 s over with nothing past the count
n.PAST_THE_COUNT = (('joined.mp3', 2 * n.N, -0.1, 0.15), *n.PAST_THE_COUNT[1:])


def rate_dff():
    """A DSDIFF file whose FS chunk holds a rate V2.1 doesn't take (44.1 kHz), next: the DFF check's own failure store
    (0x47a4d8, probe_stop_dff), which a junk .dff never reaches, stores nothing on the thread, which goes on probing.
    KNOWN GAP: V2.1's list then reaches lavf, which takes the file, and its decoder's store (0x507dd0, V1.32's 0x508370,
    one peq_player.c's ponytail leaves) still stops the song. On the Q2 the DFF check comes first and the thread gives up."""
    def chunk(cid, body): return cid + struct.pack('>Q', len(body)) + body + bytes(len(body) & 1)
    prop = b'SND ' + chunk(b'FS  ', struct.pack('>I', 44100)) + chunk(b'CHNL', struct.pack('>H', 2) + b'SLFTSRGT') + \
           chunk(b'CMPR', b'DSD ' + bytes([14]) + b'not compressed\0')
    body = b'DSD ' + chunk(b'FVER', struct.pack('>I', 0x01050000)) + chunk(b'PROP', prop) + \
           chunk(b'DSD ', random.Random(4).randbytes(44100 // 8 * 2))
    (n.aud/'rate.dff').write_bytes(chunk(b'FRM8', body))
    site, decoder = P['probe_stop'][1][0], 0x507dd0
    p = n.Player()
    hit, stores = [], []
    p.e.watch_fn(site, lambda e: hit.append(e.cur.tid))
    p.e.watch_fn(site + 0x10, lambda e: stores.append((e.cur.tid, site + 0x10)))  # the flag's store, in the b's delay slot
    p.e.watch_fn(decoder, lambda e: stores.append((e.cur.tid, decoder)))
    p.song('a.flac')
    p.run(1)
    p.gapless('rate.dff')
    p.run(1)
    n.check([t for t in hit if t != 1], f'rate.dff: the thread reached 0x{site:x} ({hit})')
    n.check(not [a for t, a in stores if t != 1 and a != decoder], f'rate.dff: the DFF check stores no stop on the thread ({[(t, hex(a)) for t, a in stores]})')
    print(f'KNOWN GAP rate.dff: lavf takes it on the thread and its decoder stores the stop: {[t for t, a in stores if a == decoder]}')


def g3():
    """2.8: the natural change onto cutblock.flac, a FLAC cut where its next metadata header should be. Its preload
    succeeds, the song's end swaps it in, it ends at once, and stock sends both exits in one 10 ms poll: demo keeps
    the newest status only, so the queue sat on it at 00:00 until a key. Now they come at least 0.3 s apart."""
    n.next_ends_at_once('cutblock.flac', 0.3)


CASES = [
    ('seam', ()), ('bad_next', ('junk.flac',)), ('bad_next', ('empty.flac',)), ('bad_next', ('junk.dff',)),
    ('bad_next', ('junk.iso',)), ('bad_next', ('big.flac',)), ('bad_next', ('big.aac', n.AAC_STOP)),
    ('bad_next', ('nostreams.wma', n.ASF_STOP)), ('rate_dff', ()), ('iso_no_tracks', ()), ('exit_apart', ()), ('g3', ()), ('metadata_cut', ()),
    ('next_whole', ('x.wma',)), ('next_whole', ('bigmeta.flac',)), ('stop_in_failed_open', ()), ('stop_while_open', ()),
    ('understated', ()), ('late', (1.5,)), ('late', (0,)), ('late_failed', ()), ('second_cold', ()), ('race_publish', ()),
    ('race_cold', ()), ('close_while_open', (False,)), ('close_while_open', (True,)), ('close_while_open', ('race',)),
    *(('tail_noise', c) for c in (('junkx.mp3', 1), ('junkx.m4a', 0.1), ('junkx.ogg', 0.1), ('junkx.wv', 0.1),
                                  ('junkx.flac', 0.1), ('junkx.wav', 0.1), ('junkx.wma', 0.1), ('junkh.mp3', None))),
    ('understated_mp3', ('off.mp3',)), ('understated_mp3', ('cut.mp3',)), ('understated_mp3', ('x.mp3',)),
    ('past_the_count', ()), ('dsd', ()), *(('seek_flac', c) for c in n.SEEKS),
    ('seek_flac', ('s44m', 44100, 215 * 4096 + 3000, 4096)), ('seek_next', ()), ('seek_past_end', ()), ('seek_filtered', (0,)),
]


if __name__ == '__main__':
    stock = sha((n.build/'peq'/'stock-hciplayer').read_bytes())
    assert stock == M1PLUS_PLAYER_SHA, f'not an M1 Plus build: {stock}'
    print(f'player: {n.player}', flush=True)
    n.failures = []
    only = set(filter(None, os.environ.get('CASES', '').split(',')))
    n.setup()
    for name, args in CASES:
        if only and name not in only: continue
        try:
            (globals().get(name) or getattr(n, name))(*args)
        except Exception as x:  # stock lacks the payload's symbols race_* inject at, and a stock hang can fault
            traceback.print_exc()
            n.check(False, f'{name}{args}: {type(x).__name__}: {x}')
    assert not n.failures, f'{len(n.failures)} failed: {n.failures}'
    shutil.rmtree(n.work)
    print('natural: all passed')
