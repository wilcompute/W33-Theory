# Part MCCLXXVI — Cyclotomic Genus Reciprocal Sheets

This part continues the MCCLXVI-MCCLXXV cyclotomic spectral algebra packet after
the corrected MCCLXVIII sign convention.

## Theorem

The W(3,3) genus oscillator is not a single positive-temperature equilibrium.
It is a reciprocal two-sheet system:

```text
Omega_live(beta) = 21 exp(-10 beta) - 6 exp(-16 beta)
Omega_dual(beta) = 21 exp(-16 beta) - 6 exp(-10 beta)
```

The live heat-trace sheet has its zero at

```text
beta_- = -log(7/2)/6,
```

while the dual energy-reversed sheet has its zero at

```text
beta_+ = +log(7/2)/6.
```

In the spectral variable `x = exp(6 beta)`, the roots are exactly reciprocal:

```text
x_- = 2/7 = r/Phi6
x_+ = 7/2 = Phi6/r
x_- x_+ = 1
```

Thus the positive root belongs to the dual sheet, not the live sheet.

## q=3 Forcing

For the W(q) parameter family,

```text
E_low  = k-r      = q^2+1
E_high = k+|s|    = (q+1)^2
gap    = E_high-E_low = 2q.
```

The gap is the factorial clock exactly at the nontrivial substrate point:

```text
2q = q!  iff  q=3  among q >= 3.
```

The genus ratio also locks to the cyclotomic ratio only at q=3.  With

```text
g  = q(q+2)
g1 = (q^3+g)/2
g2 = (q^3-g)/2
```

the equality

```text
g1/g2 = Phi6(q)/r(q)
```

has numerator

```text
q^3(3-q),
```

so the nonzero positive solution is q=3.

## The Now-Derivative Lock

At the self-entangled center `beta=0`, both sheets agree:

```text
Omega_live(0) = Omega_dual(0) = 15 = g
Z(0) = 1+24+15 = 40 = v.
```

But their first derivatives split into a substrate center plus a q-fourth
power:

```text
dOmega_live/d beta |0 = -114
dOmega_dual/d beta |0 = -276
center                 = -195 = -Phi3*g
half-split             = 81   = q^4
```

The dual derivative is exactly the Pisano period of the fine-structure
identity-sheet shadow:

```text
-dOmega_dual/d beta |0 = 276 = pi(137).
```

So the reciprocal future sheet carries the `137` clock not as a fitted
constant, but as the instantaneous derivative of the corrected genus oscillator
at now.

## Verification

Run:

```bash
python3 analysis/w33_cyclotomic_genus_reciprocal_sheets.py
```

The verifier checks the reciprocal roots, q=3 uniqueness, cyclotomic inputs,
and the now-derivative/Pisano lock.
