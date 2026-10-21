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

## How to check a build now

```sh
python3 tools/build.py 'M1 Plus Firmware V2.1.zip' --out build-m1   # refuses unknown inputs and V2.1 names
python3 test/build.py --build build-m1   # hook jumps, demo and rootfs diffs, updater rule, boot scripts
python3 test/boot.py build-m1            # V2.1's demo under QEMU, stock vs patched, touch and key walk
python3 test/boot.py build-m1 --home-menu  # the same with six Home cards: the Q2 Pod card on a page of its own
python3 test/boot.py build-m1 --media    # a card with long songs, a book and a photo: Long Songs, Books, Photos, Shuffle Songs
python3 test/patch.py build-m1           # payload under Unicorn, plus KNOWN GAP and NOT PORTED lines
python3 test/playback.py build-m1        # and m4b, id3, ldac, headset_io, bluealsa
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
