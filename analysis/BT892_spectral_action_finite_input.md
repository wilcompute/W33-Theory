# BT892 — The Finite Spectral Input to the Continuum Bridge (#2)

**Status: PROVEN (finite data exact; continuum theorem remains open), `analysis/bt892_spectral_action_finite_input.py`, data `data/bt892_spectral_action_finite_input.json`**

The continuum bridge is the almost-commutative product
Δ_total = Δ_ext ⊗ 1 + 1 ⊗ D_F², with the heat trace factorizing as
Tr e^{−tΔ_total} = Tr e^{−tΔ_ext} · Tr e^{−tD_F²}. The hard open theorem is
that the curved-4D refinement yields the Einstein–Hilbert action. BT892 does
**not** solve that — it pins the **exact finite internal input** the spectral
action consumes.

## The theorems

- **T1:** the W(3,3) Laplacian spectrum is {0¹, 10²⁴, 16¹⁵}, with heat-kernel
  moments M_p = Σ λ^p: **M₀ = v = 40** ("volume" / a₀), **M₁ = Tr L = 480 =
  2|E|** (the directed-edge / Hashimoto carrier count), M₂ = 6240, M₃ = 85440.
- **T2:** the spectral-zeta log-determinant is
  −ζ_L′(0) = log(∏ nonzero eigenvalues) = 24 ln10 + 15 ln16 = **96.851**, and
  exp of this is exactly **v·τ = 40·2⁸¹·5²³ = 10²⁴·16¹⁵** (rel. err 4e-15) —
  the *same number* as BT870's spanning-tree gravity. The partition-function
  (a₀-type) coefficient of the spectral action **is** the discrete-gravity τ.
- **T3:** the product heat-trace factorization holds on explicit finite data,
  with the substrate supplying the finite factor
  **Z_fin(t) = 1 + 24 e^{−10t} + 15 e^{−16t}**; any curved external seed
  Z_ext(t) multiplies it. The continuum theorem (product → EH action) remains
  the open frontier.

## Reading

This nails down what the substrate contributes to the spectral action — its
finite spectral data is exact and small: a Laplacian with three eigenvalues
{0, 10, 16} of multiplicities {1, 24, 15}, heat moments {40, 480, 6240, …},
and a log-determinant that equals BT870's gravitational partition function.
The first two moments are the substrate's own integers (v = 40 and 2|E| = 480),
so the leading spectral-action coefficients are not free — they are W(3,3)
graph invariants. The continuum geometry enters only through the *external*
curved factor Z_ext(t); the substrate is the fixed internal Dirac data. The
remaining (genuinely hard, genuinely open) step is the asymptotic theorem that
the refinement tower of Z_ext produces the Einstein–Hilbert term with the
right coefficient — the analytic frontier, not a finite computation.

## Open (the continuum frontier)

- the curved-4D Weyl-law / spectral-action asymptotics (the EH coefficient) —
  the established hard open theorem;
- the finite Dirac operator D_F (not just D_F²) and its first-order condition
  on the W(3,3) almost-commutative geometry.
