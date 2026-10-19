# Shanling M1 Plus Firmware Porting Analysis

Technical exploration, hardware breakdown, and reverse-engineered architecture for porting **Q2 Pod** to the **Shanling M1 Plus** (Firmware V2.1), based on **Q2 Pod v1.2.2** (the current upstream release).

---

## 1. Executive Summary & Feasibility

Porting Q2 Pod to the Shanling M1 Plus is **highly feasible**. This port targets **Q2 Pod v1.2.2**, carrying over its 30-band PEQ, ReplayGain, crossfade, visualizer, standalone Spotify Connect & Internet Radio, CUE/audiobook resume points, ratings, Coverflow 3D renderer, View Queue, and iPod Classic interface overhaul.

While the industrial design and hardware controls differ (an upright 3.2" portrait touchscreen, a side rotary encoder knob, and no physical Back/Return button instead of a landscape-mounted rounded panel with a capacitive front touch wheel), the underlying software stack comes from the same Shanling X2000 codebase family as the Q2:

| Component | Shanling Q2 (V1.32) | Shanling M1 Plus (V2.1) | Porting Impact |
| :--- | :--- | :--- | :--- |
| **CPU Architecture** | MIPS32r2 Little-Endian (`mipsel`, o32) | MIPS32r2 Little-Endian (`mipsel`, o32) | **Identical** |
| **GUI Framework** | ZLG AWTK (`/release/bin/demo`) | ZLG AWTK (`/release/bin/demo`) | **Identical** |
| **Audio Daemon** | `/usr/bin/hciplayer` (MPlayer fork) | `/usr/bin/hciplayer` (MPlayer fork) | **Identical architecture** |
| **Database Engine** | SQLite3 (`/mnt/data/database.db`) | SQLite3 (`/mnt/data/database.db`) | **Identical schema & APIs** |
| **ELF Injection Slot** | Unused `PT_NOTE`/`PT_NULL` header | Unused `PT_NOTE`/`PT_NULL` header | **Identical** |
| **Physical `/dev/fb0`** | `320 × 375` (`is_rotated=0`) | `320 × 480` (`is_rotated=0`) | Framebuffer height `+105 px` |
| **AWTK Logical UI Canvas** | **`375 × 320` landscape** (rotated 90° CW) | **`320 × 480` portrait** (upright, no 90° rotation) | **Width `-55 px` (`375` $\to$ `320`), Height `+160 px` (`320` $\to$ `480`)** |
| **Panel Shape** | Pill-shaped glass (`CORNER_R = 80` px) | Rectangular 3.2" panel (`CORNER_R = 0`) | Remove 80 px corner insets |
| **DAC / Audio Routing** | Integrated (`/dev/shanling_dac`) | ESS ES9069Q (`codec_es9069q.ko`) + Gowin FPGA (`gw_fpgadown.ko`) | Verify DAC device/ioctls for `q2video` |
| **Navigation Input** | Capacitive touch wheel (`ts_read`) + 5 buttons (incl. `KEY_RETURN`) | **3.2" Touchscreen (`gt9xx_touch.ko`) + GPIO Rotary Encoder + 4 buttons (no Return key)** | Hybrid touch + knob model; gesture/button replacement for `KEY_RETURN` |

---

## 2. Firmware Packaging & Container Analysis

The official firmware release file `update.bin` in `M1 Plus Firmware V2.1` is **an uncompressed standard POSIX tar archive** structured as follows:

```text
update.bin (tar archive)
├── firmware_v20.info
└── recovery-update/
    ├── xImage              (Ingenic Linux Kernel, ~5.4 MB)
    └── rootfs.squashfs     (SquashFS 4.0 filesystem, ~55.7 MB)
```

### Checksum & Verification Mechanism
The file `firmware_v20.info` contains:
```text
Shanling M1 Plus
V2.1
867d05c9895df6f3f136a7311f3b7a55  recovery-update/xImage
f63408dc999c94d70b5bd01f164b9162  recovery-update/rootfs.squashfs
```
- **No cryptographic signatures / RSA certificates**: The Shanling recovery update mechanism calculates the standard MD5 checksums of `recovery-update/xImage` and `recovery-update/rootfs.squashfs` and checks them against `firmware_v20.info`. Recovery runs from the device, not from `update.bin`, so this comes from the Q2 port and can't be checked here. `test/build.py` checks that the MD5 lines match the packed files.
- **What V2.1's updater accepts** (`update_firmware`, `0x4e0e34`, read from its code): line 1 of `firmware_v20.info` must equal demo's model string (`Shanling M1 Plus`, `0x747718`), and line 2 must contain a `V` and differ from demo's version literal (`V2.1`, `0x74773c`), or the card's `update.bin` is deleted unapplied. This is Q2's rule. `tools/build.py` writes its 5-character tag (`V122S`) to both the info file and that literal, so a build installs over stock, stock installs back over it, and the same build is refused once installed. `test/build.py` pins those instructions and checks the built archive against them.
- **Image format**: `tools/build.py` repacks the rootfs with stock's own settings (lzo, 128 KiB blocks, `-tailends`) and writes the archive with stock's GNU tar headers and member list. It refuses a rootfs larger than stock's, since stock's size is known to fit the partition (V2.1's rootfs shrinks by about 2.4 MB). `test/build.py` checks the superblock, members and headers against stock.
- **Flash layout** (`/proc/mtd` on the device): `uboot` 1 MiB, `kernel` 6 MiB, `rootfs` 75 MiB (`0x4b00000`), `kernel2` 6 MiB and `rootfs2` 12 MiB (a separate recovery system, which flashes the `recovery-update/` files V2.1's updater untars to the card), `userid`, `ota` and `userdata` (UBI, mounted at `/mnt/data`). The build's "no larger than stock" limit (55.7 MB) is well inside the rootfs partition.
- **Verified only on the device**: recovery's flash itself, and demo's startup. The emulator tests run the payload's hooks one by one with the toolkit mocked; nothing runs V2.1's whole demo. If demo dies at startup, `checkappprocess.sh` reboots about 10 s later, so know how to reflash stock V2.1 before the first boot test.

---

## 3. Hardware Architecture, Display Orientation & Input Mapping

### 3.1 System-on-Chip (SoC)
- **Processor**: Ingenic X2000 application processor (`Linux 5.10.21`).
- **CPU Cores**: Dual XBurst2 cores (clocked up to 1.2 GHz, MIPS32 Release 5 ISA) + one low-power XBurst0 auxiliary core (240 MHz).
- **Instruction Set**: Backward compatible with MIPS32r2. Code compiled with `clang -target mipsel-linux-gnu -mips32r2 -mabi=32` runs natively.

### 3.2 Display Orientation & Geometry (`375 × 320` Landscape vs. `320 × 480` Portrait)

> [!IMPORTANT]
> **Critical Orientation Difference:**
> On the **Shanling Q2**, `/dev/fb0` is `320 × 375` portrait (`is_rotated=0`), **but the physical LCD is mounted sideways**. AWTK renders the Q2 UI on a **`375 × 320` landscape canvas** (width = `375`, height = `320`, status bar = `30`, client height [`BOTTOM = 290`](file:///home/jtliang/Projects/q2-pod/tools/ipod.py#L29)) and rotates frames 90° clockwise onto `/dev/fb0`.
>
> On the **Shanling M1 Plus**, both the LCD (`lcd_h320qn01.ko`), the touchscreen (`gt9xx_touch.ko`: `gtp_x_coords_max=320`, `gtp_y_coords_max=480`, `gtp_x_y_coords_exchange=0`), and AWTK operate in **upright `320 × 480` portrait** (width = `320`, height = `480`, status bar = `30`, client height = `450`) with **no 90° rotation**.

 Consequently, every hardcoded `375` in Q2 Pod is a **horizontal width**, not a height:
- **Logical UI Width shrinks by `55 px`**: `375 px` $\to$ `320 px`.
- **Logical UI Height grows by `160 px`**: `320 px` (`290 px` client area) $\to$ `480 px` (`450 px` client area).
- **Corner Radius (`CORNER_R`)**: The Q2 has a pill-shaped glass bezel with an `80 px` corner radius ([`CORNER_R = 80`](file:///home/jtliang/Projects/q2-pod/tools/ipod.py#L30), [`STATUS_MARGIN = 52`](file:///home/jtliang/Projects/q2-pod/tools/ipod.py#L32), [`BAR_CORNER_R = 76`](file:///home/jtliang/Projects/q2-pod/patch/offsets.inc#L323)), which curves top/bottom list rows and insets the status bar via [`corner_inset(y)`](file:///home/jtliang/Projects/q2-pod/tools/ipod.py#L39-L43) and [`arc_inset()`](file:///home/jtliang/Projects/q2-pod/patch/navigation.c#L604-L621). The M1 Plus has a rectangular display; these corner insets must be set to `0` (with standard rectangular margins) so rows and status bar icons are not pinched inward.
- **180° Screen Flip (`ROTATEMODE=1`)**: `/etc/init.d/S11logo_display_shell` checks `grep -c "ROTATEMODE=1" /mnt/data/config.ini` to choose between `/release/assets/default/raw/images/xx/logo180.jpg` and `logo.jpg`. Boot logo hooks ([`LOGO_HOOK`](file:///home/jtliang/Projects/q2-pod/tools/build.py#L161-L163) and [`logo_sync`](file:///home/jtliang/Projects/q2-pod/patch/navigation.c#L5866-L5898)) must accept upright `320 × 480` baseline JPEGs without applying Q2's `ffmpeg -vf transpose=1` 90° rotation.

### 3.3 Audio, FPGA & Peripheral Hardware
Discovered from `/module_driver/driver_default_init_script.sh`:
- **DAC & Sound Card**: ESS Sabre ES9069Q (`codec_es9069q.ko` with `pwr_gpio=PB10 pdn_gpio=PB15 po_mute_gpio=PB11 bal_mute_gpio=PB12 digital_gpio=PC08 bal_en_gpio=PB25 dac_gpio2_gpio=PB14 i2c_bus_num=1` and `x2000_510_es9069q_sound_card.ko`).
- **FPGA**: Gowin FPGA loaded via JTAG (`gw_fpgadown.ko` with `fpga_tck=PC20 fpga_tms=PC01 fpga_tdi=PC21 fpga_tdo=PC22` in `fpgadown.sh`).
- **Amplifiers**: Dual SGM8262 op-amps supporting 3.5mm Single-Ended (`g_po_status`) and 4.4mm Balanced (`g_bal_status`) outputs, plus 3.5mm coaxial S/PDIF digital output.
- **Wi-Fi / Bluetooth**: Realtek `rtl8733bs.ko` + `hci_uart_h5_kernel_5_10_21.ko`.
- **Atmosphere LED**: `led_ktd2026.ko` on `i2c_bus_num=5` (multi-color status ring around knob).
- **Buzzer / Key Tone**: none. V2.1's `demo` has no buzzer command (`cmd_mcu write_str buzzer`) and no `buzzeer_switch`, so Key Tone is Q2 only (`test/build.py` checks the strings are absent).

### 3.4 Physical Inputs, Kernel Drivers & AWTK Key Translation
Discovered from `/module_driver/keyboard_encoder_add.sh`, `/module_driver/keyboard_gpio_add.sh`, `/module_driver/gt9xx_touch.sh`, and `/etc/init.d/S90play`:

| Input Control | Hardware Pin / Driver | Linux `input_event` Code | Stock AWTK `EVENT_KEY` (`offsets.inc`) | Notes |
| :--- | :--- | :--- | :--- | :--- |
| **Rotary Knob (Turn CCW/Down)** | GPIO `PB19` (`keyboard_encoder.ko`) | `KEY_VOLUMEDOWN` (`114`) | Verify in M1 Plus `demo` (`KEY_PREV = 172` on Q2) | Discrete GPIO encoder pulses (not `tslib`!) |
| **Rotary Knob (Turn CW/Up)** | GPIO `PB18` (`keyboard_encoder.ko`) | `KEY_VOLUMEUP` (`115`) | Verify in M1 Plus `demo` (`KEY_NEXT = 173` on Q2) | Discrete GPIO encoder pulses (not `tslib`!) |
| **Rotary Knob (Press In)** | GPIO `PE31` (`keyboard_gpio_add.ko`) | `KEY_POWER` (`116`) | `KEY_CENTER` (`218`) | Also wakes hardware (`wakeup=y`) |
| **Play / Pause Button** | GPIO `PB02` (`keyboard_gpio_add.ko`) | `KEY_PLAYPAUSE` (`164`) | `KEY_PLAY` (`171`) | On Q2 Linux code was `108` (`KEY_DOWN`) |
| **Next Track Button** | GPIO `PE26` (`keyboard_gpio_add.ko`) | `KEY_NEXTSONG` (`163`) | `KEY_FWD_BTN` (`215` on V2.1, `223` on Q2) | Active high (`active_level=1`) |
| **Previous Track Button** | GPIO `PB03` (`keyboard_gpio_add.ko`) | `KEY_PREVIOUSSONG` (`165`) | `KEY_BACK_BTN` (`214` on V2.1, `222` on Q2) | Active low (`active_level=0`). Back in Knob: Navigation (§4.2) |
| **Physical Return Button** | **None on M1 Plus** | N/A | `KEY_RETURN` (`170`) | **Missing in hardware — must be synthesized** |
| **Touchscreen** | Goodix (`gt9xx_touch.ko`, I2C0) | `/dev/input/event2` (`TSLIB_TSDEVICE`) | `EVT_POINTER_DOWN/MOVE/UP` | `320 × 480`, `flip=0`, `exchange=0` |

> [!WARNING]
> **1. Linux Keycodes vs. AWTK `EVENT_KEY` Codes:**
> Linux kernel keycodes (`114`, `115`, `116`, `163`, `164`, `165`) are read from `/dev/input/event*` by `demo`'s input thread and translated into AWTK's internal `EVENT_KEY` numbers (`170`–`223` in [`patch/offsets.inc`](file:///home/jtliang/Projects/q2-pod/patch/offsets.inc#L329-L335)) *before* reaching [`window_manager_dispatch_input_event`](file:///home/jtliang/Projects/q2-pod/patch/navigation.c#L6126) or [`on_wm_keyup_before_fun` (`ringnav`)](file:///home/jtliang/Projects/q2-pod/patch/navigation.c#L6353). Do not compare `I(event, EVENT_KEY)` against raw Linux keycodes `114`/`115`/`116` inside AWTK hooks; inspect M1 Plus's key translation table in `demo` (and `encoderknob_thread_run` / `gpio_keys` reader) first.
>
> **2. Do Not Hook `ts_read` (`WHEEL_TS_READ`) on M1 Plus:**
> On the Q2, the touch wheel is a capacitive strip on `/dev/input/event1` read via `ts_read` ([`WHEEL_TS_READ = 0x6258cc`](file:///home/jtliang/Projects/q2-pod/tools/build.py#L140), hooked by [`ringnav_ts_read`](file:///home/jtliang/Projects/q2-pod/patch/playback.c#L684-L699)). On the M1 Plus, `TSLIB_TSDEVICE=/dev/input/event2` is the main touchscreen, while the rotary knob uses `keyboard_encoder.ko`. Hooking `ts_read` with `ringnav_ts_read` on M1 Plus would corrupt touchscreen coordinates!

---

## 4. Navigation & Interaction Architecture

On the Shanling Q2, navigation is built around the front capacitive touch wheel and a dedicated physical Return button. On the M1 Plus, the 3.2-inch capacitive touchscreen is the primary interface, the side rotary knob is the hardware volume wheel, and **there is no physical Return/Back button**.

```mermaid
flowchart TD
    subgraph Input ["M1 Plus Input Sources"]
        Touch["3.2\" Capacitive Touchscreen (/dev/input/event2)"]
        BackBtn["Title-Bar Back Button (every payload page)"]
        Knob["Side Rotary Encoder (PB18 / PB19)"]
        KnobPress["Knob Push (PE31 / KEY_POWER)"]
        SideBtns["Side Buttons (Play/Pause, Next, Prev)"]
    end

    subgraph NavEngine ["M1 Plus Pod Navigation Engine"]
        TouchEngine["Direct Touch & Inertial Glide"]
        SynReturn["Synthesize KEY_RETURN (170)"]
        KnobMode{"Knob Function Setting"}
        VolCtrl["Hardware Volume & volume_dialog"]
        ListNav["Menu & List Navigation (KEY_PREV / KEY_NEXT -> ramp)"]
    end

    Touch --> TouchEngine
    BackBtn --> SynReturn
    Knob --> KnobMode
    KnobMode -->|"Volume (Default)"| VolCtrl
    KnobMode -->|"Navigation"| ListNav
    KnobPress --> Action["Context Action (Confirm Row / Screen Wake-Sleep)"]
    SideBtns --> MediaOrBack["Transport Controls / Hold Queue Menu"]
```

### 4.1 Solving the Missing Physical `KEY_RETURN` (`170`) Button
In Q2 Pod, [`KEY_RETURN`](file:///home/jtliang/Projects/q2-pod/patch/offsets.inc#L329) is the sole exit path for:
- Every custom full-screen page created via [`page_open()`](file:///home/jtliang/Projects/q2-pod/patch/coverflow.c#L926-L934) (a bare window: on M1 Plus its back button comes from `page_title` or `back_button`):
  - Coverflow ([`coverflow.c:keyup`](file:///home/jtliang/Projects/q2-pod/patch/coverflow.c#L1696))
  - 30-Band PEQ / 10-Band EQ / 3-Band EQ ([`peq_ui.c:keyup`](file:///home/jtliang/Projects/q2-pod/patch/peq_ui.c#L661))
  - Photos viewer ([`photos.c:keyup`](file:///home/jtliang/Projects/q2-pod/patch/photos.c#L118))
  - Books reader & Video player ([`books.c:keyup`](file:///home/jtliang/Projects/q2-pod/patch/books.c#L628), [`video.c:video_key`](file:///home/jtliang/Projects/q2-pod/patch/video.c#L329))
  - Crossfade settings ([`crossfade.c:keyup`](file:///home/jtliang/Projects/q2-pod/patch/crossfade.c#L61))
  - Spotify Connect & Internet Radio ([`spotify.c:keyup`](file:///home/jtliang/Projects/q2-pod/patch/spotify.c#L728), [`radio.c:keyup`](file:///home/jtliang/Projects/q2-pod/patch/radio.c#L129))
  - Shuffle, Most Played, Ratings, and Long Songs pages ([`navigation.c:page_keyup`](file:///home/jtliang/Projects/q2-pod/patch/navigation.c#L4145))
- Returning from the iPod Home `Settings` submenu ([`coverflow_home_back`](file:///home/jtliang/Projects/q2-pod/patch/coverflow.c#L1971))
- Opening Now Playing from Home or via hold ([`HOLD_RETURN`](file:///home/jtliang/Projects/q2-pod/tools/build.py#L121), [`compact_now_playing`](file:///home/jtliang/Projects/q2-pod/patch/navigation.c#L3504))
- Canceling an active scrub on Now Playing ([`navigation.c:6399`](file:///home/jtliang/Projects/q2-pod/patch/navigation.c#L6399))

**Rule: every page has an explicit Back button.** On M1 Plus, every page Q2 Pod opens or replaces
shows V2.1's title-bar back button at its top left (`btn_return`'s style and `return`/`return_down`
icons, named in `offsets.inc` so the build's V2.1 name check covers them). Make it with
[`back_button`](../patch/coverflow.c), or with `page_title`, which adds one beside the title. Its
click sends `KEY_RETURN` through `dispatch_key_return` on a timer, so the page's own keyup decides
what Back means: close the page, or step back one screen as the PEQ editor's Advanced tab does.
No gesture, hidden tap or key may be a page's only way out. A new page's `test/boot.py` step
closes it with that button.

**The Back button is always there.** V2.1's own pages have theirs. In Knob: Volume, Previous, Next
and Play/Pause stay media keys, as on stock. In Knob: Navigation, Previous also goes back: it
presses the page's back button (§4.2). It is a second way out, never the only one.

Three earlier ways in are gone:
- **The left-edge swipe and the title tap.** Nothing on screen showed them, and the swipe had to
  hold back every touch in the left 32 px of every page, stock pages included
  ([m1plus-progress.md](m1plus-progress.md) §11).
- **Previous as Return while nothing played.** Its Return skipped `wake_gate`'s screen-off drop, so
  a bump of Previous with the screen off closed a page nobody could see, even with the keys locked
  ([m1plus-progress.md](m1plus-progress.md) §13). Previous as Back in Knob: Navigation (§4.2) only
  acts where the knob navigates, which needs the screen on.

### 4.2 Side Rotary Knob (Volume by Default, Navigation Optional)
The side rotary knob defaults to **standard hardware volume control** out of the box, preserving normal M1 Plus volume wheel behavior.

Two rows in **System Settings $\rightarrow$ Display setting** provide:
- `Knob: Volume (Default) | Navigation`, saved as `config.ini [Q2POD] KNOB` (0 or 1).
- `Knob Up: List Up (Default) | List Down`, saved as `[Q2POD] KNOBDIR` (0 or 1): which way
  Navigation moves the list for a turn in the volume-up direction. List Up makes it `KEY_PREV`.

The remap happens on the key's release, in [`ringnav()`](../patch/navigation.c) (the
`on_wm_keyup_fun` hook), before stock's key-up runs. That is enough, because V2.1 turns the volume
there: `on_wm_keyup_fun` opens the volume dialog for keys 220/221. V2.1 binds no key-down handler
(`home_page_init` binds key-up and key-long only), so there is no key-down to remap. `test/build.py`
pins both facts.

When switched to **Navigation**:
- **In Menus, Lists, Coverflow, Books & EQ**:
  - Turning the knob translates encoder ticks into AWTK `KEY_PREV` (`172`) / `KEY_NEXT` (`173`) events (volume up is `KEY_PREV`, up the list, unless `Knob Up: List Down`) (suppressing stock volume changes) and feeds them into [`ringnav()`](file:///home/jtliang/Projects/q2-pod/patch/navigation.c#L6353) with duration acceleration (`ramp()`), edge bumping (`BUMP_PX`), and list wrap-around (`EDGE_PAUSE_MS`).
- **Previous is Back** (`KEY_BACK_BTN`, or `KEY_FWD_BTN` while `rotate_mode` is 1, since V2.1 swaps
  the two on a rotated screen): on its release, a timer clicks the top page's first showing button
  in `navbar_btnreturn_style`. That is V2.1's own back button, whose click is `on_back_onclick` (its
  pages take no `KEY_RETURN`), or the payload's `back_button`, whose click is a Return. On Home,
  Previous stays Previous track: there is nothing to go back to. Where the knob keeps the volume
  (below), Previous stays a media key too.
- **Knob Push (`KEY_POWER` $\to$ `KEY_CENTER`)**:
  - In Navigation mode: Single press activates the selected row (`confirm_center`), while double press toggles the screen off (`DOUBLE_CLICK_MS`).
  - In Volume mode: Single press wakes or sleeps the display immediately (stock behavior).
- **Context Fallback to Volume**:
  - Even in Navigation mode, the knob stays volume wherever the payload doesn't navigate (`knob_nav_active`: `usable()` and a context page). That covers `playing_page` and its enlarged art (`bigcover_page`), the volume dialog, the screen off (`!g_backlight_status`), Bluetooth receiver mode (`bluetoothrecv_page`, `btrecv_pageflag`) and USB DAC mode (`usbmode_page`, `usblink_status` 2). A knob press held by the boot guard stays Power.

### 4.3 Touch Long-Press Opens the Hold Menu
On the Q2, Play/Pause held on a highlighted row opens Q2 Pod's hold menu for that row: Play Next, Add to Queue, Favourites, Rate Album and the rest. On the M1 nothing is highlighted unless the knob is in Navigation mode. So a finger held still for 500 ms (`LONG_PRESS_MS`) on a row or tile of a library page opens the same menu for the row under the finger. That covers an artist's albums, Albums, Artists, Composers, Genres, All Songs, an album's tracks, Folders and Playlists. A press that moves is the list's scroll, and the row doesn't open on the release. Play/Pause held with nothing highlighted is still V2.1's own sort dialog. See [internals.md](internals.md#queue-menu).

### 4.4 The Q2 Pod Home Card and Page
V1.32 has a Local Music menu that Q2 Pod extends with its own rows. V2.1 has none: its Home *is* the library, a grid of cards the user picks in V2.1's Home menu editor. So the M1 build adds one card, **Q2 Pod**, after V2.1's own, and it opens a payload page (`library_page`) with the rows Q2 Pod adds to the Q2's Library: Shuffle, Ratings, Most Played, Long Songs, then Podcasts, Audiobooks, Photos and Books (each only when its folder is on the card), Coverflow, and Upload Scrobbles (only with an account). Videos waits for q2video on the M1's DAC.

- **No asset changes.** V2.1 builds the grid in code: `home_page_init`'s builder (`0x534064`) lays out `pdeq_choicemenu`'s ids six to a page of `home_sview` (a slide_view) and sets `home_sindicator`'s count. [`home_card`](../patch/coverflow.c) adds the card in the next slot exactly as V2.1's card builder (`0x533d8c`) places its own, or on a new page when the last one is full. The icon pair (`home_q2pod.png`, `_down`) is new art in V2.1's 66 px card style, added to the rootfs like the row icons.
- **V2.1's card click can't see it.** V2.1's card click (`0x533b80`) reads `atoi(name)` as one of its 18 ids, and the card's image has no name and its own click.
- **It survives V2.1's rebuilds.** Turning cards on or off in the editor, or changing the language, makes V2.1 rebuild the grid the next time Home comes to the front, which destroys every card. The card binds its own to-foreground handler before V2.1's init binds V2.1's, so it runs after V2.1's rebuild and puts the card back once. `test/build.py` pins the builder's only two callers.
- **The page** is built from `page_open` and `page_list` (title bar and back button) with V2.1's 64 px rows (`list_row`). Coverflow's carousel, the photo viewer and the book reader got the back button over their content, and Coverflow's covers go back to this page, not Home.

---

## 5. Verified Memory Addresses, Symbols & Patch Inventory

### 5.1 Audited Hook Targets in `/release/bin/demo` (24 Verified + 33 Remaining)
[`tools/build.py`](file:///home/jtliang/Projects/q2-pod/tools/build.py#L26-L116) installs **57 function hooks** in total: **49 `HOOKS`**, **6 `IPOD_HOOKS`**, and **2 leaf hooks (`IPOD_LEAF`, `WM_PAINT_LEAF`)**.

> [!IMPORTANT]
> **32-Byte Preamble Constraint:**
> Every non-leaf hook in `HOOKS` and `IPOD_HOOKS` is installed by [`make_trampoline`](file:///home/jtliang/Projects/q2-pod/tools/build.py#L436-L452), which copies the first **8 instructions (`32 bytes`)** of the target function into a trampoline and asserts `not has_branch_or_jump(insn)`. All 55 preamble-hooked functions in M1 Plus's `demo` must be checked to ensure no branch (`beq`/`bne`/`bgez`/etc.) or jump (`jal`/`j`) occurs within their first 8 instructions.

#### Verified M1 Plus V2.1 Hook Addresses (25 of 57)

| Function / Symbol | Q2 V1.32 Address | M1 Plus V2.1 Address | Hook Handler (`patch/`) | Purpose |
| :--- | :--- | :--- | :--- | :--- |
| `home_page_init` | `0x00523c84` | `0x00534cd4` | `coverflow_home` | Binds Home menu rows, Coverflow, Settings |
| `playing_page_init` | `0x0052ca88` | `0x0053d1e4` | `ringnav_playing` | Now Playing UI layout, album art, ratings |
| `widget_dispatch` | `0x0065e0ec` | `0x0066cec8` | `ringnav_dispatch` | Intercepts click events before native execution |
| `widget_on_paint_border` | `0x006596a0` | `0x00668810` | `ringnav_paint` | Selection outlines, Coverflow 3D frame, badges |
| `window_manager_dispatch_input_event` | `0x0066d49c` | `0x00677b74` | `ringnav_input` | Master input gate (`wake_gate`, `q2video` keys) |
| `playset_equalizer_page_init` | `0x004b642c` | `0x0049e358` | `peq_page_init` | Injects 3EQ / 10EQ / 30-band PEQ UI |
| `set_equalizer_value` | `0x004f9230` | `0x004d851c` | `peq_set_equalizer_value` | Links EQ state to `/dev/shm/q2peq` |
| `folder_page_init` | `0x00523330` | `0x0053349c` | `ringnav_folder` | Folder navigation & media shortcuts |
| `folder_back` | `0x00507ac8` | `0x004dbecc` | `ringnav_folder_back` | Directory navigation back behavior |
| `scanAllMusicFile` | `0x004fc788` | `0x004e9df4` | `ringnav_scan_all` | Invalidates Coverflow cache on full scan |
| `scanSpecFolder` | `0x004fc964` | `0x004e9e90` | `ringnav_scan_folder` | Invalidates Coverflow cache on folder scan |
| `deleteMusicFromMusicDb` | `0x00500b5c` | `0x004ede44` | `ringnav_db_delete` | Invalidates Coverflow cache on song delete |
| `toolsQueryDbTable` | `0x005c8044` | `0x005ee77c` | `ringnav_query_db` | Filters Spoken (Podcasts/Audiobooks) from music |
| `systemset_about_page_init` | `0x004bc80c` | `0x004a170c` | `ringnav_about` | Displays Stock & CFW Version rows |
| `systemset_display_page_init` | `0x004c1d04` | `0x004a5eb8` | `ringnav_display` | Adds Theme, Home, Coverflow, Accent rows |
| `systemset_sysset_page_init` | `0x004cc4cc` | `0x004ada78` | `ringnav_systemset` | Reorders System Settings & adds Boot target |
| `systemset_powermanager_page_init` | `0x004c72d0` | `0x004a9d18` | `ringnav_power` | Adds Charge Limit, Low Power, Wake options |
| `main_loop_sleep_default` | `0x00648f00` | `0x00658f70` | `ringnav_sleep` | Polls subsystems & extends screen-off sleep |
| `mclLoadPlayList` | `0x005aa8d4` | `0x005d1f28` | `ringnav_load_playlist` | Queue management & group shuffle tracking |
| `mclNextSong` | `0x005adbbc` | `0x005d5800` | `ringnav_next_song` | Track advance & group shuffle |
| `mclPrevSong` | `0x005ada98` | `0x005d56dc` | `ringnav_prev_song` | Track retreat (<5s restart vs previous) |
| `mclStartPlayer` | `0x005ad6ac` | `0x005d5300` | `ringnav_start_player` | Yields Spotify/Radio & applies playback speed |
| `mcl_tidalStartPlayer` | `0x005ad240` | `0x005d5184` | `ringnav_tidal_start` | Tidal streaming playback start |
| `save_memoryplay_info` | `0x00516344` | `0x004e3340` | `ringnav_save_memory` | Saves playback queue and position on suspend |
| `memeory_startplayer` | `0x005164e0` | `0x004e34dc` | `ringnav_memory_start` | Resumes playback queue at startup |

#### Remaining 32 `demo` Hooks to Resolve in M1 Plus `demo`
From [`tools/build.py`](file:///home/jtliang/Projects/q2-pod/tools/build.py#L26-L116):
- **Core Input & Painting**: `on_wm_keyup_before_fun` (`0x511c74` $\to$ `ringnav`), `on_wm_keydown_before_fun` (`0x5117d4` $\to$ `ringnav_keydown`), `on_wm_LongKeydown_before_fun` (`0x511ad8` $\to$ `ringnav_keylong`), `on_wm_pointer_down_before_fun` (`0x511f08` $\to$ `ringnav_touch`), `widget_on_paint_background` (`0x6595b4` $\to$ `ringnav_paint_bg`), `widget_on_paint_self` (`0x659628` $\to$ `ringnav_paint_self`), `window_manager_paint` (`0x66df68` $\to$ `ringnav_wm_paint`, leaf hook), `buzzeer_switch` (`0x4f3cc8` $\to$ `ringnav_buzzer`).
- **Library, Lists & Artwork**: `localmusic_page_init` (`0x524928` $\to$ `ringnav_localmusic`), `load_localclass_list` (`0x504698` $\to$ `ringnav_localclass`), `load_localartist_list` (`0x5069a4` $\to$ `ringnav_artist_list`; V2.1 has none: `loadAlbumList` loads an artist's albums through `loadLocalClassList(0xff01)`, where `ringnav_localclass` now orders them by year or A–Z and keeps their album ids for Rate Album. Rate Album can't be reached yet: the hold menu acts on the highlighted row, and nothing highlights one on M1 until Knob Navigation Mode or a touch long-press lands ([m1plus-roadmap.md](m1plus-roadmap.md) §2). The art keys still need V2.1's renderer sites), `load_album_detaillist` (`0x5063e0` $\to$ `ringnav_album_detail`), `folder_load_top` (`0x507d68` $\to$ `ringnav_folder_top`), `playlist_rebuild` (`0x4b20dc` $\to$ `ringnav_playlist`), `stock_search` (`0x4b3388` $\to$ `ringnav_search`), `albumcoverinfo_init` (`0x4ee6c0` $\to$ `ringnav_albumcovers`), `artist_covers` (`0x4ab9e0` $\to$ `ringnav_artist_covers`), `list_get_img_pic` (`0x501134` $\to$ `ringnav_badge`, leaf hook in iPod mode).
- **Playback, PEQ & ReplayGain**: `playset_page_init` (`0x4b7778` $\to$ `ringnav_playset`), `playset_Filter_page_init` (`0x4b6bec` $\to$ `ringnav_filter`), `playset_replaygain_page_init` (`0x4b7234` $\to$ `ringnav_rg_page`), `get_replaygain_value` (`0x5aa474` $\to$ `peq_get_replaygain_value`), `mclSend Eq` (`0x5abc3c` $\to$ `peq_mcl_send_eq`), `mclSetPlaySpeed` (`0x5abd2c` $\to$ `ringnav_speed`), `mclStopPlayer` (`0x5ae214` $\to$ `ringnav_stop_player`), `on_player_autochange` (`0x50f8cc` $\to$ `ringnav_autochange`), `player_load_songlist` (`0x50eb34` $\to$ `ringnav_load_songlist`), `config_playmode` (`0x4f849c` $\to$ `ringnav_playmode`).
- **Bluetooth, Streaming & Screensaver**: `stream_page_init` (`0x4ba98c` $\to$ `ringnav_stream`), `tidal_ReadSessionInfo` (`0x5ca180` $\to$ `ringnav_tidal_session`), `systemset_bluetooth_page_init` (`0x4bdfbc` $\to$ `ringnav_bt_page`), `btmenu_rows` (`0x4beae8` $\to$ `ringnav_bt_rows`), `bt_AutoConnect_proc` (`0x4dbf78` $\to$ `ringnav_bt_autoconnect`), `mclSetBtSoftwareVolume` (`0x5ac93c` $\to$ `ringnav_btvol`), `systemset_screensaver_page_init` (`0x4c9cb0` $\to$ `ringnav_screensaver`), `screensaver_rows` (`0x4ca160` $\to$ `ringnav_saver_rows`), `standy_page_init` (`0x530c34` $\to$ `ringnav_standby`), `saver_cover` (`0x530754` $\to$ `ringnav_saver_cover`), `statusbar_page_init` (`0x531dd0` $\to$ `ringnav_statusbar`).

### 5.2 Unnamed Static Functions (`PRIVATE_FUNCTIONS`) & Raw Offsets
In addition to dynamic symbol table entries (`FUNCTIONS`, `GLOBALS`, `CONTEXT_DATA`), [`tools/build.py`](file:///home/jtliang/Projects/q2-pod/tools/build.py#L217-L235) and [`patch/offsets.inc`](file:///home/jtliang/Projects/q2-pod/patch/offsets.inc#L326-L418) reference unnamed `static` functions and raw `.bss`/`.data`/`.rodata` addresses that must be located by disassembly pattern matching in M1 Plus's `demo`:
1. **17 `PRIVATE_FUNCTIONS`** ([`tools/build.py:217-235`](file:///home/jtliang/Projects/q2-pod/tools/build.py#L217-L235)):
   `keylock_rows`, `quick_lock`, `playlist_rebuild`, `stock_search`, `slide_menu_item_width`, `slide_menu_on_scroll_done`, `mcl_preload`, `mcl_open_preload`, `btmenu_rows`, `mcl_shuffle_pick`, `album_row`, `folder_refresh`, `class_icon`, `screensaver_rows`, `saver_cover`, `np_info`.
2. **Raw Addresses in [`patch/offsets.inc`](file:///home/jtliang/Projects/q2-pod/patch/offsets.inc) & `.c` Files**:
   - AWTK vtables: [`DEFAULT_LAYOUT_VTABLE`](file:///home/jtliang/Projects/q2-pod/patch/offsets.inc#L326), [`LIST_VIEW_LAYOUT`](file:///home/jtliang/Projects/q2-pod/patch/offsets.inc#L327), [`LIST_VIEW_LAYOUT_SLOT`](file:///home/jtliang/Projects/q2-pod/patch/offsets.inc#L328).
   - Input latches: [`KEY_LOCKOUT`](file:///home/jtliang/Projects/q2-pod/patch/offsets.inc#L365), [`BOOT_KEY_GUARD`](file:///home/jtliang/Projects/q2-pod/patch/offsets.inc#L366), [`RETURN_RELEASE_LATCH`](file:///home/jtliang/Projects/q2-pod/patch/offsets.inc#L367).
   - Media control internals: [`ALBUMINFO_ROW`](file:///home/jtliang/Projects/q2-pod/patch/offsets.inc#L372), [`MCL_POOL` through `MCL_FD` and `USB_MIXER`](file:///home/jtliang/Projects/q2-pod/patch/offsets.inc#L373-L384), [`SCAN_THREAD` & `SCAN_DONE`](file:///home/jtliang/Projects/q2-pod/patch/offsets.inc#L417-L418), [`pdeq_btpairlist`](file:///home/jtliang/Projects/q2-pod/patch/headset.c#L17), `responseSetVolume` byte ([`0xa38c41`](file:///home/jtliang/Projects/q2-pod/patch/navigation.c#L6052)).
   - Event callbacks: [`SORTSELECT_KEYUP` & `SORTSELECT_CLOSE`](file:///home/jtliang/Projects/q2-pod/patch/offsets.inc#L385-L386), [`BOOTVOL_TOGGLE` / `UP` / `DOWN`](file:///home/jtliang/Projects/q2-pod/patch/offsets.inc#L388-L390), [`FAV_CLICK`](file:///home/jtliang/Projects/q2-pod/patch/navigation.c#L4320), [`PLAYLIST_PICK`](file:///home/jtliang/Projects/q2-pod/patch/navigation.c#L5175), and `initconfig` caller return address in [`ringnav_speed`](file:///home/jtliang/Projects/q2-pod/patch/playback.c#L603).
3. **Inline Instruction Patches (`patch_word`)**:
   - [`tools/build.py`](file:///home/jtliang/Projects/q2-pod/tools/build.py#L120-L163): `SHUFFLE_CALL`, `HOLD_RETURN`, `STANDBY_WAKE`, `BT_CONNECT_START`, `AUDIO_EXTENSION_CALLS` (15 sites for `.m4b`), `SORT_TRIMS` (4 sites), `SCAN_LIMIT` (65,000 song limit), `ALBUM_ART`, `ALBUM_ART_ROW`, `CLASS_ICON`, `COVER_PAUSE`, `ARTIST_COVER_ROW`, `LDAC_HQ`, `DROP_CACHES`, `NP_INFO_CALL`, `LOGO_HOOK`, `ringnav_bootmode`, `ringnav_cover_done`, Tidal null guards, `INITCONFIG_MODE_RET`, `STYLE_COLOR_GRADIENT_RET`.
   - [`tools/ipod.py`](file:///home/jtliang/Projects/q2-pod/tools/ipod.py#L465-L539): `ARTIST_ALBUMS`, `lookup` unwind, 23 `AUDIT['immediates']`, 8 `AUDIT['row_layout_calls']`, All Songs swipe-delete disable, playlist tile geometry, and `toolsTimeItoa`.

### 5.3 SQLite Library Queries (Coverflow & Local Music)
All stock database functions in `demo` retain identical function signatures:

| SQLite Query Function | Q2 V1.32 Address | M1 Plus V2.1 Address |
| :--- | :--- | :--- |
| `getAllAlbum` | `0x004ffda8` | `0x004ea3c4` |
| `getMusicByAlbum` | `0x00502540` | `0x004ecb5c` |
| `toolsQueryDbTable` (also hooked) | `0x005c8044` | `0x005ee77c` |
| `getMusicBySonger` | `0x005021c8` | `0x004ec7e4` |
| `GetAllAlbumArtist` | `0x005000c8` | `0x004ea6e4` |
| `getMusicByAlbumAndSonger` | `0x00502720` | `0x004ecd3c` |
| `getMusicByAlbumAndAlbumSonger` | `0x005029ec` | `0x004ed008` |
| `getMusicByAlbumAndComposer` | `0x00502cb8` | `0x004ed2d4` |
| `getMusicByAlbumAndGenre` | `0x00502f84` | `0x004ed5a0` |

### 5.4 Audio Player (`/usr/bin/hciplayer` — [`tools/peq.py`](file:///home/jtliang/Projects/q2-pod/tools/peq.py) & [`patch/peq_player.c`](file:///home/jtliang/Projects/q2-pod/patch/peq_player.c))
In M1 Plus's `hciplayer`, the `.rodata` string `"equalizer\0"` is at offset `0x00485e2c` (and `"Equalizer audio filter"` at `0x004937bc`). However, [`tools/peq.py`](file:///home/jtliang/Projects/q2-pod/tools/peq.py#L14-L66) and [`patch/peq_player.c`](file:///home/jtliang/Projects/q2-pod/patch/peq_player.c) require resolving **all** of the following in `hciplayer`:
1. **`af_info_equalizer` Struct (`EQ_DESC` & `EQ_OPEN_SLOT`)**: Locate the `.data` structure referencing `"equalizer\0"` (`0x00485e2c`) and patch its `open` function pointer (`EQ_DESC + 0x14`) to `peq_af_open`.
2. **Hi-Res Sample Rate Gates (`EQ_RATE_GATES`)**: Stock `hciplayer` skips attaching `af_equalizer` when `samplerate > 48000` (`0x42ced0` and `0x42fd84` on Q2). Both branches must be NOPed so PEQ, ReplayGain, crossfade, and the visualizer work on Hi-Res (>48 kHz) tracks.
3. **`GP` & 22 GOT `LIBC` Imports**: Verify `hciplayer`'s `_gp` value and the 22 GOT slot offsets listed in [`tools/peq.py:32-55`](file:///home/jtliang/Projects/q2-pod/tools/peq.py#L32-L55).
4. **MP3 VBR Scan & Fast Seek (`VBR_SCAN`, `SEEK_SLOT`, `STOCK_SEEK`, `HR_MP3_SEEK`)**: NOP the slow full-file MP3 frame walk on open and redirect `demux_audio`'s seek slot to [`mp3_seek`](file:///home/jtliang/Projects/q2-pod/patch/peq_player.c#L604).
5. **MP3 ReplayGain (`ID3_CALLS`, `STOCK_ID3`, `AV_DICT_SET`, `AV_DICT_FREE`, `RG_EXPORT`)**: Redirect `ff_id3v2_parse_apic` call sites to [`mp3_id3`](file:///home/jtliang/Projects/q2-pod/patch/peq_player.c#L661) and export `TXXX` `replaygain_*` tags to `/tmp/q2_rg`.
6. **DSD Native Passthrough (`MPCTX`)**: [`dsd()`](file:///home/jtliang/Projects/q2-pod/patch/peq_player.c#L320-L335) reads `mpctx->sh_audio->format` (`0x11100003` / `0x11100004`) to bypass PCM biquad filtering on native DSD streams.
7. **Crossfade & Visualizer Timing (`written_audio_pts`, `LENGTH`)**: [`decoded()`](file:///home/jtliang/Projects/q2-pod/patch/peq_player.c#L339-L511) calls `written_audio_pts()` and reads `LENGTH` in `hciplayer` to synchronize the 16-slot visualizer ring in `/dev/shm/q2peq` and trigger track-end crossfades.

---

## 6. Auxiliary Binaries, Libraries & Hardware Subsystems

Beyond `demo` and `hciplayer`, [`tools/build.py`](file:///home/jtliang/Projects/q2-pod/tools/build.py) patches or compiles five additional binaries/libraries that require M1 Plus adaptation:

| Binary / Library | Q2 Implementation | Required M1 Plus Changes |
| :--- | :--- | :--- |
| **`usr/bin/bluealsa`** | [`patch_bluealsa`](file:///home/jtliang/Projects/q2-pod/tools/build.py#L926-L967) patches `AAC_44K1`, `BT_DROP`, `BT_DROP_HANDLER`, `BT_DROP_PAYLOAD`, and `BT_PCM_CALLERS`. | Verify `bluealsa` binary in M1 Plus rootfs (which uses `rtl8733bs.ko`) and update instruction offsets before patching. |
| **`usr/lib/libtag_c.so.2.0.1`** | [`patch_m4b_cover`](file:///home/jtliang/Projects/q2-pod/tools/build.py#L914-L923) patches offset `0x2278` so `.m4b` audiobooks extract cover art. | Verify `libtag_c.so.2.0.1` SHA-256 / offset in M1 Plus rootfs. |
| **`usr/bin/q2boot`** ([`patch/boot.c`](file:///home/jtliang/Projects/q2-pod/patch/boot.c)) | Matches input device `"md-gpio-keys"` and checks `KEY_PLAY = 108` at boot to toggle Rockbox vs. CFW. | Update input device name to match `keyboard_gpio_add.ko` and change `KEY_PLAY` from `108` to `164` (`KEY_PLAYPAUSE`). |
| **`usr/bin/q2video`** ([`patch/video.c`](file:///home/jtliang/Projects/q2-pod/patch/video.c)) | Checks `w != 320 \|\| h != 375` on `/dev/fb0`, rotates video with `transpose=clock`, and sends `DAC_PCM`/`DAC_MUTE` ioctls to `/dev/shanling_dac`. | Change framebuffer check to `320 × 480`, remove 90° `transpose=clock` rotation, and verify ES9069Q (`codec_es9069q.ko`) DAC device node & ioctls. |
| **`usr/bin/q2remote`** ([`patch/remote.c`](file:///home/jtliang/Projects/q2-pod/patch/remote.c)) | `--shot` checks `w != 320 \|\| h != 375` ([`remote.c:139`](file:///home/jtliang/Projects/q2-pod/patch/remote.c#L139)). | Update `--shot` dimension check to `w != 320 \|\| h != 480`. |

---

## 7. Implementation Status & Verification

All phases of the Shanling M1 Plus port have been implemented and verified:

- [x] **Nix Flake Devshell (`flake.nix`):** Hermetic multiStdenv environment providing Clang/LLD cross-compilation toolchains, squashfs-tools, and testing dependencies (`nix develop`).
- [x] **Auxiliary Binaries & Hardware Integration (`09dba3a`):**
  - `patch/boot.c`: Detects `keyboard_gpio_add` and monitors `KEY_PLAYPAUSE` (`164`) for Rockbox dual-boot toggle.
  - `patch/video.c`: Updated for upright `320 × 480` framebuffer, removed 90° clockwise rotation transpose, added M1 Plus overlay bar layout.
  - `patch/remote.c`: Updated frame dimension checks for `320 × 480`.
- [x] **Audio Engine & PEQ (`a1ac12f`):**
  - `patch/peq.c` & `patch/peq_player.c`: Added M1 Plus profile with `af_info_equalizer` open slot (`0x00494444`), rate gates (`0x42cd78`, `0x42fc6c`), demuxer seek slot (`0x44682c`), and ID3 RG parse calls (`0x442df0`, `0x4453e0`).
  - `patch/peq.h`: Symbol fallbacks and stubs for missing M1 Plus exports.
- [x] **Portrait 320x480 Geometry & Layouts (`6cca35f`):**
  - `patch/offsets.inc`: Conditioned `W=320, H=480, CORNER_R=0, STATUS_MARGIN=0, BOTTOM=450` for M1 Plus.
  - `patch/coverflow.c`, `patch/photos.c`, `patch/books.c`, `patch/visualizer.c`, `patch/lockscreen.c`: Layouts refactored for upright 320x480 display without pill-glass corner insets.
- [x] **Return Synthesis & Knob Navigation (`e9b61f7`):**
  - Left-edge swipe gesture (`dx > 50`) and title bar back-tap synthesize `KEY_RETURN`. Both were later replaced by an explicit Back button (§4.1).
  - Knob Navigation Mode converts rotary encoder inputs to `KEY_PREV` / `KEY_NEXT` list navigation, falling back to volume control on Now Playing or when screen is off.
- [x] **Build & Packaging Tooling (`feat(build)`):**
  - `tools/build.py`: Automatic model detection between Q2 and M1 Plus (`update.bin` tar container vs `update.zip`).
  - Symbol resolution, hook relocation, and trampoline generation for M1 Plus V2.1 `demo` binary.
  - Repacking into valid `update.bin` with recalculated MD5s in `firmware_v20.info`.
