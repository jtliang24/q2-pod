#!/usr/bin/env python3
"""test/player_seam.py's seams on V2.1's hciplayer: the MP3 delay and padding trim (patch/mp3_gapless.c) and the
M4A, Opus and Vorbis priming and padding trim (patch/lavf_gapless.c) that tools/m1plus.py patch_player ports from
tools/peq.py, measured in samples in the real player on test/hci_emu.py as on the Q2. HE-AAC and every file whose
numbers are of no use come out as V2.1's stock player plays them (BUILD_DIR/stock.squashfs is V2.1's in an M1 build).

The only V1.32 address in player_seam.py is its licence check, AUTH; V2.1's is player_faults.py's. Every case runs
but Bluetooth's, which goes through the 48 kHz resampler's rs_open (2.6, not ported yet).
Usage: test/m1plus/seam.py BUILD_DIR [PLAYER]  (PLAYER: another V2.1 hciplayer, e.g. BUILD_DIR/peq/stock-hciplayer,
to see stock fail). Needs ffmpeg (with libvorbis and libopus) and lame on PATH, as test/player_seam.py: gates.py's
seam step puts nixpkgs' there."""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import player_seam as s

s.AUTH = 0x43050c  # the licence check, as player_faults.py's (V1.32's 0x43084c)


def bluetooth(exe, root, aud, tmp):
    print('  NOT PORTED Bluetooth seam: the resampler keeps no state across a change until rs_open (2.6)', flush=True)


s.bluetooth = bluetooth

if __name__ == '__main__':
    s.main()
