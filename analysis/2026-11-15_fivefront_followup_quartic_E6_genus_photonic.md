# W33–E6 six-channel obstruction and quartic recovery; genus-six plane search; D9, F8 and photonic controls

**Date:** November 15, 2026. **Scope:** Five requested independent follow-ups plus an outside-the-box sixth construction. These results refine the exact finite combinatorial dictionary, NOT a Theory of Everything or a physical E6 Yang–Mills model.

**Producer:** \`analysis/toe_20261115_followup_fivefronts_nonlinear_genus_D9_F8_photon.py\` (five fronts).
**Additional producer:** \`analysis/toe_20261115_quartic_E6_sixsector_bridge.py\` (sixth front).
**Regression:** \`tests/test_toe_20261115_followup_sixfronts.py\`.
**Machine-readable results:** \`data/toe_20261115_fivefront_followup_certificates.json\`; \`data/toe_20261115_quartic_E6_sixsector_bridge.json\`.
Run via \`py -3 analysis/toe_20261115_followup_fivefronts_nonlinear_genus_D9_F8_photon.py\`, \`py -3 analysis/toe_20261115_quartic_E6_sixsector_bridge.py\`, and \`py -3 -m pytest tests/test_toe_20261115_followup_sixfronts.py -q\`.

## Executive evidence and prior art

Recent prior commits \`c23c8b5\`, \`332f410\`, \`20dee36\` reconstruct the Császár Fano-plane doubling, the 45 W33 K4,4 octets, 1,620 apartments, 45×36 disconnected one-ray hopping, 27 five-octet cubic-line partitions and 40 symplectic order-three operators. These are **already known from this repo**; this pass does not rename them new discoveries. The 2025 Bokowski–Kevin H. survey (Symmetry 17, 622; https://www.mdpi.com/2073-8994/17/4/622), §8.3, reports unsuccessful numerical searches for realizing all 59 genus-six 12-hendecagon duals. It does NOT settle their realizability. Schewe's separate primal 12-vertex triangular 3D nonrealizability theorem is rigorous.

The novel mathematical tests below show: (i) the *bilinear* 40-point→27-cubic-line incidence channel misses exactly six E6-related permutation directions; (ii) a *quartic* two-pair channel over 270 supports restores exactly all 27 output directions with equal singular values; (iii) the geometric genus-six dual planar-facet search can be parameterized by **only 12 plane equations / 36 continuous parameters** rather than 44 arbitrary vertices; (iv) structured detector calibration has a far smaller sufficient shot budget, if its symmetry is physically calibrated. The D9 and F8 arms are carefully scoped consistency checks, not solved spectra or an optimality proof.

## Front 1: exact six-dimensional dark sector of the quadratic W33–E6 map

Import the independently existing Pass1536 \`45 K4,4\` octet data; let \`P_{40×45}\` be point-octet incidence and \`T_{45×27}\` be octet-to-cubic-line (five-clique) incidence. Let \`A=T^T T-5I\`, the 27-line Schläfli graph, with adjacency eigenvalues \`10^1,1^20,(-5)^6\`.

The central 40×40×27 quadratic coefficient tensor from the preceding pass is

\`Q_{p q l} = sum_{o=1}^45 P_{p o} P_{q o} T_{o l}\`.

Although \`Q\` is nonuniform and depends on W33 adjacency, it factors through \`T\`. Consequently \`rank(Q_(1600×27))=rank(T)=21\`, by direct exact octet-row isolation: for every octet, a pair of nonadjacent W33 rays in that octet lies in *no other* octet and produces exactly one row of T. This proves rank equality, rather than merely observing a numerical singular-value threshold.

The six-dimensional null space has an explicit **exact integer projector numerator**

\`E=(A-10I)(A-I)\`, \`E²=90E\`, \`tr(E)=540\`, \`T E = 0\`, \`Q·E=0\`.

Thus \`Pi_6=E/90\` is a rank-six orthogonal projector to the -5 Schläfli eigenspace. This gives a **necessary capacity obstruction** for every scalar 45-octet-factorized transfer with last stage T: it cannot populate the 6D dark cubic-line representation sector. A quadratic W33 incidence coupling reaches only \`1⊕20\`, NOT the full 27. This statement does not forbid a genuinely different, non-factorized or higher-order transfer.

## Extra front 6: exact quartic **270×27 tight reconstruction frame** activating all six dark modes

Take two nonadjacent W33 point pairs \`(p,q)\` and \`(r,s)\`, each associated with a unique one of the 45 octets, say \`o,o'\` (the pairs are chosen from the same four-ray independent side of their K4,4, so their containing octet is unique). Require \`o\` and \`o'\` **disjoint** eight-ray supports. The 45-vertex disjoint-octet graph \`C\` is \`SRG(45,12,3,3)\`, so there are \`45×12/2=270\` such pairs.

By the exact identity \`T T^T=3I+C\`, every pair of distinct disjoint octets lies in **exactly one** common 5-clique. Therefore its quartic transfer row is exactly a one-hot 27-vector:

\`R_{(o,o'),l} = Q_{p q l} Q_{r s l} = T_{o l} T_{o' l} = delta_{l,L(o,o')}\`.

All four W33 points are distinct. Every five-octet cubic-line partition contributes \`binom(5,2)=10\` pairs, so the 270-row matrix satisfies the **exact** equal-singular-value identity

\`R^T R = 10 I_27\`.

As a result \`rank(R)=27\`, the six-dimensional dark sector is **fully reachable** (\`rank(R E)=6\`), every line label is sampled ten times, and an arbitrary real 27-vector y is exactly reconstructible as \`y=(R^T R y)/10\`. This is verified by integer matrix multiplication, not floating-point optimization. Furthermore all 40 projective symplectic transvections permute the 270 four-point sensors and 27 cubic-line outputs in a manner that preserves R exactly; all 40 actions are explicitly checked.

**Model boundary:** These quartic input features are *products of two point-pair channels*. They are not an interaction between four physical photons, not a four-body Hamiltonian, not a deterministic single-photon nonlinear optical gate and not E6 gauge dynamics. A physical photonic device would need independent sources/copies, a multi-rail nonlinear interaction or classical cross-correlation processing, a loss/noise model and an actual budget. The theorem that R is a tight frame follows naturally from the previously known cubic-line/K4,4 clique incidence; novelty is the explicit **four-ray nonlinear information-transfer design and exact six-mode rescue**, not the raw number 270 or the existence of 27 lines.

**One important design choice:** In the constrained architecture built from pair-channel multiplication, quadratic degree two is insufficient; quartic degree four works. This does NOT assert that no other genuine cubic (degree-three) invariant map exists outside this architecture.

## Front 2: planar-face genus-six dual as a 12-hyperplane arrangement

The existing \`analysis/w33_genus_six_execution.py: FACETS_ONE\` supplies a 12-vertex, 44-triangle orientable genus-six neighborly simplicial complex. Its abstract dual has **44 vertices, 66 edges, 12 eleven-gonal faces**, all faces pairwise adjacent, with each dual vertex incident with precisely three faces.

The generic 3D **planar-facet** realization problem admits the coordinate ansatz

\`Pi_i: z=a_i x+b_i y+c_i\` for \`i=0..11\`,

using **36 real plane coefficients** before removing the Euclidean gauge. Any finite collection of genuinely nonvertical face planes lies in this chart, and a generic rigid rotation makes a nondegenerate finite plane collection nonvertical. There is therefore no local loss of generality from this ansatz for a generic straight-edge planar-faced embedding.

Each primal triangle \`(i,j,k)\` corresponds to a *dual vertex* determined, rather than independently chosen, by the 3-plane intersection

\`V_ijk=solve([(-a_i,-b_i,1),(-a_j,-b_j,1),(-a_k,-b_k,1)], [c_i,c_j,c_k])\`.

The 44 vertices are derived from these plane coefficients. Every one of the 66 dual edges lies simultaneously in two face planes and joins the two triple intersection points corresponding to the pair's two incident primal triangles. The plane-induced boundary order of each of the 12 faces is exactly the eleven-step link cycle around a primal vertex. This eliminates the 44×3 unconstrained point coordinates from a future nonlinear embedding search.

**A necessary but not sufficient falsifier:** a face polygon must be simple in its own plane. The independent sampler generated 160 random plane sets, accepted 86 whose chosen 44 triple intersections were uniformly nondegenerate, and counted proper crossings between the 44 pairs of nonadjacent boundary edges on each of the 12 projected eleven-gons. No sampled arrangement had zero crossings; the smallest total was **41**, the median **68**. This is **not** evidence for a theorem of nonrealizability, since random 36-parameter points are not optimized and global face-face intersections were not tested. It does provide a compact feasible search parameterization and an exact combinatorial indexing to which gradient/SAT/interval methods can be applied.

**External evidence:** Bokowski and Kevin H., §8.3, https://www.mdpi.com/2073-8994/17/4/622; Schewe https://arxiv.org/abs/0801.2582. Note especially: Schewe's *primal* no-go is NOT a proof for the nontriangular *dual* geometry.

## Front 3: D9 flux comparison, protected vector and primitive sectors

We replay and juxtapose two existing, mathematically different source-free D9 Einstein–Maxwell solutions; no new full mixed KK diagonalization is claimed.

On \`AdS5×S²×S²\` with a nonzero monopole flux on each round S², the six rotational Killing generators are gauge-compensated symmetries of the flux (\`i_K F=dmu_K\`), giving 6 protected 5D gauge directions plus one constant Maxwell \`U(1)\`: **7 protected vector zero modes** at the classical symmetry level. \`b1=0,b2=2\` and there is **1** primitive (1,1) metric modulus, with the known protected mass squared \`m²L²=36\` at equal radii. The external TT spin-two KK tower has gap \`m_1² L²=40 min(1,t)/(1+t) <=20\` where \`t=r1²/r2²\`. At extreme anisotropic quantized-flux branches the gap tends to zero; no uniform KK scale separation is obtained.

For a smooth Kähler–Einstein **cubic surface** (a del Pezzo of degree three), \`b1=0,b2=7\`, and the continuous holomorphic automorphism group (hence the metric isometry Lie algebra for a KE metric) is trivial. So the same minimal Einstein–Maxwell field content protects **one** external vector (\`U(1)\`), not seven. Six primitive harmonic (1,1) classes have the existing protected \`m²L²=36\` result; their marked integral intersection pairing is the negative E6 root lattice. Six scalar kinetic directions **do not** imply six massless E6 gauge bosons. The model cannot turn Weyl root-lattice combinatorics into Yang–Mills gauge enhancement by itself.

The exact, gauge-invariant coupled mixed vector/scalar KK mass tower and any higher-dimensional supersymmetric or nonabelian completion are **still open**.

## Front 4: distinguish a code-space exact F8 lower bound from a numerical full-space SOS

Most critical quality-control correction: the *integer-exact* rational full-cut PPT bound

\`143060206669/68719476736 ≈ 2.081800000000\`

is **only valid for the designated 16-dimensional F8 common code**. It cannot be declared a global lower bound on the full \`C64\`. We independently replayed the existing exact proof via \`py -3 analysis/toe_20261114_regulus_ppt_dual.py\`: it passes, with strictly positive integer diagonal-dominance margin **9,726,167**.

The latest parallel Pass12673 global degree-six SOS (Heisenberg/Singer/GammaL 1,416 coefficient classes, 12,977 variables, SCS solver) finds a **numerical, not rationally certified** full-C64 bound of **0.7603388326420645**. Its known-answer control with all 4,095 nonidentity Paulis returns approximately 63, and the q=4 smaller problem matches its previously studied numerical optimum. These are useful validation controls, but solver convergence plus a numerical primal/dual fit is **not** an exact global SOS proof. The SOS was not rerun (prior recorded solver runtime ~979 s); its JSON source and control were inspected.

The exact algebraic *upper* witness remains

\`(47-32cos(2π/9))/9≈2.498508646688078\`.

There is thus no proved near-tight **full-C64** bracket. Restricting attention to the common 16D code yields a rigorous lower bound 2.0818 and an attainable upper bound 2.4985, width ≈0.41670865. The global numerical degree-six SOS-to-witness gap is ≈1.73817. The correct future route is to construct a stronger rigorous full-space lower witness, or prove a reduction from full64 to a smaller invariant code—not to equate code and global SDP certificates.

Source paths: \`analysis/toe_20261114_regulus_ppt_dual.py\`, \`data/toe_20261114_regulus_ppt_dual.json\`, \`analysis/w33_f8_global_sos6_v2.py\`, \`data/w33_f8_global_sos6.json\`, \`data/w33_f8_global_sos6_control_all.json\`.

## Front 5: pooled four-category 16-rail photonic readout at **joint** 99% confidence

The prior synthetic five-setting four-virtual-qubit GHZ witness assumed known column-wise detector confusion to \`ℓ1≤0.002\`, and two known parity-flip rates to absolute tolerance \`0.002\`. For the explicitly assumed model

\`C=(1-a-b-d)I + a Shift_+ + b Shift_- + d J/16\`,
with \`(a,b,d)=(0.023,0.017,0.006)\`,

all 16 columns are cyclic translates of ONE four-category distribution: self, +1, −1, and 13 uniform other outcomes. The four category probabilities are exactly

\`(0.954375,0.023375,0.017375,0.004875)\`.

Within this **strict circulant** model the ℓ1 error of each reconstructed **16-category** column equals the ℓ1 error of the **pooled 4-category** multinomial distribution, because all 13 other rails share one uniform parameter. Thus there is no 16-column union penalty if the hardware's cyclic invariance is independently validated.

Split the total target failure probability 0.01 into \`alpha_C=.0025\` for readout calibration, \`alpha_P=.0025\` for both parity flips, and \`alpha_W=.005\` for five synthetic witness setting means. Two-sided Bernoulli Hoeffding and an all-subsets union yield:

\`Pr(||p_hat4-p4||_1>epsilon) <= 32 exp(-N_C epsilon²/2) <= .0025\`;
\`Pr(any |flip_hat_i-flip_i|>epsilon) <=4 exp(-2 N_P epsilon²) <= .0025\`.

At epsilon=.002 the sufficient **accepted calibration counts** are **4,728,601 pooled rail clicks** plus **922,220 clicks for each prepared parity class**, **6,573,041 accepted calibration measurements total**. This is a **23.3×** reduction versus the prior *unstructured* 153,290,096 accepted rail calibrations alone. It is intentionally conservative, not a minimax lower bound. The five-setting witness's Hoeffding halfwidth is recalculated at alphaW=.005, and with calibration bias included the same synthetic observation \`Fhat≈0.96591138\` has **joint 99% lower certificate ≈0.92853840**.

**Hard limitations:** this ratio is conditional on the detector model being *exactly* translation invariant with uniform 13-rail leakage and independent trials. Fabrication mismatch, mode-dependent loss, drift, rail-to-rail crosstalk and correlated dark counts break pooling. Calibration validation costs, parity preparation errors and launch-to-accepted conversion are not included. No actual photon experiment has occurred. Four virtual qubits on one photon do not demonstrate spacelike-separated Bell nonlocality.

## Research decision and orthogonal next experiments

1. Find a *gauge-covariant, unitary or CPTP realizable* implementation of the quartic 270→27 feature frame; check photon-copy resources, nonlinearity and losses. Do not assume a four-rail polynomial is automatically a unitary quantum map.
2. Optimize the 36-parameter 12-plane genus-six dual with a validated per-face polygon simplicity penalty, then add **global face-face nonintersection constraints** and interval/SAT exactness; a numerical zero of local penalty alone would not be a valid polyhedral embedding.
3. Construct coupled D9 Maxwell–metric scalar/vector blocks for the first nontrivial internal harmonics; test gauge zero modes and Breitenlohner–Freedman/ghost conditions.
4. Improve the full-C64 F8 lower bound beyond the numerical degree-six SOS and reproduce a **rational, globally valid** certificate; prove any claimed reduction from 64 dimensions to the 16D common code.
5. Independently validate rail translation invariance and dark-tail uniformity on an optical apparatus; design a calibration decision test that detects its failure before pooling.
