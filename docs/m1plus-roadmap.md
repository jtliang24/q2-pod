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
  back one screen. The M1 has no Return key, and Previous, Next and Play/Pause are media keys, as
  on stock: no gesture, hidden tap or key may be a page's only way out. Each new page's
  `test/boot.py` step closes it with the button (`BACK`).

## 1. Small fixes (S)

Done: Crossfade's page on V2.1, the Playback rows that V2.1's list rebuild dropped, and the `test:`
lines that could be ported (see [m1plus-progress.md](m1plus-progress.md), section 14). What is left
here goes with other sections' features:

- **The `test:` lines whose features M1 can't reach yet.** Five lines, each going with its feature:
  - Home's Coverflow card layout, Coverflow's track queue through `mclNextSong`, and other slide
    menus' next and previous: with Coverflow's entry point (section 3) and its scroll distance
    (section 2);
  - the stock key-down helper with STOP (`0x65f688`): with V2.1's copy of that private AWTK
    helper, still to be found (V2.1 binds no key-down handler for the payload to hook);
  - folder rollover and the UI scheduler delay: with the player call sites (section 4).

## 2. Hardware-specific behaviour (M)

- **Touch long-press opens the hold menu.** `NOT PORTED: Rate Album from an artist's albums`.
  - **The problem:** a Play/Pause hold opens the menu for the highlighted row (`qm_hold`). On M1
    nothing highlights a row unless Knob Navigation Mode is on, so the hold falls through to V2.1's
    List sort order dialog. The menu's actions are wired but unreachable. On a touchscreen, a long
    press on the row itself is the natural way in, with or without the knob.
  - **The fix:** in the input hook (`ringnav_input`), treat a press held still on a row or tile as
    its hold. Take the row from the pressed widget's index into `p_deque_showlist`, not from a
    highlight, and enter `qm_hold`'s existing path (`qm_kind`, `qm_cls`, `qm_idx`, `qm_hash`) so
    every action and its checks ("Album changed") stay as they are. Swallow the release, so the row
    doesn't also open.
  - **Coexist with V2.1's touch handling:** a press that moves is a scroll or a swipe and stays
    V2.1's. Leave Play/Pause hold as it is: without a highlight it is still V2.1's sort dialog.
  - **Where it helps.** Each of these is a Play/Pause hold on a highlighted row on the Q2:
    - V2.1's library pages, reachable today:
      - an artist's albums (`album_page`) and Library → Albums (`localclass_page`): the album menu,
        with Add to Favourites and Rate Album (the case that showed the gap);
      - Artists, Composers and Genres (`localclass_page`): Play Next, Add to Queue or Shuffle the
        whole group;
      - All Songs and an album's tracks (`allmusic_page`, `albuminfo_page`): the song menu (Play
        Next, Add to Queue, Favourites, Add to Playlist, Go to Album or Artist, Rate);
      - Folders (`folder_page`), for a folder or a song, and Playlists (`playlist_page`).
    - Q2 Pod's own pages, once their entry points land (section 3). These are payload widgets, so
      the long press can be bound on the row directly:
      - Most Played, the Ratings lists and Long Songs: the song menu;
      - Internet Radio's stations: add to or remove from favourites (`radio_hold`);
      - Spotify's tracks: add to Spotify's queue (`spot_hold`);
      - Coverflow's centre cover: the album menu. Its hold already works without a highlight,
        because the centred cover is the selection, but a long press on the cover is the touch form.
    - Not needed on Now Playing, whose hold menu acts on the playing track.
  - **Test it:** in `test/patch.py`, a still press held on a row of each reachable page opens that
    row's menu and no click, and a moving press doesn't. In `test/boot.py`, a step long-presses an
    album tile on an artist's page; that needs the card library (section 6).
- **Bluetooth absolute volume.** `NOT PORTED: Bluetooth headset volume scaling`.
  - **The problem:** `mclSetBtVol` isn't hooked, so `stock_btvol_trampoline` is a stub. An
    absolute-volume headset gets the volume twice: as AVRCP and as software gain.
  - **The fix:** find V2.1's Bluetooth volume setter (it has no symbol: look for the caller of the
    AVRCP volume D-Bus call), hook it, and turn the Unicorn test back on.
- **Coverflow and Photos scroll distance.** `KNOWN GAP`s.
  - **The problem:** V2.1's `slide_menu` steps by its own height (260 and 450 px), not by
    `slide_menu_item_width` plus a spacer as V1.32's does. Photos leave a black gap mid-swipe, and a
    swipe must travel 450 px.
  - **The fix:** size the slide_menu to one item and draw the neighbours as V1.32 did, or animate the
    payload's own offset instead of the slide_menu's.
  - Both views are unreachable on M1 until there is an entry point (section 3), so do this with or after
    that.
- **The cover-worker mutex.**
  - **The problem:** on M1, `g_playcover_mutex` and `g_lastcover_url` are zero-filled payload storage
    (`m1stub_`). Coverflow's worker therefore isn't excluded from V2.1's player cover thread, which
    writes the same `/tmp/.tmp_picture`. Home's split view also never shows the playing cover.
  - **The fix:** find V2.1's cover mutex and last-cover path (the users of `/tmp/.tmp_picture` in
    V2.1's demo) and alias them in `M1PLUS_CONTEXT_ALIASES`.

## 3. Entry points for Q2 Pod's pages (L)

V2.1 lays out navigation differently from V1.32, so several payload pages have no way in on M1.

