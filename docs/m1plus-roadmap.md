# M1 Plus port: planned work

The goal is upstream Q2 Pod's current release (DiamondBond/q2-pod) on the M1 Plus, kept in step by merging
each upstream release. This is what is left, ordered by value and effort. What has been done, and why, is
in [m1plus-progress.md](m1plus-progress.md). How one sync runs is in [m1plus-sync.md](m1plus-sync.md).

Every item ends in the same loop. First the Q2 checks must pass:
- Q2 Legacy and iPod still build byte-identical to the upstream base's build (`UPSTREAM_BASE`,
  section U). Until U2 records one, the base is `main`, which is upstream 1.2.2;
- the Q2 suites pass on both.

See [m1plus-integration.md](m1plus-integration.md#checklist). Then the build's name check,
`test/build.py --build`, `test/patch.py` and `test/boot.py` must pass on M1. Then flash through the
menu updater, and use the menu updater with stock `update.bin` to get back. Where an item's test is a `KNOWN GAP` or `NOT PORTED`
line today, the fix removes that marker. `known_gap` fails the run once its check passes, so a fixed
gap can't be left marked.

Sizes are rough: **S** is a day or less, **M** a few days, **L** a week or more.

**Next:** U0 is done: the Q2 builds are `main`'s again. The M1 release tool is done (section 6). Its
first package, 1.2.2-m1.1, passed its device check and is not published, since upstream is past 1.2.2:
the first published M1 release is 1.3.9-m1.1, after U3. Then section U goes on in order: the restructure (U1) and the sync tooling (U2) against
1.2.2, then the first sync to upstream 1.3.9 (U3). The M1 feature work waits until U3 lands: Spotify on the
device (section 3), the iPod UI (section 5) and the final pass (section 7). Section 4 is done for 1.2.2;
one device check waits for a library that needs it (section 4, "Later validation"). Functionality comes
first: items that only change how something looks wait for the final pass (section 7).

## Ground rules

- **Q2 output is upstream's.** No change for M1 may change the Q2 firmware or its tests:
  - Q2 Legacy and iPod `update.tar` stay byte-identical to the `UPSTREAM_BASE` tag's build with the same
    toolchain (`test/q2compare.py`, U2), and every Q2 suite and case of that tag keeps running and passing.
  - M1 code goes behind `#if M1PLUS` / `if m1plus` or into a per-model table. That includes defensive checks
    only V2.1 needs.
  - A deliberate Q2 change says so in its commit, with its reason and its test.
  - The full rule is in [m1plus-integration.md](m1plus-integration.md#rule-for-future-work-dont-break-q2).
- **M1 code sits beside upstream's, not inside it** (from U1 on). It lives in `tools/m1plus.py`,
  `patch/m1plus/` and `test/m1plus/`. An upstream file changes only by a seam: a hook call or
  `M1_HOOK(...)`, a target lookup, or an `#if !M1PLUS` wrapper. Each seam line is a conflict in every
  later sync, so keep them few.
- **Fix Q2 bugs upstream.** Never change upstream's Q2 code in the fork to fix a Q2 bug. Send the fix to
  DiamondBond/q2-pod (section 6, "Upstream contributions"), and keep any M1 copy of it behind `M1PLUS`
  until a sync brings the fix in.
- **Find each V2.1 address in V2.1's code, then pin it in a test.** Read the same-named or same-role
  function in V2.1's demo, and pin the instruction or string the change relies on, as
  `test/build.py`'s updater check and `test/patch.py`'s `tslib_run` check do. Never reuse a V1.32
  address.
- **Name every stock widget, image and style through `offsets.inc`** (`VIEW_`, `ICON_`, `STYLE_`,
  `ROW_`, `ABOUT_`), so the build's V2.1 name check covers it.
- **Build rows with `list_row`/`row_of`.** They build V2.1's row structure on M1. Don't reach a row's
  parts by child index.
- **Prefer V2.1's own UI conventions.** Its title-bar back button, its row styles, and its native
  settings where one exists (for example Double wake). Avoid copying a Q2 control V2.1 already has.
- **Every page has an explicit Back button.** Every page Q2 Pod opens or replaces on M1 shows V2.1's
  title-bar back button at its top left. Make it with `back_button`, or with `page_title`, which adds
  one; its click sends Return, and the page's keyup decides whether that closes the page or steps
  back one screen. The M1 has no Return key. Previous, Next and Play/Pause are media keys, as on
  stock, except that in Knob: Navigation Previous also presses the page's back button. So no
  gesture, hidden tap or key may be a page's only way out. Each new page's `test/boot.py` step
  closes it with the button (`BACK`).

## U. Tracking upstream

The branch forked from upstream 1.2.2 (`c0a2d6b`). By Oct 22, upstream was at **1.3.9**: 226 commits and
+9.7k/−1.9k lines over 71 files in six days, about 40 commits a day. A trial merge of 1.3.9 into this
branch conflicts in 22 files, about 150 hunks:

| File | Hunks | M1 footprint today |
|---|---|---|
| `test/patch.py` | 50 | +2,357/−1,159, 161 `m1plus` branches |
| `patch/navigation.c` | 25 | +724/−92, 64 `M1PLUS` sites (the largest 97 lines) |
| `tools/build.py` | 18 | +687/−250, 61 `m1plus` branches |
| `test/build.py` | 9 | +401/−98 |
| `test/playback.py` | 6 | +149/−114 |
| `patch/offsets.inc`, `docs/internals.md` | 5 each | `offsets.inc` +473/−33 |
| 15 more files | 1–4 each | |

The conflicts come from M1 code woven into upstream's files, so the plan is to move it out first (U1),
while the base is still 1.2.2 and the Q2 byte check can prove each move. Then merge (U3).

Each upstream release also adds V1.32-only work: hooks and call sites at V1.32 addresses, and new pages.
They stay off on M1 until ported (U4), so a sync never waits for them.

- **U0. Re-establish R1 against `main` (M). Done (Oct 22).** The open items of
  [m1plus-integration.md](m1plus-integration.md#work-items) are closed: 1 (`release.py` reads
  `input_sha256`) and 3–9 (the trampolines, `dispatch_key_return`, `boot_guard`, the V2.1 defences,
  `scratch_t`, the helpers, `ringnav_artist_list`). The byte compare found three more differences, now
  fixed: `ringnav_audioset`'s strings, the EQ's tab split and the AirPlay icon's mode
  ([m1plus-progress.md](m1plus-progress.md) section 37). Legacy and iPod `update.tar` are byte-identical
  to `main`'s build.
- **U1. Move the M1 beside upstream (L).** Each step keeps Q2 `update.tar` byte-identical to `main`'s.
  - **a. The M1's own build pipeline** ([integration item 11](m1plus-integration.md#work-items), now
    required). The user chose this over a shared `build()` reading a `Target` record (Oct 22): most of the
    M1's lines sat in `build()`'s Q2-only steps, and sharing them would re-indent upstream's lines under
    `if target.q2`, a conflict at every sync.
    - `tools/build.py` is upstream's, but for its seams: stock's `update.tar` as an input, `library_page`
      in `PAYLOAD_WINDOWS`, and one dispatch, `m1plus.build()` for an M1 input.
    - `tools/m1plus.py` holds the M1's tables (`M1PLUS_HOOKS`, `CALL_SITES`, `M1PLUS_GP`, the aliases and
      stubs, `M1PLUS_FUNCTIONS`, the paint leaf, `RTC_READ_M1PLUS`, `.pdr`, TagLib) and its pipeline:
      `build()`, `compile_payload()`, `compile_helper()`, `patch_m4b_cover()`. It reuses `build.py`'s
      helpers and tables where V2.1 matches V1.32.
    - The cost: a change upstream makes to `build()` that isn't at a V1.32 address (a new asset, helper
      or packing step) doesn't reach the M1 by itself. The sync runbook reviews `build()`'s diff for them.
    - **Done (Oct 22).** `tools/build.py` keeps 14 seam lines; `tools/peq.py` (the player's PEQ and
      ReplayGain patch, whose V2.1 profile moved too) and `tools/ipod.py` are upstream's text. Each step
      kept the Q2 and M1 builds byte-identical, and every suite and gate passes.
    - `tools/q2remote.py` keeps its M1 support (knob, swipe, the upright screen, `peek`) in place:
      upstream changed 4 of its lines in the 226 commits to 1.3.9, and moving it out would itself need
      seams in its command dispatch. Revisit if a sync conflicts there.
  - **b. Split `offsets.inc`.**
    - Upstream's body stays as upstream wrote it, inside `#if !M1PLUS … #endif`, and
      `patch/m1plus/offsets.inc` holds the V2.1 values.
    - A new upstream name then fails the M1 compile, which forces a choice: a V2.1 value, or
      `M1_UNPORTED`, which compiles its feature out on M1.
    - A geometry or style macro is shared only where its Q2 value is upstream's literal.
  - **c. Move the M1 blocks out of the shared `.c` files.**
    - Each `#if M1PLUS` block of more than about 10 lines moves to `patch/m1plus/*.c`. In `navigation.c`
      that starts with the blocks at 643, 6572, 5428, 3328, 1989, 6675, 5344 and 6269. The shared file
      keeps one call or `M1_HOOK(...)` line, empty on Q2.
    - Small inline differences stay inline, through named macros.
    - Prove each move with the byte compare, not by reading it. U0 found two moves that read as no-ops
      and weren't: a block factored into a static function, inlined on Q2, still moved that block's
      strings in `.rodata` and shifted every string address after them; and a macro that was meant to
      give upstream's literal was off by one.
    - Aim for under about 150 changed lines across upstream's `patch/*.c`, from about 1,400 now.
  - **d. Move the M1 tests out.**
    - `test/patch.py`'s and `test/build.py`'s M1 paths move to `test/m1plus/`. That covers the V2.1 harness
      addresses, the `KNOWN GAP` and `NOT PORTED` lists and the M1 scenarios, which import the shared
      helpers.
    - Upstream's Q2 sections go back to upstream's text wherever the branch only added an M1 branch.
    - `test/boot.py` is M1-only already.
  - **e. Measure the footprint.** `git diff --stat <upstream base> -- <upstream's files>`, recorded in
    [m1plus-sync.md](m1plus-sync.md#footprint) after U1 and after each sync, so that growth shows.
- **U2. Sync tooling (M).**
  - **`test/q2compare.py`** ([integration item 12](m1plus-integration.md#work-items), now required). It
    builds `UPSTREAM_BASE` from `git archive` and this tree, for Legacy and iPod, and compares their
    `update.tar`. On a difference, it diffs the `manifest.json` component hashes. It replaces the
    hand-run compare in the checklist.
  - **`UPSTREAM_BASE`,** a file holding the upstream tag and commit the branch is level with. This is
    the Q2 baseline that `q2compare.py` and these docs refer to.
  - **A port report.** It lists every Q2 hook, call site and `offsets.inc` name, and classifies each for
    M1 as ported, native in V2.1 (section 4's "Not ported, because V2.1 has them"), Q2 only by design, or
    `NOT PORTED`. It goes in `test/m1plus/`, or is a mode of `test/build.py`. A sync's new `NOT PORTED`
    rows go into U4.
  - **The `upstream` remote** (`https://github.com/DiamondBond/q2-pod.git`) and the merge recipe in
    [m1plus-sync.md](m1plus-sync.md).
- **U3. First sync: upstream 1.3.9 (L).**
  - Merge the tag, by the [sync runbook](m1plus-sync.md). Don't rebase: `m1plus-progress.md` cites the
    branch's commit hashes.
  - Done when:
    - `q2compare.py` against 1.3.9 is exact, and 1.3.9's suites pass on the Q2 builds;
    - the M1 gates pass, and the port report fills U4;
    - a device pass on the M1 has run.
- **U4. Upstream features to port (M each, many).** This is the porting queue from now on; section 4 is
  the record for 1.2.2. One row per feature from the port report: its hooks and sites, and what V2.1
  has. Porting follows the ground rules: find it in V2.1's code, then pin it in a test.
  - **Seeded by 1.3.9** (to confirm against the report):
    - **New pages:** games (`games.c`), chapters (`chapters.c`), Up Next (`upnext.c`), network update
      (`netupdate.c`, `systemset_fwupdate_page_init`), online match (`onlinematch.c`), Qobuz.
    - **Hooks:** lyric search and cover search (`kugou_obtainlyric`, `kugou_obtaincover`),
      `mclLoadExLyric`, the timezone page, `localmusic_playlistsmore_page_init`,
      `toolsQueryDbTableAndSort` and `toolsQueryContentDbTable`, `mclSetOutputWay`, `write_int_config`,
      `toolsGetMusicInfo`, `toolsIntoStandby`, `player_start_queue`, `networkGetWifiSignal`.
    - **Call sites:** `FOLDER_NAME`, `BT_INIT`, `BT_PARAMS`, `BT_STATUS`, `BT_AUTOLINK`, `PLAYER_COVER`,
      `ID3_PATH`, `LYRIC_FOLLOW`, `GRID_COVER`, `SCAN_REFRESH`, `DROP_CACHES`, and the lock screen's
      `lockscreen_access` sites.
    - **A known bug these fix:** a built-in wallpaper doesn't survive a reboot, on the Q2 at 1.2.2 and on
      the M1 (seen on 1.2.2-m1.1). `config_init` resets a picture that `access()` can't find to
      `screensaver_default`, and `q2pod:aurora` and the others aren't files. Upstream's
      `lockscreen_access` (1.3.9, `f1cfeb7`) replaces the two `jalr $25` to `access`: V1.32's
      `0x4fa41c` (`config_init`) and `0x4fad60` (`get_screensaver_image`). V2.1's are `0x4e6218`
      (`config_init`, `0x4e5030`) and `0x4d75b0` (`get_screensaver_image`, `0x4d7524`), both
      `0x0320f809` with `access` at `-0x834($gp)`. Pin both in `test/build.py` when they are ported.
- **U5. Each later release (S–M each).** Sync each upstream release tag soon after it ships, by the same
  runbook as U3. Its new features go into U4.

## 1. Small fixes (S)

Done: Crossfade's page on V2.1, the Playback rows that V2.1's list rebuild dropped, and the `test:`
lines that could be ported (see [m1plus-progress.md](m1plus-progress.md), section 14). What is left
here goes with other sections' features:

- **Videos' position bar on M1 (S).** q2video's M1 `overlay` (`patch/video.c`) runs the bar from
  x 20 to `H - 20` (460) on a 320 px row, so each of its 8 rows spills 140 px into the next one: it
  paints rows 450–458 across the whole width, where 450–457 from x 20 to 299 is meant. Found in U0 on
  the host, unchanged by it. The fix is `W - M1_BAR_X` as the end, with a host check in `test/m1plus/`
  (U1d) and a look on the device.
- **The `test:` lines whose features M1 can't reach yet.** Two lines, each going with its feature:
  - the stock key-down helper with STOP (`0x65f688`): with V2.1's copy of that private AWTK
    helper, still to be found (V2.1 binds no key-down handler for the payload to hook);
  - folder rollover and the UI scheduler delay: with the player call sites (section 4).

Done since: the Shuffle page's note and the Photos row's icon ([m1plus-progress.md](m1plus-progress.md)
section 20); Coverflow's track queue through `mclNextSong`, now on M1, and other slide menus' next and
previous, Q2 only since V2.1 has none (section 21).

## 2. Hardware-specific behaviour (M)

Done: Coverflow and Photos' scroll distance, and Coverflow's covers by touch: a swipe turns them a
cover per 100 px, and a tap opens the centre cover or brings a side one to the centre
([m1plus-progress.md](m1plus-progress.md) section 21).

## 3. Entry points for Q2 Pod's pages (L)

Done ([m1plus-progress.md](m1plus-progress.md) sections 17 and 22): every payload page has a way in
from the Q2 Pod page, a back button, and the touch long-press where the Q2 has a Play/Pause hold.
- **Streaming.** V2.1 has no Streaming page (its Tidal is a Home card), so Spotify, Internet Radio and
  AirPlay are rows on the Q2 Pod page, after Coverflow. Their Now Playing pages have back buttons,
  with their text under the art on the portrait screen.
- **Videos.** Its row shows with a Videos folder. q2video draws a back chevron at the top left, where
  a tap quits, and the knob is its wheel.
- **Long presses.** Most Played, the Ratings lists and Long Songs (the song menu), a station (in or
  out of favourites), a Spotify track (Spotify's queue) and Coverflow's centre cover (the album menu).

A video and Internet Radio play through q2video on the ES9069Q, straight after a boot too (dev 18,
[m1plus-progress.md](m1plus-progress.md) section 23). Left for the device:
- Spotify, with q2-librespot on the card: its `aplay` on `plughw:0,0`, and whether the Q2's static
  MIPS build runs on the M1's kernel.

## 4. Re-pointing V1.32 call-site patches (M each, many)

This section is complete for upstream 1.2.2's call sites. Call sites that later releases add go into U4.

Each `NOT PORTED` line below names a patch or hook made at a V1.32 address. A call site is ported by
adding its V2.1 words under its name in `CALL_SITES['m1plus']` (`tools/m1plus.py`):
- the build applies them, as it applies Q2's;
- `test/build.py` checks each word, and allows it in M1's demo diff;
- `test/patch.py`'s test for that name runs once the name is in the table (`'NAME' in SITES`). Its
  harness addresses are V1.32's until the test is ported too.

A hook goes in `M1PLUS_HOOKS` instead.

Done: the boot queue bug the check found. A reboot no longer deletes the saved advanced queue
([m1plus-progress.md](m1plus-progress.md) section 25). The five sites whose V2.1 code is V1.32's:
Shuffle's Play next and history, the page cache, the 65,000-song scan, the article-free sort and M4B in
folder scans (section 26). The Ratings hold on Now Playing's heart (section 27). The Lock screen page's
Clock row and built-in thumbnails, and the Large clock on V2.1's lock window (section 28). The cover
worker's pause and stale completion (section 30). The hold menu's row selection, and the Now Playing hold's
Add to Playlist guard (section 31). LDAC HQ (section 32), still to hear on the device. Gapless in
advanced play and across speed changes (section 33), still to hear with Gapless on. Resume on connect
(section 34), still to try with a Bluetooth headphone. Same-named albums' art, on Library Albums and an
artist's albums (section 35), still to see with two such albums on the card.

Every row had been checked against V2.1's `demo` on Oct 21 ([m1plus-progress.md](m1plus-progress.md)
section 24). All are now ported or found native in V2.1, and dev 20's device pass confirmed them
([m1plus-progress.md](m1plus-progress.md) section 36), LDAC HQ by its measured bitrate, except two
that wait for the right library: same-named albums' art and gapless by ear.

**Later validation: same-named albums' art** ([m1plus-progress.md](m1plus-progress.md) section 35). The
test card has no two albums of one name, so this waits until one does. To check:
1. Put two albums with the same name by different album artists on the card (for example two
   "Greatest Hits"), each in its own folder with its own cover, and run Update Local Music. A name in
   two folders without album artist tags splits the same way, by folder.
2. Library Albums shows the name twice, each row with its own cover, not one cover on both.
3. Each row's album page shows that album's big cover.
4. Each artist's page (Artists → the artist) shows its album with its own cover.
5. Over q2remote, `ls /tmp/abp` holds two different `<md5>0.jpg` files for the name, one per album.

If they share a cover, the build's `ALBUM_ART` sites (`tools/m1plus.py`, `CALL_SITES['m1plus']`) and
`artist_tab`'s keys are where to look.

**Later validation: gapless by ear** ([m1plus-progress.md](m1plus-progress.md) section 33). On dev 20,
q2remote showed Shuffle Albums preloading the album's next track and the change using it, and the
change sounded quick, but the test card has no gapless album: the tracks tried (Paramore's self-titled
album's live tracks) fade out. To check:
1. Put a truly gapless album on the card, one whose tracks run into each other (a live album without
   fades, a DJ mix, a concept album), and turn Playback Setting → Gapless on.
2. Play it in Shuffle Albums (Q2 Pod → Shuffle): each change within the album plays without a gap or
   click.
3. For comparison, the same change in plain playback (no advanced play) is stock's own gapless.
4. Optionally, over q2remote, read `MCL_PREPOS` and `MCL_PRELOAD` from `demo`'s memory near a track's end
   (section 36 says how): the preload is the album's next track, and `MCL_POS` becomes it.

A gap only in Shuffle Albums or Folders points at `ringnav_preload` and `ringnav_next`'s handoff
(`patch/playback.c`); a gap after a speed change is `ringnav_open_preload` refusing to open across it,
as intended.

Not ported, because V2.1 has them (ground rules: prefer V2.1's own UI):
- **Artist pages open on Albums** (`ARTIST_ALBUMS`): V2.1's artist page lists the artist's albums.
- **Key lock and quick lock rows** (`keylock_rows`, `quick_lock`): V2.1's Buttons lock has a switch and
  Volume, Keys and All modes.
- **Artists defaults to Album Artist, read at boot** (`read_artistype_value`, `ringnav_bootmode`):
  V2.1's Artists page has its own Artist/Album Artist switch, saved as `ARTISTTYPE` and read in
  `config_init`. A fresh config still starts on Artist.
- **Artists rows without the head picture** (`CLASS_ICON`): V2.1 draws its own artist icon.
- **The lock window's cover repaint** (`saver_cover`): V2.1's `image_base_set_image` always
  invalidates, where V1.32's skips an unchanged name, so its lock window repaints a new track's cover
  ([m1plus-progress.md](m1plus-progress.md) section 29).

Now Playing's info lines (`NP_INFO_CALL`) only change how the lines read, so they are in section 7.
Their V2.1 site is the fill's one call, `0x53bebc` (`0x0411f760`, the fill at `0x539c40`).

## 5. The iPod UI on M1 (L, after U3 and sections 1–4)

`--ipod` is refused for M1 Plus. The iPod UI patches V1.32's UI assets, styles and code layout, and
assumes the Q2's 375x320 landscape screen and touch wheel. An M1 version would be a redesign for a
320x480 portrait touchscreen with a knob, not a port. Decide whether it is wanted before starting.
Two `test/patch.py` checks go with it: the library rows' title bounds (`compact_row_layout`) and the
info pages' unwind (`navigator_close`). In the Stock UI each runs V1.32's own code as a control.

## 6. Tooling and release

- **Q2 from the same tree.** Section U0 closed the measured differences
  ([m1plus-integration.md](m1plus-integration.md)), and U2 turns the compare into `test/q2compare.py`
  against `UPSTREAM_BASE`. The Q2 release (`tools/release.py package`) works on this branch again. Its
  user guide needs `pdftotext`, which the devShell could add (`poppler-utils` in `flake.nix`).
- **Release packaging for M1 (M). Done (Oct 22),** as `tools/release_m1.py`
  ([m1plus-releasing.md](m1plus-releasing.md), [m1plus-progress.md](m1plus-progress.md) section 38).
  `tools/release.py` packages only the Q2, and upstream owns it, so the M1's goes beside it. It takes
  stock's V2.1 `update.bin` (or its vendor ZIP) and has:
  - a reproducible `update.bin`: two builds, compared byte for byte;
  - a manifest check (`model`, `input_sha256`, `logo_source`);
  - the M1 gates on the first build: the V2.1 name check, `test/build.py --build`, `test/patch.py` and
    `test/boot.py`;
  - a version from upstream's `VERSION` plus an M1 suffix (for example `1.3.9-m1.1`), so a release
    says which upstream release it carries, and a tag the updater takes over the last (`V1391`);
  - a release note with the reflash-to-stock instructions;
  - a `test/release_m1.py` for its failure paths, as `test/release.py` has for the Q2's.
- **q2remote on M1 (first: it makes the rest faster).** Done ([remote.md](remote.md#m1-plus)):
  - upright screenshots, keys, knob turns and taps;
  - `swipe X0 Y0 X1 Y1 [MS]`, from Goodix-CTP's move frames recorded on the device;
  - `tap X Y MS`, a held tap for the long press;
  - `peek NAME...`, payload and demo variables by name, field by field, from the running `demo`
    ([remote.md](remote.md#reading-variables)).

  A remote session now reaches the Q2 Pod page by itself. Next:
  - **An on-device log:** a small ring buffer the payload writes, which q2remote reads. `peek` shows
    state at one moment; a log would show the order of events, such as which of `qm_hold`'s checks
    refused during a hold.
- **Upstream contributions.** Q2 changes found through the M1, sent as pull requests to
  DiamondBond/q2-pod rather than made in the fork (ground rules). Once one lands upstream, the next sync
  brings it in, and the fork's `M1PLUS`-only copy can go. The three items after this one (the latent
  bugs, late-sound videos and playlist stations) are the first candidates. Two more go here:
  - **The seams.** Once U1's footprint is small, offer the `Target` record, the `offsets.inc` split and
    `M1_HOOK` on their own. They change no Q2 bytes, and with them upstream the fork's seam lines stop
    conflicting.
  - **The M1 target itself (later).** Once a few syncs have gone cleanly, offer the M1 target upstream.
    The squash-and-split note in [m1plus-integration.md](m1plus-integration.md#decision-finish-on-this-tree)
    covers its history.
- **Latent Q2 bugs found through M1.** Both were fixed only behind `M1PLUS`, to keep the Q2 build
  byte-identical (ground rules). Fixing them on the Q2 is a deliberate Q2 change, best made
  upstream, with a Q2 device check:
  - Long Songs' `taglib_file_new` call passes no `readAudioProperties`, so it reads whatever `$a1`
    holds; when that is 0, every length reads as 0 and is cached as measured;
  - AWTK's hit test doesn't skip hidden views, so the hidden book reader and photo viewer take taps
    meant for the list under them. The wheel hides this on the Q2; `view_show` is the M1's fix.
- **Videos whose sound starts late in the file.** q2video's one ffmpeg writes the picture and the
  sound, and q2video paces the picture by the sound played. A file that keeps more video ahead of its
  first sound than the picture's 4 MB pipe holds (8 Q2 frames; an mp4 interleaved by the second has
  25) stops on its first frame. The M1 runs the sound through a second ffmpeg (dev 16); the Q2 could
  do the same.
- **Radio stations whose URL is a playlist.** radio-browser's `/m3u/` lists can give a station's
  `.pls` (or `.m3u`) URL rather than its stream, which ffmpeg reads as text: the station shows "Can't
  play this station". Seen with Los 40 Principales México on dev 16. The Q2 has the same code, so this
  is a Q2 Pod change: resolve a remote playlist to its first stream, or ask radio-browser for
  `url_resolved`.
- **A card library in the emulator.** `test/boot.py --media` mounts a small card on a tmpfs: two long
  songs (header-only FLAC and MP3), a book and a photo, with V2.1's `songtable` seeded. Tags (album,
  artist) in the files and a scan would let the walk open Album, Artist and Now Playing. Playback itself
  would still need a stand-in for `hciplayer`'s audio output. The touch long-press's walk step (hold an
  album tile on an artist's page; the menu opens and the tile doesn't) waits for this.
- **An after-boot log on the device.** The `.rockbox/rockbox` diagnostic script can leave a background
  job that writes `ps` and the full `dmesg` a minute after boot. That captures demo crashes and driver
  errors that the emulator can't see.
- **Recovery mode.** The device has a separate recovery system (`kernel2`, `rootfs2`) and an `ota`
  partition. Finding how to start it without demo would give a way back to stock even if demo can't
  start, which would make riskier experiments safe.

## 7. Final pass: look and feel (after U3 and sections 1–4)

Items that only change how something looks, gathered once all the functionality is ported:

- **The Shuffle page's rows.** Its three rows (`shuffle_menu`, `page_row_detail`) show on M1 as bare
  centred text, with no row background or separator, where the Q2 Pod page's rows are V2.1's (ground
  rules: `list_row`/`row_of`). Seen over q2remote on dev 12; Ratings' page has the same rows (dev 14).
  Check the other `page_list` pages too: Internet Radio's menu shows the same in the emulator.
- **The Streaming rows' icons.** On the Q2 Pod page, Spotify's and Internet Radio's icons are wider
  than V2.1's 40 px row icons and reach the row's left edge (`stream_spotify`, `stream_radio`).
- **Now Playing's info lines** (`NP_INFO_CALL`). V2.1's info page writes `Label:value` lines (album,
  genre, year, size) and the folder alone. `ringnav_np_info` spaces them and labels the folder. V2.1's
  site is in section 4's notes.
- **Coverflow's covers by touch.** A tap on a side cover moves it to the centre, sized by the
  renderer's geometry; whether a swipe's feel (100 px a cover, a flick within 300 ms) suits the
  device's panel.

## Already Q2-only by design

These are skipped on M1 on purpose (marked `Q2 only` in the tests), not gaps:

- the touch wheel and its sensitivity;
- long Return;
- the sideways splash rotation;
- the Q2's Centre-key Wake setting (V2.1 has its own Double wake);
- Standby resume staying dark (`STANDBY_WAKE`): it goes with that Wake setting. V2.1's Standby also
  closes Bluetooth and unmounts the card, and a screen tap can wake it, which a dark resume would
  leave unlit;
- Home's Coverflow card: V2.1's Home is a grid of its own cards, and Coverflow opens from the Q2 Pod
  page;
- Key Tone: V2.1 has no buzzer command, and binds no key-down handler to hook.

The Rockbox dual boot stays: there is no Rockbox for the M1 Plus yet, but the hook serves as a boot-time
diagnostic.
