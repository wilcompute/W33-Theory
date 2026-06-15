# BT1118 — Weight-to-Yukawa map search

BT1118 searches for a non-naive map from reservoir generation weights to Yukawa or mass observables.

## The BT1113 obstruction

The naive identification

```text
sqrt(m_g) proportional to w_g = 1 + epsilon cos(theta + 2*pi*g/3)
```

gives

```text
Q = (sum w_g^2)/(sum w_g)^2 = 1/3 + epsilon^2/6.
```

Exact Koide `Q=2/3` requires `epsilon^2=2`.  Therefore a small positive reservoir-projector perturbation cannot be literally the square-root charged-lepton vector.

## Candidate maps

### Map A: phase-transfer Koide map

Use the reservoir weights only to supply the generation phase `theta`, while the Yukawa square-root vector uses the Koide radius independently:

```text
sqrt(y_g) = A * (1 + sqrt(2) cos(theta + 2*pi*g/3)).
```

This map preserves exact Koide by construction but decouples the projector perturbation amplitude `epsilon` from the mass/Yukawa amplitude `sqrt(2)`.

The reservoir data controls ordering/phase; the mass map supplies the non-small radius.

### Map B: exponential hierarchy map

Use

```text
y_g = y0 * exp(kappa cos(theta + 2*pi*g/3)).
```

This produces positive hierarchical Yukawas for large `kappa`, but it does not force exact Koide without an additional equation fixing `kappa`.

### Map C: projector-expectation map

Let Yukawa entries be expectation values of another operator `Y` against the generation projector:

```text
y_g = Tr(P_w E_g Y E_g)/Tr(E_g)
```

where `E_g` is the generation block.  This is the most W33-native form, but it requires an explicit Yukawa operator `Y` that has not yet been derived.

## Current best route

The best conservative route is Map A:

```text
reservoir weights -> phase/order data,
Koide radius sqrt(2) -> mass/Yukawa amplitude.
```

This avoids the BT1113 falsifier because it does not identify the small projector weights directly with masses.  It also keeps a testable link: the same phase `theta` must organize both reservoir generation splitting and the Koide/Yukawa phase ledger.

## Boundary

BT1118 does not fit masses.  It rejects the naive map, ranks three alternatives, and selects phase-transfer as the best next candidate to test against the repo's charged-lepton and Koide ledgers.
