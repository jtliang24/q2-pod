# Phase 4.5 status — paused November 7, 2026

Work is paused at the user's request. Phase 4.5 is **incomplete**. The implementation plan remains
[.plan/phase4-5.md](../.plan/phase4-5.md). Branch: `feature/m1-ipod`; starting HEAD: `7dfdecae`.
No device was flashed during this work.

## Working-tree implementation

The implementation is uncommitted, across eight files:

- `tools/ipod.py`: Home row height accepts a profile override; Q2 defaults to 39 px.
- `patch/m1plus_nav_library.c`: expand the payload Library with native categories, playlists,
  history, ratings, conditional media and maintenance. Preserve the M1 Videos opener.
  Add a dedicated Streaming page containing native Tidal, Spotify, optional Soloify and installed
  apps, Internet Radio, AirPlay and Configuration. Keep interim Coverflow and Streaming rows in
  Library so the existing Q2 Pod grid card still provides access.
- `patch/m1plus_nav_state.inc`, `patch/navigation.c`: track and clear the separate Streaming page.
- `patch/m1plus_nav_stream.c`: service visibility changes update the Streaming page underneath
  Configuration. Existing service indices, visibility keys and backend limitations remain.
- `tools/m1plus.py`, `patch/m1plus_ipod.json`: import and pin V2.1's native Home destination
  dispatcher, `m1_home_click` at `0x533b80`. Native category rows bind their native numeric names
  and themselves as callback context. The dispatcher supplies Albums' structured context and
  native Tidal startup. Native category images use scale-down drawing to fit the 40 px row slot.
- `test/m1plus/patch.py`: revise Library expectations and Streaming helpers for the new pages;
  assert native callback bindings, icon draw type, conditional entries, order and duplicate-open
  behavior. These changes have not yet passed a complete suite.

A working-tree patch and copies of session logs are saved under `work/phase4/4.5/pause/`.
This directory is a local artifact, not tracked source.

## Builds and validation

| Build | Location | Results |
| --- | --- | --- |
| V047m | `work/phase4/4.5/cached` | Initial entry-page build completed; superseded. |
| V048m | `work/phase4/4.5/library` | Build audit, default QEMU boot/navigation walk and playback suite passed. |
| V049m | `work/phase4/4.5/library2` | Latest build, including icon sizing fix; build audit passed. Full MIPS suite and `--home-menu` QEMU walk were interrupted when pausing. |

V049m update SHA-256: `87aba3e2b5a96654776a5cdad0140611592ffe0d80b08af0055098649673ed08`.
Its manifest source SHA-256 is `846157304cc285afc7d23dc6ebdbae7d77af928b2f44e05db1039088b23e588e`.

The Q2 comparison against upstream 1.5.9 passed before the final M1-only icon fix:
`update.tar` was byte-identical (`1e9c789e9bc6` prefix). Python profile imports and diff whitespace
checks passed. `graphify update .` was run after the latest code changes.

V048m captures are in `work/phase4/4.5/library-caps/`. The Library capture revealed oversized native
category icons; V049m applies `IMAGE_DRAW_SCALE_DOWN`. Visual verification of that correction is pending.
V049m's interrupted legacy-menu walk has partial captures in `work/phase4/4.5/library2-menu-caps/`.

The MIPS regression suite has **no passing completion result**. Its interrupted latest log contains
repeated Unicorn invalid-memory-read diagnostics at PC/RA `0x658f98`, T9 `0xdeadbeef`, as well as
known unported-feature messages. Diagnose these against the gap harness before drawing conclusions;
the interrupted run did not produce its final expected/unexpected-gap summary. An earlier run also
printed a missing `local_album.png` asset diagnostic. Neither diagnostic has been resolved or classified.

Session log copies include `phase45-audit2.log`, `phase45-patch-fast.log`, `phase45-boot.log`,
`phase45-playback.log`, `phase45-q2compare.log` and `phase45-menu2.log` in the pause directory.
Earlier MIPS attempts were interrupted or superseded; they are not passes.

## Resuming validation

`nix develop` initially failed in the sandbox because of the Nix cache and daemon socket. The existing
cached development environment worked without re-evaluation:

```sh
source .direnv/flake-profile-a5d5b61aa8a61b7d9d765e1daf971a9a578f1cfa.rc
python3 test/m1plus/build.py --build work/phase4/4.5/library2
PYTHONUNBUFFERED=1 python3 test/m1plus/patch.py work/phase4/4.5/library2
```

The latest suite attempt used `/tmp/q2-patch-fast.py`, copied into the pause directory. It caches
`ast._splitlines_no_ff` with `functools.lru_cache(maxsize=1)` to reduce repeated parsing work, then
runs the normal suite. This changes only the temporary runner, not repository tests or firmware;
use the ordinary command above as the canonical check. QEMU's bubblewrap harness needed sandbox
escalation. All running validation sessions started in this work were stopped when pausing.

## Remaining work

1. Complete and diagnose the MIPS suite for the entry-page changes; verify the scaled icons and
   every native category destination, native Tidal, service visibility and page close/reopen behavior.
2. Adapt the media QEMU walk: its old Q2 Pod row indices and direct service routes no longer match
   the expanded Library and dedicated Streaming page. The media walk has not been run on these changes.
3. Implement the portrait Home asset rewrite and explicit destination bindings, fixed seven entries,
   Split/Full/Carousel layouts, scrolling and shared input. The native grid and its editor remain.
4. Implement Home settings/submenu Back integration, status chevron, shortcut support and Games
   fallback. Home and Shortcut settings remain at their previous implementation level.
5. Adapt artwork geometry, buffers, clipping, animation gating, cache eviction and fallback behavior;
   port ordinary/car-mode boot resume. Retire grid-only files and assets after replacement is working.
6. Add the planned Home tests, mode/theme coverage, failure-injection checks and review sheets;
   update the port report and phase documentation from actual validated behavior.
7. Run all required Q2/M1 gates on the final source, compare functions with dev 57, and complete the
   menu-updater/device pass while preserving and restoring device configuration.

Do not mark Phase 4.5 complete or remove its known gaps on the strength of the partial entry-page work.
