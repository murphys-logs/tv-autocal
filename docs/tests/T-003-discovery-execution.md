# T-003 discovery-only execution package

> **Draft for independent review — NOT AUTHORISED. Do not launch Argyll or carry out the physical steps.**
> Prepared by Codex (OpenAI), 28 October 2026, from merged PR #28 at `80ed7abde9644096b3aac47de1abc5ee44d06b8e`, under [S-054](../briefs/2026-10-28-t003-discovery-package.md). Preparation used source/document and local executable-file reading only; no Argyll program or equipment was operated.

This is the execution addendum for **[T-003 steps 1–4](T-003-meter.md#5-steps)**, not a new physical test. Review and authorisation must cover this file, its [private-record template](T-003-discovery-record.example.md), the parent plan and the applicable [shared prerequisites](component-execution.md#unresolved-inputs) at one plan revision. The parent plan's section 8 remains the only authorisation record. Later steps 5–11 and all T-005/T-006 work are outside this package.

**Proposed scope: one owner-initiated direct `spotread.exe -?` invocation, at most.** There is no presenter, patch, reading, menu operation, TV/Denon setting change, Ex-Link connection, driver/data installation or second attempt. The centred 960×540 patch on 3840×2160 (6.25%) is unchanged and unused. No second screen or 300% layout solution is needed for this scope. The owner still needs an accessible ordinary console and elapsed-time display; their exact method is an open input below.

## Executable identity and what is actually known

The owner reported ArgyllCMS in Downloads and also installed on the PC, with past Spyder5 use through DisplayCAL ([S-053](../briefs/2026-10-28-owner-readiness-inputs.md), C-102). Those words do not identify DisplayCAL's executable or prove that there is a second copy.

Codex performed a file-only lookup limited to the reported Downloads Argyll package on 28 October 2026. One `spotread.exe` was found there and selected as the **proposed** candidate `T003-ARGYLL-A`. Other installation locations were not searched. Exact absolute paths and the complete identity record are in ignored `local/T-003/discovery-identity.local.json`; they are not published. This record is preparation evidence, not permission or a completed session record.

| Identity field | Recorded preparation evidence / limit |
|---|---|
| Candidate location class | Existing Downloads package named for Argyll V3.5.0, win32; exact drive-absolute path private |
| Candidate SHA-256 | `51bcfe12e8923334830a94ac45ff6e5015f3a62653aa6ef77363c6c05a780a88` |
| Candidate size | 4,645,888 bytes |
| Embedded file/product version | Both absent in the inspected Windows file-version metadata; no version inferred from that metadata |
| Required reported version | **3.5.0**, to be observed only during the future authorised discovery; not observed now |
| Proposed console runtime | Existing PowerShell **7.6.5 Core**, observed in this preparation shell; exact `pwsh.exe` path private |
| Console executable SHA-256 | `362a356ce7f0940ec74f73a8fc2c990a2cc24a38a11c90bbd8eca947110ad139` |
| Other copies / previous DisplayCAL executable | Unknown; do not infer, run alternative copies or resolve through PATH |
| Driver, meter, default display type, native process/capture behaviour | Not inspected or tested; future session observations only |

Hashing records file identity, not vendor authenticity or agreement with the published source. The folder name is not version proof. The private candidate/console record must be checked by the reviewer/owner before authorisation, then both files rehashed by ordinary file reading immediately before the authorised launch. A changed file, unresolved path, different shell or unreviewed candidate stops preparation for review; never substitute a newly found copy. Later measurement plans must bind the same reviewed Argyll path/hash or explicitly review a change.

This direct discovery uses **no Python component entry point, Tk, pySerial or meter wrapper**. The 34-file source manifest and 287-test Python suite remain the unchanged component-software baseline for later tool use; they do not validate this executable or need a presenter launch to permit discovery preparation. No interpreter or dependency is installed here.

## Unresolved owner inputs and review gates

The procedure is proposed below; these are the remaining choices/records, not instructions to operate anything now. Session observations must not be filled from S-053's historical answers.

| Gate | Current state | Needed before the relevant action |
|---|---|---|
| One candidate and console | Paths/hashes privately recorded; selection proposed | Owner/reviewer checks the private identities and confirms the owner can open the pinned PowerShell with `-NoLogo -NoProfile`; no alternate shell assumed |
| Discovery workflow limit | **60 seconds proposed, NOT accepted** (Q-020) | Owner accepts or requests a reviewed alternative; D-019 accepted the later-reading deadline only |
| Stopping policy | Stop scheduling and wait without forced recovery, as specified below; **NOT accepted** (Q-020) | Owner accepts this proposed response to an outstanding process. If an immediate technical-abort method is needed, resolve and review it before authorising a launch |
| Console, timing and presence | Owner reports controls are accessible and no practical waiting limit (S-053); exact method unknown | Record how the owner sees the dedicated console and a separate elapsed-time display without typing into it; confirm ability to remain present. No new display connection, scaling/power-setting change or software installation is included |
| Private session record | Blank template supplied | Choose a fresh ignored `local/T-003/` session directory and distinct unused stdout/stderr/record files; review the filled preparation fields privately, keep observation fields blank |
| Independent review and final plan revision | This package awaits review; full final plan SHA unfilled | Cross-vendor review of this package/parent and resolution of review findings; record the full reviewed plan commit separately from the software baseline |
| Physical authorisation | **None** | Dated, exact permission for parent steps 1–4 plus this one-attempt procedure, copied verbatim into parent section 8 before execution |
| Session-only checks | Ex-Link/meter connections, other serial devices, driver and correction variables **not checked now** | Owner records them only in the authorised steps below. A missing/ambiguous requirement prevents launch; no probe, installation or repair substitutes for it |

Merging this draft does not accept Q-020 or grant physical authority. A plan change following owner feedback requires review before the affected scope can be authorised. Copying later permission into section 8 creates an authorisation-record commit; retain both it and the reviewed plan commit as described in the [shared record](component-execution.md#authorisation-and-launch-record).

## Future steps — parent T-003 steps 1–4 only

The owner performs all equipment actions and the single launch, with an agent limited to recording/assessment under that exact authorisation. No automated scheduling or retries are proposed. A preparation or isolation failure uses zero launches and ends the session.

### Step 1 — authority, isolation and console preparation

- Check the recorded authorisation covers this exact plan revision, the selected identities and steps 1–4. Check that limit/stopping acceptance and the timing/console method are resolved. Prepare the private session record before any connection change.
- Record the original Ex-Link connection state; keep its **TV end and PC USB end disconnected** throughout. If already disconnected, do not reconnect just to repeat the instruction. Record that no other non-meter serial adapter/device is connected, using owner knowledge/physical observation, not software port discovery. If uncertain or another such device is present, stop for a scope amendment.
- Close ordinary measurement applications, including DisplayCAL, using normal controls. Do not uninstall software, stop services or assume that closing an application proves driver availability.
- Open one dedicated instance of the privately pinned PowerShell with `-NoLogo -NoProfile`, using the agreed accessible console. Record its actual version and both executable hashes. Use its process environment only; never edit user/machine environment or launch through DisplayCAL.
- Privately record the presence and original values of `ARGYLL_COLMTER_CAL_SPEC_SET` and `ARGYLL_COLMTER_COR_MATRIX`, remove them from this console's **process environment only**, and verify both are absent. This is a future authorised step, not an environment change made during preparation.
- Record and set this console's `$PSNativeCommandUseErrorActionPreference` to `$false`: the expected exit code 1 must not be turned into a shell error that skips completion recording. Retain the console's other relevant error/capture settings; no permanent profile change. If the selected shell or environment checks differ from the reviewed procedure, stop.
- Select fresh, distinct stdout, stderr and session-record paths inside this checkout's ignored `local/T-003/` directory. Confirm stdout/stderr do not exist; redirection can overwrite existing files. Do not append, use an existing log, redirect outside the private directory, or add a logfile argument to Argyll.

### Step 2 — meter and session baseline

- Record the initial Spyder5 USB connection and physical position without mounting it on the screen. Leave TV/Denon settings, desktop layout, scaling and picture state unchanged; no menu inventory, warm-up, patch, dim-room setup or two-second patch wait is needed for discovery-only.
- If needed and expressly covered by the authorisation, connect the Spyder5 to the existing PC USB port. Record the existing driver name/version shown by Windows Device Manager, without requesting a scan, update, installation or property change. If those records cannot be obtained, or a driver/installation prompt appears, stop before launch for review; do not install or repair anything.
- Record the current Ex-Link both-ends isolation, absence of other non-meter serial devices, closed measurement applications, shell/environment checks and owner readiness. Historical statements do not replace these observations. Recheck the candidate hash immediately before launch; any mismatch stops.

### Step 3 — one direct discovery attempt

Only after every applicable check passes, start the agreed elapsed-time observation immediately before invoking the selected absolute executable with **exactly one argument: `-?`**. Capture stdout and stderr separately to the two fresh private files. No `-O`, `-y`, `-c`, `-X`, `-Y`, logfile argument, wrapper, pipeline, `Start-Process`, timeout/kill helper or second launch is included.

Once the invocation is attempted, its one-attempt allowance is used even if launch or redirection fails. Record the actual failure and any uncertain launch state; do not correct a path/argument and try again under this authorisation.

The following is a **placeholder command specification for review, not a command to run now**. The paths must come from the reviewed private record; no actual path is supplied here. Prepare the exact private command text for review before authorisation.

```text
& '<SELECTED-ABSOLUTE-SPOTREAD-PATH>' '-?' 1> '<FRESH-PRIVATE-STDOUT-PATH>' 2> '<FRESH-PRIVATE-STDERR-PATH>'
```

This is a foreground console invocation. While it owns the console, **type nothing**, including Enter, Escape, Ctrl+C or Ctrl+Break. Both streams are redirected, so an unexpected prompt or error may not be visible live; lack of screen output is not evidence of a hang or success. Observe elapsed time independently. At 60 seconds without confirmed return, apply the timeout procedure below; do not type into the occupied console to check it.

On uninterrupted return, immediately preserve the numeric `$LASTEXITCODE` and return time in the private record **before another native command or script** can replace that value. Do not use `$?` as the result: expected exit code 1 makes it false. Record whether the timing observation clearly establishes return before 60 seconds; if not, classify the attempt as late/timing-unconfirmed. Then inspect both capture files as text. Retain the files unchanged and record their hashes for later comparison; PowerShell text capture is not claimed to be a byte-exact forensic record or natively validated here.

The source's expected help completion is **exit code 1**, with V3.5.0 usage on stderr and the literal diagnostic `Usage requested`. This expected diagnostic is not a failure by itself. Require the complete usage through its final logfile-description line, exactly one unambiguous supported Spyder5, and generic non-refresh (`n`) marked **Default**, retaining Default/Base Calibration markers and all other listed types. Absence, conflicting version/type/device information, an additional failure/input request, missing/truncated capture or a different exit code stops the session. Do not select another type, supply input, install data, guess a device index or try another executable. Code 1 alone is never a recognition pass.

### Step 4 — record and close; no next test

Classify the attempt using the table below. Discovery completion is not permission to proceed to parent steps 5–11. Retain all failure/late/unknown results, with timing and owner actions; do not repeat this session to improve its result.

Only after an uninterrupted return, complete evidence capture and the normal-completion conditions below, close the dedicated console and restore the initial meter connection arrangement as covered by this step. Leave Ex-Link disconnected at both ends and TV/receiver/desktop settings unchanged. Do not reopen DisplayCAL or another measurement application as restoration; doing so could access the meter and is outside this scope. An error, late return, interruption or uncertain state follows the abnormal branch instead; normal-restoration wording is not permission for reset/replug recovery. Record any restoration performed or deferred. Public results later contain only checked, relevant extracts; paths, serial identifiers, environment values and raw captures stay private.

## Completion, stopping and outstanding-process procedure

**AI: Codex proposal — review and owner acceptance pending.** The separate discovery limit is 60 seconds from launch intent; accept timing only when uninterrupted return is confirmed before it. This limit stops the **schedule**, not the operating-system process. No source evidence establishes a safe forced interruption, guaranteed finish time or reset procedure on this PC.

| Observed condition | Owner's proposed action and recorded outcome |
|---|---|
| Owner declines or any pre-launch gate fails | Do not launch. Record `not launched`, reason and any preparation changes. If the meter was connected during preparation, leave that connection unchanged pending separately reviewed restoration; there is no assumed no-launch reset/disconnection path. Keep Ex-Link disconnected; do not repair/probe/retry |
| Uninterrupted return before 60 seconds; exit 1; complete expected usage; all identity/Spyder5/default checks pass | Record `recognition requirements met` and normal completion; retain evidence, close the dedicated console and restore initial meter connection only as authorised. This establishes no reading access, accuracy, repeatability or future stopping safety |
| 60 seconds reached without confirmed return, or return timing uncertain | Record `timed out` / `timing unconfirmed`; end further test scheduling. Keep the existing console/process and connections unchanged while the owner remains present. No cancellation keys, console closure, termination command, USB removal/reset, second launch or automatic recovery is the planned response |
| Owner requests stopping while discovery remains outstanding | Stop scheduling immediately; record `owner stopped schedule`, time and outstanding state. The proposed project action is to wait without interfering with the process. If the owner requires a technical abort instead, that is outside this proposed recovery procedure; no agent improvises it |
| Process later returns after timeout or schedule stop | Preserve exit/time and both captures. Retain the timeout/stop outcome, even if output looks valid; no retry, reading or continuation. Treat restoration/resumption as a separate reviewed decision, not automatic normal cleanup |
| Return has unexpected code/output, missing capture, prompt, wrong version, absent/ambiguous instrument or default | Record failed/inconclusive discovery and stop. Leave the meter connection unchanged pending assessment of the failure/restoration; no changed arguments, driver repair, data extraction or repeat launch |
| Console disappears, power/sleep event, owner interruption or process completion cannot be established | Record `interrupted` / `completion unconfirmed` and exact known events. Do not infer process exit from console disappearance; no further project meter operation or assumed cable recovery until the state and a recovery/resumption procedure are reviewed and specifically authorised |

The owner retains the unconditional right to end PC activity, including closing the console, terminating a process or shutting down. If they choose that, record what happened and preserve whatever evidence remains. Those actions are **not** presented as validated meter-reset methods, and this package does not instruct an agent to perform them. Owner acceptance of waiting does not promise that waiting is risk-free or that the process will finish. If the owner does not accept this response to a stalled process, **do not authorise the launch** until an alternative has been reviewed. No fixed kill deadline, indefinite unattended run or agent recovery is proposed.

## Evidence record and assessment limits

Use the [blank record template](T-003-discovery-record.example.md) in a fresh ignored session directory. Keep proposed values, actual observations, owner decisions and unknowns separate. Do not prefill driver state, connection checks, process status, exit code or recognition from source predictions or past DisplayCAL use.

For discovery-only, D-013's change/exit/wait/read cycle is not exercised: no TV setting changes and no readings occur. The two-second patch wait and wrapped-reading 60-second acceptance deadline remain unchanged for later separately authorised work. Discovery may read existing vendor calibration and CCSS/CCMX data to list choices; no external correction is manually inspected, installed or selected for a reading here, and no reading is requested.

This package can at most support the **recognition portion** of T-003. C-002 remains unconfirmed until actual measurement access is established separately. Correction accuracy, signal-path fidelity, display layout, Ex-Link compatibility and safe abort recovery remain untested. No physical result exists in this preparation PR.

## Sources and preparation checks

Source facts are C-104; local file observations are C-105; procedure choices are C-099/S-055. Consulted read-only on 28 October 2026:

- ArgyllCMS V3.5.0 [source archive](https://www.argyllcms.com/Argyll_V3.5.0_src.zip), the existing S-037 copy, SHA-256 `f8576ce5589fd15620abb73ff049ea31f55ddbd1bba6d1ffa87452658e7bc85f`. `spectro/spotread.c` lines 700–701 route `-?` to `usage("Usage requested")`; 447–455 write version/diagnostic to stderr; 464–490 build/list paths and display types; 562–566 finish usage, clean up the list and exit 1. No-port output can still exit 1. This is source behaviour, not proof of the selected executable's origin or behaviour.
- In that archive, `spectro/instappsup.c` 469–529 constructs instrument objects, obtains and prints default/base display types, then deletes them. `spectro/spyd2.c` 3793–3795 and 4129–4137, and `spectro/inst.c` 953–996, 1200 and 1341 show existing calibration/correction data can be read while preparing the choices. This is not a measurement request; startup can still probe ports (C-090), and interruption safety is not established (C-069).
- Microsoft PowerShell 7.6 [redirection](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_redirection?view=powershell-7.6), [automatic variables](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_automatic_variables?view=powershell-7.6), and [native exit-code preferences](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_preference_variables?view=powershell-7.6#psnativecommanduseerroractionpreference) (S-056): separate output/error streams, overwrite behaviour, numeric `$LASTEXITCODE` versus `$?`, and nonzero native exit handling. These contracts do not validate this console's native capture/interrupt behaviour.
- Candidate executable and current preparation-shell files were hashed by ordinary file reads. The proposed shell version was read from the already-running preparation shell; Argyll file-version resources were absent. No Argyll executable, help/discovery, measurement, hardware-mode tool, device/display enumeration, presentation window, port or installation was used.

The source/manifest/test files are unchanged. Documentation checks, links/IDs, privacy and the private-record ignore rule are checked for the PR; software test counts remain inherited, not new discovery evidence. Independent cross-vendor review and all unresolved authorisation gates remain required.
