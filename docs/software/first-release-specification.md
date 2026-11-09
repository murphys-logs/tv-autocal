# First functioning release: specification and acceptance

**Review proposal by Codex (OpenAI), 9 November 2026. The application is not yet functioning on the owner's equipment. No equipment test or release is authorised by this document.**

This is the proposed acceptance contract for the first complete application, not a claim that it exists. Existing owner decisions remain binding; new requirements and design choices below require review. An unresolved owner question stays unresolved even if this specification is merged. Sources and equipment status remain separate in [LEDGER.md](../../LEDGER.md), including S-101/C-137 for this proposal.

## What the owner will be able to do

Install a free, open-source Windows Python application; record the original setup; measure the TV; let the application make bounded changes to supported ordinary picture controls through Samsung Ex-Link; independently check the result; save an understandable report; and restore the recorded settings through an established procedure.

The intended result is an SDR picture assessed against **Rec.709** (the video colour standard), **D65** (the reference white colour) and **BT.1886** (the brightness curve from black to white). The application must distinguish a validated result from an unsuccessful, incomplete or uncertain run. A lower error reported by the same unvalidated meter is not sufficient to call the release functioning against this specification. No numerical accuracy promise is made here.

Initial scope is the owner's **Samsung UE49KS7000UXXU**, reported firmware **T-JZMDEUC-1270.1**, **Spyder5Pro**, Windows PC and recorded route **PC HDMI → Denon AVC-X3800H PC input → Monitor 1 → TV HDMI 4**. Movie mode, a dim room and **140–160 cd/m²** peak white are owner preferences recorded provisionally under Q-014, not final acceptance limits or measured output. The [equipment record](../equipment.md) holds the full dated setup; it must be reconfirmed for an actual session.

The fixed boundaries are D-001/D-003/D-006/D-013/D-018: Windows, Python, free/open-source dependencies, validated meter correction, TV-side adjustment, **Ex-Link as the only software TV-control route**, and **change → exit → wait → read**. Additional hardware remains capped at **£25 total: £15.99 spent, £9.01 remaining**. No purchase is proposed. HDR, service-menu work, network control, commercial calibration packages and general support for other TVs/meters are outside this release.

## Baseline and what counts as a release

The baseline was checked against live GitHub and fetched `main` at **`1de40a5c5a9e6bdb8c5f682968d4f6c5281629a9`**, on 9 November 2026. PRs #38 and #39 are merged; no open PR was returned by the live check. Existing branches and local work were inspected; the clean `codex/first-release-specification` branch was fast-forwarded from its older main baseline without discarding work. No existing release-specification document owned this topic. Later changes to main must be checked again before implementation.

The [ground-up audit](../reviews/2026-11-08-ground-up-audit.md), its [review responses](../reviews/2026-11-08-pr39-review-response.md), [second response](../reviews/2026-11-08-pr39-second-review-response.md) and [third response](../reviews/2026-11-08-pr39-third-review-response.md) are the current findings, not hardware validation. The audit's historical software test results are not fresh tests for this documentation change. Merging the audit did not repair the defects or remove equipment gates.

| Milestone | What it can establish | What it cannot establish |
|---|---|---|
| Current diagnostics: T-003 discovery and later component tools | Recognition/configuration information and, after their separate gates, bounded measurement, signal-path or ordinary-control observations | An integrated calibration application, correction validity or a calibrated TV |
| T-013 one-control feedback experiment | A reversible control response and a second change toward a nearby target, beyond measured noise, with restoration | Full greyscale/colour calibration or validated absolute accuracy; its readings stay diagnostic |
| First functioning release, demonstrated by a future T-008 plan | The complete owner journey and all essential requirements below, with independent verification against agreed targets and uncertainty | HDR, universal TV support, guaranteed recovery or accuracy beyond the evidence |

T-001/T-002 owner checks are recorded. No operational project equipment test has passed. T-003/T-005/T-006 remain unauthorised; T-004/T-013/T-008 have no complete authorised plan. These are dependencies, not instructions to execute them.

## Owner journey

