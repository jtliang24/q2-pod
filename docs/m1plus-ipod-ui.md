# M1 Plus: the iPod UI port

This plan replaces the Oct 26 "unplanned" decision in [m1plus-roadmap.md](m1plus-roadmap.md) section 5.
What is done, and why, goes in [m1plus-progress.md](m1plus-progress.md) as each phase lands.

## Why

The M1 port compiles upstream's shared C with `-DIPOD=0 -DM1PLUS=1` (`tools/m1plus.py`, the payload and
common flags). That is the Legacy, stock-UI path. Upstream 1.5.9 (`4fee7d5`, "build: iPod only, Legacy
deleted") removed that path with `unifdef -DIPOD=1`. Past 1.5.8, the M1 would have to keep the Legacy code
alive on its own.

The M1 also mixes two looks today:
- V2.1's Home grid and native pages;
- payload pages that imitate V2.1 (`page_list`, `m1plus_nav_rows.c`, `m1plus_coverflow_rows.c`);
- Q2 Pod rows added to V2.1's own lists.

Moving between them is clunky.

## Decisions (Nov 2)

- **Port the iPod UI to the M1 and make it the M1's only UI**, as on the Q2. Stock pages appear only where
  the iPod UI itself opens them.
- **Port first, on the 1.5.8 base** (`staging`, `UPSTREAM_BASE=1.5.8`), then resume syncing.
- **Look:** upstream's iPod structure reflowed for the 320x480 portrait screen, with square corners
  (`GLASS_R` 0). The knob takes the wheel's turns, and touch takes the wheel's gestures.
- **Method:** upstream's own. Audit V2.1's UI `.bin` pages, styles and row-layout code, and rewrite them
  with `tools/ipod.py`'s codec and rules, parameterised by device. The shared `#if IPOD` C then runs on the
  widget structure it expects.
- **Back:** every iPod page has a slim back chevron at the top left, beside the title. In Knob:
  Navigation, Previous presses it, as today. No gesture is a page's only way out.
- **Split Home:** the art panel goes across the top (about 320x200, still panning), with the menu rows
  below it.
- **Releases:** M1 releases continue from `staging` (1.5.8-m1.x) while the port lives on
  `feature/m1-ipod`.

## Phase 0: Set-up

1. Park the in-progress `sync/1.6.0` merge:
   - save its staged and working-tree state (`git diff --cached` and the unmerged files) to
     `work/sync/1.6.0-wip/`;
   - then run `git merge --abort`. `refs/backup/pre-sync-1.6.0` marks the start point.
2. Branch `feature/m1-ipod` from `staging`.
3. Update the docs, because the port reverses rules they state:
   - `m1plus-roadmap.md` section 5 points here.
   - The ground rule "Prefer V2.1's own UI conventions" becomes "the iPod UI's conventions".
   - "Every page has an explicit Back button" is restated for the chevron.
   - [m1plus-unported.md](m1plus-unported.md#the-ipod-ui)'s row changes to "in progress".
   - R1 is unchanged: Q2 Legacy and iPod `update.tar` stay byte-identical (`test/q2compare.py`).

## Phase 1: The M1 compiles the iPod path

Phase 0 is done: the `sync/1.6.0` WIP is in `work/sync/1.6.0-wip/`, `feature/m1-ipod` is cut from
`staging`, and the docs were updated in `6d93571`. Phase 1 is four commits, and each one passes the
Verification steps below.

1. **`build(m1plus): compile the shared C with IPOD=1`**
   - `tools/m1plus.py` `compile_common()` and `compile_payload()`: change `-DIPOD=0` to `-DIPOD=1`.
   - `compile_payload()` already gives each `HOOKS | IPOD_HOOKS` symbol that `M1PLUS_HOOKS` lacks a
     `jr $ra; move $v0, $zero` trampoline, so the payload links without any new hook entry. There is no
     `IPOD_LEAF` (`style_get_gradient`) jump, and no `--undefined` for it, until Phase 4.1.
   - Fix the `#if IPOD` compile errors (about 80 sites, mostly in `navigation.c` and `coverflow.c`) one
     at a time. Where the code names a Q2 iPod asset, name or offset that `patch/m1plus_offsets.inc` lacks,
     add an `#if M1PLUS` stub. Never invent a V2.1 value.
   - `M1PLUS_PORTS`: give each `IPOD_HOOKS` entry its own `unported` row naming its Phase 4 item, e.g.
     `'style_get_color': ('unported', 'iPod UI paint backbone (m1plus-ipod-ui.md 4.1)')`. Rewrite the
     comment that says "IPOD_HOOKS are Q2 only as a group".
   - `test/m1plus/ports.py`: drop the blanket `q2only` rule for `IPOD_HOOKS`, so they get the same row
     check as any Q2 hook. If a stub covers something other than a hook or call site, add a row kind for
     it rather than leave it untracked.
2. **`feat(m1plus): build the iPod variant only`**
   - `tools/m1plus.py` `build()`:
     - drop `check(not ipod, 'M1 Plus has no iPod build yet')`;
     - set `variant = 'ipod'` with or without `--ipod`;
     - add the M1's own tag, `TAG + 'M'`, so dev builds are `dev_tag(n, 'M')` (`V001m`);
     - release tags are still `release_m1.m1_tag`'s (`V1581`).
   - `test/m1plus/build.py`:
     - `m1plus_checks()` asserts `variant == 'ipod'` in place of "Only the Stock UI exists";
     - the "no iPod build" refusal test becomes a check that `ipod=True` and `ipod=False` produce the
       same M1 build;
     - the dev-tag checks cover `'m'` and keep the M1 tag apart from `VERSIONS`.
   - `test/m1plus/patch.py`: when `is_m1plus`, the version check expects the M1 tag.
3. **`test(m1plus): mark the iPod checks the M1 doesn't pass yet as known gaps`** (the user's choice,
   Nov 2)
   - Run `test/m1plus/patch.py` on the Phase 1 build and sort its failing `variant=='ipod'` branches (about
     40):
     - one that needs an unported asset or hook is wrapped in `known_gap('<feature> (4.N)', ...)`;
     - one that tests only `IPOD=1` C behaviour (row fast-scroll counts, key handling) must pass as it
       is. If it fails, that is a bug to fix, not a gap to mark.
   - `known_gap` fails once its check passes, so each Phase 4 item removes its own markers.
4. **`docs(m1plus): record Phase 1`**
   - Add a progress section: what changed, the gap list and the device check.
   - Roadmap section 5: drop "Until the plan's Phase 1 lands, `--ipod` is refused".
   - The unported list's iPod UI row lists the hooks as unported, by phase.

**Gate:** the M1 builds, the Verification steps pass (`patch.py` lists its known gaps and has no
failures), and a `--dev` build flashed through the menu updater boots to a working, still stock-looking
UI, checked over q2remote with screenshots. This is the branch's floor, and each later phase raises it.

## Phase 2: Device geometry as names

- **Shared C.** Replace the iPod path's screen literals (375, 320, 290, 30 and the values derived from
  them) with names.
  - Counts at 1.6.3: `coverflow.c` (15 each of 375 and 290), `peq_ui.c` 12, `navigation.c` 8, then
    `addon.c`, `games.c`, `photos.c`, `spotify.c`, `books.c`, `video.c` and `visualizer.c`.
  - Use the names that already exist where they fit: `UI_W` (375 in `m1plus_q2.inc`, 320 in
    `m1plus_offsets.inc`), `BOTTOM`, `HOME_*`, `NP_*`, `SET_*`, `CF_*`, `GLASS_R`. Add `UI_H` and
    `BAR_H`.
  - Each replacement is a seam that changes no Q2 bytes (`q2compare.py` checks this). Offer the set
    upstream with the other seams (roadmap section 6, "The seams") so these lines stop conflicting.
- **`tools/ipod.py`.** Its constants come from a device profile: `BOTTOM`, `PITCH`, `BODY`, `ART`,
  `CORNER_R`, the 320 in `corner_inset`, `STATUS_*`, `HOME_*`, `NP_*`, `QS_*`.
  - `inc()` already reads `offsets.inc`. On the M1 it reads `m1plus_offsets.inc`.
  - The Q2 profile must reproduce today's values exactly.
  - Keep the change M1-side where possible: `tools/m1plus_ipod.py` wraps or overrides, so
    `tools/ipod.py` stays upstream's text.

## Phase 3: The V2.1 audit

Create `patch/m1plus_ipod.json`, the M1's counterpart to `patch/ipod.json`, with the same keys:
- **`assets`, `navbar_only`, `slide_only`:** V2.1's page names and SHA-256 hashes, mapped from V1.32's
  17 + 36 + 1 pages using `m1plus_names()`'s decode/walk.
- **Code edits:** `immediates`, `row_layout_calls`, `private_prologues`, `event_abi_words`. Find each
  V2.1 site by hand under the ground rule (read the same-role V2.1 function, never reuse a V1.32 address),
  and pin each one in `test/m1plus/build.py` `m1plus_checks()`.
- **`settings_icons`, `quiet_icons`, `status_icons`, `styles`:** the V2.1 file names and hashes.

Then `tools/m1plus_ipod.py`: `patch_asset` and `patch_code` for V2.1.
- Reuse `ipod.py`'s `decode`, `encode`, `walk`, `patch_word`, `sized_art`, `settings_icon` and its
  `rows()` logic.
- Only the stock-geometry `check()`s and the addresses change.
- Wire it into `m1plus.build()`, which today validates V2.1's assets but patches none.

## Phase 4: Features, in dependency order

Each feature follows the same steps:
- V2.1 hook addresses go in `M1PLUS_HOOKS`, and the `M1PLUS_PORTS` row changes to `ported`;
- the asset rewrite;
- M1 input mapping;
- the M1 code it replaces is retired;
- tests (Phase 5);
- a device check on a `--dev` build.

1. **Paint backbone and themes:** `style_get_color`, `image_manager_add`, `widget_on_paint_background`,
   the `style_get_gradient` leaf, `ui_loader_load_widget_with_parent`, the `default.bin` style edits,
   Light Mode, accents and Themes. Corners stay square.
2. **Status bar:** `systembar_showface`, `system_bar.bin` with the iPod title and the back chevron (the
   new M1 piece, beside the title), and the status icons.
3. **Settings pages:**
   - the `navbar_only` rewrite, `ipod_list_layout` through V2.1's `list_view` layout vtable slot, the
     settings icons, and the Display/Appearance/Controls pages;
   - retire `m1plus_nav_rows.c`, `m1plus_nav_display.c`, `m1plus_nav_sysset.c`,
     `m1plus_nav_audioset.c` and the M1 branches of `pod_rows`.
4. **Library:**
   - compact rows: the local pages, `compact_set_row_layout` at V2.1's row-layout calls, and the
     immediates;
   - hold-return to Now Playing, mapped to the touch long-press (`m1plus_nav_touch.c`) and a knob hold;
   - retire `m1plus_coverflow_rows.c` and `page_list`'s V2.1-look overrides in `coverflow.c`.
5. **Home:**
   - the `home_page.bin` rewrite with Split (art on top, menu below) and Classic; Carousel comes with 1.5.9;
   - the Coverflow card;
   - retire `m1plus_coverflow_home.c` and `m1plus_nav_home.c`.
6. **Now Playing:** the iPod layout, Centred Now Playing, `bigcover`, the volume dialog and the quiet
   icons; scrub on the knob (`np_key`/`center_press`, with the knob press as Centre).
7. **Quick Settings and dialogs:** `statusbar_dialog.bin`, the confirm and add-to-playlist dialogs. The
   wheel QS swipe becomes a touch swipe down from the status bar; `qs_*`'s fake-finger path stays Q2-only.
8. **Left Q2-only, as `NOT PORTED` rows:**
   - Games (they need a design without the Return key and the wheel);
   - the click sound (`buzzeer_switch`), unless the M1 has a buzzer;
   - `chord_gate`'s rim presses;
   - `WHEEL_TS_READ`.

## Phase 5: Tests

- **`test/m1plus/patch.py`:** bring in upstream's iPod scenarios (status bar, row layouts, Hold Return,
  Quick Settings, Home, Now Playing, scrub, Light Mode, Display rows) through `test/m1plus/suitemerge.py`,
  run against V2.1 addresses. M1-only cases cover the chevron, the knob scrub and the portrait Split.
