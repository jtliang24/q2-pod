# M1 Plus: unported features

The upstream Q2 Pod features that the M1 Plus doesn't have yet, as of 1.4.2-m1.1. Each row has a
status:

- **Planned:** to be ported. Most have a known way in on V2.1, or a check to make first.
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
| [The iPod UI](#the-ipod-ui) | 1.2.2 or earlier | `playlist_rebuild`, `widget_on_paint_background`, `bigcover_page_init`, `style_get_color`, `image_manager_add`, `list_get_img_pic` | Planned |
| [Games](#games) | 1.3.9 | `games.c`, the iPod UI's Games row | Unplanned |
| [The extra time zones](#the-extra-time-zones) | 1.2.9 | `select_timezone` | Planned |
| [Network Update](#network-update) | 1.3.8 | `systemset_fwupdate_page_init`, `netupdate.c`, `fwupdate_tf` | Planned |
| [Battery: `check_mem_thd` returning at once](#battery-fixes) | 1.2.9 | `DROP_CACHES` | Planned |
| [Battery: the MQA side chain](#battery-fixes) | 1.2.9 | `MQA_GATE`, `MQA_PROBE` (`tools/peq.py`) | Planned |
| [Battery: Wi-Fi power save](#battery-fixes) | 1.3.0 | `WIFI_LPS` | Planned |
| [Streaming's Configuration](#streamings-configuration) | 1.2.9 | `stream_config` | Planned |
| [An artist's albums tab's album-artist rewrite](#an-artists-albums-tab) | 1.2.9 | `toolsQueryContentDbTable` | Planned |
| [Folder's roots without OTG](#folders-roots-without-otg) | 1.2.2 | `folder_load_top` | Planned |
| [The Wi-Fi transfer page](#the-wi-fi-transfer-page) | 1.3.0 | `WEB` | Planned |
| [Quick Settings' brightness through a swipe up](#quick-settings-brightness) | 1.3.8 | `g_dropdown_menu_state` | Planned |
| [Knob: Navigation on Set Time Manually](#set-time-manually) | the M1's own | an `m1plus_contexts.inc` row | Planned |
| [Tidal's cache and Tidal Downloads](#tidal) | 1.2.2 | `tidal_play`, `tidal_downloads`, `REC_TIDAL_ID` | Unplanned |
| [Knob: Navigation on the Tidal and HiFi store pages](#tidal) | the M1's own | `m1plus_contexts.inc` rows | Unplanned |

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

Roadmap section 5 (L). It comes after the catch-up's ports. Its six hooks are `q2only` in the port
report until then.

### Games

Games are the iPod UI's: their Library row is `#if IPOD` (`patch/navigation.c`), and they changed
again in 1.4.2. They use the Return key, which the M1 lacks, so they need a touch design first.

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

### Network Update

It fetches DiamondBond's Q2 `update.tar`, so it stays off until it points at this fork's M1
releases. Its `fwupdate_tf`, stock's TF card update, is `M1PLUS_UNRESOLVED`. V2.1's twin is to be
traced from its updater thread (`0x471070`, which calls `update_firmware`) back to the System Update
row's click.

### Battery fixes

- **`check_mem_thd` returning at once** (`DROP_CACHES`' 1.2.9 form). The M1 keeps 1.2.2's form,
  `check_cpumem`'s write branched over. Check what else V2.1's thread does first.
- **The MQA side chain.** The decoder runs only on MQA streams, and the probe is sized to the
  detector. V2.1's `hciplayer` takes `PLAYER_PROFILE`'s words, which don't have these yet.
- **Wi-Fi power save.** V2.1's demo has the same `rtwpriv wlan0 pm_set lps=0` string, so this is a
  string patch to port.

### Streaming's Configuration

This covers the cache sizes and Stop Streaming Services. On the M1 it would be a row on the Q2 Pod
page, with one of V2.1's icons; the Q2's icon is the one there now.

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

### Set Time Manually

V2.1's `datetime_page` has two text-selector views in a `slide_view`; it isn't the Q2's
`manualtime_page`. There, the knob turns the volume. Its row is greyed while Automatic Time Set is
on, so a device check needs that setting off.

### Tidal

On the M1, `tidal_start` passes no song id, because neither of V2.1's two callers (`0x500d5c`,
`0x51c7b0`) keeps one. So Tidal streams uncached, and there is no Downloads row. V2.1's
`get_tidal_trackurl` (`0x512ed0`) hands its URL thread (`0x51c288`) the queue row, so the id is to
be found there. The store pages' knob rows wait for the same check.

Both are unplanned until there is a Tidal account to check them on.
