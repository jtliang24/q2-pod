# Syncing with upstream

How to bring one upstream Q2 Pod release (DiamondBond/q2-pod) into `feature/m1plus-port`. Why the branch
works this way, and what has to be in place first, is in the roadmap's section U
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
- `test/m1plus/fndiff.py` lists the payload functions two M1 builds differ in, for the device checklist.

## Once

```sh
git remote add upstream https://github.com/DiamondBond/q2-pod.git
```

`test/q2compare.py` builds upstream's trees, whose `tools/build.py` takes only the vendor ZIP
(`Q2 Firmware V1.32.zip`). It is at `stock/Q2 Firmware V1.32.zip`, beside `stock/M1 Plus Firmware V2.1.zip`; `--zip`
takes another path.

## Each release

Run these in `nix develop`. `<tag>` is the upstream release tag, for example `1.3.9`.

1. **Merge.**

   ```sh
   git fetch upstream --tags
   git switch -c sync/<tag> feature/m1plus-port
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
     goes in `M1PLUS_GLOBAL_ALIASES` (`g_time_zone` is `time_zone`).
   - **Upstream's other changes to `build()`**, those not at a V1.32 address (a new asset, helper, input
     or packing step): review `git diff <old base> <tag> -- tools/build.py`, and port each into
     `m1plus.build()` or give it a U4 row. The M1's pipeline doesn't take them by itself. The same
     goes for `tools/peq.py`, the player patch: `m1plus.PLAYER_PROFILE` takes none of its new words
     (1.2.9's MQA side chain), and for a new `#define` the M1 compile needs from build.py's header
     (1.2.9's `EXTRA_TIMEZONE_NAMES`).
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
   - **A test conflict** keeps upstream's case as upstream wrote it. Its M1 path, if any, goes in
     `test/m1plus/`.
   - **Upstream's new test cases**, conflict or not: review `git diff <old base> <tag> -- test/`. The
     M1's copies in `test/m1plus/` don't take them. Merge each copy three ways, with the old base's
     suite as the base: `git merge-file --diff3 test/m1plus/<suite>.py <old base's test/<suite>.py>
     <tag's test/<suite>.py>` (1.2.9's `patch.py`: 43 conflicts, where `patch -p1` rejected 109 of 134
     hunks). In a conflict where the M1 copy restructured a section, keep the M1 side and bring in
     upstream's new cases and changed expectations; upstream's equivalent rewrites (`jal()`,
     `self.returns()`) can stay out. A case for code the M1 doesn't run, or one that needs V1.32 code,
     goes behind its hook or site (`if 'NAME' in HOOKS`) with a `not_ported` line. Then run the copies
     on a fresh M1 build: they find the rest.
   - **A conflict in a doc** takes upstream's text. The M1 docs are the `m1plus-*.md` files.
3. **Gates, in order.**
   1. **Q2 output and suites.** `TMPDIR=/tmp python3 test/q2compare.py <tag> --suites`. Under
      `nix develop`'s long `TMPDIR`, 1.2.9's `test/peq.py` fails its Tidal check on `-Wformat-truncation`,
      upstream's own tree too. Legacy and iPod `update.tar`
      must be byte-identical to `<tag>`'s own build, and the tag's suites must pass on both
      ([the checklist](m1plus-integration.md#checklist)). It fails on a suite the tag adds that it
      doesn't know how to run (`SUITES`), and names the suites whose text differs from the tag's.
   2. **Q2 scenario counts.** `test/patch.py`'s counts are at least the tag's own: no case dropped or
      skipped.
   3. **M1 gates.** The V2.1 name check (the M1 build itself: `m1plus_names` fails on a V2.1 name the rootfs lacks),
      `test/m1plus/build.py --build`, `test/m1plus/patch.py` and
      `test/m1plus/boot.py` on a fresh M1 build. Edit no source between the build and its gates: they
      check its `source_sha256` against the tree, and a table edit after the build fails every one.
   4. **Port report.** `python3 test/m1plus/ports.py` passes: every hook, site and name is classified
      (ported, native in V2.1, Q2 only, or `NOT PORTED`). `--unported` prints the rows for U4.
   5. **What changed on M1.** Keep the gated `--dev` build (U3: `work/u3/<tag>/`), and list
      `python3 test/m1plus/fndiff.py <the last flashed build> <this build>`: the payload functions the
      device checklist covers.
4. **Record.**
   - Set `UPSTREAM_BASE` to `<tag>` and its commit.
   - Add a row to the roadmap's U4 for each new `NOT PORTED` feature.
   - Add the footprint to the [table below](#footprint).
   - Add a section to [m1plus-progress.md](m1plus-progress.md) naming the tag, the conflicts and how
     each was resolved.
5. **Device pass.** Flash a `--dev` M1 build through the menu updater and run the checklist of features
   the sync touched, over q2remote where it can reach them. Stay on the build afterwards; the menu
   updater with stock `update.bin` is only for a catastrophic error (a boot loop, demo crashing at
   start, dead touch input). Keep the screen awake for touch checks: touch still works on a dark
   screen, but the hold menu and other gated input refuse it.
6. **Land.** Merge `sync/<tag>` into `feature/m1plus-port` with `--no-ff`.
7. **Release.** Add a `- **<tag>-m1.1**:` entry to [m1plus-changelog.md](m1plus-changelog.md), then
   release by [m1plus-releasing.md](m1plus-releasing.md).

## Footprint

How much of upstream's own files the M1 changes, after U1 and after each sync:

```sh
git diff --stat <UPSTREAM_BASE> -- $(git ls-tree -r --name-only <UPSTREAM_BASE> | grep -v '^docs/m1plus') | tail -1
```

`<UPSTREAM_BASE>` is the commit in `UPSTREAM_BASE`. Before the 1.2.2 pilot sync it was the fork point,
compared through `main`, whose M1 docs are the fork's and are left out.

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
