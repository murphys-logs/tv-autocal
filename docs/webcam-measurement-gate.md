# Webcam gate for patch measurements

**Required in the final program; not implemented or tested.** Owner requirement D-008 comes from [S-009](briefs/2026-10-24-webcam-measurement-gate.md). The implementation details below are a proposal by Codex (OpenAI), recorded as C-016. Detection reliability remains unproven (C-017).

## Required outcome

The program must use a webcam observing the TV to prevent patch measurements while **any menu bar is visible in the lower portion of the TV screen**. This applies even when the bar does not overlap the colour meter's patch. A check only at the start or end of a reading does not satisfy the owner's requirement.

Do not start a patch reading while a menu bar is visible. If one appears at any point during the reading, reject the entire reading: it must never enter the profile, calibration calculations, optimiser or exported valid measurements. After the menu disappears, take a completely new reading once the view is reliably clear and settled. An invalid reading cannot become valid again.

The webcam supplies the menu/visibility check. The intended colour measurements still come from the Spyder5. Webcam frames must continue to be examined while a menu is present so the program can know when it clears; those monitoring frames are not colour-meter patch readings.

## Proposed behaviour

Classify the monitored view as **Clear**, **Menu visible** or **Unknown**. Only Clear can permit a new reading. A missing, stale or unreliable camera view is Unknown, never assumed clear. Profiling must not proceed while this gate is disabled, unavailable or bypassed.

1. **Establish the view.** Locate the TV screen and cover its entire lower portion where a menu bar could appear. Use TV-screen coordinates, not merely the bottom of the webcam image. A crop must not exclude the relevant area. The precise region, camera setup and detection thresholds need validation (Q-007).
2. **Wait before starting.** Require fresh, reliable Clear observations throughout a settling interval before starting the meter. A menu, unknown state, patch change or TV adjustment resets that interval. The settling duration is not chosen or validated yet.
3. **Monitor throughout acquisition.** Continue observation for the complete time over which the meter could be collecting light, using conservative timing bounds if exact integration times are unavailable. On a menu or unknown state, request a safe cancellation if supported. If cancellation is unavailable or cannot be confirmed, let the outstanding read finish and discard its result; do not start an overlapping retry. Rejection cannot undo light already collected, so no contaminated result may be used.
4. **Hold results provisionally.** A meter result must wait until the corresponding camera interval has been processed. Use frame capture/exposure times, with uncertainty bounds, rather than delivery time alone. A menu frame delivered late but captured during acquisition invalidates that reading. If timing or delivery bounds cannot be established, the result remains ineligible; reaching a deadline discards it rather than assuming success.
5. **Recover with a fresh read.** Once rejected, associate any late meter result with the rejected acquisition and discard it. Wait for a new uninterrupted Clear settling interval, then begin a fresh acquisition for that patch. Lost screen alignment or an obstructed camera requires correction before resuming. Keep rejected readings out of valid datasets and optimisation; log the reason and timing separately.

Camera disconnects, frozen/stale frames, unexplained frame gaps, out-of-order frames that cannot be accounted for, unbounded latency, loss of screen alignment, occlusion and uncertain classifications must block or invalidate readings. These are proposed failure conditions; reliable detection of them must itself be verified. A static patch alone must not be treated as proof of a frozen camera.

The user-facing status should explain the pause plainly, for example “Waiting for the TV menu to disappear” or “Webcam view unavailable — measurement paused.” Detecting a menu does not itself trigger a TV command or attempt to dismiss it. No service-menu action is part of this feature.

## Timing and detection limits

The owner's “at any point” requirement covers the full acquisition interval. A webcam samples frames; it cannot be assumed to observe an arbitrarily short event between exposures. A visually missed menu can also be wrongly classified as Clear. Synthetic tests cannot establish that neither problem occurs on the owner's setup.

Before claiming the feature meets the requirement, validate the monitored region, camera frame/exposure coverage, latency, clock alignment, minimum detectable event duration and false-negative behaviour against representative TV menus and patch conditions. Bright, dark or changing patches, translucent bars and partial bars must be included. Do not quietly reinterpret the requirement as “no menu in the occasional frames we checked.” An unvalidated or inadequate observation interval must not qualify a reading as valid. If the available webcam cannot support the required assurance, record that limitation and keep the capability unverified rather than claiming complete protection. The concrete limits and acceptance criteria remain Q-007.

## Proposed software-only checks — T-010

**Planned; not executed.** Use synthetic frames/events, an in-memory fake meter and a fake clock. No camera, TV, colour meter, sockets or device enumeration is needed. Test both the classifier's handling of labelled synthetic images and the measurement gate's response to scripted classifications; passing the latter alone does not validate menu detection.

| Case | Required outcome |
|---|---|
| Menu visible before a reading, including a bar outside the patch | No meter-start request. |
| Clear, valid coverage across settling and the complete acquisition interval | Result eligible only after the camera interval is processed; eligibility is labelled simulated. |
| Menu appears briefly in the middle and disappears before the result | Entire result rejected; no profile, optimiser or valid-export update. |
| Menu touches the beginning or end of the acquisition interval | Treat overlap conservatively and reject; exercise timing uncertainty bounds too. |
| Menu frame captured during acquisition arrives after the meter result | Provisional result rejected before any consumer can use it. |
| Camera disconnects, timestamps stop advancing, or coverage contains an unexplained gap | Unknown state blocks/invalidates and pauses further readings. |
| TV/camera moves, lower region is obscured, or detector is uncertain | Unknown; no accepted reading. |
| Menu clears but reappears during settling | Settling restarts; the rejected reading remains rejected. |
| Meter cannot cancel, or returns after cancellation | Finish/drain and discard; no overlap with retry and no attribution to a later reading. |
| Translucent/partial bars and bright/dark patches in synthetic labelled images | A menu label blocks measurement; uncertain cases are Unknown. Record misses explicitly, not as passing gate tests. |
| User attempts to disable the gate during profiling | Profiling cannot proceed with unguarded readings. |

Record the implementation revision, fixture provenance, clock assumptions, thresholds and actual passed/failed/skipped/unrun outcomes when these tests exist. No suite or detector has been implemented by this documentation change.

## Equipment, privacy and later validation

The owner plans to supply a webcam (C-015); its model, availability, frame rate, placement and suitability are unknown. No purchase is proposed and the hardware budget is unchanged. Process frames locally by default and do not retain or upload room video by default. Any future sample images supplied for investigation must be handled as private local data under AGENTS.md.

Actual webcam/detector performance and meter-timing integration need a later, explicitly authorised equipment-validation plan (T-011). None is written or authorised here. Software-only work can proceed without it, but it cannot confirm C-017 or complete physical calibration test T-008.
