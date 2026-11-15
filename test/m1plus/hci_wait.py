#!/usr/bin/env python3
"""test/hci_wait.py's futex waits on V2.1's hciplayer (patch/peq_player.c's hci_*, m1plus.PLAYER_PROFILE's pause_wait,
cmd_done and idle_wait), then the whole player's wakeups in test/hci_emu.py.

The hooks, as on the Q2: the command handler's wrapper wakes the stopped loop when a command set the play flag
(set-songurl) and the paused loop when one changed its state (mcl-play's resume), and wakes nothing for a status query;
the stopped loop waits on the flag while 0, the paused loop on cmd_gen only while no command moved it. A Pause undone
before the PCM paused releases demo's mute once, through V2.1's DAC helper, on the jack with its DAC open only.

The whole player: stock V2.1's stopped loop sleeps 10 ms a pass and its paused loop 20 ms (the M1 before this, 50 ms)
after its own 20 ms select, so the main thread blocks 100 and 50 times a second (25 paused passes; the M1's, 14). With
the waits each loop passes once a second, the player blocks 3 and 4 times a second (the rest is stock's floor: the
command thread's 1 s select and its 10 ms sleep after, the paused loop's select), and set-songurl, mcl-play,
set-nexturl and mcl-stop still act as soon as the handler has run. demo's half (its paced scheduling,
MAINSCHEDULING_CALL) stays V2.1's by decision.
Usage: test/m1plus/hci_wait.py BUILD_DIR [PLAYER]  (PLAYER: another V2.1 hciplayer, e.g. BUILD_DIR/peq/stock-hciplayer,
to see stock fail)"""
import collections, pathlib, shutil, struct, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]/'tools'))
from build import fileoff, jal, machine, read, sha, symbols, word
from m1plus import M1PLUS_PLAYER_SHA, PLAYER_PROFILE as P
from unicorn import UC_HOOK_CODE, UC_HOOK_INTR
from unicorn.mips_const import *
import hci_emu
import player_faults as pf

build, player = pf.build, pf.player
work = build/'hci_wait'
FLAG, HANDLER, NEXT, STOP = P['play_flag'], P['cmd_handler'], P['next_flag'], P['stop_flag']
STACK, DONE, MPCTX = 0x2008000, 0x2000000, 0x2001000
IOCTL = P['plt']['ioctl']  # V2.1's ioctl PLT stub, which its DAC helper calls
WAY, MUTED, DAC_FD = P['output_way'], P['dac_muted'], P['dac_fd']  # V1.32's 0xb10e54, 0xb11584, 0xb1158c
DAC_RELEASE_MS = 130  # peq_player.c's: a resume on the jack waits this long for the DAC's mute line
IDLE_DONE = P['idle_wait'][0] + 0x14  # past the stopped loop: the flag was seen set (0x42d84c)
failures = []


def check(ok, what):
    print(('ok   ' if ok else 'FAIL ') + what, flush=True)
    failures.extend([] if ok else [what])


