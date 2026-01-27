# W33 Baseline Control Experiment

Generated: 2026-01-13T23:31:53Z

This compares W33’s base-number set against random ‘shape-matched’ base sets under the same expression grammar.
The goal is to measure whether W33 is *systematically better than generic numerology*.

## Config

- reps: 10
- seed: 1337
- max_pool: 60000
- max_depth: 3
- pair_limit: 700
- modes: strict, medium

## Mode: strict

- W33 expressions scored: 60000
- Random reps: 10

### Best-fit comparison

Empirical p-value `p(best)` means: fraction of random base sets whose best-fit error is ≤ W33’s best-fit error.

| target | W33 best % error | random best % error quantiles (q05/q50/q95) | p(best) |
|---|---:|---|---:|
| alpha | 0.077917% | q05=0.0218805, q50=0.0774306, q95=0.197805 | 0.600 |
| higgs_over_z | 0.047368% | q05=0.00189562, q50=0.00848444, q95=0.111283 | 0.700 |
| omega_lambda | 0.001613% | q05=0.014971, q50=0.0497725, q95=0.0816366 | 0.000 |
| cabibbo_deg | 0.012781% | q05=0, q50=0.011798, q95=0.0168334 | 0.900 |

### Hit-count comparison (≤1%)

Empirical p-value `p(hits)` means: fraction of random base sets whose hit-count at ≤1% is ≥ W33’s hit-count.

| target | W33 hits ≤1% | random hits ≤1% quantiles (q05/q50/q95) | p(hits) |
|---|---:|---|---:|
| alpha | 12 | q05=10.45, q50=16.5, q95=21.55 | 0.800 |
| higgs_over_z | 21 | q05=21.25, q50=30.5, q95=43.05 | 0.900 |
| omega_lambda | 13 | q05=20.45, q50=25.5, q95=30.65 | 1.000 |
| cabibbo_deg | 42 | q05=46, q50=59, q95=119.15 | 1.000 |

### Hit-count comparison (≤0.1%)

| target | W33 hits ≤0.1% | random hits ≤0.1% quantiles (q05/q50/q95) | p(hits) |
|---|---:|---|---:|
| alpha | 1 | q05=0, q50=1, q95=2 | 0.800 |
| higgs_over_z | 4 | q05=0, q50=3, q95=5 | 0.300 |
| omega_lambda | 2 | q05=1, q50=3, q95=5.65 | 0.700 |
| cabibbo_deg | 4 | q05=5.45, q50=9.5, q95=18.95 | 1.000 |

Interpretation notes:

- With small `reps`, a reported p-value of `0.000` just means `< 1/reps` (not literally zero).
- Best-fit error is typically a more sensitive measure than hit-counts, because hit-counts can be inflated by many unrelated near-misses.

## Mode: medium

- W33 expressions scored: 60000
- Random reps: 10

### Best-fit comparison

Empirical p-value `p(best)` means: fraction of random base sets whose best-fit error is ≤ W33’s best-fit error.

| target | W33 best % error | random best % error quantiles (q05/q50/q95) | p(best) |
|---|---:|---|---:|
| alpha | 0.077917% | q05=0.0201901, q50=0.0619402, q95=0.140081 | 0.500 |
| higgs_over_z | 0.005020% | q05=0.00767248, q50=0.0419628, q95=0.13458 | 0.000 |
| omega_lambda | 0.001613% | q05=0.0201708, q50=0.0387877, q95=0.0776862 | 0.000 |
| cabibbo_deg | 0.009607% | q05=0, q50=0.00332155, q95=0.0274411 | 0.700 |

### Hit-count comparison (≤1%)

Empirical p-value `p(hits)` means: fraction of random base sets whose hit-count at ≤1% is ≥ W33’s hit-count.

| target | W33 hits ≤1% | random hits ≤1% quantiles (q05/q50/q95) | p(hits) |
|---|---:|---|---:|
| alpha | 7 | q05=7.9, q50=11.5, q95=20.5 | 1.000 |
| higgs_over_z | 29 | q05=23, q50=33.5, q95=58.25 | 0.800 |
| omega_lambda | 22 | q05=26, q50=28.5, q95=35.1 | 1.000 |
| cabibbo_deg | 62 | q05=52.8, q50=62, q95=182.45 | 0.500 |

### Hit-count comparison (≤0.1%)

| target | W33 hits ≤0.1% | random hits ≤0.1% quantiles (q05/q50/q95) | p(hits) |
|---|---:|---|---:|
| alpha | 1 | q05=0, q50=1, q95=3 | 0.700 |
| higgs_over_z | 4 | q05=0, q50=1, q95=8.3 | 0.200 |
| omega_lambda | 3 | q05=1, q50=3, q95=5 | 0.700 |
| cabibbo_deg | 8 | q05=4.9, q50=11, q95=23.65 | 0.700 |

Interpretation notes:

- With small `reps`, a reported p-value of `0.000` just means `< 1/reps` (not literally zero).
- Best-fit error is typically a more sensitive measure than hit-counts, because hit-counts can be inflated by many unrelated near-misses.

## Next steps (recommended)

- Increase replicates to tighten the p-values (e.g. `--reps 200`) and consider bumping `--max-pool` once runtime is acceptable.
- Add alternate null models: (1) uniform random ints from a single range, (2) ‘permuted W33’ where we keep magnitudes but shuffle values, (3) random sets conditioned on having similar gcd structure.

