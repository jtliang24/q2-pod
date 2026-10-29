# Syncing with upstream

How to bring one upstream Q2 Pod release (DiamondBond/q2-pod) into `staging`, where the next M1
release is made (`main` is the last one). It was `feature/m1plus-port` until Oct 26, as the progress log
still calls it. Why the branch works this way, and what has to be in place first, is in the roadmap's section U
([m1plus-roadmap.md](m1plus-roadmap.md#u-tracking-upstream)). The Q2 rule a sync must keep is in
[m1plus-integration.md](m1plus-integration.md#rule-for-future-work-dont-break-q2).

The M1 code sits in `tools/m1plus.py`, `patch/m1plus_*` and `test/m1plus/` (U1). These tools check a
sync (U2):
- `UPSTREAM_BASE`, at the repo's root, names the upstream tag or commit the branch is level with;
- `test/q2compare.py` builds it and this tree, Legacy and iPod, and requires byte-identical `update.tar`;
- `test/m1plus/ports.py`, the port report, classifies every Q2 hook, call site and `offsets.inc` name for
  M1. It fails on any it can't place;
- `test/m1plus/q2only.py` lists the tag's changes inside Q2-only branches, whose M1 side the merge
  leaves as it was;
- `test/m1plus/fndiff.py` lists the payload functions two M1 builds differ in, for the device checklist;
- `test/m1plus/suitemerge.py` brings a tag's new test cases into an M1 suite copy;
- `test/m1plus/drift.py` measures upstream's drift past `UPSTREAM_BASE` and plans the next merge by the
  [cadence](#cadence).

## Once

```sh
git remote add upstream https://github.com/DiamondBond/q2-pod.git
```

`test/q2compare.py` builds upstream's trees, whose `tools/build.py` takes only the vendor ZIP
(`Q2 Firmware V1.32.zip`). It is at `stock/Q2 Firmware V1.32.zip`, beside `stock/M1 Plus Firmware V2.1.zip`; `--zip`
takes another path.

## Cadence

Upstream tags several patch releases a day: 1.4.2 to 1.4.9 took three days, 111 commits. A minor
version doesn't mark a size or a risk (1.3.9, a patch release, moved the payload's scratch state), so
merges follow the drift, and releases the calendar. The user chose this on Oct 26.

- **Merge** about every 100 commits, two or three times a week. `python3 test/m1plus/drift.py --fetch`
  says whether a merge is due and to which tag. A merge is due when the drift to the newest settled tag
  reaches 100 commits or 2,000 conflict-surface lines, when a structural change has come, or 14 days
  after the base's tag. The surface is the lines upstream changed in its files that the M1 also changes
  (the [footprint](#footprint)'s files, but `README.md`): those are where conflicts come from. A
  change to an upstream file the M1 doesn't touch merges by itself.
- **Merge settled tags.** A tag is settled 12 hours after it, if no tag followed it sooner. A tag
  followed within 12 hours is superseded: upstream fixed it fast (1.4.0, 1.4.1 and 1.4.2 came the same
  day).
- **A step** goes to the furthest settled tag within 150 commits and 3,000 surface lines: a little past
  the trigger, so it doesn't leave a stub behind. Each step is a full pass of [the runbook
  below](#each-release) up to landing (steps 1–4 and 6), with no feature ports. It is gated and its
  `--dev` build kept in `work/sync/<tag>/`. It isn't flashed.
- **A merge past due**, more than one step to the newest settled tag, leapfrogs: `drift.py` lists the
  steps, and each lands before the next starts. U3 did this by hand (1.2.9 → 1.3.0 → 1.3.8 → 1.3.9 →
  1.4.2); `drift.py` over a 1.2.2 base plans nearly the same.
- **A structural change** gets a step of its own, flashed once it is gated: the memory layout
  (`patch/link.ld`: each scratch move so far, 1.3.9's among them) or the toolchain (`flake.nix`,
  `flake.lock`). The step before it stops at the last settled tag ahead of it. A change reverted
  before its step ends isn't one.
- **Release** about weekly, from the last landed step, never from upstream's head: port the U4 rows
  whose upstream code didn't change across the last two merges, then one `--dev` build and device pass
  ([step 5](#each-release), the function diff against the build on the device), then
  `<tag>-m1.1` (step 7). A dev build that passed on the device with nothing landed since counts as the
  week's pass. Skip a week when nothing that reaches the M1 has landed.

`TRIGGER`, `LIMIT`, `SETTLE`, `MAX_DAYS` and `STRUCTURAL` at the top of `drift.py` hold these numbers.

## Each release

Run these in `nix develop`. `<tag>` is the upstream release tag, for example `1.3.9`. A merge step of
the [cadence](#cadence) runs steps 1–4 and 6; the device pass (5) and release (7) come at the weekly
release, or at once after a structural step.

1. **Merge.**

   ```sh
   git fetch upstream --tags
   git switch -c sync/<tag> staging
   git merge <tag>
   ```

   Merge the tag; don't rebase. [m1plus-progress.md](m1plus-progress.md) cites the branch's commit
   hashes, and a merge commit records which release the branch took. The merge commit resolves only
   conflicts. The M1 follow-ups below are commits after it, so the M1 build may fail at the merge itself
   (the 1.2.2 pilot's did).
2. **Resolve conflicts by these rules.**
   - **Upstream's side wins in upstream's files.** Take upstream's text, then put back only the seam
     lines: an `#include` of an M1 file, an `#if M1PLUS` / `#if !M1PLUS` wrapper, a `STYLE_*`-style
     name for a literal, `build.py`'s hand-off to `m1plus`. Any other M1 line
     in the conflict belongs in an M1 file.
   - **A new upstream hook or call site** needs nothing for the Q2: `tools/build.py` is upstream's. For
     the M1, it gets V2.1 words in `tools/m1plus.py` (`M1PLUS_HOOKS`, `CALL_SITES['m1plus']`), or a row in
     `M1PLUS_PORTS` saying why not: `native`, `q2only`, or `unported` (a U4 row). The port report fails
     until it has one or the other. Its trampoline is stubbed on M1 by itself, so its payload links
     either way. A new site also goes into `CALL_SITES['q2']`, the copy of build.py's sites the
     report reads; the report fails on a site constant `build()` patches that the copy lacks.
   - **A new stock routine in `FUNCTIONS`** that shared code calls fails the M1 compile if V2.1 has no
     symbol of that name. Find V2.1's by its callers (V1.32's `folder_reset_variable` is V2.1's
     `clear_foldervariate`, called at the same place in `folder_back`), alias it in
     `M1PLUS_FUNCTION_ALIASES` and pin the call in `test/m1plus/build.py`. A new `GLOBALS` name likewise
     goes in `M1PLUS_GLOBAL_ALIASES` (`g_time_zone` is `time_zone`). A routine only an unported hook's
     code calls can wait in `M1PLUS_UNRESOLVED` (1.3.8's `fwupdate_tf`, Network Update's): declared with
     no address, so the page compiles and `--gc-sections` drops it; the link fails if live code reaches
     it. A new `CONTEXT_DATA` name V2.1 lacks becomes a zero stub by itself: check what reads it.
   - **Upstream's other changes to `build()`**, those not at a V1.32 address (a new asset, helper, input
     or packing step): review `git diff <old base> <tag> -- tools/build.py`, and port each into
     `m1plus.build()` or give it a U4 row. The M1's pipeline doesn't take them by itself. The same
     goes for `tools/peq.py`, the player patch: `m1plus.PLAYER_PROFILE` takes none of its new words
     (1.2.9's MQA side chain), and for a new `#define` the M1 compile needs from build.py's header
     (1.2.9's `EXTRA_TIMEZONE_NAMES`, 1.3.8's `Q2POD_TAG` and `Q2POD_UA`). `m1plus.compile_common`
     copies `peq.py`'s list of payload sources and its `memcpy`/`memset` aliases: a new source (1.3.8's
     `upnext.c`, `chapters.c`, `netupdate.c`, `onlinematch.c`) fails the M1 link until it is listed. A
     rootfs file `build()` now patches (1.3.8's `bluealsa2`) goes in the M1's swap list and
     `test/m1plus/build.py`'s `replaced`.
   - **A new `offsets.inc` name** gets a V2.1 value in `patch/m1plus_offsets.inc`, found in V2.1's code
     by the roadmap's ground rules, or `M1_UNPORTED` (defined at the top of that file). `M1_UNPORTED` is
     only for a name whose code can't run on M1, because the hook or site that reaches it is unported.
     The M1 compile fails until each new name has one or the other. A name only Q2 code uses needs
     neither. A changed value counts too: `patch/m1plus_offsets.inc` copies upstream's tunables, so
     `git diff <old base> <tag> -- patch/offsets.inc` shows each `-#define` to follow there or rule out
     (1.2.9's `RESUME_SLOTS` 32 to 512). Nothing fails on a missed one.
   - **A seam must survive upstream's host tests.** `test/peq.py` and `test/coverflow.py` compile
     shared C on the host after cutting it by text; 1.2.9's strips every `#endif` from `tidal.c`, which
     left an M1 `#if`/`#else` open. Prefer a name with each model's value over an `#if` in such a file.
   - **A new upstream static function that only Q2 code calls** fails the M1 compile as unused
     (`-Werror`). Name it from the M1 file that stands in for its caller, with why, as
     `m1plus_nav_library.c` names `tidal_downloads`. Don't wrap upstream's function in `#if`.
   - **Upstream's changes to Q2-only code.** The merge takes them in an `#if !M1PLUS` branch (or the
     `#else` of `#if M1PLUS`) and leaves its M1 side, often a `patch/m1plus_*` file it includes, as it
     was. `python3 test/m1plus/q2only.py <tag>` lists each line the tag added in such a branch: make the
     same change on the M1 side, or rule it out. The 1.2.2 pilot missed one, `navigation.c`'s key-up
     taking `media_focused()`, which `m1plus_nav_keyup.inc` didn't until dev 21's device pass.
   - **A style, view or icon named by a string in shared C** uses its `STYLE_*`, `VIEW_*` or `ICON_*`
     name (`patch/m1plus_q2.inc` has the Q2's, `patch/m1plus_offsets.inc` V2.1's), adding one for a new
     string. On M1 the Q2's string is a style V2.1's theme lacks, and the widget stays unstyled: 1.2.2's
     Coverflow tracks came out grey and left-aligned on dev 21. `test/m1plus/patch.py` fails on a style
     the payload sets that V2.1's theme lacks; nothing checks views and icons.
   - **A Q2 image or screen size in new shared C** reaches the M1 with no conflict. Review the tag's
     added lines that the M1 runs, `git diff <old base> <tag> -- 'patch/*.c' | grep '^+'`, for quoted
     image names and the Q2's sizes (375, 320, 335, 302, 290): name each with each model's value
     (`UI_W`, `BOTTOM`, an `ICON_*`), or give the M1 its own function where V2.1 lays it out
     differently. 1.4.5's `list_toggle` named `switch_on` and sized its switch from a row height a
     V2.1 row only gets from its list, so the M1's rows showed no state; its `coverflow_goto_album`
     made a 375x290 body.
   - **Upstream's changes to a function an M1 file stands in for.** The merge takes them into the
     Q2's function and leaves the M1's file as it was, and `q2only.py` sees only `#if` branches. Read
     the tag's diff of each: `m1plus_nav_library.c` (the Q2 Pod page, for `ringnav_localmusic` and
     `stream_page_init`'s rows), `m1plus_nav_rows.c` (`list_row_core`), `m1plus_coverflow_rows.c`
     (`page_row_detail`, `row_into`), `m1plus_nav_goto.c` (`qm_goto`). 1.4.5's Library gave its rows
     that open a page a chevron; the Q2 Pod page followed by hand.
   - **A V1.32 number in shared C**: a load class, or a stock address called directly. Nothing fails on
     one. List the tag's hex literals with `git diff <old base> <tag> -- 'patch/*.c' | grep '^+' | grep
     -E '0x[0-9a-f]{4,}'`, and check each against V2.1's `demo` (`llvm-objdump -d` on the gated build's
     `stock-demo`). 1.3.0's artist albums took V1.32's `0xff11` where V2.1 loads `0xff01`; 1.3.9's
     Frequent and Recent (`0xf008`, `0xf007`) are V2.1's too (`guide_page_init`). An address goes in
     `offsets.inc` before its code runs on M1; until then the hook or site that reaches it stays
     unported (1.3.9's `ringnav_lyric_rows`).
   - **A test conflict** keeps upstream's case as upstream wrote it. Its M1 path, if any, goes in
     `test/m1plus/`. `test/m1plus/boot.py`'s walks tap screen positions: an upstream row added above
     one they tap moves it (1.4.5's Coverflow Sort and Refresh pushed Knob: Navigation off Display's
     screen).
   - **Upstream's new test cases**, conflict or not: review `git diff <old base> <tag> -- test/`. The
     M1's copies in `test/m1plus/` don't take them. Merge each copy with `python3
     test/m1plus/suitemerge.py <old base> <tag> <suite>`. It places each upstream hunk by its lines'
     text, at the copy's indentation, so a section the copy guards (and indents) takes upstream's
     changes too; `git merge-file --diff3` made 16 conflicts of 1.3.8's `patch.py`, `suitemerge.py` 9
     hunks to merge by hand. It prints those: a hunk whose lines the M1 copy changed or moved. Keep the
     M1 side there and bring in upstream's new cases and changed expectations; upstream's equivalent
     rewrites (`jal()`, `self.returns()`) can stay out. New cases land unguarded where upstream put
     them: the suite run on M1 names those that need a guard. A case for code the M1 doesn't run, or one that needs V1.32 code,
     goes behind its hook or site (`if 'NAME' in HOOKS`) with a `not_ported` line. Then run the copies
     on a fresh M1 build: they find the rest.
   - **A conflict in a doc** takes upstream's text. The M1 docs are the `m1plus-*.md` files. `README.md`
     is the fork's own front page, so its conflicts keep ours; read upstream's changes to it for
     anything the M1 section should say. An upstream PR of the port takes upstream's README back.
3. **Gates, in order.**
   1. **Q2 output and suites.** `TMPDIR=/tmp python3 test/q2compare.py <tag> --suites`, inside the
      shell: `nix develop` sets its own `TMPDIR` over one set outside it. Under that long `TMPDIR`,
      1.2.9's `test/peq.py` fails its Tidal check on `-Wformat-truncation`, upstream's own tree too.
      1.3.8's `test/chapters.py` runs `/usr/bin/ffmpeg`, which NixOS lacks; bind one in with
      bubblewrap: `F=$(nix build --inputs-from . nixpkgs#ffmpeg-headless --no-link --print-out-paths |
      head -1)/bin/ffmpeg; bwrap --dev-bind / / --tmpfs /usr/bin --ro-bind $F /usr/bin/ffmpeg
      --ro-bind /usr/bin/env /usr/bin/env sh -c 'TMPDIR=/tmp python3 test/q2compare.py <tag> --suites'`. Legacy and iPod `update.tar`
      must be byte-identical to `<tag>`'s own build, and the tag's suites must pass on both
      ([the checklist](m1plus-integration.md#checklist)). It fails on a suite the tag adds that it
      doesn't know how to run (`SUITES`), and names the suites whose text differs from the tag's.
   2. **Q2 scenario counts.** `test/patch.py`'s counts are at least the tag's own: no case dropped or
      skipped.
   3. **M1 gates.** The V2.1 name check (the M1 build itself: `m1plus_names` fails on a V2.1 name the rootfs lacks),
      then on a fresh M1 build the suites of [How to check a build
      now](m1plus-progress.md#how-to-check-a-build-now): `test/m1plus/build.py --build`,
      `test/m1plus/patch.py`, `test/m1plus/boot.py` with and without `--home-menu` and `--media`,
      `test/m1plus/playback.py`, `m4b`, `id3`, `headset_io`, `test/ldac.py` and `test/bluealsa.py`.
      Edit no source between the build and its gates: they check its `source_sha256` against the
      tree, and a table edit after the build fails every one. A failing gate is fixed in a follow-up
      commit. A fix to tests alone keeps the build: run the failed gate and those after it on it. A
      fix to a hashed source (`tools/*.py`, `patch/*`) needs a fresh build and every M1 gate again.
   4. **Port report.** `python3 test/m1plus/ports.py` passes: every hook, site and name is classified
      (ported, native in V2.1, Q2 only, or `NOT PORTED`). `--unported` prints the rows for
      [m1plus-unported.md](m1plus-unported.md).
   5. **What changed on M1.** Keep the gated `--dev` build (`work/sync/<tag>/`; U3's are in
      `work/u3/<tag>/`), and list
      `python3 test/m1plus/fndiff.py <the last flashed build> <this build>`: the payload functions the
      device checklist covers.
4. **Record.**
   - Set `UPSTREAM_BASE` to `<tag>` and its commit.
   - Add a row to [m1plus-unported.md](m1plus-unported.md) (roadmap U4) for each new `NOT PORTED`
     feature, with its status.
   - Add the footprint to the [table below](#footprint).
   - Add a section to [m1plus-progress.md](m1plus-progress.md) naming the tag, the conflicts and how
     each was resolved.
5. **Device pass.** Flash a `--dev` M1 build through the menu updater and run the checklist of features
   the sync touched, over q2remote where it can reach them. Stay on the build afterwards; the menu
   updater with stock `update.bin` is only for a catastrophic error (a boot loop, demo crashing at
   start, dead touch input). Keep the screen awake for touch checks: touch still works on a dark
   screen, but the hold menu and other gated input refuse it. Set System Setting → Display setting →
   Screen Off to Off for the pass (`[SYSSET] LIGHTTIME` 0), and put the user's value back after.
6. **Land.** Merge `sync/<tag>` into `staging` with `--no-ff`.
7. **Release.** Add a `- **<tag>-m1.1**:` entry to [m1plus-changelog.md](m1plus-changelog.md), then
   release by [m1plus-releasing.md](m1plus-releasing.md).

## Footprint

How much of upstream's own files the M1 changes, after U1 and after each sync:

```sh
git diff --stat <UPSTREAM_BASE> -- $(git ls-tree -r --name-only <UPSTREAM_BASE> | grep -v '^docs/m1plus\|^README.md$') | tail -1
```

`<UPSTREAM_BASE>` is the commit in `UPSTREAM_BASE`. Before the 1.2.2 pilot sync it was the fork point,
compared through `main`, whose M1 docs are the fork's and are left out. `README.md` is left out
since Oct 26, when it became the fork's front page.

Each changed line in an upstream file is a possible conflict in the next sync, so this number should
stay flat or fall.

| After | Upstream base | Lines changed in upstream's files |
|---|---|---|
| Before U1 (Oct 22) | 1.2.2 (`c0a2d6b`, through `main`) | +6,417/−2,036 over 38 files |
| U1a's `build.py` split (Oct 22) | 1.2.2 (`c0a2d6b`, through `main`) | +5,767/−1,765 over 38 files; `tools/build.py` +10/−4 |
| U1a done: `peq.py`, `ipod.py` upstream's (Oct 22) | 1.2.2 (`c0a2d6b`, through `main`) | +5,639/−1,729 over 36 files |
| U1b: `offsets.inc` split (Oct 22) | 1.2.2 (`c0a2d6b`, through `main`) | +5,172/−1,696 over 36 files; `patch/offsets.inc` +5/−0 |
| U1c: the M1 blocks out of `patch/*.c` (Oct 22) | 1.2.2 (`c0a2d6b`, through `main`) | +4,368/−1,665 over 36 files; `patch/` +671/−226 |
| After U1 (U1d: the M1 suites in `test/m1plus/`, Oct 23) | 1.2.2 (`c0a2d6b`, through `main`) | +1,417/−279 over 31 files |
| Pilot sync to 1.2.2 (U2, Oct 23) | 1.2.2 (`87e2417`) | +1,416/−278 over 30 files |
| Dev 21's fixes (Oct 23) | 1.2.2 (`87e2417`) | +1,417/−279 over 30 files: Coverflow's `STYLE_SCRLABEL_WHITE20C` |
| U3 step 1: sync to 1.2.9 (Oct 23) | 1.2.9 (`7116f34`) | +1,417/−283 over 30 files: `tidal.c`'s seam now one line (`TIDAL_ID_REG`) |
| U3 step 2: sync to 1.3.0 (Oct 23) | 1.3.0 (`92112b8`) | +1,420/−286 over 30 files |
| U3 step 3: sync to 1.3.8 (Oct 24) | 1.3.8 (`3744dac`) | +1,418/−285 over 30 files: `ringnav_input` and `library_music` lost a seam each |
| U3 step 4: sync to 1.3.9 (Oct 24) | 1.3.9 (`41844cc`) | +1,421/−285 over 30 files: the hold menu's `yslidable` (3 lines, `qm_open`) |
| U3 step 5: sync to 1.4.2 (Oct 24) | 1.4.2 (`7efbff5`) | +1,429/−287 over 30 files: MQA's icon name, the Apps row's `!M1PLUS`, `peq_boot` at `BOOT_MODE_RET` |
| The fork's README, left out (Oct 26) | 1.4.2 (`7efbff5`) | +1,468/−300 over 31 files: the polish and catch-up's seams since step 5; `README.md` had +7/−7 |
| Merge step: sync to 1.4.5 (Oct 26) | 1.4.5 (`6d50dc6`) | +1,494/−310 over 31 files: `list_toggle`'s `#if !M1PLUS`, the App Store's Rockbox rows, q2remote's `M1_GLOBALS` and its M1 rows in `remote.md` |
| Merge step: sync to 1.5.0 (Oct 27) | 1.5.0 (`d774d76`) | +1,474/−295 over 31 files: Display's sub-pages under `#if !M1PLUS`, Control Device Volume's row names, `SPOT_REFUSED_SUB`; the playlist editor's SQL seam gone |
| Five-feature batch (Oct 28; dev 13 device checks, manual exceptions recorded) | 1.5.0 (`d774d76`) | +1,485/−296 over 32 files: the CUE converter address and M1-only Streaming/Now Playing seams |