def hooks():
    """The three sites, then the hooks in the payload under Unicorn with a stand-in command handler (test/hci_wait.py's)."""
    raw = player.read_bytes()
    ps = symbols(build/'peq'/'peq.elf')
    sites = [(P[k][0], jal(ps[P[k][2]])) for k in ('pause_wait', 'cmd_done', 'idle_wait')]
    got = [struct.unpack_from('<I', raw, fileoff(raw, a))[0] for a, _ in sites]
    check(got == [w for _, w in sites], f'the three waits are jal hci_*: {[hex(w) for w in got]}')
    check(struct.unpack_from('<I', raw, fileoff(raw, 0x42ff2c))[0] == 0x24044e20, "the pause wait's slot is stock's 20000")
    if got != [w for _, w in sites]: return  # stock: nothing of the payload's to call
    gen = ps['cmd_gen']
    check({'ao_init', 'ao_uninit', 'dac_resume'} <= set(ps), 'the output side is linked: ao_init, ao_uninit, dac_resume')

    def machine_with(handler=lambda u: None):
        u = machine(raw, DONE)
        word(u, P['mpctx'], MPCTX), word(u, MPCTX + 4, 2)  # paused
        seen = []
        def syscall(u, intno, unused):
            seen.append(tuple(u.reg_read(r) for r in (UC_MIPS_REG_V0, UC_MIPS_REG_A0, UC_MIPS_REG_A1, UC_MIPS_REG_A2)))
            u.reg_write(UC_MIPS_REG_V0, 0), u.reg_write(UC_MIPS_REG_7, 0)
        def stand_in(u, address, size, unused):
            handler(u)
            u.reg_write(UC_MIPS_REG_PC, u.reg_read(UC_MIPS_REG_RA))
        u.hook_add(UC_HOOK_INTR, syscall)
        u.hook_add(UC_HOOK_CODE, stand_in, begin=HANDLER, end=HANDLER)
        return u, seen
    def call(u, fn, a0=0):
        u.reg_write(UC_MIPS_REG_29, STACK), u.reg_write(UC_MIPS_REG_31, DONE), u.reg_write(UC_MIPS_REG_4, a0)
        u.emu_start(ps[fn], DONE, count=10000)

    u, seen = machine_with()
    call(u, 'hci_command', 0x2002000)
    check(seen == [] and read(u, gen) == 0, f'a status query wakes nothing: {seen}')
    u, seen = machine_with(lambda u: word(u, FLAG, 1))
    call(u, 'hci_command')
    check(seen == [(4238, gen, 129, 1), (4238, FLAG, 129, 1)] and read(u, gen) == 1, f'set-songurl wakes both loops: {seen}')
    u, seen = machine_with(lambda u: word(u, MPCTX + 4, 1))
    call(u, 'hci_command')
    check(seen == [(4238, gen, 129, 1)], f'mcl-play wakes the paused loop: {seen}')
    for address in (NEXT, STOP):
        u, seen = machine_with(lambda u: word(u, address, 1))
        call(u, 'hci_command')
        check(seen == [(4238, gen, 129, 1)], f'0x{address:x} set while paused wakes the paused loop: {seen}')
    got = []
    u, seen = machine_with(lambda u: got.append(u.reg_read(UC_MIPS_REG_4)))
    call(u, 'hci_command', 0x2002000)
    check(got == [0x2002000], f'the command buffer reaches 0x{HANDLER:x}: {got}')
    u, seen = machine_with()
    call(u, 'hci_idle_wait', 10000)
    check(len(seen) == 1 and seen[0] == (4238, FLAG, 128, 0), f'the stopped loop waits on 0x{FLAG:x} while 0: {seen}')
    u, seen = machine_with()
    word(u, gen, 5); call(u, 'hci_pause_wait')
    call(u, 'hci_pause_wait')
    word(u, gen, 6); call(u, 'hci_pause_wait')
    check(seen == [(4238, gen, 128, 5)], f'the paused loop waits only while cmd_gen is as last seen: {seen}')
    # A Pause undone with no PCM pause (test/hci_wait.py's): no resume will come, so demo's mute(2) is released here,
    # once, through V2.1's helper (0x43ae74) and its ioctl. After a real pause, or Pause alone, resume's to do.
    def tap(state, muted=0, way=0, fd=5, then=2):
        u, seen = machine_with(lambda u: word(u, MPCTX + 4, then))
        word(u, MPCTX + 4, state), word(u, MUTED, muted), word(u, WAY, way), word(u, DAC_FD, fd)
        released = []
        def ioctl(u, address, size, unused):
            released.append((u.reg_read(UC_MIPS_REG_4), u.reg_read(UC_MIPS_REG_5), read(u, u.reg_read(UC_MIPS_REG_6))))
            u.reg_write(UC_MIPS_REG_PC, u.reg_read(UC_MIPS_REG_RA))
        u.hook_add(UC_HOOK_CODE, ioctl, begin=IOCTL, end=IOCTL)
        call(u, 'hci_command')
        return released, read(u, MUTED)
    for kw, want, what in ((dict(state=2, then=1), ([(5, 0xc0044d1f, 0)], 0), 'a Pause undone: the mute released once'),
                           (dict(state=2, muted=1, then=1), ([], 1), 'a real pause: resume releases it'),
                           (dict(state=1, then=2), ([], 0), 'Pause alone: nothing'),
                           (dict(state=2, then=2), ([], 0), 'a status query while paused: nothing'),
                           (dict(state=2, way=1, then=1), ([], 0), "Bluetooth: demo's mute isn't this DAC's to hold"),
                           (dict(state=2, fd=0, then=1), ([], 0), 'no DAC open: nothing')):
        got = tap(**kw)
        check(got == want, f'{what}: {got}')


class Counted(hci_emu.Emu):
    """hci_emu's player, with every blocking call each thread makes recorded: (virtual ns, tid, why)."""
    def __init__(self, *a, **k):
        self.blocks = []
        super().__init__(*a, **k)
    def block_current(self, wake_at, ret, why, retry=False, resume=None):
        self.blocks.append((self.clock, self.cur.tid, why))
        return super().block_current(wake_at, ret, why, retry, resume)
    def sys_futex(self, addr, op, val, timeout):
        r = super().sys_futex(addr, op, val, timeout)
        if r is None and op & 0x7f in (0, 9): self.blocks.append((self.clock, self.cur.tid, 'futex'))
        return r


def watch(p, address, main=True):
    """Virtual times the main thread (tid 1), or another, reaches address. Code already translated keeps no new hook:
    flush it."""
    at = []
    p.e.watch_fn(address, lambda e: at.append(p.now()) if (e.cur.tid == 1) == main else None)
    p.e.u.ctl_flush_tb()
    return at


def rates(p, seconds, passes):
    """Over the next `seconds`: each thread's blocking calls a second, and the main thread's passes a second through
    its loop's wait (the times in passes)."""
    n, start = len(p.e.blocks), p.now()
    p.run(seconds)
    per = collections.Counter(tid for _, tid, _ in p.e.blocks[n:])
    return {tid: per[tid] / seconds for tid in sorted(per)}, len([t for t in passes if t >= start]) / seconds


