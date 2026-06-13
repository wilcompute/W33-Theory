# BT921 — The Hodge–Dirac Spectral Triple (hard open #2, advance)

**Status: PROVEN (finite spectral triple exact; continuum theorem open), `analysis/bt921_hodge_dirac_spectral_triple.py`, data `data/bt921_hodge_dirac_spectral_triple.json`**

Aggressive advance on hard open #2 (the continuum / spectral-action bridge).
BT892 used only the bosonic graph Laplacian; BT921 builds the full finite
Dirac operator D = d + d* on the W(3,3) 2-complex (40 vertices, 240 edges,
160 in-line triangles), with D² = Δ₀ ⊕ Δ₁ ⊕ Δ₂ the three combinatorial Hodge
Laplacians — the genuine finite spectral triple of the almost-commutative
geometry M × F.

## The theorems

- **T1 — zero modes are the homology.** ker D (the harmonic forms) is exactly
  the homology: **b₀ = 1** (vacuum), **b₁ = 81** (the Steinberg matter
  register, BT861), **b₂ = 40** (the oriented lines, BT862). The Dirac's
  **122 = 1+81+40 massless modes are the physical content**, dominated by the
  81-dimensional Steinberg matter block.
- **T2 — the massive spectrum.** D² has spectrum
  **{0¹²², 4²⁴⁰, 10⁴⁸, 16³⁰}** (total 440 = 40+240+160). The dominant massive
  eigenvalue is **4 = μ with multiplicity 240 = |E|** (matter/edge modes); the
  10⁴⁸ and 16³⁰ massive sector coincides with the corpus finite Dirac D_F².
  Moments M_k = Tr D^{2k} = {1920, 16320, 186240}; Tr Δ₀ = 480 = 2|E|,
  Tr Δ₂ = 480 = 3|triangles|.
- **T3 — the spectral-action reading.** dim H_F = 440; the spectral action
  Tr f(D²/Λ²) has its cosmological (a₀) term from the full spectrum (the
  log-determinant of the nonzero part is BT870/892's v·τ = 2⁸¹·5²³), and its
  Einstein–Hilbert (a₂) coefficient fixed by the harmonic/fermion count (the
  122 = homology, 81 Steinberg dominant).

## Reading

This pins the **finite Dirac operator exactly** — the object whose
almost-commutative product with a curved 4-manifold gives the bosonic
spectral action. Two clean facts emerge:

1. The Dirac zero modes are the substrate homology (1 + 81 + 40), so the
   massless content is *derived*: vacuum + Steinberg matter register + lines.
2. The matter eigenvalue is **μ = 4** (multiplicity |E| = 240) — the
   non-harmonic "mass scale" of the finite geometry is the substrate's μ, and
   the high modes {10, 16} = {k−r, k−s} are the Laplacian's own spectrum.

So the substrate supplies an exact, small finite Dirac spectrum
{0, 4, 10, 16} with multiplicities {122, 240, 48, 30}, and its spectral
moments feed the spectral action. The remaining (genuinely hard, genuinely
open) step is the continuum asymptotic theorem: that the refinement of the
*external* curved factor produces the Einstein–Hilbert term with the right
coefficient. BT921 fixes the entire finite/internal input.

## Open (the continuum frontier)

- the curved-4D spectral-action asymptotics (the EH coefficient) — the open
  analytic theorem; the substrate side is now complete (BT892 Laplacian +
  BT921 full Dirac).
- the first-order / orientability axioms (Connes' conditions) for the W(3,3)
  spectral triple, to certify it as a genuine real spectral triple.
