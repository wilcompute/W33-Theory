# Batch 415–429: pre-merge intake findings and repair checklist

*Produced by `scripts/audit_batch.py` (first pre-merge run, Passes 432–433).
This is a repair path, not a rejection.*

## Findings

1. **The branch is stale.** `origin/agent/pass415-429-fifteen-frontiers` forks
   from the Pass-398 formula freeze. It does **not** contain the promised
   fifteen-pass archive (consistent with the stream's own report that the
   repaired transport workflow never completed). Its only content addition is
   `data/w33_formula_search_universe_v1.json`.
2. **Merging as-is would regress `master`.** The branch predates Passes
   430–433 (intake audit, nesting tower law, PDS results, harness, checker
   hardening); a merge of the branch head over master would delete them.
3. **One certified-value contradiction.** The formula-universe file asserts
   `[[240,81,4]]` three times, against the certified `[[240,81,3]]` in the
   witness corpus. This is plausibly a **d versus d_Z conflation** (the corpus
   elsewhere records `[240,81,d_Z=4]_3`), but under the `[[137,1,3]]` rule a
   batch that contradicts a certificate must name the certificate it
   supersedes and why — or fix the notation.

## Repair checklist for a mergeable resubmission

- [ ] Rebase the branch onto current `master` (≥ Pass 433); resolve nothing by
      deletion of master-side files.
- [ ] Land the actual 415–429 archive **on the branch** (not in issue
      transport): 34 files, with the manifest's SHA-256 and decoded size
      committed beside them.
- [ ] Run `py -3 scripts/audit_batch.py --archive <file> --sha256 <hex>
      --size <bytes>` and include its output in the reservation/merge commit
      message (protocol step 5).
- [ ] Disambiguate `[[240,81,4]]`: either correct to `[[240,81,3]]`, or write
      `d_Z=4` explicitly, or name the superseded certificate.
- [ ] Certificate vocabulary: every batch JSON either uses witness `PASS`/
      `FAIL` or is named `*attestation*`/`*release_manifest*` so the ledger
      checker classifies it correctly.
- [ ] Pass numbers 415–429 are honored as reserved to this batch; no
      renumbering needed if the resubmission lands on a rebase.

## Contact surface

Findings machine-verified in `data/w33_pass432_genuinely_nonabelian_pds.json`
and `data/w33_pass433_abelian_pds_tower_theorem.json`. The harness is
`scripts/audit_batch.py`; the protocol is `.continuity/INSTRUCTIONS.md`
("Batch intake").
