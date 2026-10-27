# T-006 — bounded Ex-Link control and restoration

> **Draft for independent review — NOT AUTHORISED. No equipment has been operated.**
> **Execution blocked:** electrical evidence, a reviewed physical transport, scope/restoration checks and the owner's specific authorisation are still required. T-009 is not that transport.

Prepared by Codex (OpenAI), 27 October 2026, against merged baseline `ba099e0a182713945c247636042286e6f9dca626`. This is a proposed experiment, not a statement that these commands work on the TV.

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
| Transport | Separately reviewed real sender, exact revision/hash, launch command, dependencies/licences, explicit opt-in, allowlist below, bounded receive log and manual step controls. Include logging through port closure and exact close/disconnect procedures on success and every stop path; exercise them offline first. | Not built; T-009 deliberately has no physical sender |
| Reply policy | Reviewed handling of initial/late/duplicate bytes, partial writes and per-command observations. No checksum or ACK establishes correlation or a changed setting. | Proposed below; physical transport review outstanding |
| Offline checks | Passing applicable T-009 checks; separate fixtures for the sender's Contrast/EXIT commands and late/duplicate-byte retention. T-009 retires after its first result and discards later script bytes; the physical sender must not copy that behaviour. | See [T-009](../software/t009-prototype.md); physical sender checks absent |
| Menu timing | A reviewed amendment identifies each normal menu/submenu used, its automatic-close timing and a send/observation interval that cannot overlap it. Unknown or overlapping timing makes EXIT inconclusive; do not transfer a timeout between different menus. | Missing; no timeout value assumed |
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

Only these three exact frames may be offered by the future sender. The contrast pair applies **only if the freshly observed baseline is 95**; otherwise stop and revise the reviewed plan. No arbitrary hex, other values, power, volume, factory, reset, white-balance, network or IR automation. The worksheet's command-result OSD toggle is not menu dismissal (C-066) and is excluded. The owner's ordinary handheld remote is used only for inspection/manual restoration as specified below.

## 2. Equipment and settings involved

- TV: UE49KS7000UXXU, reported firmware `T-JZMDEUC-1270.1`, intended Movie mode on HDMI 4. Confirm the active mode; S-033 did not establish the mode used during its observations.
- PC and delivered SH-U35B; recorded port COM3 is a historical observation. Select the explicitly identified device locally; no port scan or automatic selection. Keep private identifiers in ignored `local/` records.
- Denon remains on the recorded PC path with no receiver-setting changes in this plan. No meter or measurement patterns are used.
- ArgyllCMS can probe fast serial ports during startup, including help/discovery (C-090). Keep it, DisplayCAL and other discovery tools closed for the entire connected session; T-003/T-005 require the Ex-Link USB end disconnected from the PC before any meter-tool launch.
- Candidate serial profile: 9600 baud, 8 data bits, no parity, one stop bit, no flow control, binary bytes. 9600 8N1 comes from S-007 as recorded in [S-005](../research/2026-10-24-exlink-protocol-investigation.md), not a verified firmware setting. DTR/RTS/open-close behaviour must be fixed in the future sender's reviewed design; do not rely on terminal defaults.

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

These are future steps for the **owner with an agent present**, after all gates pass. The owner controls each send; no unattended sequence. Record the reviewed sender's command/hash in the plan before authorisation. The absent sender cannot be replaced with an improvised serial terminal.

1. **Owner and agent:** check every prerequisite, authorisation revision, stop method and normal-menu restoration procedure. Confirm firmware, input, mode, scope and Contrast 95; record section 3. If any differs, stop without connecting. Do not change the TV to fit these assumptions under this revision.
2. **Owner:** connect the verified cable by the reviewed route. **Agent with owner present:** open only the selected port with the fixed profile; transmit nothing for a proposed five-second observation period. Any incoming bytes (including apparent debug output) stop the test. Five seconds is a screening policy, not proof that later bytes cannot be unsolicited.
3. **Owner:** open an ordinary picture menu using the normal remote; record the opening time. **Agent:** request the single EXIT frame, once, within the approved interval that excludes automatic menu closure; record send time. Observe the reply for a proposed two-second deadline from completion of the full write. **Owner:** record when the ordinary menu closed and confirm it was within that interval, then wait two seconds (proposed Q-008 value). If automatic closure cannot be ruled out, record EXIT as inconclusive and stop. No reply, NACK, noise, duplicate or partial reply, wrong screen, or uncleared menu stops the test. Apply the same timing record and exclusion to steps 5 and 7.
4. **Agent:** send Contrast 94 once, with the same response handling. **Owner:** inspect the normal Contrast menu; it must read exactly 94 and no other inspected control may have changed unexpectedly. An ACK by itself does not pass this step. Stop on disagreement; do not continue to the next send as recovery.
5. **Agent:** send EXIT once. **Owner:** confirm closure and wait two seconds. This is a separate transaction, not a retry of step 3.
6. **Agent:** send Contrast 95 once **only on the normal successful path**. **Owner:** inspect the normal menu and verify exact restoration to 95 and the recorded visible settings.
7. **Agent:** send EXIT once. **Owner:** confirm closure and wait two seconds. Close the port, leave no sender running, and disconnect the cable using the reviewed connection procedure. Any scope restoration must follow the prerequisite amendment's exact normal-menu procedure, with its own final exit/wait.
8. **Owner and agent:** classify each result separately under section 7 and record all observations, including rejected bytes and failures. Stop; no further control or measurement test is implied.

