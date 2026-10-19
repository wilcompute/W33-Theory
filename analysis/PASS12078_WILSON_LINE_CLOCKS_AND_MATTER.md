# Pass 12078: clocks as Wilson lines

Claude track. Builds on 12056–12057, 12071 and 12077.

## Model

Commuting order-2 holonomies on Tᵏ give a one-loop potential V = −(N_B − N_F) Σ_α S_k(|ε_α|), where ε_α is the
parity pattern of the root α. Only root-pattern counts and the boson–fermion imbalance matter.

## Results

| k | Comparison | Bosons choose | Fermions choose |
|---|---|---|---|
| 1 | clock vs split holonomy | clock: V_B = −62ζ(5) | split: V_B = 0 exactly |
| 2 | two clocks | the Klein pair (e₆ + u(1)²) | the non-Klein pair |
| 3 | three clocks | the Klein triple | type (32, 96, 96, 16) |

## Reading

Bosonic loops choose one time, then a Klein group of clocks with e₆ + u(1)². Fermion domination chooses the opposite.
This mirrors 12056–12057.

## Scope

- The trivial holonomy is always lowest for bosons; these statements compare forced, non-trivial holonomies.
- Equal radii; lattice sums truncated at |n_i| ≤ 60.

Producer: `analysis/w33_pass12078_wilson_line_clocks_and_matter.py`.
