# Equipment

What the owner has said about the equipment, and what still needs confirming. The original equipment comes from the owner's brief (S-001); the selected cable and purchase details come from the owner's later confirmation (S-004); the meter's position comes from the owner's later description (S-011); the rear `EX-LINK` port, exact model label, TV firmware version, PC OS/GPU/driver and delivered cable leaflet come from the owner's confirmations and photographs of 26 October 2026 (S-032); and the normal-menu picture controls, 10-point white balance, signal path, PC output, Denon receiver settings, meter edition and viewing preferences come from the owner's completed checklist of 26 October 2026 (S-033). All are in the ledger's [sources](../LEDGER.md#1-sources). Nothing has been tested yet. [LEDGER.md](../LEDGER.md) is the formal record: if this page and the ledger ever differ, the ledger wins and this page should be corrected.

## TV — the display to calibrate

- **Model:** Samsung UE49KS7000UXXU — confirmed on the rear panel label (S-032, C-074)
- **Firmware version:** `T-JZMDEUC-1270.1 , BT - S` (`Sub-micom: T-JZMDEUS-1007`, `e-Manual: JZDVBEUK-1.1.3`) — from the `Contact Samsung` screen (S-032, C-074; AI-transcribed from withheld owner photograph)
- **Picture controls offered by the menus, and their ranges:** confirmed by the owner in S-033 (C-077, C-078):
  - Picture modes: `[Dynamic, Standard, Natural, Movie]`. Initial calibration priority is Movie mode (mode active during checklist inspection not explicitly stated).
  - Basic sliders: Backlight `0–20` (current 8), Brightness `0–100` (current 45), Contrast `0–100` (current 95), Sharpness `0–100` (current 0), Colour `0–100` (current 50), Tint `G50/R50`, Gamma integer slider `-3..+3` (current 0; a -3..+3 slider; no BT.1886 option reported), Colour Tone `Warm2` (selectable over HDMI).
  - White balance: 2-point controls all six present (`R/G/B-Offset` and `R/G/B-Gain`, range `-50..+50`, current values all 0); multi-point control offers **10 points** (`10%` to `100%`, selectable — settles X-003; 10-point slider ranges, current values and enable state not reported).
  - Colour Space: `Auto`, `Native`, `Custom` (Custom provides `Red`, `Green`, `Blue`, `Yellow`, `Cyan`, `Magenta`, each with `Red`, `Green`, `Blue` sliders).
  - Enhancement settings: HDMI Black Level `Auto`, HDMI UHD Color `On`, Digital Clean View `Off`, Auto Motion Plus `Off`, Smart LED `Off`, Dynamic Contrast `Off`, Eco Solution `All off`.
  - Input configuration: One Connect `HDMI 4`, labelled `Home Cinema`, Game Mode `Off`, Apply Picture Settings to `All Sources`, no picture controls greyed out. Substantively completes T-001 (10-point slider values remain unrecorded).
- **Control route:** Samsung Ex-Link only — D-006. Connection, cable compatibility and command support remain **not tested** — T-006.
- **Network remote control:** out of scope under D-006; C-006 and T-007 are retained as superseded history.
- **Ex-Link jack:** round 3.5 mm socket labelled **`EX-LINK`** on the rear of the TV panel (between `USB (IoT EXTEND)` and `LAN` behind `Cover Terminal`, **not** on the One Connect box) — confirmed by the owner and rear-bay photograph (S-032, C-074). Electrical compatibility and command support on `T-JZMDEUC-1270.1` remain **not tested** — T-006.

## Colour meter

