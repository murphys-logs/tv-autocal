# Owner equipment and environment checklist (26 October 2026)

| Field | Value |
|---|---|
| Title | Owner's completed equipment, display, signal path and viewing environment checklist |
| Produced by | Owner (verbatim checklist responses); structured framing by AI: Antigravity (Google) |
| Original date | 2026-10-26 |
| Imported | 2026-10-26, by Antigravity (Google), in the pull request for owner checklist import |
| How obtained | The owner's verbatim completed checklist responses provided in the Antigravity conversation |
| Fidelity | Condensed extraction of the owner's completed checklist responses, structured under the checklist section headings. Item 5's original prompt asked: "When the USB plug is inserted into the PC, what COM port number does Windows Device Manager assign to it under Ports (COM & LPT)? (PC check only; DO NOT plug into TV)". The owner's personal username in the installation path (item 2.3) is redacted under AGENTS.md section 11. No serial numbers or private credentials were submitted or recorded ([AGENTS.md section 11](../../AGENTS.md#11-privacy-and-credentials)). |
| Ledger ID | S-033 |

This archive is the source of claims C-077 to C-084 in [LEDGER.md](../../LEDGER.md), settles disagreement X-003, completes owner checks T-001 and T-002, and records the provisional calibration targets under Q-014. Do not edit it.

## Owner's completed checklist responses (structured extraction)

### 1. Samsung TV (`UE49KS7000UXXU`) — Look-Only Check (T-001)

#### 1.1 Picture Modes & Basic Sliders

- **Picture modes offered:** `[Dynamic, Standard, Natural, Movie]`
- **Current values and ranges for basic controls:**
  - Backlight: `0-20`, current value: `8`
  - Brightness: `0–100`, current value: `45`
  - Contrast: `0–100`, current value: `95`
  - Sharpness: `0–100`, current value: `0`
  - Colour: `0–100`, current value: `50`
  - Tint (G/R): current value: `G50/R50`
  - Gamma: integer slider `-3..+3`, current value: `0`
  - Colour Tone: `Warm1`, `Warm2`, `Standard`, `Cool`, current value: `Warm 2`
  - Colour Tone (and specifically `Warm2`) is selectable

#### 1.2 White Balance & Colour Space

- **2-Point White Balance controls:**
  - All six sliders present: `R-Offset`, `G-Offset`, `B-Offset`, `R-Gain`, `G-Gain`, `B-Gain`
  - Ranges and current values: `-50..+50`, current values: all `0`
- **Multi-Point White Balance (X-003):**
  - Menu offers 10-point White Balance
  - Intervals labelled `10%`, `20%`... `100%`
  - Multi-Point White Balance currently selectable
- **Colour Space Settings:**
  - Modes offered: `Auto`, `Native`, `Custom`
  - When set to `Custom`, colour controls are `Red`, `Green`, `Blue`, `Yellow`, `Cyan`, `Magenta`, each with `Red`, `Green`, `Blue` sliders

#### 1.3 Enhancements, Processing & Input Configuration

- **Enhancement settings:**
  - HDMI Black Level: `Auto`
  - HDMI UHD Color: `On`
  - Digital Clean View: `Off`
  - Auto Motion Plus: `Off`
  - Smart LED: `Off`
  - Dynamic Contrast: `Off`
  - Eco Solution settings: `All off`
- **Input labelling and lockouts:**
  - Physical HDMI port on One Connect box: `HDMI 4`
  - TV Source menu device icon / type: `Home Cinema`
  - Game Mode: currently turned off
  - Are any picture controls currently greyed out? `NO`
  - Apply Picture Settings: `All Sources`

---

### 2. Windows 10 PC — Display & Output Settings (T-002)

#### 2.1 NVIDIA Control Panel Settings (`Display → Change resolution`)

- **Resolution & Refresh Rate:** `3840×2160 @ 60 Hz`
- **Under "Apply the following settings":**
  - Output color format: `RGB`
  - Output color depth: `8bpc`
  - Output dynamic range: `Limited`

#### 2.2 Windows Settings (`Settings → System → Display`)

- **Windows HD Color / HDR:** `Off`
- **Night light:** `Off`
- **Color profile assigned:** `No profile loaded or selectable`

#### 2.3 Software & Background Utilities

- **Calibration & meter tools installed on this PC:**
  - ArgyllCMS installed: `yes V3.5.0 [unpacked in Downloads folder; personal username path redacted under AGENTS.md section 11]`
  - DisplayCAL installed: `Yes`
  - Datacolor Spyder5 software installed: `No`
- **RGB / Lighting background programs:** `No`

#### 2.4 Physical Distances

- **PC to TV Ex-Link distance (6 ft reach without strain):** `Yes`
- **PC to TV Spyder5 USB distance (reaches centre of screen):** `Yes`

---

### 3. Denon AVC-X3800H AV Receiver (T-002)

#### 3.1 Connection Route

- **Cabling route:** `PC HDMI → Denon HDMI In PC → Denon Monitor 1 (eARC) → TV HDMI 4`

#### 3.2 Denon Receiver Settings

- **Firmware version:** `6000-1060-0071-9831`
- **Video Processing settings:**
  - Video Mode: `Auto`
  - HDMI Upscaler: `Off`
  - 4K/8K Signal Format: `Enhanced`
- **On-screen volume/status overlays:** displays volume or input info banners over picture during video playback: `Yes`

---

### 4. Datacolor Spyder5 Meter (T-003)

- **Spyder5 Edition:** `Spyder5Pro`
- **Original software & license:** still has original installation software and serial/activation code: `Yes`
- **Cable length & hanging arrangement:**
  - Hanging arrangement: hanging by its USB cable draped over the top edge of the TV, counterweight hanging behind
  - Sensor rests flat against screen surface when hanging: `Yes`

---

### 5. DSD TECH Ex-Link Cable (`SH-U35B`) (T-006)

- **Assigned COM Port (checklist item 5 prompt: "When the USB plug is inserted into the PC, what COM port number does Windows Device Manager assign to it under Ports (COM & LPT)? (PC check only; DO NOT plug into TV)"; TV disconnected):** `USB Serial Port (COM3)`

---

### 6. Viewing Environment & Calibration Preferences (Q-014)

- **Room lighting:** `Dim (soft ambient lighting or low lamp)`
- **Target peak brightness preference:** `140–160 cd/m²` for SDR
- **Primary content:** `all of PC desktop, SDR movies/streaming, gaming and HDR content`
- **Initial calibration priority:** `Movie mode on PC/Denon HDMI Input`
