# M1 Plus: unported features

The upstream Q2 Pod features still unported or awaiting validation after the 1.5.8 sync (`staging`;
`1.4.2-m1.1` is the last release). Each row has a status:

- **Planned:** to be ported. Most have a known way in on V2.1, or a check to make first.
- **Native; live validation pending:** the firmware already provides the behavior; account-dependent checks remain.
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
| [The iPod UI](#the-ipod-ui) | 1.2.2 or earlier | `playlist_rebuild`, `widget_on_paint_background`, `bigcover_page_init`, `style_get_color`, `image_manager_add`, `list_get_img_pic`, `systembar_showface` (1.4.5); Light Mode, Corners and the new accents (1.5.0); `ui_loader_load_widget_with_parent`, Centred Now Playing, Smart Awake, bold font, Home art pan (1.5.8) | Unplanned |
| [Games](#games) | 1.3.9 | `games.c`, the iPod UI's Games row | Unplanned |
| [The extra time zones](#the-extra-time-zones) | 1.2.9 | `select_timezone`; `timezone_row`, `TIMEZONES` (1.5.0) | Planned |
| [Network Update](#network-update) | 1.3.8 | `systemset_fwupdate_page_init`, `netupdate.c`, `fwupdate_tf` | Planned |
| [Battery: the MQA side chain](#battery-fixes) | 1.2.9 | `MQA_GATE`, `MQA_PROBE` (`tools/peq.py`) | Planned |
| [Battery: Tidal's stream thread parked](#battery-fixes) | 1.4.5 | `STREAM_POLL_CALLS` and `get_tidal_trackurl` (1.5.0; 1.4.5's `STREAM_POLLS`) | Native; live validation pending |
| [Battery: the kernel modules' idle clocks](#battery-fixes) | 1.5.0 | `tools/aic.py`, `rotator.py`, `pwm.py`, `mcu_park.py` (`--aic-idle-wait`, `--rotator-lazy-clock`, `--pwm-idle-clock`, `--mcu-idle-sleep`) | Planned |
| [FLAC fast paths](#flac-fast-paths) | 1.5.0 | `tools/flac.py`, `patch/flac_*.c` (`tools/peq.py`, `--flac-experiments`) | Planned |
| [Display's sub-pages](#displays-sub-pages) | 1.5.0 | `ringnav_display`'s Appearance, Coverflow and Controls, `display_sub` | Planned |
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

Era, Western tag/CUE text, hidden-folder exclusions, Streaming Configuration, user-space idle
changes and lyrics passed the combined device checks in [progress section 50](m1plus-progress.md#50-five-feature-batch-on-150-oct-28).
The [validation record](m1plus-validation-1.5.0.md) retains limits of the hardware pass, including
album-worker cancellation and USB-storage shutdown covered in emulation, and the live Tidal exception.

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

Unplanned (the user's choice, Oct 26): the form factors are too far apart for a straightforward port.
The iPod UI is built for the Q2's 375x320 landscape screen and touch wheel, and patches V1.32's UI
assets, styles and code layout. On the M1 Plus's 320x480 portrait touchscreen and knob it would be a
redesign, not a port, and the M1 keeps V2.1's own look instead (roadmap section 5). Its iPod hooks stay
`q2only` in the port report.

### Games

Games are the iPod UI's: their Library row is `#if IPOD` (`patch/navigation.c`), the iPod UI is
unplanned, and they changed again in 1.4.2 and 1.4.5 (Snake). They use the Return key, which the M1 lacks, so they need a touch design first.

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
  modules are to be compared with V1.32's first: the M1's pipeline swaps none.

- **Paced player scheduling and command waits** (1.5.5). `MAINSCHEDULING_CALL` needs V2.1's UI
  scheduler call site; `PAUSE_WAIT`, `IDLE_WAIT` and `CMD_DONE` need its command state and player
  sites. The M1 keeps its existing pause sleep and native scheduler.

### FLAC fast paths

1.5.0 patches the Q2's `hciplayer` FLAC decoder (frame sync, LPC and output, on by default) through
`tools/flac.py`. V2.1's `hciplayer` is another build: `PLAYER_PROFILE` takes none of its words, and its
decoder's routines are to be found by the same callers.

### Display's sub-pages

1.5.0 splits Display into Appearance (iPod), Coverflow and Controls, each reopening stock's page with its
own rows. The M1 keeps one list (`m1plus_nav_display.c`): its Controls would hold the knob rows alone,
with no Return key for Hold Return and no wheel for Wheel QS or Wheel Sensitivity. Worth porting only if
Display grows; V2.1's page reopened over itself is to be checked first.

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

### SyncLink's keys

Eddict Player's play/pause and track keys pass the Buttons lock with the screen off. V2.1's
`main_loop_post_key_event` is `0x693d9c`, but its Buttons lock is its own (`keylock_rows` is native):
check how V2.1's lock treats posted keys first.

### A card app's own icon

A card app shipping `icon.png` or `icon-40.png` shows it on its Streaming row (#88). The M1's Q2 Pod
page draws V2.1's 40 px `stream_app` for every app; `addon_icon` would need the 40 px edition.

### Play/Pause's hold

1.4.5 moves the long press of a spare key code (232, 500 ms) to Play/Pause at 700 ms, in V1.32's
unnamed `input_device_status`. On the M1 the hold menu also opens with a touch long-press. V2.1's
routine and its key code are to be found.

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

### Enlarged art's reset default

1.5.6's Q2 build changes its default `COVERMODE` from 1 to 0 in the reset config. The M1 build does
not copy that Q2 asset edit. Audit V2.1's own reset defaults before applying it; existing saved
settings are unaffected.
