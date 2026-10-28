# Presenter controls and meter-process readiness

**Software-only implementation and fake-boundary verification; no equipment has been operated. All physical plans remain NOT AUTHORISED.** The implementation was independently reviewed and merged in PR #27 at `e424d47171f236add2451129691fc88d855548c3`, with the same tree as reviewed head `e7122a0e510337583d0da2e2a22e9b22c40f812e`. S-053's owner-input reconciliation needs separate review; neither record establishes physical display readiness or a safe way to force-stop an instrument driver.

Prepared by Codex (OpenAI), 28 October 2026, from merged PR #26 (`dc552c737ec61d5b323ceda844fd198785170c61`), under [S-050's request](../briefs/2026-10-28-component-readiness.md). Design and checks are S-051/C-101/T-018; consulted APIs are S-052. The existing [component-tool contracts and current source hashes](component-tools.md) still apply except for the explicit changes below. The renderer, serial sender, allowlists, patch geometry and diagnostic reading limits are unchanged.

## Presenter control choice

The previous presenter accepted C, Space and Right while the TV window had focus. Typing a meter command into that window could confirm the target or advance a pattern. This version separates the unchanged TV image from a visible, decorated operator window with mouse-operated **Confirm TV target**, **Next pattern** and **Stop presentation** buttons. Ordinary text, Space, Return and navigation keys cannot activate those controls or advance the TV. Escape and either window's close request stop the presenter.

This is a deliberate two-display proposal. Physical presentation additionally requires explicit `--control-x` and `--control-y`, as well as the existing TV `--x` and `--y`. The control window must fit wholly within the usable area of a different monitor and outside the TV rectangle. The native adapter checks actual outer window bounds, including decorations, alongside the TV's exact client geometry. It does not enumerate, select or rearrange displays. Invalid placement stops rather than moving or scaling either window. Actual coordinates and their collection method remain unresolved inputs.

The owner first identifies the intended TV, single-clicks Confirm TV target, then single-clicks Next pattern once. The meter is mounted only after target confirmation. Confirm alone does not apply a measurement patch; receipts still require a successfully applied frame. Next is disabled during frame application and for one second afterwards; the controller also rejects Next actions during that interval. This proposed software guard prevents rapid repeated actions from skipping an item; it is not a measured Windows double-click threshold or a settling-time rule. Wait until Next is enabled before any later authorised advance. No timer advances anything. Stop and Escape remain available during the guard, subject to the event loop processing their input. The existing 60-second visual-pattern and three-hour lifetime limits remain. A stop from either window is available without reacquiring keyboard focus on the TV, but native visibility and accessibility remain untested. No global keyboard hook or explicit focus-setting call is added. Native window mapping may change focus; the owner must still check the meter console before typing. No always-on-top promise is made.

The control window remains 440×220 physical pixels. Its requested layout must fit the client area before the TV window is shown, after confirmation changes the instructions, and during later geometry checks. Oversized text or controls fail closed; there is no font shrinking or automatic resizing fallback. This checks the toolkit's layout request, not actual font rendering or legibility. The operator display's scaling setting remains an explicit input in the shared display record.

Do not move or minimise the operator window during a run, including through its minimise/taskbar button or Win+D/Win+M. If that happens, stop and abandon the run. The geometry watchdog closes on invalid bounds, but a move wholly inside the allowed work area need not trigger it. Minimized-window coordinates and native closure remain untested, so do not rely on automatic closure to enforce this operator rule.

Keyboard focus on the meter console must still be checked before typing its command. An unintended confirmation, advance or closure remains a stop. Plain typing into the presenter now has no pattern-control effect, but this does not prove absence of overlays, correct HDMI values or successful focus transfer on the owner's setup. A geometry watchdog can react only after a change is observable; it cannot prove the image was never briefly obstructed.

## Presenter failure and closure

Controller callbacks, the Tk callback-exception hook and the event loop route exceptions and Python interrupts to a terminal failure. Both windows receive best-effort closure, and the original failure is propagated so the CLI cannot report an ordinary successful run. This includes a KeyboardInterrupt arriving inside the geometry watchdog, where Tk's normal exception reporting could otherwise leave an open window without a rescheduled check.

