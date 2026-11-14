# One exact witness for both five-qubit regulus quotients

Pass 12659 proves that restricting a parent state to a Pauli eigenspace preserves the dimension-scaled certainty objective on the corresponding quotient. Pass 12660 found a six-qubit low-value candidate with an order-four Pauli stabilizer. The two observations combine constructively: two elements of the stabilizer represent the two inequivalent five-qubit quotients. One state therefore supplies the same exact bound for the parent and both quotients. [Quotient lemma](PASS12659_REGULUS_CONSTANTS_CHAR2_MECHANISM_CERTAINTY_RELATIONS.md) · [Saved numerical candidate](PASS12660_VALIDATED_TYPE_B_BOUND_STABILISER_GAP_AT_Q8_CENSUS.md)

## Why there are two quotient point types

Represent the phase space by 2-by-2 matrices over F8 with Q equal to the determinant. Left and right multiplication by SL(2,8) preserve the determinant and the family of Lagrangians in the chosen ruling. In particular, a matrix in one member of the ruling has its rows in a specified common line, and right multiplication permutes those lines. The left action takes any invertible matrix to any other with the same determinant, by the multiplier NM⁻¹. The field Frobenius permutes determinants by squaring and also preserves the family and the traced symplectic form. Of the four trace-one determinants, 1 is fixed and the other three form one Frobenius orbit. There are 504 labels of each nonzero determinant, so these actions give point orbits of sizes 504 and 1512 on the admissible shortening points. The two quotient spectra already computed in the repo distinguish the resulting families and thus rule out a merger by a larger symmetry. In the fixture the fixed determinant gives spectral type 27 and the three-element determinant orbit gives type 17. [Kantor, On maximal symplectic partial spreads](https://pages.uoregon.edu/kantor/PAPERS/maxPartial.pdf)

## Exact certificate

The executable rounds the saved 64 complex amplitudes to Gaussian integers and projects them with the two commuting Pauli eigenspace projectors, omitting the common scalar denominators. Gaussian-integer inner products make the resulting squared expectations exact after division by the norm squared of the unnormalized state. The two useful shortening labels are (x,z)=(12,51) with determinant 1, and (57,34) with determinant 3 in the trace-pairing convention. Both have eigenvalue −1. On either eigenspace the script checks that all anticommuting covered expectations vanish and that the 279 covered quotient representatives are distinct. The parent and both quotient scaled objectives are exactly

    15615838462932985679 / 6250063775162690025
    = 2.4985086592218817...

This supplies a simultaneous upper-bound witness within 1.3e−8 of the previous numerical candidate. Combined with Pass 12659, each quotient minimum is bracketed below by the parent minimum and above by this rational number. Equality of the global minima still requires a lower bound or a proof that a global parent minimizer can be chosen in these eigenspaces.

Replay with `py -3 analysis/toe_20261114_regulus_quotient_witness.py`.

## Exact stabilizer optima for the quotients

The exhaustive parent stabilizer lower bound of 3 from Pass 12661 transfers to both five-qubit quotient stabilizer problems. A logical stabilizer state lifts to a physical stabilizer state by adding the shortening Pauli to the commuting lift of its logical generators. Conversely, the saved cost-three six-qubit stabilizer support contains a representative of each shortening orbit. The executable checks its full span and its three covered points. It therefore supplies cost-three quotient states of both types. Both five-qubit quotients have exact dimension-scaled stabilizer minimum 3, and the rational witness above proves a strict non-stabilizer advantage in both. [Exhaustive parent result](PASS12661_STABILISER_MINIMUM_THREE_AT_Q8_AND_Q_PLUS_1_OVER_3.md)
