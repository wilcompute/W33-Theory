# BT1116 — Spectral-action factorization and seed-independence boundary

BT1116 records the structural principle suggested by the parallel continuum commits and the attached Claude note: the dimensionless Standard-Model ratios already computed from the finite W33 triple are seed-independent, while dimensionful gravitational scales require the curved K3 seed.

## Product heat-kernel factorization

For an almost-commutative product

```text
M x F
```

with square

```text
D^2 = Delta_M tensor 1 + 1 tensor D_F^2
```

at the factorized level, the heat trace separates:

```text
Theta_{M x F}(t) = Tr exp(-tD^2) = Theta_M(t) Theta_F(t).
```

The finite factor has Taylor expansion

```text
Theta_F(t) = N_F - t Tr(D_F^2) + (t^2/2) Tr(D_F^4) - ...
```

so the product heat coefficients are convolutions of manifold coefficients and finite moments.

## Seed-independent outputs

All dimensionless bosonic ratios obtained from terms at a common heat-kernel order share the same manifold integral.  That shared seed factor cancels in the ratio.  Therefore the already-computed finite ratios are W33/F-determined:

```text
m_H^2/v^2 = 14/55
lambda_H = 7/55
a2/a0 finite prefactor = 14/3 = 2 Phi_6/q
a4/a2 finite prefactor = 55/7
```

These do not wait on the quantitative K3 spectral-action run.

## Seed-dependent outputs

The dimensionful gravitational scales live at different heat-kernel orders and carry different manifold integrals:

```text
cosmological scale ~ a0(M) ~ volume(M),
Einstein-Hilbert scale ~ a2(M) ~ integral_M R.
```

Thus physical `Lambda` and `1/G` require the curved seed geometry.  This explains why the remaining R3 computation is the quantitative K3 spectral-action computation rather than another finite-ratio derivation.

## Boundary theorem

The done/open split is:

```text
finite/F ratios: done, seed-independent;
gravity scales: open, seed-dependent K3 computation.
```

BT1116 does not compute the K3 values.  It proves why that computation is precisely the remaining continuum work.
