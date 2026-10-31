# Eight-front W33 quantum-group and physics falsification campaign
**Research packet:** 2026-10-31, second continuation of commit `ad8846e599812d2327821521c53dacd6058bba06`.

**Producer:** `analysis/w33_20261031_eight_quantum_fronts_round2.py`.
**Frozen certificate:** `data/w33_20261031_eight_quantum_fronts_round2.json`.
**Regression:** `tests/test_w33_20261031_eight_quantum_fronts_round2.py`.

All reported values are from deterministic executed code. "PASS" means passing the listed algebraic or numerical assertions, *not* verified experimental physics, a proof of a TOE, an emergent cosmological model, or full completion of an open classification. Existing uncommitted research by other agents was not overwritten. The repository already contained earlier W33 metaplectic, qutrit Clifford, QCA and characteristic-five torsion studies; distinguish exact new connections from prior concepts.

## 1. Characteristic-five torsion: explicit seven-dimensional operator and the remaining gap

The q=9 48-line 24x24 biadjacency's previously certified Smith form contains seven 5 factors. Prior work identified an order-five *ambient* PGSp(4,9) lift of an abstract line-graph automorphism, confirmed on all 820 projective points and all 820 isotropic lines.

This experiment rebuilds the 48-line graph and B, computes `ker_F5(B)` (dimension 13), and forms the seven-dimensional quotient by six independent reduced rational-kernel vectors. Instead of only quoting Jordan ranks, it constructs the complete 7x7 `GF(5)` operator matrix. Powers of `g-I` have ranks `[7,4,2,0,0,0]`, proving Jordan partition (3,3,1), order five, and fixed dimension three. Directly solving the 49-variable commutation equations gives a **17-dimensional centralizer**, as `sum_{i,j}min(lambda_i,lambda_j)=17` predicts.

This is a genuine explicit cyclic-subgroup action. It does **not** identify an entire 2.A5 or A5 module: the complementary order-2/3 operators must be lifted to the same ambient group, assembled and tested against multiplication relations. The previous individually primitive rational nullvectors also need a canonical *saturated integral kernel* audit before identifying the chosen quotient with a canonical integral torsion action.

## 2. Full 81-mode optics: realistic negative controls

Reconstruct the two canonical directional pure 3-mode states `(I+F^2/14 +/- F/sqrt14)|0>`, with overlap `-3/7`, and derive the Helstrom eigenbasis directly rather than simply importing the previous analyzer. Form `I27 tensor Q3`, an orthogonal full 81x81 analyzer over 27 independent 3-mode triangles. Validate unitarity.

In the first readout model, choose **explicitly assumed** five-stage survival `.995^5 = .9752487531`, per-port detection efficiencies `[.92,.90,.88]`, and small dark-click probabilities `[.0003,.0004,.0002]` conditional on no detected signal. Include an explicit no-click outcome; probabilities sum exactly to one. Recompute optimal equal-prior Bayesian discrimination with the **full multinomial likelihood** over four outcomes for 1, 5, 10, 15, 20 injected trials. The ideal single-photon Helstrom error 0.048246 becomes `0.094676` under this supplied imperfection model. At zero analyzer drift and these assumed detector parameters the 10-injection idealized Bayesian error is `8.0882e-5`, 20-injection is `4.6027e-8`. Strong analyzer drift 0.20 radians degrades the 1-shot error to about 0.11070.

The second model actually couples adjacent *different* triangles in the 81-mode analyzer through sequential passive rail rotations of angles 0, .025 and .10 radians, includes 81 nonuniform detector efficiencies and 81 small dark-click channels, and injects a state at triangle 13. It measures both leakage outside the addressed triangle and 82-outcome Bayesian classification error; zero-coupler leakage must be zero, and nonzero coupling increases leakage. This is genuine inter-triangle optical-mode crosstalk in a specified simplified circuit, not a fabricated device calibration. No multiphoton dynamics, correlated detectors, thermal phase drift or validated fabrication tolerances.

## 3. Exact 8-site distinct-color clock frustration optimum

