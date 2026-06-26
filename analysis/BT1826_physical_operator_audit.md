# BT1826 physical operator audit

BT1818 labeled the hidden quartet as

```text
00 -> I
01 -> X
10 -> Z
11 -> XZ
```

BT1826 separates what is exact from what is interpretive.

## Claim tiers

### Tier 1: exact local algebra

The quartet is exactly a four-state `F2^2` square.  The six edges are the six unordered pairs of four states, and the observed defect edge is `00 -> 11`.  In this local binary square, the difference label is `11`, which is naturally written as `XZ`.

Safe statement:

```text
The hidden quartet is an F2^2 local fibre, and the observed edge has difference 11 = XZ.
```

### Tier 2: D4 glue-code reading

The same four-state square is structurally compatible with the discriminant/glue quotient of the D4 lattice, where the four cosets are usually read as a `Z2 x Z2` quartet.  This supports the D4/GKP language, but it is still a structural identification unless the tuple rows provide a canonical map into physical displacement classes.

Safe statement:

```text
The quartet has the same Z2 x Z2 shape as the D4 glue quotient, so the D4-glue reading is structural.
```

### Tier 3: GKP coset / displacement reading

The labels `X`, `Z`, and `XZ` can be read as position, momentum, and both-quadrature half-shifts in a local GKP-like square.  This is the right engineering picture for the photonic/topological-code narrative, but it should be called an interpretation until the physical encoding map is explicitly specified.

Safe statement:

```text
In the GKP reading, the observed 00 -> 11 edge is a both-quadrature half-shift.
```

### Tier 4: physical BT1781 operator claim

This is not yet established.  The true tuple lists have not been materialized, so we cannot claim that the BT1781 data canonically names the quartet states as physical `I,X,Z,XZ` operators.

Unsafe statement:

```text
The real BT1781 tuples prove that the defect is physically the XZ Pauli operator.
```

Replace with:

```text
The current model predicts that true BT1781 tuple materialization should identify the defect with an oriented XZ-type quartet edge.
```

## Recommended wording

Use:

```text
The W(E6) stabilizer selects a six-edge quartet slice.  We model the hidden quartet as a local F2^2/D4-glue square with Pauli labels I,X,Z,XZ.  In that model the observed edge is the XZ diagonal, giving the correction T010:-2, T210:-2, T222:+2.  The physical GKP/displacement interpretation remains a claim to be tested by the tuple-list harness.
```

Avoid:

```text
W(E6) proves the physical GKP XZ displacement.
```

## Bottom line

```text
Exact: F2^2 quartet and XZ difference label.
Structural: D4 glue quotient reading.
Engineering: GKP both-quadrature half-shift reading.
Pending: physical operator realization from true BT1781 tuple rows.
```
