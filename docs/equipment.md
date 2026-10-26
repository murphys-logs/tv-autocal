# Equipment Specifications & Status

A concise record of the owner's equipment, current configuration, and look-only owner checks. Formal claim statuses are maintained in [LEDGER.md](../LEDGER.md).

---

## 1. Hardware Inventory

| Equipment | Model / Details | Role & Interface | Status |
|---|---|---|---|
| **Television** | Samsung UE49KS7000UXXU | Target display (Edge-lit Quantum Dot SUHD). Controlled via rear 3.5mm Ex-Link serial port (D-006). | Firmware & accessible picture controls pending owner check (T-001). |
| **Color Meter** | Datacolor Spyder5 | Colorimeter placed on screen center via USB to PC. Driven via ArgyllCMS `spotread -O`. | Integration pending driver & script check (T-003). |
| **Computer** | Windows PC (NVIDIA GTX 1080) | Generates test patterns, executes solver, and sends serial commands. | Configuration pending check (T-002). |
| **AV Receiver** | Denon AVC-X3800H | Pass-through HDMI switch between PC and TV. Must be configured in Video Mode Bypass. | Passthrough settings pending check (T-002). |
| **Serial Cable** | DSD TECH USB-to-RS232 with FTDI FT232RL chip & 3.5mm plug | 6-foot serial cable connecting PC USB to TV Ex-Link port. Purchased 24 Oct 2026 for £15.99. | Compatibility untested (T-006). Remaining budget: £9.01. |

---

## 2. What We Still Need from You (Look-Only Owner Checks)

These are **visual, non-destructive checks**. Do not connect cables, change active project settings, or enter the TV service menu. Report observations in conversation for recording in the ledger.

### A. TV (T-001)
- [ ] **Exact Model Confirmation:** Confirm the model number on the rear sticker is `UE49KS7000UXXU` (C-001).
- [ ] **Firmware Version:** Look up firmware in `Settings -> Support -> About This TV`.
- [ ] **Ex-Link Port Verification:** Confirm whether a 3.5mm port labeled `EX-LINK`, `RS-232C`, or `External Sync` exists directly on the TV chassis or the One Connect box.
- [ ] **Picture Menu Controls:** For your standard viewing mode (e.g. Movie), record:
  - Default values for Backlight, Brightness, Contrast, Sharpness, Color, Tint.
  - White Balance controls: 2-point controls and whether multi-point offers 10 or 20 points.
  - Gamma options: presence of BT.1886 mode vs slider only.
  - Color Space settings: presence of Custom RGB sliders.
  - HDMI Black Level setting (`Low` / `Normal`).

### B. PC & Graphics Pipeline (T-002)
- [ ] **Windows Version & Build:** Check `winver`.
- [ ] **GPU & Drivers:** Confirm NVIDIA graphics card model (e.g. GTX 1080) and installed driver version.
- [ ] **NVIDIA Control Panel Settings:** Check Resolution, Refresh Rate, Color Format (RGB 8-bit), and Dynamic Range (Full 0–255).
- [ ] **Windows Display Settings:** Confirm Windows HDR is Off, Night light is Off, and Auto Color Management is disabled.
- [ ] **Distance:** Confirm that the 6ft (1.8m) Ex-Link cable and Spyder5 USB cable comfortably reach from the PC to the TV and screen center.

### C. Denon AVC-X3800H AV Receiver (T-002)
- [ ] **Connection Topology:** Confirm cable path (e.g. `PC -> Receiver HDMI In -> Receiver Monitor Out -> TV HDMI In`).
- [ ] **Video Processing:** Confirm PC HDMI input is set to `Video Mode: Bypass` and i/p Scaler is disabled to prevent alteration of test patches.

### D. Spyder5 Colorimeter
- [ ] **Model Edition:** Express, Pro, or Elite.
- [ ] **Placement:** Confirm the probe hangs securely at screen center without putting excessive pressure on the panel.
