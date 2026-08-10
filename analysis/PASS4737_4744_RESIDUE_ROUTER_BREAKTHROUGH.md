# Passes 4737--4744 — residue-router breakthrough packet

## Executive result

The four-line involution residues from Passes 4721--4726 are not an isolated 270-object.  Under the natural `PSp(4,3)` action they are **exactly the same 270-point G-set** as the selected270 router reconstructed independently in Pass 4716.

The identification is not a count or spectrum match.  A selected270 point stabilizer fixes a unique involution residue; equality of the two order-96 stabilizers gives a well-defined `PSp(4,3)`-equivariant bijection.  Under that bijection:

- residues sharing exactly two W33 lines are exactly the 1,620 **cold** selected270 edges;
- an intrinsic degree-3 residue orbital is exactly the 405 **hot** selected270 edges;
- the hot graph is 27 disjoint Petersen graphs;
- each Petersen fiber consists of ten pairwise-disjoint four-line residues whose supports partition all forty W33 lines.

This unifies the support-12/involution/code thread of Passes 4721--4726 with the independent GQ(4,2)/S3-bundle router thread of Passes 4713--4720.

## Pass 4737 — full residue orbital algebra

For a residue `R`, its stabilizer in `PSp(4,3)` has order 96 and has twelve suborbits

`1, 12, 16, 48, 16, 6, 24, 96, 12, 12, 24, 3`.

Thus the transitive 270-action has permutation rank 12.  Its centralizer algebra has dimension 12 and center dimension 9; it is noncommutative.  Over C this means nine inequivalent irreducible constituents occur, with exactly one constituent having multiplicity two.

The share-two-lines orbital graph has degree 12, 1,620 edges, and **diameter 4**.  The distance shell from a point is

`1, 12, 67, 160, 30`.

Its exact characteristic factorization is

`(x-12)(x-8)^15(x-2)^84(x+1)^64(x+4)^60(x+6)^6(x^2-2x-12)^20`,

so the irrational sectors are `1 +/- sqrt(13)`, each with multiplicity 20.

The degree-3 orbital has 27 connected components of ten vertices, each a Petersen graph.  The 27 components form the canonical imprimitivity system of the residue action.  Quotienting the cold graph by these components gives `SRG(27,10,1,5)`, and each adjacent pair of Petersen fibers is joined by twelve cold edges arranged as three disjoint `K2,2` blocks — exactly the Pass-4716 connection law.

## Pass 4738 — the outer twist is a normalizer quotient

Let `h` be a four-fixing outer order-four square root of a four-fixed-line involution and let

`K = C_PSp(h)`.

Then `|K|=48`.  Exact enumeration gives

`N_PSp(K) = H`,

where `H` is the order-96 residue stabilizer.  Hence `H/K = C2` is the intrinsic two-sheet character.

The two order-96 subgroups in full `PGSp(4,3)` — the support-triangle stabilizer and the root centralizer — intersect exactly in `K` but are not equal.  There are representatives `t` and `n` with

`t^2=n^2=1`, `n in H\K`, `h=t n`, and `n t=h^{-1}`.

Equivalently `n h n^{-1}=h^{-1}`.  This upgrades the earlier statement “the extensions differ” to an explicit **normalizer-quotient twist**.  It is deliberately described as a `C2` torsor/normalizer class; no unsupported `H^2` cocycle claim is made.

## Pass 4739 — q=3 is exceptional as stated

The attempted all-q generalization was tested rather than assumed.

For prime `q=2,3,5,7`, direct construction gives binary line-intersection adjacency ranks

- q=2: 14;
- q=3: 10;
- q=5: 26;
- q=7: 50.

For the tested odd values this is `q^2+1`.

At q=3 the canonical elliptic projective involution fixes four pairwise-skew lines and gives the established minimum kernel word.  At **q=5**, however, an exact MILP proves the adjacency-kernel minimum is **6**, while the canonical elliptic involution fixes **8** lines.  A minimum witness is a six-line pairwise-skew partial spread.  At q=7 the elliptic involution fixes eight=q+1 pairwise-skew lines and certifies only the upper bound `d<=8`; no exact q=7 lower bound is claimed here.

Therefore the statement “involution fixed sets are the complete minimum shell” does **not** generalize verbatim beyond q=3.

## Pass 4740 — Golay coordinate intertwiner no-go

The old W33/Golay material contains exact numerical parameter relations, but Pass 4740 asks for an actual symmetry/code map.

A faithful action of `PSp(4,3)` by permutations of the 24 extended-binary-Golay coordinates is impossible because

`|PSp(4,3)| = 2^6 * 3^4 * 5`

whereas

`|M24| = 2^10 * 3^3 * 5 * 7 * 11 * 23`.

The former does not divide the latter.  This is a **coordinate-permutation** no-go only; it does not rule out a non-coordinate representation inside Conway/Leech symmetry.

The new involution geometry also supplies a canonical 24-coordinate minor: delete the sixteen W33 lines fixed by a 45-class involution.  Puncturing H10 gives

