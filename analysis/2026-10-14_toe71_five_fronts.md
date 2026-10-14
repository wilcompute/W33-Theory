# TOE71 — Five fronts: global 160-link disorder MILP, unbounded-rotor gap bound, quantum cover tunneling, flat holonomy in 4D and sitewise Hartree–Fock

**Date:** 14 October 2026. **Predecessor:** TOE70. **Model scope:** finite W33 80-vertex point-line graph and specifically supplied 3 selected phase chords. **Not solved:** a physical Theory of Everything, intrinsic 3+1 spacetime, the Standard Model, a native 4D overlap-Dirac operator, thermodynamic gauge dynamics, and experimental parameter-free predictions.

## Prior-work and novelty controls

Re-read the current exact W33 core, TOE69/70 native 238-octagon producer, 20-octagon cover/orbit certificates, 11-site/12-link overlapping-octagon Gauss-sector builder, TOE67 continuous all-temperature uniform free-fermion theorem, and TOE70 restricted-uniform Hartree model. Reviewed established ribbon transition-polynomial language (Ellis-Monaghan and Sarmiento, *European Journal of Combinatorics* 32, 782–794, 2011, DOI 10.1016/j.ejc.2011.01.019), overlap index/family literature (D. H. Adams, *Phys. Rev. Lett.* 86, 200, 2001, DOI 10.1103/PhysRevLett.86.200), and unrestricted Hartree–Fock methodology (Scholarpedia, *The Hartree–Fock method*). Standard graph-state, HF, lattice-index and matrix-analysis methods are not claimed as new mathematics; the new results are specifically their application to these native W33 data.

## Front 1 — All 160 native edges in a global 0–1 disorder program

Take the fixed integer phase test direction q=(0,−1,1) and positive hopping interval w_e∈[1−ε,1+ε]. Only 159 of the 238 native winding octagons contribute to this Rayleigh test. The resulting objective is *multi-affine* in the 160 edge weights. By optimizing one coordinate at a time, a global box minimum is attained at a high/low corner.

**Exact integer-program formulation:** Let x_e=1 mark high weight, z_{c,k}=1 mark the condition that exactly k of the eight edges in octagon c are high. For each of 159 active cycles,

\[
\sum_{k=0}^8 z_{c,k}=1,\quad
\sum_{k=0}^8 k\,z_{c,k}=\sum_{e\in c}x_e,\quad
(x_e,z_{c,k})\in\{0,1\}.
\]

The objective is linear,
\[
\sum_{c}\sum_{k=0}^8
a_c(1+\epsilon)^k(1-\epsilon)^{8-k} z_{c,k},
\quad a_c=(-1)^{1+\sum_i\mathrm{wind}_i(c)}
   [\mathrm{wind}_3(c)-\mathrm{wind}_2(c)]^2.
\]

These constraints reproduce the original multiaffine corner problem **exactly at integral x,z**; they contain 1,591 binary variables, 318 equality rows, 160 native links and 159 active octagons. The formulation therefore covers *all* 2^160 corners without blindly enumerating them.

HiGHS MILP returned **status optimal** and equal primal/solver dual objectives at every tested ε=.245, .244616, .2446151, .244615, and .244. At all five values the global solver winner was the same **17-high-edge mask** from TOE66, whose integer Rayleigh numerator was separately reconstructed with Python unbounded integers. Examples of reported optimum values:

| ε | HiGHS-reported global minimum of fixed q form | sign |
|---:|---:|---|
| .2440000 | +.4441227519 | positive |
| .2446150 | +.0001303221 | positive |
| .2446151 | +.0000580699 | positive |
| .2446160 | −.0005922005 | negative |
| .2450000 | −.2781812453 | negative |

The exact 17-edge witness has first root ≈.244615180371192 (root location is numerical; rational sign witnesses are exact). **This is a substantial upgrade over the prior three-edge-flip and 17-dimensional subcube searches.**

**Crucial qualification:** HiGHS computes with floating-point branch-and-bound bounds. Its “globally optimal” status is a *numerical mixed-integer solver report*, not yet an independently checkable exact rational global-optimality certificate. The independently evaluated winning **positive/negative rational witnesses** are exact. Also, fixed q is only one direction in the 3×3 holonomy Hessian. This does **not** prove the universal stability threshold, which may fail first along another direction; and the coefficient argument does not extend directly to all positive temperatures under disorder.

Producer: analysis/w33_20261014_toe71_global_disorder_milp.py.

## Front 2 — Actual unbounded native two-loop rotor: a conditional rigorous spectral-gap mechanism

Using the actual 11-vertex, 12-edge, 5-fermion Gauss-constrained overlapping-octagon patch with three native Wilson octagon operators and g=.8, κ=.7, β=.4, mass=.3, split the full unbounded electric-flux Hilbert space into P (both independent integer fluxes |m_i|≤3) and Q (the complement). Finite P dimension is 22,638.

