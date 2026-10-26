# Review records, 25 October 2026

Moved from [LEDGER.md](../../LEDGER.md) on 26 October 2026 under D-015, word for word; only relative link paths are changed so that they work from this folder. Each section names the ledger entry it came from.

## Source checks and planning reconciliation — 25 October 2026

From the opening of the ledger's section of the same name, which now holds claims C-055 to C-061.

Codex reviewed main at `337a58f1`, all 22 tracked files, the ten existing pull requests and available reviews/comments, issues, branches and commit history. No application code, open pull request, standalone issue or equipment-test result was present. This is an OpenAI review, not independent review of OpenAI-authored material.

## Clauses moved from ledger cells

| Ledger entry | Moved text |
|---|---|
| S-005 | Merged by the owner in PR #3. Claude Code re-reviewed d8d01db on 2026-10-24 and recommended merge (S-018). The archived pending-review wording is historical. |
| S-018 | Merge recommendations after fixes; PR #9 explicitly records a post-merge review. |
| C-061 | Q-012 is left unused; Q-015 remains unanswered. |
| Q-012 | This reconciliation introduces no replacement question under this ID and does not renumber C-060, T-013 or Q-013 to Q-015. |
| Q-013 | first suggested in Claude Code's review of PR #4; carried from PR #12 and reconciled with D-013 |
| Q-015 | Review records were rechecked by Codex (OpenAI) on 2026-10-25, including PRs #11, #12 and #13. The records distinguish authored reviews, automatic summaries, the commits covered and review timing. The proposal that reviews name their full commit and cover the latest changes does not answer this question. |
| Q-016 | ChatGPT's Part 1 question was refined by Claude Code to include the separate validation option; Codex adopts that wording refinement. |

## X-007

