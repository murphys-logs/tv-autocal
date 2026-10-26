# Structure fixes (26 October 2026)

| Field | Value |
|---|---|
| Title | Owner's instructions to fix the repository-structure problems in section 1 of a review, with that section as received |
| Produced by | The owner, drafted with help from AI: Claude Code (Anthropic). The review's section 1 was written by AI: Claude Code (Anthropic) |
| Original date | 2026-10-26 |
| Imported | 2026-10-26, by Claude Code (Anthropic), in the pull request that carries out the fixes |
| How obtained | The owner's message to Claude Code that started this task |
| Fidelity | Verbatim — reproduced exactly as received, in the text block below, except that the trailing space at the end of five lines in the review is removed, because git's whitespace check rejects trailing spaces |
| Ledger ID | S-020 |

This archive is the source of decisions D-014 and D-015, of questions Q-017 and Q-018, and of the changes to Q-004 and Q-015 in [LEDGER.md](../../LEDGER.md). The owner did not write the review: its claims are AI hypotheses. Do not edit it.

```text
Fix the repository-structure problems (review section 1)
I'm the owner of murphys-logs/tv-autocal. A review of the repository's structure found four problems. Its section 1 is pasted at the end, exactly as I received it. Please carry out the fixes it proposes and follow AGENTS.md throughout. Where this message differs from AGENTS.md, follow this message, as AGENTS.md's opening paragraph says, and record each such difference in the ledger.

Where this message comes from. I drafted it with Claude Code's help on 26 October 2026. The review was written by: Claude Code. Claude Code gathered the facts under "Already checked". Treat them as AI-checked and check each one again before you rely on it. If anything in the review or in this message turns out to be wrong, say so in the pull request instead of bending the fix to fit.

Limits for this task
Documentation only. Do not touch the equipment or run ArgyllCMS. Do not change GitHub settings: no branch protection, visibility, apps or bots. Do not add workflows. Do not rewrite history, force-push, delete branches or merge. Do not ask for or carry out after-the-fact reviews.
Change the wording, not the meaning:
every claim keeps its provenance and equipment test status;
every decision keeps its meaning;
no disagreement position is weakened (AGENTS.md section 9);
no ID is renumbered, reused or dropped.
Text you take out of LEDGER.md moves to its new home word for word. The only exception is a copy of text that will keep one official home. You may delete such a copy, but list each one in the pull request.
Leave the archives in docs/briefs/ and docs/research/ untouched. The two exceptions are the new brief in step 0 and the Fidelity lines in step 4.
Do not bring back anything removed under D-013, including old file names. When you need to point to removed material, give the commit's SHA rather than the name of the file that held it.
The result must be shorter and simpler. Do not fix a wording problem by adding more rules.
Branch and pull request
Start a new branch from current main called claude/structure-fixes. If you are Codex, call it codex/structure-fixes. If your session assigns you a claude/ or codex/ branch, use that one instead.

Open one pull request, with one commit per step below so it can be reviewed commit by commit. Every step edits LEDGER.md, so separate pull requests would conflict with each other. For this task I am waiving AGENTS.md's one-topic-per-pull-request rule. The other company's agent reviews the pull request.

New IDs: S-020, D-014, D-015, Q-017 and Q-018. Before using each one, check that main does not use it yet.

Already checked (by Claude Code, 26 October 2026; check again)
Main is at fb24abd111d0869c9e81ed19e0691e5db5f827a2, and no pull requests are open. Pull request 12 (murphys-logs/tv-autocal) was closed without being merged. Pull request 14 was merged at 23:04 UTC on 25 October, after Claude Code re-reviewed its final head, 7af5457331d04f00ba0cf061ad8c4b9ae9e44521.

LEDGER.md has 348 lines and 12,324 words.

The four copies of the recovery wording no longer match:

docs/plan.md:77 ends "No automatic recovery is authorised here.";
docs/plan.md:91 ends "No automatic recovery action is authorised here.";
docs/tests/TEMPLATE.md:50 adds an extra sentence about X-007;
LEDGER.md:257 is a reworded version inside X-007.
Outside the archives, D-013 is restated at AGENTS.md:44, README.md:26 and :47, docs/plan.md:12, docs/workflow.md:53–54, docs/tests/README.md:13 and docs/tests/TEMPLATE.md:42, and in the ledger rows for T-008, T-013 and Q-008.

GitHub shows the murphys-logs account as the author of every pull request from 1 to 14. Claude Code's four reviews on pull request 14 were posted from the same account. Their state is "Commented", not "Approved".

Commit 337a58f1ac81e5359e9c9d762b06717b156313d0 is main's merge of pull request 10. It is the last commit on main before the merge of pull request 13 cut the archives under D-013. At that commit you will find:

the uncut S-002, S-005 and S-011 archives;
the uncut S-010 archive, under its earlier file name;
both files that D-013 deleted: the S-009 archive and the design proposal from pull request 5.
To see the cuts, run git diff -M 337a58f1 fb24abd -- docs/briefs docs/research.

The D-012 name removals were made before the files were first committed. In commit 8b2dd5e, the first committed versions of the S-002 and S-013 archives already contain "[owner's name removed]". So git history holds no uncut copy for either removal. Check this without searching for the name or printing it.

Steps
0. Archive this message
Archive this whole message, including the review, word for word as docs/briefs/2026-10-26-structure-fixes.md (S-020). Use the same header table as the other briefs. Provenance: Owner, drafted with help from AI: Claude Code. For the review, use the author filled in above. Add an S-020 row to the ledger. Unless I wrote the review, treat its claims as hypotheses.

1. Give each rule one home (review point 1.2)
Stop and recovery rules. The official text is docs/plan.md#stop-rules-for-every-physical-stage.
Replace the copies at docs/plan.md:77, docs/tests/TEMPLATE.md:50 and LEDGER.md:257 with a short link to it.
Do the same for every restatement of the no-resend rule: plan stages 3 to 5, the T-013 row, X-007 and the template.
Compare the copies before you remove them. Where one differs in meaning, keep the meaning of the official text and list the difference for the reviewer.
D-013. The decision and my words stay in the ledger's D-013 row. The working detail lives in docs/plan.md#measurement-cycle-and-use-of-readings. Everywhere else, use no more than "change, exit, wait, read (D-013)" with a link. README.md may keep its plain-English sentence for me.
Test template. I authorise each plan word for word, so a later edit to a linked rule must not quietly change a plan I have already authorised. In section 7, the template should record the full SHA of the version of plan.md whose stop rules the plan adopts.
Add one sentence to AGENTS.md: each rule has one home, and other files link to it instead of restating it.
2. Move review history out of the ledger and shorten its cells (review point 1.1)
Review log. Create docs/reviews/README.md. In two or three sentences, say that the folder is a log of reviews, not evidence about the equipment and not an archive of originals. Then create docs/reviews/2026-10-25-review-records.md. Add docs/reviews/ to AGENTS.md section 12 and to docs/README.md.

What moves. Move these into the log word for word, leaving one sentence and a link in the ledger:

the "Q-015 review records" section, with its introduction and closing paragraph;
X-007's "Reconciliation note" and "Recovery wording" bullets;
X-009's "Review outcome" bullet;
the opening paragraph of "Source checks and planning reconciliation";
review-history clauses inside cells, for example in S-005, S-018, C-061 and Q-016.
Pull request 12 has since closed and pull request 14 has merged. Record that in a dated note added to the log, and leave the moved rows as they were.

What stays. The ledger keeps everything that is not history: each disagreement's positions, stated fairly, what would settle it, its status and any outcome. Where the agents' agreement is all that is left, as in X-009, one clause may say so.

Cell length. Keep every ledger table cell to about two sentences, roughly 50 words. The longest now are D-013, T-013, C-061, Q-013 to Q-016, S-002, T-008 and several Notes cells in C-035 to C-054. Move the detail to the document that owns the topic:

test steps and prerequisites go to that test's stage in docs/plan.md;
my own words stay in their brief: link to it rather than quoting it again;
import details go to docs/research/README.md, including the "S-012 import notes";
review history goes to docs/reviews/.
Use a short " in detail" note under a table only when no other home exists. D-013 may keep its one-sentence quote of my words. The withdrawn entries are already short, so leave them alone.

Target. Aim to cut LEDGER.md's word count at least in half. Report the word count before and after, for LEDGER.md alone and for all non-archive Markdown files together, including docs/reviews/.

Record the new conventions. Add the cell limit and "review history goes in the pull-request description or docs/reviews/" to the ledger's "How to read the ledger" and to AGENTS.md section 4, one sentence each. Record the conventions from steps 1 to 3 as D-015 (Owner, S-020).

3. List my decisions and the review-gap questions (review points 1.1 and 1.3)
Q-015. Rewrite it as a direct question with options:

Should written cross-vendor reviews of the final versions of pull requests 2, 6, 7, 10 and 13 be obtained after the fact? The same question applies to commit a62772c.
Does an automatic Codex summary count as the review that rule 2 requires?
Pull request 9 was reviewed after it merged. Where the review and the ledger disagree on a fact, give both versions. For example, the ledger records that Claude Code reviewed pull request 2's final version under pull request 4, before it reached main.

New Q-018. Should I approve the automatic Codex review on GitHub, or switch it off? AGENTS.md section 8 says a bot that runs by itself needs my approval, and nobody knows who switched this one on. Do not touch the setting.

Q-004. Add the facts that matter for protecting main with a required review:

Every pull request, and every review the agents post, comes from my one GitHub account.
As far as Claude Code knows, GitHub does not let a pull request's author approve it. If so, the agents' reviews, posted as they are now, could never satisfy a "required approval" rule.
Find out which branch rules would still be available if the repository became private (Q-011), and whether they need a paid plan, which rule 7 would cover.
Check both points against GitHub's documentation and cite it with the date you accessed it, or write "unverified". Then give the options and a recommendation, labelled as AI.

README.md. Near the top, add a "What needs your decision" list that fits on one screen, about 15 lines at most.

Give each item one line: a link to its ID, the question in plain words, the options in a few words, the agents' recommendation if one is recorded (otherwise "no recommendation yet") and what it holds up.
The list points to the ledger rather than repeating it.
Include Q-004, Q-008, Q-011, Q-013, Q-014, Q-015, Q-016, Q-017, Q-018 and X-009, and the other questions waiting on me if they fit. Add one line for my owner checks, T-001 and T-002.
Pull-request template. Add one checkbox to .github/PULL_REQUEST_TEMPLATE.md: "If this PR opens, answers or changes an owner decision, the README decision list is updated."

4. Point each edited archive to its uncut original (review point 1.4)
I am instructing an edit to the archives. Record it as D-014 (Owner, S-020), as D-012 and D-013 were recorded. Add it to the list of exceptions in AGENTS.md section 6.

Cut under D-013 (S-002, S-005, S-010, S-011). Add one sentence to each Fidelity line: the uncut text is in commit 337a58f1ac81e5359e9c9d762b06717b156313d0, and it stays there only while git history is left intact (Q-017). For S-010, add "under its earlier file name; see git log --follow". Do not name that earlier file.

Cut under D-012 (S-002, S-013). The Fidelity line says the name was removed before the first commit, so this repository holds no uncut copy.

Deleted under D-013. The S-009 archive and the design proposal from pull request 5 have no file left to hold a Fidelity line. Add the same SHA to the S-009 ledger row and to D-013's detail, without naming the deleted files.

Change nothing else in any archive.

New Q-017, for me. The review's section 3.1, which is not included here, could lead someone to rewrite git history. Before anyone considers that, should a private copy of the uncut originals be kept outside this public repository? If so, where, and who keeps it? The options:

(a) I keep a private copy first;
(b) we accept losing them;
(c) history is never rewritten.
Note that S-019's first sentence and the D-012 name already exist only outside the repository. No agent makes the copy or rewrites history.

Checks before you open the pull request
Keep any scripts in a scratch folder and do not commit them. Report each result in the pull request.

Every relative link and heading anchor works, and every ledger ID mentioned exists.
The set of IDs is the same before and after, and every claim's provenance and equipment test status are unchanged.
Every sentence removed from LEDGER.md either appears in its new home or is listed as a deleted copy, together with its one official home.
git diff main -- docs/briefs docs/research shows only the new S-020 brief and the Fidelity sentences from step 4.
The withdrawn-scheme search listed under "Checks actually run" in pull request 14 (murphys-logs/tv-autocal) still finds only the lines it allows.
Before and after: how many cells are over the limit, and the word counts.
git diff --check reports nothing, and .github/workflows/ contains no files.
Pull request and report
Fill in every section of the pull-request template.

Start with a plain-English summary and the items that need my decision.
List the changes step by step, with a table showing where each moved piece of ledger text went.
Name the reviewer: Codex (OpenAI) if you are Claude Code, or Claude Code (Anthropic) if you are Codex.
Then tell me what you did and what you did not do, anything in the review you found to be wrong, what needs my decision, and whether the pull request is ready for review.

The review (section 1), as received:
 1. Problems with the overall structure
1.1 Governance text is drowning the project. There is no code yet, but there are about 2,500 lines of rules and records. Single ledger cells now run to 150+ words (T-013, C-061, Q-016), and the ledger holds review history (the Q-015 table, the X-007 “reconciliation note” and “recovery wording”). A non-programmer owner cannot realistically check that. Agents also spend each new PR reconciling the previous one’s wording rather than moving the project forward.

Fix: move review history out of LEDGER.md into PR descriptions or a docs/reviews/ log. Cap ledger cells at about 2 sentences and link to detail elsewhere. Add a one-screen “What needs your decision” list to the README. Today the owner has to dig out Q-008, Q-011, Q-013, Q-014, Q-015, Q-016 and X-009 for themselves.
1.2 The same rules are copied into many files, so they will drift apart.

The recovery paragraph (“After looking at the TV’s normal menu, the owner may restore…”) appears four times: docs/plan.md:77, docs/plan.md:91, docs/tests/TEMPLATE.md:50 and LEDGER.md:257.
D-013 is restated in about 8 places.
The next small wording change will make these copies inconsistent.
Fix: keep the official text in one place (plan.md#stop-rules-for-every-physical-stage) and link to it from everywhere else.
1.3 Rule 2 (independent review by the other vendor before merging) has not reliably been met, and the gap is recorded rather than closed.

PRs
#2,
#6,
#7,
#10 and
#13 were merged without a written cross-vendor review of their final version.
#9 was reviewed after it merged.
Commit a62772c (“Add files via upload”) put substantive research straight onto main.
The automatic Codex summaries are themselves a bot running by itself. Under AGENTS §8 that needs the owner’s approval, and nobody knows who switched it on (Q-015).
Risk: the vendor-independence guarantee is honoured on paper only.
Fix: the owner answers Q-015 and Q-004 (branch protection with a required review). Both are repository-settings decisions for the owner.
1.4 Removing personal data and keeping originals intact work against each other.

Under D-012 and D-013, archives labelled “Verbatim” have had text cut out. The uncut originals now exist only in git history.
The obvious fix for §3.1 below (rewriting history) would destroy those originals.
Fix: add to each edited archive's Fidelity line the full SHA of the last commit that holds the uncut text. Decide, as the owner, whether a private copy of the originals is kept outside this public repository before anyone considers rewriting history.
```
