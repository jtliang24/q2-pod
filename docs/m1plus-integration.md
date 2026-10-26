# One tree for Q2 and M1 Plus

What it takes for `staging` to build the Q2 Pod firmware exactly as upstream's release in
`UPSTREAM_BASE` does, and the M1 Plus firmware, from one `tools/build.py`. It also sets the rule that keeps it that way. What
the port has done is in [m1plus-progress.md](m1plus-progress.md), and what it still lacks on M1 is in
[m1plus-roadmap.md](m1plus-roadmap.md).

The fork point is `main` at `b229c24`: upstream `c0a2d6b` (Q2 Pod 1.2.2) plus three M1 doc commits, so its
Q2 code is 1.2.2's. The branch then follows upstream release by release
([m1plus-roadmap.md](m1plus-roadmap.md#u-tracking-upstream), [m1plus-sync.md](m1plus-sync.md)). Since
U2, the Q2 baseline below is the build of `UPSTREAM_BASE`, the file at the repo's root naming the
upstream tag or commit the branch is level with. Each sync moves it forward. It was `main`'s before
that.

Sizes are rough: **S** is a day or less, **M** a few days.

## Goal

`tools/build.py <input>` picks the target from the audited input's SHA-256 (`ZIP_SHA` and `Q2_TAR_SHA` in
`tools/build.py`, `INPUTS` in `tools/m1plus.py`):

- a Q2 V1.32 input (the vendor ZIP or its `update.tar`) gives `UPSTREAM_BASE`'s Q2 Pod, Legacy or iPod;
- an M1 Plus V2.1 input (the vendor ZIP or its `update.bin`) gives the M1 Plus build.

The dispatch works, and `test/q2compare.py` proves the Q2 output is `UPSTREAM_BASE`'s (R1 below).

## Requirements

- **R1. Q2 output is upstream's.** For Legacy and iPod, `update.tar` is byte-identical to the baseline's
  build with the same toolchain: `UPSTREAM_BASE`'s (`main`'s before U2).
- **R2. Q2 tests are upstream's.**
  - Every Q2 suite and case that the baseline has runs and passes on the branch's Q2 builds.
  - None is dropped, skipped or turned into an M1-only check. New Q2 cases are welcome.
- **R3. The Q2 release works.** `tools/release.py package` and `upload`, and `test/release.py`, work as on
  `main`: two builds per variant, byte comparison, the suites on each.
- **R4. M1 is unchanged.** The M1 build and its gates keep passing: the V2.1 name check,
  `test/m1plus/build.py --build`, `test/m1plus/patch.py` and `test/m1plus/boot.py`.
- **R5. The docs give both targets.** `building.md` and the README give both targets' commands, and say
  what ships for each device.

## Current status (measured 2026-10-23, at upstream 1.3.0, U3 step 2)

Measured with `TMPDIR=/tmp test/q2compare.py --suites` against `UPSTREAM_BASE` (1.3.0, `92112b8`), from
the vendor ZIP.

- **R1 is met.** Legacy and iPod `update.tar` are byte-identical to 1.3.0's build: `a89b5587…` and
  `3aa1e288…`.
