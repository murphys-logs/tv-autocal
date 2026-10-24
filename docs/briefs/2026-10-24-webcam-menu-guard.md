# Webcam menu guard requirement (24 October 2026)

| Field | Value |
|---|---|
| Title | Owner's webcam menu-guard requirement, with answers to three follow-up questions |
| Produced by | The owner |
| Original date | 2026-10-24 |
| Imported | 2026-10-24, by Claude Code (Anthropic), in the pull request that records the requirement |
| How obtained | The owner's message to Claude Code, and the owner's choices among multiple-choice options that Claude Code offered |
| Fidelity | Verbatim. The requirement message, the questions, the option labels and the option descriptions are reproduced exactly; only the layout of the options is simplified |
| Ledger ID | S-009 |

This archive is the source of decision D-008 in [LEDGER.md](../../LEDGER.md). Do not edit it.

## Requirement message

```text
One thing that you must include as a part of the final program is that I will put a webcam observing the TV being profiled, no observation of the patch should be taken when any menu bar is visible in the lower portion of the screen at any point.
```

## What Claude Code said before asking

Before the questions, Claude Code restated the requirement and proposed three details: a fail-safe rule, keeping webcam pictures out of the repository, and treating the webcam like the TV and the meter. The owner did not answer those separately. They are recorded as Claude Code's proposals in D-009, not as the owner's decisions.

## Follow-up questions and the owner's answers

Claude Code wrote these questions and their options, including the "(Recommended)" labels. The owner chose one option for each.

### Question 1

```text
Shall I record this rule in the repository now, in a new pull request for Codex to review?

- Yes, new branch (Recommended): I'll use a fresh branch named claude/webcam-menu-guard. My old branch has already been merged, and your rules expect one branch per topic.
- Yes, reuse old branch: I'd first reset my old branch to match main. Your rules count that as a 'force-push', which needs your OK. Nothing would be lost, because everything on it is already in main.
- Not yet: I'll keep it in this conversation only for now. Codex won't see it until it's in the repository.
```

**Owner's answer:** "Yes, new branch (Recommended)"

### Question 2

```text
How should the program decide which part of the screen counts as the 'lower portion' that must be free of menu bars?

- Decide after a test (Recommended): Record 'lower portion' for now, and set the exact boundary once a webcam test shows where your TV's menu bars actually appear.
- Bottom third: Fix it now as the bottom third of the screen.
- Bottom half: Fix it now as the bottom half, for a wider safety margin.
- Whole screen: Strictest: a menu anywhere on screen blocks the reading.
```

**Owner's answer:** "Decide after a test (Recommended)"

### Question 3

```text
Do you already have the webcam you'll use?

- Yes, I have one: I'll record it as equipment you own. You can tell me the model later.
- No, I'll buy one: It would count towards the £25 hardware limit, which has £9.01 left, and you'd approve the purchase first.
- Not decided yet: I'll record it as an open question.
```

**Owner's answer:** "Yes, I have one"
