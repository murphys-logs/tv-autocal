# PR #41 — review response and focused follow-up

**The meter policy is retained. This follow-up fixes portable fake-process setup, accurately describes the accepted grammar, and preserves the original error if prelaunch cleanup also fails. Physical wrapped readings remain NOT AUTHORISED.** Codex (OpenAI), 9 November 2026. The final follow-up SHA is in [PR #41](https://github.com/murphys-logs/tv-autocal/pull/41) and the re-review prompt; this document does not embed its own commit hash.

## Reviews actually received

Both independent reviews address `11afa53192f615b48dd40f0eb08bc57bae27b84a` against main `d5469297ed7cf8a41ff11585d84e1f0e44575364`:

- **Claude Code (Anthropic): change first**, F1 portability and F2 grammar wording; F3 closure-interrupt coverage and F4 primary-error preservation are optional. Supplied by the owner in this chat, 9 November; Claude explicitly says the review was not posted on GitHub. It reports a fresh ZIP/member/source inspection and Linux/Python 3.13.18 runs, with targeted rather than full audit/PR39 reading.
- **Antigravity (Google): merge from a software perspective**, with disclosed single-use input and unbounded driver limits. Supplied by the owner in the same message, including reported Windows/Python 3.15.0 results and source/manifest inspection. No public review URL was supplied; none is invented here.
- **Codex connector bot (OpenAI): [portable creation-flag fixture finding](https://github.com/murphys-logs/tv-autocal/pull/41#discussion_r4516423884)**. This is the author's vendor and adds no independence.

The GitHub connector and live API initially exposed only the bot on PR #41 and Claude's separate PR #42 review. The owner then supplied the missing texts, satisfying access to the actual reviews. Private machine/scratch paths and the surrounding execution narration in that supplied text are not reproduced. Reviewers' reported executions are attributed to them; the new author runs below are separate evidence. Neither recommendation transfers automatically to changed source.

## Findings and disposition

| Finding | Assessment | Change or precise qualification |
|---|---|---|
| Claude F1 / bot: `_spawn` tests import Windows-only subprocess flags on Linux | **Agree.** Mocking Popen and TemporaryFile alone does not supply missing names. This is a test portability regression; main's hardware-free suite did not require them. | Every policy test now installs both inert flags with `create=True`, including failure-before-launch cases. Source-model spawn tests also check the requested flags. Physical launch flags/runtime routing are unchanged. |
| Claude F2: output described as more exact than the implemented grammar | **Agree on wording.** The placement prompt is exact; the result uses the inherited finite signed/scientific parser and permits surrounding whitespace. None of those forms lets diagnostic or retry text through. | Clarify the policy, T-003/shared instructions and ledger; add a regression accepting extra whitespace, missing result indentation and signed/scientific notation while still rejecting appended retry text. Do not tighten diagnostic numeric grammar or claim physical validity. |
| Claude F3: input-close Ctrl+C untested | **Partly agree on direct exception coverage.** The original `test_repeated_sigint_is_latched_through_launch_supervision_and_cleanup` already includes `input-close`, using an inert latched handler. It does not directly raise KeyboardInterrupt from close. | Retain that coverage and add an explicit KeyboardInterrupt close case: close is retried, child/readers stay confirmed and the attempt is cancelled/rejected. No signal or native file is used. |
| Claude F4: secondary close exception hides preparation/launch exception | **Agree; useful diagnostic correction.** No child was returned for supervision, but replacing the primary error obscures the cause. | Re-raise the original exception and attach a note identifying the separate cleanup error type. Tests cover preparation and launch failures with failed cleanup. No error messages or private paths are copied into the note. |
| Google: single-use stdin and a second prompt may retry at EOF | **Agree as a disclosed source limit.** One q is not a renewable abort policy. | No new retry input, restart or termination. Unexpected continuation output remains rejected; supervision may be indefinite. |
| Google: unbounded driver/native completion | **Agree on absence of a guarantee.** Accepted measurement limits and observed process/readers completion are different from interruptible driver shutdown. | Physical hold and existing no-kill policy remain. |

Claude's F1/F2 requested changes are implemented; F3/F4 receive the bounded refinements above. Google found no required software change, but that recommendation does not contradict making the test/claim/diagnostic fixes. Both vendors need focused assessment of the changed head.

## Source claims not adopted from the Google review

The review endorses the core regular-file policy and correctly separates application prompts from lower-level acquisition. Several stronger statements are not established by the cited source or passing fakes:

- The exact prompt and permitted result grammar are different from byte-exact source formatting, as Claude F2 shows. Allowed whitespace/numeric forms do not weaken diagnostic/retry-text rejection. Separately, the Google review's claim about **any** internal retry cannot cover lower-level retries that emit no application diagnostic; the maintained claim concerns emitted error/prompt/continuation text, not every internal device operation.
- The source does not establish that every stalled USB handle necessarily blocks `it->del`, or that bounded shutdown universally requires external process termination, with potential power cycling/replug as the review suggests. Neither necessity nor recovery safety on this installation is established. None is an adopted procedure.
- “Optimal, safest” is a reviewer judgement without an exhaustive comparison. The repository does not contain a blanket ban on compiling software-only custom frontends. The alternative remains a separately reviewed engineering/build/licence proposal, not equipment permission or a newly required implementation.
- Exit zero is insufficient evidence of validity; it is still a required part of the combined acceptance contract. It is not treated as proof of a successful measurement.

X-020 preserves the disputed stronger recovery/optimality propositions for re-review. No recovery experiment is requested. The consulted Argyll source identity and fixed selected Spyder5 path remain those in [the policy](../software/meter-error-policy.md#supported-source-and-identity); this revision introduces no new claim of upstream or native execution.

## Verification of changed source

Before execution, the previously inspected entry points were compared against the unchanged baseline; the changed policy test module and component-containment entry were reread. New cases were inspected before running. Windows 10 build 19045 AMD64; interpreter reported `3.15.0 (tags/v3.15.0:d220409, Oct 9 2026, 11:55:56) [MSC v.1951 64 bit (AMD64)]`.

| Actual command from repository root | New result |
|---|---|
| `py -3.15 -B -m unittest discover -s tests` | 301 passed; 0 failures/errors/skips; 13.328 seconds |
| `py -3.15 -B -m unittest discover -s tests -p 'test_component_meter*.py'` | 50 passed; 0 failures/errors/skips |
| `py -3.15 -B -m unittest discover -s tests -p test_component_containment.py` | 2 passed; guarded component rerun included |
| `py -3.15 -B -m unittest discover -s tests -p test_software_containment.py` | 1 passed |

All these results cover the final runtime/test edits in this follow-up. The full suite used normal temporary-directory permissions for the inherited inert T-009 fixture; no case was skipped or weakened. Before the optional runtime/regression refinements, the portability-only snapshot separately passed 298/47/2/1; those are intermediate results, not the final counts.

An internal OpenAI helper also used an inspected in-memory harness under `component_io_guards` to remove both Windows constants before loading the original 11 policy cases. Suppressing the new setUp reproduced one failure and ten ImportErrors; restoring it passed 11/11, and component containment passed 2/2 with the names absent. The harness restored the original module attributes afterward. This is Windows missing-name emulation, not an author Linux run or independent vendor review.

The same guarded missing-name check was then run against the final source: 14/14 policy cases and 2/2 component-containment cases passed, with zero failures/errors/skips. Original Windows attributes were restored. No real file/process/native/equipment boundary was used.

Claude reports Linux/Python 3.13.18: original 298 run with two failures/ten errors, main 287/287, and patched scratch runs 298/47/2/1 passing. Google reports Windows/Python 3.15.0 298/47/2/1 passing at the original head. These are reviewer-reported results and do not validate this new head. A native Linux rerun of the new source is requested in the focused review, not invented here.

The refreshed 36-file manifest identifies current source/test bytes. The [initial 298-test record and manifest](../software/meter-error-policy.md#initial-policy-verification-at-11afa53) are preserved with their original commit; archived briefs/research are untouched. No Argyll command, instrument/serial/device/display enumeration, operational GUI, pattern, equipment contact, native console probe, signal delivery, installation, automation, release or merge occurred.

## Focus for re-review

Compare the final head with `11afa53192f615b48dd40f0eb08bc57bae27b84a`, then check the complete PR for regressions. Prioritise absent-constant fixture creation on Linux, precise prompt/result grammar, primary-versus-cleanup errors, direct close interruption and the refreshed manifest/verification attribution. Address X-020's review-source qualifications. Keep all native/physical holds; only the owner can merge or authorise future equipment work.
