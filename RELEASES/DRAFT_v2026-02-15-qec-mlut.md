Release: Pillar-45 — GF(3) QEC primitives + MLUT decoder (draft)

Tag: v2026-02-15-qec-mlut (suggested)

Summary
- This release formalizes Pillar‑45: GF(3) qutrit QEC primitives derived from the W(3,3) finite geometry and integrated into the W33→E8 codebase. It adds encoder/decoder implementations, MLUT (exact and approximate) decoders, coverage statistics, unit/property/benchmark tests, CI notebook execution, and performance micro‑optimizations.

Notable changes (high level)
- scripts/w33_quantum_error_correction.py — new public API for GF(3) encode/decode and MLUT utilities
- notebooks/w33_qec_demo.ipynb — executed demo and visualization
- tests/test_e8_embedding.py — added comprehensive QEC test coverage
- .github/workflows/qec.yml — CI workflow to run QEC tests, execute the demo notebook, and run an MLUT benchmark

How to verify
- Run the targeted QEC tests: `pytest -q tests/test_e8_embedding.py::TestQuantumErrorCorrection`
- Execute demo: `jupyter nbconvert --to notebook --execute --inplace notebooks/w33_qec_demo.ipynb`

Assets
- Demo notebook (executed) attached to the release (after publishing)
- Example outputs: `checks/PART_CXV_qec_*.json`

Post-release next steps
- Publish to Zenodo (create DOI)
  - If the GitHub→Zenodo webhook does not create a DOI, a manual deposition script is available: `scripts/manual_zenodo_deposit.sh` (bash) or `scripts/manual_zenodo_deposit.py` (Python). See `README.md` for a short how‑to.
- Draft blog post & social announcement (included in `outreach/`)
- Solicit benchmarks from the community (issue/discussion)

Contributors
- Wilj D. (author), + reviewers

Changelog (brief)
- Add: GF(3) encoder/decoder, syndrome & MLUT decoders
- Add: approximate MLUT sampler + coverage stats
- Add: notebook, unit/property tests, CI
- Perf: fast‑syndrome helper and MLUT optimizations
