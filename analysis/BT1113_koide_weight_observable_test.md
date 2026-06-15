# BT1113 — Koide-weight observable test

BT1113 turns the BT1110 Koide-style generation-weight family into explicit observables.

## Weight family

Use

```text
w_g(theta,epsilon) = 1 + epsilon cos(theta + 2*pi*g/3),  g=0,1,2.
```

The first-order perturbation is traceless:

```text
sum_g (w_g - 1) = 0.
```

## Observable ratios

The reservoir projector depends on the rank-one generation matrix

```text
M_w = w w^T / (w.w).
```

The directly testable generation observables are therefore the normalized weights

```text
p_g = w_g^2 / (w0^2+w1^2+w2^2),
```

and ratios

```text
R_ij = w_i^2 / w_j^2.
```

These are the quantities to compare against any charged-lepton/Yukawa/generation ledger, because the projector sees weights quadratically.

## Koide-style phase anchor

For a Koide mass triple one often writes square-root masses as a phase-spaced triple.  The W33-compatible version is not yet a mass theorem; it is the ansatz

```text
sqrt(m_g) proportional to w_g(theta,epsilon).
```

Then the Koide ratio is

```text
Q = (sum_g w_g^2) / (sum_g w_g)^2.
```

Because `sum_g w_g = 3`, while

```text
sum_g w_g^2 = 3 + (3/2) epsilon^2,
```

we obtain

```text
Q = 1/3 + epsilon^2/6.
```

Thus exact Koide `Q=2/3` would require

```text
epsilon^2 = 2,
```

which violates the sufficient positivity bound `|epsilon|<1` for the simple positive-weight perturbation.  Therefore the positive reservoir-weight ansatz cannot literally be the square-root charged-lepton mass vector at exact Koide; it must either be a small perturbation, a normalized projection of a larger phase vector, or use a different physical observable.

## Conservative conclusion

BT1113 rules out overclaiming: the reservoir weights are a controlled generation-breaking knob, not yet the charged-lepton mass formula.  They can be compared to mass/Yukawa ledgers through `p_g` or `R_ij`, but exact Koide requires an additional map beyond positive first-order reservoir weights.

## Boundary

No charged-lepton masses are fitted here.  This is a structural observable test and a falsifier for the naive identification `w_g^2 proportional to m_g` at exact Koide.
