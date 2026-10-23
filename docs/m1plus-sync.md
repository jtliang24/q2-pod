# Syncing with upstream

How to bring one upstream Q2 Pod release (DiamondBond/q2-pod) into `feature/m1plus-port`. Why the branch
works this way, and what has to be in place first, is in the roadmap's section U
([m1plus-roadmap.md](m1plus-roadmap.md#u-tracking-upstream)). The Q2 rule a sync must keep is in
[m1plus-integration.md](m1plus-integration.md#rule-for-future-work-dont-break-q2).

The M1 code sits in `tools/m1plus.py`, `patch/m1plus_*` and `test/m1plus/` (U1). Three tools check a
sync (U2):
- `UPSTREAM_BASE`, at the repo's root, names the upstream tag or commit the branch is level with;
- `test/q2compare.py` builds it and this tree, Legacy and iPod, and requires byte-identical `update.tar`;
- `test/m1plus/ports.py`, the port report, classifies every Q2 hook, call site and `offsets.inc` name for
  M1. It fails on any it can't place.

## Once

```sh
git remote add upstream https://github.com/DiamondBond/q2-pod.git
```

`test/q2compare.py` builds upstream's trees, whose `tools/build.py` takes only the vendor ZIP
(`Q2 Firmware V1.32.zip`). Put it at `stock/Q2 Firmware V1.32.zip`, or leave it in `~/Downloads/`, or pass
`--zip`.

## Each release

Run these in `nix develop`. `<tag>` is the upstream release tag, for example `1.3.9`.

1. **Merge.**

   ```sh
   git fetch upstream --tags
   git switch -c sync/<tag> feature/m1plus-port
   git merge <tag>
   ```

   Merge the tag; don't rebase. [m1plus-progress.md](m1plus-progress.md) cites the branch's commit
   hashes, and a merge commit records which release the branch took.
2. **Resolve conflicts by these rules.**
   - **Upstream's side wins in upstream's files.** Take upstream's text, then put back only the seam
     lines: a hook call or `M1_HOOK(...)`, a target lookup, an `#if !M1PLUS` wrapper. Any other M1 line
     in the conflict belongs in an M1 file.
   - **A new upstream hook or call site** needs nothing for the Q2: `tools/build.py` is upstream's. For
     the M1, it gets V2.1 words in `tools/m1plus.py` (`M1PLUS_HOOKS`, `CALL_SITES['m1plus']`), or a row in
     `M1PLUS_PORTS` saying why not: `native`, `q2only`, or `unported` (a U4 row). The port report fails
     until it has one or the other.
   - **Upstream's other changes to `build()`**, those not at a V1.32 address (a new asset, helper, input
     or packing step): review `git diff <old base> <tag> -- tools/build.py`, and port each into
     `m1plus.build()` or give it a U4 row. The M1's pipeline doesn't take them by itself.
   - **A new `offsets.inc` name** gets a V2.1 value in `patch/m1plus_offsets.inc`, found in V2.1's code
     by the roadmap's ground rules, or `M1_UNPORTED` (defined at the top of that file). `M1_UNPORTED` is
     only for a name whose code can't run on M1, because the hook or site that reaches it is unported.
     The M1 compile fails until each new name has one or the other. A name only Q2 code uses needs
     neither.
   - **A test conflict** keeps upstream's case as upstream wrote it. Its M1 path, if any, goes in
     `test/m1plus/`.
   - **Upstream's new test cases**, conflict or not: review `git diff <old base> <tag> -- test/`. The
     M1's copies in `test/m1plus/` don't take them. Port each case of shared code the M1 runs into its
     `test/m1plus/` copy, or mark it with `not_ported`.
   - **A conflict in a doc** takes upstream's text. The M1 docs are the `m1plus-*.md` files.
3. **Gates, in order.**
   1. **Q2 output and suites.** `python3 test/q2compare.py <tag> --suites`. Legacy and iPod `update.tar`
      must be byte-identical to `<tag>`'s own build, and the tag's suites must pass on both
      ([the checklist](m1plus-integration.md#checklist)). It fails on a suite the tag adds that it
      doesn't know how to run (`SUITES`), and names the suites whose text differs from the tag's.
   2. **Q2 scenario counts.** `test/patch.py`'s counts are at least the tag's own: no case dropped or
      skipped.
   3. **M1 gates.** The V2.1 name check, `test/m1plus/build.py --build`, `test/m1plus/patch.py` and
      `test/m1plus/boot.py` on a fresh M1 build.
   4. **Port report.** `python3 test/m1plus/ports.py` passes: every hook, site and name is classified
      (ported, native in V2.1, Q2 only, or `NOT PORTED`). `--unported` prints the rows for U4.
4. **Record.**
   - Set `UPSTREAM_BASE` to `<tag>` and its commit.
   - Add a row to the roadmap's U4 for each new `NOT PORTED` feature.
   - Add the footprint to the [table below](#footprint).
   - Add a section to [m1plus-progress.md](m1plus-progress.md) naming the tag, the conflicts and how
     each was resolved.
5. **Device pass.** Flash the M1 build through the menu updater, run the checklist of features the sync
   touched, then use the menu updater with stock `update.bin` to get back
   ([m1plus-roadmap.md](m1plus-roadmap.md), the loop at the top).
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
