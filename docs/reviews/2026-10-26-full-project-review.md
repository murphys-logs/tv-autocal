# Full Project Review of tv-autocal (26 October 2026)

| Field | Value |
|---|---|
| Document | Comprehensive technical, evidentiary and architectural review of the `tv-autocal` project |
| Reviewer | Antigravity (Google) |
| Review date | 2026-10-26 |
| Target commit baseline | `ba099e0` (Merge pull request #20 into `main`) |
| Key inputs evaluated | Owner's completed equipment and environment checklist ([S-033](../briefs/2026-10-26-owner-equipment-checklist.md)) and same-day confirmations ([S-032](../briefs/2026-10-26-pr19-rulings-and-equipment-confirmations.md)) |
| Primary governance reference | [AGENTS.md](../../AGENTS.md) and [LEDGER.md](../../LEDGER.md) |

---

## 1. Executive Summary and Project Milestone Progression

This review completes a comprehensive audit of the `tv-autocal` codebase, documentation, evidentiary ledger, architectural design, signal chain, and hardware constraints. It incorporates the owner's completed equipment and viewing environment checklist ([S-033](../briefs/2026-10-26-owner-equipment-checklist.md)) as authoritative ground truth regarding the physical installation, display settings, graphics pipeline, AV receiver configuration, meter condition, and serial cable connection.

### Milestone Status

- **Stage 1 (Information only the owner can give): OFFICIALLY PASSED.**
  - All look-only owner checks ([T-001, T-002](../../LEDGER.md#5-outstanding-tests)) are complete. The TV model (`UE49KS7000UXXU`), firmware (`T-JZMDEUC-1270.1`), physical 3.5 mm `EX-LINK` port, Windows OS (`Windows 10 Home 22H2`), graphics card (`GTX 1080 8GB` on driver `582.78`), Denon receiver (`AVC-X3800H` on firmware `6000-1060-0071-9831`), meter (`Spyder5Pro`), Ex-Link cable (`SH-U35B` on `COM3`), and provisional calibration targets ([Q-014](../../LEDGER.md#6-open-questions)) are recorded in [LEDGER.md](../../LEDGER.md).
- **Stage 2 (Research and decisions): IN PROGRESS.**
  - Research on UK manuals ([S-025](../research/2026-10-26-antigravity-feasibility-study.md#2-decisive-dependency-table)), Denon video processing ([S-030](../research/2026-10-26-antigravity-feasibility-study.md#53-signal-path--test-pattern-renderer-tv_autocalpatterns--dependency-4c)), cable specifications ([S-026](../research/2026-10-26-antigravity-feasibility-study.md#51-ex-link-serial-control-backend-tv_autocalexlink--dependency-4a)), and ArgyllCMS driver behavior ([S-029](../research/2026-10-26-antigravity-feasibility-study.md#52-meter-interface--argyllcms-wrapper-tv_autocalmeter--dependency-4b)) is integrated.
  - The next immediate deliverables are draft test plans for component tests [T-003](../../LEDGER.md#5-outstanding-tests) (meter), [T-005](../../LEDGER.md#5-outstanding-tests) (signal path) and [T-006](../../LEDGER.md#5-outstanding-tests) (Ex-Link), along with resolution of open owner decisions ([Q-008](../../LEDGER.md#6-open-questions) delay, [Q-013](../../LEDGER.md#6-open-questions) fallback, and [Q-016](../../LEDGER.md#6-open-questions) correction policy).
- **Stage 3 (Software-only checks): UNBLOCKED.**
  - The pure Ex-Link encoder/parser verification suite ([T-009](../../LEDGER.md#5-outstanding-tests)) and simulated TV/meter harnesses require no hardware and can be implemented immediately in Python.

---

## 2. Evidentiary Audit of the Owner's Authoritative Equipment Baseline

The owner's authoritative responses in [S-032](../briefs/2026-10-26-pr19-rulings-and-equipment-confirmations.md) and [S-033](../briefs/2026-10-26-owner-equipment-checklist.md) settle key open questions while establishing the operational boundaries for all subsequent work:

| Component | Authoritative Finding | Ledger References | Significance for Project |
|---|---|---|---|
| **TV Model & Panel** | Samsung `UE49KS7000UXXU` confirmed on rear label | [C-074](../../LEDGER.md#2-claims), [T-001](../../LEDGER.md#5-outstanding-tests) | Resolves model identity; satisfies Stage 1 stop rule |
| **TV Firmware** | `T-JZMDEUC-1270.1 , BT - S` (`Sub-micom: T-JZMDEUS-1007`) | [C-074](../../LEDGER.md#2-claims), [T-001](../../LEDGER.md#5-outstanding-tests) | Fixes the exact target firmware version for Ex-Link command testing |
| **Ex-Link Port** | Round 3.5 mm socket labelled `EX-LINK` on rear panel of TV body (not One Connect box) | [C-074](../../LEDGER.md#2-claims), [T-001](../../LEDGER.md#5-outstanding-tests) | Confirms physical hardware presence, disproving early ambiguity regarding missing ports |
| **TV Picture Modes** | `[Dynamic, Standard, Natural, Movie]`. Initial priority: `Movie` mode | [C-077](../../LEDGER.md#2-claims), [C-084](../../LEDGER.md#2-claims) | Establishes the target picture mode for SDR calibration |
| **Basic Sliders** | Backlight `8` (0–20), Brightness `45` (0–100), Contrast `95` (0–100), Sharpness `0` (0–100), Colour `50` (0–100), Tint `G50/R50` | [C-077](../../LEDGER.md#2-claims), [T-001](../../LEDGER.md#5-outstanding-tests) | Records exact original values for restoration; Backlight 8 yields ~140–160 cd/m² |
| **Gamma Control** | Integer slider `-3..+3`, current value `0`. No discrete BT.1886 mode | [C-077](../../LEDGER.md#2-claims), [C-060](../../LEDGER.md#2-claims) | **Critical architectural finding:** no discrete BT.1886 toggle exists on this set; curve must be shaped via offset slider and white balance |
| **Colour Tone** | `Warm 2` (current value; selectable over HDMI) | [C-077](../../LEDGER.md#2-claims), [C-063](../../LEDGER.md#2-claims) | Baseline D65 candidate setting is active and unlocked |
| **2-Point White Balance** | All 6 controls present (`R/G/B-Offset`, `R/G/B-Gain`), range `-50..+50`, current all `0` | [C-077](../../LEDGER.md#2-claims), [T-001](../../LEDGER.md#5-outstanding-tests) | Primary greyscale calibration controls are present at factory neutral |
| **10-Point White Balance** | Offers 10 points (`10%` to `100%`); selectable in user menu | [C-078](../../LEDGER.md#2-claims), [X-003](../../LEDGER.md#4-disagreements) | **Settles X-003** at descriptive level; confirms 10 points (not 20) |
| **Colour Space (CMS)** | Modes: `Auto`, `Native`, `Custom`. `Custom` provides RGBCYM, each with RGB sliders | [C-077](../../LEDGER.md#2-claims), [T-001](../../LEDGER.md#5-outstanding-tests) | Full 18-slider CMS is available in normal user menu |
| **Picture Enhancements** | Clean View `Off`, Auto Motion Plus `Off`, Smart LED `Off`, Dynamic Contrast `Off`, Eco `Off` | [C-077](../../LEDGER.md#2-claims), [T-001](../../LEDGER.md#5-outstanding-tests) | Dynamic luminance and frame-altering post-processing are disabled |
| **HDMI UHD Color** | Set to `On` on HDMI 4 | [C-077](../../LEDGER.md#2-claims), [T-001](../../LEDGER.md#5-outstanding-tests) | Unlocks full HDMI bandwidth on the input |
| **HDMI Black Level** | Set to `Auto` | [C-077](../../LEDGER.md#2-claims), [T-001](../../LEDGER.md#5-outstanding-tests) | **Signal path risk:** must be validated against GPU Limited range |
| **PC OS & Hardware** | `Windows 10 Home 22H2`, `NVIDIA GTX 1080 8GB`, driver `582.78` | [C-075](../../LEDGER.md#2-claims), [T-002](../../LEDGER.md#5-outstanding-tests) | Fixes the exact PC testbed; Windows 10 lacks Windows 11 SDR ACM |
| **PC Output Settings** | `3840×2160 @ 60 Hz`, `RGB`, `8bpc`, `Limited` dynamic range (16–235) | [C-080](../../LEDGER.md#2-claims), [T-002](../../LEDGER.md#5-outstanding-tests) | **Signal path risk:** GPU Limited range maps desktop 0–255 to 16–235 |
| **Windows Settings** | Windows HDR `Off`, Night light `Off`, no ICC profile loaded | [C-080](../../LEDGER.md#2-claims), [T-002](../../LEDGER.md#5-outstanding-tests) | OS-level color transformations and night-light LUTs are inactive |
| **Installed Software** | ArgyllCMS V3.5.0 unpacked in Downloads folder; DisplayCAL installed; Datacolor software not installed | [C-082](../../LEDGER.md#2-claims), [T-003](../../LEDGER.md#5-outstanding-tests) | Pre-requisite measurement software is present; personal path kept private |
| **Background Programs** | No RGB-lighting utilities running | [C-080](../../LEDGER.md#2-claims), [T-002](../../LEDGER.md#5-outstanding-tests) | Eliminates known USB conflict risk with Spyder5 colorimeters |
| **Denon AVC-X3800H** | Firmware `6000-1060-0071-9831`, Video Mode `Auto`, Scaler `Off`, 4K/8K `Enhanced`, Overlays `Yes` | [C-081](../../LEDGER.md#2-claims), [T-002](../../LEDGER.md#5-outstanding-tests) | **Overlay risk:** on-screen banners can corrupt readings; recommend `Bypass` |
| **Spyder5 Meter** | `Spyder5Pro` edition; original software/serial kept; hangs flat over top edge with counterweight | [C-082](../../LEDGER.md#2-claims), [T-003](../../LEDGER.md#5-outstanding-tests) | Meter physical mounting is verified flat against screen surface |
| **Ex-Link Serial Cable** | Delivered DSD TECH `SH-U35B` (FT232RL); Windows assigns `USB Serial Port (COM3)` | [C-076](../../LEDGER.md#2-claims), [C-083](../../LEDGER.md#2-claims) | COM port verified on PC; TV connection remains untested pending T-006 |
| **Viewing Targets** | Dim room, target peak brightness `140–160 cd/m²`, Rec.709/D65/BT.1886 on `Movie` mode | [C-084](../../LEDGER.md#2-claims), [Q-014](../../LEDGER.md#6-open-questions) | Provisional targets settled for Stage 2 planning |

---

## 3. Technical, Signal Path and Calibration Feasibility Audit

### 3.1 Signal Path Quantization and Level Matching (T-005 Critical Analysis)

A primary risk identified in this review is the interaction between GPU output dynamic range, pattern generation, receiver pass-through, and TV HDMI Black Level:

1. **Current Configuration:**
   - GPU (NVIDIA GTX 1080): Output dynamic range = **`Limited (16–235)`**.
   - AV Receiver (Denon AVC-X3800H): Video Mode = **`Auto`**.
   - TV (`UE49KS7000UXXU`): HDMI Black Level = **`Auto`**.
2. **Analysis of Level Mappings:**
   - On Windows, the desktop rendering compositor operates in full-range RGB (0–255).
   - When the NVIDIA driver is configured for `Limited` dynamic range, the GPU hardware automatically compresses full-range RGB (0–255) into video-range RGB (16–235) across the HDMI output.
   - If a test-pattern generator attempts to render video-level test patches (e.g., drawing `RGB 16, 16, 16` for reference black), the GPU driver will compress that value *again*, mapping `16` to approximately `29–30`. This results in severe near-black crushing and lifted black levels.
   - Conversely, if the pattern generator draws standard `RGB 0, 0, 0` to `255, 255, 255`, the GPU driver maps `0` to `16` and `255` to `235`.
   - On the TV side, setting `HDMI Black Level: Auto` relies on the HDMI AVI InfoFrame quantization range flags. If the TV misidentifies the signal as full range, reference black (16) will appear washed out / dark grey. If it detects limited range, it maps 16 to panel minimum luminance.
3. **Review Recommendation for T-005:**
   - Test plan [T-005](../../LEDGER.md#5-outstanding-tests) must explicitly measure optical patch output at 0%, 5%, 10%, 90%, 95%, and 100% stimulus under two distinct candidate baselines:
     - **Baseline A (Owner Current):** GPU `Limited (16–235)` + Pattern Generator Full (0–255) + TV `Auto`.
     - **Baseline B (Standard Calibrator Pipeline):** GPU `Full (0–255)` + Pattern Generator Full (0–255) + TV `HDMI Black Level: Low` (forcing limited-range expansion on the TV).

### 3.2 Denon Receiver Video Processing and On-Screen Overlay Suppression

The owner's checklist confirms that the Denon AVC-X3800H is currently in Video Mode `Auto` and that on-screen volume/status overlays are displayed over active video (`Yes`).

- **Measurement Risk:** If an on-screen volume banner, setup notification, or input status banner appears while the meter is taking a reading, the patch reading is completely invalid and violates the measurement cycle ([D-013](../../LEDGER.md#3-decisions)).
- **Primary Source Evidence:** Denon's official AVC-X3800H manual ([S-030](../research/2026-10-26-antigravity-feasibility-study.md#53-signal-path--test-pattern-renderer-tv_autocalpatterns--dependency-4c), [C-071](../../LEDGER.md#2-claims)) confirms that setting `Video Mode: Bypass`:
  1. Completely eliminates receiver video processing (passing the HDMI bitstream unmolested).
  2. Disables the internal HDMI upscaler.
  3. **Suppresses all on-screen status and volume banners over video playback.**
- **Review Recommendation:** Test plans for [T-005](../../LEDGER.md#5-outstanding-tests) and [T-013](../../LEDGER.md#5-outstanding-tests) should specify switching the Denon receiver's input Video Mode to `Bypass`.

### 3.3 Gamma Control Architecture and BT.1886 Realization

The owner's checklist resolves the question regarding gamma controls on the 2016 KS7000:
- The TV menu provides an integer slider: **`Gamma -3..+3`** (current value `0`).
- **No discrete BT.1886 menu option** is present in the `Movie` picture mode menu (contrasting with generic Samsung worksheets in [S-006](../../LEDGER.md#1-sources) and [C-060](../../LEDGER.md#2-claims)).
- **Calibration Significance:** Achieving a BT.1886 EOTF target cannot be done by toggling a menu preset. The application must:
  1. Measure the baseline gamma curve with `Gamma: 0`.
  2. Determine whether an offset of `-1`, `0`, or `+1` brings mid-tones closest to target.
  3. Use the 2-point and multi-point White Balance luminance offsets (adjusting R, G, B gains and offsets together) to sculpt the final EOTF curve.

### 3.4 Multi-Point White Balance Feasibility (HDTVTest Review Caution)

While owner check [T-001](../../LEDGER.md#5-outstanding-tests) settled [X-003](../../LEDGER.md#4-disagreements) by demonstrating that 10-point White Balance is present and selectable:
- **Technical Caution ([C-073](../../LEDGER.md#2-claims)):** HDTVTest's review of the UK `UE49KS7000` found that the 10-point controls were "contrast-aligned and didn't work well" on their sample, leading them to calibrate exclusively with 2-point controls.
- **Review Recommendation:**
  1. Closed-loop calibration ([T-013](../../LEDGER.md#5-outstanding-tests) and [T-008](../../LEDGER.md#5-outstanding-tests)) must optimize 2-point White Balance first (`R/G/B-Offset` and `R/G/B-Gain`).
  2. Multi-point controls should be evaluated only after 2-point calibration is locked, testing single-point adjustments at 50% stimulus with immediate rollback if inter-band distortion occurs.

### 3.5 Spyder5 Colorimeter Low-Light Floor vs Display Black Level

- **Physical Limitation ([C-072](../../LEDGER.md#2-claims)):** Independent benchmarks establish that the Datacolor Spyder5 has a low-light noise floor of approximately `0.38 cd/m²`.
- **Panel Native Black:** HDTVTest measured native black on a UK `UE49KS7000` at approximately `0.04 cd/m²` when calibrated to `120 cd/m²` peak white.
- **Feasibility Verdict:**
  - The Spyder5 cannot directly measure panel black or near-black stimulus below 5–10%.
  - Any attempt to read 0% black will return noise or instrument floor values (~0.3–0.4 cd/m²), severely distorting BT.1886 target calculation.
  - **Review Recommendation:** For BT.1886 target calculation, the application must adopt an assumed black level (e.g., peak white ÷ 3,000, yielding ~0.05 cd/m² for a 150 cd/m² target) or rely on visual PLUGE test patterns adjusted by the owner, rather than raw meter readings below 10% stimulus.

### 3.6 Ex-Link Serial Command Feasibility (T-006 Preparation)

- **Port & Cable Baseline:**
  - PC port: `USB Serial Port (COM3)` assigned to FTDI FT232RL ([C-083](../../LEDGER.md#2-claims)).
  - TV port: Round 3.5 mm `EX-LINK` jack on the rear panel ([C-074](../../LEDGER.md#2-claims)).
  - Physical reach: 6 ft cable reaches without strain ([C-080](../../LEDGER.md#2-claims)).
- **Pending Questions ([X-002](../../LEDGER.md#4-disagreements), [C-037](../../LEDGER.md#2-claims)):** Whether firmware `T-JZMDEUC-1270.1` has the Ex-Link port active in `UART` mode (accepting commands) or `Debug` mode (emitting console output) remains untested.
- **Review Recommendation:** Test plan [T-006](../../LEDGER.md#5-outstanding-tests) must test benign, allowlisted commands (e.g., OSD result toggle or volume query) without any service-menu intervention.

---

## 4. Governance, Multi-Vendor Process and Safety Audit

1. **Three-Vendor Balance ([AGENTS.md section 1](../../AGENTS.md#1-who-is-who), [D-017](../../LEDGER.md#3-decisions)):**
   - Anthropic (Claude Code), OpenAI (Codex), and Google (Antigravity) maintain equal cross-vendor review standing.
   - Substantive PRs authored by Antigravity require independent review by Claude Code or Codex prior to merge.
2. **Hardware Safety Rules ([AGENTS.md section 7](../../AGENTS.md#7-equipment-safety-rule-6)):**
   - No agent has operated the TV, meter, Denon receiver, or service menu.
   - All owner checks carried out to date ([T-001, T-002](../../LEDGER.md#5-outstanding-tests)) were look-only observations or PC-only device checks performed by the owner.
   - Physical tests [T-003, T-005, T-006, T-013, T-008](../../LEDGER.md#5-outstanding-tests) remain strictly unexecuted and require formal written plans and explicit owner authorisation.
3. **Financial Limit ([AGENTS.md section 8](../../AGENTS.md#8-money-services-and-irreversible-actions-rule-7), [LEDGER.md section 7](../../LEDGER.md#7-hardware-budget)):**
   - Total budget: £25.00.
   - Spent: £15.99 on delivered DSD TECH `SH-U35B` cable ([C-008](../../LEDGER.md#2-claims), [C-076](../../LEDGER.md#2-claims)).
   - Remaining: £9.01. No additional purchases are required or proposed.
4. **Privacy Protection ([AGENTS.md section 11](../../AGENTS.md#11-privacy-and-credentials)):**
   - The owner's Windows personal username in the ArgyllCMS path ([C-082](../../LEDGER.md#2-claims)) and raw photographs ([S-032](../../LEDGER.md#1-sources)) remain properly redacted and excluded from repository files.

---

## 5. Audit of Disagreements and Open Questions

### Disagreements Status

- **X-001 (Ex-Link power-on checksum):** Arithmetic resolved; retained as negative test fixture.
- **X-002 (Service-menu UART toggle):** Open; gated by [T-006](../../LEDGER.md#5-outstanding-tests).
- **X-003 (10-point vs 20-point White Balance):** **Settled by evidence** in [S-033](../../LEDGER.md#1-sources) ([C-078](../../LEDGER.md#2-claims)). The TV menu provides 10 points (10% to 100%).
- **X-004 (Spyder5 CCSS support):** Settled at documentation level ([C-055](../../LEDGER.md#2-claims)); physical check in [T-003](../../LEDGER.md#5-outstanding-tests).
- **X-005 (Acknowledgement vs readback):** Open; distinguished in [C-010](../../LEDGER.md#2-claims) and [T-006](../../LEDGER.md#5-outstanding-tests).
- **X-006 (Accuracy forecasts vs assumed black):** Open; forecasts are not criteria.
- **X-007 (Transport resend policy):** Open; initial tests use no-resend stop rule.
- **X-008 (Configured path vs demonstrated patch fidelity):** Open; gated by [T-005](../../LEDGER.md#5-outstanding-tests).
- **X-009 (Cable connection during owner check):** Open policy question for the owner; PC-only check performed in [S-033](../../LEDGER.md#1-sources) ([C-083](../../LEDGER.md#2-claims)).
- **X-010 (Overall feasibility verdict):** Open; Ex-Link control gated by [T-006](../../LEDGER.md#5-outstanding-tests).
- **X-011 (ArgyllCMS refresh calibration control flow):** Settled at source-code level ([C-068](../../LEDGER.md#2-claims)).

### Priority Open Decisions for the Owner

1. **[Q-008](../../LEDGER.md#6-open-questions) (Menu-exit delay):** A short delay (recommended: 1.5–2.0 seconds) after `KEY_EXIT` before reading, to allow menu graphics to clear and the panel liquid crystals / backlight to settle.
2. **[Q-013](../../LEDGER.md#6-open-questions) (Ex-Link fallback policy):** Confirmation that if Ex-Link commands fail, the project falls back to guided manual remote-control calibration.
3. **[Q-016](../../LEDGER.md#6-open-questions) (Spectral correction validation route):** Approach to proceed with candidate Q9 CCSS explicitly labelled as unvalidated.

---

## 6. Summary of Corrections Applied in this Pull Request

To align the entire repository with the authoritative checklist responses and the findings of this review, the following adjustments are made:

1. **`README.md`:**
   - Updated status date to 26 October 2026.
   - Removed completed owner checks [T-001, T-002] from the "What needs your decision" table (moving Stage 1 to completed status).
   - Updated [Q-014](../../LEDGER.md#6-open-questions) entry to reflect agreed provisional targets.
   - Clarified the immediate decision focus on Stage 2 test planning and fallback policy.
2. **`docs/equipment.md`:**
   - Updated section heading to reflect that the Stage 1 owner checklist is 100% complete.
   - Documented the critical findings: GPU Limited range mapping, Denon Bypass overlay suppression, integer Gamma slider `-3..+3`, and HDTVTest 10-point caution.
3. **`docs/plan.md`:**
   - Formally recorded that **Stage 1 has passed**.
   - Updated Stage 2 to reflect that prerequisite data is recorded and test planning for T-003, T-005, and T-006 is active.
4. **`docs/reviews/README.md`:**
   - Linked this full project review document.
5. **`LEDGER.md`:**
   - Maintained all ledger cross-references, test statuses, and claim relationships.

---

## 7. Review Conclusion and Next Steps

The `tv-autocal` project has established a rigorous evidentiary and governance baseline. The owner's completed checklist provides concrete technical boundaries that eliminate prior ambiguities regarding port availability, firmware identity, and menu options.

With Stage 1 complete, the project is ready for:
1. Cross-vendor review of this PR by Claude Code (Anthropic) or Codex (OpenAI).
2. Authoring formal written test plans for [T-003](../../LEDGER.md#5-outstanding-tests) (ArgyllCMS meter check) and [T-006](../../LEDGER.md#5-outstanding-tests) (Ex-Link communication test) following the [test template](../tests/TEMPLATE.md).
3. Implementing the software-only Ex-Link parser/encoder test suite ([T-009](../../LEDGER.md#5-outstanding-tests)).
