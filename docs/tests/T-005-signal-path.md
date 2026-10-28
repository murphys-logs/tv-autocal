# T-005 — SDR signal-path and clipping checks

> **Status: draft plan — NOT AUTHORISED. Do not carry out any step.**
> **Equipment not tested. Ready for independent review, not execution:** the proposed software readiness revision and this amendment need review; local/display inputs and the owner's permission remain unresolved. Part M also needs T-003 evidence. A screening pass still cannot close the black/white range-interpretation gate.

Prepared by Codex (OpenAI), 27 October 2026. The choices and numerical thresholds below are **AI design proposals**, not measurements, manufacturer tolerances or an answer already given by the owner.

Execution amendment: Codex (OpenAI), 28 October 2026, for the proposed [readiness revision](../software/component-readiness.md) based on merged PR #26 at `dc552c737ec61d5b323ceda844fd198785170c61`. The [shared execution record](component-execution.md) is part of the proposed plan. Bind the final independently reviewed source/manifest before authorisation; the older PR #25 tools do not implement this revision's controls. No future reviewed plan SHA or authorisation is supplied here.

## 1. Purpose

Screen the recorded PC → Denon → TV path for visible clipping, geometry problems, changing processing and unstable output. Document the configuration and the limits of that screening for later experiments. Addresses C-004, C-030, C-044, C-059, C-063 and C-071; uses owner records C-075 and C-079 to C-081. It does **not** establish correct black/white range interpretation, exact HDMI code values, absolute colour accuracy or a validated correction. The Stage 4 range-interpretation gate and X-008 remain open even if this clipping screen passes.

This plan has two separately authorisable parts: **V** (visual checks, no meter) and **M** (optical checks using the Spyder5). Part V can run before T-003; part M cannot. Neither requires Ex-Link or T-006 because the owner exits menus manually. T-003 can take its initial relative readings before T-005 passes; it does not treat its unverified patches as calibration evidence.

**Prerequisites before authorisation:**

