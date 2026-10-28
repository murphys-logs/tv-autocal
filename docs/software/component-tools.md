# Bounded component-test tools

**Hardware-facing code is present, but it has not been operated or validated on equipment. Every physical plan remains NOT AUTHORISED.** The default command is an in-memory simulation. Actual windows, meter processes and serial ports require explicit owner opt-in after a separately reviewed, specifically authorised plan. The owner's request to build these tools is not that authorisation.

Prepared by Codex (OpenAI), 27 October 2026, from merged PR #23 (`a90258addad8791be0de1e2246e69db14e1bc9f4`), under the [verbatim request](../briefs/2026-10-27-bounded-component-tools.md), S-044. Implementation and offline verification are S-045/C-096/T-017. API and licence references are S-046/C-097. The 28 October [readiness follow-up](component-readiness.md), S-051/C-101/T-018, updates presenter controls, interruption handling and meter supervision; its source changes need independent review. These tools collect component evidence; they are not an optimiser, a complete automated test schedule or a calibration application.

## What changed and why

The reviewed `tv_autocal` package remains byte-for-byte unchanged. New `tv_autocal_tools` entry points keep effects separate from the original pure software contracts. A Windows window, an Argyll process and a serial port are three separate manual tools. There is no combined meter/serial mode: C-090's startup-probing risk remains unresolved, and physical disconnection remains the meter plan's prerequisite.

| Choice | Reason and limit |
|---|---|
| Source-run Python tools, provisionally Python 3.12+ | Reuses the current tests and renderer; no installer or packaging framework added. Q-003 remains an owner decision for production. Available interpreter versions are test environments, not a production-support promise. |
| Tkinter with native Windows geometry checks | Provides a small manual presenter using unchanged RGB buffers. Tk is optional; its availability and real DPI/colour behaviour were not checked. No profile, LUT, range or display mode is changed. |
| `subprocess.Popen` with two prestarted stream readers | Allows bounded stdout/stderr draining and supervision after a timeout without the automatic kill performed by `subprocess.run(timeout=...)`. No shell, arbitrary argument string or automatic retry. |
| Optional, pinned pySerial 3.5 | Avoids hand-written serial driver bindings. It is loaded only for explicitly armed serial use; never imported or installed for offline checks. No URL transport or port scan. |
| Separate, exclusive private journals | Command intentions are flushed before effects, raw evidence is recorded separately from acceptance, and log errors stop acceptance/writes. Logs stay under ignored `local/`; nothing is uploaded. |
| Owner attestations and concrete evidence references | Software can validate scope and syntax, not authenticate an authorisation or establish electrical safety. The operator must first satisfy the reviewed plan and keep its exact authorisation. |

Python is PSF-licensed, Tcl/Tk uses its permissive notice-retention licence, and pySerial 3.5 uses BSD-3-Clause. [requirements-hardware.txt](../../requirements-hardware.txt) records the optional pin; it does not install anything. Argyll remains the owner's existing external executable, with no binary or source archive bundled. Project licensing Q-002 remains open before distribution.

## Default simulation and explicit entry points

The following command is hardware-free and creates no files:

```text
py -3.15 -B -m tv_autocal_tools
```

It prints an authored patch/transcript example and explicitly reports that the hardware adapters were not exercised. `simulate`, or `present`, `meter`, or `serial` without `--hardware`, also use this in-memory example; supplying permit/confirmation/log options without `--hardware` instead rejects the incomplete opt-in. Help prints argument documentation without loading Tk, pySerial or a native window library. Simulation does not demonstrate driver, GUI, serial or instrument operation.

All hardware commands require **all** of `--hardware`, `--permit` pointing to a private JSON file, an exact `--confirm "RUN <plan> <full-reviewed-plan-commit>"` phrase, and `--log` pointing to a fresh private journal. For example, use `local/<plan>/authorisation.json` and `local/<plan>/<name>.log`; these common paths must stay inside the checkout's `local/` directory but need not have that particular subdirectory. The permit contains exactly `plan`, `revision`, `authorisation`, `steps`, `evidence`, and `actions`. `authorisation` is the owner's dated verbatim permission for the specified steps; `evidence` identifies the closed prerequisite records. `actions` is a list drawn from `present`/`meter` for T-003/T-005, or `serial` for T-006. T-008/T-013 are unsupported. There is no ready-to-run permit in the repository.

