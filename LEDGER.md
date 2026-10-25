# LEDGER — evidence, decisions, disagreements and outstanding tests

The ledger is the project's shared memory. It records what we believe and where each belief came from, whether it has been tested on the owner's equipment, what has been decided, where views differ, and what still needs testing. Both agents update it only through reviewed pull requests.

## How to read the ledger

**Every claim carries two separate labels** (the owner's rule 3). One says where the claim came from; the other says whether it has been tried on the owner's equipment. Neither label implies the other.

**Provenance — where did the claim come from?**

| Label | Meaning |
|---|---|
| `Owner` | Stated by the owner |
| `Primary` | Official documentation, manuals, standards, or a tool's own documentation — cited, and actually consulted |
| `Secondary` | Forums, community wikis, articles or other projects — cited, and actually consulted |
| `AI: <system>` | Produced by an AI system, for example `AI: ChatGPT` or `AI: Claude Code`. A hypothesis until checked |
| `None yet` | No source identified |

**Equipment test status — has it been tried on the owner's equipment?**

| Label | Meaning |
|---|---|
| `Not tested` | No test yet |
| `Planned` | A written test plan exists, but is not yet authorised |
| `Authorised` | The owner has authorised the plan; it has not been carried out yet |
| `Confirmed` | Tested on the owner's equipment; the result supports the claim (linked) |
| `Contradicted` | Tested; the result goes against the claim (linked) |
| `Inconclusive` | Tested; the result is unclear (linked) |
| `N/A` | Cannot be tested on equipment — for example a decision, or the owner's own description of their equipment |

Software simulations never change the equipment test status. Two agents agreeing is not evidence.

**Tests** (section 5) move through: `Waiting for the owner` (owner checks only) or `No plan yet` → `Planned` → `Authorised` → `Done`. A test removed from scope is retained as `Superseded — out of scope`, with the decision that superseded it.

**IDs:** `S` source · `C` claim · `D` decision · `X` disagreement · `T` test · `Q` open question. IDs are never reused or renumbered. An entry that is replaced is marked "superseded by …", not deleted.

## 1. Sources

| ID | Source | Produced by | Original date | In this repository | Status |
|---|---|---|---|---|---|
| S-001 | Repository setup brief | Owner | 2026-10-24 | [docs/briefs/2026-10-24-repository-setup.md](docs/briefs/2026-10-24-repository-setup.md) | Archived word for word |
| S-002 | Claude feasibility report | AI: Claude (Anthropic) | 2026-10-23 | Not yet | Awaiting import; contents not available to agents |
| S-003 | ChatGPT critique | AI: ChatGPT (OpenAI) | Unknown | Not yet | Awaiting import; contents not available to agents |
| S-004 | Owner's review decisions and cable purchase confirmation | Owner | 2026-10-24 | [docs/briefs/2026-10-24-review-decisions.md](docs/briefs/2026-10-24-review-decisions.md) | Review decisions, purchase details and total price supplied by the owner |
| S-005 | Ex-Link protocol investigation and proposed offline verification | AI: Codex (OpenAI) | 2026-10-24 | [Research report](docs/research/2026-10-24-exlink-protocol-investigation.md) | Source inspection and local arithmetic completed; proposed software suite not executed. Merged by the owner in PR #3. The archived report says it awaits Claude Code's re-review; whether that re-review took place is not recorded |
| S-006 | Samsung-branded Consumer RS232 Control Worksheet, community-hosted PDF | Samsung attribution on document; PDF metadata names Anthony Moliterno; original distribution not authenticated | 2023-06-27 creation metadata; revision unknown | [Citation and page references in S-005](docs/research/2026-10-24-exlink-protocol-investigation.md#sources-actually-consulted) | Inspected 2026-10-24 at pinned community mirror; no manufacturer-hosted or exact-model confirmation |
| S-007 | Home Assistant Libraries samsung-exlink, commit e2489b33c720c36d1995392b803f2336baf7b808 | Home Assistant Libraries contributors | 2026-10-17 commit | [Pinned source references in S-005](docs/research/2026-10-24-exlink-protocol-investigation.md#sources-actually-consulted) | Inspected 2026-10-24; primary evidence of its code, secondary evidence of TV behaviour; references S-006 |
| S-008 | mgoff/go-samsung-exlink, commit 3bed0c96a57034299cfb320589be59a1588bfd78 | mgoff and contributors | 2017-02-08 commit | [Pinned source reference in S-005](docs/research/2026-10-24-exlink-protocol-investigation.md#sources-actually-consulted) | Inspected 2026-10-24; source literal discrepancy recorded as X-001 |
| S-009 | Owner's webcam menu-guard requirement, with answers to three follow-up questions | Owner | 2026-10-24 | [docs/briefs/2026-10-24-webcam-menu-guard.md](docs/briefs/2026-10-24-webcam-menu-guard.md) | Archived word for word |
| S-010 | Owner's answers to Claude Code's design-review questions: whole-screen menu guard, Ex-Link socket check and repository visibility | Owner | 2026-10-24 | [docs/briefs/2026-10-24-whole-screen-menu-guard.md](docs/briefs/2026-10-24-whole-screen-menu-guard.md) | Archived word for word |
| S-011 | Owner's description of where the meter hangs during readings, with answers to two follow-up questions: the screen area the meter hides, and recording | Owner | 2026-10-25 | [docs/briefs/2026-10-25-meter-placement.md](docs/briefs/2026-10-25-meter-placement.md) | Archived word for word |

## 2. Claims

The initial claims come from the owner's brief (S-001); the cable purchase is owner-reported in S-004; the webcam claims follow from the owner's menu-guard requirement (S-009), widened to the whole screen (S-010); the meter's position is owner-reported in S-011. None of the equipment capabilities has been tested. A purchase record does not establish compatibility. Later research claims identify their own sources; source inspection and software arithmetic do not change equipment test status.

| ID | Claim | Provenance | Equipment test status | Tests | Notes |
|---|---|---|---|---|---|
| C-001 | The equipment is a Samsung UE49KS7000UXXU TV, a Datacolor Spyder5 colorimeter, a Windows PC and a Denon AVC-X3800H receiver. | Owner (S-001) | N/A | — | Firmware versions, settings and connections are not yet recorded (owner checks T-001 and T-002). |
| C-002 | ArgyllCMS can take measurements with the Spyder5 on the owner's PC. | Owner (S-001: intended architecture) | Not tested | T-003 | |
| C-003 | A validated spectral correction can be obtained for this meter and TV. | Owner (S-001: intended architecture) | Not tested | T-004 | What counts as "validated", and how to check it, is open (Q-001). |
| C-004 | A controlled test-pattern generator on the PC can show exact, known colours on the TV. | Owner (S-001: intended architecture) | Not tested | T-002, T-005 | That the signal must not be altered on the way — by graphics settings, Windows colour management or the receiver — is Claude Code's reading of "controlled". |
| C-005 | Software can adjust the TV's picture settings through Samsung Ex-Link on the owner's firmware. | Owner (S-001: intended interface) | Not tested | T-001, T-006 | S-001: compatibility "has not yet been demonstrated". Ex-Link is the only control route in scope under D-006; the selected cable does not establish compatibility. |
| C-006 | Software can adjust the TV's picture settings through network remote commands on the owner's firmware. | Owner (S-001: intended interface) | Not tested | T-007 (superseded) | Superseded by D-006 — network control is out of scope. Retained as history, not an active dependency; compatibility was never demonstrated. |
| C-007 | A numerical optimisation engine, using the TV's own controls in a closed loop, can bring the picture close to Rec.709, D65 and BT.1886. | Owner (S-001: project objective) | Not tested | T-001, T-008 | Depends on C-002 to C-005 and on which controls the TV offers, under the Ex-Link-only decision D-006. The optimiser can be developed in simulation first; that will not change this status. |
| C-008 | The owner purchased a DSD TECH USB RS232 to 3.5mm Serial Cable with FTDI FT232RL Chip 6FT on 24 October 2026 at 21:00, for £15.99 in total including delivery. | Owner (S-004) | N/A | — | Purchase record only. The owner wrote "2100" without a time zone (S-004); earlier records added "Europe/London" as an assumption. The product title and specifications are owner-reported; delivery status is unknown. Cable and TV compatibility remain untested (T-006). [Owner-supplied product link](https://www.amazon.co.uk/dp/B07XXWVH69). |
| C-009 | The consulted consumer-TV protocol profile uses seven binary bytes, header 08 22, four command/value bytes and a negative-sum modulo-256 checksum. | Secondary: S-006 community-hosted Samsung-branded worksheet p. 2, original distribution unverified; S-007 implementation | Not tested | T-009 (software only) | Generic source-supported profile; no assertion of support on this TV. The library references the worksheet, so they are not independent confirmations. |
| C-010 | S-007 specifies 9600 8N1 and recognises success 03 0C F1 and failure 03 0C FF; S-006 p. 3 documents success feedback. These short replies contain no command identity or setting value. | Secondary for TV behaviour: S-006, S-007; Primary for S-007 implementation | Not tested | T-009 (software only) | Timing constants are library policies. Acknowledgement or stored commanded state is not independent verification of a changed TV setting. |
| C-011 | The consulted sources do not establish KS7000 calibration-command support, signed-value encoding, ranges, persistence, readback or cable compatibility. Generic calibration commands and limited status-query extensions appear in the sources. | Secondary: S-006 pp. 1, 4 and S-007; research limitation recorded by AI: Codex (OpenAI), S-005 | Not tested | T-001, T-006 | Exact-model Samsung page was inaccessible. Absence of verified evidence here is not evidence of incompatibility. Q-006 remains open; C-005 stays unconfirmed. |
| C-012 | S-008's published power-on literal ends D6; applying the documented checksum to its first six bytes gives D4, consistent with S-007. | Primary for literal source code: S-008; local arithmetic by Codex (OpenAI), recorded in S-005 | N/A | — | Arithmetic discrepancy X-001; reason for the literal and TV handling are unknown. No hardware inference. |
| C-013 | This additive checksum can miss byte permutations and compensating changes; a valid checksum cannot establish command validity or authenticity. | AI: Codex (OpenAI), mathematical deduction and synthetic permutation calculation in S-005 | N/A | T-009 (software only) | Local arithmetic completed; no parser or hardware behaviour tested. |
| C-014 | A small pure encoder/parser with an in-memory fake, independent literal fixtures and explicit timeout/error handling can be verified without a hardware transport. | AI: Codex (OpenAI), proposal S-005 | N/A | T-009 (software only) | Proposed; no implementation or verification suite executed. No real transport or real-mode selector is proposed in this slice. |
| C-015 | The owner's webcam, once positioned, can reliably show whether a menu is visible anywhere on the TV screen while patches are being measured. | None yet — the owner's requirements (S-009, S-010) rely on it | Not tested | T-010 | No detection method chosen yet. Widened from the lower portion to the whole screen by D-010. Detection can first be developed on recorded or synthetic pictures (software only); that will not change this status. |
| C-016 | The owner has a webcam to use for the menu guard. | Owner (S-009) | N/A | — | Model, connection and position not yet recorded (Q-007). No purchase needed, so the budget is unchanged. |
| C-017 | Proposed measurement gate: Clear/Menu visible/Unknown states across the whole TV screen, a fresh clear settling interval, whole-reading rejection, safe cancellation or draining, provisional results and fresh-read recovery. | AI: Codex (OpenAI), [design proposal](docs/webcam-measurement-gate.md) building on D-008 and D-009 as widened by D-010 | N/A | T-011 | Design proposal only; not implemented. Adds implementation detail to D-009 without replacing it. |
| C-018 | Capture/exposure timestamps, bounded clock uncertainty and camera delivery limits can establish which camera observations belong to each meter acquisition before a result is accepted. | AI: Codex (OpenAI), timing hypothesis in the [design proposal](docs/webcam-measurement-gate.md#timing-and-detection-limits) | Not tested | T-011 (software only), T-012 | Unbounded timing or incomplete coverage must block acceptance. Synthetic checks do not establish the real camera or meter's timing behaviour (Q-009). |
| C-019 | The combined detector and measurement gate can exclude interference from menus anywhere on the TV screen throughout real meter acquisitions on the owner's setup (D-010). | AI: Codex (OpenAI), capability hypothesis extending C-015 to detection and acquisition timing | Not tested | T-011 (software only), T-012 | Finite frame sampling, missed detections and latency require validation; no absolute detection guarantee is established. Webcam setup remains Q-007 and the pre-reading clear duration remains Q-008; additional acceptance criteria are Q-009 and the menu definition remains Q-010. |
| C-020 | S-006 and S-007 describe two consumer-TV serial routes: a native 3.5 mm Ex-Link jack (their examples say Q70 and above), or a proprietary Samsung USB-to-Ex-Link dongle (8000 / Q60) requiring EXT Link Support and USB Serial in the service menu. Neither source identifies the 2016 KS7000 as supported. | Secondary: S-006 p. 1 and S-007 README, consulted at the pinned versions in S-005 | Not tested | T-001, T-006 | Source examples are not a compatibility list for the owner's TV. C-008's USB-to-3.5 mm cable is a candidate for the native-jack route, not evidence of support for the proprietary-dongle route. Check the TV's accessible port labels first; no service-menu step or dongle purchase is authorised. |
| C-021 | The documented 3.5 mm pin-out is tip = data received by the controller (TV transmit), ring = data transmitted by the controller (TV receive), sleeve = ground. The selected cable's wiring and electrical compatibility are unverified. | Secondary: S-006 p. 2 and S-007 README, consulted at the pinned versions in S-005 | Not tested | T-006 | Controller perspective is explicit to avoid reversing transmit/receive. A matching connector alone does not establish compatible wiring or voltage levels. |
| C-022 | The cited material contains service-menu hazards: KEY_FACTORY (0x3B), Factory-SVB / Expert-N/D Adj, and a script that sends a service-menu IR sequence through a network IR transmitter. | Secondary for TV effects: S-006 pp. 4–5; Primary for code: S-007 scripts/show_service_menu.py; consulted in S-005 | Not tested | T-009 (software only) | T-009 must exclude factory/service-menu keys and commands from its allowlist and reject them without even a fake write. The script must not run; its IR/network route is outside D-006. No service-menu behaviour is verified or authorised. |
| C-023 | During readings the Spyder5 will hang by its USB cable in the middle of the TV screen. It is circular, about 5 cm across, and its cap, about the same size, hangs beneath it. | Owner (S-011) | N/A | — | The owner's description of the planned set-up. The meter, its cap and its cable hide part of the screen from the webcam; D-011 decides how that area is treated. The owner did not say where the cable runs; Claude Code assumes it comes down the front of the screen from the top edge (unverified). How much the webcam cannot see depends on where the webcam is placed (Q-007) and is to be found in T-010. |
| C-024 | Any TV menu or pop-up that covers part of the screen hidden by the meter, its cap or its cable (C-023) is, at the same time, also visible somewhere the webcam can see. | None yet — D-011 relies on it | Not tested | T-010 | If T-010 does not confirm this, D-011 means no reading is accepted. "At the same time" is Claude Code's reading of the owner's "also appears" (S-011): a menu hidden behind the meter for even part of a reading would otherwise go unseen. T-010 can only check the menus and pop-ups it shows, so its plan must say which; what counts as a menu is Q-010. |

## 3. Decisions

| ID | Decision | Decided by | Date | Status |
|---|---|---|---|---|
| D-001 | Scope: a free, open-source Windows Python application for closed-loop, TV-side calibration. SDR Rec.709, D65 and BT.1886 first; HDR investigation secondary. Additional hardware no more than £25 in total. No commercial calibration packages to be recommended. | Owner (S-001) | 2026-10-24 | In force |
| D-002 | The nine working rules, quoted in [AGENTS.md section 2](AGENTS.md#2-the-owners-working-rules). | Owner (S-001) | 2026-10-24 | In force |
| D-003 | Intended architecture: ArgyllCMS for measurements, validated spectral corrections, a controlled test-pattern generator, a numerical optimisation engine, and a TV-control backend using Samsung Ex-Link or network remote commands. | Owner (S-001) | 2026-10-24 | Interface choice superseded by D-006 (Ex-Link only). The remaining architecture is provisional; compatibility is not demonstrated. |
| D-004 | Import the original Claude feasibility report (S-002) and ChatGPT critique (S-003) after the setup has been reviewed. | Owner (S-001) | 2026-10-24 | Pending |
| D-005 | Working conventions that go beyond the owner's wording, listed below. | Proposed by Claude Code; accepted by the owner's merge of the setup pull request (PR #1) | 2026-10-24 | In force — amended by D-007 |
| D-006 | Use Samsung Ex-Link only for TV control. Network remote control is out of scope. Record the selected cable and completed purchase (C-008); this is neither approval for another purchase nor authorisation for any physical test. | Owner (S-004) | 2026-10-24 | In force — supersedes D-003's interface choice; C-006 and T-007 retained as superseded history. Ex-Link and cable compatibility remain untested. |
| D-007 | Apply the two approved review corrections: the PR safety checklist must prohibit unauthorised equipment operation and require links to the approved plan and results where applicable; read-only reviews may finish with findings without a new PR, and the author records unresolved disagreements. | Owner (S-004) | 2026-10-24 | In force — amends the proposed workflow under D-005. |
| D-008 | Webcam menu guard: a webcam observes the TV throughout profiling, and no observation of a patch may be taken when any menu bar is visible in the lower portion of the screen at any point. The exact extent of the "lower portion" is to be set after a webcam test (T-010) shows where the TV's menu bars appear (Q-008). | Owner (S-009) | 2026-10-24 | In force — a requirement for the final program; not yet built or tested (C-015). Widened to the whole screen by D-010; Q-008's boundary question is superseded. |
| D-009 | How D-008 is applied: the working details listed below. | Proposed by Claude Code; accepted by the owner's merge of PR #6 | 2026-10-24 | In force. Under D-010, "lower portion" in items 1 and 2 means the whole screen. |
| D-010 | Whole-screen menu guard. The owner's words (S-010): "If a menu pops up anywhere, the reading from the Spyder shuld be ignored until the menu has gone. It will ruin the reading." A menu visible anywhere on the TV screen during a reading invalidates that reading; it is repeated once the menu has gone, as D-009 item 2 describes. | Owner (S-010) | 2026-10-24 | In force — widens D-008 from the lower portion of the screen to the whole screen. Not yet built or tested (C-015). What counts as a "menu" is Q-010. |
| D-011 | Screen area hidden by the meter. The owner chose this option, worded by Claude Code (S-011): "Ignore the hidden area only if the webcam test (T-010) shows that any TV menu that could cover it also appears somewhere the webcam can see. Until then, or if the test fails, no readings are accepted." The hidden area is the part of the screen behind the meter, its cap and its USB cable (C-023). | Owner (S-011) | 2026-10-25 | In force — a condition on D-010. Until T-010 confirms C-024, the hidden area counts as a view the webcam cannot confirm under D-009 item 1, so the guard accepts no reading. Not yet tested. |

**D-005 in detail.** Each item can be accepted or rejected separately. D-007 records the owner's approved amendments to the review and finish workflow; it does not approve the other proposed conventions.

1. **Branches:** Codex uses `codex/<topic>` branches, mirroring rule 1's `claude/` branches.
2. **Independence:** rule 4 applied to both vendors and to earlier AI reports — two Anthropic agents also count as one reviewer.
3. **Pull requests:** one topic per pull request; reviewers comment but do not push to the author's branch; only the owner merges; no force-pushing or branch deletion unless the owner asks.
4. **"Substantive":** anything touching code, claims, evidence, decisions, tests, instructions, safety rules or scope; when in doubt, a change is substantive; only the owner can waive review.
5. **Evidence:** AI-generated material, including an agent's own background knowledge, is a hypothesis until checked or tested; citations give enough detail to find the source again; agreement between agents is not evidence; archived originals are never edited.
6. **Equipment safety:** rule 6 extended to the Denon receiver, to searching the home network and to displaying measurement patterns; physical tests need a written plan, the owner's authorisation of specific steps (copied into the plan word for word) and the owner's presence; extra precautions for the service menu.
7. **Code:** hardware-facing code defaults to simulation, needs a deliberate setting to reach real equipment, and logs every command it sends. Until Q-002 and Q-003 are settled: only free and open-source dependencies, each recorded with its licence, and tests that run without hardware.
8. **Approvals:** rule 7 read as also covering changes to repository settings, making the repository public, and equipment changes that cannot be restored; a purchase proposal gives the item, price, supplier and running total.
9. **Privacy:** no credentials, network addresses or serial numbers are committed; private settings live in `local/` or `*.local.*` files, which git ignores; no vendor software, vendor calibration data or downloaded tools are committed.
10. **Records and routine:** the ledger's format and ID scheme, the `docs/` layout, the start-and-finish checklist in AGENTS.md section 4, and the owner's setup brief archived word for word in `docs/briefs/`.
11. **Precedence:** the owner's instructions in a current conversation override AGENTS.md, which is then updated by pull request; conflicts inside AGENTS.md go to the owner.

**D-009 in detail.** Claude Code's proposals for applying the owner's menu guard (D-008). Each item can be accepted or rejected separately; none of them narrows D-008.

1. **Fail safe:** if the webcam cannot confirm that the lower portion is clear (for example no picture, camera disconnected, view blocked, picture too dark or too bright, or pictures out of date), no reading is taken.
2. **Whole reading window:** the lower portion is watched from just before a reading starts until it ends. A menu bar seen at any moment in that window means the reading is discarded and repeated once the screen is clear again. How long "just before" lasts is part of Q-008.
3. **Seeing, not assuming:** the guard decides from what the webcam shows, never from what the software expects the TV to be showing (for example, "no command was sent, so no menu can be open").
4. **Nothing silent:** every blocked or discarded reading is logged with its time and reason. A reading taken while the guard was not satisfied is never kept.
5. **Privacy:** webcam pictures can show the owner's room and people. They stay in the private `local/` folder and are never committed, unless the owner has checked and approved a specific picture as evidence.
6. **Equipment rule:** the webcam is treated like the TV and the meter. No agent turns it on or captures pictures from it outside an authorised test plan; software-only work uses recorded or synthetic pictures.

## 4. Disagreements

Source discrepancy X-001 is recorded below. The earlier Claude report and ChatGPT critique remain unavailable; no disagreement between those documents is inferred. Future disagreements between reports and reviewers will be recorded here in this format:

> **X-NNN — topic** · Status: Open / Settled by evidence / Decided by the owner
>
> - **Position A** — held by …; evidence: …
> - **Position B** — held by …; evidence: …
> - **What would settle it:** a test (T-…) or a source (S-…)
> - **Outcome:** only once settled — how, when and by whom

**X-001 — Published Ex-Link power-on checksum** · Status: Arithmetic resolved; source discrepancy unexplained.

- **Source A:** S-008's code contains `08 22 00 00 00 02 D6`; no explanation for that final byte was established.
- **Source B:** S-006's checksum rule and S-007's literal imply `08 22 00 00 00 02 D4`.
- **Evidence:** local arithmetic on 2026-10-24 gives a first-six-byte sum of `0x2C`, hence checksum `0xD4`. The S-008 complete frame sums to `0x02` modulo 256. [Record in S-005](docs/research/2026-10-24-exlink-protocol-investigation.md#source-inconsistency-and-arithmetic-checked).
- **Outcome:** use the S-008 literal only as an offline negative fixture for this profile. The arithmetic does not establish a protocol variant or what a TV would do. Author explanation or further source history could explain the literal; none has been obtained. No equipment test is proposed to settle this discrepancy.

## 5. Outstanding tests

**The physical-test candidates below have no written plan and none is authorised. No agent may carry them out** ([AGENTS.md section 7](AGENTS.md#7-equipment-safety-rule-6)). An "owner check" means the owner looks something up for themselves, without a meter and without any agent operating the equipment. T-009 is separately labelled software-only: its proposed plan cannot operate equipment and does not authorise or complete T-006. T-011 is separately labelled software-only; its proposed checks do not authorise T-010 or T-012.

| ID | What it would establish | Equipment involved | Kind | For | Status |
|---|---|---|---|---|---|
| T-001 | The TV's firmware version, and which picture controls its menus offer (for example white balance, gamma and colour space), with their ranges; whether accessible port labels identify a native 3.5 mm Ex-Link jack | TV | Owner check | C-005, C-007, C-011, C-020 | Waiting for the owner; visual/documentation check only for the port, with no cable connection or service-menu entry |
| T-002 | How the PC, receiver and TV are connected, and the relevant details of each — for example the PC's Windows version, graphics hardware and video output settings, and the receiver's video settings | PC, receiver, TV | Owner check | C-004 | Waiting for the owner |
| T-003 | Whether ArgyllCMS on the owner's PC recognises the Spyder5 and takes a reading | PC, Spyder5 | Physical test — needs authorisation | C-002 | No plan yet |
| T-004 | How a spectral correction for this TV and meter can be obtained and validated | Spyder5, TV | Research first; any physical step needs authorisation | C-003, Q-001 | No plan yet |
| T-005 | Whether test patterns reach the TV exactly as generated | PC, receiver, TV; possibly the Spyder5 | Physical test — needs authorisation | C-004 | No plan yet |
| T-006 | Whether the selected cable's wiring and electrical levels match the TV's documented Ex-Link connection, and whether the TV responds to commands on its firmware | TV, PC and the owner-purchased DSD TECH USB RS232 to 3.5mm cable (C-008); delivery status unknown | Physical test — needs authorisation | C-005, C-011, C-020, C-021 | No plan yet; no physical test authorised. Cable specifications and compatibility are not verified. Any plan must establish the applicable connection route and pin-out first; no service-menu operation or dongle purchase is authorised. |
| T-007 | Whether the TV responds to network remote commands, and whether these can reach picture settings | TV, PC, home network | Historical test candidate only | C-006 (superseded) | Superseded — out of scope under D-006; not authorised and not an active dependency |
| T-008 | Whether a full closed-loop calibration run improves accuracy on this TV using Ex-Link | All | Physical test — needs authorisation | C-007 | No plan yet; depends on T-001 to T-006, and on T-010 because the webcam guard (D-008, D-010) is required for any calibration run |
| T-009 | Whether a pure Ex-Link encoder/parser matches cited byte fixtures, handles malformed/late replies predictably, rejects factory/service-menu commands and has no hardware I/O path | None; in-memory bytes and fake clock only | Software-only proposal; not an equipment test | C-009, C-010, C-013, C-014, C-022 | Planned in [S-005](docs/research/2026-10-24-exlink-protocol-investigation.md#proposed-software-only-verification-plan--t-009); no implementation or suite execution yet |
| T-010 | Whether the owner's webcam, as positioned, sees the whole TV screen and reliably shows menus anywhere on it while patterns are displayed (D-010); where and how the TV's menus appear; and, with the meter hung in place, which parts of the screen the meter, its cap and its cable hide from the webcam, and whether any menu or pop-up could cover those parts without also showing elsewhere (D-011) | Webcam, TV, PC; menus shown on the TV; the Spyder5 hung in place but not measuring | Physical test — needs authorisation | C-015, C-024 | No plan yet |
| T-011 | Whether the proposed webcam gate blocks or rejects readings for menus anywhere on the TV screen, camera uncertainty, incomplete screen or timing coverage, timestamp uncertainty and late results | None; synthetic images/events, fake meter and clock | Software-only proposal; not an equipment test | C-017, C-018, C-019 | Planned in the [design proposal](docs/webcam-measurement-gate.md#proposed-software-only-checks--t-011); not implemented or executed |
| T-012 | Whether the detector and timing integration exclude interference from menus anywhere on the TV screen throughout real meter acquisitions on the owner's setup (D-010) | Webcam, TV, PC and meter as required by a future plan | Physical validation — needs authorisation | C-018, C-019 | No plan yet; no physical test authorised. Builds on T-010's whole-screen view and menu-location findings; Q-009 must define additional validation criteria. |

## 6. Open questions

| ID | Question | Why it matters | Who decides | Status |
|---|---|---|---|---|
| Q-001 | How should a spectral correction be validated, given that the owner's listed equipment includes no reference instrument? | The brief asks for *validated* corrections; what that means must be agreed before T-004 can be planned. | Owner, after research by both agents | Open |
| Q-002 | Which open-source licence should the project use? | Needed before the project is published. It must be compatible with the licences of tools the project relies on, such as ArgyllCMS (not yet checked). | Owner | Open |
| Q-003 | Which Python version and Windows packaging approach? | Affects how the owner installs and runs the application. | Owner, on a proposal in a later pull request | Open |
| Q-004 | Should `main` be protected in GitHub's settings so that it can change only through pull requests? | Would enforce rule 1 automatically. Changing settings needs the owner's approval, and whether GitHub offers this for a private repository may depend on the account's plan (not yet checked). | Owner | Open |
| Q-005 | How will Codex review pull requests — directly on GitHub, or with the owner passing its review on? | Decides the exact review steps in [docs/workflow.md](docs/workflow.md). | Owner | Open |
| Q-006 | Which authenticated, model-applicable sources establish Ex-Link calibration commands, value encodings, ranges and readback for UE49KS7000UXXU and its firmware? | Generic command tables and fake acknowledgements cannot establish C-005 or the cable's electrical compatibility. See S-005 and C-011. | Research by both agents; owner for any later physical-test authorisation | Open; manufacturer page inaccessible during this investigation |
| Q-007 | Which webcam will be used (model and connection), and where will it be placed so that it sees the whole screen clearly without getting in the meter's way? | The menu guard (D-008) depends on a clear, steady view of the screen. | Owner | Open — the owner has a webcam (C-016); details not yet recorded |
| Q-008 | How long before a reading must the screen already be clear? | Affects D-009 item 2. The original question of where the "lower portion" ends is superseded by D-010 (whole screen). | Owner, after T-010 | Open — boundary part superseded by D-010 |
| Q-009 | What capture/exposure timing, clock alignment, bounded latency, detector performance and recovery criteria would demonstrate that the proposed gate meets D-008 and D-009 as widened to the whole screen by D-010? | Define and validate whole-screen and temporal coverage and missed-detection limits before declaring the feature complete. Q-007 retains camera/placement choices and Q-008 retains only the pre-reading clear duration; Q-010 retains the menu definition. This question adds implementation assurance. | Agents propose an implementation and evidence; owner authorises physical validation and decides any change to the requirement | Open; no numeric thresholds or end-to-end capability established |
| Q-010 | What counts as a "menu" under D-010? Claude Code reads it as anything the TV draws over the picture — menus, banners, pop-ups, volume or setting sliders and notifications — but the owner has not confirmed this. | Decides what the webcam guard must detect. Claude Code's unverified hypothesis (AI: Claude Code) is that changing a picture setting may show an on-screen slider; if so, it would block readings until it fades. | Owner | Open |
| Q-011 | The repository is public on GitHub. The owner did not knowingly make it public (S-010). Should it be made private? | AGENTS.md section 8 treats making the repository public as needing the owner's approval, which is not recorded. While public, everything committed, including commit author details, is visible to anyone. Changing visibility is a repository-settings change only the owner can make. | Owner | Open — visibility observed by Claude Code on 2026-10-24; how it became public is unknown |

## 7. Hardware budget

Limit: **£25 in total** for additional hardware (D-001). Every purchase needs the owner's approval first.

| Item | Purpose | Price | Approved by the owner | Bought |
|---|---|---|---|---|
| [DSD TECH USB RS232 to 3.5mm Serial Cable with FTDI FT232RL Chip 6FT](https://www.amazon.co.uk/dp/B07XXWVH69) | Selected for the Ex-Link-only route; compatibility untested (T-006) | £15.99 total, including delivery | Owner reports their completed purchase (S-004); no new purchase approval | 24 October 2026, 21:00 (time zone not stated); delivery status unknown |

Owner-confirmed purchases: **£15.99** · Spent so far: **£15.99** · Remaining: **£9.01**.

The product title and specifications above are owner-reported, not independently verified. This record authorises no further purchase and no physical test. Ex-Link and cable compatibility remain **untested**.
