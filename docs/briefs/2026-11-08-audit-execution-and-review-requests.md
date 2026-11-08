# Issued audit and review requests — 8 November 2026

Source: the owner's actual messages to Codex in the audit conversation, reproduced below. The first message uses the wording of the Codex (OpenAI)-drafted prompt at [PR #38's pinned draft](https://github.com/murphys-logs/tv-autocal/blob/75cec90159711401ada5ff52a479a366ccc73c61/docs/reviews/2026-11-08-ground-up-review-prompt.md); its full prompt body was compared with the issued message and matches. Provenance is **Owner-issued, wording drafted by Codex (OpenAI)**. The two follow-ups are owner messages; no drafting provenance is asserted for them. Source S-097.

This is separate from PR #38's earlier request to prepare a prompt. The authority comes from the issued messages, together with the existing project instructions, not from assuming that an unmerged AI draft is binding. Dates are the conversation date; exact message times are not recorded. The surrounding environment metadata and assistant replies are not part of these quotations. No equipment authority is given.

## Issued audit instruction — verbatim

You are Codex (OpenAI), conducting a complete, independent, ground-up review of https://github.com/murphys-logs/tv-autocal/.

Reconstruct the project's technical case from first principles and inspect the entire implementation. Interrogate every supposed fact and challenge every existing conclusion whose evidence does not support its wording, scope or certainty. Include your own vendor's previous work. A merged PR, a confident report, a passing test suite or agreement between agents does not make a claim correct.

Do the review and produce a reviewable GitHub PR. Do not stop at a plan, a summary of earlier reports, or a review of only the latest changes.

### 1. Establish the baseline and authority

Read the current AGENTS.md, LEDGER.md, README.md, documentation index, applicable nested instructions, PR template and relevant owner briefs. Inspect open PRs, branches and relevant history. Record the repository, default branch, full starting commit SHA, tree state and review date. Use an isolated codex/ branch; preserve unrelated work and never commit directly to main.

Read the live repository rather than trusting this prompt's preparation date. At preparation, main was bcaf3d38ef03dca3b1607e0cb36c09ee3ea8f2b2; that is a locator for this prompt's context, not a requirement to review an obsolete version.

Distinguish owner requirements from empirical assertions. Owner choices about budget, interfaces or priorities remain requirements; their technical rationale and feasibility are open to challenge. If a requirement prevents the goal, explain the conflict and propose an explicit decision instead of silently relaxing it. Critique governance and readiness procedures too: identify obsolete, contradictory or disproportionate steps, supported by evidence. Keep their current operational boundaries in force while proposing changes.

Follow the current equipment and approval rules. This review permits repository work, source research and hardware-free software validation. It is not authorisation to operate the TV, Spyder5, Denon, serial interface, service menu or home network, display measurement patterns, make purchases, enable automation, deploy, merge or change repository settings. Inspect tests and entry points before running them; a command labelled "test", "help" or "discovery" is not automatically hardware-free. Continue all independent work when a hardware check is unavailable, and record the exact remaining check.

### 2. Cover the whole project

Build a coverage inventory before drawing conclusions. Read every maintained source, test, configuration and documentation file. Inspect archived research and briefs as evidence of what was claimed or instructed; use relevant commits and PR discussions to resolve provenance, supersession and review history. Identify generated or third-party material and justify any exclusions. Do not hide omissions behind "representative sampling".

Cover at least:

- Requirements, actual implementation status, architecture, interfaces, feasibility, dependency order and the route to a working application.
- All software in tv_autocal/ and tv_autocal_tools/, all tests, dependency declarations, entry points, installation and Windows assumptions, packaging, licences, security and privacy.
- README, ledger sources/claims/decisions/disagreements/tests/questions, claim notes, equipment records, plans, software documentation, physical-test procedures and prior reviews.
- The gap between what documentation promises, what source code implements, what software tests demonstrate and what the owner's equipment has actually demonstrated.

Create a traceable coverage table with path or area, review method, evidence and outcome, including anything not assessed and why. Extend the list if the live repository contains more than the paths named here.

### 3. Audit facts and reasoning

Inventory every explicit technical factual claim and every material implicit assumption, including claims embedded in comments, fixtures, commands, acceptance criteria and user instructions. Group duplicates only when each location is traceable. Include positive and negative claims: "supported", "impossible", "safe", "necessary", "validated", "bit-exact" and "reference accuracy" all require evidence.

For each claim record:

- Claim ID, exact proposition, locations, scope and dependencies.
- Provenance: owner report, primary documentation/source code, secondary account, named AI system, or no source.
- Source title/publisher, stable URL or document identifier, version/date, consulted date and precise section or code reference. Open sources directly and check that they support the claim. Report inaccessible or missing originals; never reconstruct them.
- An assessment: supported within stated conditions, partly supported/overstated, contradicted, unsupported, or unresolved; explain why and state confidence.
- Equipment-test status separately, using the repository's labels and linked observations. Documentation, code inspection, simulations and cross-vendor agreement are not tests on this equipment.
- What evidence would resolve any uncertainty, its effect on the design and the correction needed.

Prefer primary documentation, standards and the actual versioned upstream code. Check regional/model/firmware applicability, conflicting source passages, version drift and circular citations. Secondary reports can reveal hypotheses or discrepancies but must not silently become primary confirmation.

Re-derive calculations with explicit units, assumptions and independent reference values. Look for evidence that could falsify favoured explanations. Never interpret absence of evidence as proof of impossibility, or observed repeatability as established absolute accuracy. "Absolutely correct" means the wording stays within what the evidence establishes: narrow or withdraw overstated conclusions and label unknowns instead of manufacturing certainty.

### 4. Rebuild the complete calibration chain

Investigate these as questions, not established facts:

- Exact Samsung model/region/firmware and available normal-menu controls; whether another model's evidence transfers; source and picture-mode scope; persistence, readback, restoration and cross-input effects.
- Ex-Link connector/pinout, RS-232 electrical compatibility, cable/driver assumptions, serial parameters, packet/checksum construction, command provenance, argument ranges, acknowledgements, late responses and ambiguous outcomes. Separate public Ex-Link commands from proprietary DDC workflows. A socket, ACK or changed light does not establish every control or an exact stored setting.
- Spyder5 support in the relevant ArgyllCMS version, process and prompt behaviour, discovery versus measurement, correction formats and provenance, spectral mismatch, low-light limitations, drift, repeatability and absolute-accuracy limits.
- The entire pattern path: buffer values, geometry, window/compositor behaviour, display selection, DPI/scaling, Windows HDR/ICC/night-light processing, GPU RGB/YCbCr and range conversion, HDMI/receiver processing and TV decoding. Distinguish optical checks from independent proof of digital code fidelity.
- Rec.709/D65/BT.1886 and any HDR targets: correct formulae, chromatic adaptation where relevant, units, legal/full-range encoding, black/white assumptions, clipping and error metrics. Check what selected targets can mean when black level or meter accuracy is unknown.
- Optimisation and control: implemented versus proposed functionality, coupled controls, quantisation, noise, stability, convergence, bounds, stopping criteria and validation on measurements not used for optimisation.
- The required change/exit/wait/read cycle: timing assumptions, menu and other overlay contamination, stale or invalid readings, timestamp association, settling and acceptance rules.
- Failure and recovery: cancellation, timeouts, disconnects, partial I/O, retries, malformed/NaN/infinite/out-of-range data, child processes, restart state, logs/receipts, permission gates, simulation defaults and restoration limits.

Reassess whether the goal is attainable under the owner's current equipment, free/open-source Windows Python scope, Ex-Link-only choice and total hardware budget. Verify the live records for those constraints. Separate relative improvement, measurement-only capability, closed-loop control and validated absolute accuracy. Give a conditional verdict where decisive evidence is missing, with the smallest useful next evidence-gathering steps. Do not silently introduce a network-control fallback or commercial calibration package.

### 5. Validate the software and the tests

Establish a hardware-free baseline using the actual documented commands and record environment, versions, commands, outcomes and limitations. Distinguish pre-existing failures from effects of your changes. If the intended Windows environment cannot be exercised, say precisely what remains untested.

Inspect test design, not just pass counts. Check that expected values are independently justified and that mocks do not encode the same mistaken assumptions as the implementation. Use targeted independent calculations, adversarial inputs and regression reproductions for substantive suspected defects. Check safety containment, boundaries, errors and realistic integration failure modes. Do not write tests merely to mirror code or expand low-value coverage.

Review dependency integrity, subprocess argument handling, executable/path resolution, untrusted files and outputs, permissions, logs and credential exposure. Do not publish private device identifiers, network details, credentials or raw personal logs. Record security findings with redacted evidence.

### 6. Produce the audit and findings PR

Write a plain-English verdict followed by sufficient technical detail for a different reviewer to reproduce and challenge it. Include:

1. Scope, pinned baseline, environment and coverage map.
2. Claim/evidence matrix linked to the ledger and source locators.
3. Prioritised findings with stable IDs, severity, confidence, exact file/line or claim references, impact, reproduction/evidence, proposed correction and validation method.
4. A clear separation between demonstrated defects, unsupported conclusions, hardware-dependent questions and optional improvements; lack of implementation is not a bug unless promised behaviour requires it.
5. A reassessment of prior conclusions, including those upheld, narrowed or overturned and the evidence for each.
6. Test/experiment results, unavailable checks, residual risks, dependencies and a prioritised route forward.
7. Outstanding disagreements represented fairly, without forcing consensus.

Use the repository's existing locations: the audit and coverage record in docs/reviews/, detailed claim analysis in docs/claim-notes.md, and concise source/claim/status/disagreement records in LEDGER.md. Link rather than duplicate governing rules. Preserve merged archived originals; put corrections in maintained analysis and the ledger. Update indexes and the README decision list when relevant.

Open a new PR for the completed audit and evidence-backed documentation corrections. This prompt/specification PR is not the completed audit PR. Keep findings and any necessary validation fixtures clearly separated in commits; avoid turning the audit into an unreviewable redesign. Describe proposed implementation fixes precisely and use focused linked follow-up PRs where appropriate. Fill every section of the repository PR template. Do not merge.

The PR description must state what was actually reviewed, what changed, the exact baseline/head, checks run, remaining gaps and the requirement for both Claude and Antigravity to review it. An honest complete review may end with unresolved feasibility; never claim completeness while silently skipping an area.

### 7. After the audit PR exists, write two independent review prompts

Produce two separate, ready-to-paste prompts: one addressed to Claude Code (Anthropic), one to Antigravity (Google). Populate both from the actual finished PR with its URL/number, repository, base branch, full base/head SHAs, report/claim/coverage paths and reproducible verification commands. No guessed identifiers or placeholders in the delivered prompts.

Give both agents the same full remit: independently inspect the project, challenge the audit's evidence and conclusions, review every PR change, seek missed defects and verify important calculations, citations and reproductions. Neither may merely confirm the author's findings or split the project so that no one checks the whole.

Require a two-pass process. First develop their own assessment from the baseline project and primary evidence before reading this audit's conclusions or the other new review. Then compare it with the audit and review the exact diff. Disclose any prior involvement or unavoidable exposure. Independence is by vendor; same-vendor assistance is internal checking only.

Require each reviewer to:

- Read current project instructions and verify the supplied commits exist; pin their review to the supplied head. If it changed, identify the mismatch and explicitly review the new head or label the review stale.
- Reproduce material findings and inspect their proposed remedies; distinguish original defects from audit-introduced mistakes and unsupported criticisms.
- State scope, source checks, commands/results, limitations, disagreements and remaining gaps; give precise findings with evidence rather than stylistic preferences.
- Post a review on the audit PR, including the repository reviewer checklist and full reviewed SHA. If the shared account prevents APPROVE/REQUEST_CHANGES, post a COMMENT review with an explicit recommendation; if posting is unavailable, return the complete review text for the owner.
- Recommend merge, change first or cannot assess, with reasons and any blockers. Do not edit the author's branch, merge, or operate equipment.

Provide the two prompts to the owner after the audit, and place their fully populated text in the PR description or another stable review handoff location. Do not add a self-referential commit just to embed its own hash. Re-check the head after all content changes; refresh both handoffs if it changes.

Both real vendor reviews must be received before this requested review cycle can be called complete. After revisions, obtain review of the changed head from both vendors, retaining unresolved disagreements and evidence limits. Writing prompts, internal Codex checks or silence from a reviewer does not count as either review. Only the owner decides whether to merge.

### 8. Final response

Return the audit PR link, a concise verdict, the most significant findings, checks and limitations, then the complete Claude and Antigravity prompts. State plainly whether each external review is pending or actually completed.

## First review follow-up — verbatim

Check PR #39 for Claude and Antigravity’s reviews, assess every finding against the evidence, make justified corrections, and refresh both prompts for review of the updated head. Do not merge.

## Second review follow-up — verbatim

Check PR #39 for Claude and Antigravity’s reviews of the updated head. Assess every finding, make justified corrections, and refresh both prompts if the head changes. Do not merge.
