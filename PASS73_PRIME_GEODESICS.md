# Pass 73 — The Prime Geodesic Spectrum of W(3,3)

**Status: PASS** (witness `w33_pass73_prime_geodesics.py`, test `tests/test_pass73_prime_geodesics.py`, 8/8; paper compiles clean with tectonic.)

## What this pass does

Pass 71 (Track E) computed the Ihara-zeta **poles** of the W(3,3) collinearity graph and
confirmed the graph Riemann Hypothesis. The paper's *Prime-Geodesic Expansion* section stated the
Euler product and the closed-walk counts N_n, but stopped at the asymptotic `N_n ~ 11^n`. This
pass builds the **non-backtracking (Hashimoto) operator** B (480×480) explicitly and extracts the
number-theoretic content the paper was missing — and, in doing so, **corrects a factor-2 error**.

## The correction (rigorous, three independent confirmations)

The paper's *Prime-Geodesic Expansion* claimed the length-3 prime count is
`π_G(3) = vkλ/6 = 160`. That is the **undirected triangle count T**, a different quantity.
A length-3 Ihara prime is an **oriented** triangle; each of the T = 160 undirected triangles is
traversed in two inequivalent cyclic orientations, so

> **π_G(3) = 2T = 320.**

This is forced by the paper's own Proposition on N_n: `N_3 = tr(B³) = 960`, and the exact Ihara
identity `N_m = Σ_{d|m} d·π_G(d)` gives `N_3 = 3·π_G(3) ⟹ π_G(3) = 320`. Confirmed three ways:
1. Möbius inversion of `N_m = tr(B^m)` computed on the explicit 480×480 matrix → π_G(3) = 320.
2. `2 × (triangle count)` = 2 × 160 = 320.
3. Hand-count of based closed walks: each oriented triangle returns at each of its 3 base edges,
   so tr(B³) = 3 × 2T = 960, i.e. π_G(3) = 320.

## New results (absent from the paper)

- **Full prime-counting function** π_G(m) for m = 1..12 via `m·π_G(m) = Σ_{d|m} μ(m/d) N_d`,
  each a positive integer; graph PNT ratio `π_G(m)·m / 11^m → 1` (e.g. 0.721, 0.951, 1.127,
  1.026, 0.984, 0.998, 1.001, …, 1.000 at m=12).
- **Quantitative Ramanujan error bound** (graph RH made effective):
  `|N_m − 11^m − 201 − 200(−1)^m| ≤ 78·11^(m/2)`, with `78 = 2(f+g) = 2(24+15)`, verified for all
  tested m. The exponent m/2 is the square-root-cancellation (RH) rate — the optimal
  periodic-orbit fluctuation. W(3,3) saturates it.
- **Bass spectrum** of B confirmed: `{11,1} ∪ {1±i√10}^24 ∪ {−2±i√7}^15 ∪ {±1}^200`, all
  non-trivial eigenvalues of modulus exactly √11.
- **Mixing:** non-backtracking spectral gap `11 − √11 ≈ 7.683`; Perron = k−1 = 11 with second
  modulus √11 (Ramanujan-optimal), the exact rate at which Holonet periodic routes equidistribute.

## Physical reading

Closed non-backtracking routes on W(3,3) are the **periodic orbits of the Holonet router**. Their
count obeys the graph prime number theorem π_G(m) ~ 11^m/m, and the Ramanujan property bounds the
fluctuation by the tightest possible (RH) error — a hard, effective statement, not an asymptotic.

## Files
- `w33_pass73_prime_geodesics.py` — witness (self-contained: builds W(3,3) from the symplectic
  form, the Hashimoto operator, the prime counts, and all four theorems).
- `w33_pass73_prime_geodesics.json` — machine-readable certificate.
- `tests/test_pass73_prime_geodesics.py` — 8 regression assertions.
- `w33_paper.tex` — *Prime-Geodesic Expansion* section corrected and extended (π_G(3)=320,
  full π_G(m) table, Proposition: Quantitative Ramanujan Error Bound).
