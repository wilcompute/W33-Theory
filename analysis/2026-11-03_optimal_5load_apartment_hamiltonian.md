# Optimal five-load W33 octagon basis: a sparse cycle-preserving Hamiltonian
**Date:** 2026-11-03. **Status:** exact finite arithmetic construction plus numerical in-band eigenvalue scan. **Physical status:** mathematical model only.

## Prior art and actual advance
BT545–BT551 already give the 80-node/160-edge Levi building, 1620 apartments, and the 81-dimensional Hodge/Steinberg projector. BT744 shows that apartment classes span the Steinberg module. The 2026-11-01 optical-encoder work already selected 81 shortest fundamental cycles (all length 8). The 2026-10-10 local Maxwell 2-complex already uses localized plaquettes. The latest 2026-11-03 flat-band audit correctly proves that adjacency polynomials are scalar on the protected band and onsite potentials leak from it.

**This addition optimizes congestion rather than re-proving those identities.** An independently enumerated set of 81 shortest oriented apartments is GF(2)-independent and hence rationally independent, with every Levi flag in at most five chosen apartments. Their support incidence profile is 9 flags of load 3, 134 flags of load 4, and 17 flags of load 5. Exactly 648 total incidences occur. No lower maximum load is possible: ceil(81*8/160)=5. Thus 5 is the **attained optimal maximum**.

## Explicit integer Hamiltonian and clean boundary
Let B be the 160 x 81 signed oriented cycle matrix produced by \`analysis/2026_11_03_optimal_5load_apartment_hamiltonian.py\`, and D the 80 x 160 oriented Levi incidence. Set H = B B^T. Verification gives:

- D B = 0 and D H = 0, so H maps the full flag space into ker D.
- H D^T = 0, so **no cut-to-cycle mixing** occurs.
- The Levi flag line adjacency A satisfies A H = H A = -2 H exactly; H commutes with A but is *not* an adjacency polynomial.
- The GF(2) rank of B is 81; since dim ker D = 160-79 = 81, H is positive definite on ker D and zero on im D^T.
- H is not a scalar on ker D: the exact comparison 160 H != 8 K, with K = C C^T = 160 P_cycle, proves it.
- Each octagon contributes a rank-one 8-flag interaction. With at most five octagons through any flag, each row has at most 35 possible other coupled flags. The explicit H has **3926 nonzero entries** and maximum **31 off-diagonal neighbors**.
- Its 81 positive eigenvalues are numerically distinct (rounded to 7 decimals), ranging from about 0.0000677615 to 23.2963653. Exact spectral nondegeneracy is *not* claimed.

In particular, A + epsilon H is a **finite sparse operator** with a non-flat protected 81-dimensional sector and exact zero cut leakage. This refines, rather than contradicts, the conditional no-go for H = h(A) or onsite potentials. The essential new ingredient is **orientation-sensitive 8-edge circulation interactions** that break full flag symmetry while preserving the divergence constraint.

## Important caveats
The selected octagons are a basis over GF(2) and Q, not proven a unimodular basis of the integral cycle lattice. Choice of one sparse basis is an extra, noncanonical structure and might break the target physical symmetries. A finite 160-site Hamiltonian with bounded degree does not derive a 3+1-dimensional continuum, Lorentzian causality, quantum gravity, universal light speed or physical particle masses. Generic onsite disorder still leaks between sectors. A falsifiable next test is whether the max-load-five basis can be selected **equivariantly** under a nontrivial subgroup of PSp(4,3), and whether a graph-refinement family permits controlled transport scaling.

## Reproducibility
\`OPENBLAS_NUM_THREADS=1 python analysis/2026_11_03_optimal_5load_apartment_hamiltonian.py\`

\`OPENBLAS_NUM_THREADS=1 python -m pytest -q tests/test_20261103_optimal_5load_apartment_hamiltonian.py\`

Results and the complete list of 81 eight-flag supports are generated deterministically in \`data/2026_11_03_optimal_5load_apartment_hamiltonian.json\`. The support SHA256 is \`4e3587dfdec1096401e0e91956c5b48910f5ba0e6d4c58559716e1f1a258915f\`.

External mathematical anchor: Solomon–Tits theorem, apartments generate top building homology (e.g. https://academicweb.nd.edu/~andyp/papers/Steinberg.pdf).
