# T-006 — bounded Ex-Link control and restoration

> **Draft for independent review — NOT AUTHORISED. No equipment has been operated.**
> **Execution blocked:** electrical evidence, scope/restoration, menu timing, unresolved stop/connection procedures and the owner's specific authorisation are still required. The component sender is reviewed software, not equipment validation.

Prepared by Codex (OpenAI), 27 October 2026, against merged baseline `ba099e0a182713945c247636042286e6f9dca626`. This is a proposed experiment, not a statement that these commands work on the TV.

Execution amendment by Codex (OpenAI), 27 October 2026, uses the merged PR #24/#25 software at `45ef2c28cfcb271d2f1f3373be4082706ba775a8`. This amendment needs independent review. [Common execution preparation](component-execution.md) records software identity, owner inputs and authorisation requirements; its unfilled fields are not permission to run. No source code or approved patch geometry changes.

## 1. Purpose

Establish, separately: compatible connection (C-021/C-064/C-076); a recognised reply (C-010); a visible, reversible ordinary picture-setting change (C-005/C-011); and a usable menu-exit method for D-013. Addresses Q-006 and X-002/X-005/X-007/X-010. It does not test white balance, colour management, persistence across power cycles, optical response or calibration accuracy.

T-001/T-002 are recorded in [S-033](../briefs/2026-10-26-owner-equipment-checklist.md) and [S-032](../briefs/2026-10-26-pr19-rulings-and-equipment-confirmations.md). The socket and COM-port observations are not electrical proof.

### Prerequisites before authorisation

