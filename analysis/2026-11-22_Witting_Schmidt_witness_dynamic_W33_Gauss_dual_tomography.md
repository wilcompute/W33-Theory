# Finite geometry as an operational quantum witness: Witting Schmidt dimension and dynamic W33 gauge loop

**Research date: 22 November 2026.** Three executable analyses were added to master:
- analysis/toe_20261122_2design_entanglement_capacity.py
- analysis/toe_20261122_witting_dual_frame_tomography.py
- analysis/toe_20261122_dynamic_W33_gauss_ring.py

They are exercised by 18 focused tests in tests/test_toe_20261122_schmidt_dynamic.py and the independent workflow .github/workflows/witting-schmidt-dynamic-gauge.yml. Each producer writes its own reproducible JSON certificate under data/.

## Starting from experimental evidence, not numerology

The literature scan was motivated by recent (2+1)D gauge-dynamics experiments: Stelea et al., *Nonperturbative string dynamics in a (2+1)D lattice gauge theory on a superconducting quantum processor* (arXiv:2611.14484, submitted November 10, 2026), https://arxiv.org/abs/2611.14484, and high-dimensional entanglement witnesses in arbitrary measurement bases, https://www.nature.com/articles/s41534-025-00990-6. Neither experiment confirms W33 or the finite Witting geometry.

Repository searches found earlier Witting complex-projective-2-design and tight-frame results, ququart tomography and coherent channel capacity; the 2-design itself is **not new here**. The new work creates directly measurable single-setting Schmidt-number witness formulas, rigorous compressed-outcome negative controls, and a Gauss-constrained exact dynamic benchmark on the previously verified W33 square cycle.

## Result A: Exact Schmidt-number witness from matched 40-outcome measurements

For the 40 Witting ququart rank-one projectors P_i, their known 2-design property gives

sum_i P_i = 10 I4,
sum_i P_i tensor P_i = 2 (I16 + SWAP).

After partially transposing the second system,

sum_i P_i tensor conjugate(P_i) = 2I16 + 8|Phi4><Phi4|,

with |Phi4>=(|00>+|11>+|22>+|33>)/2.

Prepare arbitrary two-ququart rho. Alice measures the complete joint 40-outcome POVM with E_i=P_i/10; Bob simultaneously measures the conjugated 40-outcome POVM F_i=conjugate(P_i)/10. The probability of **matching labels** is exactly

P_same = 0.02 + 0.08 F_Phi,
F_Phi = <Phi4|rho|Phi4>.

Since fidelity with the specified maximally entangled ququart is bounded by k/4 for states of Schmidt number <=k, matching probability strictly greater than .04, .06 or .08 certifies Schmidt number >=2, >=3 or >=4 respectively. Each bound is attained by an appropriate Schmidt-rank-k pure state, so these thresholds are sharp for the trusted witness.

For isotropic states rho(v)=v|Phi4><Phi4|+(1-v)I16/16, P_same=.025+.075v. Entanglement occurs for v>.2; the higher Schmidt thresholds are crossed at v>7/15 and v>11/15.

**Qualification:** This is a trusted and calibrated full-POVM entanglement witness. One fixed measurement setting cannot certify Bell nonlocality; these are not device-independent thresholds. Under separately assumed independent, state-independent per-photon efficiencies .8, a null-binomial-normal-approximation 5-sigma separation requires 423 ideal pairs at v=1, about 3008 pairs at v=.5 or about 108267 pairs at v=.25. These are illustrative, NOT rigorous confidence guarantees or experimentally demonstrated efficiency thresholds.

## Result B: Compression destroys the easy witness, not informational completeness

Pooling16 ray outcomes into one detector bin creates strong false positives for same-bin coincidences. Taking an explicit **separable** product state aligned to the pooled POVM operator's largest eigenvector gives:

| Layout | Same-bin coincidence on ideal Phi4 | Same-bin coincidence on explicit separable product state |
|---|---:|---:|
| Older 25-bin | 0.236667 | 0.358011 |
| Improved privacy/Fisher 25-bin | 0.255000 | 0.520210 |

Thus the full40 same-label threshold cannot be copied to the compressed detector. These are concrete **counterexamples**, not globally optimized separable bounds.

Nevertheless both compressed local POVMs have real Hermitian operator span **rank16**, the same as the full40 POVM: they remain informationally complete for a calibrated ququart. Define normalized ququart Pauli-product basis B_k, real analysis matrix A_ik=Tr(E_i B_k), target coefficients T_kl=Tr[Phi4(B_k tensor conjugate(B_l))], and minimum-Euclidean-norm coefficients C=pinv(A)^T T pinv(A). Then F_Phi=sum_ij C_ij p_ij exactly for the **entire** two-party outcome table, not just same labels.

