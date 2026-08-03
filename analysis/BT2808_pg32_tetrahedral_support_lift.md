# BT2808 — PG(3,2) tetrahedral support lift / tomotope equitable quotient

## Result

BT805 ended with an explicit open boundary:

> the W33 lift: W(3,3)'s 40 = PG(3,3) points vs the tetrahedral PG(3,2)
> ground — the q=2 vs q=3 ladder.

Pass 2808 closes that boundary by an exact support projection.

Let the 15 binary tetrahedral cells be the nonzero masks

\[
S\in\mathbb F_2^4\setminus\{0\},
\]

with Hamming weights \(1,2,3,4\) corresponding to the tetrahedron's vertices,
edges, faces, and body. Let the 40 W33 points be the projective classes

\[
[x]\in PG(3,3),\qquad x\in\mathbb F_3^4\setminus\{0\}.
\]

Define

\[
\pi([x])=\operatorname{supp}(x)\in\mathbb F_2^4\setminus\{0\}.
\]

This is well-defined because multiplying \(x\) by the only nontrivial projective
scalar, \(-1\), does not change its support.

## 1. Exact fiber law

For a nonempty support mask \(S\),

\[
\boxed{|\pi^{-1}(S)|=2^{|S|-1}.}
\]

There are \(2^{|S|}\) assignments of nonzero ternary coordinates on \(S\), and
projectivization identifies each assignment with its negative.

Consequently the tetrahedral rank census

\[
4,\ 6,\ 4,\ 1
\]

lifts to

\[
\boxed{
4\cdot1,\quad6\cdot2,\quad4\cdot4,\quad1\cdot8
=
(4,12,16,8).
}
\]

Thus the tomotope f-vector already used throughout the repository is the exact
**phase-capacity profile** of the ternary projective lift of the binary
tetrahedron:

\[
\boxed{(4,12,16,8).}
\]

This is stronger than a numerical coincidence: every tetrahedral \(k\)-cell
supports exactly \(2^k\) ternary projective phase classes.

## 2. The support fibers are equitable for W33

Choose one of the three perfect matchings of the four tetrahedral vertices,

\[
(01)(23),\qquad(02)(13),\qquad(03)(12),
\]

and use it to write a standard nondegenerate alternating form on
\(\mathbb F_3^4\). For all three choices the support fibers form an equitable
partition of the W33 collinearity graph.

Let \(Q\) be the \(15\times15\) quotient and let

\[
s_S=|\pi^{-1}(S)|=2^{|S|-1}.
\]

Then every row of \(Q\) sums to \(12\), and exact arithmetic gives

\[
\boxed{\operatorname{spec}(Q)=12^1\oplus2^9\oplus(-4)^5.}
\]

The full W33 spectrum is

\[
12^1\oplus2^{24}\oplus(-4)^{15},
\]

so the 40-point space separates into

\[
\boxed{
\text{binary-support sector: }15=1+9+5
}
\]

and

\[
\boxed{
\text{internal ternary-phase sector: }25=15+10.
}
\]

The residual spectrum is therefore

\[
\boxed{2^{15}\oplus(-4)^{10}.}
\]

The quotient satisfies two exact identities:

\[
\boxed{\operatorname{diag}(s)Q=Q^{\mathsf T}\operatorname{diag}(s)}
\]

and

\[
\boxed{Q^2=8I-2Q+4\mathbf1s^{\mathsf T}.}
\]

The first is weighted reversibility; the second is the SRG closure law after
compression to the nonuniform support fibers.

## 3. Closed entry formula

Let \(\tau\) be the involution induced by the chosen perfect matching. For
nonempty masks \(S,T\), put

\[
r=|T\cap\tau(S)|,\qquad t=|T|.
\]

Let

\[
c_r=\#\left\{\epsilon\in\{\pm1\}^r:
\sum_i\epsilon_i=0\pmod3\right\},
\]

so

\[
(c_0,c_1,c_2,c_3,c_4)=(1,0,2,2,6).
\]

Then all 225 quotient entries are given by

\[
\boxed{
Q_{S,T}=2^{t-r-1}c_r-\delta_{S,T}.
}
\]

The verifier checks this formula entry-by-entry for all three symplectic
pairings.

## 4. Why the repository keeps seeing \(24=8\cdot3\)

The tetrahedron has symmetry group \(S_4\) of order \(24\). It acts transitively
on the three perfect matchings above. The stabilizer of one matching has order
\(8\), is nonabelian, and has element-order census

\[
1^1\,2^5\,4^2,
\]

hence it is \(D_8\). Therefore

\[
\boxed{24=8\cdot3=|S_4|=|D_8|\,[S_4:D_8].}
\]

This gives an intrinsic tetrahedral source for the earlier selector split
\(24=8\cdot3\): the eightfold layer is the stabilizer of a symplectic
coordinate pairing and the threefold layer is the choice of pairing.

There is a second exact hit. The four Type-A masks in the selector stack,

```text
1110, 1101, 1011, 0111,
```

are exactly the four weight-three masks, hence exactly the four tetrahedral
faces. Pairing four faces with three symplectic matchings gives

\[
\boxed{4\cdot3=12}
\]

face-pairing charts, matching the 12 admissible Type-A/Fano sheets of BT723.

## 5. Engineering interpretation

The support mask is a four-bit coarse address for a four-trit Pauli-frame
state. The fiber size records how many ternary sign/phase variants share that
binary occupancy pattern:

| tetrahedral role | masks | phase classes per mask | total W33 points |
|---|---:|---:|---:|
| vertex | 4 | 1 | 4 |
| edge | 6 | 2 | 12 |
| face | 4 | 4 | 16 |
| body | 1 | 8 | 8 |

This supplies a natural two-stage decoder:

1. decode the 15-state binary support shell;
2. decode the 25-dimensional within-fiber ternary phase residual.

It is a concrete candidate for a support-first frame codec in the Holonet
machine, not merely a visualization.

## Evidence boundary

Three distinctions are mandatory.

1. \(\pi\) is a combinatorial projective support partition. It is not a field
   homomorphism and not a linear reduction \(\mathbb F_3^4\to\mathbb F_2^4\).
2. The exact equality \((4,12,16,8)\) proves a fiber-capacity theorem. It does
   not by itself prove that the quotient incidence object is the abstract
   tomotope.
3. The 12 face-pairing charts reproduce the selector parameter set and group
   factorization. An objectwise intertwiner to the existing \(2160\times160\)
   selector matrices remains to be constructed.

## Reproduce

```bash
python analysis/bt2808_pg32_tetrahedral_support_lift.py
python analysis/bt2808_freeze.py
pytest -q tests/test_bt2808_pg32_tetrahedral_support_lift.py
```

The frozen certificate is:

```text
data/PART_BT2808_PG32_TETRAHEDRAL_SUPPORT_LIFT_results.json
```

## External anchors

- Nicolas Magaud, *Proof Pearl: Formalizing Spreads and Packings of the
  Smallest Projective Space PG(3,2) Using the Coq Proof Assistant*,
  LIPIcs ITP 2022, DOI 10.4230/LIPIcs.ITP.2022.25.
- Giovanni Falcone and Marco Pavone, *Kirkman's Tetrahedron and the Fifteen
  Schoolgirl Problem*, American Mathematical Monthly 118 (2011), 887–900,
  DOI 10.4169/amer.math.monthly.118.10.887.

Both sources use the 15-point/35-line PG(3,2) substrate; Falcone–Pavone
explicitly realize its points as the 15 simplicial elements of a tetrahedron.
