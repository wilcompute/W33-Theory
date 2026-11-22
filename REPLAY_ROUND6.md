# W33/Witting/E6 round-six reproducibility, 22 November 2026

All runnable sources expect the companion `analysis/toe_20261122_*.py` baseline files in this same bundle/repository. Run in the bundle root:

```bash
python -m pip install numpy scipy sympy networkx pytest
OPENBLAS_NUM_THREADS=1 PYTHONPATH=analysis python -m pytest -q tests/test_toe_20261122_round6_five_and_more.py
OPENBLAS_NUM_THREADS=1 PYTHONPATH=analysis python analysis/toe_20261122_round6_execute_all.py
```

Check `data/toe_20261122_round6_exact_minimal16.json` for the exact 16-effect Witting support, weights, six modular ranks and Gram determinant `25/59049`. Compare `data/toe_20261122_round6_exact_Hasse_cut.json` for the explicit 20+20 W33 partition and sharp 80-edge deletion theorem. `analysis/2026-11-22_round6_exact16_Witting_Hasse_E6_FD_gates.md` documents all assumptions, prior art and negative controls.

For `toe_20261122_round6_minimal_ic.py`, only the LP's rank-16 solution is informationally complete; finding four rays summing to identity is NOT an IC-POVM. Other exhaustive MILP and Monte Carlo scripts are exploratory; none of their random samples are used in the exact proof.

No real hardware, E6 gauge vacuum with realistic Standard Model spectrum, or Lorentzian continuum is claimed. The local Windows clone was not modified, and GitHub CI results should be checked separately.
