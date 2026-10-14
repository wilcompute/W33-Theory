# TOE68 — Five-front execution: native coupled gauge matter, a working 4D overlap index, symmetry and zero-mode rank

**Date:** 2026-10-14. **Starting point:** TOE67 exact continuous all-\(\beta\) flux theorem.  
**Science-status discipline:** mathematical theorem / exact certificate / finite numerical experiment / non-native control / open physical interpretation. A physical Theory of Everything is NOT solved.

## Intake and cross-checks

Read TOE67's source, the TOE65 238-winding-octagon edge product producer, TOE62's Gauss-constrained three-loop implementation, the exact native W33 projective symplectic core, and the native ribbon no-go. Also checked earlier U(1)' anomaly material before selecting chiral charges. The search deliberately separates existing theorems and previously published finite-model certificates from new work.

### Front 1 — Rational native edge disorder: a verified local optimality certificate

TOE66's native 17-high-edge assignment at 24.5% disorder is given by

\[
I=\{30,31,49,51,59,62,63,82,83,93,95,118,119,138,139,142,143\},\quad q=(0,-1,1).
\]

Reconstruct all 238 native winding octagons with their actual 160-edge product incidences. For \(w_e\in\{1-\epsilon,1+\epsilon\}\), the leading high-temperature three-\(\pi\) Hessian Rayleigh form is

\[
P_I(\epsilon)=72(1+\epsilon)^2(1-\epsilon)^6+
46(1+\epsilon)^3(1-\epsilon)^5+
34(1+\epsilon)^4(1-\epsilon)^4-
12(1+\epsilon)^8.
\]

At the exact fraction \(\epsilon=245/1000\), \(1000^8 P_I\) is **negative**. For every single one of the 160 edge flips, recompute the **integer** numerator with its actual eight-edge path products. All 160 flips strictly **increase** the Rayleigh value, the smallest increase being

\[
52{,}315{,}612{,}734{,}624{,}060{,}937{,}500>0.
\]

Thus the TOE66 witness is a strict **Hamming-distance-one local minimum** of this fixed-direction binary-corner objective at \(\epsilon=.245\). This is additional evidence of an isolated adversarial pattern, not a proof of global minimax optimality. The previous universal sufficient interval \(\epsilon\le0.14875640159...\) and counterexample \(\epsilon<0.244616\) remain unchanged. No claim that edge disorder preserves TOE67's all-\(\beta\) theorem.

**Source:** analysis/w33_20261014_toe68_combinatorial_fronts.py, front disorder_corner().

### Front 2 — A genuine dynamical gauge–fermion Hamiltonian on a native W33 octagon

One exact W33 Levi octagon is represented by vertices

\[
(0,40,4,44,1,45,13,41)
\]

and ordered native edge IDs \((0,16,17,4,5,53,52,1)\). Keep four mobile spinless fermions and a compact U(1) electric-flux coordinate \(m\in[-L,L]\). Assign the alternating Gauss background \(b=(1,0,1,0,1,0,1,0)\) and reconstruct ALL eight electric link fluxes from

\[
n_j=m+\sum_{a=0}^j(o_a-b_a),\quad j=0,\ldots,7;\qquad n_7=m.
\]

This exactly enforces \(n_{j-1}-n_j+o_j-b_j=0\) for every represented state, including the closing edge. The Hamiltonian includes diagonal \(g^2\sum_j n_j^2/2\), staggered-background gauge constraints, ordinary fermionic sign-correct native oriented link hops of magnitude \(\kappa\), and **actual magnetic cycle flux raising/lowering** \(-\eta(U+U^\dagger)/2+\eta\). A single boundary hopping necessarily updates the independent electric integer coordinate. We used \(g=.9\), \(\kappa=.6\), \(\eta=.25\) and verified exact matrix Hermiticity, Gauss preservation and sparse Ritz residuals.

| Integer flux cutoff L | Hilbert dimension | Ground energy | First gap | Probability at electric boundary |
|---:|---:|---:|---:|---:|
| 1 | 210 | -2.1337539997 | 0.6709906130 | 0.160095 |
| 2 | 350 | -2.1345423000 | 0.6705681103 | 0.000149866 |
| 3 | 490 | -2.1345424783 | 0.6705679753 | 1.13e-8 |

For a matched \(L=2\) zero-magnetic control, ground energy is approximately -2.3809288932. The dynamical magnetic sector therefore matters quantitatively. The nested flux cutoffs show good finite-volume numerical stabilization, **not a rigorous bound on the full untruncated spectrum**. This is one actual **native eight-cycle**, not the entire 80-site/160-link interacting system.

**Source:** analysis/w33_20261014_toe68_native_octagon_gauge.py.

### Front 3 — A canonical, fully equivariant local geometry *bundle*

TOE67 proved an isolated cyclic ordering of the four incident flags cannot be invariant under all native \(PSp(4,3)\) symmetry. Here we avoid selecting an ordering: every 4-valent Levi vertex has exactly three unordered partitions of its four incident half-edges into two opposite pairs. The collection of all three pairings is **canonical under every graph automorphism**, even though no single pairing is individually invariant under the full group.

Reconstruct projective points and lines; for five native symplectic transvections, check all 80 vertex fibers. **400 exact equivariance checks** pass. The point-fixing order-three transvection from TOE67 cycles the three possible pairings at its fixed vertex with **no fixed member**. This gives a discrete 3-valued gauge-like geometric degree of freedom that can enter an invariant sum of local pairing interactions. The **bundle** is fully symmetric; an individual ribbon remains an extra symmetry-breaking choice.