For full40 the C_ij estimator is astonishingly simple and takes only **three values**: 19/4 for identical ray labels, -3/2 for distinct orthogonal rays, and 7/12 for distinct nonorthogonal rays. Its unbiased fidelity-score standard deviation on ideal Phi4 is **1.25 per shot**, versus 3.75 for the cruder matched-label-only fidelity estimator. That is a **ninefold variance reduction** for this target state.

With the same unbiased minimum-Euclidean-norm approach, the fidelity-score standard deviations on ideal Phi4 are 1.25 (full40), **7.7082** (older25), and **5.1284** (newer25). All three have local IC rank16; their local measurement analysis-frame condition numbers are respectively 2.2361, 20.8071 and 18.7548. The newer compressed detector is about (5.128/1.25)^2 ≈ **16.8 times** more expensive in sample count for this particular ideal-state estimator variance. A weighted state-dependent estimator might improve these figures, so they are **not** global minimum-variance bounds.

## Result C: The same Witting rays can define an entanglement-breaking channel

If one actually measures the 40-outcome POVM and reprepares the reported ray, the measure-and-reprepare channel is exactly

E(rho)=sum_i Tr[(P_i/10)rho] P_i = (rho+I4)/5.

This is the ququart depolarizing channel with shrinkage 1/5. Its normalized Choi singlet fraction is 1/4, exactly the isotropic separability threshold in dimension4. It is entanglement breaking by construction and has zero quantum capacity.

This separates the **coherent** Witting optical channel considered in earlier repo work from an **incoherent** Witting measure/reprepare instrument. The geometry alone guarantees neither a usable quantum channel nor quantum computational advantage: coherence and the laboratory instrument definition are decisive.

## Result D: A genuine eight-dimensional dynamical Z2 matter-link Gauss sector on a W33 square

Use the independently established W(3,3) graph four-cycle [0,36,9,37,0]. Place one matter excitation on one of the four vertices, four **quantum** Z2 links (one per edge), and one fixed odd background charge at vertex0. The unconstrained 4*2^4=64 dimensional state space reduces to exactly **8** physical states satisfying

G_v = (-1)^(n_v+b_v) product_(edges at v) X_e = +1 for each vertex.

The odd background charge is essential: without it, product_v G_v=-1 in the odd-matter sector, so the all-positive Gauss sector would be empty. This is a global parity obstruction, not a tuning convention.

The exact finite Hamiltonian in the physical sector is

H = -sum_edges (c†_u Z_e c_v + c†_v Z_e c_u) - h sum_e X_e - B product_e Z_e.

All terms preserve every Gauss constraint. Define the magnetic Wilson loop W=product_e Z_e. The matter hopping and plaquette magnetic term commute with W, but the electric term does not.

Starting with one matter quantum at vertex0 and a W=+1 or -1 flux eigenstate, the exact opposite-vertex arrival probabilities at h=0 are:

P_opposite(t | W=+1)=sin^4(t),
P_opposite(t | W=-1)=0.

Thus static negative Z2 flux enforces perfect Aharonov–Bohm cancellation at the opposite vertex for all t. With quantum electric-field strength h=.3, B=0 and t=1.5, the initially negative-flux state instead has opposite-vertex probability **0.596141772894** and final Wilson expectation **+0.545968094522**. This is an explicit finite example of Gauss-preserving quantum link dynamics changing a previously static interference selection rule.

**Important limitation:** A four-site loop is not a (2+1)D lattice, local continuum QFT or QCD. These matter/gauge Hamiltonians and Gauss constraints are standard tools; the W33-specific result is the selected graph cycle and exact gauge-invariant operational benchmark. The cited 2026 experiment is a motivation, not a measurement of this W33 model.

## Provenance, controls and reproducibility

The three independent standalone Python calculations in the conversation container passed exact 2-design, strict-Gauss and dual-frame reconstruction assertions. Three GitHub-native counterparts were committed to master and 18 dedicated regressions authored. The focused GitHub Actions workflow was created, but no pass is claimed until its job finishes. Existing prior Witting tight-frame work, fixed-geometry channel capacity and gauge research are acknowledged; the mathematical identities are not represented as new universal physics discoveries. No reset or force push was made to concurrent work.

**High-value orthogonal follow-ups** are: (1) design a 40-mode per-party physical Naimark interferometer and rigorously account for losses; (2) optimize dual-frame fidelity variance under measured confusion and privacy constraints; (3) extend the W33 gauge model to two neighboring plaquettes with explicit string tension and gauge-invariant charge production; (4) experimentally distinguish coherent Witting isometries from entanglement-breaking measure/reprepare implementations; and (5) compare W33 against random strongly-regular/finite-design controls to separate generic design identities from special geometry.

The point is to turn **specific geometry into explicit observables, engineering costs, no-go tests and independently checkable physical hypotheses**, not to claim a derived Theory of Everything.
