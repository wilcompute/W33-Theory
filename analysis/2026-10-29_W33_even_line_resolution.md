# W(3,q) binary incidence resolution: line parity, CSS logical space, and mod-four boundary

**Date:** 2026-10-29. **Status:** independently executable finite-geometry computation for prime q=3,5,7; conditional general-q statement below. **Physical status:** no physical realization, parameter prediction, or TOE claim.

## Position in the repository

The October 29 `af1a7ee05` / `923c4eb20` commits certify the binary adjacency CSS family and, at q=3, [[40,8,6]]. Earlier `analysis/2026-07-10_levi_five_frontiers.md` and related work already described the eight-dimensional plus-type orthogonal module and its E8/2E8 relation. **These established results are not claimed as new.** The present artifact adds an explicit incidence-to-kernel resolution, verifies it at q=3,5,7, and isolates a mod-four condition on the natural Hamming refinement.

## Exact identity and resolution

Let N be point-by-totally-isotropic-line incidence and A be point collinearity adjacency on W(3,q). Both are square of size v=(q+1)(q²+1). A point on a line is collinear with the q other points of that line; a point off a line is collinear with exactly one point on it (the generalized-quadrangle axiom). Hence, **over the integers**,

    A N = J + (q-1) N,
    N N^T = A + (q+1) I.

For odd q, reducing mod 2 gives A N = J, A = N N^T, and the strongly-regular-graph identity gives A²=0. Thus every isotropic line indicator has the same all-ones syndrome, and every even sum of line indicators lies in ker A.

For q=3,5,7 exact row-reduction yields rank_2(N)+rank_2(A)=v+1. The even-line span has rank rank_2(N)-1: any relation among line columns has even coefficient parity because its A-image is J times that parity. The kernel has dimension v-rank_2(A)=rank_2(N)-1. Therefore

    ker_2(A) = { N y : sum(y) = 0 mod 2 }.

And the CSS logical homology is H=ker(A)/im(A), dimension v-2 rank(A)=q²-1 in all three checked cases.

**General-q boundary:** the combinatorial identities hold for all odd prime powers q. The exact kernel-resolution equality at arbitrary odd prime powers follows if the corresponding binary rank-complement identity holds; this script itself verifies q=3,5,7 (prime), not every prime power.

## Quadratic refinement and its obstruction

Since A N=J, the all-ones vector lies in im A, so every vector of ker A has even weight. The quadratic function Q(x)=wt(x)/2 mod 2 has polar form the ordinary binary dot product on the even-weight subspace. It descends to the quotient H iff the stabilizer im A is doubly even.

Every adjacency row has weight q(q+1), and its intersection with any other row has size q-1 or q+1, both even. Therefore im A is doubly even precisely when q ≡ 3 mod 4. For q ≡ 1 mod 4 the generators themselves have weight 2 mod 4, so the unmodified Hamming quadratic form is not well defined on H.

Exact Arf computations for q=3 and q=7 both give plus type; for q=3, H has 136 singular vectors (including zero) and 120 nonsingular vectors, agreeing with the already known E8/2E8 finite quadratic-space type. This matching does **not** provide a canonical E8 lattice isomorphism, a Hamiltonian, or an experimentally validated physical claim.

## Reproduction

    python analysis/w33_incidence_even_line_resolution_20261029.py
    python -m unittest discover -s tests -p test_w33_incidence_even_line_resolution_20261029.py -v

Python standard library only. The producer emits `data/w33_incidence_even_line_resolution_20261029.json`. No existing artifacts are overwritten other than this producer's own deterministic output.
