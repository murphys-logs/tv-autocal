| Field | Value |
|---|---|
| Title | TV Calibration Feasibility Testing |
| Produced by | ChatGPT (OpenAI) |
| Original date | 2026-10-23 |
| Imported | 2026-10-25, by Codex (OpenAI), at the owner's request |
| How obtained | Original assistant response retrieved from the owner's ChatGPT conversation "TV Calibration Feasibility Testing"; conversation ID `6adbd0b3-97ac-83eb-8ae2-580a206673a0`, message ID `3c199ceb-caf7-55b4-871b-228a9078c731` |
| Fidelity | Verbatim complete retrieved response; one terminal newline added. Original unresolved citation markers and sandbox links retained unchanged |
| Ledger ID | S-012 |
| Provenance | AI: ChatGPT (OpenAI); source-verification limits recorded in the ledger |
| Equipment test status | Not tested; importing this historical response is not test authorisation |

**The Spyder5 interface is established. The television-control interface has two credible routes, but neither is yet verified on your exact set.** There is enough evidence to begin practical testing without buying anything.

I’ve prepared an experimental diagnostic kit: :chatgpt-content-reference{index="17"}[ACC_Probe_Kit.zip](sandbox:/C:/workspace/ACC_Probe_Kit.zip). It passes **15 offline tests**; live TV and meter testing remains outstanding.

**1. Critical feasibility verdict**

| Requirement | Verdict | Evidence | Next action |
|---|---|---|---|
| Change the TV’s actual picture settings | **Likely feasible but unverified** | Samsung publishes serial picture-control commands; network remote commands offer another route | Confirm model and connectors, then prove one reversible adjustment |
| Obtain automatic Spyder5 measurements | **Confirmed feasible in existing software** | ArgyllCMS supports Spyder5 and scripted measurements | Test your meter, driver and installed executable |
| Complete the measurement–adjustment feedback loop | **Uncertain pending hardware tests** | Its components are plausible, but their combined operation has not been demonstrated here | Measure, adjust, remeasure and calculate a second adjustment |

The strongest TV finding is that Portrait explicitly lists **“Samsung Serial – 2015/2016 SUHD”** among supported display connections. That is useful evidence of an existing calibration interface for this generation—not a recommendation to buy its software. :chatgpt-content-reference{index="0"}

One detail must be resolved first: Samsung lists a UK **UE49KS7000UXXU**, but your shorthand “49K7000” does not establish that this is your model. I have kept KS7000 compatibility conditional throughout. :chatgpt-content-reference{index="1"}

**2. Television-control investigation**

**Native Ex-Link serial control is the strongest direct-control lead.** Samsung’s own consumer RS232 worksheet contains commands for RGB gain and offset, gamma, custom colour-space adjustments and multipoint white balance. These are genuine picture controls. However, the worksheet includes newer terminology and ranges, so it cannot safely serve as an exact command map for an unidentified 2016 television. :chatgpt-content-reference{index="2"}

The remaining questions are concrete:

- Does your regional model have a usable native Ex-Link connector?
- Which commands and numerical encodings does its firmware implement?
- Can we confirm the original setting and reliably restore it?
- Does an accepted command produce the expected optical change?

