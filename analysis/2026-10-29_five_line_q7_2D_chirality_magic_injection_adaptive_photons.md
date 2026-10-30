# 2026-10-29/30 — five independent TOE workbench advances: q7 five-line theorem, logical T injection, conditional chiral phases, Heisenberg moments, adaptive photon statistics

## Status and prior-art boundary

This is a set of exact mathematical and conditional quantum-information results, **not a proven physical Theory of Everything**. Earlier repository work already established the W33 [[40,8,6]] CSS code, a seven-flag sequential Z-check extractor with 52,659,454 exactly enumerated fault histories *under a perfect subsequent full X/Z syndrome*, and a fixed-port three-photon W33-versus-dual event discriminator. We do not reinterpret those previous ideal certificates as a fault-tolerant threshold or as measured photonic hardware.

The work in this report was independently executed on a Linux research server. Four new Python regressions were also run to completion on the user's Windows computer against a fresh detached sparse worktree: **4/4 passed**. The shared main Windows checkout remains dirty with 17 preexisting modified tracked files and was not changed.

## 1. Exact W(3,7) five-line support obstruction

Source: analysis/cpp/w33_20261029_q7_five_line_pair_orbits.cpp.

Construct all 400 points in the four-dimensional projective symplectic vector space over F7, all 400 eight-point isotropic lines, and the 400-by-400 binary collinearity matrix A. For the union U of five distinct isotropic lines compute |U| - rank_GF2(A[:,U]).

The symplectic group is transitive on **intersecting ordered line pairs** and separately on **skew ordered line pairs** (symplectic Witt-extension argument). Thus fix L0, choose one representative L1 in each orbit, and enumerate all C(398,3) = 10,428,396 choices of three further distinct lines for each orbit. Total **20,856,792** representative configurations.

All supported kernels have dimension exactly **four**. Complete histogram:

| Pair orbit | Union points | Count |
|---|---:|---:|
| meeting | 34 | 2,058 |
| meeting | 35 | 86,436 |
| meeting | 36 | 840,958 |
| meeting | 37 | 2,709,602 |
| meeting | 38 | 4,124,232 |
| meeting | 39 | 2,665,110 |
| skew | 34 | 224 |
| skew | 35 | 13,440 |
| skew | 36 | 193,224 |
| skew | 37 | 993,296 |
| skew | 38 | 2,651,376 |
| skew | 39 | 3,916,080 |
| skew | 40 | 2,660,756 |

For every line indicator 1_L, A 1_L = 1 over GF2. Because five distinct isotropic eight-point lines have at least four private points each (any pair meets at most once), their indicators are independent. The *even sums* of the five lines form a four-dimensional supported kernel subspace; computed nullity four proves equality.

Every nonzero even combination has two or four lines: two-line XOR has weight 14 if meeting or 16 if skew, and four-line XOR has weight >= 4*8 - 2*C(4,2) = 20. Hence **no weight-10 or weight-12 binary adjacency-kernel vector is supported within the union of any five isotropic lines**. This is a new finite support exclusion, not a solution to global distance: W(3,7) code distance remains rigorously in the prior interval 10 <= d <= 14; arbitrary nonlocal supports are not excluded.

Additional independent Python control: 20,000 random five-line unions plus all 56 choices of five concurrent lines through a given point had supported nullity four. The compiled pair-orbit exhaustive run took approximately 25 seconds on the research server.

## 2. Conditional ideal logical non-Clifford T-gate interface

Source: analysis/w33_20261029_CSS_logical_T_injection_interface.py.

Construct the W33 adjacency binary image of rank 16 and its kernel of dimension 24. Compute an explicit eight-dimensional CSS logical quotient and eight independent logical X representatives with a dual logical Z basis satisfying X_i dot Z_j = delta_ij mod 2. Transversal CNOT over 40 corresponding physical qubits in two identical W33 blocks implements eight parallel logical CNOTs by standard Pauli conjugation.

