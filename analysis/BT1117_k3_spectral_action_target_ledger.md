# BT1117 — K3 spectral-action target ledger

BT1117 turns the R3/continuum remainder into an explicit compute target.

## Done/open boundary

BT1116 proves the structural split:

```text
finite/F ratios: seed-independent and already determined by W(3,3),
gravity scales: seed-dependent and require the curved K3 geometry.
```

Thus the K3 compute lane should not re-derive finite ratios such as `14/55` or `7/55`.  It should output the geometric coefficients that multiply the finite W33 moments.

## Input object

The input is a chosen metric or discrete-to-smooth approximation on the K3 seed:

```text
(K3, g_h)
```

where `g_h` may be the refined edgewise/Regge metric, a smoothed surrogate, or a limiting Ricci-flat K3 metric.  The computation must state which convention it uses.

## Required geometric outputs

For dimension four, the target heat-kernel ledger is:

```text
A0(K3,g_h) = integral_K3 dvol_g
A2(K3,g_h) = integral_K3 R_g dvol_g
A4(K3,g_h) = integral_K3 Q4(g) dvol_g
```

where `Q4(g)` is the convention-dependent curvature-square density appropriate to the chosen Laplace/Dirac operator.

A convention-safe output must therefore include:

```text
1. operator convention: scalar Laplacian, spin Dirac square, or full AC Dirac square;
2. volume normalization;
3. scalar curvature integral;
4. curvature-square integral(s): |Riem|^2, |Ric|^2, R^2 or equivalent Weyl/Euler/signature components;
5. boundary/defect terms if the discrete seed is not yet a closed smooth manifold;
6. convergence/refinement parameter h.
```

## Topological checks

For a closed smooth K3 target, the compute should verify the topological checks:

```text
chi(K3) = 24,
sigma(K3) = -16,
b2 = 22,
intersection signature = (3,19).
```

For curvature integrals, the Gauss--Bonnet and signature formulas must hold in the stated normalization.  These checks are more reliable than raw curvature numbers because curvature norm conventions vary by factors of 2 or 4.

## Finite W33 prefactors to attach

The finite side supplies seed-independent prefactors, including:

```text
m_H^2/v^2 = 14/55,
lambda_H = 7/55,
finite a2/a0 prefactor = 14/3 = 2 Phi_6/q,
finite a4/a2 prefactor = 55/7,
Tr(D_F^2) ledger entries from the finite triple.
```

The K3 computation supplies the geometric multipliers.  The product spectral-action coefficients are convolutions of the form

```text
a_n(M x F) = sum_j a_{n-2j}(M) * finite_moment_j(F)
```

with convention-dependent signs and factorials fixed by the chosen heat-trace expansion.

## Minimal deliverable table

The compute lane should output a table with columns:

```text
quantity, symbol, numerical value, normalization, convergence h, finite W33 multiplier, physical role.
```

Rows:

```text
volume term, A0, ..., ..., N_F or finite trace, cosmological scale;
Einstein term, A2, ..., ..., Tr(D_F^2) combination, Newton scale;
curvature-square term, A4, ..., ..., Tr(D_F^4) combination, higher-curvature/gravity correction;
finite SM ratios, 14/55 and 7/55, exact, seed-independent, none, dimensionless matter couplings.
```

## Boundary

BT1117 does not compute the K3 numbers.  It defines the exact target ledger so the compute lane cannot drift into re-proving finite ratios and cannot report unnormalized curvature values without the convention data needed to interpret them.
