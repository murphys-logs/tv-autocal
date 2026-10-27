# T-005 — SDR signal-path and clipping checks

> **Status: draft plan — NOT AUTHORISED. Do not carry out any step.**
> **Equipment not tested. Ready for independent review, not execution:** the reviewed pattern renderer and its launch instructions are not yet supplied; section 1 lists the remaining execution prerequisites. The T-009 prototype cannot display patterns or take measurements.

Prepared by Codex (OpenAI), 27 October 2026. The choices and numerical thresholds below are **AI design proposals**, not measurements, manufacturer tolerances or an answer already given by the owner.

## 1. Purpose

Screen the recorded PC → Denon → TV path for obvious range mismatch, clipping, changing processing and unstable output. Establish a documented candidate path for later relative experiments. Addresses C-004, C-030, C-044, C-059, C-063 and C-071; uses owner records C-075 and C-079 to C-081. It does **not** establish exact HDMI code values, absolute colour accuracy or a validated correction. X-008 remains open for stronger digital-fidelity claims.

This plan has two separately authorisable parts: **V** (visual checks, no meter) and **M** (optical checks using the Spyder5). Part V can run before T-003; part M cannot. Neither requires Ex-Link or T-006 because the owner exits menus manually. T-003 can take its initial relative readings before T-005 passes; it does not treat its unverified patches as calibration evidence.

**Prerequisites before authorisation:**

- T-001/T-002 owner records in [S-033](../briefs/2026-10-26-owner-equipment-checklist.md) are already available. Recheck only the live starting state in step V1; do not assume it is unchanged.
- An agent must supply a reviewed renderer with a fixed source commit or executable SHA-256, exact local launch/exit instructions, selected display, fixed patch geometry and a machine-readable list of the patterns in section 5. Add these through a reviewed revision of this plan before asking the owner to authorise pattern output. No browser, media-player or other replacement may be improvised during testing.
- Software-only renderer verification must show that it writes the listed **application RGB values** directly to an 8-bit surface, without an additional limited-range conversion, colour profile, gamma transform, scaling, interpolation, animation or audio. Verify patch arrays and captured application buffers against independent expected values. Record the renderer/Windows colour-management path and any unresolved transforms. Buffer checks are not evidence of the HDMI output or TV light.
- The renderer must provide a visible display-selection confirmation before full-screen output, owner-controlled advance/exit, and no meter, TV or receiver control. Full-screen output is confined to the chosen TV display; no automatic sequence starts at launch.
- Record the provisional Q-014 configuration and the owner's acceptance of the **2-second proposed wait** in section 8. This is a starting test value under Q-008, not a settled timing result. Do not tune TV brightness to the 140–160 cd/m² preference in this test.
- Part M additionally needs completed T-003 results documenting a working meter command, a stable warmed-up configuration, neutral-patch repeatability and the usable neutral range. Primary-channel eligibility is assessed from this test's own readings; it is not inferred from gray alone. Use that exact Argyll version/command, instrument mode and correction configuration. No new driver, OEM calibration data, correction file or software installation is included here.
- Independent review and the owner's explicit dated authorisation of the chosen part and exact plan revision are required. Missing renderer identity/launch details or missing T-003 evidence blocks the dependent part, even if the plan has been merged.

**Source basis actually consulted:** owner equipment record and S-033; the merged [proposed stages](../plan.md); S-024's signal-path discussion (AI research); Denon [AVC-X3800H Output Settings](https://manuals.denon.com/AVCX3800H/EU/EN/GFNFSYmlxuhedk.php) (S-030), reconsulted 27 October 2026; NVIDIA [To change the RGB dynamic range](https://www.nvidia.com/content/Control-Panel-Help/vLatest/en-us/mergedProjects/Display/To_change_the_RGB_range.htm), consulted 27 October 2026, live documentation with no revision stated. NVIDIA defines the Full and Limited output options; this does not prove the exact conversions performed by this renderer/driver/TV combination. Denon describes Bypass as removing video processing and preventing information overlays over video, with an IMAX sound-mode restriction; neither claim has been tested here.

