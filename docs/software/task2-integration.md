# Task 2 — combined meter and serial source

**PR #42 now combines the reviewed meter and serial input fixes in one source tree. The new hardware-free regression run passed 333 tests. This integration needs focused cross-vendor review; it authorises no equipment operation.** Codex (OpenAI), 9 November 2026. The final integration SHA is recorded in PR #42 and the review handoffs, avoiding a self-referential commit.

## Baseline and scope

| Identity | Exact revision / observation |
|---|---|
| Current main | `58fcfb7c2599b75a604d0490e52c6b9b3563a1ca`, the owner's merge of PR #41 |
| Reviewed meter head included in main | `b5c48060ed1abf3e4b256399d4589ae63e074834` |
| Previous reviewed serial head | `a7c1351adeaf73de0d043dbb029d45f1e6f9bd59` |
| Author branch | `codex/serial-console-events`, existing PR #42; no force-push or history rewrite |
| Concurrent work | GitHub reported only PR #42 open at reconciliation start; PR #41 was confirmed merged |
| Authority | Owner requested source/document/manifest reconciliation and hardware-free verification, explicitly excluding PR merge and equipment operation |

Main was incorporated into the existing serial feature branch locally. No GitHub PR merge, deployment, release, purchase, automation configuration or equipment step was performed. The historical 36-file meter and 37-file serial manifests cannot identify a combined source; they remain unchanged as records of their original heads.

## What was reconciled

Eight documentation paths had textual conflicts: `LEDGER.md`, `README.md`, `docs/reviews/README.md`, `docs/software/component-readiness.md`, `docs/software/component-tools.md`, `docs/software/first-release-specification.md`, `docs/tests/T-006-exlink.md` and `docs/tests/component-execution.md`.

The resolution retains both fixes and both sets of evidence rather than choosing one branch's status wholesale:

- C-138's explicit noninteractive regular-file give-up response, restricted accepted-output grammar, bounded raw capture and no-kill supervision remain. A deadline does not prove child or driver shutdown; lower-level acquisition/retries and cleanup remain outside the acceptance bound.
- C-139's complete nonwaiting console events, q preservation, mouse-only action allowlist, multi-poll GUI quiescence, fixed-width Win32 ABI, deadlines and uncertain-outcome stops remain. GUI/console/native timing and actual host abandonment are unverified.
- S-102/S-103/S-104, C-138/C-139 and T-020/T-021 coexist without renumbering. S-105/T-022 record this integration and its new verification. Current instructions use the new combined manifest; separate-head results stay historical.
- The existing open host-output/abandonment procedure includes the nonblocking serial re-review note about scrollbar/suspend states and Ctrl+C copying during selection. This is a clarification of source limits, not an adopted recovery recipe or a native observation. Optional pre-open stop-category and backend-error-message polish are not introduced in this integration.
- T-003/T-005 wrapped readings and T-006 remain NOT AUTHORISED. Discovery-only, isolation, display/geometry, electrical compatibility, setting scope/restoration, correction validation and exact owner permission retain their separate gates. Combining source files does not establish safe simultaneous meter/serial operation or implement a combined hardware controller.

### Application and test identity

Static comparison confirms all **20 application Python modules** exactly match the intended reviewed parent bytes: `tv_autocal_tools/meter.py` matches merged main; every other application module matches the reviewed serial head (many are identical in both parents). No application code needed manual conflict resolution or a new runtime edit.

There are **18 test Python files**, including the frozen manual audit fixture, and 17 unittest modules. Every test file matches a reviewed parent except the automatically reconciled `tests/test_component_entry.py`: its meter fixture retains `_MEASUREMENT_PROMPT` from main, and its serial CLI fixture retains explicit control coordinates and assertions from the serial head. This union is the only combined test-file edit. No test was removed, skipped or weakened.

The active [combined manifest](component-source-sha256.json) covers exactly all **38 Python application/test files**, including the historical audit fixture. It records the main and reviewed parent identities. Documentation, dependency declarations and the manifest itself are bound by the final reviewed Git commit, not by this Python-only hash set; no dependency or licence choice changed.

The following old manifests are preserved byte-for-byte and are **historical, not active launch identities**:

