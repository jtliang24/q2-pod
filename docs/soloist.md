# Spotify through Soloist (plan)

Status: a plan, not implemented (2026-10-25). It replaces librespot's playback with Spotify's own Soloist, run on a computer on the same Wi-Fi, and streams its audio to the device as PCM over TCP. Q2 Pod's firmware doesn't change: a relay on the card keeps librespot's contract ([librespot.md](librespot.md), [internals](internals.md#spotify)), so the Q2 and the M1 Plus both get it.

## Why

Spotify withholds librespot's audio keys from many accounts, mostly new ones: every track fails with `error audio key 0 1` in `.spotify/spot.log` (librespot-org/librespot#1649, DiamondBond/q2-pod#98). No client-side fix exists. [Spotify Soloist](https://developer.spotify.com/documentation/soloist), Spotify's official headless Connect client (August 2026), plays those accounts, but it needs ARMv7, AArch64 or x86_64 and PulseAudio or PipeWire, so it can't run on the X2000.

## What the first test showed (2026-10-25)

On a Linux laptop (NixOS, PipeWire 1.6.6), Soloist 1.3.9 logged in as the account librespot is refused keys for and played for 8 minutes with no key error. So the account problem is solved on the host; what's left is getting the audio and the controls to the device.

AirPlay was tried first and rejected:

