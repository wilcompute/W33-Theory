# Five TOE fronts executed again: exact third-stage Hessian compiler, Witting–Hesse SIC/MUB, E6 charged-vacuum and central-character obstructions, causal spectra, and Naimark photonics

**Research date: 2026-11-22.** This document separates precise finite-dimensional mathematical statements, numerical toy-model experiments, prior literature, and unfulfilled physical predictions. It is not a proof of the Standard Model, quantum gravity, universal photonic BQP, or a Theory of Everything.

## Source audit and parallel-work boundaries

Started at GitHub `master` `f194456adcee9fabc3cf524d261efdf7a14579cd` and read current repo files in the frozen previous research bundle. Previous exact results, not newly claimed: the order-648 Hessian group `G25=H27⋊SL(2,3)`, the one-/two-D matrix censuses `17,496` and `385,560`, the original 27+12+1 Witting ray partition, the 39-effect POVM, the 27×81 H27 Fourier coisometry and 54D E6 cubic radical, and the 4-cycle causal toy chain. Parallel 2026-11-22 commits on other phenomenological and optical topics were checked for overlap; existing code files for the new six fronts were searched before creation. No Windows checkout is claimed synchronized.

Literature prior art: Magma's complex reflection group table confirms `G25` has structure `3^(1+2).SL(2,3)` and order 648 (https://docs.magma-maths.org/v2.30-1/LieTheory/ReflectionGroups/create-group-refl-complex.html). **The Witting/Penrose 40-ray Kochen–Specker theorem was already known** (Waegell and Aravind, 2017, https://arxiv.org/abs/1701.06512), and the qutrit Hesse SIC, four qutrit MUBs and affine-plane phase-space relations are established subjects (https://www.mdpi.com/2075-1680/6/3/21). Our specific *exact embedding, reduced 30-effect measurement, and gate-layout/representation crosswalk* are the outcomes of this pass; no literature-wide priority claim is made. The full physical E6 representation hierarchy and causal-set programme are independent established mathematics and physics.

### Replay

Install `numpy scipy sympy networkx pytest` and execute from repo root:

```bash
python -m pytest -q tests/test_toe_20261122_stage3_and_outside_box.py
python -m pytest -q tests/test_toe_20261122_*.py
python analysis/toe_20261122_stage3_hessian_exact.py
python analysis/toe_20261122_witting_qutrit_sic_mub30.py
python analysis/toe_20261122_e6_higgs_tangent_and_center_gate.py
python analysis/toe_20261122_causal_growth_finite_spectrum.py
python analysis/toe_20261122_povm30_nai_mark_shot_cost.py
python analysis/toe_20261122_witting_KS_ovoid_firewall.py
```

Each producer writes a separate JSON receipt to `data/`. Re-running all scripts is compute-intensive compared with ordinary unit tests because the 3-D compiler enumerates 19,683 exact stage representatives and exhaustively checks H-coset membership. Mathematical identities are asserted explicitly; Haar approximation distances and causal gaps are numerical and are labeled accordingly.

## 1. Exact third-stage Witting compiler, not sampled beam search

Let `H` be the 648-element order-three-mirror group, `N` its normal order-27 Heisenberg subgroup, and `D` the order-two Witting projector reflection on ray 36. The known centralizer of `D` in `H` is `SL(2,3)` of order 24. Thus `H=NK` with `K` commuting with `D`, giving the normal form

\[
HDHDHDH = HDNDNDN.
\]

The raw candidate count is `648·27^3 = 12,754,584`. For each triple `(n1,n2,n3)∈N^3`, compute `x = D n1 D n2 D n3` exactly as a 4×4 matrix in `Z[omega] / 729`. There are 19,683 such matrices. Multiplication by each of the 648 elements of `H` gives all words. **Key acceleration:** every `h∈H` fixes ray 25 pointwise; hence the exact Eisenstein bra `v25†x` is constant on left `H`-cosets. Bucket the 19,683 representatives by this bra, then use the *necessary and sufficient* exact membership test

\[
x\sim y \iff xy^\dagger\in H
\]

on potentially matching pairs inside each bucket. Membership compares all 16 entries, each encoded as an integer pair for `a+bω` with the proper common denominator. No floating-point tolerance or unverified modular hash is used. `H` acts freely on invertible matrices, so each equivalence class contributes 648 distinct matrices.

| Invariant | Exact output |
|---|---:|
| Normal representatives, three D stages | 19,683 |
| Distinct fixed-bra buckets | 9,478 |
| **Inequivalent left-H cosets** | **12,027** |
| **Distinct actual 4×4 matrices** | **7,793,496** |
| Redundant raw expressions | 4,961,088 |
| Recovery of previous two-D cosets | 595 (=385,560/648) |
| Full matrix denominator with leading H | 2,187 |