- **Reconciliation note, 2026-10-25:** PR #12's unconditional test-template stop rule is scoped here to the proposed initial physical tests, as the [stop rules](../plan.md#stop-rules-for-every-physical-stage) now say. Claude Code [accepted this no-resend scope](https://github.com/murphys-logs/tv-autocal/pull/11#pullrequestreview-5645617198); that acceptance did not cover Codex's later recovery wording. The first transport follows the same initial restriction ([Stage 3](../plan.md#stage-3--software-only-checks-can-run-alongside-stages-1-and-2)). This does not settle the future transport policy or adopt the optional refinement about later absolute-setter retries; X-007 remains open.
- **Recovery wording, revised after [Claude's PR #14 review](https://github.com/murphys-logs/tv-autocal/pull/14#pullrequestreview-5645706578):** the recovery wording is now in the [stop rules](../plan.md#stop-rules-for-every-physical-stage). This is revised OpenAI proposal text, not text Claude accepted in the earlier PR #11 review.

## X-009

- **Review outcome, 2026-10-25:** Claude Code [agrees with Position B](https://github.com/murphys-logs/tv-autocal/pull/14#pullrequestreview-5645706578), including keeping mode changes out of a look-only check. No disagreement between the agents remains on this proposal; their agreement does not decide it for the owner.

## Q-015 review records checked on 25 October 2026

These are repository/GitHub observations, not a decision that any kind of review is sufficient. The check cannot establish reviews in unavailable conversations, deleted comments, or approval recorded elsewhere.

| PR or record | Evidence inspected | Timing and limits |
|---|---|---|
| #1 | [S-004](../briefs/2026-10-24-review-decisions.md) records the owner's decisions following a Codex review in conversation. | The full review is not archived; no GitHub review/comment was found. The review's time is not established by S-004. |
| #2 | [PR #2](https://github.com/murphys-logs/tv-autocal/pull/2) has no GitHub review/comment found. Its head `aecf3daa1d40c295552710a95fe120d268f72cda` was later carried unchanged by #4 and [reviewed by Claude Code](https://github.com/murphys-logs/tv-autocal/pull/4#pullrequestreview-5639980946). | Merged into the setup branch, not main, on 24 October at 20:39:10 UTC. The #4 review at 20:53:42 UTC preceded #4's merge into main at 20:54:59 UTC that day. |
| #3 | [Claude follow-up](https://github.com/murphys-logs/tv-autocal/pull/3#pullrequestreview-5640127443) at `d8d01db9b8317748881b10963216ddb425860789` recommends merge. | Before the 24 October merge. |
| #4 | [Claude review](https://github.com/murphys-logs/tv-autocal/pull/4#pullrequestreview-5639980946) at `aecf3daa1d40c295552710a95fe120d268f72cda` recommends merge. | Before the 24 October merge. |
| #5 | [Claude re-review](https://github.com/murphys-logs/tv-autocal/pull/5#pullrequestreview-5644547137) at `2348eee62fdcd502f4a7b2b0838a527ecf3132ac` recommends merge. | Before the 25 October merge; another re-review also appears after it. |
| #6 | [Automatic Codex summary](https://github.com/murphys-logs/tv-autocal/pull/6#issuecomment-6389677605) records completed checks and no findings at `33ea15abad8d7431955f8bad7e38ccf5684bac07`. | Merged; no separate authored review found on GitHub. |
| #7 | [Automatic Codex summary](https://github.com/murphys-logs/tv-autocal/pull/7#issuecomment-6390045683) has a completed code-review field but null commit/findings fields; its security field still displays running. | Merged; no separate authored review found. The summary does not establish a no-findings result or the code-review commit. |
| #8 | [Codex (OpenAI) review](https://github.com/murphys-logs/tv-autocal/pull/8#pullrequestreview-5644465363) at `1415a181592cc2507a58215ff8df992b8745731a` recommends merge. | Before the 25 October merge. |
| #9 | [Claude review](https://github.com/murphys-logs/tv-autocal/pull/9#pullrequestreview-5644638692) at `6c69626e28329095a425157cb32af4674d7e6b53` explicitly records a post-merge review. | Merge at 18:19:34 UTC; review at 18:24:34 UTC on 25 October. |
| #10 | [Automatic Codex summary](https://github.com/murphys-logs/tv-autocal/pull/10#issuecomment-6401231880) records completed checks and no findings at `b2ef4e3e8ab19e5ca0360097f0ba7d8672b9b866`. | Merged; no separate authored review found on GitHub. |
| #11 | [Claude final-head review](https://github.com/murphys-logs/tv-autocal/pull/11#pullrequestreview-5645534448) and [response to Part 1](https://github.com/murphys-logs/tv-autocal/pull/11#pullrequestreview-5645617198) at `5a96bee40a66fbc5cec793b57baf21d7d8d0b0ce` recommend merge. | Both precede the 25 October 22:16:45 UTC merge, `7eabd4f238058d3a7ff7d8fa29a68a9eb3a26c6f`. ChatGPT's Part 1 assessment is OpenAI, not an independent review of #11. |
| #12 | [Automatic Codex review](https://github.com/murphys-logs/tv-autocal/pull/12#pullrequestreview-5644826286) at `6d669fc07a6ba2d5ccde18d7b5be44f3d999983b` has the [Q-014 circular-prerequisite finding](https://github.com/murphys-logs/tv-autocal/pull/12#discussion_r4372062627). | Open/unmerged; finding remains unresolved on #12. No separate authored review found. This replacement corrects the ordering without resolving that thread. |
| #13 | [ChatGPT (OpenAI) review](https://github.com/murphys-logs/tv-autocal/pull/13#pullrequestreview-5645242159) recommends change first at earlier head `07cfeecacb6cee595589c1b06c53b12750bfac64`. The [automatic summary](https://github.com/murphys-logs/tv-autocal/pull/13#issuecomment-6402726734) reports completed checks and no findings at final head `fb9e596057b38423b439fff57c20bdabf863e6bf`; the [author response](https://github.com/murphys-logs/tv-autocal/pull/13#issuecomment-6403508636) requests another review. | Merged at 21:37:19 UTC on 25 October as `8910378d3b6e751c27be17104eb696f6ebeb848d`; no authored re-review of the final head was found. |
| S-012 upload | [Upload commit](https://github.com/murphys-logs/tv-autocal/commit/a62772c3212351ea08caa3e659573448b1825138) added the research file to main's first-parent history. | 25 October 18:04:23 UTC, before #9 merged. This records the path into main, not an equipment result or review-adequacy decision. |

The [Part 1 assessment](https://github.com/murphys-logs/tv-autocal/pull/11#issuecomment-6404046450) recorded no substantive disagreement with Claude Code. Claude's later response proposed the three-option wording now used in Q-016 and accepted scoping the early-test stop rule; Codex accepts both, so that wording difference is resolved for this proposal. In [review of PR #14 at `5f82ac1a9341b7ba96ba907ef0f1d4a97c8f7280`](https://github.com/murphys-logs/tv-autocal/pull/14#pullrequestreview-5645706578), Claude requested removing T-004 from T-013's prerequisites and preserving the owner's manual restoration, with a correction to X-007's attribution. Codex accepts those findings and has revised the proposal accordingly; these revisions need independent re-review. X-009 records the agents' agreement on a checklist boundary awaiting the owner's decision.

## Q-015: the review and the records compared

Added 26 October 2026 by Claude Code, for Q-015. S-020's review (AI: Claude Code) and the records above agree on PRs #6, #7, #9, #10 and #13. They differ, or the records add a fact, on two points:

- **PR #2.** The review: merged without a written cross-vendor review of its final version. The records: #2 merged into the setup branch, not main, without a review; Claude Code reviewed the same head, `aecf3daa1d40c295552710a95fe120d268f72cda`, under #4 before #4 merged into main.
- **Commit a62772c.** The review: it put substantive research straight onto main. The records agree, and show it landed before #9 merged. Checked on 26 October 2026: the file it added is identical (git blob `f873fd6cbb3760c32200efb40636775d3b332cf6`) to the version on PR #9's branch, which Claude Code reviewed after #9 merged.

## Note added 26 October 2026

Since these records were made, PR #12 was closed without being merged, at 23:08 UTC on 25 October 2026, and PR #14 was merged, at 23:04 UTC on 25 October 2026 as `fb24abd111d0869c9e81ed19e0691e5db5f827a2`, after Claude Code's re-review of its final head `7af5457331d04f00ba0cf061ad8c4b9ae9e44521`. The rows above are left as they were recorded.
