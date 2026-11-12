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
- **Port first, on the 1.5.9 base**, then resume syncing. 1.5.9 is the first iPod-only tag. Phase 1 started
  on 1.5.8 (`staging`); `feature/m1-ipod` then takes 1.5.9 through one sync step (Phase 1.5), since the
  M1 compiles `IPOD=1` and `4fee7d5` deletes only code it no longer compiles. `staging` stays on 1.5.8,
  because it still compiles the Legacy path. (Revised Nov 3.)
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
   - The compile had 46 errors from 26 names, not about 80. Much of the `#if IPOD` code sits in routines
     the M1 already hooks (`ringnav`, `ringnav_playing`, the paint hooks, `lyric_poll`), so it is live
     at once. The policy (the user's choice, Nov 2) is the safe stand-in: every missing name gets a value
     that cannot fault, what needs no iPod asset goes live now, and what is wrong becomes a gap. Names go in
     `patch/m1plus_offsets.inc`; functions V2.1 lacks get a stand-in in `patch/m1plus_nav.h`
     (`M1PLUS_SHIMS`). Never invent a V2.1 value.
   - A one-off, uncommitted audit (`M1_UNPORTED_ADDR` as an undefined symbol, and the payload with
     `-ffunction-sections` so `--gc-sections` drops what no hook reaches) shows which unported addresses
     live code reads: none.
   - `M1PLUS_PORTS`: each `IPOD_HOOKS` entry has its own `unported` row naming its Phase 4 item.
     `test/m1plus/ports.py` has a `function` row kind for the stand-ins and unresolved routines.
   - Found while testing: with `IPOD=1` the selection bar is drawn behind the rows by
     `widget_on_paint_background`, which hides it behind V2.1's opaque rows. The M1 keeps Stock's outline
     (`IPOD_BAR`) until 4.1's row styles.
2. **`feat(m1plus): build the iPod variant only`**
   - `tools/m1plus.py` `build()`: `variant = 'ipod'` with or without `--ipod`; the M1's tag is
     `TAG + 'M'` (dev builds `V001m`); release tags are still `release_m1.m1_tag`'s (`V1581`).
   - `test/m1plus/build.py` and `patch.py` expect the variant and tag; `--ipod` builds the same payload.
   - Knob: Navigation is the default on the M1 (`pod_default`), since the iPod UI has no wheel.
3. **`test(m1plus): list the patch.py checks the iPod UI gaps fail`** (the user's choice, Nov 2, in place
   of hand-wrapping each in `known_gap`)
   - `patch.py` fails 127 top-level checks on the M1, from about 25 causes. On the M1 it runs each one on its own
     (`test/m1plus/gaprun.py`) against `test/m1plus/patch_gaps.py`, which lists each expected failure under the
     Phase 4 item that ports it. A listed check that passes, or an unlisted failure, fails the run; each
     Phase 4 item removes its own entries. A check of pure `IPOD=1` C behaviour must pass: if one fails, that
     is a bug.
   - The harness enters the unhooked `IPOD_HOOKS` routines directly.
4. **`docs(m1plus): record Phase 1`** ([progress](m1plus-progress.md) section 57).

**Gate:** the M1 builds, the Verification steps pass (`patch.py` lists its known gaps and has no
failures), and a `--dev` build flashed through the menu updater boots to a working, still stock-looking
UI, checked over q2remote with screenshots. This is the branch's floor, and each later phase raises it.

## Phase 1.5: Sync to 1.5.9

Merge upstream 1.5.9 into `feature/m1-ipod` through the runbook ([m1plus-sync.md](m1plus-sync.md),
steps 1 to 5), with `sync/1.5.9` cut from `feature/m1-ipod` instead of `staging`, landed `--no-ff` back
into `feature/m1-ipod`. `work/sync/1.6.0-wip/` is reference for the overlapping conflicts.
- M1 seams in `#if !IPOD` or `IPOD ? a : b` sites go with upstream's unifdef: keep the iPod side.
- `test/q2compare.py` builds one (iPod) variant where the base's `build.py` has no `--ipod`.
- `tools/m1plus.py` follows the `IPOD_HOOKS` fold into `HOOKS`, and drops the dead `-DIPOD=1`.
- New names and hooks (Carousel, Click With Headphones) get V2.1 values or `M1_UNPORTED`/`unported`
  rows. Carousel is a Phase 4.5 row.
- Gates, record (`UPSTREAM_BASE=1.5.9`) and a device pass. This is the floor for Phases 2 to 4.

Done on Nov 3 (progress 59): gated, the device pass on its `--dev` build V02Hm (`work/sync/1.5.9/`), and
landed in `feature/m1-ipod` (`fd53846`). `drift.py` then has 1.5.9 → 1.6.3 due (78 commits, 2,007 lines),
which waits for Phase 6.

## Phase 2: Device geometry as names

- **Shared C.** Replace the iPod path's screen literals (375, 320, 290, 30 and the values derived from
  them) with names.
  - Recount on the 1.5.9 tree. (The earlier counts were upstream 1.6.3's, and M1 seams already name most
    of `coverflow.c`, `peq_ui.c` and `photos.c`.) The sites left are mostly `navigation.c`, Split Home in
    `coverflow.c`, and the parts of `addon.c`'s QR page that the M1 compiles. `games.c` (Q2-only, 4.8)
    and `video.c` (already split) stay as they are.
  - Use the names that already exist where they fit: `UI_W` (375 in `m1plus_q2.inc`, 320 in
    `m1plus_offsets.inc`), `UI_H`, `BOTTOM`, `HOME_*`, `NP_*`, `SET_*`, `CF_*`, `GLASS_R`. Add
    `STATUS_H` (30) for the status bar; `BAR_H` is taken by `video.c`'s progress bar.
  - Only screen-derived values go in the M1 profile now. Layout values come with their Phase 4 item.
  - Each replacement is a seam that changes no Q2 bytes (`q2compare.py` checks this). Offer the set
    upstream with the other seams (roadmap section 6, "The seams") so these lines stop conflicting.
