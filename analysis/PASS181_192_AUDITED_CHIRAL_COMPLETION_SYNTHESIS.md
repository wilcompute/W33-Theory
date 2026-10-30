# Passes 181–192: Audited Chiral Completion Synthesis

This packet re-runs the fifth-round claims at object level, repairs the
overclaims, and closes four new exact structures. Every statement below is
owned by a regenerating witness and JSON certificate.

## What survived the audit

- Pass 181 is an exact mod-3 Hom census. Pass 184 supplies the explicit
  rank-10 address and gauge maps. The address quotient is an exhaustively
  irreducible five; the gauge quotient is a 14-dimensional brick, not thereby
  proved simple; the route module fits a nonsplit
  `0 -> K14 -> route -> 1 -> 0` sequence.
- Pass 182's constant-section line and pair-partition labels are intrinsic
  only after the group-selected four-valent orbital is supplied. All 40 axis
  tables, 80 line transports, and 240 axis transports are exact.
- Pass 185's three axes are `S3/C2`, not an S3 torsor: image 6, kernel 108,
  axis stabilizer 216.
- Pass 186 has exactly two 216-element shell orbits and orbital rank 40.
  Its sparse relations are one 36-component dodecad family and two
  36-component six families.

## Complete order-eight theorem (Pass 183)

Every exact-order-eight discriminant element was enumerated in independent
Smith coordinates:

| form | numerator of `q` modulo 16 | count |
|---|---:|---:|
| address dark | 3, 11 | 32768 each |
| route dark | 3, 11 | 512 each |
| point code | 5, 13 | 32768 each |
| line code | 5, 13 | 512 each |

The invariant result is the full negation
`{3,11}/8 <-> {5,13}/8`, not a canonical `11/8` generator.
The incidence restriction gives an exact cokernel with invariant factors
`(2^5, 6^9, 24)`, hence an abstract finite-abelian-group isomorphism with the
address discriminant group. A discriminant-quadratic-form isometry remains
open. Milgram eighth-root recognition is numerical corroboration.

## Exact double-sixes (Pass 188)

The directed valency-five orbitals are transposes. Their union is 36 copies of
`K6,6` minus a perfect matching. The two symmetric orbitals are two families of
36 exact `K6`s, and every crown bipartition uses one six from each family,
bijectively. The component stabilizer is faithful `S6` of order 720. The
previous icosahedron suggestion is exactly false.

## Complete binary submodule lattice (Passes 187/189)

The point permutation module is uniserial:

```text
0 < j < C < im(A2) < ker(A2) < Cperp < jperp < F2^40
layers: 1 | 14 | 1 | 8 | 1 | 14 | 1
```

Exhaustive nonzero-vector orbit scans and successive-socle Hom computations
prove there are exactly eight invariant binary codes. The sentinel is the
unique invariant 15-space, and the central eight is the unique 8-dimensional
subquotient.

## Steinberg composition census (Pass 190)

Live GAP proves the computed character table is permutation-equivalent to the
CTblLib `U4(2)` table, transports ten permutation characters, and obtains the
Steinberg-81 multiplicities

```text
points lines arcs shell trades supports skew hyperbolic Q42-arcs flags
   0     0    2     3      0       0      2       1        2       1
```

These are modular composition multiplicities, not a selected register or
hardware-protection theorem.

## The 27+6+3 completion fibre (Pass 191)

The product conjecture is refuted:

```text
120 axes × 36 double-sixes = 3240 + 720 + 360
                            = 120 × (27 + 6 + 3).
```

The corresponding pair stabilizers have orders `8, 36, 72`. The positive
replacement is the smallest suborbit: an axis stabilizer of order 216 acts on
its three distinguished double-sixes through full `S3`, with kernel 36. This
is a native `S3/C2` completion fibre over 120 axes. The full 4320 product has
the controller's cardinality and the wrong orbit structure.

## Signed trades are tetrahedral edges (Pass 192)

For each signed second-shell trade, its positive octads contain one unique
edge of the matched four-point line and its negative octads contain the
complement. Therefore

```text
240 signed trades  <->  40 W33 lines × 6 two-point edges,
```

equivariantly in all 480 generator cases. The line stabilizer satisfies

```text
1 -> C3^3 -> H_line -> S4 -> 1.
```

The kernel is checked elementwise to be abelian, order 27, exponent three.
Signed trades carry `S4/V4`, the tetrahedral-edge action. Complement-pairing
gives the unsigned axes and `S4 -> S3`. Equal six-element counts do not turn
this action into a regular S3 controller frame.

## Reproduce

```bash
python3 analysis/w33_pass181_adjoint_shadow_mod3.py
python3 analysis/w33_pass182_line_octahedron_dictionary.py
python3 analysis/w33_pass183_incidence_square_ledger.py
python3 analysis/w33_pass184_mod3_trade_factors.py
python3 analysis/w33_pass185_octahedron_clock.py
python3 analysis/w33_pass186_pentad_core_scheme.py
python3 analysis/w33_pass187_f2_layer_sandwich.py
python3 analysis/w33_pass188_icosahedron_test.py
python3 analysis/w33_pass189_uniserial_certificate.py
python3 analysis/w33_pass190_steinberg_address.py
python3 analysis/w33_pass191_supercycle_pullback.py
python3 analysis/w33_pass192_signed_trade_edge_s4.py
```

Passes 184 and 190 use live GAP/CTblLib. The shared runner supports both
native Windows and WSL invocation of the installed GAP 4.15.1 runtime.
