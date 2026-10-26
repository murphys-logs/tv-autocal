# Staged Roadmap to SDR Calibration

> **Status:** Proposed technical roadmap. Authorises no physical tests and touches no real equipment.  
> Every physical step requires an independent test plan explicitly authorised by the owner ([AGENTS.md section 5](../AGENTS.md#5-evidence-provenance--safety-rules)).

---

## 1. Fixed Architectural Boundaries

* **TV Control Channel:** Samsung Ex-Link RS-232 serial only (D-006). Baud 9600 8N1, 7-byte binary packets (`08 22 cmd1 cmd2 cmd3 val checksum`). Service menu access is strictly forbidden.
* **Measurement Probe:** Datacolor Spyder5 colorimeter managed via ArgyllCMS `spotread -O` with quantum-dot CCSS spectral correction.
* **Measurement Cycle (D-013):** Mandatory sequence for all physical readings:  
  $$\text{Change Setting} \longrightarrow \text{Exit TV Menu} \longrightarrow \text{Settle Delay (Q-008)} \longrightarrow \text{Take Probe Reading}$$
  *Eliminates on-screen menu distortion during colorimeter measurement purely through sequential menu exit and settling.*
* **Hardware Budget:** £25.00 total limit. £15.99 spent on FTDI Ex-Link cable; £9.01 remaining.

---

## 2. Execution Stages

### Stage 1: Owner Information & Look-Only Checks
* **Action:** The owner inspects physical labels and on-screen menus without connecting cables or operating instruments ([docs/equipment.md](equipment.md#what-we-still-need-from-you)).
* **Pass Criteria:**
  * **T-001:** Exact TV model confirmed as `UE49KS7000UXXU`, firmware version recorded, user picture menu controls listed, and 3.5mm Ex-Link jack presence confirmed.
  * **T-002:** PC graphics card, Windows display settings, and Denon AVR HDMI pass-through/bypass settings recorded.
* **Stop Condition:** Model mismatch or missing Ex-Link jack (triggers fallback decision Q-013).

### Stage 2: Software Research & Pre-Test Decisions
* **Action:** Software-only research to establish model-specific Ex-Link command profiles, cable pin-outs, spectral correction candidate files (Q-001, Q-016), and provisional targets for Q-014.
* **Pass Criteria:** Written, peer-reviewed test plans prepared for Stage 4 component tests (T-003, T-004, T-005, T-006) with explicit pre-conditions, permitted commands, and restoration values.
* **Stop Condition:** Unresolved prerequisite or missing owner authorisation.

### Stage 3: Offline Software Verification (T-009)
* **Action:** Build and test pure Python Ex-Link message encoder and response parser using an in-memory mock transport with zero hardware access.
* **Pass Criteria (T-009):**
  * Exact byte encoding for standard 7-byte command frames and negative modulo-256 checksums (`checksum = (-sum(frame[0:6])) & 0xFF`).
  * Proper rejection of malformed frames, corrupted bytes, and disallowed commands (factory/service menu keys like `KEY_FACTORY 0x3B`).
  * Simulation of D-013 measurement cycle timing and failure state recovery.
* **Stop Condition:** Test suite failures or any attempt to touch real COM ports/hardware.

### Stage 4: Component Hardware Tests (T-003 to T-006)
*Each test requires an individual, owner-authorised test plan with the owner present.*

| Test | Objective | Pass Criteria | Stop / Abort Condition |
|---|---|---|---|
| **T-003 Meter** | Spyder5 / ArgyllCMS integration | ArgyllCMS detects probe; returns valid $XYZ$ values; acceptable repeatability on repeated reads | Driver conflict, communication failure, or excessive drift |
| **T-004 Correction** | CCSS spectral correction validation | Validated CCSS fingerprint verified against quantum-dot panel profile | Incompatible format, unverified correction (consult Q-016) |
| **T-005 Signal Path** | Bit-exact test pattern delivery | Full-range RGB output with video levels (16–235) verified; no clipping or crushing through AVR | Unexpected color conversion, range mismatch, or clipping |
| **T-006 Ex-Link** | Physical serial communication check | Serial cable pin-out verified; single allowlisted picture command acknowledged (`03 0C F1`); visual setting verified in menu; original value restored | No reply / NACK (`03 0C FF`), unexpected behavior, or prompt requiring service menu |

### Stage 5: Closed-Loop Reversible Feedback Test (T-013)
* **Prerequisites:** Satisfactory completion of T-001, T-002, T-003, T-005, T-006, and verified T-009 software suite.
* **Procedure:**
  1. Record original baseline setting for one non-destructive picture control (e.g. Backlight).
  2. Apply a 1-step change via Ex-Link $\rightarrow$ Exit menu $\rightarrow$ Wait settle delay $\rightarrow$ Measure change with Spyder5.
  3. Compute error gradient and apply a calculated second step $\rightarrow$ Exit menu $\rightarrow$ Wait delay $\rightarrow$ Confirm error reduction.
  4. Restore initial value via Ex-Link $\rightarrow$ Exit menu $\rightarrow$ Wait delay $\rightarrow$ Verify meter readings return to baseline within tolerance.
* **Pass Criteria:** Measured optical change matches predicted direction; restoration confirmed in both menu and meter output.
* **Stop Condition:** Measurement change indistinguishable from noise, failure to restore baseline, or unexpected TV response.

### Stage 6: Full SDR Closed-Loop Calibration (T-008)
* **Prerequisites:** Stages 1–5 passed; final target parameters chosen (Q-014); written test plan authorised by owner.
* **Execution Flow:**
  1. **Luminance:** Adjust Backlight to target peak white (100–130 cd/m²).
  2. **2-point White Balance:** Iteratively adjust RGB Gains (80% stimulus) and Offsets (20% stimulus) to D65.
  3. **Gamma / EOTF:** Set coarse Gamma slider to track BT.1886.
  4. **Multi-point Greyscale:** Tune 10-point/20-point parametric steps top-down.
  5. **CMS:** Optimize Red, Green, Blue, Cyan, Magenta, Yellow Hue/Saturation/Brightness sliders.
  6. **Independent Verification:** Run verification sweep on independent test patches (ColorChecker, saturation steps) and render final audit report and settings card.
* **Pass Criteria:** Average greyscale $\Delta E_{2000} \le 1.0$; average color gamut $\Delta E_{2000} \le 2.0$. Full settings card exported for manual recovery.

---

## 3. Universal Stop Rules for Physical Tests

1. **Owner Authority:** The owner may halt any test at any time for any reason.
2. **Immediate Abort on Anomaly:** Instantly stop testing upon unexpected display behavior, unacknowledged serial commands, unexpected menus, or probe disconnection.
3. **No Retries on Ambiguity:** Do not automatically resend failed or ambiguous serial commands. Halt, inspect state, and restore previous settings.
4. **Service Menu Guard:** Under no circumstances will any script or test plan enter the TV service menu.
5. **Restoration Protocol:** Every test plan includes an explicit manual and automated restoration procedure to return the TV to its pre-test settings.
