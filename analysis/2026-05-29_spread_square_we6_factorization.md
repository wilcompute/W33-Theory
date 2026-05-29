# Symplectic Spread-Square / W(E6) Factorization Theorem

Date: 2026-05-29

This theorem is the payoff from reading the live index / complete-theory surface harder.

The live documentation points to two exact audits as the current finite-geometric spine:

```text
scripts/w33_projective_affine_shell_audit.py
scripts/w33_symplectic_spread_frame_audit.py
```

The projective/affine shell audit states that the 40 PG(3,3) points, the 40 projective two-qutrit Pauli classes, and the repo W33 vertex set are the same object; it also states that each anchor has a PG(2,3) hyperplane of size 13 and an AG(3,3) affine complement of size 27.

The spread audit states that W(3,3) has exactly 36 symplectic spreads; each spread partitions the 40 points into 10 isotropic lines; every isotropic line lies in 9 spreads; and relative to any anchor, the 36 spreads split as 4 anchor-line sectors of size 9.

The new observation is that this rewrites the previous factorization

```text
51840 = 40 * 16 * 81
```

as

```text
51840 = 40 * 36^2.
```

## The square identity

From the earlier Q4/qutrit phase bridge:

```text
16 = |Q4 vertices|
81 = |F3^4| = 3^4
```

So:

```text
16 * 81 = 1296.
```

But the spread audit gives:

```text
36 = 4 * 9.
```

Therefore:

```text
16 * 81 = 4^2 * 9^2 = (4*9)^2 = 36^2.
```

Thus:

```text
51840 = 40 * 16 * 81 = 40 * 36^2.
```

## Symplectic group order

The same number is also the order of the linear symplectic group:

```text
|Sp(4,3)| = 3^4(3^4 - 1)(3^2 - 1) = 51840.
```

The projective action quotients by the central ±I, giving

```text
|PSp(4,3)| = 25920.
```

So the W(E6) order is naturally the full linear symplectic action on the four-mode qutrit phase space.

## Incidence counts

The verifier checks:

```text
W33 points = 40
isotropic lines = 40
points per isotropic line = 4
spreads = 36
lines per spread = 10
spreads per line = 9
```

The minimal X-ray count is the W33 point-line flag count:

```text
X_min rays = 160 = 40 * 4.
```

The spread-line incidence count double-counts as:

```text
36 spreads * 10 lines/spread = 40 lines * 9 spreads/line = 360.
```

The point-line-spread triple count is:

```text
360 * 4 = 1440.
```

Equivalently:

```text
160 point-line flags * 9 spreads/line = 1440.
```

or

```text
36 spreads * 40 points/spread = 1440.
```

Then:

```text
36 * 1440 = 51840.
```

## Interpretation

The earlier factorization was:

```text
51840 = 40 * 16 * 81.
```

The new reading is:

```text
40 = symplectic/projective W33 anchor
16 * 81 = Q4 router states * F3^4 phase states
        = 36^2
```

So:

```text
36 = complete two-qutrit stabilizer/MUB spread-frame choice.
```

and

```text
36^2 = ordered source-target spread-frame transport packet per anchor.
```

Therefore:

```text
|W(E6)| = W33 anchors * ordered spread-frame transport packets.
```

or:

```text
|W(E6)| = 40 * 36^2.
```

## Why this matters

The Q4 router and F3^4 phase factors are not arbitrary independent factors. Together they equal the square of the exact symplectic spread-frame count already present in W(3,3):

```text
Q4 router * qutrit phase space = spread-frame source * spread-frame target.
```

This links three previously separate readings:

```text
Q4/Cl4/D8 router layer: 16
F3^4 qutrit phase layer: 81
W(3,3) complete stabilizer/MUB spread layer: 36
```

by the exact identity:

```text
16 * 81 = 36^2.
```

## Compressed theorem

```text
W(3,3) has 40 symplectic anchors and 36 complete spread/MUB frames. The product of the Q4 router count and the four-mode qutrit phase-space count is exactly 36^2. Hence the Weyl-E6/symplectic order 51840 can be read equivalently as 40*16*81 or as 40*36^2. This means the router-phase packet is an ordered pair of complete two-qutrit stabilizer spread frames over a chosen W33 anchor.
```

## Honest boundary

This proves the spread-square factorization and its finite incidence counts. The next hard test is to compare the actual group action of Sp(4,3) on ordered spread pairs and anchors with the repo's W(E6) / minimal logical phase-frame action, rather than only matching the group order.