For every one of 462 occupations, reconstruct all 12 electric fluxes using the exact vertex Gauss law. The omitted Q diagonal energy has **exact minimum 18.215**, attained with flux pair (−4,1). Searching integer fluxes |m_i|≤12 is globally sufficient: since the two chord electric edges equal m_i, any omitted |m_i|≥13 contributes at least .32×13²−1.5+1.875=54.455.

Each Q row has absolute off-diagonal sum no greater than 12κ+3β/g²=10.275. Gershgorin thus proves

\[
QHQ\ge7.94\,I.
\]

Only the first omitted shell |m|∞=4 is directly coupled to P. Construct the actual sparse interface matrix K=PHQ (22,638 by 14,784), including fermionic hopping signs and all magnetic shifts. Exactly 28,476 entries are nonzero. Its maximum absolute row and column sums are **2.65** and **1.325**, giving the *rigorous* operator upper bound

\[
\|K\|_2^2\le\|K\|_\infty\|K\|_1
 =3.51125.
\]

Using the TOE70 **numerical**, not interval-certified, P ground and first excited values E0≈−3.189847448116, E1−E0≈1.064312487261, the elementary block min–max lower bound gives a **conditional** unbounded ground interval approximately

\[
-3.4968591848\ \le E_{\infty}\le\ -3.1898474481
\]

and the Schur/inertia argument for energies below zero yields a **conditional** full spectral-gap estimate

\[
\Delta_\infty\ge
(E_1(P)-E_0(P))-\frac{3.51125}{7.94}
\approx\boxed{0.6220895653}.
\]

The Q spectral lower bound, coupling bound and block inequalities are exact, but the displayed decimal energy and gap inequalities are **conditional on obtaining rigorous ordered finite-block eigenvalue enclosures**. A sparse Ritz residual alone does not certify eigenvalue *ordering*. This is therefore a strong **route to a proof**, not a finalized computer-assisted spectral-gap theorem, and certainly not a full 80-site thermodynamic mass gap.

Producer: analysis/w33_20261014_toe71_two_loop_gap_bound.py.

## Front 3 — A real quantum pairing model and second-order motion of exact-cover vacua

TOE70 classified the 51,840 member orbit of the exact 20-octagon W33 edge covers. A 4-valent native vertex has precisely **three** unordered pairings of its incident edges. Define on the full tensor product of 80 qutrits (dimension 3^80)

\[
H_{\rm pairing}=-J N_{\rm loops}
  -t\sum_{v=1}^{80}\sum_{a\ne b}|a\rangle\langle b|_v,
\quad J>0,\ t\ge0.
\]

The loop number and equal-amplitude local 3-state mixing are preserved by every automorphism of the Levi graph; this is an **exact symmetry-invariant finite quantum Hamiltonian**. Its huge full spectrum has *not* been diagonalized.

Starting at the TOE69 exact 20-loop cover, exhaustively flip one local pairing at all sites: each of the 160 alternatives merges two 8-loops into 19 loops, with excitation energy J. Now exhaustively flip two **different** vertices and both alternative pairings (4*C(80,2)=12,640). The exact loop-count histogram is

\[
N_{\rm loops}=18:12628,\quad
N_{\rm loops}=19:6,\quad
N_{\rm loops}=20:6.
\]

The six last cases are *alternative exact-cover ground configurations reachable by two local pairing flips*: hence the quantum mixing has nontrivial second-order tunnelling within the classical 20-loop vacuum manifold. The **diagonal** second-order perturbative shift from all single-site virtual states is −160t²/J, prior to diagonalizing this degenerate manifold. We do **not** equate this diagonal term with the actual full ground energy.

As an explicitly symmetry-breaking **small Galerkin control**, freeze 76–78 vertices and diagonalize 3², 3³ and 3⁴ state sectors. The four-active-site sector at t/J=.2 has ground E/J≈−20.3595917942, gap/J≈.9797958971 and expected loop number ≈19.633. These are toy-sector results, not 3^80 diagonalization, gravity or experimentally observed spacetime.

Producer: analysis/w33_20261014_toe71_quantum_pairing.py. This construction builds on established transition-polynomial and state-model ideas for 4-valent graphs.

## Front 4 — Preserve native three-deck flat holonomies on a *closed* W33-derived 4D spin control

TOE70 showed that attaching the selected 20 octagon faces kills all three chosen flat deck characters and yields no H4 after the naive product with T². An alternative construction uses a **3D regular neighborhood/handlebody of the original graph** rather than filling in those cycles.

The connected native graph has 80 vertices, 160 edges and cycle rank **81**. Its thickening H is a genus-81 orientable handlebody; the boundary ∂H=Σ81 is a **genuine closed orientable genus-81 surface**. The inclusion ∂H→H induces a **surjection**

\[
H_1(\Sigma_{81};\mathbb Z)\twoheadrightarrow
H_1(H;\mathbb Z)\cong\mathbb Z^{81}.
\]

Therefore every flat U(1) character on the original 81-dimensional graph cycle sector pulls back to a flat character on Σ81. This includes the particular three chord cycles **59,93,139** and the (π,π,π) character. Unlike the 20-face attachment, this construction **does not kill the native flat holonomies**.

