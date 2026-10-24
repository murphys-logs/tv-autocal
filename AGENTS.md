# AGENTS.md — shared instructions for Claude Code and Codex

These are the working instructions for **every AI agent** on this project. Codex reads this file directly. Claude Code reads it through `CLAUDE.md`, which contains only the import line `@AGENTS.md`. All shared rules live here, so both agents work from the same text; any vendor-specific file should only point here.

If an instruction the owner gives you in your current conversation conflicts with this file, follow the owner and propose an update to this file in a pull request. If two parts of this file conflict, stop and ask the owner.

## 1. Who is who

| Who | Role |
|---|---|
| **Owner** | The person who owns this repository and the equipment. Only the owner can authorise physical tests, give the approvals listed in rule 7, and decide whether a pull request is merged. |
| **Claude Code** (Anthropic) | AI coding agent. Works on `claude/…` branches and reviews Codex's pull requests. |
| **Codex** (OpenAI) | AI coding agent. Works on `codex/…` branches and reviews Claude Code's pull requests. |

Other AI tools can contribute material — the Claude feasibility report and the ChatGPT critique, for example — but they count as their vendor: ChatGPT and Codex are both OpenAI; the Claude apps and Claude Code are both Anthropic.

## 2. The owner's working rules

These nine rules are quoted exactly from the owner's setup brief of 24 October 2026, archived word for word in [docs/briefs/2026-10-24-repository-setup.md](docs/briefs/2026-10-24-repository-setup.md). "I" and "my" mean the owner. Only the owner can change these rules.

> 1. Work on a `claude/` feature branch, never directly on `main`.
> 2. All substantive changes require a pull request and independent review by the other vendor before I decide whether to merge.
> 3. Keep source provenance separate from whether a claim has been tested on my equipment.
> 4. Do not treat two OpenAI agents as two independent reviewers.
> 5. Do not invent experimental findings or citations.
> 6. Never operate the TV, meter or service menu autonomously. Software-only simulations are permitted. Physical tests require my explicit authorisation.
> 7. No purchases, paid APIs, automatic GitHub Actions, deployment or irreversible changes without my approval.
> 8. Make the workflow understandable to a non-programmer.
> 9. Record unresolved disagreements rather than forcing agreement.

Rule 1 was addressed to Claude Code; Codex follows it with `codex/` branches (section 5).

The rest of this file explains how agents apply these rules. It was drafted by Claude Code in the setup pull request and can be changed only by a reviewed pull request. Where it goes further than the owner's wording, the difference is listed under decision D-005 in [LEDGER.md](LEDGER.md#3-decisions).

## 3. Project scope (from the owner's briefs)

- **Goal:** a free, open-source Windows Python application for closed-loop, TV-side colour calibration of the owner's Samsung UE49KS7000UXXU, using the owner's existing Datacolor Spyder5 colorimeter, Windows PC and Denon AVC-X3800H receiver.
- **Priority:** SDR Rec.709, D65 and BT.1886. HDR investigation is secondary.
- **Budget:** additional hardware must not exceed £25 in total.
- **Do not recommend commercial calibration packages.**
- **Intended architecture:** ArgyllCMS for measurements, validated spectral corrections, a controlled test-pattern generator, a numerical optimisation engine, and a TV-control backend using **Samsung Ex-Link only**. The owner's later decision D-006 in [LEDGER.md](LEDGER.md#3-decisions) supersedes the original brief's alternative of network remote commands.
- **Selected cable:** the owner reports purchasing the DSD TECH USB RS232 to 3.5mm Serial Cable with FTDI FT232RL Chip 6FT (S-004). Purchase details and the remaining budget are in the ledger; purchase does not authorise any physical test.
- **Not yet demonstrated:** whether the selected cable and Ex-Link interface work with the owner's TV and firmware. Treat this as an open question to be tested, never as a premise.

## 4. Starting and finishing a task

### Before you start

