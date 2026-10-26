# AGENTS.md — shared instructions for Claude Code, Codex, and Antigravity

These are the working instructions for **every AI agent** on this project. Codex and Antigravity read this file directly. Claude Code reads it through `CLAUDE.md` (`@AGENTS.md`). All shared rules live here; vendor-specific files must only point here.

If an instruction given by the owner in conversation conflicts with this file, follow the owner and propose an update to this file in a pull request. If two parts of this file conflict, stop and ask the owner.

---

## 1. Who is who

| Who | Role | Branch Prefix |
|---|---|---|
| **Owner** | The person who owns this repository and equipment. Only the owner authorises physical tests, approves budget/actions, and merges pull requests. | `main` (merges only) |
| **Claude Code** (Anthropic) | AI coding agent. Proposes changes via PR and reviews Codex/Antigravity PRs. | `claude/<topic>` |
| **Codex** (OpenAI) | AI coding agent. Proposes changes via PR and reviews Claude/Antigravity PRs. | `codex/<topic>` |
| **Antigravity** (Google) | AI coding agent. Proposes changes via PR and reviews Claude/Codex PRs. | `antigravity/<topic>` |

### Multi-Agent Review Protocol (Cross-Vendor Independence)
* **Substantive changes require independent review:** Any change touching code, claims, evidence, decisions, tests, instructions, safety rules, or scope is substantive.
* **Vendor independence:** Independent review must be performed by an agent from a **different AI vendor** (Anthropic, OpenAI, or Google). Two agents from the same vendor count as one reviewer.
* **Reviewers comment; they do not push commits:** Propose modifications in PR comments or separate PRs to keep attribution clear.
* **Only the owner merges:** No agent merges PRs, force-pushes, rewrites history, or deletes branches unless explicitly directed by the owner.

---

## 2. The owner's working rules

Quoted exactly from the owner's setup brief (24 October 2026, [docs/briefs/2026-10-24-repository-setup.md](docs/briefs/2026-10-24-repository-setup.md)):

> 1. Work on a feature branch (`claude/`, `codex/`, or `antigravity/`), never directly on `main`.
> 2. All substantive changes require a pull request and independent review by another vendor before I decide whether to merge.
> 3. Keep source provenance separate from whether a claim has been tested on my equipment.
> 4. Do not treat two agents from the same vendor as two independent reviewers.
> 5. Do not invent experimental findings or citations.
> 6. Never operate the TV, meter or service menu autonomously. Software-only simulations are permitted. Physical tests require my explicit authorisation.
> 7. No purchases, paid APIs, automatic GitHub Actions, deployment or irreversible changes without my approval.
> 8. Make the workflow understandable to a non-programmer.
> 9. Record unresolved disagreements rather than forcing agreement.

---

## 3. Project scope & architecture constraints

* **Objective:** Free, open-source Windows Python application for closed-loop, TV-side SDR color calibration.
* **Target Display:** Samsung UE49KS7000UXXU (2016 Quantum Dot SUHD).
* **Target Standards:** SDR Rec.709 gamut, D65 white point ($x=0.3127, y=0.3290$), and BT.1886 gamma curve. HDR investigation is secondary.
* **Control Channel (D-006):** **Samsung Ex-Link serial only** (RS-232 via 3.5 mm jack). Network remote control (WebSocket) and infrared control are out of scope.
* **Measurement Channel:** Datacolor Spyder5 colorimeter driven via ArgyllCMS `spotread -O` subprocess using an appropriate CCSS spectral correction file.
* **Measurement Cycle (D-013):** `[Change Setting -> Exit TV Menu -> Settle Delay -> Take Reading]`. Focuses exclusively on the colorimeter probe; no auxiliary monitoring hardware is required.
* **Service Menu Prohibited:** No agent may access, command, or script interactions with the TV's service/factory menu.
* **Budget Limit:** Additional hardware strictly capped at £25.00 total. (£15.99 spent on FTDI Ex-Link cable; £9.01 remaining).

---

## 4. Starting and finishing a task

### Before starting
1. Read `AGENTS.md`, [LEDGER.md](LEDGER.md), and relevant documents.
2. Check `main`, open pull requests, and active branches to avoid conflicting work.
3. Work strictly from the repository, owner instructions, and verified sources. Do not invent citations or assume access to unlinked external chats.

### Before finishing (PR checklist)
1. Update [LEDGER.md](LEDGER.md) with any new/changed claims, decisions, disagreements, tests, or questions. Keep cells dense (~50 words) and link to topic docs.
2. Verify all internal file and markdown links.
3. Open a pull request using [.github/PULL_REQUEST_TEMPLATE.md](.github/PULL_REQUEST_TEMPLATE.md).
4. Provide a plain-English summary: what changed, what remains untested, what decisions the owner must make, and specify which cross-vendor agent is requested for review.

---

## 5. Evidence, provenance & safety rules

* **Two mandatory labels per claim:**
  * **Provenance:** `Owner`, `Primary` (manuals, standards), `Secondary` (community docs), `AI: <vendor>` (hypothesis), or `None yet`.
  * **Equipment Test Status:** `Not tested`, `Planned`, `Authorised`, `Confirmed`, `Contradicted`, `Inconclusive`, or `N/A`.
* **Zero Autonomous Hardware Actions (Rule 6):**
  * Outside an authorised, written test plan with the owner present, never send Ex-Link commands, invoke ArgyllCMS hardware commands (`spotread`, `dispcal`), adjust AVR settings, or display measurement patterns.
  * Hardware-facing code must default to simulation mode and require an explicit setting to reach physical interfaces.
* **Approvals Required (Rule 7):**
  * Purchases, paid services, automatic CI workflows, public deployment, git history rewrites, and irreversible TV adjustments require prior explicit owner approval.
* **Privacy:** Never commit credentials, serial numbers, IP/MAC addresses, or private photos. Store machine-specific configurations in `local/` or `*.local.*` (git-ignored).
