Methods & Summary — Computational Verification
-----------------------------------------------

Purpose
-------
Provide a concise description of how computational verification supports the proof in Part CXIII and references for reproducibility.

Key computational checks
-----------------------
- Group theory checks: |Sp(4, F_3)|, |W(E6)|, and |Aut(W33)| were computed and found equal to 51,840.
- Combinatorial checks: W33 has 40 vertices and 240 edges; edge-count equals number of E8 roots.
- Spectral checks: adjacency eigenvalues (12:1, 2:24, -4:15) computed and recorded.

Reproducibility & commands
--------------------------
- WSL + micromamba:
  - `bash install_sage_wsl_micromamba.sh`
  - `micromamba create -n sage -c conda-forge sage gap -y`
  - `micromamba run -n sage python3 sage_verify.py`
- Docker:
  - `docker run --rm -v "$(pwd)":/work -w /work sagemath/sagemath:10.7 sage -python sage_verify.py`

Artifacts
---------
- `bundles/v23_toe_finish/v23/PART_CXIII_sagemath_verification.json` (machine-readable verification)
- `docs/SAGE_VERIFICATION_SUMMARY.md` (human summary)
- `docs/VERIFICATION_SUPPLEMENT.md` (reproduction steps + troubleshooting)

Notes & provenance
------------------
All scripts used for verification are included under the repository root (e.g., `sage_verify.py`, `THEORY_PART_CXIII_SAGE_VERIFICATION.sage`). The outputs are recorded in the `bundles/` folder so reviewers can inspect the full logs and data used in the checks.
