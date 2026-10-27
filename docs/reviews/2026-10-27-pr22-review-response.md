# PR #22 — assessment of independent reviews

Assessed and revised by Codex (OpenAI), 27 October 2026, at the owner's request. This record describes software review and corrections only. No hardware, device/display enumeration, ArgyllCMS execution, serial access or image presentation was used.

Both reviews assessed `968bc2e4bf8a1140c5e92e8cd85bffbf14ac901e` against base `f333df41805f5c1d6e195b6635abc6d853b62a25`:

- [Antigravity (Google)](https://github.com/murphys-logs/tv-autocal/pull/22#pullrequestreview-5672956594): ready to merge, no required fixes.
- [Claude Code (Anthropic)](https://github.com/murphys-logs/tv-autocal/pull/22#pullrequestreview-5672983240): change first for two medium findings; one low finding and four optional suggestions.

Codex accepts both mandatory findings after checking the implementation. Antigravity's earlier favourable assessment is preserved here; it does not rebut Claude's concrete counterexample. No finding is left disputed by the author. The fixes change code and tests, so the revised head needs independent re-review under [AGENTS.md section 5](../../AGENTS.md#5-branches-pull-requests-and-review-rules-1-2-and-4). The automatic Codex bot and internal Codex assistance are the author's vendor and do not count as independent review.

## Findings and disposition

| Finding | Assessment and change |
|---|---|
| Claude M-1: attempt budget prevents restoration | **Accepted and fixed.** Previously, a three-attempt baseline/change/repeat sequence consumed the restoration slot. Admission now reserves that slot before the first change and preserves it for later changes/repeats while restoration is required. Refusal raises before mutation and leaves READY so the caller can explicitly restore. The total budget is unchanged; no retry or recovery after a terminal stop is introduced. Regressions cover the original sequence and smaller budgets. |
| Claude M-2: hidden simulator state presented too broadly | **Accepted and fixed.** The original setting now comes from the baseline menu observation, after a labelled simulator consistency check. Remaining direct fake-state checks in baseline, repeat, polling and stopping are explicitly documented as simulator invariants unavailable to a real controller. C-093 states that boundary. Tests check observation/capture order, missing and inconsistent observations, and labelled simulator interference. No hardware readback capability is inferred. |
| Claude L-1: wrong phase on budget stop | **Accepted and fixed.** A terminal attempt-limit event identifies the refused phase, rather than the previous completed phase. Reserved-slot refusals leave the existing event history unchanged because no attempt begins. Regression coverage distinguishes these cases. |
| Claude O-1: immediate restore issues an unchanged setter | **Accepted as documentation clarification.** Existing behaviour is retained: restore after baseline still issues an original-value setter and runs the full observation/exit/wait/read cycle. The conservative obligation clears only after success. The software record states this explicitly; it is not approval to send redundant hardware commands. |
| Claude O-2: no patch-only transition | **Accepted as scope clarification.** The controller models setting-change cycles, not a T-003/T-005 patch playlist. Requesting the same level with another patch still issues a simulated setter. No additional API or physical presenter is introduced. |
| Claude O-3: missing budget, phase and repeat-after-change coverage | **Accepted.** Added regressions exercise reservation and restoration, refused-phase reporting, and repetition of the changed target/patch without another setter, including its fresh wait. |
| Claude O-4: record the owner's patch acceptance | **Accepted.** S-040 archives the supplied owner messages; D-018 records the approved centred 960×540 rectangle on a 3840×2160 frame (6.25% area). Renderer code and its literal geometry test are unchanged. |
| Antigravity: no required fixes; renderer, timing and containment observations | **Retained as the reviewer's assessment of the earlier head.** No additional change follows from these positive observations. M-1/M-2 above address defects/limits not identified in that review. |

## Evidence and validation

The updated [software record](../software/renderer-cycle.md#manual-verification--27-october-2026) identifies the current tested file hashes, interpreter versions and full test results. Initial 87-test results belong to the reviewed head above, not to the later revision. Tests remain software-only, including guarded reruns that reject file/device opens, process launches and networking during functional cases.

The new baseline records can have `target_level=None` if no menu observation was available. This preserves unknown evidence rather than replacing it with the fake's hidden initial setting. A baseline observation inconsistent with the simulator still stops; that check is explicitly a simulation-only invariant, not an implementable physical readback strategy.

No equipment claim becomes Confirmed. The 6.25% patch, all physical-plan prerequisites and the stop-on-uncertainty boundary are preserved. T-003/T-005/T-006 remain **NOT AUTHORISED**, and future physical interfaces, correction validation, signal-range evidence and T-013/T-008 planning remain outstanding.

## Required next review

Claude Code or Antigravity must review the revised PR head before the owner decides whether to merge. Claude re-review is especially useful because Claude raised M-1/M-2; either different vendor satisfies the independence rule. Ask the reviewer to verify the reservation boundary, observation/capture semantics, simulator-only limitations and regression results. An approval of the initial head alone does not cover this revision.
