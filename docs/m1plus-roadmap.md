# M1 Plus port: planned work

What is left before the M1 Plus build has Q2 Pod's features, ordered by value and effort. What has been
done, and why, is in [m1plus-progress.md](m1plus-progress.md).

Every item ends in the same loop. First the Q2 checks must pass:
- Q2 Legacy and iPod still build byte-identical to the last verified Q2 build;
- the Q2 suites pass on both.

See [m1plus-integration.md](m1plus-integration.md#checklist). Then the build's name check,
`test/build.py --build`, `test/patch.py` and `test/boot.py` must pass on M1. Then flash through the
menu updater, and use the menu updater with stock `update.bin` to get back. Where an item's test is a `KNOWN GAP` or `NOT PORTED`
line today, the fix removes that marker. `known_gap` fails the run once its check passes, so a fixed
gap can't be left marked.

Sizes are rough: **S** is a day or less, **M** a few days, **L** a week or more.

**Next:** section 4, from the top of its table; Spotify on the device
(section 3) when there is an account. Functionality comes first:
items that only change how something looks wait for the final pass (section 7).

## Ground rules

- **Don't break Q2.** No change for M1 may change the Q2 firmware or its tests:
  - Q2 Legacy and iPod `update.tar` stay byte-identical to the last verified Q2 build, and every Q2 suite
    and case keeps running and passing.
  - M1 code goes behind `#if M1PLUS` / `if m1plus` or into a per-model table. That includes defensive checks
    only V2.1 needs.
  - A deliberate Q2 change says so in its commit, with its reason and its test.
  - The full rule is in [m1plus-integration.md](m1plus-integration.md#rule-for-future-work-dont-break-q2).
- **Find each V2.1 address in V2.1's code, then pin it in a test.** Read the same-named or same-role
  function in V2.1's demo, and pin the instruction or string the change relies on, as
  `test/build.py`'s updater check and `test/patch.py`'s `tslib_run` check do. Never reuse a V1.32
  address.
- **Name every stock widget, image and style through `offsets.inc`** (`VIEW_`, `ICON_`, `STYLE_`,
  `ROW_`, `ABOUT_`), so the build's V2.1 name check covers it.
- **Build rows with `list_row`/`row_of`.** They build V2.1's row structure on M1. Don't reach a row's
  parts by child index.
- **Prefer V2.1's own UI conventions.** Its title-bar back button, its row styles, and its native
  settings where one exists (for example Double wake). Avoid copying a Q2 control V2.1 already has.
- **Every page has an explicit Back button.** Every page Q2 Pod opens or replaces on M1 shows V2.1's
  title-bar back button at its top left. Make it with `back_button`, or with `page_title`, which adds
  one; its click sends Return, and the page's keyup decides whether that closes the page or steps
  back one screen. The M1 has no Return key. Previous, Next and Play/Pause are media keys, as on
  stock, except that in Knob: Navigation Previous also presses the page's back button. So no
  gesture, hidden tap or key may be a page's only way out. Each new page's `test/boot.py` step
  closes it with the button (`BACK`).

## 1. Small fixes (S)

Done: Crossfade's page on V2.1, the Playback rows that V2.1's list rebuild dropped, and the `test:`
lines that could be ported (see [m1plus-progress.md](m1plus-progress.md), section 14). What is left
here goes with other sections' features:

- **The `test:` lines whose features M1 can't reach yet.** Two lines, each going with its feature:
  - the stock key-down helper with STOP (`0x65f688`): with V2.1's copy of that private AWTK
    helper, still to be found (V2.1 binds no key-down handler for the payload to hook);
  - folder rollover and the UI scheduler delay: with the player call sites (section 4).

Done since: the Shuffle page's note and the Photos row's icon ([m1plus-progress.md](m1plus-progress.md)
section 20); Coverflow's track queue through `mclNextSong`, now on M1, and other slide menus' next and
previous, Q2 only since V2.1 has none (section 21).

## 2. Hardware-specific behaviour (M)

Done: Coverflow and Photos' scroll distance, and Coverflow's covers by touch: a swipe turns them a
cover per 100 px, and a tap opens the centre cover or brings a side one to the centre
([m1plus-progress.md](m1plus-progress.md) section 21).

## 3. Entry points for Q2 Pod's pages (L)

Done ([m1plus-progress.md](m1plus-progress.md) sections 17 and 22): every payload page has a way in
from the Q2 Pod page, a back button, and the touch long-press where the Q2 has a Play/Pause hold.
- **Streaming.** V2.1 has no Streaming page (its Tidal is a Home card), so Spotify, Internet Radio and
  AirPlay are rows on the Q2 Pod page, after Coverflow. Their Now Playing pages have back buttons,
  with their text under the art on the portrait screen.
- **Videos.** Its row shows with a Videos folder. q2video draws a back chevron at the top left, where
  a tap quits, and the knob is its wheel.
- **Long presses.** Most Played, the Ratings lists and Long Songs (the song menu), a station (in or
  out of favourites), a Spotify track (Spotify's queue) and Coverflow's centre cover (the album menu).

A video and Internet Radio play through q2video on the ES9069Q, straight after a boot too (dev 18,
[m1plus-progress.md](m1plus-progress.md) section 23). Left for the device:
- Spotify, with q2-librespot on the card: its `aplay` on `plughw:0,0`, and whether the Q2's static
  MIPS build runs on the M1's kernel.

## 4. Re-pointing V1.32 call-site patches (M each, many)

Each `NOT PORTED` line below names a patch or hook made at a V1.32 address. A call site is ported by
adding its V2.1 words under its name in `CALL_SITES['m1plus']` (`tools/build.py`):
- the build applies them, as it applies Q2's;
- `test/build.py` checks each word, and allows it in M1's demo diff;
- `test/patch.py`'s test for that name runs once the name is in the table (`'NAME' in SITES`). Its
  harness addresses are V1.32's until the test is ported too.

A hook goes in `M1PLUS_HOOKS` instead.

Done: the boot queue bug the check found. A reboot no longer deletes the saved advanced queue
([m1plus-progress.md](m1plus-progress.md) section 25).

Every row was checked against V2.1's `demo` on Oct 21 ([m1plus-progress.md](m1plus-progress.md)
section 24). "Same code" means V2.1's function is V1.32's after normalising addresses. Ordered by
value and effort:

| Feature | V2.1 site | Notes | Size |
|---|---|---|---|
| Shuffle honours Play next, and its Previous/Next history | `SHUFFLE_CALL`: `bal` at `0x5d5a28` (`0x0411ea61`), the pick at `0x5d03b0` | same code. One site does both (`ringnav_shuffle`) | S |
| Keep the page cache | `DROP_CACHES`: `0x50b868`'s `beq` (`0x12220006`) | same code, in `check_cpumem` | S |
| 65,000-song scan | `SCAN_LIMIT`: `0x5efeb4` (`lw` `0x8fc2b084`, `slti` `0x28424e20`, count `0x8fc4b084`) | same code | S |
| Article-free sort | `SORT_TRIMS`: `0x5e0ea4`, `0x5e0f10`, `0x5e17bc`, `0x5e1828` | same code (comparators `0x5e0dac`, `0x5e16c4`) | S |
| M4B in folder scans | `AUDIO_EXTENSION_CALLS`: `0x5e8af0`, `0x5ea840` | same list, without `.m4b`. The `strstr` load before each is `0x8f99f694` | S |
| Ratings' Now Playing heart | V2.1's heart is `btn_fav` (`show_player_face`, `btn_imgfav_style`) | no `img_fav`. Bind the rating hold to `btn_fav` | S–M |
| Lock screen Clock row and thumbnails | the Lock screen page, `systemset_screensaver_page_init` (`0x4abe04`) | a picture grid now. On the device the five built-ins the payload adds show as empty circles, and there is no Clock row | M |
| Lock screen cover repaint | the lock window (`screensaver_page_init`) reads `/tmp/abp` | V2.1's lock window differs. Check on the device whether it repaints on a track change | S |
| Cover worker pause and stale completion | not checked | `COVER_PAUSE` and `ringnav_cover_done` are Q2 only. Check with the art rows | S |
| Now Playing hold's Add to Playlist when the queue changed | V2.1's playlist pick handler, still to find | M1 already selects the row (`qm_select`). Only the stale-queue guard is missing. `playlist_rebuild` is iPod only | S |

These need hardware, a setting or a library to check on the device, so they come last:

| Feature | V2.1 site | Notes | Size |
|---|---|---|---|
| LDAC HQ sends 990 kbps | `LDAC_HQ`: `0x4d304c`–`0x4d3070` | An LDAC headphone (the WH-1000XM6), with its multipoint off. same code, so the same words except the jump table's `lw` (`0x8c42a4b0`). Check the quality page's row order | S |
| Gapless in advanced play, and across speed changes | hooks: `mcl_preload` `0x5d0ea4`, `mcl_open_preload` `0x5d0bd8` | Gapless on (off on the device now). same code. Without `mcl_preload` (not hooked on M1), Shuffle Albums/Folders lose gapless | S |
| Resume on connect | `BT_CONNECT_START`: `bal save_start_player` at `0x4d6320` (`0x04113031`). Rows: the list builder at `0x4a3734` | A Bluetooth headphone. still restarts the queue unpaused. The builder is new (five callers, V2.1's rows) | M |
| Same-named albums' art, an artist's albums' art keys | V2.1's album list and artist page renderers, still to find | Two albums of the same name by different artists on the card. V2.1's cover worker is V1.32's (`md5` of the album name), caching in `/tmp/abp`. Split rows share one cover. The order is ported (`ringnav_localclass`, `0xff01`) | M |

Not ported, because V2.1 has them (ground rules: prefer V2.1's own UI):
- **Artist pages open on Albums** (`ARTIST_ALBUMS`): V2.1's artist page lists the artist's albums.
- **Key lock and quick lock rows** (`keylock_rows`, `quick_lock`): V2.1's Buttons lock has a switch and
  Volume, Keys and All modes.
- **Artists defaults to Album Artist, read at boot** (`read_artistype_value`, `ringnav_bootmode`):
  V2.1's Artists page has its own Artist/Album Artist switch, saved as `ARTISTTYPE` and read in
  `config_init`. A fresh config still starts on Artist.
- **Artists rows without the head picture** (`CLASS_ICON`): V2.1 draws its own artist icon.

Now Playing's info lines (`NP_INFO_CALL`) only change how the lines read, so they are in section 7.
Their V2.1 site is the fill's one call, `0x53bebc` (`0x0411f760`, the fill at `0x539c40`).

## 5. The iPod UI on M1 (L, after sections 1–4)

`--ipod` is refused for M1 Plus. The iPod UI patches V1.32's UI assets, styles and code layout, and
assumes the Q2's 375x320 landscape screen and touch wheel. An M1 version would be a redesign for a
320x480 portrait touchscreen with a knob, not a port. Decide whether it is wanted before starting.
Two `test/patch.py` checks go with it: the library rows' title bounds (`compact_row_layout`) and the
info pages' unwind (`navigator_close`). In the Stock UI each runs V1.32's own code as a control.

## 6. Tooling and release

- **Q2 from the same tree.** Building the fork point's Q2 firmware beside M1's is tracked in
  [m1plus-integration.md](m1plus-integration.md): the measured differences, and items 1–9 to close them.
  The Q2 release (`tools/release.py`) is broken on this branch until its item 1 lands.
- **Release packaging for M1.** The README tells M1 users to download `update.bin` from a release, but
  `tools/release.py` packages only the Q2 (upstream owns that). An M1 path needs:
  - a reproducible `update.bin`;
  - a manifest check (`model`, `input_sha256`, `logo_source`);
  - a release note with the reflash-to-stock instructions.
- **q2remote on M1 (first: it makes the rest faster).** Done ([remote.md](remote.md#m1-plus)):
  - upright screenshots, keys, knob turns and taps;
  - `swipe X0 Y0 X1 Y1 [MS]`, from Goodix-CTP's move frames recorded on the device;
  - `tap X Y MS`, a held tap for the long press;
  - `peek NAME...`, payload and demo variables by name, field by field, from the running `demo`
    ([remote.md](remote.md#reading-variables)).

  A remote session now reaches the Q2 Pod page by itself. Next:
  - **An on-device log:** a small ring buffer the payload writes, which q2remote reads. `peek` shows
    state at one moment; a log would show the order of events, such as which of `qm_hold`'s checks
    refused during a hold.
- **Latent Q2 bugs found through M1.** Both were fixed only behind `M1PLUS`, to keep the Q2 build
  byte-identical (ground rules). Fixing them on the Q2 is a deliberate Q2 change, best made
  upstream, with a Q2 device check:
  - Long Songs' `taglib_file_new` call passes no `readAudioProperties`, so it reads whatever `$a1`
    holds; when that is 0, every length reads as 0 and is cached as measured;
  - AWTK's hit test doesn't skip hidden views, so the hidden book reader and photo viewer take taps
    meant for the list under them. The wheel hides this on the Q2; `view_show` is the M1's fix.
- **Videos whose sound starts late in the file.** q2video's one ffmpeg writes the picture and the
  sound, and q2video paces the picture by the sound played. A file that keeps more video ahead of its
  first sound than the picture's 4 MB pipe holds (8 Q2 frames; an mp4 interleaved by the second has
  25) stops on its first frame. The M1 runs the sound through a second ffmpeg (dev 16); the Q2 could
  do the same.
- **Radio stations whose URL is a playlist.** radio-browser's `/m3u/` lists can give a station's
  `.pls` (or `.m3u`) URL rather than its stream, which ffmpeg reads as text: the station shows "Can't
  play this station". Seen with Los 40 Principales México on dev 16. The Q2 has the same code, so this
  is a Q2 Pod change: resolve a remote playlist to its first stream, or ask radio-browser for
  `url_resolved`.
- **A card library in the emulator.** `test/boot.py --media` mounts a small card on a tmpfs: two long
  songs (header-only FLAC and MP3), a book and a photo, with V2.1's `songtable` seeded. Tags (album,
  artist) in the files and a scan would let the walk open Album, Artist and Now Playing. Playback itself
  would still need a stand-in for `hciplayer`'s audio output. The touch long-press's walk step (hold an
  album tile on an artist's page; the menu opens and the tile doesn't) waits for this.
- **An after-boot log on the device.** The `.rockbox/rockbox` diagnostic script can leave a background
  job that writes `ps` and the full `dmesg` a minute after boot. That captures demo crashes and driver
  errors that the emulator can't see.
- **Recovery mode.** The device has a separate recovery system (`kernel2`, `rootfs2`) and an `ota`
  partition. Finding how to start it without demo would give a way back to stock even if demo can't
  start, which would make riskier experiments safe.

## 7. Final pass: look and feel (after sections 1–4)

Items that only change how something looks, gathered once all the functionality is ported:

- **The Shuffle page's rows.** Its three rows (`shuffle_menu`, `page_row_detail`) show on M1 as bare
  centred text, with no row background or separator, where the Q2 Pod page's rows are V2.1's (ground
  rules: `list_row`/`row_of`). Seen over q2remote on dev 12; Ratings' page has the same rows (dev 14).
  Check the other `page_list` pages too: Internet Radio's menu shows the same in the emulator.
- **The Streaming rows' icons.** On the Q2 Pod page, Spotify's and Internet Radio's icons are wider
  than V2.1's 40 px row icons and reach the row's left edge (`stream_spotify`, `stream_radio`).
- **Now Playing's info lines** (`NP_INFO_CALL`). V2.1's info page writes `Label:value` lines (album,
  genre, year, size) and the folder alone. `ringnav_np_info` spaces them and labels the folder. V2.1's
  site is in section 4's notes.
- **Coverflow's covers by touch.** A tap on a side cover moves it to the centre, sized by the
  renderer's geometry; whether a swipe's feel (100 px a cover, a flick within 300 ms) suits the
  device's panel.

## Already Q2-only by design

These are skipped on M1 on purpose (marked `Q2 only` in the tests), not gaps:

- the touch wheel and its sensitivity;
- long Return;
- the sideways splash rotation;
- the Q2's Centre-key Wake setting (V2.1 has its own Double wake);
- Standby resume staying dark (`STANDBY_WAKE`): it goes with that Wake setting. V2.1's Standby also
  closes Bluetooth and unmounts the card, and a screen tap can wake it, which a dark resume would
  leave unlit;
- Home's Coverflow card: V2.1's Home is a grid of its own cards, and Coverflow opens from the Q2 Pod
  page;
- Key Tone: V2.1 has no buzzer command, and binds no key-down handler to hook.

The Rockbox dual boot stays: there is no Rockbox for the M1 Plus yet, but the hook serves as a boot-time
diagnostic.
