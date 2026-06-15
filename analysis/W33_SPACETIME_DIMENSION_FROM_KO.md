# Why spacetime is 4-dimensional, derived from W(3,3)'s KO-dimension

**Status: derivation (upgrades the dimensional-unification conjecture). The
spacetime dimension `4` — the one input the almost-commutative framing took
from observation — is forced by W(3,3).** Witness
`analysis/w33_spacetime_dimension_from_KO.py`, data
`data/w33_spacetime_dimension_from_KO.json`.

## The derivation

Two established facts and two standard NCG identities:

1. **KO-dim(F) = 6** for the finite `W(3,3)` spectral triple. The corpus
   verifies the real-structure signs `J²=+1, JD=+DJ, Jγ=−γJ`, i.e. the sign
   triple `(ε,ε',ε'') = (+,+,−)`, which is exactly KO-dimension `6` in the
   8-periodic KO table. (And `6 = 2q`, `q=3`.)
2. **Connes–Barrett:** to solve the fermion-doubling problem and admit the
   Euclidean fermionic (Pfaffian) functional integral, the **total** spectral
   triple `M × F` must have **KO-dimension ≡ 2 (mod 8)**.
3. KO-dimension is **additive** under product: `KO(M×F) = KO(M)+KO(F) (mod 8)`.
4. For a **spin manifold** `M`, KO-dimension `≡` metric dimension `(mod 8)`.

Therefore
```text
KO(M) = KO(total) − KO(F) = 2 − 6 = −4 ≡ 4 (mod 8),
dim(M) ≡ KO(M) ≡ 4 (mod 8)  ⟹  dim(spacetime) = 4  (minimal solution).
```

So **four-dimensional spacetime is forced by W(3,3)**: its finite triple has
KO-dimension `6 = 2q`, and the fermion-doubling constraint then leaves only
`dim M ≡ 4 (mod 8)`, whose minimal (physical) value is the observed `4`.

## Why this is the crux (KO ≠ metric dimension)

The derivation works precisely because, in NCG, **KO-dimension and metric
dimension are independent** (Connes–Barrett). That is what lets the finite
`F = W(3,3)` be *metrically* zero-dimensional yet carry KO-dimension `6`, and it
is the same independence that the SM finite space exploits. The metric (Weyl-law)
dimension of `M` is `4`; the KO-dimensions add to give the global `2 (mod 8)`
required for the functional integral.

## What it closes

The almost-commutative framing `M⁴ × F` previously took the `4` of `M⁴` from
observation. It is now **derived**: given `KO(F)=6` (a W(3,3) invariant `= 2q`)
and the Connes–Barrett constraint, spacetime *must* be 4-dimensional. The "why
4D" question reduces to "why `q=3`" (already answered by the spectral-action
`(q−3)(3q−1)` selection and the `q!=2q` master equation). Combined with the
two-continua result — the metric continuum is `K3` (`χ=24=f`), the symplectic
continuum is the oscillator rep — the substrate now fixes both *that* spacetime
is 4-dimensional and *which* curved seed (`K3`) realizes it, leaving only the
quantitative spectral-action computation.

## Honest scope

A derivation within the established NCG framework: it uses the corpus-verified
`KO(F)=6`, the standard Connes–Barrett total-KO `≡ 2 (mod 8)` constraint, and
KO additivity/spin-manifold identities. The residual choices are (i) minimality
(`4` rather than `12, 20, …`, all `≡ 4 mod 8`), resolved by physicality, and
(ii) that `M` be a spin manifold (assumed throughout the AC framework). It does
not by itself construct `M`; it fixes its dimension.

## Sources

- A. Connes, *Noncommutative geometry and the standard model with neutrino
  mixing*, [hep-th/0608226](https://arxiv.org/abs/hep-th/0608226) — KO-dim 6
  finite space.
- J. Barrett, *A Lorentzian version of the non-commutative geometry of the
  standard model* — the fermion-doubling resolution / total KO-dimension.
- *On the uniqueness of Barrett's solution…*,
  [arXiv:1903.04769](https://arxiv.org/abs/1903.04769).