- **R2 is met.** 1.3.0's 21 suite runs pass on this tree's builds: `build --build`, `patch` (Legacy 1116,
  iPod 1498 scenarios, 1.3.0's own), `playback`, `id3`, `m4b`, `headset_io`, `ldac` and `bluealsa` on
  each, and `peq`, `mp3`, `remote`, `coverflow` and `release` once.
- **R3 was last met on Oct 22, at the fork point.** `tools/release.py package 'stock/Q2 Firmware
  V1.32/update.tar'` built both variants twice, validated them, found each pair byte-identical and wrote
  both ZIPs and the user guide. The guide's build (`docs/manual/build.py`) needs `pdftotext`, then run with
  `nix shell nixpkgs#poppler-utils`; the devShell has it since `1f737de`. At 1.2.2, `test/release.py`
  passes (part of R2); the package step wasn't rerun.
- **R4 holds.** On a fresh M1 build, `test/m1plus/build.py --build`, `test/m1plus/patch.py` (1042
  scenarios, no `KNOWN GAP`, 21 `NOT PORTED`), `test/m1plus/boot.py` and `test/m1plus/ports.py` pass, and
  so do the M1's `playback`, `id3`, `m4b` and `headset_io` and the shared `ldac` and `bluealsa`. Dev 29
  (`V00Ts`, 1.2.9) is on the device; the next flash comes at 1.3.8.

Measured on Oct 22, after U0, `main` from the vendor ZIP and the branch from `stock/`'s `update.tar`: the
same byte-identity at the fork point (`8190e0c8…`, `48784f86…`), with the manifests differing in keys only
(`input_sha256` for `input_zip_sha256`, and the new `model` and `logo_source`; the manifest is not in
`update.tar`).

U0 closed items 1 and 3–9 below. The byte compare then found three more differences, which the
2026-10-18 measurement had not listed:
- **`ringnav_audioset`'s strings.** The branch had moved its body into a static `audioset_rows`, for
  V2.1's foreground rebuild. Q2 inlined it, so its code was the same, but a static function is generated
  after the others. Its strings moved in `.rodata`, and every string address after them shifted.
- **The EQ's tab split.** `tab_touch`'s `(TAB_LEFT + TAB_W + TAB_RIGHT) / 2` is 187 on Q2, where `main`
  has 188.
- **The AirPlay icon's mode.** Its rootfs entry copied its mode from `netservice_airplay.png` (0775),
  where `main` copies it from `list_tidal.png` (0664).

## Status before U0 (measured 2026-10-18)

### How it was measured

- **Builds.** Run in the `nix develop` shell, which has clang and LLD 21.1.8, squashfs-tools 4.7.5 and
  ImageMagick 7.1.2.
  - **The fork point:** exported with `git archive main`. It was built from the vendor ZIP, since `main` takes
    nothing else, and with `SOURCE_DATE_EPOCH` unset (see below).
  - **The branch:** built from `stock/Q2 Firmware V1.32/update.tar`, the git-ignored `stock/` inputs.
- **Comparisons.**
  - Component hashes, from each `manifest.json`.
  - Payload symbols, from `llvm-nm -S`.
  - A disassembly of every payload function, with addresses and immediates normalised so that layout shifts
    don't count.
  - Each suite on each build, with `main`'s suites on `main`'s builds as the control.

### Q2 output

**R1 is not met.** Both variants build, but their `update.tar` differs from `main`'s:

| | `main` | branch |
|---|---|---|
| Legacy `update.tar` | `8190e0c8…` | `fea21df2…` |
| iPod `update.tar` | `48784f86…` | `2e58a870…` |
| Legacy `patch.bin` | 236,408 bytes | 236,712 bytes |
| iPod `patch.bin` | 284,104 bytes | 284,456 bytes |

The branch's ZIP input and its bare-tar input give the same `update.tar`.

| Component | Same as `main`? | Cause |
|---|---|---|
| `hciplayer` (PEQ, ReplayGain) | yes | `PLAYER_PROFILES` keeps V1.32's addresses |
| `bluealsa`, kernel, `libtag_c`, font, UI assets, strings, logo | yes | |
| `demo` and `patch.bin` | no | the payload changes below |
| `q2boot` | no | `patch/boot.c:20` also takes `KEY_PLAYPAUSE` (164), M1's key, as the Rockbox key on Q2 |
| `q2video` | no | `patch/video.c:51` picks the screen at run time (`fb_h`) instead of at compile time. On Q2's 320x375 framebuffer it takes the same path |
| rootfs | no | it contains the files above |

The payload's strings match `main`'s exactly, so no style, widget or image name changed for Q2. Each code and
data difference has one of the causes below:

| Payload change | Effect on Q2 |
|---|---|
| **Legacy only:** five trampolines (`paint_bg`, `bigcover`, `color`, `image`, `playlist`) are `return 0` stubs. `compile_payload` resumes only `hooks(ipod)` (`tools/build.py:908`), where `main` resumed `HOOKS \| IPOD_HOOKS`, and fills the rest from `ALL_TRAMPOLINES` (`:914`) | None. All five are iPod hooks, and each is called only from its own hook's replacement, which Legacy doesn't install |
| `dispatch_key_return` (`patch/navigation.c:6296`) is compiled in, but its only caller is M1's `back_return` | None: dead code |
| `ringnav` reads `boot_guard` on entry on Q2 too (`:6574`). It ORs that into the Centre release check, beside the live reads `main` makes there (`:6681`) | **Possible.** Stock's key-up runs between the two reads and can clear `g_power_longkey`. When the guard was set on entry but cleared at the check, the branch cancels a Centre release that `main` lets through |
| `qm_open` closes the dialog if its back button or list is missing (`:5474`) | None on V1.32, whose sortselect dialog always has both |
| `xfade_open` checks two more widgets, and always calls `widget_set_enable(xf.view, 1)` (`patch/crossfade.c:171`) | Probably none: V1.32 isn't known to disable the view. It is still a new call on Q2 |
| `artist_tab` is factored out of `ringnav_artist_list` | None: the same steps, in the same order |
| `scratch_t` gains `knob_mode`, and `setting_label` grows from 5 to 6 entries (`patch/navigation.c:252`) | None: the state layout moves by 24 bytes (Legacy) or 8 (iPod) |
| **iPod only:** `arc_out` returns 0 when `r` is 0 (`patch/offsets.inc:263`) | None: Q2's `CORNER_R` is 80 |

The geometry and style macros evaluate to `main`'s literals on Q2. `UI_W - 65` is 310, and
`WM_KEY_SLEEP` is `KEY_CENTER`. They produce the same code.

### Q2 tests

**R2 is not met, because of one test bug.**

| Suite | `main` on `main`'s builds | branch on the branch's builds |
|---|---|---|
| `test/patch.py` | Legacy 1016, iPod 1397 scenarios pass | Legacy 1017 pass. **iPod crashes** at `test/patch.py:5906` |
| `test/playback.py` | **fails** at `:591` on both variants | passes on both |
| `test/build.py --build` | passes | passes: `main`'s checks, plus the boot scenarios on the built `S90play` and `S11logo` |
| `id3`, `m4b`, `headset_io`, `ldac`, `bluealsa` | pass | pass, with the same output |
| `peq`, `mp3`, `remote`, `coverflow`, `release` | pass | pass |

- **The iPod crash.** Commit `75bc4b3` added the module-level helper `def S(name)` (`test/patch.py:67`). The
  iPod section at `:5766` still rebinds `S = O['CONFIRM_SURFACE']`, so the next `S('s_listitem_black')`
  calls an int. With that local renamed in a scratch copy, the iPod run passes 1398 scenarios. So nothing
  else fails behind the crash.
- **`main`'s playback failure is `main`'s own.** Its test picks the hold menu's Shuffle by a fixed index
  (`m.pick(6)`). `68358fe` changed it to pick by label (`test/playback.py:621`), which passes. Count this as
  a fix, not as a Q2 difference.

### Q2 release

**R3 is not met.** `build.py` renamed the manifest key `input_zip_sha256` to `input_sha256`, but
`tools/release.py:51` still reads the old one. `validate()` raises `KeyError: 'input_zip_sha256'` on a branch
build, so `release.py package` fails after its first build.

### Nix and `SOURCE_DATE_EPOCH`

The devShell sets `SOURCE_DATE_EPOCH=315532800`. mksquashfs 4.7 refuses that together with the time options
the build passes ("SOURCE_DATE_EPOCH and command line options can't be used at the same time"). So
`main`'s `build.py` can't build in the devShell at all.

The branch first cleared the variable at import in `tools/build.py`. Since U1a the devShell's `shellHook`
unsets it (`flake.nix`), so `build.py` is upstream's there, and `main`'s builds in the devShell too. The
build then takes stock's times, as without Nix. This is an environment fix, and it changes no output.

## Decision: finish on this tree

Q2 support is finished on `staging`, not reimplemented on a fresh branch from `main`.

**Why not restart.**
- **The M1 work is large and proven.** It is about 5,000 lines, most of them V2.1 addresses, struct offsets
  and event numbers, each found by reading V2.1's code.
- **Its harnesses keep it correct:** `test/boot.py`, M1 support in `test/patch.py`, and
  `test/build.py --build` (since U1d, their M1 copies in `test/m1plus/`).
- **It has passed three device tests.**
- **A rewrite would re-derive all of it.** That brings back the risk the correction pass of 2026-10-16 paid
  for, and it would need fresh device tests.

**Why finishing here is small.** The measurement shows the Q2 side intact apart from the short list above.

**If a clean history matters later,** for example for an upstream PR, squash and re-split this branch into
logical commits. That is cheaper than redoing the work. The reasons stay in
[m1plus-progress.md](m1plus-progress.md), whose commit hashes would then need a mapping note.

## Work items

Each item ended with the same check: build Q2 Legacy and iPod, compare them with the baseline's (`main`'s
then; `UPSTREAM_BASE`'s now), and run the Q2 suites (see [Checklist](#checklist)). Then run the M1 gates for R4.

| # | Item | Fix | Size | For |
|---|---|---|---|---|
| 1 | The release key | `tools/release.py:51` reads `input_sha256`, and checks it against `ZIP_SHA` or `Q2_TAR_SHA`. `validate()` stays Q2-only. `test/release.py` covers the key | S | R3 |
| 2 | The iPod test crash | Rename the `S` local at `test/patch.py:5766` (and its uses through `:5867`) | S | R2 |
| 3 | Trampolines | Resume `HOOKS \| IPOD_HOOKS` for Q2, as `main` did. Emit `ALL_TRAMPOLINES` stubs only when `m1plus` | S | R1 |
| 4 | Dead M1 code in Q2 | Put `dispatch_key_return` under `#if M1PLUS` | S | R1 |
| 5 | `boot_guard` on Q2 | On Q2, keep `main`'s Centre check: no entry read, only the live reads. Keep the entry read for M1 only, where the knob's Power remap needs it | S | R1 |
| 6 | V2.1 defences that run on Q2 | Put `qm_open`'s missing-widget close, `xfade_open`'s extra checks and `widget_set_enable`, and `arc_out`'s zero radius under `#if M1PLUS`. That also puts back `main`'s `!r` path | S | R1 |
| 7 | `scratch_t` | Put `knob_mode` under `#if M1PLUS`, and size `setting_label` per model, with 5 on Q2 | S | R1 |
| 8 | Helpers | `compile_helper` already passes `-DM1PLUS=1` for M1. Choose `KEY_PLAYPAUSE` and `video.c`'s 480-line path by `#if M1PLUS`, not at run time | S | R1 |
| 9 | `ringnav_artist_list` | Restore `main`'s body under `#if !M1PLUS`. The difference is behaviour-neutral, but syncing needs exact equality: an accepted difference would show in every later compare | S | R1 |
| 10 | Docs | `building.md` gives both targets' commands and gates. The README stops pointing M1 users to a release `update.bin` until releases carry one | S | R5 |
| 11 | Per-target split (roadmap U1a) | The M1's tables and its own build pipeline move to `tools/m1plus.py`, and `build.py` hands it an M1 input: `build.py` is upstream's but for a few seam lines, so upstream's changes merge with few conflicts. (Planned as one `build()` reading a `Target` record; the separate pipeline re-indents none of upstream's lines.) | M | R1 |
| 12 | The compare as a script (roadmap U2) | A `test/q2compare.py` that builds the baseline (`main`, then `UPSTREAM_BASE`) from `git archive` and the working tree, and reports differing components. This turns the checklist into one command, and every sync runs it | S | R1 |

