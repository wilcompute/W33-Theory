# Physical FI Alt(5) prime-shadow torsor theorem

The newest cross-repository FI bridge supplies the exact physical five-star vector
[
v=(-5,3,1,-5,6),qquad sum_i v_i=0.
]
This note records a new finite theorem about that measured vector, not a new fit.

## Integral orbit

The coordinate Weyl group of the hypercharge-orthogonal charge sector is (S_5).
The vector has exactly one repeated value, the two (-5)'s, so its (S_5)
stabilizer is the transposition exchanging those positions. That reflection is odd.
Consequently the alternating subgroup has trivial stabilizer:
[
|operatorname{Alt}(5)cdot v|=60=|operatorname{Alt}(5)|.
]
Thus the 60 integral FI orientations form a regular (operatorname{Alt}(5)) torsor.

The vector lies on exactly one (A_4) Weyl wall. Its simple-root coordinates are
[
(-5,-2,-1,-6)=3(-5/3,-2/3,-1/3,-2),
]
which independently recovers the physical coefficients imported from Holotrade.

## Prime shadows

After factoring out the baseline repeated (-5), the distinct values are
[
-5,1,3,6.
]
Their Vandermonde product is
[
6cdot8cdot11cdot2cdot5cdot3
=15840=2^5,3^2,5,11.
]
Therefore only (p=2,3,5,11) create new coordinate collisions. Exhaustive
enumeration of (S_5) and (operatorname{Alt}(5)) gives:

| prime | residue multiplicities | Alt(5) stabilizer | quotient orbit | integral fiber |
|---|---:|---:|---:|---:|
| 2 | 4+1 | (A_4), 12 | 5 | 12 |
| 3 | 3+2 | (S_3), 6 | 10 | 6 |
| 5 | 2+2+1 | (C_2), 2 | 30 | 2 |
| 11 | 3+1+1 | (C_3), 3 | 20 | 3 |

For tested primes outside this collision set, the regular 60-state torsor remains
free.

The (p=3) shadow is especially clean:
[
vmod3=(1,0,1,1,0).
]
It selects a (3+2) partition of the five star coordinates, and its ten-element
orbit is exactly the set of three-subsets (equivalently two-subsets) of a
five-set:
[
10=inom53=[S_5:S_3	imes S_2].
]
Each partition has six integral FI lifts.

## Physics boundary

This (3+2) selector lives in the **Abelian** hypercharge-orthogonal (A_4)
charge module inside the (u(1)^5) center. The flagship Wilson-line theorem also
contains a non-Abelian (SU(5)) block, but these are different objects. The
shared (S_5/(S_3	imes S_2)) combinatorics is therefore recorded as a target for
an explicit intertwiner, not as a proved gauge-breaking identification.

Likewise (11=k-1) is W33's nonbacktracking branching number. The fact that 11 is
also an FI collision prime is exact, but it is not promoted to a physical bridge
without an operator-level map.