- **`tools/ipod.py`.** Its constants come from a device profile: `BOTTOM`, `CORNER_R`, the 320 in
  `corner_inset`, `BC_ART`, `STATUS_*`, `HOME_LIST_W`, `NP_*`, and the rewrites' screen-wide outputs.
  - Everything is computed at import, and `inc()` reads only the text of `offsets.inc`, which holds
    neither the Q2's `UI_W` (it is `m1plus_q2.inc`'s) nor the M1's layout names. So the seam is in
    `tools/ipod.py`: `O` gets `UI_W`, `UI_H` and `STATUS_H` at the Q2's values, overlaid by a
    `PROFILE` global when one is set, and `BOTTOM` is `UI_H - STATUS_H`. The Q2 import sets none and
    reproduces today's values exactly. The checks of V1.32's stock geometry keep their literals, and
    the Now Playing cross-checks against `SPOT_*`/`NP_ART_TOP` run only for the Q2 (4.3 lays out the
    M1's).
  - `tools/m1plus_ipod.py` loads a second copy with the M1's screen alone (`UI_W`, `UI_H`, `STATUS_H`,
    `GLASS_R`, from `m1plus_offsets.inc`), leaving `sys.modules['ipod']` the Q2's. Every layout name
    keeps the Q2's value until its Phase 4 item, and nothing builds with the copy until Phase 3.
- **It changes the M1.** The named sites the M1 compiles now take its values (320, 480, 450):
  `qr_open`, Split Home (`coverflow_home`, `_art`, `_clip`, `home_fit`, `home_tex`), `bc_fit` (in
  `ringnav_paint_bg`) and `ringnav_playlistsmore`. `fndiff.py` lists them, and the device pass checks them.

Done on Nov 3 (progress 60): `e8c1163`, `f946c64`, `7809395`.

## Phase 3: The V2.1 page inventory and the patch framework

An up-front audit of V2.1 for every key in `patch/ipod.json` turned out to be mostly Phase 4's design work:
34 of V1.32's 54 audited pages sit at the same path in V2.1 and the rest are renamed, moved or gone; none
of the 8 styles that `default.bin` edits exist in V2.1; 33 of 39 settings icons and all 8 quiet icons have
other names (`pset_*`, `sset_*`); and V2.1's rows are their own structure, so the V1.32 row immediates have
no direct counterparts. So Phase 3 is slim, and each Phase 4 item audits the sites, styles and icons it
rewrites.

