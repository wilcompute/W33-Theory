# Passes 4976–4983 — executed outcomes

**Date:** 2026-08-11  
**Status:** EXECUTED locally/exactly; remote replay pending observation.  
**Renumbering:** these eight attacks were initially reserved as 4968–4975, but a parallel lane landed commit `f9db42c7fe192690b824a307df7fe27abadbd483` using 4968–4972 after the reservation. No theorem artifact from this lane was written under the collided numbers. The reservation was relinquished and this packet moved intact to 4976–4983.

## Pass 4976 — signed-shell correlations kill the Pass4960 fake character

The 360 coordinates of `K=[360,36,20]_2` are the edges of the 36-double-six graph `H36`. Reconstructing the Pass4859 E6 switching cochain `sigma` gives an exact split of the 1200 H36 triangles:

- 1080 non-Steiner triangles have `sigma` parity 0;
- 120 Steiner triangles have `sigma` parity 1.

The 1080 parity-even triangles are exactly the weight-three words of `K^perp`, and their GF(2) span has rank **324**, the full dual dimension. Therefore the shell-three signs determine the complete dual character in the two extremal cases:

- `T3=+1080` forces `Tj=Aj`;
- `T3=-1080` forces `Tj=(-1)^j Aj`.

Hence the Pass4960 relaxed tuple with `T3=-1080` and `T4=-1936` is **not realizable by any dual character**: it would require `T4=+10530`.

A second exact correlation comes from pairwise sums of shell-three words. Among the `C(1080,2)` unordered pairs, 12,960 sums have weight 4 and 569,700 have weight 6. The weight-four sums hit 9,720 distinct `A4=10,530` words, with multiplicities `1^6480 2^3240`; 810 weight-four words are outside `S3+S3`.

**Boundary:** this destroys the particular degree-seven relaxation witness but does not yet exclude every distance-173 coset. The rigorous covering-radius interval stays `134 <= rho(K) <= 173`.

## Pass 4977 — the actual PGSp outer twist does not rescue the dark 15

Pass4961 proved the ordinary point/line dark-15 Hom spaces vanish. Let `alpha` be conjugation on PSp by the explicit multiplier-minus-one element of PGSp used in Pass4966. Both the 40-point and 40-line permutation representations extend to PGSp, so twisting either restriction by `alpha` is implemented by conjugation with the corresponding outer permutation matrix. Their unique 15-dimensional constituents are therefore individually `alpha`-stable.

Thus

`Hom_PSp(^alpha V15_line, V15_point) = Hom_PSp(^alpha V15_point, V15_line) = 0`.

The genuine point/line correlation sought in Pass1879 is not the ordinary PGSp/PSp outer involution.

## Pass 4978 — Witting phase is an outer-sign compensator for the quadratic Hom plane

Pass4875 gives a two-dimensional PSp quadratic Hom space `H` on which the PGSp/PSp involution acts as `-I2`. Pass4966 gives the Witting oriented-phase sign line `epsilon_W`, also `-1` on the outer coset and `+1` on PSp.

Therefore the compensated multiplicity space

`H_comp = H tensor epsilon_W`

has outer action `(-I2)(-1)=+I2`: it is a two-dimensional **PGSp-even** quadratic channel space.

This is the same sign-cancellation mechanism that Pass4941 uses internally at quartic degree, but with a crucial difference: the Witting compensator leaves the two-dimensional projective ambiguity intact. It does not choose a preferred quadratic channel.

## Pass 4979 — the 45 tritangents are the missing 1+20 spread reader

For every cubic-surface tritangent, exactly 24 of the 36 double-sixes contain exactly two of its three cubic lines and the other 12 contain none. Transporting double-sixes through the unique Pass4964 bijection defines a canonical `45 x 36` tritangent/spread selector matrix `M`.

Exact results:

- row weight 24, column weight 30;
- `rank(M)=21`;
- `M^T M = 18J + 12I + 3A_H36`;
- nonzero spread sector is `1+20`, while the 15 is dark;
- squared singular values are `720^1, 18^20`.

For two tritangents, the row Gram is 18 exactly when they share one cubic line (270 pairs) and 15 when they are disjoint (720 pairs).

