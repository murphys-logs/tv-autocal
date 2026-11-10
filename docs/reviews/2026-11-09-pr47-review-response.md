# PR #47 review response — CEC method and first-discovery readiness

Codex (OpenAI), author follow-up 10 November 2026; reviews and owner D-023 choice received 9 November (S-126/S-127). This records retrieved reviews and proposed author corrections, not equipment results or changed-head approval. Every review below covers **`fa6710ee6307af90be42480f578f03ee6153ad41`**, against **`a545dc5171581ce3c322223c75e53e21d6229e7c`**. Their recommendations are not carried forward to the revised head.

## Retrieved reviews and coverage limits

| Review actually retrieved | Recommendation and relevant coverage |
|---|---|
| [Claude Code (Anthropic), formal review 5834498728](https://github.com/murphys-logs/tv-autocal/pull/47#pullrequestreview-5834498728) | Change first: R1–R3, optional O1/O2. Claude independently assessed the tracked-authority gap, re-read the Denon English/German HDMI Setup and front-panel sources, and reported link/ID/whitespace checks. Microsoft pages were not re-fetched and the retained Samsung manual was not inspected. Claude supports the ordinary-control interpretation as reasonable for this bounded proposal, not evidence of successful operation |
| [Antigravity (Google), formal review 5834528999](https://github.com/murphys-logs/tv-autocal/pull/47#pullrequestreview-5834528999) | Merge at the old head, with no findings. Google reported eight public-source fetches, mechanical checks and an offline test run. It disclosed no access to private local records, unredacted configuration or the original chat beyond the archived brief. Those are reviewer-reported checks, not new author runs or equipment evidence |
| [Automated Codex review 5834234564](https://github.com/murphys-logs/tv-autocal/pull/47#pullrequestreview-5834234564) | Its [P1 finding](https://github.com/murphys-logs/tv-autocal/pull/47#discussion_r4519143880) identifies the missing tracked CEC-authority location. This is the author's vendor, OpenAI, and does not count as independent review. Claude's R2 expressly concurs after its own assessment |

The Google approval does not cancel Claude's required findings. Neither review supplies execution permission. This response was prepared from the GitHub review bodies and inline findings; no manufacturer was contacted and no equipment, console/registry procedure, Argyll command or physical trial was performed for it.

## Proposed corrections for changed-head review

| Item | Author disposition and retained boundary |
|---|---|
| [R1 — connection warning](https://github.com/murphys-logs/tv-autocal/pull/47#discussion_r4519362473) | Accepted. Make the PR summary and S-124 record state plainly: **do not connect Ex-Link**. [T-006's electrical gate](../tests/T-006-exlink.md) remains missing and permits no connection; T-003 requires both Ex-Link ends disconnected. This PR does not complete every prerequisite to connecting equipment. The [readiness checklist](../tests/T-003-discovery-readiness.md) identifies remaining Spyder/discovery gates |
| [R2 — tracked CEC authority](https://github.com/murphys-logs/tv-autocal/pull/47#discussion_r4519363045) | Accepted, including the same-vendor P1 finding. Add a separate tracked owner-authorisation section 10 to the [CEC method](../tests/T-003-cec-ordinary-control-method.md), initially **NONE**, with the reviewed plan commit, covered steps/both directions, date and verbatim owner words. Require that record before step 4.1. Private equipment values remain private; parent T-003 section 8 stays discovery-only |
| [R3 — Windows Update criterion](https://github.com/murphys-logs/tv-autocal/pull/47#discussion_r4519363628) | Accepted: the owning [first-discovery exception in readiness](../tests/T-003-discovery-readiness.md#first-discovery-windows-update-exception--d-023) records the new explicit owner choice, **D-023/S-127**, rather than inferring a waiver from S-124. The owner selected the Codex-worded option “Narrow for first discovery only (recommended)”. The proposed first-discovery exception requires no further collection for that scope; unknown fields stay unknown, interruption/restart risk and existing stop rules remain visible, and later scopes retain their requirements. Independent review and owner merge are still required before using the exception; it grants no physical authority |
| [O1 — restoration references](https://github.com/murphys-logs/tv-autocal/pull/47#discussion_r4519364013) | Accepted. Name section 4 steps 4–6 as the reused Off/On phases, then section 6 step 4 for restored-state verification. Do not reuse section 4 step 7's Off/Off criterion after restoration or repeat the Off-setting edits |
| O2 — spacing and ownership | Accepted. Keep the Windows Update decision in readiness and link to it from the CEC method; remove the detached duplicate paragraph/spacing. Do not duplicate or silently retain an inconsistent criterion |

These fixes are implemented and document checks pass; independent review of the final changed head remains outstanding. The tracked CEC section is unfilled, discovery authority and physical results remain absent. The owner's D-023 choice is a specific planning decision; it is not authorisation to change CEC settings, cycle power, connect equipment or launch discovery.

## Review statements that do not become guarantees

Google's explanation that PC-first shutdown keeps video visible until shutdown completes, and TV/receiver-first startup establishes the HDMI chain before the PC boots, is an expected workflow rationale. The cited material and review establish neither uninterrupted video nor successful HDMI/EDID negotiation on this installation. The order remains the author's candidate choice; linked-power actions, standby pass-through, Windows shutdown semantics and unexpected visibility/state changes retain the method's checks and failure branches. Agreement between vendors does not validate reset sufficiency or restoration.

The Google-reported offline test result does not test this physical procedure. No connection, CEC edit, power cycle, successful restoration, Spyder recognition or measurement is reported by this response. Changed-head independent review is needed, with fresh prompts prepared for both vendors; only the owner decides whether to merge, and exact later physical permission remains separate.

## Author verification — 10 November 2026

The combined diff against the stated main base contains 14 Markdown files. `git diff --check` passes; 561 relative links/anchors resolve, all 364 referenced ledger IDs are defined, and there are 364 unique definitions with no duplicates. The checked diff contains no private user paths, application/test/workflow changes or edits to merged brief/research archives; the private validation files remain ignored.

S-127's complete question, both options and selected answer match the retrieved current-chat source exactly. S-124's original brief and D-019 through D-022 are unchanged. Fenced command blocks in the affected execution/preflight/identity documents, the ten-file fingerprint manifest and parent T-003 authority document are unchanged. Internal same-vendor document QA found no remaining scope/authority/restoration inconsistency; this does not count as independent review. No application suite, Argyll, console/registry preparation or equipment procedure was run for this documentation revision.
