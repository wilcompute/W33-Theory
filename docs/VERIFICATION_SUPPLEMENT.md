Verification Supplement — Part CXIII
-----------------------------------

This short supplement documents how the Sage verification (Part CXIII) was executed and how to reproduce it.

Reproducing locally (WSL + micromamba):
1. Install micromamba (see `install_sage_wsl_micromamba.sh`).
2. Create the `sage` environment and install Sage + GAP:
   - `micromamba create -n sage -c conda-forge sage gap -y`
   - Note: adding `gap` explicitly can resolve missing `lib/init.g` errors on some systems.
3. Run the verification script:
   - `micromamba run -n sage python3 sage_verify.py`
   - Output: `PART_CXIII_sagemath_verification.json` (contains the key numeric checks and logs).

Docker (alternative, stable):
- `docker run --rm -v "$(pwd)":/work -w /work sagemath/sagemath:10.7 sage -python sage_verify.py`
  - The Docker approach avoids many WSL / system-specific library issues and is the recommended path for CI reproducibility.

Troubleshooting & expected outputs
- If you see a GAP error such as `cannot find 'lib/init.g'` or intermittent SIGSEGV, try:
  - Ensuring `gap` is installed into the `sage` micromamba env (see step 2).
  - Use the Docker image above (stable & reproducible).  
- Expected verification outputs (sample):
  - `vertices`: 40
  - `edges`: 240
  - `sp4_f3_order`: 51840
  - `w_e6_order`: 51840
  - `aut_order`: 51840
  - `eigenvalues`: [[12,1],[2,24],[-4,15]]

Notes:
- The final verification JSON is saved under `bundles/v23_toe_finish/v23/PART_CXIII_sagemath_verification.json`. The verification summary is in `docs/SAGE_VERIFICATION_SUMMARY.md`.
- If you want, I can run Docker-based verification on CI and attach the logs to the PR for complete transparency.

Contact:
- If you want, I can run the Docker-based verification end-to-end and attach logs to the PR.