- **`test/unit/test_ipod.py`:** parameterise by device profile, and add V2.1 synthetic trees for
  `tools/m1plus_ipod.py`. This is the CI suite.
- **`test/m1plus/build.py --build`:** pins every `m1plus_ipod.json` site and hash, and checks
  `changed_assets`.
- **`test/m1plus/boot.py`:** walks each iPod page under qemu at 320x480 and closes it with `BACK` (the
  chevron).
- **`test/ui_preview.py`:** an M1 profile for the review sheets before each device check.

## Phase 6: Back to syncing

Once the branch reaches parity (Phases 1 to 4.7 pass on the device):
- land it on `staging` and release `1.5.8-m1.N`;
- restart the sync through the upstream-sync runbook ([m1plus-sync.md](m1plus-sync.md)). `4fee7d5` now
  only removes code the M1 no longer compiles, and the saved `work/sync/1.6.0-wip/` resolutions are
  reference only.
- Carousel and the other 1.5.9/1.6.x iPod features then arrive as ordinary port rows.

## Files

- **Edited:** `tools/m1plus.py`, `patch/m1plus_offsets.inc`, `patch/m1plus_q2.inc`, `patch/navigation.c`
  and `patch/coverflow.c` (seams only), `test/m1plus/{build,patch,boot,ports}.py`, `docs/m1plus-*.md`.
