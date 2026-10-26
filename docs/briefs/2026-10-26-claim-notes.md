# Claim notes (26 October 2026)

| Field | Value |
|---|---|
| Title | Owner's instructions to move long analytical claim notes out of LEDGER.md, word for word |
| Produced by | Owner |
| Original date | 2026-10-26 |
| Imported | 2026-10-26, by Codex (OpenAI), in the pull request that carries out the move |
| How obtained | The owner's message to Codex that started this task |
| Fidelity | Verbatim — the complete message below preserves the text as received, including its Markdown escapes and line-break markers |
| Ledger ID | S-021 |

This archive is the source of decision D-016 in [LEDGER.md](../../LEDGER.md). Do not edit it.

```text
Task: move long analytical claim notes out of LEDGER.md, word for word (option (c) from PR #15)\
\
Repository: murphys-logs/tv-autocal. Follow AGENTS.md throughout. Where this message differs from AGENTS.md, follow this message and record each difference in the ledger.\
\
Before you start\
\- Confirm that pull request #15 has been merged into main. If it has not, stop and tell me.\
\- Start a new branch from current main called codex/claim-notes. If your session assigns you a codex/ branch, use that one instead.\
\- Check that main does not yet use the new IDs S-021 and D-016.\
\
What to do\
1\. Archive this message word for word as docs/briefs/2026-10-26-claim-notes.md (S-021), with the same header table as the other briefs, and add an S-021 row to the ledger.\
2\. Create docs/claim-notes.md. Open it with one or two sentences saying that it holds the analysis behind the claims in LEDGER.md, moved there word for word; that the ledger remains the record of each claim's provenance and equipment test status; and that this file adds no claims. Then give each moved claim its own heading, named by its ID (for example "## C-035"), so it has a stable link.\
3\. Move Notes text out of the claims tables (C-001 to C-061):\
&#x20;  \- Only the Notes column. Do not change the Claim, Provenance, Equipment test status or Tests cells, or any other table.\
&#x20;  \- Move a Notes cell's text when the cell is longer than 20 words. Move it word for word, in its original order, under that claim's heading. Shorter Notes cells stay as they are.\
&#x20;  \- In the ledger, the cell keeps, word for word, any sentence marking the claim as superseded, and gains a link to the claim's heading, for example "[Notes]\(docs/claim-notes.md#c-035)". Nothing else is reworded.\
&#x20;  \- Leave the withdrawn entries (C-015 to C-019 and C-024) alone.\
&#x20;  \- Adjust relative link paths inside moved text so they still work from docs/. Change nothing else in the moved text.\
4\. Record the decision as D-016 (Owner, S-021): analytical notes on claims live in docs/claim-notes.md, and the ledger's Notes cells link to them. Add docs/claim-notes.md to AGENTS.md section 12 and to docs/README.md, and add one sentence to "How to read the ledger" saying where claim notes are. Add no other rules.\
\
Limits\
\- Documentation only. Do not touch the equipment or run ArgyllCMS. Do not change GitHub settings, add workflows, rewrite history, force-push, delete branches or merge.\
\- Change where text lives, not its wording or meaning. No claim, decision, disagreement, test or question changes meaning. No ID is renumbered, reused or dropped.\
\- Leave the archives in docs/briefs/ and docs/research/ untouched, apart from adding the new S-021 brief.\
\- Do not bring back anything removed under D-013. Refer to the withdrawn-scheme search as "the PR 14 search"; do not list its terms.\
\
Checks before you open the pull request\
Keep any scripts out of the repository, and report each result in the pull request.\
\- Every sentence removed from LEDGER.md appears word for word in docs/claim-notes.md, link paths aside. List any exception.\
\- The set of IDs is the same before and after, apart from S-021 and D-016. Every claim's Claim, Provenance, Equipment test status and Tests cells are identical to main.\
\- Every relative link and heading anchor works, including links from other files into LEDGER.md.\
\- git diff main -- docs/briefs docs/research shows only the new S-021 brief.\
\- The PR 14 search still finds only the lines it allows.\
\- Before and after: the word count of LEDGER.md, the word count of all non-archive Markdown, and how many ledger cells are over 50 and over 60 words.\
\- git diff --check reports nothing, and .github/workflows/ contains no files.\
\
Pull request\
\- Open one pull request and fill in every section of .github/PULL_REQUEST_TEMPLATE.md, starting with a plain-English summary.\
\- Include a table showing, for each claim, how many words moved and how many stay in the ledger cell.\
\- Name the reviewer: Claude Code (Anthropic).\
\- Tell me what you did, what you did not do, and whether the pull request is ready for review.
```
