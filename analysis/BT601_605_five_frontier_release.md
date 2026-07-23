# Passes 601-605: torsion, gauge, outer packet, selector, and noise release

This release executes the five non-sequential directions following Pass 600. Every statement below is backed by a deterministic JSON certificate and a focused regression.

## Pass 601 — twisted torsion anatomy

The exact primary Smith profiles now include

- `2`: `(Z/2)^32 + (Z/4)^7 + (Z/8)^5 + Z/16 + Z/32 + Z/64`,
- `3`: `(Z/3)^24 + (Z/9)^13 + (Z/27)^2 + Z/2187`,
- `5`: `(Z/5)^9 + (Z/25)^3`,
- `7`: `(Z/7)^7`,
- `13`: `(Z/13)^5`.

All other resolved determinant primes have exponent one and hence contribute a single cyclic `Z/p` factor. A 62-digit composite cofactor remains unsplit. The release records a direct Fermat compositeness witness and does not call the Smith form complete.

## Pass 602 — complete gauge normal form

For all reversible `S5`-valued connections on `J(8,3)`, spanning-tree gauge leaves 365 loop holonomies and one global simultaneous conjugation. Hence the complete gauge quotient is

`S5^365 / S5`,

with exact Burnside count

`120^364 + 12^364 + 8^364 + 2*6^364 + 5^364 + 4^364`.

The six Pass-596 order-statistic connections are pairwise gauge inequivalent. The narrower set of six exterior-transposition choices is not itself gauge-stable, so an unrestricted local-assignment quotient of only those six choices is not intrinsically defined.

## Pass 603 — the outer 15=1+5+9 packet

The classical duad-syntheme incidence matrix has rank ten and gives an exact outer-automorphism intertwiner:

`15 = 1 + 5 + 9  ->  15 = 1 + 5' + 9`.

It annihilates the natural five-dimensional packet, maps the singlet with singular value three, and maps the common nine-dimensional packet with singular value two. Thus the outer automorphism supplies a second canonical packet basis, but no canonical invertible 15-dimensional bridge.

## Pass 604 — snub-color selector ladder

Adding one Pass-579 snub coloring to the apexed icosahedron leaves tetrahedral `A4`. This residual group remains transitive on all six Singer axes and all six tetrahedral transporter edges. Marking one opposite-yellow pair leaves `C3` and splits the six transporters into two orbits of size three. An ordered adjacent yellow-pair flag has trivial stabilizer and is the first datum that selects one transporter uniquely.

## Pass 605 — noise-aware Wilson falsifier

With effective coherent amplitude retention `a`, class means scale as

`(a Tr U, a^2 Tr U^2, a^3 Tr U^3)`.

Under the stated six-channel Gaussian variance proxy, the limiting confusion changes at

`sqrt((-9+sqrt(113))/16) = 0.3191929092...`.

At one-percent familywise error and dark-variance ratio `0.01`, the conservative shots per trace are 23 at `a=1`, 50 at `a=0.8`, 170 at `a=0.5`, and 567 at `a=0.3`. A simultaneous Hoeffding bound requires 2,820 classified loops to estimate all four histogram frequencies within absolute error 0.03 at 95 percent confidence.

## Validation

The five witnesses pass 47 of 47 internal checks, regenerate byte-identical certificates under `--check`, compile, and pass the focused regression.
