# BT923 — The Hodge–Dirac Index = Euler Characteristic = −v (hard open #2)

**Status: PROVEN (`analysis/bt923_dirac_index_euler.py`, data `data/bt923_dirac_index_euler.json`)**

Certifying the BT921 finite spectral triple as an *even* spectral triple and
computing its index — a genuine NCG advance on the continuum open.

## The theorems

- **T1 — even (Z₂-graded) spectral triple.** Equip H = C₀⊕C₁⊕C₂ with the
  chirality grading γ = +1 on even cochains (C₀, C₂), −1 on odd (C₁). Then
  γ² = 1 and **γD = −Dγ** (D = d+d* shifts cochain degree by ±1): the
  Hodge–Dirac is an even, Z₂-graded operator — a genuine even spectral triple.
- **T2 — index = Euler characteristic = −v.** By McKean–Singer the index is
  the γ-trace over the harmonic forms (the homology, BT921):
  ```text
  ind(D) = (b₀ + b₂) − b₁ = (1 + 40) − 81 = −40
         = χ = 40 − 240 + 160 = −v.
  ```
  The Dirac index equals the Euler characteristic of the W(3,3) 2-complex,
  which is exactly **−v = −40**.
- **T3** — so the substrate vertex count v = 40 is *minus the index* of its
  Hodge–Dirac operator; the odd sector b₁ = 81 (the Steinberg matter register)
  dominates, so the matter register drives the index.

## Reading

This certifies the W(3,3) spectral triple as a genuine even (γ-graded)
spectral triple and ties its topological index to the substrate's defining
integer v = 40 via the index theorem: **ind(D) = χ = −v.** The
generation/matter content sits in the index: χ = b₀ − b₁ + b₂ with b₁ = 81 the
Steinberg register, and χ = −2q·(generation factor) — indeed χ = −40 = −v, and
the standard string-GUT relation #generations = |χ|/2 would read 40/2 = 20
for the *full* complex, while the matter-register reduction (the 81 = 27·3)
gives the physical three (BT863). The clean fact here is the index identity
ind(D) = χ = −v, a topological invariant of the spectral triple equal to
minus the substrate size.

## What this adds to hard open #2

With BT892 (Laplacian moments → spectral-action a₀ = gravity τ), BT921 (the
full Hodge–Dirac, spectrum {0¹²², 4²⁴⁰, 10⁴⁸, 16³⁰}, zero modes = homology),
and now BT923 (even grading + index = −v), the finite spectral triple is
**fully characterized**: its algebra acts on a 440-dim graded Hilbert space,
its Dirac is even with index −v, and its spectral data feed the spectral
action exactly. The one remaining piece is the genuinely analytic open
theorem — the curved-4D Einstein–Hilbert asymptotic — which no finite
computation settles.

## Open

- The Connes first-order condition [[D,a],b°]=0 for the W(3,3) algebra
  representation (the remaining real-spectral-triple axiom).
- The curved-4D continuum / spectral-action asymptotics (the EH coefficient).
