# Ex-Link protocol investigation and proposed offline verification

**UE49KS7000UXXU compatibility: not tested and not established by these sources.** The verification plan below is **proposed; not executed**. No equipment was contacted.

| Field | Value |
|---|---|
| Title | Ex-Link protocol investigation and proposed offline verification |
| Produced by | Codex (OpenAI) |
| Original date | 2026-10-24 |
| Imported | 2026-10-24, by Codex (OpenAI) |
| How obtained | Direct inspection of published documents and pinned source code; local arithmetic on literal bytes |
| Fidelity | Original research summary and proposal; short source excerpts only. One clause in the Finding section was later removed at the owner's instruction (D-013); the marker "\[removed under D-013\]" shows where. The uncut text is in commit 337a58f1ac81e5359e9c9d762b06717b156313d0, and it stays there only while git history is left intact (Q-017) |
| Ledger ID | S-005 |

## Finding

There is enough published information to propose a small, hardware-free packet encoder and response parser. There is insufficient evidence here to promise control of this particular TV's calibration settings. The generic packet format, model-specific command support, cable compatibility and measurement of actual picture changes are separate questions.

This investigation did not use the unavailable earlier Claude feasibility report or ChatGPT critique. Research assistance from other Codex agents is still one vendor's work. Claude Code reviewed the initial proposal; this revision addresses its three findings and awaits re-review. The proposal incorporates main's Ex-Link-only decision and cable record (D-006, C-008) \[removed under D-013\]. This proposal concerns Ex-Link alone and makes no additional purchase or equipment-test proposal.

## Sources actually consulted

All sources below were accessed on **24 October 2026**. References use fixed commits so a later upstream change cannot silently change the cited evidence.

