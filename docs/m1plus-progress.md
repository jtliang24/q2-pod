# M1 Plus port: work done and why

This is the history of porting Q2 Pod to the Shanling M1 Plus (firmware V2.1): what was changed, in
what order, and why. It runs from the feasibility study on `main` to firmware verified on the device.
What is left is in [m1plus-roadmap.md](m1plus-roadmap.md). The hardware and firmware analysis is in
[m1plus.md](m1plus.md).

Commits are listed oldest first. Where a commit's message gives its reason, that reason is
summarised. Where it doesn't (several early feature commits have a subject line only), the purpose is
inferred from what the commit changed and is marked *(inferred)*.

## Timeline

| When | Stage | Commits |
|---|---|---|
| Oct 15–16 | Feasibility study, on `main` | `ac5a498`, `09020b6`, `b229c24` |
| Oct 16 | First port: every part of Q2 Pod given an M1 Plus path | `09dba3a` … `31b83db` |
| Oct 16 | Correction pass: V1.32 assumptions found and replaced with V2.1's | `c404855` … `17e143b` |
| Oct 17 | Completion and M1 Plus support in the tests | `e6032d4` … `68358fe` |
| Oct 17 | Review, then honest tests and tooling | `2aa5185` … `7893fb5` |
| Oct 17 | Assumptions turned into checks | `bed13e5` … `028a13e` |
| Oct 17 | V2.1's whole demo under emulation | `9ab2a38` … `72c3310` |
| Oct 17 | First device test, then fixes from it | `75bc4b3` … `d2fbfe5` |
| Oct 17 | Keys in the emulator, second device test | `c265690`, `15f52d2` |
| Oct 17 | A Back button replaces the edge swipe, third device test | `117bbc9` … `82c2866` |
| Oct 18 | An artist's albums on V2.1 | `063416d` … `944ac29` |
| Oct 18 | Previous is a media key again | `47ee97e` … `3f74f4c` |
| Oct 18 | The roadmap's small fixes | `5b7bb1d` … `994451b` |

The branch leaves `main` at `b229c24`. There are 85 commits on `feature/m1plus-port`.

## 1. Feasibility study (on `main`)

- **`ac5a498` M1 Plus porting document.** The first version of [m1plus.md](m1plus.md): a study of
  whether Q2 Pod could run on the M1 Plus *(inferred)*. Both players are Ingenic X2000 devices running
  the same AWTK-based `demo`, `hciplayer` and SQLite stack, so the payload approach (patch `demo`, append
  code, hook functions) should carry over. The differences that shape the port:
  - a 320x480 portrait screen instead of the Q2's 375x320 sideways one;
  - a touchscreen and a knob instead of a touch wheel;
  - no Return key;
  - a different DAC.
- **`09020b6` versioning.** Pins the port's base to an upstream Q2 Pod release (v1.2.1 at the time).
  That gives a fixed set of features to carry over.
- **`b229c24` further exploration.** Expands the study into the porting plan, which covers:
  - how `update.bin` is packaged (a plain tar of kernel, rootfs and an MD5 list);
  - the input devices and their key codes;
  - the display geometry;
  - the list of hooks and V1.32-only call sites to re-point.

  It is the branch point.

## 2. First port (Oct 16)

Each part of Q2 Pod got an M1 Plus path, mostly behind `#if M1PLUS` so the Q2 build stays as it was.

| Commit | Change | Purpose |
|---|---|---|
| `09dba3a` | q2boot, q2remote and q2video for M1 Plus | The helper programs assumed Q2 hardware *(inferred)*. q2boot reads Play/Pause at boot for the Rockbox dual boot, and the M1's key is `KEY_PLAYPAUSE` (164), not the Q2's 108. q2video checked for a 320x375 framebuffer and rotated video for the sideways screen. |
| `2f14003` | `flake.nix` devShell | A reproducible toolchain (clang, lld, squashfs-tools, Python), so builds don't depend on the host *(inferred)*. |
| `a1ac12f` | `hciplayer` and the PEQ patch for M1 Plus | V2.1's `hciplayer` is a different binary. `tools/peq.py` gained per-firmware profiles (the EQ descriptor, VBR scan, rate gates, seek slot, ID3 calls) chosen by the binary's SHA-256, so the PEQ and ReplayGain patch the right addresses. |
| `6cca35f` | Portrait 320x480 geometry without corner insets | Every payload page was laid out for the Q2's 375x320 rounded screen. `offsets.inc` gained M1 values (`UI_W`, `UI_H`, `BOTTOM`, no `CORNER_R`), and the pages (Coverflow, Photos, Books, Spotify, Radio, the PEQ editor, the lock screen) were moved to them *(inferred from the files changed)*. |
| `e9b61f7` | Return synthesis and Knob Navigation Mode | The M1 has no Return key, which Q2 Pod's own pages rely on to close. `dispatch_key_return` was added, with three ways in: a left-edge swipe, a tap on a page title and Previous. A "Knob: Volume/Navigation" setting would let the knob scroll lists. |
| `c972599` | The M1 Plus build target | `tools/build.py` learned to recognise V2.1's `update.bin`, resolve V2.1's symbols, install `M1PLUS_HOOKS`, set V2.1's version literal and pack an `update.bin`. This is the commit that makes an M1 firmware at all. |
| `aa8195c` | Docs | README, `building.md` and `m1plus.md` updated for the new target. |
| `31b83db` | graphify in the devShell | Tooling for navigating the codebase. |

## 3. Correction pass (Oct 16)

Going back over the port, many V1.32 values turned out to be wrong for V2.1. Each commit below fixes
one class of mistake, and its message records how V2.1's own code showed the right value.

| Commit | Fix | Why it mattered |
|---|---|---|
| `c404855` | `pic_gp` helper | Factors out the check that a hook target starts with a PIC prologue computing the expected GOT base, so the M1 checks can reuse it for V2.1 routines. |
| `0807405` | V2.1's `slide_menu` and animator layout | V2.1's `slide_menu` has no spacer and no item-width routine, and its fields moved. With V1.32's values, the Home wheel and Coverflow called a V1.32 address on every paint. |
| `0d78bfd` | V2.1 addresses for queue, scan, key latch, mixer and Bluetooth state | V1.32's raw addresses fall in V2.1's heap, so every read was garbage and every write corrupted memory. The values were re-derived from V2.1's getters. Code for things V2.1 doesn't have (the wheel lockout, the Return latch) is compiled out. |
| `787497b` | Symbols resolved against V2.1, not V1.32 | Missing globals had been placed inside the payload's own state (`g_carmode` landed on `st`), and V1.32 private routines were merged into V2.1's table. Names now resolve through size-checked aliases, and anything unmatched gets zeroed storage of its own (`m1stub_`). |
| `8cd5dd9` | An in-place erase instead of a `deque_pop_back` fallback | V2.1 doesn't import `deque_pop_back`. The fallback rebuilt deques with the wrong element type and freed memory twice. |
| `cd44b3d` | Payload key replays go to the stock key-up handler | On V2.1 the payload hooks `on_wm_keyup_fun` itself, so its replays re-entered the hook. |
| `24788ba` | V1.32 click handlers kept out of ratings and playlists | `FAV_CLICK` and `PLAYLIST_PICK` are V1.32 addresses, so calling them on V2.1 would jump into unrelated code. |
| `f97348e` | V2.1's sortselect dialog in the Play hold menu | V2.1 names the dialog's widgets differently, so the menu looked up missing widgets. |
| `7a658b3` | Crossfade leaves V2.1's Boot volume page alone | V2.1's page has other widgets and handlers, so it can't be re-dressed the way V1.32's was. |
| `a568a1c` | Tidal streams without the cache when the song id is unaudited | V2.1's two callers weren't checked to hold the song id where the payload reads it. |
| `044bd70` | The title-tap Return is deferred out of the click dispatch | The Return closes the page, which could free the title while its own click was still running. |
| `8d2f6e8` | The RTC is read as UTC on M1 too | The build writes the RTC in UTC. V2.1 also reads it back at each start as local time, which would shift the clock by the time-zone offset. |
| `fe4ab48` | `bluealsa` pinned by SHA-256 | Its patch uses fixed addresses, and the binary is byte-identical in V1.32 and V2.1. A different binary now fails the build. |
| `99d099d` | V2.1's AWTK event numbers | V2.1 numbers its key, focus, value and window events differently. Each value was read from the same stock function in both firmwares. |
| `f1d4b65` | V2.1's widget, emitter and canvas offsets | `widget_t` has one field fewer before `parent`, so the payload's paint paths dereferenced the wrong fields. |
| `835752f` | Previous and Next key codes | The codes were swapped, so Back-to-Return fired on Next. |
| `5e57c59` | Media keys taken before V2.1's key-up handler | V1.32 has a key-up filter the payload hooks. V2.1 has none, and its handler plays and skips as it runs, so the payload has to act first. |
| `fe4d898` | Function aliases corrected | `stop_player` matches V1.32's `player_stop`. A rounded-rect alias pointed at a function taking six arguments instead of two. |
| `17e143b` | Global aliases corrected | Matched by the functions that use them in both firmwares. Aliasing `g_artist_type` to `artist_type` would have overwritten the user's Artists setting, so it gets its own storage. |

The lesson of this pass: a V1.32 name or address that "looks right" on V2.1 is a guess until the same
code in V2.1 is read. That method (same-named function, compare its loads, stores and constants)
carried through the rest of the work.

## 4. Completion and test support (Oct 17)

| Commit | Change | Purpose |
|---|---|---|
| `e6032d4` | Ignore the build folder | Keep generated firmware out of git *(inferred)*. |
| `4033cf6` | Unicorn, fontTools and ImageMagick in the devShell | Dependencies of the test suites and the build's asset steps. |
| `3d252f6` | The ID3 ReplayGain hook and `AVDictionary` offset for M1 | MP3 ReplayGain hooks `hciplayer`'s ID3 walker. V2.1's has a third call site and a different dictionary layout *(inferred from the diff)*. |
| `bc427d6` | The last AWTK offsets, symbol bindings and input handling | More widget and animator offsets, V2.1's `input_device_status` location, and two more function aliases. The Display settings, including the knob setting, were reorganised for M1 *(inferred from the diff)*. |
| `68358fe` | M1 Plus in the MIPS test suites | `test/patch.py`, `playback.py`, `m4b.py`, `id3.py` and `headset_io.py` learned to load an M1 build: V2.1's symbols and offsets and the `M1PLUS_HOOKS` table. This is the first emulated coverage of the M1 payload. |

At this point the branch built an M1 firmware and its unit tests passed.

## 5. Review, then honest tests and tooling (Oct 17)

A code review of the branch found ten problems:
- **Silent no-ops:** features that did nothing on M1. Streaming's rows had no hook; the Knob mode
  setting could never be read; Bluetooth absolute volume wasn't hooked; most of the Q2's call-site
  patches were skipped.
- **Tests that couldn't fail:** two assertions compared a value with itself, and one test faked a hook
  the M1 build never installs.
- **No M1 support in `test/build.py`:** it crashed on an M1 build.
- **Stale build folders:** they still bound hooks to V1.32 addresses.

The decision was to make the tests and tooling honest first and boot-test on the device before fixing
features. A wrong boot path is the expensive mistake. A missing feature is not.

| Commit | Change | Why |
|---|---|---|
| `2aa5185` | Accept only audited firmware inputs, including the M1 Plus ZIP | A bare Q2 `update.tar` skipped the hash check, so hard-coded addresses could be patched into an unknown binary. |
| `21afeed` | Refuse `--ipod` for M1 | The iPod UI patches are Q2-only. An M1 "iPod" build was stock UI labelled `V122I`, and the tests then ran Q2 addresses inside V2.1. |
| `141b837` | `PDR_M1PLUS` | So the tests check the zeroed `.pdr` against the build's own constant. |
| `c64f1f3` | `logo_source` in the manifest | Without `--logo`, an M1 build silently keeps V2.1's splash, because `assets/boot-logo.jpg` is the Q2's size. |
| `c5ccdd9` | Boot and splash scenarios run on the image's whole init scripts | Testing only the hook fragments would miss a script that patches cleanly but no longer boots. |
| `64cac73` | `test/build.py` audits M1 builds | Checks the hook jumps and their GOT base, a demo diff limited to audited sites, a rootfs diff limited to named files, and the boot hook's environment. |
| `ac09714` | Hooks a test enters must be ones V2.1 installs; `known_gap()` and `not_ported()` | Replaces the faked hook and the two always-true assertions. Roughly 35 silent skips now print their reason. |
| `7e5fa57` | Tests for Return gestures, locked Back and knob mode | Navigation on the M1 depends on these, and none was tested. |
| `2d2b4d5` | `id3.py` and `playback.py` | A printed claim that wasn't checked is now asserted, and the skips are named. |
| `7893fb5` | `docs/building.md` | Inputs, the splash rule and the test markers. |