Create `patch/m1plus_ipod.json`, the M1's counterpart to `patch/ipod.json`, with the same keys plus `pages`:
- **`pages`:** one row per V1.32 page in `ipod.json`'s `assets | navbar_only | slide_only` (54 rows):
  `{"v21": path | null, "opener": V2.1 function, "why": ...}`. The rows are decided by role, from the V2.1
  function that opens the page name, not by path. A `null` row names the Phase 4 item that decides it.
- **`assets`, `navbar_only`, `slide_only`:** the mapped V2.1 paths with their SHA-256, in the category of
  the V1.32 page.
- **Everything else** (`immediates`, `row_layout_calls`, `private_prologues`, `event_abi_words`,
  `settings_icons`, `quiet_icons`, `status_icons`, `styles`): empty. Phase 4 fills each one.

Then `tools/m1plus_ipod.py`: `patch_asset` and `patch_code` for V2.1.
- `patch_asset` checks the hash, the round trip and the root kind. It then applies the page's entry in
  `REWRITES` (empty until Phase 4), or returns the page unchanged.
- `patch_code` walks `immediates` and `row_layout_calls` with the copy's `patch_word`, and returns the
  changes (none yet).
- Wire both into `m1plus.build()`, which today validates V2.1's assets but patches none. `compact_code`
  in the manifest comes from `patch_code`.
- No M1 byte changes except the version string, so Phase 3 has no device pass: `fndiff.py` against the last
  device build and the manifest prove it.

Done on Nov 3 (progress 61): `36e1df6`, `9f2676d`.

## Phase 4: Features, in dependency order

Each feature follows the same steps:
- audit the item's V2.1 code sites, styles and icons into `m1plus_ipod.json` (read V2.1's own code, never
  reuse a V1.32 address), pin them in `m1plus_checks()`, and add its rewrite to `REWRITES`;
- V2.1 hook addresses go in `M1PLUS_HOOKS`, and the `M1PLUS_PORTS` row changes to `ported`;
- the asset rewrite;
- M1 input mapping;
- the M1 code it replaces is retired;
- tests (Phase 5);
- a device check on a `--dev` build.

1. **Paint backbone and themes:** `style_get_color`, `image_manager_add`, `widget_on_paint_background`,
   the `style_get_gradient` leaf, `ui_loader_load_widget_with_parent`, the `default.bin` style edits
   (the `styles` section), Light Mode, accents and Themes. Corners stay square.
   Code and gates done on Nov 3 (progress 62): the hooks, the leaf, seven style edits and the retired outline. The
   device pass (Nov 4) found two Light Mode faults. The hold menu's row is fixed by two more style edits (progress
   64); the press band didn't reproduce in qemu. Light Mode now leaves the lock window dark (progress 65).
2. **Status bar:** `systembar_showface`, `system_bar.bin` with the iPod title and the back chevron (the
   new M1 piece, beside the title), and the status icons (the `status_icons` section).
   Code and gates done on Nov 4 (progress 63): the clock centred, the chevron at the far left, `back_button`
   retired. V2.1's widgets the iPod doesn't draw stay inside the bar, transparent: an invalidate off the screen
   loses a frame's flush there. The lock screen's battery is ported (progress 64); the Q2-shaped bar scenarios
   stay a listed gap. The device pass (Nov 4, progress 64) passed. Since progress 73 the left group is the chevron
   alone, with Back's tap across the whole 64 px corner (down to the page's back row on Now Playing); the right group
   is Bluetooth, the play icon, Wi-Fi and the battery. The icon shows the action (❚❚ while playing) and its tap is the
   Play key. Since progress 74 the bar gives the keys back when a press in it lifts, and a tap in it opens no VOLUME on
   the lock screen. For the visual pass: the chevron is small and
   hard to hit with a case on, so it can stay small only where Previous goes back; pages where the knob doesn't
   navigate (Now Playing) need a prominent back button, and pages showing both the chevron and V2.1's navbar back
   settle on one. Previous now goes back on V2.1's slider pages too, and the PEQ's tab focus card shows only in
   Knob: Navigation (progress 65).
