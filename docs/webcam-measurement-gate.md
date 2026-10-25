# Design proposal: webcam gate for patch measurements

**Proposal by Codex (OpenAI); not implemented or tested.** The requirement and working rules are [D-008 and D-009, widened to the whole screen by D-010, in the ledger](../LEDGER.md#3-decisions), inherited from merged PRs #6 and #7. The owner's original words and follow-up answers remain in [S-009](briefs/2026-10-24-webcam-menu-guard.md) and [S-010](briefs/2026-10-24-whole-screen-menu-guard.md). This document adds a design, not another record of the requirement. The proposed gate is C-017; its timing and end-to-end reliability remain unproven (C-018 and C-019).

## Relationship to D-008, D-009 and D-010

D-008, as widened by D-010, defines which observations must be excluded. D-009 defines the six working rules below, applied to the whole screen under D-010. No change to these decisions is proposed; the additions in this document need review as implementation choices. A menu anywhere on the TV screen matters even if it is outside the colour meter's patch. T-010 checks the whole-screen view and where and how menus appear; Q-008 retains only the pre-reading clear duration. What counts as a menu remains open under Q-010; this proposal does not settle that definition.

| D-009 item | How this proposal applies it | Added detail or difference |
|---|---|---|
| 1. Fail safe | Only a reliable Clear state permits a new reading; Menu visible and Unknown block or invalidate it. | Adds explicit states, timestamp/coverage checks, alignment checks and a prohibition on bypassing the gate during profiling. No relaxation of D-009. |
| 2. Whole reading window | Observe before and throughout acquisition; reject any affected reading and start a fresh one after recovery. | Adds conservative acquisition bounds, safe cancellation or draining, capture-time correlation, provisional results and rejection that cannot be reversed. The pre-reading duration remains Q-008. |
| 3. Seeing, not assuming | Use webcam observations to decide visibility. Sending no TV command is never evidence that the screen is clear. | Adds image-space alignment and detector validation. A patch change or TV adjustment resets settling as a precaution; it never proves Clear. |
| 4. Nothing silent | Log every blocked or discarded reading with its time and reason; prevent invalid readings entering any valid dataset. | Adds acquisition identifiers, provisional-result isolation and late-result handling so rejected results cannot be attributed to a retry. |
| 5. Privacy | Any retained pictures stay private in `local/`; committing a specific picture still needs the owner's approval. | Adds local processing with no routine image/video retention or upload by default. Live frames may be processed in memory; this narrows retention, not the approval rule. |
| 6. Equipment rule | Software-only work uses synthetic or recorded pictures; actual capture needs an authorised plan. | Adds T-011 for synthetic checks and T-012 for later integration validation after T-010. Neither test proposal authorises equipment use. |

## Intended measurement flow

Do not start a patch reading while a menu is visible anywhere on the TV screen. If one appears at any point during the reading, reject the entire reading: it must never enter the profile, calibration calculations, optimiser or exported valid measurements. After the menu disappears, take a completely new reading once the view is reliably clear and settled. An invalid reading cannot become valid again.

The webcam supplies the menu/visibility check. The intended colour measurements still come from the Spyder5. Webcam frames must continue to be examined while a menu is present so the program can know when it clears; those monitoring frames are not colour-meter patch readings.

## Proposed behaviour

Classify the monitored view as **Clear**, **Menu visible** or **Unknown**. Only Clear can permit a new reading. A missing, stale or unreliable camera view is Unknown, never assumed clear. Profiling must not proceed while this gate is disabled, unavailable or bypassed.

1. **Establish the view.** Locate the entire TV screen and confirm that all of it is reliably visible, as required by D-010 and assessed by T-010. Use TV-screen coordinates within the webcam image. A crop must not exclude any part of the TV screen; missing or obscured screen areas make the view Unknown. Camera setup remains Q-007; detection and timing acceptance criteria are Q-009.
2. **Wait before starting.** Require fresh, reliable Clear observations throughout a settling interval before starting the meter. A menu, unknown state, patch change or TV adjustment resets that interval. The settling duration remains Q-008; this proposal chooses no value.
3. **Monitor throughout acquisition.** Continue observation for the complete time over which the meter could be collecting light, using conservative timing bounds if exact integration times are unavailable. On a menu or unknown state, request a safe cancellation if supported. If cancellation is unavailable or cannot be confirmed, let the outstanding read finish and discard its result; do not start an overlapping retry. Rejection cannot undo light already collected, so no contaminated result may be used.
4. **Hold results provisionally.** A meter result must wait until the corresponding camera interval has been processed. Use frame capture/exposure times, with uncertainty bounds, rather than delivery time alone. A menu frame delivered late but captured during acquisition invalidates that reading. If timing or delivery bounds cannot be established, the result remains ineligible; reaching a deadline discards it rather than assuming success.
5. **Recover with a fresh read.** Give each acquisition its own identifier. Once rejected, associate any late meter result with that rejected acquisition and discard it. Wait for a new uninterrupted Clear settling interval, then begin a fresh acquisition for that patch. Lost screen alignment or an obstructed camera requires correction before resuming. Keep rejected readings out of valid datasets and optimisation. Log every blocked or discarded reading with its acquisition/attempt identifier, time and reason; record the affected interval and recovery separately without storing room imagery by default.

Camera disconnects, frozen/stale frames, unexplained frame gaps, out-of-order frames that cannot be accounted for, unbounded latency, loss of screen alignment, occlusion and uncertain classifications must block or invalidate readings. These are proposed failure conditions; reliable detection of them must itself be verified. A static patch alone must not be treated as proof of a frozen camera.

The user-facing status should explain the pause plainly, for example “Waiting for the TV menu to disappear” or “Webcam view unavailable — measurement paused.” Detecting a menu does not itself trigger a TV command or attempt to dismiss it. No service-menu action is part of this feature.

## Timing and detection limits

The owner's “at any point” requirement covers the full acquisition interval. A webcam samples frames; it cannot be assumed to observe an arbitrarily short event between exposures. A visually missed menu can also be wrongly classified as Clear. Synthetic tests cannot establish that neither problem occurs on the owner's setup.

Before claiming the feature meets the requirement, validate visibility of the whole TV screen, camera frame/exposure coverage, latency, clock alignment, minimum detectable event duration and false-negative behaviour against representative TV menus and patch conditions. Include menus across the top, middle, bottom, sides, edges and corners, including outside the meter's patch. Bright, dark or changing patches, translucent bars and partial bars must be included. Do not quietly reinterpret the requirement as “no menu in the occasional frames we checked.” An unvalidated or inadequate observation interval must not qualify a reading as valid. If the available webcam cannot support the required assurance, record that limitation and keep the capability unverified rather than claiming complete protection. The additional timing and detection limits and acceptance criteria remain Q-009; Q-008 retains only the pre-reading clear duration. This uncertainty adds a validation obligation to D-009, not an exception to D-008 as widened by D-010.

## Proposed software-only checks — T-011

**Planned; not executed.** Use synthetic frames/events, an in-memory fake meter and a fake clock. No camera, TV, colour meter, sockets or device enumeration is needed. Test both the classifier's handling of labelled synthetic images and the measurement gate's response to scripted classifications; passing the latter alone does not validate menu detection.

| Case | Required outcome |
|---|---|
| Menu visible before a reading at the top, middle, bottom, sides, edges or corners, including outside the patch | No meter-start request for any tested position. |
| Clear, valid coverage across settling and the complete acquisition interval | Result eligible only after the camera interval is processed; eligibility is labelled simulated. |
| Menu appears briefly midway through acquisition at any of the screen positions above and disappears before the result | Entire result rejected for every tested position; no profile, optimiser or valid-export update. |
| Menu touches the beginning or end of the acquisition interval | Treat overlap conservatively and reject; exercise timing uncertainty bounds too. |
| Menu frame captured during acquisition arrives after the meter result | Provisional result rejected before any consumer can use it. |
| Camera disconnects, timestamps stop advancing, or coverage contains an unexplained gap | Unknown state blocks/invalidates and pauses further readings. |
| TV/camera moves, a crop excludes any part of the screen, any screen area is obscured, or detector is uncertain | Unknown; block a new reading or invalidate an active reading. Include upper-screen, edge and corner coverage failures. |
| Menu clears but reappears during settling | Settling restarts; the rejected reading remains rejected. |
| Meter cannot cancel, or returns after cancellation | Finish/drain and discard; no overlap with retry and no attribution to a later reading. |
| Translucent/partial bars and bright/dark patches in synthetic labelled images | A menu label blocks measurement; uncertain cases are Unknown. Record misses explicitly, not as passing gate tests. |
| User attempts to disable the gate during profiling | Profiling cannot proceed with unguarded readings. |
| Timing/delivery bounds are unavailable, frames arrive out of order, or the provisional-result deadline expires | Unaccounted coverage remains Unknown; discard on the deadline, never accept by timeout. |
| A static patch produces identical images but timestamps and coverage remain valid | Do not diagnose a frozen camera solely from repeated image content. |
| A reading is blocked or discarded and recovery creates a new attempt | Log the time, reason and correct attempt identifier; retain no frame by default. |

Record the implementation revision, fixture provenance, clock assumptions, thresholds and actual passed/failed/skipped/unrun outcomes when these tests exist. No suite or detector has been implemented by this documentation change.

## Equipment, privacy and later validation

The owner already has a webcam (C-016). Its model, connection and placement remain Q-007; suitability remains untested (C-015 and C-019). No purchase is proposed and the hardware budget is unchanged. Process frames locally by default and do not retain or upload room images or video by default. If frames are deliberately retained for investigation, they stay in `local/` under D-009 item 5 and [AGENTS.md](../AGENTS.md#11-privacy-and-credentials). The owner must check and approve each specific picture before it is committed. No agent turns the webcam on or captures pictures outside an authorised test plan (D-009 item 6).

Main's T-010 remains the candidate physical test for a reliable whole-screen camera view and where and how menus appear under D-010. Actual detector performance and meter-timing integration need a later, explicitly authorised equipment-validation plan (T-012), building on those findings. T-012 would assess capture timing, latency and clock bounds; the representative menu/patch conditions and whole-screen positions above; and blocking, discard and fresh-read recovery across real acquisition windows. Its steps and acceptance criteria must be written and reviewed before authorisation; none is written or authorised here. Software-only T-011 can proceed without it, but cannot confirm C-018 or C-019. A future full calibration plan under T-008 must also satisfy D-008 and D-009 as widened by D-010 and account for the applicable webcam checks; this proposal does not authorise that test.
