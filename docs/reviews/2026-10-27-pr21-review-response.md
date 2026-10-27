# PR #21 — assessment of independent reviews

Assessed and revised by Codex (OpenAI), 27 October 2026, at the owner's request to address valid review findings without operating hardware. This is a review record, not equipment evidence or physical-test authorisation.

Both reviews assessed original head `9df5521779d44ceb5f985435fa9d07812c270864` against base `ba099e0a182713945c247636042286e6f9dca626`:

- [Claude Code (Anthropic)](https://github.com/murphys-logs/tv-autocal/pull/21#pullrequestreview-5672025283): change first for M-1/M-2; software prototype acceptable within its stated scope.
- [Antigravity (Google)](https://github.com/murphys-logs/tv-autocal/pull/21#pullrequestreview-5672222191): change first for M-1/M-2; software prototype acceptable within its stated scope.

These reviews do not approve the subsequent changes. The revised PR needs independent re-review before the owner's merge decision. The automatic Codex bot is the author's vendor and is not counted as an independent reviewer. No hardware, Argyll executable, serial port, measurement pattern or device control was operated during this response.

## Findings and disposition

| Finding | Assessment and change |
|---|---|
| Both M-1: Argyll startup serial probing | **Accepted.** Fresh source inspection S-037 confirms a conditional fast-serial probe path, including help/discovery. T-003/T-005 now require both Ex-Link ends disconnected before launches, record that state and leave the cable disconnected. T-006 excludes ArgyllCMS/DisplayCAL and other discovery tools while connected. C-090 and the staged plan carry the future meter-adapter/coexistence constraint. The owner's adapter classification and binary behaviour remain untested; the reviews' unconditional wording is not adopted. |
| Both M-2: range interpretation | **Accepted.** T-005 purpose, outcome and conclusion now describe clipping/stability screening only. Limited decoded as Full and repeated compression can pass these checks. The ledger and staged plan explicitly retain the unmet Stage 4 black/white interpretation gate; a screening pass alone cannot satisfy T-013/T-008. No extra physical comparison is added. |
| Claude L-1 / Antigravity L-2: later optical session | **Accepted.** T-005 M0 verifies a continuous session or repeats authorised preparation with a fresh dated baseline after restoration/a later session. R1 restores that session's originals. |
| Claude L-2: electrical gate | **Accepted.** T-006 defines evidence for both actual hardware interfaces: pins, reference, polarity, transmitter limits and receiver tolerances. Generic labels or agent agreement cannot close it. Missing documentation leaves it blocked; physical investigation or a residual-risk proposal requires its own reviewed amendment and explicit owner decision. No risk acceptance is inferred. |
| Both L-3: setting scope | **Choice accepted; premise unresolved.** Mandatory Current Source isolation is removed. Both retained All Sources and explicit isolation need reviewed baseline/restoration procedures and an owner choice. S-033 does not establish that every input/mode shares the same values or that one restoration restores all scopes. X-012 preserves that remaining disagreement. |
| Claude L-4: stopping a meter reading | **Accepted.** T-003 defines normal stop, outstanding-process reporting and the 60-second workflow limit. The owner may end their PC activity with the abort risk stated. There is no automatic kill, restart or recovery; unfinished attempts remain in the record. |
| Claude L-5 / Antigravity L-1: low-light rule | **Accepted.** T-003 names every adjacent pair, including 0→5, adds a two-printed-increment floor, and requires an unbroken passing range. Zero remains noise evidence, not panel-black validation. Undefined chromaticity at zero/non-positive XYZ sums cannot pass the nonzero usable-range criterion. |
| Claude L-6 / Antigravity L-4: dropped late fake replies | **Accepted as a documented limitation.** The permitted one-request fake is unchanged. Its early return discards later scripted/delivered bytes; the software record gives the ACK-then-NACK example. T-006 demands separate tests showing the future sender retains all bytes through port closure and stops further sends on unexpected replies. |
| Claude L-7: Planned versus Not tested | **Accepted.** C-002/C-005/C-087/C-089 are Planned. The ledger explains why compound claims with only partial plan coverage remain Not tested; source-only/software-only labels remain separate. Nothing becomes Confirmed. |
| Both: C-086 provenance and S-014 scope | **Accepted.** Standard AI provenance label restored; the source row records the 27 October option/discovery/default-calibration consultation. |
| Claude: missing C-030/C-010 references | **Accepted.** Claim/test links now include the relevant T-005/T-006 relationship, without implying broad validation. |
| Claude: T-005 settings record | **Accepted.** HDMI UHD Color, Digital Clean View and Auto Motion Plus are record-only fields; no new setting changes are permitted. |
| Claude: AGENTS path map | **Accepted.** Section 12 lists application prototype, software tests and software records; full application and packaging/licence choices remain future work. |
| Claude: recursive containment check | **Accepted.** Static inspection now descends into subpackages. A regression creates inert nested source, proves permitted text passes and a forbidden import is caught, without importing or executing the fixture. |
| Claude: menu-close timing | **Accepted.** T-006 records menu identity, open/send/close times and requires a reviewed interval excluding automatic closure. Unknown/overlapping timing is inconclusive. The same rule applies to all three EXIT attempts. |
| Claude: Q-013 stop boundary | **Accepted.** T-006 requires acceptance of this test's stop boundary, not selection of a future fallback. README and the staged proposal agree; Q-013 remains open. |
| Claude: plain English | **Accepted.** ACK/NACK and statistical terms receive explanations in the relevant plans/software record. |

## Two recommendations not adopted

**Antigravity M-1's `ARGYLL_EXCLUDE_SERIAL_SCAN=1`: incorrect for the inspected version.** S-037 `spectro/icoms.c:580–624,640–656` parses a comma/semicolon-separated list and compares literal port names (`strcmp` at line 649). `1` is not a blanket disable flag and cannot match `COM3`. T-003 and C-090 explain the verified semantics and keep physical disconnection mandatory. Exclusion effectiveness on this installation is still untested. This source check settles the syntax issue; it does not establish hardware safety.

**Antigravity's proposed single-hyphen anchor: false positive.** The archived heading is “Proposed software-only verification plan — T-009”. GitHub-rendered HTML at the reviewed head was checked on 27 October 2026: its outline anchor is `proposed-software-only-verification-plan--t-009` and heading ID is `user-content-proposed-software-only-verification-plan--t-009`. The existing link is retained; changing it would break the target. The archive is untouched.

## Related source finding

While checking M-1, Codex verified that two environment variables can load an external correction even without `-X` (`spotread.c:1150–1158`; C-091). T-003 now records their presence privately and clears them only in a dedicated future test shell; T-005 inherits that prerequisite. No persistent environment or correction file was changed and no owner environment was inspected during this work.

## Validation and remaining gates

The revised [software record](../software/t009-prototype.md) records 39 passed, zero failed/errors/skipped/unrun on each of Python 3.12.14 and 3.15.0, including recursive containment and the guarded rerun of 35 functional cases. It preserves the earlier runs and the temporary-directory permission errors encountered under the sandbox before the successful local runs. Application module hashes and behaviour are unchanged; the test-file hash is updated.

The source archive was read only; its SHA-256 matched the value in Claude's review. No downloaded tools or source were committed. Local links/anchors, ledger IDs, plan template sections and recorded software hashes were checked; the two pre-existing broken relative links in the archived claim-notes-review brief remain untouched. No existing archive or workflow was changed.

All three physical plans remain **NOT AUTHORISED** and unrun. Renderer, electrical, scope/restoration, menu-timing and physical-sender gates remain as specified; the Stage 4 range-interpretation gap and concurrent meter/serial design also remain open. A merge of this PR would accept reviewed plans and software work only. The owner still decides whether to merge after independent re-review.
