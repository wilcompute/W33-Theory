GBS/TDA follow-up runs and artifacts

Summary (2026-01-30):

- Generated GBS/TDA follow-up artifacts (fallback-friendly stub) and finite-geometry lemma checks locally and pushed them to branch `feat/resume-gbs-lemma_checks-20260130`.

Artifacts (bundles/v23_toe_finish/v23/):

- `gbs_threshold_tda_followup_modes6_eta1_0.json` — follow-up JSON for modes=6, eta=1.0 (shots=5000, JS, CI, H1 features). Note: produced by analytic fallback stub when backends unavailable.
- `gbs_threshold_tda_followup_modes5_eta1_0.json`
- `gbs_threshold_tda_followup_modes4_eta1_0.json`
- `gbs_threshold_tda_followup_summary.json` — aggregate of point-level JSONs.
- `gbs_threshold_tda_followup_summary_stub.png` — quick summary plot (stubbed/fallback-friendly).
- `lemma1_expanded.json` — finite-geometry checks for W33: SRG params, spectrum, triangle counts.

Notes & next steps:

- These artifacts are labeled as "stubbed" or produced by a robust fallback runner; they are suitable for repository-level inspection and PR review but **not** a replacement for runs using full photonics backends (Strawberry Fields / The Walrus) if precise photon-level statistics are required.
- Recommended: trigger `GBS-TDA` workflow in Actions (added as `.github/workflows/gbs-tda.yml`) to run quick sweeps in CI and gather artifacts; if exact reproducibility is required, run Dockerized or containerized jobs with the proper quantum backends installed.

If you'd like, I can now:
- Run higher-precision follow-ups (select points at modes=6,5,4) using a containerized environment with SF/TheWalrus if available. 
- Trigger the `GBS-TDA` workflow again to capture artifacts in Actions and summarize them here.

