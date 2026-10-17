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

The branch leaves `main` at `b229c24`. There are 59 commits on `feature/m1plus-port`.

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

## How to check a build now

```sh
python3 tools/build.py 'M1 Plus Firmware V2.1.zip' --out build-m1   # refuses unknown inputs and V2.1 names
python3 test/build.py --build build-m1   # hook jumps, demo and rootfs diffs, updater rule, boot scripts
python3 test/boot.py build-m1            # V2.1's demo under QEMU, stock vs patched, touch and key walk
python3 test/patch.py build-m1           # payload under Unicorn, plus KNOWN GAP and NOT PORTED lines
python3 test/playback.py build-m1        # and m4b, id3, ldac, headset_io, bluealsa
```

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
