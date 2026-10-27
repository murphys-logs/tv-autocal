# T-009 — software-only Ex-Link prototype

> **Implemented and tested in memory only; ready for independent review.**
> This software cannot connect to equipment. No TV setting, meter reading,
> calibration improvement, electrical compatibility or firmware support has
> been demonstrated. T-006 and all physical tests remain unauthorised.

Prepared by Codex (OpenAI), 27 October 2026, from merged baseline
`ba099e0a182713945c247636042286e6f9dca626`, implementing the bounded proposal in
[S-005](../research/2026-10-24-exlink-protocol-investigation.md#proposed-software-only-verification-plan--t-009).
This is an engineering proposal under C-014, not an agreed production transport
design or an independent review. Q-002 (project licence), Q-003 (Python version
and packaging), Q-006 (model-specific commands) and X-007 (future transport
policy) remain open.

## What this slice contains

| File | Responsibility |
|---|---|
| [exlink.py](../../tv_autocal/exlink.py) | Pure byte encoding, separate frame/checksum validation, strict bounded ACK/NACK parsing |
| [simulation.py](../../tv_autocal/simulation.py) | Manually advanced fake clock, literal scripted replies, one-request in-memory session and distinct software evidence |
| [test_t009.py](../../tests/test_t009.py) | Literal reference fixtures, malformed inputs, error/timing cases and containment checks |

There are no third-party dependencies. The standard library provides `enum`,
`dataclasses` and the test runner (`unittest`); Python uses the PSF licence.
The source uses Python 3.10+ annotation syntax, but support is demonstrated only
on the two interpreters in the run record below. No Python version, package
manager or installer is selected for the eventual application. No automatic
GitHub Actions or scheduled jobs are added.

## Fixture evidence and limits

Expected test bytes are literals transcribed independently of the encoder.
The fake does not derive replies from the request. Protocol values are research
fixtures, **not instructions or permission to send these commands to a TV**.
In particular, the power and volume examples could alter equipment if another
program transmitted them; this prototype has no mechanism to do so.

| Fixture | Bytes | Provenance |
|---|---|---|
| Power off | `08 22 00 00 00 01 D5` | Published: S-006 p. 2, also S-007 README |
| Power on | `08 22 00 00 00 02 D4` | Published: S-007 README |
| Volume 25 | `08 22 01 00 00 19 BC` | Published: S-007 README |
| ACK | `03 0C F1` | Published: S-006 p. 3, S-007 constants |
| NACK | `03 0C FF` | Published: S-007 constants; model behaviour not established |
| Incorrect power-on checksum | `08 22 00 00 00 02 D6` | Published negative fixture: S-008 as recorded in S-005/X-001 |
| Checksum-preserving permutation | `08 22 00 01 00 19 BC` | Synthetic negative fixture from S-005; no command meaning asserted |
| KEY_FACTORY | `08 22 0D 00 00 3B 8E` | Derived negative fixture: S-007 key command triple and key value, with calculated checksum |
| Factory-SVB / Expert-N/D Adj | `08 22 0B 0D 00 00 BE`, `08 22 0B 0D 00 01 BD`, `08 22 0B 0D 00 02 BC` | Derived negative fixtures: S-006 p. 5 command/value rows, with calculated checksums; never allowlisted |

The implementation author reconsulted S-007's pinned
[README](https://github.com/home-assistant-libs/samsung-exlink/blob/e2489b33c720c36d1995392b803f2336baf7b808/README.md),
[constants](https://github.com/home-assistant-libs/samsung-exlink/blob/e2489b33c720c36d1995392b803f2336baf7b808/src/samsung_exlink/const.py)
and [protocol source](https://github.com/home-assistant-libs/samsung-exlink/blob/e2489b33c720c36d1995392b803f2336baf7b808/src/samsung_exlink/protocol.py)
through the GitHub connector on 27 October 2026. These are primary evidence for
that MIT-licensed library's code, not for the owner's TV. It was neither
installed nor imported, and no implementation was copied into the prototype.
The S-006 Factory-SVB rows were checked visually by the parent Codex author
against page 5 of the pinned worksheet during this task; its SHA-256 is
`38b932a0a712815f845c509ca77b8ea470b703425a598ac905a9d4998d4657fb`.
The S-008 literal is taken from the consulted repository archive S-005, not a
new inspection of S-008. The [archived source inventory](../research/2026-10-24-exlink-protocol-investigation.md#sources-actually-consulted)
preserves the original provenance and exact-model limitations.

## Deliberate limits and failure behaviour

- The encoder allows **only the three complete published request tuples** above.
  It does not expose arbitrary keys, calibration controls, status queries,
  service commands, signed setting encodings, or other volume values.
- `validate_frame` checks raw structure/checksum only. A checksum-valid frame
  can still be unsupported or dangerous. Both `encode` and `submit_frame` apply
  the closed fixture allowlist before any fake write. Factory commands and the
  checksum-preserving permutation are rejected.
- Integer fields reject booleans, floats, strings and out-of-byte-range values;
  nothing is coerced or silently wrapped. Binary inputs must be immutable bytes.
- The standalone parser accepts whole, split and concatenated ACK/NACK replies.
  It retains at most two incomplete bytes and limits each feed to 96 bytes.
  Noise, unknown status, reversed headers or a truncated end of input fail
  explicitly and permanently retire the parser. There is no resynchronisation.
- A fake session permits one request only. Every ACK, NACK, timeout, cancellation,
  partial fake write or malformed reply permanently retires it. There is no
  automatic resend, real reconnection, or subsequent request in that session.
  A fresh test constructs an independent fake with its own script and state.
- The default deadline is **2,000 fake milliseconds**, an explicit test policy,
  not a manufacturer timing guarantee and not Q-008's menu-settling delay.
  Arrival strictly before the deadline can count; arrival at/after it cannot.
  When polling is delayed, scripted arrival times determine the result.
- Multiple replies or a complete reply followed by partial extra bytes in one
  delivery produce an unknown outcome. Later bytes cannot change a terminal
  outcome. Scripted polling and direct synthetic delivery cannot be mixed.
- `Evidence` separates encoded bytes, accepted fake write, simulated ACK,
  simulated rejection and unknown outcome. It has no TV-setting-verification
  or calibration-improvement field. An ACK never proves either.

The application modules import only `enum`, `dataclasses` and their local
protocol module. There is no transport implementation, device enumeration,
serial library, network access (including localhost), USB/Bluetooth access,
subprocess, Argyll invocation, pattern display, port/host configuration or
real-mode selector. Supplying `port`, `host`, `transport` or `real_mode` fails
locally. The fake accepts its own concrete clock and immutable scripted data,
not an arbitrary transport callback.

Static import/call inspection and runtime guards against file/device opens,
socket access and process launches supplement this absence of hardware code.
The guarded test reruns all 35 functional tests with those guards active.
These checks are not a security sandbox for arbitrary Python or future edits.
Source review remains necessary when the code changes.

## Reproduce the software tests

From the repository root, using an already installed Python interpreter:

```powershell
python -B -m unittest discover -s tests -v
```

On the owner's existing Python launcher, the command actually run was:

```powershell
py -3.15 -B -m unittest discover -s tests -v
```

The bundled Python 3.12.14 executable was also invoked with
`-B -m unittest discover -s tests`; its machine-specific path is intentionally
not committed. No installation is needed for this slice. `-B` avoids bytecode
cache writes; the runner only imports software and prints test results.

## Manual software run record — 27 October 2026

| Run | Interpreter | Passed | Failed | Errors | Skipped | Unrun discovered tests |
|---|---|---:|---:|---:|---:|---:|
| Initial draft | Python 3.15.0 | 35 | 1 | 0 | 0 | 0 |
| After adding explicit Factory-SVB fixtures and fixing nested-suite count | Python 3.15.0 | 37 | 0 | 0 | 0 | 0 |
| Same revision | Python 3.12.14 | 37 | 0 | 0 | 0 | 0 |
| Final code below, including rejection of mixed delivery modes | Python 3.15.0 | 38 | 0 | 0 | 0 | 0 |
| Same final code | Python 3.12.14 | 38 | 0 | 0 | 0 | 0 |

The initial failure was a test-bookkeeping assertion expecting 35 nested
functional tests when 33 existed. The guard itself reported no I/O failure.
The assertion now compares executed count with the suite's discovered count.
The final 38 top-level cases include the guarded rerun of 35 functional cases;
those nested executions are not counted as 35 additional distinct tests.
Loops cover 5,355 single-byte corruptions and 65,024 unsupported first-command-byte/value
combinations. These counts describe synthetic inputs, not equipment operations.

The exact tested application/test contents are identified below so the run
record does not rely on a self-referential commit hash. The containing PR commit
identifies the full proposed tree; any later code change requires a new record.

| File | SHA-256 of tested bytes |
|---|---|
| `tv_autocal/__init__.py` | `02a4bc365fe39e9bcb75a8dc978d04ae87a249fd33d9ecda252cae1cc1ab651d` |
| `tv_autocal/exlink.py` | `d55c4ac872e95c02dd5a379e68ea4a4d7661dab63e57dd5769560f779c423596` |
| `tv_autocal/simulation.py` | `bd84b7e1b597156af4ce2952fc6f2e3cfa2094d6fba1ef4e0a639406e94b69d8` |
| `tests/test_t009.py` | `daaec54ad5f478a725ab4aa680851e4f159e0dffdd725b313ed39472067ec008` |

## What remains outside T-009

There is no real serial transport, command-correlation guarantee, TV state
simulator, meter simulator, measurement-cycle controller, pattern renderer,
optimisation engine or graphical application in this bounded slice. A future
T-006 harness must be separately designed/reviewed; this fake must not be
repurposed as a physical driver simply by adding a port option. T-009's passing
tests do not satisfy T-003, T-005, T-006, T-013 or T-008 and do not change any
equipment claim to Confirmed. Review is still required from Claude Code
(Anthropic) or Antigravity (Google); two Codex agents are one vendor.
