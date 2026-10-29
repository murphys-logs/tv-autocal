# Tests on the owner's equipment

This folder holds the plans, authorisations and results of every test that involves the owner's real equipment: the TV, the Spyder5, the Denon receiver, the Ex-Link cable, or the PC when it is driving any of them. It answers *"what actually happened on the owner's equipment?"*.

Software-only simulations do not belong here and need no authorisation, because they never touch the equipment. Their results must always be labelled as simulations.

## Plans awaiting independent review

PR #26 reviewed the execution amendments; PR #27 merged the [readiness changes](../software/component-readiness.md), and PR #28 merged the owner-input reconciliation. PR #29 merged the [T-003 discovery-only execution package](T-003-discovery-execution.md). PR #30 merged D-020's accepted owner choices, the reviewed [console amendment](T-003-discovery-console.md) and [private-record template](T-003-discovery-record.example.md). PR #31 merged the [locking/standby preflight](T-003-discovery-preflight.md), with visual owner checks, separate software-only registry preparation and Windows update gates. PR #32 merged the Samsung update/restart gate and source/status follow-up. PRs #33/#34 merged the [Samsung method](T-003-samsung-update-evidence.md) and research. Owner decision D-021 retires that method and removes the Samsung clarification questions as readiness prerequisites; PR #35 merged that amendment. The [remaining readiness checklist](T-003-discovery-readiness.md) separates preparation, authority and later session checks; it needs independent review. This index publishes no current session values. T-005/T-006 operating sequences are unchanged. All three plans below are **NOT AUTHORISED** and have **no equipment results**; preparing or merging a plan does not authorise a test.

| Plan | Scope | Execution prerequisites still open |
|---|---|---|
| [T-003 meter](T-003-meter.md) | [Discovery-only package](T-003-discovery-execution.md) for steps 1–4 first; later readings separately authorised | D-020 answers Q-020; PRs #31/#32 reviews complete. D-021 merged in PR #35; remaining private visual/software preparation, actual session checks and exact authority remain open; Samsung clarification questions are not required |
| [T-005 signal path](T-005-signal-path.md) | Clipping/stability screening; correct range interpretation remains unproved | Authorisation; display/runtime inputs and separate visual runs; T-003 before optical steps; additional method for Stage 4 range gate |
| [T-006 Ex-Link](T-006-exlink.md) | Electrical gate, bounded ordinary control, menu exit and restoration | Authorisation; electrical evidence, scope/restoration, menu timing and exact connection/stop procedures |

The [T-009 prototype](../software/t009-prototype.md) is separate software-only work. It cannot run these plans, display patterns or contact a device. The [bounded component tools](../software/component-tools.md) were reviewed and merged in PR #24, followed by PR #25's documented console limitation; their hardware paths remain unoperated. PR #26 supplied execution amendments and PR #27 merged the current presenter/meter implementation. The [shared execution record](component-execution.md) distinguishes the pinned software from the still-unfilled reviewed plan revision and local identities. S-053 records the intended two-screen layout and D-019's accepted generic-only diagnostic and timing policies; neither is a completed setup or test authorisation. [Unresolved inputs](component-execution.md#unresolved-inputs) remain explicit; merging a further amendment will not authorise any physical test step.

The separate [temporary CEC change/restoration proposal](T-003-cec-change-proposal.md) records the owner's preferred route and outstanding reset/method/authority holds. It is not executable and supplies no completed readiness or settings result.

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
