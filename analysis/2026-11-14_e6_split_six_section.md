# A split E6 shear isolates one six-coordinate section

The [double-six result for packet words](2026-11-14_e6_packet_section_pairing.md) extends to every orthogonal cubic symmetry that preserves a coordinate six-section. Removing orthogonality gives an exact counterexample. The construction uses the split E6 root matrices whose [parallel parabolic calculation](2026-11-13_E6_generalized_gauge_USp8_full_clock_Z2.md) found the full 57-dimensional six-section stabilizer.

## Orthogonal obstruction

Let T be the signed symmetric cubic tensor, with entries of magnitude one on the 270 ordered support triples. For a real section S and an orthonormal basis e_a of S, define

    H(S) = sum_a T(e_a, ., .) T(e_a, ., .)^T.

This operator is independent of the orthonormal basis. Orthogonal cubic transformations send it to the conjugate operator for the transformed section. In the coordinate chart it is diagonal because the slice at a coordinate index is a signed matching. For all 72 coordinate six-sections its spectrum, with multiplicities, is 0 (6), 2 (15), 5 (6). The zero space is S. The eigenvalue-five space is its Schlaefli partner, as each of those six coordinates meets five of the six indices of S. An orthogonal cubic symmetry fixing S must preserve the partner as a subspace, even when the symmetry mixes coordinate axes. The compact stabilizer dimensions are 15 for the six-section and 11 for the five-section, in agreement with the earlier parabolic calculation.

## Noncompact witness

In the exact root order of the repo, take R = root 2. Its only entries, as (row, column, value), are

    (0,14,-1), (1,19,1), (3,21,-1), (4,23,1), (7,25,1), (11,26,1).

The verifier checks R squared is zero, the infinitesimal cubic identity, and the finite cubic identity for U = I+R. The six-section A = (3,4,7,8,17,24) is fixed pointwise. Its partner B = (9,10,13,14,19,26) moves. Adjoin U to the previously verified compact tuple whose only maximal invariant sections are A and B. The separating involutions still force all common invariant real subspaces to be coordinate. The augmented tuple has exactly one invariant maximal real section, A. It is realizable on the same open strip by adding a face with top link U inverse. These are prescribed split-group holonomies. Whether an action and boundary data select them remains open. [Exceptional field theory](https://arxiv.org/abs/1312.0614)

## An action degeneracy with an explicit diagnostic

The shear has trace 27 and nonzero square distance 6 from identity in the reference positive metric. Thus the trace action adds zero for this nonflat face and gives the same score before and after breaking the pairing. For a positive metric G on the common base-point fiber, the quantity Tr[G^{-1}(U-I)^T G(U-I)] is nonnegative, vanishes exactly for identity, and is invariant when U is conjugated and G is transported by inverse congruence. It equals 6 at G=I in this example. This distinguishes the two prescribed tuples when their common positive metric is specified. Selecting the metric and deriving its coupling require dynamics.

## Parallel attractor check

[Pass 12665](PASS12665_ATTRACTORS_ARE_PURE_STATES.md) identifies the pure-state charge orbit and reports numerical attractor flows. Its mixed-state upper bound N <= 1 follows directly from the spectral formula, with no convexity assumption. For the four quaternionic eigenvalues x of X, one has -1 <= x <= 3 and their sum is zero. The identity 7x + 6 - x^3 = (3-x)(x+1)(x+2) is nonnegative on that interval. Summing gives N = sum x^3/24 <= 1. Equality forces one x=3 and three x=-1, which is the stated quaternionic-line support condition. This supplies a proof of that part of the parallel calculation. The spectral truncation observed along the numerical flows is a separate claim.

Replay with py -3 analysis/toe_20261114_e6_split_six_section.py.
