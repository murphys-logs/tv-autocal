# tv-autocal

A free, open-source Windows application, written in Python, for **closed-loop, TV-side colour calibration** of a Samsung Smart TV. 

Instead of applying color corrections on a PC, `tv-autocal` commands the TV's own internal hardware picture controls directly over a physical serial connection, measures the resulting light with a colorimeter, and optimizes settings iteratively until display output matches broadcast/cinema standards.

> **Current Status (October 2026): Planning, research, and software simulation.**  
> There is no application code on real hardware yet. All hardware claims remain untested on the owner's equipment.  
> Formal claim statuses, decisions, and evidence are tracked in [LEDGER.md](LEDGER.md).

---

## 1. Project Goals

* **Target Display:** Samsung UE49KS7000UXXU (2016 Quantum Dot SUHD).
* **Primary Target (SDR Video):**
  * **Color Gamut:** ITU-R BT.709 (Rec.709 standard HD color space).
  * **White Point:** CIE Standard Illuminant D65 ($x = 0.3127, y = 0.3290$).
  * **Transfer Function (EOTF):** ITU-R BT.1886 gamma curve built on display black and peak white.
* **Secondary Target:** HDR10 PQ tracking investigation (deferred to subsequent phases).

---

## 2. Core Architecture & Hardware

| Component | Hardware / Software Channel | Role & Status |
|---|---|---|
| **TV Control Backend** | Samsung Ex-Link (RS-232 via 3.5mm jack) | 7-byte binary command framing at 9600 8N1. Hardware compatibility untested. Network/IR control is out of scope (D-006). |
| **Measurement Service** | Datacolor Spyder5 via ArgyllCMS (`spotread -O`) | Reads screen emission with CCSS quantum-dot spectral correction. Subprocess integration. |
| **Pattern Generator** | Full-screen Python renderer (Pygame / SDL2) | Outputs bit-exact windowed patches (18% window, 18% APL) via PC (NVIDIA GTX 1080) &rarr; Denon AVR &rarr; TV. |
| **Optimization Engine** | Python / NumPy / colour-science | Damped least-squares solver calculating discrete integer setting changes to minimize $\Delta E_{2000}$. |
| **Measurement Cycle** | Sequence: `Change -> Exit Menu -> Settle Delay -> Read` | Mandated by decision D-013. Eliminates on-screen menu interference during probe readings through deterministic sequencing. |

---

## 3. Collaborative Multi-Agent Workflow

This project is developed collaboratively by the owner and **three independent AI coding agents**:
* **Claude Code** (Anthropic) &mdash; working on `claude/<topic>` branches.
* **Codex** (OpenAI) &mdash; working on `codex/<topic>` branches.
* **Antigravity** (Google) &mdash; working on `antigravity/<topic>` branches.

All agents operate under the rules in [AGENTS.md](AGENTS.md):
1. **Never commit directly to `main`:** All work is proposed via pull requests.
2. **Cross-Vendor Peer Review:** Substantive PRs must be independently reviewed by an agent from a different AI vendor before merging.
3. **Owner Authority:** Only the owner authorises physical tests and merges pull requests.
4. **Zero Autonomous Hardware Actions:** No agent operates real hardware without an explicitly approved test plan and the owner present.

---

## 4. Hardware Budget

* **Budget Limit:** Strictly capped at **£25.00** total (D-001).
* **Spent:** £15.99 on DSD TECH USB-to-RS232 FTDI FT232RL 3.5mm serial cable (C-008).
* **Remaining Balance:** **£9.01**.

---

## 5. Active Decisions Waiting for Owner

| ID | Decision Question | Options | Current Agent Consensus | Blocks |
|---|---|---|---|---|
| [T-001, T-002](docs/equipment.md#what-we-still-need-from-you) | Visual equipment check: TV firmware, menu controls, PC/AVR connection | Look-only report | Complete owner checklist before physical tests | Stage 1 & physical plans |
| [Q-001, Q-016](LEDGER.md#6-open-questions) | Spectral correction validation criteria without a reference spectrometer | Block T-008 / Borrow reference / Proceed with unvalidated label | Research candidate CCSS fingerprints | Stage 4 (T-004) & Stage 6 (T-008) |
| [Q-008](LEDGER.md#6-open-questions) | Post-menu-exit settle delay duration before taking probe readings | Delay interval in seconds | Propose measured timing in Stage 3 simulations | All test plans with readings |
| [Q-013](LEDGER.md#6-open-questions) | Fallback path if TV Ex-Link port does not accept picture control commands | Guided manual adjustment / Service-menu step / Revisit interface | Agents recommend guided manual adjustment as primary fallback | Stage 2 fallback architecture |
| [Q-014](LEDGER.md#6-open-questions) | Target peak luminance and black-level handling for first calibration | 100–130 cd/m² vs dim-room targets; measured black vs nominal ratio | Agree provisional targets in Stage 2; finalize after T-003 | Component test plans; T-008 |
| [Q-002, Q-003](LEDGER.md#6-open-questions) | Open-source license and Python distribution packaging approach | MIT / GPL / Apache 2.0; PyInstaller standalone bundle | Open-source compliant with ArgyllCMS & dependencies | Application distribution |

---

## 6. Repository Structure

* [AGENTS.md](AGENTS.md) &mdash; Multi-agent operating rules, safety boundaries, and workflow protocols.
* [LEDGER.md](LEDGER.md) &mdash; Formal record of sources, claims, decisions, disagreements, and budget.
* [docs/plan.md](docs/plan.md) &mdash; Staged technical roadmap from owner checks to full SDR calibration.
* [docs/workflow.md](docs/workflow.md) &mdash; Plain-English guide to PRs, reviews, and test authorisations.
* [docs/equipment.md](docs/equipment.md) &mdash; Hardware specifications and look-only owner checklist.
* [docs/research/](docs/research/README.md) &mdash; Archived protocol investigations and feasibility research.
* [docs/tests/](docs/tests/README.md) &mdash; Physical test plans, safety templates, and test results.
