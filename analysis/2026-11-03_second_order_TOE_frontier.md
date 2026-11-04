# 2026-11-03 — Five second-order TOE constraints, plus a native W33 operator reconstruction

**Status: finite mathematical/computational controls only.** No derivation of Lorentzian 3+1D spacetime, general relativity, graviton physics, the Standard Model, Planck scale, or observed particle masses. These tests independently extend the six-front prior baseline `94ee11b997c448f310327c4a80902500b4173ba7`; they do not silently promote previously assumed ingredients to predictions.

## Intake, prior owners, and methodological decisions

Read the parallel `94ee11b99` six-front release and newest `12563–12582` cosmology branch markers. The previous six-front baseline already gave (i) abelian toroidal Wilson plaquettes, (ii) two density-matched causal growth null models at N=72, (iii) genuine 2D Pachner moves on a sphere, (iv) separately conserved free scalar stress tensors with a soft-graviton Ward identity, (v) the five-qubit algebraic code locality ambiguity, and (vi) distance extracted from a **supplied** hopping graph. This round makes the local mathematical controls stronger and tackles the remaining hidden assumptions:

1. Nonabelian cube gauge curvature with all parallel transports and gauge covariance.
2. Fixed-parameter causal growth tested across **four sizes**, not just a single calibrated N.
3. Local **dimension-changing** simplex attachment, with complete 256-state homology census.
4. **Interacting** two-species stress-energy exchange and universality as a conservation condition.
5. Microscopic Pauli commutator tomography, with an explicit three-body false-positive and local basis gauge ambiguity.
6. Bonus: the same operator-tomography principle for 40 W33 one-excitation modes, with strong-regularity checks.

Project code: `analysis/2026_11_03_second_order_toe_frontier.py`. Producer certificate: `data/2026_11_03_second_order_toe_frontier.json`. Regression: `tests/test_20261103_second_order_toe_frontier.py`.

## A. Nonabelian Bianchi identity: curvature requires transported face comparison

Assign 12 independent SU(2) link matrices to the edges of one 3-cube. Form six oriented face Wilson products. Opposite faces live at different corners: to compare them, each face must be transported to a common base vertex by a specified link path. A combinatorial shelling of the six boundary faces cancels every link letter and its inverse, giving an exact free-group word identity and a matrix product equal to the identity. Random SU(2) links need not commute.

Deterministic seeded results:

- Ordered six-face Bianchi identity residual: **8.5663e-16**.
- Under independent site-by-site SU(2) gauge changes, rooted face holonomies transform by the single basepoint conjugation; maximum covariance residual: **1.1322e-15**.
- Without transporting displaced face holonomies to the common basepoint, the analogous naive product has identity defect **1.6243**.
- At least one nontrivial face holonomy differs from identity by norm **2.5845**.

The positive result is a **lattice gauge** Bianchi identity, not a gravitational Levi-Civita connection, a curved-space ADM Hamiltonian, an Einstein field equation, or a derived gravitational symmetry. It does clarify the missing structural ingredient in the earlier flat lattice spin-two control: naive replacement of commuting flat derivatives by position-dependent operators is insufficient. A future gravitational construction must transport tensor/gauge data consistently and close its constraint algebra.

Reference: Höhn, *Canonical linearized Regge calculus: Counting lattice gravitons with Pachner moves*, Phys. Rev. D 91, 124034 (2015), https://doi.org/10.1103/PhysRevD.91.124034 . This concerns the closely related constraint problem; the present code is its own elementary SU(2) group identity, not a reproduction of that gravitational paper.

## B. A causal growth law calibrated once fails across volume

Use the existing verified 4D Minkowski Alexandrov sprinkling constructor (the dimension **is externally supplied**). The theoretical ordering fraction is

```text
r_4 = Gamma(5)Gamma(2) / (2Gamma(6)) = 1/10.
```

Train a sequential transitive-percolation growth law on **N=48 only** using 32 independent 4D target histories and 26 null samples per p grid point. Select `p=0.05` by **comparable-pair fraction alone**. Freeze that p. At N in {32,48,72,96}, evaluate new 30 target and 45 CSG null histories at each size.