1. Read this file, [LEDGER.md](LEDGER.md) and the documents relevant to the task.
2. Look at `main` and any open pull requests or branches, so you don't duplicate or contradict work in progress.
3. Work only from what is in the repository and the owner's current instructions. You have no access to earlier conversations — your own or anyone else's. If the owner refers to material that is not here, such as the earlier feasibility report and critique, say so and ask for it to be imported. Never reconstruct or guess its contents.
4. Check whether the task needs the owner's approval (sections 7 and 8). If it does, ask and wait.

### Before you finish

For tasks proposing repository file changes:

1. Update [LEDGER.md](LEDGER.md) with new or changed claims, decisions, disagreements, tests and questions.
2. Check that links between files work and that every ledger ID you mention exists.
3. Open a pull request and fill in every section of the [template](.github/PULL_REQUEST_TEMPLATE.md).
4. Tell the owner plainly what you did, what you did not do, what is untested, what needs their decision, and whether the pull request is ready for independent review — and by which agent.

For review-only tasks, finish by reporting findings and unresolved disagreements in the review or to the owner. A review alone does not require a ledger edit or another pull request. The pull-request author records unresolved disagreements in the ledger as part of the proposed changes.

## 5. Branches, pull requests and review (rules 1, 2 and 4)

- **Never commit directly to `main`.** Claude Code uses branches named `claude/<topic>`; Codex uses `codex/<topic>`.
- **One topic per pull request**, small enough to review properly.
- **Substantive changes need independent review.** A change is substantive if it touches code, claims, evidence, decisions, tests, instructions, safety rules or project scope. If in doubt, it is substantive. Only the owner can decide that a change is too minor to need review.
- **Independence is counted by vendor, not by agent.**
  - Claude Code's pull requests are reviewed by Codex; Codex's are reviewed by Claude Code.
  - Two OpenAI agents — ChatGPT and Codex, or two Codex sessions — are one reviewer, not two. The same applies to two Anthropic agents.
  - An earlier AI report counts as its vendor's view, not as an independent check.
- **Reviewers comment; they don't edit.** A reviewer does not push commits to the author's branch. Suggest changes in review comments, or open a separate pull request, so it stays clear who wrote what.
- **Only the owner merges.** No agent merges a pull request, closes the other agent's pull request, force-pushes, rewrites shared history or deletes branches unless the owner explicitly asks for that specific action.

## 6. Evidence, provenance and citations (rules 3 and 5)

- **Two separate labels for every claim.** Each factual claim that affects the design or the owner's equipment goes in [LEDGER.md](LEDGER.md) with:
  - **provenance** — where it comes from: the owner, primary documentation, a secondary source, an AI system, or none yet; and
  - **equipment test status** — whether it has been tested on the owner's own equipment.

  A well-sourced claim can be untested; a test result can lack any published source. Never let one label stand in for the other.