An open-source [Samsung Ex-Link implementation](https://github.com/home-assistant-libs/samsung-exlink) already handles serial communication. It gives us reusable transport code, although its existence does not prove KS7000 compatibility. :chatgpt-content-reference{index="3"}

**Network remote navigation is the best £0 experiment.** The inspected `samsungtvws` implementation sends ordinary remote keys through WebSocket connections on ports 8001/8002. Its source supports Menu, Exit and directional keys. A successful send does **not** report the highlighted menu item or resulting picture-setting value. :chatgpt-content-reference{index="4"}

That makes the engineering problem reliable menu-state control. Our sequence must start from a reproducible state, cope with remembered cursor positions, clear the menu before measurement and stop after ambiguous communication failures. Blindly retrying a missed-looking arrow press could apply the adjustment twice.

The other routes remain secondary:

| Route | Assessment |
|---|---|
| Separate JSON-RPC IP control, ports 1515/1516 | Implementations exist for other Samsung models. Exact 2016 compatibility and RGB/CMS access remain unproven. |
| Public Tizen APIs | The examined `TvInfo` API does not expose the required white-balance/gamma/CMS controls. |
| Legacy Samsung remote protocols | Possible alternative remote transport if the actual model requires one; not evidence of direct calibration access. |
| Infrared | Plausible menu-navigation fallback, with transmitter compatibility and state tracking still to solve. |
| HDMI-CEC | No verified calibration-control route found for this model. |
| DDC/CI | Windows exposes capability discovery and RGB controls for implementing displays; this TV’s support is unknown. |

The JSON-RPC implementation specifically warns that available methods differ between models. Microsoft likewise makes DDC/CI functionality conditional on the display’s implementation. :chatgpt-content-reference{index="5"}

For **your exact television**, backlight/brightness, contrast, colour/tint, RGB gain/offset, gamma, multipoint white balance and CMS must currently all be classified as **potentially accessible but not yet verified**. We cannot honestly assign them to “directly adjustable” until the model and physical tests establish that.

**3. Spyder5 access**

ArgyllCMS already supports the Spyder5, including display-spectrum corrections. We do not need to reverse-engineer its USB protocol to begin. :chatgpt-content-reference{index="6"}

The simplest interface is `spotread`:

```powershell
& 'C:\Argyll\bin\spotread.exe' '-?'
& 'C:\Argyll\bin\spotread.exe' '-e' '-x' '-c' '1' '-y' 'n' '-O'
```

Replace the path and instrument index with those from your installation.

Here, `-e` requests absolute emissive measurements, `-x` includes chromaticity, and `-O` performs one calibration or measurement and exits. Our wrapper requires an actual finite XYZ result; a successful process exit alone is insufficient. The generic `n` selection is for initial diagnostics, not a claim of accurate colour measurement on this display. :chatgpt-content-reference{index="7"}

Use your existing working installation first. Argyll’s Windows documentation explains its USB-driver requirements and switching between drivers; there is no reason to replace a functioning driver unnecessarily. :chatgpt-content-reference{index="8"}

For accurate work, we must select an appropriate correction. Argyll can import vendor calibration data using `oeminst`; that proprietary data is not included in its distribution. :chatgpt-content-reference{index="9"}

**4. Minimal combined proof of concept**

I would first close the loop around **backlight and measured luminance**. It provides a simpler test of automatic hardware adjustment before tackling interacting colour controls.

The proposed experiment is:

1. Record the original setting, input, picture mode and signal format.
2. Stabilise the display and hold one grey patch unchanged.
3. Take ten automatic baseline readings.
4. Change backlight by one validated step through software.
5. Clear the menu, allow settling and measure again.
6. Estimate the local response from setting change to luminance change.
7. Calculate a bounded second setting aimed at a nearby, predefined luminance target.
8. Apply it automatically and verify that the error decreases.
9. Restore the original setting and confirm both its displayed value and optical result.

The second adjustment follows the measured slope:

\[
s=\frac{Y_1-Y_0}{p_1-p_0},
\qquad
p_2=p_1+\frac{Y_{\text{target}}-Y_1}{s}
\]

The software must round to available setting increments and restrict movement to a small, validated range. If the response is indistinguishable from noise or drift, it stops.

**A manually positioned slider followed by scripted arrow presses is only an intermediate interface test.** Passing the full milestone requires repeated adjustment and measurement without manual menu navigation between readings.

**5. Application architecture—conditional on those tests**

I would keep full application development gated until the combined experiment passes.

The provisional design is straightforward: Python orchestrates separate meter, TV-control and pattern-generator components; an explicit state machine schedules operations; JSON or SQLite retains original settings, measurements and recovery state.

For optimisation, begin with bounded coordinate descent and measured control sensitivities. Accept changes against a collection of patches, rather than improving one patch while damaging the rest. Stop when improvements fall below measured uncertainty.

Argyll’s pattern tools can support initial generation and verification sweeps. A later custom Windows renderer is justified only if testing exposes a limitation. :chatgpt-content-reference{index="10"}

A Windows executable can eventually be packaged with PyInstaller. Bundling the program does not remove the need for working instrument drivers or dependency-licence compliance. :chatgpt-content-reference{index="11"}

**6. Accuracy and technical limits**

For a controlled dark-room SDR calibration, the starting target should be **Rec.709, D65 and approximately 100 cd/m²**, with the BT.1886 transfer function. Your previous 250 cd/m² is a brighter viewing target; luminance alone says nothing about calibration accuracy. BT.1886 accounts for measured black and white levels, so it is not always identical to a pure gamma-2.4 curve. :chatgpt-content-reference{index="12"}

Three issues deserve particular attention.

- **Meter uncertainty.** Repeated readings reduce random noise, but do not remove spectral mismatch or establish sensor accuracy. If this is the quantum-dot KS7000, choosing a generic ordinary white-LED correction merely because it is an LCD would be unjustified. A suitable CCSS can help; someone else’s meter-specific CCMX is not a calibration of your Spyder. :chatgpt-content-reference{index="13"}
- **Windows signal processing.** HDR, automatic colour management, Night Light, profile loaders and GPU transforms must be accounted for. Turning HDR off or clearing a legacy gamma ramp alone does not establish an untouched signal path. :chatgpt-content-reference{index="14"}
- **HDMI levels.** Full-range and limited-range output must match the television’s interpretation. Range conversion should happen once; combining application-level video encoding with another GPU conversion can distort the intended levels. :chatgpt-content-reference{index="15"}

My proposed verification procedure also treats **input, picture mode and SDR/HDR state as separate calibration contexts**. We must check the Shield, Apple TV and Xbox routes afterwards rather than assuming PC-input results transfer unchanged.

Native TV adjustments can benefit those sources when the relevant settings apply. PC ICC/GPU corrections affect the PC signal path. If reliable TV control ultimately fails, a measurement-guided manual TV calibration remains a useful fallback.

HDR should follow successful SDR testing: correct PQ output and HDR signalling add another verification problem.

**7. Development milestones**

| Milestone | Pass condition |
|---|---|
| Identify hardware | Full TV model, firmware, connectors and meter configuration recorded |
| Prove measurement access | Ten automatic valid readings with repeatability recorded |
| Prove picture adjustment | Software changes an ordinary setting and restores its confirmed original value |
| Prove autonomous control | Repeated menu navigation or direct writes work reliably; ambiguous failures stop safely |
| Prove feedback | Measured response determines a second adjustment that reduces error |
| Expand calibration | Grayscale, colours, clipping and independent playback checks improve together |
| Package application | Recovery and restoration work before unattended use |

**8. Costed requirements**

The first tests cost **£0**: existing PC, HDMI/network connections, Spyder5, ArgyllCMS and our code.

No additional hardware is currently justified. If Ex-Link proves necessary, we should identify the connector, electrical requirements and wiring before pricing a compatible cable combination within your **£25 delivered total**. Buying a generic serial lead now would be premature.

**9. First practical experiment**

Extract :chatgpt-content-reference{index="18"}[ACC_Probe_Kit.zip](sandbox:/C:/workspace/ACC_Probe_Kit.zip) and open PowerShell in the extracted folder. The README contains the full procedure.

First, query the TV using its actual local IP:

```powershell
py .\acc_probe.py tv-info --ip 192.168.1.50
```

Then enumerate the meter using your actual Argyll path:

```powershell
py .\acc_probe.py meter-info --spotread 'C:\Argyll\bin\spotread.exe'
```

With the Spyder positioned over a stable grey patch and competing meter applications closed:

```powershell
py .\acc_probe.py measure --spotread 'C:\Argyll\bin\spotread.exe' --instrument 1 --count 10 --display-type n
```

The kit saves raw responses, XYZ measurements, luminance, chromaticity and repeatability statistics. It also includes an optional Menu/Exit test and a supervised ordinary-slider adjustment test. **It does not yet implement automatic calibration.**

To resolve the decisive compatibility questions, send back:

- The **full TV model code and installed software version**.
- A photograph of the TV/One Connect **connector labels**.
- The `tv-info` and `meter-info` output.
- The measurement summary, if the meter test runs successfully.

The model code and connector photograph are the most useful next pieces of evidence.