Each new check was proven able to fail against a deliberately broken copy of the build.

## 6. Assumptions turned into checks (Oct 17)

Listing how the codebase knew the M1 build would work showed several facts that had been checked only
by hand. These became tests:

| Commit | Check | Why |
|---|---|---|
| `bed13e5` | V2.1's updater rule, read from `update_firmware` | The model must match and the version must differ, or the card's `update.bin` is refused. The test pins those comparisons. This was the main unknown on the way to flashing. |
| `3ab9f3b` | The squashfs keeps stock's compression and block size; the archive keeps stock's tar layout and correct MD5s; each helper's loader and libraries exist in the rootfs | The build hard-codes lzo, which only happened to match, and the rest was unchecked. |
| `5dfe810` | The harness uses V2.1's window-manager vtable, read back from V2.1's code | It had been writing V1.32's. |
| `028a13e` | `docs/m1plus.md` | Records the updater rule, and what only the device can verify. |

## 7. V2.1's whole demo under emulation (Oct 17)

Unit tests mock the toolkit and share `offsets.inc` with the payload, so a wrong M1 offset passes both.
A crash in demo's startup would also boot-loop the device.

- **`9ab2a38`:** QEMU and bubblewrap in the devShell.
- **`edf0993`, `test/boot.py`:** runs stock and patched demo side by side under `qemu-mipsel`, sandboxed,
  with V2.1's own `dbus-daemon`.
  - A preloaded shim provides a file-backed framebuffer and the device's serial number. Without a
    serial, Home shows "SN Error" and stops setting up.
  - The patched demo must stay up as long as stock, draw the same Home, and enter the payload through
    its startup hooks.
  - It was shown to fail on a build that crashes at startup, and on one whose hook was left unpatched.
- **`72c3310`:** docs.

## 8. First device test

The build flashed through V2.1's own menu updater (System Update → TF card update) and booted, but it
looked exactly like stock:

1. **About showed `V122S` and no CFW row.** The hook looked its list up by V1.32's name.
2. **No Q2 Pod settings appeared.** Same cause, on every settings page.
3. **The PEQ editor had no way out.** The edge swipe did nothing.
4. **A boot stalled on the logo.** The cause was a diagnostic script at `/.rockbox/rockbox` that never
   exits. Q2 Pod's dual boot runs that file before demo. Its log also gave the flash layout: a 75 MiB
   rootfs partition and a separate recovery system.

Also confirmed:
- the menu updater works both ways (stock → V122S → stock);
- a card `update.bin` alone does nothing at power-on;
- the RTC-in-UTC patch keeps the clock right.

## 9. Fixes from the device test (Oct 17)

Touch input was added to the emulator first, so each fix could be checked on V2.1's real widgets
before flashing. The shim stands in for tslib and replays touch samples.

| Commit | Change | Why |
|---|---|---|
| `75bc4b3` | Nine V1.32 style names become per-model `STYLE_*` macros | V2.1 has none of them, so AWTK drew the payload's widgets in its light default. |
| `60a054e` | About and settings rows in V2.1's lists and row format | Lists, icons and row parts are named per model. About rewrites V2.1's `"%s:%s"` version row and adds a CFW row. `list_row` builds V2.1's row. Rows appear on the Playback, Idle and Display pages. Q2-only rows are dropped, as are V1.32's row orders. |
| `5b37b2e` | The edge swipe works as Return | See below. |
| `bf91fbd` | The EQ's Simple tab and tab bar derive from the screen width | They were painted for 375 px, so they were cut off at 320 px. |
| `f33a93c` | The M1 build refuses any payload name V2.1's assets lack | Makes that whole class of bug impossible to ship. |
| `6771632` | `test/boot.py` walks the UI by touch, stock against patched | Each screen must match stock or differ only where the payload changes it, and the swipe must close the EQ. |
| `07e7ca0`, `d2fbfe5` | Docs, including the flash layout | |

**Why the edge swipe failed (`5b37b2e`).** There were two causes:
- **Wrong event type:** V2.1's touch thread queues a press as `0xff`, and the code waited for the window
  manager's `0x100`.
- **Unpaired Return:** the Return was a release alone, which the window manager drops.

The fix:
- **Edge presses are held:** a press in the left edge strip is kept from the page.
- **A swipe right becomes Return:** sent as a press and release, with nothing of the touch reaching the
  page.
- **Anything else is replayed:** a tap or other drag gets the held press first, so the title-bar back
  button and sliders still work.

The original unit test had used the wrong event type and passed. It now replays V2.1's own sequence.

## 10. Keys, and the second device test (Oct 17)

**`c265690`, `15f52d2`.** The emulated button and knob devices are now FIFOs that the test writes key
events to. The walk turns the knob on both demos, and presses Previous on the patched one, which must
close the EQ.

**On the device,** the fixed build (`update.bin` `1c6512f5…`) checked out:
- About shows "FW. Version:V2.1" and "CFW. Version:1.2.2";
- the Playback, Idle and Display rows work;
- the edge swipe, the title-bar back button and Previous all act as Back;
- the PEQ fits the screen and works with music;
- settings survive a reboot.

## 11. A Back button replaces the edge swipe, and the third device test (Oct 17)

Q2 Pod's pages were left by gestures that nothing on screen showed: the left-edge swipe and a tap on
the page title. Previous also acts as Back, but only while nothing plays. So with music on, those
hidden gestures were the only way out of the PEQ editor.

The swipe also cost the most of anything in the port:
- **It sat in front of every touch, on every page, stock pages included.** It held back each press in
  the left 32 px until the touch turned out to be a swipe, then replayed it.
- **It needed a device fix.** It had the wrong event type and an unpaired Return (section 9).

V2.1's own pages use a visible title-bar back button, so Q2 Pod's pages now use the same one:
- **`back_button`** (`patch/coverflow.c`) copies V2.1's `btn_return`: the style
  `navbar_btnreturn_style`, the icons `return` and `return_down`, and its place at the top left.
  These names are in `offsets.inc`, so the build checks them against V2.1's theme.
- **Its click sends Return on a timer,** as the title tap did. The page's keyup decides what Back
  means: the PEQ's Advanced tab steps back one screen, and its Home closes.
- **`page_title` adds the button,** so every titled payload page has one. The PEQ editor's title bar
  adds it too; its tabs now start after the button.
- **`edge_swipe` and the title tap are gone.** Touches reach stock as they arrive.

**Tests.**
- `test/patch.py` checks the button's style, icons and place, that its click sends exactly one
  Return on the timer, and that a swipe from the edge now reaches stock unchanged.
- `test/boot.py` closes the EQ with the button. It also opens Advanced and its Preamp screen, and
  checks that Back returns to Advanced before a second Back closes the page.

**Commits:** `117bbc9` (the button), `ae3c58f` (the swipe removed), `d1e596b` (the boot walk) and
`82c2866` (docs).

**On the device,** a `--dev` build (`update.bin` `88246102…`, tag `V001s`) installed through the menu
updater directly over `V122S`. The updater takes a new tag, so it didn't need stock first. Then:
- About shows "CFW. Version:1.2.2 dev 1";
- the PEQ editor's Back button closes it from Simple and from Advanced's first screen;
- from Advanced's Preamp, Balance, band and Presets screens, Back returns to Advanced;
- a drag from the left edge of a stock page (a list, a slider) behaves as on stock.

From now on, every page on M1 has an explicit Back button. The rule is in
[m1plus-roadmap.md](m1plus-roadmap.md)'s ground rules and in [m1plus.md](m1plus.md) §4.1.

## 12. An artist's albums on V2.1 (Oct 18)

V1.32 lists an artist's albums through `load_localartist_list`, which Q2 Pod hooks to order them by
year (or A–Z) and to keep each row's album for Rate Album. V2.1 has no such function. Its
`album_page_init` calls `loadAlbumList`, which saves the artist in `classinfo_save` and runs
`loadLocalClassList(0xff01)`. So on M1 the albums stayed in stock's order. Every artist albums test
was V1.32-only, and the one `NOT PORTED` line named only the art keys, so nothing showed the order
was missing.

| Commit | Change | Why |
|---|---|---|
| `063416d` | The `QueueMachine` calloc mock rounds to a word | A byte-sized calloc (`coverflow_by_year`'s taken flags) left every later allocation misaligned, and the payload's next word store faulted. |
| `d28932e` | An album artist's songs come from V2.1's album query | V2.1 has no `getMusicByAlbumArtist`, and `peq.h` stood `getMusicBySonger` in for it, so with Album Artist browsing the songs came from the Artist tag. `getMusicByAlbumAndAlbumSonger`, with its drop-the-album flag set, is the query. |
| `11adf1e` | An artist's albums by year or A–Z | The work is now `artist_tab`. `ringnav_localclass` calls it for `0xff01` on M1, before `albumcoverinfo_init` builds the covers. M1's tests load the albums through the real hook. |
| `315e805` | The ranking SQL runs on SQLite with stock's `songtable` | The C tests' canned rows answered any ORDER BY, so only the SQL's text was checked. |
| `5a2c73d` | Docs | How V2.1 loads an artist's albums. |
| `3b0f6e8`, `ad6dbf4` | Rate Album on an artist's albums marked `NOT PORTED` | The hold menu acts on the highlighted row, and nothing highlights one on M1, so a Play/Pause hold falls through to V2.1's List sort order dialog. The test highlights the row itself, so it checks the wiring only. |
| `944ac29` | Roadmap: a touch long-press opens the hold menu | It is the natural way in on a touchscreen, with or without the knob. |

## 13. Previous is a media key again (Oct 18)

The M1 has no Return key. `e9b61f7` made Previous act as Return while nothing played, because
Q2 Pod's pages then had no visible way out. Since section 11 every page has a Back button, so
Previous-as-Return was a hidden second path, and it had a bug:
- **It ran before the key lock.** `ringnav` turned Previous into Return before it tested `locked`
  and before stock's key-up ran.
- **Its Return skipped the screen-off drop.** On the Q2, `wake_gate` drops Return while the screen
  is off, so a bump of Back leaves the page alone. `dispatch_key_return` calls the stock input
  handler directly and skips that check.

So with the screen off and nothing playing, a bump of Previous in a pocket closed a page nobody could
see, locked or not. The roadmap listed this as `KNOWN GAP: Back with the screen off and the keys
locked sends Return to the hidden page`.

The fix removes the path. Previous goes through the key lock and `media_key`/stock, as Next and
Play/Pause do, and acts as it does on stock V2.1. The Back button is the only Return.

**Tests.**
- `test/patch.py`: Previous dispatches no Return and reaches stock's key-up, both idle and with the
  screen off and the keys locked. On Now Playing it dispatches no Return either. The known gap is
  gone.
- `test/boot.py`'s `eq_previous` step presses Previous with the PEQ editor open, and the editor
  must stay as it was.
- Both fail against the old code.

**Commits:** `47ee97e` (the fix and its tests), `e605e6b` (Back is M1's only Return, in
m1plus.md, building.md and the roadmap's ground rule) and `3f74f4c` (the roadmap brought up to
date with the code).

## 14. The roadmap's small fixes (Oct 18)

**Crossfade's page on V2.1.** Until now Crossfade's row only switched between Off and the saved
length, because `crossfade.c` knew only V1.32's Boot volume page. V2.1's page was mapped from its
asset and its init: `playset_bootvol_page_init` binds in a `widget_foreach` visit (`0x49cf60`).
The switch is a settings row, `btn_memory` (`0x49d328`). The minus and plus are the buttons
`btn_dec` (`0x49d39c`) and `btn_add` (`0x49d4c8`). `vol_slider` has `EVT_VALUE_CHANGING` only
(`0x49d418`). `xfade_open` now re-dresses this page as it does V1.32's, with its names in
`offsets.inc` (`VIEW_BOOTVOL*`, `ICON_SWITCH_*`). Two things came out of reading V2.1's code:
- **V2.1 disables the view it hides.** With Volume memory on, V2.1 also disables `bootvol_view`,
  so a page that was only shown again would have had a dead slider. `xfade_open` enables it too.
- **The slider takes doubles.** V2.1 passes `slider_set_value` a double in `$a2:$a3`, as
  `tools/build.py`'s prototypes already said.

**Playback's rows after a sub-page.** V2.1's Playback init binds `EVT_WINDOW_FOREGROUND` (`0x12d`)
to `0x4a0c50`, which empties the list and builds stock's 16 rows again. So the payload's rows
(Year Order, Artists, Artist Album Order, Crossfade) disappeared once the page came back from any
sub-page: EQ, Default Vol, or Crossfade's own. The device test had checked them only on first open.
`ringnav_audioset` now binds its own handler, `audioset_again`, to that event, and it adds the rows
again. AWTK runs a widget's newest handler first (`emitter_on_with_tag` puts each at the head,
`0x6f4668`), so the handler is bound before stock's init runs. That makes it run after stock's
rebuild. Idle's page also binds that event, but its handler (`0x4a9924`) only refreshes the sleep
timer and keeps the rows.

