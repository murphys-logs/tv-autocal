# T-003 — Spyder5 recognition and diagnostic repeatability

> **Status: draft plan for independent review — NOT AUTHORISED. Do not carry out any step.**
> No instrument, display, receiver or cable was operated while preparing this plan. The owner's request to prepare it is not permission to run it.
> **Execution blockers:** independent review, explicit owner authorisation, and the reviewed patch renderer required for steps 5–11. No patch renderer is supplied by T-009.

Author: Codex (OpenAI), 27 October 2026. Baseline: `ba099e0a182713945c247636042286e6f9dca626`. Numerical limits below are **AI: Codex diagnostic proposals**, not published accuracy guarantees or owner decisions.

## 1. Purpose

Establish whether the installed ArgyllCMS can identify the owner's Spyder5Pro and produce actual XYZ measurements, then measure repeatability, warm-up drift and a provisional usable low-light range under one fixed setup. XYZ are the three reported colour-measurement components; Y represents luminance. A successful process exit alone is not a measurement.

This addresses C-002, the access portion of C-041, C-056, C-068 and X-011. It collects bounded evidence relevant to C-043/C-072 without adopting another meter's reported low-light floor. It does not deliberately test the interrupted-driver behaviour in C-069. C-082 supplies the owner's descriptive baseline. Neither repeatability nor this plan validates colour accuracy, a spectral correction, HDMI code fidelity or any TV control.

**Prerequisites and scope:**

| Requirement | Current state / action before the relevant step |
|---|---|
| T-001/T-002 owner baseline | Complete in [S-032](../briefs/2026-10-26-pr19-rulings-and-equipment-confirmations.md) and [S-033](../briefs/2026-10-26-owner-equipment-checklist.md); use these records, then record the actual session settings without treating the earlier values as factory defaults. |
| Independent review and owner authorisation | Pending. Authorisation must identify this plan's reviewed commit, date and exact steps. Discovery-only steps 1–4 may be authorised separately. |
| Meter installation | ArgyllCMS V3.5.0 is reportedly unpacked; USB driver access has not been demonstrated. Driver installation, replacement, `oeminst` and vendor-data extraction are outside this plan. Discovery failure stops the session for a separate proposal. |
| Reviewed patch renderer for steps 5–11 | **Missing.** Before authorisation of these steps, a reviewed amendment must identify the exact renderer/version or commit, executable/file SHA-256, launch/close procedure, display selection and software verification of its RGB buffers and geometry. It must implement the fixed patch sequence below without unattended changes or TV control. A browser, image viewer or an unspecified DisplayCAL window is not an interchangeable substitute. |
| Timing and diagnostic scope | Owner accepts the proposed 2.0-second minimum wait and section 7 limits for this test (Q-008). This does not settle a production delay. Q-014's existing Movie/HDMI 4/dim-room preference is sufficient; do not adjust brightness to achieve 140–160 cd/m² here. |
| Correction policy | This plan uses Argyll's generic calibration with no external `-X` file. The owner must explicitly accept these **uncorrected diagnostic readings only** within this plan. Q-001/T-004/Q-016 remain open for calibration. |

T-005 need not pass before these initial relative meter checks: the unchanged signal path is recorded as unvalidated. T-006 is not a prerequisite because the owner exits menus manually. Neither arrangement authorises Ex-Link operation or a later test.

