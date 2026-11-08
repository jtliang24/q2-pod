# Phase 4.5 status — November 7, 2026

Phase 4.5, the portrait iPod Home, is implemented, passes every emulator and Q2 gate, and passed its device pass
on `V04Hm` (the findings below are to be planned). The plan is [.plan/phase4-5.md](../.plan/phase4-5.md) and the record is
[m1plus-progress.md §69](m1plus-progress.md#69-phase-45-the-portrait-ipod-home-nov-7). Branch: `feature/m1-ipod`.

## What is in place

- Library and Streaming entry pages (`patch/m1plus_nav_library.c`), bound to V2.1's Home dispatcher
  (`m1_home_click`, `0x533b80`) by the ids in its own table.
- The Home asset rewrite (`tools/m1plus_ipod.py` `home_page`), and V2.1's Home initializer and refresh,
  whose returns with the grid gone are pinned in the build audit.
- Split, Full and Carousel in both themes (`patch/coverflow.c`, M1 seams). Settings opens from every layout, and
  the chevron or Previous goes back to the row or card it left. Shortcut works, and the art is at the M1's panel.
- `home_click`, which works around V2.1's `image_base` press defect.
- The grid is retired (`m1plus_coverflow_home.c`, `m1plus_nav_home.c`).

## Tested build

`work/phase4/4.5/h6`, `V04Hm`. It is a dev build with q2remote, and its update SHA-256 is
`dae62c65aadd96a2d04018d2514b631c930477c6c7a22be5c5dc634f24aa4403`. The payload sources have not changed since it
was built. It passes:

- the build audit;
- the MIPS suite (1,840 scenarios; 691 expected failures in 10 later-phase groups);
- the plain, Home-menu and media walks;
- playback, M4B, ID3, headset I/O, LDAC and Bluetooth;
- the port report;
- the Q2 comparison against 1.5.9, with all 33 suites and a byte-identical `update.tar`.

Its function diff against dev 57 and its Home review sheets are under `work/phase4/4.5/` (`h6-fndiff.log`,
`h6-sheets/`).

## Device pass

Flashed by the user and driven over q2remote on Nov 7: every Home destination in all three layouts and both
themes, Settings and Back, both knob modes, artwork and a reboot. The device's configuration, boot target and
volume were restored. [§69](m1plus-progress.md#69-phase-45-the-portrait-ipod-home-nov-7) has the record.

## Fixes and the second pass (Nov 8)

The five findings are done except the Carousel's knob rate ([§70](m1plus-progress.md#70-phase-45-the-device-pass-fixes-and-a-second-pass-nov-8)):
the login Back (`698976fd`, `a8ab1ec7`), the Settings list's first selection (no fix; `34dae142` pins the Q2's
behaviour), the Shortcut card's art (`b6f9945d`, `8ef0a607`), the q2remote knob pace (`423e8bcd`) and the cosmetics
(the aesthetics queue in [m1plus-ipod-ui.md](m1plus-ipod-ui.md#aesthetics-queue)). `V04Om` (`work/phase4/4.5f/a7`)
passed every gate and a second device pass, and Knob Up: List Down and a cover-less track are now covered.

## Remaining

1. The Carousel drops knob detents that come within about 200-250 ms of the last one that moved it (a 5-detent turn at
   40 ms moves one card; at 250 ms and slower, five). The lists count every detent. A fix needs its own plan, and a
   fast turn on the real knob is still untried.
2. Not covered: car-mode boot resume (car mode was not switched on).
