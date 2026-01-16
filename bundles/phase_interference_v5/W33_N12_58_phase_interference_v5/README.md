W33 ↔ N12_58 phase interference optimization (v5)

This bundle builds on the v3 phase-aware predicate and treats each 2T cycle as a 'transport loop' in the W33 four-center (±3) triad graph.

For each 2T cycle, we compute a complex partition function:

    Z_cycle(λ) = Σ_{closed walks} Π_i [ exp(2π i hol(triad_i)/12) * exp(-λ * cover12(triad_i)) ]

Where:
- hol(triad_i) ∈ {3, 9} (i.e., ±3 mod 12) comes from the ray realization.
- cover12(triad_i) ∈ {0, 1} indicates whether the triad covers all 12 vertex symbols (a 'trivial satisfier').
- λ controls how strongly we bias toward structurally constrained (non-cover12) steps.

Time-modified / delta-twisted interference:
We introduce a phase factor f(delta) ∈ {±1, ±i} per N12 flip-step delta ∈ {0, 2, 4, 6} and maximize constructive interference:

    maximize  | Σ_cycle  Z_cycle(λ) * Π_{steps in cycle} f(delta_step) |

The file best_delta_phase_maps_by_lambda.json lists the best f(delta) found (brute force over 4^4=256 maps) for λ ∈ {0.0, 0.2, 0.5, 1.0}.

Key outputs:
- per_cycle_partition_functions_and_adjusted.csv : raw Z_cycle and adjusted Z_cycle under the best f(delta), for each λ and each cycle.
- best_delta_phase_maps_by_lambda.json : best interference score and the maximizing f(delta) for each λ.

Interpretation:
The optimal f(delta) is a concrete 'time modification' that makes the five holonomy cycles phase-cohere as strongly as possible, given your v3 transport constraints.

How to reproduce:
Run recompute_v5_phase_interference.py (included) in the same environment where the v3 bundle is present at:
  /mnt/data/W33_N12_58_phase_aware_bundle_v3_20260112.zip