## 2. Equipment and settings involved

Use the existing Windows 10 Home 22H2 PC / GTX 1080 / driver 582.78 → Denon HDMI In PC → Monitor 1 → Samsung HDMI 4 path, with the TV's firmware T-JZMDEUC-1270.1. Use only SDR. The owner-reported PC output is 3840×2160 at 60 Hz, RGB, 8bpc, Limited; Windows HDR and Night light are off. TV HDMI Black Level is Auto. Retain those settings for this first screening pass.

**Encoding contract:** every RGB number below is an application-buffer value in the range 0–255. Application black is `(0,0,0)` and white is `(255,255,255)`. Do not substitute `(16,16,16)` and `(235,235,235)` merely because the GPU is set to Limited. A single full-to-limited conversion in the output path is the working hypothesis, not a demonstrated fact; the possible quantisation and transformations must remain in the result's limits. No GPU-Full/TV-Limited comparison is included.

The only proposed setting changes are owner selection of the PC receiver input and TV HDMI 4/Movie mode, and the Denon PC input's Video Mode from its captured original value to Bypass and back. No TV picture slider, white-balance value, colour-space value, HDMI range, Apply Picture Settings scope, Windows profile, GPU lookup table, HDR setting or receiver sound mode is changed. No `dispwin -c` or other calibration-loader command is included.

Part M adds the Spyder5Pro, in the same placement and fixed configuration as T-003. Ex-Link remains disconnected from the TV; no serial or network commands are part of this plan.

## 3. Risks and how to undo them

**No service-menu step is included.** Menu navigation and input/mode selection are by the owner with the ordinary remote. Stop if a menu differs from the recorded procedure, if Bypass is unavailable, or if there is unexpected behaviour. In particular, do not change an IMAX DTS/IMAX DTS:X sound mode to unlock Bypass; revise the plan separately.

Input/mode selection can change the picture seen by normal playback; Denon Bypass changes receiver processing and information displays. Restore the original input selections, original HDMI 4 picture mode and original Denon PC Video Mode in step R1. The TV's reported **Apply Picture Settings: All Sources** is a reason to leave picture sliders and that scope untouched. Do not describe recorded current values as factory defaults.

Write the actual starting values before each corresponding change; the table contains recording fields, not prefilled results. If the known PC range, HDR state or signal route differs from section 2, stop for a reviewed revision instead of changing it to match.

| Device | Setting or state | Original value recorded during authorised session | Restored afterwards? |
|---|---|---|---|
| TV | Active source before session | Not recorded | Not carried out |
| TV | HDMI 4 picture mode before selecting Movie | Not recorded | Not carried out |
| TV | Movie mode HDMI Black Level; Apply Picture Settings; Backlight/Brightness/Contrast; Gamma; Smart LED; Dynamic Contrast; Eco settings (record only) | Not recorded | No changes permitted |
| PC | Output resolution/refresh/format/depth/range; HDR; Night light; assigned colour profile; renderer and display selection | Not recorded | No settings changes permitted; renderer exits |
| Denon | Active input before session; PC input Video Mode; Upscaler; signal format; sound mode | Not recorded | Not carried out |
| Meter (part M) | Placement, instrument mode and correction configuration | Not recorded | Restore T-003/session-start placement after removing meter |

A changed mode may have different settings from S-033; record them before taking readings. Part M requires Smart LED, Dynamic Contrast and the recorded Eco processing to be off in the actual Movie-mode state; if not, stop for a revised plan rather than changing them. This plan does not automatically overwrite them. Unexplained differences that affect range or stability stop the test. On a stop, the owner may restore the listed original values manually if the ordinary menus are understood; no automatic recovery, blind key sequence or continued measurement is permitted.

## 4. Cost

