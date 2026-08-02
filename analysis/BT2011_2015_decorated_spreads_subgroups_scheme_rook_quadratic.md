# Passes 2011–2015 — decorated spread pairs, subgroup exact covers, rank-three transport, rook doubles, and quadratic readout

The five requested fronts close with **53/53 frozen checks** and one independent
literal exact-cover witness.

## 2011 — the sibling classes are decorated four-line spread pairs

The 270 spread pairs meeting in four lines have stabilizer `S4×D8` of order 192.
The three related conjugacy-class carriers form exact decoration bundles:

- `270=270×1`: the canonical linewise half-turn;
- `540=270×2`: the two inverse coherent linewise quarter-turns;
- `1620=270×6`: the six cyclic orders of the four common lines.

The size-540 and size-1620 stabilizers have orders 96 and 32.  Their local
permutations and full `G`-orbits agree with the proposed decorations; this is not
a count-only identification.

## 2012 — enumerated subgroups construct parallel classes

Inside one four-line pair stabilizer `H≅S4×D8`, all 1,026 subgroups were
enumerated and reduced to 234 `H`-conjugacy classes.  Exact cover from whole
frame orbits succeeds for 204 subgroups in 33 conjugacy classes.

Every success has subgroup order 2, 4, or 8.  No subgroup of order at least 12
succeeds.  A literal `D8` witness uses twelve orbits of sizes

`2,2,4,4,4,4,4,4,8,8,8,8`

and covers each of the 240 edges exactly once with 60 frames.

This reverses the earlier weak negative from random large subgroups: the useful
construction band is real and concentrated at low subgroup order.

## 2013 — why spread intersections are one or four

The group action on 36 spreads has subdegrees `1,15,20`.  Each line belongs to
nine spreads, so a fixed spread has total overlap 80 with the other 35 spreads.
The valency-15 orbital consists of four-line pairs and accounts for 60.  The
remaining 20 spreads must therefore contribute one line each.

The four-line relation is

`SRG(36,15,6,6)`

and its adjacency matrix satisfies

`A²=9I+6J`.

The complement is `SRG(36,20,10,12)`.  The spread/frame incidence Gram matrix is
`45I+6A`, with eigenvalues `135,63,27`.  On mean-zero spread signals, the
centered and scaled adjacency is an exact involution.

## 2014 — the 360 orbit is a rook double, not an octet fiber

The one-line spread-pair stabilizer has octet orbits `6,9,12,18`, hence fixes no
octet.  There is no equivariant map from the 360 one-line pairs to the 45
octets; `360=45×8` is only arithmetic.

After deleting the common line, the two banks of nine remaining lines carry the
bipartite double cover of the `3×3` rook graph.  It has 18 vertices, degree four,
36 edges, and automorphism group order 144—exactly the pair stabilizer.

## 2015 — degree-safe interfaces and quadratic phase readout

Degrees 240 and 540 join the unsafe degree table:

- two nonconjugate order-216 stabilizers occur at degree 240;
- the three order-96 centralizers of the size-540 classes are pairwise
  nonconjugate.

Thus count matches at either degree prove nothing without a stabilizer or
permutation-character audit.

The phase is linearly confined but quadratically connected.  `Sym²(90)` reaches
all four rational blocks, including five copies of 81.  `Λ²(90)` contains no 15,
while `Sym²(90)` contains three copies, yielding a symmetric-versus-
antisymmetric selection rule.

Five bounded engineering architectures are recorded:

1. rank-three 36-lane spread mixer;
2. two-bank rook-double crossbar;
3. `D8` orbit-compressed exact-cover scheduler;
4. quadratic phase readout with a gauge-channel selection test;
5. stabilizer-aware `G`-set application binary interface.

## Boundaries

- `chi(H)=9` remains open.
- The subgroup enumeration is complete only within one fixed `S4×D8`
  four-line-pair stabilizer.
- The association scheme and rook-double theorems are finite `q=3` results.
- Quadratic multiplicities permit channels but do not supply coupling constants.
- Hardware designs are proposals, not demonstrated devices.
- Charge, flux, colour, generation, and neutrino readings remain withdrawn.
