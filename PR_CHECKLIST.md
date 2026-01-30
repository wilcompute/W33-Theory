Checklist for PR review & merge
-----------------------------
- [ ] **Run interactive `detect-secrets` audit locally** and commit finalized `.secrets.baseline` (a conservative placeholder exists at `scripts/generated_baseline.json`).
- [ ] **Confirm Git LFS tracked files** — known large artifacts were moved into LFS (e.g., `data/repetend_scan/*`, `maniplex_doc_bundle/*.pdf`, `bundles/**/*.json`).
- [ ] **Resolve any CI failures** reported on the PR (a no-op commit was pushed to trigger CI; please re-run/inspect CI checks).
- [ ] **Assign reviewers** and mark the PR ready for review once the above items are complete.

Notes
-----
- I can complete any of these steps on request. The branch `photonic/threshold-sweeps` is pushed and a draft PR created. If you finish the interactive detect-secrets audit, tell me and I’ll finalize the baseline and re-run checks.