The permit is an **attestation**, not a way to grant permission. Copying this build request into it, or inventing prerequisite evidence, would not authorise operation. Before use, amend the physical plan with the reviewed tool source hashes, launch options, exact dependency versions, display/port identification, timing and closure procedures, then obtain and archive the owner's specific authorisation. Existing unamended plans must not be treated as executable merely because this PR merges.

Journals contain a sequential event number, UTC time, monotonic time and event fields. The CLI records the plan/authorisation and hashes of application/tool Python sources. It uses exclusive creation, rejects paths outside this checkout's `local/`, reserved device names and alternate data streams, flushes and syncs each event, and reserves a final closure record within an 8 MiB limit. Overflow or write failure is terminal. `journal-close.complete` describes journal integrity, not successful equipment operation; outcome/abort events are separate. These are ordinary local-file checks, not protection against hostile concurrent filesystem replacement.

## Manual presenter

Future entry point: `present --hardware` with the common authorisation options, explicit nonnegative TV `--x`/`--y`, separate operator-window `--control-x`/`--control-y` desktop coordinates, and `--sequence patch|t003|t005-visual|t005-optical`. The operator window must fit wholly on a different monitor outside the TV rectangle; no single-screen fallback is supplied. `patch` additionally accepts `--rgb R,G,B`. No display is enumerated or automatically selected. Negative desktop origins are unsupported in this slice; do not rearrange a physical setup to fit the tool without a reviewed amendment.

The initial screen contains confirmation instructions, not a measurement patch. The owner single-clicks **Confirm TV target** in the visible operator window, then single-clicks **Next pattern** for each item. Next is disabled while applying a frame and for one second afterwards; repeated Next actions during that interval are ignored. This is an input guard, not a settling-time rule. Ordinary typing, Space, Return and navigation keys do not activate either action. **Stop presentation**, Escape or closing either window requests closure without waiting for the Next guard to expire. Button activation is mouse-only; keyboard focus on the TV is unnecessary for the operator-window buttons. No timer advances patterns. The `t003` sequence includes grey 128, the six planned range patches, then grey 128; the owner holds the initial grey through the planned warm-up/read blocks. `t005-visual` uses the existing seven-pattern manifest; `t005-optical` brackets the neutral and primary sequences with the planned grey references. These are manual playlists, not automatic reading schedules. No readings may be taken from an ineligible low-light patch in T-005 merely because it appears in the playlist.

The hardware entry point restricts colours/patterns to its plan: T-003's seven neutral values; T-005's reviewed neutral values, high primary values and visual patterns. It retains **960×540 at x=1440…2399, y=810…1349 on 3840×2160: exactly centred, 6.25% area**. The original renderer and its geometry tests are untouched. Patches contain no text.

Before Tk creates a window, the backend establishes and verifies per-monitor V2 DPI awareness. It checks the TV window's client rectangle and its associated monitor rectangle against the exact supplied 3840×2160 location, before each frame and every 200 ms. It also checks the operator window's actual outer bounds against the usable area of a different monitor and rejects overlap with the TV. Its requested control layout must fit the fixed client area, including after confirmation changes its text; overflow fails before presenting a pattern. It does not enumerate monitors. A mismatch closes the window; there is no scaling fallback. Raw PPM pixels use gamma 1.0 with no resampling requested. Intent/hash is journaled before painting, and application to the window is recorded afterwards. These checks do not prove HDMI code values, actual light, freedom from occlusion, Windows colour transforms or absence of TV overlays.

