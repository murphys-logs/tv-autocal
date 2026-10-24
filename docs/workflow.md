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
5. When you are satisfied, click **Merge pull request**, then **Confirm merge**. If you are not, add a comment saying what you want changed, or click **Close pull request**.

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