No purchase or paid service is proposed: **£0**. The ledger remains £15.99 spent and £9.01 remaining of the £25 hardware limit. No digital HDMI analyser is assumed available; the resulting evidence cannot claim independent digital code verification.

## 5. Steps

**All steps below are future steps.** The owner operates remotes, launches the reviewed renderer and, in part M, runs the already reviewed T-003 meter command. An agent may record observations and compute statistics with the owner present. These instructions do not authorise an agent to operate hardware.

### Part V — record the path and inspect patterns

1. **V1 — Owner:** verify the authorised plan revision and record the original states in section 3. Select the Denon's PC input and TV HDMI 4; record HDMI 4's current picture mode, then select Movie. Record its relevant settings, without changing them. Confirm the section 2 SDR/PC/range state; a difference stops this run. Exit all menus with the normal remotes, then wait at least 2 seconds. The owner confirms this initial exit is clear.
2. **V2 — Owner:** launch the identified renderer using the reviewed instructions and confirm the target display. Display the geometry pattern once: a one-pixel outer border and labelled corner markers at native 3840×2160. Record whether any edge is cropped or rescaled. If a border/corner is missing or the renderer reports scaling, stop; do not change TV size, GPU scaling or overscan controls under this plan.
3. **V3 — Owner:** show the visual patterns below in order, at most 60 seconds each, advancing manually. Leave at least 2 seconds after each pattern change before judging it. Labels occupy a separate area and never enter a measurement patch. Record each specified comparison as visible / indistinguishable / uncertain. For black, distinguish "looks black" from a measured black level. Gross unexpected colour shifts, crushed/lifted blacks or clipping end this run; do not tune controls until the suspected cause is reviewed.

| Visual pattern | Application RGB values and observation |
|---|---|
| V-black | Neutral bars `(v,v,v)` for `v = 0, 4, 8, 12, 16, 24, 32, 51` on black. Record the first visibly distinguishable bar, and whether 16/32/51 remain distinct from 0 and one another. Failure to distinguish very low bars alone may reflect display/vision limits. |
| V-white | Neutral bars for `v = 204, 230, 242, 250, 255`. Record each adjacent pair; broad merging below 242 is a clipping warning, not permission to lower Contrast. |
| V-red, V-green, V-blue | For each primary in turn, bars with that channel `204, 230, 242, 255` and the other channels 0. Record adjacent distinctions and any colour reversal or loss of detail. |
| V-detail | Alternating one-pixel red/blue vertical lines beside one-pixel black/white lines, plus native-pixel text. Record visible smearing/cropping. This is a visual spatial-detail screen, not proof of RGB 4:4:4 delivery. |

4. **V4 — Owner:** stop the renderer at neutral application gray 128. In the Denon PC input's ordinary Video → Output Settings menu, set Video Mode to Bypass. If unavailable, stop without changing sound mode. Exit the receiver menu and TV menu if opened, wait at least 2 seconds, and confirm this exit is clear. Repeat the V3 visual sequence exactly once in Bypass. Do not deliberately trigger volume/status banners. Record observed differences and any unexpected overlay; absence during this short observation does not prove overlays can never occur.
5. **V5 — Owner and agent:** record the visual outcome against section 7. If only part V is authorised, carry out R1 and finish with a **visual-only partial result**. Part M needs its own explicit inclusion in section 8 and all T-003 prerequisites.

### Part M — bounded optical checks in Bypass

