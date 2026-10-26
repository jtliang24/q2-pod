# M1 Plus port: planned work

The goal is upstream Q2 Pod's current release (DiamondBond/q2-pod) on the M1 Plus, kept in step by merging
each upstream release. This is what is left, ordered by value and effort. What has been done, and why, is
in [m1plus-progress.md](m1plus-progress.md). How one sync runs is in [m1plus-sync.md](m1plus-sync.md).

Every item ends in the same loop. First the Q2 checks must pass:
- Q2 Legacy and iPod still build byte-identical to the upstream base's build (`UPSTREAM_BASE`,
  section U);
- the Q2 suites pass on both.

`python3 test/q2compare.py --suites` checks both ([m1plus-integration.md](m1plus-integration.md#checklist)).
Then the build's name check, `test/m1plus/build.py --build`, `test/m1plus/patch.py`,
`test/m1plus/boot.py` and the port report, `test/m1plus/ports.py`, must pass on M1. Then flash through the
menu updater and stay on the build; stock `update.bin` is only for a catastrophic error. Where an item's test is a `KNOWN GAP` or `NOT PORTED`
line today, the fix removes that marker. `known_gap` fails the run once its check passes, so a fixed
gap can't be left marked.

Sizes are rough: **S** is a day or less, **M** a few days, **L** a week or more.

**Next:** the first full sync, to upstream 1.4.2 (U3): merges in steps, then a batch of ports, then
one device pass. All five steps, 1.2.9, 1.3.0, 1.3.8, 1.3.9 and 1.4.2, are merged and gated
([m1plus-progress.md](m1plus-progress.md) sections 40 to 44); 1.2.9 (dev 29), 1.3.0 (dev 5), 1.3.8
(dev 1) and 1.4.2 (dev 1) passed on the device. The batch of ports is done and passed on the device as
1.4.2 dev 3 (section 45), Standby Limit's power-off included, and section 7's look and feel with the
knob on Home followed (section 46).
`1.4.2-m1.1` is next. Done so far:
U0 (the Q2 builds are `main`'s again), U2 (the sync tooling, and a pilot sync to the 1.2.2 tag, which is
now the base), the M1 release tool (section 6; its 1.2.2-m1.1 passed its device
check and is not published, since upstream is past 1.2.2, so the first published M1 release is
U3's `<tag>-m1.1`), and U1 (the M1 code beside upstream's: +1,417/−279 lines over upstream's files,
from +6,417/−2,036). The M1 feature work waits until U3 lands: Spotify on the
device (section 3), the iPod UI (section 5) and the final pass (section 7). Section 4 is done for 1.2.2;
one device check waits for a library that needs it (section 4, "Later validation"). Functionality comes
first: items that only change how something looks wait for the final pass (section 7).

## Ground rules

- **Q2 output is upstream's.** No change for M1 may change the Q2 firmware or its tests:
  - Q2 Legacy and iPod `update.tar` stay byte-identical to the `UPSTREAM_BASE` tag's build with the same
    toolchain (`test/q2compare.py`, U2), and every Q2 suite and case of that tag keeps running and passing.
  - M1 code, defensive checks only V2.1 needs included, goes in M1 files (the next rule).
  - A deliberate Q2 change says so in its commit, with its reason and its test.
  - The full rule is in [m1plus-integration.md](m1plus-integration.md#rule-for-future-work-dont-break-q2).
- **M1 code sits beside upstream's, not inside it** (from U1 on). It lives in `tools/m1plus.py`,
  `patch/m1plus_*` and `test/m1plus/`. An upstream file changes only by a seam: an `#include` of an
  M1 file where its block stood, an `#if M1PLUS` / `#if !M1PLUS` wrapper, a name the M1 gives its own
  value (a `STYLE_*` for a literal), or `build.py`'s hand-off to `m1plus.takes()` / `m1plus.build()`. Each seam line is a conflict in every
  later sync, so keep them few.
- **Fix Q2 bugs upstream.** Never change upstream's Q2 code in the fork to fix a Q2 bug. Send the fix to
  DiamondBond/q2-pod (section 6, "Upstream contributions"), and keep any M1 copy of it behind `M1PLUS`
  until a sync brings the fix in.
- **Find each V2.1 address in V2.1's code, then pin it in a test.** Read the same-named or same-role
  function in V2.1's demo, and pin the instruction or string the change relies on, as
  `test/m1plus/build.py`'s updater check and `test/m1plus/patch.py`'s `tslib_run` check do. Never reuse a V1.32
  address.
- **Name every stock widget, image and style through a name** (`VIEW_`, `ICON_`, `STYLE_`, `ROW_`,
  `ABOUT_`: V2.1's in `patch/m1plus_offsets.inc`, the Q2's in `patch/m1plus_q2.inc`), never a string in
  shared code, so the build's V2.1 name check covers it and the Q2 keeps its own.
- **Build rows with `list_row`/`row_of`.** They build V2.1's row structure on M1. Don't reach a row's
  parts by child index.
- **Prefer V2.1's own UI conventions.** Its title-bar back button, its row styles, and its native
  settings where one exists (for example Double wake). Avoid copying a Q2 control V2.1 already has.
- **Every page has an explicit Back button.** Every page Q2 Pod opens or replaces on M1 shows V2.1's
  title-bar back button at its top left. Make it with `back_button`, or with `page_title`, which adds
  one; its click sends Return, and the page's keyup decides whether that closes the page or steps
  back one screen. The M1 has no Return key. Previous, Next and Play/Pause are media keys, as on
  stock, except that in Knob: Navigation Previous also presses the page's back button. So no
  gesture, hidden tap or key may be a page's only way out. Each new page's `test/m1plus/boot.py` step
  closes it with the button (`BACK`).

## U. Tracking upstream

The branch forked from upstream 1.2.2 (`c0a2d6b`). By Oct 22, upstream was at **1.3.9**: 226 commits and
+9.7k/−1.9k lines over 71 files in six days, about 40 commits a day. A trial merge of 1.3.9 into this
branch conflicts in 22 files, about 150 hunks:

| File | Hunks | M1 footprint then (before U1) |
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
  - **b. Split `offsets.inc`. Done (Oct 22).**
    - Upstream's body stays as upstream wrote it, behind `#if M1PLUS #include "m1plus_offsets.inc" #else`,
      5 seam lines. `patch/m1plus_offsets.inc` holds every name at its V2.1 value.
    - `patch/m1plus_q2.inc` holds the Q2's values for the 86 names the port added to shared code (styles,
      views, icons, `UI_W`, `W_CHILDREN`...), included after upstream's. Each is V1.32's, or an upstream
      literal the shared code now names; U1c can drop those the moved code no longer needs.
    - The M1 files are flat, `patch/m1plus_*`, not `patch/m1plus/`: upstream's `source_sha256` hashes
      `patch/*` as files, and a flat name stays in it with no seam.
    - A new upstream name then fails the M1 compile, which forces a choice: a V2.1 value, or
      `M1_UNPORTED`, which compiles its feature out on M1.
    - A geometry or style macro is shared only where its Q2 value is upstream's literal.
  - **c. Move the M1 blocks out of the shared `.c` files. Done (Oct 22).**
    - Each `#if M1PLUS` block of about 10 lines or more moved to its own `patch/m1plus_*` file (31 of
      them), and the shared file keeps one `#include` where it stood, after any Q2 `#else` code inside
      `#if !M1PLUS`. Each file wraps its code in `#if M1PLUS`, so each model compiles the same text in the
      same order: both builds stayed byte-identical through every move. Blocks inside a function or
      `scratch_t` are `.inc` fragments of it.
    - The declarations went to `m1plus_nav.h`, `m1plus_peq.h` and `m1plus_peq_decls.h`, and
      `peq_player.c`'s V2.1 addresses override upstream's literals after them.
    - The port's rewrites of upstream's comments are undone; their V2.1 notes are in
      [m1plus.md](m1plus.md) section 8.
    - Small inline differences stay inline, through named macros.
    - Prove each move with the byte compare, not by reading it. U0 found two moves that read as no-ops
      and weren't: a block factored into a static function, inlined on Q2, still moved that block's
      strings in `.rodata` and shifted every string address after them; and a macro that was meant to
      give upstream's literal was off by one.
    - The aim was under about 150 changed lines across upstream's `patch/*.c`. The result is
      +671/−226, from about +1,945/−290: most of the rest are one-line seams that stay by design, a literal
      named by a macro with upstream's Q2 value (`UI_W`, `STYLE_…`, `view_show`), an `#include`, or an
      `#if` around a Q2-only line. Lowering it further would mean restructuring upstream's functions.
  - **d. Move the M1 tests out. Done (Oct 22).**
    - `test/` holds upstream's suites, and `patch.py`, `build.py`, `playback.py`, `id3.py`, `m4b.py` and
      `headset_io.py` there were upstream's text but for one line: `playback.py` picked the hold menu's
      Shuffle by its label, as upstream 1.3.9 does, since `main`'s fixed index failed on `main`'s own build.
      Since the 1.2.2 sync, which has the same pick, all six are upstream's text, and `patch.py` passes
      1.2.2's 1029 (Legacy) and 1410 (iPod) scenarios.
    - `test/m1plus/` holds the M1's: those six as the branch had them, with both models' paths, and
      `boot.py`; U2 added `ports.py` and `q2only.py`. They run on M1 builds as before; their Q2 branches are dead there and can be trimmed.
    - `coverflow.py` and `peq.py` stay in `test/` with small seams: they build the shared C on the host,
      which the port changed. `remote.py` keeps its M1 cases, as `tools/q2remote.py` does.
  - **e. Measure the footprint. Done (Oct 23).** After U1: +1,417/−279 over upstream's 31 changed files,
    from +6,417/−2,036 over 38. What remains is `patch/*.c`'s one-line seams (+671/−226), `tools/q2remote.py`
    (+443) and the docs' and tests' M1 notes. It is measured with `git diff --stat <upstream base> --
    <upstream's files>` and recorded in [m1plus-sync.md](m1plus-sync.md#footprint) after U1 and after each
    sync, so that growth shows.
- **U2. Sync tooling (M). Done (Oct 23)** ([m1plus-progress.md](m1plus-progress.md) section 39).
  - **`test/q2compare.py`** ([integration item 12](m1plus-integration.md#work-items)). It builds
    `UPSTREAM_BASE` from `git archive` and a snapshot of this tree, Legacy and iPod, from the vendor ZIP,
    and requires byte-identical `update.tar`. On a difference it names the differing `manifest.json`
    components and the first moved symbol. `--suites` runs the base's suites on the tree's builds. It
    replaces the hand-run compare in the checklist.
  - **`UPSTREAM_BASE`**, at the repo's root: the upstream tag and commit the branch is level with, the Q2
    baseline these docs refer to. It is `1.2.2` (`87e2417`).
  - **The port report**, `test/m1plus/ports.py`. It lists every Q2 hook, call site and `offsets.inc`
    name, and classifies each for M1 as ported, native in V2.1, Q2 only, or `NOT PORTED`, from
    `M1PLUS_PORTS` in `tools/m1plus.py` and `M1_UNPORTED` in `patch/m1plus_offsets.inc`. A hook or site
    it can't place fails it. A sync's new `NOT PORTED` rows go into U4.
  - **The `upstream` remote** (`https://github.com/DiamondBond/q2-pod.git`) and the runbook,
    [m1plus-sync.md](m1plus-sync.md).
  - **A pilot sync to the `1.2.2` tag.** The branch had forked at `c0a2d6b`, 13 commits before the tag.
    The merge had no conflicts, but the M1 needed three follow-ups: a trampoline stub, two
    `M1_UNPORTED` names and an unused page. Those, and the new test cases the M1 copies missed, became
    runbook rules.
  - **Its device pass** (dev 21) found two more the gates had missed: a Q2 style named by its string in
    Coverflow, and a key-up change the merge took only in Q2-only code. Both are fixed (dev 22), with a
    harness check for the first and `test/m1plus/q2only.py` for the second, both now runbook rules.
- **U3. First sync: upstream 1.4.2 (L).** The user chose 1.4.2 on Oct 23. 1.4.3, out the same day,
  is the first U5 sync. 1.4.2 is 235 commits past 1.2.2, and a trial merge conflicts in 15 files, 57
  hunks (28 in `navigation.c`). U1 brought this down from about 150 hunks.
  - **Merge in steps**, each one a full pass of the [sync runbook](m1plus-sync.md):
    1.2.9 → 1.3.0 → 1.3.8 → 1.3.9 → 1.4.2. Don't rebase: `m1plus-progress.md` cites the branch's commit
    hashes.
    - Each step only merges and keeps the M1 working. New upstream features stay off on M1, as
      `unported` rows.
    - Each step's `--dev` build is gated and kept in `work/u3/<tag>/`, and `test/m1plus/fndiff.py` lists
      the payload functions it changed against dev 22.
    - 1.3.9 is its own step for 13f04f0, which moves the payload's scratch state to 0xb80000 and lets it
      grow to 128 KB. The M1 takes `SCRATCH` from `build.py`. 1.3.8 already moves it once, to 0xb60000
      (`9738051`), and V2.1's `demo` maps nothing above its data segment's end (0xa10fc8): the payload's
      segment at 0xb00000 grows, and the heap starts above `__scratch_end`. Checked at the 1.3.8 step,
      for both moves. 13f04f0 also folds `.bss` into `.scratch`, upstream's own fix for the orphan
      `.bss` the 1.3.8 step found on M1 (progress section 42), so there is no PR to raise.
  - **Then port the finished features in one batch. Done (Oct 24,** [m1plus-progress.md](m1plus-progress.md)
    **section 45):** all but the time zones, which went to U4 (the user's choice), and with one fix the
    device pass found (`LYRIC_SOURCES`: V2.1 ran NetEase after every lyric search). Those whose code
    doesn't change after the step that brings them, whose function V2.1's `demo` has, and that aren't
    tied to the Q2:
    - the shared hooks `toolsQueryDbTableAndSort` (V2.1's `0x5ee9ac`) and `networkGetWifiSignal`
      (`write_int_config` and `mclSetOutputWay` are native: V2.1 keeps Bluetooth's level apart);
    - `lockscreen_access` (the wallpaper fix, below);
    - the timezone page (`select_timezone`): to U4;
    - View Queue's and Up Next's picks in a shuffle's play order (`player_start_queue`, V2.1's
      `start_playqueue`, `0x4e47d0`, which the payload's own calls already reach by alias);
    - embedded lyrics (`mclLoadExLyric`);
    - chapters;
    - online cover and lyric search (`kugou_obtain*`);
    - Standby Limit (`toolsIntoStandby`): V2.1's RTC alarm wakes it at the limit, and it powers off.

    Porting after the merges, not at each step, ports each feature once, against the final code, and
    keeps each step's changes to merges alone.
  - **One device pass at the end**: the function diff's list plus the ports. A regression is bisected by
    flashing the kept step images.
  - Done when:
    - `q2compare.py` against 1.4.2 is exact, and its suites pass on the Q2 builds;
    - the M1 gates pass, and the port report fills U4;
    - the device pass has run. `1.4.2-m1.1` is then the first published M1 release.
- **U4. Upstream features to port (M each, many).** This is the porting queue from now on; section 4 is
  the record for 1.2.2. One row per feature from the port report: its hooks and sites, and what V2.1
  has. Porting follows the ground rules: find it in V2.1's code, then pin it in a test.
  - **Found by the port report** (U2), in 1.2.2's hooks and names:
    - *Done (Oct 25, [progress section 47](m1plus-progress.md)).* **A manual Play/Pause and the headset** (`player_play_pause` → `ringnav_play_pause`). On the Q2
      it calls `headset_manual`, so a headset's automatic resume doesn't undo a pause the user made.
      V2.1's `play_pause_music` is aliased but not hooked. Find its callers in V2.1's `demo` first.
    - **Folder's roots without OTG** (`folder_load_top` → `ringnav_folder_top`). Without a drive, the
      Q2 lists the card alone. Check whether V2.1's Folder lists OTG at all before porting.
    - *Done (Oct 25, [progress section 47](m1plus-progress.md)).* **A FLAC's ALBUM ARTIST** (`toolsGetMusicInfo` → `ringnav_music_info`, new in 1.2.2). The Q2 reads
      foobar2000's spelling when stock's libtag finds no `ALBUMARTIST`. V2.1's `toolsGetMusicInfo`
      keeps the album artist at `+0x580` too (`MUSIC_INFO_ALBUM_ARTIST`, pinned since the 1.2.9 step),
      so only the hook is left.
    - **Tidal's cache and Tidal Downloads** (`tidal_play`, `tidal_downloads`, `REC_TIDAL_ID`). On M1
      `tidal_start` passes no song id, since V2.1's two callers (`0x500d5c`, `0x51c7b0`) keep none, so
      Tidal streams uncached and there is no Downloads row. V2.1's `get_tidal_trackurl` (`0x512ed0`) hands
      its URL thread (`0x51c288`) the queue row: the id is to be found there.
    - `NP_INFO_CALL` stays in section 7.
  - **Found by the 1.2.9 step** (U3, Oct 23):
    - **An artist's albums tab's album-artist rewrite** (`toolsQueryContentDbTable`): V2.1 has no such
      function, so find what V2.1's `getAlbumByAlbumArtist` queries through first.
    - *Done (Oct 25, [progress section 47](m1plus-progress.md)).* **Now Playing's art through ffmpeg** (`PLAYER_COVER`), **Bluetooth's callbacks before the radio
      powers on** (`BT_POWER`) and **a folder scan refreshing existing tags** (`SCAN_REFRESH`): call
      sites, each to find in V2.1's `player_parsecover_thd`, `openBluetooth` and `toolsLoadAllFile`.
    - **`check_mem_thd` returning at once** (`DROP_CACHES`' 1.2.9 form, a battery fix). The M1 keeps
      1.2.2's: `check_cpumem`'s write branched over. Check what else V2.1's thread does first.
    - **The MQA side chain** (`tools/peq.py`'s `MQA_GATE` and `MQA_PROBE`, a battery fix): the decoder
      runs only on MQA streams, and the probe is sized to the detector. V2.1's `hciplayer` takes
      `PLAYER_PROFILE`'s words, which don't have these yet.
    - **Streaming's Configuration** (`stream_config`): the cache sizes and Stop Streaming Services. It
      would be a Q2 Pod page row on M1, with an icon of V2.1's.
    - **Test cases that need V1.32 code**: Folder Root's open and Back (V2.1 keeps one history stack,
      `yoffset_rowsave`, and `m3ufile_path`), and Shuffle Songs being one-shot (V2.1 has no
      `config_playmode` symbol to stand for the user's mode choice). Both features run on M1.
    - Q2 only: Hold Return: Home (the M1 has no Return key) and Volume Guard (the touch wheel's).
  - **Found by the polish pass** (Oct 25, progress section 46):
    - *Partly done (Oct 25, progress section 47): the stock pages have rows; the Tidal and HiFi pages wait for an account to check them on.* **Knob: Navigation outside System Setting.** The knob turns the volume on V2.1 pages ringnav
      doesn't list: stock's View Queue dialog (`playqueue_dialog`; `playmore_dialog` is Now Playing's ⋯ menu), the Home editor (`homemenu_dialog`),
      search (`search_page`, `onlinesearch_page`), CD Ripper (`cdripper_page`, `searchcdripper_page`),
      Recent and Frequent's `guide_page`, and the Tidal and HiFi store pages. Each needs a check on the
      device before its `m1plus_contexts.inc` row.
    - **Set Time Manually** (V2.1's `datetime_page`, two text-selector views in a `slide_view`) isn't
      the Q2's `manualtime_page`: the knob turns the volume there.
  - **Found by the batch** (U3, Oct 24):
    - **The extra time zones** (`select_timezone`, V2.1's `0x4d6b2c`). V2.1 keeps its 27 labels as a
      `const char *` table at `0x97c810`, NULL-ended, with the `lan_*` table right after it, and its row
      layout (`timezone_listitem_layout`, `0x4a21c8`) copies the table onto its stack (108 bytes, under
      another buffer), so the table can't grow. A jal at the label read (`0x4a224c`) returning the
      payload's labels would do instead. The counts to raise by 11: the page builder's `li 29`
      (`0x4a246c`), the click's `sltiu 30` (`0x4a2604`), `config_init`'s `sltiu 27` (`0x4e65dc`); the
      hook covers `select_timezone`'s own (`0x4d6b68`). `set_systime` (`0x4d77b0`) and
      `networktime_adjust_thd` (`0x4d9454`) each have a `sltiu 28` to read first.
  - **Found by the 1.3.0 step** (U3, Oct 23):
    - **Lyrics from tags**, **Standby Limit** and **the Wi-Fi signal**: ported in the batch.
    - **Wi-Fi power save** (`WIFI_LPS`, a battery fix): V2.1's demo has the same
      `rtwpriv wlan0 pm_set lps=0` string, so it's a string patch to port.
    - **The Wi-Fi transfer page** (`WEB`: English, folder uploads): V2.1 has `/usr/share/web`; check its
      files against the patch's strings.
    - *Done (Oct 25, [progress section 47](m1plus-progress.md)).* **Folder names with `%`** (`FOLDER_NAME`): stock's row formatter crashes on them; check V2.1's
      `folder_create_tablerow` (`0x5331fc`).
    - *Done (Oct 25, [progress section 47](m1plus-progress.md)).* **A CUE track's file tags** (`ID3_PATH`) and **Ogg art in the grids** (`GRID_COVER`).
  - **Found by the 1.3.8 step** (U3, Oct 24):
    - **Network Update** (`systemset_fwupdate_page_init`, `netupdate.c`): it fetches DiamondBond's Q2
      `update.tar`, so it stays off until it points at the fork's M1 releases. Its `fwupdate_tf`, stock's
      TF card update, is `M1PLUS_UNRESOLVED`: V2.1's twin is to be found from its updater thread
      (`0x471070`, which calls `update_firmware`) back to the System Update row's click.
    - *Done (Oct 25, [progress section 47](m1plus-progress.md)).* **Playlist editing, and a playlist row's hold** (`localmusic_playlistsmore_page_init`,
      `PLAYLIST_ADD_MODE`): V2.1 has `playlist_page` but no `playlistsmore_page`. The hold stays in
      `qm_hold`'s Q2 branch, and `more_image` is named from `m1plus_nav_library.c`.
    - *Done (Oct 25, [progress section 47](m1plus-progress.md)).* **Bluetooth's boot and incoming links** (`BT_INIT`, `BT_PARAMS`, `BT_STATUS`, `BT_AUTOLINK`, in place
      of 1.2.9's `BT_POWER`): V2.1's `platform_init`, `openBluetooth` and `autoLinkBluetooth` to check.
    - *Done (Oct 25, [progress section 47](m1plus-progress.md)).* **The lyrics' top row whole** (`LYRIC_FOLLOW`): V2.1's Now Playing timer to check. With it, 1.3.9's
      **lyrics keeping their place on a refresh** (`LYRIC_ROWS`): V2.1's page refresh and its lyric row
      builder to find. `ringnav_lyric_rows` calls V1.32's builder by its address (`0x529f0c`), so it
      needs an `offsets.inc` name before the site is ported. On M1 it links (the build keeps the
      `ringnav_*` entry points) but nothing calls it.
    - **Quick settings' brightness through a swipe up**: `g_dropdown_menu_state` is a stub on M1; V2.1 has
      `dropdown_menu_state` (`0xa05a2c`) and a `slider_backlight`, whose states are to be checked against
      V1.32's (1, 2 sliding, 3 open) before it is aliased.
    - Q2 only: Return closing a search's keyboard (`search_key`), and `ringnav_input`'s USB prompt keys and
      Now Playing's transition volume ticks (the wheel's). The M1's input include hands a key to stock first.
  - **Found on the device** (1.3.8 dev 1, Oct 24; progress section 42):
    - *Q2 only (the user's choice, Oct 25): the knob stays volume there.* **Quick Settings' knob stays volume.** `knob_nav_active` leaves the pull-down to stock, so 1.3.8's
      Play/Pause hold there (the wheel's brightness or volume, `QSVOLUME`) changes nothing on the M1.
      Either take the knob in Quick Settings when Knob: Navigation is on, or mark the hold Q2 only.
    - *Done (Oct 25, [progress section 47](m1plus-progress.md)).* **A Now Playing under a folder play doesn't refresh.** Go to Folder from Now Playing, then a play
      from the folder, opens a second Now Playing. Back past the folders reaches the first, which still
      shows the old track and position beside the new track's time. Check whether V2.1's own playing_page
      refreshes when another one is on top, or close the lower one on a new play.
  - **Found on the device** (1.4.2 dev 1, Oct 24; progress section 44), all older than 1.2.2:
    - *Done (Oct 25, [progress section 47](m1plus-progress.md)).* **The hold menu's Go to Artist does nothing**, from a song's menu and from Cover Flow's.
      `qm_goto` opens `localmusic/artistinfo_page` with V1.32's `{cls, record}` context. Find what
      V2.1's own callers hand `artistinfo_page`.
    - *Done (Oct 25, [progress section 47](m1plus-progress.md)).* **Its Go to Album opens the playing song's album.** `qm_goto` fills V1.32's
      `g_local_classinfo_save` and opens `playerjumpinfo_page`, which on V2.1 reads the playing song.
      Open the row's album as Album's list does instead.
    - ~~The hold menu closes only by OK.~~ Done (progress section 46): a tap outside and Previous close it.
  - **Found on the device** (dev 29, Oct 23):
    - ~~The rating picker has no way out but a rating.~~ Done (progress section 46): a tap outside it, or
      Now Playing's back button, closes the picker alone.
  - **Found on the device** (dev 21, Oct 23):
    - *Done (Oct 25, [progress section 47](m1plus-progress.md)).* **A touch hold on an album's tracks plays the track.** On Album's list the hold menu opens for the
      row held. On an album's track list (16 tracks), `load` counted 17 rows (`g_menu.rows`, read over
      q2remote), so `qm_hold`'s check against the showlist's size fails and the release's click plays the
      row. The hold code is the same as V1221's, so the gap is likely older than 1.2.2. Find what the
      17th row is first (the album header?).
  - **Seeded by 1.3.9** (to confirm against the report; a later tag adds its own):
    - **New pages:** games (`games.c`), chapters (`chapters.c`), Up Next (`upnext.c`), network update
      (`netupdate.c`, `systemset_fwupdate_page_init`), online match (`onlinematch.c`), Qobuz.
    - **Left for after U3, and why** (checked Oct 23 against 1.4.2 and V2.1's `demo` symbols):
      - V2.1 has no `toolsQueryContentDbTable` or `localmusic_playlistsmore_page_init`. Each needs a
        V2.1 stand-in found first. (`player_start_queue` is V2.1's `start_playqueue`: ported in the batch.)
      - Network update fetches DiamondBond's Q2 `update.tar`. It stays off on M1 until it points at
        the fork's M1 releases.
      - *Done (Oct 25, [progress section 47](m1plus-progress.md)).* The card app host (`addon.c`, `usbmode_page_init`, 1.4.2) runs over librespot: it goes with
        section 3. So does System settings' **Apps** (1.4.0's Q2 Shelf, `netupdate.c`), which installs
        the card apps, Rockbox and Spotify from their GitHub releases: its row is off on M1 (`!M1PLUS`
        in `ringnav_systemset`). Whether what it downloads runs on the M1 is to be checked first.
      - Games changed again in 1.4.2 and use the Return key, which the M1 lacks. They need a touch
        design.
    - **Hooks:** the timezone page, `localmusic_playlistsmore_page_init` and `toolsQueryContentDbTable`
      (`mclSetOutputWay` and `write_int_config` are native; the batch ported the rest).
    - **Call sites:** `FOLDER_NAME`, `BT_INIT`, `BT_PARAMS`, `BT_STATUS`, `BT_AUTOLINK`, `PLAYER_COVER`,
      `ID3_PATH`, `LYRIC_FOLLOW`, `GRID_COVER`, `SCAN_REFRESH`, `DROP_CACHES` (the lock screen's
      `lockscreen_access` sites: ported in the batch).
    - **A known bug these fix:** a built-in wallpaper doesn't survive a reboot, on the Q2 at 1.2.2 and on
      the M1 (seen on 1.2.2-m1.1; fixed on M1 by the batch's `LOCKSCREEN_ACCESS`, section 45). `config_init` resets a picture that `access()` can't find to
      `screensaver_default`, and `q2pod:aurora` and the others aren't files. Upstream's
      `lockscreen_access` (1.3.9, `f1cfeb7`) replaces the two `jalr $25` to `access`: V1.32's
      `0x4fa41c` (`config_init`) and `0x4fad60` (`get_screensaver_image`). V2.1's are `0x4e6218`
      (`config_init`, `0x4e5030`) and `0x4d75b0` (`get_screensaver_image`, `0x4d7524`), both
      `0x0320f809` with `access` at `-0x834($gp)`. Pin both in `test/m1plus/build.py` when they are ported.
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
[m1plus-progress.md](m1plus-progress.md) section 23). The Q2's static q2-librespot runs on the M1's
kernel: on dev 21 it was up and signed in, and the Spotify page's menu loaded. Left for the device:
- Spotify's sound: a track through its `aplay` on `plughw:0,0`.

## 4. Re-pointing V1.32 call-site patches (M each, many)

This section is complete for upstream 1.2.2's call sites. Call sites that later releases add go into U4.

Each `NOT PORTED` line below names a patch or hook made at a V1.32 address. A call site is ported by
adding its V2.1 words under its name in `CALL_SITES['m1plus']` (`tools/m1plus.py`):
- the build applies them, as it applies Q2's;
- `test/m1plus/build.py` checks each word, and allows it in M1's demo diff;
- `test/m1plus/patch.py`'s test for that name runs once the name is in the table (`'NAME' in SITES`). Its
  harness addresses are V1.32's until the test is ported too.

A hook goes in `M1PLUS_HOOKS` instead.

Done: the boot queue bug the check found. A reboot no longer deletes the saved advanced queue
([m1plus-progress.md](m1plus-progress.md) section 25). The five sites whose V2.1 code is V1.32's:
Shuffle's Play next and history, the page cache, the 65,000-song scan, the article-free sort and M4B in
folder scans (section 26). The Ratings hold on Now Playing's heart (section 27). The Lock screen page's
Clock row and built-in thumbnails, and the Large clock on V2.1's lock window (section 28). The cover
worker's pause and stale completion (section 30). The hold menu's row selection, and the Now Playing hold's
Add to Playlist guard (section 31). LDAC HQ (section 32). Gapless in advanced play and across
speed changes (section 33). Resume on connect (section 34). Same-named albums' art, on Library Albums and
an artist's albums (section 35).

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
Two `test/m1plus/patch.py` checks go with it: the library rows' title bounds (`compact_row_layout`) and the
info pages' unwind (`navigator_close`). In the Stock UI each runs V1.32's own code as a control.

## 6. Tooling and release

- **Q2 from the same tree.** Section U0 closed the measured differences
  ([m1plus-integration.md](m1plus-integration.md)), and U2 turned the compare into `test/q2compare.py`
  against `UPSTREAM_BASE`. The Q2 release (`tools/release.py package`) works on this branch again. Its
  user guide's `pdftotext` is in the devShell (`poppler-utils` in `flake.nix`).
- **Release packaging for M1 (M). Done (Oct 22),** as `tools/release_m1.py`
  ([m1plus-releasing.md](m1plus-releasing.md), [m1plus-progress.md](m1plus-progress.md) section 38).
  `tools/release.py` packages only the Q2, and upstream owns it, so the M1's goes beside it. It takes
  stock's V2.1 `update.bin` (or its vendor ZIP) and has:
  - a reproducible `update.bin`: two builds, compared byte for byte;
  - a manifest check (`model`, `input_sha256`, `logo_source`);
  - the M1 gates on the first build: the V2.1 name check, `test/m1plus/build.py --build`, `test/m1plus/patch.py` and
    `test/m1plus/boot.py`;
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
  - **The seams.** U1 made the footprint small (+1,417/−279), so offer the seams on their own: the
    `offsets.inc` split, the `#include` points for the M1 files, the names that stand for literals
    (`patch/m1plus_q2.inc`) and `build.py`'s hand-off to `m1plus`. They change no Q2 bytes, and with them
    upstream the fork's seam lines stop conflicting.
  - **The M1 target itself (later).** Once a few syncs have gone cleanly, offer the M1 target upstream.
    The squash-and-split note in [m1plus-integration.md](m1plus-integration.md#decision-finish-on-this-tree)
    covers its history.
- **Latent Q2 bugs found through M1.** Each was fixed only for M1 (behind `M1PLUS`, or a name with
  each model's value), to keep the Q2 build byte-identical (ground rules). Fixing them on the Q2 is a
  deliberate Q2 change, best made upstream, with a Q2 device check:
  - Edit Playlist's Move Up and Move Down always fail with "Could not save playlist": `ple_mutate`'s
    temporary id is a HAVING with no GROUP BY, which both firmwares' SQLite 3.19.3 refuses. The M1's
    `PLE_TEMP_ID_SQL` is a CASE instead ([m1plus-progress.md](m1plus-progress.md) section 47). The draft
    pull request [DiamondBond/q2-pod#107](https://github.com/DiamondBond/q2-pod/pull/107) has the same
    CASE (`fix/playlist-move-sqlite319`, off upstream `main`); the seam goes at the sync after it lands;
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
- **A card library in the emulator.** `test/m1plus/boot.py --media` mounts a small card on a tmpfs: two long
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

**Done (Oct 25,** [m1plus-progress.md](m1plus-progress.md) **section 46),** with the knob on Home: the
`page_list` pages' rows, the Streaming icons and Now Playing's info lines. Coverflow's touch works as
designed on the device; its feel is the user's call. Left:
- **Coverflow's back arrow** overlaps the left cover at the top left.
- **The selection frame on V2.1's pickers** (Theme, Screen Rotation) reaches into the scroll bar.

The items as recorded:

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
- Quick Settings' brightness/volume switch on a Play/Pause hold (1.3.8): the M1's knob stays volume
  in Quick Settings, which Knob: Navigation leaves to stock (the user's choice, Oct 25).

The Rockbox dual boot stays: there is no Rockbox for the M1 Plus yet, but the hook serves as a boot-time
diagnostic.