`[24,10,6]`,

with weight enumerator

`1 + 16 z^6 + 87 z^8 + 240 z^10 + 336 z^12 + 240 z^14 + 87 z^16 + 16 z^18 + z^24`.

Its weight-6 words immediately prevent it from being a subcode of the extended binary Golay `[24,12,8]`.  Shortening H10 on the same sixteen coordinates gives only `[24,2,16]`.  Puncturing `H10^perp` there gives `[24,22,2]`.

## Pass 4741 — exact optimal 27-round decoder/check schedule

The 27 Petersen fibers discovered in Pass 4737 are simultaneously 27 **parallel check classes**.  Every fiber contains ten pairwise-disjoint weight-4 residue checks and covers all forty W33 line coordinates exactly once.  The 27 fibers partition all 270 checks.

Every line participates in exactly 27 residue checks, so any schedule forbidding simultaneous reuse of a line needs at least 27 rounds.  The Petersen-fiber schedule attains 27 and is therefore optimal.  The group permutes the 27 rounds, so this resolution is `PSp(4,3)`-equivariant.

The 270 checks have binary rank 30.  Since they form one `PSp(4,3)` orbit, there is no nonempty strict `PSp`-invariant subset of checks; a non-equivariant algebraic basis uses 30 checks.

For H10=`[40,10,12]`, all error patterns through weight 5 have unique syndromes.  At weight 6 the only collisions are the complementary 6+6 halves of the forty weight-12 H10 words: exactly 18,480 syndrome classes are doubletons and there are no triple collisions.  The distinct coset-leader counts are

- w0: 1
- w1: 40
- w2: 780
- w3: 9,880
- w4: 91,390
- w5: 658,008
- w6: 3,819,900.

## Pass 4742 — bonkers: the check-dependency matroid has 540 triangles

The 270 residue masks have rank 30, so their binary dependency code has parameters

`[270,240,3]`.

Its complete minimum shell contains exactly **540 weight-3 dependencies**.  Every minimum dependency consists of three residue checks whose supports pairwise meet in two lines and whose union has six lines.  These 540 dependency triangles partition all 1,620 cold edges exactly once.  Each residue check lies in six such circuits.

A tempting new `540=540` identification was explicitly falsified.  A dependency-triangle stabilizer and a Pass-4723 support/root-triangle stabilizer both have order 48, but their element-order censuses differ:

- dependency triangle: `1^1 2^19 3^8 4^12 6^8`;
- root/support triangle: `1^1 2^7 3^8 4^24 6^8`.

They are therefore not conjugate PSp subgroups and not the same 540-point G-set.

## Pass 4743 — bonkers: an exact commuting four-body parity Hamiltonian

Put a Z-bit/qubit on each W33 line and, for each residue R, define

`S_R = product_{i in R} Z_i`, `H = - sum_R S_R`.

This is a finite commuting-check model.  The check rank is 30, so the common +1 ground space has degeneracy `2^10=1024`; in the computational basis it is exactly H10.

The syndrome code `im(B^T)` is **[270,30,27]**.  An exact MILP proves distance 27, and a second exclusion MILP proves that the complete weight-27 shell consists of the forty single-line syndromes.  Hence

- ground energy = -270;
- finite-model gap = 54;
- first-excited degeneracy = `40*1024 = 40,960`.

A one-line defect violates 27 terms.  Two skew W33 lines violate 48 terms because they coexist in three residue checks; two meeting W33 lines violate 54 terms because they coexist in none.  Thus the two-defect spectrum already resolves W33 incidence.

The 540 Pass-4742 dependencies are operator identities `S_a S_b S_c=I`, and the 27 Pass-4741 parallel classes give an optimal 27-layer disjoint-support measurement schedule.

No microscopic or thermodynamic-limit physical interpretation is inferred.

## Pass 4744 — bonkers: natural 24-coordinate minor census

A second intrinsic family of 24-coordinate minors comes from deleting the support of any of the 135 weight-16 H10 words.  All 135 have the same signatures:

- puncture H10: `[24,9,4]`;
- shorten H10: `[24,1,24]`.

So this family also cannot be an extended-Golay subcode.  Together with Pass 4740, the two most canonical W33-derived 24-coordinate routes fail for structural distance reasons, not merely because a guessed construction did not work.

## Evidence boundary

The executable sources are:

- `analysis/w33_pass4737_4738_4741_4742_residue_router_cocycle_decoder.py`
- `analysis/w33_pass4739_w3q_involution_minimum_shell_probe.py`
- `analysis/w33_pass4740_4744_golay_intertwiner_minor_no_go.py`
- `analysis/w33_pass4743_residue_parity_hamiltonian.py`

The positive identifications are finite group/code/incidence theorems and the negative statements are explicit falsifiers.  No physical claim is inferred from count equality, no all-q theorem is inferred from q=2,3,5,7 tests, and the Golay no-go is restricted to the standard coordinate-permutation route.
