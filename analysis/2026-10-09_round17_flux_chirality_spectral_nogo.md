# Round 17 addendum: interaction sees geometry, not magnetic orientation

**Date:** 2026-10-09. **Status:** exact bipartite and antiunitary operator identities; native 3240-dimensional numerical matrix regression checks.

For the 80-vertex bipartite W33 point-line Levi graph, orient Peierls hoppings by a three-edge real flux vector phi. The Bose-Hubbard Hamiltonian in the symmetric two-boson sector is H(U,phi)=dGamma(A_phi)+U P, where P projects onto doubly occupied site states.

There are two distinct exact spectral symmetries:

1. **Flux reversal:** A_{-phi} = conjugate(A_phi), and P is real, so H(U,-phi) = conjugate(H(U,phi)) for every real U. Hermiticity implies the spectra and characteristic polynomials are identical. Interaction cannot, by energy eigenvalues alone, choose one of two opposite Peierls flux orientations, even though it can distinguish different three-edge geometries as established by the Round17 trace certificate.
2. **Bipartite interaction sign duality:** Let C=diag(+1 on point nodes, -1 on line nodes). Then C A_phi C = -A_phi. On the symmetric two-boson space J=Sym^2(C), so J dGamma(A_phi) J = -dGamma(A_phi), and J P J = P. Therefore J H(U,phi) J = -H(-U,phi). In particular spec H(-U,phi) = -spec H(U,phi). Odd trace moments are odd functions of U.

The source-recomputing regression tests instantiate the actual Round16 3240x3240 Hamiltonians, not a mock graph, for representative selectors and verify both matrix identities to numerical roundoff. The algebraic proof is general and exact.

**TOE boundary:** The paper Forty Points (150-page PDF, Section 9.6 and Section 11) distinguishes carrying chiral structures from selecting chirality. The interaction-sensitive orbit fingerprint is not a solution of that selection problem. A physical source of time orientation must enter through a state, boundary condition, driven-dissipative law or chiral dynamical term not reducible to the real-U Hermitian onsite Hamiltonian alone. Such a term should be validated by actual symmetry-breaking observables rather than by count coincidences.

Test: python -m pytest -q tests/test_w33_20261009_round17_flux_time_reversal_nogo.py.