- **Model:** Datacolor Spyder5 colorimeter — **Spyder5Pro** edition confirmed by the owner (S-033, C-082). Original installer and activation serial code retained; vendor software not installed.
- **Position during readings:** hangs by its USB cable draped over the top edge of the TV in the middle of the screen, counterweight hanging behind; sensor rests flat against the screen surface — reported by the owner (S-033, C-023, C-082; clarifies S-011's description of cap hanging beneath).
- **Software installed on PC:** ArgyllCMS V3.5.0 unpacked in Downloads; DisplayCAL installed (S-033, C-082). S-053/C-102 additionally reports ArgyllCMS as installed on the PC. Whether these refer to one or multiple copies, and which executable DisplayCAL used, are unknown. Select one reviewed path/hash under the [execution identity gate](tests/component-execution.md#reviewed-software-and-local-inputs); private paths stay out of the repository.
- **Works with ArgyllCMS on the owner's PC:** owner reports prior Spyder5 use through DisplayCAL without noticed issues ([S-053](briefs/2026-10-28-owner-readiness-inputs.md#runtime-choice-and-historical-use)); project discovery and wrapper operation remain untested — T-003.
- **Spectral correction for this TV:** none identified or validated — T-004, Q-001

## Computer

- **Type:** Windows PC
- **Windows version:** `Windows 10 Home 22H2` — confirmed by the owner (S-032, C-075)
- **Graphics card and driver:** `NVIDIA GTX 1080 8GB`, `GeForce Driver Version 582.78` — confirmed by the owner (S-032, C-075; confirms C-045's GPU model)
- **Video output settings and colour/display tools:** confirmed by the owner (S-033, C-080): resolution `3840×2160 @ 60 Hz`, Output color format `RGB`, Output color depth `8bpc`, Output dynamic range `Limited` (16–235), Windows HD Color / HDR `Off`, Night light `Off`, no color profile loaded or selectable. No RGB-lighting background utilities running. Physical distances from PC reach both the TV rear Ex-Link jack (6 ft) and Spyder5 screen placement without strain. Completes T-002.

## AV receiver

- **Model:** Denon AVC-X3800H
- **Firmware version:** `6000-1060-0071-9831` — confirmed by the owner (S-033, C-081)
- **Signal route:** sits in the video path between PC and TV: `PC HDMI → Denon HDMI In PC → Denon Monitor 1 (eARC) → TV HDMI 4` (S-033, C-079).
- **Video settings:** Video Mode `Auto`, HDMI Upscaler `Off`, 4K/8K Signal Format `Enhanced`, on-screen volume/status overlays `Yes` (S-033, C-081). Switching to `Bypass` in a future plan remains available to bypass processing and overlays (C-071). Completes T-002.

## Additional hardware

- **Selected cable:** [DSD TECH USB RS232 to 3.5mm Serial Cable with FTDI FT232RL Chip 6FT](https://www.amazon.co.uk/dp/B07XXWVH69) (`Model: SH-U35B`).
- **Source:** purchase details reported by the owner (S-004, C-008); delivered printed user-guide leaflet (`A100033`) supplied by the owner and transcribed in S-032 (C-076), matching the online `SH-U35B` guide (S-026, C-064).
- **Purchased:** 24 October 2026 at 21:00 (time zone not stated).
- **Total paid:** £15.99, including delivery.
- **Delivery status:** arrived (confirmed 26 October 2026, S-032, C-076).
- **Leaflet specifications:** `Model: SH-U35B`, `FTDI FT232RL` (or `FT232RNL` on some batches), 6 ft, described as an RS-232 serial cable wired `Tip = RX (device TX), Ring = TX (device RX), Sleeve = GND`; separate RS-232 transceiver IC and voltage swing are not stated (C-064, C-076).
- **PC COM Port:** `USB Serial Port (COM3)` assigned in Device Manager when inserted into PC with TV disconnected (S-033, C-083).
- **Compatibility with the TV and Ex-Link:** **not tested** — T-006. Neither the purchase nor the leaflet establishes electrical or firmware compatibility or authorises any physical test.

Budget: **£25** in total · Spent: **£15.99** · Remaining: **£9.01** — see the ledger's [budget section](../LEDGER.md#7-hardware-budget). No further purchase or physical test is authorised by this record.

## Viewing environment and calibration targets (provisional Q-014)

- **Room lighting:** Dim (soft ambient lighting or low lamp) (S-033, C-084).
- **Target peak brightness preference:** `140–160 cd/m²` for SDR (S-033, C-084).
- **Primary content:** PC desktop, SDR movies/streaming, gaming, and HDR content (S-033, C-084).
- **Initial calibration priority:** Movie mode on PC/Denon HDMI input (`HDMI 4`) (S-033, C-084).

## What we still need from you

These are **owner checks**: you look things up and tell us. They need no test plan, because no agent operates anything. Please:

- **only look:** write down current values before changing anything, and change nothing for the project yet;
- **stay out of the service menu**, and don't plug the Ex-Link cable into the TV;
- **keep private details out of what you send:** no serial numbers, IP or MAC addresses, or photos that show people or your room. Photos of labels or menus are fine; they stay in the private `local/` folder unless you approve one for the repository.

The initial look-only checklist is substantively **complete** (S-033), with the items recorded below and in [LEDGER.md](../LEDGER.md). 10-point white-balance slider values and enable state remain unrecorded and can be noted when relevant before future calibration.

The proposed order of work after this is in [plan.md](plan.md).

### 1. TV

- [x] **Confirm the model** on the rear label. Confirmed in S-032 (C-074): rear label reads **UE49KS7000UXXU** (`Model: UE49KS7000U`, `Type No.: UE49KS7000`).
- [x] **Firmware version** (Settings → Support → Contact Samsung). Confirmed in S-032 (C-074): **`T-JZMDEUC-1270.1 , BT - S`** (`Sub-micom: T-JZMDEUS-1007`, `e-Manual: JZDVBEUK-1.1.3`). Please don't install a firmware update during the project without telling us first (C-053).
- [x] **Normal-menu picture controls** (T-001). Substantively confirmed in S-033 (C-077, C-078):
  - Picture modes offered: `[Dynamic, Standard, Natural, Movie]`;
  - Controls, ranges and owner-reported current values: Backlight `0–20` (8), Brightness `0–100` (45), Contrast `0–100` (95), Sharpness `0–100` (0), Colour `0–100` (50), Tint `G50/R50`, Gamma slider `-3..+3` (0; a -3..+3 slider; no BT.1886 option reported), Colour Tone `Warm2` (selectable over HDMI);
  - White balance: 2-point controls all six present (`-50..+50`, current all 0); multi-point control offers **10 points** (`10%` to `100%`, selectable; settles X-003; 10-point slider values/range unrecorded);
  - Colour Space: `Auto`, `Native`, `Custom` (Custom provides RGBCYM with RGB sliders);
  - HDMI Black Level `Auto`, HDMI UHD Color `On`, Digital Clean View `Off`, Auto Motion Plus `Off`, Smart LED `Off`, Dynamic Contrast `Off`, Eco Solution `All off`;
  - Apply Picture Settings set to `All Sources`;
  - Colour Tone (and specifically `Warm2`) is selectable over HDMI;
  - No picture controls greyed out; Game Mode is off; input labelled `Home Cinema`.
- [x] **Connectors:** Confirmed in S-032 (C-074): round 3.5 mm socket labelled **`EX-LINK`** on the rear of the TV panel (not on the One Connect box).
- [x] **Which HDMI input** the receiver feeds: `HDMI 4`, icon/device type `Home Cinema` (S-033, C-079).

### 2. PC

- [x] Windows version: confirmed in S-032 (C-075) as **`Windows 10 Home 22H2`** (exact OS build number via `winver` optional).
- [x] Graphics card model and driver version: confirmed in S-032 (C-075) as **`NVIDIA GTX 1080 8GB`**, **`GeForce Driver Version 582.78`** (confirming C-045's GPU model).
- [x] Output to the TV: resolution `3840×2160 @ 60 Hz`, colour format `RGB`, colour depth `8bpc`, output dynamic range `Limited` (16–235), as shown in NVIDIA Control Panel (S-033, C-080).
- [x] Windows settings for the TV display: HDR `Off`, Night light `Off`, no color profile loaded or selectable (S-033, C-080).
- [x] Colour or display tools installed: ArgyllCMS V3.5.0 unpacked in Downloads folder, DisplayCAL installed, Datacolor Spyder software not installed (S-033, C-082).
- [x] RGB-lighting or similar background programs: none running (S-033, C-080).
- [x] **Distances:** PC is close enough for both the 6 ft Ex-Link cable and Spyder5 USB cable to reach without strain (S-033, C-080).

### 3. Denon AVC-X3800H receiver

- [x] Firmware version: `6000-1060-0071-9831` (S-033, C-081).
- [x] Connection diagram: `PC HDMI → Denon HDMI In PC → Denon Monitor 1 (eARC) → TV HDMI 4` (S-033, C-079).
- [x] For the PC's input: Video Mode `Auto`, HDMI Upscaler `Off`, 4K/8K Signal Format `Enhanced` (S-033, C-081).
- [x] Whether receiver shows on-screen overlays over picture: `Yes` (S-033, C-081).

### 4. Spyder5 colour meter

- [x] Which edition: `Spyder5Pro` (S-033, C-082).
- [x] Whether Datacolor's software is installed: not installed, but original installation software and serial/activation code retained (S-033, C-082).
- [x] USB cable length and hanging arrangement: USB cable draped over top edge of TV, counterweight hanging behind; sensor rests flat against screen surface (S-033, C-082; clarifies S-011).

### 5. Ex-Link cable

- [x] Has it arrived? Confirmed in S-032 (C-076): arrived.
- [x] What the packaging or product page says about wiring and RS-232 level: confirmed in S-032 (C-076, matching S-026/C-064) — `SH-U35B` leaflet (`A100033`) states `Tip: RX, Ring: TX, Sleeve: GND`, describing a `USB serial RS232 cable` without naming a transceiver IC or voltage levels.
- [x] Device name and COM port: `USB Serial Port (COM3)` assigned on PC with TV disconnected (S-033, C-083).

### 6. Viewing and playback

- [x] Normal viewing room: Dim (soft ambient lighting or low lamp) (S-033, C-084).
- [x] Brightness preference: `140–160 cd/m²` target for SDR (S-033, C-084).
- [x] What you watch on this TV: PC desktop, SDR movies/streaming, gaming, and HDR content (S-033, C-084).
- [x] Which input and picture mode to calibrate first: Movie mode on PC/Denon HDMI input (`HDMI 4`) (Q-014, S-033, C-084).
