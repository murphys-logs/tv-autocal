# Shared execution amendment for T-003, T-005 and T-006

**Draft for independent review — NOT AUTHORISED. No equipment has been operated.** This document is part of the three plans, not a fourth physical test or permission to start one. Unresolved inputs below must be closed for the relevant steps before authorisation. The owner's request to prepare amendments is not an execution permit.

Prepared by Codex (OpenAI), 27 October 2026 (S-048), from merged `main` at `45ef2c28cfcb271d2f1f3373be4082706ba775a8`. [S-047](../briefs/2026-10-27-component-execution-amendments.md) records the request and possible second screen. These are source-checked operating proposals, not equipment findings. Existing test purposes, diagnostic thresholds, stop boundaries and **960×540 at x=1440, y=810 on 3840×2160 (6.25%)** remain unchanged.

## Reviewed software and local inputs

The component tools were independently reviewed and merged in PR #24, with the documented L-4 limitation in PR #25. Use the Python source bytes at the baseline above, identified by the complete [34-file SHA-256 manifest](../software/component-tools.md#offline-verification). That manifest includes the tests; do not substitute a later source revision without review. The software does not automatically compare its running source against this manifest: its journal records source hashes for the operator/reviewer to compare. T-009 alone is not the physical sender.

| Item | Proposed identity or required record | State before authorisation |
|---|---|---|
| Component source | Baseline above; all manifest hashes must match, including unchanged renderer | Reviewed software; actual launch checkout to be recorded |
| Python | Propose existing Python **3.12.14**, one of the recorded 252-test environments, selected by its exact private interpreter path | Owner acceptance and actual interpreter identity pending; no installation proposed. A different version needs recorded offline evidence and review |
| Tk/Tcl for presentation | Exact available versions/build and Python association, recorded privately with the interpreter | Unknown; availability and native behaviour untested. No `python -m tkinter` or other window probe during preparation |
| pySerial for T-006 only | **3.5**, as pinned in [requirements-hardware.txt](../../requirements-hardware.txt) | Actual availability unknown. Do not install or substitute a version as part of these plans |
| ArgyllCMS for T-003/T-005 | Existing **V3.5.0** `spotread.exe`; exact drive-absolute path and lowercase 64-character SHA-256 | Binary identity unresolved; ordinary file hashing does not run discovery or establish provenance. Bind the reviewed local identity before any launch; source-archive hashes are not executable hashes |
| Driver/build records | Existing Spyder5 driver, OS/GPU and output settings; existing serial driver for T-006 | Retain earlier owner baseline and confirm actual values only within the relevant authorised steps; no driver changes |
| Plan revision | Full 40-character commit containing the final independently reviewed amendments and resolved prerequisites | Unfilled. This differs from the pinned software baseline and must not be replaced with it automatically |

Licence and source rationale remain in [component-tools.md](../software/component-tools.md). There are no new dependencies or installations. Production Python/packaging Q-003 and project licensing Q-002 remain open. Missing software stops preparation for a separate proposal.

## Display and console arrangement

**Owner input partly supplied (Q-019/C-098):** the owner can, and probably will, connect a second screen. Whether it will be used, its connection, desktop layout and console placement remain **unconfirmed**. This amendment proposes keeping the TV as the pattern display and all launch/measurement consoles and notes on the second screen. It does not authorise connecting or rearranging displays.

Before authorisation of presentation steps, record the chosen arrangement, original arrangement, any proposed setup/restoration steps, TV desktop origin, native size, scaling, and the console locations. Setup changes must themselves appear in reviewed authorised steps; do not improvise them to make the tool work. If the TV is the only screen, stop preparation until a reviewed procedure explains how console interaction leaves the held TV image unobstructed.

The presenter requires explicit nonnegative desktop `--x`/`--y` coordinates (0..32767) for a 3840×2160 TV rectangle. These are the **desktop origin of the whole TV**, not the patch coordinates. The patch remains centred within that rectangle. A negative origin, unavailable native size or geometry mismatch requires a revised procedure; there is no scaling fallback or instruction to rearrange the desktop. No enumeration, coordinate detection or physical check has occurred.

