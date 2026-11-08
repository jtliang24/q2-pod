# Phase 4.5 status — November 7, 2026

Phase 4.5, the portrait iPod Home, is implemented and passes every emulator and Q2 gate. The device pass is
pending. The plan is [.plan/phase4-5.md](../.plan/phase4-5.md) and the record is
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

## Remaining

1. Flash `V04Hm` through the menu updater; the user confirms the update.
2. Run the device pass over q2remote, with Screen Off set to Off and restored afterwards:
   - every Home destination;
   - all modes in both themes;
   - Settings and Back;
   - both knob modes;
   - artwork;
   - reboot.

   Record the pass in §69.
3. Leave the two cosmetic points from the review sheets to the aesthetics pass: the Split knob walk clips the
   top row, and Classic's Settings card is grey.
