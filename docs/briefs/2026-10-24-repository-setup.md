# Repository setup brief (24 October 2026)

| Field | Value |
|---|---|
| Title | Repository setup brief |
| Produced by | The owner |
| Original date | 2026-10-24 |
| Imported | 2026-10-24, by Claude Code (Anthropic), in the setup pull request |
| How obtained | The owner's message to Claude Code that started the setup task |
| Fidelity | Verbatim — reproduced exactly as received, in the text block below |
| Ledger ID | S-001 |

This is the owner's original instruction that started the repository setup, copied word for word. It is the source of the working rules quoted in [AGENTS.md](../../AGENTS.md) and of every ledger entry marked S-001. Do not edit it.

```text
I want you to initialise my new private GitHub repository, `tv-autocal`, as the permanent shared workspace for a collaborative project involving Anthropic Claude Code and OpenAI Codex.
Project objective
Build a free, open-source Windows Python application capable of closed-loop, TV-side colour calibration of my Samsung UE49KS7000UXXU using my existing Datacolor Spyder5 colorimeter, Windows PC and Denon AVC-X3800H receiver.
Prioritise SDR Rec.709, D65 and BT.1886. HDR investigation is secondary. Additional hardware expenditure must not exceed £25 in total. Do not recommend commercial calibration packages.
The intended architecture involves ArgyllCMS for measurements, validated spectral corrections, a controlled test-pattern generator, a numerical optimisation engine and a TV-control backend using Samsung Ex-Link or network remote commands. The precise compatibility of these interfaces with my firmware has not yet been demonstrated.
Your first task is repository setup only.
Create or update:

* `README.md` — project overview and goals
* `AGENTS.md` — shared instructions for Claude Code and Codex
* `CLAUDE.md` — containing the single import `@AGENTS.md`
* `LEDGER.md` — evidence, disagreements, decisions and outstanding tests
* `docs/` — documentation and research archive structure
* `.gitignore` — appropriate Python, temporary-file and credential exclusions
* `.github/PULL_REQUEST_TEMPLATE.md` — review checklist

Working rules

1. Work on a `claude/` feature branch, never directly on `main`.
2. All substantive changes require a pull request and independent review by the other vendor before I decide whether to merge.
3. Keep source provenance separate from whether a claim has been tested on my equipment.
4. Do not treat two OpenAI agents as two independent reviewers.
5. Do not invent experimental findings or citations.
6. Never operate the TV, meter or service menu autonomously. Software-only simulations are permitted. Physical tests require my explicit authorisation.
7. No purchases, paid APIs, automatic GitHub Actions, deployment or irreversible changes without my approval.
8. Make the workflow understandable to a non-programmer.
9. Record unresolved disagreements rather than forcing agreement.

There is an extensive Claude feasibility report dated 23 October 2026, as well as a ChatGPT critique. Do not pretend to have access to these earlier conversations. We will import their original contents after the repository setup is reviewed.
Create the initial files, check their consistency, push a feature branch and prepare the first pull request against `main`.
Do not merge it. Explain plainly when the pull request is ready for independent review.
```
