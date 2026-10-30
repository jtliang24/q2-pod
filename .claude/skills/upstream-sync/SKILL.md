---
name: upstream-sync
description: Check whether an upstream Q2 Pod merge is due for the M1 Plus port and, if it is, catch up, leapfrogging in gated steps when it is past due. Use when the user asks to check upstream, catch up, sync or merge upstream tags, or asks whether the port is behind; also at the start of M1 port work when the last check is more than a day old.
---

# Upstream sync

The cadence (when to merge, which tag, how to step) is in `docs/m1plus-sync.md#cadence`; the per-merge
procedure is that doc's "Each release" runbook. This skill drives them. Read both sections before the
first step of a session; don't restate them here from memory.

## 1. Check

```sh
python3 test/m1plus/drift.py --fetch
```

Report its table's last lines and verdict to the user in a sentence or two.

- **Not due:** say so, with the drift to the newest tag, and stop.
- **Due or past due:** say the steps it lists (`1.4.2 → 1.4.5 → 1.4.8`) and why, then carry them out
  without asking again. These are local, reversible merges. Ask only when a conflict or follow-up isn't
  covered by the runbook's rules, or a choice is the user's (a feature's status, a fix that would
  change Q2 output).
- **Structural step:** the plan says `flash it`. Stop after that step lands (section 3).

The working tree must be clean and on `staging` before a step starts; if not, stop and ask.

## 2. Each step, `<old>` → `<tag>`

One step at a time; the next starts from the landed result of this one. Re-run `drift.py` (no
`--fetch`) after each landing: the plan can change as upstream tags settle.

1. **Backup:** `git update-ref refs/backup/pre-sync-<tag> staging`.
2. **Merge** (runbook step 1) on `sync/<tag>`. The merge commit resolves conflicts only, by the
   runbook's rules (step 2): upstream's side in upstream's files, M1 lines back as seams.
3. **Follow-ups**, each its own commit after the merge (runbook step 2's lists):
   - the M1 build compiles and links: new hooks, sites, `FUNCTIONS`, `offsets.inc` names, sources;
   - `python3 test/m1plus/q2only.py <tag> --base <old>`: each line made on the M1 side or ruled out;
   - `git diff <old> <tag> -- patch/offsets.inc tools/build.py tools/peq.py` and the hex-literal
     check, each item followed or ruled out;
   - the runbook's two checks no tool makes: Q2 image names and screen sizes in the tag's new shared
     C that the M1 runs, and upstream's changes to a function an M1 file stands in for (the Q2 Pod
     page, `list_row_core`, the page rows, `qm_goto`);
   - `python3 test/m1plus/suitemerge.py <old> <tag> <suite>` for each M1 suite copy upstream's suite
     changed in, then the hand hunks; run the copies on a fresh M1 build until they pass (a failure
     stops the run, so it takes several).
   No feature ports in a step: a new upstream feature gets a `NOT PORTED` row, and its suite cases
   a guard with a `not_ported` line.
4. **Gates** (runbook step 3), from the gate worktree `work/gatetree` so the main tree stays free:
   `git -C work/gatetree checkout --detach sync/<tag>`, then in it `nix develop`, Q2 first
   (`TMPDIR=/tmp python3 test/q2compare.py <tag> --suites`, with the ffmpeg bind the runbook gives),
   then a fresh `--dev` M1 build (`python3 tools/build.py 'stock/M1 Plus Firmware V2.1.zip' --dev --out
   <main tree>/work/sync/<tag>`: an absolute path, since the worktree's own `work/` is apart) and its gates (`docs/m1plus-progress.md`'s "How
   to check a build now": `test/m1plus/build.py --build`, `patch.py`, `boot.py` alone and with
   `--home-menu` and `--media`, `playback.py`, `m4b`, `id3`, `headset_io`, `test/ldac.py`,
   `test/bluealsa.py`), then `test/m1plus/ports.py`. The full run is about 30 minutes: run it in the
   background and don't edit hashed sources (`tools/*.py`, `patch/*`) of the tree it builds meanwhile.
   Stop at the first failure, so a fix doesn't wait on the rest.
   A failing gate is fixed in a follow-up commit on `sync/<tag>` (made in the main tree; the worktree
   checks it out). A fix to tests alone keeps the build: run the failed gate and those after it on
   it. A fix to a hashed source needs a fresh build and every M1 gate again.
5. **Function diff:** `python3 test/m1plus/fndiff.py <the build on the device> work/sync/<tag>/`.
   The build on the device is the `--dev` build of the newest device pass in `docs/m1plus-progress.md`
   (find its directory by the `version` in each `work/*/manifest.json`; on Oct 26, dev 10 in
   `work/u3/1.4.2-catchup3`). Keep its list for the next device pass's checklist (in the progress
   section).
6. **Record** (runbook step 4): `UPSTREAM_BASE`, `docs/m1plus-unported.md` rows, the footprint row,
   a `docs/m1plus-progress.md` section (the tag, conflicts and how each was resolved, the function
   diff). Commit them as one `docs(m1plus): record the merge step to upstream <tag>` commit, as
   earlier steps did.
7. **Land** (runbook step 6): `git switch staging && git merge --no-ff sync/<tag>`, then
   `graphify update .`. Re-run `drift.py`: a leapfrog's later steps may no longer be due once the
   base has moved (1.4.5's landing left 1.4.8 at 47 commits).

Don't push, and don't move `main`: it moves only at a release (`docs/m1plus-releasing.md`).

## 3. After the last step

Report: the steps landed, conflicts worth knowing, new `NOT PORTED` rows, the function-diff list, and
the drift left (the newest tag may not have settled yet).

Then say what's next, and leave it to the user:

- **A structural step** needs its device pass before more merges: flash `work/sync/<tag>/` as a `--dev`
  build and run the checklist. Follow the device-pass rules in memory (Screen Off for the pass and
  restored after, testing separate from fixing, staying on the test build).
- **The weekly release:** compare the last M1 release tag's date (`git log -1 --format=%cs
  <tag>-m1.<n>`) with today. If a week or more has passed and something that reaches the M1 has
  landed, say a release is due: the U4 ports whose upstream code held still across the last two
  merges, one device pass, then `<tag>-m1.1`. Releases need the user's go-ahead.
