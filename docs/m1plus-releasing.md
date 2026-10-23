# Releasing for the M1 Plus

The Q2's release is upstream's ([releasing.md](releasing.md), `tools/release.py`). The M1 Plus's is this
fork's: `tools/release_m1.py` packages one M1 Plus `update.bin` and publishes it to
[jtliang24/q2-pod](https://github.com/jtliang24/q2-pod/releases).

## Names and tags

An M1 release carries an upstream release and an M1 revision: `<VERSION>-m1.<n>`, for example `1.2.2-m1.1`.
`VERSION` is upstream's (`tools/build.py`), and `n` counts the M1 releases of it from 1.

The updater needs a 5-character tag that differs from the installed one
([building.md](building.md#versioning)). An M1 release's tag is `V`, `VERSION`'s digits and `n`:
`1.2.2-m1.1` is `V1221`. Its last character is a digit, so it never equals a Q2 tag (`V122S`, `V122I`), a
`--dev` tag (`V00Ks`, lowercase last) or another release's. The updater takes each release over the last,
over stock and over a dev build. `n` is one digit, so an upstream release can have nine M1 releases.

About's **CFW. Version** row shows the name, and **FW. Version** the tag.

## Procedure

1. Add a `- **<VERSION>-m1.<n>**:` entry to the top of [m1plus-changelog.md](m1plus-changelog.md). Its
   text becomes the release notes: one bullet a sentence, or nested bullets as written. After a sync
   that changed `VERSION`, `n` starts again at 1.
2. Commit, then package in `nix develop`, from stock V2.1's `update.bin` (or the vendor ZIP):

   ```sh
   python3 tools/release_m1.py package 'stock/M1 Plus Firmware V2.1/update.bin' --out <fresh dir>
   python3 test/release_m1.py
   ```

   Packaging builds twice and compares `update.bin` and the ZIP byte for byte. It validates the first
   build: the manifest's model, release, tag, stock input and splash; the archive against V2.1's
   updater rule; then `peq`, `build --build`, `patch`, `boot`, `playback`, `m4b` and `ldac`. It writes
   `M1Plus.Firmware.<name>.zip` (`update.bin` and `manifest.json`), `SHA256SUMS`, `release-notes.md`
   and `release.json`. It uses no network.
3. Flash `m1plus/update.bin` from the output through the menu updater, run the device checklist, and
   stay on it: stock's `update.bin` is only for a catastrophic error (the roadmap's loop).
4. Upload a draft, check it on GitHub, then publish:

   ```sh
   python3 tools/release_m1.py upload <dir>
   python3 tools/release_m1.py upload <dir> --publish
   ```

   Upload checks the ZIP and sources against `release.json`, refuses a published release, downloads
   the asset again and compares it before `--publish` takes the draft live. A failure leaves the draft
   unpublished; run upload again to repair it.

The release notes end with the install steps and the way back to stock: Shanling's V2.1 `update.bin` at
the card root, then the same TF card update.