1. **Install and prepare.** Follow reviewed Windows instructions, identify the approved application/Python/Argyll versions and meter configuration, and start in simulation. The application explains missing prerequisites and the proposed session. The owner deliberately enables only the reviewed, authorised real session, with the owner present.
2. **Save the starting point.** Reconfirm the TV, firmware, source, picture mode, signal path, display arrangement and room conditions. Record every setting the session could affect, including shared inputs/modes and temporary PC/receiver settings. Unknown values are marked unknown and block dependent changes. The old checklist is not a current backup.
3. **Confirm measurement readiness.** Establish usable meter access, correction identity and validation, stable presentation, range interpretation, warm-up/drift and usable light range. Keep instructions and controls off the measurement area. Record the agreed targets, limits, timing and restoration procedure before adjustment starts.
4. **Measure a baseline.** Use only eligible calibration readings under the final plan. Record the purpose and patch for every reading. Exit menus and wait before reading; a repeated reading still needs the applicable completed exit and a fresh wait. Generic diagnostic readings cannot be promoted into calibration evidence later.
5. **Adjust and measure.** The session controller asks the adjustment engine for a bounded next step, checks it against the permitted controls and remaining budget of attempts, sends it through Ex-Link, exits the menu, waits, then measures. Acknowledgement, setting confirmation and changed light are separate observations. Stop if the evidence is unclear or a limit is reached.
6. **Verify separately.** Fix the settings and use a separate session and patches not used to choose adjustments. Check drift, greyscale, the brightness curve and colours against the agreed acceptance rules and correction/reference evidence. A failed verification is reported as failed or inconclusive, even if the adjustment loop reported success.
7. **Report and choose.** Show before/after results, uncertainties, rejected readings, settings changed and verification/restoration status. The owner can retain the verified settings or request the planned restoration. A report never converts a missing check into a pass.
8. **Restore and close.** In a known state, use the established restoration procedure and verify stored settings and light output where the plan requires it, including affected inputs/modes. After an uncertain outcome, stop further adjustment and follow the separately reviewed owner-led procedure. Do not promise that software can automatically recover the TV, a stuck meter process or an unknown setting.

## Responsibilities and present implementation

These responsibilities are a proposed division for the release. The linked designs describe smaller existing components; their historical statements about missing later components do not override this baseline.

| Part | Responsibility in the release | Exists now | Still needed / evidence gate |
|---|---|---|---|
| Pattern generator | Show the requested colour on the intended TV; identify and hold the patch during a reading | Literal RGB8 buffers, manifests, off-screen checks and a manually operated Windows presenter; [renderer](renderer-cycle.md), [component tools](component-tools.md), [readiness](component-readiness.md) | Integrated sequencing; native geometry/focus/closure evidence and validated signal interpretation. A buffer hash proves buffer identity, not light or HDMI codes |
| ArgyllCMS measurement adapter | Start the selected meter operation, retain output/errors, identify valid results and supervise its lifetime | Strict transcript parser and a one-child-invocation wrapper; [meter-policy amendment](meter-error-policy.md) adds first-error give-up and source-model tests | C-136 review/native prerequisites, predictable stopping evidence, real meter results and coexistence with serial. One child launch is not one instrument attempt; supervision may remain outstanding indefinitely |
| Meter correction | Apply the identified correction for the display's light spectrum; retain its source, fingerprint, settings, validation and uncertainty | Argyll support researched; diagnostic configuration controls exist | No validated correction selected. File acceptance or repeatability is not accuracy; Q-001/T-004/Q-016 remain open |
| Ex-Link controller | Send only validated ordinary commands, one outstanding command at a time; preserve replies, uncertainties and observed effects | Pure encoder/parser, command audit and manual serial component tool; [T-009](t009-prototype.md), integration, component tools | Electrical compatibility, exact-firmware controls/encodings/scope/restoration, [serial input repair](serial-console-input.md) native validation/review, production transport review. Candidate Contrast/EXIT bytes are not validated calibration controls |
| Session controller | Own setup, baseline, patch/read identity, the required cycle, limits, stopping, records, verification and restoration state | Toy cycle, offline one-attempt composition, separate journals and component controls | Integrated production controller and owner interface. The physical system cannot inspect the simulator's hidden TV state; no combined meter/serial mode exists |
| Adjustment engine | Compare accepted readings with targets and choose limited, justified TV adjustments | Scripted toy readings and cycle checks; no production optimiser | Response evidence, coupled-control strategy, uncertainty-aware limits, convergence checks and independent verification. Algorithm and tuning choices require review |

## Essential requirements

Identifiers `FR-001`–`FR-020` are stable: keep them when wording changes, and retire rather than reuse them. All are essential to acceptance. **SW** means a software-only check using inert inputs/fakes or an installation that does not contact equipment. **EQ** means evidence from a separately reviewed, owner-authorised equipment plan. Neither substitutes for the other.