The planned-close rules in the [shared execution procedure](../tests/component-execution.md#display-and-console-arrangement) remain: the allowed reason must match the owner's intended action after all required steps and evidence checks. A timeout, interrupt or accidental close is never a successful boundary. `presenter_closed.fields.close_completed` must be true for a planned close; false or absent stops the plan. This records return from the close calls, not proof of native window disappearance, which still needs owner observation. Forced console closure, process termination, a stuck native API and OS failure remain outside the software guarantee. Presenter-console Ctrl+C is an abandonment/failure path, not the planned Stop action or a tested recovery method.

## Meter-process choice

The meter keeps its existing no-kill policy because the consulted Argyll driver warning C-069 does not establish that aborting a stalled driver is safe. It still launches only the reviewed one-attempt argument list, with a separate process group, no window, no interactive stdin and two prestarted readers. It never sends an interrupt, termination request, reset, retry or second reading to the child.

A main-thread SIGINT handler now latches cancellation throughout the attached-child lifetime: launch/attachment, supervision, reader completion and pipe cleanup. It performs no logging or locking inside the signal handler. Normal supervision rejects the attempt and continues retaining bounded late output until actual child exit and reader completion. Repeated cancellation cannot deliberately turn into a force-kill. A cancellation observed during cleanup still invalidates the result; handler registration failure occurs before any child launch. The previous handler is restored after supervision finishes.

Private output and journal evidence distinguish `wrapper_pid` from `child_pid`, plus `child_exit_confirmed` and `readers_complete`. A child exit can precede completion of its output readers. These fields complement, rather than replace, `capture_complete`, `log_complete`, timeout/cancellation, exit status and dropped-byte counts. Process IDs are observations for this one lifetime, not durable identities or permission to target a process later. No global process enumeration or PID-based termination is added.

An indefinitely outstanding child still has no guaranteed finish time. Closing the wrapper console externally can leave child lifetime and output uncertain (C-100). Ctrl+Break is also unsupported: Python identifies it as SIGBREAK on Windows, while this wrapper handles SIGINT only. It must not be used as a cancellation or recovery command; wrapper supervision and closure evidence could be lost. No exact native wrapper/child outcome is claimed. The owner can stop at any time, but exact console/cable handling and any forced interruption need their own reviewed procedure before physical authorisation. This PR improves supervision and reporting; it does not close that equipment gate.

## Offline verification

The complete suite was run manually on 28 October 2026 using each interpreter with `-B -m unittest discover -s tests`, against the [current 34-file SHA-256 manifest](component-tools.md#offline-verification).

| Interpreter | Passed | Failures | Errors | Skipped | Unrun |
|---|---:|---:|---:|---:|---:|
| Python 3.12.14 | 287 | 0 | 0 | 0 | 0 |
| Python 3.15.0 | 287 | 0 | 0 | 0 | 0 |

The Windows test-runner builds identify as `3.12.14 (main, Aug 25 2026, 14:01:42) [MSC v.1944 64 bit (AMD64)]` and `3.15.0 (tags/v3.15.0:d220409, Oct 9 2026, 11:55:56) [MSC v.1951 64 bit (AMD64)]`. Private interpreter paths are not committed. These runs do not bind or validate the interpreter/dependencies chosen for a future physical session.

There are 35 additional distinct tests over the 252-test baseline: 25 presenter, eight meter and two CLI cases. The 149 inherited tests remain unchanged; the component slice now has 15 entry, 36 meter, 44 presenter, 12 receipt, 29 serial and two containment tests. The containment rerun covers all 136 component functional cases with real file/process/network/native operations and real signal-handler registration forbidden.

Initial runs of the earlier 277-case snapshot each reported 276 passes and one error in the unchanged T-009 temporary-text fixture because the sandbox denied temporary-directory access. Final runs used normal local temporary-directory permissions; no test was skipped or weakened. Internal QA also found two inherited meter tests installing a real Python SIGINT handler. All meter tests now substitute that registration, and the strengthened containment guard rejects real registration. No signal was sent to any process.

Tests use fake Tk/native geometry, processes, signals, streams and clocks. No real windows, meter executable, hardware-mode command, display/device enumeration or equipment operation occurred. No dependency was installed.

The full suite includes the unchanged renderer's exact **960×540 at x=1440, y=810 on 3840×2160: 6.25% area** checks. New regression cases target accidental typing, control placement, callback interrupts, closure failures, repeated meter cancellation and separate process/reader completion. The nine additional cases since the initial 278-test readiness revision cover rapid/reentrant Next actions, final-frame closure, Stop/Escape during the guard or frame application, guard callback failure and layout overflow before mapping, after confirmation and during later checks. Containment checks rerun component cases with real I/O boundaries forbidden; these reruns are not additional distinct tests.

## Sources consulted

Codex (OpenAI) consulted these primary sources on 28 October 2026, without executing examples or installing libraries:

- Python [signal](https://docs.python.org/3.12/library/signal.html): handlers run in the main interpreter thread and may be delayed; the main thread installs them. SIGBREAK identifies Ctrl+Break on Windows, separately from SIGINT/Ctrl+C. The 3.12 documentation currently identifies itself as 3.12.16; the separately recorded test interpreter versions are not inferred from it.
- Python [subprocess](https://docs.python.org/3.12/library/subprocess.html): process status and separate output pipes; a timeout is not proof of termination. The default `run(timeout=...)` kill policy is unsuitable for this driver's unresolved abort behaviour.
- CPython [Tkinter at v3.12.14](https://github.com/python/cpython/blob/v3.12.14/Lib/tkinter/__init__.py): `CallWrapper.__call__` reports callback exceptions through the widget hook and re-raises SystemExit. The adapter's explicit failure path avoids relying on default reporting as closure.
- Tcl/Tk [bind, 8.6](https://www.tcl-lang.org/man/tcl8.6/TkCmd/bind.htm): widget bindings precede class bindings; returning `break` prevents later key handlers from activating a button.
- Tcl/Tk [button.tcl, core-8-6-branch](https://github.com/tcltk/tk/blob/core-8-6-branch/library/button.tcl), consulted 28 October 2026: Button press/release class bindings invoke enabled buttons without a separate double-click guard. The added Next interval is a Codex design policy, not a Tk or equipment timing result.
- Tcl/Tk [winfo manual source, core-8-6-branch](https://github.com/tcltk/tk/blob/core-8-6-branch/doc/winfo.n), consulted 28 October 2026: requested width/height describe geometry-manager needs in pixels; actual width/height are separate. The fit check compares these after initial layout and confirmation updates, without establishing native font rendering.
- Microsoft [GetAncestor](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getancestor) (`GA_ROOT`, page updated 2024-11-27) and [GetWindowRect](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getwindowrect) (page updated 2025-04-11): outer screen coordinates, parent-window traversal and DPI caveats. Existing S-046 covers per-monitor DPI awareness and associated-monitor checks.

API descriptions and source inspection are not equipment results. No new dependency is added; existing licences and open Q-002/Q-003 decisions remain in [component-tools.md](component-tools.md).

## What remains before physical use

The owner supplied the intended second-display arrangement in [S-053](../briefs/2026-10-28-owner-readiness-inputs.md): primary Samsung above LG, both 4K at 300% scaling, extended desktop, LG via DisplayPort. It is planned, not connected or verified. Controls may not fit the fixed window at that scaling; no successful native launch is claimed. Coordinate acquisition, console visibility/focus checks, exact local runtime identities and actual window closure still require the [execution record](../tests/component-execution.md). The source manifest must be bound to the final reviewed plan revision; old PR #26 instructions alone do not cover this interface. T-003 discovery-only is first and uses no presenter. T-006 electrical, scope/restoration and timing questions, T-005 range interpretation, correction validation and meter/serial coexistence are unaffected.
