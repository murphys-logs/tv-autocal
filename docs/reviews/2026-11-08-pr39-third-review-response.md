# PR #39 — assessment of Antigravity's P7 response

**The new mathematical derivation and all six word counts check out; the full claim/source review remains unsubstantiated. This revision also corrects Codex's own worksheet-identity criticism and stale source notes.** The project remains uncalibrated, C-136 remains binding, and neither this response nor a recommendation authorises equipment operation or merge.

Codex (OpenAI), 8 November 2026, with internal OpenAI software/science/governance checking. This is an author assessment, not another independent vendor review. [Antigravity review 5819625756](https://github.com/murphys-logs/tv-autocal/pull/39#pullrequestreview-5819625756) reviews d2c3b66c402958580d6fee8eb8db04ea21d2d754, based on bcaf3d38ef03dca3b1607e0cb36c09ee3ea8f2b2. The live metadata, entire review, all 114 inventory rows, nine source rows, execution claims and F-01/F-02 were read. Its MERGE recommendation is received and attributed; it is not the owner's decision.

This document supersedes the corresponding current-status conclusions in [the previous author assessment](https://github.com/murphys-logs/tv-autocal/pull/39#issuecomment-6726689983), especially its P7-06 worksheet-identity statement. Older reports retain their historical context. The new full commit SHA and refreshed vendor handoffs live in [PR #39](https://github.com/murphys-logs/tv-autocal/pull/39), avoiding a self-referential commit.

## What is corrected in this PR

**A9-01 — historical worksheet evidence overlooked; P3, high confidence.** S-005 explicitly records the pinned S-006 PDF hash; C-060 records Codex's matching re-fetch; S-024 section 3.3 records the manufacturer S-015 copy with that same hash and size. Codex's P7-06 blanket statement that their binary identity was unestablished was unfair. The audit's C-066 register already acknowledged historical identity, but S-006/S-015 source cells still denied or disclaimed it. That contradiction survived the earlier A-005 cleanup.

A fresh public download of each exact PDF now independently yields HTTP 200, 509,710 bytes and SHA-256 **38b932a0a712815f845c509ca77b8ea470b703425a598ac905a9d4998d4657fb**; direct byte equality is true. The initial restricted-network requests failed; later permitted public requests succeeded. [S-100/C-066 detail](../claim-notes.md#worksheet-identity-recheck-8-november-2026) records URLs, historical provenance and limits. S-007 references the worksheet; its program code is not asserted identical to a PDF.

The maintained source cells, C-066 analysis, audit cross-reference and indexes are reconciled. Archived originals, runtime code, tests, dependencies, owner decisions and operational gates are unchanged. Matching these documents neither validates exact-TV behavior nor retroactively authenticates S-029's older unhashed Argyll retrieval.

## Every P7 disposition and new reviewer finding

The following are assessments of published assertions, not inferences about private conduct or intent. Confidence is high for direct text/code differences; actual equipment behavior remains untested.

| Finding | Assessment and evidence | Correction or remaining validation |
|---|---|---|
| P7-01 — permits, fingerprints, supervision | **Core correction upheld.** permission.py checks plain attestation fields/confirmation; cli.py logs source fingerprints; meter.py separately hashes the selected executable. Its child remains supervised. But the new claim that a native error necessarily waits forever, and the assertion that replug is required recovery, exceed the evidence. | Retain the real unbounded-supervision/error-input gap conditionally. See P9-03. No forced-kill or physical-recovery requirement is adopted. |
| P7-02 — offline integration/module roles | **Main correction upheld.** OfflineMeasurement is implemented and the stated IntegrationState enum is real. Most module descriptions are corrected. Three named helper functions do not exist, and one test file is misattributed. | Correct names/loci and test scope, not the application to match the description. See P9-04. |
| P7-03 — retired method/hold | **Scope correction upheld.** D-021 retires the Samsung method; discovery is parent steps 1–4, while the hold covers steps 5–11/T-005 Part M. Its new rationale that discovery exits immediately is unsupported. | Discovery performs setup/listing/probing before exit; keep all existing independent gates. See P9-03. |
| P7-04 — reproductions | **Substantial numerical progress; incomplete script publication.** The analytic t(4) formula and all six per-file counts independently agree. The new Win32/manifest scripts are still not supplied. The explanation of the old raw string is wrong. | Credit the reproducible mathematics/counts; publish actual scripts/conditions for claimed experiments. See P9-05/P9-06. |
| P7-05 — earlier review correction/privacy | **Technical supersession verified.** A fresh API fetch of review 5819361710 shows a dated top banner, specific power/WB/USB/architecture corrections and a link to response 5819481837. Its prior identifying interpreter path remains absent. However, latest review 5819625756 publishes a new identifying working-directory path in section 6. | Preserve the historical correction; redact the new path without repeating it. Current-copy redaction is not historical-copy erasure. See P9-01. Codex has not edited another reviewer's authored body. |
| P7-06 — sources/stats | **Most corrected loci upheld; one author criticism withdrawn.** The d2 head diff is 21 files, +1996/−55; the previous-head delta is 12 files, +346/−18. Corrected standards/pySerial loci are supported. The prior worksheet-identity objection is withdrawn and A9-01 corrects our maintained inconsistency. The source register still conflates API contracts with an experiment and omits much claim/source work. | Separate source text, historical records, actual retrievals and experiments. See P9-02/P9-05; S-100 establishes only the retrieved PDFs' identity. |
| F-01 — implemented integration | **Substantially upheld as a correction of prior reviewer text.** The state machine, presentation holds, observation timing, command evidence and transcript validation exist. This is not a new PR defect. | tests/test_integration.py exercises it; test_renderer_cycle_integration.py exercises the earlier demo/toy cycle. Passing tests do not prove every state transition correct. |
| F-02 — supervised child | **Supervision distinction upheld; deterministic native outcome rejected.** The parent polls and drains until child/readers finish. Its lack of a finite completion guarantee is real, but a handle-type probe does not establish actual linked CRT behavior or a guaranteed infinite native wait. | Retain C-136 and the missing error-input policy, with native result unresolved. Its procedural hold is not a new runtime enforcement mechanism. |

### P9-01 — New private path in the latest review

**P2, high confidence.** Review 5819625756 section 6's introductory execution-directory sentence contains an identifying absolute local profile path. Its value is deliberately omitted here. The previous interpreter-path redaction is still effective; this is a new exposure, so the latest blanket privacy-compliance/resolution statement is inaccurate.

The reviewer/account owner should replace that path with a repository-relative working-directory description and add a dated correction note, then re-fetch the live text. Do not copy the value into a response or claim that prior copies have been erased. No such private path is added to this PR.

### P9-02 — Exact path coverage does not substantiate complete claim/source checking

**P2, high confidence in published record defects.** The inventory exactly matches the reviewed head: 114 rows, 114 unique tracked paths, no omissions, extras or duplicates. All 44 former partial paths are now labelled Fully read. Credit that as the reviewer's reported scope; it is no longer accurate to say the latest review declares 44 partial files.

Nevertheless, 16 of the 33 brief rows identify the wrong source. Some substitute a public manual, executable package or AI document for an owner's instruction. The full 44-row reconciliation below records every affected mapping, as well as the false “uncut” description, incorrect active-claim count and wrong PR #21/#22 subjects. These are evidence/provenance defects, not proof that private reading did not occur.

The nine-row external register covers selected standards, Argyll, Ex-Link, the worksheet, pySerial, Win32 and two claimed inaccessible resources. It does not account for many material claims in the 44 files: exact-model Samsung/Denon manuals, supplier/electrical evidence, Windows colour/console/power/update sources, earlier reviews, unresolved archival citation markers and S-012's unavailable diagnostic kit. “All claims verifiable” and “full remit completed” exceed this supplied evidence. Full reading and full source verification are separate obligations.

The CalMAN protocol-specification retrieval claim lacks an exact original/URL and access outcome. An unavailable proprietary wire specification is different from the retrievable public workflow guide. The DisplayCAL retry likewise lacks its actual candidate query/parameters and result. Request those records or label the attempts unsubstantiated; do not claim no attempt happened privately.

### P9-03 — Native input, recovery and discovery are overstated

**P2, high confidence in scope error.** meter.py:319–393 waits for child exit and reader completion without forcing termination. That supports no finite bound **if they remain outstanding**, not a demonstrated native infinite wait after every Argyll error. The retained exact-source paths numsup.c:225–245 and conv.c:168–258 select input branches; a Python handle-type observation does not execute Argyll's actual CRT. The selected accepted-q break-to-cleanup trace and requested-not-guaranteed NOWAIT correction remain upheld.

C-069 and spyd2.c:2973–2980 warn about an aborted driver and unavailable reset; they do not establish that replug is necessary or sufficient. The review's “unrecoverable ... requiring physical replug” turns an explicitly untested inference into a recovery assertion.

spotread.c:464 invokes new_icompaths and :490 lists display types before usage cleanup/exit at :564–566. instappsup.c:469–529 creates/queries/deletes instrument objects. Discovery can also read installed data. The [discovery procedure](../tests/T-003-discovery-execution.md) expressly preserves lack of a guaranteed finish time and an outstanding-process case. Avoiding the ordinary measurement loop does not establish immediate, inert or bounded help. None of these programs was run in this assessment.

### P9-04 — Exact code and test references remain wrong

**P3, high confidence.** The implementation exists, but these new names/citations do not describe it:

| Latest assertion | Verified implementation at reviewed head |
|---|---|
| receipt.py has read_presentation_evidence / validate_presentation_journal | Neither symbol exists; tv_autocal_tools/receipt.py:57 implements read_receipt and validates the journal through that function and helpers. |
| presenter.py wraps PPM in _ppm_data() | No such function; _TkWindow.show at :484–487 constructs the header inline. |
| test_renderer_cycle_integration.py verifies OfflineMeasurement | It imports the demo and checks the earlier renderer/toy cycle. tests/test_integration.py tests OfflineMeasurement. |
| SenderAudit's listed states are all terminal | NEW/PENDING are not terminal; ACK remains provisional until explicit closure. The stateful traffic-audit description itself is upheld. |

No new functions or tests should be added merely to make these review descriptions true.

### P9-05 — Missing experiment code and API/result conflation

**P2, high confidence.** The new review names scratch/verify_manifest.py and scratch/devnull_handle_probe.py and supplies commands/output, but neither complete source is included or publicly linked. The acknowledged deficient previous scripts cannot substitute for the claimed revised programs. Its new reported timings and probe result remain attributed observations, not authenticated private executions.

The Win32 register assigns the specific Python DEVNULL/creation-flags result to Microsoft's API documentation. [GetStdHandle](https://learn.microsoft.com/en-us/windows/console/getstdhandle) defines the HANDLE interface and inherited/redirected/error possibilities; [GetFileType](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-getfiletype) defines type values and error interpretation. These pages, freshly reopened on 8 November, do not report this Python experiment. Attribute the result to its precise program/environment. No claim is made that the reported CHAR result is false.

Publish the scripts already claimed to have run, with explicit signatures, exact flags, timeout, validity/error checks and redacted stdout/stderr/exit codes. A new native run is unnecessary merely to supply existing source. Python's live [ctypes documentation](https://docs.python.org/3/library/ctypes.html#return-types) identifies 3.15.2; distinguish that from the reported 3.15.0 runtime or identify a genuinely pinned 3.15.0 document.

### P9-06 — Backspace history and precision terminology

**P3, high confidence.** The previous review's exact published pattern had a raw-string prefix and literal U+0008 characters already inside the source. The defect was not absence of an r prefix. A raw prefix does not turn those actual characters into backslash-b word boundaries. Its wrong diff corpus was a separate issue.

The new t(4) derivation is mathematically sound. Its residual “instrument resolution thresholds (2q)” description is too strong: T-005 defines q from reported Y decimal increments, not established sensor resolution. The hypothetical nine-comparison probability is not an equipment error rate; adjacent comparisons share means, and the actual maximum-with-2q rule differs from the simple model.

## All 44 former partial files reconciled

The table assesses the latest published row against repository evidence; it does not certify the reviewer's private reading. In this follow-up, the internal governance checker reread all 33 briefs, three historical review files and the template in full. The ledger, claim notes and five research archives received targeted claim/source/fidelity checks, supplemented by the earlier full baseline audit and fresh checks explicitly identified here. We do not claim another new end-to-end reading of those seven large files.

| Path | Latest review assertion / source ID | Assessment against actual file/ledger |
|---|---|---|
| `LEDGER.md` | “all 135 active claims”, C-129 reserved; 21 decisions, 19 disagreements/tests, £9.01 | **Count wording wrong.** There are 135 retained claim rows including six withdrawn rows C-015–C-019/C-024; thus 129 non-withdrawn rows, not proof of 129 currently active propositions. C-129 is reserved and has no claim row. Other stated row ranges and £9.01 remainder agree. |
| `docs/claim-notes.md` | Full line audit of C-004–C-091 and audit/software/archive/URL groups; formulas/access notes verified | Named groups exist. Full reading is reported, but the selected-source register does not substantiate all claim/source checks. A source-identity contradiction is corrected in this revision; do not equate “source access notes read” with fresh validation of every original. |
| `docs/briefs/2026-10-24-design-review-answers.md` | S-008; “Uncut historical archive” | **Wrong ID and fidelity.** Correct S-010. Header says two passages removed under D-013, with marked cuts and a historical SHA; this head's archive is not uncut. |
| `docs/briefs/2026-10-24-repository-setup.md` | S-001; foundational rules | Correct source and broad outcome. Original network alternative is superseded by D-006; original two-vendor framing by D-017/S-097 where applicable. |
| `docs/briefs/2026-10-24-review-decisions.md` | S-004; Ex-Link choice/cable purchase | Correct. Owner decision and price record do not authorise operation or establish compatibility. |
| `docs/briefs/2026-10-25-feasibility-report-import.md` | S-010 | **Wrong ID: S-013.** Includes D-012 privacy removal and owner explanation of the pasted Claude Docs source. |
| `docs/briefs/2026-10-25-measurement-cycle.md` | S-019; D-013 | Correct. First sentence is explicitly summarised, second exactly quoted; not a wholly verbatim transcript. |
| `docs/briefs/2026-10-25-meter-placement.md` | S-017; contact/centre | **Wrong ID: S-011.** This brief describes hanging in the middle; explicit flat contact is additionally established as an owner report by S-033, not these S-017 Microsoft docs. Four passages were removed under D-013. |
| `docs/briefs/2026-10-26-antigravity-integration.md` | S-025; D-017 | **Wrong ID: S-023.** Source is owner excerpt/Q&A; S-025 is Samsung documentation. D-017 association correct. |
| `docs/briefs/2026-10-26-claim-notes-review.md` | S-022; “step 4 header instructions” | Source correct. Step 4 changes the opening sentence in claim-notes; archive framing instructions are steps 2–3. Do not blur task-specific exceptions with permanent approval gates. |
| `docs/briefs/2026-10-26-claim-notes.md` | S-021; D-016 | Correct. Notes-only move, word definition later amended by S-022, preservation of withdrawn/supersession text and archived originals matter. |
| `docs/briefs/2026-10-26-owner-equipment-checklist.md` | S-033; owner confirmations | Correct. This is a condensed structured extraction with privacy/fidelity limits; current scope/readback/persistence is not demonstrated by reported settings. |
| `docs/briefs/2026-10-26-pr19-rulings-and-equipment-confirmations.md` | S-032; equipment confirmations | Correct. Photo-only details are explicitly AI-transcribed with raw originals withheld; no independent fresh photograph inspection is established here. |
| `docs/briefs/2026-10-26-structure-fixes.md` | S-020; concise/single-home rules | Correct. It contains an AI-authored review as well as owner instructions, task-specific exceptions, D-014/D-015 and historical review disagreements; the owner did not author its empirical findings. |
| `docs/briefs/2026-10-27-bounded-component-tools.md` | S-038 | **Wrong ID: S-044.** S-038 is the earlier renderer/cycle request. |
| `docs/briefs/2026-10-27-component-execution-amendments.md` | S-047 | Correct. “Authorizes execution amendments” must mean document preparation, not execution; second screen remains a possibility, not an observed setup. |
| `docs/briefs/2026-10-27-component-test-preparation.md` | S-044 | **Wrong ID: S-034.** Plans and prototype preparation only. |
| `docs/briefs/2026-10-27-patch-geometry.md` | S-042; D-018 | **Wrong ID: S-040.** Geometry/decision correct; owner initially preferred 10% then accepted existing 6.25%. |
| `docs/briefs/2026-10-27-software-integration.md` | S-048 | **Wrong ID: S-041.** S-048 is the AI component-plan execution amendment, not this owner request. |
| `docs/briefs/2026-10-27-software-renderer-cycle.md` | S-040 | **Wrong ID: S-038.** S-040 is the later patch acceptance. |
| `docs/briefs/2026-10-28-component-readiness.md` | S-055 | **Wrong ID: S-050.** Owner software-only readiness request; S-055 is later AI discovery package. |
| `docs/briefs/2026-10-28-discovery-owner-decisions.md` | S-060; D-020 | **Wrong ID: S-059.** S-060 is Microsoft console documentation. Owner accepts planning limit/waiting, explicitly without guaranteed finish time or safe forced stop. |
| `docs/briefs/2026-10-28-owner-readiness-inputs.md` | S-057 | **Wrong ID: S-053.** S-057 is a Windows Argyll executable ZIP. D-019 is an accepted diagnostic policy, not hardware authority. |
| `docs/briefs/2026-10-28-t003-discovery-package.md` | S-058 | **Wrong ID: S-054.** S-058 is PowerShell source, not this owner brief. |
| `docs/briefs/2026-10-28-t003-preflight-amendment.md` | S-062 | **Wrong ID: S-063.** S-062 is Windows screen-saver/inactivity documentation. |
| `docs/briefs/2026-10-29-samsung-evidence-review-follow-up.md` | S-073 | Correct. Document revisions, no observations/actions; preserves look-only exemption. |
| `docs/briefs/2026-10-29-samsung-primary-research.md` | S-076 | **Wrong ID: S-074.** S-076 is resulting primary-source material, not the owner's research request. |
| `docs/briefs/2026-10-29-samsung-readiness-amendment.md` | S-081; D-021 | Correct. Removes specified readiness prerequisites; does not resolve underlying empirical questions. |
| `docs/briefs/2026-10-29-samsung-research-review-follow-up.md` | S-079 | Correct. Bounded wording clarifications, reviewed method unchanged. |
| `docs/briefs/2026-10-29-samsung-update-evidence-method.md` | S-070 | Correct. Historical method-preparation authority, not current collection permission. |
| `docs/briefs/2026-10-29-t003-cec-restoration-preference.md` | S-085 | Correct. Preference for proposed temporary changes/restoration reminder, not dated authority for changes/reset/discovery. |
| `docs/briefs/2026-10-29-t003-checklist-review-follow-up.md` | S-084 | Correct. Documentation correction/re-review request only. |
| `docs/briefs/2026-10-29-t003-preflight-followups.md` | S-067 | **Wrong ID: S-068.** S-067 is Windows active-hours/restart documentation, not owner authority. |
| `docs/briefs/2026-10-29-t003-readiness-checklist.md` | S-082 | Correct. Remaining discovery checklist preparation; explicit no hardware. |
| `docs/briefs/2026-10-30-t003-cec-review-follow-up.md` | S-088 | Correct. PR #37 document fixes/re-review only. |
| `docs/research/2026-10-23-chatgpt-feasibility-research.md` | “Early OpenAI critique; untouched historical archive” | Broad identity correct, but this is original feasibility research S-012, distinct from the still-unavailable S-003 critique. Its unresolved citation markers and inaccessible claimed 15-test kit require explicit treatment; generic “AI hypothesis checked” does not supply it. |
| `docs/research/2026-10-23-claude-feasibility-report.md` | S-002 early Anthropic report, untouched archive | Broad current-PR preservation correct. Historical cuts/missing embedded originals and many unverified/overstated premises remain; the latest selected-source register cannot support “all claims verifiable.” No fresh full archival-source recheck is established by this row. |
| `docs/research/2026-10-24-exlink-protocol-investigation.md` | S-005/S-006/S-007, foundation for T-006 | Broad provenance correct. It also cites S-008 and contains historical identity/hash evidence relevant to the author's own S-006/S-015 correction. Calling sources unresolved wholesale misses evidence already present. |
| `docs/research/2026-10-26-antigravity-feasibility-study.md` | S-024; “conditional infeasibility” | **Over-compressed outcome.** Actual table separates blocked automatic operation, conditionally feasible relative improvement and “infeasible under present constraints” validated absolute accuracy/near-black. Current analysis narrows the last conclusion; a faithful reassessment must preserve those distinct positions and evidence limits. |
| `docs/research/2026-10-29-samsung-update-gap-research.md` | Update research; untouched archive | Broad identity/preservation correct. P1–P11/S-076–S-078/S-080 primary checks and supersession under D-021 are not accounted for by the latest nine-entry register. Historical no-clearance banner must not reinstate retired prerequisites. |
| `docs/reviews/2026-10-25-review-records.md` | Historical records under D-015 | Correct broad outcome. The file preserves differences on PR #2 timing and later status notes; a new source-verification claim should identify actual GitHub records checked versus merely reading this record. |
| `docs/reviews/2026-10-27-pr21-review-response.md` | “aligns pySerial loci in PR #39” | **Wrong outcome.** The PR #39 diff only adds final-review completion history; this record concerns Argyll startup probes, clipping limitations and T-009. It does not align pySerial loci. |
| `docs/reviews/2026-10-27-pr22-review-response.md` | “component tools review” | **Wrong subject.** It covers renderer/toy-cycle attempt-budget restoration and hidden-simulator-state fixes, not the later physical component tools. No PR #39 change to this file. |
| `docs/tests/T-003-discovery-record.example.md` | Blank private session template | Correct. Planning-history fields coexist with NOT OBSERVED/UNRESOLVED/NOT RUN session fields; it supplies no completed readiness or operational evidence. |

## Source checks, accepted qualifications and limits

The corrected BT.709-6 printed p. 3 §1 items 1.3–1.4 and BT.1886 Annex 1 printed p. 2 references are upheld using the same-day directly inspected official originals. Exact Ex-Link query/toggle semantics, Spyder identifiers, generic WB prefixes and pinned pySerial loci retain the already documented source checks. Retained previously checked Argyll member text was reread; this round does not claim another fresh archive hash. S-029 includes source and documentation, while S-037 identifies the independently hashed artifact; their historical copies must not be silently equated.

Fresh work here consists of the S-006/S-015 binary comparison, primary Win32/ctypes page checks, review/history fetches, source/brief reconciliation, manifest/file identity and independent mathematics/text counts. No proprietary protocol original or fresh DisplayCAL candidate query was obtained by this author in this round. Standards/API/source inspections are not equipment observations.

The new response fairly restores these limits: exact-TV toggle behavior untested; defaults need not equal captured originals; no global DisplayCAL-schema absence conclusion; NOWAIT requested, not guaranteed; selected accepted-q exits to cleanup without a native delivery/cleanup guarantee; D-019 is a fresh owner-approved diagnostic minimum, with production settling unresolved. Preserve those corrections. The historical bounded correction search establishes neither a certification criterion nor global absence.

## Reproducible checks

Run these only as inspected standard-library text/arithmetic/public-download work from the pinned repository checkout. They import no project code and contact no device. The commands used Python 3.15.0 on Windows 10 build 19045. Reviewers' separately reported 287-test runs are not new author results; no broad suite, audit fixture, native handle probe or Argyll executable was run for this documentation revision.

### Mathematics and six-file counts

The density 3/8 * (1+t²/4)^(-5/2), substitution t=2 tan(theta), and integral of cos³(theta) give p=1/2−45/(26 sqrt(13)) at t=3. An independent antiderivative in z=3/sqrt(13) agrees. Computed p≈.0199709840358594 and 1−(1−p)^9≈.166030040171520. The latter assumes nine independent comparisons; actual adjacent differences share means.

Save this published code to an ignored local file and run with py -3.15 -B. It reproduces the model and corpus, not measurements:

```python
from decimal import Decimal, localcontext
from pathlib import Path

with localcontext() as ctx:
    ctx.prec = 60
    z = Decimal(3) / Decimal(13).sqrt()
    p = Decimal("0.5") - 3*z/4 + z**3/4
    alternate = Decimal("0.5") - Decimal(45)/(26*Decimal(13).sqrt())
    print("p", p, "alternate", alternate, "difference", p-alternate)
    print("independent_family", 1-(1-p)**9)

names = [
    "T-003-discovery-execution.md",
    "T-003-discovery-preflight.md",
    "T-003-discovery-console.md",
    "T-003-discovery-readiness.md",
    "T-003-discovery-record.example.md",
    "T-003-cec-change-proposal.md",
]
totals = [0, 0]
for name in names:
    tokens = (Path("docs/tests") / name).read_text(encoding="utf-8").split()
    counts = (len(tokens), sum(any(c.isalnum() for c in t) for t in tokens))
    print(name, *counts)
    totals = [a+b for a, b in zip(totals, counts)]
print("totals", *totals)
```

| Document suffix | Whitespace tokens | Tokens containing a letter/digit |
|---|---:|---:|
| execution | 4178 | 4017 |
| preflight | 3678 | 3523 |
| console | 2109 | 2072 |
| readiness | 1363 | 1308 |
| record.example | 1468 | 1344 |
| cec-change-proposal | 1692 | 1643 |
| **Total** | **14488** | **13907** |

Every per-file result in Antigravity's new review agrees. The analytic derivation and specified corpus/rules now provide useful independent reproducibility; missing script publication must not be misrepresented as absence of all numerical evidence.

### Public worksheet identity

The inspected download calculation below is a public equivalent of the actual run, which additionally saved requested/final URLs and results to ignored JSON. It neither installs nor executes the PDFs. The 2,000,000-byte limit exceeds the actual 509,710-byte responses.

```python
from hashlib import sha256
from urllib.request import urlopen

urls = [
    "https://raw.githubusercontent.com/home-assistant-libs/samsung-exlink/"
    "e2489b33c720c36d1995392b803f2336baf7b808/docs/Samsung-RS232-Control.pdf",
    "https://image-us.samsung.com/SamsungUS/samsungbusiness/"
    "tv-ci-resources/Samsung-RS232-Control.pdf",
]
copies = []
for url in urls:
    with urlopen(url, timeout=30) as response:
        data = response.read(2_000_001)
        if len(data) > 2_000_000:
            raise ValueError("Response exceeds comparison limit")
        print(response.status, len(data), sha256(data).hexdigest(), data[:5])
        copies.append(data)
print("direct_bytes_equal", copies[0] == copies[1])
```

Both responses returned the full digest and size above; direct_bytes_equal was True. Later live manufacturer content may change, so retain the date, pinned community URL and observed digest. No hardware applicability follows.

### Identity and diff checks

The unchanged application/test files and documented 34-entry manifest were checked against disk bytes. The baseline archive files were checked for preservation. Full diff, IDs and local Markdown links were checked; existing frozen-brief broken links remain outside this revision. No source/test/dependency edit or new execution fixture is needed for a documentation/source-provenance correction. Exact resulting head and validation results are in the PR description.

## Decision and remaining work

Correct A9-01 and the stale maintained source cells in a small documentation commit. Credit Antigravity's updated reading report, P7 withdrawals, exact inventory, technical supersession and correct calculations. Retain P9-01–06 and the missing source/experiment evidence; do not mark the requested Google full-remit review complete from the supplied record.

Both vendors need to review the changed head. Claude's complete current-head review remains pending/unavailable; Antigravity's latest review covers only the prior d2 head. Refreshed prompts must identify this correction, the author error it withdraws, current paths and exact SHAs. No recommendation, internal Codex check or silence replaces an actual review. Only the owner decides whether to merge. No merge or equipment action occurred.
