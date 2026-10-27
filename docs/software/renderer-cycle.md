# Off-screen renderer and simulated measurement cycle

**Software only. No hardware operated or authorised.** This implementation produces image buffers in memory and exercises toy TV/meter objects. It does not open a window, select a monitor, launch ArgyllCMS, open a serial port or send device commands. Its results are synthetic software evidence, never calibration measurements.

Prepared by Codex (OpenAI), 27 October 2026, under [S-038](../briefs/2026-10-27-software-renderer-cycle.md), from merged baseline `f333df41805f5c1d6e195b6635abc6d853b62a25` (PR #21). Design choices are AI proposals recorded in S-039/C-092/C-093. T-014 and T-015 are new software-only tests; withdrawn test IDs are not reused.

## Technical choices

| Choice | Reason and limit |
|---|---|
| Python standard library only | No installation or new third-party dependency is needed. Python uses the PSF licence. This does not choose the project's licence (Q-002), supported production Python version or Windows packaging (Q-003). |
| Separate pure rendering and simulated control modules | Pixel generation can be checked independently of controller order and fault handling. Neither module contains a physical backend or a real-mode switch. |
| Fixed native 3840×2160, row-major RGB8 buffers | Matches the plans' source geometry. Each pixel is three unsigned bytes, red then green then blue, with no alpha or row padding. Values are application RGB codes, not demonstrated HDMI values or percentages of measured light. |
| Explicit integers and immutable records | Booleans are rejected as numeric settings/times/colour codes. Buffers and result snapshots cannot be changed through their public fields. This is predictable software behaviour, not a security sandbox against arbitrary Python modification. |
| Fake monotonic clock and explicit cycle calls | Tests advance time directly; no sleeps, wall clock, unattended runner or physical timing claim. The proposed 2,000 ms delay remains unvalidated under Q-008. |
| Literal scripted measurements and toy level 0–100 | The meter's XYZ samples are supplied independently of the requested setting. There is no model of this TV, spectral correction, optical accuracy or optimiser; the toy setting is not a Samsung command. |
| Stop after an uncertain outcome | No automatic retry, restart or restoration after failure/cancellation. Normal restoration is a separately requested simulated cycle and can itself fail. Physical recovery remains subject to its own reviewed plan. |
| Manual test invocation, no packaging or automation | No installer, executable release, scheduled task or GitHub Actions workflow is added. Production dependencies and deployment remain later choices. |

## Renderer boundary

The [renderer](../../tv_autocal/renderer.py) supplies the patch and visual-pattern buffers needed to review T-003/T-005's application-side definitions. A centred 960×540 measurement patch has black surround and no text underneath the meter area. Visual geometry, black/white/primary bars and one-pixel detail patterns are separately identified in an immutable manifest. Labels use a small original bitmap alphabet with integer pixels; there is no font file, antialiasing or image-library colour conversion.

Rendering never applies a limited-range conversion, gamma curve, correction profile or scaling. The native buffer is 24,883,200 bytes. Buffers are constructed on request rather than retaining every pattern at once. No file export or GUI presentation is part of this implementation.

**T-003/T-005 remain blocked for physical pattern output.** The missing presenter must later provide deliberate display selection, fullscreen presentation without scaling, a reviewed launch/close procedure and checks of the Windows presentation path. These buffers do not establish correct HDMI range decoding, bit-exact transport, visible pixel geometry or actual light output. The additional Stage 4 range-interpretation method remains unresolved.

The library API is `render_patch((r, g, b))`, `render_pattern(name)` and `pattern_manifest()`. Names, in plan order, are `geometry`, `black`, `white`, `red`, `green`, `blue`, `detail`. The manifest records the visual regions, colours and label positions. T-003 range codes and T-005 neutral/primary codes are separate literal tuples; none is a timed playlist or launches an automatic sequence. `RGBFrame.pixel(x, y)` reads a top-left-origin pixel for software inspection.

| Pattern | Application-side definition |
|---|---|
| Measurement patch | Rectangle x=1440…2399, y=810…1349; supplied RGB triple, black elsewhere, no labels |
| Geometry | One-pixel white outer border, TL/TR/BL/BR labels inside the corners |
| Black bars | Neutral 0, 4, 8, 12, 16, 24, 32, 51 |
| White bars | Neutral 204, 230, 242, 250, 255 |
| Primary bars | Red/green/blue in separate frames; active channel 204, 230, 242, 255, other channels zero |
| Detail | Alternating single-pixel red/blue stripes beside black/white stripes; native one-pixel bitmap text below |

## Controller boundary

The [controller](../../tv_autocal/cycle.py) uses concrete simulated devices and the existing in-memory `FakeClock`. It does not accept arbitrary transport callbacks. Baseline, adjustment and normal restoration each go through simulated menu observation, successful menu exit, the configured wait and an attempted meter read. Acknowledgement, observed setting and XYZ result remain separate evidence. A repeat does not reopen a menu, but must honour the configured inter-reading wait.

Event and attempt records retain simulated timestamps, purpose, patch, settings, raw samples and rejection reasons. A failed or cancelled attempt is retained; accepted means eligible within this simulation, not suitable calibration data. A terminal stop prevents further project actions in that controller. The restoration state describes toy state only; it cannot certify any physical restoration.

`read_started_ms` records when polling actually requests the sample; `sample_due_ms` is its scripted availability time; `read_deadline_ms` is the exclusive deadline. The latter two are absent if no read began. A sample due strictly before its deadline may still be accepted when polling occurs later. `completed_ms` records that later observation/finalisation time, not an inferred arrival time. A sample due exactly at the deadline is rejected.

`start_baseline(rgb)` captures the initial toy level and baseline RGB. `measure_change(level, rgb)` requests a new toy value; `repeat()` reuses the last patch and confirmed exit with a fresh wait. `restore()` returns to the original level and baseline RGB through the full cycle. Each call is explicit; `poll()` neither advances the clock nor starts another cycle after completion. `cancel()` stops the session permanently. The next call must respect the public state:

| State | Permitted progression |
|---|---|
| NEW | Start a baseline or cancel |
| WAITING | Poll until the exit-to-read wait has passed, or cancel |
| READING | Poll for the queued synthetic sample or deadline, or cancel |
| READY | Explicit change, repeat, normal restoration or cancel |
| COMPLETE / STOPPED | No further measurement or setting action; polling leaves the result unchanged |

The controller accepts only concrete `FakeClock`, `SimulatedTV` and `SimulatedMeter` objects. `TVStep` scripts command reply, whether the setter applies, menu observation and exit confirmation independently. `MeterSample` supplies literal XYZ, a fake delay and an optional failure. Fixture queues are capped at 256 entries; a controller permits 1–256 attempts (default 16, including baseline/restoration), a positive wait and a read timeout (both at most 3,600,000 ms). Exhausted meter scripts reject the attempt. Reserve enough attempts for restoration; reaching the limit stops rather than adding an unplanned attempt.

Zero and negative finite XYZ may be accepted as synthetic diagnostic data; no black-level or accuracy claim follows. COMPLETE means that the original toy setting was observed, exit/wait succeeded and a finite synthetic reading was returned. It does **not** mean that light returned to a baseline tolerance; no optical model or T-013 acceptance comparison is implemented. `restoration_required` remains conservative after an uncertain setter or detected drift, and clears only after a successful normal restoration cycle. It is separate from the stopped/menu state.

This layer does not reuse T-009's one-request fake as a physical sender. It does not address serial reply correlation, late-byte logging, ArgyllCMS serial discovery or concurrent meter/Ex-Link isolation (C-090/C-091). Those remain requirements for a later adapter and sender.

## Run without equipment

From the repository root, with an existing Python interpreter:

```text
py -3.15 -B -m tv_autocal.demo
py -3.15 -B -m unittest discover -s tests -v
```

Those commands use the tested Windows Python launcher. With another existing interpreter, replace `py -3.15` with that interpreter's invocation; no installation is part of these instructions. The author also tested the installed Python 3.12.14 runtime using its private local path. Production support beyond the two tested runtimes remains undecided.

The [demo](../../tv_autocal/demo.py) prints a JSON report with buffer metadata, the visual manifest and three explicitly synthetic baseline/change/restoration readings. It rejects all arguments, including output-file, port and real-mode options. It displays no image and creates no file. The sample values are literals chosen to exercise the flow; they are not a model, prediction or measurement of the owner's TV.

The test runner creates and removes inert source files in a temporary directory for T-009's existing recursive-inspection regression; those files are never imported. `-B` prevents bytecode files. All new functional suites also run with file/device opens, network calls and process launches guarded. Static inspection uses explicit import permissions per application module. These checks supplement source review and absence of physical backends; they are not a general security boundary.

## Manual verification — 27 October 2026

| Run | Interpreter | Passed | Failed | Errors | Skipped | Unrun |
|---|---|---:|---:|---:|---:|---:|
| Complete suite, recorded files below | Python 3.12.14 | 87 | 0 | 0 | 0 | 0 |
| Same files | Python 3.15.0 | 87 | 0 | 0 | 0 | 0 |

The 87 distinct top-level tests comprise 39 T-009 tests, 11 renderer tests, 34 cycle tests, two composition/demo tests and one new guarded-suite test. Guards re-execute 35 existing protocol cases and 47 new functional cases; those are not additional distinct tests. Complete runs used normal local temporary-directory permissions for the inherited inert-file regression. No dependency was installed or hardware accessed.

Checks cover every native patch/surround byte against literal row boundaries, exact visual levels and one-pixel stripes, immutable records, strict input validation before mutation, baseline failure, acknowledged-but-unapplied changes, wrong menu values, exit failures, wait/read boundaries, cancellation, exhausted scripts, malformed/non-finite samples, attempt limits and restoration failures. Internal source review identified and corrected restoration using the most recent rather than baseline patch, and a missing restoration flag after detected baseline-state drift; both have regression coverage. Same-vendor checks are not independent review.

The text-only module command was also run successfully on Python 3.12.14: three synthetic readings, toy level 50→49→50, final state COMPLETE and 6,000 fake milliseconds. No image was displayed. The gray-128 native buffer's SHA-256 was `ec5fdc9c0deba9f98fcdc9019e9a373047830a2fb62661547ff6cc75a92d897b`. This identifies software bytes only.

The current tested source hashes below avoid a self-referential commit hash. The containing PR identifies the full tree; later source changes require a new verification record. The [T-009 record](t009-prototype.md) retains its separately identified historical PR #21 hashes.

| File | SHA-256 |
|---|---|
| `tv_autocal/__init__.py` | `02a4bc365fe39e9bcb75a8dc978d04ae87a249fd33d9ecda252cae1cc1ab651d` |
| `tv_autocal/exlink.py` | `d55c4ac872e95c02dd5a379e68ea4a4d7661dab63e57dd5769560f779c423596` |
| `tv_autocal/simulation.py` | `bd84b7e1b597156af4ce2952fc6f2e3cfa2094d6fba1ef4e0a639406e94b69d8` |
| `tv_autocal/renderer.py` | `1eaadc72e2785c3d7d96980a979469c9f26788f8a0d938ad19e5c8bc142f518f` |
| `tv_autocal/cycle.py` | `bbe84b015115319e6c7eb4add5351a073d7bc75f43c4f040577514a27b0847f9` |
| `tv_autocal/demo.py` | `0dd82febfe3489b9ecf964377739a0643d6aa223f0d34361a87a5b5df5dd4fce` |
| `tests/test_t009.py` | `67f086ad539e29c166ab51f46067503c43ef1839ff15148fe98234b15af08bae` |
| `tests/test_renderer.py` | `9df6b56ef3ede15ba6b3c88c95178e97ef2ca26a7ac9a93288b7c7be5278bbab` |
| `tests/test_cycle.py` | `5dc6e067751fd6912704a3db8060acde58669920f16daf8954bce404132c943c` |
| `tests/test_renderer_cycle_integration.py` | `102cff513e480922646a3d0b88933cc37888e5c30aea76e0fa50ee142c9a76d9` |
| `tests/test_software_containment.py` | `8e1eefdea704dc7c810ecc427deca60c305ec63041e371d24401669c8deacc14` |

## Independent review and remaining work

Review is needed from Claude Code (Anthropic) or Antigravity (Google); same-vendor assistance is not independent review. Review should check literal pixel values and geometry, failure transitions, cancellation/read deadlines, restoration semantics, complete evidence records and absence of physical I/O routes.

No equipment claim becomes Confirmed. T-003/T-005/T-006 remain unauthorised; electrical compatibility, setting scope (X-012), menu timing, physical sender, correction validation, the stronger signal-range method and T-013/T-008 plans remain open. Full white-balance/colour-control support and calibration accuracy are not demonstrated by these simulations.
