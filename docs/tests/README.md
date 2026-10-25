# Tests on the owner's equipment

This folder holds the plans, authorisations and results of every test that involves the owner's real equipment: the TV, the Spyder5, the Denon receiver, the webcam, the Ex-Link cable, or the PC when it is driving any of them. It answers *"what actually happened on the owner's equipment?"*.

Software-only simulations do not belong here and need no authorisation, because they never touch the equipment. Their results must always be labelled as simulations.

## Ground rules

- **No physical test without the owner's explicit authorisation of that specific plan** ([AGENTS.md section 7](../../AGENTS.md#7-equipment-safety-rule-6)). If the owner authorises in conversation, their words are copied into the plan before any step is carried out.
- **Only the authorised steps, with the owner present.** Anything else needs fresh authorisation. The owner can stop a test at any time.
- **Record what actually happened** — including failures, surprises and anything done differently from the plan. Never fill in expected or typical values.
- **Write down original settings before changing anything**, so they can be restored.
- **Keep the three kinds of meter reading apart** — diagnostic, guard-validation and accepted calibration readings, described in [docs/plan.md](../plan.md#three-kinds-of-meter-reading). Only accepted readings can be used to calibrate or to judge accuracy, and a reading can never be moved to a higher kind later.

## Life of a test

| Step | What happens | Test status in the ledger |
|---|---|---|
| 1. Plan | An agent copies [TEMPLATE.md](TEMPLATE.md) to `T-NNN-short-title.md` (`NNN` is the test's ledger number), fills in the plan sections and opens a pull request. | Planned |
| 2. Review | The other company's agent reviews the plan, as for any pull request. | Planned |
| 3. Authorise | The owner fills in the authorisation section, or authorises in a pull-request comment or in conversation; their words are copied into the file. | Authorised |
| 4. Carry out | Only the authorised steps, with the owner present. | Authorised |
| 5. Record | Observations go in the results section. Data files go in a `T-NNN-data/` folder, after private details such as serial numbers and network addresses have been removed. Webcam pictures stay in the private `local/` folder unless the owner approves a specific picture (D-009 item 5). | Done |

After step 5, the equipment test status of each claim tested changes to Confirmed, Contradicted or Inconclusive in the ledger, with a link to the results.

## Owner checks

Some ledger entries are "owner checks": the owner looks something up for themselves — a firmware version, a menu, a cable — without a meter and without any agent operating the equipment. These need no plan or authorisation. The owner reports what they found, and an agent records it in the ledger with the owner as the source.

An owner check only looks. Anything that connects, sends, measures or changes something for the project — plugging the Ex-Link cable into the TV, running ArgyllCMS with the meter, recording with the webcam, or changing a TV, PC or receiver setting — belongs in a written test plan, so that its risks and its record are thought through first. Owner checks never involve the service menu. The current list of owner checks is in [docs/equipment.md](../equipment.md#what-we-still-need-from-you).
