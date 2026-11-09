# Meter error and input policy

**The wrapper now supplies an explicit give-up response and rejects every transcript outside its one supported success form. This is a software fix for A-007/C-136, not proof of driver shutdown or permission to use equipment.** Native Argyll, instrument and cleanup behaviour remain untested. The [shared wrapped-reading hold](../tests/component-execution.md#meter-attempt-and-closure), exact-source review and remaining physical prerequisites still apply.

Codex (OpenAI) prepared this policy on 9 November 2026 from current main `d5469297ed7cf8a41ff11585d84e1f0e44575364`, the implementation, latest audit/review responses and exact Argyll source. No Argyll executable was launched, including help/discovery; no port/device was opened or enumerated, equipment contacted or pattern displayed. The prior [audit](../reviews/2026-11-08-ground-up-audit.md#a-007--wrapped-meter-readings-do-not-control-argyll-error-retries) and its historical verification remain unchanged.

## What the defect was

`-O` does not mean one instrument attempt. V3.5.0 can prompt and continue after a misread or communications failure; other generic branches can continue without asking. The old wrapper supplied DEVNULL, inherited Argyll's input mode and waited for completion. EOF is not an abort answer, a zero exit can follow an error, and a deadline does not terminate a child.

The change gives the selected path one explicit response and a stricter acceptance rule. It preserves fixed arguments `-O -e -x -Y n` with the unique logfile last, reviewed executable/hash/discovery assertions, two prestarted readers, separate stdout/stderr and the existing no-kill supervision policy. Accepted values remain component diagnostics, never calibration data.

## Supported source and identity

The retained [official ArgyllCMS V3.5.0 source ZIP](https://www.argyllcms.com/Argyll_V3.5.0_src.zip), release dated 4 February 2026, was rehashed and its members read directly as text on 9 November 2026. ZIP SHA-256: `f8576ce5589fd15620abb73ff049ea31f55ddbd1bba6d1ffa87452658e7bc85f`. This is a fresh inspection of the retained S-037 artifact, not a newly downloaded copy or source-build verification of the selected executable.

| Member below `Argyll_V3.5.0/` | SHA-256 |
|---|---|
| `spectro/spotread.c` | `f903bd8cf3cfb9b7eb1c31ea413859f064a346c8567f4321fc3dabd69ba91d24` |
| `numlib/numsup.c` | `cf361c4acf302de8ab112f5da90e62943ffa5ff664fbe2eae4646f438a49e4f5` |
| `spectro/conv.c` | `c6b04014888cb6f4bbd90237460278498766fe20e3ec3d000edadb9e7f74a6fd` |
| `spectro/instappsup.c` | `249e0bfdb8904f8efae4537672ce7d3b1c5935b7fe2000c53ff3031c3c38d63b` |
| `spectro/spyd2.c` | `2e2db1744774740436071a4806ab1142e064b0cf8f7332f8b5b38ee3252a025a` |

Locators below count LF-delimited source lines. Relevant `inst.c` and `icoms.c` excerpts were also consulted. No downloaded source/tool is committed.

The supported success branch is selected USB Spyder5, absolute emissive `-e`, Yxy `-x`, non-refresh `-Y n`, without spectrum, reference, ambient, X-Y table, instrument switch, target, verbose/debug or `SALONEINSTLIB` alternatives. Exact package/executable identity and actual device/configuration still need the reviewed session checks. Source inspection does not prove binary build options or native behaviour.

## Input and inherited environment

Before launch, the wrapper removes both correction-default variables and every case variant of `ARGYLL_NOT_INTERACTIVE`, then supplies one canonical `ARGYLL_NOT_INTERACTIVE=1`. An inherited empty value or `0` cannot silently choose the policy: V3.5.0 tests presence, not truthiness (`numsup.c:225–258`). Other environment settings, including serial-scan exclusions, are retained. This is not complete environment sanitisation and does not replace physical serial isolation.

The wrapper creates a binary temporary regular file, writes exactly the two bytes `q` and LF in one operation, checks the write, flushes and rewinds it **before** calling `Popen`. Allocation/write/flush/rewind failure therefore prevents launch. The file is stdin; neither operator keys nor retry/continue text are forwarded. The parent retains its file through confirmed child exit and reader completion, then attempts closure. A close failure rejects the result; cancellation during closure is latched while cleanup continues.

This choice follows the exact Windows source rather than assuming DEVNULL or an empty pipe is safe:

| Input path in `conv.c` | Consequence |
|---|---|
| Interactive or noninteractive CHAR, `182–201,252–255` | Uses CRT console input; redirecting a file alone does not select that file |
| Noninteractive PIPE, `204–236` | Accumulates up to ten bytes or a delimiter; EOF with a waiting call can loop, and an empty blocking pipe can block |
| Noninteractive regular-file branch, `238–245` | Polls do not read; a waiting call reads up to ten bytes once and returns the first byte. EOF/read failure returns zero |

`numsup.c:241–245` requests pipe NOWAIT without checking success. The regular file avoids dependence on that request and avoids postlaunch stdin writing. Its branch technically also covers handle types other than CHAR/PIPE; the wrapper supplies an actual temporary file rather than treating an unknown handle as valid. Native inheritance/classification remains untested.

Noninteractive `empty_con_chars()` leaves supplied input unread (`conv.c:275–276`). The selected `-O` callback immediately triggers and does not consume it (`spotread.c:423–428,1887–1888`; `spyd2.c:3077–3101`). Ordinary Spyder initialization contains no input callback. Serial identification/default callbacks are separate paths (`inst.c:634–646`, `instappsup.c:53–80`); this policy does not broaden supported devices or relax C-090 isolation.

The regular-file branch does not need the LF to delimit its read; it returns q and discards the rest of its up-to-ten-byte batch. There is one response, not a renewable supply. A later unsupported waiting read can reach EOF and return zero; it must not be described as another reliable abort answer.

## Success and failure policy

The wrapper requires complete capture, complete logging, confirmed zero child exit, no cancellation/deadline failure, and this whole-stdout contract:

1. Exactly the selected ordinary placement/command prompt from `spotread.c:2189,2193–2196,2200,2207`.
2. Exactly one complete Yxy result using the supported numeric grammar, with no other non-whitespace suffix.
3. Empty stderr. CRLF is normalised to LF for grammar checking; original raw bytes remain unchanged.

`-O` does **not** suppress the ordinary prompt. Its final colon-space has no newline: `fl_end` remains empty (`numsup.c:208,223`), and the result formatter supplies the separating newline (`spotread.c:2969–2970`). Bare results, missing/truncated/repeated/alternative prompts, unknown preludes/trailers and other output modes fail closed. The legacy synthetic parser keeps its broader contract; the fixed wrapper applies this narrower rule.

CCT defaults off (`spotread.c:601`); ambient toggling at `1170–1176` does not apply to fixed `-e`, and `-T` is absent. No CCT/CRI extras are allowed. No reference, density or spectrum output is selected. The normal `-O` exit follows the result/log writes (`3171–3172`), then common cleanup (`3187–3201`).

| Upstream outcome | Explicit policy and source limit |
|---|---|
| Successful selected sample | One supported prompt/result, exit and complete streams can be accepted; q remains unread |
| Misread or communications failure | q answers the first blocking give-up question, before application retry or communications reinitialisation (`2329–2369`). Error output is rejected even if exit is zero |
| User-abort question | q selects give-up (`2301–2310`); the transcript remains rejected. Wrapper cancellation does not inject a driver interrupt |
| Initial or mid-read calibration | Calibration text is rejected. Immediate calibration may perform work without reading stdin (`2109–2151,2313–2322`; `instappsup.c:222–223,403–404`) |
| Wrong-position/configuration | Output is rejected, including any later result; the generic branch can continue without reading q (`2324–2326`) |
| Fatal error or failed setup | Reject diagnostics, absent/ambiguous result, incomplete capture or unsuccessful exit. Fatal dispatch can still reach zero-return cleanup (`2373–2379,3201`) |

For this driver, `spyd2.c:3442–3487` has no wrong-config mapping; its needs-calibration return at `3338` concerns explicit refresh querying outside ordinary fixed sampling. That narrows the supported path; it does not erase generic branches. The fakes must show that a nonprompting continuation can leave q unread and still produce a later result that is rejected.

## Acceptance bounds and completion evidence

The wrapper accepts at most one supported measurement and supplies no application retry answer or second child launch. An error followed by an uncontrolled internal retry cannot silently become an accepted result. This does not mean one low-level device operation: V3.5.0 has USB retries (`spyd2.c:120,695–830`) and adaptive acquisition (`1727–1784`) below the application prompt.

Timeout and cancellation permanently reject acceptance. Supervision and bounded draining continue, potentially indefinitely, until observed child exit and output-reader completion. Per-stream raw retention remains 65,536 bytes; later bytes are drained and counted, and overflow, read/log/close errors prevent acceptance. Neither a timeout nor exhausted stdin is proof of driver shutdown.

The journal/result distinguish wrapper/child PIDs, `meter_child_exit`/`child_exit_confirmed`, stream EOF, `meter_readers_complete`/`readers_complete`, and final wrapper reporting. `meter_wrapper_complete` means supervision reached final reporting after resource-close attempts; it does not prove OS termination of the wrapper or successful cleanup after a recorded close error. Wrapper-console closure, shutdown, Ctrl+Break and forced termination remain outside the SIGINT contract. No restart, replug, reset, kill or assumed recovery is introduced.

If a stronger requirement demands exactly one `read_sample` call across all instruments, no automatic calibration/position continuation, or a bounded driver shutdown, the existing console adapter cannot establish it. A concrete alternative is a separately reviewed, source-pinned Argyll frontend/amendment that returns structured statuses and enforces application limits before cleanup. It needs build/licence/provenance review and separately authorised native validation; it cannot promise that a stalled driver or cleanup call is interruptible merely by changing the frontend.

## Offline verification

The [complete 36-file source/test manifest](meter-error-policy-manifest.sha256) identifies this amendment's software bytes, including the new regression module and manual audit probe. The old 34-file manifest and October/November audit results remain historical; they do not validate these changes. The separate serial amendment is not included: combining changes requires reviewed source/manifest reconciliation.

All 16 existing test entry files were inspected before the first run, including the manual audit probe and the existing temporary inert-text fixture. New tests were also read before execution. On Windows 10 build 19045 AMD64, the installed interpreter reported `3.15.0 (tags/v3.15.0:d220409, Oct 9 2026, 11:55:56) [MSC v.1951 64 bit (AMD64)]`. No Python 3.12 run is claimed for this source.

| Command, from repository root | Actual result, 9 November 2026 |
|---|---|
| `py -3.15 -B -m unittest discover -s tests` | Final 298 passed; 0 failures/errors/skips, no discovered test unrun; 14.205 seconds |
| `py -3.15 -B -m unittest discover -s tests -p test_component_meter*.py` | 47 passed; 0 failures/errors/skips |
| `py -3.15 -B -m unittest discover -s tests -p test_component_containment.py` | 2 passed; reruns all component cases with real file/process/network/native/signal operations forbidden |
| `py -3.15 -B -m unittest discover -s tests -p test_software_containment.py` | 1 passed; guarded pure software regressions |

The explicit 47-case/containment run preceded only the final event-order assertions; the final full suite includes those assertions and both guarded reruns. Eleven new meter-policy cases model the upstream dispatch and input contract; existing meter/CLI fixtures now include the required prompt. The initial 297-case run reported two failures caused by the old CLI bare-result fixture and one sandbox temporary-directory permission error in unchanged T-009. After fixture correction, a normal-permission 297-case run passed; the final extra nonprompting-continuation case and lifecycle assertions produced the 298-case pass above. No test was skipped or weakened. Normal-permission execution was needed only because the sandbox denied the inherited inert temporary-text fixture.

The source-model regressions use fake processes, streams, temporary files and clocks, covering first-prompt give-up, old retry responses, nonprompting continuation, fatal/calibration-only zero exits, strict prompt grammar, split diagnostics, preparation failures and input-resource closure/cancellation. Existing lifetime tests cover late output, cancellation, timeout, overflow and separate child/reader completion. Passing fakes establish these software contracts only; native console, file-handle inheritance, Argyll binary, instrument and driver shutdown remain untested.

## Documents consulted and physical prerequisites

The live [Argyll environment documentation](https://www.argyllcms.com/doc/Environment.html#ARGYLL_NOT_INTERACTIVE), [Python subprocess documentation](https://docs.python.org/3.15/library/subprocess.html) and [tempfile documentation](https://docs.python.org/3.15/library/tempfile.html) were opened on 9 November 2026. The Argyll page describes noninteractive input/progress and correction defaults; exact Windows branch details above come from the pinned source. Python documents file-object stdin, explicit child environments and temporary-file ownership. Its live pages identify themselves as **3.15.2**; that label must not be confused with the separately reported **3.15.0** test interpreter.

Before physical use, the final exact source and affected plans need cross-vendor review, then the owner must supply dated authority for the particular steps. The selected executable/hash/build/configuration, native regular-file stdin and selected success/error handling, actual closure, meter behaviour and interruption procedure remain unverified. No recovery experiment is implied. All unrelated display, isolation, correction, electrical, restoration, discovery/session and equipment-authorisation gates remain; this amendment cannot mark any equipment test complete.

