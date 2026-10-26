# How this project works — a plain-English guide

This guide is for the owner. It explains, without assuming any programming knowledge, how work is proposed, checked and accepted, and how tests on your equipment are approved.

## The short version

These steps apply to work that changes repository files. A review-only task finishes with findings; it does not require another pull request. The pull-request author records unresolved disagreements in [LEDGER.md](../LEDGER.md).

1. You ask Claude Code or Codex to do something.
2. The agent works on its own **branch** — a separate copy — never on `main`, the accepted version.
3. When it has finished, the agent opens a **pull request**: a proposal to add its changes to `main`. It fills in a checklist and tells you when the pull request is ready for review.
4. You ask the agent from the **other company** to review it.
5. You read the summary and the review, then decide: **merge** (accept), **ask for changes**, or **close** (reject).

Nothing reaches `main` without your decision. No agent operates your TV, meter or receiver without your written authorisation for a specific test.

## Words you will see

| Word | Meaning |
|---|---|
| Repository ("repo") | The project's folder on GitHub, including its full history |
| `main` | The accepted version of the project |
| Branch | A separate line of work. Claude Code's branches start with `claude/`, Codex's with `codex/` |
| Commit | A saved set of changes, with a note saying what changed |
| Pull request (PR) | A proposal to add a branch's changes to `main`. It shows exactly what would change, and it is where review and discussion happen |
| Review | A check of a pull request by the agent from the other company |
| Merge | Accepting a pull request, so its changes become part of `main`. Only you do this |
| Ledger | [LEDGER.md](../LEDGER.md): the record of sources, claims, decisions, disagreements and tests |
| Provenance | Where a claim came from — you, official documentation, a forum, an AI, and so on |
| Simulation | Software that imitates the TV or meter, so code can be checked without touching your equipment |

## Calibration words

Plain-English explanations written by Claude Code, reconciled with D-013 by Codex (OpenAI). They explain words; they are not evidence about your equipment. The ledger IDs point to what is still unknown.

| Word | Meaning |
|---|---|
| Calibration | Adjusting the TV's own settings so that what it shows matches the video standards as closely as it can |
| Colour meter (colorimeter) | A small sensor placed on the screen that measures how bright the light is and what colour it is. Yours is a Datacolor Spyder5 |
| ArgyllCMS | Free, open-source colour-measurement software. The plan is to use its `spotread` program to take readings from the Spyder5 (C-002, not yet tried) |
| Spectral correction (CCSS file) | A file describing the kind of light a type of screen gives out. A colour meter like the Spyder5 needs a suitable one to read a particular kind of screen accurately. What counts as validation and how to establish it remain Q-001; possible next steps if no practical validation route is found remain Q-016 |
| Patch, test pattern | A known colour or grey shown on the screen for the meter to measure |
| Rec.709, D65, BT.1886 | The three SDR targets: the standard red, green and blue; the standard white; and the standard brightness curve from black to white. See the [README](../README.md#goals) |
| cd/m² ("nits") | The unit of screen brightness. The brightness to aim for is still to be chosen (Q-014) |
| Black level | How dark the TV's black is. BT.1886's curve depends on it; whether the Spyder5 can measure it on this TV is not known (C-043) |
| White balance (2-point, multi-point) | TV controls that adjust red, green and blue so that greys look neutral: 2-point at one dark and one bright level, multi-point at 10 or 20 levels (X-003) |
| Colour management system (CMS) | TV controls that adjust where red, green, blue, cyan, magenta and yellow fall |
| Picture mode | A set of picture settings the TV keeps separately, such as Movie or Standard. Settings belong to a picture mode on a particular input |
| Ex-Link | Samsung's serial (RS-232) control socket, a 3.5 mm jack on some TVs. The project's only route for software to change TV settings (D-006); not yet tested on your TV |
| Acknowledgement | The short "received" reply a TV may send after an Ex-Link command. It does not prove that the setting changed (C-010) |
| Service menu | A hidden factory menu. Changes there can be hard or impossible to undo. No agent may open it, and the project avoids it |
| HDMI range (full or limited) | Two ways of numbering black to white in a video signal (0–255, or 16–235). The PC, receiver and TV must agree, or blacks and whites are crushed or washed out |
| Measurement cycle | [Change, exit, wait, read](plan.md#measurement-cycle-and-use-of-readings) (D-013) |
| Diagnostic and calibration readings | Readings have a recorded purpose and acceptance criteria. Diagnostic readings stay separate from accepted calibration data; see [plan.md](plan.md#measurement-cycle-and-use-of-readings) |
| Owner check | Something you look up yourself, without any agent operating the equipment. See [tests/README.md](tests/README.md#owner-checks) |
| ΔE2000 ("delta E") | A number for how different two colours look. Smaller is better; a value around 1 is often quoted as barely noticeable |

## Who reviews whom

| Pull request written by | Independent review by |
|---|---|
| Claude Code (Anthropic) | Codex (OpenAI) |
| Codex (OpenAI) | Claude Code (Anthropic) |

Agents from the same company do not count as independent of each other. ChatGPT and Codex together are one opinion from OpenAI; the Claude apps and Claude Code together are one opinion from Anthropic.

## Reviewing and merging a pull request, step by step

1. On GitHub, open the repository, click **Pull requests**, then click the pull request you want.
2. Read the **plain-English summary** at the top. The **Files changed** tab shows every change.
3. Ask the other company's agent to review it. You can paste this message, filling in the number:

   > Please review pull request #___ in the tv-autocal repository against AGENTS.md. Do not push changes to its branch. Post your review on the pull request, or give it to me to post. List anything you disagree with, so it can be recorded in LEDGER.md.

4. If the review asks for changes, pass it to the agent that wrote the pull request. If the two agents still disagree, the disagreement is recorded in the ledger. It does not have to be settled before you decide.
5. **Check that the review covers the latest version.** Every review names the full commit SHA it checked. If the author has pushed anything since, the new changes have not been reviewed yet; ask the reviewer to check them. Codex's automatic GitHub comment ("Codex Review Summary") is not the checklist review; whether it counts towards rule 2 is question Q-015.
6. When you are satisfied, click **Merge pull request**, then **Confirm merge**. If you are not, add a comment saying what you want changed, or click **Close pull request**.

How Codex will receive review requests — directly on GitHub, or through you — is still to be decided (question Q-005 in the ledger).

## Tests on your equipment

1. An agent writes a **test plan** in [docs/tests/](tests/README.md) and proposes it in a pull request. The plan lists every step, which equipment is involved, what could go wrong and how to undo it.
2. **Nothing happens until you authorise it in writing**, for example: *"Authorised by the owner on 2 November 2026, steps 1–5 only."*
3. Only the steps you authorised are carried out, with you present. You can stop at any time.
4. The results — including failures — are written up in the plan and summarised in the ledger.

Software-only simulations need no authorisation: they never touch your equipment.

## Spending and other approvals

An agent must ask you first, and wait for your answer, before any purchase, paid service, automatic GitHub Actions, publishing, or anything that would be hard to undo. Extra hardware is limited to £25 in total; the ledger keeps a running total.

## If something looks wrong

Ask either agent to explain it in plain English. Any statement that is not backed by a source or a test should be marked as such in the ledger; if it isn't, that is worth raising.
