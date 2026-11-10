# M1 Plus: unported features

The upstream Q2 Pod features still unported or awaiting validation after the 1.5.8 sync (`staging`;
`1.5.8-m1.1` is the last release). Each row has a status:

- **Planned:** to be ported. Most have a known way in on V2.1, or a check to make first.
- **Native; live validation pending:** the firmware already provides the behavior; account-dependent checks remain.
- **In progress:** being ported on a branch, per its plan.
- **Unplanned:** not to be ported for now, for the reason given.

Features left out of the M1 on purpose are listed in
[m1plus-roadmap.md](m1plus-roadmap.md#already-q2-only-by-design) instead.

This doc replaces the roadmap's U4 list. Machines keep two other lists:
- the port report, `test/m1plus/ports.py --unported`;
- `test/m1plus/patch.py`'s `NOT PORTED` lines.

A sync's new rows go here (roadmap U5). A port follows the ground rules: find the feature in V2.1's
code, then pin it in a test. A row is removed once its port has passed on the device, with a pointer
to its [progress](m1plus-progress.md) section.

| Feature | Since | Q2 Pod's pieces | Status |
|---|---|---|---|
| [The iPod UI](#the-ipod-ui) | 1.2.2 or earlier | `playlist_rebuild`, `widget_on_paint_background`, `bigcover_page_init`, `style_get_color`, `image_manager_add`, `list_get_img_pic`, `systembar_showface` (1.4.5); Light Mode, Corners and the new accents (1.5.0); `ui_loader_load_widget_with_parent`, Centred Now Playing, Smart Awake, bold font, Home art pan (1.5.8); Carousel, Click With Headphones, the art following the player's cover (1.5.9); Single Press Scrub (1.6.0) | In progress |
| [Games](#games) | 1.3.9 | `games.c`, the iPod UI's Games row | Unplanned |
| [The extra time zones](#the-extra-time-zones) | 1.2.9 | `select_timezone`; `timezone_row`, `TIMEZONES` (1.5.0) | Planned |
| [Network Update](#network-update) | 1.3.8 | `systemset_fwupdate_page_init`, `netupdate.c`, `fwupdate_tf` | Planned |
| [Battery: the MQA side chain](#battery-fixes) | 1.2.9 | `MQA_GATE`, `MQA_PROBE` (`tools/peq.py`) | Planned |
| [Battery: Tidal's stream thread parked](#battery-fixes) | 1.4.5 | `STREAM_POLL_CALLS` and `get_tidal_trackurl` (1.5.0; 1.4.5's `STREAM_POLLS`) | Native; live validation pending |
| [Battery: the kernel modules' idle clocks](#battery-fixes) | 1.5.0 | `tools/aic.py`, `rotator.py`, `pwm.py`, `mcu_park.py` (`--aic-idle-wait`, `--rotator-lazy-clock`, `--pwm-idle-clock`, `--mcu-idle-sleep`) | Planned |
| [FLAC fast paths](#flac-fast-paths) | 1.5.0 | `tools/flac.py`, `patch/flac_*.c` (`tools/peq.py`, `--flac-experiments`) | Planned |
| [Display's sub-pages](#displays-sub-pages) | 1.5.0 | `ringnav_display`'s Appearance, Coverflow and Controls, `display_sub` | In progress |
| [Videos in Folder view](#videos-in-folder-view) | 1.5.0 | `folder_click`, `books_video`, `LOAD_DIRECTORY_RET` (1.5.5) | Planned |
| [A reboot keeping the place](#a-reboot-keeping-the-place) | 1.5.0 | `device_reboot`, `dialog_checkfw_dialog_init` | Planned |
| [SyncLink's keys past the Buttons lock](#synclinks-keys) | 1.5.0 | `main_loop_post_key_event` | Planned |
| [A card app's own Streaming icon](#a-card-apps-own-icon) | 1.5.0 | `addon_icon` (#88) | Planned |
| [Play/Pause's hold at 700 ms](#playpauses-hold) | 1.4.5 | `HOLD_KEYS` (replaces `PLAY_HOLD` in 1.5.5) | Planned |
| [Playlist allocation and deletion](#playlist-allocation-and-deletion) | 1.5.5 | `createPlayListItem`, `playlist_delete_click` | Planned |
| [Battery: paced player scheduling and command waits](#battery-fixes) | 1.5.5 | `MAINSCHEDULING_CALL`, `PAUSE_WAIT`, `IDLE_WAIT`, `CMD_DONE` | Planned |
| [MP3 encoder delay and padding](#mp3-encoder-delay-and-padding) | 1.5.5 | `mp3_gapless.c`, `MP3_ALLOC`, `MP3_FILTER`, `MP3_CLOSE`, `MP3_READ` | Planned |
| [Bluetooth resampler continuity](#bluetooth-resampler-continuity) | 1.5.6 | `RS_OPEN_SLOT`, `rs_open` (`tools/peq.py`, `peq_player.c`) | Planned |
| [Coverflow flick gestures](#coverflow-flick-gestures) | 1.5.7 | `touch`, `carousel_glide`, `CF_DRAG_*` and `CF_*` gesture tunables | Planned |
| [Directory markers](#directory-markers) | 1.5.8 | `library_scope.c`, `MUSIC_WHERE`, `music_records`, Era SQL | Planned |
| [Automatic scrobble uploads](#automatic-scrobble-uploads) | 1.5.8 | `scrobble_auto`, `[SCROBBLE] AUTO` | Planned |
| [Simple EQ's Presets shortcut](#simple-eqs-presets-shortcut) | 1.5.7 | `E3_PRESETS`, three-button Simple EQ layout | Planned |
| [Enlarged art's reset default](#enlarged-arts-reset-default) | 1.5.6 | `DEFAULT_CONFIG`, `COVERMODE` (`tools/build.py`) | Planned |
| [Stock's Chinese UI text in English](#stocks-chinese-ui-text) | 1.4.5 | `english_ui`, the `system_prove` label (`tools/build.py`) | Planned |
| [q2remote's demo log](#q2remotes-demo-log) | 1.4.5 | `LOG_HOOK` (`tools/build.py`) | Planned |
| [An artist's albums tab's album-artist rewrite](#an-artists-albums-tab) | 1.2.9 | `toolsQueryContentDbTable` | Planned |
| [Folder's roots without OTG](#folders-roots-without-otg) | 1.2.2 | `folder_load_top` | Planned |
| [The Wi-Fi transfer page](#the-wi-fi-transfer-page) | 1.3.0 | `WEB` | Planned |
| [Quick Settings' brightness through a swipe up](#quick-settings-brightness) | 1.3.8 | `g_dropdown_menu_state`; `quick_stuck` (1.4.5) | Planned |
| [Knob: Navigation on Set Time Manually](#set-time-manually) | the M1's own | an `m1plus_contexts.inc` row | Planned |
| [Tidal's cache and Tidal Downloads](#tidal) | 1.2.2 | `tidal_play`, `tidal_downloads`, `REC_TIDAL_ID` | Planned |
| [Tidal's lists past 50](#tidal) | 1.5.0 | `tidalPlaylistDetailThd`, `tidalAlbumDetailThd`, `tidalColTracksThd`, `TIDAL_PAGE_DONE` | Planned |
| [Knob: Navigation on the Tidal and HiFi store pages](#tidal) | the M1's own | `m1plus_contexts.inc` rows | Planned |
| [Card apps' library update](#card-apps-library-update) | 1.5.9 | `addon_library.c` (`library_poll`), `M3U_DIR_CALL`, the caps' `library` | Planned |
| [An .lrc's UTF-8 test](#an-lrcs-utf-8-test) | 1.5.9 | `mclIsUtf8WithoutBOM` (`ringnav_lrc_utf8`) | Planned |
| [A playlist row's hold menu](#a-playlist-rows-hold-menu) | 1.5.9 | `qm_hold`'s `QM_PLAYLIST` | Ported; dev 57 device pass |
| [Night Shift](#night-shift) | 1.6.0 | `nightshift.c`, `night_row`, `LCD_*` (`offsets.inc`) | Planned |
| [The watchdog and the crash log](#the-watchdog-and-the-crash-log) | 1.6.1, 1.6.2 | `wdt_poll`, `state_poll`, `WDT_MS`, `WDT_LONG_MS` (`navigation.c`) | Planned |
| [A USB DAC across a gapless change](#a-usb-dac-across-a-gapless-change) | 1.6.1 | `ao_init` (`peq_player.c`), `AO_INIT_SLOT`, `USB_BUFFER` (`tools/peq.py`) | Planned |
| [The settings restack](#the-settings-restack) | 1.6.4 | `library_open`, `playset_sub`, `library_order`, `keylock_open`, `boot_row` on Power, `POD_KEYTONE`, `POD_CARMODE` (`navigation.c`) | Planned |
| [The stale press backstop](#the-stale-press-backstop) | 1.6.4 | `stale_heal`, `stale_note`, `LOOP_PRESSED`, `QUEUE_LEAF` (`ringnav_queue_event`), `WHEEL_LOG_HOOK` | Planned (`stale_heal`); the rest Q2 only |

Era, Western tag/CUE text, hidden-folder exclusions, Streaming Configuration, user-space idle
changes and lyrics passed the combined device checks in [progress section 50](m1plus-progress.md#50-five-feature-batch-on-150-oct-28).
The [validation record](m1plus-validation-1.5.0.md) retains limits of the hardware pass, including
album-worker cancellation and USB-storage shutdown covered in emulation, and the live Tidal exception.

## Known issues on the M1

Found on the device and not fixed yet. Each goes to a fix round of its own:
- **G1. View Queue does nothing without a shuffle.** `qm_run` falls back to
  `navigator_to("playerqueue_page")`, a Q2 page V2.1 does not have: its queue is the player's list
  dialog. With a shuffle on, View Queue opens. This predates 1.5.8
  ([progress section 54](m1plus-progress.md#54-fixes-for-the-158-device-pass-nov-1)).
- **G2. Now Playing shows a refused track.** After the player refuses a file (the oversized copy in
  section 54), Now Playing's position and the album list's highlight move to it while the previous
  track keeps playing. Cosmetic.

## Ported, not yet checked on the device

These are on the M1 and pass the suites, but the passes so far had nothing to check them on:
- **CD Ripper's pages with Knob: Navigation** (`cdripper_page`, `searchcdripper_page`, `e47f232`): no
  CD drive at hand.
- **A card app ending before USB storage takes the card** (`usbmode_page_init`, `5efb249`).
- **Ogg and Opus covers, a CUE track's file tags, WebP art and a folder rescan's refreshed tags**
  (`GRID_COVER`, `PLAYER_COVER`, `ID3_PATH`, `SCAN_REFRESH`): the card has none of these files.

## Test cases that need V1.32 code

These features run on the M1, but a few of their suite cases can't run there:
- Folder Root's open and Back, and Go to Folder's, through stock `folder_back`. V2.1 keeps one history
  stack, `yoffset_rowsave` and `m3ufile_path`, where the cases read V1.32's history globals.
- Shuffle Songs being one-shot. V2.1 has no `config_playmode` symbol to stand for the user's mode
  choice.

## Notes

### The iPod UI

In progress on `feature/m1-ipod` (the user's choice, Nov 2), per [m1plus-ipod-ui.md](m1plus-ipod-ui.md).
This replaces the Oct 26 decision to keep V2.1's own look. Upstream 1.5.9 deleted the Legacy path the
M1 compiles, and the M1's mix of V2.1 pages and Q2 Pod pages is clunky (roadmap section 5). The iPod
UI is built for the Q2's 375x320 landscape screen and touch wheel, and patches V1.32's UI assets,
styles and code layout. The M1 version reflows it for the 320x480 portrait touchscreen and knob, and
rewrites V2.1's assets the same way. Phase 1 is done: the M1 compiles the iPod path, and the port report
lists each iPod hook as `unported` with the Phase 4 item that ports it (`style_get_color`,
`image_manager_add`, `widget_on_paint_background` and `ui_loader_load_widget_with_parent` 4.1;
`systembar_showface` 4.2; `list_get_img_pic` 4.4; `playlist_rebuild` 4.7). `bigcover_page_init` is ported (4.6, progress 71).

### Now Playing's owners and pages

`compact_now_playing` opens the page of `media_owner()` (progress 72), with these left as they are:
- **A video (owner 4) keeps the local path.** It has no Now Playing of its own to open, so Hold Return and Home's row open `playing_page` as before.
- **Hold Return again, to go back,** is reachable on a device only from Radio's page, by the held chevron. The chevron is hidden on the local and Spotify pages, and Previous's hold skips both. The suite checks those two by a direct call.
- **Spotify's page has no heart, More, lyrics, info, visualizer or big cover,** and its Mode icon is static: neither backend's contract carries them (progress 71).
- **The Theme's glyph and bold title do nothing on the M1.** It has no on-page `img_playstate` and no bold font (`BOLD_RANGES` is empty), so `np_view_theme` reaches only the album.
- **V2.1's VOLUME page closes 3 s after it opens,** with no check of what is happening on it. That's stock's timer (`0x47d9f8`, in `dialog_volume_dialog_init`). Cancelling it in `vol_paint`'s page 2 branch would keep the page open, if that is ever wanted.

### Games

Games are the iPod UI's. `games.c` has compiled on the M1 since the iPod path did, but its Library row is
`ringnav_localmusic`'s, which the M1 doesn't hook: its Library rows are the Q2 Pod page's
(`m1plus_nav_library.c`), which has no Games row, so they can't be opened. They stay unplanned
within the iPod UI port ([m1plus-ipod-ui.md](m1plus-ipod-ui.md) Phase 4.8), and they changed again in
1.4.2 and 1.4.5 (Snake). They use the Return key, which the M1 lacks, so they need a touch design first.
Card-app games (`addon_game_*`, 1.6.x) have no row either, and the M1's addon caps leave out `game`; the App
Store still lists 1.6.3's Buddy (`q2-fidget`), which installs but can't be opened.

### The extra time zones

V2.1's `select_timezone` is `0x4d6b2c`. It keeps its 27 labels as a `const char *` table at
`0x97c810`, NULL-ended, with the `lan_*` table right after it. Its row layout
(`timezone_listitem_layout`, `0x4a21c8`) copies the table onto its stack (108 bytes, under another
buffer), so the table can't grow. A jal at the label read (`0x4a224c`) that returns the payload's
labels would work instead.

The counts to raise by 11:
- the page builder's `li 29` (`0x4a246c`);
- the click's `sltiu 30` (`0x4a2604`);
- `config_init`'s `sltiu 27` (`0x4e65dc`);
- `select_timezone`'s own (`0x4d6b68`), which the hook covers.

`set_systime` (`0x4d77b0`) and `networktime_adjust_thd` (`0x4d9454`) each have a `sltiu 28` to read
first.

1.5.0 rewrote the table: `TIMEZONES` relabels every row, stock's 27 included ("GMT-12 Baker Island"),
adds five, and `timezone_row` (`autotime_page`'s row builder) shows each row the offset in effect now,
sorted west to east (`TIMEZONE_ORDER`). The M1's header carries the tables; V2.1's row builder is to be
found beside `timezone_listitem_layout`.

### Network Update

It fetches DiamondBond's Q2 `update.tar`, so it stays off until it points at this fork's M1
releases. Its `fwupdate_tf`, stock's TF card update, is `M1PLUS_UNRESOLVED`. V2.1's twin is to be
traced from its updater thread (`0x471070`, which calls `update_firmware`) back to the System Update
row's click.

### Battery fixes

- **The MQA side chain.** The decoder runs only on MQA streams, and the probe is sized to the
  detector. V2.1's `hciplayer` takes `PLAYER_PROFILE`'s words, which don't have these yet.
- **Tidal's stream thread parked.** V2.1 instead creates an on-demand URL worker, at
  `0x51c288`, from `get_tidal_trackurl` (`0x512ed0`). It has no boot worker polling a start
  flag, nor Baidu Pan. The native lifecycle stays and is executed in emulation with mocked
  network/thread endpoints. Live Tidal start/change/stop still needs a signed-in account.
- **The kernel modules' idle clocks** (1.5.0). The Q2 build patches V1.32's `soc_aic.ko` (the stopped
  PCM notifier sleeps), `soc_rotator.ko` (its clock taken at first use) and the PWM driver and MCU
  image (idle clocks gated; MCU sleep, dev only). Each pins the stock module's SHA-256. V2.1's
  modules are to be compared with V1.32's first: the M1's pipeline swaps none. Since 1.6.x (`0405c29`)
  all four are experiments, off by default and `--dev` only, on the Q2 too.

- **Paced player scheduling and command waits** (1.5.5). `MAINSCHEDULING_CALL` needs V2.1's UI
  scheduler call site; `PAUSE_WAIT`, `IDLE_WAIT` and `CMD_DONE` need its command state and player
  sites. The M1 keeps its existing pause sleep and native scheduler.

### FLAC fast paths

1.5.0 patches the Q2's `hciplayer` FLAC decoder (frame sync, LPC and output, on by default) through
`tools/flac.py`. V2.1's `hciplayer` is another build: `PLAYER_PROFILE` takes none of its words, and its
decoder's routines are to be found by the same callers.

### Display's sub-pages

1.5.0 splits Display into Appearance (iPod), Coverflow and Controls, each reopening stock's page with its
own rows. Ported with the iPod settings pages (ipod-ui 4.3, progress 66), device-checked through progress 66 and 68:
- **Appearance:** Theme, Light Mode, Accent, Home and Battery.
- **Coverflow:** Artist Albums, Coverflow Sort and Refresh Coverflow.
- **Controls:** Shortcut, Smart Awake, Hold Return (Recent or Home), then the knob and its direction.

Home (in Appearance) and Shortcut came with Home (4.5, progress 69). The M1's Shortcut offers Favorites, Shuffle,
Rated Albums, Artists and Albums: Rockbox and Games stay Q2-only, and a stored value for either reads as Favorites
until the row is changed. Centred Now Playing came with Now Playing (4.6, progress 71): it opens V2.1's own page. Hold Return is
ported with the Library (4.4): hold Previous in Knob: Navigation wherever it is Back, or hold the status bar
chevron in either Knob mode. Corners (square glass), Wheel QS, Wheel Sensitivity and Click With Headphones (no wheel, no
buzzer) stay Q2-only. V2.1's page reopens over itself as the Q2's does.

### Videos in Folder view

1.5.0's Library Videos row opens Folder view, where `folder_click` (V1.32's `0x521bc4`) plays a video
row in q2video. The M1's Videos row keeps 1.4.5's list (`videos_open`). V2.1's folder row click, bound in
`folder_page_init`'s refresh (`0x5318ac`), is to be found, and whether V2.1's Folder lists video files.
1.5.5's new Folder video listing stays disabled through `LOAD_DIRECTORY_RET = M1_UNPORTED`
until that click handler is ported; shared queue filtering still excludes video records.

### A reboot keeping the place

Restart and the firmware update's dialog save the queue first, as power-off does. V2.1's
`device_reboot` is `0x4e743c`; V2.1 has no `dialog_checkfw_dialog_init` by name, and its updates come
from the card.
On `V054m` a flash and a shell `reboot` both came back to `memoryfile`'s last power-off (progress §72).
Centre's long press offers only Shutdown, and `device_reboot`'s one direct caller is `on_wm_idle_status`, so the
M1 shows no Restart to hook there.

### SyncLink's keys

Eddict Player's play/pause and track keys pass the Buttons lock with the screen off. V2.1's
`main_loop_post_key_event` is `0x693d9c`, but its Buttons lock is its own (`keylock_rows` is native):
check how V2.1's lock treats posted keys first.

### A card app's own icon

A card app shipping `icon.png` or `icon-40.png` shows it on its Streaming row (#88). The M1's Q2 Pod
page draws V2.1's 40 px `stream_app` for every app; `addon_icon` would need the 40 px edition.

### Play/Pause's hold

1.4.5 moves the long press of a spare key code (232, 500 ms) to Play/Pause at 700 ms, in V1.32's
unnamed `input_device_status`. On the M1 the hold menu also opens with a touch long-press. V2.1 uses AWTK's
key-long event after 1000 ms for Play/Pause and Previous; the Q2's 700 ms `HOLD_KEYS` rewrite remains unported.

### Stock's Chinese UI text

1.4.5's `english_ui` gives every Chinese text in stock's UI assets in English, and relabels About's
`system_prove`. The M1's pipeline takes neither: V2.1's assets are to be checked for Chinese text
first.

### q2remote's demo log

`LOG_HOOK` sends demo's output to `/tmp/q2-demo.log` on `--dev` builds, which `q2remote.py log`
reads. The M1's `S90play` is V2.1's; its demo loop is to be checked against the hook's text.

### An artist's albums tab

V2.1 has no `toolsQueryContentDbTable`. Find what V2.1's `getAlbumByAlbumArtist` queries through
first.

### Folder's roots without OTG

Without a drive, the Q2 lists the card alone. Check whether V2.1's Folder lists OTG at all before
porting.

### The Wi-Fi transfer page

The Q2's page is in English and takes folder uploads. V2.1 has `/usr/share/web`, whose files are to be
checked against the patch's strings.

### Quick Settings' brightness

`g_dropdown_menu_state` is a stub on the M1. V2.1 has `dropdown_menu_state` (`0xa05a2c`) and a
`slider_backlight`. Check their states against V1.32's (1, 2 sliding, 3 open) before aliasing it.
1.4.5's `quick_stuck`, which closes a pull-down whose release was lost, reads the same state, so it
never fires on the M1 until then.

### Set Time Manually

V2.1's `datetime_page` has two text-selector views in a `slide_view`; it isn't the Q2's
`manualtime_page`. There, the knob turns the volume. Its row is greyed while Automatic Time Set is
on, so a device check needs that setting off.

### Tidal

On the M1, `tidal_start` passes no song id, because neither of V2.1's two callers (`0x500d5c`,
`0x51c7b0`) keeps one. So Tidal streams uncached, and there is no Downloads row. V2.1's
`get_tidal_trackurl` (`0x512ed0`) hands its URL thread (`0x51c288`) the queue row, so the id is to
be found there. The store pages' knob rows wait for the same check.

1.5.0 loads Tidal's playlists, albums and favourite tracks past stock's first 50: the three list
threads run once a page, their done store nopped (`TIDAL_PAGE_DONE`), and the hooks set the page's flag
after the last. V2.1 has the threads (`0x516b9c`, `0x5178cc`, `0x51b2d4`) and parsers by name, but no
`tidal_albuminfo_thread_run` or `tidal_collection_thread_run`: their flags are to be found.

Nothing in the M1's hardware blocks either. The way in:
1. Read both callers and the URL thread for where the id is and how long it stays valid.
2. Find the id's offset in V2.1's queue row for `REC_TIDAL_ID`.
3. Port [Streaming's Configuration](#streamings-configuration) first, since its cache size caps
   `trim`.
4. Put the Downloads row on the Q2 Pod page, as V2.1 has no Streaming page.

Steps 1 and 2 can be done from the code. The device check needs a signed-in Tidal account.

### Playlist allocation and deletion

1.5.5 allocates playlist IDs under the database lock, independently of display sort order, and
makes deletion transactional. V2.1's allocator and delete callback need their own pinned entry
points before these hooks run. The existing M1 playlist editor remains available.

### MP3 encoder delay and padding

1.5.5 trims an MP3 encoder's delay and padding through four hciplayer sites. V2.1's sites and
private decoder state need to be established before adding the source and hooks to its player
pipeline. The shared seek notification is inert on M1 until then.

### Bluetooth resampler continuity

1.5.6 replaces V1.32's lavcresample open slot (`0x8a4554`, stock `0x4ac2c0`) to retain its
state across gapless changes. The M1 player's profile does not patch that slot; `rs_open` and its
V1.32-only callees are discarded by the linker. Find and pin V2.1's descriptor and callbacks before
porting. Q2's `test/bt_resample.py` covers the actual resampler; it cannot run on this M1 build.

### Coverflow flick gestures

M1 retains `m1plus_coverflow_touch.c` and the existing native `slide_swipe` path. Upstream's new
continuous drag, velocity, rubber band and catch-a-glide handler are Q2-only until adapted to V2.1's
portrait touch events and vertical `slide_menu` layout. Shared caption updates and the insensitive
hidden-covers fix are inherited. The shared wheel animator uses V2.1's easing callback field at
`0x44`, pinned in the build audit; this alone does not enable the new touch handler.

### Directory markers

The sync retains M1's existing spoken-word and hidden-folder filtering. The new `database.ignore`
and `database.unignore` rules await an M1 port: `m1plus_library_scope.c` keeps ordinary SQL unchanged
and leaves stored Favourites, Recent and Frequent lists intact. Its SQL and Era tests explicitly
report `NOT PORTED`. Indexing and explicit playlists continue to use their existing rules.

### Automatic scrobble uploads

The existing manual upload path remains. `ringnav_sleep` does not call the new `scrobble_auto`
scheduler on M1; `[SCROBBLE] AUTO=1` therefore does not start automatic uploads. Scheduling arithmetic
can be tested without enabling the feature.

### Simple EQ's Presets shortcut

M1 keeps its two buttons (Enabled and Reset) and its existing wheel order in
`m1plus_peq_simple.inc`. Presets remain available through Advanced. The new three-button shortcut
needs a portrait layout and a device check; the other shared EQ state improvements are inherited.

### Card apps' library update

1.5.9's request file (`/tmp/q2-<id>.library`: Update Local Music and the app's own playlist import) is
answered on the Q2 alone: `addon_poll` skips `library_poll` on M1, and the caps the apps read leave out
`library`, so an app doesn't ask. The import reads V1.32's Playlists class (`0xf00b`) and patches
`importPlayList`'s listing call (`M3U_DIR_CALL`); V2.1's `importPlayList` is `0x4ef394`, its listing
call not yet found.

### An .lrc's UTF-8 test

1.5.9 replaces stock's `mclIsUtf8WithoutBOM`, which read 6 bytes and no 4-byte character (an emoji, or
Korean's one-syllable words, failed it). V2.1's is `0x5d1824`; whether it has the same fault is not yet
checked.

### A playlist row's hold menu

1.5.9's Play/Pause hold on a Playlists row opens the queue menu (Play Next, Add to Queue, Shuffle,
More…). Ported in the Library item (m1plus-ipod-ui.md 4.4): Play/Pause hold and touch long-press open
`QM_PLAYLIST` on V2.1's numeric playlist rows. More… opens the payload's playlist editor
(`m1plus_nav_playlist_hold.inc`), since V2.1 has no `playlistsmore_page`. New, Import and the Add to Playlist
picker keep their own actions. The dev 57 device pass confirmed the menu and editor.

### Night Shift

1.6.0's Display row warms the screen (`nightshift.c`): while it is on, the screen's lcd `end_frame` is
replaced by `night_end`, which warms the frame's dirty rect in V1.32's `lcd_mem` (`LCD_OFFLINE_FB`,
`LCD_DIRTY`, `LCD_LINE_LENGTH`; `offsets.inc`). The M1's `LCD_*` are `M1_UNPORTED`, `night_paint` returns
at once on M1, and Display's row is the Q2's only: V2.1's `lcd_mem` layout is to be read first (its
`lcd_mem` create and `lcd_end_frame`), and its 320x480 panel is portrait where the Q2's buffer is 375 x 320.

### The watchdog and the crash log

1.6.2 starts `/dev/jz_watchdog` on the UI loop's first pass and feeds it each pass (`wdt_poll`,
`WDT_MS` 60 s, `WDT_LONG_MS` for an import), so a frozen UI restarts the Q2; 1.6.1 keeps
`/mnt/data/q2-state` (`state_poll`) and turns it into `q2-crash.log` on the card after an unchosen
restart. Both return at once on M1 (`if (M1PLUS || ...)`): a watchdog that misfires on V2.1 would
reboot in a loop. To check first: V2.1's kernel has the device and the same ioctls, and that nothing of
V2.1's own (`libhardware2`) already feeds it.

### A USB DAC across a gapless change

1.6.1 replaces ao_alsa's init slot in V1.32's `hciplayer` (`AO_INIT_SLOT`, `ao_init` in
`peq_player.c`) so a USB DAC's PCM stays open across a gapless change, and keeps its 500 ms buffer
(`USB_BUFFER`). The M1 player's profile patches neither; the M1 payload's `--gc-sections` drops
`ao_init`. V2.1's `hciplayer` ao_alsa init and its USB output way are to be found first.

### Enlarged art's reset default

1.5.6's Q2 build changes its default `COVERMODE` from 1 to 0 in the reset config. The M1 build does
not copy that Q2 asset edit. Audit V2.1's own reset defaults before applying it; existing saved
settings are unaffected.

### The settings restack

1.6.4 restacks the settings by use. Playback's library rows move to a Library & Folders page (stock's Playback
page opened again, `library_open` and `playset_sub`, keeping its rows 13 and 14). System gets a Controls row, which
opens Display's Controls page; Key Tone, Click With Headphones, Buttons Lock, Wake and Volume Guard move there.
In-Vehicle Mode (`POD_CARMODE`) and Boot to (`boot_row`) move to Power, and Smart Awake to Display's own page.
Stock's System rows stay, hidden. The M1 keeps its pages as they were: `m1plus_nav_display.c`,
`m1plus_nav_sysset.c` (the iPod's order by role) and `m1plus_nav_audioset.c` (V2.1 rebuilds Playback on each
return to the front). V2.1's System rows differ (Double Tap, the rotation, Format card), its Power page has
no icons, and `reorder`'s row ids are V1.32's. Port it with the next settings pass, by role as
`sysset_ipod_order` does, after Phase 4.7's Quick Settings.

### The stale press backstop

1.6.4 lifts a touch the window manager still holds pressed after `STALE_TOUCH_MS` with no pointer event
(`stale_heal`), and notes each on `--dev` builds in `q2-wheel.log` (`stale_note`, `LOOP_PRESSED`,
`WHEEL_LOG_HOOK`). Its found cause, Wheel QS's lift flooding the UI queue with the touch thread's empty events,
is closed by `main_loop_queue_event`'s leaf (`QUEUE_LEAF`, `ringnav_queue_event`), which also stamps a rim
button for Wheel QS. The M1 has no wheel, so the leaf and the log are the Q2's. `stale_heal` itself would
help the M1's touch, but it reads the last pointer event that `ringnav_input` notes, and the M1's
`ringnav_input` returns before that (`m1plus_nav_input.inc`): it runs on the Q2 only until the M1 notes its
fingers. V2.1's `main_loop_queue_event` (`0x658f18`) is the same leaf.