A separate *supplied perfect* eight-logical-qubit encoded magic resource, with one T|+> magic state per logical qubit, permits the standard gate-injection identity. For the logical input bits x and measured ancilla bits m, with omega = exp(i pi/4), the branch phase is omega^wt(m XOR x), followed by logical S_i correction for every measurement m_i=1. Because

wt(m XOR x) + 2 wt(m AND x) = wt(m) + wt(x),

the output has the T^tensor8 phase omega^wt(x) up to the global branch phase omega^wt(m). Exhaust all 256*256 = **65,536** x,m pairs and verify the identity exactly with integer arithmetic. The matching logical X/Z construction also passes exact mod-2 rank and pairing tests.

**Limits:** No encoded magic-state factory, no individually addressable logical S_i implementation, no distillation, no noisy logical measurement circuit, no threshold, and no claim of universal physical gates. The previous seven-flag Z round and its Hadamard-dual X counterpart separately require 394 physical two-qubit CNOTs apiece before further overhead, not a full combined FT proof. Flag gadgets based on classical codes are established prior art: Anker and Marvian, PRX Quantum 5, 040340 (2024), DOI 10.1103/PRXQuantum.5.040340.

## 3. H27 chiral sectors: a 2D, explicitly assumed, genuinely symmetry-breaking toy model

Source: analysis/w33_20261029_chiral_2d_peierls.py.

The previous H27 one-cell real K-even Hamiltonian has conjugate central sectors O=i(Z-Z^{-1}) with eigenvalues +/-sqrt(3), each with three locally degenerate lowest states. Project to these two chiral signs and **assume externally** a 2D square lattice with nearest-neighbor interaction -J O_i O_j. On this low-energy projected space it is the standard 2D nearest-neighbor Ising Hamiltonian -K sum_{edges}s_i s_j with K=3J and signs +/-1. The factor 3 of internal degeneracy per site cancels from the normalized projected Gibbs measure.

For an illustrative, freely chosen J=1/10, enumerate all 16, 512 and 65,536 Ising sign configurations on 2x2, 3x3 and 4x4 periodic square lattices. There are precisely two aligned ground-sign configurations for each.

At inverse temperature beta*K = (log 12)/2, a standard Peierls contour bound in the plus-boundary thermodynamic limit gives

P(s_0=-1) <= sum_{l>=4} l*3^l*exp(-2 beta K l)
           = sum_{l>=4} l*(1/4)^l = 13/576.

Thus <s_0>_+ >= **275/288 > 0**, and the conjugate minus-boundary state has negative expectation. The infinite 2D projected model therefore admits *spontaneous K symmetry breaking at sufficiently low positive temperature* with two distinct extremal Gibbs phases. This corrects the no-SSB-at-positive-T result for the previous 1D finite-range model, because dimensionality was **changed by explicit assumption**.

**Limits:** H27 does not derive the 2D lattice, coupling J, absence of the k=0 and excited sectors, effective temperature, or preferred chirality. No model of the observed Standard Model, mass gap, or cosmological vacuum follows. Classical proof is prior art: Griffiths, *Peierls Proof of Spontaneous Magnetization in a Two-Dimensional Ising Ferromagnet*, Physical Review 136, A437 (1964), DOI 10.1103/PhysRev.136.A437.

## 4. H(Z) intrinsic dynamics: exact second moments for all integer times

Source: analysis/w33_20261029_Hp_all_n_second_moments.py.

On the infinite integer Heisenberg group with multiplication
(x,y,z)(u,v,w)=(x+u,y+v,z+w+xv),
choose each random-walk step uniformly among X+, X-, Y+, Y-. For every integer n>=0,

E[x_n^2] = E[y_n^2] = n/2,
E[z_n^2] = n(n-1)/8.

Proof: independent centered horizontal increments have individual second moments 1/2. The central increment at step k is x_(k-1)*Delta y_k, a martingale difference with orthogonal increments, so

E[z_n^2] = sum_(k=1)^n E[x_(k-1)^2] E[(Delta y_k)^2]
          = sum_(k=1)^n (k-1)/4 = n(n-1)/8.

