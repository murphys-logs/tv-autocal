# Claude feasibility report (23 October 2026)

| Field | Value |
|---|---|
| Title | Samsung UE49KS7000 auto-calibration: feasibility and design |
| Produced by | Claude (Anthropic) |
| Original date | 2026-10-23, from the date line at the top of the document |
| Imported | 2026-10-25, by Claude Code (Anthropic) |
| How obtained | Pasted by the owner into a Claude Code conversation on 25 October 2026, copied from a Claude Docs document (the owner's answer, S-013). Claude Code had no access to the document or to the conversation that produced it |
| Fidelity | Verbatim as pasted, with one change made at the owner's request (D-012): the owner's name in the byline on the second line, written there as an @ mention, is replaced (with its @ sign) by "[owner's name removed]". Two embedded items, a run-time chart in section 8 and an architecture diagram in section 11, did not come through the paste; they appear only as the placeholder lines the paste contained. Item 8 of the "Blind navigation design" list in section 3 was later removed at the owner's instruction (D-013); the marker "\[removed under D-013\]" shows where. The text cut under D-013 is in commit 337a58f1ac81e5359e9c9d762b06717b156313d0, and it stays there only while git history is left intact (Q-017). The name was removed before the first commit, so this repository holds no uncut copy of the name |
| Ledger ID | S-002 |

**Every statement in this report is an AI hypothesis (provenance `AI: Claude`), including those it labels \[V\] "verified".** No agent in this repository has yet checked its citations, and **nothing in it has been tested on the owner's equipment.** Where it differs from the owner's later decisions, the decisions win: in particular, TV control is Ex-Link only (D-006), so the report's network key-press and infrared routes are out of scope, and every reading follows the owner's measurement cycle: change a setting, exit the menu, wait a short delay, then read (D-013). The report's service-menu and infrared steps are not authorised ([AGENTS.md section 7](../../AGENTS.md#7-equipment-safety-rule-6)). The claims taken from it, and how they relate to the rest of the project, are in [LEDGER.md](../../LEDGER.md#claims-from-the-claude-feasibility-report-s-002).

Everything below the line is the original. Do not edit it.

---

# Samsung UE49KS7000 auto-calibration: feasibility and design

Oct 23, 2026 · [owner's name removed]

## 1. Verdict and corrected premises

Feasible. Every SDR stage can be automated with the kit you own, and about £17 of serial parts upgrades the crux from blind key presses to direct values. HDR is only partly feasible, and the Spyder 5, not the TV, caps the accuracy.

Labels: **\[V\]** verified (documented or measured), **\[R\]** reported (owner or forum anecdote), **\[I\]** inferred (my reasoning).

| Stage | Verdict | Deciding evidence |
| --- | --- | --- |
| Measurement automation | Feasible | spotread -O exists for scripted single readings, and ArgyllCMS applies CCSS spectral correction to the Spyder 5 \[V\] ([spotread](https://www.argyllcms.com/doc/spotread.html), [instruments](https://www.argyllcms.com/doc/instruments.html)) |
| 2-point white balance | Feasible | Calman autocalibrates this TV generation's 2-point controls over Ex-Link \[V\] ([Portrait KB](https://kb.portrait.com/help/samsung-2016-suhd-tvs-c67d5bca)); network key presses work on 2016 sets as a £0 fallback \[V\] ([HA docs](https://git.jeena.net/jeena/home-assistant.github.io/src/branch/rc/source/_components/media_player.samsungtv.markdown)); the meter is strong at 20 and 80% |
| Multi-point white balance | Feasible, with caveats | Calman calibrates it too \[V\]; sources disagree on 10 or 20 points, and HDTVTest found the points "contrast-aligned" on its sample, so the program maps each point's effect first \[V\] ([HDTVTest](https://www.hdtvtest.co.uk/news/ue49ks7000-201610234374)) |
| Gamma (EOTF) | Feasible above about 10% stimulus | Slider plus multi-point shaping reach BT.1886; the meter cannot verify anything darker than about 0.3 cd/m2 \[I\] from \[V\] ([ChromaPure](https://chromapure.com/newgear-new.asp)) |
| CMS | Feasible | Custom colour space with six colours x three sliders, settable on both routes; HDTVTest brought 137 of 140 patches under dE 3 with it \[V\]; accuracy on saturated quantum-dot colours is limited by the meter \[I\] |
| HDR10 | Partly feasible | White balance works in HDR \[V\] ([HDTVTest](https://www.hdtvtest.co.uk/news/ue49ks7000-201610234374)), but power limiting, an unknown meter ceiling and no HDR CMS limit it to a greyscale touch-up and a PQ check; even Calman supports only SDR on 2016 SUHD sets \[V\] ([Portrait KB](https://kb.portrait.com/help/samsung-2016-suhd-tvs-c67d5bca)) |

### Premises checked

- **Budget:** a £0 route exists (network key presses). The recommended Ex-Link route costs about £16.70, or £19.80 with a contingency adapter (section 14).
- **Control (the crux):** better than the brief assumed. A documented direct-value route exists on this TV generation, and you need not rely on blind key emulation. Nothing reads settings back, so the meter confirms every change.
- **Meter:** cannot read black or anything darker than about 5% stimulus on this panel, and reads 10% only noisily; absolute accuracy about dE 1.5 to 2 with the best CCSS available; Datacolor's vendor data is not needed for spectral correction; HDR ceiling unpublished. "Highest standard" therefore means reference-grade tracking as the meter sees it, not reference-grade absolute accuracy.
- **Model and panel:** confirmed. UE49KS7000 (US KS8000), RGB-stripe VA, bottom-edge LEDs, quantum-dot film, Tizen 2.4; the One Connect Mini carries the HDMI inputs, and the TV has a 3.5 mm RS-232 Ex-Link jack.
- **Multi-point white balance:** may be 10 or 20 points on your firmware; check before building stage 5.

## 2. The TV

Your set is almost certainly the UE49KS7000, and its normal user menu already holds every control a calibration needs: 2-point and 10-point white balance, a gamma slider and a full colour management system (CMS). The service menu is not needed.

### Identity and hardware

- **Backlight:** LEDs along the bottom edge, through a quantum-dot film; Smart LED dims in 10 full-height columns, with at least five lit at any time \[V\] ([HDTVTest](https://www.hdtvtest.co.uk/news/ue49ks7000-201610234374)). Expect narrow red and green spectral peaks, which is what trips filter colorimeters \[I\].
- **Black and contrast:** 0.04 cd/m2 on a 4x4 ANSI chequerboard with peak white at 120 cd/m2, about 3,000:1; black level only stays stable with Smart LED off \[V\] ([HDTVTest](https://www.hdtvtest.co.uk/news/ue49ks7000-201610234374)).
- **Firmware:** EU family T-JZMDEUC (Tizen 2.4), shared with the KS8000 and KU6670; versions 1240.0 to 1243.2 were circulating in 2021 \[R\] ([SamyGO](https://forum.samygo.tv/viewtopic.php?p=100846), [SamyGO](https://forum.samygo.tv/viewtopic.php?p=109445)). Read yours from the Support menu.
- **Light output:** SDR full-field 579 cd/m2; HDR peak 1,380 cd/m2 held for about 19 s, then sagging over 16 s to 570 cd/m2 through power limiting \[V\] ([HDTVTest](https://www.hdtvtest.co.uk/news/ue49ks7000-201610234374)).
- **Model:** UE49KS7000 (UK suffixes U and S); the US equivalent is the KS8000, and the curved twin is the KS7500 \[V\] ([HDTVTest](https://www.hdtvtest.co.uk/news/ue49ks7000-201610234374), [Kitele](https://www.kitele.com/en/tv-samsung-ue49ks7000)). A flat 49-inch 2016 set with a One Connect Mini can only be a KS7000 \[I\].
- **Native gamut:** 94% of DCI-P3 measured \[V\] ([HDTVTest](https://www.hdtvtest.co.uk/news/ue49ks7000-201610234374)).
- **Panel:** RGB-stripe VA, confirmed by macro photo \[V\] ([HDTVTest](https://www.hdtvtest.co.uk/news/ue49ks7000-201610234374)); marketed as 10-bit \[R\] ([Richer Sounds](https://blog.richersounds.com/?p=29336)).
- **Ports that matter:** four HDMI 2.0 on the One Connect Mini \[V\] ([Samsung](https://www.samsung.com/in/support/tv-audio-video/what-are-the-ports-available-in-samsung-one-connect-box/)); Ethernet and an RS-232 Ex-Link port \[V\] ([Expert Reviews](https://www.expertreviews.co.uk/samsung/1405210/samsung-ue49ks7000-review-an-amazing-4k-hdr-smart-tv-for-gaming-and-more-1/2)), reported on the TV body rather than the box \[R\] ([listing](https://www.finn.no/451056523)).

### Calibration controls

Ranges come from Samsung's consumer Ex-Link command sheet, which lists the value range of each control \[V\] ([Samsung](https://image-us.samsung.com/SamsungUS/samsungbusiness/tv-ci-resources/Samsung-RS232-Control.pdf)); that sheet covers later models too, so confirm each range on your set.

| Control | Range and step | Calibration setting | Basis |
| --- | --- | --- | --- |
| Auto Motion Plus (incl. LED Clear Motion) | Off, Clear, Standard, Smooth, Custom | Off: LED Clear Motion is black frame insertion and dims the image | \[V\] [HDTVTest](https://www.hdtvtest.co.uk/news/ue49ks7000-201610234374) |
| Backlight | 0 to 20, step 1 | Sets peak white; first coarse control | \[R\] [owner settings](https://www.elotrolado.net/hilo_ayuda-configuracion-tv-samsung-ks7000_2192904_s1100) |
| Brightness | 0 to 100, step 1 | Black level; set by PLUGE, then left | \[R\] [owner settings](https://www.elotrolado.net/hilo_ayuda-configuracion-tv-samsung-ks7000_2192904_s1100) |
| Colour | 0 to 100, step 1 | Default, then CMS does the work | \[V\] [Samsung sheet](https://image-us.samsung.com/SamsungUS/samsungbusiness/tv-ci-resources/Samsung-RS232-Control.pdf) |
| Colour Space | Auto, Native, Custom; Custom picks red, green, blue, cyan, magenta or yellow, each with Red, Green and Blue sliders 0 to 100 | Auto first; Custom for CMS | \[V\] [Samsung sheet](https://image-us.samsung.com/SamsungUS/samsungbusiness/tv-ci-resources/Samsung-RS232-Control.pdf), [HDTVTest](https://www.hdtvtest.co.uk/news/ue49ks7000-201610234374) |
| Colour Tone | Cool, Standard, Warm1, Warm2 | Warm2, nearest D65 | \[V\] [RTINGS](https://www.rtings.com/tv/reviews/samsung/ks8000/settings) |
| Contrast | 0 to 100, step 1 | Highest value with no channel clipping | \[V\] [Samsung sheet](https://image-us.samsung.com/SamsungUS/samsungbusiness/tv-ci-resources/Samsung-RS232-Control.pdf) |
| Digital Clean View | Off, Auto | Off | \[V\] [RTINGS](https://www.rtings.com/tv/reviews/samsung/ks8000/settings) |
| Dynamic Contrast (later called Contrast Enhancer) | Off, Low, High | Off | \[R\] [owner settings](https://www.elotrolado.net/hilo_ayuda-configuracion-tv-samsung-ks7000_2192904_s1100) |
| Eco Solution: Eco Sensor (ambient light), Energy Saving, Motion Lighting | On or off each | All off; Eco Sensor ships on in Standard mode | \[V\] [HDTVTest](https://www.hdtvtest.co.uk/news/ue49ks7000-201610234374) |
| Gamma | -3 to +3, step 1 (SDR); ST.2084 slider in HDR | Coarse EOTF trim; 10-point does the fine shaping | \[R\] [owner settings](https://www.elotrolado.net/hilo_ayuda-configuracion-tv-samsung-ks7000_2192904_s1100) |
| HDMI Black Level | Auto, Low, Normal | Low for limited-range signals (see section 6) | \[V\] values; \[I\] meaning |
| HDMI UHD Colour | On or off per HDMI input | On for 2160p60 4:4:4 and 10-bit HDR | \[V\] [HDTVTest](https://www.hdtvtest.co.uk/news/ue49ks7000-201610234374), [RTINGS](https://www.rtings.com/tv/reviews/samsung/ks8000/settings) |
| HDR+ Mode | On or off | Off | \[V\] [RTINGS](https://www.rtings.com/tv/reviews/samsung/ks8000/settings) |
| Picture Mode | Dynamic, Standard, Natural, Movie | Movie: closest to target, least processing | \[V\] [RTINGS](https://www.rtings.com/tv/reviews/samsung/ks8000/settings), [HDTVTest](https://www.hdtvtest.co.uk/news/ue49ks7000-201610234374) |
| RGB Only Mode | Off, Red, Green, Blue | Off (visual aid only) | \[V\] [Samsung sheet](https://image-us.samsung.com/SamsungUS/samsungbusiness/tv-ci-resources/Samsung-RS232-Control.pdf) |
| Sharpness | 0 to 100 | 0; no colour effect | \[R\] [owner settings](https://www.elotrolado.net/hilo_ayuda-configuracion-tv-samsung-ks7000_2192904_s1100) |
| Smart LED (local dimming) | Off, Low, Standard, High | Off, or black and white drift with picture content | \[V\] [HDTVTest](https://www.hdtvtest.co.uk/news/ue49ks7000-201610234374) |
| Tint | G/R balance about a centre point | Centre | \[V\] [Samsung sheet](https://image-us.samsung.com/SamsungUS/samsungbusiness/tv-ci-resources/Samsung-RS232-Control.pdf) |
| White Balance, 2-point | R, G, B Offset and Gain, -50 to +50, step 1 | Main greyscale tool | \[V\] [Samsung sheet](https://image-us.samsung.com/SamsungUS/samsungbusiness/tv-ci-resources/Samsung-RS232-Control.pdf) |
| White Balance, 10-point | Interval 1 to 10 (10% to 100%); R, G, B -50 to +50 each | Fine greyscale and EOTF shaping | \[V\] [Samsung sheet](https://image-us.samsung.com/SamsungUS/samsungbusiness/tv-ci-resources/Samsung-RS232-Control.pdf), [HDTVTest](https://www.hdtvtest.co.uk/news/ue49ks7000-201610234374) |

**Conflict flagged:** HDTVTest calls the UK set's multi-point control 10-point, and found it "contrast-aligned" and unhelpful on its sample; RTINGS lists 20-point for the US KS8000 \[V\] ([HDTVTest](https://www.hdtvtest.co.uk/news/ue49ks7000-201610234374), [RTINGS](https://rtings.com/tv/tools/compare/samsung-ks8000-samsung-nu8000/291/586)). The program must count the points itself and map which stimulus levels each one moves, rather than assume point n equals n x 10%.

**Not confirmed for 2016:** a BT.1886 gamma preset. Samsung's later sets have one; owner settings for this set show only the slider \[R\]. Treat BT.1886 as a target the program reaches with the slider plus 10-point, not as a menu option.

### How settings are stored

- Full 4:4:4 works at 1080p and 2160p60 with the PC icon and HDMI UHD Colour on \[V\] ([HDTVTest](https://www.hdtvtest.co.uk/news/ue49ks7000-201610234374)). Which expert controls PC and Game modes lock out is not documented; check on the set.
- Game Mode sits under Special Viewing Mode \[V\] ([RTINGS](https://www.rtings.com/tv/reviews/samsung/ks8000/settings)). Lag: 22 ms Game, 37 ms with the PC input icon, 128 ms Movie \[V\] ([HDTVTest](https://www.hdtvtest.co.uk/news/ue49ks7000-201610234374)).
- HDR signals load their own settings, calibrated separately \[V\] ([HDTVTest](https://www.hdtvtest.co.uk/news/ue49ks7000-201610234374) calibrated white balance again in HDR Movie mode).
- Picture settings belong to a picture mode on an input; Apply Picture Settings switches between Current Source and All Sources \[V\] ([Samsung sheet](https://image-us.samsung.com/SamsungUS/samsungbusiness/tv-ci-resources/Samsung-RS232-Control.pdf)).
- Rule for the program: calibrate the exact input, input icon and picture mode you watch through, because the result does not carry to other combinations \[I\].

### Service menu

- **Contents:** a white balance page with Sub Brightness, Sub Contrast and R, G, B offset and gain on wide numeric scales, for example 128 to 164 on an ES7000 \[R\] ([SamyGO](https://forum.samygo.tv/viewtopic.php?p=64672)); K-series owners mention a WBMovie entry \[R\] ([SamyGO](https://forum.samygo.tv/viewtopic.php?p=105755)).
- **Entry:** with the TV in standby, press Mute, 1, 8, 2, Power on a basic Samsung IR remote \[V\] ([Samsung sheet](https://image-us.samsung.com/SamsungUS/samsungbusiness/tv-ci-resources/Samsung-RS232-Control.pdf)). The 2016 Smart Control has no number keys; an IR blaster can send the factory key (code 0x3B in Samsung's key map) instead \[V\] code, \[I\] that it opens the menu on this set.
- **Finer control?** Probably finer steps, but this is the factory base under every picture mode \[I\]. The user menu's -50 to +50 already gives fine enough steps (section 13).
- **Real risks:** an accidental factory reset wiped a 40KU6072's factory ADC and white balance, with no restore \[R\] ([SamyGO](https://forum.samygo.tv/viewtopic.php?p=105670)); toggling Option, Type resets the advanced settings \[R\] ([SamyGO](https://forum.samygo.tv/viewtopic.php?p=105734)); switching the RS-232 jack from Debug to UART removes the debug path you would need to recover a bricked set \[R\] ([SamyGO](https://forum.samygo.tv/viewtopic.php?p=113512)).
- **Verdict:** keep it out of the program's normal path. If ever used, photograph every page first and never touch anything labelled Reset.

### HDR10

- Meaningful HDR work is limited to greyscale at mid PQ levels and an EOTF check; gamut and CMS work in HDR is beyond this meter (section 5) \[I\].
- Tone mapping is fixed, and the power limiter makes large bright windows sag within about 35 s \[V\]. Readings above about 500 cd/m2 must be quick, with cool-down pauses \[I\].
- White balance controls stay active in HDR: HDTVTest calibrated RGB tracking in HDR Movie mode and checked PQ tracking against ST.2084 \[V\] ([HDTVTest](https://www.hdtvtest.co.uk/news/ue49ks7000-201610234374)).

## 3. Controlling the TV from the PC

Two routes can change white balance on this set: menu key presses over the network (free but slow) and Ex-Link serial commands (direct values, about £17 of parts). Calman's documented autocalibration of 2016 SUHD sets over Ex-Link proves the second route exists; the exact 2016 command encoding still needs confirming with a probe. No route reads settings back, so the meter serves as the readback.

### Every route assessed

| Route | What it can do on this set | Set or step | Readback | Verdict | Basis |
| --- | --- | --- | --- | --- | --- |
| Ex-Link RS-232 (3.5 mm jack on the TV) | Samsung's consumer sheet lists direct-value commands for picture mode, backlight, contrast, gamma, 2-point and 10-point white balance, CMS, colour tone, local dimming, HDMI black level, key presses and OSD off; success reply 03 0C F1. One KS7000 owner who had switched the jack to Debug saw console output but no response to commands; a SamyGO moderator says UART mode is needed | Direct absolute set | None (acknowledge only) | Recommended route: Calman autocalibrates this TV generation through this port (see below); the 2016 command encoding needs a probe, and the jack's service-menu mode may need checking | \[V\] [Samsung sheet](https://image-us.samsung.com/SamsungUS/samsungbusiness/tv-ci-resources/Samsung-RS232-Control.pdf); \[R\] [SamyGO](https://forum.samygo.tv/viewtopic.php?p=107013), [SamyGO](https://forum.samygo.tv/viewtopic.php?p=113512) |
| HDMI-CEC | PC graphics cards have no CEC; a USB adapter costs about $54; CEC carries only remote-key codes anyway | Step | None | Not viable (over budget, no gain) | \[V\] [AnandTech](https://www.anandtech.com/show/5463), [NVIDIA forum](https://forums.developer.nvidia.com/t/hdmi-cec-support/31445), [price](https://moveonup.csd.auth.gr/products/usb-hdmi-cec-adapter/218487134/) |
| Infrared blaster | Samsung's key map has discrete codes, including the factory key 0x3B; a microcontroller and IR LED fit the budget | Step | None | Fallback, and the only automatic way into the service menu | \[V\] [Samsung sheet](https://image-us.samsung.com/SamsungUS/samsungbusiness/tv-ci-resources/Samsung-RS232-Control.pdf) key map; \[I\] hardware |
| MDC (port 1515) | Samsung's control protocol for commercial and signage displays; libraries state it is not for TV sets | None | n/a | Not viable | \[V\] [samsung-lfd](https://npmjs.com/package/samsung-lfd); \[R\] [AMX forum](https://proforums.harman.com/amx/discussion/comment/199945) |
| SmartThings cloud | 2016 sets could be added in 2017; power, volume, picture mode and sound mode worked; no sliders or white balance | Picture mode only | Picture mode only, often stale | Not useful | \[R\] [SmartThings community](https://community.smartthings.com/t/samsung-2016-smart-tvs-as-devices/79181), [stale state](https://community.smartthings.com/t/the-api-does-not-return-the-current-picturemode/308861) |
| Tizen network remote (WebSocket) | Any remote key; device info JSON at :8001/api/v2/. 2016 K-series sets answer on port 8001; after some 2016 firmware updates only 8002 with a token worked. One-off on-screen Allow prompt; same subnet required | Step | Device info only | Primary route, £0 | \[V\] [HA docs 2017](https://git.jeena.net/jeena/home-assistant.github.io/src/branch/rc/source/_components/media_player.samsungtv.markdown), [openHAB](https://v50.openhab.org/addons/bindings/samsungtv/), [samsungtvws](https://pypi.org/project/samsungtvws); \[R\] [HA issue 17802](https://github.com/home-assistant/core/issues/17802), [HA community](https://community.home-assistant.io/t/samsung-smart-tv-no-control/32914?page=11) |
| Undocumented or rooted interfaces | Community rooting work exists for these sets, but it relies on exploits and changes the system | n/a | n/a | Excluded by your no-modification rule | \[R\] [SamyGO](https://forum.samygo.tv/viewtopic.php?p=98698) |
| UPnP RenderingControl | Brightness, contrast, sharpness and colour temperature channels work only on pre-2016 (legacy) sets | None | None | Not viable; probe once and log, at no cost | \[V\] [openHAB](https://v50.openhab.org/addons/bindings/samsungtv/) |

**Why Ex-Link is the recommended route:** Portrait Displays documents Calman connecting to 2016 SUHD sets through a 3.5 mm Ex-Link cable (tip to DB9 pin 2, ring to pin 3, sleeve to pin 5, via an FTDI USB-RS232 adapter) and automatically calibrating their 2-point, multi-point and CMS controls in SDR. Its guide lists no service-menu step \[V\] ([Portrait KB](https://kb.portrait.com/help/samsung-2016-suhd-tvs-c67d5bca)). Calman's own protocol is not published, so the program's first Ex-Link task is a harmless probe: power, then picture mode, then a single 2-point gain step confirmed by the meter. That shows whether Samsung's public command table works on your firmware \[I\]. Look for the 3.5 mm jack, labelled Ex-Link or External Sync, on the TV's rear panel or the One Connect Mini.

Practical notes on the primary route: openHAB queues keys with a 300 ms default gap, and Wake-on-LAN power-on works on 2016+ sets with quirks \[V\] ([openHAB](https://v50.openhab.org/addons/bindings/samsungtv/)). WebSocket control fails across subnets or VLANs \[V\] ([HA docs](https://www.hasscn.top/home-assistant/integrations/samsungtv)). Expect 0.3 s per key plus about 1 s of menu animation per page change \[I\].

### Blind navigation design (key emulation)

1. **Known start state.** Send Exit three times, wait 1.5 s, open the menu, then press Up more times than the list is long. The teach stage confirms the lists do not wrap round.
2. **Menu map as data.** Each control's path (Picture, Expert Settings, White Balance, 10p, Interval) lives in a file per firmware version. A one-off teach wizard builds it: the program sends one key, you confirm what is highlighted, and it records the path.
3. **Absolute values without readback.** Re-zero a slider by pressing Left more times than its range (111 presses for -50 to +50), then count up to the target. After that, track position by counting, and re-zero whenever a measurement disagrees.
4. **Pacing.** Single clicks only, 300 ms apart by default, never press-and-hold, which accelerates sliders \[I\]. Widen the gap automatically after any failed check.
5. **Measurement confirms every change.** The sensitivity model (section 8) predicts what each step should do. A miss beyond 3 standard deviations of meter noise triggers re-home and re-zero; two misses in a row stop the run and ask you.
6. **Time-outs and lost menus.** Never rely on a menu staying open. Each adjustment is a self-contained open, navigate, adjust, close, and every key goes in the journal.
7. **On-screen menus versus readings.** Put the meter where menus never draw (centre of screen; check). At start-up, read the same patch with the menu shut and open: a difference above 0.5% in luminance or 0.0005 in u'v' means the program closes the menu before every reading, at about 2 s extra each time. The Ex-Link route can switch the OSD off entirely \[V\] ([Samsung sheet](https://image-us.samsung.com/SamsungUS/samsungbusiness/tv-ci-resources/Samsung-RS232-Control.pdf)).
8. \[removed under D-013\]

### Backup and rollback

- Before the first run, photograph every Expert Settings and White Balance page for the input and mode in use. That is the baseline.
- Each run ends with a settings card: the final absolute value of every control it touched, which you can re-enter by hand.
- Nothing can read this set's picture settings: the UPnP picture channels are legacy-only and Samsung's Ex-Link sheet has no read commands \[V\] ([openHAB](https://v50.openhab.org/addons/bindings/samsungtv/), [Samsung sheet](https://image-us.samsung.com/SamsungUS/samsungbusiness/tv-ci-resources/Samsung-RS232-Control.pdf)).
- Rollback: Reset Picture for that mode restores Samsung's defaults \[V\] (listed in the [Samsung sheet](https://image-us.samsung.com/SamsungUS/samsungbusiness/tv-ci-resources/Samsung-RS232-Control.pdf)); then re-enter the baseline photos or an earlier card.
- The program never touches other inputs, other picture modes or the service menu unless you switch that option on.
- The program writes a journal line per change: time, control, intended absolute value, keys sent, measured result.

## 4. Capability matrix

Every calibration control is reachable step by step over the network for £0; Ex-Link makes almost all of them directly settable; Calman does exactly that on 2016 SUHD sets, though the public command encoding still needs confirming on your firmware. Nothing is readable except through its measured effect.

Key: **Step** = menu key presses, value tracked by counting. **Set** = absolute value in one command. **Set\*** = in Samsung's consumer Ex-Link sheet; Calman controls these on 2016 SUHD sets, but the public encoding is unconfirmed on 2016 firmware and ranges may differ. CEC, MDC and UPnP control nothing on this set (section 3), so they get no column.

| Control | Range and step | WebSocket keys (£0) | IR blaster | Ex-Link | SmartThings | Readable | Risk |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Auto Motion Plus, LED Clear Motion | Off to Custom; On or off | Step | Step | Set\* | No | No | Low |
| Backlight | 0 to 20, step 1 | Step | Step | Set\* | No | Via meter | Low |
| Brightness | 0 to 100, step 1 | Step | Step | Set\* | No | Via meter (weak near black) | Low |
| Colour | 0 to 100, step 1 | Step | Step | Set\* | No | Via meter | Low |
| Colour Space Custom (CMS) | 6 colours x R, G, B sliders, 0 to 100 | Step | Step | Set\* | No | Via meter | Low |
| Colour Space mode | Auto, Native, Custom | Step | Step | Set\* | No | Via meter | Low |
| Colour Tone | Cool, Standard, Warm1, Warm2 | Step | Step | Set\* | No | Via meter | Low |
| Contrast | 0 to 100, step 1 | Step | Step | Set\* | No | Via meter | Low |
| Digital Clean View | Off, Auto | Step | Step | Set\* | No | No | Low |
| Dynamic Contrast | Off, Low, High | Step | Step | Set\* | No | Via meter (drift) | Low |
| Eco Sensor, Motion Lighting | On or off | Step | Step | Set\* | No | Via meter (drift) | Low |
| Energy Saving Mode | Off to High | Step | Step | Step (key codes) | No | Via meter | Low |
| Gamma | -3 to +3, step 1 | Step | Step | Set\* | No | Via meter | Low |
| HDMI Black Level | Auto, Low, Normal | Step | Step | Set\* | No | Via meter and PLUGE | Low; wrong value crushes or lifts black |
| HDMI UHD Colour | On or off per input | Step | Step | Set\* | No | No | Low; input re-syncs |
| HDR+ Mode | On or off | Step | Step | Set\* | No | Via meter | Low |
| Picture Mode | Dynamic, Standard, Natural, Movie | Step | Step | Set\* | Set \[R\] | SmartThings, often stale | Low |
| Reset Picture | One action per mode | Step (confirm dialog) | Step | Set\* | No | n/a | Medium: wipes that mode's settings |
| RGB Only Mode | Off, R, G, B | Step | Step | Set\* | No | Via meter | Low |
| Service-menu white balance | Wide numeric scales | Untested over network | Step (factory key) | No | No | Shown on screen only | High: factory base for every mode |
| Sharpness | 0 to 100, step 1 | Step | Step | Set\* | No | No | Low |
| Smart LED | Off, Low, Standard, High | Step | Step | Set\* | No | Via meter (drift) | Low |
| Tint | G/R about centre | Step | Step | Set\* | No | Via meter | Low |
| White Balance, 2-point | 6 sliders, -50 to +50, step 1 | Step | Step | Set\* | No | Via meter | Low |
| White Balance, 10-point | 10 levels x R, G, B, -50 to +50, step 1 | Step | Step | Set\* | No | Via meter | Low |

Sources: ranges and Ex-Link coverage from [Samsung's consumer RS-232 sheet](https://image-us.samsung.com/SamsungUS/samsungbusiness/tv-ci-resources/Samsung-RS232-Control.pdf) \[V\]; SmartThings picture mode from the [SmartThings community](https://community.smartthings.com/t/samsung-2016-smart-tvs-as-devices/79181) \[R\]; no readback from [openHAB](https://v50.openhab.org/addons/bindings/samsungtv/) \[V\].

## 5. Measurement with the Spyder 5

ArgyllCMS can drive the Spyder 5 entirely from code, and with a quantum-dot spectral correction it should read white to within roughly 0.003 to 0.006 in xy. Its weak spots are speed and anything below about 0.3 cd/m2, which rules out measuring black and the bottom 5 to 10% of the greyscale.

### Set-up on Windows

1. Unzip ArgyllCMS to a folder with no spaces (for example C:\\Argyll) and add its bin folder to PATH \[V\] ([ArgyllCMS](https://www.argyllcms.com/doc/Installing_MSWindows.html)).
2. The Spyder 5 is not a HID device, so run usb\\ArgyllCMS\_install\_USB.exe, accept the UAC prompt and re-plug the meter. If Datacolor's software is installed, switch the driver in Device Manager, or keep one USB port per driver \[V\] ([ArgyllCMS](https://www.argyllcms.com/doc/Installing_MSWindows.html)).
3. Disable RGB-lighting services such as Logitech LampArray, Gigabyte RGBFusion and MSI Center, which are reported to block instrument access \[V\] ([ArgyllCMS](https://www.argyllcms.com/doc/Installing_MSWindows.html)).
4. Optional: run oeminst on Datacolor's Spyder 5 installer to unlock Datacolor's display types (f, L, e, B, x). This is **not** needed for spectral correction: Argyll accepts CCSS files for the Spyder 4 and 5 "as an alternative" \[V\] ([oeminst](https://www.argyllcms.com/doc/oeminst.html), [instruments](https://www.argyllcms.com/doc/instruments.html)).
5. Express, Pro and Elite: Pro and Elite are identical hardware; the Express only lacks the ambient sensor, which display readings do not use \[V\] ([instruments](https://www.argyllcms.com/doc/instruments.html)).
6. Check with spotread -? that the Spyder 5 and its display types are listed.

### Spectral correction for the quantum-dot backlight

- Best available: DisplayCAL's bundled "LCD Quantum Dot LED (Samsung QLED Q9)" CCSS. DisplayCAL's author advised exactly this one over the RGB-LED and white-LED families for a KS7000 \[R\] ([DisplayCAL forum](https://hub.displaycal.net/forums/topic/i1-display-pro-for-quantum-dots-led-display-calibration/)). The community database may hold closer matches \[V\] ([database](https://colorimetercorrections.displaycal.net)).
- **Conflict flagged:** one DisplayCAL forum reply says Spyders use built-in modes rather than spectral corrections \[R\] ([forum](https://hub.displaycal.net/forums/topic/color-correction-and-instument-mode/)); ArgyllCMS's own documentation says the Spyder 4 and 5 accept CCSS \[V\]. Follow Argyll, and have the program confirm spotread accepts -X before trusting any reading.
- Error with it: ChromaPure measured the SpyderX at 0.003 to 0.006 average xy error (dE 1.3 to 2.0) across display types, and the Spyder 5 matched or slightly beat it at 10% stimulus and above \[V\] ([ChromaPure](https://chromapure.com/newgear-new.asp)). Treat that as the absolute floor with a well-matched CCSS \[I\].
- Error without it: owners report a Spyder and an i1 Display disagreeing by 500 to 600 K on the same wide-gamut screen \[R\] ([forum](https://hub.displaycal.net/forums/topic/for-srgb-workflow-is-srgb-only-monitor-better-than-adobergb/page/2/)). Expect several dE2000 of white error with a generic mode \[I\].
- I found no CCSS measured on a 2016 SUHD set. Argyll's contributed list holds only a MacBook Pro file \[V\] ([ArgyllCMS](https://www.argyllcms.com/doc/ccsss.html)).
- Relative greyscale tracking is far less sensitive to the CCSS choice than absolute white, because every grey shares nearly the same spectral mix \[I\]. The program keeps the CCSS swappable and stores raw readings so a run can be re-scored later.
- The Spyder 4 and 5 are calibrated from their sensors' spectral sensitivities, so a CCSS file describing the display's spectra sets the calibration; spotread takes it with -X file.ccss \[V\] ([spotread](https://www.argyllcms.com/doc/spotread.html)).

### Realistic performance on this TV

- **Averaging and rejection:** repeat each reading until the standard error of Y is under 0.3% and of x and y under 0.0005, up to 8 readings; use the median; drop readings more than 3 median absolute deviations out, and any zero, negative or clipped value \[I\].
- **HDR ceiling:** I found no published maximum for the Spyder 5; Datacolor rates its current models at about 750 or 2,000 cd/m2 \[V\] ([Datacolor](https://spyder-support.datacolor.com/hc/en-us/articles/15888461682332)). The program must test for saturation before any HDR reading.
- **Low-light floor:** the SpyderX is more than 10 times as sensitive as the Spyder 5 and is usable to about 0.028 cd/m2 \[V\] ([ChromaPure](https://chromapure.com/newgear-new.asp)), which puts the Spyder 5 near 0.3 cd/m2 \[I\]. When it does read black, it reads high and fluctuates \[R\] ([forum](https://hub.displaycal.net/forums/topic/contrast-ratio-reported-as-17001-when-it-could-be-higher-spyder5-limitation/)). With 120 cd/m2 peak and BT.1886 on this panel's 0.04 cd/m2 black, 5% stimulus is about 0.3 cd/m2 and 10% about 0.9 cd/m2 \[I\]. So 0 to 5% sits at or under the floor, 10% needs heavy averaging, and Brightness is set by eye on a PLUGE.
- **Settle time:** after a pattern change, wait 1 s, then read until two consecutive readings agree within noise; after a TV control change, wait 1 s once the menu has closed \[I\]. Movie mode adds 128 ms of processing delay \[V\] ([HDTVTest](https://www.hdtvtest.co.uk/news/ue49ks7000-201610234374)).
- **Speed:** the i1 Display Pro is 4 to 5 times faster than the Spyder 5 \[R\] ([forum](https://hub.displaycal.net/forums/topic/best-monitor-calibrator/)); the SpyderX is twice as fast \[V\] ([ChromaPure](https://chromapure.com/newgear-new.asp)). Budget 2 to 4 s per bright reading, longer in shadows, plus 1 to 3 s to open the meter on each spotread call \[I\].
- **Warm-up and drift:** warm the TV for 45 minutes on a mid-grey field, with the meter resting on the screen for the last 15; start only when white drifts less than 0.5% in 5 minutes. Re-read a 75% reference every 10 minutes and pause if it moves more than 1% or 0.001 u'v' \[I\].

### Driving the meter from code

- A log file argument writes tab-separated readings with column headers, which is simpler to parse than screen output \[V\].
- Integration time is adaptive by default (longer when dark); -Y A trades low-light accuracy for speed, so do not use it here \[V\].
- Pitfall: only one program can hold the meter, so close DisplayCAL and Datacolor software first \[I\].
- Pitfall: without -O, spotread waits for a key press, and feeding keys from Python on Windows needs a pseudo-console library such as pywinpty \[I\]. Start with one -O call per reading and optimise only if run time hurts.
- **spotread -O** takes one reading (or one calibration) and exits; Argyll says the option exists to simplify scripted use. Combine with -N (skip calibration), -x (Yxy output), -X file.ccss and -y n (non-refresh, for LCD) \[V\] ([spotread](https://www.argyllcms.com/doc/spotread.html)).

### Physical set-up

- Contact reading at the centre of the screen, meter flat and square to the panel: VA panels shift colour and gamma off-axis, and this one has a 60-degree viewing cone \[V\] ([HDTVTest](https://www.hdtvtest.co.uk/news/ue49ks7000-201610234374)).
- Counterweight the cable over the top edge so the meter rests without pressing; pressure on an LCD changes the reading \[I\].
- Dark room, curtains shut, a black cloth over the meter and the surrounding screen, no lamps reflecting off the panel.
- Same spot all session: mark it with masking tape on the bezel, not the screen.
- TV in its viewing position and orientation, Eco Sensor off.

## 6. Test patterns and signal path

A bit-exact SDR path is achievable for £0: the GPU outputs full-range 8-bit RGB untouched, our own full-screen renderer draws video-level (16 to 235) patterns, and the TV is told to expect limited range. Route the PC through the Denon with Video Mode set to Bypass, so the calibration lands on the TV input every source uses.

### Signal path from the GTX 1080

| Setting | Value for calibration | Why | Basis |
| --- | --- | --- | --- |
| ArgyllCMS video LUT | Cleared with dispwin -c before every run | Any loaded calibration curve alters every pixel | \[V\] [dispwin](https://www.argyllcms.com/doc/dispwin.html) |
| NVIDIA dithering | Off, set explicitly | Dithering is invisible to a meter but breaks bit-exactness | \[V\] control via [ColorControl](https://github.com/Maassoft/ColorControl); \[I\] need |
| NVIDIA output colour depth | 8 bpc for SDR | Patterns are 8-bit; avoids any re-quantisation | \[I\] |
| NVIDIA output dynamic range | Full | Stops the GPU compressing 0-255 into 16-235, which is not bit-exact and relies on dithering | \[R\] [Kodi/madVR levels guide](https://forum.kodi.tv/printthread.php?tid=259188) |
| NVIDIA output format | RGB | Pixel values reach the TV unconverted | \[I\] |
| Pattern values | Video levels: black 16, white 235, with codes below and above available for checks | Matches what a Blu-ray player or streamer sends | \[R\] [Kodi/madVR levels guide](https://forum.kodi.tv/printthread.php?tid=259188) |
| Samsung HDMI Black Level | Low | Low expects limited 16-235; Normal expects full 0-255 | \[R\] [AMD community](https://community.amd.com:443/t5/graphics-cards/too-dark-with-pixel-format-set-to-rgb-4-4-4-full/m-p/467882), [videogameperfection](https://videogameperfection.com/members/vmagix/forums/replies/) |
| Windows Automatically manage colour for apps (ACM) | Off (Settings, System, Display, Colour profile) | ACM transforms app colours on supported displays | \[R\] [guide](https://macmyths.com/how-to-fully-disable-automatically-manage-color-for-apps-in-windows-11-24h2/) |
| Windows display profile | None, or sRGB with no calibration curve | Same reason as the LUT | \[I\] |
| Windows HDR, Night light, adaptive colour | All off for SDR | Each alters output; Microsoft's own SDR measurement set-up switches them off | \[V\] [Microsoft Learn](https://learn.microsoft.com/surface/configure-sdr-and-hdr-display) |

The PC desktop will look crushed with this combination; that is expected and irrelevant during a run. The program saves and restores the NVIDIA and TV settings it changes.

### Verifying levels end to end

1. **Below black:** show bars at 8, 12, 16, 18, 20 and 25 with Brightness raised temporarily. If 12 differs from 16 the range interpretation is right and below-black passes (HDTVTest reports this set passes) \[V\] ([HDTVTest](https://www.hdtvtest.co.uk/news/ue49ks7000-201610234374)). Done by eye, because the meter cannot see this low.
2. **Above white:** measure 230, 235, 240 and 250 with the meter. Luminance should keep rising past 235 unless Contrast clips; record where each channel stops rising.
3. **Channel clipping:** repeat step 2 on red, green and blue fields at 235 and 250 to catch a single channel clipping first.
4. **Dithering:** a meter averages it away, so set it explicitly and check by eye on a one-code step chart \[I\].
5. **Format check:** run the final verification once more with the GPU set to YCbCr 4:4:4 limited. RGB patterns skip the TV's YCbCr decoding, which every disc and streaming source uses; a gap above 0.5 dE2000 between the two runs means that decoding needs attention \[I\].

### Pattern display

- **ArgyllCMS's own window** can show patches, place and scale them (-P), black out the rest of the screen (-F), use video levels (-E) and drive madTPG (-d madvr) \[V\] ([dispwin](https://www.argyllcms.com/doc/dispwin.html)). It is a good cross-check, not the main renderer, because it cannot hold a pattern while the program adjusts the TV.
- **madTPG** (free, closed source) is the practical route for HDR10 patterns; HDR has to be switched on in madTPG before measuring \[R\] ([DisplayCAL forum](https://hub.displaycal.net/forums/topic/question-for-hdr-calibration-with-madtpg/)). Reports say some NVIDIA drivers stop madTPG triggering HDR mode \[R\] ([madVR tracker](https://bugs.madshi.net/view.php?id=593)).
- **Near-black stimuli:** skip 0 to 5% for measurement, average heavily at 10%, and set Brightness by eye on the PLUGE (section 5).
- **Recommendation: our own full-screen renderer (Python, pygame on SDL2)** \[I\]. It writes raw 8-bit values with no colour management, holds a pattern on screen while the TV is adjusted, draws PLUGE and clipping charts, and keeps every on-screen instruction away from the meter.
- **Window size and APL:** Portrait Displays uses an 18% window at 18% APL for this TV generation \[V\] ([Portrait KB](https://kb.portrait.com/help/samsung-2016-suhd-tvs-c67d5bca)), so that is the default. With Smart LED off the backlight should not react to content, but the program tests it: it measures 100% white as a 10%, 18%, 50% and full-field window, and switches to constant-APL patterns everywhere if these differ by more than 1% \[I\].

### PC direct, or through the Denon

- 4K/8K Signal Format "Enhanced" (the default) carries 4K60 4:4:4 8-bit and 4:2:2 or 4:2:0 10-bit; 4K60 RGB at 10 or 12 bit needs "8K Enhanced" \[V\] ([Denon manual](https://manuals.denon.com/AVCX3800H/EU/EN/DRDZSYuvqzolrz.php)). The TV's HDMI 2.0 inputs cannot take 4K60 RGB 10-bit anyway, so send HDR patterns at 1080p or 4K30 RGB 10-bit \[I\].
- Fallback if Bypass misbehaves: temporarily move the Denon's cable on the TV input to the PC, calibrate, then swap back \[I\].
- For every other source to inherit the result, their Denon inputs should also avoid video processing (Bypass, or Auto with the upscaler off), and they must arrive at the same TV input with the same input icon and picture mode \[I\].
- On the Denon, set the PC's input to Video Mode **Bypass**, which removes all video processing from the HDMI path and also stops volume and information overlays appearing on the picture \[V\] ([Denon manual](https://manuals.denon.com/AVCX3800H/EU/EN/GFNFSYmlxuhedk.php)). Keep HDMI Upscaler Off (the default) \[V\].
- Picture settings belong to the TV input, so calibrate the TV input your sources actually arrive on (section 2). Routing the PC through the Denon guarantees that.

## 7. Targets and pass marks

Target BT.709 primaries, D65 white and BT.1886 built on the panel's real black, at 100 to 130 cd/m2 for a dark room or 130 to 170 cd/m2 for a dim one. Aim for greyscale dE2000 under 1 relative to the meter, and treat about 1.5 as the honest floor of this meter's absolute accuracy.

### SDR targets

| Target | Dark room | Dim room | Justification | Basis |
| --- | --- | --- | --- | --- |
| EOTF | BT.1886 (technical gamma 2.4 with input black offset) | BT.1886 with effective gamma 2.2 to 2.3, or a 2.2 to 2.3 power curve | BT.2035 calls for BT.1886; lower gamma suits brighter surroundings | \[V\] [BT.2035 text](https://itu.int/dms_pubrec/itu-r/rec/bt/R-REC-BT.2035-0-201307-I!!MSW-C.docx), [collink -I](https://www.argyllcms.com/doc/collink.html) |
| Peak white | 100 to 130 cd/m2 (HDTVTest uses 120) | 130 to 170 cd/m2 | BT.2035 reference white is 100 cd/m2; Portrait Displays' 2016 SUHD guide gives these room bands | \[V\] [BT.2035 text](https://itu.int/dms_pubrec/itu-r/rec/bt/R-REC-BT.2035-0-201307-I!!MSW-C.docx), [Portrait KB](https://kb.portrait.com/help/samsung-2016-suhd-tvs-c67d5bca), [HDTVTest](https://www.hdtvtest.co.uk/news/ue49ks7000-201610234374) |
| Primaries | BT.709 | BT.709 | All SDR video is mastered to it | \[V\] [BT.2035 text](https://itu.int/dms_pubrec/itu-r/rec/bt/R-REC-BT.2035-0-201307-I!!MSW-C.docx) |
| Surround | Bias light near 10% of peak, D65 | Room light kept off the screen | BT.2035's reference room has a 10 cd/m2 background for 100 cd/m2 white | \[R\] [W3C list summary](https://lists.w3.org/Archives/Public/public-colorweb/2021Jan/0005.html) |
| White point | D65, x 0.3127, y 0.3290 | Same | BT.2035 | \[V\] [BT.2035 text](https://itu.int/dms_pubrec/itu-r/rec/bt/R-REC-BT.2035-0-201307-I!!MSW-C.docx) |

**Black level for BT.1886.** The formula needs the display's black, which the Spyder 5 cannot measure on this panel (section 5). Default it to peak white divided by 3,000, from HDTVTest's 0.04 cd/m2 at 120 cd/m2 \[V\] ([HDTVTest](https://www.hdtvtest.co.uk/news/ue49ks7000-201610234374)), and let you override it. The choice mainly changes the curve below about 10%, where the meter is weakest \[I\].

### Pass marks

- Benchmark: after a professional CMS calibration of this model, only 3 of 140 ColorChecker SG patches exceeded dE 3 \[V\] ([HDTVTest](https://www.hdtvtest.co.uk/news/ue49ks7000-201610234374)).
- dE ITP (BT.2124, the ICtCp metric): 1 is a just-noticeable difference in the most critical viewing state \[V\] ([colour-science docs](https://colour.readthedocs.io/en/latest/generated/colour.difference.delta_E_ITP.html)). Report it alongside dE2000; it handles wide gamut and HDR better \[V\] ([Portrait Displays](https://www.portrait.com/resource-center/eitp-is-now-itu-r-bt-2124-is-the-industry-ready-to-move-on-from-e2000/)).
- dE2000 below 1 is generally invisible, and calibrators stop tweaking there \[V\] ([Portrait Displays](https://kb.portrait.com/help/about-deltae-e)). HDTVTest treats dE below 3 as not visible \[V\] ([HDTVTest](https://www.hdtvtest.co.uk/news/ue49ks7000-201610234374)).
- The meter's absolute white error with a good CCSS is about dE 1.3 to 2.0 (section 5), so absolute numbers under about 1.5 are not meaningful. Repeatability is much better than accuracy, so relative targets can go lower \[I\].

Proposed pass marks for this tool \[I\]:

| Measure | Pass | Reference grade |
| --- | --- | --- |
| Colour checker (24 patches) | Average 2.5, maximum 4 | Average 1.5, maximum 3 |
| EOTF | Within 5% of target luminance, 20 to 90% | Within 3% |
| Greyscale 20 to 100%, dE2000 relative to meter | Average 1.5, maximum 2.5 | Average 0.8, maximum 1.5 |
| Primaries and secondaries at 100% | Average 2.5, maximum 4 | Average 1.5, maximum 2.5 |
| White point vs D65 (u'v') | 0.003 | 0.0015 |

### Verification suite

1. **Greyscale 0 to 100% in 5% steps:** luminance, xy, CCT, dE2000 and dE ITP against BT.1886; points under the meter floor are reported as "below meter floor", not as numbers.
2. **Primaries and secondaries:** 100% and 75% saturation at 75% stimulus, plus luminance error per colour.
3. **Saturation sweeps:** 25, 50, 75 and 100% for red, green, blue, cyan, magenta and yellow.
4. **Colour checker:** the 24 classic patches as BT.709 video values; optional 140-patch SG set for long runs.
5. **Contrast and black:** full-field white versus black, with black flagged when it is below the meter floor.
6. **Before and after report:** one HTML page with RGB balance, EOTF, CIE diagram and dE bar charts, the raw readings as CSV, the meter, CCSS and software versions, and the settings card.

colour-science supplies dE2000, dE ITP, CCT and the colour-space conversions \[V\] ([colour-science docs](https://colour.readthedocs.io/en/latest/generated/colour.difference.delta_E_ITP.html)).

## 8. The algorithm

Adjust in the order the TV applies its controls: fixed settings, contrast and backlight, 2-point, gamma, multi-point, then CMS. A sensitivity-based integer solver does the work, and it refuses to move a control for any gain smaller than the meter's noise.

### Order of operations

1. **Pre-flight:** read the model and firmware from the TV's device-info endpoint, run the signal-path checks (section 6), the menu-overlay and APL tests, the warm-up gate, and meter checks (CCSS accepted, noise at 100, 50 and 20%).
2. **Fixed settings:** Movie mode, Warm2, every dynamic feature off, Colour Space Auto, Gamma 0, white balance zeroed via Reset Picture. Portrait Displays' guide for this generation also starts with a full reset \[V\] ([Portrait KB](https://kb.portrait.com/help/samsung-2016-suhd-tvs-c67d5bca)).
3. **Contrast:** leave it at the mode default unless the clipping check in section 6 fails. The same guide keeps Brightness and Contrast at their defaults for its autocalibration on this generation \[V\] ([Portrait KB](https://kb.portrait.com/help/samsung-2016-suhd-tvs-c67d5bca)).
4. **Backlight:** set peak white to the target; on an LED backlight it moves luminance far more than colour \[I\].
5. **Brightness:** the one manual step. The program shows a PLUGE and plain instructions; you confirm the setting.
6. **2-point white balance:** gains at 80%, offsets at 20%, the points Portrait Displays uses for this generation \[V\] ([Portrait KB](https://kb.portrait.com/help/samsung-2016-suhd-tvs-c67d5bca)). Iterate, because each pair leaks into the other end \[I\].
7. **Gamma slider:** choose the step with the smallest EOTF error from 20 to 90% \[I\].
8. **Multi-point white balance:** first map which stimulus levels each point moves, because HDTVTest found the points "contrast-aligned" on this model \[V\] ([HDTVTest](https://www.hdtvtest.co.uk/news/ue49ks7000-201610234374)). Then correct points from the top down; R, G and B together at each point fix both balance and EOTF \[I\].
9. **Re-check white:** touch up the gains if white has moved beyond target \[I\].
10. **CMS:** primaries before secondaries. For each colour, solve its three sliders for xy and luminance at 100% saturation and 75% stimulus, then check 75% saturation \[I\]. HDTVTest found this CMS works well \[V\].
11. **Verify** (section 7), write the report, the settings card and the journal.

Interactions the order respects \[I\]:

- Backlight scales everything, so it comes before any white balance work.
- Colour and Tint overlap the CMS, so both stay at their defaults.
- Contrast and the gains both shape the top end; Contrast is settled first.
- The CMS moves saturated colours rather than white, but white is re-checked afterwards anyway.
- The gamma slider and the multi-point overlap: the slider is the coarse step, the points the fine one.
- The multi-point is a correction on top of the 2-point, so changing the 2-point afterwards invalidates it.

### Control strategy

- **Error space:** convert each reading to linear RGB relative to the target using the inverse BT.709 matrix. Gains and offsets then act on red, green and blue errors almost independently \[I\].
- **Integer steps:** solve damped least squares (step factor 0.7), then test the neighbouring whole-number settings (27 combinations for three sliders) on the model and keep the lowest predicted dE2000 \[I\].
- **No oscillation:** keep the best settings measured so far and always finish on them; freeze any control that has reversed direction twice \[I\].
- **Non-linearity:** re-linearise every iteration and cap moves at 6 steps per control per iteration \[I\].
- **Route-specific:** with Ex-Link the sensitivity sweeps are cheap; with key presses the program groups changes by menu page to save navigation \[I\].
- **Sensitivity (Jacobian):** nudge each control up and down by enough steps to move the reading at least 5 times the noise (typically 3 to 6 steps). Re-measure the sensitivity whenever a prediction misses by more than 30% \[I\].
- **Stopping rules:** stop when every point meets its pass mark, when the predicted gain is under 2 standard deviations of dE noise, after 3 iterations without improvement, or at an iteration cap (10 for 2-point, 4 per multi-point level, 6 per CMS colour) \[I\].

### Run time

&#91;embedded content: Estimated from the reading and key timings in sections 3 and 5 · 7 stages, 2 control routes\]

Add 45 minutes of warm-up to either route. The key-press route spends most of its time navigating and re-zeroing sliders, which is why multi-point and CMS shrink most with Ex-Link.

### Failure handling

- **Crash or power cut:** a checkpoint file after every stage holds every known absolute value; the next start offers resume or rollback \[I\].
- **Drift mid-run:** the 75% reference is re-read every 10 minutes. A shift above 1% in luminance or 0.001 in u'v' pauses the run and re-baselines; a second shift means warm-up was not finished, so the program waits 10 minutes \[I\].
- **Meter disconnected:** a non-zero spotread exit triggers one retry, then a pause with a plain-English prompt, then a resume from the last stage checkpoint \[I\].
- **Safe abort:** Esc or the Abort button stops all commands, closes menus, re-applies the best settings found (Ex-Link) or leaves the last confirmed ones (key presses), and writes the journal and settings card \[I\].
- **TV off or menu lost:** a closed WebSocket, or no 03 0C F1 acknowledgement on Ex-Link \[V\] ([Samsung sheet](https://image-us.samsung.com/SamsungUS/samsungbusiness/tv-ci-resources/Samsung-RS232-Control.pdf)), triggers three retries, then a pause; on resume the program re-homes the menu and re-zeroes the control it was on \[I\].

## 9. PC-side correction (secondary)

The program can build a 3D LUT with ArgyllCMS from its own measurements, but it only corrects what the PC outputs, so it is an optional last polish rather than part of the calibration. Build it only if verification shows saturation errors the TV's CMS could not fix.

- **Guard rail:** the TV-side run always clears the PC's video LUT first (dispwin -c), so a PC-side LUT can never contaminate a TV calibration \[V\] ([dispwin](https://www.argyllcms.com/doc/dispwin.html)).
- **How:** profile the calibrated TV with dispread (a few hundred patches, roughly 30 to 60 minutes on the Spyder 5 \[I\]), build a profile with colprof, then link with collink. collink writes madVR .3dlut (-3 m), IRIDAS .cube (-3 c) or eeColor (-3 e) files, implements BT.1886 exactly with -I B, and handles video levels with -e t and -E t \[V\] ([collink](https://www.argyllcms.com/doc/collink.html)).
- **Is it worth it?** Mostly no. Your PC's main TV job is GeForce Now, so only a desktop-wide LUT would matter, and its gain is limited by the same meter accuracy (section 13). Expect perhaps 0.5 to 1 dE on saturation sweeps over a good TV-side result \[I\].
- **Where it applies:** madVR takes the .3dlut directly, and -a or -H appends calibration curves for it \[V\] ([collink](https://www.argyllcms.com/doc/collink.html)); .cube suits other players; a desktop-wide LUT needs a separate DWM injector, which DisplayCAL users mention \[R\] ([DisplayCAL forum](https://hub.displaycal.net/forums/topic/regarding-the-issue-of-inaccurate-calibration-results/)).
- **Where it cannot help:** anything that reaches the TV without passing through the PC (Apple TV, Xbox, the TV's own apps) gets only the TV-side calibration \[I\].

## 10. Prior art

I found no open-source tool that auto-calibrates a Samsung consumer TV, but every piece exists. Most important, Calman's documented serial autocalibration of exactly this TV generation proves the TV accepts calibration commands over Ex-Link.

| Project or source | What it shows or does | What we reuse | Licence | Basis |
| --- | --- | --- | --- | --- |
| aiopylgtv and bscpylgtv (LG) | Open-source upload of 1D and 3D LUTs and picture settings to LG TVs in a calibration mode; warns that calibration data can brick a set | Design patterns only (calibration-mode bracketing, per-mode data); not usable on Samsung | Not checked | \[V\] [PyPI](https://pypi.org/project/aiopylgtv/0.3.2/) |
| ArgyllCMS | Spyder 5 driver, patch window, profiling, 3D LUTs | Run as separate programs (spotread, dispwin, collink) | AGPL-3.0 | \[V\] [ArgyllCMS](https://argyllcms.com/commercialuse.html), [Homebrew](https://formulae.brew.sh/formula/argyll-cms) |
| Calman (Portrait Displays), commercial | Serial autocalibration of 2016 SUHD sets over Ex-Link: 2-point, multi-point and CMS, Cal Day and Cal Night modes, full reset first, 18% window at 18% APL, FTDI adapter recommended, SDR only | Knowledge only: cable pinout, order of work, reset step, firmware workaround (toggle Expert Mode, then pick a Cal mode) | Commercial; not used | \[V\] [Portrait KB](https://kb.portrait.com/help/samsung-2016-suhd-tvs-c67d5bca) |
| ColorControl | Samsung key macros; NVIDIA presets for range, depth, format, dithering and HDR | Run alongside to set NVIDIA output and dithering | GPL-3.0 | \[V\] [GitHub](https://github.com/Maassoft/ColorControl) |
| DisplayCAL | GUI over ArgyllCMS; bundles the Samsung QLED quantum-dot CCSS | One-off CCSS import and an independent verification cross-check | Not checked | \[R\] [DisplayCAL forum](https://hub.displaycal.net/forums/topic/x-rite-i1-display-pro-plus/) |
| HDTVPolska and AVCesar | Ex-Link calibration offered on 2016 SUHD sets; Cal Day and Cal Night modes on 2015 and 2016 SUHD | Confirms the 2016 serial route in the field | n/a | \[R\] [HDTVPolska](https://hdtvpolska.com/?p=15210), [AVCesar](https://www.avcesar.com/calibrage-calman-calday-calnight-dispo-sur-tv-samsung-suhd-qled-2015-2016-2017-et-2018-28448) |
| openHAB Samsung TV binding | Which control channels work on which model years; queued keys with 300 ms gaps | Facts and pacing defaults | Not checked | \[V\] [openHAB](https://v50.openhab.org/addons/bindings/samsungtv/) |
| Samsung consumer RS-232 sheet | Full Ex-Link command table: picture controls, 2-point, 10-point and 20-point white balance, CMS, OSD off, key codes, checksum, acknowledgement 03 0C F1 | The Ex-Link backend's command map | Samsung document | \[V\] [Samsung](https://image-us.samsung.com/SamsungUS/samsungbusiness/tv-ci-resources/Samsung-RS232-Control.pdf) |
| samsung-tv (Node.js, phillipsnick) | Ex-Link command builders and checksum: picture mode including Cal Night and Cal Day, backlight 0 to 20, contrast, brightness, gamma -3 to +3; no two-way communication; port may need enabling in the service menu | Port the command encoding to Python | MIT | \[V\] [GitHub](https://github.com/phillipsnick/samsung-tv) |
| samsungtvws (Python) | WebSocket remote keys, device info, Wake-on-LAN, 2016+ Tizen | Import as the key-press backend | LGPL-3.0 | \[V\] [GitHub](https://github.com/xchwarze/samsung-tv-ws-api) |
| SamyGO forum | Owner experience of Ex-Link Debug versus UART modes and service-menu hazards on K-series sets | Risk notes | n/a | \[R\] [SamyGO](https://forum.samygo.tv/viewtopic.php?p=113512) |

Licence consequence: for your own use nothing here constrains you. Run ArgyllCMS and ColorControl as separate programs and import samsungtvws as a library; only redistributing the packaged tool would bring LGPL and AGPL obligations into play \[I\].

## 11. Recommended architecture

Build a Python Windows app with one run controller and four services. The TV control layer has three interchangeable backends, so nothing else in the program cares whether a change arrives by Ex-Link, key presses or IR.

&#91;embedded content: Architecture · 1 controller, 4 services, 3 interchangeable TV backends\]

Read it top down: the wizard starts the controller; each stage asks the renderer for a pattern, the meter service for a reading, the solver for the next change and the TV control layer to make it, and every step is journalled.

### One adjustment cycle

1. The controller asks the renderer for a patch, for example 80% grey in an 18% window at 18% APL (Portrait Displays' setting for this generation \[V\] ([Portrait KB](https://kb.portrait.com/help/samsung-2016-suhd-tvs-c67d5bca))).
2. After the settle time, the meter service runs spotread -O with the CCSS and averages or rejects readings (section 5).
3. The solver converts the reading into error against target and predicts the best whole-number change (section 8).
4. The TV control layer applies it: one absolute command on Ex-Link, or a navigate-adjust-close sequence on keys, and reports success or failure.
5. The journal writes the line; the controller checks drift, abort and iteration limits, then loops.

### Components and tools

| Component | Free library or tool | Role |
| --- | --- | --- |
| Colour maths | colour-science, NumPy | dE2000, dE ITP, BT.1886, chromaticity conversions |
| Ex-Link backend | pyserial, plus a Python port of the samsung-tv command encoding | Absolute-value commands, checksum, acknowledgement check |
| IR backend (optional) | An ESP32 running an IR library, driven over USB serial | Key presses and the factory key if the network route fails |
| Journal and report | Python standard library (JSON Lines, CSV), a templated static HTML page | Audit trail, settings card, before and after report |
| Key-press backend | samsungtvws | WebSocket keys, device info, Wake-on-LAN |
| Meter service | ArgyllCMS spotread, called as a subprocess | Readings with CCSS correction |
| NVIDIA set-up | ColorControl, used once by hand | Output range, depth, format and dithering |
| Packaging | PyInstaller one-folder build with a first-run checklist | One-click start, no Python install needed |
| Pattern renderer | pygame (SDL2) | Full-screen patches, PLUGE, clipping charts |
| Solver | NumPy | Sensitivity model, damped least squares, integer search |
| Wizard UI | PySide6 (Qt) | Guided steps, plain-English status, big Abort button |

Why Python: ArgyllCMS is driven from the command line, and the Samsung WebSocket and colour libraries are Python already, so no other language would save work \[I\]. The first-run checklist confirms ArgyllCMS is unzipped, the Argyll USB driver is bound to the Spyder, the CCSS file is present and the TV answers; it explains in plain English how to fix whichever check fails.

## 12. Staged build plan

Nine stages, each usable on its own; the first three carry no risk to the TV at all, because the program does not touch it until stage 3. Stages 7 and 8 are optional.

1. **Stage 0, bench set-up (no code).** Unzip ArgyllCMS, bind its USB driver to the Spyder, import the quantum-dot CCSS via DisplayCAL, set NVIDIA output with ColorControl, set the Denon input to Bypass, put the TV in Movie with dynamic features off, and photograph every settings page.
   - *You do:* all of it, from a printed checklist. *You get:* a clean, documented signal path and baseline.
2. **Stage 1, measure and report.** Pattern renderer, meter service, verification suite and HTML report; no TV control.
   - *You do:* place the meter, start the run. *You get:* an honest "before" report, and a live-reading screen to use while adjusting by remote.
3. **Stage 2, guided manual calibration.** The solver suggests changes ("R-Gain +3, B-Offset -2") and re-measures after you key them in.
   - *You do:* enter each suggestion with the remote. *You get:* a semi-automatic calibration with no TV-control risk.
4. **Stage 3, TV control layer.** Ex-Link backend with its probe (if you bought the cable), WebSocket key backend with the menu-teach wizard, journal and settings card.
   - *You do:* connect the cable or run menu-teach once, accept the TV's connection prompt. *You get:* reliable remote setting of every control, with rollback.
5. **Stage 4, automatic 2-point and gamma.** Closed loop for Backlight, 2-point white balance and the gamma slider.
   - *You do:* confirm the PLUGE for Brightness, then watch. *You get:* most of the visible gain of a calibration.
6. **Stage 5, automatic multi-point.** Influence mapping, then 10-point (or 20-point) correction from 20 to 100%.
   - *You do:* nothing beyond starting it. *You get:* neutral greyscale and BT.1886 tracking above the meter floor.
7. **Stage 6, automatic CMS.** Primaries, then secondaries, then the full verification and before and after report.
   - *You do:* nothing beyond starting it. *You get:* the complete SDR calibration.
8. **Stage 7 (optional), HDR10 check and greyscale.** madTPG HDR patterns, saturation test for the meter, 2-point white balance at mid PQ levels, PQ tracking report.
   - *You do:* switch madTPG to HDR before the run. *You get:* a verified, partly corrected HDR mode.
9. **Stage 8 (optional), PC-side 3D LUT.** dispread profile, collink LUT for madVR or a desktop injector.
   - *You do:* choose where the LUT is used. *You get:* a final polish for PC playback only.

Packaging (one-click executable, checkpoints and resume) is added from stage 3 onwards, so every later stage ships as the same program.

## 13. Expected accuracy

Expect the TV to measure as reference grade on its own meter (greyscale under dE 1 from 20 to 100%) while truly sitting within about dE 1.5 to 2 of D65, with colours truly averaging about 2 to 3. The meter, not the TV's controls, sets the ceiling.

| Measure | Expected, as the Spyder reads it | Likely true error | Limiting factor |
| --- | --- | --- | --- |
| Colour checker (24) | Average about 1.5 to 2 | Average about 2 to 3 | Meter on saturated colours |
| EOTF, 20 to 90% | Within 3% of target luminance | Similar | Relative luminance is the meter's strongest suit |
| Greyscale 0 to 5% | Not measurable | Unknown; set by eye | Meter floor near 0.3 cd/m2 |
| Greyscale 10% | dE 1 to 3, noisy | Similar | Low-light noise |
| Greyscale 20 to 100% | Average dE2000 at or under 1 | Average about 1 to 2, mostly a shared white offset | CCSS match |
| HDR greyscale at mid PQ | dE about 2 to 3 | Unknown | Power limiting, meter ceiling unknown, no HDR CMS |
| Primaries and secondaries | Average about 1.5 to 2.5 | Up to 1 to 2 worse on red and green | Narrowband quantum-dot peaks versus filter sensitivities |
| White point vs D65 | Within 0.001 u'v' | 0.003 to 0.006 in xy (about dE 1.3 to 2) | Meter accuracy with a borrowed CCSS |

All figures in the middle two columns are my estimates \[I\], reasoned as follows:

- **Absolute accuracy:** ChromaPure measured average errors of 0.003 to 0.006 xy (dE 1.3 to 2.0) for the SpyderX across display types, with the Spyder 5 matching it at 10% and above \[V\] ([ChromaPure](https://chromapure.com/newgear-new.asp)). A CCSS measured on a different quantum-dot set (Samsung Q9) adds an unknown error on top \[I\].
- **HDR:** even Calman supports only SDR calibration on 2016 SUHD sets \[V\] ([Portrait KB](https://kb.portrait.com/help/samsung-2016-suhd-tvs-c67d5bca)); with this meter, HDR stays a check plus greyscale touch-up.
- **Low light:** the floor near 0.3 cd/m2 (section 5) removes everything at or under about 5% stimulus at 120 cd/m2 and makes 10% noisy \[I\].
- **Relative accuracy:** greys share one spectral mix, so a CCSS error shifts every grey alike; tracking between greys stays much tighter than absolute white \[I\]. ChromaPure found SpyderX repeatability near perfect from 20% grey upwards \[V\]; the Spyder 5 was not tested for this \[I\].
- **The TV is not the limit.** HDTVTest reached D65 on this model with the 2-point controls alone and brought all but 3 of 140 ColorChecker SG patches under dE 3 with the CMS \[V\] ([HDTVTest](https://www.hdtvtest.co.uk/news/ue49ks7000-201610234374)). Sliders of -50 to +50 give fine steps \[V\] ([Samsung sheet](https://image-us.samsung.com/SamsungUS/samsungbusiness/tv-ci-resources/Samsung-RS232-Control.pdf)).

## 14. Shopping list

Nothing is strictly needed: the key-press route costs £0. The recommended Ex-Link route needs about £16.70 of parts, or £19.80 if the transmit and receive lines turn out swapped.

| Item | UK price | Running total | Purpose | Basis |
| --- | --- | --- | --- | --- |
| 3.5 mm stereo jack to DB9 female serial cable, wired tip to pin 2, ring to pin 3, sleeve to pin 5 | About £8 (listings run roughly £4 to £10) | £8.00 | Connects the TV's Ex-Link jack to the adapter | \[V\] wiring ([Portrait KB](https://kb.portrait.com/help/samsung-2016-suhd-tvs-c67d5bca)); \[R\] price ([eBay](https://www.ebay.de/itm/175683763380), [listing](https://ubbcentral.com/store/item/9-Pin-RS232-DB9-Female-to-3-5mm-Male-Jack-Plug-Adapter-Serial-Data-Cable_235620274348.html)) |
| DB9 null-modem cable, male to female (only if the probe gets no reply) | £3.10 | £11.10 | Sits between adapter and cable to swap transmit and receive if the cable is wired the other way | \[V\] [The Pi Hut](https://thepihut.com/collections/serial-cables) |
| USB to RS232 cable with an FTDI FT232RL chip, DB9 male (Waveshare) | £8.70 | £19.80 | The PC's serial port; Portrait Displays found FTDI adapters the most reliable for this job | \[V\] [The Pi Hut](https://thepihut.com/collections/serial-cables), [Portrait KB](https://kb.portrait.com/help/samsung-2016-suhd-tvs-c67d5bca) |

- A DIY Ex-Link lead from a spare 3.5 mm stereo cable and a DB9 female solder connector costs about £2 instead of the first item \[I\].
- Already owned: Spyder 5, PC, HDMI leads, a black cloth for shading the meter.
- Not on the list: the IR blaster. It only matters if both Ex-Link and the network route fail, and fits the remaining budget only if you already own a microcontroller board \[I\].

## 15. Risks, mitigations and recovery

The only risks that could leave the TV in a bad state live in the service menu, which the program never enters by itself; everything else is recoverable with Reset Picture and the settings card.

| Risk | Likelihood | Mitigation | Recovery | Basis |
| --- | --- | --- | --- | --- |
| Cal Day or Cal Night settings lock after calibration | Low (Movie is the default) | Calibrate Movie; use a Cal mode only deliberately | Reset that mode, or a full reset of picture settings | \[V\] lock noted for 2019 sets ([Portrait](https://www.portrait.com/resource-center/samsung-2019-qled-autocal-guide/)); \[I\] for 2016 |
| CCSS mismatch tints white | Medium | Use the quantum-dot CCSS; keep raw readings | Re-score saved readings with a better CCSS; re-run 2-point only | \[I\] |
| Ex-Link jack needs a service-menu change from Debug to UART | Unknown | Try first with no change (Calman's guide lists none); if needed, photograph the page and change only that item | Set it back to Debug with an IR remote | \[V\] [Portrait KB](https://kb.portrait.com/help/samsung-2016-suhd-tvs-c67d5bca); \[R\] [SamyGO](https://forum.samygo.tv/viewtopic.php?p=113512) |
| Factory calibration wiped in the service menu | Low (never automated) | The program has no service-menu code path; never press Reset there | None at home; Samsung service visit | \[R\] [SamyGO](https://forum.samygo.tv/viewtopic.php?p=105670) |
| Firmware update changes menus or network control | Low to medium | Record the firmware version; hold updates during the project; menu map stored per firmware | Re-run menu-teach; switch to port 8002 with a token | \[R\] [HA issue 17802](https://github.com/home-assistant/core/issues/17802) |
| HDR patterns saturate the meter or hit the power limiter | Medium | Saturation test first, short exposures, cool-down pauses | Discard affected readings | \[V\] limiter ([HDTVTest](https://www.hdtvtest.co.uk/news/ue49ks7000-201610234374)) |
| Lost slider position on the key route | Medium | Measurement check after every change; re-zero against the end stop | Reset Picture, then the settings card | \[I\] |
| Meter drift or movement | Medium | Warm-up gate, reference re-reads, tape marks, counterweight | Re-run the affected stage | \[I\] |
| Settings land on the wrong input or picture mode | Low | Input and mode confirmed at start; Ex-Link sets the mode directly | Reset Picture on that mode; re-enter its baseline photos | \[I\] |
| USB conflicts (Datacolor software, RGB lighting services) | Medium | First-run checklist; disable the named services | Switch the driver in Device Manager | \[V\] [ArgyllCMS](https://www.argyllcms.com/doc/Installing_MSWindows.html) |
| Wrong signal levels (crushed or lifted black) | Medium on first set-up | PLUGE and clipping checks before any calibration; range pinned on GPU and TV | Restore the saved NVIDIA settings; HDMI Black Level back to its previous value | \[I\] |

## 16. Assumptions and checks to do on the TV

Twelve quick checks on the set and the Denon settle nearly every open question in this report; do them before any code is written.

### Assumptions I made

- Calibration targets SDR on the TV input the Denon feeds, in Movie mode, with the input icon you use every day.
- Ex-Link control works without a service-menu change, as Calman's guide implies; if not, you accept one recorded setting change.
- PC and TV share one network subnet, and the TV can be woken by the remote or Wake-on-LAN.
- The room can be made dark for runs of up to three hours.
- The Spyder 5 is healthy: its filters degrade with light exposure, so it should have been stored with its cap closed \[R\] ([Camera Tico](https://cameratico.com/articles/datacolor-spyder-5-review/)).
- The TV is a UE49KS7000 on the EU firmware family T-JZMDEUC.
- You run the tool yourself and can answer simple on-screen prompts.

### Checks on the TV and kit

- [ ] Apply Picture Settings: Current Source or All Sources?
- [ ] Denon: which TV HDMI input it feeds; set the PC's Denon input to Video Mode Bypass.
- [ ] Device Connect Manager: allow the PC and set access notification to first time only \[V\] ([samsungtvws](https://github.com/xchwarze/samsung-tv-ws-api)).
- [ ] Ex-Link jack: where it is and how it is labelled (Ex-Link, External Sync or RS-232C).
- [ ] Firmware version, from the Support menu.
- [ ] Game and PC modes: which expert controls grey out.
- [ ] Gamma: is a BT.1886 option offered, or only the slider?
- [ ] HDMI UHD Colour: its state on the Denon's TV input.
- [ ] Model code on the rear label.
- [ ] Multi-point white balance: 10 or 20 points, and the interval labels.
- [ ] Spyder 5 edition (Express, Pro or Elite), and whether you still have Datacolor's installer.
- [ ] TV IP address, reserved on the router so it never changes.

## 17. One-page build specification

Build "KS7000 AutoCal": a Windows Python app that calibrates one input and picture mode of a UE49KS7000 to BT.709, D65 and BT.1886, using a Spyder 5 via ArgyllCMS and the TV's Ex-Link port, with key presses over the network as the fallback.

### Components and interfaces

| Component | Interface |
| --- | --- |
| Journal | append(event); checkpoint(state); settings\_card() returns the final value of every touched control |
| Meter | read(min\_n, max\_n, se\_target) returns XYZ, xyY, n, standard deviation and flags (clipped, below floor, outlier-rejected) |
| Renderer | show(rgb8, window\_pct, apl\_pct); show\_chart(name); clear(); runs full screen on the TV output |
| Report | build(run\_id) writes one HTML page and CSV files |
| Run controller | run(stages, config); abort() within 2 s; resume(checkpoint) |
| Solver | sensitivity(controls, patches) returns a Jacobian; propose(errors, jacobian, bounds) returns whole-number steps |
| TV control | identify() returns model and firmware; probe() returns a capability map; set(control, value) and step(control, delta) return acknowledged or failed; reset\_mode() |

Config (one YAML file): targets, CCSS path, TV IP address, COM port, backend order (Ex-Link, keys, IR), menu map per firmware, averaging thresholds, pass marks.

### Acceptance tests per stage

| Stage | Passes when |
| --- | --- |
| 0 Bench set-up | spotread -x -y n -X (quantum-dot CCSS) -O returns a reading; dispwin -c succeeds; PLUGE shows 16 black with 18 and above visible; Denon input in Bypass |
| 1 Measure and report | 10 repeat reads of 75% grey vary under 0.5% in Y and 0.0005 in x and y; the full verification suite completes and the report renders; two runs agree within 1% |
| 2 Guided manual | For a deliberate +5 R-Gain change, predicted and measured change agree within 30% |
| 3 TV control | Ex-Link: picture-mode command acknowledged with 03 0C F1 and visible, and one gain step confirmed by the meter. Keys: menu-teach builds a map, and 20 random set-to-value tests land exactly as confirmed by measurement. Abort leaves menus closed within 2 s |
| 4 2-point and gamma | White within 0.002 u'v' of D65 as measured; greyscale 20 to 100% average dE2000 at most 1.5; EOTF within 5% |
| 5 Multi-point | Greyscale 20 to 100% average dE2000 at most 1.0, maximum 1.5; EOTF within 3% from 20 to 90% |
| 6 CMS | Primaries and secondaries average at most 2.5, maximum 4; colour checker average at most 2.5; white moves no more than 0.001 u'v' |
| 7 HDR (optional) | Meter saturation test passes; PQ tracking report produced; no exposure above 500 cd/m2 lasts longer than 30 s |
| 8 PC LUT (optional) | The LUT loads in madVR, and saturation sweeps through it improve by at least 0.5 dE |

### Rules the build must keep

- Abort from the window or Esc at any time, finishing on the best settings found.
- Clear the PC's video LUT before any run, and restore NVIDIA and TV range settings afterwards.
- Every message in plain English, with the next action spelled out.
- Never enter the service menu automatically, and never send a factory-reset command.
- Touch only the configured input and picture mode, and confirm both before changing anything.
- Write the journal line before every change and a checkpoint after every stage.

## 18. Self-check: weakest findings

The verdict rests most on two things I could not test: whether your firmware accepts Samsung's public Ex-Link commands, and how far the borrowed quantum-dot CCSS sits from your panel's real spectrum.

### Weakest parts

- **Ex-Link encoding:** Calman proves the port controls calibration on 2016 SUHD sets, but its protocol is private; Samsung's public table comes from a later document. If the probe fails, the key route takes over and run time roughly doubles (section 8); no stage verdict changes.
- **Forum evidence:** several findings rest on owner reports, all labelled \[R\].
- **Key-route behaviour:** menu wrap-around, time-outs and slider acceleration are untested; the menu-teach wizard exists to find them.
- **Meter on quantum dots:** the largest uncertainty in absolute accuracy, because the CCSS was measured on a 2018 Samsung Q9, not a KS-series set.
- **Multi-point count and behaviour:** sources disagree on 10 versus 20 points, and HDTVTest found the points "contrast-aligned"; influence mapping is the mitigation, not a proof.
- **Run times:** modelled from reading and key timings, not measured.
- **Spyder 5 HDR ceiling:** unpublished; if it saturates below about 600 cd/m2, the HDR stage shrinks to a mid-level greyscale check.

### What would change the verdict

- **Better:** a CCSS measured on a KS-series panel, or one evening with a borrowed spectrophotometer, would move absolute accuracy towards dE 1.
- **Worse:** the TV ignores Ex-Link and firmware blocks network key presses, leaving only IR, which the budget covers only if you already own a microcontroller board. Stages 0 to 2 stay useful regardless.
- **Worse:** Ex-Link needs the service-menu change and you decline it; the key route still delivers every SDR stage, just more slowly.

## 19. Sources

These are the pages this report draws on; each claim above carries its own label and link.

### Conflicts flagged

- **Calman defaults for 2016 SUHD:** the same Portrait page gives Brightness 45 and Contrast 95 in one place, 44 and 85 in another.
- **Ex-Link mode:** SamyGO and the samsung-tv README say the port may need enabling in the service menu; Portrait's 2016 guide lists no such step.
- **HDMI Black Level in PC mode:** one forum poster says it is unavailable, another that it works.
- **Multi-point white balance:** 10 points per HDTVTest (UK sample) and Portrait's introduction; 20 points per RTINGS (US KS8000) and Portrait's workflow text.
- **Spyder and CCSS:** ArgyllCMS documents CCSS support for the Spyder 4 and 5; a DisplayCAL forum reply says Spyders use built-in modes instead.
- **WebSocket port:** 8001 for 2016 sets per Home Assistant's docs; after some 2016 firmware updates only 8002 with a token answered.

### Source list

- [AMD community: Samsung HDMI Black Level, full versus limited](https://community.amd.com:443/t5/graphics-cards/too-dark-with-pixel-format-set-to-rgb-4-4-4-full/m-p/467882)
- [AMX forum: Samsung hospitality display and MDC](https://proforums.harman.com/amx/discussion/comment/199945)
- [AnandTech: Pulse-Eight USB CEC adapter review](https://www.anandtech.com/show/5463)
- [ArgyllCMS: collink](https://www.argyllcms.com/doc/collink.html)
- [ArgyllCMS: commercial use and licensing](https://argyllcms.com/commercialuse.html)
- [ArgyllCMS: contributed CCSS files](https://www.argyllcms.com/doc/ccsss.html)
- [ArgyllCMS: dispwin](https://www.argyllcms.com/doc/dispwin.html)
- [ArgyllCMS: installing on Microsoft Windows](https://www.argyllcms.com/doc/Installing_MSWindows.html)
- [ArgyllCMS: oeminst](https://www.argyllcms.com/doc/oeminst.html)
- [ArgyllCMS: operation of particular instruments](https://www.argyllcms.com/doc/instruments.html)
- [ArgyllCMS: spotread](https://www.argyllcms.com/doc/spotread.html)
- [AVCesar: Calman Cal Day and Cal Night on Samsung SUHD 2015 and 2016](https://www.avcesar.com/calibrage-calman-calday-calnight-dispo-sur-tv-samsung-suhd-qled-2015-2016-2017-et-2018-28448)
- [Camera Tico: Datacolor Spyder5 Pro review](https://cameratico.com/articles/datacolor-spyder-5-review/)
- [ChromaPure: SpyderX review with Spyder5 comparison](https://chromapure.com/newgear-new.asp)
- [ColorControl (GitHub)](https://github.com/Maassoft/ColorControl)
- [colour-science: delta\_E\_ITP](https://colour.readthedocs.io/en/latest/generated/colour.difference.delta_E_ITP.html)
- [Datacolor: SpyderPro, Spyder and SpyderExpress differences](https://spyder-support.datacolor.com/hc/en-us/articles/15888461682332)
- [Denon AVC-X3800H manual: 4K/8K Signal Format](https://manuals.denon.com/AVCX3800H/EU/EN/DRDZSYuvqzolrz.php)
- [Denon AVC-X3800H manual: Output Settings](https://manuals.denon.com/AVCX3800H/EU/EN/GFNFSYmlxuhedk.php)
- [DisplayCAL colorimeter corrections database](https://colorimetercorrections.displaycal.net)
- [DisplayCAL forum: best monitor calibrator](https://hub.displaycal.net/forums/topic/best-monitor-calibrator/)
- [DisplayCAL forum: colour correction and instrument mode](https://hub.displaycal.net/forums/topic/color-correction-and-instument-mode/)
- [DisplayCAL forum: contrast ratio and Spyder5 limitation](https://hub.displaycal.net/forums/topic/contrast-ratio-reported-as-17001-when-it-could-be-higher-spyder5-limitation/)
- [DisplayCAL forum: HDR calibration with madTPG](https://hub.displaycal.net/forums/topic/question-for-hdr-calibration-with-madtpg/)
- [DisplayCAL forum: i1 Display Pro for quantum-dot LED (KS7000)](https://hub.displaycal.net/forums/topic/i1-display-pro-for-quantum-dots-led-display-calibration/)
- [DisplayCAL forum: inaccurate calibration results](https://hub.displaycal.net/forums/topic/regarding-the-issue-of-inaccurate-calibration-results/)
- [DisplayCAL forum: sRGB versus Adobe RGB monitor](https://hub.displaycal.net/forums/topic/for-srgb-workflow-is-srgb-only-monitor-better-than-adobergb/page/2/)
- [DisplayCAL forum: X-Rite i1 Display Pro Plus](https://hub.displaycal.net/forums/topic/x-rite-i1-display-pro-plus/)
- [eBay listing: DB9 to 3.5 mm serial cable](https://www.ebay.de/itm/175683763380)
- [Elotrolado forum: KS7000 owner settings](https://www.elotrolado.net/hilo_ayuda-configuracion-tv-samsung-ks7000_2192904_s1100)
- [Expert Reviews: Samsung UE49KS7000 review](https://www.expertreviews.co.uk/samsung/1405210/samsung-ue49ks7000-review-an-amazing-4k-hdr-smart-tv-for-gaming-and-more-1/2)
- [GitHub: Home Assistant core issue 17802](https://github.com/home-assistant/core/issues/17802)
- [HDTVPolska: Ex-Link calibration of Samsung SUHD](https://hdtvpolska.com/?p=15210)
- [HDTVTest: Samsung UE49KS7000 review](https://www.hdtvtest.co.uk/news/ue49ks7000-201610234374)
- [Home Assistant community: Samsung smart TV no control](https://community.home-assistant.io/t/samsung-smart-tv-no-control/32914?page=11)
- [Home Assistant docs, 2017 snapshot: supported Samsung models](https://git.jeena.net/jeena/home-assistant.github.io/src/branch/rc/source/_components/media_player.samsungtv.markdown)
- [Home Assistant docs mirror: Samsung Smart TV](https://www.hasscn.top/home-assistant/integrations/samsungtv)
- [Homebrew: argyll-cms formula](https://formulae.brew.sh/formula/argyll-cms)
- [ITU-R BT.2035 text](https://itu.int/dms_pubrec/itu-r/rec/bt/R-REC-BT.2035-0-201307-I!!MSW-C.docx)
- [Kitele: Samsung UE49KS7000 specifications](https://www.kitele.com/en/tv-samsung-ue49ks7000)
- [Kodi forum: madVR set-up guide, video levels](https://forum.kodi.tv/printthread.php?tid=259188)
- [MacMyths: disabling Auto Colour Management in Windows 11](https://macmyths.com/how-to-fully-disable-automatically-manage-color-for-apps-in-windows-11-24h2/)
- [madVR bug tracker: madTPG will not switch to HDR](https://bugs.madshi.net/view.php?id=593)
- [Microsoft Learn: configure SDR and HDR display](https://learn.microsoft.com/surface/configure-sdr-and-hdr-display)
- [moveonup: Pulse-Eight USB-CEC adapter price](https://moveonup.csd.auth.gr/products/usb-hdmi-cec-adapter/218487134/)
- [npm: samsung-lfd](https://npmjs.com/package/samsung-lfd)
- [NVIDIA developer forum: HDMI-CEC support](https://forums.developer.nvidia.com/t/hdmi-cec-support/31445)
- [openHAB: Samsung TV binding](https://v50.openhab.org/addons/bindings/samsungtv/)
- [Portrait Displays: About DeltaE](https://kb.portrait.com/help/about-deltae-e)
- [Portrait Displays: Delta E ITP is now ITU-R BT.2124](https://www.portrait.com/resource-center/eitp-is-now-itu-r-bt-2124-is-the-industry-ready-to-move-on-from-e2000/)
- [Portrait Displays: Samsung 2016 SUHD TVs](https://kb.portrait.com/help/samsung-2016-suhd-tvs-c67d5bca)
- [Portrait Displays: Samsung 2019 QLED AutoCal guide](https://www.portrait.com/resource-center/samsung-2019-qled-autocal-guide/)
- [PyPI: aiopylgtv](https://pypi.org/project/aiopylgtv/0.3.2/)
- [PyPI: samsungtvws](https://pypi.org/project/samsungtvws)
- [Richer Sounds blog: Samsung KS7000](https://blog.richersounds.com/?p=29336)
- [RTINGS: Samsung KS8000 calibration settings](https://www.rtings.com/tv/reviews/samsung/ks8000/settings)
- [RTINGS: Samsung KS8000 versus NU8000](https://rtings.com/tv/tools/compare/samsung-ks8000-samsung-nu8000/291/586)
- [samsung-tv (phillipsnick, GitHub)](https://github.com/phillipsnick/samsung-tv)
- [Samsung: consumer RS-232 control worksheet](https://image-us.samsung.com/SamsungUS/samsungbusiness/tv-ci-resources/Samsung-RS232-Control.pdf)
- [Samsung: ports on the One Connect box](https://www.samsung.com/in/support/tv-audio-video/what-are-the-ports-available-in-samsung-one-connect-box/)
- [samsungtvws (GitHub)](https://github.com/xchwarze/samsung-tv-ws-api)
- [SamyGO forum: Control TV using Ex-Link (KS7000)](https://forum.samygo.tv/viewtopic.php?p=107013)
- [SamyGO forum: ES7000 white balance values](https://forum.samygo.tv/viewtopic.php?p=64672)
- [SamyGO forum: firmware 1165.1 thread](https://forum.samygo.tv/viewtopic.php?p=100846)
- [SamyGO forum: firmware and root note](https://forum.samygo.tv/viewtopic.php?p=98698)
- [SamyGO forum: K-series service menu, factory reset](https://forum.samygo.tv/viewtopic.php?p=105670)
- [SamyGO forum: K-series service menu, Option Type reset](https://forum.samygo.tv/viewtopic.php?p=105734)
- [SamyGO forum: K-series service menu, WBMovie](https://forum.samygo.tv/viewtopic.php?p=105755)
- [SamyGO forum: T-JZMDEUC 1241.5 request](https://forum.samygo.tv/viewtopic.php?p=109445)
- [SamyGO forum: UE40C6000 Ex-Link, UART versus Debug](https://forum.samygo.tv/viewtopic.php?p=113512)
- [SmartThings community: 2016 Samsung TVs as devices](https://community.smartthings.com/t/samsung-2016-smart-tvs-as-devices/79181)
- [SmartThings community: API not returning current picture mode](https://community.smartthings.com/t/the-api-does-not-return-the-current-picturemode/308861)
- [The Pi Hut: serial cables](https://thepihut.com/collections/serial-cables)
- [ubbcentral listing: DB9 female to 3.5 mm cable](https://ubbcentral.com/store/item/9-Pin-RS232-DB9-Female-to-3-5mm-Male-Jack-Plug-Adapter-Serial-Data-Cable_235620274348.html)
- [videogameperfection forum: HDMI black level](https://videogameperfection.com/members/vmagix/forums/replies/)
- [W3C public-colorweb list: BT.1886 and BT.2035](https://lists.w3.org/Archives/Public/public-colorweb/2021Jan/0005.html)