**Sources consulted for this plan, 27 October 2026:** Graeme Gill/ArgyllCMS, [spotread documentation](https://www.argyllcms.com/doc/spotread.html) (S-014: `-O`, `-e`, `-x`, `-Y`, logfile and discovery behaviour) and [instrument documentation, Spyder 5 section](https://www.argyllcms.com/doc/instruments.html) (S-014: generic default calibration and optional CCSS/vendor data). The V3.5.0 source interpretation and abort warning are carried forward from [S-024 section 5.2 at the reviewed baseline](https://github.com/murphys-logs/tv-autocal/blob/ba099e0a182713945c247636042286e6f9dca626/docs/research/2026-10-26-antigravity-feasibility-study.md#L185), C-068/C-069 and X-011; those source files were not independently re-inspected for this plan. Live documentation alone does not prove the installed binary's behaviour.

## 2. Equipment and settings involved

- Owner's Windows 10 PC, GTX 1080, existing ArgyllCMS V3.5.0, Spyder5Pro and existing USB connection.
- Samsung UE49KS7000UXXU and Denon AVC-X3800H on `PC HDMI → Denon PC input → Monitor 1 → TV HDMI 4`.
- Ex-Link is unused. Keep the serial cable disconnected from the TV; no COM port is opened.
- Retain the recorded pipeline: 3840×2160 at 60 Hz, RGB, 8 bpc, NVIDIA Limited, Windows HDR/Night light off, TV HDMI Black Level Auto and Denon Video Mode Auto. Record any mismatch and stop for a plan amendment; do not silently normalise it.
- The owner may select the already agreed HDMI 4 input and Movie mode after recording the starting input/mode. No numerical picture control, GPU setting, LUT/profile or receiver setting is changed. Confirm the existing enhancement settings in [equipment.md](../equipment.md); a mismatch stops preparation.
- For readings, the reviewed renderer must show a centred **960×540 pixel** uniform patch on a black (`RGB 0,0,0`) surround. Meter stays flat at its centre. Patch values are equal-channel application RGB codes, **not demonstrated HDMI code values or known luminance percentages**.

The ordinary controls in Movie mode can differ from the values recorded during the earlier checklist, whose active mode was not explicit. Record this session's actual mode and values; do not substitute checklist values or change sliders to match them.

## 3. Risks and how to undo them

**No service menu is used.** Do not change white balance, brightness, backlight, gamma or colour controls. Repeated static patches, meter pressure or an unsecured cable are avoided by the fixed duration, supported counterweight and the owner's ability to stop. Stop if mounting cannot be done without strain.

The meter may be unavailable because its driver is missing or another program holds it. Close ordinary measurement programs before starting, but do not uninstall software or stop system services. C-069 warns against aborting the driver. There is no automatic kill, retry, USB reset or replug recovery in this plan.

Original session values must be recorded before changes; all cells below are deliberately blank observations:

| Device | Setting | Original value | Restored afterwards? |
|---|---|---|---|
| TV | Power state; input; picture mode | Not recorded | Not performed |
| TV | Current Movie settings: backlight, brightness, contrast, gamma, colour tone and enhancements | Not recorded | No slider changes permitted |
| PC / Denon / TV | Output format/range; HDR/Night light/profile state; receiver Video Mode; TV HDMI Black Level | Not recorded | No changes permitted |
| PC | Applications closed for the session; renderer display and window state | Not recorded | Not performed |
| Spyder5 | Initial USB connection and mounting state | Not recorded | Not performed |

On normal completion the owner closes the renderer, restores the original input/mode using normal menus, exits and waits 2.0 seconds, then restores the original physical meter arrangement after the measurement program has exited. No reading is taken after changing away from the diagnostic input; the final comparison reading is deliberately before that restoration. On abnormal behaviour, stop measurement activity; the owner may manually restore recorded ordinary settings as described in the pinned stop rules. Do not send further equipment commands or restart/replug the meter as an assumed recovery.

## 4. Cost

No purchase or paid service. Proposed extra spend: **£0**; project total remains **£15.99 spent / £9.01 remaining**. Use the existing installation. No vendor binary, calibration data, correction file or ArgyllCMS executable is committed or redistributed.

## 5. Steps

Every action below is a **future authorised action**, not an instruction to execute during review. The owner operates the equipment and launches each command; an agent may record and analyse results with the owner present. No unattended script or measurement loop is authorised.

1. **Owner and agent:** verify the authorisation covers the steps about to be performed and record the plan commit. Check the TV end of Ex-Link is disconnected, close DisplayCAL/other measurement applications, and identify the existing `spotread.exe` path privately. Record its version from its output when run and calculate its SHA-256 by ordinary file reading. Do not run any other calibration executable.
2. **Owner:** record section 3 baselines. For discovery-only authorisation leave TV/receiver settings unchanged. Connect the Spyder5 to the existing PC USB port if not already connected; record the driver name/version already shown by Windows Device Manager, without installing or changing it. If an installation prompt appears, stop.
3. **Owner:** run exactly `spotread.exe -?` using the identified executable. This is **instrument/port discovery and a physical step**, not a harmless software-only help check. Record the version, discovered instrument and selectable display types with device identifiers kept private. Stop if Spyder5 is absent, the device is ambiguous, the version differs from 3.5.0 or generic non-refresh type is unavailable. Do not guess a `-c` index or use the Ex-Link COM port.
4. **Owner and agent:** if only discovery was authorised, stop here and record the discovery result. No readings or TV patterns are permitted. For further steps, confirm the renderer prerequisite and explicit authorisation are satisfied, with exactly one supported measurement instrument available and the command's default instrument unambiguous.
5. **Owner:** record start time and whether the TV was already warm. If needed, turn it on with its normal remote, select HDMI 4 and Movie mode, and record the Movie settings without changing numerical controls. Set up the agreed dim room and mount the Spyder5 at the renderer's centre using the counterweight, without pressing it into the panel. Start the pinned renderer in the recorded output configuration; show `RGB 128,128,128`. Exit normal TV/receiver menus using the owner-operated remotes and wait at least **2.0 seconds** after menus have disappeared and the patch is stable. If an unexpected overlay/menu appears, stop; no automated screen check is claimed.
6. **Owner:** with that patch unchanged, take one initial reading using the command described below. Record actual finite XYZ/Yxy output and process completion. If output is calibration-only, erroneous, incomplete, non-finite or names the wrong instrument, reject the attempt and stop; do not repeat automatically. A valid initial reading establishes access only, not repeatability or accuracy.
7. **Owner:** retain the mid-grey patch and fixed setup. At **30, 35 and 40 minutes after step 5**, take **five consecutive readings per block**, each separately launched and logged. Record actual times; if a block takes longer than its five-minute slot, finish that block normally and stop the schedule as timing-inconclusive. The minimum 2.0-second wait applies before every new reading, including unchanged-patch repeats. At the end of the three blocks apply section 7's stability limits. If they fail, end the session; do not extend warm-up or loosen limits during the run.
8. **Owner:** once step 7 passes, display each of `RGB 255,255,255`, `51,51,51`, `26,26,26`, `13,13,13`, `5,5,5`, and `0,0,0` in that order, with the same geometry and surround. After each change, ensure the previously established menu exit remains complete, wait at least 2.0 seconds and take **five readings**. No menu or numerical control changes occur. The low-light sequence intentionally probes noise: a finite result that fails the predefined low-light reliability criterion is retained as diagnostic data, not silently dropped. Hardware/protocol errors or other stop events still end the session immediately.
9. **Owner:** return to `RGB 128,128,128`, wait at least 2.0 seconds and take **five final readings**. Compare with the final warm-up block using section 7. A failed end check makes the range assessment inconclusive, without erasing the initial access result.
10. **Owner and agent:** retain all attempts, including rejected ones. Record the passing code range and any failed/indistinguishable low-light patches, without extrapolating below the tested codes or adopting a black-level value. Do not adjust the TV in response to results.
11. **Owner:** complete normal restoration from section 3, record each restoration, and stop. There are at most **51 reading launches** (one initial, 15 warm-up, 30 range, five final). Do not add a repeat run, new correction or recovery sequence under this authorisation.

**Allowlisted measurement invocation, for steps 6–9 only:**

```text
spotread.exe -O -e -x -Y n <unique-local-attempt.log>
```

The path and logfile are resolved in the authorised local session, never by copying this placeholder. Put the logfile last, **not immediately after `-O`**, which has an optional spectrum filename. Use a fresh logfile per attempt under ignored `local/T-003/`; retain console output and exit status too. No shell script is supplied by this plan. `-e` selects emissive readings; `-x` requests Yxy display; uppercase `-Y n` forces non-refresh mode. The documented Spyder5 default uses generic non-refresh calibration. No external correction (`-X`) or unsupported no-calibration option (`-N`) is used.

`-O` can perform one calibration or measurement and exit; require an actual XYZ result. Do not answer an unexpected calibration prompt or send keys as an improvised workaround. If a launch has not returned within **60 seconds**, record a diagnostic timeout and stop scheduling work. Do not forcibly kill it or replug/restart the meter; its outstanding state requires a separate reviewed recovery procedure before any further project equipment operation. This is a workflow deadline, not a claim that terminating a driver is safe.

## 6. What will be recorded

All readings are **relative diagnostic evidence only**, permanently excluded from calibration data or absolute-accuracy claims. A header records the reviewed plan commit, authorisation text/date, operator, TV/receiver/OS/GPU/driver versions, Argyll version/executable hash, discovered instrument and active generic display type, renderer identity/hash, dimensions and source RGB encoding, viewing conditions, warm-up start and unchanged signal-path settings. Exact paths and device serial identifiers stay in ignored local records.

For each attempt record a unique ID; purpose (`initial-access`, `warmup-30`, `warmup-35`, `warmup-40`, `range`, `end-check`); start/end time; exit code or outstanding state; raw XYZ and Yxy; application RGB code/window/surround; input/mode/settings; correction filename **none** and correction hash **N/A**; generic calibration **not validated for this TV**; wait start/end; and acceptance/rejection reason. Keep all raw attempts before computing statistics. No removal of inconvenient values or median-only retention.

**D-013:** initial input/mode preparation and every normal-menu inspection are followed by owner manual exit, then at least 2.0 seconds before reading. Patch changes also receive that wait. Repeated readings do not require reopening menus; they require the preceding exit to remain complete and the wait to be observed. Failed/uncertain exit or an unexpected overlay stops the run. This plan does not test the program's Ex-Link exit method or detect overlays automatically.

Rejected protocol/output attempts remain in the record with reasons and stop the session. Finite low-light samples outside the numerical reliability envelope remain valid *noise-characterisation observations*, marked unusable for later feedback. Do not promote them into calibration evidence. Publish only privacy-checked result extracts and data under a future reviewed change to `docs/tests/T-003-data/`; raw logs remain ignored locally.

## 7. How results will be judged

These criteria are fixed **before** execution and need owner acceptance as part of authorising the plan. They are pragmatic proposed diagnostics, not Delta-E targets, model specifications or proof of correction validity.

For each five-reading block compute arithmetic mean and sample standard deviation (SD) of Y; coefficient of variation `CV = 100 × SD(Y) / mean(Y)` when the mean is positive; and the ranges `max(x)-min(x)` and `max(y)-min(y)`. Do not calculate chromaticity statistics for zero/non-positive XYZ sums.

| Check | Proposed interpretation |
|---|---|
| Access | Correct Spyder5 identified, and one command returns exactly one finite XYZ result plus a completed successful process. No result with a successful exit is **inconclusive**, not a pass. A discovery/driver error identifies a failed setup, not proof the meter can never work. |
| Mid-grey repeatability | Every warm-up block has positive mean Y, CV ≤1.0%, and both chromaticity ranges ≤0.002. A failure blocks use for the later relative-feedback experiment until investigated. |
| Warm-up drift | Means at 30→35 and 35→40 minutes each differ by ≤1.0% of the earlier mean; x and y block means each shift by ≤0.002. This establishes stability only over the observed window, not a universal warm-up time. |
| End stability | Final mid-grey mean Y differs from the 40-minute block by ≤1.0%; x/y means each differ by ≤0.002. Otherwise range evidence is inconclusive because the setup drifted. |
| Low-light usable range | For each nonzero application code require positive mean Y, CV ≤5.0%, x/y ranges ≤0.005, and increasing Y between adjacent tested codes separated by more than `3 × sqrt(SD_low² + SD_high²)`. Report the lowest tested nonzero code in a contiguous passing range upward; exclude any gap. These are observed relative limits of this setup. |
| Zero patch | Retain readings and variability, including zero or negative finite values. Never interpret repeated floor values as verified panel black. No assumed 0.38 cd/m² cutoff, borrowed TV black value or black-level acceptance target is imposed. |

If the low-light code is indistinguishable from the next code, that range fails the diagnostic criterion; do not infer a meter-only fault because the unvalidated video path and TV can also contribute. T-005 and T-004 remain separate. Numeric success cannot confirm the accuracy forecasts in C-043, the other-unit benchmark in C-072, or correction validity under Q-001.

**Stop immediately:** owner requests it; unexpected TV behaviour/menu/overlay; setup differs from this plan; instrument missing/ambiguous; unplanned prompt; driver/communication error; non-finite or missing output; timeout; mid-grey stability failure; disturbed meter mounting; uncertain menu exit; or any required step outside the authorisation. No automatic resend, repeat, recovery, driver change or USB replug. A finite noisy low-light result is handled by the predefined range criteria, not reclassified as a protocol fault.

**Stop rules adopted:** [docs/plan.md stop rules](../plan.md#stop-rules-for-every-physical-stage) at full commit `ba099e0a182713945c247636042286e6f9dca626`. The user can stop at any time. A later plan revision requires review and explicit authorisation for its changed scope.

## 8. Owner's authorisation

*To be completed by the owner only, or copied word for word from the owner's written authorisation. The current preparation request explicitly excludes hardware operation.*

- Authorised: **No — not requested or granted**
- Reviewed plan commit: not yet recorded
- Steps authorised: none
- Conditions or limits: not yet recorded
- Acceptance of proposed diagnostic thresholds and 2.0-second wait: not granted
- Acceptance of generic, uncorrected diagnostic readings: not granted
- Renderer revision/hash and launch/close procedure accepted for steps 5–11: not yet supplied
- Date: not authorised
- Verbatim authorisation: none

## 9. Results

**Not run.** Do not fill these fields with predicted output.

- Date carried out:
- Present:
- Differences from the plan:
- Observations:
- Attempt counts (accepted/rejected/outstanding/unrun):
- Data files:
- Original-state restoration:

## 10. Conclusions and ledger updates

**No equipment conclusions yet.** This document only makes T-003 a planned, unauthorised test. After authorised execution, a reviewed result update must distinguish device discovery, actual reading access, repeatability, drift and low-light limitations rather than marking the entire purpose confirmed from one reading.

C-002/C-041/C-056/C-068/X-011 may receive narrowly scoped observed evidence; failures may remain inconclusive. C-069 is not experimentally probed. C-043/C-072 receive only this unit's observed relative-range evidence, never transferred accuracy or black-level claims. C-082 remains an owner equipment description. Q-008/Q-014 recommendations may follow the observations; no owner answer, spectral validation or permission for T-005/T-006/T-013/T-008 follows automatically.
