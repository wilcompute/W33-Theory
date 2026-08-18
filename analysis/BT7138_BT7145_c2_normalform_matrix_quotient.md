# Passes 7138–7145 — C2 normal form, eight Gram cases, rank-one idempotents, quotient spectrum, and a semilinear hexad

## Scope

This packet executes the five attacks left by Pass7130–7137 and three deliberately orthogonal probes.  Everything labelled theorem below is finite algebra/combinatorics replayed by `analysis/w33_pass7138_7145_c2_normalform_matrix_quotient.py`.  The proposed all-q quotient **spectrum** is deliberately left as a conjecture: it matches q=3,5,7,9, but four anchors are not a proof.  Nothing here proves `alpha(W(3,9))=51`.

## Pass7138 — put the involution in the right coordinates

For the q=9 stabilizer involution, choose dual Lagrangian bases

```
E+ = [(5,4,1,0), (1,5,0,1)]
E- = [(0,6,6,6), (0,6,8,8)]
```

so that

```
A = diag(I2,-I2)
B((u,w),(u',w')) = u·w' - w·u'.
```

The recovered 51-set is exactly one fixed point (graph index 80) plus 25 two-cycles.  Each two-cycle lies on a unique projective line joining one point of `P(E+)` to one point of `P(E-)`.  On a non-isotropic transversal, the q-1 internal points are paired by `t <-> -t`, giving `(q-1)/2` possible involution-pairs.

This is the clean structural model that the raw 51 coordinates were hiding.

## Pass7139 — the 52 problem is eight 48-clique problems on 512 states

A rank-four alternating Gram matrix has a nonsingular four-point principal block.  For a hypothetical 52-set, choosing such four anchors reduced 1326 off-diagonal pairings to 198 field entries in Pass7132.

There is another exact quotient.

Independent projective rescaling of the 48 remaining points normalizes one anchor pairing in each row.  The four anchor rescalings, an ambient symplectic-similitude multiplier, anchor permutation and Frobenius reduce the nonzero nonsingular anchor block to one of exactly eight q=9 matching-product types:

```
(1,1,2) (1,1,3) (1,1,4) (1,1,5)
(1,2,3) (1,2,4) (1,3,4) (1,3,5)
```

For a fixed type every further point is represented by

```
r = (1,a,b,c),  a,b,c in GF(9)^*,
```

so there are exactly `8^3 = 512` states.  Two states are compatible iff

```
-r G^{-1} s^T != 0.
```

Hence a 52-point partial ovoid exists iff at least one of these eight compatibility graphs contains a 48-clique.  Their edge counts are 116412, 116421 or 116430 depending on anchor type; every vertex degree lies between 448 and 456.

The live 51-witness uses anchor positions `(0,1,2,5)`, whose canonical type is `(1,3,5)`, and its remaining 47 points give an explicit 47-clique.  Thus the reduction is calibrated against a real witness rather than an abstract coordinate count.

**Boundary:** this packet does not prove that the eight graphs have clique number 47.  The target-48 decision remains open.

## Pass7140 — all-q involution theorem

Let q be odd and let `g` be a non-scalar projective involution represented by a symplectic similitude with `g^2=I` and multiplier `-1`.

For `x,y` in the same eigenspace,

```
B(gx,gy)=B(x,y)
```

from the eigenvalue, but also

```
B(gx,gy)=-B(x,y)
```

from the multiplier.  Hence each eigenspace is totally isotropic.  In dimension four both eigenspaces therefore have dimension two, so the complete fixed projective locus is two disjoint generator lines.

Consequences:

- fixed points: `2(q+1)`;
- a partial ovoid can use at most one point from each fixed line;
- an odd-sized g-invariant partial ovoid must contain exactly one fixed point;
- nonfixed projective points form `(q-1)(q+1)^2/2` involution orbits;
- `(q^2-1)/2` of those orbits are internally collinear and unusable;
- `q(q^2-1)/2` are admissible weight-two orbit carriers;
- there are `q(q+1)` non-isotropic transversals and `(q-1)/2` internal orbit labels per transversal.

This theorem explains simultaneously the `1+25*2` q=9 witness and `1+16*2` q=7 control pattern without fitting either cardinality.

## Pass7141 — the C2 quotient has closed all-q counts

Collapse each fixed point to a weight-one quotient node and each admissible nonfixed involution pair to a weight-two node.  Two quotient nodes conflict when any constituent points are collinear.

The selectable quotient has

```
2(q+1)                     fixed nodes
q(q^2-1)/2                 pair nodes
```

with valencies

```
d_fixed = (q^2+q+2)/2
d_pair  = (2q^2-q+3)/2.
```

The edge classes are

```
fixed-fixed : (q+1)^2
fixed-pair  : q(q^2-1)
pair-pair   : q(q^2-1)(2q^2-q-1)/8.
```

At q=7 this gives 184 nodes, 4180 edges and degrees 29/47.  At q=9 it gives 380 nodes, 14500 edges and degrees 46/78 exactly.

### Spectrum frontier — intentionally conjectural

Exact adjacency builds at q=3,5,7 and GF(9) show the same spectrum pattern.  Besides two simple roots of