3. **Settings pages:**
   - the `navbar_only` rewrite, `ipod_list_layout` through V2.1's `list_view` layout vtable slot
     (`LIST_VIEW_LAYOUT_SLOT`), the settings icons (the `settings_icons` section), and the
     Display/Appearance/Controls pages;
   - retire `m1plus_nav_rows.c`, `m1plus_nav_display.c`, `m1plus_nav_sysset.c`,
     `m1plus_nav_audioset.c` and the M1 branches of `pod_rows`.

   Code and gates done on Nov 6 (progress 66):
   - **The rows:** V2.1's 32 settings pages hide their title bar and hold six 72 px rows. The Lock Screen page keeps
     its title bar, which holds its switch.
   - **The layout:** the list_view layout slot points at `ipod_list_layout`, which maps V2.1's buttonless rows.
   - **Back:** the chevron's tap is 64 px wide, and the hidden title bar's back button is still Previous's.
   - **Display:** Appearance (Theme, Light Mode, Accent, Battery), Coverflow and Controls (Smart Awake, the knob's
     two rows).
   - **Icons:** V2.1's settings icons keep their colours.

   `m1plus_nav_display.c` is retired. Three M1 files stay:
   - `m1plus_nav_rows.c`: V2.1's row shape for `list_row`. V2.1 lacks the Q2's row styles.
   - `m1plus_nav_audioset.c`: V2.1 rebuilds Playback's list on each return, so the payload's rows are added again.
   - `m1plus_nav_sysset.c`: System Setting in the iPod order by role (progress 67): the Q2's rows, then V2.1's
     extras, then maintenance, About last. The shared `reorder` takes the Q2's row ids, so the M1 keeps its seam.

   The M1 branches of `pod_rows`' callers are features, not V2.1's look (no Wake row, no volume guard, the knob
   rows), so they stay. Rows waiting for later items: Home and Shortcut (4.5), Centred Now
   Playing (4.6). The reordered settings passed on dev 57 (progress §68).
4. **Library (implemented and device-checked on dev 57, progress §68):**
   - compact rows: the local pages, `compact_set_row_layout` at V2.1's row-layout calls, and the
     immediates (the `immediates`, `row_layout_calls`, `private_prologues` and `event_abi_words` sections,
     and the other library words in `patch_code`);
   - Hold Return to Now Playing or Home: Previous held in Knob: Navigation wherever it is Back, and the
     status bar chevron held in either Knob mode (`m1plus_nav_back.c`);
   - retire `m1plus_coverflow_rows.c` and use the shared payload page rows in `coverflow.c`.

   Implementation: the V2.1 lists use 64 px pitch and 60 px bodies, with 40 px stock art. Payload lists use
   the shared page-row helpers at 64 px. Pull to search opens V2.1's `search_page`; playlist holds open
   the queue menu with More… opening the editor. Photos, Books and media folders enter through
   `library_page_open`. Verification and device-pass status are recorded in progress §68.
5. **Home:**
   - the `home_page.bin` rewrite with Split (art on top, menu below), Classic and Carousel (an `unported`
     row since the 1.5.9 sync);
   - the Coverflow card;
   - retire `m1plus_coverflow_home.c` and `m1plus_nav_home.c`.

   Implemented and gated on Nov 7 (progress §69; plan `.plan/phase4-5.md`):
   - **Entry pages:** `library_page_open` is the complete Library (upstream's order, V2.1's categories bound to its
     Home card click `0x533b80` by its Home ids, then CD Ripper and Update Local Music); `streaming_open` is
     Streaming (native Tidal and HiFi Music, then the payload's services and Configuration).
   - **The asset:** `home_page.bin` drops V2.1's grid, dots and playing strip, keeping the serial-error label;
     the Q2's Home lists and a portrait carousel take their place. V2.1's initializer and refresh still run:
     their returns with the grid gone are pinned (`m1plus_ipod.json` `home`), the playing strip's pointer-up
     binding is skipped, and the boot resume is `ringnav_boot`'s.
   - **Layouts:** Split is a 320x200 art panel over 64 px rows; Full the rows from the top; Carousel 290 px cards
     with 190 px art and arrows. Settings opens Playback and System from every layout; the chevron and
     Previous (Knob: Navigation) go back. Appearance has Home; Controls has Shortcut (no Rockbox or Games).
   - **Art:** the shared pan, at the M1's panel, with `DRIFT_TEXELS` four panels, V2.1's cover types,
     `savecover_path` as `g_lastcover_url`, and an unload by name on V2.1's lookup and unload.
   - `m1plus_coverflow_home.c` and `m1plus_nav_home.c` are retired.
6. **Now Playing (implemented Nov 8, progress §71; device-passed on `V053m`, and the Soloify page's touch and the other fixes of progress §72 on `V054m`; that pass's open findings are in §72):** the iPod layout with V2.1's
   transport row, Centred Now Playing on V2.1's own page, `bigcover`, the volume dialog, the quiet icons (the `quiet_icons`
   section) and the NP bar. Back is a large button in the page's top row; the chevron hides there. The knob stays the
   volume on the lyrics page, which scrolls by touch. The Spotify page, for both backends, takes the same layout; Radio
   keeps its stack. The scrub on the knob landed early (progress 58): `patch/m1plus_nav_np.c`, with `playing_timer_*`
   aliased to V2.1's.
   Both pages now share `patch/m1plus_np_view.c`: one source interface, painters, scrub and entry point (`compact_now_playing` opens the page that owns playback). Only the page trees, the slides and the cover
   pipelines stay separate.
