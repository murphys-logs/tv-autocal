# T-003 discovery-only locking and standby preflight

**Draft for independent review — discovery remains NOT AUTHORISED. No current settings were inspected, no Argyll program was run and no equipment was operated to prepare this amendment.** Codex (OpenAI), 28 October 2026, under [S-063](../briefs/2026-10-28-t003-preflight-amendment.md).

This supplements the [discovery package](T-003-discovery-execution.md) and [console instructions](T-003-discovery-console.md), reviewed through PR #30 at `c94d226ec156c92ae1ebfa233b536bcca987c62d` and merged as `4925daa6980fdd1e71200acc8dc2542457158f20` with the same tree. Review this amendment and its linked plan changes together at a new full commit before any discovery authorisation. PR #30's completed review is not pending again; the new preflight method is.

## Scope and order

The owner accepted waiting without forced recovery if discovery has not clearly returned before 60 seconds (D-020). A finite idle timeout merely longer than one minute does not accommodate that potentially open-ended wait. These proposed checks address known ways the ordinary desktop could disappear while the owner observes the console; they do not establish a safe abort, a guaranteed finish time or protection against power failure.

After independent review, the owner can report existing settings under the repository's [look-only owner-check rule](README.md#owner-checks), without separate physical-test authorisation. This document is preparation only, not a request to perform those checks now. No agent operates the PC settings or remotes. Owner checks do not connect, measure, alter the settings being inspected or run Argyll. The separate read-only registry preparation uses the already reviewed temporary console privacy controls below; it makes no persistent Windows, power, lock or equipment setting change. If a value cannot be read without changing it, leave it unresolved. Never enter a service menu.

Use the Samsung's already visible ordinary PC desktop, through the unchanged Denon input and TV HDMI 4; the LG remains deferred. Do not switch inputs, turn equipment on, connect a cable or alter the desktop to make this look-only check possible. If that starting state is unavailable, stop for a separately scoped setup plan. Record the date, original visible desktop/input indications and all actual values privately using the [record template](T-003-discovery-record.example.md#owner-look-only-preflight-record--before-discovery-authorisation). Defaults and earlier S-033 answers are not current observations.

Complete and assess these checks **before** requesting discovery authority or making its connection changes. Any settings, management, input or connection change afterwards invalidates the relevant record; an unexplained restart or newly reported lock also needs reassessment. Immediately before a later authorised launch, confirm the recorded conditions still apply and no relevant changes occurred. If uncertain, do not launch. No idle experiment, lock/standby trial, device enumeration or exhaustive application/task inventory is proposed.

## Windows checks