```
2x^2 -(2q^2+q+1)x +(2q^3-q^2-1)=0,
```

the candidate eigenvalues/multiplicities are

```
 q-1       : (q+1)(q^2-3q+4)/4
-(q+1)     : q(q-3)(q-1)/4
-(q+3)/2   : q(q+1)/2
 (q-1)/2   : (q-1)(q+2)/2
 0         : q(q-3)/2
-(q-1)     : q.
```

The formulas sum to the exact quotient-node count, and the q=3,5,7,9 spectra reproduce them including the q=5 eigenvalue collision.  They are recorded as a sharp all-q target, **not a theorem**.

## Pass7142 — the quadratic-character switching objects are rigid

For q=9, `Q_ij = chi(B(v_i,v_j))` is a symmetric 51x51 Seidel matrix of rational rank 51.  It is not conference.  The switching-invariant pair color

```
c_ij = Q_ij (Q^2)_ij
```

has colored-graph automorphism group of order exactly two.  The known projective involution lifts to the nontrivial signed switching automorphism, so the extended switching group is exactly `C2`.

For q=7 the sign matrix is skew-symmetric of exact rank 32.  The absolute pair colors `|(Q^2)_ij|` again have automorphism group two; the projective involution acts as an **anti-switching** symmetry, carrying Q to minus a diagonal switch of Q.  This sign change is exactly what the nonsquare similitude multiplier predicts.

This is finite-field switching algebra.  It is not promoted to a physical handedness statement.

## Pass7143 — bonkers #1: the carriers are rank-one idempotents in M2

In the dual-Lagrangian normal form, a non-isotropic transversal is specified by endpoint lines `[u]` and `[w]` with `u·w != 0`.  Normalize the rank-one outer product:

```
E = w u^T / (u·w).
```

Then

```
tr(E)=1,
E^2=E,
rank(E)=1.
```

Conversely every rank-one trace-one idempotent determines exactly one non-isotropic transversal.  Therefore the transversal carrier is the GL2 conjugacy class of rank-one idempotents in `M2(F_q)`, of size

```
q(q+1).
```

At q=9 there are exactly 90 such idempotents and the 51-witness selects 25 distinct ones.  The q=7 control selects 16 distinct transversals.

This is a real interface to the repo's earlier M2/rank/Fourier program, but the objects must not be collapsed: the earlier nonzero rank-one Fourier sector has `(q-1)(q+1)^2` matrices.  At q=2 the new carrier has six trace-one rank-one idempotents, whereas the full rank-one sector has nine matrices.  The numerical six also must not be confused with the six units: idempotents here have rank one; units have rank two.

## Pass7144 — bonkers #2: A and Frobenius generate a D12 hexad of 51-witnesses

Let `F:x->x^3` be the field automorphism of GF(9).  On the full 820-point geometry, the projective involution A and F generate a permutation group of order 12, with

```
A^2=F^2=1,
order(AF)=6.
```

Thus the generated group is dihedral of order 12.

Its orbit on the recovered 51-set has six distinct partial ovoids.  Every one has size 51, and astonishingly **every one of the 15 pairwise intersections has size four**.  Their union has 248 points with incidence multiplicities

```
192 points in one witness,
54  points in two witnesses,
2   points in three witnesses.
```

The two triple points are graph indices 50 and 80.  Three hexad members contain 50 and not 80; the complementary three contain 80 and not 50.  Pairwise binary incidence distance is 94.

This generalizes the single Frobenius-pair intersection `|S cap F(S)|=4` from Pass7135 into a closed six-object semilinear configuration.

## Pass7145 — bonkers #3: the hexad is a binary [248,6,51] code

Take the six hexad incidence vectors and puncture away the 572 coordinates absent from their union.  The six generators have integer Gram matrix

```
47 I_6 + 4 J_6,
```

because every word has weight 51 and every pair intersects in four points.  Hence its eigenvalues are `71^1 + 47^5`; modulo two the Gram matrix is exactly `I_6`, so the six words are linearly independent.

The resulting binary code is

```
[248,6,51]
```

with weight enumerator

```
1
+ 6 z^51
+ 15 z^94
+ 18 z^129
+ 2 z^133
+ 9 z^156
+ 6 z^160
+ 6 z^179
+ z^194.
```

This is a coding-theoretic object extracted from the semilinear witness orbit, not an identification with any existing CSS code in the repo.

## Literature / provenance boundary

The q=7 value 33 is a positive control against the exhaustive generalized-quadrangle computations of Cimrakova and Fack and related 2007 work.  The modern large-partial-ovoid construction of Ceria–De Beule–Pavese–Smaldore treats odd-square W(3,q) under hypotheses excluding q divisible by 3, so it does not supply the present q=9 witness.  Targeted searches did not locate the exact C2-normal-form/idempotent/D12-hexad package above; this is **not** a formal novelty proof.

The M2 interface is checked against Pass5848–5855: that packet's full rank-one Fourier sector and determinant/unit partition remain exactly as stated there.  Pass7143 introduces the smaller trace-one idempotent conjugacy class and explicitly firewalls the two objects.
