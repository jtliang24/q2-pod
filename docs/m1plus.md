# Shanling M1 Plus Firmware Porting Analysis

Technical exploration, hardware breakdown, and reverse-engineered architecture for porting **Q2 Pod** to the **Shanling M1 Plus** (Firmware V2.1), level with the upstream release named in `UPSTREAM_BASE` (now **Q2 Pod 1.2.2**; [m1plus-sync.md](m1plus-sync.md) moves it).

---

## 1. Summary

The port carries over Q2 Pod's 30-band PEQ, ReplayGain, crossfade, visualizer, Spotify Connect and Internet Radio, CUE and audiobook resume points, ratings, the Coverflow 3D renderer and View Queue. The iPod Classic interface is not ported yet ([m1plus-roadmap.md](m1plus-roadmap.md) section 5), and the Q2 hooks the M1 doesn't take are listed by `test/m1plus/ports.py`.

While the industrial design and hardware controls differ (an upright 3.2" portrait touchscreen, a side rotary encoder knob, and no physical Back/Return button instead of a landscape-mounted rounded panel with a capacitive front touch wheel), the underlying software stack comes from the same Shanling X2000 codebase family as the Q2:

| Component | Shanling Q2 (V1.32) | Shanling M1 Plus (V2.1) | Porting Impact |
| :--- | :--- | :--- | :--- |
| **CPU Architecture** | MIPS32r2 Little-Endian (`mipsel`, o32) | MIPS32r2 Little-Endian (`mipsel`, o32) | **Identical** |
| **GUI Framework** | ZLG AWTK (`/release/bin/demo`) | ZLG AWTK (`/release/bin/demo`) | **Identical** |
| **Audio Daemon** | `/usr/bin/hciplayer` (MPlayer fork) | `/usr/bin/hciplayer` (MPlayer fork) | **Identical architecture** |
| **Database Engine** | SQLite3 (`/mnt/data/database.db`) | SQLite3 (`/mnt/data/database.db`) | **Identical schema & APIs** |
| **ELF Injection Slot** | The image's final `PT_NULL` program header | The image's final `PT_NULL` program header | **Identical** (`append_payload`) |
| **Physical `/dev/fb0`** | `320 × 375` | `320 × 480` | Framebuffer height `+105 px` |
| **AWTK Logical UI Canvas** | **`375 × 320` landscape** (rotated 90° CW) | **`320 × 480` portrait** (upright, no 90° rotation) | **Width `-55 px` (`375` $\to$ `320`), Height `+160 px` (`320` $\to$ `480`)** |
| **Panel Shape** | Pill-shaped glass (`CORNER_R = 80` px) | Rectangular 3.2" panel (`CORNER_R = 0`) | No corner insets on M1 |
| **DAC / Audio Routing** | Integrated (`/dev/shanling_dac`) | ESS ES9069Q (`codec_es9069q.ko`) + Gowin FPGA (`gw_fpgadown.ko`), also behind `/dev/shanling_dac` | `q2video`'s DAC ioctls unchanged |
| **Navigation Input** | Capacitive touch wheel (`ts_read`) + 5 buttons (incl. `KEY_RETURN`) | **3.2" Touchscreen (`gt9xx_touch.ko`) + GPIO Rotary Encoder + 4 buttons (no Return key)** | Touch first, the knob optionally navigating; a title-bar Back button for `KEY_RETURN` (§4.1) |

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
- **No cryptographic signatures / RSA certificates**: The Shanling recovery update mechanism calculates the standard MD5 checksums of `recovery-update/xImage` and `recovery-update/rootfs.squashfs` and checks them against `firmware_v20.info`. Recovery runs from the device, not from `update.bin`, so this comes from the Q2 port and can't be checked here. `test/m1plus/build.py` checks that the MD5 lines match the packed files.
- **What V2.1's updater accepts** (`update_firmware`, `0x4e0e34`, read from its code): line 1 of `firmware_v20.info` must equal demo's model string (`Shanling M1 Plus`, `0x747718`), and line 2 must contain a `V` and differ from demo's version literal (`V2.1`, `0x74773c`), or the card's `update.bin` is deleted unapplied. This is Q2's rule. The M1 build (`tools/m1plus.py`) writes its 5-character tag (`V122S`; a `--dev` build's, such as `V00Ms`; or a release's, `V1221`) to both the info file and that literal, so a build installs over stock, stock installs back over it, and the same build is refused once installed. `test/m1plus/build.py` pins those instructions and checks the built archive against them.
- **Image format**: the M1 build (`tools/m1plus.py`) repacks the rootfs with stock's own settings (lzo, 128 KiB blocks, `-tailends`) and writes the archive with stock's GNU tar headers and member list. It refuses a rootfs larger than stock's, since stock's size is known to fit the partition (V2.1's rootfs shrinks by about 2.4 MB). `test/m1plus/build.py` checks the superblock, members and headers against stock.
- **Flash layout** (`/proc/mtd` on the device): `uboot` 1 MiB, `kernel` 6 MiB, `rootfs` 75 MiB (`0x4b00000`), `kernel2` 6 MiB and `rootfs2` 12 MiB (a separate recovery system, which flashes the `recovery-update/` files V2.1's updater untars to the card), `userid`, `ota` and `userdata` (UBI, mounted at `/mnt/data`). The build's "no larger than stock" limit (55.7 MB) is well inside the rootfs partition.
- **Verified only on the device**: recovery's flash itself, and the hardware. `test/m1plus/patch.py` runs the payload's hooks one by one with the toolkit mocked, and `test/m1plus/boot.py` starts V2.1's whole demo, stock and patched, under qemu-user (see [building.md](building.md#tests)). If demo dies at startup on the device, `checkappprocess.sh` reboots about 10 s later, so know how to reflash stock V2.1 before a first boot test.

---

## 3. Hardware Architecture, Display Orientation & Input Mapping

### 3.1 System-on-Chip (SoC)
- **Processor**: Ingenic X2000 application processor (`Linux 5.10.21`).
- **CPU Cores**: Dual XBurst2 cores (clocked up to 1.2 GHz, MIPS32 Release 5 ISA) + one low-power XBurst0 auxiliary core (240 MHz).
- **Instruction Set**: Backward compatible with MIPS32r2. Code compiled with `clang -target mipsel-linux-gnu -mips32r2 -mabi=32` runs natively.

### 3.2 Display Orientation & Geometry (`375 × 320` Landscape vs. `320 × 480` Portrait)

> [!IMPORTANT]
> **Critical Orientation Difference:**
> On the **Shanling Q2**, `/dev/fb0` is `320 × 375` portrait, **but the physical LCD is mounted sideways**. AWTK renders the Q2 UI on a **`375 × 320` landscape canvas** (width = `375`, height = `320`, status bar = `30`, client height [`BOTTOM = 290`](../tools/ipod.py)) and rotates frames 90° clockwise onto `/dev/fb0`.
>
> On the **Shanling M1 Plus**, both the LCD (`lcd_h320qn01.ko`), the touchscreen (`gt9xx_touch.ko`: `gtp_x_coords_max=320`, `gtp_y_coords_max=480`, `gtp_x_y_coords_exchange=0`), and AWTK operate in **upright `320 × 480` portrait** (width = `320`, height = `480`, status bar = `30`, client height = `450`) with **no 90° rotation**.

 Consequently, every hardcoded `375` in Q2 Pod is a **horizontal width**, not a height:
- **Logical UI Width shrinks by `55 px`**: `375 px` $\to$ `320 px`.
- **Logical UI Height grows by `160 px`**: `320 px` (`290 px` client area) $\to$ `480 px` (`450 px` client area).
- **Corner Radius (`CORNER_R`)**: The Q2 has a pill-shaped glass bezel with an `80 px` corner radius ([`CORNER_R = 80`](../tools/ipod.py), [`STATUS_MARGIN = 52`](../tools/ipod.py), [`BAR_CORNER_R = 76`](../patch/m1plus_q2.inc)), which curves top/bottom list rows and insets the status bar via [`corner_inset(y)`](../tools/ipod.py). The M1 Plus has a rectangular display, so `CORNER_R` and `STATUS_MARGIN` are `0` on it ([`patch/m1plus_offsets.inc`](../patch/m1plus_offsets.inc)) and nothing is pinched inward.
- **180° Screen Flip (`ROTATEMODE=1`)**: `/etc/init.d/S11logo_display_shell` checks `grep -c "ROTATEMODE=1" /mnt/data/config.ini` to choose between `/release/assets/default/raw/images/xx/logo180.jpg` and `logo.jpg`. The M1 build's logo ([`LOGO_HOOK`](../tools/build.py), [`logo_sync`](../patch/navigation.c)) is an upright `320 × 480` JPEG, with no 90° turn; without `--logo` it keeps V2.1's own splash (`tools/m1plus.py` `build`).

### 3.3 Audio, FPGA & Peripheral Hardware
Discovered from `/module_driver/driver_default_init_script.sh` and the scripts it runs:
- **DAC & Sound Card**: ESS Sabre ES9069Q (`codec_es9069q.ko` with `pwr_gpio=PB10 pdn_gpio=PB15 po_mute_gpio=PB11 bal_mute_gpio=PB12 digital_gpio=PC08 bal_en_gpio=PB25 dac_gpio2_gpio=PB14 i2c_bus_num=1` and `x2000_510_es9069q_sound_card.ko`).
- **FPGA**: Gowin FPGA loaded via JTAG (`gw_fpgadown.ko` with `fpga_tck=PC20 fpga_tms=PC01 fpga_tdi=PC21 fpga_tdo=PC22` in `fpgadown.sh`).
- **Outputs**: single-ended 3.5 mm (`g_po_status`) and balanced 4.4 mm (`g_bal_status`).
- **Wi-Fi / Bluetooth**: Realtek `rtl8733bs.ko` + `hci_uart_h5_kernel_5_10_21.ko`.
- **Atmosphere LED**: `led_ktd2026.ko` on `i2c_bus_num=5` (multi-color status ring around knob).
- **Buzzer / Key Tone**: none. V2.1's `demo` has no buzzer command (`cmd_mcu write_str buzzer`) and no `buzzeer_switch`, so Key Tone is Q2 only (`test/build.py` checks the strings are absent).

### 3.4 Physical Inputs, Kernel Drivers & AWTK Key Translation
Discovered from `/module_driver/keyboard_encoder_add.sh`, `/module_driver/keyboard_gpio_add.sh`, `/module_driver/gt9xx_touch.sh`, and `/etc/init.d/S90play`:

| Input Control | Hardware Pin / Driver | Linux `input_event` Code | V2.1 AWTK `EVENT_KEY` ([`m1plus_offsets.inc`](../patch/m1plus_offsets.inc)) | Notes |
| :--- | :--- | :--- | :--- | :--- |
| **Rotary Knob (Turn CCW)** | GPIO `PB19` (`keyboard_encoder.ko`) | `KEY_VOLUMEDOWN` (`114`) | `KEY_VOLUMEDOWN` (`221`); Knob: Navigation makes it `KEY_NEXT` (`173`), or `KEY_PREV` with Knob Up: List Down | Active low (`active_level=0`) |
| **Rotary Knob (Turn CW)** | GPIO `PB18` (`keyboard_encoder.ko`) | `KEY_VOLUMEUP` (`115`) | `KEY_VOLUMEUP` (`220`); Knob: Navigation makes it `KEY_PREV` (`172`), or `KEY_NEXT` with List Down | Active low (`active_level=0`) |
| **Rotary Knob (Press In)** | GPIO `PE31` (`keyboard_gpio_add.ko`) | `KEY_POWER` (`116`) | `KEY_POWER` (`210`); Knob: Navigation makes it `KEY_CENTER` (`218`) | Also wakes hardware (`wakeup=y`) |
| **Play / Pause Button** | GPIO `PB02` (`keyboard_gpio_add.ko`) | `KEY_PLAYPAUSE` (`164`) | `KEY_PLAY` (`213`) | On the Q2 the Linux code is `108` (`KEY_DOWN`) |
| **Next Track Button** | GPIO `PE26` (`keyboard_gpio_add.ko`) | `KEY_NEXTSONG` (`163`) | `KEY_FWD_BTN` (`215`; `223` on the Q2) | Active high (`active_level=1`) |
| **Previous Track Button** | GPIO `PB03` (`keyboard_gpio_add.ko`) | `KEY_PREVIOUSSONG` (`165`) | `KEY_BACK_BTN` (`214`; `222` on the Q2) | Active low (`active_level=0`). Back in Knob: Navigation (§4.2) |
| **Physical Return Button** | **None on M1 Plus** | N/A | `KEY_RETURN` (`170`), sent by the payload's Back button | Synthesized (§4.1) |
| **Touchscreen** | Goodix (`gt9xx_touch.ko`, I2C0), `Goodix-CTP` | `/dev/input/event3` on the device | `EVT_POINTER_DOWN/MOVE/UP` | `320 × 480`, `flip=0`, `exchange=0` |

On the device (V00A, read over `q2remote`), the kernel lists event0 as `axp2101-pek` (the PMIC's power key, 116), event1 as `md-gpio-keys` (116, 163, 164, 165), event2 as `md-rotary-knob` (114, 115) and event3 as `Goodix-CTP`. `demo` holds event1, event2 and event3 open. `S90play`'s `TSLIB_TSDEVICE=/dev/input/event2` is the knob, not the touchscreen. The panel reports upright screen pixels in `ABS_X`/`ABS_Y`, with no `BTN_TOUCH` and no multitouch positions. A tap is `X, Y, ABS_PRESSURE 1, ABS_PRESSURE 0, SYN`, then `ABS_PRESSURE 1, SYN` about 11 ms later, then `ABS_PRESSURE 0, SYN` at the release.

> [!WARNING]
> **1. Linux Keycodes vs. AWTK `EVENT_KEY` Codes:**
> Linux kernel keycodes (`114`, `115`, `116`, `163`, `164`, `165`) are read from `/dev/input/event*` by `demo`'s input thread and translated into AWTK's own `EVENT_KEY` numbers (V2.1's `210`–`221` in the table above, in [`patch/m1plus_offsets.inc`](../patch/m1plus_offsets.inc)) *before* reaching [`window_manager_dispatch_input_event`](../patch/navigation.c) (`ringnav_input`) or V2.1's `on_wm_keyup_fun` (`ringnav`). Never compare `I(event, EVENT_KEY)` against raw Linux keycodes inside AWTK hooks.
>
> **2. Do Not Hook `ts_read` (`WHEEL_TS_READ`) on M1 Plus:**
> On the Q2, the touch wheel is a capacitive strip read via `ts_read`, whose call at `0x625b6c` (`WHEEL_TS_READ`, `CALL_SITES['q2']` in [`tools/m1plus.py`](../tools/m1plus.py)) goes to [`ringnav_ts_read`](../patch/playback.c). On the M1 Plus, `ts_read` reads the touchscreen (`Goodix-CTP`, event3 on the device), so the site is Q2 only (`M1PLUS_PORTS`): redirecting it would corrupt touch coordinates.

---

## 4. Navigation & Interaction Architecture

On the Shanling Q2, navigation is built around the front capacitive touch wheel and a dedicated physical Return button. On the M1 Plus, the 3.2-inch capacitive touchscreen is the primary interface, the side rotary knob is the hardware volume wheel, and **there is no physical Return/Back button**.

```mermaid
flowchart TD
    subgraph Input ["M1 Plus Input Sources"]
        Touch["3.2\" Capacitive Touchscreen (/dev/input/event3)"]
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
In Q2 Pod, [`KEY_RETURN`](../patch/offsets.inc) is the sole exit path for:
- Every custom full-screen page created via [`page_open()`](../patch/coverflow.c) (a bare window: on M1 Plus its back button comes from `page_title` or `back_button`):
  - Coverflow ([`coverflow.c:keyup`](../patch/coverflow.c))
  - 30-Band PEQ / 10-Band EQ / 3-Band EQ ([`peq_ui.c:keyup`](../patch/peq_ui.c))
  - Photos viewer ([`photos.c:keyup`](../patch/photos.c))
  - Books reader & Video player ([`books.c:keyup`](../patch/books.c), [`video.c:video_key`](../patch/video.c))
  - Crossfade settings ([`crossfade.c:keyup`](../patch/crossfade.c))
  - Spotify Connect & Internet Radio ([`spotify.c:keyup`](../patch/spotify.c), [`radio.c:keyup`](../patch/radio.c))
  - Shuffle, Most Played, Ratings, and Long Songs pages ([`navigation.c:page_keyup`](../patch/navigation.c))
- Returning from the iPod Home `Settings` submenu ([`coverflow_home_back`](../patch/coverflow.c))
- Opening Now Playing from Home or via hold ([`HOLD_RETURN`](../tools/build.py), [`compact_now_playing`](../patch/navigation.c))
- Canceling an active scrub on Now Playing ([`ringnav`](../patch/navigation.c), `st.scrub`)

**Rule: every page has an explicit Back button.** On M1 Plus, every page Q2 Pod opens or replaces
shows V2.1's title-bar back button at its top left (`btn_return`'s style and `return`/`return_down`
icons, named in `offsets.inc` so the build's V2.1 name check covers them). Make it with
[`back_button`](../patch/coverflow.c), or with `page_title`, which adds one beside the title. Its
click sends `KEY_RETURN` through `dispatch_key_return` on a timer, so the page's own keyup decides
what Back means: close the page, or step back one screen as the PEQ editor's Advanced tab does.
No gesture, hidden tap or key may be a page's only way out. A new page's `test/m1plus/boot.py` step
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
(`home_page_init` binds key-up and key-long only), so there is no key-down to remap. `test/m1plus/build.py`
pins both facts.

When switched to **Navigation**:
- **In Menus, Lists, Coverflow, Books & EQ**:
  - Turning the knob translates encoder ticks into AWTK `KEY_PREV` (`172`) / `KEY_NEXT` (`173`) events (volume up is `KEY_PREV`, up the list, unless `Knob Up: List Down`) (suppressing stock volume changes) and feeds them into [`ringnav()`](../patch/navigation.c) with duration acceleration (`ramp()`), edge bumping (`BUMP_PX`), and list wrap-around (`EDGE_PAUSE_MS`).
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
On the Q2, Play/Pause held on a highlighted row opens Q2 Pod's hold menu for that row: Play Next, Add to Queue, Favourites, Rate Album and the rest. On the M1 nothing is highlighted unless the knob is in Navigation mode. So a finger held still for 500 ms (`LONG_PRESS_MS`) on a row or tile of a library page opens the same menu for the row under the finger. That covers an artist's albums, Albums, Artists, Composers, Genres, All Songs, an album's tracks, Folders and Playlists. A press that moves is the list's scroll, and the row doesn't open on the release. Play/Pause held with nothing highlighted is still V2.1's own sort dialog. See [internals.md](internals.md#queue-menu). On the device (dev 21), a hold on an album's track list plays the row instead: [m1plus-roadmap.md](m1plus-roadmap.md) U4.

### 4.4 The Q2 Pod Home Card and Page
V1.32 has a Local Music menu that Q2 Pod extends with its own rows. V2.1 has none: its Home *is* the library, a grid of cards the user picks in V2.1's Home menu editor. So the M1 build adds one card, **Q2 Pod**, after V2.1's own, and it opens a payload page (`library_page`) with the rows Q2 Pod adds to the Q2's Library: Shuffle, Ratings, Most Played, Long Songs, then Podcasts, Audiobooks, Photos, Books and Videos (each only when its folder is on the card), Coverflow, then Streaming's Spotify, Internet Radio and AirPlay (V2.1 has no Streaming page), and Upload Scrobbles (only with an account).

- **No asset changes.** V2.1 builds the grid in code: `home_page_init`'s builder (`0x534064`) lays out `pdeq_choicemenu`'s ids six to a page of `home_sview` (a slide_view) and sets `home_sindicator`'s count. [`home_card`](../patch/coverflow.c) adds the card in the next slot exactly as V2.1's card builder (`0x533d8c`) places its own, or on a new page when the last one is full. The icon pair (`home_q2pod.png`, `_down`) is new art in V2.1's 66 px card style, added to the rootfs like the row icons.
- **V2.1's card click can't see it.** V2.1's card click (`0x533b80`) reads `atoi(name)` as one of its 18 ids, and the card's image has no name and its own click.
- **It survives V2.1's rebuilds.** Turning cards on or off in the editor, or changing the language, makes V2.1 rebuild the grid the next time Home comes to the front, which destroys every card. The card binds its own to-foreground handler before V2.1's init binds V2.1's, so it runs after V2.1's rebuild and puts the card back once. `test/m1plus/build.py` pins the builder's only two callers.
- **The page** is built from `page_open` and `page_list` (title bar and back button) with V2.1's 64 px rows (`list_row`). Coverflow's carousel, the photo viewer and the book reader got the back button over their content, and Coverflow's covers go back to this page, not Home.
- **What its rows needed on V2.1.** The details are in [m1plus-progress.md](m1plus-progress.md) section 18.
  - Long Songs passes TagLib's `readAudioProperties` (`taglib_file_open(path, 1)`). V2.1's scanner passes 0, and an unset flag read every length as 0.
  - Books and Photos make their hidden full-size views insensitive (`view_show`), because AWTK's hit test skips insensitive children but not hidden ones.
  - Shuffle Songs sets the play mode as V2.1's Play mode page does, since V2.1 has no `config_playmode`.

---

## 5. What the M1 Build Changes in V2.1

The tables in [`tools/m1plus.py`](../tools/m1plus.py) are the source: every V2.1 address the build
uses is there or in [`patch/m1plus_offsets.inc`](../patch/m1plus_offsets.inc), found in V2.1's own code
and pinned in `test/m1plus/build.py`. This section says what they cover. For each Q2 hook, call site
and name the M1 doesn't take, and why (V2.1 has it already, Q2 only, or not ported yet), run
`python3 test/m1plus/ports.py`.

### 5.1 Hooks (`M1PLUS_HOOKS`: 42, and one leaf hook)

> [!IMPORTANT]
> **PIC Prologue Constraint:**
> Every non-leaf hook is installed by overwriting the first two words of the target function with a `j` to its payload replacement and a `nop` (`tools/m1plus.py` `build`, as upstream's `tools/build.py` does for the Q2). So each target must start with the standard 3-instruction PIC prologue (`lui $gp` / `addiu $gp` / `addu $gp, $t9`) computing V2.1's GOT base, which the build checks (`pic_gp(...) == M1PLUS_GP`). The function's `stock_<x>_trampoline` (`compile_payload`) sets `$gp` itself and resumes at the target's address + 12, past the prologue. A Q2 hook the M1 doesn't take gets a trampoline that returns 0, so upstream's payload links either way.

| V2.1 function | Payload | Q2 hook it stands for |
| :--- | :--- | :--- |
| `widget_on_paint_border` | `ringnav_paint` | same |
| `widget_dispatch` | `ringnav_dispatch` | same |
| `on_wm_keylong_fun` | `ringnav_keylong` | same |
| `playset_equalizer_page_init` | `peq_page_init` | same |
| `set_equalizer_value` | `peq_stock_eq` | same |
| `home_page_init` | `coverflow_home` | same |
| `toolsQueryDbTable` | `ringnav_library_query` | same |
| `scanAllMusicFile` | `coverflow_scan_all` | same |
| `scanSpecFolder` | `coverflow_scan_folder` | same |
| `deleteMusicFromMusicDb` | `coverflow_delete_song` | same |
| `main_loop_sleep_default` | `ringnav_sleep` | same |
| `systemset_about_page_init` | `ringnav_about` | same |
| `folder_page_init` | `ringnav_folder` | same |
| `folder_back` | `ringnav_folder_back` | same |
| `window_manager_dispatch_input_event` | `ringnav_input` | same |
| `systemset_sysset_page_init` | `ringnav_systemset` | same |
| `systemset_display_page_init` | `ringnav_display` | same |
| `get_screensaver_image` | `lockscreen_images` | same |
| `save_memoryplay_info` | `ringnav_savequeue` | same |
| `mclLoadPlayList` | `ringnav_load` | same |
| `mclNextSong` | `ringnav_next` | same |
| `mclPrevSong` | `ringnav_prev` | same |
| `mclSetPlayMode` | `ringnav_mode` | same |
| `mclSetPlaySpeed` | `ringnav_speed` | same |
| `mcl_preload` | `ringnav_preload` | same |
| `mcl_open_preload` | `ringnav_open_preload` | same |
| `btmenu_rows` | `ringnav_btrows` | same |
| `memeory_startplayer` | `ringnav_memory` | same |
| `systemset_powermanager_page_init` | `ringnav_powermanager` | same |
| `playset_playset_page_init` | `ringnav_audioset` | same |
| `mclStartPlayer` | `ringnav_start_player` | same |
| `mcl_tidalStartPlayer` | `tidal_start` | same |
| `playing_page_init` | `ringnav_playing` | same |
| `on_wm_keyup_fun` | `ringnav` | `on_wm_keyup_before_fun` |
| `on_wm_before_tsdown_fun` | `ringnav_touch` | `on_wm_tsdown_before_fun` |
| `screensaver_page_init` | `lockscreen_init` | `saverscreen_page_init` |
| `systemset_screensaver_page_init` | `lockscreen_page` | M1 only |
| `loadLocalClassList` | `ringnav_localclass` | `load_localclass_list` |
| `loadAlbumdetailList` | `ringnav_album_detail` | `load_album_detaillist` |
| `change_music` | `ringnav_change` | `player_change_music` |
| `mclSetVol` | `ringnav_btvol` | `mclSetBtVol` |
| `dialog_sortselect_dialog_init` | `qm_sortselect_init` | M1 only |
| `window_manager_paint` (leaf: its first words, pinned) | `ringnav_wm_paint` | same |

### 5.2 Call Sites, Private Functions and Names

- **Call sites** (`CALL_SITES['m1plus']`, 10): single instructions the build rewrites, each checked against its stock word: `ALBUM_ART` (same-named albums apart in art), `AUDIO_EXTENSION_CALLS` (recognize M4B alongside existing audio extensions), `BT_CONNECT_START` (Bluetooth: Resume on connect), `COVER_DONE` (discard stale cover completion), `COVER_PAUSE` (album grids never pause the cover worker), `DROP_CACHES` (keep the page cache), `LDAC_HQ` (LDAC HQ sends 990 kbps), `SCAN_LIMIT` (scan up to 65,000 songs), `SHUFFLE_CALL` (shuffle honours Play next), `SORT_TRIMS` (sort without a leading article).
- **Private functions** (`M1PLUS_PRIVATE_FUNCTIONS`, 10): static V2.1 functions the payload calls, found by their code: `album_row`, `btmenu_rows`, `folder_refresh`, `gif_image_create`, `mcl_open_preload`, `mcl_preload`, `mcl_shuffle_pick`, `saver_pick`, `slide_menu_on_scroll_done`, `volume_refresh`.
- **Names.** `patch/offsets.inc` is upstream's, with the Q2's values. Its `#if M1PLUS` side includes [`patch/m1plus_offsets.inc`](../patch/m1plus_offsets.inc), which gives V2.1's value for every name the M1 build uses, or `M1_UNPORTED` for a name whose code can't run on M1. [`patch/m1plus_q2.inc`](../patch/m1plus_q2.inc) gives the Q2's value for the names the port added to shared code (a `STYLE_*` or `VIEW_*` string, a layout constant). Stock functions with dynamic symbols, such as the library queries (`getAllAlbum`, `getMusicByAlbum`), are resolved by name (`FUNCTIONS`).

### 5.3 The Player (`/usr/bin/hciplayer`)

`tools/m1plus.py` `patch_player` applies upstream's player patch ([`tools/peq.py`](../tools/peq.py), [`patch/peq_player.c`](../patch/peq_player.c)) at V2.1's addresses (`PLAYER_PROFILE`), on the one audited binary (`M1PLUS_PLAYER_SHA`):
1. **The equalizer filter's open slot.** The filter descriptor at `0x893808` (its info string `"Equalizer audio filter"` at `0x8937bc`, its name `"equalizer"` at `0x885e2c`, checked byte for byte) gets `peq_open` in its open slot (`0x89381c`).
2. **Hi-res rate gates.** The two branches that skip the filter above 48 kHz (`0x42ce34`, `0x42e6fc`) become `nop`s, so PEQ, ReplayGain, crossfade and the visualizer run on hi-res tracks.
3. **MP3 seek.** The full-file VBR scan on open (`0x48f5fc`) is skipped, and the audio demuxer's seek slot (`0x89f76c`) goes to `mp3_seek`.
4. **MP3 ReplayGain.** The three calls to V2.1's ID3v2 walker (`0x48b760`, from `0x48ee74`, `0x492028`, `0x492ab4`) go to [`id3_gain`](../patch/m1plus_peq_player_id3.c), which reads `TXXX` `replaygain_*` tags (V2.1's walker takes its arguments swapped).
5. **The rest** is upstream's code at V2.1's addresses: [`dsd()`](../patch/peq_player.c) leaves native DSD unfiltered, and [`decoded()`](../patch/peq_player.c) reads `written_audio_pts` (`0x4300f4`) and the track length (`0xb10e5c`) for crossfade and the visualizer.

The payload is mapped through the player's final `PT_NULL` header, as the demo's is.

## 6. Other Binaries and Scripts

| File | On the M1 build |
| :--- | :--- |
| **`usr/bin/bluealsa`** | The same binary as the Q2's (`BLUEALSA_SHA`), so upstream's [`patch_bluealsa`](../tools/build.py) applies unchanged. |
| **`usr/lib/libtag_c.so.2.0.1`** | V2.1's own build of it (`TAG_C_SHA` in `tools/m1plus.py`). `patch_m4b_cover` there adds `.m4b` to its cover dispatch at V2.1's offsets (the M4A branch at `0x1255c`); the Q2's is at `0x125ac`. |
| **`usr/bin/q2boot`** ([`patch/boot.c`](../patch/boot.c)) | The same `md-gpio-keys` device, with Play/Pause `164` (`KEY_PLAYPAUSE`) where the Q2 has `108`. |
| **`usr/bin/q2video`** ([`patch/video.c`](../patch/video.c)) | `H` is 480, and ffmpeg scales and pads to `320 × 480` with no `transpose=clock`. The DAC ioctls are the Q2's: V2.1 has `/dev/shanling_dac` too. The position bar is the M1's (`m1plus_video_overlay.c`), and every frame shows a back chevron, since there is no Return key. |
| **`usr/bin/q2remote`** ([`patch/remote.c`](../patch/remote.c), `--dev` only) | `shot` takes a 375- or 480-line framebuffer. |
| **`/etc/init.d/S90play`, `S11logo_display_shell`, `watchdog`** | Upstream's edits: `BOOT_HOOK`, and `REMOTE_HOOK` with `--dev`, in `S90play`, and `LOGO_HOOK` in `S11logo_display_shell`, each checked to match V2.1's script exactly once; `WATCHDOG_SLEEP` in `watchdog`. |

## 7. Status

The port runs Q2 Pod at `UPSTREAM_BASE` on the M1 Plus: the M1 gates and their counts are in [m1plus-integration.md](m1plus-integration.md#current-status-measured-2026-10-23-at-upstream-122-after-u2), what remains to port is the roadmap's U4 ([m1plus-roadmap.md](m1plus-roadmap.md)), and what was done, when and why is the log, [m1plus-progress.md](m1plus-progress.md).

## 8. Notes on the shared code

Where upstream's code in `patch/*.c` behaves differently on V2.1, the note lives here, not in upstream's
comments, so a sync never conflicts on a comment (roadmap U1c). By file and function:

- `coverflow.c`, `build_art`: V2.1 has the one cover lock. Its player cover thread (`parseplaycover_thd`)
  holds `parse_cover_mutex` too (`test/m1plus/build.py`).
- `coverflow.c`, `changed`: on M1 Plus the view under the carousel takes the touch (`touched`).
- `coverflow.c`, `pick` and `coverflow_home_back`: Return from the covers or the message goes to the Q2 Pod
  page, since V2.1's Home is a grid of cards and the Q2 Pod card follows them.
- `crossfade.c`, `xfade_open`: V2.1's Boot volume page has its switch on a settings row
  (`VIEW_BOOTVOL_SWITCH`), which becomes Crossfade's, and its title bar's Back button stays stock's.
- `lockscreen.c`, `big_clock`: the Large clock's top line is at `LOCK_CLOCK_Y`; at its right end the M1
  Plus shows V2.1's battery icon with its level bar, where the Q2 shows the percent.
- `navigation.c`, `ringnav_art_header`: V2.1's album page big cover snprintf is at `0x525b84`.
- `navigation.c`, `qm_pick`: on V2.1, `qm_sortselect_init` clears `to_modal`, so the dialog is the top
  window once `navigator_to` returns.
- `navigation.c`, `qm_hold`: a touch long-press (`LP_TOUCH`) takes the row under the finger instead of the
  highlighted one, with the finger still down and no key to swallow.
- `navigation.c`, `headset_gain`: V2.1 has no `mclSetBtVol`. Its `mclSetVol` sets the DAC and, on Bluetooth,
  hciplayer's gain. Over 100 is its player's own full scale (the private routine at `0x5d4e00` sends 255,
  255), never a volume, and stays stock's. Bluetooth's end puts the DAC back: `checkBluetoothStatus` and
  `switchBluetooth` stop the player, change the output and call `set_devicevolume` before they restart it.
- `peq_ui.c`, `render` and `bar`: there is no Back row; the M1 Plus's back button, over the title bar's left
  end, steps back as Return does, created after the page's other widgets so it takes the taps there.
- `photos.c`, `moved`: V2.1's `slide_menu` has no spacer and steps by its height, so on M1 Plus the viewer
  takes the touch (`swiped`) and the paint spaces the photos a screen apart.
