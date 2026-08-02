# Passes 2550–2557 — seven-front breakthrough sprint

## Executive result

This packet executes the five requested frontiers and two independent high-risk probes.  The strongest closure is chromatic: the complete cover-link computation rules out every possible nine-cover resolution, so the canonical 540-frame graph is not 9-colourable.  The global U6 coefficient is not yet completely enumerated, but the lower shadow is closed exactly and 63 disjoint regular singleton orbits are certified.

## Pass 2550 — global U6 lower shadow and singleton orbits

The complete lower shadow contains

\[
1+\binom{240}{2}+\binom{240}{4}=134{,}839{,}021
\]

error records and exactly

\[
\boxed{91{,}007{,}752}
\]

distinct syndromes.  Every weight-zero and weight-two syndrome is already represented at weight four, so the lower-shadow union is exactly the weight-four image.

A complete triple-pair fiber test then proves 63 explicit weight-six errors are genuine singleton fibers: their syndromes are absent from the lower shadow and have no second weight-six representative.  The 63 witnesses lie in 63 disjoint regular `PGSp(4,3)` orbits, each of size 51,840.  Hence

\[
\boxed{U_6^{\rm singleton}\ge 63\cdot 51{,}840=3{,}265{,}920.}
\]

This proves the global singleton coefficient is nonzero and already multi-million. Equality remains open.

## Pass 2551 — complete cover-link K8 refutation

The previously missing frame labelling is reconstructed from the 45-octet syndrome hypergraph.  The octet co-occurrence graph is the canonical `SRG(45,32,22,24)`; its isomorphism transports all 240 edge labels and 540 frame labels into the frozen cover convention.

The transported action has order 25,920 and reproduces exactly:

\[
394{,}200\text{ fixed-frame covers},\qquad327\text{ orbits},\qquad3{,}547{,}800\text{ global covers}.
\]

Every one of the 327 orbit-representative disjointness links was searched exactly for eight mutually disjoint partner covers.  Link sizes range from 9,232 to 18,754.  No search timed out and no `K_8` exists. Therefore no nine exact covers partition the 540 frames:

\[
\boxed{\chi(H)\ge10.}
\]

## Pass 2552 — complete radius-five trade closure

The exact five-for-five meet-in-the-middle search finds precisely 33 sum-preserving signature tuples at trade radius five.  Of these, 27 contain an exact fiber pair with zero disjoint cover pairs.  The six pairwise-compatible survivors are all direct exact-lift UNSAT, with no timeout.

Thus the selected nine-signature tuple has no exact lift anywhere in its complete trade ball through radius five.  Pass 2551 independently settles the global nine-colour question.

## Pass 2553 — geometric decoder of the rank-nine block tower

Each of the 45 twelve-frame imprimitivity blocks is decoded geometrically.  The union of its twelve frame matchings uses 32 W33 points; the omitted eight points induce a canonical `K_{4,4}`.  Each frame determines one perfect matching of this omitted `K_{4,4}`.  The twelve frames are exactly one parity half of the 24 perfect matchings, hence form an `A_4` torsor.

The local relations are:

\[
A_4/V_4\cong C_3,
\]

\[
R_{16}=3K_4,
\qquad
R_{13}=K_{4,4,4},
\qquad
R_{13}\cup R_{16}=K_{12}.
\]

`PGSp(4,3)` acts faithfully on the 45 blocks with order 51,840; a block stabilizer has order 1,152, its action on the twelve matchings has order 576, and its quotient action on the three `V_4` cosets is the full `S_3`.

## Pass 2554 — first nonlinear 5:8 covariants

For the faithful four-dimensional module of the nonsplit normalizer `5:8`, exact modular linear algebra gives scalar invariant dimensions

\[
1,0,0,0,2,0,3,0,10,0,13,0,24
\]

in degrees zero through twelve.  The first nonconstant scalar invariants are two quartics.

The dimensions of equivariant homogeneous self-maps in degrees zero through nine are

\[
0,1,0,4,0,11,0,24,0,44.
\]

Thus the center eliminates all even-degree self-covariants and all odd-degree scalar invariants, but four genuinely nonlinear cubic self-covariants survive.  The linear normalizer obstruction therefore does not prohibit projective cubic dynamics.  This remains a normalizer-level result, not a full `PSp(4,3)` coupling.

## Pass 2555 — outside-box syndrome triangle geometry

The 240 frozen syndrome columns are the incidence vectors of 240 triangles on the 45 octets.  Every octet lies on 16 triangles, every co-occurring octet pair occurs once, and the triangles partition all 720 edges of

\[
\operatorname{SRG}(45,32,22,24).
\]

For the 45-by-240 parity-check matrix `H`,

\[
\boxed{HH^T=16I+A_{45}},
\]

with eigenvalues

\[
48^1,\quad18^{24},\quad12^{20},
\]

and binary rank 45.  The U6 syndrome map and the nonlinear exact-cover signature carrier are therefore the same 45-octet geometry viewed from opposite sides.

## Pass 2556 — outside-box chromatic spectral synthesis

The frame graph has spectrum

\[
32^1,\ 14^{44},\ 8^{15},\ 4^{81},\ 2^{84},\ (-4)^{315}.
\]

Hoffman gives `alpha(H)<=60`, and the exact-cover census attains 60.  A nine-colouring would therefore have to consist of nine maximum independent sets—nine disjoint exact covers—which Pass 2551 excludes.  A deterministic proper 14-colouring is frozen. Hence

\[
\boxed{10\le\chi(H)\le14.}
\]

The exact value within this interval remains open.

## Evidence boundary

All finite counts, ranks, orbit decompositions, pair relations, and exact-lift decisions above have executable witnesses and frozen semantic hashes.  The final global U6 singleton equality and the exact chromatic value above ten are not claimed.
