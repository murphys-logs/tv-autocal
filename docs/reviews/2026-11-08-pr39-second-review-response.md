# PR #39 — assessment of reviews on the second head

**The earlier byte-identity and wrapped-reading findings are addressed as documented; this round corrects provenance, visibility and fairness.** The code still has the meter error-input gap. The shared hold prevents its planned wrapped use; it is not an implementation fix. No equipment operation or merge occurred.

Codex (OpenAI), 8 November 2026. [Claude Code review 5819081577](https://github.com/murphys-logs/tv-autocal/pull/39#pullrequestreview-5819081577) recommends **change first**, and [Antigravity review 5818988506](https://github.com/murphys-logs/tv-autocal/pull/39#pullrequestreview-5818988506) recommends **merge**. Both review `52ab35586887e399a1653534f1409f26c6960035`, with base `bcaf3d38ef03dca3b1607e0cb36c09ee3ea8f2b2`. Both complete bodies, metadata and comment collections were read; no inline review comments were returned. This response is S-098; the previous round remains in the [first response](2026-11-08-pr39-review-response.md). The next full SHA and both refreshed handoffs are in [PR #39](https://github.com/murphys-logs/tv-autocal/pull/39), avoiding a self-referential commit.

Both second-head reviews were actually received. They do not cover later changes. Claude still discloses structural/targeted readings of some tests/procedures and less than full reading of S-002/S-012/S-024; Antigravity supplies no complete coverage map and makes the additional errors below. Neither gap is erased by a recommendation or by same-vendor checking. Both vendors must review the next head and account for the full original remit; a single-vendor delta review would not satisfy S-097. Their reported private test runs remain attributed, not authenticated by this author.

## New Claude findings

Assessment confidence is confidence in the evidence below, not equipment capability. Source/software facts are N/A as equipment tests; physical applicability remains **Not tested**.

| Finding | Assessment, evidence and impact | Correction / remaining validation |
|---|---|---|
| N1 — authority attribution | **Agree on missing traceable provenance; P3, high.** D-016 already places claim analysis in claim-notes. The actual owner-issued audit message in this conversation also explicitly specifies that location in section 6. It matches the Codex-drafted prompt body on PR #38, whereas that PR's earlier owner request merely commissioned the prompt. The reviewer appropriately distinguished repository evidence from uncertainty about what the owner issued. | Archive the actual issued instruction and both follow-ups verbatim as [S-097](../briefs/2026-11-08-audit-execution-and-review-requests.md), explicitly **Owner-issued, wording drafted by Codex/OpenAI**. Cite D-016/S-097 in the ledger, audit and D2 response. No claim that an unmerged AI draft itself grants authority; no extra owner confirmation needed for the messages already issued. |
| N2 — hold visibility | **Agree; P3, high.** The binding hold was present in the requested procedure locations, but absent from the status and authorisation summaries. This was a visibility defect, not absence of a hold. | Link C-136's single shared hold from both plan banners, both authorisation sections, README and both ledger test rows. Preserve scope: T-003 steps 5–11 and T-005 Part M. Direct discovery remains subject to its existing independent gates. |
| N3 — luminance attribution | **Agree; P3, high after independent recomputation.** The previous response silently assumed that Claude's numbers were intended as V=k/255. Claude now specifies a rounded 16–235 encode/decode mapping; its earlier rounded numbers match that model. The omission was an unstated mapping, not demonstrated arithmetic error. Neither model is measured. | Withdraw “require correction” as a judgement of Claude's arithmetic, state both mappings and values below, and update X-019/claim analysis. The other-unit .38 cd/m² benchmark still cannot establish this meter's floor or likelihood of failure. |
| N4 — PR #38 merge order | **Partly supported; high.** Combining PR #38 at `75cec90159711401ada5ff52a479a366ccc73c61` with the reviewed head produces three content conflicts. This does not show that either conflicts with main or that PR #39 depends on PR #38. The proposed dependency rests on citing S-089/S-090 as operative authority, which S-097 avoids. | Record the overlap for the owner's eventual integration decision. Do not merge, rebase or rewrite either branch. This PR is self-contained on the pinned main; its reserved-ID/history references do not import the draft as authority. Both vendors still need to review changed heads, not merely one delta reviewer. |
| N5 — private local URL in a review | **Agree; high, outside this PR's tracked files.** Antigravity's second review includes a local profile URL containing identifying information. Its value is deliberately not reproduced here. | Record redacted evidence under existing privacy questions and explicitly prohibit local-profile URLs in both handoffs. The review author/account owner should remove that URL from the review body; Codex does not alter another reviewer's authored text or change history/settings. No claim that this removes earlier copies or public commit metadata. |
| N6 — optical over-range retry path | **Supported with narrower scope; high for source, unresolved likelihood.** The `spyd2` driver rejects computed `maxfreq > 500000.0` and maps that error to misread. The dispatch covers Spyder1–5; SpyderX/X2 use other drivers, so “every Spyder generation” is too broad. No evidence ranks this as the “most plausible” persistent trigger on the owner's TV. | Add the source path to A-007/C-056 analysis, retaining unknown luminance threshold, persistence and likelihood. This strengthens the possible-trigger evidence, not a prediction that the planned patches reach it. Exact loci below. |

The inert merge check was `git merge-tree --write-tree --messages 75cec90159711401ada5ff52a479a366ccc73c61 52ab35586887e399a1653534f1409f26c6960035`. It reported content conflicts only in `LEDGER.md`, `docs/README.md` and `docs/reviews/README.md`; merge base was the pinned main. It created synthetic Git objects, without changing a branch, index or working tree. It is evidence of overlap, not a requested merge order. PR #38's eventual status wording will need reconciliation with actual review receipts if the owner later integrates it.

## Numerical assumptions and optional proposals

For both models below, gamma=2.4, Lw=150 cd/m² and Lb=.05 cd/m² are hypothetical. Model F uses V=k/255. Model L encodes `h=floor(16+219*k/255+.5)` and decodes V=(h−16)/219. The two models are alternatives, not successive transforms. “Exact” below refers to evaluating the model; the displayed values are rounded.

| App code k | h, model L | L, model F (cd/m²) | L, model L (cd/m²) |
|---|---|---|---|
| 51 | 60 | 4.337624852 | 4.377865928 |
| 26 | 38 | 1.203544862 | 1.172491208 |
| 13 | 27 | .401400072 | .393204220 |
| 5 | 20 | .139073830 | .131271538 |
| 0 | 16 | .050000000 | .050000000 |

Reproduction uses the standard library and no project code:

```python
from math import floor, sqrt
g = 2.4
d = 150**(1/g) - .05**(1/g)
def luminance(v):
    return d**g * max(v + .05**(1/g)/d, 0)**g
for k in (51, 26, 13, 5, 0):
    h = floor(16 + 219*k/255 + .5)
    print(k, h, luminance(k/255), luminance((h-16)/219))
z = 3/sqrt(13)
p = (1 - 1.5*z + .5*z**3)/2
print(p, 1-(1-p)**9)  # one-sided t(4), hypothetical independent family
```

| Proposal / assertion | Assessment and disposition |
|---|---|
| O1 — rounded XYZ/Yxy intervals | A useful proposed consistency rule, subject to floating formatting, six-decimal rounding and the small-sum branch. ±5e-7 is the ideal nearest-rounding half-step, not a measurement uncertainty. Apply it to the reviewed six-decimal format, not indiscriminately to the parser’s broader synthetic/scientific notation grammar. Test negative/zero/near-threshold values and denominator intervals containing zero before choosing a contract. Changes to pinned fixtures/parser belong in a focused software PR. |
| O3 — 2% per pair and about 17% across nine | The one-sided t(4) tail at 3 is about .019971; the hypothetical independent nine-test family probability is about .16603. Adjacent differences share means, so independence is not established for the actual plan. Its max-with-2q threshold can also reduce the simplified event rate. Neither value is a validated family error rate for T-005. It is an at-least-one false-step illustration, not the probability that the entire clipping screen passes; the plan requires each eligible increase. |
| O3 — print-precision floor | `%f` gives a 1e-6 printed increment in the reviewed formatting. That is not sensor resolution. “Negligible at any TV luminance” is too broad near zero or for tiny differences; retain it as a rounding screen without pretending it models optical uncertainty. An engineering minimum effect may reflect measured noise, drift and purpose, not necessarily instrument resolution alone. Thresholds remain unchanged and unaccepted. |
| O4 — strip all inherited ARGYLL_* settings | Reasonable policy candidate, not an adopted fix. Define case handling, allowlist, required reintroduced settings and interaction with exclusions; validate that removing an exclusion does not expand probes without the separately required physical isolation. Other environment/OS/configuration inputs still exist, so this cannot remove every unknown inherited setting. |
| O7 — pySerial hash pinning | Optional supply-chain improvement, already within the audit's dependency limitation. Hashes identify artifacts; they do not prove publisher trust, absence of vulnerabilities or driver compatibility. No install or dependency edit is made in this findings PR; a focused reviewed packaging change can choose accepted distributions and pip hash-checking behavior. Primary checks are recorded below. |

## Antigravity's second review and other material assertions

| Assertion / area | Assessment |
|---|---|
| First-review corrections and no disagreements | Its explicit withdrawals of wrong file names, first diff paths, numbers and owner-meter/global-CCSS claims are accepted and X-019 is updated. Its statement of agreement records its position, not evidence of correctness. Hypothetical factory profiling/transfer standards are not an identified viable route within this project's constraints. |
| Exact head, diff, manifest and application identity | Match the author's independently verified head, 19-file +1667/−54 diff and unchanged source/34-entry manifest. Precise reported private execution durations remain attributed. |
| New `--permit-file` flag | Incorrect: `cli.py:31–33` defines `--permit`, `--confirm`, `--log`. Its corrected module paths are right. The begin/inspect/exit/wait/read/set/reply labels do occur in `CycleEvent.action`; they should not be misrepresented as a list of public controller methods. |
| `_getch` described as stdin reading | Incorrect: the interactive branch reads console input. Noninteractive handling depends on the handle type and can also choose `_getch`. EOF discussion belongs to the applicable pipe/file branch, not an assumed console result. |
| Hold “prevents any wrapped meter execution”; discovery “unhindered” | Narrow to a procedural prohibition: the code is unchanged and has no new executable enforcement. The hold adds no direct-discovery restriction, but all its pre-existing gates remain. Neither review supplies physical permission. |
| B1/B2 and O1–O6 endorsements | Correct within the source/grammar/procedure boundaries above and in the first response. O6 means the consulted documents lack applicable endpoint limits; it does not establish that future manufacturer documentation could never close the gap. |
| Arithmetic and source verification | The corrected BT.1886, matrix, code-state and t-tail numbers are supported. Re-executing the author's snippet reproduces it; that alone is not an independent derivation. “All claims ... verifiable” is too broad for unavailable originals and hardware questions. No new Portrait-page corroboration is documented by this review. |
| Recommendation and whole-project coverage | MERGE is its recommendation, not the owner's decision. Repeated incorrect details and no complete coverage inventory leave the requested exhaustive review unsubstantiated. No inference is made about undisclosed session conduct. Current-head re-review and explicit remaining coverage are still required. |
| Claude's near-black and readback summary | “Near-black is likely below what this meter can verify” is not established by borrowing another unit's floor. No implemented readback and an ACK lacking an identifier do not prove all exact-TV readback impossible. The audit retains these evidence limits. |
| Claude's CCSS access summary | The audit directly opened the database homepage (URL-122); candidate-query access and validation were limited. “Inaccessible in both” should distinguish homepage from unsuccessful query paths. Neither an inaccessible query nor an index proves that a suitable correction does not exist. |
| Claude C1–C4 and first-round dispositions | Accept the narrower manifest/discovery scope, nontermination qualification, corrected read() end line and now-explicit signal mapping. D2 relocation is withdrawn; N1 addresses provenance. Both first-round blockers are resolved as byte restoration and an operational hold, not runtime repairs. New qualifications to pipe and generation claims are retained above/below. |

## Source checks and inert Windows observation

The official [ArgyllCMS V3.5.0 source archive](https://www.argyllcms.com/Argyll_V3.5.0_src.zip), release dated 4 February 2026, was rehashed and relevant members reread as text on 8 November: SHA-256 `f8576ce5589fd15620abb73ff049ea31f55ddbd1bba6d1ffa87452658e7bc85f`. The table assesses every numbered B2 follow-up note; member paths refer to that exact archive. No source compilation or Argyll launch occurred.

| Claude B2 note | Exact source and assessment |
|---|---|
| 1 — presence semantics | `numlib/numsup.c:225`: any non-NULL getenv result, including the string `"0"`, selects noninteractive handling. Explicit child policy is a reasonable proposal, not a change already made. |
| 2 — pipe consumption/EOF | `spectro/conv.c:204–236`: multiple ReadFile calls can accumulate up to ten bytes; LF/CR/Ctrl-C or a full buffer ends collection and only the first byte is returned. Further characters already read into that buffer are discarded. With wait=1, persistent zero-byte EOF before completion causes unbounded 100-ms sleep/retry; an empty blocking pipe can instead block inside ReadFile. The first response's “not established bounded” wording understated this conditional source result. A complete q-newline can answer the first prompt; a lone q or later prompt after the pipe is exhausted is not equivalent. |
| 3 — q and callbacks | For the selected USB Spyder5/-O path, the source supports q surviving to the first eligible error prompt **if a future implementation establishes noninteractive PIPE input and supplies a complete q-newline**. `conv.c:275–276` leaves it unread; `spotread.c:423–428,1887–1888` replaces the default callback before `spyd2.c:3077–3101` invokes it. The abort/misread/comms prompts at `spotread.c:2304,2333,2345` accept q; cleanup can return zero (`3176–3201`), so failure-text rejection remains necessary. Default callbacks/serial identification (`instappsup.c:53–80,103–115`; `inst.c:634–646`) and nonselected lamp/X-Y options must not be generalized into this path. Low-level USB retries (`spyd2.c:120,695–830`) and adaptive acquisition (`1727–1784`) precede the prompt; q does not bound those calls or cleanup. |
| 4 — nonprompting loops | `spotread.c:2313–2326` contains generic needs-calibration/wrong-config retries. Full driver text and `spyd2.c:3442–3487` reveal no wrong-config return for this driver. Its needs-calibration return at `3338` is in explicit refresh-rate querying, not the ordinary -Y n sample path. Immediate calibration errors return without prompting (`instappsup.c:222–223,403–404`). Retain generic cases without claiming they occur on this equipment. |
| 5 — pipe mode/rights | `numsup.c:241–245` ignores the result of requesting NOWAIT. A failed change can leave a previously blocking pipe blocking; failure alone does not prove its prior mode. Microsoft documents CreatePipe handles as accepted, and GENERIC_READ plus FILE_WRITE_ATTRIBUTES for a read-only handle. Actual Python-created pipe rights/mode and the future implementation remain untested. |
| 6 — current DEVNULL/CHAR path | The Python-only observation below returned CHAR. `numsup.c:234–245` and `conv.c:182–201` would select `_getch` for noninteractive CHAR; that branch accumulates up to ten characters until LF/CR/Ctrl-C, while interactive `252–255` returns one character. Thus inherited mode affects input consumption too, not only buffering. This source inference does not establish what actual Argyll/MSVCRT does with the redirected handle. |
| 7 — follow-up scope | Any meter.py change needs reviewed source fingerprints, meaningful fakes and applicable native validation. Pure software-only Windows API queries are within this task; executing Argyll or equipment-bound checks still requires the existing authority. The hold remains; no stdin fix or forced recovery is adopted. |

N6's additional path is `spectro/spyd2.c:991–996` (computed maxfreq >500000.0), ordinary sample propagation `1733–1735,3131–3132`, error mapping `3482–3484`, then `spectro/spotread.c:2329–2338`. Spyder3/4/5 decoding includes a factor of 8.125 (`spyd2.c:967–976`); this is not a cd/m² specification. `spectro/inst.c:705–719` dispatches Spyder1–5 here and later X/X2 models elsewhere. Non-refresh selection (`spyd2.c:3158–3159`) skips ordinary automatic refresh detection (`3113–3114`); other explicit refresh paths and warned failures are separate. Source establishes a possible over-range trigger, not a universal saturation threshold or its likelihood.

Primary documents/artifacts consulted 8 November 2026:

- Microsoft Learn, [GetFileType](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-getfiletype), updated 2021-10-13, Return value: CHAR=2, PIPE=3, UNKNOWN/error distinction; [GetStdHandle](https://learn.microsoft.com/en-us/windows/console/getstdhandle), updated 2021-12-30, Parameters/Return value/Remarks: redirected handles and unsigned STD_INPUT_HANDLE. The alternate `/windows/win32/api/processenv/nf-processenv-getstdhandle` URL was inaccessible in the tool; the canonical console page was opened directly.
- Microsoft Learn, [SetNamedPipeHandleState](https://learn.microsoft.com/en-us/windows/win32/api/namedpipeapi/nf-namedpipeapi-setnamedpipehandlestate), updated 2023-02-02, hNamedPipe/mode/return sections, and [CreatePipe](https://learn.microsoft.com/en-us/windows/win32/api/namedpipeapi/nf-namedpipeapi-createpipe), updated 2021-10-13, handle roles: API contracts only, not observed access masks or Argyll behavior.
- PyPI, [pyserial 3.5 versioned release metadata](https://pypi.org/pypi/pyserial/3.5/json), `urls` artifact metadata uploaded 2020-11-23. Fresh inert downloads match wheel SHA-256 `c4451db6ba391ca6ca299fb3ec7bae67a5c55dde170964c7a14ceefec02f2cf0` and sdist `3c77e014170dfffbd816e6ffc205e9842efb10be9f58ec16d3e8675b4925cddb`. Both `serial/serialwin32.py` members equal the [pinned upstream file](https://github.com/pyserial/pyserial/blob/0e7634747568547b8a7f9fd0c48ed74f16af4b23/serial/serialwin32.py): 20,284 bytes, SHA-256 `17681ea9a650120c71db1aae9b8881301a40d38c47b34bb0da050e3f5bfbbe00`. No archive code was installed/imported. These artifact checks support the corrected v3.5 loci, not the safety of an installation.
- ITU-R [BT.1886-0, March 2011](https://www.itu.int/dms_pubrec/itu-r/rec/bt/R-REC-BT.1886-0-201103-I!!PDF-E.pdf), Annex 1: normalized V, luminance endpoints and gamma 2.4, reopened for the independent endpoint derivation. The [DisplayCAL correction index](https://colorimetercorrections.displaycal.net/) was reopened successfully; live undated homepage access does not reproduce the inaccessible historical query or validate a candidate. The [CurtPalme/ChromaPure benchmark](https://www.curtpalme.com/ChromaPure_SpyderX.shtm), live undated seller page, was reread for “Performance compared to previous Spyder models” and low-light table: secondary other-unit luminance-repeatability evidence, not an owner-unit accuracy floor.

**Actual software-only observation:** on Windows 10 build 19045 AMD64/Python 3.15.0, the inspected disposable Python child below returned a valid stdin handle, FILE_TYPE_CHAR (2), error 0 and exit 0. The parent used DEVNULL stdin, captured outputs, CREATE_NEW_PROCESS_GROUP|CREATE_NO_WINDOW, no shell and a five-second limit. No Argyll, repository runtime, CRT input, GUI, serial or network-device call ran. This narrows the handle-type uncertainty only; it does not prove native Argyll blocking/retry/cleanup behavior or lift C-136. The timeout would terminate only this inert Python child, never an instrument process.

For reproduction, save this inspected standard-library script locally and run `py -3.15 -B devnull_type_probe.py --execute-software-only-probe` on Windows. No local paths or handle values are printed. This is a focused observation, not a new regression suite or a hardware test:

```python
import json
import subprocess
import sys

CHILD = r'''
import ctypes
from ctypes import wintypes
import json
import sys
k32 = ctypes.WinDLL("kernel32", use_last_error=True)
k32.GetStdHandle.argtypes = [wintypes.DWORD]
k32.GetStdHandle.restype = wintypes.HANDLE
k32.GetFileType.argtypes = [wintypes.HANDLE]
k32.GetFileType.restype = wintypes.DWORD
ctypes.set_last_error(0)
handle = k32.GetStdHandle(wintypes.DWORD(4294967286))
invalid = handle is None or handle == ctypes.c_void_p(-1).value
if invalid:
    print(json.dumps({"python_version": sys.version.split()[0],
                      "stdin_handle_valid": False,
                      "get_std_handle_error": ctypes.get_last_error()}))
    raise SystemExit(2)
ctypes.set_last_error(0)
kind = k32.GetFileType(handle)
error = ctypes.get_last_error() if kind == 0 else 0
print(json.dumps({"python_version": sys.version.split()[0],
                  "stdin_handle_valid": True, "file_type": kind,
                  "file_type_name": {0: "UNKNOWN", 1: "DISK", 2: "CHAR", 3: "PIPE"}.get(kind, "OTHER"),
                  "get_file_type_error": error}))
raise SystemExit(0 if kind != 0 or error == 0 else 3)
'''


def main():
    if sys.argv[1:] != ["--execute-software-only-probe"]:
        print("UNRUN proposal: requires explicit --execute-software-only-probe")
        return 0
    if sys.platform != "win32":
        raise SystemExit("Windows only; no child launched")
    try:
        result = subprocess.run(
            [sys.executable, "-I", "-S", "-B", "-c", CHILD],
            shell=False, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, close_fds=True,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.CREATE_NO_WINDOW,
            timeout=5, check=False,
        )
    except subprocess.TimeoutExpired:
        # subprocess.run kills and waits for only this inert Python child.
        print(json.dumps({"result": "inert Python probe timeout", "timeout_seconds": 5}))
        return 4
    if result.returncode or result.stderr:
        # Do not dump paths or unrelated interpreter diagnostics into public evidence.
        print(json.dumps({"result": "probe failed", "exit_code": result.returncode,
                          "stderr_bytes": len(result.stderr)}))
        return 5
    report = json.loads(result.stdout)
    report["equipment_operated"] = False
    report["scope"] = "this Python/Windows child launch only; no Argyll or CRT-input test"
    print(json.dumps(report, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## Scope and validation limits

This revision changes documentation, links and evidence records only. Baseline application/test bytes and the existing audit fixture remain untouched. Source inspection, arithmetic, private read-only QA and any explicitly described inert process probe do not operate equipment. All 34 source-manifest entries remain applicable; merged briefs/research remain unchanged. Public review privacy evidence is redacted, not copied into the repository.

No broad suite rerun is warranted by documentation-only changes; the original 287/287 Windows baseline and both reviewers' separately attributed runs retain their original scope. The PR description records exact checks and final head. No test of Argyll/native input, meter saturation, actual digital mapping, driver recovery or TV behaviour is inferred. The known L-4 defect and A-007 implementation gap remain for focused reviewed follow-up; every physical plan stays NOT AUTHORISED.