7. **Quick Settings and dialogs (implemented Nov 12, progress §82):** upstream removed the wheel's Quick Settings in
   1.6.5, and the M1's pull-down is V2.1's own: a drag of more than 10 px from above y 81 opens
   `dialog/dropdown_dialog`, which stands in for V1.32's `statusbar_dialog` (`QUICK_NAME`). The payload hooks its
   init (`ringnav_quick_settings`) for the holds on Wi-Fi, Bluetooth and Playback and for `quick_cancel`, and the
   knob stays the volume while it is open. `tools/m1plus_ipod.py` lays out the pull-down as the iPod's Quick
   Settings and V2.1's centred 260x180 confirm pop-up as a full-width sheet from the top: its prompts above
   `CONFIRM_TOP` (112) at `CONFIRM_PROMPT_PX` (22) and Cancel and OK as two rows below them. Add to Playlist hooks
   V2.1's row builder (`playlist_rebuild`, `0x53e74c`): each playlist page keeps the add mode it opened with, and
   Now Playing's picker keeps its guarded pick on the rows New Playlist rebuilds. V2.1's New Playlist keyboard
   needs no rewrite (its `add_edit` has no `sensitive` prop). Pull-to-search now starts below the pull-down's edge.
   After the V063m pass (progress §83): in Knob: Navigation a single knob press closes Quick Settings and a double
   press turns the screen off (`quick_knob_key`); Knob: Volume keeps V2.1's power key. A hold menu's Add to Playlist
   opens V2.1's `playlist_page`. The confirm sheet has a 1 px foot rule and V2.1's toast is drawn in styles, so both
   read in Light Mode. The page under the pull-down keeps its highlighted row. The Playback and System Setting
   switches are dimmed while you are inside those settings by V2.1's design: its visitor disables them there and
   binds no click (`m1plus_ipod.json` `quick.into`).
   After the V064m pass (progress §84): a hold menu's View Queue off Shuffle opens V2.1's queue
   (`dialog/playqueue_dialog`), and an album's art comes back after Add to Playlist. The page under Quick Settings
   keeps its row while a knob turn's volume shows over it. V2.1's unticked ring ships as the Q2's, a clear ring, so
   Light Mode flips it. Choosing a Theme applies its `theme.xml` preset, as on the Q2: Modern turns Light Mode on
   with Cobalt, and Minimal turns it off with Graphite (Light Mode's Auto is kept). So Minimal to Modern setting
   `LIGHT` is by design.
8. **Left Q2-only, as `NOT PORTED` rows:**
   - Games (they need a design without the Return key and the wheel); the 181 execution checks are
     grouped as `Games (ipod-ui 4.8, Q2 only)` in `patch_gaps.py`;
   - the click sound (`buzzeer_switch`), unless the M1 has a buzzer;
   - `chord_gate`'s rim presses;
   - `WHEEL_TS_READ`;
   - Display's Corners (the glass is square), and Wheel QS, Wheel Sensitivity and Click With Headphones (no wheel,
     no buzzer) (4.3).

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
- land it on `staging` and release `1.5.9-m1.N`;
- restart the sync from 1.5.9 through the upstream-sync runbook ([m1plus-sync.md](m1plus-sync.md));
  `drift.py` then plans 1.6.0 and 1.6.3. The saved `work/sync/1.6.0-wip/` resolutions are reference only.
- The 1.6.x iPod features then arrive as ordinary port rows.

## Aesthetics queue