| Historical artifact | Source it identifies |
|---|---|
| [Meter 36-file manifest](https://github.com/murphys-logs/tv-autocal/blob/b5c48060ed1abf3e4b256399d4589ae63e074834/docs/software/meter-error-policy-manifest.sha256) | Meter-only reviewed head `b5c4806`; 301-test author record |
| [Serial 37-file manifest](https://github.com/murphys-logs/tv-autocal/blob/a7c1351adeaf73de0d043dbb029d45f1e6f9bd59/docs/software/serial-console-input-sha256.json) | Serial-only reviewed head `a7c1351`; 319-test author record |

No single old manifest is applied to mixed bytes. Existing 34-file/287-test and earlier records also remain historical. Archived briefs/research are untouched.

## Combined offline verification

All 18 test entry points and the actual application entry/permission boundaries were inspected before execution. The review checked module-level execution and every process/native/GUI/serial/network/signal route used by tests, including the combined CLI fixture and containment guards. Hardware-facing paths are replaced by inert fixtures or rejected before use; the inherited T-009 fixture writes temporary inert Python text without importing or executing it. Reader threads operate on in-memory streams.

The actual interpreter reported `3.15.0 (tags/v3.15.0:d220409, Oct 9 2026, 11:55:56) [MSC v.1951 64 bit (AMD64)]` on Windows 10 build 19045 AMD64. Commands ran from the combined checkout's repository root on 9 November 2026:

| Actual command | Passed | Failures / errors / skipped | Duration |
|---|---:|---|---:|
| `py -3.15 -B -m unittest discover -s tests` | 333 | 0 / 0 / 0 | 13.988 s |
| `py -3.15 -B -m unittest discover -s tests -p 'test_component_meter*.py'` | 50 | 0 / 0 / 0 | 0.173 s |
| `py -3.15 -B -m unittest discover -s tests -p 'test_component_serial*.py'` | 61 | 0 / 0 / 0 | 0.075 s |
| `py -3.15 -B -m unittest discover -s tests -p test_component_containment.py` | 2 | 0 / 0 / 0 | 4.234 s |
| `py -3.15 -B -m unittest discover -s tests -p test_software_containment.py` | 1 | 0 / 0 / 0 | 2.844 s |
| `py -3.15 -B tests/audit_ground_up.py` | All assertions | Exit 0; frozen historical decoder/arithmetic only | Not timed |

No discovered test was unrun. The component containment rerun includes all 182 functional component cases under real I/O/native/signal guards; reruns are not additional distinct cases. Full discovery used normal temporary-directory permissions solely for the unchanged inert T-009 fixture. No new fixture failure or skipped case occurred in this integration run. Python source files use the existing LF attribute.

These are new author results for the combined bytes, not a sum or reuse of 301 and 319. No Linux run of this combined head is claimed. No Argyll executable (including help/discovery), native console/GUI probe, device/display enumeration, serial port, measurement pattern, signal delivery or equipment contact occurred. No dependency was installed.

Passing fakes do not validate native console or Tk delivery, file-handle inheritance into the installed Argyll binary, USB/driver cleanup, GUI placement/focus/startup, QuickEdit/output stalls, serial line timing/loss, electrical compatibility, TV response, restoration, measurement accuracy or safe meter/serial coexistence. Bounded acceptance/input work is not a guaranteed OS/driver completion time.

## Review provenance and X-020

The owner supplied complete final-head re-review texts for both original fixes on 9 November 2026. Claude Code (Anthropic) and Antigravity (Google) each recommended merge at meter head `b5c4806` and serial head `a7c1351`. Claude's [serial re-review is posted on GitHub](https://github.com/murphys-logs/tv-autocal/pull/42#pullrequestreview-5831088878); no public URL was supplied for the other three texts. Private paths/execution narration in the supplied messages are not reproduced, and no public receipt is invented.

Claude reports Linux/Python 3.13.18 passing 301/50/2/1 for the meter head and 319/61/2/1 plus audit for the serial head. Google reports Windows/Python 3.15.0 passing those corresponding suites and manifest checks. These remain **reviewer-reported results for the separate heads**. They do not review or validate this new combination; internal Codex assistance is one vendor.

In the final meter re-review Google explicitly accepted the X-020 qualifications: source does not establish device-specific forced termination/replug necessity, safety or sufficient recovery; “optimal/safest” was comparative judgement; silent lower-level retries are outside output parsing; exit zero is necessary but insufficient. X-020 is therefore recorded as resolved by those qualifications, with no recovery policy or equipment evidence adopted. Existing no-kill and authorisation rules remain binding.

## Focused review and remaining work

Review the final PR #42 head against main `58fcfb7`, and compare reconciliation with serial parent `a7c1351`. Check all eight conflict resolutions, parent byte identities, the combined CLI fixture, the 38-file manifest, preserved historical results and the new combined runs. Verify the X-020 resolution fairly reflects the supplied re-review and that every physical/native gate remains open. Repeat only inspected hardware-free checks using an actually available interpreter and disclose platform/coverage limits.

No PR #42 merge is performed by this task. The integrated head is ready for focused Claude/Antigravity assessment; original-head recommendations do not automatically approve its documentation, manifest or combined verification. Only the owner decides whether to merge after that review and separately authorises any future physical use.