The existing W33 mediator `E_ab=J(3-Tr Pi_aPi_b)-K||[Pi_a,Pi_b]||^2` distinguishes collinear and noncommuting directions. On a hypothetical complete 8-site spatial graph with **distinct Pauli direction labels**, it is impossible to realize all 28 bonds as noncommuting: the maximum pairwise noncommuting W33 direction set is size seven. This work exhaustively lists 2,880 seven-direction cliques, extends each by every possible eighth direction, and finds an eight-direction witness with **exactly one commuting bond**, hence 27 satisfied noncommuting bonds. Therefore *the global combinatorial optimum for distinct eight-direction labels is exactly 27/28*, not merely a heuristic upper bound.

Frozen witness indexes: `[0,9,26,27,30,32,34,4]`. At externally supplied J=1, K=2, energies are `2-4K/3=-2/3` for each noncommuting pair and `2J=2` for the commuting pair; total `27(-2/3)+2=-16`. This is not an exact global thermal/vacuum optimum allowing repeated tick labels or allowing a more complicated many-body Hamiltonian.

## 4. Spatial locality/no-go: finite-depth native Clifford gates cannot force chiral transport

Explicitly enumerate across-cut wire permutations of two alternating nearest-neighbor qutrit SWAP layers. The first-layer/second-layer composition transports exactly one input qutrit left and one right across a cut: `3^(1-1)=1` as the GNVW index. An infinite translation one site to the right transports one qutrit only right: `3^(1-0)=3`. Native on-site Jones/Clifford gates and any additional bounded-depth local circuits cannot change the index.

Hence merely concatenating native braid gates into a finite-depth 1D local circuit cannot yield a genuinely anomalous chiral QCA. One needs a nontrivial shift, a 2D anomalous boundary, a different local algebra or other supplied dynamics. The index result is standard prior art, reproduced as a concrete falsifier here; no native 2D anomaly has been derived.

## 5. Matter–geometry: numerical convergence and reversibility, not Einstein gravity

Continue the earlier *externally postulated* positive Hamiltonian on a periodic four-dimensional **spatial** lattice:

`H=1/2 Σ[p_u²+p_phi²+exp(2alpha phi)(D u)^T Q(D u)+kappa|D phi|²+mu²phi²]`.

Integrate the same initial data to T=1.6 with time steps 0.02, 0.01, 0.005 using symmetric velocity Verlet, then integrate *backwards* with the corresponding negative steps. Direct reversal errors are O(10^-16), while relative energy errors are ~0.00123834, 0.000309437, 0.000077350, giving error ratios **4.0019** and **4.0005**: strong second-order convergence consistent with the integrator. For nonzero coupling the conformal metric field responds with norm ~0.01396.

A further analytic lattice conservation identity is that u has a global shift symmetry: it enters H only through forward differences; summing its canonical force over periodic positions telescopes to zero. Thus total p_u is conserved by this model. This is a conventional Hamiltonian/Noether charge, *not* proof that W33 derives general covariance, Lorentzian signature or spin-two gravitons.

## 6. Outside-box physics: native Jones braid commutant is exactly parity 5+4

The native five-strand Jones braid generating projectors act on the two-qutrit 9D carrier. Form the complex linear commutator equations `[X,Pi_i]=0` as a 405x81 matrix and count the numerical kernel singular values; the commutant has dimension **2**, with a good nonzero singular-value separation.

Construct explicit `P|a,b>=|-a,-b>` over GF3. Verify all five projector commutators vanish, P²=I, Tr(P)=1. Its parity eigenspaces are dimensions **5 and 4**. Because I and P are independent and exhaust the two-dimensional commutant, the full commutant is exactly `span_C{I,P}`. Therefore the *-algebra generated by these projectors acts irreducibly on the 5D and 4D blocks separately (finite bicommutant/Burnside). The 9D representation is reducible, and the native finite *unitary braid subgroup* remains not dense even though the complex linear operator algebra can span full block matrices.

This concretely relates the native W33 metaplectic braid representation to the parity splitting of finite Weil representations. This identification is a finite algebraic equivalence, **not** a new anyon type or a physical fusion sector.

## 7. Outside-box physics: Wigner negativity separates native braid from injected magic

Use the explicit Hermitian order-3 phase-point operators `A_(q,p)` on each qutrit and their 81 two-qutrit products to evaluate the Gross discrete Wigner function.

