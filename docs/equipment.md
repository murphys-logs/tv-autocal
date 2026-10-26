# Equipment

What the owner has said about the equipment, and what still needs confirming. The original equipment comes from the owner's brief (S-001); the selected cable and purchase details come from the owner's later confirmation (S-004); the meter's position comes from the owner's later description (S-011); and the rear `EX-LINK` port, exact model label, TV firmware version, PC OS/GPU/driver and delivered cable leaflet come from the owner's confirmations and photographs of 26 October 2026 (S-032). All are in the ledger's [sources](../LEDGER.md#1-sources). Nothing has been tested yet. [LEDGER.md](../LEDGER.md) is the formal record: if this page and the ledger ever differ, the ledger wins and this page should be corrected.

## TV — the display to calibrate

- **Model:** Samsung UE49KS7000UXXU — confirmed on the rear panel label (S-032, C-074)
- **Firmware version:** `T-JZMDEUC-1270.1 , BT - S` (`Sub-micom: T-JZMDEUS-1007`, `e-Manual: JZDVBEUK-1.1.3`) — from the `Contact Samsung` screen (S-032, C-074; AI-transcribed from withheld owner photograph)
- **Picture controls offered by the menus, and their ranges:** unknown — T-001
- **Control route:** Samsung Ex-Link only — D-006. Connection, cable compatibility and command support remain **not tested** — T-006.
- **Network remote control:** out of scope under D-006; C-006 and T-007 are retained as superseded history.
- **Ex-Link jack:** round 3.5 mm socket labelled **`EX-LINK`** on the rear of the TV panel (between `USB (IoT EXTEND)` and `LAN` behind `Cover Terminal`, **not** on the One Connect box) — confirmed by the owner and rear-bay photograph (S-032, C-074). Electrical compatibility and command support on `T-JZMDEUC-1270.1` remain **not tested** — T-006.

## Colour meter

- **Model:** Datacolor Spyder5 colorimeter
- **Position during readings:** hangs by its USB cable in the middle of the screen. It is circular, about 5 cm across, and its cap, about the same size, hangs beneath it — reported by the owner (S-011, C-023)
- **Works with ArgyllCMS on the owner's PC:** not tested — T-003
- **Spectral correction for this TV:** none identified or validated — T-004, Q-001

## Computer

- **Type:** Windows PC
- **Windows version:** `Windows 10 Home 22H2` — confirmed by the owner (S-032, C-075)
- **Graphics card and driver:** `NVIDIA GTX 1080 8GB`, `GeForce Driver Version 582.78` — confirmed by the owner (S-032, C-075; confirms C-045's GPU model)
- **Video output settings and colour/display tools:** unknown — T-002

## AV receiver

- **Model:** Denon AVC-X3800H
- **Whether it sits in the video path between the PC and the TV, and its video settings:** unknown — T-002

## Additional hardware

- **Selected cable:** [DSD TECH USB RS232 to 3.5mm Serial Cable with FTDI FT232RL Chip 6FT](https://www.amazon.co.uk/dp/B07XXWVH69) (`Model: SH-U35B`).
- **Source:** purchase details reported by the owner (S-004, C-008); delivered printed user-guide leaflet (`A100033`) supplied by the owner and transcribed in S-032 (C-076), matching the online `SH-U35B` guide (S-026, C-064).
- **Purchased:** 24 October 2026 at 21:00 (time zone not stated).
- **Total paid:** £15.99, including delivery.
- **Delivery status:** arrived (confirmed 26 October 2026, S-032, C-076).
- **Leaflet specifications:** `Model: SH-U35B`, `FTDI FT232RL` (or `FT232RNL` on some batches), 6 ft, described as an RS-232 serial cable wired `Tip = RX (device TX), Ring = TX (device RX), Sleeve = GND`; separate RS-232 transceiver IC and voltage swing are not stated (C-064, C-076).
- **Compatibility with the TV and Ex-Link:** **not tested** — T-006. Neither the purchase nor the leaflet establishes electrical or firmware compatibility or authorises any physical test.

Budget: **£25** in total · Spent: **£15.99** · Remaining: **£9.01** — see the ledger's [budget section](../LEDGER.md#7-hardware-budget). No further purchase or physical test is authorised by this record.

## What we still need from you

These are **owner checks**: you look things up and tell us. They need no test plan, because no agent operates anything. Please:

- **only look:** write down current values before changing anything, and change nothing for the project yet;
- **stay out of the service menu**, and don't plug the Ex-Link cable into the TV;
- **keep private details out of what you send:** no serial numbers, IP or MAC addresses, or photos that show people or your room. Photos of labels or menus are fine; they stay in the private `local/` folder unless you approve one for the repository.

The proposed order of work after this is in [plan.md](plan.md).

### 1. TV

- [x] **Confirm the model** on the rear label. Confirmed in S-032 (C-074): rear label reads **UE49KS7000UXXU** (`Model: UE49KS7000U`, `Type No.: UE49KS7000`).
- [x] **Firmware version** (Settings → Support → Contact Samsung). Confirmed in S-032 (C-074): **`T-JZMDEUC-1270.1 , BT - S`** (`Sub-micom: T-JZMDEUS-1007`, `e-Manual: JZDVBEUK-1.1.3`). Please don't install a firmware update during the project without telling us first (C-053).
- [ ] **Normal-menu picture controls** (T-001). For the picture mode you watch most:
  - the picture modes offered;
  - each control's name, range and current value: Backlight, Brightness, Contrast, Sharpness, Colour, Tint, Gamma, Colour Tone;
  - white balance: the 2-point controls, and whether the multi-point control has 10 or 20 points and how they are labelled (X-003);
  - whether gamma offers a BT.1886 setting or only a slider;
  - Colour Space options and the Custom sliders;
  - HDMI Black Level, HDMI UHD Colour for that input, Smart LED, Auto Motion Plus and the Eco Solution settings;
  - whether Apply Picture Settings is set to Current Source or All Sources;
  - whether Colour Tone (and Warm2) is selectable or greyed out in your normal PC/receiver setup (Samsung's e-Manual notes Colour Tone is available only with an HDMI-to-DVI connection, so please check whether it is available over standard HDMI);
  - which controls are greyed out in the current configuration, and whether the input is already labelled as a PC or Game Mode is already on; do not switch either setting for this checklist.
- [x] **Connectors:** Confirmed in S-032 (C-074): round 3.5 mm socket labelled **`EX-LINK`** on the rear of the TV panel (not on the One Connect box).
- [ ] **Which HDMI input** the receiver or PC feeds, and the input's name or icon in the TV's source list.

### 2. PC

- [x] Windows version: confirmed in S-032 (C-075) as **`Windows 10 Home 22H2`** (exact OS build number via `winver` optional).
- [x] Graphics card model and driver version: confirmed in S-032 (C-075) as **`NVIDIA GTX 1080 8GB`**, **`GeForce Driver Version 582.78`** (confirming C-045's GPU model).
- [ ] Output to the TV: resolution, refresh rate, colour format (RGB or YCbCr), colour depth, and output dynamic range (full or limited), as shown in the NVIDIA Control Panel.
- [ ] Windows settings for the TV display: HDR on or off, "Automatically manage colour for apps" (if applicable), Night light, and any colour profile assigned to it.
- [ ] Colour or display tools installed: DisplayCAL, ArgyllCMS (which version), Datacolor's Spyder software, ColorControl, or similar.
- [ ] RGB-lighting or similar background programs (for example Gigabyte RGB Fusion), which ArgyllCMS's instructions say can block meter access.
- [ ] **Distances:** how far the PC is from the TV's Ex-Link socket and from the middle of the screen. The selected cable is 6 ft (about 1.8 m); the meter's cable must also reach.

### 3. Denon AVC-X3800H receiver

- [ ] Firmware version.
- [ ] A simple connection diagram, for example "PC → Denon HDMI input 2 → Denon monitor output → TV HDMI 3", including every other source and which input it uses.
- [ ] For the PC's input: the Video Mode setting (for example Auto, Game, Movie or Bypass), HDMI Upscaler, and the 4K/8K Signal Format setting.
- [ ] Whether the receiver shows its own on-screen messages, such as volume or input information, over the picture.

### 4. Spyder5 colour meter

- [ ] Which edition: Spyder5Express, Spyder5Pro or Spyder5Elite.
- [ ] Whether Datacolor's software is installed, and whether you still have its installer.
- [ ] Its USB cable length, and how you plan to hang it: where the cable runs (over the top edge?), and whether the meter will touch the screen (C-023).

### 5. Ex-Link cable

- [x] Has it arrived? Confirmed in S-032 (C-076): arrived.
- [x] What the packaging or product page says about the 3.5 mm plug's wiring and RS-232 level: confirmed in S-032 (C-076, matching S-026/C-064) — printed `SH-U35B` leaflet (`A100033`) states `Tip: RX (Receives from device TX), Ring: TX (Transmits to device RX), Sleeve: GND` and describes a `USB serial RS232 cable`, without naming a transceiver IC or voltage levels.
- [ ] If its device name and COM port are already recorded, report them; otherwise leave them unknown. Do not connect either end for this checklist. A connection check belongs in a reviewed, authorised plan (X-009).

### 6. Viewing and playback

- [ ] The room when you normally watch: dark, dim or bright, and whether daylight reaches the screen.
- [ ] Any brightness you prefer or have used before. The ChatGPT research mentions 250 cd/m² as a previous value of yours (C-029); is that right?
- [ ] What you watch on this TV, through which devices and inputs (for example a PC, games console or streaming box), and whether any of them send HDR.
- [ ] Which input and picture mode you would like calibrated first (Q-014).
