# T-003 — Spyder5 recognition and diagnostic repeatability

> **Status: draft plan for independent review — NOT AUTHORISED. Do not carry out any step.**
> No instrument, display, receiver or cable was operated while preparing this plan. The owner's request to prepare it is not permission to run it.
> **Execution blockers:** independent review of the proposed software readiness revision and this amendment, unresolved local/display inputs listed below, and explicit owner authorisation. Earlier component versions were reviewed; the revised presenter and meter runner still have no Windows/equipment validation.

Author: Codex (OpenAI), 27 October 2026. Baseline: `ba099e0a182713945c247636042286e6f9dca626`. Numerical limits below are **AI: Codex diagnostic proposals**, not published accuracy guarantees or owner decisions.

Execution amendment: Codex (OpenAI), 28 October 2026, for the proposed [readiness revision](../software/component-readiness.md) based on merged PR #26 at `dc552c737ec61d5b323ceda844fd198785170c61`. The [shared execution record](component-execution.md) is part of this proposed plan. Bind the final independently reviewed source/manifest before authorisation; the older PR #25 tools do not implement this revision's controls. No future reviewed plan SHA or authorisation is supplied here.

## 1. Purpose

Establish whether the installed ArgyllCMS can identify the owner's Spyder5Pro and produce actual XYZ measurements, then measure repeatability, warm-up drift and a provisional usable low-light range under one fixed setup. XYZ are the three reported colour-measurement components; Y represents luminance. A successful process exit alone is not a measurement.

This addresses C-002, the access portion of C-041, C-056, C-068 and X-011. It collects bounded evidence relevant to C-043/C-072 without adopting another meter's reported low-light floor. It does not deliberately test the interrupted-driver behaviour in C-069. C-082 supplies the owner's descriptive baseline. Neither repeatability nor this plan validates colour accuracy, a spectral correction, HDMI code fidelity or any TV control.

**Prerequisites and scope:**