Each page reached this way needs a Back button (ground rules):
- **Already have one:** the list pages, through `page_list` and `page_title`. These are Shuffle,
  Ratings, Most Played, Long Songs, Photos' albums and grid, Books' list, and Spotify's and Radio's
  browsers.
- **Still need one:** the full-screen views with no title bar. These are Coverflow's carousel, the photo
  viewer, the book reader and video player, and Spotify's and Radio's Now Playing pages
  (`spotify_page`, `radionp_page`). Add `back_button` to each, over its content.

- **The Library's extras.** `NOT PORTED: Library's Shuffle, Ratings, Most Played and media rows`.
  - **The problem:** V1.32 has a Local Music menu that the payload extends. V2.1's Home carousel *is* the
    library, and `ringnav_localmusic` is bound to `localclass_page_init`, the per-category page.
  - **Options:**
    1. Add Home cards by patching V2.1's `home_page.bin`, as the Q2's Coverflow card does. That needs an
       asset patcher for V2.1's UI format and new card icons.
    2. Add a single "Q2 Pod" Home card that opens a payload page listing Shuffle, Ratings, Most Played,
       Long Songs, Podcasts, Audiobooks, Photos, Books, Videos and Coverflow.

    Option 2 is less invasive, and it fits the build's no-asset-changes M1 policy.
    Either way the new page gets a Back button (ground rules), as must each page it opens.
  - Then unbind `localclass_page_init` from `ringnav_localmusic`.
- **Streaming's Spotify, Internet Radio and AirPlay rows.** `NOT PORTED`.
  - **The problem:** V2.1 has no `stream_page_init` symbol.
  - **The fix:** find the Streaming page's init through the page-name dispatch table, which maps
    `"stream_page"`-like names to init functions (the table that holds `systemset/fwupdate_page`). Hook
    it as a private function (`M1PLUS_PRIVATE_FUNCTIONS`, PIC entry checked). Then the existing
    Spotify and Radio tests can go through the real hook instead of calling `ringnav_stream`.
  - **Device dependency:** librespot's sink and the radio helper use the DAC and ALSA. Check
    `patch/video.c`'s `/dev/shanling_dac` use against the ES9069Q driver first. The device's dmesg
    already shows codec I²C errors at probe.

## 4. Re-pointing V1.32 call-site patches (M each, many)

Each `NOT PORTED` line below names a patch or hook made at a V1.32 address. Porting one means finding the
same call in V2.1 (by the function it sits in and the call it replaces), adding an M1 table entry
beside the Q2 one in `tools/build.py`, and moving the test's address to a per-model table.

| Feature | V1.32 site | Notes |
|---|---|---|
| Shuffle honours Play next | `SHUFFLE_CALL` | mclNextSong's shuffle pick |
| Shuffle's Previous/Next history | V1.32 call-site patches | |
| Playlist rows and click guards | V1.32 playlist builders | |
| LDAC HQ sends 990 kbps | `LDAC_HQ` | switchBtPriority |
| Resume on connect | `BT_CONNECT_START`, `btmenu_rows` | plus the Bluetooth page's row |
| Standby resume stays dark | `STANDBY_WAKE` | device_standby's `awake_screen` |
| Now Playing's info lines | `NP_INFO_CALL` | |
| M4B in folder scans | `AUDIO_EXTENSION_CALLS` | the `strstr` extension checks |
| 65,000-song scan, article-free sort, Artists rows | `SCAN_LIMIT`, `SORT_TRIMS`, `CLASS_ICON` | |
| Same-named albums' art, artist covers | `ALBUM_ART`, `ALBUM_ART_ROW`, `ARTIST_COVER_ROW` | |
| An artist's albums' art keys | V2.1's artist page renderer | the order is ported (`ringnav_localclass`, `0xff01`) |
| Artist pages open on Albums | `ARTIST_ALBUMS` | |
| Artists defaults to Album Artist, read at boot | `read_artistype_value`, `ringnav_bootmode` call | |
| Lock screen Clock row, thumbnails, cover repaint | `screensaver_rows`, `saver_cover` | |
| Key lock and quick lock rows | `keylock_rows`, `quick_lock` | V2.1 may already offer equivalents |
| Ratings' Now Playing heart | `img_fav` binding | |
| Gapless preload across speed changes | `mcl_open_preload` | |
| Keep the page cache | `DROP_CACHES` | `check_mem_thd`'s write |

Check whether V2.1 already has the behaviour before porting it. V2.1 is newer than V1.32, and some of
these may be fixed or offered natively.

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
- **A card library in the emulator.** `test/boot.py` runs with an empty card. A small generated library
  (a few tagged FLAC/MP3 files) would let the walk open Album, Artist and Now Playing. Playback itself
  would still need a stand-in for `hciplayer`'s audio output.
- **An after-boot log on the device.** The `.rockbox/rockbox` diagnostic script can leave a background
  job that writes `ps` and the full `dmesg` a minute after boot. That captures demo crashes and driver
  errors that the emulator can't see.
- **Recovery mode.** The device has a separate recovery system (`kernel2`, `rootfs2`) and an `ota`
  partition. Finding how to start it without demo would give a way back to stock even if demo can't
  start, which would make riskier experiments safe.

## Already Q2-only by design

These are skipped on M1 on purpose (marked `Q2 only` in the tests), not gaps:

- the touch wheel and its sensitivity;
- long Return;
- the sideways splash rotation;
- the Q2's Centre-key Wake setting (V2.1 has its own Double wake);
- Key Tone: V2.1 has no buzzer command, and binds no key-down handler to hook.

The Rockbox dual boot stays: there is no Rockbox for the M1 Plus yet, but the hook serves as a boot-time
diagnostic.
