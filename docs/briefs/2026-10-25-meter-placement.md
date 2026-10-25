# Meter placement and the screen area it hides (25 October 2026)

| Field | Value |
|---|---|
| Title | Owner's description of where the meter hangs during readings, with answers to two follow-up questions |
| Produced by | The owner |
| Original date | 2026-10-25 |
| Imported | 2026-10-25, by Claude Code (Anthropic), in the pull request that records the description and answers |
| How obtained | The owner's message to Claude Code, and the owner's choices among multiple-choice options that Claude Code offered |
| Fidelity | Verbatim. Claude Code's request, the owner's message, the questions, the option labels and the option descriptions are reproduced exactly, including spelling; only the layout of the options is simplified |
| Ledger ID | S-011 |

This archive is the source of claim C-023 and decision D-011 in [LEDGER.md](../../LEDGER.md). Do not edit it.

## Context

Claude Code reviewed the webcam measurement-gate design proposal (pull request #5). Its first finding was that the colour meter probably hides part of the screen from the webcam, and that the repository did not record where the meter sits during readings. Claude Code's report of that review to the owner ended with this request:

```text
One thing would help directly: telling us where you'll put the Spyder5 during readings (resting on the screen, or on a stand?), which is the open question behind finding 1.
```

## The owner's message

```text
The meter will be hanging by usb cable into the middle of the screen it is a circular shape approximately 5cm diameter and the covering cap is the same size which hangs beneath it.
```

## What Claude Code said before asking

```text
Thanks, that settles where the meter sits. It also confirms finding 1: the webcam can't see the screen behind the meter, behind its cap, or behind the cable running down from the top. On a 49-inch screen (about 108 × 61 cm) that's a small area, but it's right where the reading is taken. That makes it your decision rather than the programmers'.
```

## Follow-up questions and the owner's answers

Claude Code wrote these questions and their options, including the "(Recommended)" labels. The owner chose one option for each.

### Question 1

```text
The webcam can't see the screen behind the meter, its cap or its USB cable. How should the menu guard treat that hidden area?

- Accept if a test shows it's safe (Recommended): Ignore the hidden area only if the webcam test (T-010) shows that any TV menu that could cover it also appears somewhere the webcam can see. Until then, or if the test fails, no readings are accepted.
- Accept it now: Treat the hidden area as a known blind spot from the start. A menu or pop-up small enough to sit entirely behind the meter, its cap or the cable would go unnoticed.
- Decide later: Record it as an open question. Codex's design must leave it undecided, and no reading can be accepted until you choose.
```

**Owner's answer:** "Accept if a test shows it's safe (Recommended)"

### Question 2

```text
Shall I record where the meter hangs, and your answer above, in a new pull request for Codex to review?

- Yes, new pull request (Recommended): Your words archived exactly, plus the ledger entries, on my branch claude/fervent-einstein-jvw1ia. I'll tell Codex on PR #5 which ledger IDs I'm using, so the two pull requests don't clash again.
- Not yet: Keep it in this conversation for now. Codex can't see it until it's in the repository, so it can't use it to fix finding 1.
```

**Owner's answer:** "Yes, new pull request (Recommended)"
