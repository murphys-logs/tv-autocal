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
5. **Never edit an archived original once merged.** If a better copy turns up, archive it as a new file and note the relationship in the ledger.

## AI-generated material

AI reports and critiques are archived like any other source, but every statement in them is a hypothesis — provenance `AI: <system>` — until it has been checked against a primary source or tested. An AI document that cites a source is not the same as the source: check the source itself before relying on it.

## Third-party material

The project is intended to become open source. Unless a document's licence allows redistribution, do not archive full copies of third-party material such as manuals, web pages or papers. Record the citation, short relevant quotations and notes instead.

## Research recorded here

- [TV Calibration Feasibility Testing — original ChatGPT research](2026-10-23-chatgpt-feasibility-research.md) — ChatGPT (OpenAI), 23 October 2026, S-012. Complete original response; citations remain unresolved and equipment capabilities remain untested. Historical proposals do not authorise physical tests or replace later project decisions. See the [import notes](../../LEDGER.md#s-012-import-notes).

- [Ex-Link protocol investigation and proposed offline verification](2026-10-24-exlink-protocol-investigation.md) — Codex (OpenAI), 24 October 2026, S-005. Cited source inspection and checksum arithmetic; the software-only verification plan is proposed and unexecuted. TV compatibility remains untested.

## Earlier reports waiting to be imported

| Ledger ID | Document | Produced by | Original date | Planned file name | Status |
|---|---|---|---|---|---|
| S-002 | Claude feasibility report | Claude (Anthropic) | 2026-10-23 | `2026-10-23-claude-feasibility-report.md` | Waiting for the owner to supply the original text |
| S-003 | ChatGPT critique | ChatGPT (OpenAI) | Unknown | To be decided once the date is known | Waiting for the owner to supply the original text |

The original texts of S-002 and S-003 are still unavailable in this repository. The separate feasibility response S-012 has been recovered and archived; it does not replace either document. Until S-002 and S-003 are imported, nothing in this repository depends on their contents.
