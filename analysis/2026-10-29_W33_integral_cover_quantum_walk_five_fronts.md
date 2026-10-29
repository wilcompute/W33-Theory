# W33 TOE: five-front continuation — code distance, nonsplit integral E8 lift, photonic compiler, local dynamics, and falsifiable optical intensities

**Date:** 2026-10-29. **Status:** independently computed exact finite mathematics and an executable *standard-quantum-optics* prototype. This does not establish a theory of everything, explain measured constants, or demonstrate a beyond-QM prediction. Prior and new claims are separated below.

## 1. The q=7 binary adjacency CSS distance: certified lower bound 10

**Prior results:** W(3,q) has binary adjacency matrix A with A²=0 and dim ker(A)/im(A) = q²-1 for odd q. Earlier work proved the q=3 code [[40,8,6]], and our previous Oct 29 commit proved q=5 **[[156,24,10]]** by 23,738,715 exhaustive fixed-linear-projection comparisons. Parallel commit 2afb7f2 reports randomized q=7 search finding words of weight 14; that supports an upper bound, not a lower bound.

**New deterministic exhaustive certificate:** analysis/cpp/w33_20261029_q7_weight8_exact.cpp reconstructs all 400 projective points of F7^4 and symplectic collinearity A. The automorphism Sp4(7) is transitive on points. Suppose there exists an even nonzero kernel word S of weight <=8. Conjugate a support point to vertex 0. Split S into a 4-subset T containing vertex 0 and a distinct 4-subset U excluding vertex 0 (pad T outside S for |S|<8, choosing half of S for the intersection). Since A 1_S=0, the full syndromes A 1_T and A 1_U agree.

The verifier assigns a **fixed F2-linear** 64-bit image to each adjacency syndrome, using deterministic splitmix64 row coefficients, and checks that no 4-subset containing vertex 0 has the same *projected* syndrome as any 4-subset excluding vertex 0. Computing the former is equivalent to enumerating all C(399,3)=10,507,399 three-point projections, and the latter C(399,4)=1,040,232,501 four-point projections. **Zero cross collisions**. Absence under any linear projection implies absence of full syndrome equalities; no statistical or cryptographic assumption is involved. The program also validates geometry's 400 points, degree 56 and exact enumeration totals. Initial independent run: approximately 10.43s on five server cores with g++ -O3 -fopenmp.

Hence no nonzero ker(A) word has weight 2,4,6,8, and all have even weight. Intersecting-line differences exhibit weight 14 logicals. **[[400,48,d]] with 10<=d<=14, exact d still open.** Exclusion of weights 10 and 12 requires a stronger certificate or proof. A separate fixed-pair MILP feasibility search (q=7, both pair adjacency types, 35s each) timed out *without* a bound; we do not count that as evidence.

## 2. Integral E8: a proven nonsplit central extension

**Prior art:** Earlier code identifies the logical quadratic space H of [[40,8,6]] as the eight-dimensional plus-type form and builds a faithful PSp4(3) action in O8+(2), with 25,920 finite matrices. These observations are not novel claims.

**New integral result:** analysis/w33_20261029_e8_double_cover_obstruction.py loads the previously certified seven generators, defines a fixed integer 8x8 matrix M in the E8 simple-root basis, and verifies:

    M^T (2I - adjacency(E8 Dynkin)) M = 2I - adjacency(E8 Dynkin);
    M^2 = -I8;
    reduction_mod2(M) = g0*g1*g5*g4, where g_i are the prior generators;
    (reduction_mod2(M))^2 = I8, but reduction_mod2(M) != I8.

Since E8 has no Dynkin-diagram outer automorphism, its integral positive-definite lattice isometry group is its Weyl group. The standard reduction W(E8) -> O8+(2) has kernel {+I,-I}. Thus *both* integral lifts of this finite involution square to -I; its image cannot be the square of a group-homomorphic section. **The pullback of the Weyl double cover to this PSp4(3) subgroup is nonsplit.**

An independent full finite group closure gives 25,920 elements; 315 nonidentity involutions split into two PSp conjugacy classes of sizes **270 and 45**, with binary ranks of g-I equal to 4 and 2. The witness belongs to the 270 class, hence all 270 involutions have order-four integral lifts. This does *not* rule out projective E8 actions, central extensions, or spinorial implementations; it rules out the naive honest integral PSp action.

Related established source: Jouve–Kowalski–Zywina, *An explicit integral polynomial whose splitting field has Galois group W(E8)*, https://people.math.ethz.ch/~kowalski/weyl-group-e8.pdf (the Weyl/orthogonal double-cover relationship).

