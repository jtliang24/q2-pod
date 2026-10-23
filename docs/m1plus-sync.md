# Syncing with upstream

How to bring one upstream Q2 Pod release (DiamondBond/q2-pod) into `feature/m1plus-port`. Why the branch
works this way, and what has to be in place first, is in the roadmap's section U
([m1plus-roadmap.md](m1plus-roadmap.md#u-tracking-upstream)). The Q2 rule a sync must keep is in
[m1plus-integration.md](m1plus-integration.md#rule-for-future-work-dont-break-q2).

This runbook assumes U1 and U2 are done: the M1 code sits in `tools/m1plus.py`, `patch/m1plus/` and
`test/m1plus/`, and `test/q2compare.py`, `UPSTREAM_BASE` and the port report exist. Until then, a merge
hits the conflicts measured in section U.

## Once

```sh
git remote add upstream https://github.com/DiamondBond/q2-pod.git
```

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
     the M1 it is `NOT PORTED` until it has V2.1 words in `tools/m1plus.py` (the port report lists it).
   - **Upstream's other changes to `build()`**, those not at a V1.32 address (a new asset, helper, input
     or packing step): review `git diff <old base> <tag> -- tools/build.py`, and port each into
     `m1plus.build()` or give it a U4 row. The M1's pipeline doesn't take them by itself.
   - **A new `offsets.inc` name** gets a V2.1 value in `patch/m1plus/offsets.inc`, found in V2.1's code
     by the roadmap's ground rules, or `M1_UNPORTED`, which compiles its feature out on M1. The M1
     compile fails until each new name has one or the other.
   - **A test conflict** keeps upstream's case as upstream wrote it. Its M1 path, if any, goes in
     `test/m1plus/`.
   - **A conflict in a doc** takes upstream's text. The M1 docs are the `m1plus-*.md` files.
3. **Gates, in order.**
   1. **Q2 output.** `python3 test/q2compare.py <tag>`: Legacy and iPod `update.tar` byte-identical to
      `<tag>`'s own build.
   2. **Q2 suites.** The tag's suites on both Q2 builds, as in
      [the checklist](m1plus-integration.md#checklist): no case dropped or skipped.
   3. **M1 gates.** The V2.1 name check, `test/build.py --build`, `test/patch.py` and `test/boot.py` on a
      fresh M1 build.
   4. **Port report.** Every new hook, site and name is classified (ported, native in V2.1, Q2 only, or
      `NOT PORTED`).
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

Before the first sync, `<UPSTREAM_BASE>` is `main`, whose M1 docs are the fork's and are left out.

Each changed line in an upstream file is a possible conflict in the next sync, so this number should
stay flat or fall.

| After | Upstream base | Lines changed in upstream's files |
|---|---|---|
| Before U1 (Oct 22) | 1.2.2 (`c0a2d6b`, through `main`) | +6,417/−2,036 over 38 files |
| U1a's `build.py` split (Oct 22) | 1.2.2 (`c0a2d6b`, through `main`) | +5,767/−1,765 over 38 files; `tools/build.py` +10/−4 |