- PipeWire's RAOP sink sent Soloist to the M1's stock receiver (`/usr/bin/shairport`, Shanling's Shairport 1.1.1, AirPlay 1). The M1 played 10, 17 and 24 s, then V2.1's AirPlay page went idle.
- A second Shairport run by hand with `-l` logged `player.c:161: alac_decode: Assertion 'outsize == FRAME_BYTES(frame_size)' failed`: Shairport 1.x aborts on any packet that isn't a whole 352-frame frame.
- The cause is PipeWire's. `module-rtp` keeps the audio in a 4 MiB ring (`BUFFER_SIZE`, 23.8 s at 44.1 kHz S16 stereo) and cuts packets from it with `set_iovec`, which splits a packet that straddles the ring's end into two iovecs. `module-raop-sink.c`'s `stream_send_packet` reads only the first (`n_frames = iov[1].iov_len / impl->stride`), so once a wrap it sends a short packet and drops the rest. The ring's start is random, so the first crash comes within 23.8 s. No property changes it. That is worth an upstream PipeWire fix, but this plan doesn't need it.

## Design

```
 host (Linux)                                              device (Q2 or M1 Plus)
 ┌──────────────────────────────────────────────┐          ┌──────────────────────────────────────┐
 │ Soloist ──PulseAudio── null sink q2_soloist   │          │ Q2 Pod (unchanged)                    │
 │   ▲ WebSocket 127.0.0.1    │ monitor (parec)  │          │   state file, control socket,         │
 │   │                        ▼                  │   TCP    │   browse socket, run, killall         │
 │ q2-soloist bridge ── PCM s16le 44.1k stereo ──┼────────► │      ▲                                │
 │   │   Web API (browse, search, covers)        │ ◄──────► │ .spotify/librespot = the relay        │
 │   └── control, state, Q2SPOT/1 ───────────────┼──────────┤      └─► aplay.sh (aplay / q2video -s) │
 └──────────────────────────────────────────────┘          └──────────────────────────────────────┘
```

Two programs, neither in the firmware:

- **The bridge** (host): runs Soloist, turns its WebSocket API and the Spotify Web API into what the relay needs, and sends the audio.
- **The relay** (card): installed as `.spotify/librespot` and started by `.spotify/run`, it does everything Q2 Pod expects librespot to do, over a TCP connection to the bridge instead of a Spotify session.

The relay takes librespot's file names because Q2 Pod finds the backend by them: `spot_launch` checks `SPOT_BIN` (`.spotify/librespot`) and runs `SPOT_RUN` (`.spotify/run`), and `spot_stop` and Home's Rockbox row stop it with the loop's pid in `/tmp/q2-librespot` and `killall -9 librespot aplay`.

## The relay (card)

It keeps the contract in [internals](internals.md#spotify), item by item:

- **Status file.** `/tmp/q2-librespot.state`, rewritten whole (`.tmp`, renamed) from the bridge's state: `state=` (`none`, `stopped`, `paused`, `playing`), `track=`, `title=`, `artist=` (joined by `, `), `album=`, `duration=`, `position=`, `at=`, and `cover=1` once `/tmp/q2-librespot.state.jpg` holds the bridge's cover for this track. `at=` is the relay's own `CLOCK_MONOTONIC` ms when the message came in; the bridge sends the position at its send time.
- **Control socket.** Binds `/tmp/q2-librespot.sock` (`AF_UNIX` datagrams) and forwards `p`, `P`, `s`, `n`, `b` and `S <ms>`. Binding it also answers `spot_alive`'s liveness check.
- **Browse socket.** Binds `/tmp/q2-librespot.browse.sock` and passes each Q2SPOT/1 request to the bridge unchanged, writing back its response. Without a bridge it answers `offline` itself, with "Can't reach the Spotify bridge" as the message.
- **Sink.** Like librespot's subprocess sink: on `playing` it starts `/bin/sh ./aplay.sh` and feeds it the PCM. On anything else it kills and reaps `aplay.sh` **before** it writes the new state, since `spot_yield` takes the state's leaving `playing` to mean the DAC is free. `aplay.sh` is kept unchanged, so `SPOT_OUT`, `q2video -s` and Bluetooth or USB output work as they do now. (Bluetooth and Wi-Fi exclude each other on the M1, so the M1 can't use Bluetooth output with this.)
- **Buffer.** A ring of about 1 s, filled before the sink starts, so a short Wi-Fi stall doesn't reach the DAC. The host's null sink and the device's DAC run on different clocks (up to about 0.2 s an hour apart), so above twice the target it drops a frame in every N, and when empty the sink just waits.
- **Bridge address.** `.spotify/remote` holds `HOST PORT TOKEN`. The relay connects, and keeps reconnecting with the run loop's backoff (5 s doubling to a minute), so the device's DHCP address never matters.
- **Never written:** `/tmp/q2-librespot.download`, since there are no downloads.

The device has no `nc` or `socat` (BusyBox has only `telnet` and `wget`, and `telnet` would rewrite `0xff` bytes), so the relay must be a binary. It's small: sockets, one child process, a ring buffer. Build it in C as `q2video` is linked (`tools/build.py`: the rootfs's `libc-2.28.so`, `nan2008`, `fp64`, `/lib/ld-linux-mipsn8.so.1`), so one binary runs on both devices.

## The bridge (host)

A long-running service on the host, for example a Python asyncio process under a systemd user unit:

- **Soloist.** It runs `soloist -k KEY -n NAME --ws 127.0.0.1:PORT` and restarts it if it exits. With `NAME` set to `Q2`, the pairing prompt ("choose Q2") stays true. Builds expire after 90 days and can't be redistributed, so the bridge (or its installer) downloads them from Spotify's downloads page and replaces the build before it expires; Soloist prints `client expires in N days` at start. The API key is the user's own; keep it out of logs, and out of the command line if Soloist can read it any other way (on the command line, `ps` shows it).
- **Audio.** A null sink, `pactl load-module module-null-sink sink_name=q2_soloist rate=44100 channels=2 format=s16le`, with Soloist's stream sent there (`PULSE_SINK=q2_soloist` if Soloist honours it, otherwise a stream target set from `pactl` or `pw-metadata`), and `parec -d q2_soloist.monitor --raw --format=s16le --rate=44100 --channels=2` read into the TCP stream. It sends audio only while Soloist reports `playing`; the null sink's silence otherwise is never sent. That's 1411 kbit/s.
- **State.** From `playback_state`, `track_changed`, `playback_changed` and `position_sync`: the relay's state lines. `state=none` while Soloist isn't the active device (`auth_state`'s `is_active`).
- **Covers.** It fetches `decorations.visual_identity.cover[]`'s `default` size (about 300 px, the size librespot picks) over HTTPS and sends the JPEG, so the device still does no TLS.
- **Volume.** Soloist stays at 100 (`set_volume 100` on activation and after any `volume_changed`), as librespot's `--volume-ctrl fixed` does; the device's volume is the DAC's or `q2video -s`'s.
- **Controls.** `p` → `play` or `pause` by the current state, `P` → `play`, `s` → `pause`, `n` → `skip_next`, `b` → `skip_prev`, `S ms` → `seek position_ms`.

### Q2SPOT/1 over the bridge

Soloist's API has no browsing or search, so the bridge answers those from the [Web API](https://developer.spotify.com/documentation/web-api), with OAuth (authorization code with PKCE) on the host, the refresh token kept beside Soloist's data. The app is the developer dashboard app the Soloist key came from. Before relying on an endpoint, check it's still available to new development-mode apps; Spotify has restricted some.

| Op | Answered from |
| --- | --- |
| `caps` | the ops below; `message` the bridge's version |
| `account` | `GET /me` (`display_name`, `product`); `login` while Soloist has no session |
| `playlists`, `playlist` | `GET /me/playlists`, `GET /playlists/{id}/items` |
| `liked` | `GET /me/tracks`, context `spotify:user:{id}:collection` |
| `albums`, `album` | `GET /me/albums`, `GET /albums/{id}/tracks` |
| `artists`, `artist` | `GET /me/following?type=artist`; `GET /artists/{id}/top-tracks` then `/albums` |
| `search` | `GET /search` with `type` from the category |
| `play` | `PUT /me/player/play?device_id=` Soloist's, with `context_uri` and `offset.position` (so a duplicated entry starts at the copy chosen), or `uris` for a track alone; whether Liked Songs plays as a context is to be checked (else its tracks as `uris`) |
| `queue` | WebSocket `get_queue` |
| `skip` | `get_queue`, check the row's URI is still at its position (else `unavailable`), then `skip_next` that many times |
| `enqueue` | WebSocket `add_to_queue` |
| `settings`, `shuffle`, `repeat` | the state's options; `set_shuffle`, `set_repeat_context`, `set_repeat_track` |
| `signout` | `unsupported`, "Sign out on the computer" |
| `downloaded`, `playdownload`, `download`, `downloadstatus` | `unsupported`, "Not available through Soloist" |

Status mapping: Web API 401 after a failed token refresh → `refused`; 429 → `throttled` with `Retry-After` in the message, answered without asking again until then; no network → `offline`. Cursors are the Web API's `offset` (opaque to Q2 Pod, as now), and pages are 50 rows at most.

### Relay ↔ bridge wire

The relay connects to `HOST:PORT` and sends `hello 1 TOKEN`; a wrong token closes the connection. After that, both sides send framed messages, one type byte and a 32-bit length:

- relay → bridge: `c` a control datagram, `q` a Q2SPOT/1 request (its bytes as Q2 Pod sent them).
- bridge → relay: `s` the state as `key=value` lines, `j` a cover JPEG, `r` a Q2SPOT/1 response, `a` PCM.

Audio on the same connection keeps one reconnect path and one token. If control messages wait behind PCM, a second connection for audio is the fallback (step 1 decides). The bridge listens on the LAN, so the token is what keeps other machines on the network out; it isn't encryption.

## Limits

- Only on the bridge's network: away from home there is no Spotify, and nothing is cached on the card (Downloaded Tracks and Download Playlist answer `unsupported`).
- The bridge's computer has to stay on and keep Soloist under 90 days old.
- 16-bit 44.1 kHz on the wire: Soloist's 24-bit lossless is cut to 16 bits.
- Controls answer about the relay's buffer late (~1 s).
- Termux on Android: not planned. Spotify doesn't list Android for Soloist, it would need a glibc `proot` and PulseAudio inside Termux, and Android kills long-running background processes. A Linux box is the target.

## Steps

Each step ends with its check passing; a device pass on both a Q2 and the M1 at the end.

1. **Audio spike.** A minimal relay that only connects and copies to stdout (`relay HOST PORT | aplay -D plughw:0,0 -f S16_LE -r 44100 -c 2`) and a bridge that only runs the null sink and `parec`. Check: 10 minutes without a gap on the M1 (AirPlay never lasted 24 s), with Wi-Fi throughput, CPU and the buffer's low mark measured. It decides the buffer size and whether audio needs its own connection.
2. **Bridge core.** Soloist supervision, the WebSocket client, state, covers, controls and the wire, against a fake relay on the host. Check: a scripted session (cast, pause, seek, skip, track change, deactivate) produces the expected state lines and covers.
3. **Relay contract.** Status file, control socket, sink lifecycle, buffer, reconnects, `.spotify/run` with the loop and pid file. Check, on the device with Q2 Pod's Spotify as it is: Now Playing and its art, Play/Pause and the side buttons, scrub and seek, local music taking over (`spot_yield`) and Spotify taking back (`spot_take`), the idle stop, Stop Streaming Services, the Rockbox row's kill, and a crashed relay (`spot_alive`).
4. **Browsing.** OAuth and the table above. Check: every menu in Q2 Pod's browser, More…, search in each category, a playlist track playing in its context, Queue's skip, shuffle and repeat, 429 and 401 handling against a fake Web API.
5. **Packaging.** Card files (`librespot` = the relay, `run`, the unchanged `aplay.sh`, a sample `remote`), the bridge's install (a systemd user unit; a NixOS module for this machine), Soloist's download and refresh, and the user guide's section.

## Open decisions

- **Where it lives.** A repo of its own beside q2-librespot (bridge, relay, card ZIP) is the likely fit, with only this doc and any firmware follow-ups here. Building the relay in this repo would reuse `tools/build.py`'s link recipe.
- **Firmware follow-ups, later and upstream.** Hide Downloaded Tracks and Download Playlist when `caps` lacks their ops (today `patch/spotify.c` always shows them), and word "choose Q2" from the account's device name. Neither is needed for the first version.
- **Bridge language.** Python is assumed for its WebSocket, HTTP and OAuth libraries; Rust if it should share code with q2-librespot.
- **Compression.** If step 1 shows 1411 kbit/s is too much for the device's Wi-Fi, FLAC through the stock `/usr/bin/ffmpeg` on the device is the next thing to try, at some CPU cost.
