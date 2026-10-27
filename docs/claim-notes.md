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

Bears on C-004. These are settings on the owner's PC, TV and receiver, made by the owner; no agent may send commands to the Denon (AGENTS.md section 7). S-002's black-level and clipping checks belong to T-005. Owner's active signal path and settings recorded in S-033 (C-079 to C-081) differ from C-044's proposed baseline in three ways: GPU output is Limited dynamic range (16–235), TV HDMI Black Level is Auto, and Denon Video Mode is Auto (rather than Bypass).

## C-045

The owner's own equipment, reported at second hand. Confirmed in S-032 (C-075) for the NVIDIA GTX 1080 GPU model and driver version. S-033 (C-084) records mixed PC usage (desktop, SDR streaming, gaming, and HDR) rather than confirming GeForce Now as the main use.

## C-046

D-001 already fixes Rec.709, D65 and BT.1886. The brightness bands, the black-level default and the pass marks are proposals for the owner to decide, not decisions (Q-014).

## C-051

**Superseded by D-006:** TV control is Ex-Link only, so S-002's network and infrared routes, including its £0 key-press fallback, are out of scope. Retained as history. If Ex-Link fails on this TV, any change of route is the owner's decision.

## C-052

Subsequently checked in S-015/C-057: the manufacturer-hosted PDF is accessible. Its bytes have not been compared with S-006; publisher hosting does not establish first publication date, exact-model applicability or firmware support.

## C-060

Documentary observations, not TV behaviour. Claude Code's inference that the table covers later models is consistent with these renamed controls/features, but the document does not establish exact-model applicability. This supports the caution in C-011/C-027 and bears on C-039's ranges. The owner's menu inspection in S-033 (C-077) offers an integer slider `-3..+3` without listing BT.1886 or other discrete gamma types, contrasting with the worksheet's listed types.

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

Qualifies C-041 and C-056 and corrects S-002 section 5 line 230: QLED `.ccss` files declare `TECHNOLOGY "Unknown"` (`ccss.c` L303–321 -> `disptech_unknown`, `disptechs.c` L393–396 `refr = 1`), causing `spotread.c` L1734 and `spyd2.c` L3235 to override lowercase `-y` into inline refresh-synchronised measurement unless uppercase `-Y n` is passed. `-N` warns as unsupported (`spyd2.c` L4088), the logfile name must not immediately follow `-O` (which takes an optional spectrum filename; `spotread.c` L1034), and X-011 records the static `-O` control flow, now settled at source level by Codex withdrawing its initial reading ([S-024 section 3.1](research/2026-10-26-antigravity-feasibility-study.md#31-comparison-with-the-claude-feasibility-report-s-002-anthropic-23-october-2026)).

## C-069

Direct driver constraint from `spyd2.c` (L2973–2980): Spyder3/4/5 hardware lacks a reset command, may enter a `"borked state if the driver is aborted"`, and may not clear on immediate restart. Physical USB replugging is an untested AI inference, so our wrapper must exit `spotread` cleanly rather than killing subprocesses mid-read.

## C-070

Confirms C-042's missing 2016 SUHD `.ccss` on 2026-10-26 (`SAM`: 307, `SEC`: 42 entries), shows `oeminst` omits quantum-dot LED, and clarifies why standard `spotread` logs cannot be re-scored: loading a `.ccss` sets `p->ccmat` to unity (`spyd2.c` L2347, L2386) and folds spectra into the `3x7` sensor matrix `p->cal_A` (L2248–2253), discarding the 7 raw sensor channels on output.

## C-071

Primary-manual confirmation for C-044's Denon `Video Mode: Bypass` step on the exact `AVC-X3800H` model, including the helpful side-effect that Denon suppresses its own on-screen volume/status overlays over video in `Bypass` (provided `Video Mode` is not locked out by an active `IMAX DTS` or `IMAX DTS:X` sound mode). Actual owner cabling and settings await T-002 and T-005.

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


## C-077

Owner's normal-menu picture controls, ranges and current values in the primary viewing picture mode (intended calibration target: Movie mode; mode active during inspection not explicitly stated) on the `UE49KS7000UXXU` with firmware `T-JZMDEUC-1270.1` ([S-033](briefs/2026-10-26-owner-equipment-checklist.md)). Confirms basic sliders (Backlight 0–20, Brightness 0–100, Contrast 0–100, Sharpness 0–100, Colour 0–100, Tint G50/R50), integer Gamma slider -3..+3 (a -3..+3 slider; no BT.1886 option reported), Warm2 selectable over standard HDMI (clarifying C-063's e-Manual note), 2-point White Balance (-50..+50, all 0), Custom Colour Space (RGBCYM with RGB sliders), the listed picture processing settings disabled (Smart LED, Auto Motion Plus, Dynamic Contrast, Clean View, Eco), and Apply Picture Settings to All Sources. 10-point white balance slider ranges, current values and enable state were not reported.

## C-078

Owner check T-001 settles disagreement X-003 at the descriptive menu level: the multi-point White Balance menu on the owner's UK `UE49KS7000UXXU` offers 10 points (labelled 10%, 20%... 100%), which are selectable with the Denon/PC input ([S-033](briefs/2026-10-26-owner-equipment-checklist.md)). This confirms Position A (HDTVTest review of UK KS7000) and disproves Position B (20 points from US KS8000) for the owner's unit. 10-point slider values, ranges and optical response on equipment remain untested pending Stage 4/5.

## C-079

Establishes the physical video path from the PC's GTX 1080 through the Denon AVC-X3800H receiver to the TV's external One Connect box: PC HDMI -> Denon HDMI In 'PC' -> Denon Monitor 1 (eARC) -> One Connect HDMI 4 ([S-033](briefs/2026-10-26-owner-equipment-checklist.md)). On the TV, the input is labelled 'Home Cinema' with Game Mode turned off, and no picture controls are greyed out in this configuration.

## C-080

Owner's PC display configuration in NVIDIA Control Panel and Windows 10 Home 22H2 ([S-033](briefs/2026-10-26-owner-equipment-checklist.md)): 3840×2160 @ 60 Hz, RGB, 8bpc, Limited dynamic range (16–235), Windows HDR Off, Night light Off, and no ICC profile loaded. No RGB lighting background utilities are running. Confirms both the 6 ft Ex-Link cable and Spyder5 USB cable reach from the PC without strain.

## C-081

Denon AVC-X3800H receiver configuration ([S-033](briefs/2026-10-26-owner-equipment-checklist.md)): firmware 6000-1060-0071-9831, Video Mode Auto, HDMI Upscaler Off, 4K/8K Signal Format Enhanced, and on-screen volume/status banners enabled over video playback. While Video Mode is currently Auto, C-071 notes switching to Bypass in a future test plan would guarantee zero video processing and suppress Denon overlays during measurements.

## C-082

Meter and software status on the owner's PC ([S-033](briefs/2026-10-26-owner-equipment-checklist.md)): Datacolor Spyder5Pro with original installer and activation serial retained (vendor software not installed). ArgyllCMS V3.5.0 is unpacked in the Downloads folder (exact path kept out of the repository under AGENTS.md section 11) and DisplayCAL is installed. When hanging by its USB cable draped over the top edge of the TV with the counterweight behind, the meter rests flat against the screen surface (clarifying S-011's description of the cap hanging beneath).