- **AI output is a hypothesis.** Material produced by an AI system — the Claude feasibility report, the ChatGPT critique and your own background knowledge — stays a hypothesis until it has been checked against a primary source or tested. Label it with the system that produced it.
- **Cite only what you have actually consulted.** Give enough detail to find it again: title, author or publisher, URL or document number, version or date, and the date you accessed it. If you could not check a source, write "unverified".
- **Never invent** measurements, test results, quotations, page numbers, URLs, version numbers or firmware behaviour. If something is unknown, write "unknown".
- **Simulations are not tests on equipment.** Label simulation results as simulations. They never change a claim's equipment test status.
- **Agreement is not evidence.** Two agents, or two vendors, agreeing does not make a claim true.
- **Archived originals stay untouched.** Once merged, archived documents in `docs/briefs/` and `docs/research/` are never edited; corrections and commentary go in the ledger. (The folders' README files are not archives and can be updated.)

## 7. Equipment safety (rule 6)

No agent may operate the owner's equipment on its own initiative. Agents running in the cloud normally cannot reach it, but an agent running on the owner's PC could, so these rules apply everywhere. Outside an authorised test plan, never:

- send any command to the TV — by Ex-Link (serial), network remote or any other route — or change its settings;
- open or change anything in the TV's service menu, including by sending remote-control key sequences;
- run anything that communicates with the Spyder5, including ArgyllCMS measurement commands such as `spotread`, `dispcal` or `dispread`;
- send commands to the Denon receiver, or search the home network for devices;
- display test patterns on the TV for measurement.

**Allowed without authorisation:** software-only work, including simulated meters and TVs, replaying recorded data, and tests that need no hardware.

**Physical tests** follow [docs/tests/README.md](docs/tests/README.md):

1. An agent may write a test plan and propose it in a pull request.
2. The owner authorises that specific plan explicitly — in the plan, in a pull-request comment or in conversation — giving the date and the steps covered. The authorisation is copied into the plan word for word before any step is carried out.
3. Only the authorised steps are carried out, with the owner present. Anything else needs new authorisation. The owner can stop at any time.
4. Results are recorded exactly as observed, including failures and surprises.

**Service menu:** changes made there can be hard or impossible to undo. A plan that uses it must say so at the top, explain why the normal menus are not enough, record the original values first, and explain how to restore them.

**Hardware-facing code**, once it exists, must default to simulation, must need a deliberate setting by the owner before it can reach real equipment, and must log every command it sends.

## 8. Money, services and irreversible actions (rule 7)

Ask the owner, and wait for explicit approval, before:

- **any purchase** — a proposal gives the item, price, supplier and the running total against the £25 limit, which is tracked in the ledger's budget section;
- **any paid API or paid service**;
- **any automation that runs by itself** — GitHub Actions (anything in `.github/workflows/`), scheduled jobs or bots;
- **any deployment or publishing** — releases, packages, websites, or making the repository public;
- **anything hard to undo** — force-pushing, rewriting history, deleting branches or files from history, changing repository settings, or changing equipment settings that cannot be restored.

Never recommend commercial calibration packages. Free and open-source tools may be discussed; note their licences.

## 9. Disagreements (rule 9)

- If you disagree with the other agent, an earlier report or a ledger entry, say so plainly. For tasks proposing file changes, record it in the ledger's Disagreements section: each position, who holds it, the evidence each relies on, and what test or source could settle it. For review-only tasks, report it in the review; the pull-request author records unresolved disagreements in the ledger (section 4).
- State the other side's position fairly, and never weaken it when editing the ledger.
- A disagreement stays open until evidence settles it or the owner decides. Do not force agreement.

## 10. Writing for the owner (rule 8)

- Use plain English. Explain a technical term the first time you use it, or point to the glossary in [docs/workflow.md](docs/workflow.md).
- Start every pull request with a short plain-English summary: what changed, why, and what the owner needs to do next, if anything.
- When you need a decision, ask one direct question, give the options and your recommendation, and say what happens under each option.
- Put "not tested", "unverified" and "needs your approval" where the owner will see them, not at the bottom.

## 11. Privacy and credentials

- Never commit passwords, tokens (including TV pairing tokens), API keys, IP or MAC addresses, Wi-Fi details, device serial numbers or other personal information.
- Keep private or machine-specific settings in the `local/` folder, or in files whose names contain `.local.` (for example `settings.local.toml`). Git ignores both. If the format needs documenting, commit an example file with made-up values.
- Log files (`*.log`) are ignored because they can contain private details. Copy only checked, relevant extracts into the repository.
- Do not commit vendor software, calibration data extracted from vendor software, or downloaded tools such as ArgyllCMS. Record where to obtain them instead.

## 12. Where things go

| Path | Contents |
|---|---|
| `README.md` | Project overview and goals |
| `AGENTS.md` | This file |
| `CLAUDE.md` | Imports this file for Claude Code — nothing else |
| `LEDGER.md` | Sources, claims, decisions, disagreements, tests, open questions and budget |
| `docs/workflow.md` | Plain-English guide for the owner |
| `docs/equipment.md` | The owner's equipment: what is known and what still needs confirming |
| `docs/briefs/` | The owner's instructions, archived word for word |
| `docs/research/` | Research material, archived with its provenance |
| `docs/tests/` | Plans, authorisations and results of tests on the owner's equipment |
| `.github/PULL_REQUEST_TEMPLATE.md` | Review checklist for every pull request |

Application code, its tests and its dependencies will come in later pull requests. The Python version and packaging (Q-003) and the licence (Q-002) are still open. Until they are decided: use only free and open-source dependencies, record each new dependency and its licence in the pull request, and make sure tests can run without hardware.
