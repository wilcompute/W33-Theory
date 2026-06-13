# BT905 — Holonet Profile CI Guard

BT905 adds a one-command local guard for the Holonet profile correction stack.

## Command

```bash
python tools/run_bt905_holonet_profile_ci.py --compile
```

Without `--compile`, it still runs the patch/profile/cross-index checks but skips `pdflatex`.

## What it runs

1. `tools/apply_bt903_holonet_root_patch.py`
2. `analysis/bt899_photonic_holonet_static_guard.py` indirectly through BT903
3. `analysis/bt901_s3_profile_basis_search.py`
4. `analysis/bt904_constrained_profile_solver.py`
5. `analysis/bt902_holonet_profile_cross_index.py`
6. optional two-pass `pdflatex` through BT903

## Guarded invariant

\[
\boxed{\text{The Holonet paper remains the Holonet paper, while the Yukawa/numerical layer remains a shifted-reflection }S_3\text{ skeleton plus }q^2=9\text{ profile layer.}}
\]

## Witness

```text
tools/run_bt905_holonet_profile_ci.py
data/PART_BT905_HOLONET_PROFILE_CI_results.json
```
