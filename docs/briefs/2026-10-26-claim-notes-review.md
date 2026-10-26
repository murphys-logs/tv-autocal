# Claim notes review (26 October 2026)

| Field | Value |
|---|---|
| Title | Owner's instructions to act on Claude Code's review of PR #16 (claim notes, S-021) |
| Produced by | Owner, drafted with help from AI: Claude Code (Anthropic) |
| Original date | 2026-10-26 |
| Imported | 2026-10-26, by Codex (OpenAI), in the pull request that carries out the review changes |
| How obtained | The owner's message supplied to Codex in Pasted text.txt for this task |
| Fidelity | Verbatim — the complete supplied message is preserved in the text block below, with CRLF line endings normalised to LF and a final newline before the closing fence |
| Ledger ID | S-022 |

This archive is the source of the review changes to claim notes and the clarification of decision D-016 in [LEDGER.md](../../LEDGER.md). Do not edit it.

```text
Task: act on Claude Code's review of PR #16 (claim notes, S-021)

Repository: murphys-logs/tv-autocal. Follow AGENTS.md throughout. Where this message differs from AGENTS.md, follow this message and record each difference in the ledger. I drafted this message with help from Claude Code (Anthropic), the reviewer.

Before you start
- Confirm that PR #16 is still open, that its head is a93961ff99f90d692f0ab1a7c60ae0e900ec47ae and that main is still c7fdd1eac1e0136b1d18e02afcc6f084d4146c4c. If any of these has changed, stop and tell me.
- Read Claude Code's review and its four inline comments: https://github.com/murphys-logs/tv-autocal/pull/16#pullrequestreview-5651797994
- Check that S-022 and X-010 are unused on main and on this branch.
- Work on codex/claim-notes and add new commits. Do not force-push or rebase.

My decisions
I want all four findings implemented as set out below. On finding 4 I choose option (b). For S-021's 20-word cutoff, a word is a whitespace-separated token containing at least one letter or digit. A dash or other punctuation standing alone is not a word.

What to do
1. Rule on each finding before changing anything. Check its facts against the repository and S-021, then give a verdict: agree, agree with changes, or disagree, with reasons.
   - If a finding's facts don't hold (for example a count or line reference is wrong), don't implement that finding. Stop and tell me.
   - If the facts hold but you disagree with the judgement, implement it anyway as my decision. Record your position as X-010 in the ledger's Disagreements section, stating both sides fairly.
2. Archive this message word for word as docs/briefs/2026-10-26-claim-notes-review.md (S-022). Use the same header table as the other briefs, with Produced by "Owner, drafted with help from AI: Claude Code (Anthropic)". After the table, add a framing line, as the other briefs have, saying what the archive is the source of and ending "Do not edit it." Add an S-022 row to the ledger.
3. Finding 1: in docs/briefs/2026-10-26-claim-notes.md, after the header table and before the text block, add this line: "This archive is the source of decision D-016 in [LEDGER.md](../../LEDGER.md). Do not edit it." Change nothing else in that file. The brief isn't merged yet, so AGENTS.md section 6 doesn't stop this.
4. Finding 2: in docs/claim-notes.md, replace the first sentence of the opening with: "This file holds the analysis behind the claims in [LEDGER.md](../LEDGER.md), moved here word for word; only relative link paths are changed so that they work from this folder." Leave the second sentence as it is.
5. Finding 3: replace the new sentence in "How to read the ledger" (LEDGER.md line 39) with: "**Claim notes** longer than 20 words are in [docs/claim-notes.md](docs/claim-notes.md), linked from the claim's Notes cell; withdrawn claims keep theirs here." This replaces the review's suggested wording, which overlooked the six withdrawn entries.
6. Finding 4: apply my definition of a word to all 61 claims. I expect C-006 to be the only claim affected. If any other claim changes, apply the definition anyway and list it. For C-006, restore its Notes cell exactly as it is on main, and remove its section from docs/claim-notes.md.
7. D-016 isn't merged either, so update it: Decided by "Owner (S-021, S-022)", and add my word definition to its Status cell. Keep the cell to about 50 words; you may tighten D-016's own new wording but not change its meaning. Add no other rules.

Limits
- Archives: leave docs/briefs/ and docs/research/ untouched, apart from the new S-022 brief and the one line in step 3.
- Documentation only: don't touch the equipment or run ArgyllCMS. Don't change GitHub settings, add workflows, rewrite history, force-push, delete branches or merge.
- IDs: none renumbered, reused or dropped. The only new IDs are S-022 and, if needed, X-010.
- PR 14 search: refer to it by that name only. Don't list its terms or bring back anything removed under D-013.
- Wording: change only what steps 2 to 7 require. Moved text stays word for word, and no claim, decision, disagreement, test or question changes meaning.

Checks before you push
Keep any scripts out of the repository, and report each result in the pull request.
- All of S-021's checks, rerun against main. Use my word definition for every count, including main's baseline, and say so.
- C-006's row is byte-identical to main, and docs/claim-notes.md has 26 sections, none for C-006.
- Each of the four changes appears exactly as specified, or as your ruling changed it, with the reason.
- The S-021 brief differs from a93961f only by the added line, and its text block is unchanged.
- The S-022 archive matches this message.

Pull request
- Update PR #16's description; don't open a new pull request.
- Recompute the per-claim table and the before-and-after figures.
- Add a rulings table: finding, verdict, what changed, file and line.
- Reset the reviewer section to pending.
- Reply to each of Claude Code's four inline comments with your ruling.
- Name the reviewer for a re-review of the new head: Claude Code (Anthropic).
- Tell me what you did, what you didn't do, the new head SHA, and whether the pull request is ready for re-review.
```
