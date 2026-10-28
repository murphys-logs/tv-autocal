# Presenter controls and meter-process readiness

**Software-only implementation and fake-boundary verification; no equipment has been operated. All physical plans remain NOT AUTHORISED.** This follow-up needs independent review before the owner considers merging it. It does not supply missing display coordinates, confirm a second screen, or establish a safe way to force-stop an instrument driver.

Prepared by Codex (OpenAI), 28 October 2026, from merged PR #26 (`dc552c737ec61d5b323ceda844fd198785170c61`), under [S-050's request](../briefs/2026-10-28-component-readiness.md). Design and checks are S-051/C-101/T-018; consulted APIs are S-052. The existing [component-tool contracts and current source hashes](component-tools.md) still apply except for the explicit changes below. The renderer, serial sender, allowlists, patch geometry and diagnostic reading limits are unchanged.

## Presenter control choice

The previous presenter accepted C, Space and Right while the TV window had focus. Typing a meter command into that window could confirm the target or advance a pattern. This version separates the unchanged TV image from a visible, decorated operator window with mouse-operated **Confirm TV target**, **Next pattern** and **Stop presentation** buttons. Ordinary text, Space, Return and navigation keys cannot activate those controls or advance the TV. Escape and either window's close request stop the presenter.

This is a deliberate two-display proposal. Physical presentation additionally requires explicit `--control-x` and `--control-y`, as well as the existing TV `--x` and `--y`. The control window must fit wholly within the usable area of a different monitor and outside the TV rectangle. The native adapter checks actual outer window bounds, including decorations, alongside the TV's exact client geometry. It does not enumerate, select or rearrange displays. Invalid placement stops rather than moving or scaling either window. Actual coordinates and their collection method remain unresolved inputs.

The owner first identifies the intended TV, clicks Confirm TV target, then clicks Next pattern once. The meter is mounted only after target confirmation. Confirm alone does not apply a measurement patch; receipts still require a successfully applied frame. Next advances exactly one item; no timer advances anything. The existing 60-second visual-pattern and three-hour lifetime limits remain. A stop from either window is available without reacquiring keyboard focus on the TV, but native visibility and accessibility remain untested. No global keyboard hook or explicit focus-setting call is added. Native window mapping may change focus; the owner must still check the meter console before typing. No always-on-top promise is made.

Keyboard focus on the meter console must still be checked before typing its command. An unintended confirmation, advance or closure remains a stop. Plain typing into the presenter now has no pattern-control effect, but this does not prove absence of overlays, correct HDMI values or successful focus transfer on the owner's setup. A geometry watchdog can react only after a change is observable; it cannot prove the image was never briefly obstructed.

## Presenter failure and closure

Controller callbacks, the Tk callback-exception hook and the event loop route exceptions and Python interrupts to a terminal failure. Both windows receive best-effort closure, and the original failure is propagated so the CLI cannot report an ordinary successful run. This includes a KeyboardInterrupt arriving inside the geometry watchdog, where Tk's normal exception reporting could otherwise leave an open window without a rescheduled check.

