# BT1902-BT1904 summary

Executed BT1902-BT1904.

## BT1902

Added the Holonet insert integrator:

```text
tools/integrate_bt1899_holonet_insert.py
```

It reads `papers/BT1899_holonet_residual_and_guard_insert.tex`, splits it into residual and guard blocks, inserts them at marker locations, and writes a non-destructive output artifact:

```text
papers/BT1347_photonic_holonet_journal_with_BT1899.tex
```

## BT1903

Added a small synthetic demonstrator fixture:

```text
data/bt1903_synthetic_demonstrator_fixture.jsonl
```

It has 24 rows: 16 diagonal contextual rows with 2 clicks, 4 off-diagonal data rows, 2 dark-reference guards, and 2 loss-probe guards.  It is meant to exercise the validator and estimator end-to-end, not to simulate a full 640-record run.

## BT1904

Added the exact/Bayesian contextual-fraction estimator:

```text
analysis/bt1904_exact_contextual_fraction_estimator.py
```

It reports an exact two-sided binomial p-value for target p=1/10, a Beta(1,1) posterior summary, an equal-tail credible interval by dependency-free grid quadrature, and the same dark/loss-corrected point estimate used by BT1901.

Boundary: local integration script, synthetic fixture, and statistical estimator only; no remote TeX build, experimental data, or final detector calibration is claimed.
