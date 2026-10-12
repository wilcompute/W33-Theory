# Pass 11934: the radiative + residual-ℤ₃ principle, applied uniformly, fails in the charged sectors

Producer: `analysis/w33_pass11934_uniform_radiative_z3_fails.py`
Certificate: `data/w33_pass11934_uniform_radiative_z3_fails.json`
Regression: `tests/test_w33_pass11934.py`
Track: Claude. This is a consistency check on Pass 11933, recorded to prevent an over-read.

## Test

Setting: the Eisenstein point with the A₂ dual pair. For every Yukawa channel I took the mediator's radiative top space
(the Gram top eigenspace) and its residual-ℤ₃-symmetric directions:

| channel | mediator | top-space dim | symmetric directions | spectrum at ω | nearby |
|---|---|---|---|---|---|
| up (10·10) | H_u, flux 2A₂ | 3 (charges 0, 2) | 1 + 2 | (1, 1, 0) | top = charm |
| down / charged leptons (10·5̄) | H_d, flux 4·1 | 1 (charge 2) | 1 | (1, 1, 0) | (1, 1 − O(ε²), 0): m_b = m_s, m_τ = m_μ, lightest exactly massless |
| Weinberg (L·L) | flux 2A₂′ | 3 (charges 0, 2) | 1 + 2 | (1, 1, 0) | inverted ordering (Pass 11933) |

## Reading

**What the uniform principle predicts.** Applied to every sector, the principle gives the theta-zero pattern everywhere.

**Where it fails.** Three charged sectors contradict the data:

| ratio | measured | predicted |
|---|---|---|
| m_c/m_t | ≈ 4·10⁻³ | 1 |
| m_s/m_b | ≈ 0.02 | ≈ 1 |
| m_μ/m_τ | ≈ 0.06 | ≈ 1 |

**What follows for Pass 11933.** Its inverted-ordering neutrino prediction is **not** a consequence of a universal rule. As
a universal rule, the principle is excluded. The prediction survives only if the neutrino mediator has dynamics specific
to it, for example a type-II triplet whose potential differs from the Higgs doublets'. The note to Pass 11933 is amended
accordingly.
