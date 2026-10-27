# Documentation

| Path | What it holds |
|---|---|
| [claim-notes.md](claim-notes.md) | Analysis behind the ledger claims |
| [workflow.md](workflow.md) | How the project runs, in plain English — roles, pull requests, reviews, approvals and physical tests — with a glossary |
| [equipment.md](equipment.md) | The owner's equipment: what is known and what still needs confirming |
| [plan.md](plan.md) | Claude Code's proposed order of work, reconciled by Codex with D-013: pass and stop conditions towards a first SDR calibration — a proposal, not a decision |
| [briefs/](briefs/) | The owner's instructions to the agents, archived word for word |
| [research/](research/README.md) | Research material — reports, critiques and references — archived with its provenance |
| [tests/](tests/README.md) | Plans, authorisations and results of tests on the owner's equipment |
| [tests/component-execution.md](tests/component-execution.md) | Shared draft execution amendment: source/runtime identities, proposed display arrangement, authorisation records and unresolved inputs |
| [software/t009-prototype.md](software/t009-prototype.md) | Hardware-free T-009 prototype, source fixtures, manual checks and their limits |
| [software/renderer-cycle.md](software/renderer-cycle.md) | Off-screen renderer, simulated change/exit/wait/read controller, technical choices and manual checks |
| [software/integration.md](software/integration.md) | Offline presentation, meter transcript, command-audit and observation contracts, with technical choices and verification |
| [software/component-tools.md](software/component-tools.md) | Bounded Windows component-test tools, explicit execution gates, dependencies, offline checks and remaining physical prerequisites |
| [reviews/](reviews/README.md) | A log of reviews of pull requests — not evidence about the equipment, and not an archive |

## Two rules for this folder

1. **Sources and test results are kept apart.** `research/` records *what someone said*; `tests/` records *what happened on the owner's equipment*. This is how the project keeps to the owner's rule 3. [LEDGER.md](../LEDGER.md) links the two.
2. **Archived originals are never edited.** Once merged, documents in `briefs/` and `research/` keep their original wording; corrections and commentary go in the ledger. The README files that describe each folder are not archives and can be updated. The only exceptions are changes the owner has explicitly instructed, listed in [AGENTS.md section 6](../AGENTS.md#6-evidence-provenance-and-citations-rules-3-and-5).

## File names

- Briefs and research documents: `YYYY-MM-DD-short-title.md`, using the date of the original.
- Test plans: `T-NNN-short-title.md`, using the test's ledger ID.
