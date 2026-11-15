#!/usr/bin/env python3
"""test/bt_resample.py's resampler half on V2.1's hciplayer, at V2.1's lavcresample descriptor (m1plus.PLAYER_PROFILE's
rs_open_slot): the built player's lavcresample and libswresample under Unicorn, as on the Q2.

A tone split across two files comes out of two instances exactly as one instance plays it whole at AAC/SBC's 48 kHz and
LDAC's 96 kHz; V2.1's stock open (the slot's word before the patch) loses the first file's tail and starts the second
from a fresh resampler, as do a skip, a pause and another input rate. Its output half (ao_init, dac_*, ao_uninit,
ao_write) runs at V1.32's addresses there; test/m1plus/ao.py runs those cases on V2.1.
Usage: test/m1plus/bt_resample.py BUILD_DIR"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]/'tools'))
from build import sha
from m1plus import M1PLUS_PLAYER_SHA, PLAYER_PROFILE as P
import bt_resample as b

if __name__ == '__main__':
    stock = sha((b.out/'stock-hciplayer').read_bytes())
    assert stock == M1PLUS_PLAYER_SHA, f'not an M1 Plus build: {stock}'
    slot, stock_open, _ = P['rs_open_slot']
    b.resampler(slot, stock_open)
    print('bt_resample: all as expected')