The prior two-D census is recovered exactly by the same method, including the fact that distinct left cosets can share the fixed-bra signature (514 bra buckets versus 595 cosets): the final exact membership check is essential.

Three seeded unseen Haar U(4) targets, scored by global-phase-insensitive distance `sqrt(2-2|Tr(U†V)|/4)`, give:

| Target | One D | Two D | **Three D** | Three-D primitive gate length |
|---|---:|---:|---:|---:|
| 0 | 0.6573 | 0.48196 | **0.32834** | 22 |
| 1 | 0.6439 | 0.55256 | **0.45381** | 28 |
| 2 | 0.7161 | 0.50926 | **0.46535** | 24 |

The three-stage comparison is exhaustive **within the bounded macro family**, not an optimal global gate-word algorithm. Approximation distances are numerical; the cardinalities are exact. Neither demonstrates optical efficiency, logical fault tolerance, scalable BQP, nor a hardware/energy advantage.

Producer: `analysis/toe_20261122_stage3_hessian_exact.py`.

## 2. New exact Witting → Hesse 9-point affine-plane dictionary and **conditionally optimal 30-effect IC POVM**

Choose the distinguished Witting ray `L=P25`. The remaining 39 rays split into two H27 orbit types: `O12` (12 rays in the three-dimensional subspace `L^⊥`) and `O27` (27 rays with squared overlap `|<v25,vj>|²=1/3`).

**Exact orbit geometry:**

1. The 12 rays partition into four mutually unbiased orthonormal qutrit bases:
   `[1,5,33]`, `[8,23,26]`, `[11,14,24]`, `[28,35,38]`. Cross-basis squared overlap is exactly `1/3`.
2. Project each of the 27 rays onto `L^⊥`, normalize, then identify the order-three H27 center's nine fibers (three rays apiece). All three projections of a fiber coincide projectively; the nine distinct projected rank-one operators have squared overlap exactly `1/4`. They are therefore a **qutrit SIC** (specifically a Hesse-type SIC in this H27 chart).
3. Every blocked `O12` ray is orthogonal to precisely three of the nine SIC projections and has squared overlap `1/2` with the other six. Its three zeroes form an affine line. There are exactly 12 such three-point lines, grouped into four parallel classes corresponding to the four MUBs. Different affine lines from distinct classes meet in one point; lines within a class are disjoint.

All statements in items 1–3 are verified by exact rational pairs in `Q(ω)`; the operator-rank tests are repeated over six split finite primes. This is a source-specific identification of the known 9-point Hesse affine plane and qutrit SIC/MUB dictionary inside the actual canonical 40 Witting rays.

The previously established exact projector sums are

\[
\sum_{j\in O27}P_j=6I+3L, \qquad
\sum_{j\in B}P_j=I-L
\]

for **each** of the four blocked MUB bases `B⊂O12`. Consequently

\[
\boxed{\sum_{j\in O27}\frac{P_j}{9}+\sum_{k\in B}\frac{P_k}{3}=I_4}
\]

is a valid rank-one **30-effect** informationally complete POVM. Every choice of the four MUB bases gives a rank-16 operator span, positive weights and a 30×4 Naimark isometry. This replaces the earlier 39-effect scheme (`Pj/9` on 27 and `Pk/12` on all 12), using nine fewer outcomes: 23.08% fewer.

**New minimality theorem in the specified architecture:** Suppose all 27 universal-control rays must retain **strictly positive** POVM weights and all additional rank-one effects must come from the other 12 Witting rays. Pairing completeness with `Q=3L-I` forces the *total blocked-ray weight* to equal one. Expand the subspace-`L^⊥` part in the **linearly independent nine qutrit SIC projectors**. A blocked MUB projector has SIC expansion coefficient `-1/3` on its three orthogonal SIC states and `+1/3` on its other six SIC states. If some SIC point is not on any selected blocked-ray affine zero-line, coefficient matching forces the **sum of the three positive universal-ray weights at that SIC point to be zero**, a contradiction. Thus the selected affine zero-lines must cover all nine SIC points.

At least three affine lines are needed. Three lines cover all nine points only if they are pairwise disjoint, precisely **one MUB basis** among the four parallel classes. Therefore **30 effects, with three blocked rays forming one MUB basis, is minimal for the positive all-27-universal-ray Witting architecture**. This does not claim a general dimension-four rank-one IC POVM must have 30 outcomes: unconstrained IC POVMs can have 16 effects.

The 39-effect reconstruction superoperator condition number is 10.581; each 30-effect variant has condition number 14.083. Positivity and informational completeness are preserved, but a smaller detector alphabet may increase statistical variance.

Producer: `analysis/toe_20261122_witting_qutrit_sic_mub30.py`.

## 3. Full E6 Higgs first-order audit and conditional 81D E6–H27 representation no-go

