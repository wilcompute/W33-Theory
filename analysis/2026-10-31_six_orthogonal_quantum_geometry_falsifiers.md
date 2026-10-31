# W33 continuation: six independent finite-field, quantum-information and gauge falsifiers
**31 October 2026. Status:** six deterministic research producers + independent regression. These are finite mathematical and supplied toy physical models, **not** a TOE or any claim of observed particle physics.

## Parallel-agent provenance / duplicate avoidance

We inspected the then-latest \`e7ba2d6243c18017abbba6e00aa07a9d18b4d805\` and local unpushed \`75c80b29c\` and \`bf26b8779\`, and the independent \`6343cdf59\` plus \`937445da5\` branch. Critically **the complete seven-dimensional A5×C2 module is ALREADY solved by parallel work** as \`1_even+3_even+3_odd\`. We did not repeat it. A prior September 2026 script \`analysis/w33_20260901_clique_h1_equals_building_steinberg.py\` already proves the clique H1 is Steinberg81. The 2026-10-09 exact integral clique/Levi bridge already proves the 81-cycle correspondence. Neither is ours. A prior October 31 parallel script already supplied four-label finite quantum Hamiltonians and an SO(2) finite gauge Ward test. We built different systems to establish independent consequences.

**Producer:** \`analysis/w33_20261031_six_orthogonal_falsifiers.py\`
**Frozen output:** \`data/w33_20261031_six_orthogonal_falsifiers.json\`
**Regression:** \`tests/test_w33_20261031_six_orthogonal_falsifiers.py\`.

## 1. Actual seven-dimensional characteristic-five torsion admits invariant orthogonal structures, but no alternating form

Read the 7×7 GF5 generator matrices for orders2,3,5 from the already-proven actual common A5×C2 geometric subgroup, \`data/w33_20261031_full_subgroup_GF5_representation.json\`. Independently solve \`g^T B g = B mod5\` for every generator in 28 symmetric and 21 alternating unknowns. Exact modular Gaussian elimination gives:

- symmetric invariant bilinear forms: **3-dimensional** space; exhibited basis ranks **3,7,7**;
- alternating invariant bilinear forms: **zero-dimensional** space.

This matches the three irreducible central-parity blocks and constrains any interpretation as a canonical symplectic quantum phase space; the odd-dimensional module could not admit a nondegenerate alternating form even without symmetry, but this test excludes *every* nonzero invariant alternating form. None of the GF5 quadratic forms is a measured Lorentzian metric.

## 2. Actual resource-accountable qutrit Strange-state heralding

The native TLJ idempotent \`f4=|0><0| tensor |S><S|\`, \`|S>=(|1>-|2>)/sqrt2\`, was established in prior commit \`7a57f825\`. Unlike treating \`f4\` as a free operation, here construct a concrete **ancilla-controlled qutrit parity** unitary instrument. Set \`R|j>=|-j mod3>\`, \`P_-= (I-R)/2=|S><S|\`. An ancilla qubit |0>, Hadamard, controlled-R, Hadamard, ancilla Z measurement implements the two-outcome projective measurement. From a stabilizer input |1> the heralded success probability is **1/2**, with remaining qutrit exactly |S>, Wigner minimum -1/3, L1 5/3, mana log(5/3). Both Kraus maps follow directly from the unitary six-dimensional matrix.

The **controlled-R interaction is an externally supplied nonstabilizer-capable resource**: this does NOT violate stabilizer mana monotonicity or give free Clifford-to-magic conversion. Destructive photon counting consumes a photon; a usable optical qudit requires QND readout, teleportation/heralding, or a further supplied resource. Under independently assumed *depolarizing noise on the heralded output*, \`rho=(1-eps)|S><S|+eps I/3\`, Wigner negativity vanishes at eps=3/4; this is a resource-theory negativity boundary, NOT an error-correction threshold. Published 2026 comparator: Prakash & Singhal, *Search for high-threshold qutrit magic-state distillation routines*, Physical Review A 113, 042404 (2026), DOI 10.1103/61q5-f754. Also Jain & Prakash 2020, Phys Rev A 102,042409.

## 3. Exactly soluble native 40-direction one-dimensional nearest-neighbor clock

This is independent of the earlier 120-tick transfer clock or the all-to-all Turan theorem; we **select a single spectral outcome** for each of the 40 W33 Pauli directions. On the supplied 1D cyclic spatial chain, use bond costs \`0\` same direction, \`2J\` distinct commuting, \`epsilon=2J-4K/3<0\` noncommuting. The 40×40 transfer matrix \`T=I+a A_W33+b (J40-I-A_W33)\`, \`a=e^{-2beta J}\`, \`b=e^{-beta epsilon}\` has EXACT spectrum:

    lambda0 = 1+12a+27b (mult1)
    lambda2 = 1+2a-3b (mult24)
    lambda-4= 1-4a+3b (mult15)

The script checks all forty numerical eigenvalues against this analytic spectrum at beta=.05,.2,.7,1.5,3,10 with J=1,K=2. For every finite beta, all transfer entries are strictly positive, so Perron-Frobenius forbids a finite-temperature 1D nonanalyticity. The zero-temperature limiting correlation length is 1/log9 (~.455 lattice sites) and entropy per site log27. Finite low-temperature degeneracy is not symmetry breaking or spontaneous time.

## 4. No equivariant linear identification Steinberg81 with 81 two-qutrit Pauli vector labels

The previous repo has ALREADY proved \`H1(W33 clique;C)\` is the irreducible dimension81 Steinberg module under PSp(4,3), hence its invariant dimension is 0. A common temptation is to identify 81 topological harmonic modes with the 81 two-qutrit Pauli labels in F3^4 using their equal count.

But symplectic transvections act on all 81 Pauli vectors with **two orbits**: the singleton zero vector and one orbit of all 80 nonzero vectors (enumerated explicitly using five generating transvections). Consequently the Pauli-vector **permutation module** contains a two-dimensional fixed subspace (one constant on each orbit). The irreducible Steinberg81 does not. Hence the two 81-dimensional representations are NOT isomorphic equivariantly over C, despite the dimensional coincidence. This does not forbid alternative tensor, nonlinear, characteristic-three, or 81-photonic-mode bridges, but it precisely falsifies the naive Pauli-label permutation identification.

## 5. Noncompact Lorentz frame/connection gauge Ward identity, with GR constraint limitation exposed

Move beyond the prior supplied SO(2) frame model to an explicitly **non-Abelian SO^+(1,3)** link connection. Define \`eta=diag(-1,1,1,1)\`, boost generators Kx, Ky and rotation Jz with \`[Kx,Ky]=-Jz\`. On an assumed periodic 3×3 two-dimensional spatial lattice, assign four-vector frames at sites and Lorentz links; compute

    S=(1/2) sum_(site,mu) [e(site+mu)-U(site,mu)e(site)]^T eta [same].

Transform independently at each site \`e(x)->G(x)e(x)\`, \`U(x,mu)->G(x+mu)U(x,mu)G(x)^-1\`. Test nonuniform random boosts and rotations, verifying action and plaquette Wilson-trace invariance to <1e-10 and a local gauge Ward derivative to <1e-8. This is **genuinely noncompact Lorentz gauge covariance**, in contrast to earlier SO2.

However this action is **indefinite**, a 2D spatial test substrate is supplied, and no tetrad constraints, first-class Dirac algebra, Einstein-Hilbert/Palatini term, dynamical light cone, or stable Hamiltonian has been derived. It is not 3+1D Einstein–Cartan. Comparator: Hamilton, *Covariant Hamiltonian tetrad approach to numerical relativity*, PRD96 124027 (2017), DOI 10.1103/PhysRevD.96.124027; 2026 Chrono-Grid work DOI 10.1140/epjc/s10052-026-16018-y is another proposed *assumed* discrete-time gauge framework and not independent experimental validation.

## 6. Anomalous 2D Floquet edge is stable to unitary dressing; noisy channel needs separate criterion

The prior verified 13-Jones-tick SWAP and 52-tick-layer four-stage 2D exchange loop were in \`7a57f825\`. Exact finite open-lattice edge orbit lengths at L=4,6,8 remain 7,11,15, and GNVW active-edge qutrit index remains 3. By the GNVW theorem, multiplying by bounded-depth **unitary local** circuits cannot change this integer/rational transport index. Onsite coherent miscalibrations change the local transported qutrit basis but cannot remove the index as long as the unitary QCA assumptions persist.

A deliberately simple independent *information survival per layer* proxy \`eta^52\` is frozen for eta=1,.999,.995,.99,.98. This is not a robustness theorem for a noisy **channel**: completely positive nonunitary noise does not possess the standard unitary GNVW index. Measuring channel memory, entanglement fidelity and edge transport under actual correlated noise remains required; no topological fault-tolerance threshold is claimed.

## Main discipline / outside-the-box conclusion

The strongest hypotheses now have both an enabling operation and an independent obstruction: GF5 torsion has orthogonal but not symplectic invariants; root-of-unity Jones gives an actual Strange projector but its heralding instrument costs a controlled non-Clifford measurement; a 2D Floquet boundary supports a nontrivial chiral index but its robustness is unitary rather than arbitrary noisy; a Lorentz gauge action can be explicitly invariant without producing Einstein gravity; 81 equal dimension does not imply equivariant quantum-topological equivalence.

## Five best independent next steps

1. Build an explicit **equivariant physical coupling** from Steinberg81 to photonic 81-mode operators or prove an obstruction for a specified coupling category, not a dimension match.
2. Optimize an **implementable QND Strange projector** with controlled parity decomposition into calibrated photonic/hybrid gates; derive exact success, false herald, and Wigner negativity resource costs.
3. Measure a **noisy Floquet edge channel invariant** operationally: entanglement fidelity and directed operator transport, versus gapped local perturbations and noise rates.
4. Derive a 120-tick **quantum statistical mechanics transfer/Hamiltonian** with a thermodynamic limit, and compare its symmetry content against the 40-direction 1D no-transition benchmark.
5. Replace the indefinite SO+(1,3) gauge toy with a **constrained 3+1 Palatini/tetrad Hamiltonian** and verify Gauss, diffeomorphism and scalar constraints on a refinement family, including anomalous closure tests.


## 7. Explicit coherent SU(3) disorder experiment on the compiled Floquet exchange loop

**Producer:** analysis/w33_20261031_floquet_coherent_dressing.py. **Frozen result:** data/w33_20261031_floquet_coherent_dressing.json. This is a stronger operational control than merely citing the index theorem.

For every site in open L=4 and L=6 square qutrit lattices (plus an L=6 periodic torus control), at each of four swap stages prepend an independently sampled local unitary V=exp(i epsilon H), H random 3x3 Hermitian. Follow not only every qutrit's physical source and destination but also the complete accumulated local 3x3 SU(3)-type unitary (global phase unrestricted). Check unitarity for every routed carrier and recover any transported input state by applying the calibrated inverse.

With epsilon=0.04, .2, .5, mean UNCALIBRATED |0> infidelities on L=4 are approximately 0.0154, 0.2308 and 0.6121; on L=6, 0.0134, 0.2507, 0.7096 (all from seeded numerical samples, not measurements). All CALIBRATED inverses reconstruct the transported input to ~machine precision. The open boundary still has one shift orbit of length 2L-1, the bulk site permutation is unchanged, and the periodic torus still has identity site permutation. This verifies the locality-preserving QCA index is robust against the class of onsite coherent dressing, while also showing that basis-sensitive fidelity deteriorates without calibration. Entangling cross-talk, losses and completely positive nonunitary channels remain outside the scope.