Taking the **externally supplied** T² gives a closed spin four-manifold M=Σ81×T², with Betti numbers (1,164,326,164,1), signature zero, untwisted spin Dirac index zero. Its intersection form has 163 hyperbolic planes. Flat characters alone have c1=0 in this torsion-free setting, so their spin Dirac index is **zero**. To obtain a nonzero index one must impose extra nonflat line-bundle curvature in **both** 2D factors. For c1(L)=m u+n v, the standard Atiyah–Singer formula yields ind D_L^+=mn. For the prior-art five anomaly-free left-handed U(1) charges (1,5,−7,−8,9), the formal sum of charge-squared twisted indices is 220mn; cancelling cubic/linear anomalies does not mean that index sum vanishes.

**This is an honest topology-versus-chirality distinction:** retaining three native flat holonomies is possible in a closed continuum 4-manifold, but retaining them does not *force* chiral matter. The ribbon/handlebody thickening, added torus, U(1) flux, spin choice, and chiral field assignment remain external; **no admissible native 4D overlap lattice Dirac operator or physical Standard Model** has been built.

Producer: analysis/w33_20261014_toe71_4d_holonomy_and_index.py.

## Front 5 — Fully site-dependent Hartree–Fock, with native exchange

Go beyond TOE70's uniform sublattice Hartree ansatz. Use the full real-space spinless W33 80×80 hopping matrix H0 at native (π,π,π) and all 160 density-repulsion interactions

\[
H_{\rm int}=V\sum_{\langle i,j\rangle}
 (n_i-\tfrac12)(n_j-\tfrac12).
\]

Solve the site-dependent occupied projector ρ (40 occupied orbitals, canonical half filling) with the unrestricted HF effective matrix

\[
h_{ii}=V\sum_{j\sim i}(\rho_{jj}-\tfrac12),\quad
h_{ij}=(H_0)_{ij}-V\rho_{ij}\quad(i\sim j),
\]

with the Fock term optionally disabled as a matched Hartree control. No uniformity constraint is placed on the 80 local densities. Repeated eigendiagonalization with mixing converges to residual <10^−11. At four repulsions V=.05,.2,.4,.8, each with and without Fock, the two opposite initial sublattice biases converge to symmetry-related, equal-energy broken-density solutions.

Examples of **exchange-inclusive** solutions:

| V | HF quasiparticle gap | sitewise point-charge mean | sitewise point-density standard deviation |
|---:|---:|---:|---:|
| .05 | .05203797 | −.15519551 | .04414298 |
| .20 | **.24044421** | −.17235968 | .03997693 |
| .40 | .58144965 | −.19922780 | .03293488 |
| .80 | 1.63682147 | −.26390298 | .01648002 |

The V=.2 HF trial energy is ≈−66.7435015; it is ≈.84529816 below the symmetric half-filled zero-mode mixed reference trial. These are **self-consistent sitewise Hartree–Fock results, with exchange**, rather than TOE70's known non-self-consistent uniform density ansatz.

**Limits:** convergence to a self-consistent Slater determinant does not prove it is the global HF minimum, that the exact finite interacting system has a degenerate symmetry-breaking ground state, or that a thermodynamic gauge-invariant gap survives. The phase (π,π,π) remains an imposed gauge background in this test, and the interaction strength V is externally specified. Symmetry-breaking mean-field wavefunctions are well-known variational approximations, not exact eigenstates (see Scholarpedia, *The Hartree–Fock method*). No physical fermion mass hierarchy is derived.

Producer: analysis/w33_20261014_toe71_sitewise_hartree_fock.py.

## Reproducibility

Five independent source producers in analysis/, a focused tests/test_w33_20261014_toe71_five_fronts.py suite, and a GitHub Actions workflow that regenerates five JSON certificates. Producer stages have been independently prototyped using the native W33 graph in a local Python scientific runtime; the GitHub CI result is reported separately.

All exact statements above concern abstract graph topology, finite permutations or rational inequalities. Claims about MILP global optimality, HF symmetry breaking and native finite gauge low-energy eigenvalues explicitly retain their numerical status.

## The five strongest independent successors

1. Export and independently validate an **exact rational mixed-integer global optimality proof** for the 160-edge fixed-q disorder problem, then optimize the full 3×3 Hessian eigenvalue over edge weights.
2. Obtain **certified ordered** finite 22,638-dimensional gauge-block eigenvalue enclosures using inertia-checked interval sparse factorization, completing or falsifying the conditional unbounded-rotor gap proof.
3. Analyze the **effective second-order graph** of 20-octagon exact covers, compute its connected components and group representation content, and test finite-size quantum geometry selection.
4. Construct an actual **W33-derived four-dimensional overlap-Dirac lattice** on the preserved-holonomy spin manifold and quantify admissibility, overlap locality, index and anomaly cancellation without extra arbitrary continuum choices.
5. Compare the site-dependent HF phase against exact diagonalization of **small native interacting patches**, include full gauge dynamics and determine whether a nonzero order parameter and measurable gap survive beyond mean field.

**The physical Theory of Everything remains unsolved.**