| Requirement | Current state / action before the relevant step |
|---|---|
| T-001/T-002 owner baseline | Complete in [S-032](../briefs/2026-10-26-pr19-rulings-and-equipment-confirmations.md) and [S-033](../briefs/2026-10-26-owner-equipment-checklist.md); use these records, then record the actual session settings without treating the earlier values as factory defaults. |
| Independent review and owner authorisation | Pending. Authorisation must identify this plan's reviewed commit, date and exact steps. Discovery-only steps 1–4 may be authorised separately. |
| Meter installation | ArgyllCMS V3.5.0 is reportedly unpacked; USB driver access has not been demonstrated. Driver installation, replacement, `oeminst` and vendor-data extraction are outside this plan. Discovery failure stops the session for a separate proposal. |
| Serial-device isolation | Before **any** ArgyllCMS launch, including `spotread -?`, the owner must record and disconnect the Ex-Link cable's **USB end from the PC** and keep its TV end disconnected. It stays disconnected throughout this test. If another non-meter serial device is connected, stop for a scope amendment; do not discover it by probing. |
| Presenter and meter runner for steps 5–11 | The proposed readiness source and hashes are identified in the [shared software record](component-execution.md#reviewed-software-and-local-inputs); this revision needs independent review. The sequence/launch mapping is below. Actual Python/Tk/driver availability, the installed Argyll executable identity and the display workflow remain unverified; no substitute renderer or direct measurement launch is permitted. |
| **Unresolved owner input — display/console arrangement (Q-019)** | The owner can, and probably will, connect a second screen; its availability remains unconfirmed. This revision requires one for the visible operator window. The [display procedure](component-execution.md#display-and-console-arrangement) must resolve both window positions and their acquisition method/authorisation, console placement, button access and a console-focus check before typing. No connection or display-setting change is carried out by this amendment. |
| Timing and diagnostic scope | Owner accepts the proposed 2.0-second minimum wait and section 7 limits for this test (Q-008). This does not settle a production delay. Q-014's existing Movie/HDMI 4/dim-room preference is sufficient; do not adjust brightness to achieve 140–160 cd/m² here. |
| Correction policy | This plan uses Argyll's generic calibration with no external `-X` file or inherited correction environment variables. Follow the [isolated launch environment](#isolated-launch-environment). The owner must explicitly accept these **uncorrected diagnostic readings only** within this plan. Q-001/T-004/Q-016 remain open for calibration. |

**Still needed from the owner before execution:** final display/console arrangement for steps 5–11; acceptance of the proposed wait, diagnostic thresholds and generic readings; and dated permission for exact reviewed steps. The [shared unresolved-input list](component-execution.md#unresolved-inputs) separates these decisions from missing installation/evidence records. Discovery-only steps 1–4 do not require a presenter, but still require their own review, isolation, executable identity and authorisation.

T-005 need not pass before these initial relative meter checks: the unchanged signal path is recorded as unvalidated. T-006 is not a prerequisite because the owner exits menus manually. Neither arrangement authorises Ex-Link operation or a later test.

**Sources consulted for this plan, 27 October 2026:** Graeme Gill/ArgyllCMS, [spotread documentation](https://www.argyllcms.com/doc/spotread.html) (S-014: `-O`, `-e`, `-x`, `-Y`, logfile and discovery behaviour) and [instrument documentation, Spyder 5 section](https://www.argyllcms.com/doc/instruments.html) (S-014: generic default calibration and optional CCSS/vendor data). C-068 and X-011 carry forward the reviewed mode interpretation in S-029. Fresh, software-only inspection of the [V3.5.0 source archive](https://www.argyllcms.com/Argyll_V3.5.0_src.zip) (S-037; SHA-256 `f8576ce5589fd15620abb73ff049ea31f55ddbd1bba6d1ffa87452658e7bc85f`) checked discovery, environment defaults and C-069's abort warning. No Argyll program was run. These sources do not establish the owner's installed binary or cable's behaviour.

The source's `spectro/spotread.c` lines 464 and 1192 build a port list for help and measurement launches. `spectro/icoms_nt.c` lines 93–99 and 125–135 identify and probe Windows VCP/USBSER ports; `spectro/inst.c` lines 1455–1456 and 1499–1544 open ports and send identification bytes. Fast serial support is enabled in the source build defaults (`Jamtop` line 41; `spectro/Jamfile` lines 101–102). The owner's actual adapter classification has **not** been checked. Thus omitting `-c` or unplugging only the TV end does not establish that the USB serial adapter receives no traffic. [Environment documentation](https://www.argyllcms.com/doc/Environment.html#ARGYLL_EXCLUDE_SERIAL_SCAN) describes `ARGYLL_EXCLUDE_SERIAL_SCAN`, but its effectiveness on this installation is untested; it is not a substitute for physical USB disconnection in this plan. Concurrent measurement and Ex-Link use requires a separately reviewed solution before T-013/T-008.

That variable takes a semicolon/comma-separated list of exact port names, **not a Boolean switch**. In S-037, `spectro/icoms.c` lines 580–624 parse the list and lines 640–656 compare each entry with the port path using exact string equality. Setting it to `1` does not disable all serial scanning. No exclusion setting is relied on here.

## 2. Equipment and settings involved

- Owner's Windows 10 PC, GTX 1080, existing ArgyllCMS V3.5.0, Spyder5Pro and existing USB connection.
- Samsung UE49KS7000UXXU and Denon AVC-X3800H on `PC HDMI → Denon PC input → Monitor 1 → TV HDMI 4`.
- Ex-Link is unused. Keep the cable disconnected at **both the PC USB end and the TV end** before and throughout every Argyll launch. Argyll discovery may itself open/probe serial ports; no claim of a passive COM-port listing is made.
- Retain the recorded pipeline: 3840×2160 at 60 Hz, RGB, 8 bpc, NVIDIA Limited, Windows HDR/Night light off, TV HDMI Black Level Auto and Denon Video Mode Auto. Record any mismatch and stop for a plan amendment; do not silently normalise it.
- The owner may select the already agreed HDMI 4 input and Movie mode after recording the starting input/mode. No numerical picture control, GPU setting, LUT/profile or receiver setting is changed. Confirm the existing enhancement settings in [equipment.md](../equipment.md); a mismatch stops preparation.
- For readings, the reviewed presenter must show a centred **960×540 pixel** uniform patch on a black (`RGB 0,0,0`) surround. Meter stays flat at its centre. Patch values are equal-channel application RGB codes, **not demonstrated HDMI code values or known luminance percentages**.

The ordinary controls in Movie mode can differ from the values recorded during the earlier checklist, whose active mode was not explicit. Record this session's actual mode and values; do not substitute checklist values or change sliders to match them.

## 3. Risks and how to undo them

**No service menu is used.** Do not change white balance, brightness, backlight, gamma or colour controls. Repeated static patches, meter pressure or an unsecured cable are avoided by the fixed duration, supported counterweight and the owner's ability to stop. Stop if mounting cannot be done without strain.

The meter may be unavailable because its driver is missing or another program holds it. Close ordinary measurement programs before starting, but do not uninstall software or stop system services. C-069 warns that aborting the driver may leave pending meter data; the same source attempts to flush stale data on startup (`spyd2.c` lines 2973–2989). This is not evidence of permanent damage or a validated recovery method. There is no automatic kill, retry, USB reset or replug recovery in this plan. The owner retains the right to stop; the [stop procedure](#stopping-and-an-outstanding-reading) explains an unfinished reading.

Original session values must be recorded before changes; all cells below are deliberately blank observations:

| Device | Setting | Original value | Restored afterwards? |
|---|---|---|---|
| TV | Power state; input; picture mode | Not recorded | Not performed |
| TV | Current Movie settings: backlight, brightness, contrast, gamma, colour tone and enhancements | Not recorded | No slider changes permitted |
| PC / Denon / TV | Output format/range; HDR/Night light/profile state; receiver Video Mode; TV HDMI Black Level | Not recorded | No changes permitted |
| PC | Applications closed for the session; presenter display and window state | Not recorded | Not performed |
| PC | Presence/value of the two correction environment variables; dedicated launch console | Private local record pending | Parent/user/machine environment unchanged; close dedicated console |
| Ex-Link cable | Original USB/TV connection state; both ends disconnected before any Argyll launch | Not recorded | Leave both ends disconnected; reconnection requires its own authorised scope |
| Spyder5 | Initial USB connection and mounting state | Not recorded | Not performed |

On normal completion the owner closes the presenter, restores the original input/mode using normal menus, exits and waits 2.0 seconds, then restores the original physical meter arrangement after the measurement program has exited. Close the dedicated launch console only after every measurement process has completed, and leave both Ex-Link cable ends disconnected. No reading is taken after changing away from the diagnostic input; the final comparison reading is deliberately before that restoration. On abnormal behaviour, follow the [stop procedure](#stopping-and-an-outstanding-reading); the owner may manually restore recorded ordinary settings as described in the pinned stop rules. Do not send further equipment commands or restart/replug the meter as an assumed recovery.

## 4. Cost

No purchase or paid service. Proposed extra spend: **£0**; project total remains **£15.99 spent / £9.01 remaining**. Use the existing installation. No vendor binary, calibration data, correction file or ArgyllCMS executable is committed or redistributed.

## 5. Steps

Every action below is a **future authorised action**, not an instruction to execute during review. The owner operates the equipment and launches each command; an agent may record and analyse results with the owner present. No unattended script or measurement loop is authorised.

1. **Owner and agent:** verify the authorisation covers the steps about to be performed and record the plan commit. Record the Ex-Link cable's original connection state, disconnect its USB end from the PC, and check its TV end is disconnected. Keep both ends disconnected throughout this test and recheck before every launch. Close DisplayCAL/other measurement applications and prepare the [isolated launch environment](#isolated-launch-environment). Identify the existing `spotread.exe` path privately. Record its version from its output when run and calculate its SHA-256 by ordinary file reading. Do not run any other calibration executable.
2. **Owner:** record section 3 baselines. For discovery-only authorisation leave TV/receiver settings unchanged. Connect the Spyder5 to the existing PC USB port if not already connected; record the driver name/version already shown by Windows Device Manager, without installing or changing it. If an installation prompt appears, stop.
3. **Owner:** after rechecking both Ex-Link ends are disconnected and the isolated environment, run exactly `spotread.exe -?` using the identified executable. This is **instrument/port discovery and a physical step**: it can open and write to serial devices during discovery. Record the version, discovered instrument and selectable display types with device identifiers kept private. Stop if Spyder5 is absent, the device is ambiguous, the version differs from 3.5.0 or generic non-refresh type is unavailable. Do not guess a `-c` index or use the Ex-Link COM port.
4. **Owner and agent:** if only discovery was authorised, stop here and record the discovery result. After the discovery process exits normally, close the dedicated console and restore the initial meter connection arrangement; leave Ex-Link disconnected and TV/receiver settings unchanged. If the process remains outstanding or failed unexpectedly, use the stop procedure instead. No readings or TV patterns are permitted. For further steps, confirm the presenter prerequisite and explicit authorisation are satisfied, with exactly one supported measurement instrument available and the command's default instrument unambiguous.
5. **Owner:** record start time and whether the TV was already warm. If needed, turn it on with its normal remote, select HDMI 4 and Movie mode, and record the Movie settings without changing numerical controls. Set up the agreed dim room. With the centre of the TV still unobstructed by the meter, launch the presenter using the [execution mapping](#reviewed-tool-execution-mapping); inspect the intended TV, click **Confirm TV target** in the separate operator window, then click **Next pattern** once to apply frame 1, `RGB 128,128,128`. Keep frame 1 held, then mount the Spyder5 flat at its centre using the counterweight, without pressing it into the panel. Exit normal TV/receiver menus using the owner-operated remotes and wait at least **2.0 seconds** after menus have disappeared and the patch is stable. If an unexpected overlay/menu appears, stop; no automated screen check is claimed.
6. **Owner:** with that patch unchanged, launch one meter-runner attempt with purpose `initial-access`, using the mapping below. Record actual finite XYZ/Yxy output and process completion. If output is calibration-only, erroneous, incomplete, non-finite or names the wrong instrument, reject the attempt and stop; do not repeat automatically. A valid initial reading establishes access only, not repeatability or accuracy.
7. **Owner:** retain the mid-grey patch and fixed setup. At **30, 35 and 40 minutes after step 5**, take **five consecutive readings per block**, each separately launched and logged. Record actual times; if a block takes longer than its five-minute slot, finish that block normally and stop the schedule as timing-inconclusive. The minimum 2.0-second wait applies before every new reading, including unchanged-patch repeats. At the end of the three blocks apply section 7's stability limits. If they fail, end the session; do not extend warm-up or loosen limits during the run.
8. **Owner:** once step 7 passes, display each of `RGB 255,255,255`, `51,51,51`, `26,26,26`, `13,13,13`, `5,5,5`, and `0,0,0` in that order, with the same geometry and surround. After each change, ensure the previously established menu exit remains complete, wait at least 2.0 seconds and take **five readings**. No menu or numerical control changes occur. The low-light sequence intentionally probes noise: a finite result that fails the predefined low-light reliability criterion is retained as diagnostic data, not silently dropped. Hardware/protocol errors or other stop events still end the session immediately.
9. **Owner:** return to `RGB 128,128,128`, wait at least 2.0 seconds and take **five final readings**. Compare with the final warm-up block using section 7. A failed end check makes the range assessment inconclusive, without erasing the initial access result.
10. **Owner and agent:** retain all attempts, including rejected ones. Record the passing code range and any failed/indistinguishable low-light patches, without extrapolating below the tested codes or adopting a black-level value. Do not adjust the TV in response to results.
11. **Owner:** complete normal restoration from section 3, record each restoration, and stop. There are at most **51 reading launches** (one initial, 15 warm-up, 30 range, five final). Do not add a repeat run, new correction or recovery sequence under this authorisation.

### Reviewed tool execution mapping

These are **argument specifications for future review and authorisation, not commands to run now**. Use the source-run `tv_autocal_tools` entry point and exact interpreter recorded in the [shared software record](component-execution.md#reviewed-software-and-local-inputs). Every tool launch also needs the common `--hardware`, `--permit`, exact `--confirm` and fresh `--log` fields defined in the [authorisation/launch record](component-execution.md#authorisation-and-launch-record), with plan `T-003`. All unresolved values stay labelled **UNRESOLVED**; do not substitute this preparation request as permission.

| Tool | Required plan-specific argument values |
|---|---|
| `present` — one run for steps 5–10 | `--sequence t003`; `--x`/`--y` are the confirmed nonnegative TV desktop origin; `--control-x`/`--control-y` position the operator window wholly within a different display's usable area. Both positions remain **UNRESOLVED**. Use a fresh presenter journal under `local/T-003/`. |
| `meter` — one run per scheduled attempt | `--executable` and `--sha256` identify the locally reviewed Argyll V3.5.0 executable; `--attempt-log` is a fresh simple filename directly under `local/T-003/`, different from the evidence `--log`; `--presentation-log` names the still-open presenter journal; `--presentation-sequence`, `--rgb` and `--purpose` come from the table below. Use `--wait-ms 2000 --timeout-ms 60000` only after owner acceptance; include `--isolated --exit-confirmed --discovery-confirmed` only when each statement is true. |

The meter tool performs **no separate discovery command**. Step 3's separately authorised `spotread.exe -?` remains outside the wrapper and must finish successfully before `--discovery-confirmed` can be used. Each subsequent `spotread` measurement child still builds its instrument/port list and may probe serial ports at startup (C-090); this is why isolation is rechecked before every attempt. Discovery output, its exit state and exact executable hash belong in the private evidence record; no help/discovery was run while preparing this amendment.

| Plan step | Presenter frame (`--presentation-sequence`) | `--rgb` | `--purpose` | Maximum attempts |
|---|---:|---|---|---:|
| 6 | 1 | `128,128,128` | `initial-access` | 1 |
| 7, 30 / 35 / 40 minutes | 1, held without advance | `128,128,128` | `warmup-30` / `warmup-35` / `warmup-40` | 5 each |
| 8 | 2 / 3 / 4 / 5 / 6 / 7 | `255,255,255` / `51,51,51` / `26,26,26` / `13,13,13` / `5,5,5` / `0,0,0` | `range` | 5 per frame |
| 9 | 8 | `128,128,128` | `end-check` | 5 |

Before each launch, match the intended RGB and frame number to the journal's latest `pattern_present_intent` and completed `pattern_buffer_applied` pair. The frame number is the event's **`fields.sequence`**, not the journal's top-level event counter. The runner checks the renderer hash and this receipt before and after the attempt; a receipt is not proof the display is still visible. Keep the patch unobstructed and unchanged until the meter runner has finished and its evidence has been checked. Do not advance or close the presenter while an attempt is outstanding.

After each completed block, click **Next pattern** once per next frame in the operator window, only when no reading is outstanding. Use the still-required [operator-access/console-focus procedure](component-execution.md#display-and-console-arrangement); before typing or editing a meter command, check that the meter console has focus, without using typing as the test. Ordinary presenter-window typing does not confirm or advance; Escape still stops if either presenter window has focus. Do not move either presenter window or minimise the controls, including through Win+D/Win+M or the taskbar; if this happens, abandon the run under the shared procedure even if it does not close automatically. An unplanned confirmation, advance or close also stops the run. There is no automatic schedule or restart after failure. Use the visible **Stop presentation** button for presenter closure; callback interruption is treated as failure with attempted closure, not a validated native stopping/recovery method.

After all final readings and evidence checks, intentionally click **Stop presentation**, or click **Next pattern** once after frame 8. For a planned normal boundary require `presenter_closed.fields.reason` to be exactly `owner requested stop` or `manual advance after final pattern`, matching the owner's recorded intended action, plus `presenter_closed.fields.close_completed: true`, disappearance of both windows, normal CLI exit and final `journal-close` with `complete: true`. The new closure field records successful return of the close calls, not physical verification; false or absent stops the plan. Those reasons do not make an early or accidental close a normal completion. Any other reason (including either time limit, `window loop ended` or `failure: …`) stops the plan; an absent or failed record leaves completion unconfirmed. The three-hour lifetime remains a hard stop, never permission to restart or ignore an outstanding process. Native geometry checks do not establish HDMI fidelity or absence of overlays.

### Isolated launch environment

These are future authorised preparation steps, not actions during review. Use one dedicated PowerShell console for discovery and meter attempts, and a separate console for the presenter, whose run occupies its launch console. Privately record whether `ARGYLL_COLMTER_CAL_SPEC_SET` and `ARGYLL_COLMTER_COR_MATRIX` are present and their original values, then remove both from **the discovery/meter console process's environment only**. Verify that both are absent before discovery and every measurement launch; stop if that cannot be established. The wrapper additionally removes both keys from its child-environment copy: that is a second safeguard for readings, not a replacement for the shell checks that also cover direct discovery. Do not edit the Windows user or machine environment, and do not launch through DisplayCAL or another wrapper that may supply a correction. Close the dedicated console after all measurement processes have completed; the original parent/user/machine environment remains unchanged.

Omitting `-X` alone is insufficient: `spotread.c` lines 1150–1158 and `doc/Environment.html` lines 128–136 in S-037 show that these variables can supply a default correction. No correction file is loaded or inspected as part of this test.

**Allowlisted child invocation made by the meter runner, for steps 6–9 only:**

```text
spotread.exe -O -e -x -Y n <unique-local-attempt.log>
```

This describes the runner's fixed child argument list; it is **not an alternative direct-launch procedure**. The path/hash and fresh logfile are resolved in the authorised local record, never by copying this placeholder. The wrapper places the logfile last, **not immediately after `-O`**, removes both correction defaults from a copy of its environment, and records raw output and exit evidence in its separate journal. `-e` selects emissive readings; `-x` requests Yxy display; uppercase `-Y n` forces non-refresh mode. The documented Spyder5 default uses generic non-refresh calibration. No external correction (`-X` or either environment default) or unsupported no-calibration option (`-N`) is used.

### Stopping and an outstanding reading

`-O` can perform one calibration or measurement and exit; require an actual XYZ result. Do not answer an unexpected calibration prompt or send keys as an improvised workaround. A normal stop means launch no more readings and let an in-flight reading finish before closing its console. The owner may request an immediate stop at any time.

If a launch has not returned within **60 seconds**, record a diagnostic timeout and stop the test schedule. Report whether the process is still running; do not automatically kill it, restart it or replug the meter. For the direct discovery launch, the owner may leave it running to finish or exercise their unconditional right to stop PC activity, including closing its console, ending that process or shutting down. These are descriptions of the owner's right, not validated meter-reset or project-recovery procedures; an interruption may abort the driver and leaves completion unconfirmed. Record any owner-directed interruption and reject the unfinished attempt. The agent does not initiate recovery. Before further project meter operation, review the outstanding state and obtain specific authorisation for a recovery/resumption procedure. This deadline is a workflow limit, not an established measurement-duration bound.

Wrapped readings use a separate child process with no console window and piped output. Closing the wrapper's console must not be assumed to stop `spotread.exe`: the child may remain running without a window, holding the meter while further output is lost. This is an untested consequence identified in Claude Code's (Anthropic) review and considered in the [shared abnormal-stop gate](component-execution.md#meter-attempt-and-closure), not an observed Windows result. Ending the wrapper and ending its child are different actions; neither is prescribed as recovery here. The exact interruption/console/cable procedure for wrapped attempts remains unresolved before authorisation, while the owner's right to stop remains unconditional.

For wrapped readings, follow the [meter attempt and closure procedure](component-execution.md#meter-attempt-and-closure). A timeout rejects the attempt while the wrapper remains attached to the child and drains output. Python-delivered SIGINT requests, normally Ctrl+C, are latched throughout launch/supervision/cleanup; repeated requests do not escalate to killing the child. Ctrl+Break is unsupported, is not covered by that policy and must not be used as an alternative project stop action; if it occurs, apply the shared abnormal-stop gate. Native delivery remains untested, and no shutdown by 60 seconds is promised. Keep the held patch and both consoles until normal completion unless the owner chooses an interruption. The owner can stop at any time. A disappearing presenter, three-hour expiry or any interruption makes the affected reading unusable and stops further work; do not extend the presenter lifetime or reopen it to salvage the attempt.

The final meter JSON has **no `closed` field**. Privately retain `wrapper_pid`, `child_pid`, `child_exit_confirmed`, `readers_complete`, `exit_code`, `accepted`, `reason`, `timed_out`, `cancelled`, `capture_complete` and `log_complete`, together with lifecycle/raw stream events, `meter_exit`, the CLI outcome and the final `journal-close` record. Child exit and completion of both readers are distinct requirements; identity/status notices do not prove driver safety. JSON is printed before final journal closure; `accepted: true` alone is insufficient if that closure subsequently fails. Missing/failed closure evidence or an outstanding process is not successful completion. Discovery is not supervised by this runner; retain its separate terminal result and treat unknown completion under the same stop boundary.

## 6. What will be recorded

All readings are **relative diagnostic evidence only**, permanently excluded from calibration data or absolute-accuracy claims. A header records the reviewed plan commit, authorisation text/date, operator, TV/receiver/OS/GPU/driver versions, Argyll version/executable hash, discovered instrument and active generic display type, absence of both correction environment defaults in the launch process, Ex-Link disconnection checks, presenter identity/hash, dimensions and source RGB encoding, viewing conditions, warm-up start and unchanged signal-path settings. Exact paths, inherited environment values and device serial identifiers stay in ignored local records.

For each attempt record a unique ID; purpose (`initial-access`, `warmup-30`, `warmup-35`, `warmup-40`, `range`, `end-check`); start/end time; exit code or outstanding state; raw XYZ and Yxy; application RGB code/window/surround; input/mode/settings; correction filename **none** and correction hash **N/A**; generic calibration **not validated for this TV**; wait start/end; and acceptance/rejection reason. Keep all raw attempts before computing statistics. No removal of inconvenient values or median-only retention.

**D-013:** initial input/mode preparation and every normal-menu inspection are followed by owner manual exit, then at least 2.0 seconds before reading. Patch changes also receive that wait. Repeated readings do not require reopening menus; they require the preceding exit to remain complete and the wait to be observed. Failed/uncertain exit or an unexpected overlay stops the run. This plan does not test the program's Ex-Link exit method or detect overlays automatically.

Rejected protocol/output attempts remain in the record with reasons and stop the session. Finite low-light samples outside the numerical reliability envelope remain valid *noise-characterisation observations*, marked unusable for later feedback. Do not promote them into calibration evidence. Publish only privacy-checked result extracts and data under a future reviewed change to `docs/tests/T-003-data/`; raw logs remain ignored locally.

## 7. How results will be judged

These criteria are fixed **before** execution and need owner acceptance as part of authorising the plan. They are pragmatic proposed diagnostics, not Delta-E targets, model specifications or proof of correction validity.

For each five-reading block compute arithmetic mean and sample standard deviation (SD) of Y; coefficient of variation `CV = 100 × SD(Y) / mean(Y)` when the mean is positive; and the ranges `max(x)-min(x)` and `max(y)-min(y)`. SD describes the spread of repeated readings; CV expresses that spread as a percentage of their mean. Finite XYZ values remain required, including at code 0. If their sum is zero/non-positive, x/y are not valid colour coordinates: retain the raw output, mark chromaticity undefined and do not calculate its statistics. Undefined x/y in that case does not by itself reject otherwise finite XYZ noise data. A nonzero code with any such sample cannot pass the usable-range criterion; the zero patch never needs to pass an x/y criterion.

For range comparisons use step 8's five-reading blocks at codes 0, 5, 13, 26, 51 and 255, plus the **40-minute** five-reading block at 128. Compare exactly these ascending pairs: **0→5, 5→13, 13→26, 26→51, 51→128, 128→255**. Do not pool the initial or other warm-up/final blocks into these comparisons. End stability must pass before interpreting the pairs.

A pair is distinguishable only if `mean(Y_high) − mean(Y_low) > max(3 × sqrt(SD_low² + SD_high²), 2q)`, where `q` is the coarser printed Y increment in that pair's raw output (for example, four decimal places means an increment of 0.0001). Record `q`; if output precision is unknown, the pair is inconclusive. In plain English, the rise must exceed both the proposed noise margin and two printed increments; rounded identical repeats cannot provide an arbitrarily small pass threshold. This is a diagnostic proposal, not a formal confidence interval.

| Check | Proposed interpretation |
|---|---|
| Access | Correct Spyder5 identified, and one command returns exactly one finite XYZ result plus a completed successful process. No result with a successful exit is **inconclusive**, not a pass. A discovery/driver error identifies a failed setup, not proof the meter can never work. |
| Mid-grey repeatability | Every warm-up block has positive mean Y, CV ≤1.0%, and both chromaticity ranges ≤0.002. A failure blocks use for the later relative-feedback experiment until investigated. |
| Warm-up drift | Means at 30→35 and 35→40 minutes each differ by ≤1.0% of the earlier mean; x and y block means each shift by ≤0.002. This establishes stability only over the observed window, not a universal warm-up time. |
| End stability | Final mid-grey mean Y differs from the 40-minute block by ≤1.0%; x/y means each differ by ≤0.002. Otherwise range evidence is inconclusive because the setup drifted. |
| Low-light usable range | A nonzero code needs positive mean Y, CV ≤5.0% and x/y ranges ≤0.005. Its pair with the immediately lower listed code must be distinguishable, as must every pair above it through 255; every block from it through 255 must pass these block limits. Report the lowest code meeting all conditions, or none. A gap cannot be skipped. These are relative limits of this setup. |
| Zero patch | Retain readings and variability, including zero or negative finite values. Never interpret repeated floor values as verified panel black. No assumed 0.38 cd/m² cutoff, borrowed TV black value or black-level acceptance target is imposed. |

Thus code 5 needs separation from code 0 as well as code 13; if 0→5 fails but 5→13 and every higher pair/block pass, the lowest reportable code is 13. The zero block supplies a noise comparison only, never a calibrated black value. An indistinguishable pair fails that range criterion; do not infer a meter-only fault because the unvalidated video path and TV can also contribute. T-005 and T-004 remain separate. Numeric success cannot confirm the accuracy forecasts in C-043, the other-unit benchmark in C-072, or correction validity under Q-001.

**Stop immediately:** owner requests it; unexpected TV behaviour/menu/overlay; setup differs from this plan; instrument missing/ambiguous; unplanned prompt; driver/communication error; non-finite XYZ or missing measurement output; invalid x/y despite a positive XYZ sum; timeout; mid-grey stability failure; disturbed meter mounting; uncertain menu exit; or any required step outside the authorisation. No automatic resend, repeat, recovery, driver change or USB replug. Finite noisy low-light XYZ, including undefined x/y for a zero/non-positive XYZ sum, is handled by the predefined range criteria, not reclassified as a protocol fault.

**Stop rules adopted:** [docs/plan.md stop rules](../plan.md#stop-rules-for-every-physical-stage) at full commit `ba099e0a182713945c247636042286e6f9dca626`. The user can stop at any time. A later plan revision requires review and explicit authorisation for its changed scope.

## 8. Owner's authorisation

*To be completed by the owner only, or copied word for word from the owner's written authorisation. The current preparation request explicitly excludes hardware operation.*

- Authorised: **No — not requested or granted**
- Reviewed plan commit: not yet recorded
- Steps authorised: none
- Conditions or limits: not yet recorded
- Acceptance of proposed diagnostic thresholds and 2.0-second wait: not granted
- Acceptance of generic, uncorrected diagnostic readings: not granted
- Component source revision/hash: identified above; local interpreter/Tk/Argyll identities and display/console record remain unresolved
- Reviewed launch/close procedure accepted for steps 5–11: not granted
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
