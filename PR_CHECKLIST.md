Checklist for PR review & merge
-----------------------------
- [ ] **Run interactive `detect-secrets` audit locally** and commit finalized `.secrets.baseline` (a conservative placeholder exists at `scripts/generated_baseline.json`).
- [ ] **Confirm Git LFS tracked files** — known large artifacts were moved into LFS (e.g., `data/repetend_scan/*`, `maniplex_doc_bundle/*.pdf`, `bundles/**/*.json`).
- [x] **Sage verification (Part CXIII) added** — results saved to `bundles/v23_toe_finish/v23/PART_CXIII_sagemath_verification.json` and summarized in `docs/SAGE_VERIFICATION_SUMMARY.md`.
- [ ] **Resolve any CI failures** reported on the PR (a no-op commit was pushed to trigger CI; please re-run/inspect CI checks).
- [ ] **Assign reviewers** and mark the PR ready for review once the above items are complete.
- [ ] **Post the prepared PR comment** (see `PR_COMMENT.md`) so reviewers are notified of the verification artifacts and next steps.

Notes
-----
- I can complete any of these steps on request. The branch `photonic/threshold-sweeps` is pushed and a draft PR created. If you finish the interactive detect-secrets audit, tell me and I’ll finalize the baseline and re-run checks.