1. **M1 — Owner:** use T-003's fixed meter configuration on the unchanged input/Movie/range settings and Denon Bypass state recorded in part V. Keep the central gray-128 patch displayed for at least the warm-up duration established by T-003 before M2; record elapsed time and hold the configuration fixed. Use the same reviewed command as T-003: `spotread.exe -O -e -x -Y n <unique-local-attempt.log>`, with the logfile last and no external correction. The exact accepted command and configuration must be copied from the completed T-003 record before authorisation. No installer, `oeminst`, profile loader or alternative command is allowed here. Stop on errors or unexpected prompts. Use the same central 960×540 patch on RGB 0 surround, occupying 25% of width and 25% of height, with no text beneath the meter.
2. **M2 — Owner:** show gray 128, exit menus if inspected and wait at least 2 seconds, then take five consecutive readings, allowing at least 2 seconds before each launch. Apply that inter-reading wait throughout part M. Record finite XYZ and luminance Y; reject nothing merely for being inconvenient. If these readings fail T-003's stable-repeatability criterion, stop before the ramp.
3. **M3 — Owner:** show neutral patches in the fixed order `0, 13, 26, 51, 102, 153, 204, 230, 242, 255`, where each code sets all three channels. At each patch wait at least 2 seconds after presentation, then take three consecutive readings. Codes at or above T-003's lowest usable tested neutral code are candidates for this run's monotonicity check, not presumed already verified. Lower codes 0/13/26 may be measured diagnostically only if T-003 returned finite readings for that code within its timeout; otherwise mark them **unmeasurable under the established configuration**, not zero. Retain noisy low readings as diagnostic/inconclusive. Then show gray 128 and take five reference readings. Stop on an unexpected plateau/reversal above the usable floor or failed drift criterion; do not continue to colour checks.
4. **M4 — Owner:** for red, then green, then blue, show application channel values `204, 230, 242, 255`, other channels 0. Wait at least 2 seconds after each presentation and take three readings. Then show gray 128 and take five final reference readings. This is a high-end channel clipping screen; it does not assess Rec.709 gamut accuracy or D65.
5. **M5 — Agent with owner present:** calculate the predeclared statistics in section 7 and retain all valid, invalid and omitted attempts. Do not adjust the display to obtain a pass. The maximum is **81 meter invocations** (15 gray-reference readings, 30 neutral readings and 36 primary readings), fewer where low patches are ineligible. There is no automatic retry. Each invocation uses T-003's approved timeout; any failure stops the run rather than extending the count.

### Restoration

1. **R1 — Owner:** on normal completion, restore the Denon's captured original PC Video Mode, the captured original HDMI 4 picture mode, and the original receiver/TV source selections. Inspect the restored values in normal menus, exit, and wait at least 2 seconds. Do not take more readings after returning to another source or mode. Close the renderer and remove the meter if part M used it. Record each restoration separately. On an earlier stop use only the manual restoration procedure in section 3; stop further project work if restoration is uncertain.

## 6. What will be recorded

Record the plan revision, authorisation, dates/times, participants, source/firmware/software versions, renderer commit/hash/launch method and output-display choice, every setting in section 3, pattern definition/hash and geometry, and the chronological observation table. Keep machine-specific paths and original logs in ignored `local/`; sanitise copies before committing. No device serials, network addresses or personal path components belong in the public results.

For part M, additionally record one row per attempt: unique ID, purpose **T-005 diagnostic only**, patch application RGB, input/mode/settings, start/end times, exact meter command/version, display/instrument mode, correction filename/hash and validation status (or `none / not applicable`), raw XYZ, return/error state and acceptance/rejection reason. Preserve every rejected attempt and every omitted low patch. Include the T-003 eligibility/noise evidence; never silently substitute predicted HDMI values or target luminance for observations.

**Measurement cycle:** V1/V4 establish the owner-controlled menu-exit method. After any menu inspection or permitted setting change, the owner exits all opened menus and waits at least 2 seconds before the next reading. Each patch change also gets at least 2 seconds. Subsequent readings of an unchanged patch require that preceding exit/wait to be complete, not another menu visit. Restoration follows change → exit → wait, with no reading when returning to the original non-test state. No Ex-Link menu-exit mechanism is exercised. An observed overlay invalidates the affected attempt and ends the run; this plan provides no automatic overlay detector and does not require inspecting the whole screen before every reading.

## 7. How results will be judged

The following are proposed screening thresholds to agree **before execution**. They do not certify absolute accuracy or derive from a manufacturer specification.

