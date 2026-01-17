Running verification scripts (local instructions)

Prerequisites:
- Python 3.10+ (for general scripts and tests)
- SageMath 10.7 (or compatible) installed and accessible
- Ensure `external/sage` points to a local installation or update `SAGE_DIR` in scripts

Quick steps:

1. Install Python dev requirements:

   python -m pip install -r requirements-dev.txt

2. Run unit tests:

   pytest -q

3. Run Sage verification (requires Sage):

   # From workspace root (if you have Sage installed locally):
   python sage_verify.py

   This produces `PART_CXIII_sagemath_verification.json`.

   Alternatively, using Docker (no local Sage install required):

   # Run a single Sage script in the official Sage container:
   docker run --rm -v "$(pwd)":/work -w /work sagemath/sagemath:10.7 ./claude_workspace/run_sage.sh claude_workspace/THEORY_PART_CXIII_SAGE_VERIFICATION.sage

   # Or run the full set of Sage verifications (helper script):
   docker run --rm -v "$(pwd)":/work -w /work sagemath/sagemath:10.7 bash -lc "chmod +x scripts/run_all_sage.sh && scripts/run_all_sage.sh"

4. Run proofs (numerical) - ensure `data/` files exist:

   python src/PROOF_MINUS_ONE.py
   python extracted/claude_workspace/claude_workspace/THE_PROOF.py

Notes:
- The Sage script sets PATH to `external/sage/bin` and inserts the Sage site-packages path; if you have Sage installed elsewhere, edit `SAGE_DIR` at the top of `sage_verify.py` and `part_cxviii_sage.py`.
- Verification scripts write JSON summaries into the workspace root (files named `PART_*.json`).
- If tests fail, open an issue with the failing test name and stack trace.

Last automated trigger: 2026-01-16T20:40:00Z