## 3. A concrete, loss-aware 40-mode photonic experiment

analysis/w33_20261029_optical_mesh_and_locality.py constructs U = exp(-i*pi*A/2) on the **one-photon** 40-mode Hilbert space using the exact three-eigenvalue spectral projectors. It then decomposes U into **653 active adjacent-mode SU(2) Givens blocks** plus 40 output phases (versus C(40,2)=780 possible blocks), and verifies full matrix reconstruction to below 5e-12 entrywise.

The simulation gives each active 2-mode element transmissivity eta=0.999, attenuating only its two modes; its loss channel is contractive. For injection in the first mode, independently computed survival is approximately **0.980466** in that illustrative component-loss model, with eigenvalues of K†K between approximately 0.948546 and 0.991341. These figures are *device-assumption dependent*, not new material parameters or a hardware demonstration. The architecture is implementable in principle with standard beam splitters and phase shifters (Reck decomposition); a rectangular Clements layout could improve physical loss/depth but is not compiled here.

**Critical boundary:** a single photon in 40 modes has dimension 40, not 2^8. This is not a physical realization of the full eight-logical-qubit [[40,8,6]] CSS code. Ancillas, extra carriers, quantum memories and heralding are missing for a fault-tolerant computer.

References: Reck et al., Phys. Rev. Lett. 73, 58 (1994), https://doi.org/10.1103/PhysRevLett.73.58 ; Clements et al., Optica 3, 1460 (2016), https://doi.org/10.1364/OPTICA.3.001460 ; Knill & Laflamme, Phys. Rev. A 55, 900 (1997), https://doi.org/10.1103/PhysRevA.55.900 .

## 4. What symmetry and locality select (and what they do not)

The seven W33 generators have **exactly three orbits** on ordered point pairs: diagonal 40; adjacent 480; nonadjacent 1080. Therefore the commutant in Mat_40(C) of the entire point-permutation representation has dimension three and is spanned by I, A and J.

A group-invariant single-particle Hermitian Hamiltonian has the form H=aI+bA+c(J-I-A), with real a,b,c. Imposing **strict W33-nearest-neighbor hopping** sets c=0, leaving H=aI+bA. The first term is a physically irrelevant global phase; the second is the adjacency quantum walk up to an **undetermined energy/time scale**. Thus *symmetry plus graph locality selects the dimensionless one-photon dynamics*, but cannot determine Planck's constant, speed of light, gravitational coupling, or measured particle masses. Larger Hilbert spaces with additional degrees of freedom are not covered by the simple commutant classification.

## 5. An experimentally falsifiable signature — and an identifiability caveat

For the adjacency walk at t=pi/(2b), one-site injection produces exact site-resolved probabilities:

    injection site: 1/25;
    each of its 12 neighbors: 1/25;
    each of its 27 nonneighbors: 4/225.

They sum to 13/25+27*(4/225)=1. At t=pi/b, H=aI+bA has a perfect revival (up to global phase). An alternative symmetry-invariant but nonlocal H=A+J/40 has at t=pi the **361/400** return probability and **1/400** for each other output. These are valid, quantitative, parameter-calibrated optical tests discriminating those two Hamiltonians.

**Important no-go:** any SRG with the same (40,12,2,4) parameters has the *same site/neighbor/nonneighbor single-source walk intensity profile*. The above tests validate the spectral-family and locality model but are not a unique signature of W33 topology or a violation of standard quantum mechanics. Distinguishing the concrete W33 adjacency graph requires phase-sensitive multi-input tomography with mode labels. A genuine new-physics prediction requires a specified nonstandard dynamics or interaction and a prediction not fitted to known observations.

## Reproduce

    python analysis/w33_20261029_e8_double_cover_obstruction.py
    python analysis/w33_20261029_optical_mesh_and_locality.py
    g++ -O3 -std=c++20 -fopenmp -o /tmp/w33_q7_weight8 analysis/cpp/w33_20261029_q7_weight8_exact.cpp
    OMP_NUM_THREADS=5 /tmp/w33_q7_weight8
    python -m unittest discover -s tests -p test_w33_20261029_advanced_five.py -v

The E8 certificate requires only the Python standard library; optical compilation requires NumPy. The C++ test requires approximately 256MB for a 2^25-element 64-bit lookup array. Run in a separate worktree; none of the tools here modify the original repository's unrelated local changes.

**Research boundary:** precise q=7 distance and any fundamental-dynamics selection remain open. The obstruction and the 40-mode optical walk are mathematical/engineering outputs, not experimental confirmations.
