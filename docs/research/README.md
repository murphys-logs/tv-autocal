# Research archive

This folder keeps research material — reports, critiques, references and notes — **exactly as received**, with a record of where each item came from. It answers *"who said this, and when?"*. It does not answer *"is it true on the owner's equipment?"* — that is the job of [docs/tests/](../tests/README.md). [LEDGER.md](../../LEDGER.md) keeps the two apart, as the owner's rule 3 requires.

## Filing a new item

1. **One file per document**, named `YYYY-MM-DD-short-title.md` with the original's date. If the date is unknown, use the import date and say so in the header.
2. **Start the file with this table:**

   | Field | Value |
   |---|---|
   | Title | |
   | Produced by | Person or organisation, or AI system and vendor |
   | Original date | |
   | Imported | Date, and by whom |
   | How obtained | For example: "pasted by the owner from a ChatGPT conversation" |
   | Fidelity | Verbatim, excerpt or summary |
   | Ledger ID | S-___ |

3. **Paste the original unchanged**, mistakes included. Put any comments in the ledger, not in the document.
4. **Add a source entry** to section 1 of the ledger, and record any claims taken from the document in section 2, with provenance pointing back to it.
5. **Never edit an archived original once merged.** If a better copy turns up, archive it as a new file and note the relationship in the ledger. The only exceptions are changes the owner has explicitly instructed, listed in [AGENTS.md section 6](../../AGENTS.md#6-evidence-provenance-and-citations-rules-3-and-5).

## AI-generated material

AI reports and critiques are archived like any other source, but every statement in them is a hypothesis — provenance `AI: <system>` — until it has been checked against a primary source or tested. An AI document that cites a source is not the same as the source: check the source itself before relying on it.

## Third-party material

The project is intended to become open source. Unless a document's licence allows redistribution, do not archive full copies of third-party material such as manuals, web pages or papers. Record the citation, short relevant quotations and notes instead.

## Research recorded here

- [TV Calibration Feasibility Testing — original ChatGPT research](2026-10-23-chatgpt-feasibility-research.md) — ChatGPT (OpenAI), 23 October 2026, S-012. Complete original response; citations remain unresolved and equipment capabilities remain untested. Historical proposals do not authorise physical tests or replace later project decisions. See the [import notes](#s-012-import-notes).

- [Claude feasibility report](2026-10-23-claude-feasibility-report.md) — Claude (Anthropic), 23 October 2026, S-002. Pasted by the owner from a Claude Docs document and archived word for word, except that the owner's name is removed at the owner's request (D-012) and one list item is removed at the owner's instruction (D-013). Imported as AI hypotheses. Targeted later source checks are recorded in the ledger (S-014 to S-017); unchecked assertions remain hypotheses and nothing has been tested on the owner's equipment. Its network and infrared control routes are out of scope under D-006.

- [Ex-Link protocol investigation and proposed offline verification](2026-10-24-exlink-protocol-investigation.md) — Codex (OpenAI), 24 October 2026, S-005. Cited source inspection and checksum arithmetic; the software-only verification plan is proposed and unexecuted. TV compatibility remains untested. One clause is removed at the owner's instruction (D-013).

- [TV-side auto-calibration of the Samsung UE49KS7000UXXU: independent feasibility study](2026-10-26-antigravity-feasibility-study.md) — Antigravity (Google), 26 October 2026, S-024. Independent feasibility synthesis and primary/secondary source audit (S-025 to S-031, C-062 to C-073, X-010); AI analysis and design proposals remain hypotheses, and nothing has been tested on the owner's equipment.

## Earlier report waiting to be imported

| Ledger ID | Document | Produced by | Original date | Planned file name | Status |
|---|---|---|---|---|---|
| S-003 | ChatGPT critique | ChatGPT (OpenAI) | Unknown | To be decided once the date is known | Waiting for the owner to supply the original text |

The original text of S-003 is still unavailable in this repository. The separate feasibility response S-012 has been recovered and archived; it does not replace S-003. Until S-003 is imported, nothing in this repository depends on its contents.

## S-012 import notes

Moved here from [LEDGER.md](../../LEDGER.md) on 26 October 2026 under D-015, word for word apart from link paths. In these notes, "below" refers to the ledger, where the S-012 claims (C-025 to C-034) and the comparisons are recorded.

The owner requested this original feasibility response on 2026-10-25: "Use the original feasibility research as shown in your reply". The response was retrieved through the chat-reading connector, rather than reconstructed from summaries. It contains no Claude-authored report, quotation or commentary. The retrieved assistant body has 13,203 characters; the archived body preserves them and adds one terminal newline. Original response completion: 2026-10-23 21:35:18 UTC. Source and message identifiers are in the archive header.

- **Unverified citations:** all 18 original `:chatgpt-content-reference` markers remain as returned. Their underlying sources were not resolved or newly checked for this import. The one ordinary GitHub URL is retained as an original citation, not a claim of a new source check. The two `sandbox:` ZIP links are historical conversation links, not working repository downloads; no diagnostic kit or executable is included.
- **Unverified historical result:** the statement that the kit passed 15 offline tests is an original AI-reported result (C-025), not a result reproduced or established by this import. No hardware operation, simulation or calibration test was run for the import.
- **Historical scope:** the report predates D-006, so its network-control proposals and commands remain archived history, outside the current Ex-Link-only scope. Its proposed physical steps are not an authorised plan under [AGENTS.md section 7](../../AGENTS.md#7-equipment-safety-rule-6). The later measurement cycle (D-013) applies to any future implementation.
- **Historical equipment and budget wording:** uncertainty about the model and advice not to buy a cable precede the owner's model and purchase records C-001 and C-008. The claimed £0 starting experiment does not reset the current £15.99 spend or £9.01 balance.
- **Example address:** the network command contains an assistant-created illustrative private address, not a supplied or observed address of the owner's equipment. It is preserved solely for fidelity to the original; the source user prompt supplied no IP address. No credentials, actual network addresses or device serial numbers are imported.
- **Coverage:** this file contains the complete single feasibility response selected by the owner. It is not a compilation of every OpenAI project chat and is not the separate ChatGPT critique S-003. S-002 has since been imported by PR #10; only S-003 remains missing. The two available reports are compared below; no view is attributed to the unavailable critique.

All technical assertions in S-012 remain `AI: ChatGPT (OpenAI)` hypotheses for this import. Existing claims C-002 to C-007 and their equipment test statuses are unchanged. The additional claim records below catalogue the historical report without adopting its recommendations as new project decisions.