- **New:** `tools/m1plus_ipod.py`, `patch/m1plus_ipod.json`.
- **Reused as is:** `tools/ipod.py` (codec and rewrites), `compile_payload()`'s trampoline fallback,
  `m1plus_names()`, `test/m1plus/suitemerge.py`, and q2remote for device screenshots.
- **Retired over Phase 4:** `m1plus_nav_rows.c`, `m1plus_coverflow_rows.c`, `m1plus_nav_display.c`,
  `m1plus_nav_sysset.c`, `m1plus_nav_audioset.c`, `m1plus_coverflow_home.c`, `m1plus_nav_home.c`,
  `m1plus_coverflow_back.c` (replaced by the chevron).

## Verification

After every commit:
1. **Q2 unchanged:** `TMPDIR=/tmp python3 test/q2compare.py 1.5.8 --suites`. Legacy and iPod
   `update.tar` must be byte-identical.
2. **M1 gates:** a fresh `--dev` build, then `test/m1plus/build.py --build`, `patch.py`, `boot.py` (plain,
   `--home-menu` and `--media`), `playback.py`, `m4b`, `id3`, `headset_io`, `test/ldac.py`,
   `test/bluealsa.py`, then `ports.py`. Each ported row moves from `unported` to `ported`, and a
   `known_gap` that now passes is removed.
3. **CI suite:** `pytest test/unit`.
4. **Device:** at the end of each Phase 4 item, flash through the menu updater, then walk the feature over
   q2remote with screenshots. Record it as a progress section, with `test/m1plus/fndiff.py` against the
   build on the device.

Rough sizes (as in the roadmap: **S** a day, **M** a few days, **L** a week or more): Phases 0 to 2 **M**,
Phase 3 **L**, Phase 4 about **L** for every two items.
