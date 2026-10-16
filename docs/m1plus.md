# Shanling M1 Plus Firmware Porting Analysis

Technical exploration, hardware breakdown, and reverse-engineered architecture for porting **Q2 Pod** to the **Shanling M1 Plus** (Firmware V2.1), based on **Q2 Pod v1.2.1** (the current release of the upstream repository).

---

## 1. Executive Summary & Feasibility

Porting Q2 Pod to the Shanling M1 Plus is **highly feasible**. This port will be based off **Q2 Pod v1.2.1** (current upstream release), carrying over its 30-band PEQ, Standalone Spotify Connect browsing, CUE/audiobook resume points, View Queue, and iPod Classic interface overhaul.

While the industrial design and hardware controls differ (side rotary knob and a larger 3.2" touchscreen instead of a front touch wheel), the underlying software stack is from the exact same codebase family as the Shanling Q2:

| Component | Shanling Q2 | Shanling M1 Plus (V2.1) | Status |
| :--- | :--- | :--- | :--- |
| **CPU Architecture** | MIPS32 Little-Endian (`mipsel`) | MIPS32 rel2 Little-Endian (`mipsel`) | **Identical** |
| **GUI Framework** | ZLG AWTK (`/release/bin/demo`) | ZLG AWTK (`/release/bin/demo`) | **Identical** |
| **Audio Daemon** | `/usr/bin/hciplayer` (MPlayer `af_equalizer`) | `/usr/bin/hciplayer` (MPlayer `af_equalizer`) | **Identical** |
| **Database Engine** | SQLite3 (`/mnt/data/database.db`) | SQLite3 (`/mnt/data/database.db`) | **Identical APIs** |
| **ELF Injection Slot**| Unused `PT_NULL` header (Segment 10) | Unused `PT_NULL` header (Segment 10) | **Identical** |
| **Display Resolution**| 320 × 375 portrait | **320 × 480** portrait | Geometry update needed |
| **Navigation Input** | Front capacitive touch wheel | **3.2" Touchscreen + Side Rotary Knob** | Hybrid navigation model |

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
- **No cryptographic signatures / RSA certificates**: The Shanling recovery update mechanism calculates the standard MD5 checksums of `recovery-update/xImage` and `recovery-update/rootfs.squashfs` and checks them against `firmware_v20.info`.
- **Builder compatibility**: [`tools/build.py`](file:///home/jtliang/Projects/q2-pod/tools/build.py) can generate custom flashable `update.bin` packages by repacking squashfs with `mksquashfs` and archiving the files into a `.tar` named `update.bin`.

---

## 3. Hardware Architecture & Input Mapping

### System-on-Chip (SoC)
- **Processor**: Ingenic X2000 application processor.
- **CPU Cores**: Dual XBurst2 cores (clocked up to 1.2 GHz, MIPS32 Release 5 ISA) + one low-power XBurst0 auxiliary core (240 MHz).
- **Instruction Set**: Backward compatible with MIPS32 rel2. Code compiled with `clang -target mipsel-linux-gnu` runs natively.

### Display & Framebuffer
- **Display Panel**: 3.2-inch TFT LCD (`lcd_h320qn01.ko` via `/tmp/m1plus_init/module_driver/lcd_h320qn01.sh`).
- **Resolution**: **320 × 480** portrait.
- **Framebuffer**: `/dev/fb0` managed by `soc_fb.ko` (2 double-buffered frames, 32 bpp BGRA).
- **Boot Splash**: Baseline 8-bit JPEG, exactly 320×480 pixels (`/release/assets/default/raw/images/xx/logo.jpg` and `logo180.jpg` for inverted rotation).

### Audio Section
- **DAC**: ESS Sabre ES9069Q (`codec_es9069q.ko`, `x2000_510_es9069q_sound_card.ko`).
- **Amplifiers**: Dual SGM8262 op-amps supporting 3.5mm Single-Ended and 4.4mm Balanced outputs.
- **Software Interface**: Standard ALSA PCM streaming via `hciplayer`.

### Physical Inputs & Kernel Drivers
Discovered from `/module_driver/keyboard_encoder_add.sh` and `/module_driver/keyboard_gpio_add.sh`:

| Input Control | Hardware Pin / Driver | Linux Input Event | Key Code |
| :--- | :--- | :--- | :--- |
| **Rotary Knob (Turn Down)** | GPIO `PB19` (`keyboard_encoder.ko`) | `KEY_VOLUMEDOWN` | `114` |
| **Rotary Knob (Turn Up)** | GPIO `PB18` (`keyboard_encoder.ko`) | `KEY_VOLUMEUP` | `115` |
| **Rotary Knob (Press In)** | GPIO `PE31` (`keyboard_gpio_add.ko`) | `KEY_POWER` | `116` |
| **Play / Pause Button** | GPIO `PB02` (`keyboard_gpio_add.ko`) | `KEY_PLAYPAUSE` | `164` |
| **Next Track Button** | GPIO `PE26` (`keyboard_gpio_add.ko`) | `KEY_NEXTSONG` | `163` |
| **Previous Track Button** | GPIO `PB03` (`keyboard_gpio_add.ko`) | `KEY_PREVIOUSSONG` | `165` |
| **Touchscreen** | Goodix (`gt9xx_touch.ko`) | Touch events on `/dev/input/event2` via `tslib` | Standard touch |
| **Atmosphere LED Ring** | `led_ktd2026.ko` | Multi-color status lamp around knob | PWM / I2C |

---

## 4. Navigation & Interaction Architecture

On the Shanling Q2, all navigation is built around the front touch wheel. On the M1 Plus, the 3.2-inch capacitive touch screen is responsive, spacious, and already central to the device experience.

The proposed interaction model provides **touchscreen-first navigation** with the **side rotary knob as a configurable option**:

```mermaid
flowchart TD
    subgraph Input ["User Input Sources"]
        Touch["3.2\" Capacitive Touchscreen (tslib)"]
        Knob["Side Rotary Encoder (KEY_VOLUMEUP / DOWN)"]
        KnobPress["Knob Push (KEY_POWER)"]
    end

    subgraph NavEngine ["Q2 Pod Navigation Engine"]
        TouchEngine["Direct Touch & Inertial Glide (Tap, Scroll, Edge-Swipe Return)"]
        KnobMode{"Knob Mode Setting"}
        VolCtrl["Standard Hardware Volume"]
        ListNav["Menu & List Navigation (Duration Ramps, Edge Bump, Wrap)"]
    end

    Touch --> TouchEngine
    Knob --> KnobMode
    KnobMode -->|"Mode: Volume"| VolCtrl
    KnobMode -->|"Mode: Navigation"| ListNav
    KnobPress --> Action["Context Action (Select / Screen Off)"]
```

### 1. Touchscreen Navigation (Default & Always Active)
- **Direct Selection & Scroll**: Natural finger scrolling with inertia and boundary clamping on lists (`scroll_view`, `table_client`).
- **Swipe-to-Go-Back**: Edge swipe from left to return to previous menu/window.
- **Coverflow Touch**: Horizontal swipe to flick through album covers; tap center cover to open tracklist.
- **Now Playing**: Direct tap on scrub bar, heart rating toggle, and volume sliders.

### 2. Side Rotary Knob (Volume by Default, Navigation Optional)
The side rotary knob defaults to **standard hardware volume control** out of the box, preserving the expected DAP tactile volume wheel behavior.

An opt-in setting in **System Settings $\rightarrow$ Display / System** provides:
- `Knob Function: Volume (Default) | Navigation`

When explicitly switched to **Navigation**:
- **In Menus & Lists**:
  - Turning the knob steps through menu rows using the duration acceleration ramp (`ramp()` in [`patch/navigation.c`](file:///home/jtliang/Projects/q2-pod/patch/navigation.c)).
  - Edge bumping (`BUMP_PX`) and list wrap-around (`EDGE_PAUSE_MS`) operate identically to Q2 Pod.
- **In Setting Sliders / EQ**:
  - Turning the knob adjusts the active slider (brightness, EQ bands, balance) in discrete steps.
- **Knob Push (`KEY_POWER`)**:
  - In Navigation mode: Single press activates the selected row (Centre click).
  - In Volume mode: Single press wakes or sleeps the display (stock behavior).
  - Double press toggles the display on/off.
- **Context Fallback**:
  - Even in Navigation mode, when playback is active on the Now Playing screen or when the screen is dark, turning the knob automatically reverts to master audio volume.

---

## 5. Verified Memory Addresses & Symbols (M1 Plus V2.1)

Below is an audited comparison of hook targets in `release/bin/demo` between Q2 V1.32 and M1 Plus V2.1:

| Function / Symbol | Q2 V1.32 Address | M1 Plus V2.1 Address | Purpose |
| :--- | :--- | :--- | :--- |
| `home_page_init` | `0x00523c84` | `0x00534cd4` | Binds Home menu rows and Coverflow card |
| `playing_page_init` | `0x0052ca88` | `0x0053d1e4` | Now Playing UI layout, album art, position |
| `widget_dispatch` | `0x0065e0ec` | `0x0066cec8` | Intercepts click events before native execution |
| `widget_on_paint_border`| `0x006596a0` | `0x00668810` | Custom selection outlines, radio dots, chevrons |
| `window_manager_dispatch_input_event` | `0x0066d49c` | `0x00677b74` | Master input gate (intercepts keys and touch) |
| `playset_equalizer_page_init` | `0x004b642c` | `0x0049e358` | Injects 30-band PEQ UI in place of stock EQ |
| `set_equalizer_value` | `0x004f9230` | `0x004d851c` | Links EQ icon to 3EQ / PEQ state |
| `folder_page_init` | `0x00523330` | `0x0053349c` | Folder navigation and audiobook shortcut root |
| `folder_back` | `0x00507ac8` | `0x004dbecc` | Directory navigation back behavior |
| `scanAllMusicFile` | `0x004fc788` | `0x004e9df4` | Invalidates Coverflow album cache on scan |
| `scanSpecFolder` | `0x004fc964` | `0x004e9e90` | Invalidates Coverflow album cache on folder scan|
| `deleteMusicFromMusicDb`| `0x00500b5c` | `0x004ede44` | Invalidates Coverflow album cache on song delete|
| `systemset_about_page_init` | `0x004bc80c` | `0x004a170c` | Displays CFW Version row |
| `systemset_display_page_init`| `0x004c1d04` | `0x004a5eb8` | Adds Knob Mode, Theme, and Wheel settings |
| `systemset_sysset_page_init` | `0x004cc4cc` | `0x004ada78` | System settings injection |
| `systemset_powermanager_page_init` | `0x004c72d0` | `0x004a9d18` | Adds Charge Limit and Power options |
| `main_loop_sleep_default` | `0x00648f00` | `0x00658f70` | Extended sleep during screen-off (Battery) |
| `mclLoadPlayList` | `0x005aa8d4` | `0x005d1f28` | Queue management (Play Next, Add to Queue) |
| `mclNextSong` | `0x005adbbc` | `0x005d5800` | Track advance & custom shuffle selection |
| `mclPrevSong` | `0x005ada98` | `0x005d56dc` | Track retreat |
| `mclStartPlayer` | `0x005ad6ac` | `0x005d5300` | Pauses Spotify Connect when local track plays |
| `mcl_tidalStartPlayer` | `0x005ad240` | `0x005d5184` | Tidal streaming playback start |
| `save_memoryplay_info` | `0x00516344` | `0x004e3340` | Saves playback queue and position on suspend |
| `memeory_startplayer` | `0x005164e0` | `0x004e34dc` | Resumes playback queue at startup |

### SQLite Library Queries (Coverflow & Local Music)
All stock database functions in `demo` retain identical function signatures:
- `getAllAlbum`: `0x004ea3c4`
- `getMusicByAlbum`: `0x004ecb5c`
- `toolsQueryDbTable`: `0x005ee77c`
- `getMusicBySonger`: `0x004ec7e4`
- `GetAllAlbumArtist`: `0x004ea6e4`
- `getMusicByAlbumAndSonger`: `0x004ecd3c`
- `getMusicByAlbumAndAlbumSonger`: `0x004ed008`
- `getMusicByAlbumAndComposer`: `0x004ed2d4`
- `getMusicByAlbumAndGenre`: `0x004ed5a0`

### Audio Player (`/usr/bin/hciplayer`)
- **Equalizer Filter**: MPlayer audio filter descriptor string `equalizer` located at offset `0x485e2c`; verbose tag `Equalizer audio filter` at `0x4937bc`.
- **Payload Injection Slot**: Unused `PT_NULL` program header at index 10, identical to Q2.

---

## 6. Implementation & Porting Roadmap

```mermaid
flowchart LR
    Phase1["Phase 1: Build & Packaging Tooling"] --> Phase2["Phase 2: PEQ Audio Hook in hciplayer"]
    Phase2 --> Phase3["Phase 3: UI Geometry (320x480)"]
    Phase3 --> Phase4["Phase 4: Hybrid Navigation Engine"]
```

### Phase 1: Tooling & Firmware Packaging
1. Create `tools/build_m1plus.py` based on [`tools/build.py`](file:///home/jtliang/Projects/q2-pod/tools/build.py):
   - Accepts M1 Plus `update.bin` as input.
   - Extracts `recovery-update/rootfs.squashfs` and `xImage`.
   - Repacks SquashFS and writes a new POSIX tar `update.bin` with updated MD5 entries in `firmware_v20.info`.

### Phase 2: PEQ & Audio Hooking
1. Disassemble `/usr/bin/hciplayer` around `0x485e2c` to locate the exact open slot for `af_equalizer`.
2. Compile [`patch/peq.c`](file:///home/jtliang/Projects/q2-pod/patch/peq.c) and [`patch/peq_player.c`](file:///home/jtliang/Projects/q2-pod/patch/peq_player.c) for MIPS32 rel2.
3. Inject the payload at `0xe10000` via the unused `PT_NULL` header in `hciplayer`.
4. Validate that 30-band PEQ and AutoEQ presets operate cleanly through the ES9069Q DAC.

### Phase 3: Screen Scaling (320 × 480)
1. Adapt [`tools/ipod.py`](file:///home/jtliang/Projects/q2-pod/tools/ipod.py):
   - Update viewport height constant from 375 to 480 pixels.
   - Calculate new row pitch (`PITCH`) to show 5 or 6 items cleanly.
   - Adjust Now Playing artwork inset and progress bar placement.
2. Adapt [`patch/coverflow.c`](file:///home/jtliang/Projects/q2-pod/patch/coverflow.c):
   - Recalculate camera distance, depth offset, and vertical centering for the taller 480px screen.

### Phase 4: Hybrid Navigation Engine
1. Update [`patch/navigation.c`](file:///home/jtliang/Projects/q2-pod/patch/navigation.c) and [`patch/offsets.inc`](file:///home/jtliang/Projects/q2-pod/patch/offsets.inc) with the M1 Plus addresses.
2. In `window_manager_dispatch_input_event` hook:
   - Allow touchscreen events to navigate lists with native inertial glide.
   - Map `KEY_VOLUMEUP` (115) and `KEY_VOLUMEDOWN` (114) to the duration ramp `ramp()` when Knob Mode is set to Navigation.
   - Map `KEY_POWER` (116) short-release to row confirmation (Centre click).