- T-001/T-002 owner records in [S-033](../briefs/2026-10-26-owner-equipment-checklist.md) are already available. Recheck only the live starting state in step V1; do not assume it is unchanged.
- The proposed readiness presenter and meter source/hashes are identified in the [shared software record](component-execution.md#reviewed-software-and-local-inputs), with the launch/sequence mapping below; this revision needs independent review. Actual Windows/Tk behaviour remains untested. The final local interpreter/dependency identities and display arrangement must be recorded before authorisation. No browser, media-player or other replacement may be improvised during testing.
- The [offline renderer verification](../software/renderer-cycle.md) checks the listed **application RGB values** and native geometry against independent expected buffers. The presenter passes those buffers through Tk's PPM image path at gamma 1.0 without requested resampling or range conversion. This is not an observation of a real Windows surface or proof that Windows/GPU/HDMI add no transform. Record that untested boundary and the exact Tk/Windows configuration; do not promote source or buffer checks into HDMI/light evidence.
- The TV initially shows a target-confirmation screen, not a measurement patch. In the separate operator window, the owner clicks **Confirm TV target**, then **Next pattern** once per pattern; **Stop presentation** requests closure. Ordinary typing cannot confirm or advance. Escape requests stop if either presenter window has focus. There is no automatic display selection or enumeration. **Unresolved owner input (Q-019):** the owner can, and probably will, connect a second screen; this revision requires one, but connection, both window positions, coordinate-acquisition method/authorisation, console placement and operator-access/focus checks remain unconfirmed. Resolve the [display procedure](component-execution.md#display-and-console-arrangement) before pattern output is authorised.
- Record the provisional Q-014 configuration and the owner's acceptance of the **2-second proposed wait** in section 8. This is a starting test value under Q-008, not a settled timing result. Do not tune TV brightness to the 140–160 cd/m² preference in this test.
- Part M additionally needs completed T-003 results documenting a working meter command, a stable warmed-up configuration, neutral-patch repeatability and the usable neutral range. Primary-channel eligibility is assessed from this test's own readings; it is not inferred from gray alone. Use that exact Argyll version/command, instrument mode and correction configuration. No new driver, OEM calibration data, correction file or software installation is included here.
- Before any ArgyllCMS launch, including help/discovery and each measurement child, the owner must verify that the SH-U35B Ex-Link cable is physically disconnected from **both the PC's USB port and the TV**, and record that state. ArgyllCMS can probe serial adapters during startup instrument discovery (C-090/S-037); disconnecting only the TV end does not prevent writes to the adapter. Follow T-003's [isolated launch environment](T-003-meter.md#isolated-launch-environment) as well; a command without `-X` alone does not establish that no external correction is selected.
- Independent review of this execution amendment and the owner's explicit dated authorisation of the chosen part and exact plan revision are required. Unresolved display/local identities or missing T-003 evidence block the dependent part, even if the plan has been merged. The [shared unresolved-input list](component-execution.md#unresolved-inputs) identifies outstanding decisions and evidence; the proposed wait and screening limits still need owner acceptance.

**Source basis actually consulted:** owner equipment record and S-033; the merged [proposed stages](../plan.md); S-024's signal-path discussion (AI research); Denon [AVC-X3800H Output Settings](https://manuals.denon.com/AVCX3800H/EU/EN/GFNFSYmlxuhedk.php) (S-030), reconsulted 27 October 2026; NVIDIA [To change the RGB dynamic range](https://www.nvidia.com/content/Control-Panel-Help/vLatest/en-us/mergedProjects/Display/To_change_the_RGB_range.htm), consulted 27 October 2026, live documentation with no revision stated. NVIDIA defines the Full and Limited output options; this does not prove the exact conversions performed by this renderer/driver/TV combination. Denon describes Bypass as removing video processing and preventing information overlays over video, with an IMAX sound-mode restriction; neither claim has been tested here.

## 2. Equipment and settings involved

Use the existing Windows 10 Home 22H2 PC / GTX 1080 / driver 582.78 → Denon HDMI In PC → Monitor 1 → Samsung HDMI 4 path, with the TV's firmware T-JZMDEUC-1270.1. Use only SDR. The owner-reported PC output is 3840×2160 at 60 Hz, RGB, 8bpc, Limited; Windows HDR and Night light are off. TV HDMI Black Level is Auto. Retain those settings for this first screening pass.

**Encoding contract:** every RGB number below is an application-buffer value in the range 0–255. Application black is `(0,0,0)` and white is `(255,255,255)`. Do not substitute `(16,16,16)` and `(235,235,235)` merely because the GPU is set to Limited. A single full-to-limited conversion in the output path is the working hypothesis, not a demonstrated fact; the possible quantisation and transformations must remain in the result's limits. No GPU-Full/TV-Limited comparison is included.

The only proposed setting changes are owner selection of the PC receiver input and TV HDMI 4/Movie mode, and the Denon PC input's Video Mode from its captured original value to Bypass and back. No TV picture slider, white-balance value, colour-space value, HDMI range, Apply Picture Settings scope, Windows profile, GPU lookup table, HDR setting or receiver sound mode is changed. No `dispwin -c` or other calibration-loader command is included.

Part M adds the Spyder5Pro, in the same placement and fixed configuration as T-003. Keep both ends of the Ex-Link cable disconnected throughout this test, including its USB end at the PC; do not reconnect it for restoration. No TV-control or network commands are part of this plan. The disconnection prevents ArgyllCMS's serial discovery from reaching this adapter; it is not evidence that ArgyllCMS never opens a serial port.

## 3. Risks and how to undo them

**No service-menu step is included.** Menu navigation and input/mode selection are by the owner with the ordinary remote. Stop if a menu differs from the recorded procedure, if Bypass is unavailable, or if there is unexpected behaviour. In particular, do not change an IMAX DTS/IMAX DTS:X sound mode to unlock Bypass; revise the plan separately.

Input/mode selection can change the picture seen by normal playback; Denon Bypass changes receiver processing and information displays. Restore the original input selections, original HDMI 4 picture mode and original Denon PC Video Mode in step R1. The TV's reported **Apply Picture Settings: All Sources** is a reason to leave picture sliders and that scope untouched. Do not describe recorded current values as factory defaults.

Write the actual starting values before each corresponding change; the table contains recording fields, not prefilled results. If the known PC range, HDR state or signal route differs from section 2, stop for a reviewed revision instead of changing it to match.

| Device | Setting or state | Original value recorded during authorised session | Restored afterwards? |
|---|---|---|---|
| TV | Active source before session | Not recorded | Not carried out |
| TV | HDMI 4 picture mode before selecting Movie | Not recorded | Not carried out |
| TV | Movie mode HDMI Black Level; HDMI UHD Color for HDMI 4; Apply Picture Settings; Backlight/Brightness/Contrast; Gamma; Smart LED; Dynamic Contrast; Digital Clean View; Auto Motion Plus; Eco settings (record only) | Not recorded | No changes permitted |
| PC | Output resolution/refresh/format/depth/range; HDR; Night light; assigned colour profile; presenter and display selection | Not recorded | No settings changes permitted; presenter exits |
| Denon | Active input before session; PC input Video Mode; Upscaler; signal format; sound mode | Not recorded | Not carried out |
| Meter (part M) | Placement, instrument mode and correction configuration | Not recorded | Restore T-003/session-start placement after removing meter |
| Ex-Link cable | USB end disconnected from PC and TV end disconnected; verify before any Argyll launch | Not recorded | Leave disconnected; reconnection is outside this plan |
| PC (part M) | T-003 launch-environment checks, including external-correction defaults | Not recorded | Use T-003's process-local setup/exit procedure; do not change persistent defaults |

A changed mode may have different settings from S-033; record them before taking readings. Part M requires Smart LED, Dynamic Contrast and the recorded Eco processing to be off in the actual Movie-mode state; if not, stop for a revised plan rather than changing them. This plan does not automatically overwrite them. Unexplained differences that affect range or stability stop the test. On a stop, the owner may restore the listed original values manually if the ordinary menus are understood; no automatic recovery, blind key sequence or continued measurement is permitted.

## 4. Cost

No purchase or paid service is proposed: **£0**. The ledger remains £15.99 spent and £9.01 remaining of the £25 hardware limit. No digital HDMI analyser is assumed available; the resulting evidence cannot claim independent digital code verification.

## 5. Steps

**All steps below are future steps.** The owner operates remotes, launches the reviewed presenter and, in part M, launches one reviewed meter-runner attempt at a time. An agent may record observations and compute statistics with the owner present. These instructions do not authorise an agent to operate hardware.

### Reviewed tool execution mapping

The following argument specifications are **for review, not executable instructions now**. Every tool launch also needs the common `--hardware`, `--permit`, exact `--confirm` and fresh `--log` fields in the [authorisation/launch record](component-execution.md#authorisation-and-launch-record), with plan `T-005`. The interpreter and source identity come from the [shared software record](component-execution.md#reviewed-software-and-local-inputs). Keep unresolved values labelled **UNRESOLVED**, and provide no permit until the actual reviewed scope has been authorised.

| Run | Tool-specific argument values and scope |
|---|---|
| V-A: original-state visual inspection | `present --sequence t005-visual`; explicit `--x`/`--y` for the confirmed nonnegative TV origin and `--control-x`/`--control-y` for the operator window on a different display; fresh presenter journal. One geometry frame followed by six V3 patterns. |
| V-B: hold grey through the Bypass change | `present --sequence patch --rgb 128,128,128`; same confirmed TV and operator-window positions, new journal. One held grey patch, no meter. |
| V-C: Bypass visual inspection | `present --sequence t005-visual`; re-confirmed unchanged TV and operator-window positions through the reviewed display procedure, new journal. Repeat geometry explicitly, then six V3 patterns once. |
| M: one continuous optical presenter | `present --sequence t005-optical`; re-confirmed unchanged TV and operator-window positions through the reviewed display procedure, new journal, held through the warm-up and all eligible attempts. |
| Each M reading | `meter`; local `--executable`/`--sha256` from the accepted T-003 record; fresh `--attempt-log` directly under `local/T-005/`, distinct from its evidence `--log`; `--presentation-log` names the active M presenter journal; `--presentation-sequence`, `--rgb`, `--purpose` follow the table below. Proposed `--wait-ms 2000 --timeout-ms 60000`; include `--isolated --exit-confirmed --discovery-confirmed` only when each statement is true. |

Both explicit positions, their acquisition/reconfirmation method and the arrangement remain unresolved inputs. Every presenter run requires all four coordinate options; the operator window's outer rectangle must fit wholly in a different display's usable area, outside the TV. Inspect the TV's target-confirmation screen, then click **Confirm TV target** and **Next pattern** in the operator window to display the first frame. Use the still-required [operator-access/console-focus procedure](component-execution.md#display-and-console-arrangement), including a check that the meter console has focus before typing or editing; never use typing as the focus test. No console or controls may cover the TV image. Do not move either presenter window or minimise the controls, including through Win+D/Win+M or the taskbar; if this happens, abandon the run under the shared procedure even if it does not close automatically. An unplanned confirm, advance or close also stops the run. Use **Stop presentation** for closure; Escape also stops with either presenter window focused. Callback interruption causes a terminal failure and closure attempt, but native interrupt delivery and actual closure remain untested. Each meter launch is manual and the full attempt must finish before a patch change or presenter closure. A journal receipt cannot prove either window remains alive or visible.

Every named visual frame has a **60-second limit**: record it and click **Next pattern** before expiry. Expiry closes the run and is a stop, not permission to relaunch. All presenter runs have a **three-hour lifetime**; reaching it during an outstanding meter attempt rejects that attempt and stops the schedule. No restart, extension or extra visual comparison is included. At a planned boundary, after completing that run's required steps, intentionally click **Stop presentation** (or **Next pattern** once after the last frame). Require `presenter_closed.fields.reason` to be exactly `owner requested stop` or `manual advance after final pattern`, matching that intended action, plus `presenter_closed.fields.close_completed: true`, disappearance of both windows, normal CLI exit and final `journal-close` with `complete: true` before the next planned run. The new closure field records successful return of the close calls, not physical verification; false or absent stops the plan. The reason alone does not legitimise an accidental or early close. Any other reason (including either time limit, `window loop ended` or `failure: …`) stops the plan even if the CLI exits 0 and the journal is complete. Missing closure evidence stops further work; it does not establish successful closure or electrical safety.

### Part V — record the path and inspect patterns

1. **V1 — Owner:** verify the authorised plan revision and record the original states in section 3. Select the Denon's PC input and TV HDMI 4; record HDMI 4's current picture mode, then select Movie. Record its relevant settings, without changing them. Confirm the section 2 SDR/PC/range state; a difference stops this run. Exit all menus with the normal remotes, then wait at least 2 seconds. The owner confirms this initial exit is clear.
2. **V2 — Owner:** launch run V-A using the mapping above, inspect the intended TV, then click **Confirm TV target** and **Next pattern** in the operator window to show geometry (frame 1): a one-pixel outer border and labelled corner markers at native 3840×2160. Record whether any edge is cropped or rescaled. If a border/corner is missing or the presenter reports scaling, stop; do not change TV size, GPU scaling or overscan controls under this plan.
3. **V3 — Owner:** show the visual patterns below in order, at most 60 seconds each, advancing manually. Leave at least 2 seconds after each pattern change before judging it. Labels occupy a separate area and never enter a measurement patch. Record each specified comparison as visible / indistinguishable / uncertain. For black, distinguish "looks black" from a measured black level. Gross unexpected colour shifts, crushed/lifted blacks or clipping end this run; do not tune controls until the suspected cause is reviewed.

| Visual pattern | Application RGB values and observation |
|---|---|
| V-black | Neutral bars `(v,v,v)` for `v = 0, 4, 8, 12, 16, 24, 32, 51` on black. Record the first visibly distinguishable bar, and whether 16/32/51 remain distinct from 0 and one another. Failure to distinguish very low bars alone may reflect display/vision limits. |
| V-white | Neutral bars for `v = 204, 230, 242, 250, 255`. Record each adjacent pair; broad merging below 242 is a clipping warning, not permission to lower Contrast. |
| V-red, V-green, V-blue | For each primary in turn, bars with that channel `204, 230, 242, 255` and the other channels 0. Record adjacent distinctions and any colour reversal or loss of detail. |
| V-detail | Alternating one-pixel red/blue vertical lines beside one-pixel black/white lines, plus native-pixel text. Record visible smearing/cropping. This is a visual spatial-detail screen, not proof of RGB 4:4:4 delivery. |

4. **V4 — Owner:** after V3's detail frame (frame 7), close V-A normally and confirm its closure reason/evidence as specified above. The visual playlist has no grey return. Launch the separately recorded V-B run, confirm the target, advance once to grey 128, and keep it displayed. In the Denon PC input's ordinary Video → Output Settings menu, set Video Mode to Bypass. If unavailable, stop without changing sound mode. A V-B self-closure, signal loss or detected desktop-layout change during this operation stops the plan; do not relaunch to finish the comparison. Exit the receiver menu and TV menu if opened, wait at least 2 seconds, and confirm this exit is clear while grey remains displayed. Record completion, then close V-B normally and re-confirm the unchanged TV and operator-window positions using the reviewed method. Do not enumerate displays or try coordinates unless that exact action is separately included in the reviewed authorisation. Launch V-C, confirm the target, **repeat V2's geometry check** once and then V3's six patterns exactly once in Bypass; close V-C normally after detail. A failed geometry/visual/closure check stops the plan; these three planned runs are not retries. Do not deliberately trigger volume/status banners. Record observed differences and any unexpected overlay; absence during this short observation does not prove overlays can never occur.
5. **V5 — Owner and agent:** record the visual outcome against section 7. If only part V is authorised, carry out R1 and finish with a **visual-only partial result**. Part M needs its own explicit inclusion in section 8 and all T-003 prerequisites.

### Part M — bounded optical checks in Bypass

1. **M0 — Owner:** establish this session's starting state before preparing the meter. If M follows V without interruption or restoration, retain V1's original-state records and recheck the active input, Movie settings, PC range and Denon Bypass state. If V was completed in an earlier session, or R1 has already restored the settings, start a new dated section 3 record and repeat V1–V4, including setting Bypass and confirming menu exit/wait. Part M authorisation must explicitly include these setup steps when applicable. Do not overwrite the earlier session's originals or assume its Bypass state persisted. Re-confirm the unchanged TV and operator-window positions through the reviewed method. Any unexplained difference or failed visual check stops M. Verify both Ex-Link ends are disconnected and complete T-003's isolated launch-environment checks before any Argyll command.
2. **M1 — Owner:** use T-003's fixed meter configuration on the input/Movie/range settings and Denon Bypass state just verified in M0. Start and confirm the M presenter while its instruction screen is unobstructed, advance to grey 128 (frame 1), then mount the meter at the patch centre as in T-003. Keep it displayed for at least the warm-up duration established by T-003 before M2; record elapsed time and hold the configuration fixed. Each scheduled reading uses the meter runner, which launches the fixed child argument list `spotread.exe -O -e -x -Y n <unique-local-attempt.log>` with the logfile last and no external correction, including none supplied by environment defaults. This is not an alternative direct-launch command. The exact accepted executable/hash/configuration and isolated launch-environment procedure must come from the completed T-003 record before authorisation. The wrapper runs no separate discovery command, but every measurement child may probe ports at startup (C-090). No installer, `oeminst`, profile loader or alternative command is allowed here. Stop on errors or unexpected prompts, following T-003's stop/timeout procedure. Use the same exactly centred 960×540 patch at x=1440, y=810 on 3840×2160, RGB 0 surround, **6.25% area**, with no text beneath the meter.

   For M1's `--discovery-confirmed`, the prior T-003 discovery may be reused only if its exact executable/hash, instrument, USB arrangement, driver and measurement/correction configuration remain unchanged and the default instrument remains unambiguous. Record that comparison even in a later session; do not infer it from the passage of time or an old successful reading. A change or uncertainty blocks part M until a fresh, separately reviewed and authorised T-003 discovery record resolves it. Part M does not authorise help/discovery or an automatic repeat of T-003.

3. **M2 — Owner:** show gray 128, exit menus if inspected and wait at least 2 seconds, then take five consecutive readings, allowing at least 2 seconds before each launch. Apply that inter-reading wait throughout part M. Record finite XYZ and luminance Y; reject nothing merely for being inconvenient. If these readings fail T-003's stable-repeatability criterion, stop before the ramp.
4. **M3 — Owner:** show neutral patches in the fixed order `0, 13, 26, 51, 102, 153, 204, 230, 242, 255`, where each code sets all three channels. At each patch wait at least 2 seconds after presentation, then take three consecutive readings. Codes at or above T-003's lowest usable tested neutral code are candidates for this run's monotonicity check, not presumed already verified. Lower codes 0/13/26 may be measured diagnostically only if T-003 returned finite readings for that code within its timeout; otherwise mark them **unmeasurable under the established configuration**, not zero. Retain noisy low readings as diagnostic/inconclusive. Then show gray 128 and take five reference readings. Stop on an unexpected plateau/reversal above the usable floor or failed drift criterion; do not continue to colour checks.
5. **M4 — Owner:** for red, then green, then blue, show application channel values `204, 230, 242, 255`, other channels 0. Wait at least 2 seconds after each presentation and take three readings. Then show gray 128 and take five final reference readings. This is a high-end channel clipping screen; it does not assess Rec.709 gamut accuracy or D65.
6. **M5 — Agent with owner present:** calculate the predeclared statistics in section 7 and retain all valid, invalid and omitted attempts. Do not adjust the display to obtain a pass. The maximum is **81 meter invocations** (15 gray-reference readings, 30 neutral readings and 36 primary readings), fewer where low patches are ineligible. There is no automatic retry. Each invocation uses T-003's approved timeout; any failure stops the run rather than extending the count.

Use this literal mapping for the M presenter and each meter-runner receipt:

| Step | Presenter frame (`--presentation-sequence`) | `--rgb` | `--purpose` | Maximum attempts |
|---|---|---|---|---:|
| M2 | 1 | `128,128,128` | `initial-reference` | 5 |
| M3 neutral ramp | 2–11, in order | Equal channels: `0`, `13`, `26`, `51`, `102`, `153`, `204`, `230`, `242`, `255` | `neutral` | 3 per eligible frame |
| M3 middle reference | 12 | `128,128,128` | `middle-reference` | 5 |
| M4 red | 13–16 | `204,0,0` / `230,0,0` / `242,0,0` / `255,0,0` | `primary` | 3 per frame |
| M4 green | 17–20 | `0,204,0` / `0,230,0` / `0,242,0` / `0,255,0` | `primary` | 3 per frame |
| M4 blue | 21–24 | `0,0,204` / `0,0,230` / `0,0,242` / `0,0,255` | `primary` | 3 per frame |
| M4 end reference | 25 | `128,128,128` | `end-check` | 5 |

For example, neutral frame 2 requires `--rgb 0,0,0`; all three comma-separated channels are supplied. If a low patch is ineligible under M3, record the omission and advance past its frame without launching a reading; never renumber subsequent frames. Match each entry to the latest `pattern_present_intent`/`pattern_buffer_applied` pair in the still-open M journal. Use **`fields.sequence`**, not the journal's top-level event number. The same patch/frame is reused for repeated readings; there is a fresh meter journal and native attempt logfile for each. Advance once per next frame only after the previous attempt has finished and its evidence is checked. No meter attempt may span V-A/V-B/V-C/M or any presenter closure.

Apply the [shared meter closure procedure](component-execution.md#meter-attempt-and-closure) and [T-003 stop procedure](T-003-meter.md#stopping-and-an-outstanding-reading). Privately retain `wrapper_pid`/`child_pid`, `child_exit_confirmed`, `readers_complete`, `exit_code`, acceptance/reason and capture/log status, **not an invented `closed` field**; retain lifecycle/stream-end/`meter_exit` evidence and final `journal-close` after CLI completion. Require both confirmed child exit and completed readers as well as the remaining acceptance checks. A timeout or Python-delivered Ctrl+C rejects an attempt while capture stays attached; repeated SIGINT requests during launch/supervision/cleanup do not escalate to child termination. Ctrl+Break is unsupported, is not covered by that policy and must not be used as an alternative project stop action; if it occurs, apply the shared abnormal-stop gate. Native interrupt behaviour remains untested. Hold the patch while a process is outstanding unless the owner chooses to stop; the owner's right to stop is unconditional. Any interrupted/expired presentation or unknown completion rejects the affected attempt and blocks further work. No true status flag proves driver or equipment safety.

### Restoration

1. **R1 — Owner:** on normal completion, restore this session's captured original Denon PC Video Mode, HDMI 4 picture mode, and receiver/TV source selections (V1 originals for a continuous V/M session; M0's new originals for a separate M session). Inspect the restored values in normal menus, exit, and wait at least 2 seconds. Do not take more readings after returning to another source or mode. Close the remaining presenter and this session's dedicated meter console after normal meter exit and evidence checks, and remove the meter if part M used it. Leave Ex-Link disconnected at both ends. Record each restoration separately. On an earlier stop use only the manual restoration procedure in section 3 and T-003's stop/timeout procedure; stop further project work if restoration is uncertain.

## 6. What will be recorded

Record the plan revision, authorisation, dates/times, participants, source/firmware/software versions, presenter commit/hash/launch method and output-display choice, every setting in section 3, pattern definition/hash and geometry, and the chronological observation table. Keep machine-specific paths and original logs in ignored `local/`; sanitise copies before committing. No device serials, network addresses or personal path components belong in the public results.

For part M, additionally record one row per attempt: unique ID, purpose **T-005 diagnostic only**, patch application RGB, input/mode/settings, start/end times, exact meter command/version, display/instrument mode, correction filename/hash and validation status (or `none / not applicable`), raw XYZ, return/error state and acceptance/rejection reason. Preserve every rejected attempt and every omitted low patch. Include the T-003 eligibility/noise evidence; never silently substitute predicted HDMI values or target luminance for observations.

**Measurement cycle:** V1/V4 (repeated by M0 for a separate session) establish the owner-controlled menu-exit method. After any menu inspection or permitted setting change, the owner exits all opened menus and waits at least 2 seconds before the next reading. Each patch change also gets at least 2 seconds. Subsequent readings of an unchanged patch require that preceding exit/wait to be complete, not another menu visit. Restoration follows change → exit → wait, with no reading when returning to the original non-test state. No Ex-Link menu-exit mechanism is exercised. An observed overlay invalidates the affected attempt and ends the run; this plan provides no automatic overlay detector and does not require inspecting the whole screen before every reading.

## 7. How results will be judged

The following are proposed screening thresholds to agree **before execution**. They do not certify absolute accuracy or derive from a manufacturer specification.

In the checks below, **mean Y** is average measured brightness and **sample standard deviation** describes the scatter of repeated readings. The step formula requires the increase between two patches to exceed both a noise allowance and two increments of the printed brightness precision. `max` chooses the larger allowance; `sqrt` means square root. This avoids counting a tiny printed difference as a clear improvement when the meter's variation or rounding could explain it.

| Check | Proposed interpretation |
|---|---|
| Recorded path and geometry | Every setting and presenter identity is recorded; native border/corners are visible. A missing record, crop or unexplained transform makes the relevant part inconclusive. |
| Visual levels | All observations retained. Broad merging/reversal of the 16/32/51 dark bars or of the 204/230/242/255 high bars requires explanation before a pass. The visibility of 4/8/12 or 250 is reported without requiring the owner to resolve one-code differences. Visual black appearance alone cannot establish correct black decoding. |
| Repeatability and drift | Gray-128 groups satisfy T-003's accepted repeatability limit. Their mean Y differs from the first group by no more than 2%; otherwise the optical run is inconclusive and stops. This 2% is a test policy, not an accuracy claim. |
| Usable neutral and high-primary steps | For each adjacent eligible group, mean Y must increase by more than `max(3 × sqrt(s_a²/n_a + s_b²/n_b), 2q)`, where `s` is the sample standard deviation, `n = 3`, and `q` is the coarser of the two groups' reported Y decimal increments. Also report raw ranges and rounded output precision; identical printed readings do not establish zero uncertainty. A plateau/reversal or a difference indistinguishable from noise is inconclusive (possible clipping/instability), not automatically a bad TV. No extra runs are implied. |
| Low-light limitation | Record results below the T-003 usable floor as inconclusive and list omitted patches. No assumed black value is substituted; no gamma/BT.1886 target is calculated. |
| Denon comparison | Record Auto-versus-Bypass visual behaviour only. Part M qualifies the Bypass configuration; it does not measure equality to Auto or prove the receiver passes identical digital values. |

A **clipping-screen pass within the reported range** requires complete V and M records, no unexplained clipping/geometry problem in the eligible tested range, acceptable repeatability/drift, and confirmed restoration. If required near-black evidence cannot be obtained, record **partial/inconclusive** and list the screened range rather than a blanket pass.

**The Stage 4 requirement to establish correct black and white interpretation remains unmet by this plan.** A Limited signal mistakenly interpreted as Full can still show stable, increasing, distinct bars, despite raised black and reduced peak white. Repeating a full-to-limited conversion can also preserve those distinctions while compressing the range. These are limitations of the proposed method, not observations on this equipment. A clipping-screen pass therefore does not establish correct range decoding and cannot by itself complete the T-005 prerequisite for T-013 or T-008 in [the staged plan](../plan.md). Resolving that gap requires an additional reviewed method and, for any new physical steps, separate owner authorisation; no HDMI range changes or comparative runs are added here.

C-004's stronger exact-code claim and X-008 are not established by this method, even if screening passes. Measured monotonicity cannot exclude all transforms, gamma changes or subtle channel clipping. C-071's documented Bypass behaviour can gain a bounded observation only; absence of overlays during the run is not proof of universal suppression. Other C-030/C-044/C-059/C-063 implications must be reported with their tested scope, not changed wholesale to Confirmed.

**When to stop:** owner requests it; unexpected device behaviour or menu; signal loss; unknown starting state; unlisted setting/command needed; Bypass unavailable; unknown presenter scaling/transform; unplanned confirmation/advance/closure; meter error/timeout/unexpected prompt; unstable eligible readings or drift beyond the threshold; unexplained clipping/reversal; observed overlay during a reading; uncertain exit or restoration. There is no resend, automatic retry, service-menu entry or automatic recovery.

**Stop rules adopted:** [docs/plan.md stop rules](../plan.md#stop-rules-for-every-physical-stage) at commit `ba099e0a182713945c247636042286e6f9dca626`. Changing these rules or the allowed settings/steps requires a reviewed plan revision and new authorisation for the affected work.

## 8. Owner's authorisation

*To be completed by the owner only, or copied word for word from explicit written authorisation. The request to prepare plans is not authorisation to execute them.*

- Authorised: **No**
- Exact plan commit/revision:
- Reviewed readiness source commit and manifest: unresolved; independent review and local identities/display record required
- Accepted launch/exit instructions and completed display/console record:
- T-003 result and exact accepted meter command/configuration (part M only):
- Steps authorised (V, M, R1; specify exact steps):
- Accepted proposed delay and criteria; any conditions or limits:
- Separate V-A/V-B/V-C runs and repeated geometry accepted; M included if prerequisites met:
- Date:
- Owner's authorisation, verbatim:

## 9. Results

**Not carried out.** Do not prefill expected observations.

- Date carried out:
- Present:
- Differences from the plan:
- Visual observations / part V outcome:
- Meter attempts, excluded patches, statistics / part M outcome:
- Original settings and restoration checks:
- Data files:
- Failures, stops and unresolved questions:

## 10. Conclusions and ledger updates

No equipment conclusion is available. After an authorised run, record the exact configuration and eligible range, visual/optical/restore outcomes separately, and update only the claims actually supported, contradicted or left inconclusive. A clipping-screen pass does not complete T-005's Stage 4 black/white range-interpretation gate. Keep that missing evidence, digital code fidelity, correction validity, absolute accuracy and any untested range explicit. Q-008 is not settled merely because a 2-second wait was used; Q-014's final black-level and pass criteria and Q-001/Q-016 remain open.
