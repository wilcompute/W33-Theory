# The signed cubic realizes the E6 Tits group

Pass 12655 proved that the signed monomial group of the repository cubic has order 3,317,760 and left its identification with the Tits group open. The native 27-dimensional Chevalley representation supplies the missing map. The recent exceptional-field-theory section calculations supply the two kinds of maximal coordinate sections. Here we compute the action of the integral signed group on both sections, including the sign information invisible to the Weyl permutations.

For each root matrix `e`, the code recovers the coroot `h = [e, eᵀ]`. The six simple roots in a fixed generic positive chamber give `nᵢ = (I + eᵢ)(I − eᵢᵀ)(I + eᵢ)`.
The root matrices square to zero, so these factors are the Chevalley exponentials at `1, −1, 1`. Each lift is an integral signed permutation preserving the exact cubic. The code verifies the E6 Cartan matrix, the braid relations, torus conjugation, and `nᵢ² = hᵢ(−1)`. The six square masks generate 64 diagonal signs. The unsigned permutations generate 51,840 elements. The Chevalley construction defines a homomorphism from the abstract Tits group, whose order is 64 × 51,840. The two verified orders force its image to have that order, so the map is faithful and exhausts the signed group counted in Pass 12655. [Adams and He, Lifting of elements of Weyl groups](https://arxiv.org/abs/1608.00510).

| Coordinate section | Orbit | Signed setwise stabilizer | Image on the section | Pointwise kernel |
| --- | ---: | ---: | --- | --- |
| IIB, dimension 5 | 216 | 15,360 | All determinant +1 signed permutations, order 1,920 | Dihedral group of order 8 |
| M, dimension 6 | 72 | 46,080 | All signed permutations, order 46,080 | Trivial |

The IIB image ties the parity of the sign flips to the permutation parity. This is an orientation condition on the coordinate five-space. The eight-element kernel has exactly two elements of order four and five involutions, identifying it as dihedral. Four kernel elements are diagonal. The unsigned stabilizer had an additional permutation fixing the five coordinates individually, and its signed lifts account for the other four kernel elements. The six-space action has no such ambiguity.

This result concerns the finite integral subgroup acting on the repository's coordinate section representatives. The connected ExFT stabilizers and the continuum embeddings of the two sections use additional structure. [Repository parallel report](2026-11-13_E6_generalized_gauge_USp8_full_clock_Z2.md) · [Hohm and Samtleben, Exceptional Field Theory I](https://arxiv.org/abs/1312.0614).

Replay with `py -3 analysis/toe_20261113_e6_tits_coordinates.py`. The resulting certificate records the six signed matrices and the section counts.
