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
