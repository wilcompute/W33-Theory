# Pass 84 — W(3,3) and Q(4,3) are a Sunada–Gassmann pair

**Status: PASS** — witness `w33_pass84_sunada_gassmann.py` (8/8 checks), test
`tests/test_pass84_sunada_gassmann.py` (5/5). Self-contained on the committed Pass 73/76/82 spine.

Kac asked *"can you hear the shape of a drum?"*; Sunada built isospectral non-isometric manifolds
from Gassmann-equivalent subgroups; Perlis studied arithmetically equivalent number fields (same
Dedekind zeta). The cospectral, locally identical, non-isomorphic pair **W(3,3) / Q(4,3)** (Pass 76)
is the exact graph instance — and Passes 82/83 pin down precisely what you can and cannot hear.

## Verified directly
- **T1 — identical Ihara zeta.** N_m = Tr(Bᵐ) computed on *both* 480×480 Hashimoto operators agree
  for all m = 1..12 (960, 181440, …, 3138359764320). Same zeta ⇒ same primes, same RH, same
  functional equation.
- **T2 — identical spectral zeta.** ζ_L(s) = Σ_{λ>0} λ⁻ˢ is identical; special values
  **ζ_L(0) = n−1 = 39**, **ζ_L(−1) = 2m = 480**, and the regularized determinant
  **det′(L) = n·κ** — all the same for both.
- **T3 — same class number, different class group.** Both have class number
  **κ = 2⁸¹·5²³** (= #spanning trees), but the critical groups differ
  (K(W) = (ℤ/10)⁸⊕ℤ/40⊕(ℤ/160)¹⁴ vs K(Q) = (ℤ/2)⁶⊕(ℤ/10)⁸⊕ℤ/40⊕(ℤ/80)⁶⊕(ℤ/160)⁸, Pass 82) —
  the Gassmann phenomenon, where the arithmetic hears what the zeta cannot.

## The hearing hierarchy — "can you hear the shape of W(3,3)?"
| probe | verdict |
|---|---|
| adjacency / Ihara / Bartholdi spectrum | **DEAF** (identical) |
| spectral zeta special values | **DEAF** (identical) |
| local neighbourhood + μ-graph (Pass 76) | **DEAF** (both 4K₃ / 4K₁) |
| class number κ = spanning trees | **DEAF** (both 2⁸¹·5²³) |
| ovoid number α (Pass 77) | **HEARS** (7 vs 10) |
| critical group / class group (Pass 82) | **HEARS** (2-Sylow differs) |

So W(3,3) and Q(4,3) are isospectral in every zeta sense and identical in every local and
class-number sense; only a global geometric invariant (ovoids) and a global arithmetic invariant
(the critical group) distinguish them. This is the complete graph "you cannot hear the shape"
picture — and it names the phenomenon: a Sunada–Gassmann pair.

## Files
- `w33_pass84_sunada_gassmann.py`, `.json` — witness + certificate (8 checks).
- `tests/test_pass84_sunada_gassmann.py` — 5 assertions.