A **fixture** or **fake** is an artificial test input or substitute, not a real measurement. An **ACK** is a device acknowledgement, not confirmation of the stored setting. Further terms are explained in the [workflow glossary](../workflow.md#calibration-words).

Status terms below describe this baseline: **partial** means relevant components exist, **not built** means the release behaviour is missing, and **blocked** means evidence or an owner decision is also needed. None means accepted. Detailed numerical limits belong in a later reviewed acceptance plan, agreed before the decisive run.

### FR-001 — Setup, identity and deliberate real operation

- **Behaviour:** Explain the supported setup in plain English, default to simulation, require deliberate selection of the approved real session, and prevent work whose prerequisites or authority are missing. Record versions, configuration and current equipment identity without silently reusing dated observations.
- **Check:** SW: fresh start, missing/mismatched setup, absent permission and wrong mode fail closed; simulation cannot reach hardware. EQ: owner confirms the exact approved setup and understandable start/stop procedure before operation.
- **Dependencies/status:** Partial component opt-ins; integrated setup not built. D-001/D-002, Q-003/Q-019 and current [execution requirements](../tests/component-execution.md) apply. Typed attestations alone do not authenticate authority.
- **Not accepted if:** installation/startup operates equipment, an unapproved mode/control is reachable, or missing facts are filled with guesses.

### FR-002 — Original settings and affected scope

- **Behaviour:** Save an owner-readable, private original-setting record before any change, including input/mode scope, all affected controls and any temporary Windows/GPU/Denon configuration. Record how each value was obtained. Do not assume automatic readback.
- **Check:** SW: incomplete/stale originals and an unknown affected scope block setters; original records survive later updates. EQ: establish which inputs/modes change and verify the backup against normal menus and the approved procedure.
- **Dependencies/status:** Not built; blocked by Q-006, X-005/X-012 and T-006. Owner-reported All Sources and old values in C-077/C-078 are not a tested restoration map; 10-point values/ranges remain incomplete.
- **Not accepted if:** only the active input is backed up despite wider effects, settings are overwritten in the backup, or default values stand in for observed originals.

### FR-003 — Controlled patch presentation

- **Behaviour:** Present and hold the identified patch on the selected display, preserve D-018's centred **960×540 patch on 3840×2160 (6.25%)**, and keep operator controls usable without obscuring it. A patch change invalidates the previous reading association.
- **Check:** SW: literal pixel/geometry checks, wrong target, stale receipt, lost hold, closure and sequencing failures. EQ: native scaling, geometry, focus, visibility and closure checks in T-003/T-005 and the display procedure.
- **Dependencies/status:** Partial renderer/presenter; native behaviour untested. Q-019, T-014/T-016/T-018 and T-005 apply. Production integration remains missing.
- **Not accepted if:** a generated buffer or journal is treated as proof of display, the wrong patch/display is measured, or scaling/occlusion remains unexplained. D-013 does not provide automatic unexpected-overlay detection.

### FR-004 — Signal range and display behaviour

- **Behaviour:** Record and justify the interpretation of application RGB values through Windows, GPU, HDMI, Denon and TV. Establish correct black/white interpretation, no unexplained clipping and appropriate stable SDR behaviour for the approved path.
- **Check:** SW: explicit conversion assumptions and independent literal mapping examples. EQ: T-005 screening plus an additional reviewed method capable of resolving the range interpretation that screening alone cannot establish; document each method's limits.
- **Dependencies/status:** Blocked. C-080/C-081 record Limited output and receiver Auto/overlays as dated observations; C-088, X-008 and the [Stage 4 qualification](../plan.md#stage-4--component-tests-t-003-to-t-006-each-physical-step-needs-its-own-authorisation) remain unresolved.
- **Not accepted if:** monotonic unclipped readings, Bypass, a hash or reported settings alone are called proof of correct range or bit-exact transport. No Full/Limited recipe is chosen here.

### FR-005 — Valid meter attempts and error handling

- **Behaviour:** Associate every result with its exact patch, purpose, executable/options, correction and attempt; retain raw output and rejection reasons. Reject incomplete, malformed, duplicate, non-finite, wrong-format, late or failed results. Production validity also requires physically meaningful values and uncertainty checks, not merely finite numbers. Expose error prompts/retries and outstanding processes.
- **Check:** SW: realistic versioned success, misread, communications-error, prompt/retry, cancellation, late output, full storage and stuck-child cases; verify no failed attempt becomes accepted. EQ: approved installed-meter lifecycle and error/stop observations only where safely planned.
- **Dependencies/status:** The [meter-policy implementation](meter-error-policy.md) supplies an explicit first-error give-up response and strict complete-output acceptance, with source-model regressions. **C-136/A-007 physical hold remains** pending independent amendment review, installed-binary/input/cleanup evidence and abnormal-stop procedure; T-003 steps 5–11/T-005 Part M remain unauthorised. Low-level retry/shutdown bounds remain unavailable; direct discovery has separate gates.
- **Not accepted if:** `-O` or one process launch is assumed to bound instrument attempts, parser success implies accurate light measurement, or timeout is reported as proof that the child stopped. No forced kill/restart guarantee is adopted.

### FR-006 — Repeatability, drift and low-light usability

- **Behaviour:** Establish how consistently this meter measures this setup, how readings change over time, and the darkest useful range. Use these limits to reject unreliable adjustment/verification data and detect drift.
- **Check:** SW: noisy/drifting/near-floor fixtures cause the agreed rejections and stops. EQ: T-003 repeated readings, warm-up/drift and low-light observations with recorded configuration and an agreed analysis; later sessions check continuing applicability.
- **Dependencies/status:** Blocked by safe presentation, FR-005 and T-003; no operational readings exist. Initial T-003 relative checks may use a fixed, recorded but unvalidated path under that plan's own gates; full FR-004 acceptance is needed before using the evidence for release calibration. Q-014 follows the relevant measurement evidence.
- **Not accepted if:** another meter/TV benchmark supplies this meter's floor, a precise repeatability number is invented, or stable readings are labelled accurate without independent validation.

### FR-007 — Validated correction and accuracy basis

- **Behaviour:** Identify the correction's source, licence, file fingerprint and application settings; justify its applicability and uncertainty for this meter/TV. Explain separately what the meter reports and what the independent validation supports.
- **Check:** SW: absent, changed, mismatched or unvalidated correction cannot satisfy calibration acceptance. EQ: T-004's future Q-001-agreed reference/validation method and recorded results, with limitations independently assessed.
- **Dependencies/status:** Blocked: Q-001/T-004/Q-016, C-070/C-130 and X-006/X-017. No established validation route within the recorded constraints; that is not proof of impossibility.
- **Not accepted if:** a borrowed correction, accepted file, repeatable result or lower reported error alone is called validated accuracy. If validation cannot be obtained, Q-016 requires an explicit reviewed scope decision; an unvalidated alternative does not silently pass this specification.

### FR-008 — Electrical and exact-TV control compatibility

- **Behaviour:** Permit the Ex-Link connection and commands only after applicable wiring/electrical evidence and the authorised exact-TV test establish the route. Stop without substituting another route if it is unsupported.
- **Check:** SW: absent compatibility evidence blocks physical enablement. EQ: T-006 electrical gate before connection, then only the separately authorised ordinary command/exit/restoration steps on the recorded firmware.
- **Dependencies/status:** Blocked by T-006, Q-006, C-064/C-074/C-076 and X-002/X-010. A socket, cable label and PC COM-port appearance are insufficient. Q-013 can remain open while testing the approved route; failure returns the fallback question to the owner, without adopting one.
- **Not accepted if:** electrical levels are assumed from the chip/marketing name, a generic worksheet is treated as exact-TV proof, or network/service-menu fallback is used.

### FR-009 — Supported controls and command meaning

- **Behaviour:** Publish a closed list of supported ordinary controls, with encodings, legal ranges/steps, interactions, input/mode effects, confirmation method and restoration evidence. Enable only what is established for this firmware and sufficient for the accepted SDR targets; explain unsupported controls.
- **Check:** SW: boundaries, signed encodings, disallowed commands, partial/late/duplicate replies and no service commands. EQ: reviewed per-control effect/scope/restoration checks beyond the narrow T-006 candidate test, including menu exit. An ACK is not stored-value readback or optical proof.
- **Dependencies/status:** Partial protocol/audit tools; production control set blocked by FR-002/FR-008, Q-006, X-005/X-012. Backlight, gamma, white balance and colour controls are candidates, not promised support.
- **Not accepted if:** Contrast/EXIT success implies all calibration controls work, effective scope is unknown, or insufficient controls are concealed by changing the target or using a PC correction profile instead.

### FR-010 — Meter and serial coexistence

- **Behaviour:** Ensure measurement startup/use cannot send unintended traffic through the TV's serial connection; coordinate resource ownership and closure across the whole session.
- **Check:** SW: demonstrate the reviewed isolation/configuration contract, unexpected process/port access rejection and ownership failure handling. EQ: a separately reviewed coexistence plan establishes behaviour for the selected binaries, drivers and connection sequence before combined operation.
- **Dependencies/status:** Not built; blocked by C-090/C-091 and FR-005/FR-008. Current T-003/T-005 isolate the cable; T-006 excludes measurement/discovery software. No combined mode exists.
- **Not accepted if:** independent component passes are treated as coexistence evidence, startup probing is ignored, or isolation settings are assumed to be a universal guarantee.

### FR-011 — Session ordering and production timing

- **Behaviour:** The integrated controller enforces change → exit → wait → read for baseline preparation, adjustment, menu inspections and restoration. It invalidates stale observations after changes; failed or uncertain exit prevents reading. Repeats retain the completed exit condition and a fresh wait.
- **Check:** SW: order/clock boundary, stale evidence, patch changes and exit-failure cases. EQ: approved exact-TV exit method and settling/timing evidence across relevant changes and readings.
- **Dependencies/status:** Partial toy/offline cycle; production controller not built. D-013, Q-008, FR-003/FR-005/FR-009/FR-010 apply. D-019's two-second minimum and 60-second deadline are diagnostic policies, not production timing validation.
- **Not accepted if:** exit is inferred solely from an ACK, menu inspections bypass the cycle, or a diagnostic delay is promoted to a production guarantee. Unexpected overlays remain a declared D-013 limitation, not a detection promise.

### FR-012 — Targets agreed before adjustment

- **Behaviour:** Record the final Q-014 input/mode, room, peak white, BT.1886 black basis, colour/error metric, reference white and acceptance tolerances before calibration. Label a measured versus assumed black explicitly; do not calculate a default black from a borrowed contrast ratio.
- **Check:** SW: absent targets, changed targets mid-run, unknown black basis and missing acceptance rules prevent a pass. EQ: targets/uncertainty are justified using T-003/T-004 and the owner-approved T-008 plan.
- **Dependencies/status:** Blocked by Q-014, FR-006/FR-007; provisional preferences alone are insufficient. D-001 retains Rec.709/D65/BT.1886.
- **Not accepted if:** targets are selected after seeing results, numerical tolerances are invented here, assumed black is described as measured, or relative improvement replaces the accuracy goal.

### FR-013 — Bounded adjustment engine

- **Behaviour:** Choose changes using accepted measurements and an established response model; limit step sizes, allowed values, total attempts and run duration, and reserve capacity for planned restoration. Account for controls affecting one another, discrete steps, noise and drift. Stop on oscillation, no useful progress or exhausted limits.
- **Check:** SW: independent scripted responses covering coupling, noise, reversal, limits and failure; confirm every proposed change passes the controller's checks. EQ: T-013 followed by the broader T-008/control-response evidence; neither simulated convergence nor one successful control proves a full solver.
- **Dependencies/status:** Not built. FR-006/FR-009–FR-012 and T-013 required before full physical calibration. Algorithm, order and numerical limits are proposals for later review.
- **Not accepted if:** changes/iterations are unbounded, the engine uses rejected data, exceeds an allowlist, or claims success merely because it ran out of steps.

### FR-014 — Stopping and uncertain outcomes

- **Behaviour:** Provide an accessible owner stop throughout the session. Stop new adjustments on cancellation, ambiguous commands, measurement failure, stale state, unexpected behaviour or record failure; retain evidence and distinguish stop requested, process/port closed and equipment state confirmed. An uncertain run cannot resume automatically.
- **Check:** SW: cancellation in each phase, blocked input, full/error logs, delayed replies and a child that outlives its acceptance deadline. EQ: approved native stop/focus/closure procedures and their observed limits; no dangerous fault injection is implied.
- **Dependencies/status:** Partial component stops. C-138 repairs meter input/acceptance and C-139 repairs serial input in software; the [combined source](task2-integration.md) requires focused review. Native console/GUI, driver shutdown and physical prerequisites remain unverified. X-007's production retry policy is undecided. Proposed first-release policy: stop on ambiguity, no automatic resend/reconnect/recovery; requires review.
- **Not accepted if:** a consumed quit key can suspend control, stop is advertised as instant hardware shutdown, unresolved closure is reported as success, or an automatic restoration is sent into unknown state. C-132 also prevents treating complete application logs as lossless wire capture.

### FR-015 — Restoration with evidence

- **Behaviour:** Offer restoration from the protected originals when the state and procedure permit it, and show a separate result for each affected scope and temporary setting. Verify settings and, where required, repeat optical checks after exit/wait. Preserve the owner's manual restoration route after uncertain outcomes.
- **Check:** SW: normal, partial, failed and unavailable restoration, changed scope and missing originals; never collapse them into success. EQ: T-006/T-013 and final T-008 restoration checks for every affected input/mode/configuration in the reviewed plan.
- **Dependencies/status:** Partial toy restoration only; blocked by FR-002/FR-009/FR-014 and X-012. The detailed physical restoration/recovery procedure remains to be established.
- **Not accepted if:** commanded values or ACKs alone certify restoration, factory reset substitutes for originals, or failure triggers unreviewed automatic recovery. A stopped session may legitimately end with restoration unconfirmed and clearly reported.

### FR-016 — Private and durable session records

- **Behaviour:** Save original settings, configuration identities, purposes, patches, accepted/rejected readings, commands/replies, timings, stop reasons and verification/restoration outcomes privately. Separate simulated, diagnostic and calibration data. Keep personal/device details in ignored `local/` or `.local.` files under AGENTS.md section 11; export only deliberately checked material.
- **Check:** SW: interruptions, disk/full/write errors, bounded logs, incomplete records, schema/version changes and export redaction. EQ: compare an authorised session's record with observations and retained raw evidence.
- **Dependencies/status:** Partial component journals; integrated records/export not built. FR-001/FR-002/FR-005/FR-014 apply; C-132 limits serial evidence.
- **Not accepted if:** failure evidence disappears, incomplete logs count as complete, private raw data is committed/shared automatically, or diagnostics are relabelled as calibration.

### FR-017 — Understandable reports

- **Behaviour:** Produce an owner-readable report with setup/version, target and black basis, correction provenance/validation, before/after and separate verification results, uncertainty, exclusions, failed attempts, changed settings and restoration status. Clearly say passed, failed, stopped, incomplete or inconclusive and explain why; numeric meter values alone cannot confer an accuracy pass.
- **Check:** SW: reports from success, failure, uncertainty and simulated fixtures reconcile with records and contain no invented missing data. EQ: independently reconcile the final report to the real evidence package.
- **Dependencies/status:** Not built. FR-007/FR-012/FR-015/FR-016 define report content; completed FR-018 evidence is needed for the final release report, not for building and testing reports with fixtures. Report format is a later design choice.
- **Not accepted if:** a simulated chart resembles unlabelled hardware results, “as measured” is confused with true accuracy, or failed verification/restoration is hidden by a success headline.

### FR-018 — Independent verification and functioning-release evidence

- **Behaviour:** Verify fixed settings in a separate session with patches not used by the adjustment engine, using predefined rules, repeated checks and drift assessment. Establish accuracy through the Q-001/T-004-agreed independent reference/correction evidence, not just reuse of the optimisation meter. Record owner playback checks and restoration evidence separately.
- **Check:** SW: verifier/report tests with independent expected outcomes, including a loop that improves its training patches but fails withheld patches. EQ: future T-008 evidence bundle described below, independently reviewed against every requirement and final acceptance criterion.
- **Dependencies/status:** Not built/blocked by FR-001–FR-016, T-004/T-013 and Q-014/Q-016; verification and its FR-017 report are accepted together. A separate session with the same meter checks consistency/generalisation; it does not independently establish absolute accuracy.
- **Not accepted if:** verification patches influence later adjustments without a fresh verification, bias/uncertainty is unaddressed, any essential gate lacks evidence, or another AI's agreement substitutes for measurement.

### FR-019 — Reproducible Windows installation

- **Behaviour:** Provide a reviewed supported Windows/Python configuration, exact dependency versions, clear installation/start/update/removal instructions and a hardware-free first-run check. Explain how the owner obtains and selects Argyll/driver/correction files and preserves private records. Normal installation must not operate equipment.
- **Check:** SW: reproduce installation and simulation in a clean representative Windows environment, including missing/conflicting dependencies and paths with spaces; verify version identity and record preservation. EQ: separate authorised confirmation of actual driver/meter/control operation on the owner's PC.
- **Dependencies/status:** Not built; Q-003 open. Historical test interpreters and the component-test Python delegation do not select production support or an installer. Packaging format requires an owner-reviewed proposal.
- **Not accepted if:** success requires an undocumented developer setup, hidden manual code edits, unreviewed downloads or hardware discovery during install. No release publication is authorised here.

### FR-020 — Free/open-source licensing and distribution readiness

- **Behaviour:** Choose the project licence under Q-002 and document compatible use/distribution obligations for Python, GUI, serial, Argyll and correction data, with notices and reproducible dependency sources. Stay within the hardware budget and avoid paid services/commercial calibration dependencies.
- **Check:** SW/document review: inventory the exact intended package and licences, distinguish externally obtained tools from bundled files, and resolve applicable obligations before distribution. EQ: none; licensing review is not an equipment test.
- **Dependencies/status:** Blocked by Q-002/Q-003 and correction selection. The audit records Argyll package/component licence distinctions; separate processes alone do not settle obligations. No licence or packaging answer is selected here.
- **Not accepted if:** required files lack usable permission/provenance, the project remains unlicensed at distribution, or the planned release depends on unapproved expenditure/publication.

## Evidence needed to call the release functioning

Two separate records are required; neither a merged PR nor a passing simulation completes both.

**Software-only acceptance record:** identify the exact source/package revision and supported Windows/Python/dependency versions; map FR-001–FR-020 to focused checks; retain actual passed/failed/skipped/unrun outcomes; reproduce failure/cancellation/uncertainty behaviour and report generation with inert data; and demonstrate installation without equipment access. Resolve the meter-wrapper and console defects with reviewed implementation and regressions. State the limits of fakes and any untested native behaviour. This document runs no application suite and claims no new software results.

**Equipment acceptance record:** a future reviewed T-008 plan must link satisfactory T-001–T-006 and T-013 evidence, the exact owner authority and software identities, the supported-control/scope/restoration record, the corrected meter configuration and validation, signal-range/display evidence, coexistence evidence and justified production timing. Include original settings, baseline and adjustment records, all rejected/failed attempts, separate-session withheld-patch verification, uncertainty/drift analysis, owner playback observations and restoration results. Raw private records remain private; reviewed summaries must be traceable to them.

Before those decisive measurements, the owner must approve the final Q-014 targets and success limits, with the Q-001 correction-validation method and uncertainty basis. The final review must show that the criteria were actually met, not invent them afterwards. No particular colour-error threshold, repeatability tolerance, black level, settling delay or iteration limit is selected by this specification. Until these are agreed, the dependent requirements cannot be accepted.

Acceptance requires all essential requirements to have evidence and no unresolved failure that invalidates the result. A successful T-013 experiment, improved same-meter numbers, a complete log, a clean exit or two agreeing AI reviews cannot establish that. An honest failed/inconclusive report is required product behaviour but is not evidence of a successful calibration. If a dependency cannot be met within scope/budget, retain the blocked status and obtain an explicit reviewed owner decision before changing the release promise.

## Reconciliation with earlier proposals

| Earlier proposal or possible confusion | Governing decision or evidence for this release |
|---|---|
| Original architecture and S-002 include network fallback | D-006 supersedes that route. Q-013 is unanswered; no fallback is adopted |
| S-002 forecasts accuracy/low-light performance and defaults black to white/3,000 | C-058, X-006, C-130 and audit A-004 require equipment/validation evidence. Q-014 selects any final black basis; this spec assumes none |
| S-002 proposes retries after missing acknowledgements | X-007 remains open. Current physical plans stop; FR-014 proposes that conservative first-release policy for review, without claiming a settled production design |
| Stage 6 in the older plan describes improvement beyond repeatability in a separate session | This remains useful relative evidence, but is insufficient for validated accuracy. D-003, Q-001/T-004/Q-016 and FR-007/FR-018 also govern acceptance; the plan is clarified accordingly |
| A T-005 clipping/stability pass implies correct range or exact pixels | The current Stage 4 qualification and X-008 explicitly reject that inference. FR-004 needs the additional range method and preserves digital-fidelity limits |
| Generic diagnostic data, T-013 success or accepted diagnostic timing are a release | D-019 and the plan keep diagnostics separate. Q-008 production timing, Q-014 targets and T-004 accuracy evidence remain open |
| Early software records say the presenter/transport is missing | Later component tools/readiness implement bounded separate paths. They do not supply an integrated controller, optimiser, full control set or hardware results |
| Ten menu white-balance points or proprietary DDC documentation prove public command support | C-078 resolves menu count only; C-065/C-133, Q-006 and X-010 preserve exact-protocol uncertainty |
| The audit's merge repairs defects, authorises tests or completes all historical review coverage | The audit did not repair C-131/C-136. Later C-138/C-139 software changes address meter acceptance and serial input; their combined source needs focused review, while native and physical gates remain. X-019 preserves historical review qualifications |
| Discovery preparation is either automatically waived or expanded again | D-020/D-021 and current plans govern. Q-021 may commission simplification, but is not a new mandatory release gate and does not revive retired Samsung questions |

Archived originals remain unchanged. The ledger retains disputed positions and historical results; this proposal does not settle X-005/X-006/X-007/X-008/X-010/X-012/X-017 by wording alone.

## Dependency-ordered implementation checklist

These are future reviewed work packages, not permission to implement or operate equipment in this documentation task. Software-only development can proceed while equipment work is blocked. The order follows dependencies rather than requiring every earlier investigation to finish: T-013 may proceed after its own component/coexistence gates while correction validation and final T-008 targets remain unresolved, as the current plan permits.

1. [ ] Review this contract and retain the open owner decisions. Propose the final Windows/Python/packaging and licensing route early (Q-002/Q-003); research correction validation and exact-TV compatibility without assuming success.
2. [ ] Review the [combined meter/serial source and verification](task2-integration.md), then resolve the separate native/physical prerequisites (FR-005/FR-014/FR-016). Both software fixes are implemented; prior-head reviews/results do not validate their combination. Retain C-136's physical hold and every unrelated equipment-authorisation gate.
3. [ ] Complete current discovery preparation and obtain exact authority for discovery. Then separately establish meter validity/repeatability/range, display/range interpretation and electrical/control/scope/restoration evidence under each component plan's own gates (FR-002–FR-009). These independent investigations need not wait for unrelated repository administration.
4. [ ] Resolve the correction/reference route, final target criteria and production timing with the owner after relevant evidence (FR-007/FR-011/FR-012; Q-001/Q-008/Q-014/Q-016). Establish enough supported controls to meet that contract or report the limitation before promising calibration.
5. [ ] Build and review the integrated controller, original-state records, private evidence/report format and safe meter/serial coexistence; verify offline before authorised combined operation (FR-001/FR-010/FR-011/FR-014–FR-017).
6. [ ] Prepare T-013 against its [Stage 5 prerequisites](../plan.md#stage-5--t-013-one-reversible-adjustment-with-measured-feedback-needs-authorisation), including the existing meter/serial coexistence gate described in FR-010. Complete the bounded orchestration, original-setting/measurement records, limits and stop/restoration handling needed for that experiment; item 4 and the full production controller/reporting in item 5 need not be complete. Review and obtain explicit authority before executing the plan, then assess its results. Use that diagnostic response/restoration evidence to inform the production adjustment engine; build and verify the engine offline once its FR-013 dependencies are met. T-013 remains diagnostic, not release acceptance.
7. [ ] Complete the supported Windows package and hardware-free installation checks, licence/data obligations and owner instructions (FR-019/FR-020). Package preparation does not authorise publication.
8. [ ] Prepare the final T-008 acceptance plan, obtain exact authority, and demonstrate the whole journey with independent verification/restoration evidence. Have a different vendor review the exact final implementation and evidence; only the owner decides release readiness and separately authorises any publication (FR-018).

**Optional later enhancements:** broader hardware support, richer report formats, convenience controls and more sophisticated optimisation, provided essential acceptance is already met. HDR remains a separate later project stage. Automatic recovery would require its own design/evidence and approval; it is not promised here. These are possibilities, not commitments.

**Separate repository administration:** Q-004/Q-005/Q-011/Q-015/Q-017/Q-018 concern branch protection, review delivery, visibility/history and automation. They remain recorded but are not technical prerequisites for a functioning calibration application. No setting, automation, archive/history rewrite or publishing change is part of this specification. Existing cross-vendor review and owner-only merge rules still apply.
