# Passes 4849–4856 executed outcomes

Reserved collision-free at `aa5439c1253feefdc6e10cb4d0b89cf31e60e336`. All five queued fronts and three outside-box probes are now frozen with exact certificates.

## 4849 / 4854 / 4855 / 4856 — the missing binary direction is the E6 root-signing switching class

The Pass4842 binary right kernel

`K = [360,36,20]_2`

has 36 minimum words whose span has dimension 35. The 36 minima are exactly the 36 twelve-line `K6,6-M6` carriers. Cross-checking Pass4659 identifies these supports with the classical 36 cubic-surface double-sixes. Each of the 360 K3,3 witnesses lies in exactly two double-sixes, so the `36 x 360` minimum-shell incidence matrix is the ordinary vertex-edge incidence matrix of

`H36 = SRG(36,20,10,12)`.

The complement is the older `SRG(36,15,6,6)` double-six overlap graph. Therefore the minimum shell spans exactly the 35-dimensional binary cut code of `H36`.

An independent E6 construction gives 72 roots and 36 projective root pairs. Joining two projective roots when their inner product has absolute value one produces a graph explicitly isomorphic to `H36`. Under that graph isomorphism the entire order-51840 carrier action is conjugate to the Weyl `W(E6)` action on projective roots.

Choose one positive root from every projective pair and sign every edge by the sign of the root inner product. The set `sigma_E6` of negative edges has weight 120, belongs to `K`, and extends the cut-space span from dimension 35 to 36. The signed adjacency matrix has spectrum

`10^6 + (-2)^30`,

and `2I+B` is the rank-six projective E6 root Gram matrix with nonzero spectrum `12^6`.

Thus

`K = Cut(H36) + <sigma_E6>`.

The nontrivial switching coset has exact minimum 120. If one representative is chosen from each root pair and `N_-` is the number of negative nonorthogonal pairs, then

`||sum r||^2 = 792 - 4 N_-`.

For a positive E6 root system the sum is `2 rho`, with `||2 rho||^2=312`, hence `N_-=120`. Equality orientations are Weyl chambers. Opposite chambers induce the same edge signing, so the complete coset-minimum shell has `51840/2=25920` vectors. PGSp/W(E6) is transitive on them with stabilizer two; PSp splits them into two orbits of 12960.

The characteristic-two extension

`0 -> Cut(H36) -> K -> F2 -> 0`

is nonsplit for both PSp and PGSp. Both groups are transitive on the 360 coordinates, so the ambient fixed space is only the all-one line. The all-one vector is not in `K` because each defining binary incidence row has odd weight three. Hence no fixed lift of the trivial quotient exists.

The carrier incidence matrix has row/column degrees 20/2 and ranks

`rank_F2=35`, `rank_F3=rank_F5=rank_F7=36`.

Its real squared singular values are `40^1,22^20,16^15`.

The standalone kernel code has exact low shell below weight 64

`A20=36, A38=360, A40=270, A54=1200, A56=3240, A58=2160, A60=540`.

Its dual is

`K^perp = [360,324,3]_2`.

The 1200 triangles of `H36` split into 1080 E6-sign-even triangles and 120 sign-odd triangles. The 1080 even triangles are precisely the binary Levi-cycle minimum checks. ML decoding of `K` reduces to two exact signed switching/MaxCut optimizations on `H36`, one per coset of its cut code; `d=20` gives bounded-distance radius nine.

The full code automorphism group has order 51840 and is the `W(E6) ~= PGSp(4,3)` action on the 36 projective roots/double-sixes. This follows from the complete minimum shell reconstructing the double-six scheme (whose full automorphism order was already independently certified as 51840) together with the explicit order-51840 Weyl action preserving the E6 switching class.

## 4850 — exact 59/49-orbital algebras

The 1080 Levi minima support noncommutative orbital algebras.

For PSp:

- orbital dimension 59;
- center dimension 15;
- over `C`, `A ~= C^7 x M2(C)^4 x M3(C)^4`;
- rational center `Q^9 x Q(sqrt(-3))^3`.

For PGSp:

- orbital dimension 49;
- center dimension 13;
- over `C`, `A ~= C^6 x M2(C)^4 x M3(C)^3`;
- rational center `Q^13`.

Thus the outer involution both fuses ten stabilizer orbitals and removes the three Eisenstein center factors seen by PSp. Split-versus-division status of every noncommutative rational simple block remains separate until explicit rational matrix units are constructed.

The K3,3 incidence Gram operator on the 1080-cycle carrier is extremely sparse in the PGSp orbital basis:

`M M^T = 3 A_0 + A_1 + A_5`.

Those three orbitals have subdegrees `1,12,12` and shared-Levi-edge counts `8,4,2`. The operator is not central; its commutant inside the 49-dimensional orbital algebra has dimension 27.

## 4851 — the S3^45 sheet kernel cannot be killed by code shells

Pass4843/4845 left the intrinsic class-shell automorphism group

`S3^45 : Aut(GQ(4,2))`.

This is not an artifact of stopping at the first cross-cell shell. The three sheet cells above each of the 45 recovered GQ points are genuinely interchangeable in the complete `[2025,399,14]_2` code construction. Equal generator columns also admit arbitrary internal coordinate permutations.

The full coordinate automorphism group is therefore

`(S4^405 x S3^135) : (S3^45 : PGSp(4,3))`.

Consequently no higher intrinsic codeword or dual shell can remove `S3^45`: breaking it requires extra structure outside the classical code, such as fixed hardware placement, timing, labels, or dynamics.

## 4853 — ternary lift requires an orientation local system

Pass4807 gives the canonical ternary quotient

`C^perp / (direct_sum_27 G10) ~= H1(Levi(GQ(4,2));F3)`,

with dimension 64.

The 1080 projective Levi 8-cycle lines span all 64 dimensions of ternary Levi homology. The 360 projective induced-K3,3 weight-six witnesses span only 54 dimensions, leaving a genuine ten-dimensional quotient.

The ordinary `1080 x 360` containment matrix has `rank_F3=359` and kernel generated by the all-one vector. An exact mixed-integer sign-gauge test proves that no choice of plus/minus orientations on the 360 projective K3,3 witnesses makes their signed total homology class zero. Therefore the projective unweighted incidence quotient cannot linearly factor to the K3,3 homology witness map.

The correct functorial object is the 720-object oriented-K3,3 double cover. Its anti-invariant `F3` sector has deck reversal acting by `-1`, and the map sending an oriented K3,3 to its signed 18-edge Levi flow is PGSp-equivariant. Its image has dimension 54 and kernel dimension 306. Via Pass4807 this image sits canonically inside the 64-dimensional nonlocal ternary Golay/Levi logical quotient.

The remaining ten homology dimensions are deliberately not identified with any other ten-dimensional object from dimension alone.

## Evidence boundaries

All statements above are exact finite graph/group/code/root/homology results. The E6 identification is objectwise and action-level: explicit projective roots, explicit graph isomorphism, and conjugate 51840-element permutation actions. No physical E6 field, particle assignment, measured threshold, or hardware timing claim follows.