An independent *integer path-count dynamic program*, not Monte Carlo, verifies all three moments for every step n=0,...,12, ending with 5,167 occupied group elements and E[z_12^2] = 33/2.

**Consequence:** horizontal root-mean-square scale is O(sqrt(n)), central RMS O(n). This is a sharp intrinsic sub-Riemannian scaling signature and an explicit obstruction to interpreting the natural Cayley walk as isotropic three-dimensional Brownian motion. It is **not** a theorem ruling out every possible Lorentzian model built with extra structures, nor a derivation of spacetime or physical c.

## 5. W33-vs-dual photon discrimination under adaptive classical feedback

Source: analysis/w33_20261029_adaptive_complex_gram_photon_test.py.

For the previously fixed three-photon inputs and four-output success event, the repo already derived sharp per-shot bounds under arbitrary complex Gram overlaps of three independently prepared photons, with independent state choices under the two hypotheses:

pW >= 17496/15^6 = 0.001536,
pDual <= 6752/15^6 ~= 0.00059276817558.

The prior exhaustive integer binomial threshold test certified minimum N=43,047 and count cutoff k=43 for false-positive and false-negative probabilities individually strictly below 0.001.

The **extension** removes the need for between-shot independence or identical distributions: it suffices that *each shot's conditional event probability given all prior classical outcomes* obeys the same lower/upper bound. An auxiliary-uniform coupling represents each success event as 1[U_t < p_t(history)]. Since p_t(history) is pointwise >= pW (under W33) or <= pDual (under dual), the sum is stochastically bounded by the corresponding i.i.d. binomial endpoint even though the success indicators can be adaptively dependent.

The same N=43,047, k=43 maintains worst-case false positive <=0.00097804529 and false negative <=0.00099997081. The new producer checks 45 exact small-size dynamic-programming recurrences as a separate control. The earlier calibration/loss envelopes are also compatible *if they hold conditionally for each shot*. Bounds on only the unconditional averages do **not** suffice. Correlated inter-shot quantum states and detector memory violating conditional product-Gram envelopes are **not** covered. For experimental complex-Gram tomography prior art see Kotowski et al., arXiv:2610.06736 (2026).

## Executed reproductions and regression status

Linux C++ exhaustive: compile analysis/cpp/w33_20261029_q7_five_line_pair_orbits.cpp with g++ -O3 -std=c++20 and run. Result: 20,856,792 representatives, zero exceptions, full histograms verified.

Windows isolated detached sparse checkout: C:\Repos\Theory of Everything\.research_worktrees\toe_20261029_verified_mirror. Run:
python -m unittest discover -s tests -p test_w33_20261029_q7_five_line_t_injection_chiral_moments_adaptive.py -v.
**Four of four new focused Windows tests passed**, testing all four Python producers and the 65,536 injection branch identities. The shared main checkout was intentionally not overwritten: 17 preexisting tracked modifications still belonged to parallel active work. Windows g++ was not available on PATH in the earlier compiler audit, so the full C++ census was independently verified on the research Linux server rather than claimed to be run on Windows.

## Five independent open problems

1. Global distance for [[400,48,d]] at q7: either exhibit non-five-line-local weight10 or12 kernel support, or close the lower bound d=14 with an independent proof/certified SAT UNSAT.
2. Real fault tolerance for **mixed X/Z rounds** and a magic-state *factory*: prove correction of two arbitrary faulty locations with noisy repeated syndromes and construct addressable logical S and logical T using experimentally plausible components.
3. Endogenous chirality: derive the effective interaction graph and Hamiltonian, remove the projected-sector assumption, and obtain a physical preference for one of the K-exchanged phases.
4. Emergent Lorentzian spacetime/gravity with a consistent continuum causal metric; intrinsic Heisenberg graph diffusion demonstrably has anistropic scaling and is not sufficient alone.
5. Hardware-calibrated falsification of W33-vs-dual optical event distributions with measured three-photon internal Gram matrices, nonuniform loss, detector dead time, background correlations and adaptively varying source noise.