The preceding toy superpotential has three vectorlike Higgs pairs `27_H+27bar_H` and five driving fields `X_ab` with singlet bilinear constraints `B_ab`. The previous report correctly solved and locally isolated the **six E6-singlet Higgs variables**, modulo their complexified U1 gauge orbit. It did not solve the full Higgs model.

The real gauge group is E6, dimension 78. A generic vacuum with nonzero VEVs only in the SO10-singlet components of `27_H` and `27bar_H` preserves SO10 (dimension 45), hence has **33 broken complex gauge directions**: one singlet U1 and 32 spinor directions. The entire Higgs sector has `3·(27+27)=162` complex field coordinates. At zero drivers and zero matter, the five independent holomorphic F-term gradients constrain only the singlet Higgs sector; the bilinears' first derivatives vanish in **all 156 nonsinglet Higgs directions**.

Therefore the full holomorphic F-flat **Zariski tangent** has dimension `162−5=157`; after removing the 33-dimensional complex gauge orbit, at least

\[
\boxed{157-33=124}
\]

**nonsinglet charged complex tangent modes** remain with no quadratic superpotential mass. They decompose at this quadratic level into 60 `10_H/10bar_H` components and 64 spinor components after 32 charged Goldstone directions are removed. **These are not proven to be 124 actual nonlinear flat moduli**: higher-order F equations, the D-flat real quotient at singular points, gauge interactions and new superpotential interactions must be analyzed separately. This establishes that the chosen five-driver potential does not by itself lift the full charged Higgs spectrum.

**A stronger center obstruction than the earlier rank-nine 27→27 case:** Assume the source is exactly **three copies of the H27 regular address module**, the destination an **honest 81-dimensional complex representation of simply connected E6**, and the Heisenberg center maps to global `Z(E6)` as it does in the specified center-correct operator construction. The source's center eigenvalues `1,ω,ω²` each have 27-dimensional eigenspaces, and its whole H27-invariant space has dimension **3** (one for each regular copy). Every nontrivial E6 irrep with *trivial center* has dimension at least 78 (adjoint). Thus the 27-dimensional center-trivial subspace of any candidate 81D E6 module must be **27 copies of the E6 trivial representation**, implying at least **27 H27-invariant vectors**. Contradiction.

Hence there is **no 81-dimensional E6 representation extension** of this literal `3×regular27` source with the identified center. To embed the existing H27 source into a larger E6 module while keeping three nonzero center sectors, a necessary elementary dimension bound is at least `78+27+27=132` (nontrivial center-neutral sector plus opposite center characters). This is not an existence theorem at dimension 132 and says nothing about gauge-noncovariant encodings, projective models, alternative H27 embeddings or additional physical fields. Standard E6 irrep dimensions and center characters: https://oeis.org/A121737 and https://pure.hw.ac.uk/ws/portalfiles/portal/14368878/e6_paper_CMP.pdf .

Producer: `analysis/toe_20261122_e6_higgs_tangent_and_center_gate.py`.

## 4. Actual multi-size W33 causal-order spectrum, still not a graviton

Build nested connected induced subgraphs of the canonical 40-vertex W33 orthogonality/adjacency graph, starting with a chordless four-cycle. For each n=4,5,6,7, include **every one of n! total orders** and its induced acyclic directed graph. Give each total order the prior toy action `E=0.06N0−0.09N1+0.045N2`, where `Nk` counts comparable pairs having exactly k interior causal elements. Propose adjacent transpositions uniformly, Metropolis accept, and use detailed balance to construct the symmetric positive semidefinite quantum-walk Hamiltonian `I−D(sqrt(pi)) P D(1/sqrt(pi))`.

| Vertices n | Exhaustively represented orders | First excited spectral gap (arbitrary units) |
|---|---:|---:|
| 4 | 24 | 0.1782243733 |
| 5 | 120 | 0.0915717744 |
| 6 | 720 | 0.0507024153 |
| 7 | 5,040 | 0.0314744702 |

The ground state is `sqrt(pi)`, unique and positive. Reversing each total order preserves the interval action, so the stationary state is reversal-even and the expectation of each reversal-odd order observable is zero. The eigenvalues are explicitly computed from sparse real-symmetric operators. Gap decrease across **four non-equivalent, arbitrarily selected finite graphs is not a continuum scaling law**; different graphs, couplings, weights and boundary conditions can change it. These spectra do not establish a Lorentzian causal light cone, gravitons, positive-energy tensor excitations, or Einstein's equations. For the established causal-set action and continuum challenges, see https://doi.org/10.1007/s10714-024-03281-1 and 2026 quantum BDG algorithm https://doi.org/10.1103/qdst-yrh6 .

Producer: `analysis/toe_20261122_causal_growth_finite_spectrum.py`.

## 5. One-shot 30-port Naimark measurement: exact statistical cost and SPAM boundary