The Pass4967 spread-line channel `C` obeys `C C^T = 4J + 6I - 3A_H36` and has rank 16=`1+15`. The adjacency terms cancel:

`18 I_36 = C C^T + M^T M - 22 J_36`.

Thus stacking the 40 W33-line readout and the 45 tritangent readout gives an `85 x 36` matrix of rank **36**: the **40+45 channels exactly reconstruct the entire 36-spread/double-six carrier**.

## Pass 4980 — the local nine-spread chart has full wreath-product gauge

Fix a W33 line. Its nine incident spreads carry the Pass4965 canonical `3+3+3` Steiner partition. The full `W(E6)` line stabilizer has order 1296 and acts faithfully on these nine spreads. The induced permutation group also has order 1296, exactly the order of the full imprimitive wreath product

`S3 wr S3`.

So the substrate canonically gives the **unlabelled block system**, but no canonical order of the three blocks and no canonical order inside a block. A qutrit/time-bin compiler must choose/calibrate a finite gauge; the raw incidence structure does not supply labels for free.

## Pass 4981 — Q43 tetrahedra close both H1 and H2 and obey S3 Bianchi

The Q43 disjointness graph has 40 vertices, 540 edges, 3240 triangles, and **9450 K4 tetrahedra**. Over GF(2):

- triangle-to-edge boundary rank = 501;
- its kernel dimension = 2739;
- tetrahedron-to-triangle boundary rank = **2739**.

Therefore the clique 3-skeleton has

`H1(F2)=0` and `H2(F2)=0`.

For the Pass4962 S3 matching connection, the triangle curvature remains 1080 flat faces and 2160 reflection faces. On tetrahedra, reflection-face counts are

- 0 faces: 270 tetrahedra;
- 2 faces: 6480;
- 4 faces: 2700.

No tetrahedron has odd reflection parity. More strongly, all 9450 tetrahedra satisfy the exact nonabelian identity

`H_abc H_acd H_adb = P_ab H_bcd P_ba`.

Thus the local reflection curvature carries no residual GF(2) two-cycle charge once tetrahedra are filled.

## Pass 4982 — there are exactly 12 AG(2,3) completions, none canonical

Treat the canonical `3+3+3` partition at a W33 line as one parallel class of a putative affine plane on the nine spreads. Exact enumeration gives **12** labelled `AG(2,3)` completions containing that fixed parallel class. Equivalently, the nine remaining affine lines are the triples of one of the 12 Latin squares of order 3.

The full local `S3 wr S3` group acts **transitively** on all 12 completions. A chosen completion has stabilizer order `1296/12 = 108`.

Therefore the bare W33/double-six incidence data does **not** canonically complete the nine-spread chart to an affine qutrit plane. There is an exact 12-fold finite gauge ambiguity.

## Pass 4983 — the dual A3=1080 shell is “empty common spread line”

The 1200 triangles of the 36-spread one-overlap graph split under the Pass4964 bridge exactly as follows:

- 120 triangles: the three spreads share exactly **one** W33 line;
- 1080 triangles: the three spreads have **empty** triple intersection.

The 120 one-common-line triangles are precisely the Steiner triangles. Combining with Pass4976, the 1080 empty-common-line triangles are precisely the complete weight-three shell of `K^perp`.

So the code coefficient `A3(K^perp)=1080` now has a direct finite-geometric meaning:

> **three pairwise one-overlap spreads form a weight-three dual check iff their common W33-line intersection is empty.**

This also explains the complementary `120+1080=1200` triangle split that had previously appeared as two disconnected census numbers.

## Packet-level result

The five queued attacks plus three outside-box attacks all returned exact finite statements. The strongest new synthesis is the complementary carrier chain:

- 40 W33 lines read the `1+15` sector of the 36 spreads;
- 45 cubic tritangents read the complementary `1+20` sector;
- together they reconstruct all 36 spread coordinates exactly.

At the same time, the local nine-spread geometry is now sharply bounded: its `3+3+3` block system is canonical, but affine/qutrit coordinates are not—there is a full `S3 wr S3` local gauge and exactly 12 affine completions.
