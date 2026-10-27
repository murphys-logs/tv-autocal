# Tests on the owner's equipment

This folder holds the plans, authorisations and results of every test that involves the owner's real equipment: the TV, the Spyder5, the Denon receiver, the Ex-Link cable, or the PC when it is driving any of them. It answers *"what actually happened on the owner's equipment?"*.

Software-only simulations do not belong here and need no authorisation, because they never touch the equipment. Their results must always be labelled as simulations.

## Plans awaiting independent review

All three plans below are **NOT AUTHORISED** and have **no equipment results**. Each identifies unresolved execution prerequisites; preparing or merging a plan does not authorise a test.

| Plan | Scope | Execution prerequisites still open |
|---|---|---|
| [T-003 meter](T-003-meter.md) | Device discovery, actual readings, repeatability, drift and observed usable range | Review/authorisation; reviewed patch renderer before measurement steps |
| [T-005 signal path](T-005-signal-path.md) | Source-code levels, visual clipping checks and relative optical response | Review/authorisation; reviewed renderer; T-003 evidence before optical steps |
| [T-006 Ex-Link](T-006-exlink.md) | Electrical gate, bounded ordinary control, menu exit and restoration | Electrical evidence, scope/restoration amendment, reviewed physical sender, review/authorisation |

The [T-009 prototype](../software/t009-prototype.md) is separate software-only work. It cannot run these plans, display patterns or contact a device.

## Ground rules

- **No physical test without the owner's explicit authorisation of that specific plan** ([AGENTS.md section 7](../../AGENTS.md#7-equipment-safety-rule-6)). If the owner authorises in conversation, their words are copied into the plan before any step is carried out.
- **Only the authorised steps, with the owner present.** Anything else needs fresh authorisation. The owner can stop a test at any time.
- **Record what actually happened** — including failures, surprises and anything done differently from the plan. Never fill in expected or typical values.
- **Write down original settings before changing anything**, so they can be restored.
- **Every reading follows [change, exit, wait, read](../plan.md#measurement-cycle-and-use-of-readings) (D-013).** Each plan shows how, in section 6 of the [template](TEMPLATE.md).
- **Keep diagnostic evidence separate from calibration data** ([use of readings](../plan.md#measurement-cycle-and-use-of-readings)).

## Life of a test

| Step | What happens | Test status in the ledger |
|---|---|---|
| 1. Plan | An agent copies [TEMPLATE.md](TEMPLATE.md) to `T-NNN-short-title.md` (`NNN` is the test's ledger number), fills in the plan sections and opens a pull request. | Planned |
| 2. Review | An agent from a different company reviews the plan, as for any pull request. | Planned |
| 3. Authorise | The owner fills in the authorisation section, or authorises in a pull-request comment or in conversation; their words are copied into the file. | Authorised |
| 4. Carry out | Only the authorised steps, with the owner present. | Authorised |
| 5. Record | Observations go in the results section. Data files go in a `T-NNN-data/` folder, after private details such as serial numbers and network addresses have been removed. | Done |

After step 5, the equipment test status of each claim tested changes to Confirmed, Contradicted or Inconclusive in the ledger, with a link to the results.

## Owner checks

Some ledger entries are "owner checks": the owner looks something up for themselves — a firmware version, a menu, a cable — without a meter and without any agent operating the equipment. These need no plan or authorisation. The owner reports what they found, and an agent records it in the ledger with the owner as the source.

An owner check only looks. Anything that connects, sends, measures or changes something for the project — connecting either end of the Ex-Link cable, running ArgyllCMS with the meter, or changing a TV, PC or receiver setting — belongs in a written test plan, so that its risks and its record are thought through first. Owner checks never involve the service menu. The current list of owner checks is in [docs/equipment.md](../equipment.md#what-we-still-need-from-you); the cable-check difference from the earlier proposal is recorded in X-009.