In a future authorised run, the owner confirms the intended TV using the presenter's initial instruction screen and **C**, then advances one item with a separate **Space/Right** press. Wrong target: close with **Escape**, mark the run stopped, and review before another launch. Do not drag a running presenter between displays. Console focus may move to the second screen, but the owner must observe that the TV patch remains unchanged and unobstructed. Window geometry and a matching journal cannot prove visibility, HDMI values or freedom from overlays.

The presenter has a three-hour session cap and closes a named visual pattern after 60 seconds without advance. A closure during a meter attempt rejects it, including a still-outstanding rejected process. Do not disable the cap, restart the presenter, or resume measurements to rescue that attempt. Normal completion uses Escape or advance past the final item only after all meter attempts have returned and their records have been checked. Retain `presenter_closed`, final `journal-close` and the owner's observation of actual closure; a logged close attempt alone does not prove native window closure.

## Authorisation and launch record

**No filled permit or ready-to-run hardware command is supplied.** The option tables in each plan are specifications for a future authorised launch. Every placeholder and prerequisite must be resolved, reviewed and recorded before copying the owner's dated, exact authorisation into section 8. A local attestation is not evidence that permission or electrical compatibility exists.

For each plan retain a private setup record under ignored `local/<plan>/`. It contains the reviewed plan commit, source manifest comparison, exact interpreter/dependency identities, device/executable identification, accepted timing/thresholds, prerequisite evidence, original settings and restoration instructions. Machine paths, device identifiers and raw logs stay private. Public results contain checked, relevant extracts only.

The tool prefix is the selected interpreter, `-B -m tv_autocal_tools`, followed by `present`, `meter` or `serial`. Each physical launch requires all four common options:

| Option | Value to bind before use |
|---|---|
| `--hardware` | Explicit physical mode, only after authorisation; never used during preparation/review |
| `--permit` | Private JSON path inside this checkout's `local/`, ending `.json` |
| `--confirm` | Exact single argument `RUN <plan> <full-reviewed-plan-commit>` |
| `--log` | A fresh, distinct private `.log` journal inside this checkout's `local/` |

The permit has exactly six fields: `plan` (`T-003`, `T-005` or `T-006`), `revision` (reviewed plan commit), `authorisation` (dated verbatim owner permission), `steps` (exact covered steps/limits), `evidence` (references to closed prerequisite records), and `actions` (list). T-003/T-005 permit only `present` and/or `meter`; T-006 only `serial`. A visual-only T-005 permit lists only `present`. T-003 discovery is outside this wrapper and must be separately included in the written authorisation; no permit turns help into a software-only action.

The software checks field shape and broad action scope, not the meaning of the steps, owner identity, physical prerequisites, attempt totals or playlist position. The owner must check these against the plan before **every** launch. Reusing a permit does not authorise another run after failure. Presenter and meter must share the same plan/revision; T-003 evidence cannot be relabelled T-005 by reusing a journal.

Use one fresh presenter journal per planned run, one fresh wrapper journal per meter attempt, and one separate native Argyll logfile per attempt. The latter must be a simple filename directly under `local/T-003/` or `local/T-005/`, containing letters/digits/hyphens/underscores, ending `.log`; never reuse an existing file. Start from the repository root so relative paths resolve consistently. The wrapper reserves this native file before launch; do not pre-create it. T-006 uses one journal for its complete bounded session, not one per command. No command loops or unattended next steps are proposed.

## Meter attempt and closure

Only the already authorised T-003 discovery establishes the unambiguous instrument/configuration; the wrapper never discovers devices. Before each attempt, recheck both Ex-Link ends remain disconnected, no other non-meter serial device/tool is involved, and the intended patch is held with menus exited. The owner records the current presenter's **frame sequence** from `pattern_buffer_applied.fields.sequence`, along with RGB and matching `pattern_present_intent` hash. Do not use the journal's top-level event number as the frame number. The plan's frame table supplies the expected sequence.

Bind `--presentation-log`, `--presentation-sequence` and `--rgb` to that current applied frame. The meter reads the receipt before and after the process. It rejects a changed, closed or incomplete presenter journal, but cannot detect every crash, overlay or physical display fault. Owner observation remains necessary throughout, including after a timeout. Each attempt needs its own pre-recorded purpose and identifier.

