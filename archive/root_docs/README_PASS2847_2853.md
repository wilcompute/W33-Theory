# Passes 2847--2853 release navigation

- Exact executable verifier: `analysis/bt2847_2853_protected_observer_noisy_m36.py`
- Frozen certificate: `data/PART_BT2847_BT2853_PROTECTED_OBSERVER_NOISY_M36_results.json`
- Technical report: `analysis/BT2847_BT2853_protected_observer_noisy_m36.md`
- Claim ledger: `analysis/BT2847_BT2853_claim_ledger.md`
- Literature boundary: `analysis/BT2847_BT2853_literature_boundary.md`
- Manuscript insert: `analysis/BT2847_BT2853_protected_observer_noisy_m36_insert.tex`
- Feature encoder: `rtl/w33_pass2848_affine_square_feature_encoder.sv`
- Protected decoder: `rtl/w33_pass2853_affine_square_nn_decoder.sv`
- RTL testbench: `rtl/tb_w33_pass2853_affine_square_nn_decoder.sv`
- Regressions: `tests/test_bt2847_2853_protected_observer_noisy_m36.py`
- Canonical integrator: `tools/integrate_bt2847_bt2853.py`
- Observable workflow: `.github/workflows/w33_pass2847_2853_protected_observer.yml`

Headline: the historical protected trajectory has an exact 28-tap optimum, while a new affine-square measurement schedule reaches distance four in 24 samples. Active feedback identifies every ternary frame in at most four operations. The noisy deep-grade recurrence has a golden saddle node at `g=(7-3sqrt(5))/4`.