For either the earlier 39-outcome or new 30-outcome POVM, define rows of the optical isometry by `V_j= sqrt(w_j) <v_j|`, giving `V†V=I4`. Complete those columns numerically to a square unitary with an orthonormal nullspace basis and verify `U†U=I`. This proves **a mathematical passive-linear-optical dilation** of the single-photon 4→30 map is possible. It does not prove a compact, low-loss implementation; generic full meshes would have 435 two-mode cells at 30 ports versus 741 at 39 ports, a conditional **41.3% reduction in full-mesh cell count**, not a measured savings.

To quantify the control-versus-observation trade-off, calculate the **exact multinomial linear-inversion mean-squared Hilbert–Schmidt error coefficient** for N detected photons:

\[
\mathbb E\|\widehat\rho-\rho\|_{HS}^2
=\frac1N\left[\sum_k p_k\|F^{-1}(E_k)\|_{HS}^2-\operatorname{tr}(\rho^2)\right],\quad
F=\sum_k |E_k)(E_k|.
\]

The frame is invertible for every 30-outcome MUB choice and for the 39-outcome design. For a seeded generic pure state, the **variance × detected shots** is about **18.7104** for the 39-effect design versus **22.0586** for each of the four 30-effect designs. For the maximally mixed state the coefficients are 19.4832 and 23.7600, respectively. Thus the 30-effect design *saves possible output ports but incurs more statistical noise under this particular unbiased linear estimator*. It is not a global comparison of maximum likelihood, optimized dual frames or detector models.

If an uncalibrated SPAM channel mimics 1% depolarization, even infinite detected photons leave a trace-distance bias **0.0075** on a pure four-mode state. Increasing shot count cannot remove a systematic calibration bias; a reference/calibration model is necessary. Relevant recent photonic research includes an 8×8 28-MZI reconfigurable processor (Nature Photonics, Nov 2026, https://www.nature.com/articles/s41566-026-02050-7) and displacement-enhanced phase calibration (NIST Optica 2025, https://www.nist.gov/publications/enabling-phase-stabilization-quantum-networks-displacement-enhanced-photon-counting). Neither validates our optical hardware losses or physical component count.

Producer: `analysis/toe_20261122_povm30_nai_mark_shot_cost.py`.

## 6. Extra: an independent exact-cover contextuality/ovoid replay and a no-parity firebreak

The 40 Witting rays have 240 orthogonality edges and exactly 40 maximal orthonormal four-ray contexts; each ray belongs to four contexts. A noncontextual binary valuation would require exactly one true ray per context; summing all contexts forces exactly **10 selected rays**. Such a set is an **ovoid** of the symplectic generalized quadrangle W(3,3). A dependency-free bitset exact-cover search visits only 65 memoized residual states (64 branch trials) and finds no solution. Thus the exact canonical 40–40 ray/context system is Kochen–Specker uncolorable. **This is established prior art**, not a new KS discovery (Waegell/Aravind 2017 and the odd-q symplectic GQ ovoid theorem).

A separate \\mathbb F_2 test gives incidence rank 25, unchanged when the all-one context-parity column is appended. Thus there is **no simple parity proof using only these 40 complete contexts** (the parity column is already in the binary column span). An explicit 12-ray parity-odd transversal hits 36 contexts once and four contexts three times: it is a mod-two assignment but fails the exact-one requirement. This shows why **uncolorability and the presence of a parity proof must not be conflated**.

Producer: `analysis/toe_20261122_witting_KS_ovoid_firewall.py`.

## Five independent next experiments (not a dependent checklist)

1. **Compiler gate geometry:** Classify the Hesse/affine-plane Hecke double-coset algebra for all D-stage counts, derive provable asymptotic volume/packing bounds, and find physically shorter words for a calibrated gate model.
2. **Full E6 charged-sector vacuum:** Add only gauge/H27-invariant couplings, then compute the full 162-component scalar/fermion Hessians, nonabelian D terms, gauge Goldstones, anomalies and spontaneous breaking to the Standard Model; do not treat the 124 tangents as physical massless particles without this analysis.
3. **Center-compatible representation engineering:** Test whether the 132D lower-bound candidate `78+27+27bar` can contain a copy of the actual 3×regular H27 module and preserve a *nondegenerate* E6 cubic or a suitable higher invariant, or prove a stronger no-go.
4. **Causal continuum discriminant:** Build genuinely Lorentzian, locally finite growing causal sets with physical interval-action coefficients and gauge-consistent spin-2 response; verify spectral dimensionality and Bianchi constraints instead of fitting toy finite gaps.
5. **Hardware calibration and estimation:** Optimize Naimark dilations for 30 versus 39 effects with measured insertion loss, switching cost, dark counts and adaptive statistical reconstruction; physically compare end-to-end photons and experimental error budgets.