No actual 3+1 Lorentz metric, tetrahedral spacetime cellulation, gravitational constraint algebra or dynamical selection rule follows.

**Source:** analysis/w33_20261014_toe68_combinatorial_fronts.py, front matching_and_bundle().

### Front 4 — Actual computed nonzero overlap lattice index: a non-W33 control

Build a periodic, oriented \(3\times3\times3\times3\) Euclidean lattice, 81 lattice sites and 324 spinor components. Impose exact quantized U(1) background flux through the (0,1) and (2,3) torus coordinate planes:

\[
F_{01}=2\pi m/9,\qquad F_{23}=2\pi n/9.
\]

The simple periodic Landau construction uses phase twists at the boundary; checks of all plaquette products match the target fields to numerical roundoff. Assemble the full **Hermitian 324×324 Wilson kernel** with Euclidean gamma matrices and Wilson mass \(m_0=1\); compute \(\mathrm{ind}(D_\mathrm{overlap})=-\tfrac12\mathrm{Tr}\,\mathrm{sign}(H_W)\).

| Fluxes (m,n) | overlap index | minimum absolute kernel eigenvalue |
|---|---:|---:|
| (0,0) | 0 | 1.000000 |
| (1,0) | 0 | 0.638483 |
| (0,1) | 0 | 0.638483 |
| (1,1) | +1 | 0.345510 |
| (1,-1) | -1 | 0.345510 |

The indices match the continuum Chern product \(Q=mn\). Numerically stable nonzero kernel gaps make the signature meaningful at this precision. These spectral counts are **numerical**, not interval-certified eigenvalue enclosures.

The known standard example of five left-chiral U(1) charges \((1,5,-7,-8,9)\) has \(\sum q=0\) and \(\sum q^3=0\), with no vectorlike opposite pair. This is **prior art**, not new W33-derived matter content; see Babu, Jana and Lindner et al., *Chiral Abelian Gauge Theories with Few Fermions*, Phys. Rev. D 101 095032 (2020), https://doi.org/10.1103/PhysRevD.101.095032. Algebraic anomaly cancellation alone does not define a chiral gauge measure or lattice construction.

This **does not** construct a W33-native 4D gauge bundle or chiral Standard Model family. It supplies a reproducible positive-control harness for testing a future native discretization.

**Source:** analysis/w33_20261014_toe68_overlap_control.py.

### Front 5 — Generic zero-mode lifting without a phenomenological gap claim

Compute one explicit perfect matching of all 40 point-line incidence rows/columns in the 40×40 W33 hopping block. Rescale precisely the 40 matched **native links** by a common \(t>0\), while keeping TOE67's three phase chords at \(\pi\). The determinant is a degree-40 polynomial in \(t\) whose leading coefficient is **exactly \(+1\)** for this canonical matching, so it is not identically zero. It has only finitely many roots. Therefore the hopping block becomes full rank for generic \(t\) **arbitrarily close to 1**, removing all exact one-particle zero modes and giving a unique canonical half-filled free-Fock ground state with a finite *one-particle* gap at this fixed phase.

Direct 40×40 SVD at \(\pi\), under matching weights:
- \(t=1\): smallest singular value approximately \(1.5\times10^{-17}\);
- \(t=1.0001\): approximately \(4.66\times10^{-7}\);
- \(t=1.001\): approximately \(5.03\times10^{-6}\);
- \(t=1.01\): approximately \(8.74\times10^{-5}\).

**Exact theorem:** the determinant polynomial has a nonzero leading coefficient. **Numerical confirmation:** the indicated finite positive perturbations are nonsingular. This establishes that TOE67's 24 massless zero modes are not protected against generic positive *edge-amplitude* perturbations, even if bipartiteness is retained. It does **not** demonstrate a many-body interacting gap, parameter-free hierarchy, uniform free-energy flux selection at all \(\beta\), Lorentz symmetry or gravity.

**Source:** analysis/w33_20261014_toe68_combinatorial_fronts.py, front matching_and_bundle().

## Verification and review gates

All five fronts were independently evaluated server-side with self-reconstructed \(\mathbb F_3^4\) W33 lines. Four model tests plus the exact rational flip check passed; full standalone repo-based producers and pytest checks are included for repeatability. Numerical eigensolver outputs are sampled finite-cutoff results, not formal floating-point interval certificates. This research does not establish an overarching dynamical spacetime or unique physical W33 theory.

Additional context: standard overlap index and admissibility results are described in https://doi.org/10.1016/S0550-3213(02)00567-9; Hamiltonian compact U(1) truncation benchmarks have advanced (https://doi.org/10.1140/epjc/s10052-026-15753-6). Neither proves anything specific to W33.

## Five strongest independent next steps

1. Certify a **global** native edge-product minimax disorder bound through symmetry reduction and branch-and-bound beyond the local 160-flip result.
2. Scale the exact-Gauss **coupled fermion and magnetic** Hamiltonian from one octagon to overlapping octagons, with explicit spectral interval bounds and Wilson/charge screening.
3. Introduce an invariant Hamiltonian on the **three-pairing bundle**, then test whether its low-energy ground sector selects manifold-compatible local charts.
4. Replace the four-torus control with an **actual W33-derived admissible 4D lattice**, compare integer overlap index, anomaly cancellation and spin structure against a matched non-W33 control.
5. Study generic zero-mode lifting **with** gauge dynamics, prove or refute a stable interacting gap, and derive a quantitative falsifiable W33-specific observable.

**No physical Theory of Everything is solved.**
