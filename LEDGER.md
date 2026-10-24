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

**Tests** (section 5) move through: `Waiting for the owner` (owner checks only) or `No plan yet` → `Planned` → `Authorised` → `Done`.

**IDs:** `S` source · `C` claim · `D` decision · `X` disagreement · `T` test · `Q` open question. IDs are never reused or renumbered. An entry that is replaced is marked "superseded by …", not deleted.

## 1. Sources

| ID | Source | Produced by | Original date | In this repository | Status |
|---|---|---|---|---|---|
| S-001 | Repository setup brief | Owner | 2026-10-24 | [docs/briefs/2026-10-24-repository-setup.md](docs/briefs/2026-10-24-repository-setup.md) | Archived word for word |
| S-002 | Claude feasibility report | AI: Claude (Anthropic) | 2026-10-23 | Not yet | Awaiting import; contents not available to agents |
| S-003 | ChatGPT critique | AI: ChatGPT (OpenAI) | Unknown | Not yet | Awaiting import; contents not available to agents |
| S-005 | Ex-Link protocol investigation and proposed offline verification | AI: Codex (OpenAI) | 2026-10-24 | [Research report](docs/research/2026-10-24-exlink-protocol-investigation.md) | Source inspection and local arithmetic completed; proposed software suite not executed; independent Claude Code review outstanding |
| S-006 | Samsung-branded Consumer RS232 Control Worksheet, community-hosted PDF | Samsung attribution on document; PDF metadata names Anthony Moliterno; original distribution not authenticated | 2023-06-27 creation metadata; revision unknown | [Citation and page references in S-005](docs/research/2026-10-24-exlink-protocol-investigation.md#sources-actually-consulted) | Inspected 2026-10-24 at pinned community mirror; no manufacturer-hosted or exact-model confirmation |
| S-007 | Home Assistant Libraries samsung-exlink, commit e2489b33c720c36d1995392b803f2336baf7b808 | Home Assistant Libraries contributors | 2026-10-17 commit | [Pinned source references in S-005](docs/research/2026-10-24-exlink-protocol-investigation.md#sources-actually-consulted) | Inspected 2026-10-24; primary evidence of its code, secondary evidence of TV behaviour; references S-006 |
| S-008 | mgoff/go-samsung-exlink, commit 3bed0c96a57034299cfb320589be59a1588bfd78 | mgoff and contributors | 2017-02-08 commit | [Pinned source reference in S-005](docs/research/2026-10-24-exlink-protocol-investigation.md#sources-actually-consulted) | Inspected 2026-10-24; source literal discrepancy recorded as X-001 |

## 2. Claims

The initial claims come from the owner's brief (S-001). Later research claims identify their own sources. No equipment capability has been tested; source inspection and software arithmetic do not change that status.

| ID | Claim | Provenance | Equipment test status | Tests | Notes |
|---|---|---|---|---|---|
| C-001 | The equipment is a Samsung UE49KS7000UXXU TV, a Datacolor Spyder5 colorimeter, a Windows PC and a Denon AVC-X3800H receiver. | Owner (S-001) | N/A | — | Firmware versions, settings and connections are not yet recorded (owner checks T-001 and T-002). |
| C-002 | ArgyllCMS can take measurements with the Spyder5 on the owner's PC. | Owner (S-001: intended architecture) | Not tested | T-003 | |
| C-003 | A validated spectral correction can be obtained for this meter and TV. | Owner (S-001: intended architecture) | Not tested | T-004 | What counts as "validated", and how to check it, is open (Q-001). |
| C-004 | A controlled test-pattern generator on the PC can show exact, known colours on the TV. | Owner (S-001: intended architecture) | Not tested | T-002, T-005 | That the signal must not be altered on the way — by graphics settings, Windows colour management or the receiver — is Claude Code's reading of "controlled". |
| C-005 | Software can adjust the TV's picture settings through Samsung Ex-Link on the owner's firmware. | Owner (S-001: intended interface) | Not tested | T-001, T-006 | S-001: compatibility "has not yet been demonstrated". |
| C-006 | Software can adjust the TV's picture settings through network remote commands on the owner's firmware. | Owner (S-001: intended interface) | Not tested | T-001, T-007 | S-001: compatibility "has not yet been demonstrated". |
| C-007 | A numerical optimisation engine, using the TV's own controls in a closed loop, can bring the picture close to Rec.709, D65 and BT.1886. | Owner (S-001: project objective) | Not tested | T-001, T-008 | Depends on C-002 to C-006 and on which controls the TV offers. The optimiser can be developed in simulation first; that will not change this status. |
| C-009 | The consulted consumer-TV protocol profile uses seven binary bytes, header 08 22, four command/value bytes and a negative-sum modulo-256 checksum. | Secondary: S-006 community-hosted Samsung-branded worksheet p. 2, original distribution unverified; S-007 implementation | Not tested | T-009 (software only) | Generic source-supported profile; no assertion of support on this TV. The library references the worksheet, so they are not independent confirmations. |
| C-010 | S-007 specifies 9600 8N1 and recognises success 03 0C F1 and failure 03 0C FF; S-006 p. 3 documents success feedback. These short replies contain no command identity or setting value. | Secondary for TV behaviour: S-006, S-007; Primary for S-007 implementation | Not tested | T-009 (software only) | Timing constants are library policies. Acknowledgement or stored commanded state is not independent verification of a changed TV setting. |
| C-011 | The consulted sources do not establish KS7000 calibration-command support, signed-value encoding, ranges, persistence, readback or cable compatibility. Generic calibration commands and limited status-query extensions appear in the sources. | Secondary: S-006 pp. 1, 4 and S-007; research limitation recorded by AI: Codex (OpenAI), S-005 | Not tested | T-001, T-006 | Exact-model Samsung page was inaccessible. Absence of verified evidence here is not evidence of incompatibility. Q-006 remains open; C-005 stays unconfirmed. |
| C-012 | S-008's published power-on literal ends D6; applying the documented checksum to its first six bytes gives D4, consistent with S-007. | Primary for literal source code: S-008; local arithmetic by Codex (OpenAI), recorded in S-005 | N/A | — | Arithmetic discrepancy X-001; reason for the literal and TV handling are unknown. No hardware inference. |
| C-013 | This additive checksum can miss byte permutations and compensating changes; a valid checksum cannot establish command validity or authenticity. | AI: Codex (OpenAI), mathematical deduction and synthetic permutation calculation in S-005 | N/A | T-009 (software only) | Local arithmetic completed; no parser or hardware behaviour tested. |
| C-014 | A small pure encoder/parser with an in-memory fake, independent literal fixtures and explicit timeout/error handling can be verified without a hardware transport. | AI: Codex (OpenAI), proposal S-005 | N/A | T-009 (software only) | Proposed; no implementation or verification suite executed. No real transport or real-mode selector is proposed in this slice. |

## 3. Decisions

| ID | Decision | Decided by | Date | Status |
|---|---|---|---|---|
| D-001 | Scope: a free, open-source Windows Python application for closed-loop, TV-side calibration. SDR Rec.709, D65 and BT.1886 first; HDR investigation secondary. Additional hardware no more than £25 in total. No commercial calibration packages to be recommended. | Owner (S-001) | 2026-10-24 | In force |
| D-002 | The nine working rules, quoted in [AGENTS.md section 2](AGENTS.md#2-the-owners-working-rules). | Owner (S-001) | 2026-10-24 | In force |
| D-003 | Intended architecture: ArgyllCMS for measurements, validated spectral corrections, a controlled test-pattern generator, a numerical optimisation engine, and a TV-control backend using Samsung Ex-Link or network remote commands. | Owner (S-001) | 2026-10-24 | Provisional — interface compatibility not demonstrated (C-005, C-006) |
| D-004 | Import the original Claude feasibility report (S-002) and ChatGPT critique (S-003) after the setup has been reviewed. | Owner (S-001) | 2026-10-24 | Pending |
| D-005 | Working conventions that go beyond the owner's wording, listed below. | Proposed by Claude Code | 2026-10-24 | Proposed — takes effect if the owner merges the setup pull request |

**D-005 in detail.** Each item can be accepted or rejected separately.

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

**The physical-test candidates below have no written plan and none is authorised. No agent may carry them out** ([AGENTS.md section 7](AGENTS.md#7-equipment-safety-rule-6)). An "owner check" means the owner looks something up for themselves, without a meter and without any agent operating the equipment. T-009 is separately labelled software-only: its proposed plan cannot operate equipment and does not authorise or complete T-006.

| ID | What it would establish | Equipment involved | Kind | For | Status |
|---|---|---|---|---|---|
| T-001 | The TV's firmware version, and which picture controls its menus offer (for example white balance, gamma and colour space), with their ranges | TV | Owner check | C-005, C-006, C-007 | Waiting for the owner |
| T-002 | How the PC, receiver and TV are connected, and the relevant details of each — for example the PC's Windows version, graphics hardware and video output settings, and the receiver's video settings | PC, receiver, TV | Owner check | C-004 | Waiting for the owner |
| T-003 | Whether ArgyllCMS on the owner's PC recognises the Spyder5 and takes a reading | PC, Spyder5 | Physical test — needs authorisation | C-002 | No plan yet |
| T-004 | How a spectral correction for this TV and meter can be obtained and validated | Spyder5, TV | Research first; any physical step needs authorisation | C-003, Q-001 | No plan yet |
| T-005 | Whether test patterns reach the TV exactly as generated | PC, receiver, TV; possibly the Spyder5 | Physical test — needs authorisation | C-004 | No plan yet |
| T-006 | Whether the TV has a usable Ex-Link connection and responds to commands on its firmware | TV, PC; possibly a cable or adapter (any purchase needs approval) | Physical test — needs authorisation | C-005 | No plan yet |
| T-007 | Whether the TV responds to network remote commands, and whether these can reach picture settings | TV, PC, home network | Physical test — needs authorisation | C-006 | No plan yet |
| T-008 | Whether a full closed-loop calibration run improves accuracy on this TV | All | Physical test — needs authorisation | C-007 | No plan yet; depends on T-001 to T-007 |
| T-009 | Whether a pure Ex-Link encoder/parser matches cited byte fixtures, handles malformed/late replies predictably and has no hardware I/O path | None; in-memory bytes and fake clock only | Software-only proposal; not an equipment test | C-009, C-010, C-013, C-014 | Planned in [S-005](docs/research/2026-10-24-exlink-protocol-investigation.md#proposed-software-only-verification-plan--t-009); no implementation or suite execution yet |

## 6. Open questions

| ID | Question | Why it matters | Who decides | Status |
|---|---|---|---|---|
| Q-001 | How should a spectral correction be validated, given that the owner's listed equipment includes no reference instrument? | The brief asks for *validated* corrections; what that means must be agreed before T-004 can be planned. | Owner, after research by both agents | Open |
| Q-002 | Which open-source licence should the project use? | Needed before the project is published. It must be compatible with the licences of tools the project relies on, such as ArgyllCMS (not yet checked). | Owner | Open |
| Q-003 | Which Python version and Windows packaging approach? | Affects how the owner installs and runs the application. | Owner, on a proposal in a later pull request | Open |
| Q-004 | Should `main` be protected in GitHub's settings so that it can change only through pull requests? | Would enforce rule 1 automatically. Changing settings needs the owner's approval, and whether GitHub offers this for a private repository may depend on the account's plan (not yet checked). | Owner | Open |
| Q-005 | How will Codex review pull requests — directly on GitHub, or with the owner passing its review on? | Decides the exact review steps in [docs/workflow.md](docs/workflow.md). | Owner | Open |
| Q-006 | Which authenticated, model-applicable sources establish Ex-Link calibration commands, value encodings, ranges and readback for UE49KS7000UXXU and its firmware? | Generic command tables and fake acknowledgements cannot establish C-005 or the cable's electrical compatibility. See S-005 and C-011. | Research by both agents; owner for any later physical-test authorisation | Open; manufacturer page inaccessible during this investigation |

## 7. Hardware budget

Limit: **£25 in total** for additional hardware (D-001). Every purchase needs the owner's approval first.

| Item | Purpose | Price | Approved by the owner | Bought |
|---|---|---|---|---|
| *None yet* | | | | |

Approved so far: **£0** · Spent so far: **£0**
