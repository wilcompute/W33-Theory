# Positive geometries of del Pezzo moduli and multi-qudit Pauli geometry: the E6 and E7 rungs

*Standalone note. Computations: Passes 12634–12638 (`analysis/w33_pass12634_naruki_fan.py`, `w33_pezzotope_check.py`, `w33_pezzotope_chirality.py`, `w33_e7_orbit_census.py`, `w33_e7_scalene.py`, `w33_e7_facet_test.py`). Exact certificates of the E6 identification: the other track's Yoshida packet (779cc43ba).*

## Background

The real moduli space of marked del Pezzo surfaces of degree 9 − n has W(E_n)-equivalent regions, called pezzotopes. Each is a positive geometry, proved for n = 6 and conjectured for n = 7 (Early, Geiger, Panizzut, Sturmfels and Yun, arXiv:2306.13604; Sturmfels and Telen, arXiv:2605.11909). Two exceptional isomorphisms connect these Weyl groups to Pauli groups:
- W(E6) ≅ PGSp(4,3), the two-qutrit Clifford symmetries;
- W(E7)/{±1} ≅ Sp(6,2), the three-qubit ones. The root-level dictionary for E7 is Cerchiai and van Geemen's (arXiv:1003.4255), building on Lévay, Saniga and Vrana.

## The two rungs

| | E6 (cubic surfaces) | E7 (degree-2 del Pezzo) |
|---|---|---|
| Pauli geometry | W(3,3), two qutrits | W(5,2), three qubits |
| positive roots ↔ | spreads (complete MUB sets) | points (non-identity Paulis) |
| number of regions | 432 | 60,480 |
| **a region ↔** | **a maximal partial spread of 5 lines** (pentad) | **a scalene triple of Lagrangians** (pairwise intersection dims 0, 1, 2) |
| region stabiliser | S5 (exotic, inside S6) | S4 |
| how the region determines it | its 5 cusp facets are the 5 lines | the unique 6-A1-root frame, plus the 2 frames totally singular for all 3 A7 facets |

**E6.** The 432 regions are exactly the 432 maximal 5-line partial spreads of W(3,3); these are the corpus's "pentads".
- Codex identified the actual real components with them by facet labels.
- In quantum-information terms, they are **strongly unextendible sets of 5 two-qutrit MUBs**: no vector in C⁹ is unbiased to all five. This is certified by a Hermitian sum-of-squares bound F(v) ≥ |v|⁴/9 (Pass 12638).
- Their chirality (two PSp(4,3)-orbits) is exchanged by the Kramers reversal, the Weyl reflection in a double-six root.

**E7.** Among Sp(6,2)'s 12 orbits on triples of three-qubit maximal commuting sets, exactly one has 60,480 elements, the scalene triples, with stabiliser S4.
- The explicit E7 region in Early et al. canonically determines one scalene triple.
- Equivariance plus matching orbit sizes makes the map a bijection.
- Unlike E6, the regions are **not** unextendible MUB sets: three-qubit unextendible sets number 960 + 24,192.

## Scope

This is exact combinatorics and one SOS certificate. The E7 bijection is shown on one explicit region and transported by equivariance; an atlas-wide check is proposed. No claim is made about the E8 rung: the region count of the real moduli of degree-1 del Pezzo surfaces is not in the literature I found.