The proposed wait is `--wait-ms 2000`, freshly applied before **each** launch after confirmed menu exit and stable patch; `--timeout-ms 60000` is an exclusive acceptance deadline, not a promise of process termination. These remain owner inputs under Q-008. The wrapper uses exactly the plan's one-attempt Argyll argument list, with no interactive stdin, and removes both correction defaults from a copy of its environment. Discovery retains T-003's separately specified isolated-console procedure.

On a successful attempt, retain the final JSON, `meter_exit` and `meter_result` journal events, and after the CLI returns, the final `journal-close` with `complete: true`. The meter JSON has **no `closed` field**. Inspect `exit_code`, `capture_complete`, `log_complete`, `accepted`, `reason`, timeout/cancellation and dropped-byte fields together. A successful measurement requires a finite parsed result, exit code 0, complete capture/logs, no reported loss/failure and the plan's acceptance criteria. `journal-close` concerns the journal, not instrument safety or successful measurement. A result printed before a failed journal close is not a completed accepted record.

Timeout, cancellation, unexpected output or any other rejection ends the measurement schedule. The wrapper keeps draining and waiting for actual child exit and both output readers; do not advance or close the patch, start another attempt, kill/reset/replug, or treat the deadline as shutdown. Ctrl+C requests rejection in the wrapper and does not intentionally interrupt its separate child process; immediate delivery on this installation is untested. No further readings follow a rejected attempt even if the process later exits. Retain all partial/late evidence and the reason.

If no final result/return appears, process or capture completion is unconfirmed. If the presenter closes or changes meanwhile, record the interrupted patch and reject the attempt. There is no guaranteed finish time or automatic recovery. The owner can stop at any time under AGENTS.md section 7; force-closing or disconnecting may lose evidence or interrupt the driver and does not authorise continuation. The acceptable owner-directed interruption procedure for a persistently outstanding process, including console/cable handling, is **unresolved and must be reviewed before measurement authorisation**. This preparation does not prescribe an unverified recovery.

## Unresolved inputs

These are execution gates, not reasons to prevent independent review of this draft. Fill answers with evidence; do not write expected results into observation cells.

| Applies to | Missing input or evidence | Who supplies it / effect |
|---|---|---|
| T-003/T-005 presentation | Confirm second-screen use, actual layout/coordinates, console placement and any setup/restoration changes (Q-019) | Owner describes intended setup; agents incorporate exact steps for review. No display use yet |
| Each relevant tool | Exact local interpreter/build/dependencies, executable hash, private paths and launch revision | Owner/local file records; agents check consistency. No installations or device probes implied |
| T-003/T-005 measurements | Accept proposed wait, diagnostic thresholds, generic-only correction and duration limits | Owner, after review; Q-008 and calibration questions remain distinct |
| T-003/T-005 abnormal stop | Accept a reviewed procedure for an indefinitely outstanding meter process and console/cable handling | Agents propose with evidence and owner input; currently unresolved, no automatic recovery |
| T-005 optical steps | T-003 evidence identifying the usable range and repeatability | Future authorised T-003; visual screening can be scoped separately |
| T-005 Stage 4 completion | Method establishing correct black/white interpretation beyond clipping/monotonicity screening | Technical evidence/design, not an owner assertion; no method or pass invented here |
| T-006 connection | Model/revision-specific cable and TV electrical compatibility evidence | Technical research or separately reviewed investigation; no connection until its gate closes |
| T-006 setting change | Choose All Sources or Current Source only after affected settings and restoration are established (X-012) | Owner decision informed by evidence; neither choice selected |
| T-006 EXIT test | Per-menu automatic-close evidence and a non-overlapping observation interval | Technical evidence or separately authorised check; no guessed `--menu-window-ms` |
| T-006 abnormal stop | L-4, Ctrl+C/missing closure and exact console/cable handling | [T-006 amendment](T-006-exlink.md); unresolved procedures block authorisation, owner can always stop |
| Every physical step | Final independent review plus dated, step-specific owner authorisation | Owner only; all sections 8 remain unfilled/NOT AUTHORISED |

No full calibration, T-013 combined control, fallback/service-menu operation or concurrent Argyll/Ex-Link use is included. Correction validation, final calibration targets and the combined-adapter design retain their existing gates. Preparing or merging this document closes none of those equipment questions.