Named visual patterns close after 60 seconds without manual advance; a stale timer cannot close a later pattern. A proposed three-hour session cap closes the window and ends the run, never restarts it. Both limits and the exact GUI build need physical-plan review. The owner must keep the measurement patch unobstructed and unchanged throughout a meter attempt, including an outstanding process after timeout. Focus changes alone do not close it because the owner needs to use the separate meter console. Python interrupts and callback failures take the terminal failure/closure path described in the [readiness design](component-readiness.md#presenter-failure-and-closure); forced OS closure or successful native destruction is not guaranteed.

### T-005 visual run boundaries

The existing `t005-visual` sequence ends after the detail pattern; it does not return to grey 128, and advancing again closes the window. T-005 V4 therefore needs separate presenter runs. PR #26 records these three runs; the readiness amendment updates their controls and launch options. Their separate journals and planned closure evidence remain required before any authorisation:

1. Use `t005-visual` for V2's geometry check and the six V3 patterns in the original recorded Denon mode, then close normally. A failed check stops the plan; this is not permission to restart after a failure.
2. Use `patch` with RGB `(128,128,128)`. Confirm and advance once, then hold that grey patch while the owner performs V4's authorised Bypass change, menu exit and wait. Do not advance past grey or change the receiver while the presenter is closed. Record completion before closing this run normally.
3. Use `t005-visual` in the recorded Bypass state, then close normally. This existing playlist starts with geometry, so the amendment must explicitly include and record that repeated geometry check, followed by exactly one repetition of the six V3 patterns. Each visual item keeps the 60-second limit and manual advance.

These are documented launch details with readiness changes pending review, not authorised physical steps. No new playlist, pattern or allowlist entry is added. No meter attempt may span a presenter closure or transition between these runs; any later optical attempt needs its own held patch and current receipt. T-005's original-state and restoration requirements still apply across the runs.

### Display arrangement to confirm

**Partly answered (Q-019/C-098):** the owner can, and probably will, connect a second screen (S-047). Actual use, connection, layout and console placement remain unconfirmed. The [execution amendment](../tests/component-execution.md#display-and-console-arrangement) proposes consoles on that second screen, with exact setup/restoration details still required before authorisation. No additional display has been connected or inspected during this work.

The reviewed procedure must explain how the owner launches and observes each meter attempt while keeping the TV image unobstructed, including while a rejected process remains outstanding. The readiness implementation requires a separate display for its operator window; if the TV is the only display, presentation remains blocked. This proposal does not confirm a second display or authorise connecting/rearranging one. No display enumeration or physical setup check has been performed.

## One meter attempt

Future entry point: `meter --hardware` with common options, `--executable` (drive-absolute `spotread.exe`), a reviewed lowercase `--sha256`, fresh `--attempt-log local/<plan>/<name>.log`, `--purpose`, `--presentation-log`, `--presentation-sequence`, and `--rgb`. It also requires explicit `--isolated`, `--exit-confirmed`, and `--discovery-confirmed` attestations. These mean both Ex-Link ends are disconnected and no other non-meter serial device/tool is involved; the selected patch is stable with menus exited; and prior authorised discovery identified the expected V3.5.0 Spyder5/default generic non-refresh configuration unambiguously. **The wrapper performs no separate discovery/help step. Each launched Argyll child still uses startup discovery that may probe ports (C-090); isolation remains required for every attempt.**

T-003 purposes are `initial-access`, `warmup-30`, `warmup-35`, `warmup-40`, `range`, `end-check`. T-005 purposes are `initial-reference`, `neutral`, `middle-reference`, `primary`, `end-check`. The CLI checks that the purpose's RGB matches the plan: grey 128 for references/warm-up, the stated neutral range or the stated high primary values for other purposes. The owner records remaining setup/warm-up/eligibility observations in the plan's private record. The runner performs one attempt, not a 51/81-attempt schedule, and cannot authorise a subsequent attempt or recovery after failure.

The executable is checked by bounded file reading against the supplied hash. The only launched argument list is the existing plan's `spotread.exe -O -e -x -Y n <fresh-attempt.log>`, with no shell, inherited interactive stdin or extra switches. The native attempt file is distinct from the evidence journal and must be fresh. Argyll owns that separate file; the wrapper does not impose a size limit on it. Both correction-environment defaults are removed from a **copy** of the parent's environment, case-insensitively; parent/user/machine configuration is untouched. A new 2,000 ms wait precedes every launch. `--wait-ms` permits a longer reviewed wait up to 60,000 ms; `--timeout-ms` can shorten, but not exceed, the plan's 60,000 ms deadline. These remain proposed test policies, not measured settling times.

Two reader resources are established before spawning, preventing a thread-start failure from leaving a child with an unread pipe. Each stream retains at most 65,536 bytes; output is logged in bounded chunks. Overflow preserves the retained prefix and omitted-byte counts, marks the capture incomplete, and continues draining. Missing EOF, stream errors, log failure, nonzero exit, stderr, wrong format, unsupported output, timeout or cancellation prevents acceptance. The reused pure parser is a grammar check only: physical records have explicit physical provenance, while unit fixtures remain synthetic. Even an accepted result is diagnostic, never calibration data.

The deadline is exclusive. Unlike the previous one-attempt fixture, capture continues after either timeout or cancellation, so call order cannot discard later transcript bytes. The runner announces rejection/outstanding state and remains attached until process exit and pipe EOF. It never kills, resets, retries or starts another reading. This deliberately has no guaranteed shutdown time if the driver stalls. Closing the console or ending the process is an owner-directed interruption with possible driver consequences, not a recovery supplied by this tool. A failed capture/unknown process state must be reviewed before further operation. The readiness follow-up latches SIGINT across launch, supervision and cleanup without forwarding it to the child. Private lifecycle records distinguish wrapper/child PIDs, confirmed child exit and completed readers; these are separate from capture/log completeness. Native signal delivery and forced-console-close behaviour remain untested.

The CLI reads the presenter's bounded journal before launch and after exit, requiring matching plan/revision, applied sequence, RGB and frame hash. Every RGB intent's hash is checked against SHA-256 of the unchanged renderer's native patch pixels; a well-formed but wrong hash is rejected. A logged change, closure, incomplete write or mismatched receipt rejects the attempt while retaining its raw meter evidence. This does not prove the presenter is still alive, visible or unobscured: an uncleanly terminated process may leave an apparently active log. Owner observation and the stable-patch attestation remain necessary; there is no cross-process frame lock or automatic overlay detector.

## One bounded Ex-Link session

Future entry point: `serial --hardware` with common options, one explicit `--port COM...`, `--prerequisites-confirmed` and mandatory `--menu-window-ms` from the reviewed menu-timing amendment. No guessed timeout can fill that field. The attestation covers actual cable/TV electrical compatibility, setting scope/restoration, owner presence and all measurement/discovery programs remaining closed. The code cannot establish those facts.

The lazy backend requires pySerial 3.5. It constructs a closed port with 9600 baud, 8N1, no flow control, nonblocking reads and a one-second write timeout; DTR/RTS are set false before open. pySerial documents possible driver/OS line activation on open, so this is not proof of electrically harmless behaviour. No port URLs, scans, arbitrary bytes, reset buffers, retries, reconnects, power/service commands or automatic restoration are exposed.

The manual sequence is exactly **EXIT → Contrast 94 → EXIT → restore 95 → EXIT**, at most five writes. Keys are `b` (fresh observed baseline 95), `m` (before opening the normal menu), `o` (owner observed the stated expected value), `e` (EXIT), `c` (owner confirmed exit), `d` (set 94), `r` (restore 95), and `q` (close). The successful key order is `b → m,o,e,c → d,m,o,e,c → r,m,o,e,c → q`, with enforced reply/settling phases. Wrong-phase keys do not send. Every send is manual and logged before dispatch.

The serial console accepts only those exact lowercase characters. Python's documented special-key prefix (`\x00` or `\xe0`) and its following keycode are consumed together and ignored, so an arrow/function key cannot become an attestation, send or quit command. Unrecognised characters such as uppercase aliases and Escape are ignored silently; literal `à` has the [known console limitation](#known-console-limitation) below. Ctrl+C uses the existing `KeyboardInterrupt` stop/drain/close handling; no `\x03` character branch is used. Fake-console tests cover the reported Right, End, Insert, PgDn, F8, F9 and F10 sequences across all session phases and repeated command stages.

Menu-opening boundaries precede the owner's opening action, so the later observation cannot reset the automatic-close clock. Every command invalidates the old observation generation; setter and EXIT IDs are paired with the fresh setting/closure attestations. These remain human observations, not hardware readback. A mismatch or uncertain value requires stopping, not pressing the confirmation key.

Proposed policies: initial silence 5,000 ms after completed open; reply deadline 2,000 ms after complete write; post-ACK quiet 500 ms; settling 2,000 ms; final drain 500 ms; total session 120,000 ms. They require review against the actual menu timings before authorisation. ACK is provisional, cannot establish attribution, and does not prove a setting changed. Partial writes, late/duplicate/unsolicited bytes, negative/malformed replies, timing or log failures prohibit all later writes, including restoration commands. Manual ordinary-menu restoration after a stop remains governed by the physical plan.

The same port is retained through observations and idle intervals; receive polling continues while each console read returns promptly. The console limitation below can pause polling and deadline checks. Receive bytes are logged before parsing; another read and deadline check precede each write. The audit has a 65,536 receive-byte/2,048 event limit; overflow becomes explicitly incomplete. Fault/stop paths still drain for the bounded closing interval and attempt OS close. Closure failure is reported. The final read/close boundary cannot guarantee retention of bytes that arrive afterwards, and no quiet interval proves reply correlation. A successful tool result means the bounded sequence and owner attestations completed with logged closure, not that T-006's external scope/electrical requirements passed.

### Known console limitation

**L-4 remains unfixed in code.** A literal `à` (U+00E0) has the same value as the `\xe0` prefix checked by `_WindowsRuntime.key()`. It therefore triggers a second `getwch()` call: if no further key is pending, that read waits; when another key arrives, it is discarded. A single `q` after `à` can thus be swallowed instead of closing the session.

While that read is blocked, the loop performs no port reads, deadline checks or writes. Session deadlines cannot interrupt the blocked call. After input resumes, buffered replies receive the later read time and may be rejected as late; timestamps cannot establish their actual arrival time, and lossless retention is not guaranteed. The stop/drain/close path cannot be assumed to have started while input is blocked. Immediate Ctrl+C response in this condition has not been verified on Windows.

Evidence: [Claude Code (Anthropic) reported L-4 and a fake-console reproduction](https://github.com/murphys-logs/tv-autocal/pull/24#pullrequestreview-5675474412). Codex (OpenAI) inspected the unchanged code and reconsulted [Python's `getch`/`getwch` documentation](https://docs.python.org/3.12/library/msvcrt.html#console-i-o) on 27 October 2026. The code-path conclusion and documented blocking behaviour are not a test of a real Windows console or the owner's equipment. The earlier 252-test suite covered the special-key pairs; the current suite preserves that coverage without fixing this ambiguity.

Proposed guidance for the **future reviewed T-006 amendment**, not permission to run it:

- Type only the listed lowercase command keys; uppercase letters and Escape do not stop the sender. Avoid text input, pasted text and composed/accented characters in this console.
- If input seems stalled, press the harmless non-command **Space** once, then lowercase **q** to request closure. Space may satisfy the pending read; this is a stop request, not a way to continue the test. Look for `"closed": true` in the final printed JSON result and retain its `reason`. A `Phase: stopped` line, if printed, describes the session phase and does not establish port closure; it need not appear after `q`. A missing result or `"closed": false` leaves closure unconfirmed. Software-reported port closure does not establish restoration or electrical safety.
- Treat the interrupted session as inconclusive even if the tool reports acceptance. Retain its logs and record the input interruption and uncertain timing. Do not resume, retry or send restoration commands; use only the reviewed plan's manual restoration procedure. If closure or restoration cannot be confirmed, stop further project work for review.

After a block, the final `reason` may say `exclusive reply deadline reached` or report late/unexpected bytes even if the TV replied within the intended window. Record the input interruption alongside that reason or any error output; do not treat the software's read timestamp as evidence of when the TV replied.

The future T-006 amendment must explicitly settle whether and how Ctrl+C may be used and what the owner should do if closure is never reported, including console and cable handling. These procedures remain unresolved. This guidance does not authorise force-closing the console or disconnecting equipment, and does not promise immediate Ctrl+C response.

PR #25's documentation-only follow-up added no console feedback, input-API replacement or `kbhit()` workaround. The current presenter/meter change likewise leaves this serial console implementation unchanged. Any future code change must preserve special-key rejection and establish how pending input is handled. The T-006 amendment must address this limitation and its stop guidance before physical authorisation.

## Sources consulted

S-046 records these primary references, consulted 27 October 2026. No sample program from them was executed and no library was installed.

- Python: [Tkinter/images](https://docs.python.org/3/library/tkinter.html#images), [subprocess](https://docs.python.org/3.12/library/subprocess.html), [threading](https://docs.python.org/3.12/library/threading.html), [msvcrt console input: `getch`/`getwch` and special-key pairs](https://docs.python.org/3.12/library/msvcrt.html#console-i-o), [PSF licence](https://docs.python.org/3.12/license.html).
- Tcl/Tk: [photo image/PPM/gamma](https://www.tcl-lang.org/man/tcl8.6/TkCmd/photo.htm), [licence](https://www.tcl-lang.org/software/tcltk/license.html).
- Microsoft: [process DPI awareness](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-setprocessdpiawarenesscontext), [DPI-context comparison](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-aredpiawarenesscontextsequal), [associated monitor](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-monitorfromwindow), [monitor rectangle](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getmonitorinfow). API setup is provisional for this source-run tool; a future packaged executable should review Microsoft's manifest recommendation.
- pySerial: [3.5 API, open/timeout/line semantics](https://pyserial.readthedocs.io/en/latest/pyserial_api.html), [BSD-3-Clause licence and line behaviour](https://pyserial.readthedocs.io/en/latest/appendix.html).
- Argyll output/argv evidence remains [S-037/S-043](integration.md#meter-output-contract-and-consulted-source); this change does not revalidate the installed executable or meter.

## Offline verification

Current verification is recorded in [component-readiness.md](component-readiness.md#offline-verification), with exact interpreter versions and the current suite count. On 28 October 2026, Python 3.12.14 and 3.15.0 each passed **287/287**, with zero failures, errors, skipped or unrun tests.

The earlier PR #25 record passed 252/252 on Python 3.12.14 and 3.15.0 on 27 October 2026. This follow-up changes presenter/meter code and tests, so those historical results do not establish the new code's result. The original `tv_autocal` modules and inherited renderer/protocol tests remain byte-identical to the merged PR #26 base. The serial sender and its special-key regression remain unchanged.

The component containment test reruns all component functional cases with real file/process/network/native calls and hardware imports forbidden. Those guarded reruns are not additional distinct tests. Backend cases supply inert fake Tk, native APIs, signals, processes and pipes; neither a real GUI nor instrument child is used. The inherited source-regression test writes only temporary inert text. No dependency is installed.

The SHA-256 manifest below identifies the tested source bytes without a self-referential commit hash. Source files use LF. No existing archive, instruction file, dependency or workflow changes; physical-plan documentation is updated to the new interface without filling any authorisation.

| File | SHA-256 |
|---|---|
| `tests/test_component_containment.py` | `d49ba807604d4726b1fd4adbb4b4d4ca93293de9240a3ec6b07e0c08f65d5ff9` |
| `tests/test_component_entry.py` | `40ebc16b4fcfbb9b95ad571133fd2b6b26746c3d40163a34ec53e1e0ee6303a3` |
| `tests/test_component_meter.py` | `a3811ae32cda1ece1cd42e46fffd5ff6eceec0e4a688182881535ec851cdcfd7` |
| `tests/test_component_presenter.py` | `c48f642495cf87f66b63cd2d14e8a920cea03c305b5ab33f29a914b872575195` |
| `tests/test_component_receipt.py` | `29a8d5684cfd8d0ae8110fbc277d922257ff991e5a9744d6d047d7760070bf85` |
| `tests/test_component_serial.py` | `efa42233e5fc85ed8121225b581b647489b0949883f244f276482bd8185fd1bd` |
| `tests/test_cycle.py` | `2afb23d1268e82f77a4546b1a82d784f8762c87f65e7401accaf8bfdef5d2f30` |
| `tests/test_integration.py` | `8afda185be5736d14196793263ffe9f626066322241f0def188269b83c65531f` |
| `tests/test_meter_output.py` | `14308754d93164f13d7779a829171c778f4fbddaa825c5326185041af63600ac` |
| `tests/test_presentation.py` | `33cfda3e4c85def864ada43b44a715c38f123b06a586843f43b30f70fb778b48` |
| `tests/test_renderer.py` | `9df6b56ef3ede15ba6b3c88c95178e97ef2ca26a7ac9a93288b7c7be5278bbab` |
| `tests/test_renderer_cycle_integration.py` | `102cff513e480922646a3d0b88933cc37888e5c30aea76e0fa50ee142c9a76d9` |
| `tests/test_sender_audit.py` | `d421d8a9c84158fe95010c85d0f853f6d951112792a05f51b0cde7953137f45e` |
| `tests/test_software_containment.py` | `0836f4c8f9523a2af9192bc1051f078feedd15bfcb0d674a778dcf2a78fa2486` |
| `tests/test_t009.py` | `3913b69c1c507b3a08f700d602ca106566c07d95cee3d7fd578847b64a2eeb74` |
| `tv_autocal/__init__.py` | `02a4bc365fe39e9bcb75a8dc978d04ae87a249fd33d9ecda252cae1cc1ab651d` |
| `tv_autocal/cycle.py` | `82cbbe9e231d90caf94b451d1cf6713d85e9929cdc3d4711c795a3151316ab80` |
| `tv_autocal/demo.py` | `0dd82febfe3489b9ecf964377739a0643d6aa223f0d34361a87a5b5df5dd4fce` |
| `tv_autocal/exlink.py` | `d55c4ac872e95c02dd5a379e68ea4a4d7661dab63e57dd5769560f779c423596` |
| `tv_autocal/integration.py` | `56f091070e40ad29ad67ebf9c590df61b486f1814f0bca668795daa9cb3ab00c` |
| `tv_autocal/meter_output.py` | `23de206707e4998aac5b3e8b71108a7fab25336f754c3deaded88b03a9f0987c` |
| `tv_autocal/presentation.py` | `0b4ddbd5eaf6eaf533dedc194da891c171a9a00c96fe418c78e72e3d9ce71648` |
| `tv_autocal/renderer.py` | `1eaadc72e2785c3d7d96980a979469c9f26788f8a0d938ad19e5c8bc142f518f` |
| `tv_autocal/sender_audit.py` | `c0b61f096ec3fd84cdd9c8c21743f000ec849feacc0302b488f1332a9986a185` |
| `tv_autocal/simulation.py` | `bd84b7e1b597156af4ce2952fc6f2e3cfa2094d6fba1ef4e0a639406e94b69d8` |
| `tv_autocal_tools/__init__.py` | `1c12211105f7dc70ba509a15241aceae7a5c0c644bb37d925b9a81ac902378b1` |
| `tv_autocal_tools/__main__.py` | `04ab59fcc90685a56c34e0bd25f7b60c4c844a05b1df39d5de3bcc106ff69b46` |
| `tv_autocal_tools/cli.py` | `69769e7cc229ec84c0538b40a8f5eeb570965d370f441a0a11b699be211bbb00` |
| `tv_autocal_tools/journal.py` | `3f77cc36429017ebbe5f2a71c759b1f25098a3c748e393575e1f64a962438ffe` |
| `tv_autocal_tools/meter.py` | `e6aedd1440e86cf0cd4a38567f4ca85509bc21d212ff4b283bbe5dc8c390fc03` |
| `tv_autocal_tools/permission.py` | `ecabf7bc25ce444d407323d949f34b5def0c1c309fd64c7c6316967d6d928ddc` |
| `tv_autocal_tools/presenter.py` | `7070154654b6ad600be4ab5d0168be660ab4a31c15a71bfa644cfe72fc1ac281` |
| `tv_autocal_tools/receipt.py` | `e05fbae85ff166b529961e9c2d008346b64c346b0b58758e5ea329b305972c61` |
| `tv_autocal_tools/serial_tool.py` | `6b9a51ccb38f3960d3fba78b2b24bfc8501a2df4315e982ebf88ec773eebb716` |

## Remaining gates

The source paths were independently reviewed and merged in PR #24, with the documented console limitation reviewed and merged in PR #25. No operational window, monitor check, process launch, meter discovery, serial open or equipment test was performed during implementation or amendment preparation. Tk/driver/pySerial availability, actual Windows presentation, electrical compatibility, setting restoration and installed Argyll behaviour remain untested.

PR #26 merged the [execution amendments](../tests/component-execution.md). The [readiness follow-up](component-readiness.md) updates the source manifest, presenter interface and meter lifecycle records; these changes await independent review. Actual runtime/display inputs, abnormal-stop procedures and owner permission remain open. T-005's amendment specifies the separate V4 presenter runs but does not establish correct range interpretation. T-006 still needs electrical evidence, setting-scope/restoration, menu timing and exact physical connection/stop procedures, including [L-4](#known-console-limitation), Ctrl+C and missing closure reports. Existing approved patch geometry and all unfilled authorisation sections are preserved. T-013/T-008 remain unsupported and blocked on their respective evidence, correction and authorisation gates. Q-001/Q-002/Q-003/Q-008/Q-014/Q-016 and X-012 are not resolved by these amendments.