**The `test:` lines.**
- **About's row:** ported. V2.1 has no row builder: the rows are in its asset, and the init's visit
  (`0x4a12c0`) fills them. The test builds the page from V2.1's asset, runs that visit for Model and
  FW. Version, then the payload's hook. The added row must match V2.1's row and label in type,
  geometry and style.
- **Display settings rows:** the check behind this line was Wheel Sensitivity's page, which is
  Q2 only. On M1 its place goes to Crossfade's page.
- **Library row title bounds** and **the info pages' Back:** not M1 work. What they test is the iPod
  UI's (`compact_row_layout`, and `tools/ipod.py`'s `navigator_close` unwind). In the Stock UI they
  run V1.32's own code as a control. They are noted under the roadmap's iPod section.

**Tests.**
- `test/patch.py`: V2.1's Boot volume page is built from its asset and bound by V2.1's own init.
  The handlers it binds must be `offsets.inc`'s. After the row's click, none of them is left (Back
  is). The view must be shown and enabled, and the switch, the slider and +/- must set and save
  Off, the length and the clamps. The Playback test pins V2.1's foreground binding, the rebuild's
  `widget_destroy_children` and the emitter's head insert. It checks that the payload's handler is
  bound before stock's init and brings the rows back as they were.
- `test/boot.py`: after the EQ steps, the walk scrolls Playback to its end and opens Crossfade. It
  taps the slider, and goes Back to the list as it was but for Crossfade's row. The run must have
  executed `xfade_open`. The walk's budget is 120 seconds.
- Each new check failed against a deliberately broken build. Binding the handler after stock's init
  was caught by `test/patch.py`, and by `test/boot.py` once it required `xfade_open`. Before that
  requirement, the tap toggled Folder Skip instead and still changed the screens. Leaving
  `bootvol_view` disabled was caught by `test/patch.py`.

**Commits:** `5b7bb1d` (Playback's rows), `54eb321` (Crossfade's page and its test), `2c3f809` (the
boot walk), `c2777fd` (About's test), `994451b` (the two iPod-UI checks) and this record.

## 15. Hardware-specific behaviour (Oct 18)

The roadmap's section 2, apart from the Coverflow and Photos scroll distance, which waits for an
entry point. Reading V2.1's code changed two of the plans before any code did.

**Knob Navigation Mode.** The roadmap planned a V2.1 key-down hook, but V2.1 has none to hook.
`home_page_init` binds the window manager's touch events, key-up (`0x113`, `on_wm_keyup_fun`) and
key-long (`0x110`), and no key-down or key-down-before. V2.1 turns the volume on the release:
`on_wm_keyup_fun` tests `key - 220 < 2` (`0x4cdbf4`) and opens `dialog/volume_dialog`. So the remap
`ringnav` already made on the release was enough. What was wrong was the setting:
- M1 builds always compile with `IPOD=0`, so the KNOB read in `accent()` and the Knob row in
  `ringnav_display` were dead code;
- `st.knob_mode` stayed 0.

The Knob row is now one of the `pod_*` settings, on M1 only. It sits after Artist Albums in Display
setting, saved as `[Q2POD] KNOB`. `knob_nav_active` reads it through `pod_settings()`. The dead
iPod-and-M1 code and `ringnav_keydown`'s unreachable M1 remap are gone. V2.1 has no buzzer command
either, so Key Tone moved from `NOT PORTED` to Q2 only.

Tests:
- `test/patch.py`: the `KNOWN GAP` is now a check. Turns become Previous and Next, and the press
  Centre. Volume mode, a dark screen, Now Playing and a press held by the boot guard keep the
  knob's keys. The Display test covers the new row, its click and its saved value.
- `test/build.py`: pins the key-up binding, the absence of a key-down binding in `home_page_init`,
  the 220/221 test, and the missing buzzer strings.
- `test/boot.py`: after Crossfade, the walk opens Display setting and taps Knob. Back on System
  Setting, two knob turns must change the list (the selection outline) and leave the status bar's
  volume as it was. With the row left at Volume, the same step fails.

**The cover-worker mutex.** It needed no alias. `/tmp/.tmp_picture` is used only by
`toolsGetAlbumCover`, which is called from two threads:
- three calls in `parse_albumcovertask_thd`;
- one in `parseplaycover_thd`, which holds `parse_cover_mutex` (`0xa04588`) around it.

V2.1 has no second, player-cover lock. Coverflow's `build_art` already held `parse_cover_mutex`, so
its worker was excluded all along. The second lock it took on M1 was the zero-filled
`m1stub_g_playcover_mutex`, which was harmless, since zeroed memory is an unlocked default mutex.
That lock is now Q2 only.

`g_lastcover_url` (V2.1's `savecover_path`) matters only to Home's split view, which is iPod-only and
not built for M1. So the roadmap's "Home never shows the playing cover" can't happen on M1.

`test/build.py` pins the four `toolsGetAlbumCover` call sites and the lock before the player
thread's call.

**Bluetooth absolute volume.** V2.1 has no `mclSetBtVol`. It merged V1.32's `mclSetLocalVol` and
`mclSetBtVol` into the exported `mclSetVol` (`0x5d4cb0`), which does two things:
- it always issues the DAC's volume ioctl (`0xc0044d00`);
- on Bluetooth, it also sends hciplayer `{mcl-setvol\%d}`.

`set_devicevolume` calls it with 0–100. Two things differ from the Q2, and the hook
(`M1PLUS_HOOKS['mclSetVol']` → `ringnav_btvol`) handles both:
- **Full scale.** A private routine that `mclStartPlayer` and `mcl_tidalStartPlayer` call
  (`0x5d4e00`) sends `mclSetVol(255, 255)`. On the Q2 that call goes to the unhooked `mclSetVol`.
  Through the hook, 255 would clamp to 100 and push the headset to AVRCP 127. So on M1 anything
  over 100 goes straight to stock.
- **The DAC.** While a headset takes absolute volume, stock gets (100, 100), which now sets the DAC
  to 100 as well. Bluetooth's end puts it back. Both `checkBluetoothStatus` (three paths) and
  `switchBluetooth` run `save_stop_player`, `set_outputchannel`, `set_devicevolume`,
  `save_start_player`, in that order, so the jack never plays at the DAC's 100. A restore in the
  payload's poll was planned and dropped: it would bypass balance and the fixed line-out level that
  `set_devicevolume` applies.

`test/build.py` pins these:
- the merged body, and that the old symbols are gone;
- `set_devicevolume`'s clamps;
- the 255 call;
- the order of the four calls on each disconnect path.

`test/patch.py`'s Bluetooth volume and volume-limit tests now run on M1 through the real hook.
`mclSetVol` stands in for both of V1.32's setters. The 255 case passes to stock and leaves the
headset as it was, and it fails without the pass-through. The device test still has to check, at
low volume, that wired headphones come back at the slider's level after a headset disconnects.

**Touch long-press.** A press held still for 500 ms on a library row or tile opens that row's hold
menu, as Play/Pause held on a highlighted row does on the Q2.
- **Arming and the row.** `lp_input` in `ringnav_input` arms on V2.1's `0xff` press, on a
  `CTX_FOLDER`/`CTX_LOCAL` page, and stops on a `0x101` move of 8 px or on the `0x103` release.
  `qm_hold` then runs with `LP_TOUCH` set and takes the row under the pressed point (`lp_entry`),
  without the pointer gate or a key latch. `LP_TOUCH` is the constant 0 on Q2, so Q2's `qm_hold` and
  both Q2 `update.tar` are byte-identical.
- **The release.** As a claimed pull does, the hold aborts the native press. `ringnav_dispatch`
  swallows clicks until the release has been through stock.
- **Its own point.** The hit test requires the point to be on the list, because a recycled table
  keeps rows past its viewport.

`test/patch.py` long-presses a row of each library page and checks four things:
- the title and the menu of the row under the finger, not the highlighted first;
- that the page got the abort;
- that the row's click was swallowed, and the next click goes through;
- that nothing else opens.

A move of 8 or 9 px, a release 1 ms early, and a press below or beside the list open nothing, and
their click reaches the row. A 7 px tremor still opens the menu, and a press on a non-library page
opens nothing. The `NOT PORTED` line for Rate Album on an artist's albums is now a long press on its
second album. `tslib_run`'s `0x101` and `0x103` are pinned beside its `0xff`. Without the swallow,
the suite fails.

**The hold menu on V2.1 (fourth device test, V004s).** The long press reached the menu's open, but
V2.1's own sort window came up. V2.1's navigator runs a dialog modally when its `to_modal` reads set,
and V2.1's sortselect init, unlike V1.32's, never clears it. So `navigator_to` returned only once the
dialog had closed, and the menu's re-dress found nothing to dress. The tests had missed it because
`test/patch.py` stood in a V1.32-style dialog.
- **The fix.** `qm_sortselect_init` (`M1PLUS_HOOKS`) clears `to_modal` for the menu's own open
  alone. The menu takes V2.1's row sizes and styles, in its 260 px popup.
- **Tests.** `test/patch.py` now opens V2.1's real dialog from its asset, through V2.1's init and the
  hook, with the navigator's modal check modelled; `QueueMachine.nested` runs stock code from inside
  a mock. Without the clear, the suite fails. `test/build.py` pins the navigator's init call, its
  `to_modal` default and `dialog_modal`, an init that sets no property, and the asset.

**Bluetooth's own level (fifth device test, V005s).** With a Sony WH-1000XM6, the headset's buttons
changed its volume but not the M1's indicator, and the knob made the headset jump back first. A
temporary log on the card showed why: V2.1 keeps Bluetooth's level apart from the jacks'.
- **V2.1's two levels.** The volume dialog (`on_volume_tsup_fun`) steps `btsource_volume` while
  `headset_output` is 2 and saves it as `[PLAYSET] BTVOLUME`. It steps `volume` (`[PLAYSET] VOLUME`)
  only for the jacks. The dialog's refresh (`0x47d664`) and the status bar show the output's level.
- **What went wrong.** The payload, as on the Q2, synced `g_volume`, which on V2.1 is the jacks'.
  On connect it put the headset at the jacks' level, so the knob, stepping from Bluetooth's own,
  jumped. The headset's own steps moved and saved the jacks' level instead of Bluetooth's.
- **The fix.** On M1, `BT_VOLUME` is `g_btvolume` (`M1PLUS_GLOBALS`, V2.1's `btsource_volume`).
  The poll and `headset_gain` use it, and it is saved as `BTVOLUME`. An open volume dialog is
  refreshed through V2.1's own routine (`volume_refresh`), since V2.1's dialog has no `slider_vol`.
  `g_volume` stays the jacks', and so does the DAC restore when a headset stops answering.
- **Tests.** `test/patch.py`'s Bluetooth tests set and read Bluetooth's level on M1. A new case
  checks four things for a headset step: Bluetooth's level, the `BTVOLUME` save, the dialog refresh,
  and the jacks' volume left alone. `test/build.py` pins the dialog's two levels and keys, the
  refresh's reads and the status bar's.

**Knob direction (after the fifth device test).** In Navigation, a turn toward volume up went down
the list. It now goes up by default (`KEY_PREV`). A new Display row under Knob, `Knob Up: List Up` or
`List Down` (`POD_KNOB_DIR`, `[Q2POD] KNOBDIR`), flips it back. `test/patch.py` checks both
directions, the default, Volume mode ignoring the row, and the row's click and saved value.

**The knob in Bluetooth receiver mode (sixth device test, V007s).** With the phone as the source,
the phone's slider worked but the knob, in Navigation, did nothing. The receiver page
(`bluetoothrecv_page`) isn't Now Playing, so the turn became Previous or Next, which neither the page
nor the payload takes there. `knob_nav_active` now remaps only where `ringnav` navigates: `usable()`
(which leaves Bluetooth receiver and USB DAC modes to stock) and a context page. So the receiver page,
USB DAC mode's `usbmode_page`, the volume dialog and Now Playing's enlarged art (`bigcover_page`,
which V007s had also lost) keep the volume. In receiver mode V2.1 scales the
jacks' `volume` by the phone's AVRCP level (`bt_recv_volume` / 127, in `set_devicevolume`), and the
payload's Bluetooth hook passes it through. `test/patch.py` checks each page and both flags. With
the old gate, the suite fails.

Confirmed on the device:
- the knob in both modes, and a long press opening the hold menu (V004s, V005s);
- Bluetooth output volume with a Sony WH-1000XM6: the headset's buttons and the knob agree (V006s);
- with Knob on Navigation, the knob's volume on the enlarged art and in Bluetooth receiver and USB
  DAC modes (V008s).

What is left for the device test, at low volume first:
- wired headphones after a headset disconnects, at the jacks' own level;
- both ways of Knob Up;
- Rate Album's hearts (V2.1 has no `play_fav`/`play_unfav` images), deferred for now.

## 16. Previous is Back in Knob: Navigation (Oct 19)

With the knob navigating, the hand is already on the hardware, and Previous is where a Back key
would be. Section 13 took Previous-as-Return away because it was a hidden path with a bug. It comes
back in a narrower form: Back, only in Knob: Navigation, and only where the knob navigates. The
on-screen Back button stays on every page in both modes, so Knob: Volume always has a visible way
out.

**Where.** `ringnav` (the `on_wm_keyup_fun` hook) takes Previous inside `knob_nav_active()`, beside
the knob's remap. That gate needs the screen on and a context page, and it excludes Now Playing,
the enlarged art, the volume dialog, and Bluetooth receiver and USB DAC modes. Section 13's two
bugs (the key lock, the screen-off drop) both need the screen off, so they can't happen. On Home
Previous stays Previous track, because there is nothing to go back to. Previous is the button stock
takes as Previous: on a rotated screen (`rotate_mode` 1) `on_wm_keyup_fun` swaps 214 and 215
(`0x4cd9f8`), so there it is 215. `rotate_mode` is a new M1 global (`M1PLUS_GLOBALS`).

**How.** The first try sent a Return, as the payload's back button does. `test/boot.py` showed
System Setting stayed open: V2.1's pages take no `KEY_RETURN` (the M1 has none, and
`on_wm_keyup_fun` has no case for 170). Their back buttons are built by each page's init: a
`button_create` in `navbar_btnreturn_style` whose click is `on_back_onclick` (`0x47f12c` is one of 42
such sites). Section 10's check that Previous closed a page only covered the PEQ, a payload page. So
Previous now presses the page's own button. A timer, after the key's dispatch, finds the top page's
first showing button in that style and dispatches a click to it. That is V2.1's own button on its
pages, and `back_button` (same style) on the payload's, which then sends its Return.

The second build crashed demo on the first Previous. `widget_get_prop_str(w, "style", "")` returns
NULL, not the default, for a widget with no style (`value_str` of a NULL `widget->style`), and the
payload's `strcmp` doesn't take NULL. The search now reads the style of buttons only and checks for
NULL. The test machine's `widget_get_prop_str` now returns NULL for an unset style too.

**Tests.**
- `test/patch.py`, with KNOB=1:
  - on System Setting, Previous clicks the showing back button, not a hidden one or a styleless
    button, and runs neither stock's key-up nor a media key;
  - the same with another source owning playback, and with the rotated screen's swapped button;
  - Next stays Next;
  - on a payload page, it clicks `back_button`'s button.

  Volume mode, Home, Now Playing, the enlarged art, and a dark screen (locked or not) keep Previous
  a media key. On Home with Spotify or Radio owning playback, it is that source's Previous.
- `test/boot.py`: after `knob_nav`, Previous closes System Setting to Home (`previous_back`), and a
  second Previous leaves Home as it was (`previous_home`). The first build (a Return) failed
  `previous_back`, and the second crashed there.

**On the device** (V009s, `update.bin` `fa861687…`, through the menu updater over V008s):
- it boots, and About shows dev 9;
- the on-screen back button works as before;
- with Knob: Navigation, Previous goes back on System Setting and its pages, V2.1's library pages and
  the PEQ editor's screens, stays Previous track on Home, Now Playing and the enlarged art, and does
  nothing to the page with the screen off;
- no crashes or freezes.

Still to check: Previous with Spotify or Internet Radio playing, once Streaming's rows are ported
(roadmap §3).

## 17. The Q2 Pod Home card and page (Oct 19)

The roadmap's section 3, the Library's extras: on M1, Shuffle, Ratings, Most Played, Long Songs, the
media folders and Coverflow had no way in. V1.32 has a Local Music menu Q2 Pod extends; V2.1 has
none, because its Home is the library. The roadmap chose one Home card opening a payload page.

**V2.1's Home, read from its code.** `home_page.bin` holds only an empty `home_sview` (a
slide_view) and `home_sindicator`. A private routine at `0x534064` builds the grid: it destroys
`home_sview`'s children and makes one 320x364 page view per six ids of `pdeq_choicemenu` (the cards
picked in V2.1's Home menu editor, `[MAIN] HOMEMENU` in config.ini), then sets the dots' count. Its
card builder (`0x533d8c`) places each card: a 154x118 view in two columns from x 6, rows at 0, 118
and 236, holding a clickable 66 px image (`home_<name>_style`: `bg_image` `<name>`, pressed
`<name>_down`) and a line-wrapped label in Home's own style file. A card's click (`0x533b80`) reads
`atoi(name)` as one of 18 ids. The grid is rebuilt only by `home_page_init` and by Home's refresh
(`0x534858`), which runs when Home comes to the front and rebuilds only after the editor or a
language change (`homemenu_changeflag` 2).

**The card.** `home_card` (`patch/coverflow.c`) adds "Q2 Pod" in the next slot exactly as V2.1
places its own, or on a new page with the dots counting it when the last page is full. Its image has
no name, so V2.1's click never sees it, and its own click opens the page. V2.1's rebuild destroys it
with the other cards. The card binds its own to-foreground handler before V2.1's init binds V2.1's,
so it runs after V2.1's rebuild (the emitter runs the newest first) and puts the card back once.
The icon pair is new art in V2.1's flat card style (a gold circle no stock card uses, with a white
iPod), added as new rootfs images.