Maximum: five single-frame transmissions on the successful path (EXIT, Contrast94, EXIT, Contrast95, EXIT). An unclear outcome ends it earlier. No resend; no automatic reconnect/resume; no automatic restore after a fault. The future sender must pause for the owner's observations between transmissions and retain all intervening receive bytes. A response outside the active window is unexpected and ends the run. ACKs have no transaction identity: silence or reconnecting cannot prove attribution. Therefore menu observations are mandatory, and a clean run still supports only the tested sequence, not a general transport guarantee.

## 6. What will be recorded

Plan revision/authorisation; sender revision/hash and dependency versions; identified device/profile (private locally); original settings and scope; monotonic and wall-clock timestamps; each exact transmitted frame, write count, all received bytes and timing, including bytes after a reply or stop until the port is closed; menu-open, send and menu-close times against the automatic-close boundary; owner menu observations; each stop reason; restored values and whether restoration was manual after a stop. Copy only privacy-checked excerpts into a future `T-006-data/` folder. Raw logs stay ignored.

**Measurement cycle:** no meter readings or calibration data are taken. After every successful change or menu inspection the proposed sequence uses EXIT, owner confirmation and a two-second delay. If EXIT fails, there is no further serial action; manual restoration includes ordinary menu exit/wait. This tests the exit method before T-013 relies on it. It does not detect later unexpected overlays. Q-008 remains open; two seconds is a design proposal for this revision, not established settling time.

## 7. How results will be judged

**ACK** means acknowledgement (the candidate success reply); **NACK** means a negative response. Neither identifies the command or verifies a changed TV setting.

| Result | Interpretation |
|---|---|
| Electrical evidence absent, sender absent or other gate open | Blocked before operation; no equipment result |
| `03 0C F1` within the proposed window | Candidate ACK only; not readback or proof of execution |
| `03 0C FF` | Candidate NACK as recognised by S-007; stop, record actual bytes |
| Missing/malformed/late/duplicate response, partial write, failed exit, unexpected menu/control | Inconclusive or contradicted for the specific tested behaviour; stop, no retry |
| EXIT visibly works, Contrast changes 95→94 and restores to 95 with required replies and observations | Supports only these exact controls/profile/session and their bounded restoration |
| All above plus scope restoration verified | T-006 bounded pass; does not establish white balance, CMS, HDR, persistence, readback or optical response |

No response alone does not prove a service-menu change is necessary or that every Ex-Link command is unsupported. Failed restoration is a failure, even if the initial change worked. T-013 and T-008 remain separate, unauthorised tests.

**Stop rules adopted:** [docs/plan.md stop rules](../plan.md#stop-rules-for-every-physical-stage) at full SHA `ba099e0a182713945c247636042286e6f9dca626`. Stop immediately on the owner's request, any unlisted behaviour, suspected electrical issue or uncertainty; no active recovery beyond the owner's recorded normal-menu restoration.

## 8. Owner's authorisation

**Not given.** The 27 October request authorises preparation and software-only work; it explicitly prohibits hardware operation now.

- Authorised: no
- Plan revision and steps authorised: none
- Conditions or limits: pending all prerequisites and independent review
- Date: not authorised
- Verbatim owner authorisation for a future test: not supplied

## 9. Results

**Not run.** Date carried out, people present, differences, observations, data files and restoration results: none.

## 10. Conclusions and ledger updates

This draft changes T-006 to Planned, not Authorised or Done. Electrical/command compatibility remains untested. No claim is confirmed by candidate bytes, documentation, software simulation or the owner's earlier socket/COM-port observations. A future results review must identify which narrow claims were supported, contradicted or left unresolved.
