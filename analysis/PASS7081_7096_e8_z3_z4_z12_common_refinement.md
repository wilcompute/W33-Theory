# Passes 7081–7096 — CE2 and Kummer are adjacent gradings of one E8

## Executive result

Two previously separate lanes now meet inside one explicit E8 root system.

The repo's native CE2/E8 decomposition is the order-three grading

\[
\mathfrak e_8=(\mathfrak e_6\oplus\mathfrak{sl}_3)
\oplus(27\otimes3)\oplus(27^*\otimes3^*)
\]

with dimensions

\[
\boxed{86+81+81=248}.
\]

The Kummer/spinor-tenfold lane uses the order-four grading

\[
\mathfrak e_8=(\mathfrak{so}_{10}\oplus\mathfrak{sl}_4)
\oplus(16\otimes4)\oplus(10\otimes6)\oplus(16^*\otimes4^*)
\]

with dimensions

\[
\boxed{60+64+60+64=248}.
\]

An independent enumeration of all 240 E8 roots shows that these are induced by **adjacent simple-root coefficients** of highest-root marks 3 and 4.  The two toral automorphisms therefore commute and refine to

\[
\boxed{\mathbb Z_4\times\mathbb Z_3\cong\mathbb Z_{12}}.
\]

The complete joint dimension table is

\[
\boxed{
\begin{array}{c|ccc}
 &0&1&2\\\hline
0&54&3&3\\
1&16&48&0\\
2&0&30&30\\
3&16&0&48
\end{array}}
\]

with rows indexed by `Z4` and columns by `Z3`.

## Pass7081 — one E8 root certificate

The verifier reconstructs the 240 E8 roots in doubled coordinates:

- 112 integral roots of the form `±2e_i±2e_j`;
- 128 half-integral-type roots represented as eight `±1` coordinates with even minus parity.

A generic linear functional determines a positive system and eight indecomposable simple roots.  In the deterministic ordering used by the script, the highest-root marks are

\[
\boxed{(4,6,5,4,3,2,2,3)}.
\]

The relevant mark-4 node is index 3 and the relevant mark-3 node is index 4.  They are adjacent in the recovered E8 Dynkin diagram.

The script deliberately records the actual simple-root coordinates and indices so that a change of root ordering cannot silently corrupt the grading certificate.

## Pass7082 — deleting the mark-3 node recovers CE2

Taking the coefficient of simple root 4 modulo three partitions the full E8 algebra into dimensions

\[
\boxed{86,81,81}.
\]

The grade-zero roots form exactly

\[
\boxed{E_6+A_2}.
\]

Thus the grading is the standard trinification decomposition

\[
(78,1)+(1,8)\mid(27,3)\mid(27^*,3^*).
\]

This independently recovers the representation carrier used by the repo's native CE2 construction.

## Pass7083 — deleting the adjacent mark-4 node recovers the Kummer spinor grading

Taking the coefficient of the adjacent simple root 3 modulo four gives

\[
\boxed{60,64,60,64}.
\]

The neutral root subsystem is

\[
\boxed{D_5+A_3},
\]

so the standard representation dimensions are

\[
(45,1)+(1,15)
\mid(16,4)
\mid(10,6)
\mid(16^*,4^*).
\]

This is the E8 grading appearing in the spinor/Kummer lane: the half-spin 16 and the `SL4` four-space occupy the 64-dimensional odd sectors.

## Pass7084 — exact common refinement

Because both gradings come from diagonal toral actions, they commute.  Classifying every root by the pair

\[
(c_4\bmod4,c_3\bmod3)
\]

gives the exact `4 x 3` table

\[
\begin{array}{c|ccc}
 &0&1&2\\\hline
0&54&3&3\\
1&16&48&0\\
2&0&30&30\\
3&16&0&48.
\end{array}
\]

The row sums recover the Kummer grading:

\[
60,64,60,64,
\]

and the column sums recover CE2:

\[
86,81,81.
\]

Nothing is fitted: the table is obtained by enumerating the E8 roots once and reducing two integer simple-root coefficients.

## Pass7085 — the common neutral algebra is `so10 + sl3 + u1`

The doubly neutral cell contains 46 roots.  Their semisimple root system is

\[
\boxed{D_5+A_2}
\]

of rank seven.  Since the two gradings live in rank-eight E8, one Cartan direction remains central in the common fixed algebra.  Therefore

\[
\boxed{\mathfrak g_{(0,0)}\cong
\mathfrak{so}_{10}\oplus\mathfrak{sl}_3\oplus\mathfrak u_1}
\]

at the level of complexified/reductive Lie algebras, with dimension

\[
45+8+1=54.
\]

This common fixed algebra is a concrete meeting point between the qutrit/CE2 and Kummer/spinor coordinate systems.

## Pass7086 — the 81 splits into `48+30+3`