| N | 4D target density | CSG density, p=0.05 | 4D mean height | CSG mean height |
|---:|---:|---:|---:|---:|
| 32 | 0.100403 | 0.082034 | 3.300 | 4.289 |
| 48 | 0.099675 | 0.109082 | 3.900 | 5.756 |
| 72 | 0.093571 | 0.158355 | 4.133 | 8.156 |
| 96 | 0.099181 | 0.228879 | 4.867 | 10.556 |

The target ordering fraction is approximately stable (~0.1), whereas the fixed-p CSG ordering fraction drifts by **+0.14685** from N=32 to N=96. CSG longest chains grow more rapidly. One-parameter finite-size calibration therefore does **not** recover a stable 4D Alexandrov causal ensemble. This rules out the *specific fixed-parameter transitive-percolation null as a four-dimensional sprinkling surrogate across this measured size range*, not all causal-set dynamics or all methods of emergent dimension.

Reference: Surya, *The causal set approach to quantum gravity*, Living Reviews in Relativity 22 (2019), https://doi.org/10.1007/s41114-019-0023-1 ; this is where the distinction between sprinkling kinematics and a physically selected dynamics matters.

## C. A real local dimension-changing move necessarily changes topology or manifold purity in this packet

Begin with the octahedral S^2 complex: 6 vertices, 12 edges, 8 triangles, Betti vector over F2 `(1,0,1,0)`. Choose a single new apex vertex, then independently attach a tetrahedron over any subset of the eight original triangular faces, closing all simplices under taking faces. These are **genuine simplex attachments** (not Pachner moves), and their choice is local to one original triangular face.

Exhaustively enumerate all 2^8 = **256** such complexes, build boundary matrices `∂1,∂2,∂3` over F2, verify alternating Euler and Betti identities, and inspect which are pure.

- No attached tetrahedron: the original pure **2D sphere**, `f=(6,12,8,0)`, `betti=(1,0,1,0)`.
- Between one and seven attachments: **254 mixed-dimensional, nonpure complexes**. Their second Betti number is not even fixed; there exist states with `beta2=2,3,4`, depending on which faces were selected.
- All eight attached: pure **3D cone over S^2**, a **three-ball with boundary**, `f=(7,18,20,8)`, `betti=(1,0,0,0)`.

Thus real dimension change can occur in a finite local attachment system, but a smooth closed four-dimensional spacetime phase does not appear. In this finite family a move-by-move 2D-to-3D path must cross nonpure complexes, while the final pure 3D object is only a ball with boundary. This is not a universal theorem forbidding dimension-changing models with more fundamental primitives; it identifies what a candidate action must address rather than concealing dimension changes inside a global state label.

Reference for dimension-preserving bistellar/Pachner moves: *Small Triangulations of 4-Manifolds and the 4-Manifold Census*, Discrete & Computational Geometry (2026), https://link.springer.com/article/10.1007/s00454-026-00818-w .

## D. Nonuniversality becomes dynamically inconsistent when species interact

Consider two classical scalar fields in 1+1-dimensional flat spacetime:

```text
L = 0.5 (partial phi)^2 + 0.5 (partial chi)^2
    - 0.5 m^2 phi^2 - 0.5 n^2 chi^2
    - (g/2) phi^2 chi^2.
```

For bookkeeping only, assign fraction `alpha` of the shared interaction potential to a nominal species-A stress tensor and the rest to B. Using the interacting field equations, exact symbolic tensor differentiation gives:

```text
partial_mu T_A^(mu nu) =
 Q^nu = g[(alpha-1) phi chi^2 partial^nu phi
           + alpha phi^2 chi partial^nu chi],
partial_mu T_B^(mu nu) = -Q^nu.
```

Therefore, for arbitrary couplings to a candidate massless spin-two source,

```text
partial_mu (kappa_A T_A^(mu nu) + kappa_B T_B^(mu nu))
    = (kappa_A-kappa_B) Q^nu.
```

The conserved, physically relevant object is the **total interacting stress tensor**. In a fixed illustrative field configuration with `alpha=1/2, g=2`, the current is `Q^nu=(-174,+42)`; selecting `kappa_A=1, kappa_B=2` yields a **nonconserved** source with divergence `(+174,-42)`. Identical couplings produce zero divergence.

