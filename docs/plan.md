# Proposed path to a first SDR calibration

> **Proposal by Claude Code (Anthropic), reconciled by Codex (OpenAI), 25 October 2026. It is not a decision and authorises nothing (C-061).**
> Nothing here has been tested on the owner's equipment. Every physical step needs its own reviewed test plan and the owner's explicit authorisation ([AGENTS.md section 7](../AGENTS.md#7-equipment-safety-rule-6)). Where this page and the [ledger](../LEDGER.md) differ, the ledger and the owner's decisions win.

This page puts the work in order: what has to be known, tested or decided before the next step can start, and what would make each step stop.

## What stays fixed

- **TV control is Samsung Ex-Link only** (D-006). Whether it works on this TV is not known (C-005).
- **Hardware budget:** £25 in total; £15.99 spent; **£9.01 left**. No purchase is proposed here.
- **Measurement cycle (D-013):** after every TV setting change, the program exits the TV's menu and waits a short delay before taking any reading: change, exit, wait, read. Q-008 leaves the delay undecided; the way the program exits the menu over Ex-Link also needs a reviewed design. This page selects neither.
- **No service menu.** No agent opens it, and no plan below uses it.

## Measurement cycle and use of readings

Every reading follows D-013, including diagnostic readings, the first baseline, the readings after a calculated change, and the readings after restoration. Each test plan must specify how D-013 applies to every step that changes a TV setting. A menu-value inspection is followed by menu exit and the planned delay before the next reading too. A repeated reading without another setting change still requires the preceding exit and delay to have been completed; sending a command alone does not establish that the exit worked.

Record each reading's purpose and its acceptance criteria before taking it. Component-test readings are diagnostic evidence, kept out of calibration data and accuracy claims; they cannot be promoted later. T-013 tests a limited feedback response and restoration, not absolute calibration accuracy. T-008 uses only readings meeting its reviewed plan's criteria. Applying D-013 does not establish correction validity or measurement accuracy (Q-001, T-004).

**Known limitation:** exiting the menu and waiting does not detect an unexpected TV notification or other overlay during a reading. A reading could be affected without the program knowing. This is D-013's recorded risk, not a proposal for detection or extra equipment.

## The stages in order

Each stage starts only when the one before it has passed, unless it says otherwise. These are proposed criteria for future plans, not a record that any stage has passed.

### Stage 1 — Information only the owner can give

The owner looks things up and reports them. No meter, no Ex-Link connection, no service menu. The full list is in [equipment.md](equipment.md#what-we-still-need-from-you).

- **Passes when:** the model is confirmed and T-001 and T-002 are recorded in the ledger.
- **Stops if:** the model is not UE49KS7000UXXU (the research must be checked again), or no 3.5 mm Ex-Link socket can be found (the owner decides what happens next, Q-013, before any Ex-Link work).

### Stage 2 — Research and decisions (software only)

- Find model-specific Ex-Link evidence (Q-006, X-002), the cable's wiring and signal levels (C-021), what the Denon's Bypass setting does (C-044), and the available spectral corrections and their licences (Q-001, Q-002).
- Record Q-013's fallback decision. For Q-014, agree only a **provisional** input, picture mode, room, brightness/black assumptions and criteria sufficient to write the component-test plans. The **final** answer follows T-003's evidence and must be recorded before T-008; Stage 2 does not require it.
- Agree what correction validation means under Q-001 before planning T-004. If no practical validation route is found, ask Q-016; do not assume permission to proceed with an unvalidated correction.
- Write test plans for T-003, T-005 and T-006, and for any physical step in T-004. State each plan's own prerequisites, proposed Q-008 delay, menu-exit method, permitted commands and restoration procedure. Each plan is reviewed by the other company's agent before the owner is asked to authorise it.
- **Passes when:** those plans are reviewed and their prerequisite answers and provisional targets are recorded.
- **Stops if:** a prerequisite or necessary authorisation is missing. Software-only research can continue while a physical step is blocked.

### Stage 3 — Software-only checks (can run alongside stages 1 and 2)

- T-009: Ex-Link message encoder and reply reader, with no route to real hardware.
- A simulated TV and meter, the record format for readings, and the design for sending Ex-Link commands: one command at a time, and **no automatic resend after an unclear result**, because an acknowledgement does not prove the setting changed (C-010) and a repeated step could be applied twice.
- Exercise change, exit, wait, read with simulated settings, menus and time, including baseline preparation, menu inspections and restoration. A failed or uncertain exit must not silently permit a reading. These software checks cannot prove real TV behaviour or detect unexpected overlays.
- **Passes when:** each applicable suite is implemented and run by hand and its passed, failed, skipped and unrun counts are recorded. These are simulations: they never change an equipment test status.

### Stage 4 — Component tests T-003 to T-006 (each physical step needs its own authorisation)

These take **diagnostic readings** only, following D-013. They can run in any order once their own prerequisites are met; diagnostic results do not authorise subsequent stages.

| Test | Passes when | Stops if |
|---|---|---|
| T-003 meter | ArgyllCMS sees the Spyder5 and returns real numbers (not just a successful exit); repeatability, warm-up drift and the darkest usable patch are measured | No reading, a driver conflict, or readings that wander more than the plan allows |
| T-004 correction | The agreed Q-001 validation requirements are met and the correction's source, version and file fingerprint are recorded; merely accepting the file does not validate it | The file is rejected or validation remains unavailable. Record the limitation and wait for the owner's Q-016 decision; do not continue to feedback or calibration by assuming unvalidated use is acceptable |
| T-005 signal path | Every setting between the pattern program and the TV is recorded; black and white levels are interpreted correctly; no channel clips inside the video range | Black is crushed or lifted, or clipping, without an explanation. Settings alone do not prove that exact colour values arrive; the plan must say what its method can and cannot prove |
| T-006 Ex-Link | The connection route and pin-out are confirmed first; then one ordinary, reversible, allowlisted command is acknowledged, its effect is seen in the TV's normal menu, and the original value is restored; the planned exit method is established before readings rely on it | No reply, an unexpected reply, uncertain exit/restoration, or anything that suggests the service menu is needed. Do not enter it: the owner decides (Q-013, X-002) |

After T-003, the owner can finalise Q-014 using T-001/T-002 and the measured usable range. If black cannot be measured, any selected assumption stays labelled as assumed. Q-014 remains open until the owner answers; no target is chosen here. A Q-016 answer alone does not change the existing validated-correction requirement: any proposed exception needs a reviewed change and a separately authorised plan before dependent tests proceed.

### Stage 5 — T-013: one reversible adjustment with measured feedback (needs authorisation)

The first time the program changes the TV and uses what it measures (C-031). One ordinary picture control, for example Backlight, chosen in the plan. **No plan yet; not authorised.**

**Prerequisites:** satisfactory T-001 to T-006 evidence, implemented and passing applicable T-009 software checks, and a reviewed, explicitly authorised T-013 plan. The plan must establish the permitted control/range, original value and restoration, the menu-exit method and proposed Q-008 delay, a nearby provisional target, and a repeatability threshold. Q-001/T-004's validation requirement still applies; Q-016 offers no automatic exception. A final Q-014 answer is required for T-008, not as a circular prerequisite to T-003.

The future plan would specify these steps:

1. Write down the control's original value from the normal menu, exit the menu and wait the planned delay, then take repeated readings of one unchanging patch.
2. Change the control by one step through Ex-Link, exit the menu, wait the planned delay, then measure again.
3. Work out a second change aimed at a nearby target, apply it, exit the menu, wait the planned delay, and check that the error got smaller by more than the meter's noise.
4. Restore the original value through the planned procedure. Check it in the normal menu outside any reading, exit the menu and wait the planned delay, then check that the readings return to where they started within the plan's tolerance.

- **Passes when:** the change is measured, the second change improves the reading, and restoration is confirmed both ways.
- **Stops if:** a command's result is unclear (stop; no resend), the change cannot be told apart from noise, or restoration fails. Stop and record the failure; any owner recovery follows only a separately reviewed and explicitly authorised procedure after the TV's state is established.

### Stage 6 — T-008: full SDR calibration (needs authorisation)

One input and picture mode, the **final** targets chosen under Q-014 after T-003, and accepted readings only. Requires satisfactory T-001 to T-006 and T-013 evidence and implemented, passing applicable T-009 software checks. Every reading follows D-013; unmet prerequisites block full calibration. No plan yet; not authorised.

- **Passes when:** a check in a separate session, using patches the program did not adjust to, shows improvement beyond the meter's repeatability. Results are reported both "as the meter reads it" and, separately, with the stated limits of the correction. The original settings can be restored, and the owner checks the calibrated mode with their usual playback sources.
- **Stops if:** any stop rule below applies, or the results do not improve on the starting point.

## Stop rules for every physical stage

- The owner can stop at any time.
- Stop at the first unexpected TV behaviour, unclear command result, menu that should not be there, or anything not in the authorised steps.
- Never enter the service menu or send a command outside the plan's list. In these proposed initial tests, stop after an unclear result and do not resend the command. This test restriction leaves the future transport policy in X-007 open; it is not a decision on retries in the finished program.
- Record what happened, including failures, before trying anything else. Recovery requires established TV state and a separately reviewed and explicitly authorised procedure; no automatic recovery action is authorised here.
