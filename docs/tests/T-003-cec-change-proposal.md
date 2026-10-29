# T-003 temporary CEC changes and restoration: planning proposal

**DOCUMENT-ONLY PROPOSAL FOR INDEPENDENT REVIEW. NOT READY / NOT AUTHORISED. No setting change or power operation is requested. This is not yet an executable physical plan.** Codex (OpenAI), 29 October 2026; S-086. Based on PR #36, reviewed head `4502b68373157848f4fc316c19aa713ce49efdf8`, adopted as merge `00d562921145a76fecf47ff316294623e507cfc2` with the same tree.

## 1. Purpose and unchanged boundaries

The owner prefers temporarily setting Samsung Anynet+ and Denon HDMI Control Off before a run, then restoring both On with a reminder ([verbatim preference S-085](../briefs/2026-10-29-t003-cec-restoration-preference.md)). This proposal identifies the effects and unresolved method details for that route. It does not investigate or adopt a replacement for the [tracked Off/Off criterion](T-003-discovery-preflight.md#tv-and-denon-checks), waive failed criteria, or make owner changes into look-only checks.

The proposed scope is one later T-003 discovery-only session, not blanket permission before every future run. Discovery retains its [separate package](T-003-discovery-execution.md), at most one invocation, no readings/presenter and unchanged stopping rules. The parent's [section 8](T-003-meter.md#8-owners-authorisation) remains the discovery authority record. The [readiness checklist](T-003-discovery-readiness.md) and D-021 exclusions remain in force. No Samsung update/version/queue investigation is revived.

## 2. Sources and their limits

Primary documents consulted read-only by Codex (OpenAI), **29 October 2026** (S-087). Statements about operation on this equipment remain **untested**. The proposed lifecycle below is AI: Codex planning, not a manufacturer procedure or observed result.

- **Samsung UE49KS7000UXXU:** [exact-model UK support](https://www.samsung.com/uk/support/model/UE49KS7000UXXU/) and the previously retained manufacturer [ENG-JZDVBEUK-1.1.3 e-Manual](https://org.downloadcenter.samsung.com/downloadfile/ContentsFile.aspx?CDSite=UNI_UK&OriginYN=N&ModelType=N&ModelName=UE49KS7000U&CttFileID=6648666&CDCttType=UM&VPath=UM%2F201612%2F20161209100212986%2FENG-JZDVBEUK-1.1.3.pdf). The live PDF request was unavailable through the web tool; the retained PDF was rehashed as `816e1c6f563aac973b676f68f73e623dead66163141c5a74f53357150422a3bc`, then PDF pages 67 and 89 (printed 62 and 84) rendered and visually inspected. These describe the Settings → System → Expert Settings → Anynet+ (HDMI-CEC) route, On for compatible device control and Off to exit Anynet+. Configuration/view-switch messages can temporarily make the remote unavailable. They do not guarantee immediate switching, exact current firmware presentation, uninterrupted visibility or complete restoration. No troubleshooting scan, cable reconnection or TV power cycle from that page is adopted.
- **Denon AVC-X3800H EU/EN manual, revision unstated:** [HDMI Setup](https://manuals.denon.com/AVCX3800H/EU/EN/GFNFSYkabkahie.php), sections HDMI Control and ARC: On enables linked operation, Off disables HDMI Control; changing HDMI Control calls for resetting power to connected devices. Restoring On is also a change. TV-remote volume control can remain available with receiver HDMI Control Off when ARC is On; TV HDMI Control is a prerequisite for ARC. These distinguish dependent functions rather than proving this installation's behaviour. The page does not give a device-specific reset sequence or duration for this PC/receiver/TV path.
- **Same Denon manual:** [Menu operations](https://manuals.denon.com/AVCX3800H/EU/EN/GFNFSYwahcrdvi.php) describes SETUP/BACK and separate navigation/value-edit roles. [HDMI Control setting procedure](https://manuals.denon.com/AVCX3800H/EU/EN/GFNFSYkfayrqor.php) includes input switching and a linked-standby check. Those setup/test actions are not silently imported into discovery or this proposal. They would need their own explicit bounded scope if required.

Disabling these functions can remove linked remote/power/audio conveniences; that is a planning consequence inferred from the documented functions, not a claim that all HDMI communication or every interruption path is isolated. No reliable audio/video continuity, automatic restoration or safe timing is established by these sources. Samsung overlay/configuration behaviour remains relevant to the change itself, separately from D-021's retired update questions.

## 3. Proposed original-state and restoration record

Actual values belong in a fresh ignored private record **before** any later authorised change; none are supplied here. Earlier private observations must retain their dates and cannot be relabelled as fresh.

| Item | Proposed target before discovery | Proposed restoration target | Actual pre-change / after-change / restored evidence |
|---|---|---|---|
| Samsung Anynet+ | Off | On, as requested; reconcile with the freshly recorded original value before authority | NOT OBSERVED HERE |
| Denon HDMI Control | Off | On, as requested; reconcile with the freshly recorded original value before authority | NOT OBSERVED HERE |
| Relevant existing ARC / linked-power / input settings and indications | Record only; no subordinate setting change included | Preserve/reassess against original record; differences stop the procedure | NOT OBSERVED HERE |
| Display/input state and affected device power states | Explicit baseline and restoration scope still to be settled | Return only by the separately reviewed method | UNRESOLVED |

An original value differing from the intended On restoration target is a planning discrepancy, not permission to overwrite it. No factory reset, service menu, ARC change, cable operation, device scan, other-zone operation or PC setting change is included. If a dependent value changes automatically, retain it as a deviation and stop; do not repair it under an assumed restoration mandate.

## 4. Candidate lifecycle and holds for the executable amendment

This is the order to complete in documentation and review, not instructions to perform now:

1. **Resolve the connected-device power-reset method.** Identify the finite affected device set from existing owner knowledge, including relevant HDMI inputs and outputs, and the exact ordinary power controls, order, PC/session consequences and restoration. An input-only account is insufficient to cover other outputs. Do not infer that a Denon-only standby cycle, an unplug, a factory reset or an ignored reset note is sufficient. No survey or power trial is requested by this proposal. Both Off and On transitions need this treatment.
2. **Write and independently review the exact owner-operated change/restore sequence.** Specify normal-menu selection/confirmation/exit for the two settings, supported values, original-state capture, dependent-setting effects, reset scope and failure/restoration handling. Known menu routes alone do not establish firmware-specific editing details or a validated reset method. No guessed key sequence is supplied. Resolve stage 1 before representing the sequence as executable.
3. **Obtain dated, exact owner authority after review and owner merge.** Authority must separately cover the change, associated power actions and restoration; planning preference or a reminder is not authority. No pre-change physical step is allowed before that authority. Discovery itself still needs its own parent-section-8 record at the applicable reviewed revision.
4. **Only under that completed future plan:** the owner records originals, makes the authorised changes, handles the reviewed reset/closure steps and reassesses affected preflight records. A loss of desktop, changed input, unexpected setting, configuration message or uncertain result prevents proceeding to discovery. All menus must be closed and required fresh evidence supported. A changed/restarted state invalidates affected old observations until reassessed.
5. **Keep discovery separate.** A favourable change result alone never starts Argyll. A fresh console, hashes, identity/environment/isolation/driver checks, Windows Update/active-hours fit and every other remaining gate stay required under the discovery package. No menu/power/restoration action is added during an outstanding invocation.
6. **At the appropriate completed-session boundary:** remind the owner to restore the two settings to the agreed recorded originals (intended On/On), using the reviewed restoration and power-reset method, and record actual outcomes. If no discovery is launched after a setting change, that changed state also needs the reviewed closure/restoration path. If discovery is outstanding, late, interrupted or completion-unconfirmed, its unchanged waiting/recovery rules control; do not act on the reminder as automatic normal cleanup. The owner's unconditional right to end activity remains.

**Current hold:** stages 1–3 are incomplete. This document can be reviewed as a source-grounded planning proposal, but cannot be used to authorise or carry out the setting changes. A later tracked amendment must resolve the method and receive independent cross-vendor review and owner merge before execution authority is sought. This hold does not require reopening D-021 questions or collecting later-reading/component prerequisites.

## 5. Reminder and recordkeeping

The owner's requested completion reminder covers Anynet+ and HDMI Control restoration. The separate Windows display-off restoration preference remains on the private completion checklist; no PC change is added here. Reminders prompt the owner at the appropriate completion boundary and do not operate equipment, promise successful restoration or create timed/recurring automation. Record restored, deferred or unknown separately for each item; missing confirmation is never a completed restoration.

No measurement occurs, so D-013's change/exit/wait/read cycle is not exercised. No two-second patch wait, warm-up, second display or optical check is added. No purchase or paid service is needed; proposed additional spending is £0. Other dependencies, operating commands, discovery attempt allowance, source/test baselines and stop procedures are unchanged.

## 6. Authorisation and results

- Change/restoration authority: **NONE**.
- Exact executable reset/change sequence: **UNRESOLVED**.
- Discovery authority: **NONE**, recorded only in the parent plan if later granted.
- Settings changed or restored for this proposal: **NOT PERFORMED**.
- Equipment results or continuity/restoration validation: **NONE**.
- Independent planning review: requested from Claude Code (Anthropic) or Antigravity (Google); no approval claimed.
