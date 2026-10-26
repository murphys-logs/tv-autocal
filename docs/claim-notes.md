# Claim notes

This file holds the analysis behind the claims in [LEDGER.md](../LEDGER.md), moved here word for word; only relative link paths are changed so that they work from this folder. The ledger remains the record of each claim's provenance and equipment test status; this file adds no claims.

## C-004

That the signal must not be altered on the way — by graphics settings, Windows colour management or the receiver — is Claude Code's reading of "controlled".

## C-005

S-001: compatibility "has not yet been demonstrated". Ex-Link is the only control route in scope under D-006; the selected cable does not establish compatibility.

## C-007

Depends on C-002 to C-005 and on which controls the TV offers, under the Ex-Link-only decision D-006. The optimiser can be developed in simulation first; that will not change this status.

## C-008

Purchase record only. The owner wrote "2100" without a time zone (S-004); earlier records added "Europe/London" as an assumption. The product title and specifications are owner-reported; delivery status is unknown. Cable and TV compatibility remain untested (T-006). [Owner-supplied product link](https://www.amazon.co.uk/dp/B07XXWVH69).

## C-009

Generic source-supported profile; no assertion of support on this TV. The library references the worksheet, so they are not independent confirmations.

## C-011

Exact-model Samsung page was inaccessible. Absence of verified evidence here is not evidence of incompatibility. Q-006 remains open; C-005 stays unconfirmed.

## C-020

Source examples are not a compatibility list for the owner's TV. C-008's USB-to-3.5 mm cable is a candidate for the native-jack route, not evidence of support for the proprietary-dongle route. Check the TV's accessible port labels first; no service-menu step or dongle purchase is authorised.

## C-022

T-009 must exclude factory/service-menu keys and commands from its allowlist and reject them without even a fake write. The script must not run; its IR/network route is outside D-006. No service-menu behaviour is verified or authorised.

## C-023

The owner's description of the planned set-up. The owner did not say where the cable runs; Claude Code assumes it comes down the front of the screen from the top edge (unverified).

## C-029

S-012 section 6. Historical recommendation, not a newly accepted luminance target. No black, white or accuracy measurements were made; the previous 250 cd/m² mention is not verified here.

## C-031

S-012 sections 4, 5 and 7. The report's local-slope equation and milestones remain proposals; the later Ex-Link-only decision (D-006) and measurement cycle (D-013) govern any future implementation.

## C-035

If the cited page says this, it is the most direct evidence so far that this TV generation accepts calibration commands over Ex-Link (C-005, Q-006). It would not establish the command encoding: S-002 says Calman's protocol is unpublished and proposes a probe. The wiring matches C-021's pin-out. S-002 treats the KS7000 as one of these sets; the page's model list has not been checked here.

## C-036

T-001's look-only check of the port labels would settle this. S-006 and S-007 do not name the KS7000 (C-020). A jack being present would not establish that it accepts commands (C-005) or that the owner's cable (C-008) matches it (T-006).

## C-038

The absolute absence claim is not established by C-010/C-011: those sources do not document picture-setting readback. See X-005 for the distinction between acknowledgement, numeric state and measured light. Claude Code's unverified hypothesis (AI: Claude Code): if OSD-off works on this TV, it might stop setting sliders appearing after a change. Change, exit, wait, read ([D-013](plan.md#measurement-cycle-and-use-of-readings)) applies either way.

## C-039

S-002 says the sheet also covers later models and that each range must be confirmed on the set. Menu ranges are not Ex-Link value encodings (C-011). T-001 (owner check) reads the actual menus.

## C-040

S-002 proposes that the program count the points and map which grey levels each one moves, rather than assume. Source conflict X-003.

## C-041

Bears on C-002, C-003 and Q-001. S-002 also reports a conflicting forum reply: X-004. S-014/C-055/C-056 now verify documented CCSS support. C-056 corrects the shorthand "one reading": -O can perform a calibration instead.

## C-042

S-002 calls the mismatch between this file, measured on a 2018 TV, and the owner's panel the largest uncertainty in absolute accuracy. How to validate any correction is still Q-001; S-002 says one evening with a borrowed spectrophotometer would help, which would be for the owner to decide.

## C-043

If right, Brightness has to be set by eye on a PLUGE pattern, BT.1886's black level has to be assumed (C-046), and the meter, not the TV, limits absolute accuracy.

## C-044

Bears on C-004. These are settings on the owner's PC, TV and receiver, made by the owner; no agent may send commands to the Denon (AGENTS.md section 7). S-002's black-level and clipping checks belong to T-005.

## C-045

The owner's own equipment, reported at second hand. The owner should confirm it in T-002 before the design relies on it.

## C-046

D-001 already fixes Rec.709, D65 and BT.1886. The brightness bands, the black-level default and the pass marks are proposals for the owner to decide, not decisions (Q-014).

## C-051

**Superseded by D-006:** TV control is Ex-Link only, so S-002's network and infrared routes, including its £0 key-press fallback, are out of scope. Retained as history. If Ex-Link fails on this TV, any change of route is the owner's decision.

## C-052

Subsequently checked in S-015/C-057: the manufacturer-hosted PDF is accessible. Its bytes have not been compared with S-006; publisher hosting does not establish first publication date, exact-model applicability or firmware support.

## C-060

Documentary observations, not TV behaviour. Claude Code's inference that the table covers later models is consistent with these renamed controls/features, but the document does not establish exact-model applicability. This supports the caution in C-011/C-027 and bears on C-039's ranges.

## C-061

Proposal only; no stage has passed, no physical test plan is completed or authorised, and no transport is implemented. Look-only checklist boundary: X-009. [Review history](reviews/2026-10-25-review-records.md#clauses-moved-from-ledger-cells)

## C-062

Samsung's UK User Manual (`BN68-07864G-00` pp. 5, 8, 10–12) shows `HDMI`, `USB` and `Optical` on the external `One Connect` box (called `One Connect Mini` in `S-031`; no 3.5 mm jack) and `LAN` plus `CI` behind the rear `Cover Terminal`. S-032 (C-074) now confirms an undocumented rear 3.5 mm `EX-LINK` socket; detail: [S-024 section 2](research/2026-10-26-antigravity-feasibility-study.md#2-decisive-dependency-table).

## C-063

`ENG-JZDVBEUK-1.1.3` (PDF pp. 56–58, 75; printed pp. 51–53, 70) documents `Colour Tone` (`HDMI-to-DVI` note; `Cool`/`Standard` in `Dynamic` only), `HDMI Black Level` requiring `RGB444`, `Game Mode` switching `Picture Mode` to `Game`, and `HDMI UHD Color` turning the TV off and on when set to `On`. Which `Expert Settings` grey out on `T-JZMDEUC-1270.1` remains a look-only T-001 check ([S-024 section 5.3](research/2026-10-26-antigravity-feasibility-study.md#53-signal-path--test-pattern-renderer-tv_autocalpatterns--dependency-4c)).

## C-064

S-026 (pp. 2–5) matches C-021's 3.5 mm Tip/Ring/Sleeve pin-out and describes the `SH-U35B` as an RS-232 serial cable, corroborated by the delivered leaflet in S-032 (C-076). Because an unbuffered `FT232R` is logic-level (TTL) and neither guide names a transceiver IC or voltage swing, electrical and TV compatibility await a reviewed T-006 plan.

## C-065

Qualifies C-035 and bears on Q-006 and X-010: Portrait's archived 2016 SUHD guide selects `"Control Method: Samsung DDC"` (wire bytes unpublished), which neither proves nor disproves compatibility with public `08 22` consumer picture commands, leaving them unestablished pending T-006. It also refers generically to `"the Samsung OneConnect box"` and switches internally between 10-point and 20-point wording (X-003).

## C-066

Byte-for-byte identity proves S-006, S-007 and S-015 share one upstream worksheet rather than independent confirmations (qualifying C-052 and C-060). Clarifies C-038: `0x0e 0x01` controls command-result feedback banners, so `KEY_EXIT` (`08 22 0d 00 00 2d 9c`) remains necessary under [D-013](plan.md#measurement-cycle-and-use-of-readings). SamyGO `p=107012` (`stich86`) and `p=107013` (`zoelechat`) reflect a `KS7000` switched to `Debug` mode, while S-015 p. 1 shows `UART` selected in an example (X-002).

## C-067

`phillipsnick/samsung-tv` (commit `221d0855`, `lib/app.js` L30–38, L360–438) implements `setPictureGamma` (`0x0b 0x07 0x03`) and basic `0x0b 0x01–0x06` sliders matching S-015 p. 4 addresses, omits white-balance and colour-space commands, and omits two's-complement checksum negation (invalid unless the six-byte sum is `0` or `128 mod 256`). Its `README.md` service-menu warning remains weak secondary context behind C-037.

## C-068

Qualifies C-041 and C-056 and corrects S-002 section 5 line 230: QLED `.ccss` files declare `TECHNOLOGY "Unknown"` (`ccss.c` L303–321 -> `disptech_unknown`, `disptechs.c` L393–396 `refr = 1`), causing `spotread.c` L1734 and `spyd2.c` L3235 to override lowercase `-y` into inline refresh-synchronised measurement unless uppercase `-Y n` is passed. `-N` warns as unsupported (`spyd2.c` L4088), `-O` must precede flags when logging (`spotread.c` L1034), and X-011 records the static `-O` control-flow disagreement ([S-024 section 3.1](research/2026-10-26-antigravity-feasibility-study.md#31-comparison-with-the-claude-feasibility-report-s-002-anthropic-23-october-2026)).

## C-069

Direct driver constraint from `spyd2.c` (L2973–2980): Spyder3/4/5 hardware lacks a reset command, may enter a `"borked state if the driver is aborted"`, and may not clear on immediate restart. Physical USB replugging is an untested AI inference, so our wrapper must exit `spotread` cleanly rather than killing subprocesses mid-read.

## C-070

Confirms C-042's missing 2016 SUHD `.ccss` on 2026-10-26 (`SAM`: 307, `SEC`: 42 entries), shows `oeminst` omits quantum-dot LED, and clarifies why standard `spotread` logs cannot be re-scored: loading a `.ccss` sets `p->ccmat` to unity (`spyd2.c` L2347, L2386) and folds spectra into the `3x7` sensor matrix `p->cal_A` (L2248–2253), discarding the 7 raw sensor channels on output.

## C-071

Primary-manual confirmation for C-044's Denon `Video Mode: Bypass` step on the exact `AVC-X3800H` model, including the helpful side-effect that Denon suppresses its own on-screen volume/status overlays over video in `Bypass` (provided `IMAX DTS` is not active). Actual owner cabling and settings await T-002 and T-005.

## C-072

Replaces S-002's indirect `~0.3 cd/m²` inference (C-043) with ChromaPure's benchmark reporting a `0.38 cd/m²` low-light limit on a 2018 LG OLED (`231 s` for 95 reads), 11-point greyscale error (0.015 in x, 0.005 in y) and colour error (0.006 in x, 0.005 in y) on an unspecified display (no numerical `0.005 / 0.005` figure is given for 10%+), motivating near-black caution against HDTVTest's `0.04 cd/m²` sample UK `UE49KS7000` black. Low-light floor on the owner's unit remains not tested pending T-003.

## C-073

Supports X-003 Source A (`10p` on UK `UE49KS7000UXXU`) while noting HDTVTest states only that `10p` was `"contrast-aligned and didn't work well"` on its sample and labels one chart `"2p & 10p"`. As proposed in [S-024 section 5.4](research/2026-10-26-antigravity-feasibility-study.md#54-numerical-optimiser-verification--safe-stopping-tv_autocaloptimiser--dependency-4d), Stage D runs a reversible single-interval probe and restores recorded `(r_0, g_0, b_0)` and `e_0` if skipped.

## C-074

Resolves the physical Ex-Link port question in C-036, C-062 and T-001, and answers the model-label and firmware items in [equipment.md](equipment.md) (updating C-053). Photographs are withheld under [AGENTS.md section 11](../AGENTS.md#11-privacy-and-credentials) ([S-032](briefs/2026-10-26-pr19-rulings-and-equipment-confirmations.md)). Confirming the physical 3.5 mm `EX-LINK` jack does not prove electrical or command compatibility on `T-JZMDEUC-1270.1`, which remains Not tested pending T-006.

## C-075

Confirms C-045's GPU model directly from the owner ([S-032](briefs/2026-10-26-pr19-rulings-and-equipment-confirmations.md)) and answers the OS and GPU/driver items in T-002. Because the PC runs `Windows 10 Home 22H2`, Windows 11's SDR automatic colour-management toggle (C-059) does not apply, while GPU LUTs, HDR, Night Light and HDMI range checks remain for T-002 and T-005.

## C-076

Updates C-008's delivery status and confirms the delivered unit matches the `SH-U35B` model and 3.5 mm Tip/Ring/Sleeve pin-out in S-026 (C-064; [S-032](briefs/2026-10-26-pr19-rulings-and-equipment-confirmations.md)). Because neither the leaflet (`A100033`) nor S-026 states a transceiver IC or voltage swing, electrical and protocol compatibility with the rear `EX-LINK` port remain Not tested and require a reviewed, authorised T-006 plan.