The existing [console guide, preparation steps 5–7](T-003-discovery-console.md#proposed-future-preparation--no-steps-to-carry-out-now), owns the plugged-in **Never** display-off/sleep/hibernate and **None** screen-saver criteria. Record all its fields, including screen-saver Wait and resume controls. Do not change them. Missing or ambiguous controls fail unless a reviewed, specific explanation establishes inapplicability.

Add these observations using ordinary Windows 10 Settings, reading without applying changes:

| Check | Proposed criterion / response |
|---|---|
| Accounts → Sign-in options → Dynamic lock | Existing option is Off/unchecked. On, missing or unclear is unresolved; do not pair, unpair or inspect Bluetooth devices. |
| Sign-in options → Require sign-in | Record the actual wording. A requirement to sign in after waking is not itself an independent lock timer and need not be disabled when the Never/None gate passes. An additional timed-away condition, policy restriction or unclear wording requires assessment. |
| Accounts → Access work or school | Record whether any connection or management indication is shown; keep organisation/account details private. Do not Connect, Disconnect, Sync or open a management action. A connection, managed-settings banner or uncertainty requires a targeted policy assessment; Home edition alone is not evidence of no management. |
| Owner knowledge | Record whether any known locking utility, scheduled locking task, remote-control arrangement, recent policy change or unexplained automatic lock exists. Any such item or uncertainty needs targeted assessment. A negative report is owner evidence, not a software inventory or proof that no application can lock Windows. |
| Machine inactivity policy | Use the bounded read below. An enabled timeout, wrong type, failed/unclear read or uncertainty about a recent change prevents readiness. Do not edit policy, elevate, refresh policy, reboot or install a policy editor. |

### Bounded policy read proposed for review

This checks one documented configuration location, **not whether every lock mechanism is absent or the Windows 10 Home installation honours that policy**. Microsoft's policy page defines zero/not configured as disabled; the registry mapping is documented in a Windows Server/RDS article. The Policy CSP edition table excludes Home, which is not proof that Home ignores the registry value. Treat a nonzero value conservatively as unresolved on this PC.

For the future owner check only, use the selected ordinary, non-elevated PowerShell and the [console guide's entry/host rules](T-003-discovery-console.md#proposed-future-preparation--no-steps-to-carry-out-now). Complete its steps 2–4 before entering these lines, including their session-only history/prediction changes; no Argyll command, connection change or discovery environment change is part of this check. Identify the existing Windows system `reg.exe` by its private absolute path rather than PATH lookup; record that path and verify it belongs to the existing Windows System32 directory. Missing/ambiguous identity stops preparation; do not download a substitute. These are command specifications with a placeholder, not commands to run now:

```text
& '<WINDOWS-SYSTEM32-REG-EXE>' query 'HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System' /v InactivityTimeoutSecs /reg:64
```

After it returns, record its complete output and immediately record `$LASTEXITCODE` before invoking any other native program. Require successful return and an unambiguous `REG_DWORD` value of `0x0` for the zero branch. A nonzero value or wrong type stops preparation. **Exit code 1 means failure, not “disabled” or “absent”.**

Only if the named-value query reports not found, the following one non-recursive read can distinguish a readable parent key with no such value from an inaccessible/missing key:

```text
& '<WINDOWS-SYSTEM32-REG-EXE>' query 'HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System' /reg:64
```

Retain its complete private output and immediate exit code. Accept the absence branch only if this second query succeeds, identifies the exact requested key and its complete value listing contains no `InactivityTimeoutSecs`. Missing key, access denial, truncated output, inconsistent results or any other failure remains **unknown**, not a pass. Do not recurse, query remote computers, inspect other registry trees or publish the raw listing. A positive zero/absence record establishes only no timeout configured at this location at that time. Any known or uncertain recent policy change or pending application of settings requires assessment; current registry contents alone do not establish which policy the running session loaded.

After return, use the reviewed GUI-copy method to select and copy the **entire registry output and each exit-code observation**, rather than just the discovery guide's status line. Keep it private. Close this idle preparation console normally; it is not the later discovery console and no attempt allowance has been consumed. Later authorised discovery retains all of its own fresh identity, host, environment and isolation checks. No registry command was executed while drafting this amendment.

## TV and Denon checks

These are **future owner look-only observations in normal menus**, completed and closed before discovery. They add no menu operation during an outstanding discovery attempt. Record each visible current value; do not press a toggle or change a value to reach the proposed criterion. If navigation or a displayed value differs from the cited exact-model manual, stop that check as unknown rather than borrow another model's instructions.

For Samsung, open its ordinary Settings navigation and enter only a clearly identified submenu. Arrows can change values, and Select can activate a setting: do not use them on a value/toggle. Read a value from its existing summary where possible. If it cannot be exposed without an uncertain edit, record unknown. Use a **short Return** to go back while observing each step; do not hold Return or press it repeatedly without looking. Close the menus and confirm the same ordinary desktop remains visible.

For Denon, use a remote already known to be in **MAIN** mode, then **SETUP** to open the menu. If its mode is different or unknown, leave the Denon menu fields unknown; do not change or restore the remote's mode in this look-only check. Read only clearly identified menu entries. **Left/Right changes values**: do not use it on a setting. Use **BACK** for the previous menu and **SETUP** to close. Do not select another input, zone state or power state. If the menu cannot be read without altering a setting, leave the field unknown.

| Existing setting / indication to record | Documented route or observation | Proposed criterion |
|---|---|---|
| Samsung Sleep Timer | Settings → System → Time → Sleep Timer | Off |
| Samsung Off Timer | Settings → System → Time → Off Timer | Every schedule actually shown is Off; do not assume a number of entries |
| Samsung Auto Power Off | Settings → System → Eco Solution → Auto Power Off | Off; a multi-hour timeout does not pass |
| Samsung Auto Protection Time | Settings → System → Expert Settings → Auto Protection Time | Off if clearly available and already selected; the consulted manual does not enumerate its choices, so missing/unclear options remain unresolved |
| Samsung Anynet+ (HDMI-CEC) | Settings → System → Expert Settings → Anynet+ (HDMI-CEC) | Off under the conservative CEC proposal below |
| Denon Auto Standby, MAIN ZONE | General → ECO → Auto Standby → MAIN ZONE | Off |
| Denon sleep timer | Existing front-panel **SLEEP** indicator | Clearly visible display and indicator unlit. A dim/off/unreadable panel is unknown, not proof of Off |
| Denon HDMI Control | Video → HDMI Setup → HDMI Control | Off under the conservative CEC proposal below |

**Do not press Denon's SLEEP button to check an unknown timer.** The manual describes that button starting/changing the timer; its remaining-time instruction assumes an already active timer. Do not brighten the panel, set/cancel a timer or wait for a standby event to infer its state.

**CEC criterion is an AI: Codex proposal, not a manufacturer requirement or an accepted owner decision.** HDMI-CEC lets connected devices affect one another. Requiring existing Anynet+ and HDMI Control both Off bounds this first procedure without surveying other connected devices or testing linked standby. If either is On, leave it unchanged and stop for a narrower reviewed assessment of the relevant controls; do not disable it just to pass. The Denon manual describes conditional Power Off Control and other linked behaviours, not the owner's current configuration. Its screen-saver page concerns specific receiver screens; no claim is made that it starts over every still HDMI desktop.

End by recording that all menus are closed, the original inputs and ordinary desktop remain visible and no value changed. If anything changed unexpectedly, stop and record the deviation; do not improvise a restoration sequence or continue to discovery. A proposed corrective setting change needs its own reviewed scope, original values, restoration procedure and explicit owner authority.

## Unresolved owner inputs and readiness decision

All entries below are deliberately unobserved. The companion private template contains individual fields; a manual default, merged document or AI agreement cannot fill them.

| Input | Current state | How it closes |
|---|---|---|
| Windows power and screen saver | UNKNOWN | Owner's current values satisfy the console guide's Never/None gate, or a specific inapplicability explanation is reviewed |
| Dynamic lock, sign-in wording, management and known lock mechanisms | UNKNOWN | Owner's look-only records meet the Windows table; any flagged item receives targeted assessment |
| Machine inactivity location and recent-change uncertainty | UNKNOWN | Complete zero/absence evidence under the bounded read, with no unresolved application-of-policy concern; no Home/default inference |
| Samsung timers, protection and Anynet+ | UNKNOWN | Each actual value meets the TV table or a narrower alternative is independently reviewed |
| Denon MAIN ZONE standby, sleep indication and HDMI Control | UNKNOWN | Each actual value/indication meets the receiver table or a narrower alternative is independently reviewed |
| Read-only navigation, unchanged inputs and desktop, menus closed | NOT OBSERVED | Owner records completed look-only checks and any deviation; settings remain unchanged |
| New preflight review | PENDING | Claude Code (Anthropic) or Antigravity (Google) independently reviews the new full head and criteria |
| Discovery authority | NONE | After review and assessed preparation, owner separately authorises dated parent steps 1–4 at the new reviewed revision |

Ready for a **later authorisation decision** means all applicable rows are supported, no flagged unknown remains, the private record is assessed, and the separate package's identity/console preparation gates are also complete. It does not mean discovery has run or that its session-only isolation/driver/environment checks may be skipped. Owner look-only checks need no new physical authority; connecting/changing/sending/measuring and the one discovery launch still do.

If a row fails or is unknown, record **NOT READY** and identify that specific gap. Seek only the evidence or narrower amendment needed for it. Do not silently weaken a criterion, change settings, add a keep-awake utility or run a trial. The listed checks reduce identified risks; they cannot guarantee absence of every possible lock, overlay, standby event or failure. During a later outstanding attempt, visibility loss still follows the package's unchanged abnormal branch: no wake/unlock input, cancellation or retry, and separate recovery assessment. The owner's unconditional right to end PC activity remains.

## Sources and applicability limits

Primary sources below were consulted read-only by Codex (OpenAI) on **28 October 2026**. S-064/S-065 and C-110/C-111 distinguish source facts from this untested proposed procedure (C-112). No actual settings, behaviour or safe stopping result was established.

- **Microsoft (S-064):** [Sign-in options in Windows](https://support.microsoft.com/en-us/accounts-billing/security/sign-in-options-in-windows) covers Dynamic lock and varying options. [Surface sign-in guidance](https://support.microsoft.com/en-us/surface/setup/sign-in-to-and-out-of-your-surface) documents Windows 10's Require sign-in wording in a Surface context; actual controls on this PC must be recorded. [MDM enrolment](https://learn.microsoft.com/en-us/windows/client-management/mdm-enrollment-of-windows-devices) prevents treating Home as proof of no management; [LockWorkStation](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-lockworkstation) shows that an application can request a lock. No API call, enrolment, pairing or inventory is proposed.
- **Microsoft policy/read semantics (S-064):** [Machine inactivity limit](https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/security-policy-settings/interactive-logon-machine-inactivity-limit), [Policy CSP edition scope](https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-localpoliciessecurityoptions#interactivelogon-machineinactivitylimit), [Server/RDS registry mapping](https://learn.microsoft.com/en-us/troubleshoot/windows-server/remote/troubleshoot-unexpected-rds-session-locks-or-disconnections) (12 February 2026), and [reg query](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/reg-query) (3 February 2023). The policy page requires restart after a local change; the RDS article discusses immediate application/reconnection in its server context. Neither proves the running Home session's effective configuration. This proposal makes no change and escalates recent/pending-change uncertainty for assessment.
- **Samsung (S-065, extending S-025):** [exact-model UK support](https://www.samsung.com/uk/support/model/UE49KS7000UXXU/) and [ENG-JZDVBEUK-1.1.3 e-Manual](https://org.downloadcenter.samsung.com/downloadfile/ContentsFile.aspx?CDSite=UNI_UK&OriginYN=N&ModelType=N&ModelName=UE49KS7000U&CttFileID=6648666&CDCttType=UM&VPath=UM%2F201612%2F20161209100212986%2FENG-JZDVBEUK-1.1.3.pdf): printed pp. 20, 60–62 (PDF pp. 25, 65–67), navigation, timers/protection and Anynet+. Retrieved PDF SHA-256 `816e1c6f563aac973b676f68f73e623dead66163141c5a74f53357150422a3bc`. S-032 reports this e-manual version; no current firmware/menu match is inferred. The manual does not enumerate every timer choice or a guaranteed read-only sequence; no borrowed “No Signal Power Off” setting is added.
- **Denon (S-065, extending S-030):** exact **AVC-X3800H EU/EN online manual**, revision unstated: [Menu operations](https://manuals.denon.com/AVCX3800H/EU/EN/GFNFSYwahcrdvi.php), [Auto Standby](https://manuals.denon.com/AVCX3800H/EU/EN/HJWMSYqdgglnxg.php), [Sleep timer](https://manuals.denon.com/AVCX3800H/EU/EN/GFNFSYlqgglmjj.php), [Display/indicators](https://manuals.denon.com/AVCX3800H/EU/EN/GFNFSYdqzxliff.php), [HDMI Setup](https://manuals.denon.com/AVCX3800H/EU/EN/GFNFSYkabkahie.php) and [Screen Saver](https://manuals.denon.com/AVCX3800H/EU/EN/DRDZSYwqejabmr.php). Defaults/options are documentation, not current owner settings.

No code, dependencies, test counts, source hashes, discovery command or stopping policy changes. The approved centred **960×540 patch at (1440, 810) on 3840×2160 (6.25%)** remains unchanged and unused. Merging this amendment authorises no physical test.
