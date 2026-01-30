Quick start — Quantum Photonics prototypes

1. Create/activate the project's venv (already present):
   & ".venv\Scripts\Activate.ps1"  (PowerShell)

2. Install dependencies (we provide a pinned requirements file):
   python -m pip install -r requirements-quantum-photonics.txt

3. Run a quick smoke test:
   & ".venv\Scripts\python.exe" scripts\quantum_photonics\run_cv_repeater.py

4. Notebooks are in `notebooks/quantum_photonics/` — open in Jupyter or VS Code.

Notes:
- Strawberry Fields required SciPy pinned to 1.10.1 in this environment for import compatibility.
- GBS sampling can use either the `gaussian` backend (fast Gaussian states) or the `fock` backend for true Fock sampling on small instances.

Next: implement backend selection in `run_gbs.py`, add classical emulator comparisons, and expand the notebooks.
