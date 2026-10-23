# q2remote: drive a development Q2 or M1 Plus over Wi-Fi

`q2remote` gives a developer, or an AI agent working on the project, a root shell, screenshots and input on a Q2 over the local network, so a change can be tried and checked without touching the device. It ships **only in `--dev` builds** ([building.md](building.md)): `tools/build.py --dev` compiles `patch/remote.c` into `/usr/bin/q2remote` and starts it from `S90play` after dbus; release builds don't contain it, and `test/build.py` checks that.

It listens on TCP port 2302 and sends the key and every command **unencrypted**. Use it only on a network you trust, such as your own phone's hotspot, and never leave a key on a card you lend or sell.

## Setup

1. Install a `--dev` update on the Q2 and join it to the same Wi-Fi network as your PC.
2. Put a key on the card: 16-127 characters from `A-Z a-z 0-9 _ -`, one line. With the Q2 connected over USB storage:

   ```sh
   openssl rand -hex 16 > /run/media/$USER/<card>/q2remote.key
   ```

3. **Eject, then unplug the cable or restart the Q2.** While the card is shared over USB storage the Q2 unmounts it, so a new key is read only once the cable is out, or at the next boot, before USB storage takes the card. q2remote keeps a copy in `/mnt/data/q2remote.key` and uses it while the card is away, so a cable in, even from boot, doesn't lock you out.
4. Find the Q2's address: the hotspot's or router's client list, or `ip neigh` after a ping sweep of the subnet.
5. Load the key into the environment without echoing it:

   ```sh
   export Q2_HOST=10.0.0.42
   export Q2_KEY="$(cat path/to/q2remote.key)"
   python3 tools/q2remote.py sh id        # uid=0(root) gid=0(root)
   ```

   If you keep a copy of the key on the workstation, a temporary location such as
   `$XDG_RUNTIME_DIR/q2remote.key` is a good fit: it may be cleared at logout or reboot.

Each connection rereads `/mnt/mmc/q2remote.key` while the card is mounted, so replacing the file rotates the key and deleting it revokes access, the internal copy included. A change made over USB storage applies once the cable is out.

## Commands

