<!--
Fill in every section. Write "None" rather than deleting a section.
The rules behind this checklist are in AGENTS.md.
-->

## Summary in plain English

What changes and why, and what the owner needs to do next, if anything.

## Author

- Written by (agent and company):
- Branch:
- Independent review needed from (the other company's agent):

## What changed

-

## Author's checklist

### Evidence

- [ ] New or changed claims are in `LEDGER.md`, each with its provenance **and**, separately, its equipment test status.
- [ ] Nothing is invented: every citation was actually consulted, and every measurement or test result really happened.
- [ ] AI-generated statements are labelled with the system that produced them.
- [ ] Simulation results are labelled as simulations, not as tests on the owner's equipment.

### Safety and approvals

- [ ] No unauthorised equipment operation. Any authorised equipment operation links to the approved test plan, the owner's authorisation and, if carried out, its results. Plans without authorisation are clearly marked as awaiting it.
- [ ] No purchases, paid APIs or services, GitHub Actions or other automation, deployment or irreversible changes — unless the owner approved them first (link the approval here).
- [ ] No passwords, tokens, network addresses, serial numbers or other private details.
- Hardware spending proposed: £___ (the running total must stay within £25 — ledger section 7)

### Disagreements and clarity

- [ ] Unresolved disagreements are recorded in `LEDGER.md`, not smoothed over.
- [ ] The summary makes sense to a non-programmer.

## For the independent reviewer

Copy this section into your review and fill it in.

- Reviewer (agent and company):
- [ ] My company is not the author's company.
- [ ] The changes match the summary, and nothing unrelated is included.
- [ ] I checked the claims and citations against their sources. Problems found:
- [ ] Nothing appears invented — or I have listed it here:
- [ ] The safety, approval and privacy rules in `AGENTS.md` are respected.
- Disagreements with the author (to be recorded in `LEDGER.md` if unresolved):
- Recommendation: merge / change first / cannot assess (say why)

## Owner's decision

Only the owner merges or closes this pull request.
