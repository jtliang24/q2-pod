# M1 Plus five-feature validation, 2026-10-28

This batch starts from upstream 1.5.0 (`d774d764d4968b644ffdb0338b6cdcb5731ff568`) on
`staging`. It excludes MQA, kernel/MCU work, FLAC fast paths, Tidal caching/downloads,
Network Update and the iPod UI. Live Tidal start/change/stop remains pending without an account.

## Build

- Development image: `work/batch-five/dev13/update.bin`, version `V01Vs` (1.5.0 dev 13; global development tag 67).
- SHA-256: `1b2faa9dc92de792156288f7e2d9f0f6b8f7830e7e5168cc20a7964cb58fe4fc`.
- Payload: 368,856 bytes. Rootfs: 53,395,456 bytes, below stock's 55,738,368 bytes.
- Build source SHA-256: `bb035420d49007c587414bc7b1d90304e97813b0680a11159c60324c35ea5f4b`.
- The device before this pass matches `work/u3/1.4.2-catchup3`, `V01Cs` (1.4.2 dev 10),
  demo MD5 `0f3a6f6260f1d463d489650686d642af`.
- Function comparison with that flashed image: 236 changed, 109 added, 3 removed, of 1,006.
  Full list: `work/batch-five/function-diff-final.txt`.
- Footprint over upstream's files, excluding the fork's README and M1 docs: +1,485/−296,
  32 files. Shared changes are seams; the port implementations stay in M1 files.

## Native instruction evidence

| Port | V2.1 evidence |
|---|---|
| Hidden directories | `toolsLoadAllFile`'s recursive walk `0x5ea364`, first directory `strcmp` at `0x5ea6a8`, delay slot `0x24a53ed4` for `.` |
| Tags | `toolsFixId3ErrorCode` `0x5ec460`, round-trip `strcmp` at `0x5ec5e4` (`0x0320f809`) |
| CUE | Seven `bal toolsIconvConvert` calls at `0x5e72dc`, `0x5e73a0`, `0x5e7458`, `0x5e7514`, `0x5e77d4`, `0x5e7b90`, `0x5e7f18`, plus the native indirect call at `0x5e7de4`; named converter `0x5e39b0`, Q2's remains `0x5bccac` |
| Memory thread | `check_cpumem` `0x50b810`: open/write/sleep loop only; entry words `0x3c1c0050`, `0x279c86c0` become return NULL |
| Status/cover polling | Outer status sleep `0x5d1814`; cover sleeps `0x4dd4b4`, `0x4deef0`; all `0x0320f809` |
| Pause loop | hciplayer `0x42ff2c`: `0x24044e20` becomes `0x3404c350`, 20 ms to 50 ms |
| Tidal | Native launcher `0x512ed0`, worker `0x51c288`; thread creation `0x512fd0`, worker argument in delay slot `0x24c6c288` |
| External LRC | Private loader called by `mclLoadExLyric`: final `fopen` at `0x5d3bdc` (`0x0320f809`) |
| Options | `dialog_playmore_dialog_init` `0x479cc4`; native asset has seven 50 px rows, search at index 3; inserted action at index 4 |
| Lyric save | Accept's `snprintf` `0x537ca0`; format load `0x537c9c` (`0x24c61b90`) |
| Cover save | Accept's first native `toolsThumbSpecCover` call at `0x537b10`, preserving thumbnail refresh and return while saving its JPEG beside the song |

Streaming retains upstream's `Q2POD/STREAMHIDE` keys and `.tidal/.cache-size` /
`.spotify/.cache-size` files. Native Tidal's Home card has no switch; unavailable Tidal Downloads
has none. An initial scenario found an unnamed Q2 Pod scroll view, preventing immediate updates;
the view is now named, and the final build is rebuilt after that fix.

## Automated gates

The final build's logs and summaries are in `work/batch-five/gates13/`. All M1 gates are rerun
after the final hashed-source change; test-only corrections do not change the image.

| Gate | Result |
|---|---|
| Build/rootfs/instruction audit | Pass |
| MIPS payload scenarios | 1,351 pass; 0 known gaps; 21 unrelated checks not ported |
| Playback, M4B, ID3, headset I/O | Pass |
| LDAC and Bluetooth | Pass |
| Port report | 615 entries classified |
| Default and customized-Home boot walks | Pass |
| Media boot walk | Pass, including Era, Configuration and Back navigation |
| Q2 Legacy and iPod | Byte-identical to upstream 1.5.0 (`d9ece51c3547…`, `5936f7554a5e…`) |
| Q2 upstream suites | All 36 runs accounted for, including five failures reproduced in upstream's own tree |

Baseline exceptions remain explicit: `chapters`, `aic_build`, `flac_build`, `pwm_build` and
`rotator_build`. The harness reruns each failing host suite in the upstream tree and reports it
as `BASE`; it does not turn those failures into new passing tests.