def until(p, ok, seconds, step=0.001):
    """Virtual seconds until ok(), at most `seconds` (None past it)."""
    start = p.now()
    while not ok():
        if p.now() - start > seconds: return None
        p.run(step)
    return p.now() - start


def command(p, text, handled, back, done, what, release=0):
    """Send text; once the command thread calls the handler (handled: the times it does; the emulator's read may come a
    loop, 10 ms, after the select), the main thread's wait returns at once (back), and done() follows within 50 ms of
    the command, plus release: the jack's DAC_RELEASE_MS, which a resume (dac_resume) waits before audio flows."""
    sent, n, m = p.now(), len(handled), len(back)
    p.e.send_cmd(text)
    took = until(p, done, 1)
    took = None if took is None else p.now() - sent
    after = [t - handled[n] for t in back[m:] if len(handled) > n and t >= handled[n]]
    woke = after[0] if after else None
    print(f'  {what}: the wait returned {woke} s after the handler, done after {took} s', flush=True)
    check(woke is not None and woke <= 0.002, f'{what}: the main thread is up within 2 ms of the handler ({woke} s)')
    check(took is not None and release <= took <= release + 0.05, f'{what}: done within {release * 1000 + 50:g} ms, after {release * 1000:g} ({took} s)')


def whole_player():
    """Stopped and paused, the main thread's loop passes no more than once a second, and the player's blocking calls
    drop to its idle floor: the command thread's select (1 s) and 10 ms sleep after it, and paused, the loop head's
    own 20 ms select (mp_input_get_cmd) before each wait. Stock: 100 and 50 passes a second."""
    pf.Emu = Counted
    try:
        p = pf.Player()
    finally:
        pf.Emu = hci_emu.Emu
    idle_pass, pause_pass = watch(p, P['idle_wait'][0]), watch(p, P['pause_wait'][0])
    idle_back, pause_back = watch(p, IDLE_DONE), watch(p, P['pause_wait'][0] + 8)
    handled = watch(p, P['cmd_done'][0], main=False)
    p.run(1)
    blocks, passes = rates(p, 10, idle_pass)
    print(f'  stopped: {passes} loop passes a second; blocking calls a second by thread: {blocks}', flush=True)
    check(passes <= 1.1, f'stopped: the idle loop passes {passes} times a second')
    check(sum(blocks.values()) <= 3.1, f'stopped: the player blocks {sum(blocks.values())} times a second ({blocks})')
    command(p, '{set-songurl\\/mnt/mmc/a.flac|ss=0|0|0|1|0|90}', handled, idle_back, lambda: p.frames() > 0, 'stopped, set-songurl')
    p.run(1)
    pcm = p.e.pcm
    p.e.send_cmd('{mcl-pause\\null}')
    check(until(p, lambda: pcm.state == 6, 1) is not None, f'mcl-pause: the PCM pauses ({pcm.state})')
    p.run(0.5)
    blocks, passes = rates(p, 10, pause_pass)
    print(f'  paused: {passes} loop passes a second; blocking calls a second by thread: {blocks}', flush=True)
    check(passes <= 1.1, f'paused: the pause loop passes {passes} times a second')
    check(sum(blocks.values()) <= 4.1, f'paused: the player blocks {sum(blocks.values())} times a second ({blocks})')
    command(p, '{mcl-play\\null}', handled, pause_back, lambda: pcm.state == 3, 'paused, mcl-play', DAC_RELEASE_MS / 1000)
    p.run(0.5)
    p.e.send_cmd('{mcl-pause\\null}')
    until(p, lambda: pcm.state == 6, 1)
    p.run(0.5)
    n = len(p.e.events)
    opened = lambda: any(name == 'open' and kw.get('path', '').endswith('a.flac') for _, name, kw in p.e.events[n:])
    command(p, '{set-nexturl\\/mnt/mmc/a.flac|ss=0|0|0|0|0|90}', handled, pause_back, opened, 'paused, set-nexturl')
    until(p, lambda: p.e.pcm is not None and p.e.pcm.state == 3, 1)
    p.run(0.5)
    p.e.send_cmd('{mcl-pause\\null}')
    until(p, lambda: p.e.pcm.state == 6, 1)
    p.run(0.5)
    n = len(idle_pass)
    command(p, '{mcl-stop\\null}', handled, pause_back, lambda: len(idle_pass) > n, 'paused, mcl-stop')
    check(p.e.exited is None, f'the player is still up ({p.e.exited})')


if __name__ == '__main__':
    stock = sha((build/'peq'/'stock-hciplayer').read_bytes())
    assert stock == M1PLUS_PLAYER_SHA, f'not an M1 Plus build: {stock}'
    print(f'player: {player}', flush=True)
    hooks()
    pf.work, pf.root, pf.aud = work, work/'root', work/'aud'
    pf.setup()
    whole_player()
    assert not failures, f'{len(failures)} failed: {failures}'
    shutil.rmtree(work)
    print('hci_wait: all passed')
