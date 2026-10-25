# Spotify through Soloist (plan)

Status: a plan, not implemented (2026-10-25). Spotify's own Soloist runs on an always-on computer at home. The device reaches it from any network, home Wi-Fi or a phone's hotspot away from home, over one outgoing TLS connection, plays its audio as Opus, and is controlled from Q2 Pod's own Spotify pages. Q2 Pod's firmware doesn't change: a relay on the card keeps librespot's contract ([librespot.md](librespot.md), [internals](internals.md#spotify)), so the Q2 and the M1 Plus both get it.

## Why

Spotify withholds librespot's audio keys from many accounts, mostly new ones: every track fails with `error audio key 0 1` in `.spotify/spot.log` (librespot-org/librespot#1649, DiamondBond/q2-pod#98). No client-side fix exists. [Spotify Soloist](https://developer.spotify.com/documentation/soloist), Spotify's official headless Connect client (August 2026), plays those accounts, but it needs ARMv7, AArch64 or x86_64 and PulseAudio or PipeWire, so it can't run on the X2000 (below).

## Tests (2026-10-25)

All on a Linux laptop (NixOS, PipeWire 1.6.6) running Soloist 1.3.9, and an M1 Plus on Q2 Pod 1.4.2's dev build.

**Soloist plays the refused account.** Logged in as an account librespot gets no keys for, it played for 8 minutes with no key error.

**AirPlay: rejected.** PipeWire's RAOP sink sent Soloist to the M1's stock receiver (`/usr/bin/shairport`, Shanling's Shairport 1.1.1, AirPlay 1), which played 10, 17 and 24 s and then died; V2.1's AirPlay page went idle. A second Shairport run by hand with `-l` logged `player.c:161: alac_decode: Assertion 'outsize == FRAME_BYTES(frame_size)' failed`: Shairport 1.x aborts on any packet that isn't a whole 352-frame frame. The short packets are PipeWire's: `module-rtp` keeps the audio in a 4 MiB ring (`BUFFER_SIZE`, 23.8 s at 44.1 kHz S16 stereo), `set_iovec` splits a packet that straddles the ring's end into two iovecs, and `module-raop-sink.c`'s `stream_send_packet` reads only the first (`n_frames = iov[1].iov_len / impl->stride`). So once a wrap it sends a short packet; the ring's start is random, hence a crash within 23.8 s. No property changes it. Worth an upstream PipeWire fix, not needed here.

**Opus over HTTP, at home.** Soloist's stream went to a null sink (`module-null-sink`, 44.1 kHz S16 stereo), ffmpeg 8.1 encoded its monitor (`-f pulse`) to Ogg Opus at 160 kbit/s (20 ms frames, 100 ms Ogg pages), and a small HTTP server sent it to the M1's own Internet Radio as a station in a `.m3u` under `/mnt/mmc/Radio/`: no device code at all. Results:

- It sounded good to the user, Spotify's lossy audio encoded once more notwithstanding.
- The M1 decodes it with the stock `/usr/bin/ffmpeg` (4.2, native Opus decoder) at about 1% CPU; the device stayed 97% idle.
- A track change in the Spotify app reached the headphones in under 1 s.
- The first server, `ffmpeg -listen 1`, ran 20 s behind: ffmpeg started capturing before a listener came, and PulseAudio held the audio meanwhile, up to its 4 MiB record buffer (23.8 s), which the M1 then played as a backlog. Starting the encoder per connection removed it. The bridge must never let audio queue before or while it sends.

**Opus over the internet, on a phone's hotspot.** The same station through a port forward on the home router, the URL carrying a random token (anything else got a 404), the M1 on an Android phone's hotspot with the phone's Wi-Fi off. A logger on the card recorded the battery, the radio state, Wi-Fi bytes and the network every 10 s; the server logged each connection.

| | |
| --- | --- |
| Played | about 6½ minutes, two connections (365 s, then 16 s after a stop and start) |
| Data | 7.6 MB at 157 kbit/s: about 70 MB an hour |
| Stalls | two of about 10 s (one with 11 KB arriving in 10 s), heard as gaps |
| After a stall | about 10 s behind until the stop and start: the server sends live and never drops, so the audio held during the stall queued on the host, and the hotspot then delivered barely faster than real time (241 to 256 KB per 10 s against 220), so the queue never drained |
| Battery | unmeasured: 100% throughout, just off the charger, too short a run |

**Soloist on the device: ruled out.** It is closed source, so it could only run under QEMU's user-mode emulation, and only its ARMv7 build, since QEMU can't run 64-bit programs on the 32-bit X2000. Measured on x86_64 a minute into playback, the main process peaked at 65 MB (17 threads, 1.9% of one core) and its crash reporter at 21.7 MB, about 87 MB in all. The M1 has 115 MB of RAM, about 85 MB free with V2.1 running, and no swap, before QEMU's translation cache, the ARM libraries and a stand-in `libpulse.so.0` (Soloist links only glibc and loads `libpulse.so.0` at run time). Its CPU use, scaled to the X2000's 1.2 GHz cores and slowed further by emulation, comes to roughly a whole core or more.

## Design

```
 home server (Linux, always on)                            device, on any network
 ┌──────────────────────────────────────────────┐          ┌──────────────────────────────────────┐
 │ Soloist ──PulseAudio── null sink q2_soloist   │          │ Q2 Pod (unchanged)                    │
 │   ▲ WebSocket 127.0.0.1    │ monitor          │          │   state file, control socket,         │
 │   │                        ▼                  │          │   browse socket, run, killall         │
 │ q2-soloist bridge ── Opus 160 kbit/s          │  TLS,    │      ▲                                │
 │   │   Web API (browse, search, covers)        │  token   │ .spotify/librespot = the relay        │
 │   └── control, state, Q2SPOT/1 ───────────────┼◄─────────┤   ffmpeg (Opus) ─► aplay.sh           │
 └──────────────────────────────────────────────┘ internet └──────────────────────────────────────┘
          reached by a port forward or a tunnel                (home Wi-Fi or a phone's hotspot)
```

Two programs, neither in the firmware:

- **The bridge** (home server): runs Soloist, turns its WebSocket API and the Spotify Web API into what the relay needs, and encodes and sends the audio.
- **The relay** (card): installed as `.spotify/librespot` and started by `.spotify/run`, it does everything Q2 Pod expects librespot to do, over a connection to the bridge instead of a Spotify session. It always dials out, so the device's network and address never matter.

The relay takes librespot's file names because Q2 Pod finds the backend by them: `spot_launch` checks `SPOT_BIN` (`.spotify/librespot`) and runs `SPOT_RUN` (`.spotify/run`), and `spot_stop` and Home's Rockbox row stop it with the loop's pid in `/tmp/q2-librespot` and `killall -9 librespot aplay`.

### Buffer and stalls

Soloist's audio is live: the device can't hold more of it than has already played at home, so the relay's buffer is also the delay for anything that starts new audio. The tests set the rules:

- **One buffer, on the device.** The relay starts playing once it holds its target, about 1 s on home Wi-Fi and 3 to 5 s on mobile (to be tuned in step 1). The bridge holds nothing: it encodes only while connected and sends at once.
- **Pause is local and instant.** The relay stops its output, then sends the pause; Soloist stops a buffer's length later. Play resumes from the device's buffer, then Soloist's continuation follows without a gap.
- **Skip and seek** clear the device's buffer and wait for new audio: the target's length.
- **A stall longer than the buffer** makes the relay send a pause, so Soloist stops instead of playing to nobody and the queue the hotspot test hit can't build. Once the link is back and the buffer refilled, the relay sends play: nothing is missed and the delay doesn't grow.
- **A changed network** (home Wi-Fi to the hotspot and back) breaks the connection: the relay reconnects with the run loop's backoff and resumes as after a stall.

## The relay (card)

It keeps the contract in [internals](internals.md#spotify), item by item:

- **Status file.** `/tmp/q2-librespot.state`, rewritten whole (`.tmp`, renamed) from the bridge's state: `state=` (`none`, `stopped`, `paused`, `playing`), `track=`, `title=`, `artist=` (joined by `, `), `album=`, `duration=`, `position=`, `at=`, and `cover=1` once `/tmp/q2-librespot.state.jpg` holds the bridge's cover for this track. `at=` is the relay's own `CLOCK_MONOTONIC` ms; the position is the one playing out of the device's buffer, not Soloist's, which runs a buffer ahead.
- **Control socket.** Binds `/tmp/q2-librespot.sock` (`AF_UNIX` datagrams) and forwards `p`, `P`, `s`, `n`, `b` and `S <ms>`, with pause done locally first (above). Binding it also answers `spot_alive`'s liveness check.
- **Browse socket.** Binds `/tmp/q2-librespot.browse.sock` and passes each Q2SPOT/1 request to the bridge unchanged, writing back its response. Without a bridge it answers `offline` itself, with "Can't reach the Spotify bridge" as the message.
- **Sink.** Like librespot's subprocess sink: on `playing` it starts the stock ffmpeg decoding the Opus stream (`/usr/bin/ffmpeg -f ogg -i pipe:0 -ac 2 -ar 44100 -f s16le pipe:1`, or the bare packets if the wire carries them so) into `/bin/sh ./aplay.sh`. On anything else it kills and reaps both **before** it writes the new state, since `spot_yield` takes the state's leaving `playing` to mean the DAC is free. `aplay.sh` is kept unchanged, so `SPOT_OUT`, `q2video -s` and Bluetooth or USB output work as they do now. (Bluetooth and Wi-Fi exclude each other on the M1, so the M1 can't use Bluetooth output with this.)
- **TLS.** Through the rootfs's own `libssl.so.1.1` and `libcrypto.so.1.1`, verifying the server against `/etc/scrobble-ca.pem` (ISRG Root X1, so a Let's Encrypt certificate) and its name. Q2 Pod itself still does no TLS.
- **Bridge address.** `.spotify/remote` holds `HOST PORT TOKEN`.
- **Never written:** `/tmp/q2-librespot.download`, since there are no downloads.

The device has no `nc`, `socat`, `ssh` or `timeout` (BusyBox has only `telnet` and `wget`, and `telnet` would rewrite `0xff` bytes), and no `/dev/net/tun`, so no WireGuard or Tailscale on it: the relay must be a binary that makes its own connection. It stays small: sockets, OpenSSL, two child processes, a ring buffer. Build it in C as `q2video` is linked (`tools/build.py`: the rootfs's `libc-2.28.so`, `nan2008`, `fp64`, `/lib/ld-linux-mipsn8.so.1`), so one binary runs on both devices.

## The bridge (home server)

A long-running service, for example a Python asyncio process under a systemd user unit:

- **Soloist.** It runs `soloist -k KEY -n NAME --ws 127.0.0.1:PORT` and restarts it if it exits. With `NAME` set to `Q2`, the pairing prompt ("choose Q2") stays true. Builds expire after 90 days and can't be redistributed, so the bridge (or its installer) downloads them from Spotify's downloads page and replaces the build before it expires; Soloist prints `client expires in N days` at start. The API key is the user's own; keep it out of logs, and out of the command line if Soloist can read it any other way (on the command line, `ps` shows it).
- **Audio.** The null sink (`pactl load-module module-null-sink sink_name=q2_soloist rate=44100 channels=2 format=s16le`) with Soloist's stream sent there (`PULSE_SINK=q2_soloist` if Soloist honours it, otherwise moved with `pactl move-sink-input` whenever it appears, as the test did), and ffmpeg encoding its monitor: `-f pulse -fragment_size 3528 -i q2_soloist.monitor -af asetpts=N/SR/TB -ac 2 -ar 48000 -c:a libopus -b:a 160k -application audio -frame_duration 20`. The encoder starts when the relay asks for audio and stops when it pauses or goes, so nothing queues (Tests). `asetpts` rebuilds the timestamps from the sample count; without it ffmpeg warns of non-monotonic timestamps after a wait. With ffmpeg from nixpkgs on NixOS, run it without an inherited `LD_LIBRARY_PATH`, or it loads a mismatched `libasound`.
- **State.** From `playback_state`, `track_changed`, `playback_changed` and `position_sync`: the relay's state lines. `state=none` while Soloist isn't the active device (`auth_state`'s `is_active`).
- **Covers.** It fetches `decorations.visual_identity.cover[]`'s `default` size (about 300 px, the size librespot picks) over HTTPS and sends the JPEG.
- **Volume.** Soloist stays at 100 (`set_volume 100` on activation and after any `volume_changed`), as librespot's `--volume-ctrl fixed` does; the device's volume is the DAC's or `q2video -s`'s.
- **Controls.** `p` → `play` or `pause` by the current state, `P` → `play`, `s` → `pause`, `n` → `skip_next`, `b` → `skip_prev`, `S ms` → `seek position_ms`.

### Q2SPOT/1 over the bridge

Soloist's API has no browsing or search, so the bridge answers those from the [Web API](https://developer.spotify.com/documentation/web-api), with OAuth (authorization code with PKCE) on the server, the refresh token kept beside Soloist's data. The app is the developer dashboard app the Soloist key came from. Before relying on an endpoint, check it's still available to new development-mode apps; Spotify has restricted some.

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
| `signout` | `unsupported`, "Sign out on the server" |
| `downloaded`, `playdownload`, `download`, `downloadstatus` | `unsupported`, "Not available through Soloist" |

Status mapping: Web API 401 after a failed token refresh → `refused`; 429 → `throttled` with `Retry-After` in the message, answered without asking again until then; no network → `offline`. Cursors are the Web API's `offset` (opaque to Q2 Pod, as now), and pages are 50 rows at most.

### Relay ↔ bridge wire

The relay opens TLS to `HOST:PORT` and sends `hello 1 TOKEN`; a wrong token closes the connection. After that, both sides send framed messages, one type byte and a 32-bit length:

- relay → bridge: `c` a control datagram, `q` a Q2SPOT/1 request (its bytes as Q2 Pod sent them), `A` start or stop the audio (with the buffer's state, so the bridge knows a stall from a pause).
- bridge → relay: `s` the state as `key=value` lines, `j` a cover JPEG, `r` a Q2SPOT/1 response, `a` Opus audio.

Audio on the same connection keeps one TLS session, one reconnect path and one token. At 160 kbit/s a control message waits behind at most a frame or two; a second connection for audio stays the fallback if step 1 shows otherwise.

## Network and hosting

- **Reaching home.** With a public IPv4 address at home (not carrier-grade NAT: the router's WAN address matches what an outside site reports, and isn't in `100.64.0.0/10`), a TCP port forward to the server, a dynamic DNS name and a Let's Encrypt certificate, all free. Behind carrier-grade NAT, Tailscale Funnel (free on the personal plan, a `ts.net` name with a Let's Encrypt certificate, bandwidth limits to check). Cloudflare Tunnel needs a domain on Cloudflare, and its terms have restricted audio and video; read them first.
- **The port forward.** One TCP port, a fixed destination port and forward port: on the router tested, "Destination port: Any" with a forward port would have sent every incoming port to the server. Reserve the server's address in the router's DHCP so the rule keeps pointing at it.
- **Security.** TLS and the token are mandatory, since the port is open to the internet. Soloist's WebSocket stays on loopback (it has no authentication). A small machine that does nothing else, such as a Raspberry Pi (Soloist runs on ARM), is a better home for an open port than a laptop.
- **Costs.** Hosting can be free. A Pi draws 3 to 5 W, a few dollars a year in power. Mobile data is about 70 MB an hour at 160 kbit/s (Spotify's own "Very high" is 320 kbit/s); many unlimited plans cap hotspot data separately.

## Limits

- No offline playback: in a dead zone the device plays out its buffer, then pauses Soloist until the link is back. Downloaded Tracks and Download Playlist answer `unsupported`.
- The home server has to stay on and keep Soloist under 90 days old.
- Skips and seeks wait a buffer's length; pause doesn't.
- Battery: both the device's Wi-Fi and the phone's hotspot stay on; not yet measured.
- Spotify's audio is lossy, and Opus encodes it once more (good to the ear at 160 kbit/s in the test); Soloist's 24-bit lossless can't reach the device this way.
- Personal listening only: Soloist's documentation describes only local output.
- Termux on Android: not planned. Spotify doesn't list Android for Soloist, it would need a glibc `proot` and PulseAudio inside Termux, and Android kills long-running background processes.

## Steps

Each step ends with its check passing; a device pass on both a Q2 and the M1 at the end.

1. **Relay audio.** The relay's TLS connection, token, Opus decode through the stock ffmpeg into `aplay.sh`, the buffer and the stall rule, against a bridge that only encodes. Check: on home Wi-Fi and on a phone's hotspot, delay at the target, a forced stall (the server's port blocked for 15 s) pausing and resuming Soloist without a growing delay, a network switch reconnecting, and a battery run (from a full charge, charger out, an hour of playback) on the device. It sets the buffer targets.
2. **Bridge core.** Soloist supervision, the WebSocket client, state, covers, controls and the wire, against a fake relay. Check: a scripted session (cast, pause, seek, skip, track change, deactivate) produces the expected state lines and covers.
3. **Relay contract.** Status file, control socket, sink lifecycle, `.spotify/run` with the loop and pid file. Check, on the device with Q2 Pod's Spotify as it is: Now Playing and its art, Play/Pause and the side buttons, scrub and seek, local music taking over (`spot_yield`) and Spotify taking back (`spot_take`), the idle stop, Stop Streaming Services, the Rockbox row's kill, and a crashed relay (`spot_alive`).
4. **Browsing.** OAuth and the table above. Check: every menu in Q2 Pod's browser, More…, search in each category, a playlist track playing in its context, Queue's skip, shuffle and repeat, 429 and 401 handling against a fake Web API.
5. **Packaging.** Card files (`librespot` = the relay, `run`, the unchanged `aplay.sh`, a sample `remote`), the server's install (a systemd user unit; a NixOS module), the certificate and dynamic DNS, Soloist's download and refresh, and the user guide's section.

## Open decisions

- **Where it lives.** A repo of its own beside q2-librespot (bridge, relay, card ZIP) is the likely fit, with only this doc and any firmware follow-ups here. Building the relay in this repo would reuse `tools/build.py`'s link recipe.
- **Backend.** Spotify's desktop app could stand in for Soloist on an x86_64 server already running it: its MPRIS interface (checked on 1.2.95) has `PlayPause`, `Next`, `Previous`, `Seek`, `SetPosition`, `OpenUri`, a Spotify-only `LoadContextUri`, settable `Shuffle` and `LoopStatus`, and `Metadata` with `mpris:artUrl`, with change signals; no queue (`HasTrackList` false), which the Web API covers. It needs no API key and doesn't expire, but needs a graphical session, is far larger, and Spotify publishes it for x86_64 only, so not for a Pi. The relay and the wire don't change either way.
- **Firmware follow-ups, later and upstream.** Hide Downloaded Tracks and Download Playlist when `caps` lacks their ops (today `patch/spotify.c` always shows them), and word "choose Q2" from the account's device name. Neither is needed for the first version.
- **Bridge language.** Python is assumed for its WebSocket, HTTP and OAuth libraries; Rust if it should share code with q2-librespot.
- **Bitrate.** 160 kbit/s sounded good; 96 to 128 kbit/s would save mobile data at some quality, worth an A/B in step 1.
