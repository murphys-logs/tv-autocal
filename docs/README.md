# Documentation

| Path | What it holds |
|---|---|
| [claim-notes.md](claim-notes.md) | Analysis behind the ledger claims |
| [workflow.md](workflow.md) | How the project runs, in plain English — roles, pull requests, reviews, approvals and physical tests — with a glossary |
| [equipment.md](equipment.md) | The owner's equipment: what is known and what still needs confirming |
| [plan.md](plan.md) | Claude Code's proposed order of work, reconciled by Codex with D-013: pass and stop conditions towards a first SDR calibration — a proposal, not a decision |
| [software/first-release-specification.md](software/first-release-specification.md) | Proposed first functioning release: owner journey, component responsibilities, stable requirements, separate software/equipment acceptance and dependency-ordered implementation checklist |
| [briefs/2026-11-08-audit-execution-and-review-requests.md](briefs/2026-11-08-audit-execution-and-review-requests.md) | Issued audit and follow-up instructions; Owner-issued audit wording drafted by Codex (S-097) |
| [briefs/](briefs/) | The owner's instructions to the agents, archived word for word |
| [research/](research/README.md) | Research material — reports, critiques and references — archived with its provenance |
| [tests/](tests/README.md) | Plans, authorisations and results of tests on the owner's equipment |
| [tests/component-execution.md](tests/component-execution.md) | Shared execution record, reconciles merged operator controls/meter-process evidence with owner inputs; unresolved prerequisites and authorisation |
| [tests/T-003-discovery-execution.md](tests/T-003-discovery-execution.md) | Discovery-only executable identities, one-launch completion/stopping proposal and unresolved owner inputs; no Argyll run |
| [tests/T-003-discovery-console.md](tests/T-003-discovery-console.md) | Accepted discovery choices and reviewed console entry/history/copy/power procedure; no physical authority |
| [tests/T-003-discovery-preflight.md](tests/T-003-discovery-preflight.md) | PRs #31/#32 reviewed the preflight and update gate; visual observations and software-only registry preparation remain separate, with Windows update gates and private evidence still required |
| [tests/T-003-samsung-update-evidence.md](tests/T-003-samsung-update-evidence.md) | Retired readiness method under D-021; retained source limits and former requirements are historical, with no collection requested |
| [tests/T-003-discovery-readiness.md](tests/T-003-discovery-readiness.md) | Remaining discovery-only preparation, owner authority and later session checks after PR #35; no hardware actions or completed observations |
| [tests/T-003-cec-change-proposal.md](tests/T-003-cec-change-proposal.md) | Document-only temporary CEC Off/restoration proposal; power-reset method, review of the future executable amendment and exact authority still required; planning reviewed in PR #37 |
| [tests/T-003-discovery-record.example.md](tests/T-003-discovery-record.example.md) | Blank template for private preparation/session records; no authorisation or results |
| [software/component-readiness.md](software/component-readiness.md) | Software-only presenter controls, interruption handling, meter supervision and offline verification |
| [software/t009-prototype.md](software/t009-prototype.md) | Hardware-free T-009 prototype, source fixtures, manual checks and their limits |
| [software/renderer-cycle.md](software/renderer-cycle.md) | Off-screen renderer, simulated change/exit/wait/read controller, technical choices and manual checks |
| [software/integration.md](software/integration.md) | Offline presentation, meter transcript, command-audit and observation contracts, with technical choices and verification |
| [software/component-tools.md](software/component-tools.md) | Bounded Windows component-test tools, explicit execution gates, dependencies, offline checks and remaining physical prerequisites |
| [reviews/2026-11-08-ground-up-review-prompt.md](reviews/2026-11-08-ground-up-review-prompt.md) | Task prompt for a complete independent project audit, its findings PR and subsequent Claude/Antigravity reviews; no audit performed by preparing the prompt |
| [reviews/](reviews/README.md) | Pull-request reviews and the [8 November ground-up audit/coverage](reviews/2026-11-08-ground-up-audit.md); no equipment validation |
| [reviews/2026-11-08-pr39-third-review-response.md](reviews/2026-11-08-pr39-third-review-response.md) | Antigravity P7 response assessment, 44-file coverage reconciliation and corrected worksheet identity/provenance |

## Two rules for this folder

1. **Sources and test results are kept apart.** `research/` records *what someone said*; `tests/` records *what happened on the owner's equipment*. This is how the project keeps to the owner's rule 3. [LEDGER.md](../LEDGER.md) links the two.
2. **Archived originals are never edited.** Once merged, documents in `briefs/` and `research/` keep their original wording; corrections and commentary go in the ledger. The README files that describe each folder are not archives and can be updated. The only exceptions are changes the owner has explicitly instructed, listed in [AGENTS.md section 6](../AGENTS.md#6-evidence-provenance-and-citations-rules-3-and-5).

## File names

- Briefs and research documents: `YYYY-MM-DD-short-title.md`, using the date of the original.
- Test plans: `T-NNN-short-title.md`, using the test's ledger ID.