The CE2 grade-one sector is `27 x 3`.  Under `D5 x u1`, the E6 fundamental branches dimensionally as

\[
27=16+10+1.
\]

Tensoring by the surviving `3` gives

\[
\boxed{81=48+30+3}.
\]

The joint table exhibits this split directly in root space.  The conjugate 81 column is the mirror `3+30+48`.

This is especially useful for the CE2 program because the old 81-dimensional grade is no longer an indivisible carrier: the Kummer-compatible refinement separates it into spinor, vector, and singlet-sized channels.

## Pass7087 — the Kummer 64 splits into `48+16`

Conversely, the Kummer order-four sector

\[
16\otimes4
\]

meets the CE2 `A2` structure through

\[
4\to3+1,
\]

so

\[
\boxed{64=48+16}.
\]

The central `48=16 x 3` therefore appears simultaneously as:

- the half-spin part of `27 x 3` on the CE2 side;
- the triplet part of `16 x 4` on the Kummer side.

This is a substantially stronger structural overlap than a shared dimension alone, because both embeddings are fixed inside the same E8 root decomposition.

## Pass7088 — CRT produces a genuine Z12 grading

Since `gcd(4,3)=1`, the pair of grades is equivalent by the Chinese remainder theorem to one grade modulo 12.  In residue order `0,...,11`, the sector dimensions are

\[
\boxed{54,48,30,16,3,0,0,0,3,16,30,48}.
\]

They sum to 248 and display the conjugation symmetry expected from root negation.

The zero sectors at residues 5, 6 and 7 are not assumptions; no E8 roots/Cartan components occupy those joint congruence classes.

## Pass7089 — relation to the repo's independent mu12 theorem

The photonic/Clifford lane independently proves that the scalar phase group of the qutrit Clifford construction is

\[
\mu_{12}.
\]

The present E8 result produces a cyclic **grade group** `Z12`.  These are not the same kind of object:

- `Z12` here labels E8 root-space eigenspaces of an order-12 automorphism;
- `mu12` there is a scalar phase subgroup acting on qutrit Clifford matrices.

The fact that both have order 12 is therefore only a new target, not an identification.  A genuine bridge would require an explicit character

\[
\mathbb Z_{12}\to\mu_{12},\qquad n\mapsto\zeta_{12}^{kn},
\]

together with a proof that the Holonet/Clifford action on the relevant E8-derived carrier realizes that character.

## Pass7090 — why the Kummer bridge matters here

Pass7065 identified the `[16,6,6]` bent biplane with the abstract Kummer `16_6` configuration.  The recent spinor-tenfold literature obtains that Kummer combinatorics from a half-spin representation inside an E8 grading.

The present root calculation shows exactly where that grading sits relative to the repo's older E6+A2/CE2 grading: the grading nodes are adjacent and have coprime orders four and three.

That explains, structurally, why the Kummer lane can refine rather than compete with the qutrit lane.

## Pass7091 — a new CE2 route

The strongest next use is not to fit the 5,832 CE2 signs to twelve labels.  It is to push the actual CE differential/bracket through the joint E8 decomposition and ask which of the six nonzero Z12 sector sizes

\[
48,30,16,3,3,16,30,48
\]

carry the simple-family and fiber-family repair terms.

If the bracket respects the Z12 grading, every nonzero CE2 row acquires a representation-theoretic selection rule before any sign fitting occurs.  That would attack the blind-replay problem from the algebra rather than the answer table.

## Pass7092 — a new K3 route

On the Kummer side, the joint neutral `D5+A2+u1` algebra supplies a natural place to compare the half-spin 16-node configuration with the qutrit triplet structure.  A projective Kummer/K3 realization labeled by the sixteen half-spin weights could therefore be tested against the same joint grading before any attempt is made to map it into the 45-point curvature precomplex.

This provides a much more constrained K3 chain-map search than a raw `2428 x 36` matrix hunt.

## Pass7093–7096 — strict evidence boundary

Closed by exact root enumeration:

- E8 Z3 grading `86+81+81`, neutral `E6+A2`;
- E8 Z4 grading `60+64+60+64`, neutral `D5+A3`;
- adjacency of the mark-3 and mark-4 grading nodes;
- exact joint `4 x 3` dimension table;
- common neutral `D5+A2+u1`, dimension 54;
- CRT Z12 grading with dimensions `54,48,30,16,3,0,0,0,3,16,30,48`.

Not claimed:

- that the E8 Z12 grading equals the qutrit Clifford scalar phase group `mu12`;
- that the Z12 refinement by itself solves CE2 signs;
- that it realizes a K3 curvature map;
- that it is a Vogel-universal object.

The new theorem is narrower and stronger:

\[
\boxed{\text{the repo's CE2 Z3 and Kummer Z4 structures admit one exact common Z12 refinement inside E8}.}
\]
