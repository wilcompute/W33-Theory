# Passes 4833–4840 — executed outcomes

## Exact packet closure

This packet closes the code-interaction / intrinsic-symmetry / minimum-cycle lane reserved in `PASS4833_4840_RESERVATION.md`.

### Passes 4833 + 4838 — Levi code is an exact invariant subcode

On the identical 2025 physical coordinates,

\[
C_{\rm Levi}\le C_{378}\le C_{399},
\]

with

\[
\dim C_{\rm Levi}=64,\qquad \dim C_{378}=378,\qquad \dim C_{399}=399.
\]

Hence

\[
\dim(C_{399}/C_{\rm Levi})=335.
\]

The 405-hot-coordinate puncture is injective on `code399`: its dimension remains 399.  Thus the inclusion survives on the 1620-coordinate cold carrier.  The Levi code is PGSp-invariant, but no invariant complement/direct-summand statement is made.

### Pass 4834 — the sparse syndrome schedule is exactly three layers

The earlier eight-layer construction was not optimal, and the first six-layer continuation argument was also too rigid: intersecting W6 outer words need not use intersecting *physical representatives* because the local repetition dual lets each global functional move among the four equal cold coordinates in a repetition class.

For the canonical sparse rank-1620 local check basis, the exact result is

\[
\boxed{\text{minimum schedule depth}=3}.
\]

Two Pass4821 local layers contain 945 and 675 checks.  A finite exhaustive W6-basis search finds an outer basis of weights

\[
12,12,16,12,12,12
\]

whose maximum coordinate multiplicity is four.  The six global functionals can therefore be assigned injectively to the four physical representatives of every active cold class and placed together in one third layer.  The full check rank is still 1626.

Two layers are impossible in this sparse-basis model: the connected bipartite local-cell conflict graph fixes the two local colors up to swap, leaving at most one globally usable representative in each logical repetition class.  Six global supports would then have to be pairwise disjoint on 27 outer coordinates, forcing total outer weight at most 27, while any W6 basis has total weight at least `6*12=72`.

This is a correction to the Pass4825–4832 manuscript paragraph that described an eight-layer upper bound and to the first Pass4834 six-layer formulation.  The theorem is deliberately restricted to the stated sparse check family / disjoint-support scheduling model.

### Passes 4835 + 4839 — the minimum dual-shell design is far too symmetric

The intrinsic Pass4832 design has 540 quotient classes:

\[
405\text{ cold classes of size }4,
\qquad
135\text{ hot classes of size }3.
\]

Its 135 minimum quotient relations have profile `(4,4,4,3)` and partition all 540 classes.  Retaining only this weight-two repetition shell plus the complete minimum quotient shell yields 135 disconnected typed cells.  Consequently the exact class-level automorphism group is

\[
\boxed{S_3^{135}:S_{135}},
\]

with order `6^135 * 135!`, already enormously larger than PGSp(4,3).  At physical-coordinate level there is additionally an internal repetition-class kernel containing

\[
S_4^{405}\times S_3^{135}.
\]

Therefore these two dual shells alone cannot reconstruct the 45 packets, 27 GQ lines, Petersen fibers, or PGSp router action.  Higher-shell/full-code data are mathematically necessary to break the free `S_135` cell permutation symmetry.

### Pass 4836 — complete binary Levi minimum shell

The 1080 weight-96 words of

\[
[1620,64,96]_2
\]

are exactly the twelvefold repetitions of Levi 8-cycles, equivalently the 1080 four-cycles of the 27-line graph `SRG(27,10,1,5)`.

They form one PSp orbit and one PGSp orbit:

\[
25920/1080=24,
\qquad
51840/1080=48.
\]

Thus the stabilizers have orders 24 and 48.  For every minimum word, the other 1079 minima split by shared Levi edges as

\[
0^{759},\quad1^{192},\quad2^{88},\quad3^{24},\quad4^{16}.
\]

### Pass 4840 — exact binary-cycle / ternary-K3,3 incidence

The count coincidence `1080=3*360` is now replaced by a literal incidence theorem.  Let a binary minimum four-cycle be incident with a ternary K3,3 witness when its four quotient-line vertices lie inside the six vertices of that induced K3,3.  Then

\[
\boxed{\text{each binary cycle lies in exactly 3 induced }K_{3,3}\text{s}},
\]

and

\[
\boxed{\text{each induced }K_{3,3}\text{ contains exactly 9 binary cycles}}.
\]

Hence

\[
1080\cdot3=360\cdot9=3240.
\]

The resulting `1080_3 – 360_9` incidence graph is connected.  Its incidence matrix has ranks

\[
324,\;359,\;360,\;360
\]

over `F2,F3,F5,F7`, respectively.

A tempting coarse association scheme is also falsified.  Partitioning pairs of binary minima only by their number of shared Levi edges does not form an association scheme: in the shared-one-edge relation, adjacent pairs have 30, 31, or 36 common neighbors within the same relation.

### Pass 4837 — evidence boundary remains explicit

The four heavy carryovers from Pass4825–4832 remain producer-installed but do not yet have frozen generated certificates on `master`:

1. characteristic-two Brauer/Loewy closure of the large flag-H1 module;
2. PGSp Burnside quotient on the 64-dimensional sign module;
3. arbitrary-rho outage-flow phase diagrams;
4. the exact common-generator 64x64 sign-H1 / Levi-H1 intertwiner.

The heavy workflow and an observable PR-triggered workflow are installed.  Until their generated JSON certificates materialize, none of those four computations is promoted as a theorem.

## Main structural conclusion

The new exact filtration is

\[
C_{\rm Levi}^{64}
\subset
C_{378}
\subset
C_{399},
\]

while the complete Levi minimum shell is a single highly symmetric 1080-object orbit coupled biregularly to the 360 ternary K3,3 witnesses.  At the same time, the low dual shells of `code399` are *not* sufficient to recover the global GQ/router geometry: the missing cross-cell structure is real and measurable as an enormous extra wreath-product symmetry.

This cleanly separates three layers that were previously easy to blur:

- high-distance binary Levi homology as an invariant subcode;
- the larger distance-14 ambient code and its three-layer syndrome engine;
- the ternary nonlocal K3,3 homology shell, linked to the binary minima by incidence rather than identification.
