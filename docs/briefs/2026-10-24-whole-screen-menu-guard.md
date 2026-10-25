# Whole-screen menu guard and repository visibility (24 October 2026)

| Field | Value |
|---|---|
| Title | Owner's answers to three questions from Claude Code's design review, and approval to record them |
| Produced by | The owner |
| Original date | 2026-10-24 |
| Imported | 2026-10-24, by Claude Code (Anthropic), in the pull request that records the answers |
| How obtained | The owner's message to Claude Code, and the owner's choice among multiple-choice options that Claude Code offered |
| Fidelity | Verbatim. Claude Code's questions and the owner's answers are reproduced exactly, including spelling; Markdown emphasis in the questions is removed and the layout of the options is simplified |
| Ledger ID | S-010 |

This archive is the source of decision D-010 and questions Q-010 and Q-011 in [LEDGER.md](../../LEDGER.md). Do not edit it.

## Context

Claude Code reviewed the Ex-Link research, the webcam measurement-gate design proposal (pull request #5) and the ledger. It ended its review with three questions for the owner.

## Claude Code's questions

```text
1. Will you check the TV for an Ex-Link socket (T-001) now? I recommend yes, because it's a look-only check.
2. Should a menu or pop-up anywhere over the meter also block readings, or only bars in the lower part as now?
3. Did you make the repository public on purpose?
```

## The owner's answers

```text
1. I'll check for the ex-link socket tomorrow
2. If a menu pops up anywhere, the reading from the Spyder shuld be ignored until the menu has gone. It will ruin the reading.
3. No, I don;t know what happend there
```

## Follow-up question and the owner's answer

Claude Code wrote this question and its options, including the "(Recommended)" label. The owner chose one option.

```text
Shall I record your new 'menu anywhere on screen' rule, and fix the out-of-date ledger entries, in a new pull request for Codex to review?

- Yes, both (Recommended): One pull request on my branch: your words archived exactly, a new decision widening the webcam rule to the whole screen, and the stale ledger items fixed (D-005, D-009, S-005, T-008, the time-zone note, and that the repository was made public without a recorded decision). Codex then reviews it.
- Only the new rule: Record just your whole-screen rule now; leave the ledger fixes for later.
- Not yet: Keep it in this conversation for now. Codex won't see it until it's in the repository.
```

**Owner's answer:** "Yes, both (Recommended)"