The planned-close rules in the [shared execution procedure](../tests/component-execution.md#display-and-console-arrangement) remain: the allowed reason must match the owner's intended action after all required steps and evidence checks. A timeout, interrupt or accidental close is never a successful boundary. `presenter_closed.fields.close_completed` must be true for a planned close; false or absent stops the plan. This records return from the close calls, not proof of native window disappearance, which still needs owner observation. Forced console closure, process termination, a stuck native API and OS failure remain outside the software guarantee. Presenter-console Ctrl+C is an abandonment/failure path, not the planned Stop action or a tested recovery method.

## Meter-process choice

The meter keeps its existing no-kill policy because the consulted Argyll driver warning C-069 does not establish that aborting a stalled driver is safe. It still launches only the reviewed one-attempt argument list, with a separate process group, no window, no interactive stdin and two prestarted readers. It never sends an interrupt, termination request, reset, retry or second reading to the child.

A main-thread SIGINT handler now latches cancellation throughout the attached-child lifetime: launch/attachment, supervision, reader completion and pipe cleanup. It performs no logging or locking inside the signal handler. Normal supervision rejects the attempt and continues retaining bounded late output until actual child exit and reader completion. Repeated cancellation cannot deliberately turn into a force-kill. A cancellation observed during cleanup still invalidates the result; handler registration failure occurs before any child launch. The previous handler is restored after supervision finishes.

Private output and journal evidence distinguish `wrapper_pid` from `child_pid`, plus `child_exit_confirmed` and `readers_complete`. A child exit can precede completion of its output readers. These fields complement, rather than replace, `capture_complete`, `log_complete`, timeout/cancellation, exit status and dropped-byte counts. Process IDs are observations for this one lifetime, not durable identities or permission to target a process later. No global process enumeration or PID-based termination is added.

An indefinitely outstanding child still has no guaranteed finish time. Closing the wrapper console externally can leave child lifetime and output uncertain (C-100). The owner can stop at any time, but exact console/cable handling and any forced interruption need their own reviewed procedure before physical authorisation. This PR improves supervision and reporting; it does not close that equipment gate.

## Offline verification

The complete suite was run manually on 28 October 2026 using each interpreter with `-B -m unittest discover -s tests`, against the [current 34-file SHA-256 manifest](component-tools.md#offline-verification).

| Interpreter | Passed | Failures | Errors | Skipped | Unrun |
|---|---:|---:|---:|---:|---:|
| Python 3.12.14 | 278 | 0 | 0 | 0 | 0 |
| Python 3.15.0 | 278 | 0 | 0 | 0 | 0 |

The Windows test-runner builds identify as `3.12.14 (main, Aug 25 2026, 14:01:42) [MSC v.1944 64 bit (AMD64)]` and `3.15.0 (tags/v3.15.0:d220409, Oct 9 2026, 11:55:56) [MSC v.1951 64 bit (AMD64)]`. Private interpreter paths are not committed. These runs do not bind or validate the interpreter/dependencies chosen for a future physical session.

There are 26 additional distinct tests over the 252-test baseline: 16 presenter, eight meter and two CLI cases. The 149 inherited tests remain unchanged; the component slice now has 15 entry, 36 meter, 35 presenter, 12 receipt, 29 serial and two containment tests. The containment rerun covers all 127 component functional cases with real file/process/network/native operations and real signal-handler registration forbidden.

Initial runs of the earlier 277-case snapshot each reported 276 passes and one error in the unchanged T-009 temporary-text fixture because the sandbox denied temporary-directory access. Final runs used normal local temporary-directory permissions; no test was skipped or weakened. Internal QA also found two inherited meter tests installing a real Python SIGINT handler. All meter tests now substitute that registration, and the strengthened containment guard rejects real registration. No signal was sent to any process.

Tests use fake Tk/native geometry, processes, signals, streams and clocks. No real windows, meter executable, hardware-mode command, display/device enumeration or equipment operation occurred. No dependency was installed.

The full suite includes the unchanged renderer's exact **960×540 at x=1440, y=810 on 3840×2160: 6.25% area** checks. New regression cases target accidental typing, control placement, callback interrupts, closure failures, repeated meter cancellation and separate process/reader completion. Containment checks rerun component cases with real I/O boundaries forbidden; these reruns are not additional distinct tests.

## Sources consulted

Codex (OpenAI) consulted these primary sources on 28 October 2026, without executing examples or installing libraries:

- Python [signal](https://docs.python.org/3.12/library/signal.html): handlers run in the main interpreter thread and may be delayed; the main thread installs them. The 3.12 documentation currently identifies itself as 3.12.16; the separately recorded test interpreter versions are not inferred from it.
- Python [subprocess](https://docs.python.org/3.12/library/subprocess.html): process status and separate output pipes; a timeout is not proof of termination. The default `run(timeout=...)` kill policy is unsuitable for this driver's unresolved abort behaviour.
- CPython [Tkinter at v3.12.14](https://github.com/python/cpython/blob/v3.12.14/Lib/tkinter/__init__.py): `CallWrapper.__call__` reports callback exceptions through the widget hook and re-raises SystemExit. The adapter's explicit failure path avoids relying on default reporting as closure.
- Tcl/Tk [bind, 8.6](https://www.tcl-lang.org/man/tcl8.6/TkCmd/bind.htm): widget bindings precede class bindings; returning `break` prevents later key handlers from activating a button.
- Microsoft [GetAncestor](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getancestor) (`GA_ROOT`, page updated 2024-11-27) and [GetWindowRect](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getwindowrect) (page updated 2025-04-11): outer screen coordinates, parent-window traversal and DPI caveats. Existing S-046 covers per-monitor DPI awareness and associated-monitor checks.

API descriptions and source inspection are not equipment results. No new dependency is added; existing licences and open Q-002/Q-003 decisions remain in [component-tools.md](component-tools.md).

## What remains before physical use

The owner must confirm the intended second-display arrangement. Coordinate acquisition, console visibility/focus checks, local interpreter/dependency/binary identities, and actual window closure still require the reviewed execution record. The new source manifest must be bound to the final reviewed plan revision; old PR #26 launch instructions alone do not cover this changed interface. T-006 electrical, scope/restoration and timing questions, T-005 range interpretation, correction validation and meter/serial coexistence are unaffected.