**The page.** `library_open` (`patch/navigation.c`) opens `library_page`: `page_open` and
`page_list` (title bar and back button) over V2.1's 64 px rows (`list_row`), in the Q2 Library's
order: Shuffle, Ratings, Most Played, Long Songs, Podcasts, Audiobooks, Photos and Books (each only
with its folder), Coverflow, and Upload Scrobbles (only with an account). Videos waits for q2video on
the M1's DAC. `localclass_page_init` is no longer hooked: `ringnav_localmusic` found no Local Music
list there.

**What the page needed.**
- **Row icons.** V2.1 has no `local_fav` or `local_frequentplay`, so Ratings and Most Played had
  none: they are now V2.1's Favourites and Frequent card art at the rows' 40 px. The drawn icons
  (52 px, V1.32's size) and a Coverflow icon from its card art are resized to 40 px too.
- **Back buttons** over Coverflow's carousel, the photo viewer and the book reader. On M1 Coverflow's
  covers go back to the Q2 Pod page, not Home.
- **The name check** reads Home's style file as well as `default.bin`, since the card's label style
  is in it.

**Tests.**
- `test/patch.py`:
  - V2.1's real `home_page` asset and V2.1's real grid code, run under Unicorn for 1, 5, 6, 12, 17
    and 18 cards: the card lands where V2.1 would put the next card, with a new page and the dots'
    count when the last page is full;
  - cards turned off and on in the editor (17, then 6, then 13), through V2.1's rebuild and the
    to-foreground handler: the card comes back once, on the right page;
  - the card's image, label and click, and a grid not as V2.1 builds it getting no card;
  - the page's rows, icons, order and conditions, and the rows' clicks. The `NOT PORTED` line is
    gone. The Library tests that click rows reach their handlers, the ones this page uses, through
    Q2's builder.
- `test/build.py` pins V2.1's grid: six to a page, the page and card geometry, the label style,
  the click's 18 ids, and the builder's only two callers. The rootfs check expects the five new
  images.
- `test/boot.py`: Home's last page matches stock's but for the card; the card opens the page, its
  Shuffle row opens Shuffle, and Previous and the back button close the page. With `--home-menu`,
  V2.1's Home has six cards (seeded `[MAIN] HOMEMENU`): Home matches stock's but for the dots, and
  the card, alone on the second page, opens its page. The walk's budget is now 180 s.
- Without the to-foreground binding, the rebuild tests fail.

## 18. The dev 10 (V00A) device pass (Oct 19)

Section 17's build on the device. The card and the page worked through Home edits, themes and
languages, and nothing crashed. Three rows didn't work. Each was diagnosed in the emulator, and
Long Songs was also confirmed on the device over `q2remote`.

- **Long Songs found nothing, and never measured again.** Shanling's libtag_c `taglib_file_new`
  takes a second argument, `readAudioProperties`: it is `new FileRef(name, flag, Average)` (`0x98a0`,
  the same on V1.32), and V2.1's scanner passes 0 (`0x5ec818`). The payload declared one argument,
  which left the flag to whatever `$a1` held. On the worker thread that was 0, so no file had
  properties, and all 417 of the device's songs were cached as 0 s, which counts as measured. The
  M1 now calls `taglib_file_open(path, 1)`, an alias of the same import. A cache
  written before the fix (dev builds only) has to be deleted once, by hand (`/mnt/data/ringnav-lengths`). The worker's `$gp` is
  not V2.1's GOT pointer, which looked like a cause, but isn't: glibc's MIPS resolver finds the
  object by the stub's address. The Q2's call is unchanged: the bug is latent there.
- **Book rows and photo tiles didn't open by tap.** A tap's down and up landed on the page's hidden
  full-size view (the reader or the viewer, created after the list). AWTK's hit test
  (`widget_find_target_default`, V2.1 `0x6747d4`) skips a child by `flags & 9` (enable, sensitive),
  never by visible (bit 2), and searches the newest child first. On the M1 the pages now make hidden
  views insensitive (`view_show`, `patch/peq.h`), as Coverflow's Settings list already did. V1.32's
  hit test is the same, so the Q2 has it too, behind its wheel; its build is unchanged.
- **Shuffle Songs played the library in order.** It saves stock's Shuffle with `config_playmode`,
  which V2.1 doesn't have, and the stand-in did nothing. On the M1 it is now V2.1's Play mode page's
  own sequence (`0x49fc78`): the mode through the `mclSetPlayMode` hook (`ringnav_mode`), then
  `notifyPlayMode()`, `dmrSendPlayMode(mode)` and `write_int_config(mode, "PLAYSET", "PLAYMODE")`.
  2 is Shuffle on V2.1 too (`playset/playmode_page`'s third row).

Not bugs: Shuffle Albums and Folders work (the queue view shows the whole library, as on the Q2);
Coverflow's covers don't take taps by design (the Q2 turns them by wheel); the card isn't in V2.1's
Home menu editor, which knows only its 18 ids; long press on these rows waits for roadmap section 3.

**Tests.** `test/boot.py --media` mounts a tmpfs card in the sandbox. On ext4, a 32-bit guest's
`readdir` under qemu-user fails with EOVERFLOW, so the payload found the card empty. The card holds
two 11-minute songs (generated FLAC and MP3 headers), a book and a photo, and V2.1's `songtable`
lists the songs. The walk:
- opens Long Songs, which must cache 660 s for both;
- taps the first book and the first photo, which must reach `to_reader` and `to_viewer`;
- taps Shuffle Songs, which must save `PLAYMODE=2`.

On the unfixed build, the walk fails at the book tap.

**q2remote on M1.** The device side already ran in every M1 `--dev` build; the client
`tools/q2remote.py` is now ported to the M1 ([remote.md](remote.md#m1-plus)):
- `shot` saves the 320x480 page upright;
- `key` uses V2.1's codes;
- `knob N` turns `md-rotary-knob`;
- `tap` replays the Goodix panel's tap, as recorded on the device: upright pixels, pressure only,
  no `BTN_TOUCH`.

The device's input list also corrected `m1plus.md`: the touchscreen is event3, not
`TSLIB_TSDEVICE`'s event2, which is the knob.

**On the device (dev 11, `V00Bs`, commit `e1f897c`).** The user checked:
- Long Songs lists their four songs over 10 minutes;
- book rows and photo tiles open by touch;
- Shuffle Songs shuffles.

Over q2remote, `/mnt/data/ringnav-lengths` holds 417 lengths and no zeros, four over 600 s, and
`config.ini` has `PLAYMODE=2`. The dev 10 cache was deleted over q2remote before Long Songs first
opened. Left for later (roadmap): the Shuffle page's clipped note, Coverflow's covers by touch, long
press on these lists, a q2remote swipe, and the two latent Q2 bugs.

## 19. The touch long-press's row (Oct 20)

**The problem.** On dev 11, a touch hold on Album opened the hold menu once, then opened the album
instead. Play/Pause held on a highlighted row always worked. The menu that did open was often for a
different album from the one held: a hold on "All I Need" opened "Clair Obscur", the next row down.

**Finding it.** q2remote's new `peek` ([remote.md](remote.md#reading-variables)) read the state
around q2remote's held taps, which failed as a finger did:
- 0.6 s into a hold, `st.lp_x`/`lp_y` held the press point, and the long-press timer had fired;
- everything `usable()` reads was clear, with no pending timer, dialog or playlist, and AirPlay's
  flag was 1;
- the showlist (a libcstl deque, read on the device) had 24 rows, as `g_menu.rows` did, and
  `g_class_type` was all albums.

That left `lp_entry`, the row under the finger. V2.1's `widget_to_local` (`0x669b88`) adds each
widget's own `get_offset` (vtable +0x34), the list's own included: a `scroll_view`'s
(`SCROLL_X`, `SCROLL_Y`), a `table_client`'s (0, `TABLE_TOP`). So the point came out in the list's
content, while `bounds()` measures rows on screen. On a scrolled list the point fell a row or more
below the finger. Scrolled further, it fell past the list's height and `lp_entry` returned -1. The
first hold after opening a page worked only while the list was near the top. Play/Pause takes the
highlighted row and never maps a point.

**The fix.** `lp_entry` takes the list's own offset off the point again, as `bounds()` does.
`test/patch.py`'s stand-in `widget_to_local` now adds the offsets as V2.1's does (M1 only, pinned
against V2.1's code). Holds on a table scrolled two rows and eight rows take the row under the
finger, and both failed before the fix. The Q2's `update.tar` (Legacy and iPod) is byte-identical:
`lp_entry` is M1 only.

**On the device (dev 12, `V00Cs`, commit `76830bd`).** The user checked by finger that taps, holds
and Play/Pause held on a row behave. Over q2remote, holds on Album scrolled near its end (a scroll
view) opened "Pop 2", "Lies of P: Overture" and "No Mythologies to Follow", each the row held, one
after another with OK between. Holds on All Songs scrolled (a table) opened "Amalfi Coast" and
"All That".

## 20. The Shuffle page's note and the Photos icon (Oct 20)

Two of the roadmap's small fixes, both M1 only:
- **The Shuffle page's note** was the Q2's 335 px scrolling label at x 20, past the M1's 320 px
  screen ("…to shuf"). The whole sentence is about 290 px at 16 px, wider than the screen less its
  margins, so on M1 it is a centred label `UI_W - 40` wide that wraps onto two lines, between
  words: on dev 13, `line_wrap` alone split "shu/ffle", so dev 14 also sets `word_wrap`.
  `test/patch.py` checks the label, its width and both wraps.
- **The Photos row's icon** was a copy of V2.1's `scover_wait0.png`, a frame of the 54 px loading
  spinner. V2.1 has no photo art, so it is now `pset_covermode.png`, V2.1's 40 px cover-mode badge,
  as the Q2 uses V1.32's `playset_covermode`. `test/build.py --build` checks the copy and its size.

**On the device (dev 14, `V00Es`, commit `79bc00d`).** Over q2remote, the note reads "Albums and
folders take a moment to / shuffle", centred, and the Photos row shows the blue badge at the other
rows' size (dev 13 already had the badge). The user checked both.

## 21. Coverflow and Photos by touch (Oct 20)

The roadmap's section 2: the scroll distance, which was two `KNOWN GAP`s, and Coverflow's covers by
touch.

**The problem, read from V2.1's code.** V2.1's `slide_menu` has no spacer. Its scroll-done
(`0x6123f4`, through `0x612360`) commits `round(xoffset / h)`, and its drag sets `xoffset` to the
finger's travel one for one (`x - xdown`, `0x6128f0`), once the finger has moved 10 px. So it steps by
its own height: 260 px on Coverflow's covers, 450 px on the photo viewer. The payload draws a cover
every `CF_STRIDE` (100 px) and a photo every screen width (320 px). On the viewer, which took V2.1's own
drag, the next photo was drawn 450 px on, which left a 130 px black gap mid-swipe, and a swipe had to
travel 225 px to turn. Coverflow's covers took no touch at all: as on the Q2, the `slide_menu` is
insensitive and only the wheel (on M1, the knob in Navigation) turns them.

**What was ruled out.** A handler on the `slide_menu` can't rescale its drag: V2.1's `widget_dispatch`
(`0x66cec8`) runs the widget's own `on_event` before its emitter, and the `slide_menu` stops a drag's
moves there. Sizing the `slide_menu` to one item would leave the frame painted past its bounds and
outside its dirty rect.

**The fix.** On M1 both carousels' `slide_menu` is insensitive, and the view under it takes the
touch:
- `slide_swipe` (`patch/navigation.c`) moves the offset by `stride / px` per pixel, so the finger
  moves one item as painted: `CF_STRIDE` on the covers (the flat fallback's own stride), a screen
  width on the viewer. The release settles on the nearest item, or the next one for a flick (released
  within 300 ms). It uses the knob's animator, so `home_done` commits the index as the knob's steps do.
  A press on moving covers catches them, and the back button's press is its own.
- Coverflow (`touched`): a tap on the centre cover opens it through `pick`, as Centre does. A tap on
  a side cover brings it to the centre, by the renderer's geometry (`CF_X1`, `CF_XS`). An artist's
  albums still stop at both ends, with the knob's bounce.
- Photos (`swiped`): a tap shows or hides the caption, as the photo's own click did. The paint spaces
  the photos a screen apart, not by the `slide_menu`'s stride.

The Q2's `update.tar` (Legacy and iPod) is byte-identical: all of it is M1 only.

**Section 1's two `test:` lines that waited for this.**
- Coverflow's track queue through `mclNextSong` now runs on M1, in order (mode 0). Shuffle's pick of
  the Play next track waits for `SHUFFLE_CALL` (roadmap section 4).
- Other slide menus' next and previous is Q2 only: no V2.1 page has a `slide_menu`, so the payload's
  two carousels are the M1's only ones. `test/build.py` checks every V2.1 UI page for one.

**Tests.**
- `test/patch.py`: both `KNOWN GAP`s are now checks.
  - On Coverflow's covers: a slow drag of one cover's width moves the offset a whole step, and its
    release commits the next album. Less than half a cover goes back, and 2.4 covers moves two. A flick
    moves one, and a 7 px tremor is a tap that opens the centre album. Taps on side covers bring them
    to the centre. A press on moving covers lets them finish without opening anything. The back
    button's press, a tap under the frame and an aborted press do nothing. On an artist's albums a
    drag past either end stops at the bounce and springs back.
  - On the viewer: the photo follows the finger with the next one a screen behind it and no gap.
    Past half a screen the next photo settles in, short of it the photo returns, a flick moves one, a
    tap toggles the caption, and the back button's press moves nothing.
- `test/build.py` pins V2.1's scroll-done division by the height, the drag's `x - xdown`, its 10 px
  threshold, and that no V2.1 page holds a `slide_menu`.
- `test/boot.py --media`, on V2.1's real dispatch: a swipe of one cover turns Coverflow to the Sort
  card, a swipe back returns to the album, and a tap on the centre cover opens its tracks. The card
  now holds two photos, and swipes move the viewer to the second photo and back. qemu decodes neither
  photo, so this shows in the trace (`moved`), not on screen.

## 22. Entry points: Streaming, Videos and the long presses (Oct 21)

The roadmap's section 3, the rest of it.

**Streaming.** The roadmap planned to hook V2.1's Streaming page through its page-name table. V2.1 has
no Streaming page at all: no `stream_page` asset or init, and its Tidal is one of Home's 18 cards. It
also has no AirPlay card; AirPlay's switch is on System settings' Network service page
(`netservice_airplay`), as on V1.32. So on M1, Spotify, Internet Radio and AirPlay are rows on the Q2
Pod page, after Coverflow, with the Q2's handlers. `ringnav_stream` is Q2 only. The tests that went
through `ringnav_stream` on M1 now open the Q2 Pod page and click its rows, and the `NOT PORTED` line
is gone.

**Their Now Playing pages.** Spotify's (`spotify_page`) and Radio's (`radionp_page`) Now Playing pages
get the back button. Their title, artist and album sat at `SPOT_ART_Y + 41`, which beside the Q2's art
is right, but on the M1 put them over its 254 px art. On M1 the art is 220 px, centred, and the text,
bar and times are under it (`SPOT_TITLE_Y`, `SPOT_ARTIST_Y`, `SPOT_ALBUM_Y`). The page's tag starts
after the back button, and Radio's heart is at the top right. `test/patch.py` checks that no text or
bar meets the art or the back button.

**Videos.** The device dependency was checked over q2remote on dev 14:
- `/dev/shanling_dac` is there, and V2.1's `hciplayer` issues the two ioctls q2video does (`0x4d1b`
  once, `0x4d1f` six times);
- ALSA card 0 has `pcmC0D0p`, so `plughw:0,0`, and `aplay` and `ffmpeg` are in the rootfs;
- `/dev/fb0` is `jzfb`, 320x480 with a 320x960 virtual size at 32 bpp, which is what q2video's
  check takes.

The Videos row now shows on the Q2 Pod page with a Videos folder. The player needed a way out and its
volume:
- q2video owns the framebuffer while it plays, so no widget can show over it. On the M1 build it draws
  a back chevron at the top left of every frame (`back_glyph`, white, in V2.1's title bar's place).
  `ringnav_input` already diverts all input while a video plays: a tap pressed and lifted in the 64 px
  square there quits, as Return does (`video_touch`).
- The knob's keys (220 and 221) are the Q2's wheel: the volume, or the seek after Centre.

The Q2's q2video is unchanged: the chevron is `#if M1PLUS`, and `test/peq.py` builds it for the host.

**The long presses.** `lp_input` armed only on V2.1's library pages (`CTX_FOLDER`, `CTX_LOCAL`).
Most Played, the rated lists and Long Songs are `CTX_FIXED`, though `qm_hold` already reads their
tracks (`page_tracks`). It now arms on any page a hold can act on:
- those lists, where it opens the song menu;
- Coverflow's covers, where `qm_hold`'s album branch took only the Play key. A touch needs the finger
  on the centre cover at rest (`coverflow_centre`);
- the stations and Spotify's tracks. `radio_hold` and `spot_hold` take the highlighted row, so the
  hold highlights the row under the finger first (`lp_select`), then toasts as the key's hold does.

On Coverflow a long press's abort ends the swipe without a tap.

**Tests.**
- `test/patch.py`:
  - the Q2 Pod page's rows, Videos and Streaming's included;
  - the Now Playing pages' back buttons and layout, and Radio's heart;
  - holds on Most Played (the row under the finger, nothing on the title bar), a station, a Spotify
    track (nothing on an album row) and the centre cover (nothing on a side cover or on moving
    covers);
  - in a video, the knob's volume steps and the chevron's tap, which quits only when pressed and
    lifted in its square.
- `test/peq.py` checks the chevron's pixels and that nothing else changes.
- `test/boot.py --media`: on V2.1's real dispatch, Spotify (not on the card) shows its message, and
  Internet Radio its menu, and each closes with its back button.

The Q2's `update.tar` (Legacy and iPod) is byte-identical.

## 23. The dev 15 (V00F) device pass (Oct 21)

Sections 21 and 22 on the device. The user checked:
- Coverflow turns by swipe, and a tap opens the centre cover;
- the photo viewer's swipes and captions;
- AirPlay opens Network service;
- Spotify, not on the card, says so, and its back button closes the page.

Two bugs:
- **Internet Radio rebooted the device on a station's first play.** Reproduced over q2remote, with
  the kernel's messages and `ps` logged to the card each second. q2video started and opened the DAC
  at 48 kHz, then demo took a SIGSEGV, a NULL read in libc's `strcmp`, called from radio.c's `set()`.
  The device restarts when demo dies. `set()` compares a label's text through `tk_strcmp` before
  setting it. V2.1 has no `tk_strcmp`, so on the M1 it was glibc's `strcmp`, and V2.1's
  `widget_get_prop_str` returns NULL, not the default, for a label with no text yet. AWTK's
  `tk_strcmp`, which the Q2 calls, takes NULL. On the M1, `tk_strcmp` is now that same NULL-safe
  compare (`peq.h`), which fixes all ten such sites, Spotify's Now Playing title among them.
  `test/patch.py`'s glibc `strcmp` now fails on NULL, as libc does. Against the unfixed build it fails
  at Spotify's Now Playing, which would have crashed once a track played. The tests had missed it
  because the harness's `strcmp` was its NULL-safe `tk_strcmp`.
- **Coverflow's track list didn't scroll by swipe.** Opening an album hid the covers' view without
  making it insensitive. AWTK's hit test doesn't skip hidden views (section 18), and that view lies
  over the list. Coverflow's views now use `view_show`, and so does `page_list`'s body when it is
  shown again.

Not a bug: on Spotify's page, Previous with Knob: Navigation is a media key, not Back. It's a Now
Playing page, where Previous stays the media key (section 16).

Both fixes are M1 only, so the Q2's `update.tar` is byte-identical.

**On the device (dev 16, `V00Gs`, commit `4a343b2`).** The user played Kiss 95 through q2video on the
ES9069Q, and an album's track list scrolls in Coverflow. Over q2remote, with the kernel log on the
card, a favourite that would not play (a radio-browser `.pls` URL, which ffmpeg reads as text) showed
"Can't play this station" and demo kept running. That station is the Q2's issue too (roadmap
section 6).

**A video stopped on its first frame (dev 16).** The user's test file (640x360 H.264 with AAC) showed
its first frame and nothing more. Over q2remote, the PCM was prepared but never started:
- ffmpeg, which wrote both the picture and the sound, was blocked writing the picture's pipe;
- q2video's sound thread was waiting on an empty sound pipe;
- q2video paces frames by the sound it has played, so it took no frame past the first.

The file keeps a second of video (30 frames) ahead of its first sound chunk. ffmpeg had to write 25
frames of 614 KB, about 15 MB, before it read any sound, against the video pipe's 4 MB. Raising the
kernel's `pipe-max-size` didn't help. On M1, q2video now runs the sound through an ffmpeg of its own
(`-vn`), so neither stream waits on the other; a file without sound ends that one at once, and the
picture goes by the wall clock, as before. The new q2video was checked on the device before
flashing, bind-mounted over `/usr/bin/q2video` and played from the Videos row: the sound ran at
48,000 frames a second, the picture moved, the knob stepped the volume, and a tap on the chevron
quit to the list. The Q2's q2video is unchanged, though its one-ffmpeg design has the same latent
bug (roadmap section 6).

**Dev 17 (`V00Hs`): the video froze the device.** Flashed, so from a cold boot, the video showed
nothing and the back chevron did nothing. Over q2remote:
- the PCM was running with its buffer full (`avail 0`) and the hardware pointer never moved;
- q2video's sound thread was blocked in `snd_pcm_writei`, and its main thread waited to join it after
  a quit. While q2video lives, `ringnav_input` hands it every key and touch.

The by-hand check had passed only because music had played first. V2.1's own player powers the DAC on
before playing (`on[1]`, an FPGA load, `on[2]` in the kernel's log); a cold q2video never did.
- **The cause.** V2.1's `set_outputchannel` takes a third argument, which V1.32's lacks. On the
  output path it calls `mclSetDacPwr(a2 ? 100 : 1)` (`0x4d6fd4`), and only 1 does the full power-on
  (ioctl `0x4d1a` 1, `toolsDownFpgafirmware`, `0x4d1a` 2). `start_player` passes 0. The payload's
  `dac_take` passed V1.32's two, leaving whatever the register held. On M1 it now passes 0. Radio had
  the same gap; it played for the user only after music.
- **The freeze.** On M1, a quit (the chevron) that q2video hasn't acted on within 3 s is forced, as
  radio.c's stop forces one (`killall -9 q2video`). So the chevron and every key work again,
  whatever ALSA does.

`test/patch.py` checks the third argument and the forced quit. `test/build.py` pins
`set_outputchannel`'s choice, `start_player`'s 0 and `mclSetDacPwr`'s full path. The Q2's
`update.tar` is byte-identical.

**On the device (dev 18, `V00Is`, commit `5752670`).** Straight after a reboot, before any music, the
user played the video and an Internet Radio station. Over q2remote, the kernel's log showed the DAC's
full power-on (the FPGA load, `on[2]`) at 19 s, with no segfault, and no q2video left running.

## 24. Roadmap section 4 checked against V2.1 (Oct 21)

Before porting any of section 4's call sites, each one was looked up in V2.1's `demo`, and each
behaviour was checked against what V2.1 already does. V2.1 is newer than V1.32, so some rows might
be native there. The method:
- Find the same-named or same-role function, from its symbol, its strings or its callees.
- Compare it with V1.32's after normalising addresses and immediates.
- Where the code had changed, look at the page on the device over q2remote.

The results are in the roadmap's section 4. In summary:
- **Unchanged code.** Most of V2.1's player and library code is V1.32's, moved: `mclNextSong`, the
  shuffle pick, `switchBtPriority`, `check_cpumem` (V1.32's `check_mem_thd`), `into_standby`
  (`device_standby`), `toolsLoadAllFile`, `toolsLoadDirectory`, the folder lister and both name
  comparators. So Shuffle's Play next and history, LDAC HQ, the page cache, Standby, the scan limit,
  M4B and the article-free sort keep their V1.32 behaviour, and each port is a site and a word.
- **Native in V2.1.** An artist's page lists the artist's albums. Buttons lock has its own Volume, Keys
  and All modes. The Artists page has its own Artist/Album Artist switch (`btn_artistswitch`), which
  `config_init` reads at boot. Its Artists rows draw V2.1's own icon. Those rows are dropped from
  section 4.
- **Changed pages.** The Bluetooth list builder (`0x4a3734`), the Lock screen page (a picture grid),
  Now Playing's heart (`btn_fav`) and the cover cache (`/tmp/abp`, still keyed by the album's name
  alone) need new sites, not moved ones.

Three things turned up that the roadmap didn't list:
- **A reboot lost the advanced queue.** V2.1's `config_init` applies the saved play mode by calling
  `mclSetPlayMode` itself (`jalr` at `0x4e596c`). V1.32's called `config_playmode`, which Q2 Pod
  replaces with `ringnav_bootmode`. On M1 that call reached `ringnav_mode` as a user's choice, so
  `playback_clear` deleted `/mnt/data/ringnav-queue` before the Home page's memory play could read
  it. On dev 18, over q2remote, the queue file was there before a reboot and gone after it. The
  file was put back from a copy on the card.
- **No gapless in advanced play.** `mcl_preload` isn't hooked on M1, so stock preloads its own next
  track, and `ringnav_next` drops it and starts the right one without the gapless handoff. V2.1's
  `mcl_preload` (`0x5d0ea4`) is V1.32's.
- **The cover worker's Q2 fixes.** `COVER_PAUSE` and the stale-completion check
  (`ringnav_cover_done`) are Q2 only. Whether V2.1's album lists have the same bugs isn't known yet.

## 25. A reboot keeps the advanced queue (Oct 22)

Section 24 found that a reboot lost a Shuffle Albums or Shuffle Folders queue on M1.
- **The cause.** V2.1's `config_init` applies the saved play mode itself, with a `jalr mclSetPlayMode`
  at `0x4e596c`. V1.32's goes through `config_playmode`, which Q2 Pod replaces with `ringnav_bootmode`.
  `mclSetPlayMode` is hooked on M1 too (`ringnav_mode`), so the boot call counted as a choice:
  `playback_clear` deleted `/mnt/data/ringnav-queue` before memory play could read it.
- **The fix.** `ringnav_mode` leaves advanced play alone when it returns to `BOOT_MODE_RET`
  (`0x4e5974`), as it already does for `player_initconfig`'s call (`INITCONFIG_MODE_RET`). That
  check is M1 only, so the Q2's `update.tar` is byte-identical. `tools/build.py` pins the call as it
  pins the other two: a `jalr` after a `lw $t9` of `mclSetPlayMode`'s GOT slot.
- **The test.** `test/playback.py` now runs V2.1's own call site for each mode before memory play
  reads the queue. Its M1 test had run only the later `config_mplayer` call, and after the read. It
  failed on the unfixed build, as the device did.

`test/playback.py` hadn't run on M1 at all before this. It loads only parts of `test/patch.py`, and
`named`, which `QueueMachine`'s V2.1 sortselect dialog calls, was outside them. `named` now sits
above the slice's end, and the hold menu's choice marker is the model's `ICON_SORTSELECT_CHECK`
(V2.1's `mulselected`). Its 258 checks pass on M1.

**On the device (dev 19, `V00Js`, commit `92b3fe2`).** The device held a saved album shuffle of 417
tracks. Over q2remote:
- the queue file survived the flash's own reboot, rewritten once as the resume saved its place;
- it survived a second, plain reboot byte for byte;
- after each boot, `peek` showed the payload had restored it (`s.active` 1, `s.n` 417, `s.shuffle` 3).

The user then played on from it: Play resumed the track, and Next and Previous stayed in the album
shuffle.

## 26. The call sites whose code is V1.32's (Oct 21)

Five of section 4's rows had V2.1 code that is V1.32's, moved (section 24). Each is now a
`CALL_SITES['m1plus']` entry, with the same words as the Q2's except for addresses and offsets:
- **Shuffle's Play next and history** (`SHUFFLE_CALL`): `mclNextSong`'s `bal` to the shuffle pick at
  `0x5d5a28`. The pick (`0x5d03b0`, a PIC entry with V2.1's GOT base) is a private routine, now in
  `M1PLUS_PRIVATE_FUNCTIONS`, so `ringnav_shuffle` is built for M1 too.
- **The page cache** (`DROP_CACHES`): `check_cpumem`'s `beq` at `0x50b868` becomes `b`.
- **The 65,000-song scan** (`SCAN_LIMIT`): `toolsLoadAllFile`'s count load and `slti` at `0x5efeb4`. The
  count is `-0x4f7c($fp)`, where V1.32's is `-0x3cac($fp)`.
- **M4B in folder scans** (`AUDIO_EXTENSION_CALLS`): `toolsLoadDirectory`'s and the recursive scan's
  `strstr` calls, at `0x5e8af0` and `0x5ea840`, with their GOT loads pinned.
- **The article-free sort** (`SORT_TRIMS`): the four `toolsTrimLeft` calls in the name comparators
  `0x5e0dac` and `0x5e16c4`.

Their `test/patch.py` tests now run on M1 against V2.1's code:
- the scan test's count, stop flag, listing deque and its two private routines are V2.1's, read from
  `toolsLoadAllFile`;
- the sort test runs V2.1's two comparators;
- the M4B test takes each site's stack slot from the table's order, since V2.1's slots are V1.32's.

Coverflow's Play next test now runs in Shuffle on M1 too. `test/patch.py` on M1 has 17 `NOT PORTED`
lines, down from 22, and passes 979 scenarios. Q2 Legacy and iPod `update.tar` are byte-identical to
the previous build, and their runs still pass (1017 and 1398).

## 27. The Ratings hold on Now Playing's heart (Oct 21)

V1.32's heart is the image `img_fav`, whose click (`0x52b154`) `rate_bind` swaps for one that tells a
tap from a hold. V2.1's is a button, `btn_fav`, and nothing is bound to an `img_fav`, so on M1 the heart
had only V2.1's tap.
- **V2.1's click.** `playing_page_init` runs a `widget_foreach` visit (`0x53b190`) that binds each
  button by its name; `btn_fav`'s click is `0x53b480`, with the window as context. It toggles My Fav
  for the playing track (`manage_myfav`), and shows the result by the button's style
  (`btn_imgfav_style` or `btn_imgunfav_style`, from `styles/playing_page.bin`). It takes the button
  from the event's target (`0x10`), not from its context.
- **The port.** `offsets.inc` names the heart per model: `VIEW_FAV`, `FAV_CLICK_ADDR`, `STYLE_FAV`, and
  the picker's images `ICON_FAV` and `ICON_UNFAV` (V2.1's `p_fav`, `p_unfav`). `rate_bind` finds the
  binding in the heart's emitter as on the Q2. The badge reads the button's style. When a save changes
  My Fav, `rate_close` calls V2.1's click with an event made for the button, since V2.1's click reads
  its target. The build's V2.1 name check now reads `playing_page`'s styles too.
- **The test.** On M1, `RateMachine` builds V2.1's `playing_page` from its asset, runs V2.1's visit on
  `btn_fav` (checking it binds `0x53b480` with the window), then runs V2.1's click for real, with only
  `manage_myfav` and `notifyFavor` mocked. The harness's click now carries its target, as AWTK's does.
  The checks are the Q2's. With the made event's target set to the window instead, the save check
  fails.

`test/patch.py` on M1 passes 988 scenarios, with 16 `NOT PORTED` lines. Under QEMU, the `--media` walk
opens V2.1's Now Playing through the hook. Q2's `update.tar` files are byte-identical.

## 28. The Lock screen page and the Large clock (Oct 21)

On the device (dev 19), the Lock screen page showed the default picture and five of the six
built-ins as empty frames with check circles, the sixth and any card picture behind the Time show
and About rows, and no Clock row. V1.32's page is a list its rows builder makes, which Q2 Pod hooks;
V2.1's is different:
- **V2.1's page.** `systemset_screensaver_page_init` (`0x4abe04`) places one 90x135 `imgcover%d`
  per picture in `view_covers`, a plain 400 px view that also holds the asset's Time show and About
  rows. It lays out two rows of three: a seventh picture lands off the screen to the right. Its visit
  binds only `imgcover0` to `imgcover5`, each to V2.1's pick (`0x4ab52c`) with its index.
- **The port.** A new hook, `lockscreen_page`, runs after V2.1's init. It moves `view_covers`'
  children into a scroll view over it, keeps V2.1's grid for every picture, and puts Time show, a
  Clock row (`pod_rows`, with Time show's icon) and About under it. Pictures past the sixth get a
  click that calls V2.1's pick, now a checked private routine (`saver_pick`). The built-ins'
  thumbnails lose V2.1's `file://` name and are drawn by `lockscreen_paint`, as on the Q2.
- **The Large clock.** V2.1's lock window names its clock `dclock_time` and `dclock_date`, and its
  battery is an icon with a level bar. Large found none of V1.32's names, so it did nothing on M1.
  `offsets.inc` now names them per model, and on M1 the icon and bar sit at the top line's right end.
- **The tests.** On M1 the page test builds V2.1's `systemset/screensaver_page` from its asset and
  runs V2.1's own init and visit through the hook. It checks the layout, the Clock row, and a pick of
  pictures 9, 4, 8 and 1 through V2.1's pick, with its check marks and saved path. The lock window
  test uses V2.1's `screensaver_page` asset. It had run on M1 with V1.32's widget names, so it passed
  without testing V2.1's window. The harness gained `widget_add_child`, `widget_remove_child`,
  `scroll_view_create` and `strcpy` mocks, and its `widget_set_name` writes the name where V2.1's
  visits read it.
- **Under QEMU.** `test/boot.py`'s walk opens the page, switches it on (V2.1's grid with the
  built-ins drawn), scrolls to the Clock row, switches it off and goes back.

`test/patch.py` on M1 passes 991 scenarios, with 15 `NOT PORTED` lines. Q2's `update.tar` files are
byte-identical.

## 29. The lock window's cover is native in V2.1 (Oct 21)

On the Q2, the lock window kept the old cover after a track change. Its timer sets `img_playcover` to
the same `file:///tmp/coverpic.jpg` for every track, and V1.32's `image_base_set_image` compares the
new name with the old and skips its `widget_invalidate` when they match. `lockscreen_cover` (on the
private `saver_cover`) invalidates it after stock.

V2.1's lock window does the same (`0x53f9b4`, on `view_img_icon`, then `widget_unload_image` so the
next paint decodes the new file), but V2.1's `image_base_set_image` (`0x654910`) has no compare: it
copies the name and always invalidates. So the cover repaints on M1 without a hook, and the row moves
to the roadmap's "V2.1 has them" list. On M1, `test/patch.py` runs V2.1's own `image_base_set_image`
twice with the same name and checks both calls invalidate. 14 `NOT PORTED` lines are left; it passes
992 scenarios. To check on the device: with the lock screen on, Next on the lock window shows the new
track's cover.

## 30. The cover worker's pause and stale completion (Oct 22)

Two Q2 fixes to the album-art worker were Q2 only (`COVER_PAUSE`, `COVER_DONE`). V2.1 has both bugs:
- **The stale completion.** V2.1's `parse_albumcovertask_thd` and `set_albumcover_flag` are V1.32's. A
  job marks its row ready by index alone, so a job that finishes after the list was rebuilt marks
  another album, whose art is then never requested. `COVER_DONE` patches V2.1's local completion
  (`0x4dd630`: the key at the same `sp + 0x1688` into `a2`, then `jal ringnav_cover_done`) and the
  folder path's branch to it (`0x4de660`, one word earlier). V2.1's Tidal completion (`0x4dd8b4`) is
  new and keeps stock's.
- **The pause.** V2.1 pauses the worker at scroll start on one local list, Library Albums
  (`album_page`, `0x522870`). Its scroll end (`0x524134`) resumes it only when the first row in view
  (`yoffset / 60`) changed. So a scroll within a row, or a scroll start sent alone, left the worker
  paused. `COVER_PAUSE` makes that store a `nop`. V2.1's Songs and its artist page don't pause. The
  other pausing pages are Tidal's, search and the lock window.

On M1 the checks run V2.1's own worker code: the completion and folder paths with stale and current
keys, then V2.1's readiness check and small-cover request queue. With V2.1's words put back, the stale
job marks the new row ready, and the scroll start pauses the worker. `test/patch.py` on M1 passes 994
scenarios. Q2's `update.tar` files are byte-identical.

## 31. The hold menu's selection and the Add to Playlist guard (Oct 22)

The roadmap said M1 already selected the held row for Add to Playlist (`qm_select`). It didn't:
- **The selection.** `qm_select` puts the row alone in the batch record, which `batch_add_file`
  reads. V1.32's calls are `batch_init_selectrecord` and `batch_set_selectitem`. V2.1 has neither
  name, so `peq.h`'s stubs made `qm_select` a no-op on M1. V2.1 renamed them: `select_recordinit`
  (`0x4da3b0`, the vector cleared and `n` zeros pushed) and `set_selectindex` (`0x4da434`, one
  index toggled), both on `pvec_selectrecord`, as V1.32's on `p_vector_select_record`. V2.1's
  `batch_add_file` adds only the entries the vector flags. So on M1 the hold menu's Add to
  Favourites and Add to Playlist added nothing, or a leftover multi-selection. Both are now
  `M1PLUS_FUNCTION_ALIASES`. Five `test/patch.py` checks had encoded the empty selection on M1;
  they now expect the Q2's.
- **The guard.** Opened from Now Playing's hold, the playlist page adds the queue's selected record
  in add mode 2. If the queue changed while the page was open, the Q2 refuses ("Queue unchanged")
  rather than add another song. V2.1's row click is `0x53d300`, which its row builder (`0x53e74c`)
  binds with the row. It is V1.32's `0x4b1d24` in role: in mode 2 it calls `batch_add_file` on
  `mcl_pdeqplaylist`. `offsets.inc` names it per model (`PLAYLIST_PICK_ADDR`), and
  `qm_playlist_bind` swaps it on M1 too. The guard test runs on both models. The V1.32 rows builder
  tests stay Q2 only: V2.1's builder isn't hooked, as Legacy's isn't.

`test/patch.py` on M1 passes 996 scenarios, with 13 `NOT PORTED` lines. Q2's `update.tar` files are
byte-identical.

## 32. LDAC HQ sends 990 kbps (Oct 22)

V2.1's `switchBtPriority` (`0x4d3024`) is V1.32's moved: the same dispatch, with its jump table at
`-0x5b50` from its GOT page, where V1.32's is at `-0xfd0`. The table sends rows 0 and 1 to the same
`li $4, 0x16`, as V1.32's does. Those rows are LDAC HQ and LDAC Standard: V2.1's Quality page
(`systemset/btquality_page`) builds its rows from a label table (`0x97ca08`) that starts
`btcode_ldachq`, `btcode_ldacst`, `btcode_ldacauto`, and its click passes the row's index. So
`LDAC_HQ` is the Q2's six words at `0x4d304c`, with V2.1's table offset in the `lw`.
`test/patch.py`'s check runs V2.1's `switchBtPriority` patched and stock: HQ sends 0x15, Standard
0x16 and Auto 0x18 patched, and stock sends 0x16 for HQ. On M1 it passes 998 scenarios, with 12
`NOT PORTED` lines. To hear on the device: a WH-1000XM6 with its multipoint off reports 990 kbps on HQ.

## 33. Gapless in advanced play and across speed changes (Oct 22)

Section 24 found that Shuffle Albums and Shuffle Folders lost gapless on M1: `mcl_preload` wasn't
hooked, so stock preloaded its own next track, and `ringnav_next` dropped it and started the right
one without the handoff. V2.1's `mcl_preload` (`0x5d0ea4`) is V1.32's instruction for instruction;
its `mcl_open_preload` (`0x5d0bd8`) differs only in register allocation and its loop's tail. Neither
has a symbol. Both are now `M1PLUS_HOOKS`, as on the Q2:
- `ringnav_preload` picks advanced play's successor into `MCL_PREPOS` and opens it;
- `ringnav_open_preload` refuses to open across a speed boundary, as a gapless handoff skips
  `player_initconfig`'s speed.

They are also `M1PLUS_PRIVATE_FUNCTIONS`, so `ringnav_preload`'s own open goes through the hook, and
`test/build.py` accepts a hook named there, still a PIC entry with V2.1's GOT base.
`test/playback.py` had stood in for both on M1. It now runs them, and the open-preload check is no
longer `NOT PORTED`. To hear on the device: with Gapless on, a gapless album in Shuffle Albums plays
through without a gap.

## 34. Resume on connect (Oct 22)

Q2 Pod's Bluetooth row, **Resume on Connect** (off by default), keeps a paused queue paused when a
headphone connects, where stock restarts it unpaused. On M1 neither part was ported:
- **The restart.** V2.1's `checkBluetoothStatus` restarts the queue with `bal save_start_player` at
  `0x4d6320`, `a0 = 0`, where V1.32's has a `jalr`. `BT_CONNECT_START` makes it
  `jal ringnav_bt_connect_start`.
- **The row.** V2.1's list builder (`0x4a3734`, unnamed) is new code: five callers, 64 px rows in
  V1.32's order (switch, name, Quality, Bluetooth Headset Volume Control, search, then the devices).
  It is hooked as `btmenu_rows` with the Q2's `ringnav_btrows`, so the row goes fifth with Bluetooth
  on. V2.1 calls the builder with any widget of the page, usually the clicked row, so on M1 the hook
  finds the window first (`widget_get_window`). The row's height is `offsets.inc`'s `BT_ROW_H`.
- **The tests.** The row test runs on M1, with V2.1's label offset and row height, and once more
  with a row passed to the builder. The harness's `widget_get_window` now walks up to the window
  for every `QueueMachine`, and its settings page sets its views' parents.

`test/patch.py` on M1 passes 1002 scenarios, with 10 `NOT PORTED` lines. Q2's `update.tar` files are
byte-identical. To try on the device: with a Bluetooth headphone, pause, disconnect and reconnect it,
and the queue stays paused with the row off and plays with it on.

## 35. Same-named albums' art (Oct 22)

V2.1's cover worker names a cover by the `md5` of the album's name alone, as V1.32's does, so the
split rows of a shared name (two artists' "Greatest Hits") shared one cover. On the Q2, `ALBUM_ART`
gives such rows a key with the album artist or the folder (`art_key`), at the renderer, the cover tasks
and the album page's big cover. V2.1 differs in where those are:
- **One page for both lists.** V2.1 lists the library's albums and an artist's on the same
  `album_page`: `loadAlbumList` loads `0xf003` or `0xff01`, and `ringnav_localclass` already splits
  the first and gives the second `artist_tab`'s keys (section 21's order). So the sites serve both:
  the row renderer's `snprintf(buf, 0x100, "%s", album)` (`0x523a34`, the row in `$s2`) and the page's
  three `albumcoverinfo_init` calls (`0x524720`, `0x524760`, `0x5248d0`). On M1,
  `ringnav_art_name` and `ringnav_albumcovers` take a row's artist key when the list is the artist's,
  else `art_key`. Loading the library's Albums drops the artist's keys.
- **The album page's big cover** (`img_albumcover_m`) formats `classinfo_save + 0xd` at `0x525b84`.
  `albuminfo_page_init` (`0x526828`) keeps the row it opened, its context's high half, at `0xa06680`,
  which is V2.1's `ALBUMINFO_ROW`. So `ringnav_art_header` is the Q2's.
- **Not patched:** search results (`pdeq_searchshowlist`, `0x54149c`, `0x542a28`), which the Q2 doesn't
  patch either.

On M1 the checks run V2.1's own renderer, cover-task and header code on an artist's albums whose
"Mid" shares its name with another artist's album: the renderer and tasks give it the folder key and
leave the others, and the header follows its row's task. With V2.1's renderer words put back, it gets
the bare name. The key and header helpers' Q2 checks run on M1 too. The V1.32 artist-page checks stay
Q2 only. `test/patch.py` on M1 passes 1004 scenarios, with 8 `NOT PORTED` lines; Q2's runs are
unchanged and its `update.tar` files byte-identical.

## 36. Dev 20 (V00Ks) for the device (Oct 22)

Built from commit `f21632f` with `--dev` (`build-m1-dev20`, `update.bin` `35474ff9…`). `test/build.py`,
`test/patch.py` (1004 scenarios, 8 `NOT PORTED`), `test/playback.py` and the three `test/boot.py` walks
pass on it. It was copied to the card over q2remote, hash-checked, as `update.bin`, ready for System
Update → TF card update. What to check on it:
- **Shuffle:** in stock Shuffle, Play next from the hold menu plays next; Previous then Next returns to
  the track Previous left.
- **Ratings:** a hold on Now Playing's heart opens the picker; a tap still toggles My Fav. A saved 1-4
  shows as a badge on the empty heart.
- **Hold menu:** Add to Favourites and Add to Playlist add the held song only; Add to Playlist from Now
  Playing refuses ("Queue unchanged") when the track changed meanwhile.
- **Lock Screen page:** the built-ins show as pictures, the grid scrolls to Time show, Clock and About,
  and every picture can be picked. Clock: Large lays out the lock window's clock.
- **Lock window:** Next shows the new track's cover (V2.1's own repaint).
- **Library:** an article-free sort (The Cure under C), M4B files in folder view, and covers that load
  after a small scroll on Albums.
- **Hardware and settings:** LDAC HQ at 990 kbps (WH-1000XM6, multipoint off); gapless in Shuffle
  Albums with Gapless on; Resume on Connect off keeps a paused queue paused on reconnect; two
  same-named albums by different artists show their own covers.

**On the device (dev 20, flashed Oct 22).** The user checked the first five items: Shuffle's Play next
and history, the Ratings hold and badge, the hold menu's adds and the playlist guard, the Lock Screen
page and Large clock, the lock window's cover, and the library items. Over q2remote:
- **Gapless:** with Gapless on, Shuffle Albums started on Foxes' "Rise Up (Intro)", queue position
  291. Reading `MCL_PREPOS` and `MCL_PRELOAD` from `demo`'s memory: about 10 s before its end the
  preload opened position 38, "Better Love", the album's next track (stock would have opened 292).
  At the change `MCL_POS` became 38 and the preload was used. Gapless was set back off. By ear the
  change sounded quick, but the card has no gapless album (Paramore's live tracks fade out), so the
  listening check is kept as a later validation in the roadmap's section 4.
- **Bluetooth:** with Bluetooth off, the page shows only its switch, so no Resume on Connect row, as
  intended. Turning Bluetooth on asks to turn Wi-Fi off first, which ends q2remote.
- **LDAC HQ:** measured on the WH-1000XM6. No screen shows the bitrate, so a logger started over
  q2remote (`setsid nohup`, it outlives Wi-Fi) sampled `hciconfig`'s TX byte counter every 5 s to the
  card while the user played on Auto, then HQ, then Standard. Steady samples: HQ about 133 KB/s
  (1064 kbps on air), Standard about 89 KB/s (711 kbps), a ratio of 1.50, which is 990/660 with about
  7.5% of Bluetooth packet overhead on both. Stock sends Standard's rate for HQ too (ratio 1).
  The Auto segment was too short to read.
- **Resume on Connect:** the user confirmed it with the WH-1000XM6.
- **Same-named albums:** the card's 24 albums share no name, across artists or folders, so that check
  needs two such albums on the card. It is kept as a later validation in the roadmap's section 4.

## 37. U0: the Q2 builds are upstream's again (Oct 22)

Roadmap U0, before the branch moves its M1 code beside upstream's (U1) and merges upstream 1.3.9 (U3).
Every sync checks the Q2 build by exact equality with the upstream base's, so no known difference can
be accepted. Legacy and iPod `update.tar` are now byte-identical to `main`'s build.

| Commit | Change | Why |
|---|---|---|
| `a547843` | `release.py` reads `input_sha256` (integration item 1) | `build.py` had renamed the manifest key, so `release.py package` failed with `KeyError` after its first build. |
| `8b239c1` | Q2 resumes `HOOKS \| IPOD_HOOKS` (item 3) | Legacy's five iPod trampolines were `return 0` stubs. The stubs are M1's only. |
| `264806f` | `dispatch_key_return` M1-only (item 4) | Its only caller is M1's back button. |
| `6c4f352` | `boot_guard`'s entry read M1-only (item 5) | On Q2 it could cancel a Centre release that `main` lets through. |
| `611bdc3` | V2.1's widget checks M1-only (item 6) | `qm_open`'s and `xfade_open`'s missing-widget checks, `widget_set_enable` and `arc_out`'s zero radius ran on Q2. |
| `a400c39` | `scratch_t` as `main`'s on Q2 (item 7) | `knob_mode` and a sixth `setting_label` grew Q2's state. |
| `94ec8a0` | The helpers' M1 paths by `#if M1PLUS` (item 8) | q2boot's `KEY_PLAYPAUSE` and q2video's 480-line screen were chosen at run time. |
| `91b3dcc` | `main`'s `ringnav_artist_list` on Q2 (item 9) | On M1 the body is `artist_tab(tab, n)`, which `ringnav_localclass` also calls. |
| `a0ecac9` | `main`'s `ringnav_audioset` on Q2 | Found by the compare: the static `audioset_rows` moved its strings in `.rodata`, shifting every string address after them. |
| `b7af86f` | The EQ's tab split rounded up | Found by the compare: 187 on Q2, where `main` has 188. It is 180 on M1 either way. |
| `ef2f638` | The Q2 AirPlay icon's mode from `list_tidal.png` | Found by the compare: the rootfs differed in that one file's mode. |

How it was checked:
- A function-by-function compare of `patch.elf`, with addresses normalised, then `cmp` of `patch.bin`,
  `q2boot`, `q2video`, the unpacked rootfs (`unsquashfs -lls` for modes) and `update.tar`.
- Each commit on its own: the three builds, the Q2 suites on Legacy and iPod, the host suites and the M1
  gates. At `ef2f638`: `test/patch.py` passes Legacy 1017, iPod 1398 and M1 1004 scenarios, and
  `test/boot.py`'s walk passes.
- `tools/release.py package` from `stock/`'s `update.tar`: both variants validated and reproducible,
  their `update.tar` `main`'s, with `pdftotext` added to the devShell's `PATH` for the user guide.

Item 7 moved `setting_label` back into the iPod block, where every use is, so the M1 payload's state
shrank, with no change in behaviour. Items 8 and 9 changed the M1's code too. q2video's M1 position bar
was checked on the host before and after item 8, and paints the same pixels. Those pixels show a bug the
M1 has had since `09dba3a`: the bar runs from x 20 to 460 on a 320 px row, so it spills into the next
row. It is in the roadmap's section 1.

## 38. The M1 release, and 1.2.2-m1.1 for the device (Oct 22)

`tools/release.py` is upstream's and packages only the Q2, so the M1's release goes beside it as
`tools/release_m1.py` ([m1plus-releasing.md](m1plus-releasing.md)).

| Commit | Change | Why |
|---|---|---|
| `a4734f4` | `build()` takes `m1_release=(name, tag)` | Every M1 build had the Q2 Legacy tag, `V122S`, so a second release of one upstream version would be refused over the first. A release's tag replaces it, and About's CFW. Version row shows the name. Q2 output is unchanged, and so is the plain M1 build. |
| `ea225e4` | `tools/release_m1.py`, `test/release_m1.py`, [m1plus-changelog.md](m1plus-changelog.md) | Two builds compared byte for byte, the first validated by its manifest, V2.1's updater rule and the M1 gates, a ZIP, notes and a record, and an upload to the fork as `release.py` does upstream. |

A release is named `<VERSION>-m1.<n>` by the changelog's top entry, and its tag is `V`, `VERSION`'s
digits and `n`. The last character is a digit, so the tag never equals a Q2 tag, a `--dev` one or another
release's. `test/release_m1.py` checks that over every name, as well as the identity checks and the
build and upload failure paths.

`release_m1.py package 'stock/M1 Plus Firmware V2.1/update.bin'` at `ea225e4` gives 1.2.2-m1.1 (`V1221`):
`update.bin` `7872e551…`, `M1Plus.Firmware.1.2.2-m1.1.zip` `241b5869…`. Both builds are byte-identical,
and `peq`, `build --build`, `patch` (1004 scenarios), `boot`, `playback`, `m4b` and `ldac` pass on it. It
is not uploaded. To check on the device, over dev 20 (`V00Ks`):
- **The flash:** the updater takes `V1221` over `V00Ks`. About shows FW. Version `V1221` and CFW. Version
  `1.2.2-m1.1`, which must fit its row.
- **What U0 changed in M1 code** (section 37), which should behave as on dev 20:
  - Display's **Knob**: Navigation moves the list and Previous goes back; Volume turns the volume.
  - **Videos** from a cold boot: the picture and sound play, and a seek shows the position bar. The bar
    still spills past the screen's width (roadmap section 1).
  - An **artist's albums** (Artists → an artist): in year or A-Z order, with their own covers.
  - **Playback Setting**: Year order, Artists A-Z and Crossfade are there, and still there after the EQ
    and back.
- **A quick pass:** the Q2 Pod page, Shuffle Songs, Coverflow by touch, a touch long-press's hold menu.
- **Back to stock** (optional): the TF card update with stock V2.1's `update.bin`.

A release build has no q2remote (it is a `--dev` helper), so state can't be read over Wi-Fi while it is
installed. Flashing a `--dev` build brings it back.

**The device pass (Oct 22).** It was copied to the card over dev 20's q2remote (hash checked), and the
user flashed it with the TF card update: the updater took `V1221` over `V00Ks`, and every item above
passed. It is not uploaded: it carries 1.2.2, which upstream has moved past, so the first published M1
release is the first after the 1.3.9 sync (U3), 1.3.9-m1.1.

## How to check a build now

```sh
python3 tools/build.py 'M1 Plus Firmware V2.1.zip' --out build-m1   # refuses unknown inputs and V2.1 names
python3 test/m1plus/build.py --build build-m1   # hook jumps, demo and rootfs diffs, updater rule, boot scripts
python3 test/m1plus/boot.py build-m1            # V2.1's demo under QEMU, stock vs patched, touch and key walk
python3 test/m1plus/boot.py build-m1 --home-menu  # the same with six Home cards: the Q2 Pod card on a page of its own
python3 test/m1plus/boot.py build-m1 --media    # a card with long songs, a book and two photos: Long Songs, Books, Photos and Coverflow by touch, Streaming, Shuffle Songs
python3 test/m1plus/patch.py build-m1           # payload under Unicorn, plus KNOWN GAP and NOT PORTED lines
python3 test/m1plus/playback.py build-m1        # and test/m1plus/m4b, id3, headset_io; test/ldac, bluealsa
```

On a `--dev` build, `python3 tools/q2remote.py` reaches the device over Wi-Fi: files, settings,
screenshots and input, without a manual pass ([remote.md](remote.md)).

To return a device to stock: put stock V2.1's `update.bin` at the card root and use System Update → TF
card update.

## Principles that came out of this

- **Read V2.1's own code before trusting a V1.32 value.** The correction pass (section 3) and every bug
  since came from a V1.32 address, offset, event number or name assumed to carry over.
- **Pin facts to V2.1's code in the tests, not to `offsets.inc`.** A value the payload and the tests
  both take from one file can be wrong in both.
- **Compare against stock.** In the emulator, stock under the same conditions is the control.
- **A skip has a name.** `KNOWN GAP` and `NOT PORTED` replace silent skips, and neither can quietly start
  passing.
- **Prove each new check can fail,** once, against a deliberately broken build.
- **A way out is on screen.** Every page has a visible Back button. A gesture or a key can't be the
  only exit. The hardware keys keep stock's meaning, except Previous in Knob: Navigation, which
  presses that same button.