For the native maximally entangling `(1,1,0,0)` Clifford/Jones braid applied to the two-qutrit product stabilizer `|00>`, the 81 Wigner entries are all nonnegative within numerical tolerance, with **mana 0**. Apply an **externally supplied** non-Clifford phase `diag(1,1,exp(i pi/3))` to `|+>` on one qutrit, tensor `|0>` on the other. Its minimum Wigner value is exactly approximately **−1/27**, total Wigner `L1=13/9`, mana `log(13/9)≈0.367725`.

This is a *resource-theory obstruction*: the proposed finite Clifford braid gates acting on stabilizer preparations cannot create this magic resource without a non-Clifford operation or suitable non-stabilizer resource. It is not an experimental claim that W33 produces the supplied injection. It follows established odd-prime Wigner contextuality/magic theory.

## 8. Outside-box physics: 48-line graph cycle torsion is not seven Smith factors

Build the selected 48-line intersection graph directly. Its 48 vertices, 240 edges and one connected component imply `H1(graph; Z)=Z^193`, **without torsion**, by the standard cellular chain complex of a graph.

Enumerate all **1,680 four-cycles** and attach formal 2-cells to them; compute the boundary image rank over GF2, GF3, GF5 using exact modular sparse elimination. For each of the three fields the rank is **193**, equal to the graph's original cycle-space dimension; hence the *square-filled complex* has `H1=0` over each tested field.

This is an important falsification of overinterpreting Smith factors: the seven `Z/5` torsion terms in an independent 24x24 *biadjacency* cokernel do **not** correspond to the first homology torsion of the original 48-vertex one-dimensional graph. Nor does this calculation prove the square-filled complex has zero integral torsion at all primes (only fields 2,3,5 tested). A physical topological gauge interpretation must specify an actual chain complex and the relevant 2-cells/holonomies first.

## Literature / independent context

- Gross, Nesme, Vogts, Werner, *Index theory of one dimensional quantum walks and cellular automata*, arXiv:0910.3675 (original QCA index and shifts).
- Jones and Lim, *An index for quantum cellular automata on fusion spin chains*, arXiv:2309.10961 (categorical/fusion-chain generalization).
- Cui and Wang, *Universal quantum computation with metaplectic anyons*, J. Math. Phys. 56, 032202 (2015), DOI 10.1063/1.4914941: metaplectic SU(2)4 braid plus charge measurements needed for universality.
- *Quantum magic dynamics in random circuits*, npj Quantum Information (2026), DOI 10.1038/s41534-026-01253-8: odd-prime Wigner negativity and mana.
- Mlodinow and Brun, *Quantum field theory from a quantum cellular automaton in one spatial dimension and a no-go theorem in higher dimensions*, Phys. Rev. A 102, 042211 (2020): explicitly warns naive higher-dimensional QCA derivations of field theory are obstructed.

## Reproduction

From repository root:

```powershell
python -m analysis.w33_20261031_eight_quantum_fronts_round2
python -m pytest -q tests/test_w33_20261031_eight_quantum_fronts_round2.py
```

All eight functions have explicit assertions and saved machine-readable numbers. The tests verify modular nilpotent ranks, independent algebraic block sizes, 81-mode optical normalization, second-order energy scaling, negative and positive contextuality controls, clock packing and homology dimensional constraints.

## Top five independent next tests, chosen after the eight current results

1. **Full finite-group module:** lift and verify the *same-subgroup* order-2/order-3 symmetries in PGSp(4,9), compute actual 2.A5 relations on the canonical saturated seven-dimensional torsion lattice, and extract modular composition factors. Do not infer a subgroup from separate graph automorphisms.
2. **Hardware-calibrated 81-mode optical inference:** replace assumed loss/dark/background curves with measured transfer matrices and detector likelihoods; quantify identifiability of oriented pulse sign vs unknown rail gauge.
3. **Quantum clock actual low-energy phase:** diagonalize the multi-site positive local quantum Hamiltonian on small non-bipartite spatial graphs, include the exact 8-site 27/28 frustration barrier and distinguish a true phase transition from imposed couplings.
4. **Chern/QCA genuinely intrinsic:** test 2D periodically driven native W33 Clifford layers for protected edge transport and evaluate a bulk invariant and anomaly without inserting a shift or QWZ Chern band by hand.
5. **Dynamics/geometry constraints:** introduce discrete tetrads and gauge/connection variables with first-class constraints, identify would-be spin-2 degrees and require actual continuum Ward identities; reject models that merely carry the supplied acoustic Q or a scalar conformal mode.