## C-083

PC-side serial port check for the DSD TECH SH-U35B Ex-Link cable ([S-033](briefs/2026-10-26-owner-equipment-checklist.md)): Windows Device Manager assigns `USB Serial Port (COM3)` to the FTDI chip when plugged into the PC with the TV end disconnected. This check was performed in response to Antigravity's checklist request (item 5; TV disconnected), which requested the PC-only USB plug-in, differing from the look-only text in docs/equipment.md on main and docs/tests/README.md. Prospective project policy for owner checks remains an open question under X-009. Communication with the TV remains Not tested pending an authorised T-006 plan.

## C-084

Provisional calibration targets and viewing preferences (Q-014, [S-033](briefs/2026-10-26-owner-equipment-checklist.md)): dim viewing room, target peak brightness 140–160 cd/m² for SDR Rec.709/D65/BT.1886, mixed usage (PC desktop, SDR streaming/movies, gaming, HDR), and initial calibration priority on Movie mode for the PC/Denon HDMI input (HDMI 4). Final black target and pass marks await T-003 and T-004.

## C-090

Codex (OpenAI) retrieved and read the official [ArgyllCMS V3.5.0 source ZIP](https://www.argyllcms.com/Argyll_V3.5.0_src.zip) on 27 October 2026 (S-037), SHA-256 `f8576ce5589fd15620abb73ff049ea31f55ddbd1bba6d1ffa87452658e7bc85f`. No Argyll executable was run and no downloaded source is committed. Identity with the earlier S-029 copy is unknown because that retrieval did not record a hash.

`spectro/spotread.c:464,1192` builds the instrument list for help and measurement launches. `spectro/icoms_nt.c:93–99,125–135` classifies Windows VCP/USBSER device names and probes fast serial devices. `spectro/inst.c:1455–1456,1499–1544` selects candidate baud rates and writes identification bytes. `Jamtop:41` and `spectro/Jamfile:101–102` enable fast serial support in the source build defaults. This establishes a source-level hazard, not that the owner's adapter classification or installed binary has been tested.

The [Environment documentation](https://www.argyllcms.com/doc/Environment.html#ARGYLL_EXCLUDE_SERIAL_SCAN) and bundled `doc/Environment.html:384–391` describe excluded port names separated by commas/semicolons. `spectro/icoms.c:580–624,640–656` parses that list and compares each token with the port path using exact `strcmp` at line 649. `ARGYLL_EXCLUDE_SERIAL_SCAN=1` is therefore not a Boolean disable-all setting and would not exclude a port named `COM3`. No exclusion setting has been tested on this installation.

[T-003](tests/T-003-meter.md) and [T-005](tests/T-005-signal-path.md) require both Ex-Link ends disconnected before any Argyll launch. [T-006](tests/T-006-exlink.md) prohibits ArgyllCMS/DisplayCAL and other discovery tools during the connected session. The future meter adapter and concurrent T-013/T-008 sessions need separately reviewed, verified isolation; a port exclusion alone is not currently accepted as that verification.

## C-091

S-037 `spectro/spotread.c:1150–1158` and bundled `doc/Environment.html:128–136` show that `ARGYLL_COLMTER_CAL_SPEC_SET` and `ARGYLL_COLMTER_COR_MATRIX` can supply a default external correction without an explicit `-X`. Codex identified this during the source check; no owner environment values were inspected. [T-003's isolated launch environment](tests/T-003-meter.md#isolated-launch-environment), also required by T-005, records their presence privately and removes them only from the dedicated future test shell before launching Argyll. Persistent defaults remain unchanged. This is a proposed setup procedure, not proof of generic-only readings or correction accuracy on the owner's equipment.
