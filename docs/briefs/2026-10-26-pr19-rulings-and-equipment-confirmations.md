# PR #19 review rulings and equipment confirmations (26 October 2026)

| Field | Value |
|---|---|
| Title | Owner's rulings on PR #19 cross-vendor review findings, and equipment and cable confirmations |
| Produced by | Owner (verbatim message and four photographs); privacy-redacted photograph transcription by AI: Antigravity (Google) |
| Original date | 2026-10-26 |
| Imported | 2026-10-26, by Antigravity (Google), in PR #19 |
| How obtained | The owner's message and four attached photographs in the Antigravity conversation assessing the Claude Code and Codex reviews of PR #19 |
| Fidelity | Verbatim for the owner's message in the text block below. The four raw photographs are withheld from the public repository under AGENTS.md section 11 (Photograph 2 shows the TV's serial number and desktop screen) and docs/equipment.md; Antigravity's redacted transcription of non-private label, screen and leaflet text is recorded separately below as AI-transcribed evidence |
| Ledger ID | S-032 |

This archive is the source of the pre-merge review updates in PR #19 and claims C-074 to C-076 in [LEDGER.md](../../LEDGER.md). Do not edit it.

## Owner's message (verbatim)

```text
I will go with both your recommendations. I can now confirm that there is an EX LINK socket on the rear of the TV panel, not on the one connect box (photograph attached). Also attached is a photograph of the exact model number and current firmware version. The PC is running Windows 10 Home 22H2 with an Nvidia GTX 1080 8GB using Geforce Driver Version 582.78. The two attached photographs of the leaflet are the full user manual and details of the DSD TECH cable.
```

## Context of the two recommendations accepted by the owner

*(Note: The text below is Antigravity's retrospective summary of the two recommendations it put to the owner; it is not the owner's wording.)*

In the immediately preceding assessment turn on 26 October 2026, Antigravity (Google) asked the owner to rule on two questions following the independent reviews of PR #19 by Claude Code (Anthropic) and Codex (OpenAI):

1. **Decision 1 — How to handle PR #19 given S-024's archive rule:** Antigravity's recommended Option A was to correct PR #19 on branch `antigravity/feasibility-study` before merge, then ask Claude Code or Codex to review the new commit SHA.
2. **Decision 2 — Which disagreements to record in `LEDGER.md`:** Antigravity's recommended Option A was to add `X-011` (`spotread -O` control flow when Spyder5 refresh calibration is pending: Codex versus Claude Code and Antigravity, settled by `T-003`) alongside the revised `X-010`, and fold the softened OneConnect wording into `C-065` without opening a second new disagreement entry unless Codex still objects after checking `BN68-07864G-00` pp. 5 and 10.

## Redacted transcription of the four owner-supplied photographs (`AI: Antigravity (Google)`)

The four attached JPEG files are withheld from git under [AGENTS.md section 11](../../AGENTS.md#11-privacy-and-credentials) and [docs/equipment.md](../equipment.md#what-we-still-need-from-you) because Photograph 2 contains the TV's serial number and parts of the owner's personal desktop screen. Because other agents cannot inspect the withheld image files unless the owner supplies redacted copies to them, details visible only in the photographs carry `AI: Antigravity (Google)` transcription provenance alongside the owner's photograph provenance:

1. **Photograph 1 — Rear port bay and manufacturer label on the TV panel:**
   - Recessed vertical port bay on the rear of the TV panel (with `Cover Terminal` removed), labelled from top to bottom: `COMMON INTERFACE`, `USB (IoT EXTEND)`, `EX-LINK` (round 3.5 mm socket), `LAN`, and `ONE CONNECT` (with the One Connect cable connected).
   - Manufacturer rear label beside the bay: `SAMSUNG`, `Model : UE49KS7000U`, `Type No.: UE49KS7000`, `Model Code : UE49KS7000UXXU`, `AC220-240V~ 50/60Hz 170W`, `Typical power : 84W` (rear moulding mark `BN68-07835C`).
2. **Photograph 2 — TV on-screen `Contact Samsung` (`Product Information`) overlay:**
   - `Model Code: UE49KS7000`
   - `Serial Number: [REDACTED — omitted under AGENTS.md section 11]`
   - `Software Version: T-JZMDEUC-1270.1 , BT - S`
   - `Sub-micom Version: T-JZMDEUS-1007`
   - `e-Manual Version: JZDVBEUK-1.1.3`
3. **Photographs 3 and 4 — Printed fold-out leaflet supplied with the DSD TECH cable (code `A100033`, front cover plus panels `P1`–`P6`):**
   - **Front cover:** `DSD TECH`, `User Guide`, `Model: SH-U35B`, `USB RS232 to 3.5mm Serial Cable`.
   - **Panel `P1`:** `Warranty Tips`, `Product Website Page` QR code, `Technical Support`.
   - **Panel `P2`:** `Important Note` stating the cable uses `FTDI FT232RL` by default and some batches use `FTDI FT232RNL` due to chip supply; `Product Introduction` (`USB to 3.5mm serial converter cable`).
   - **Panel `P3`:** Cable diagram (`1 USB`, `2 3.5MM Jack`, `3 UL2464 28AWG`) and `Specifications`: `Model: SH-U35B`, `Connectors: USB Type-A (Male), 3.5mm Audio Jack (Male)`, `Interface Chip: FTDI FT232RNL`, `Cable Length: 6Feet (Approx.)`, `Signal Lines: TX, RX, GND`.
   - **Panel `P4`:** `Pinout (3.5mm Jack): Tip: RX (Receives from device TX), Ring: TX (Transmits to device RX), Sleeve: GND`; `Supported OS`; `Features` (`USB serial RS232 cable`, `TIP-RXD, RING-TXD, SLEEVE-GND`); `Wiring Diagram` (`Pin #1 - RXD`, `Pin #2 - TXD`, `Pin #3 - GND`, `1800±30` mm). Neither a separate RS-232 transceiver IC nor voltage levels are stated.
   - **Panel `P5`:** `How to find the driver` QR codes, `List of supported systems`, `Warranty` (24-month warranty).
   - **Panel `P6` (`A100033`):** `Contact DSD TECH`, `DONG GUAN DESHIDE TECHNOLOGY CO, LTD`, `Support Email: dsd_tech@outlook.com`.

Interpretation and claims are recorded in [LEDGER.md](../../LEDGER.md). This archive does not establish electrical or protocol compatibility (`T-006`) or authorise any physical test.
