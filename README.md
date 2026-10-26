# tv-autocal

A free, open-source Windows application, written in Python, intended to calibrate a Samsung TV's **own picture settings** automatically. It will show a test colour, measure it with a colour meter, adjust the TV, and measure again — until the picture is as close to the video standards as the TV allows.

> **Status, 25 October 2026: planning and research only.**
> There is no application code yet, and **nothing in this repository has been tested on the owner's equipment.**
> [LEDGER.md](LEDGER.md) records what is known, where each claim came from, and what still needs testing.

## What needs your decision

| ID | Question | Options | Agents' recommendation | Holds up |
|---|---|---|---|---|
| [T-001, T-002](docs/equipment.md#what-we-still-need-from-you) | Your owner checks: look up the TV, PC and receiver details | — | — | Stage 1 of the [plan](docs/plan.md), and later physical tests |
| [Q-004](LEDGER.md#6-open-questions) | Protect `main` so it changes only through pull requests? | Pull request only / also an approval / none | Claude Code: settle Q-011 first, then pull request only | Nothing yet |
| [Q-008](LEDGER.md#6-open-questions) | How long to wait after leaving the menu before reading? | A short delay, to be proposed | No recommendation yet | The delay in every test plan that takes readings |
| [Q-011](LEDGER.md#6-open-questions) | Make the repository private? | Private / stay public | No recommendation yet | Q-004's options |
| [Q-013](LEDGER.md#6-open-questions) | What if Ex-Link cannot change the TV's settings? | Guided manual adjustment / service-menu step / revisit D-006 | Claude Code: guided manual adjustment | Stage 2 of the plan |
| [Q-014](LEDGER.md#6-open-questions) | Input, picture mode, room, brightness, black level and pass marks for the first calibration? | Provisional now, final after T-003 | No recommendation yet | Component-test plans; T-008 |
| [Q-015](LEDGER.md#6-open-questions) | Get after-the-fact reviews of PRs #2, #6, #7, #10, #13 and commit a62772c? Does a Codex bot summary count as a review? | Yes / no, for each | No recommendation yet | Nothing yet |
| [Q-016](LEDGER.md#6-open-questions) | If no spectral correction can be validated, what then? | Keep T-008 blocked / seek a way to validate / unvalidated, with limits | No recommendation yet | T-008 |
| [Q-017](LEDGER.md#6-open-questions) | Keep a private copy of cut archive text before anyone rewrites git history? | You keep a copy / accept the loss / never rewrite history | No recommendation yet | Any rewrite of git history |
| [Q-018](LEDGER.md#6-open-questions) | Approve the automatic Codex review on GitHub, or switch it off? | Approve / switch off | No recommendation yet | Nothing yet |
| [X-009](LEDGER.md#4-disagreements) | May an owner check connect the cable to the PC? | Yes / no, look only | Both agents: look only | The cable item in your checklist |
| [Q-002](LEDGER.md#6-open-questions) | Which open-source licence? | Any open-source licence | No recommendation yet | Distributing the application |
| [Q-005](LEDGER.md#6-open-questions) | How does Codex receive review requests? | On GitHub / through you | No recommendation yet | The review steps in [docs/workflow.md](docs/workflow.md) |

## Goals

The first priority is accurate **SDR** (standard dynamic range) video:

| Target | What it means |
|---|---|
| **Rec.709** (ITU-R BT.709) | The exact red, green and blue that HD video is made for — and so every colour mixed from them |
| **D65** | The standard "daylight" white that whites and greys should match |
| **BT.1886** (ITU-R BT.1886) | How brightness should rise from black to full white for SDR video (the "gamma" curve) |

**HDR** (high dynamic range) investigation comes second.

**Closed-loop, TV-side calibration** means the software adjusts the TV's own controls (such as its colour and white-balance settings) and checks every change with the meter, instead of altering the picture on the PC:

1. The PC shows a known test colour on the TV.
2. The meter measures what the TV actually displays. The reading is then corrected for this TV's type of light.
3. The software compares the measurement with the target.
4. It works out which TV setting to change, and by how much, and sends that change to the TV. It then exits the TV's menu and waits a short moment, so the menu does not disturb the next reading (D-013).
5. Steps 1–4 repeat until the error is small enough or the TV can do no better.

## Equipment

As stated by the owner. Details still to be confirmed are listed in [docs/equipment.md](docs/equipment.md).

| Role | Equipment |
|---|---|
| TV to calibrate | Samsung UE49KS7000UXXU |
| Colour meter | Datacolor Spyder5 colorimeter |
| Computer | Windows PC |
| AV receiver | Denon AVC-X3800H |
| Selected Ex-Link cable | DSD TECH USB RS232 to 3.5mm Serial Cable with FTDI FT232RL Chip 6FT — purchase reported by the owner; compatibility not tested |

## Constraints

- **Free and open source**, for **Windows**, written in **Python**.
- **No commercial calibration packages** are to be recommended.
- **Extra hardware: £25 in total at most.** Spent so far: £15.99 on the selected Ex-Link cable; £9.01 remains. See the ledger's [budget record](LEDGER.md#7-hardware-budget).
- **Safety:** no AI agent may operate the TV, the meter or the TV's service menu by itself. Software-only simulations are allowed; every physical test needs the owner's explicit authorisation.
- **Measurement cycle (required):** [change, exit, wait, read](docs/plan.md#measurement-cycle-and-use-of-readings) (D-013).

## Intended design — not yet proven

| Part | Job | Status |
|---|---|---|
| Measurement (ArgyllCMS) | Takes readings from the Spyder5 | Not yet tried with this meter on this PC |
| Spectral correction | Corrects the meter's readings for this TV's type of light | No validated correction identified yet |
| Test-pattern generator | Shows exact, known colours on the TV | Not built; signal path not yet confirmed |
| Optimisation engine | Works out which setting to change, and by how much | Not built; can be developed in simulation first |
| TV-control backend | Changes TV settings using Samsung Ex-Link (serial) only, as selected by the owner in D-006 | **Selected cable and TV firmware compatibility not demonstrated** |

## How the project is run

Two AI coding agents from different companies share this repository: **Claude Code** (Anthropic) and **Codex** (OpenAI).

1. An agent works on its own branch (`claude/…` or `codex/…`), never directly on `main`.
2. It proposes its changes in a pull request and fills in the [review checklist](.github/PULL_REQUEST_TEMPLATE.md).
3. The agent from the *other* company reviews the pull request.
4. The owner decides whether to merge it.

Read more:

- [docs/workflow.md](docs/workflow.md) — the same process, step by step, for a non-programmer
- [docs/plan.md](docs/plan.md) — a proposed order of work, from the information you need to give to a first calibration (a proposal, not a decision)
- [docs/equipment.md](docs/equipment.md#what-we-still-need-from-you) — what we still need you to look up
- [AGENTS.md](AGENTS.md) — the rules both agents follow
- [LEDGER.md](LEDGER.md) — evidence, decisions, disagreements and outstanding tests

## What's where

| Path | Contents |
|---|---|
| `README.md` | This overview |
| `AGENTS.md` | Shared instructions for Claude Code and Codex |
| `CLAUDE.md` | One line that makes Claude Code read `AGENTS.md` |
| `LEDGER.md` | Evidence, decisions, disagreements and outstanding tests |
| `docs/` | Documentation and research archive — see [docs/README.md](docs/README.md) |
| `.github/PULL_REQUEST_TEMPLATE.md` | The checklist every pull request fills in |
| `.gitignore` | Files git must never store here, such as temporary files, passwords and private settings |

## Earlier work

The Claude feasibility report of 23 October 2026 is archived in [docs/research/](docs/research/2026-10-23-claude-feasibility-report.md) (S-002). It is AI research: its claims are recorded in the [ledger](LEDGER.md#claims-from-the-claude-feasibility-report-s-002) as hypotheses, **none has been tested on the owner's equipment**, and where it differs from the owner's later decisions (for example Ex-Link-only control, D-006) the decisions win.

The original [ChatGPT feasibility research](docs/research/2026-10-23-chatgpt-feasibility-research.md) is also archived (S-012). Its citation markers and claimed historical software-test result remain unverified; this is a separate document from the critique. Later source checks and reconciliations are recorded in the ledger.

A ChatGPT critique also exists outside this repository. Its original contents will be imported into [docs/research/](docs/research/README.md) once the owner supplies them. Until then, nothing here relies on it.

## Licence

Not chosen yet — see question Q-002 in [LEDGER.md](LEDGER.md#6-open-questions). The project is intended to be open source.