Looks left for the visual pass once the M1's functions are all ported. None is a fault; each was seen on the device.
The screenshots are under `work/phase4/4.5/device-pass/` (Phase 4.5's pass on `V04Hm`).
The Nov 4 finding that Now Playing needs a prominent back is closed by Phase 4.6's large top-row button.
- **Split's knob walk clips the top row.** Walking down Split's menu with the knob scrolls the list so that the row
  above the selection sits half under the art (`53-fav-sel.png`: Library cut at the top, Favorites selected).
- **Classic's Settings card is grey.** In Classic the Carousel's other cards keep V2.1's colours; Settings keeps its
  grey gear (`131-card.png`).
- **Classic's settings icons take different colours.** V2.1's rows keep their own colours (System: purple, teal,
  orange, green, red), and the payload's rows take theirs (Display: Appearance red, Coverflow blue; Controls: orange),
  with no common scheme (`141-system.png`, `143-controls.png`, `180-display.png`).
- **Split's cover is zoomed in too much.** The art panel is 320x200, so a square cover fills the width and its top and
  bottom are cropped (the Vergecast cover on `V04Om`: `work/phase4/4.5f/device-pass/301-home.png`). The user would
  rather see the whole cover in the same 200 px of height.
- **Now Playing's transport glyphs keep V2.1's colours.** Previous, Play and Next are its orange in both themes, on the
  iPod page, Centred and Spotify's (Phase 4.6; `work/phase4/4.6/i6-sheets/`). The accent or the theme's ink would suit
  them. Centred's art also sits 3 px right of centre, as V2.1 has it (`img_playcover` x 36, its DLNA twin 33).
- **Display's first rows are shifted and clipped.** The rows without icons (Brightness, Screen Off, Lock screen,
  Atmosphere Lamp Settings) start at the left edge, and "Atmosphere Lamp Settings" loses its first letters in both
  themes (`112-display.png`; again on `V04Om`, `work/phase4/4.5f/device-pass/008-display.png`). It may be a marquee
  caught mid-scroll.

## Files

- **Edited:** `tools/m1plus.py`, `patch/m1plus_offsets.inc`, `patch/m1plus_q2.inc`, `patch/navigation.c`,
  `patch/coverflow.c` and `patch/addon.c` (seams only), `tools/ipod.py` (the screen profile seam; its codec
  and rewrites are reused), `test/m1plus/{build,patch,boot,ports}.py`, `docs/m1plus-*.md`.
- **New:** `tools/m1plus_ipod.py`, `patch/m1plus_ipod.json`.
- **Reused as is:** `compile_payload()`'s trampoline fallback,
  `m1plus_names()`, `test/m1plus/suitemerge.py`, and q2remote for device screenshots.
- **Retired over Phase 4:** `m1plus_nav_rows.c`, `m1plus_coverflow_rows.c`, `m1plus_nav_display.c`,
  `m1plus_nav_sysset.c`, `m1plus_nav_audioset.c`, `m1plus_coverflow_home.c`, `m1plus_nav_home.c`,
  `m1plus_coverflow_back.c` (replaced by the chevron).

## Verification

After every commit:
1. **Q2 unchanged:** `TMPDIR=/tmp python3 test/q2compare.py 1.5.9 --suites` (1.5.8 before Phase 1.5). The
   iPod `update.tar` must be byte-identical.
2. **M1 gates:** a fresh `--dev` build, then `test/m1plus/build.py --build`, `patch.py`, `boot.py` (plain,
   `--home-menu` and `--media`), `playback.py`, `m4b`, `id3`, `headset_io`, `test/ldac.py`,
   `test/bluealsa.py`, then `ports.py`. Each ported row moves from `unported` to `ported`, and a
   `known_gap` that now passes is removed.
3. **CI suite:** `pytest test/unit`, from the 1.6.2 sync on (upstream adds `test/unit` in 1.6.2).
4. **Device:** at the end of each Phase 4 item, flash through the menu updater, then walk the feature over
   q2remote with screenshots. Record it as a progress section, with `test/m1plus/fndiff.py` against the
   build on the device.

Rough sizes (as in the roadmap: **S** a day, **M** a few days, **L** a week or more): Phases 0 to 2 **M**,
Phase 3 **M**, Phase 4 about **L** for every two items, each absorbing its own share of the audit.
