#!/usr/bin/env python3
"""V2.1's hciplayer faults that tools/peq.py fixes on the Q2 (MEDIA_INFO_NULL), in the real player:
test/hci_emu.py runs it, its threads, demuxers and decoders on Unicorn with ALSA modelled and a virtual clock, driven
over its socket as demo drives it. test/hci_natural.py's music_info_no_stream, at V2.1's addresses
(m1plus.PLAYER_PROFILE's media_info_null).

A get-music-info with no sh_audio gets the no-stream reply, and playback carries on; stock reads through NULL and the
player dies. The FLAC is written here (verbatim subframes), so the suite needs no encoder.
Usage: test/m1plus/player_faults.py BUILD_DIR [PLAYER]  (PLAYER: another V2.1 hciplayer, e.g. BUILD_DIR/peq/stock-hciplayer,
to see stock fail)"""
import pathlib, random, shutil, struct, subprocess, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]/'tools'))
from unicorn.mips_const import UC_MIPS_REG_V1
from hci_emu import Emu
from build import sha
from m1plus import M1PLUS_PLAYER_SHA, PLAYER_PROFILE

build = pathlib.Path(sys.argv[1]).resolve()
player = pathlib.Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else build/'peq'/'hciplayer'
work, root, aud = build/'player_faults', build/'player_faults'/'root', build/'player_faults'/'aud'
AUTH = 0x43050c        # the licence check, called from 0x420ee8 as V1.32's 0x43084c
LENGTH = 0xb10e68      # the length get-music-info reads (V1.32's 0xb10e84); 0 takes the length call's path
RATE, FRAMES = 44100, 54   # 54 blocks of 4096: 5 s
failures = []


def check(ok, what):
    print(('ok   ' if ok else 'FAIL ') + what, flush=True)
    failures.extend([] if ok else [what])


def crc8(data):
    c = 0
    for b in data:
        c ^= b
        for _ in range(8): c = (c << 1 ^ 0x07) & 0xff if c & 0x80 else c << 1 & 0xff
    return c


def crc16(data):
    c = 0
    for b in data:
        c ^= b << 8
        for _ in range(8): c = (c << 1 ^ 0x8005) & 0xffff if c & 0x8000 else c << 1 & 0xffff
    return c


def flac(seed):
    """A 16-bit stereo FLAC at 44.1 kHz of quiet noise, every frame 4096 samples, verbatim subframes."""
    r = random.Random(seed)
    info = struct.pack('>HH', 4096, 4096) + bytes(6)  # block sizes; frame sizes unknown
    info += ((RATE << 44) | (1 << 41) | (15 << 36) | FRAMES * 4096).to_bytes(8, 'big') + bytes(16)
    out = bytearray(b'fLaC' + bytes([0x80]) + len(info).to_bytes(3, 'big') + info)
    for n in range(FRAMES):
        num = bytes([n]) if n < 0x80 else bytes([0xc0 | n >> 6, 0x80 | n & 0x3f])
        head = b'\xff\xf8\xc9\x18' + num  # 4096 samples, 44.1 kHz; two independent channels, 16 bits
        frame = bytearray(head + bytes([crc8(head)]))
        for _ in range(2):
            frame += b'\x02' + struct.pack('>4096h', *(r.randint(-300, 300) for _ in range(4096)))
        out += frame + crc16(frame).to_bytes(2, 'big')
    return bytes(out)


def setup():
    shutil.rmtree(work, ignore_errors=True)
    aud.mkdir(parents=True)
    subprocess.run(['unsquashfs', '-no-progress', '-d', root, '-f', build/'stock.squashfs', 'lib', 'usr/lib'], check=True,
                   stdout=subprocess.DEVNULL)
    (aud/'a.flac').write_bytes(flac(1))


class Player:
    def __init__(self):
        self.e = e = Emu(player, root, work, log=work/'player.log', fsmap={'/mnt/mmc': str(aud)})
        e.hook_fn(AUTH, lambda e: 0)
        self.pcm = bytearray()
        e.on_write = lambda e, data, n, p: self.pcm.extend(data)
        e.alsa_active = True
        self.run(0.3)
    def run(self, s):
        self.e.run(until=self.now() + s)
    def now(self):
        return (self.e.clock - 10**12) / 1e9
    def frames(self):
        return len(self.pcm) // 4
    def song(self, name):
        self.e.send_cmd('{set-songurl\\/mnt/mmc/%s|ss=0|0|0|1|0|90}' % name)


def music_info_no_stream():
    """get-music-info, on the command thread, while the main thread has no sh_audio: the no-stream reply, not a fault. The
    loads are forced to NULL on that thread alone, since the race itself can't be timed here."""
    sites = [a for a, _, _ in PLAYER_PROFILE['media_info_null']]
    for name, load, length in ('sh_audio', sites[0], 1), ('mpctx after the length call', sites[1], 0):
        try:
            p = Player()
            p.song('a.flac')
            p.run(1)
            check(p.frames() > 0, f'music info, no {name}: a.flac plays ({p.frames()} frames)')
            if not length: p.e.w32(LENGTH, 0)
            p.e.watch_fn(load, lambda e: e.u.reg_write(UC_MIPS_REG_V1, 0) if e.cur.tid != 1 else None)
            p.e.replies.clear()
            p.e.send_cmd('{media-info\\get-music-info}')
            before = p.frames()
            p.run(0.5)
            said = b''.join(p.e.replies)
            check(b'no-playing-status' in said, f'music info, no {name}: {said[-50:]}')
            check(p.frames() > before, f'music info, no {name}: playback carries on')
        except RuntimeError as x:
            check(False, f'music info, no {name}: the player faulted: {x}')


if __name__ == '__main__':
    stock = sha((build/'peq'/'stock-hciplayer').read_bytes())
    assert stock == M1PLUS_PLAYER_SHA, f'not an M1 Plus build: {stock}'
    print(f'player: {player}')
    setup()
    music_info_no_stream()
    assert not failures, f'{len(failures)} failed: {failures}'
    shutil.rmtree(work)
    print('player_faults: all passed')