## Combined device checklist

The final candidate is checksum-verified at `/mnt/mmc/update.bin` (MD5
`4065000ff9d466d1cb0e4719adb8bcf0`). The pre-batch image remains at
`/mnt/mmc/.q2/update-before-five-feature.bin`; dev 11 is separately preserved as
`update-five-feature-dev11.bin`. The user flashed through the menu updater. About reports 1.5.0 dev 13, and the running
`/release/bin/demo` MD5 is `8081b9d0cc9152228311e3fb5f5ca606`, matching the gated build.
No remote flash was started.

Device address: `192.168.1.210`. Original Screen Off is one minute (`LIGHTTIME=3`), restored through native settings
after temporarily using Off for touch checks. Original config and the 419-song database are backed up in
`work/batch-five/device/`. Temporary media in `/mnt/mmc/MusicLibrary/M1BatchValidation`
and `/mnt/mmc/.m1-batch-validation` were removed. The cleanup scan returned to 419 songs, with
exactly the original file-path set (`database-final.db`). Both originally absent cache-size
files and the temporary `STREAMHIDE` override were removed. Home menu, Bluetooth off and volume
20 match the original config; Coverflow sort is restored to Artist (`dev13-final-state.txt`).

Passed on dev 11:

- Menu updater flash, installed demo identity, Era touch and knob navigation, decade/album lists,
  two-song Play All and Shuffle queues, Coverflow and visible Back buttons.
- Library scan: 419 to 422 songs, Latin-1 title/artist preserved, hidden sentinel excluded.
- Streaming Configuration: cache cycles and on-card values, immediate Spotify/Radio/AirPlay
  visibility changes, reopening persistence, always-reachable Configuration, Stop Streaming
  Services with local playback continuing. Native Tidal remains on Home.
- External LRC millisecond order, word-stamp removal and blank-line cleanup. Album download
  progress and two saved LRC files; single lyric acceptance and JPEG saved beside the song,
  with native cover refresh. HTTPS cover search and LRCLIB both returned results.
- Go to Folder, Coverflow Sort/Refresh (Artist restored), PEQ simple/Advanced pages, video playback
  and paused-player exit after the timeout. Wi-Fi driver reports LPS mode MAX.

Device findings fixed and confirmed in dev 13:

- Configuration's unused lower area needed a black background. Native `toolsReadConfig` leaves
  an output buffer untouched for a missing key with an empty default, so the visibility parser
  now initializes its buffer; a poisoned-stack regression covers the first-open case.
- V2.1's CUE parser also uses an eighth indirect conversion at `0x5e7de4`. The seven-call port
  displayed CP1252 `Canção` as `Can玢o`. The additional native word is now pinned and redirected.
  Full native-parser tests cover CP1252, UTF-8 and GBK; the old-site control reproduces the fault.
  Native Folder and Now Playing now show `Canção` correctly (`dev13-native-folder.png`,
  `dev13-cue-playing.png`).

Final dev 13 checks:

- Configuration's black background, cache limits and Spotify-hidden state survived the flash.
  Restoring visibility updated the underlying page immediately. With `STREAMHIDE` absent,
  reopening showed clean defaults and both cache sizes at 2 GB (`dev13-missing-key.png`).
- Paused dark-screen samples are saved in `dev13-idle-dark-{1,2}.txt`. Wi-Fi stayed reachable,
  its driver reports LPS MAX, and screen off/wake/unlock worked. Bucket played across screen off
  and returned with its correct cover and advancing time (`dev13-playback-after-dark.png`).
  Playback was paused afterward. These are functional/activity checks, not battery-life measurements.
- App Store loaded its HTTPS catalog; no app was installed or erased. Spotify's browser and
  Liked Songs list loaded. The refusal note was not forced on the user's working account.

Bluetooth acceptance and remaining coverage limits:

- Physical Bluetooth/headset checks passed on dev 13, reported by the user after the local
  checklist for playback, volume, transport, screen-off/wake and reconnect. These were manual
  because enabling Bluetooth disconnects Wi-Fi.
- Earlier 1.4.5/1.5.0 checklist items still pending on hardware: playlist move up/down, app retry/stop
  and album sorting. Their automated coverage remains passing.
- Album-download cancellation was not conclusively exercised on hardware (the small test album
  completed first). Cancellation/failure/USB-storage shutdown, empty library and installed-app
  switch ordering are covered in emulation; no installed card app was available for a device check.

V2.1's Tidal URL worker is already on demand, so its native lifecycle is retained instead of
adding a semaphore to a nonexistent idle poller. Offline refusal and cancel/join/create/detach
ordering execute in emulation. Live Tidal start/change/stop remains pending without an account.
No controlled battery measurement is performed, and no battery-life improvement is claimed.