| Ledger source | Citation and location | Provenance and limits |
|---|---|---|
| S-006 | *Consumer RS232 Control Worksheet*, Samsung-branded, five pages. [PDF at commit e2489b3](https://github.com/home-assistant-libs/samsung-exlink/blob/e2489b33c720c36d1995392b803f2336baf7b808/docs/Samsung-RS232-Control.pdf). PDF metadata names Anthony Moliterno and a creation date of 27 June 2023; no document revision number was established. | A community-hosted copy of a manufacturer-branded document. Its original distribution and authenticity have not been independently authenticated. Page 1 gives applicability limits, native-jack/dongle routes and service-menu setup; page 2 covers framing/checksum and the pin-out; page 3 shows success feedback; pages 4–5 list generic picture controls and factory/service-menu hazards. |
| S-007 | Home Assistant Libraries, *samsung-exlink*, commit `e2489b33c720c36d1995392b803f2336baf7b808`, 17 October 2026: [README](https://github.com/home-assistant-libs/samsung-exlink/blob/e2489b33c720c36d1995392b803f2336baf7b808/README.md), [protocol.py](https://github.com/home-assistant-libs/samsung-exlink/blob/e2489b33c720c36d1995392b803f2336baf7b808/src/samsung_exlink/protocol.py), [const.py](https://github.com/home-assistant-libs/samsung-exlink/blob/e2489b33c720c36d1995392b803f2336baf7b808/src/samsung_exlink/const.py), [tv.py](https://github.com/home-assistant-libs/samsung-exlink/blob/e2489b33c720c36d1995392b803f2336baf7b808/src/samsung_exlink/tv.py), [show_service_menu.py](https://github.com/home-assistant-libs/samsung-exlink/blob/e2489b33c720c36d1995392b803f2336baf7b808/scripts/show_service_menu.py). | Primary evidence of this library's implementation; secondary evidence of Samsung TV behaviour. The library explicitly references S-006, so agreement between them is not independent confirmation. MIT-licensed; inspected, not installed or executed. |
| S-008 | mgoff, *go-samsung-exlink*, commit `3bed0c96a57034299cfb320589be59a1588bfd78`, 8 February 2017: [exlink.go](https://github.com/mgoff/go-samsung-exlink/blob/3bed0c96a57034299cfb320589be59a1588bfd78/exlink.go), especially the `powerOn` constant. | Primary evidence of its literal source code; secondary evidence of TV behaviour. Contains the checksum inconsistency described below. Inspected, not installed or executed. |

The downloaded worksheet's SHA-256 is `38b932a0a712815f845c509ca77b8ea470b703425a598ac905a9d4998d4657fb`. This identifies the inspected copy; it does not authenticate its publisher. No third-party PDF or implementation is added to this repository. For this revision, the pinned PDF, README and service-menu script were read again; the PDF hash still matches. Source code was read only, not run.

The [Samsung exact-model support page](https://www.samsung.com/uk/support/model/UE49KS7000UXXU/) could not be consulted: the network proxy returned HTTP 403. The worksheet's linked partner portal was also inaccessible. These are retrieval limitations, not evidence that documentation or support does not exist. No manufacturer-hosted protocol or exact-model compatibility claim is treated as verified.

## What the references support

| Topic | Finding | Evidence and equipment status |
|---|---|---|
| Connection routes | The sources describe a native 3.5 mm Ex-Link jack (their examples say “Q70 and above”, plug and play) or a proprietary Samsung USB-to-Ex-Link dongle (“8000 or Q60”). Neither names the 2016 KS7000. | S-006 p. 1; S-007 README Hardware. C-020; **not tested** on the owner's TV. These are the sources' model examples, not verified applicability here. |
| Dongle setup hazard | The dongle route requires service-menu settings **EXT Link Support** and **USB Serial**, under Control → Sub Option. The sources describe entering that menu with the TV off via Mute–1–8–2–Power. This is a hazard record, not a test instruction or authorisation. | S-006 p. 1; S-007 README Hardware. C-020; **not tested**. Service-menu changes have the additional safeguards in [AGENTS.md section 7](../../AGENTS.md#7-equipment-safety-rule-6); buying a proprietary dongle would need separate approval. |
| 3.5 mm pin-out | From the controller's perspective: **tip = received data** (TV transmit); **ring = transmitted data** (TV receive); **sleeve = ground**. S-006 labels these pins 2, 3 and 5 respectively. | S-006 p. 2; S-007 README Hardware. C-021; **not tested**. The selected cable's actual wiring and voltage levels remain unverified. |
| Factory/service-menu hazards | S-006 includes **KEY_FACTORY (0x3B)** and **Factory-SVB / Expert-N/D Adj**. S-007's `scripts/show_service_menu.py` sends the Mute–1–8–2–Power IR sequence through a network IR transmitter. | S-006 key map p. 4 and control table p. 5; S-007 script. C-022; **not tested**. Do not run the script or import it into the verification path. The T-009 allowlist must never include factory/service-menu keys or commands. |
| Consumer command frame | Seven **binary bytes**: `08 22 cmd1 cmd2 cmd3 value checksum`. The four middle bytes select a command and its value. The displayed hex text is a human-readable representation, not an ASCII message to send. | S-006 p. 2; S-007 `build_frame`. C-009; **not tested** on the owner's equipment. |
| Checksum | Add the first six bytes, take the negative modulo 256: `checksum = (-sum(frame[0:6])) & 0xFF`. The complete frame then sums to zero modulo 256. | S-006 p. 2 supplies the worked example; S-007 supplies the explicit wraparound rule. C-009; **not tested** on equipment. |
| Serial settings | S-007 documents **9600 baud, 8 data bits, no parity, 1 stop bit (8N1)**. This is a candidate profile, not a confirmed setting for this TV. | S-007 README. C-010; **not tested**. Cable voltage levels, wiring and driver behaviour are not established here. |
| Replies | `03 0C F1` is described as success feedback. S-007 also recognises `03 0C FF` as failure/NACK. These short replies contain no command identifier or picture-setting value. | S-006 p. 3 for success; S-007 for NACK. C-010; **not tested**. An absent response must produce an explicit timeout/unknown outcome. |
| Status readback | S-007 implements some `F0` queries and `03 0C F5` data responses for power, volume, mute, channel and source, while warning of unsupported firmware and generation-dependent values. | S-007 README/protocol implementation. C-011; **not tested**. This does not establish calibration-setting readback on KS7000. Keep these extensions outside the first verification slice. |
| Calibration controls | The worksheet lists gamma, white-balance gains/offsets and colour-space controls, including negative ranges. It does not establish their availability, ranges, signed-value encoding, persistence or readback on UE49KS7000UXXU. | S-006 pp. 1, 4. C-011; **not tested**. Do not infer a two's-complement setting encoding merely from a negative range. |

S-006 expressly says that some models are unsupported and that consumer commands differ from commercial-model commands. A generic Samsung RS232 command table cannot therefore be assumed to apply to this TV. The owner-purchased USB-to-3.5 mm cable (C-008) is only a candidate for the native-jack route; it does not substitute for the proprietary Samsung USB dongle. T-001 should first record whether the TV's accessible port labels identify a native Ex-Link jack, without connecting anything or entering the service menu. Any later T-006 plan must establish the actual connection route, matching pin-out and electrical compatibility before connecting or sending commands. Neither candidate is authorisation to proceed (C-020, C-021).

An acknowledgement means only what a particular source and model establish. S-007 updates some stored state from sent commands; that stored value is not an independent observation of a changed setting. Its two-second timeout and one-second late-response window are library choices, not manufacturer timing guarantees. Since the three-byte acknowledgement has no transaction identity, even a finite quiet interval cannot prove that a later acknowledgement belongs to the next request. These distinctions motivate the failure cases below (C-010, C-011, C-014).

## Source inconsistency and arithmetic checked

S-008 defines power-on as `08 22 00 00 00 02 D6`. The first six bytes total `0x2C`; their negative modulo 256 is **`D4`**. S-007 uses `D4`, consistent with the worksheet's rule. Record this as **X-001**, a published-source discrepancy. The arithmetic is resolved; why the Go literal differs and what a TV would do with it are unknown. It is not evidence of a different supported protocol variant (C-012).

The following was calculated locally with Python 3.12.14 using only `bytes.fromhex`, integer sums and modulo arithmetic. No third-party library or transport was executed. This is a source-arithmetic check, not execution of the proposed verification suite.

| Literal fixture | Provenance | Calculated checksum | Complete sum modulo 256 |
|---|---|---|---|
| `08 22 00 00 00 01 D5` | S-006 p. 2, power off | `D5` | `00` |
| `08 22 00 00 00 02 D4` | S-007 README, power on | `D4` | `00` |
| `08 22 01 00 00 19 BC` | S-007 README, volume 25 | `BC` | `00` |
| `08 22 00 00 00 02 D6` | S-008 literal, intentionally retained as a negative fixture | `D4` | `02` |
| `08 22 00 01 00 19 BC` | Codex synthetic permutation of the volume fixture; no command meaning asserted | `BC` | `00` |

The last row demonstrates a limitation of an additive checksum: a byte permutation can preserve it. Compensating changes can do the same. A valid checksum alone cannot establish a recognised command, an authentic response or a safe operation (C-013). None of the fixture commands is described as harmless if transmitted to equipment; the proposed work is harmless because it has no equipment transport.

## Proposed software-only verification plan — T-009

**Status: proposed; not executed.** This is an AI: Codex (OpenAI) design proposal (C-014). It requires no hardware, purchases, new dependencies or automatic jobs. It does not settle the project's Python-version/packaging choice (Q-003). Keep software simulation material here or in ordinary software-test documentation; `docs/tests/` is reserved for physical-test plans and results.

The first implementation should contain only a pure byte encoder/parser and a small in-memory fake transport: a queue of scripted reply bytes and a record of requested writes. It should have **no real transport implementation or real-mode switch**. No serial library, COM/device enumeration, sockets (including localhost), USB/Bluetooth probing, subprocesses, measurement tools, service-menu actions or pattern output belong in this verification path. Attempting to supply a port or host must fail locally. Do not import the cited libraries' controllers or run their example applications, especially `scripts/show_service_menu.py`. The factory/service-menu hazards listed above are excluded from the command allowlist, including `KEY_FACTORY` and Factory-SVB / Expert-N/D Adj; raw command entry must not bypass that exclusion (C-022).

| Step | Proposed check | Acceptance condition |
|---|---|---|
| 1. Freeze evidence | Record the literal fixtures above and ACK/NACK bytes, their pinned references and the selected protocol profile. | Expected bytes are transcribed independently of the encoder. Each fixture is identified as published, derived or synthetic. Unsupported details remain explicit. |
| 2. Encode and validate | Compare complete output with the three valid request fixtures. Reject wrong types, missing fields, values outside 0–255 and unsupported command/value combinations. | Exact byte-for-byte matches; no silent truncation or wrapping. Raw byte validity is separate from command-specific validity. Invalid inputs produce no fake write. |
| 3. Check corruption | Reject wrong lengths, wrong header and the S-008 checksum fixture. Change each covered byte in turn without updating the checksum. Also retain the checksum-preserving permutation. Include factory/service-menu keys and commands as rejected inputs, including KEY_FACTORY (0x3B) and Factory-SVB / Expert-N/D Adj. | Single-byte corruption is detected. The permutation may pass arithmetic, but must not acquire the original command's meaning or pass the selected command allowlist. Factory/service-menu keys and commands must never enter the allowlist, even with a valid checksum; each is rejected before any fake write. Checksum acceptance alone never authorises a command. |
| 4. Parse replies | Feed ACK/NACK whole, byte by byte, split at every boundary and concatenated. Include noise, reversed header bytes, truncation and unknown status bytes. | Only a complete recognised reply yields a simulated ACK/NACK. Preserve incomplete data within a bounded buffer; unexpected input fails explicitly. Unsolicited or duplicate replies cannot complete a future request. |
| 5. Exercise failure handling | Script no response, partial write, cancellation, duplicate ACK and late ACK. Use an injected fake clock around an explicitly chosen deadline. | Exactly one request is allowed per fake session, with no automatic resend. Every terminal outcome, including ACK/NACK, retires that session; later bytes cannot confirm another command in it. A new test starts with a fresh fake session. Concatenated-byte parser tests are standalone. This containment policy does not solve real-stream correlation or make claims about real reconnection. |
| 6. Separate evidence states | Track “encoded”, “fake write accepted”, “simulated ACK”, “simulated rejection” and “unknown outcome” separately. | None can set “TV setting verified” or “calibration improved”. Any fake state change remains labelled simulated. |
| 7. Verify containment | Inspect imports/call paths and exercise rejected port/host configuration. Use test guards that fail on unexpected device/network/process access. | The test program has no route to a real device. Guards supplement the absence of a hardware backend; they are not the sole safeguard. |
| 8. Run manually and record | After an implementation is separately prepared, run its exact documented command with the normal hardware-free test runner. Record revision, interpreter, fixture sources and case outcomes. | Report passed, failed, skipped and unrun counts separately. Retain failures. No automatic GitHub Action is introduced. |

Avoid circular verification: expected packet bytes must not be produced by the encoder under test, and the fake must not compute its responses with that encoder. Encode/decode round trips can supplement the published fixtures but cannot replace them. No fake can establish how the real firmware handles a packet.

The successful outcome of T-009 would be limited to agreement with the selected published fixtures, predictable error handling and absence of hardware I/O. **C-005 stays Not tested and T-006 stays an unauthorised physical-test question.** Model-specific documentation, electrical/cable compatibility and actual TV behaviour remain unresolved (Q-006). Any future physical plan would be a separate proposal under AGENTS.md.
