# tv-autocal

A free, open-source Windows application, written in Python, intended to calibrate a Samsung TV's **own picture settings** automatically. It will show a test colour, measure it with a colour meter, adjust the TV, and measure again — until the picture is as close to the video standards as the TV allows.

> **Status, 25 October 2026: planning and research only.**
> There is no application code yet, and **nothing in this repository has been tested on the owner's equipment.**
> [LEDGER.md](LEDGER.md) records what is known, where each claim came from, and what still needs testing.

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
2. The meter measures what the TV actually displays, but never while the webcam shows a menu anywhere on the screen. The reading is then corrected for this TV's type of light.
3. The software compares the measurement with the target.
4. It works out which TV setting to change, and by how much, and sends that change to the TV.
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
| Screen monitor | The owner's webcam, watching the TV — model not yet recorded |

## Constraints

- **Free and open source**, for **Windows**, written in **Python**.
- **No commercial calibration packages** are to be recommended.
- **Extra hardware: £25 in total at most.** Spent so far: £15.99 on the selected Ex-Link cable; £9.01 remains. See the ledger's [budget record](LEDGER.md#7-hardware-budget).
- **Safety:** no AI agent may operate the TV, the meter or the TV's service menu by itself. Software-only simulations are allowed; every physical test needs the owner's explicit authorisation.
- **Webcam menu guard (required):** a menu anywhere on screen blocks or invalidates the whole reading (D-008, D-010). D-011 permits only the recorded meter/cap/cable hidden area to be ignored, after T-010 supports C-024 for that setup. This condition is **not yet tested**. See the [ledger](LEDGER.md#3-decisions) and [gate design](docs/webcam-measurement-gate.md).

## Intended design — not yet proven

| Part | Job | Status |
|---|---|---|
| Measurement (ArgyllCMS) | Takes readings from the Spyder5 | Not yet tried with this meter on this PC |
| Menu-bar guard (webcam) | Watches the TV, and blocks or discards any reading taken while a menu is visible anywhere on the screen | Required by the owner (D-008, D-010, conditioned by D-011); not built or tested |
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
