# Passes 9185–9196 — Golay/Tetracode Glue Bifurcation

## Status

**Machine-verified.** Canonical executable witness:
`analysis/w33_pass9185_9196_golay_tetracode_glue_bifurcation.py`.
Frozen result:
`data/PART_W33_PASS9185_9196_GOLAY_TETRACODE_GLUE_BIFURCATION.json`.

This is the collision-free rehome of the theorem first developed under the superseded 9041–9052 label. The mathematics is unchanged.

## Common A2^12 substrate

Passes 9173–9184 identify the 72 quotient-zero roots of the `E6^4` W33 carrier as a full-rank `A2^12` root subsystem. This lets `N(E6^4)` and `N(A2^12)` be compared over the same discriminant space `(A2^*/A2)^12 ~= F_3^12`.

Both are index `3^6=729` unimodular overlattices of an `A2^12` root lattice, but the selecting self-dual ternary `[12,6]` codes are different.

For the `A2^12` Niemeier lattice:

`C_G = [12,6,6]_3`,

`W_G(y) = 1 + 264 y^6 + 440 y^9 + 24 y^12`.

There are no weight-three words. Since a nonzero A2 discriminant class has minimum norm `2/3`, Golay glue has minimum added norm at least `6*(2/3)=4`, so it adds no roots and the root system remains `A2^12` with 72 roots.

For `N(E6^4)` relative to the quotient-selected `A2^12` subsystem:

`C_E = [12,6,3]_3`,

`W_E(y) = 1 + 8 y^3 + 240 y^6 + 464 y^9 + 16 y^12`.

The eight weight-three words are four nonzero-scalar pairs on exactly four disjoint supports:

`{0,1,2}`, `{3,4,5}`, `{6,7,8}`, `{9,10,11}`.

Their four projective directions span a dimension-four local extension subcode. Each support performs one `A2^3 -> E6` extension. Quotienting by these four local directions leaves the self-dual tetracode

`[4,2,3]_3`,

with weight enumerator `1+8y^3`.

## Root-count mechanism

Each nonzero A2 discriminant coordinate has three minimum representatives. A weight-three glue word therefore contributes

`3^3 = 27`

norm-two vectors. Hence

`72 + 8*27 = 288`,

the exact `E6^4` root count.

The eight words occur as four `+/-` pairs, so each of the four line channels contributes

`2*27 = 54`

visible roots, exactly matching the four-point W33 root shadow measured in Passes 9173–9184.

Thus the line shadow is not an unexplained multiplicity: it is the image of the four disjoint weight-three glue supports. The remaining two dimensions of the glue are the global tetracode tying the four E6 components together.

## Evidence boundary

The classical ingredients are the ternary-Golay construction of `N(A2^12)`, the tetracode construction of `N(E6^4)`, and Niemeier gluing. The new repository statement is the explicit comparison in the quotient-selected common `A2^12` coordinates and its exact identification with the four W33 line channels. No continuum or particle-physics claim is made.
