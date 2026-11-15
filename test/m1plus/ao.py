#!/usr/bin/env python3
"""test/hci_ao.py's output cases on V2.1's hciplayer, at V2.1's addresses (m1plus.PLAYER_PROFILE's dac_release,
ao_init_slot, ao_uninit_slot, usb_buffer and the globals they read), in the real player on test/hci_emu.py as on the Q2.

A natural change at another format reopens at what the file is, and one at the same format keeps the PCM whole; a kept
PCM that runs dry before the first write moves past hw_ptr (ao_write); a resume after a pause on the jack replays the
ring's frames from the fade (dac_resume); a natural start that skipped demo's mute waits for the line before frames
(dac_ioctl), and a natural end out of DSD sets ao_uninit's word. Two of V2.1's own: a USB DAC's buffer is 500 ms, not
stock's 100 ms (usb_buffer), and on a USB DAC that negotiated 48 kHz for a 44.1 kHz album the next track's same request
keeps the PCM open (ao_init's held request) where stock closes and reopens it. Bluetooth's cases compare a cold change
with a preload through stock's resampler on both routes, so they need no carry (2.6, round 2 step 7).
Usage: test/m1plus/ao.py BUILD_DIR [PLAYER]  (PLAYER: another V2.1 hciplayer, e.g. BUILD_DIR/peq/stock-hciplayer, to
see stock fail). CASES=name,... runs only those. Needs ffmpeg on PATH, as test/hci_ao.py: gates.py's step puts
nixpkgs' there."""
import os, pathlib, shutil, signal, sys, traceback
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]/'tools'))
from build import sha
from m1plus import M1PLUS_PLAYER_SHA, PLAYER_PROFILE as P
import hci_ao as h

# V2.1's twins of hci_ao.py's V1.32 addresses
h.AUTH = 0x43050c                       # the licence check, as player_faults.py's
h.WAY, h.NEXT_FLAG = P['output_way'], P['next_flag']
h.STOCK_UNINIT = P['stock_ao_uninit']
h.HOLD_AFTER = P['exit_hold'][0] + 8    # past exit_hold's jal and its delay slot, as V1.32's 0x4226dc
failures = []


def usb_buffer():
    """The buffer time ao_alsa's init asks for (set_buffer_time_near): 500 ms on every way; stock cuts USB's to 100."""
    got = {}
    for way in 0, 2:
        p = h.Player(way)
        p.song('a44.flac')
        assert p.until(lambda: p.e.pcm and p.e.pcm.appl > 0, 3), way
        got[way] = p.e.pcm.buffer_us
    print(f'  buffer time by way: {got}')
    assert got == {0: 500000, 2: 500000}, got
    print('USB DAC: the PCM keeps its 500 ms buffer, as the jack.')


def held_request():
    """A USB DAC that takes only 48 kHz: a 44.1 kHz album's next track asks again for 44.1, and ao_init asks for what the
    DAC gave last time, so the PCM stays open. A cold natural change (no preload, no mark: USB has no demo mute) and a
    skip while playing. Stock compares the request with what the DAC negotiated, and reopens each time."""
    for how in 'natural', 'skip':
        p = h.Player(2, 48000)
        p.song('a44.flac')
        if how == 'natural':
            assert p.until(p.ended, 8)
        else:
            p.run(0.6)
        p.song('b44.flac')
        p.run(h.SECONDS + 0.8)
        opens = [k for _, n, k in p.e.events if n == 'pcm_open']
        print(f'  {how}: {len(p.e.streams)} PCM(s), rates {[s.rate for s in p.e.streams]}')
        assert len(p.e.streams) == 1 and p.e.pcm.rate == 48000 and len(opens) == 1, (how, len(p.e.streams), len(opens))
    print('USB DAC at 48 kHz only: a 44.1 kHz album keeps one PCM across a natural change and a skip.')


CASES = (*h.CASES, usb_buffer, held_request)


if __name__ == '__main__':
    stock = sha((h.build/'peq'/'stock-hciplayer').read_bytes())
    assert stock == M1PLUS_PLAYER_SHA, f'not an M1 Plus build: {stock}'
    print(f'player: {h.player}', flush=True)
    only = set(filter(None, os.environ.get('CASES', '').split(',')))
    signal.alarm(3000)  # a spinning player fails the run
    h.setup()
    for case in CASES:
        if only and case.__name__ not in only: continue
        try:
            case()
            print(f'ok   {case.__name__}', flush=True)
        except Exception as e:
            traceback.print_exc()
            print(f'FAIL {case.__name__}: {e!r}'[:400], flush=True)
            failures.append(case.__name__)
    assert not failures, f'{len(failures)} failed: {failures}'
    shutil.rmtree(h.work, ignore_errors=True)
    print('ao: all passed')
