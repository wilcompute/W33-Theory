# Batch 415–429: intake findings, repair, and closure

*The initial findings were produced by `scripts/audit_batch.py` during Passes
432–433. They correctly described the stale branch that existed at that time.
This file now also records the completed repair path.*

## Initial findings

1. **The original branch was stale.** `origin/agent/pass415-429-fifteen-frontiers`
   forked from the Pass-398 formula freeze and did not contain the promised
   fifteen-pass scientific tree. Its only content addition was
   `data/w33_formula_search_universe_v1.json`.
2. **Merging that branch as-is would have regressed `master`.** It predated
   Passes 430–433 and could not be overlaid safely.
3. **The stale formula-universe file contained one certified-value
   contradiction.** It wrote `[[240,81,4]]` where the certified code is
   `[[240,81,3]]_3` with `d_Z=4`.

Those findings remain historically correct. They do **not** describe the final
repaired release.

## Repair closure — completed 2026-07-18

The batch was rebuilt from readable source on current `master`, with no opaque
transport artifact and no destructive rebase:

- PR #120 merged Passes 415–424 at
  `2766a9c3c5cb81ed0e13553443790ae84cfc1c2d`.
- PR #125 merged Passes 425–429 at
  `2b83623f866c22df42232630248792be3e2a7309`.
- PR #126 hardened Pass 426's floating diagnostics for cross-runner portable
  certification at `822739b1224418b76159dc38b6857600d75aff97`.
- The exact Passes 425–429 intake audit passed in workflow run `29655712622`.
- The same run passed all fifteen deterministic witnesses, all three regression
  suites, schema validation, and the live claims ledger.
- The stale formula-universe file was not imported by the repaired batch; the
  repository's certified `[[240,81,3]]_3`, `d_Z=4` notation remains canonical.

## Repair checklist disposition

- [x] Rebuild on current `master` without deleting master-side work.
- [x] Land the actual scientific files directly in Git, replacing the failed
      issue-comment/archive transport with a stronger readable-source path.
- [x] Run the executable intake harness on the exact released file list and
      retain it as a permanent CI gate.
- [x] Preserve the certified `[[240,81,3]]_3`, `d_Z=4` distinction.
- [x] Use witness `PASS`/`FAIL` vocabulary and content-addressed certificates.
- [x] Preserve the reserved Pass numbers 415–429.
- [x] Record explicit claim boundaries: Pass 426 is numerical; Passes 427–428
      use synthetic channel/noise assumptions; no physical experiment is
      claimed.

## Current status

🟢 **MERGED AND AUDITED.** The v1.2 batch-resolution gate is closed.

The harness is `scripts/audit_batch.py`; the protocol is
`.continuity/INSTRUCTIONS.md` ("Batch intake"). The original machine findings
remain in `data/w33_pass432_genuinely_nonabelian_pds.json` and
`data/w33_pass433_abelian_pds_tower_theorem.json` as the pre-repair record.