Important qualification: splitting interaction stress between species is conventional. The test is a classical conservation/linear source-consistency check, not a complete nonlinear spin-two theorem or a measurement of Newton's constant. It builds directly on the earlier noninteracting soft graviton Ward test, which separately requires universal coupling for nonforward two-species scattering.

Reference: Weinberg, *Photons and Gravitons in S-Matrix Theory*, Phys. Rev. 135, B1049 (1964), https://doi.org/10.1103/PhysRev.135.B1049 .

## E. Hamiltonian commutator tomography and the fundamental tensor-factor caveat

In a prescribed 5-qubit tensor factorization, take

```text
H = sum_(i<j) J_ij X_i X_j + sum_i h_i Z_i.
```

The exact double commutator identity for distinct sites is

```text
[Z_j,[H,Z_i]]=4 J_ij Y_i Y_j,
J_ij = Tr(Y_iY_j [Z_j,[H,Z_i]])/(4*2^5).
```

Set five nonzero two-body couplings on a weighted ring, keep unknown local Z fields. All ten pair projections recover the five nonzero couplings and five zeros, maximum matrix reconstruction defect **1.11e-16**.

Two controls expose hidden assumptions:

- A genuine three-body term `1.2 X_0 X_1 X_2` generates a nonzero double commutator norm (**27.1529**), despite containing no `X_0X_1` two-body coefficient. A naive nonzero-commutator edge detector would hallucinate a two-body interaction. Projecting onto the **correct Pauli tensor basis** gives exactly zero.
- A local `Z_0` conjugation flips the signs of recovered incident XX couplings while preserving their magnitudes and all physics under the transformed local frame. Thus the local Pauli-frame choice remains a gauge/reference input.

This is a useful route to *operationally reconstructing* a microscopic interaction graph **when tensor factors and local measurements are available**, not a derivation of those factors from a coordinate-free information algebra.

### Bonus — 40 native W33 modes

Build the symplectic projective geometry directly from `F3^4`, yielding **40** projective points and the W(3,3) collinearity graph **SRG(40,12,2,4)** with **240** edges. Supply its adjacency as the one-excitation 40-mode hopping Hamiltonian `H`, and local occupancy projectors `P_i=|i><i|`. Then for any two distinct modes:

```text
[P_j,[H,P_i]] = H_ij |i><j| + H_ji |j><i|.
```

This matrix-unit identity determines the interaction graph exactly from a pair's double commutator. Fifty explicit 40×40 matrix probes verify zero residual. The geometry W33 and the Hamiltonian were **inputs**; the valid result is an operational readout in the 40-mode photonic Hilbert space, not a spontaneous selection of W33 or an implementation of a universal photonic computer.

See recent work on Lieb-Robinson information transport and the distinction between a given local interaction and emergent propagation, e.g. McDonough et al., *Lieb-Robinson Bounds with Exponential-in-Volume Tails*, PRX Quantum 6, 040322 (2025), https://doi.org/10.1103/n242-m1l2 .

## Cross-front inference

The five negative/positive controls clarify a single problem:

**A theory cannot be declared emergent merely because its output admits a geometric re-interpretation.** We can impose W33 and reconstruct its graph; impose link gauge fields and satisfy a nonabelian Bianchi identity; impose a simplicial action and locally change dimension; impose an interacting stress tensor and derive conservation conditions; or impose a growth law and compare causal dimensions. None of these independently selects *the same* microscopic dynamics, 3+1D Lorentzian continuum phase, universal interacting spin-two force, physical time calibration or gravitational scale.

A materially stronger next theorem must derive at least **two of those structures from one frozen action**, with the remaining observable held out. This is why independent controls and hostile nulls are essential.

## Reproduce

```powershell
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD='1'
python -m pytest -q -s -o addopts='' tests/test_20261103_second_order_toe_frontier.py --maxfail=1
```

The test suite recomputes all six certificates using deterministic seeds, with independent checks of Bianchi closure, causal scale drift, simplicial Betti counts, interacting stress divergence, two-body Pauli extraction and W33 SRG/commutator identities. Run from repository root. Avoid interpreting any algebraic finite witness as observed experimental evidence without separately defined physical measurement procedures.