| Command         | Does                                                                                                                                       |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| `sh 'COMMAND'`  | Runs `COMMAND` with busybox `sh` as root, printing stdout and stderr together. There is no exit status: append `; echo $?` if you need it. |
| `shot OUT.png`  | Saves the displayed framebuffer as an upright 375×320 PNG.                                                                                 |
| `key NAME [MS]` | Presses a button for `MS` ms (default 80).                                                                                                 |
| `wheel N`       | Turns the wheel `N` ticks: positive is down/next, negative up/back.                                                                        |
| `tap X Y [MS]`  | Taps the screen at upright screenshot coordinates (0-374, 0-319), holding `MS` ms (default 20).                                             |
| `peek NAME...`  | Prints payload or `demo` variables by name from the running `demo`, field by field ([below](#reading-variables)). Needs `Q2_BUILD`.        |
| `events N [S]`  | Prints raw events from `/dev/input/eventN` for `S` seconds (default 5).                                                                    |
| `devices`       | Lists the input devices and their key and axis codes.                                                                                      |
| `reboot`        | Syncs and reboots into the saved boot target; q2remote answers again once the Q2 rejoins Wi-Fi, which can take a few minutes.              |

## Input

| Control        | How                                                                | Device                                                    |
| -------------- | ------------------------------------------------------------------ | --------------------------------------------------------- |
| Centre         | `key centre`; hold 5 s (`key centre 5000`) for the shutdown prompt | `md-gpio-keys`, `KEY_POWER` 116                           |
| Return         | `key return`                                                       | `md-gpio-keys`, `KEY_UP` 103                              |
| Play/Pause     | `key play`                                                         | `md-gpio-keys`, `KEY_DOWN` 108                            |
| Next, Previous | `key next`, `key prev`                                             | `md-gpio-keys`, 163, 165                                  |
| Wheel          | `wheel N`                                                          | `hyn_sliderbar`: x 1-200 a turn, read through tslib       |
| Touch          | `tap X Y`                                                          | `hyn_ts`: the portrait panel's axes, which `tap` converts |

All of it is injected by writing input events to `/dev/input/eventN`, so the firmware sees exactly what the hardware would send and `demo` needs no change. `wheel` reads the saved **Wheel Sensitivity** from `/mnt/data/config.ini`, so one tick is one tick of the firmware at any setting ([internals.md](internals.md), the wheel). The PMIC's 10-15 s Centre reset is wired in hardware and can't be injected; use `reboot`.

## M1 Plus

M1 Plus `--dev` builds ship the same helper, started the same way, and the setup is the same. The
client tells the models apart by their devices (the M1's `md-rotary-knob`) and by the
framebuffer's size:

| Command | On the M1 Plus |
| --- | --- |
| `shot OUT.png` | An upright 320×480 PNG, as the screen is: no rotation. |
| `key NAME [MS]` | `centre` (the knob's press, KEY_POWER 116), `play` (KEY_PLAYPAUSE 164), `next` 163, `prev` 165, on `md-gpio-keys`. There is no Return button. With Knob: Navigation a single `centre` is a select, and turning the screen off needs a double press within 250 ms, which two client calls are too slow for. With Knob: Volume (the default) a single `centre` wakes or sleeps the screen, as stock; a wake shows V2.1's lock screen, which `swipe 40 458 300 458 500` unlocks. |
| `knob N` | Turns the knob `N` detents on `md-rotary-knob`: positive is clockwise (KEY_VOLUMEUP 115), negative anticlockwise (114). It is the volume, or moves the selection with Knob: Navigation. With the volume bar closed, stock's first detent only opens it, so `knob 1` from a closed bar changes nothing; the bar closes again after a few seconds. |
| `tap X Y [MS]` | Upright screen pixels (0-319, 0-479) on `Goodix-CTP`, sent as the panel sends a real tap (see [m1plus.md](m1plus.md), the input table). `MS` holds the finger down that long, 100 ms by default: `tap X Y 1000` is a long press. The screen times out between commands and touch still works on a dark panel, but the hold menu refuses a dark screen's press: peek `g_backlight_status` (1 is lit) before a touch check. |
| `swipe X0 Y0 X1 Y1 [MS]` | A drag from one point to the other over `MS` (300 ms by default; 50-5000). It sends a move frame every 12 ms, as the panel does, carrying only the axes that changed. A short one flings a list or turns Home's page (`swipe 280 250 40 250`); a long one (`800` and up) drags with little fling. |

`wheel` is the Q2's only; `knob` and `swipe` are the M1's. Each command says so if it's used on the other model. The M1's input commands open the device once and write every frame to it: opening `Goodix-CTP` costs about 45 ms, which would stretch a 12 ms frame to 60. With
**Knob: Navigation** on, `key prev` is Back.

## Reading variables

`peek` reads the running `demo`'s memory and prints what the payload's variables hold, so a check
like "is a long-press timer pending?" needs no extra logging. Set `Q2_BUILD` to the `--out` directory of
the build on the device, and run it inside `nix develop`: it needs clang.

```sh
export Q2_BUILD=build-m1-dev
python3 tools/q2remote.py peek st.qm_timer st.qm_dialog g_menu.n g_backlight_status
python3 tools/q2remote.py peek st              # every field, nested records indented
python3 tools/q2remote.py peek 'ls.tab->sec'   # through a pointer; quote ->, or the shell redirects it
python3 tools/q2remote.py peek coverflow.c:fx  # a static named in two files: say which
```

A name is a payload variable (from the build's `patch.elf`) or a `demo` global (`peq_platform.h`'s
`#define`s, such as `g_backlight_status`), followed by `.FIELD`, `[N]` and `->FIELD`. `->` reads the
pointer and goes on from what it points to; an index into a pointer (`p[3]`) isn't supported.

To find each name's address, offset and type, `peek` compiles a probe with the build's flags that
includes the source file that defines it. Numbers print in decimal and hex, pointers in hex, `char`
arrays as strings, and arrays as their first 16 elements. An array of records prints as hex with its
type: peek one element (`st.pos[0]`) to see its fields. Each call checks two things before it prints:

- the payload `demo` holds matches the build manifest's `patch_sha256`, or it refuses: the addresses
  would be another build's;
- each variable's size from the source matches its size in `patch.elf`, which tells if the source has
  changed since that build.

A `NULL` or unmapped pointer is reported for its name alone, and the exit status is 1. Checked on an M1
Plus (dev 11). The Q2's payload is built and linked the same way, but `peek` hasn't been run on one.

## Working with it

- Take a `shot` after every action, about a second after it, once the page's slide has finished, and look at it before the next step.
- If input seems to do nothing, the screen may be off: `key centre` wakes it. While it's dark the wheel changes the volume.
- With a cable in, the Q2 shows **USB Connected** and the wheel changes the volume. `key return` ends USB storage and the Q2 mounts its card again; eject it on the PC first.
- With **Wake: Double Press** on, a dark Q2 needs two Centre presses to wake.
- A tap hides the wheel's selection, and the next tick only shows it again without moving.
- Busybox has no `timeout`, `pkill` or `killall -r`. Background a command and `kill $!` it.
- Logs and settings: `/mnt/data/config.ini`, the card at `/mnt/mmc`, and `ps` for `demo`.

## Troubleshooting

- **`authentication rejected`:** the key differs from the card's file, the file is malformed, or the key is new and the USB cable is still connected (setup step 3).
- **`cannot reach Q2` / `No route to host`:** the Q2 isn't on the network yet (after a boot or a reboot it can take a few minutes), or is in Rockbox, which has no q2remote. Make sure the PC is on the same network and not still on wired Ethernet.
- **`no md-gpio-keys input device`:** run `devices`; the firmware may name its devices differently.

## Protocol

The client sends the key, a newline, the command, a newline, then any stdin. The helper answers `OK\n` and then streams the command's output until it exits, or answers `ERR\n` and closes. A handshake has to arrive within 10 seconds. `q2remote --shot` writes `Q2FB\0`, then the width, height, stride and size as little-endian 32-bit integers, then the displayed page, which `tools/q2remote.py` rotates and encodes. `python3 test/remote.py` builds the helper for the host and checks authentication, rotation, revocation, the internal copy, framing and the input encoders.
