# Q2 Pod for the Shanling M1 Plus

<p align="center">
  An unofficial port of <a href="https://github.com/DiamondBond/q2-pod">Q2 Pod</a>, the firmware mod for the Shanling Q2, to the <b>Shanling M1 Plus</b>.<br>
  PEQ, Coverflow, ratings, lyrics, Spotify and more, built on top of the M1 Plus's stock firmware V2.1.
</p>

<p align="center">
  <a href="https://github.com/jtliang24/q2-pod/releases/latest"><img alt="Latest release" src="https://img.shields.io/github/v/release/jtliang24/q2-pod?style=flat-square&color=3D424B&label=release"></a>
  <a href="#features"><img alt="Device: Shanling M1 Plus" src="https://img.shields.io/badge/device-Shanling%20M1%20Plus-B99AC8?style=flat-square"></a>
  <a href="https://github.com/DiamondBond/q2-pod"><img alt="Upstream: Q2 Pod" src="https://img.shields.io/badge/upstream-Q2%20Pod-6E8BA8?style=flat-square"></a>
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-D77868?style=flat-square"></a>
</p>

<p align="center">
  <b><a href="https://github.com/jtliang24/q2-pod/releases/latest">Download</a></b> ·
  <b><a href="#install">Install</a></b> ·
  <b><a href="docs/m1plus-changelog.md">Changelog</a></b> ·
  <b><a href="docs/m1plus-unported.md">Not ported yet</a></b>
</p>

> [!NOTE]
> **Have a Shanling Q2?** This repository is the M1 Plus port. Get Q2 Pod for the Q2 from
> [DiamondBond/q2-pod](https://github.com/DiamondBond/q2-pod), and report M1 Plus problems
> [here](https://github.com/jtliang24/q2-pod/issues), not upstream.

## What it is

[Q2 Pod](https://github.com/DiamondBond/q2-pod) by DiamondBond patches the Shanling Q2's stock firmware.
The M1 Plus runs software from the same family (the same CPU, GUI toolkit, audio daemon and library database),
so this fork builds Q2 Pod's features into the M1 Plus's stock firmware V2.1.

The M1 Plus keeps **V2.1's own look**: its Home grid, settings and Now Playing. Q2 Pod's features are added to it,
most of them behind a **Q2 Pod** card on Home. The iPod interface isn't ported yet.

Each release carries an upstream Q2 Pod release and an M1 revision: `1.4.2-m1.1` is Q2 Pod 1.4.2's first M1 Plus build.
The fork follows upstream by merging each of its release tags.

## Features

- **The Q2 Pod card on Home:** Shuffle, Ratings, Most Played, Long Songs, Podcasts, Audiobooks, Photos, Books,
  Videos, Coverflow, Spotify, Internet Radio and AirPlay. Podcasts, Audiobooks, Photos, Books and Videos only show when their folder is on the card.
- **EQ:** the 30-band parametric EQ with a live curve, and Auto preamp for each sample rate.
- **Playback:** Crossfade, ReplayGain, gapless Shuffle Albums and Folders, a queue that survives a reboot, and View Queue.
- **Ratings:** rate songs and albums 0–5 hearts, then browse Top Rated, Loved and rated albums.
- **Playlists:** hold a playlist's row to add songs (with a search), move them and remove them.
- **Lyrics and covers:** lyrics from a track's tags, and lyrics and covers found online.
- **Podcasts and audiobooks:** `.m4b` audiobooks with chapters (including ones split by a CUE sheet), and podcasts resume where you stopped.
- **Streaming:** Spotify (Premium), Internet Radio and AirPlay. **System settings → Apps** installs Spotify, Deezer, Soulseek and File Browser over Wi-Fi.
- **Lock screen:** a large clock and wallpapers, built-in or your own.
- **Bluetooth:** LDAC HQ at 990 kbps, and Resume on Connect.
- **Battery:** Standby Limit powers the player off after a long Standby.

Not on the M1 Plus yet: the iPod UI, Network Update, Streaming's Configuration, Games and the extra time zones.
[m1plus-unported.md](docs/m1plus-unported.md) lists each one and whether it is planned.

## Install

**Requirements:** a Shanling M1 Plus on stock firmware V2.1 (or any build from this repository), a microSD card,
a USB-C cable and a computer.

> [!IMPORTANT]
> Charge the M1 Plus before you start, and back up anything on the card you can't lose.
> Flashing firmware carries risk.

1. **Download** `M1Plus.Firmware.<version>.zip` from the [latest release](https://github.com/jtliang24/q2-pod/releases/latest) and unzip it.
2. **Plug the M1 Plus into your computer** with the USB-C cable. The card shows up as a drive.
3. **Copy `update.bin`** to the **root** of the card (not inside a folder), then eject and unplug.
4. **Update:** open **System settings → System Update → TF card update**. Leave the card in until the player restarts.

## Using it

- **Touch** works as on stock. Every Q2 Pod page has V2.1's title-bar back button.
- **Long-press** a row to open the hold menu (Play/Pause's hold on the Q2): Go to Album and Artist, playlist and queue options, and ratings.
- **Display → Knob: Navigation** turns the volume knob into list navigation: turn to move, press to open, and Previous goes back.
  It works on Home's cards, the Q2 Pod pages and V2.1's settings pages.
- **Q2 Pod's settings** live in V2.1's own settings pages: its EQ page opens Q2 Pod's PEQ, and Crossfade and the lock screen have their rows there.

## Updating

Repeat the [install steps](#install) with the newest release. Your settings, ratings and play counts are kept.
The updater refuses the build that's already installed, so only a different one goes on.

## Restoring stock firmware

Put Shanling's V2.1 `update.bin` at the root of the card and run the same **TF card update**.

## For developers

The M1 Plus build sits beside upstream's Q2 build: `tools/build.py` hands M1 Plus input to `tools/m1plus.py`,
the M1 code lives in `patch/m1plus_*`, and its suites in `test/m1plus/`. The Q2 builds from this tree stay
byte-identical to upstream's.

- [Building](docs/building.md): `nix develop -c python3 tools/build.py "<M1 Plus Firmware V2.1.zip>" --out <fresh dir>`
- [The M1 Plus port](docs/m1plus.md): the hardware, the firmware's layout and how the port works
- [Syncing with upstream](docs/m1plus-sync.md) · [Releasing](docs/m1plus-releasing.md) · [Roadmap](docs/m1plus-roadmap.md) · [Unported features](docs/m1plus-unported.md) · [Progress log](docs/m1plus-progress.md)
- [Remote control (dev builds)](docs/remote.md) · [Internals](docs/internals.md)

## Credits and license

Q2 Pod is [DiamondBond](https://github.com/DiamondBond)'s work. This fork only ports it to the M1 Plus.
If it has made your player better, consider [supporting Q2 Pod on Ko-fi](https://ko-fi.com/diamondbond).

[MIT](LICENSE) covers this repository's code and docs. The Shanling firmware included in release images remains
Shanling's. Neither Q2 Pod nor this port is affiliated with Shanling.
