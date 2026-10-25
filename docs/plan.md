# Proposed path to a first SDR calibration

> **Proposal by Claude Code (Anthropic), 25 October 2026. It is not a decision and authorises nothing.**
> Nothing here has been tested on the owner's equipment. Every physical step needs its own reviewed test plan and the owner's explicit authorisation ([AGENTS.md section 7](../AGENTS.md#7-equipment-safety-rule-6)). Where this page and the [ledger](../LEDGER.md) differ, the ledger and the owner's decisions win.

This page puts the work in order: what has to be known, tested or decided before the next step can start, and what would make each step stop.

## What stays fixed

- **TV control is Samsung Ex-Link only** (D-006). Whether it works on this TV is not known (C-005).
- **Hardware budget:** £25 in total; £15.99 spent; **£9.01 left**. No purchase is proposed here.
- **Menu guard:** a menu anywhere on the screen during a reading spoils that reading, and it is repeated once the menu has gone (D-008, D-010). The screen behind the meter, its cap and its cable may be ignored only if the webcam test T-010 shows that any menu covering it also shows somewhere the webcam can see at the same time (D-011, C-024). Until then, no reading is accepted.
- **No service menu.** No agent opens it, and no plan below uses it.

## Three kinds of meter reading

Some tests need the meter before the menu guard has been proven, and T-012 needs real readings to prove the guard. So readings are kept in three separate kinds, and only the last kind can ever be used to calibrate or to judge accuracy.

| Kind | Taken in | Used to calibrate or judge accuracy? |
|---|---|---|
| **Diagnostic reading** | Component tests T-003 to T-006: does the meter work, how repeatable is it, does a setting change show up? | **Never.** Labelled diagnostic and kept out of calibration data and accuracy reports. How the menu guard applies to these readings is for the owner to decide (Q-012). |
| **Guard-validation reading** | T-012: menus are shown on purpose to check that the guard throws readings away | **Never.** These readings exist to be rejected. |
| **Accepted calibration reading** | The integrated program, from T-013 onwards | **Yes**, but only if the webcam saw the whole screen clear for the whole reading (apart from the hidden area, if T-010 has confirmed C-024) and the reading's record is complete. |

A diagnostic or guard-validation reading can never be promoted to an accepted one later.

## The stages in order

Each stage starts only when the one before it has passed, unless it says otherwise.

### Stage 1 — Information only the owner can give

The owner looks things up and reports them. No meter, no Ex-Link connection, no service menu. The full list is in [equipment.md](equipment.md#what-we-still-need-from-you).

- **Passes when:** the model is confirmed and T-001 and T-002 are recorded in the ledger.
- **Stops if:** the model is not UE49KS7000UXXU (the research must be checked again), or no 3.5 mm Ex-Link socket can be found (the owner decides what happens next, Q-013, before any Ex-Link work).

### Stage 2 — Research and decisions (software only)

- Find model-specific Ex-Link evidence (Q-006, X-002), the cable's wiring and signal levels (C-021), what the Denon's Bypass setting does (C-044), the webcam's capabilities, and the available spectral corrections and their licences (Q-001, Q-002).
- The owner answers Q-010 (what counts as a menu), Q-012 (diagnostic readings), Q-014 (input, picture mode, room, brightness target, black level and success criteria) and Q-013 (what to do if Ex-Link fails).
- Write test plans for T-010, T-003, T-005 and T-006, and for any physical step in T-004. Each plan is reviewed by the other company's agent before the owner is asked to authorise it.
- **Passes when:** the plans are reviewed and the answers are recorded.

### Stage 3 — Software-only checks (can run alongside stages 1 and 2)

- T-009: Ex-Link message encoder and reply reader, with no route to real hardware.
- T-011: the menu guard, tested with made-up camera pictures and a fake meter.
- A simulated TV and meter, the record format for readings, and the design for sending Ex-Link commands: one command at a time, and **no automatic resend after an unclear result**, because an acknowledgement does not prove the setting changed (C-010) and a repeated step could be applied twice.
- **Passes when:** each suite is run by hand and its passed, failed and skipped counts are recorded. These are simulations: they never change an equipment test status.

### Stage 4 — T-010: what the webcam can see (needs authorisation)

The meter hangs in place but takes no reading. The owner opens the TV's normal menus with the remote; agents send nothing to the TV.

- **Passes when:** the webcam sees the whole screen; where and how menus appear is recorded; the area hidden by the meter, cap and cable is recorded; and C-024 is checked for the menus the plan lists.
- **Stops if:** the webcam cannot see the whole screen (move it and write a new plan), or a menu can hide entirely behind the meter, cap or cable. Then D-011 means no reading can be accepted, and the owner decides what to change.

### Stage 5 — Component tests T-003 to T-006 (each needs its own authorisation)

These take **diagnostic readings** only. They can run in any order once their own prerequisites are met.

| Test | Passes when | Stops if |
|---|---|---|
| T-003 meter | ArgyllCMS sees the Spyder5 and returns real numbers (not just a successful exit); repeatability, warm-up drift and the darkest usable patch are measured | No reading, a driver conflict, or readings that wander more than the plan allows |
| T-004 correction | A chosen correction file is accepted with the Spyder5, and its source, version and file fingerprint are recorded | The file is rejected. Without a reference instrument, the correction stays labelled **unvalidated** (Q-001) |
| T-005 signal path | Every setting between the pattern program and the TV is recorded; black and white levels are interpreted correctly; no channel clips inside the video range | Black is crushed or lifted, or clipping, without an explanation. Settings alone do not prove that exact colour values arrive; the plan must say what its method can and cannot prove |
| T-006 Ex-Link | The connection route and pin-out are confirmed first; then one harmless, allowlisted command is acknowledged, its effect is seen in the TV's normal menu, and the original value is restored | No reply, an unexpected reply, or anything that suggests the service menu is needed. Do not enter it: the owner decides (Q-013, X-002) |

### Stage 6 — T-012: the menu guard with the real meter (needs authorisation)

The owner opens menus on purpose, at different places and times, while the meter is reading. These are **guard-validation readings**.

- **Passes when:** the pass marks written in advance under Q-009 are met: every reading overlapped by a menu, an unclear camera picture or a timing gap is rejected, and no rejected reading reaches the data.
- **Stops if:** any reading overlapped by a menu is accepted. Fix it, re-run the software checks, then repeat T-012.

### Stage 7 — T-013: one reversible adjustment with measured feedback (needs authorisation)

The first time the program changes the TV and uses what it measures (C-031). One ordinary picture control, for example Backlight, chosen in the plan.

1. Write down the control's original value from the normal menu, then take repeated readings of one unchanging patch.
2. Change the control by one step through Ex-Link. Wait until the guard sees the screen clear, then measure again.
3. Work out a second change aimed at a nearby target, apply it, and check that the error got smaller by more than the meter's noise.
4. Restore the original value. Check it in the normal menu, outside any reading, and check that the readings return to where they started.

- **Passes when:** the change is measured, the second change improves the reading, and restoration is confirmed both ways.
- **Stops if:** a command's result is unclear (stop; no resend), the change cannot be told apart from noise, or restoration fails (the owner restores the recorded value by hand).

### Stage 8 — T-008: full SDR calibration (needs authorisation)

One input and picture mode, the targets chosen under Q-014, and accepted readings only.

- **Passes when:** a check in a separate session, using patches the program did not adjust to, shows improvement beyond the meter's repeatability. Results are reported both "as the meter reads it" and, separately, with the stated limits of the correction. The original settings can be restored, and the owner checks the calibrated mode with their usual playback sources.
- **Stops if:** any stop rule below applies, or the results do not improve on the starting point.

## Stop rules for every physical stage

- The owner can stop at any time.
- Stop at the first unexpected TV behaviour, unclear command result, menu that should not be there, or anything not in the authorised steps.
- Never enter the service menu, never send a command outside the plan's list, and never resend after an unclear result.
- Record what happened, including failures, before trying anything else.