| Check | Proposed interpretation |
|---|---|
| Recorded path and geometry | Every setting and renderer identity is recorded; native border/corners are visible. A missing record, crop or unexplained transform makes the relevant part inconclusive. |
| Visual levels | All observations retained. Broad merging/reversal of the 16/32/51 dark bars or of the 204/230/242/255 high bars requires explanation before a pass. The visibility of 4/8/12 or 250 is reported without requiring the owner to resolve one-code differences. Visual black appearance alone cannot establish correct black decoding. |
| Repeatability and drift | Gray-128 groups satisfy T-003's accepted repeatability limit. Their mean Y differs from the first group by no more than 2%; otherwise the optical run is inconclusive and stops. This 2% is a test policy, not an accuracy claim. |
| Usable neutral and high-primary steps | For each adjacent eligible group, mean Y must increase by more than `max(3 × sqrt(s_a²/n_a + s_b²/n_b), 2q)`, where `s` is the sample standard deviation, `n = 3`, and `q` is the coarser of the two groups' reported Y decimal increments. Also report raw ranges and rounded output precision; identical printed readings do not establish zero uncertainty. A plateau/reversal or a difference indistinguishable from noise is inconclusive (possible clipping/instability), not automatically a bad TV. No extra runs are implied. |
| Low-light limitation | Record results below the T-003 usable floor as inconclusive and list omitted patches. No assumed black value is substituted; no gamma/BT.1886 target is calculated. |
| Denon comparison | Record Auto-versus-Bypass visual behaviour only. Part M qualifies the Bypass configuration; it does not measure equality to Auto or prove the receiver passes identical digital values. |

A **limited signal-path screening pass** requires complete V and M records, no unexplained level/clipping/geometry problem in the eligible tested range, acceptable repeatability/drift, and confirmed restoration. If required near-black evidence cannot be obtained, record **partial/inconclusive** with the verified range rather than a blanket pass. An independent review must judge whether that bounded evidence is sufficient for a particular T-013 plan. No result here authorises T-013 or T-008.

C-004's stronger exact-code claim and X-008 are not established by this method, even if screening passes. Measured monotonicity cannot exclude all transforms, gamma changes or subtle channel clipping. C-071's documented Bypass behaviour can gain a bounded observation only; absence of overlays during the run is not proof of universal suppression. Other C-030/C-044/C-059/C-063 implications must be reported with their tested scope, not changed wholesale to Confirmed.

**When to stop:** owner requests it; unexpected device behaviour or menu; signal loss; unknown starting state; unlisted setting/command needed; Bypass unavailable; unknown renderer scaling/transform; meter error/timeout/unexpected prompt; unstable eligible readings or drift beyond the threshold; unexplained clipping/reversal; observed overlay during a reading; uncertain exit or restoration. There is no resend, automatic retry, service-menu entry or automatic recovery.

**Stop rules adopted:** [docs/plan.md stop rules](../plan.md#stop-rules-for-every-physical-stage) at commit `ba099e0a182713945c247636042286e6f9dca626`. Changing these rules or the allowed settings/steps requires a reviewed plan revision and new authorisation for the affected work.

## 8. Owner's authorisation

*To be completed by the owner only, or copied word for word from explicit written authorisation. The request to prepare plans is not authorisation to execute them.*

- Authorised: **No**
- Exact plan commit/revision:
- Reviewed renderer identity/hash and exact launch/exit instructions:
- T-003 result and exact accepted meter command/configuration (part M only):
- Steps authorised (V, M, R1; specify exact steps):
- Accepted proposed delay and criteria; any conditions or limits:
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

No equipment conclusion is available. After an authorised run, record the exact configuration and eligible range, visual/optical/restore outcomes separately, and update only the claims actually supported, contradicted or left inconclusive. Keep digital code fidelity, correction validity, absolute accuracy and any untested range explicit. Q-008 is not settled merely because a 2-second wait was used; Q-014's final black-level and pass criteria and Q-001/Q-016 remain open.