Items 1–10 are done: item 2 earlier, 1 and 3–9 as roadmap U0 (2026-10-22), with R1–R3 met (see
[Current status](#current-status-measured-2026-10-23-at-upstream-130-u3-step-2)), and 10 with the M1 release. `building.md`
gives both targets, and the README points M1 users to the `M1Plus.Firmware.*.zip` that
`tools/release_m1.py` makes ([m1plus-releasing.md](m1plus-releasing.md)). Items 11 and 12, which
syncing needs, are done too: 11 as roadmap U1 (2026-10-22), 12 as U2's `test/q2compare.py` (2026-10-23).

## Rule for future work: don't break Q2

From now on, no change on this branch may break Q2 support. That holds for M1 features, refactors, tooling
and tests alike.

- **Q2 output stays upstream's.** Q2 Legacy and iPod `update.tar` stay byte-identical to the baseline's
  build: `UPSTREAM_BASE`'s, checked by `test/q2compare.py`.
  - A change that alters Q2 bytes on purpose says so in its commit message, with the reason and the Q2 test
    that covers it.
  - Such a change belongs upstream: send it there, and let a sync bring it in. A Q2 change made only in
    the fork would differ from every later upstream build.
- **Q2 tests stay.**
  - Every Q2 suite and case keeps running and passing on Q2 builds.
  - An M1 port of a test adds an M1 path beside the Q2 one. It never replaces the Q2 one.
  - A new shared test helper must not clash with names a Q2 section already uses. The crash above came from
    exactly that.
- **M1 code goes beside upstream's.**
  - New M1 code goes in an M1 file (`tools/m1plus.py`, `patch/m1plus_*`, `test/m1plus/`), joined to
    upstream's files only by seams ([m1plus-roadmap.md](m1plus-roadmap.md), the ground rules).
  - Shared code changes only through names whose Q2 values are upstream's (`patch/m1plus_q2.inc`).
  - Trust the byte compare, not a reading of the source. U0 found a macro that was meant to give
    `main`'s literal and was off by one, and a body factored into a static function: on Q2 it was
    inlined, but its strings still moved in `.rodata`.
  - A defensive check that only V2.1 needs is M1-only too.
- **The Q2 release works.** `release.py package` keeps working.
- **Check both before each commit:** the Q2 compare and the Q2 suites, then the M1 gates.

## Checklist

Run these in `nix develop`. `<scratch>` is any fresh directory, and the build commands refuse an existing
output directory. `test/q2compare.py` needs the vendor ZIP, the only input upstream's `tools/build.py`
takes: it takes `stock/Q2 Firmware V1.32.zip`, or `--zip`.

```sh
# R1–R3: Legacy and iPod update.tar byte-identical to UPSTREAM_BASE's build, then the base's suites on
# this tree's builds (build --build, patch, playback, id3, m4b, headset_io, ldac, bluealsa on each;
# peq, mp3, remote, coverflow, release once). The base's builds are kept in work/q2compare/<commit>/.
python3 test/q2compare.py --suites

# R4: a fresh M1 build and its gates
python3 tools/build.py 'stock/M1 Plus Firmware V2.1/update.bin' --out <scratch>/m1
python3 test/m1plus/build.py --build <scratch>/m1
python3 test/m1plus/patch.py <scratch>/m1
python3 test/m1plus/boot.py <scratch>/m1
python3 test/m1plus/ports.py

# Before a Q2 release
python3 tools/release.py package 'stock/Q2 Firmware V1.32/update.tar' --out <scratch>/release
```

On a difference, `q2compare.py` names the differing `manifest.json` components and the first patch symbol
that moved; `--keep <scratch>` keeps this tree's snapshot and builds to look into. Without `--suites` it
only compares, in about a minute once the base is built.

`test/patch.py` ends with its scenario count, which must match or exceed the base's on Q2: 1029 (Legacy) and
1410 (iPod) at `1.2.2`. When a suite's exit status is captured in a script, read `$?` straight after the
command, never after a `$(…)` in the same line: the substitution resets it.