| Gate | Required evidence / decision | Current status |
|---|---|---|
| Electrical compatibility | Close both cable and TV checks under the acceptance criteria below; record exact evidence and remaining uncertainty. A chip name or connector fit alone is insufficient. | Missing; no connection permitted |
| Route | Rear native EX-LINK jack only; no USB dongle, rewiring, electrical probing or adapters in this plan. Any physical electrical investigation needs its own reviewed plan. | Socket identity recorded; electrical gate still open |
| Scope | Owner accepts this test's stop boundary: on failure stop and return to the owner; no fallback or service-menu entry. This does not require settling the broader fallback question Q-013, which remains open. | Open |
| Setting scope | Owner chooses a reviewed procedure: retain All Sources with every affected scope's baseline/restoration checks, or isolate Current Source with explicit scope-change/restoration steps. Neither option is selected by this draft. | Missing; amendment required before authorisation; X-012 |
| Other software | ArgyllCMS, DisplayCAL and other instrument/serial discovery software must remain closed while either end of the Ex-Link cable is connected. No background discovery or second port user. | Must be checked before connection; C-090 |
| Transport | Use only the pinned `tv_autocal_tools` serial entry point and source hashes below, with pySerial 3.5 and the reviewed local interpreter. No terminal substitute or arbitrary-byte input. | Software reviewed in PR #24/#25; real port/driver behaviour not tested; this execution amendment awaits review |
| Reply policy | Initial/late/duplicate bytes, partial writes, bounded logs and paired observations follow the source-backed sequence below. No checksum or ACK establishes correlation or a changed setting. | Implemented and checked offline; equipment behaviour not tested |
| Offline checks | T-009 and T-017 coverage includes Contrast/EXIT literals, late-byte retention, fake-console command rejection and closure failures. | [Recorded 252-test suite](../software/component-tools.md#offline-verification); no physical evidence and no L-4 code fix |
| Menu timing | A reviewed amendment identifies each normal menu/submenu used, its automatic-close timing and a send/observation interval that cannot overlap it. Unknown or overlapping timing makes EXIT inconclusive; do not transfer a timeout between different menus. | Missing; no timeout value assumed |
| Connection and stopping | Specify physical connect/disconnect order and conditions, normal closure, and what the owner does if the console never reports closure. Include consequences of interrupting the console and cable handling. | **OPEN — procedure/evidence needed.** The policy below stops the test but does not invent an electrically safe disconnect procedure |
| Owner inputs | Accept the test-only timing limits and stop boundary; select the evidence-backed setting-scope procedure; confirm usable console placement and local run identity. | **OPEN.** A second screen is proposed, not confirmed connected; see [unresolved inputs](component-execution.md#unresolved-inputs) |
| Owner | Dated authorisation for an identified revision and exact steps, copied verbatim into section 8, after independent review and closure of these gates. | Not authorised |

Research can close a gate; it does not authorise a physical step. Do not fill evidence gaps by scanning commands, trying baud rates, opening the service menu or inferring signal levels from the FT232 chip name.

**Electrical gate acceptance criteria:** identify the actual SH-U35B hardware revision and the UE49KS7000UXXU native jack. For each side, record connector orientation, transmit/receive/ground pins, signal polarity, transmitter output limits and receiver input limits. A cited manufacturer specification explicitly covering that hardware must show that each transmitter's output fits the other receiver's limits and the wiring joins transmit to receive with the correct reference. Generic RS-232 wording, matching plugs, a USB device listing or two reviewers agreeing cannot close either half. If matching documentation cannot be obtained, the gate stays blocked; any physical electrical investigation needs its own reviewed, explicitly authorised plan and competent assessment before connection. An owner proposal to accept residual uncertainty would require a separately reviewed amendment and recorded decision; this draft grants no waiver.

**Setting-scope choice:** retaining All Sources avoids an extra scope change, but S-033 does not prove that all inputs/modes have identical values or that restoring HDMI 4 restores every affected setting. The retained-scope option must identify affected inputs/modes, record their original Contrast values and specify checks/restoration for each. The isolation option must specify the original scope, exact normal-menu change, its effect on stored values and the restoration sequence. A source or separately authorised check must establish these behaviours before the chosen amendment is authorised; neither is inferred here (X-012).

### Consulted evidence and candidate bytes

[Samsung's generic Consumer RS232 Control Worksheet](https://image-us.samsung.com/SamsungUS/samsungbusiness/tv-ci-resources/Samsung-RS232-Control.pdf) (S-015; pp. 2–5) was reconsulted on 27 October 2026. Its tables were also visually checked in the pinned S-006 copy, SHA-256 `38b932a0a712815f845c509ca77b8ea470b703425a598ac905a9d4998d4657fb`. No copy is added here. The worksheet does not establish support on UE49KS7000UXXU firmware 1270.1.

The generic table identifies Contrast as `0B 02 00 value`, range 0–100; key generation as `0D 00 00 key`, with EXIT `2D`. Candidate checksums below are **derived** with S-005's rule, not captured traffic. Contrast avoids the newer worksheet's renamed Backlight/Brightness ambiguity (C-060). Its exact-model meaning remains the hypothesis being tested.

| Proposed action | Seven binary bytes (hex display only) | Source / derivation |
|---|---|---|
| Exit ordinary user menu | `08 22 0D 00 00 2D 9C` | S-015 pp. 4–5; first-six sum 100, checksum 156 |
| Contrast 95 to 94 | `08 22 0B 02 00 5E 6B` | S-015 p. 4; first-six sum 149, checksum 107 |
| Restore Contrast to 95 | `08 22 0B 02 00 5F 6A` | S-015 p. 4; first-six sum 150, checksum 106 |

Only these three exact frames may be offered by the pinned sender. The contrast pair applies **only if the freshly observed baseline is 95**; otherwise stop and revise the reviewed plan. No arbitrary hex, other values, power, volume, factory, reset, white-balance, network or IR automation. The worksheet's command-result OSD toggle is not menu dismissal (C-066) and is excluded. The owner's ordinary handheld remote is used only for inspection/manual restoration as specified below.

## 2. Equipment and settings involved

- TV: UE49KS7000UXXU, reported firmware `T-JZMDEUC-1270.1`, intended Movie mode on HDMI 4. Confirm the active mode; S-033 did not establish the mode used during its observations.
- PC and delivered SH-U35B; recorded port COM3 is a historical observation. Select the explicitly identified device locally; no port scan or automatic selection. Keep private identifiers in ignored `local/` records.
- Denon remains on the recorded PC path with no receiver-setting changes in this plan. No meter or measurement patterns are used.
- ArgyllCMS can probe fast serial ports during startup, including help/discovery (C-090). Keep it, DisplayCAL and other discovery tools closed for the entire connected session; T-003/T-005 require the Ex-Link USB end disconnected from the PC before any meter-tool launch.
- Candidate serial profile: 9600 baud, 8 data bits, no parity, one stop bit, no flow control, binary bytes. 9600 8N1 comes from S-007 as recorded in [S-005](../research/2026-10-24-exlink-protocol-investigation.md), not a verified firmware setting. The pinned sender uses nonblocking reads, a one-second write timeout and DTR/RTS set false before opening; driver/OS activation on open is still possible. These settings are not electrical proof. No terminal defaults, line-setting experiments or port scan are permitted.

### Pinned sender and proposed launch

The source identity is `45ef2c28cfcb271d2f1f3373be4082706ba775a8`, with the complete [SHA-256 manifest](../software/component-tools.md#offline-verification). In particular, `tv_autocal_tools/serial_tool.py` is `6b9a51ccb38f3960d3fba78b2b24bfc8501a2df4315e982ebf88ec773eebb716`; source identity includes the CLI, permission, journal and protocol modules too. Verify the whole manifest and the [local interpreter/dependency record](component-execution.md#reviewed-software-and-local-inputs), not this one file alone. pySerial must be exactly 3.5; nothing is installed by this amendment.

The following is a **non-executable specification with unfilled placeholders**, for independent review only. `<PYTHON>` means the exact reviewed local interpreter invocation. `<PLAN_SHA>` means the full commit of the final reviewed execution plan, not the older tool-source commit. The private permit must identify `T-006`, action `serial`, the exact steps, dated verbatim owner authorisation and closed prerequisite evidence under the [common launch record](component-execution.md#authorisation-and-launch-record).

```text
<PYTHON> -B -m tv_autocal_tools serial --hardware --permit "local/T-006/<PERMIT>.json" --confirm "RUN T-006 <PLAN_SHA>" --log "local/T-006/<FRESH_SESSION>.log" --port <EXPLICIT_COM_PORT> --prerequisites-confirmed --menu-window-ms <REVIEWED_INTERVAL_MS>
```

Do not fill `--prerequisites-confirmed` by inference from the presence of a permit. The code checks an attestation, not electrical compatibility, genuine authorisation or menu timing. The port name and fresh journal are local inputs; no permit or ready-to-run command is supplied here. T-006 uses no presenter or meter process; the centred 960×540 patch on 3840×2160 remains unchanged and is not displayed in this test.

The CLI fixes these proposed policies; it does not expose overrides for them:

| Boundary | Pinned value / meaning |
|---|---|
| Initial observation | 5,000 ms after completed port open, no writes; any received bytes stop |
| Reply | Exclusive 2,000 ms deadline after the full seven-byte write completes |
| Post-ACK quiet | 500 ms before the next owner-observation phase; an ACK remains provisional |
| Settling | 2,000 ms after each owner exit confirmation; not a measured Q-008 value |
| Final receive drain | 500 ms and a final read before attempting port close; not a guarantee against later bytes |
| Whole session | 120,000 ms from completed open, including owner interaction; cannot interrupt a blocked console read |
| Evidence capacity | 65,536 received bytes / 2,048 serial events, within the 8 MiB journal; overflow is incomplete and stops acceptance |

**OPEN — menu interval:** the code has one `--menu-window-ms` value for all three menu cycles (integer 1–60,000). The reviewed evidence must justify that same conservative interval for every named menu/submenu used; if it cannot, stop and revise the procedure or software. The interval begins when `m` is pressed **before** opening the menu and must cover observation, EXIT dispatch, reply/quiet processing and `c` confirmation while excluding automatic closure. Do not choose a value merely because the CLI accepts it. The owner must also accept whether the fixed session limit is practicable; exceeding it ends the run, never authorises a restart.

## 3. Risks and how to undo them

**No service menu is used.** Incorrect electrical assumptions can damage equipment; the unresolved electrical gate prevents connecting. A valid-looking reply can accompany no change or the wrong change. Original values, menu observations and restoration are separate evidence. All Sources may affect other inputs; the unresolved scope gate prevents relying on a single-input restoration.

On any unexpected response or behaviour, stop sending. The owner may restore documented original settings using the ordinary remote, after inspecting the normal menu. Never send a speculative recovery frame, retry, reset or power cycle. If the normal menu or restoration is uncertain, stop and record it for a new plan.

Record immediately before a future test; do not substitute S-033's old values:

| Device | Setting | Original value | Restored afterwards? |
|---|---|---|---|
| TV | Input / active picture mode | Not recorded for this test | Not tested |
| TV | Apply Picture Settings / affected-source scope | Not recorded for this test | Not tested |
| TV | Contrast (must be 95 for this revision) | Not recorded for this test | Not tested |
| TV | Other visible picture controls, baseline normal-menu state | Not recorded for this test | Not tested |
| PC | Exact identified port and serial profile | Private local record pending | Not tested |
| PC | ArgyllCMS, DisplayCAL and other discovery/serial software closed | Not recorded for this test | Not tested |
| TV | Ordinary-menu automatic-close timing and approved observation interval | Not established | Not tested |

## 4. Cost

£0 proposed. Budget remains £15.99 spent / £9.01 remaining of £25. No purchase, paid service, automation or software installation is authorised here.

## 5. Steps

These are future steps for the **owner with an agent present**, after all gates pass. The owner launches the pinned tool and presses each key; the agent may record/interpret the evidence. There is no unattended sequence, pasted key sequence, terminal substitute or agent-generated hardware input. Use only exact lowercase `b m o e c d r q`, one deliberate key at the stated phase. Uppercase aliases and Escape are silently ignored; special keys do not act as command keys. See the [L-4 stop policy](#stopping-closure-and-l-4) before authorisation.

1. **Owner and agent:** check every prerequisite, authorisation revision, stop method and normal-menu restoration procedure. Confirm firmware, input, mode, scope and Contrast 95; record section 3. Finish these pre-run inspections, exit the ordinary menu with the remote and wait the proposed two seconds before launch. If any baseline differs, stop without connecting. Do not change the TV to fit these assumptions under this revision.
2. **Owner:** connect the verified cable by the still-required reviewed connection procedure, then launch the pinned sender with the completed local record. During `initial quiet`, transmit nothing for five seconds. Any incoming bytes (including apparent debug output) stop the test. Five seconds is a screening policy, not proof that later bytes cannot be unsolicited. At `baseline`, press `b` only to attest the fresh Contrast 95 observation from step 1.
3. At `menu preparation`, press `m` **before** opening the named ordinary picture menu with the remote; record its actual opening time. At `observe setting`, inspect Contrast 95 and the recorded visible controls, then press `o` only if correct. At `exit ready`, press `e` once to request EXIT within the reviewed interval. The tool logs the write and checks its reply; wait through `reply` and `ack quiet`. At `confirm exit`, press `c` only after observing the menu closed within the same interval, recording its actual closure time. Wait through `settling` until `set ready`. If automatic closure cannot be ruled out, or any value/menu is uncertain, request a stop instead of attesting success. No reply, NACK, noise, duplicate or partial reply, wrong screen, or uncleared menu stops the test. Apply these observations/timing checks in steps 5 and 7 too.
4. At `set ready`, press `d` once to request Contrast 94. After the full reply/quiet phases, at `menu preparation` press `m` before opening the menu. Inspect exactly 94 and the recorded visible controls; at `observe setting`, press `o` only if correct. An ACK by itself does not pass this step. Stop on disagreement; do not continue as recovery.
5. At `exit ready`, press `e` once. After reply/quiet processing, at `confirm exit` press `c` only after the required closure observation, then wait through settling until `restore ready`. This is a separate transaction, not a retry of step 3.
6. At `restore ready`, press `r` once to request Contrast 95 **only on the normal successful path**. After reply/quiet processing, at `menu preparation` press `m` before opening the menu; verify exact restoration to 95 and the recorded visible settings. At `observe setting`, press `o` only if correct.
7. At `exit ready`, press `e` once. After reply/quiet processing, at `confirm exit` press `c` only after the required closure observation. Wait through settling until `complete`, then press `q` once to request final drain/closure. Check the final result and journal as specified below before treating the run as complete. Leave no sender running; disconnect only by the separately completed reviewed connection procedure. Scope restoration follows the evidence-backed amendment's exact normal-menu procedure, with its own final exit/wait.
8. **Owner and agent:** classify each result separately under section 7 and record all observations, including rejected bytes and failures. Stop; no further control or measurement test is implied.

Maximum: five single-frame transmissions on the successful path (EXIT, Contrast94, EXIT, Contrast95, EXIT). The key order is `b → m,o,e,c → d,m,o,e,c → r,m,o,e,c → q`, with the phase waits above; this is a checklist, never text to paste. An unclear outcome ends it earlier. No resend; no automatic reconnect/resume; no automatic restore after a fault. The sender retains intervening receive bytes within its limits while console reads return promptly. A response outside the active window is unexpected and ends the run. ACKs have no transaction identity: silence or reconnecting cannot prove attribution. Therefore menu observations are mandatory, and a clean run still supports only the tested sequence, not a general transport guarantee.

### Stopping, closure and L-4

The owner can stop at any time under [AGENTS.md section 7](../../AGENTS.md#7-equipment-safety-rule-6). This policy does not restrict that right. It describes software evidence and the unresolved consequences of a stop; it is not a claim that force-closing a console or disconnecting a cable is electrically safe.

- **Ordinary stop request:** press lowercase `q` once. It sends no frame, stops an incomplete run and requests the final drain/close path. After an automatic stop, no later send is allowed and the tool attempts closure itself. Do not type recovery, restore or retry keys.
- **L-4 remains unfixed:** a literal `à` can block polling and swallow the following key. If input appears stalled, press **Space once, then lowercase q** solely to request a stop. Do not resume the test after input resumes. Mark the whole session inconclusive even if the tool later reports acceptance; reads/deadlines were paused and serial arrival times are unknown. Retain the interruption description, every reported reason and error, including any reply/session/menu deadline reason. A timeout reason after this interruption does not prove that the TV replied late.
- **Ctrl+C policy proposed for this amendment:** it may be used only as an owner's request to interrupt and abandon the run, never to advance or resume it. The source catches `KeyboardInterrupt` in the operating loop and attempts drain/close, but immediate delivery during blocked `getwch()` and successful OS closure are unverified. Repeated interrupts can interrupt closure itself. Do not describe Ctrl+C as a guaranteed stop, flush, restoration or recovery mechanism; record its use and treat the interrupted run as inconclusive.
- **Closure evidence:** retain the final printed JSON result's `closed`, `completed`, `log_complete`, `accepted`, `reason`, write count, receive/omission counts and evidence pairs. `"closed": true` reports the software's port-close outcome. A `Phase: stopped` line is neither required after `q` nor closure evidence. Also retain `serial_close` and `serial_result` plus the terminal `journal-close` record; `journal-close.complete` concerns the evidence file, not the port or TV. A failed/missing final journal closure makes the audit incomplete even if an earlier result said accepted. Software-reported closure alone proves neither restoration nor electrical safety.
- **Missing/false closure or unexpected termination:** no further project connection, serial command, restart, retry, meter launch or assumed recovery is permitted. Record the last output and unknown state without inventing a completed result. **OPEN before physical authorisation:** agree an evidence-backed owner procedure for a console that never returns, including whether/how to close it and handle the cable, and record the consequences of an owner-directed interruption. No such physical procedure is established by this amendment. If a real emergency leads the owner to stop by other means, record what happened and leave closure/restoration unconfirmed until assessed; the owner's right to stop remains unconditional.

After any fault, only the already reviewed, evidence-backed normal-menu restoration procedure may be followed. If that procedure or closure cannot be confirmed, stop further project work for review. This amendment adds no automatic restoration and cannot close the electrical, setting-scope or missing-closure procedure gates by wording alone.

## 6. What will be recorded

Plan revision/authorisation; sender revision/hash and dependency versions; identified device/profile (private locally); original settings and scope; monotonic and wall-clock timestamps; each exact transmitted frame, write count, all received bytes and timing, including bytes after a reply or stop until the port is closed; menu-open, send and menu-close times against the automatic-close boundary; owner menu observations; each stop reason; restored values and whether restoration was manual after a stop. Copy only privacy-checked excerpts into a future `T-006-data/` folder. Raw logs stay ignored.

**Measurement cycle:** no meter readings or calibration data are taken. After every successful change or menu inspection the proposed sequence uses EXIT, owner confirmation and a two-second delay. If EXIT fails, there is no further serial action; manual restoration includes ordinary menu exit/wait. This tests the exit method before T-013 relies on it. It does not detect later unexpected overlays. Q-008 remains open; two seconds is a design proposal for this revision, not established settling time.

## 7. How results will be judged

**ACK** means acknowledgement (the candidate success reply); **NACK** means a negative response. Neither identifies the command or verifies a changed TV setting.

| Result | Interpretation |
|---|---|
| Electrical evidence absent, sender identity unverified or other gate open | Blocked before operation; no equipment result |
| `03 0C F1` within the proposed window | Candidate ACK only; not readback or proof of execution |
| `03 0C FF` | Candidate NACK as recognised by S-007; stop, record actual bytes |
| Missing/malformed/late/duplicate response, partial write, failed exit, unexpected menu/control | Inconclusive or contradicted for the specific tested behaviour; stop, no retry |
| Input interruption, owner cancellation, missing/false closure or incomplete audit | No T-006 pass; retain the raw evidence and unresolved state, even if an earlier tool result was accepted |
| EXIT visibly works, Contrast changes 95→94 and restores to 95 with required replies and observations | Supports only these exact controls/profile/session and their bounded restoration |
| All above plus scope restoration verified | T-006 bounded pass; does not establish white balance, CMS, HDR, persistence, readback or optical response |

No response alone does not prove a service-menu change is necessary or that every Ex-Link command is unsupported. Failed restoration is a failure, even if the initial change worked. T-013 and T-008 remain separate, unauthorised tests.

**Stop rules adopted:** [docs/plan.md stop rules](../plan.md#stop-rules-for-every-physical-stage) at full SHA `ba099e0a182713945c247636042286e6f9dca626`. Stop immediately on the owner's request, any unlisted behaviour, suspected electrical issue or uncertainty; no active recovery beyond the owner's recorded normal-menu restoration.

## 8. Owner's authorisation

**Not given.** The owner's execution-amendment request authorises preparation only and explicitly prohibits hardware operation now. S-053's planned second screen and D-019's diagnostic policies authorise no T-006 step and close none of its electrical, scope/restoration, menu-timing or connection/stop gates. This amendment and every unresolved prerequisite must be reviewed and completed before specific dated permission is copied here.

- Authorised: no
- Plan revision and steps authorised: none
- Conditions or limits: pending all prerequisites and independent review
- Date: not authorised
- Verbatim owner authorisation for a future test: not supplied

## 9. Results

**Not run.** Date carried out, people present, differences, observations, data files and restoration results: none.

## 10. Conclusions and ledger updates

T-006 remains Planned, not Authorised or Done. This amendment identifies already reviewed software and proposes its execution procedure; electrical/command compatibility remains untested. No claim is confirmed by candidate bytes, documentation, software simulation or the owner's earlier socket/COM-port observations. A future results review must identify which narrow claims were supported, contradicted or left unresolved.
