# TOE54 — Physics-first test of W33 Lorentz emergence

**13 October 2026 — W33-Theory only.** Holotrade, frame carriers, K81 compiler architecture and cross-repo matching are OUT OF SCOPE.

## The fundamental question

A Theory of Everything must explain the continuum spacetime metric, Lorentz invariance, Einstein dynamics, the anomaly-free Standard Model, measured particles and constants, and out-of-sample predictions. Mathematical graph identities are not substitutes for a physical action.

Pass11956 previously established a *leading-order* two-polarization acoustic cone for the native TOE38 W33 160-edge Maxwell 2-complex. It selected positive electric link weights to obtain Gauss-reduced G=I/2. In these **dimensionless** lattice conventions, the two low bands behave asymptotically as omega² ~ 2|k|².

This paper tests what happens at FINITE momentum and what the finite lattice can or cannot prove about exact Lorentz symmetry.

## Rigorous no-go at fixed lattice spacing

For a finite cell with finitely many finite-range plaquette loops, Bloch magnetic P(k) consists of finite sums of phases exp(i k·n) with integer winding n. With fixed strictly positive W=diag(w_e), the operator H(k)=W^-1/2 P(k)^dag P(k) W^-1/2 is real analytic and uniformly bounded over all real k. Indeed every row corresponding to a walk of L steps has Euclidean norm at most L, so the spectral norm obeys:

    ||H(k)|| <= [sum_{plaquette loops} L^2]/min_e w_e < infinity.

**Theorem (standard lattice-dispersion obstruction, applied to this W33 model):** For any constant c>0 there is no nonempty open set U in real three-momentum space such that c²|k|² is an eigenvalue of H(k) for every k in U.

**Proof:** D(k)=det(H(k)−c²|k|² I) is real analytic. If it vanishes on U, analytic continuation on connected R³ implies it vanishes everywhere. For sufficiently large |k|, c²|k|² exceeds the uniform upper bound on H(k), so D(k) cannot vanish: contradiction.

This applies to the possibility of ANY exact quadratic eigenvalue branch on an open neighborhood, independently of degeneracy or branch labeling. It is NOT a no-go on emergent infrared Lorentz symmetry, a continuum scaling limit, an alternative nonlocal model or a different interacting theory. It is generic lattice mathematics, not a new universal physics theorem.

## Actual W33 finite-Bloch experiment

Producer: analysis/w33_20261013_toe54_lorentz_dispersion.py
Certificate: data/w33_20261013_toe54_finite_lorentz_dispersion.json
Regression: tests/test_w33_20261013_toe54_physics_lorentz_no_go.py

Reconstruct the actual TOE38 plaquette+commutator operator with its selected W33 deck marking and 160 positive Pass11956 kinetic weights. At six wavevector directions x, y, z, (1,1,0), (1,1,1), (2,-1,3) and four radii .02, .04, .08, .16, diagonalize the Hermitian 160x160 matrix H(k). The gauge zero modes are excluded and the two smallest strictly positive eigenvalues retained. The third positive mode remains gapped at omega² about91.57, and the exact local gauge closure P(k)B(k)=0 is numerically verified.

Define v_mean²(k)=(omega_1²+omega_2²)/(2|k|²). At radius |k|=.16:

| Direction | v_mean² | relative shift versus 2 | relative two-polarization split |
|---|---:|---:|---:|
| x | 1.9935582 | -0.32209% | 0.033834% |
| y | 1.9934661 | -0.32669% | 0.011544% |
| z | 1.9934436 | -0.32782% | 0.066726% |
| xy | 1.9958612 | -0.20694% | 0.029308% |
| xyz | 1.9963000 | -0.18500% | 0.051027% |
| (2,-1,3) | 1.9954771 | -0.22614% | 0.074060% |

At radius=.02, v_mean² lies within 1.1e-4 of 2 in all six directions, consistent with the previously established leading acoustic cone. The simple finite-difference coefficient [v_mean²(.04)−v_mean²(.02)]/(.04²−.02²), a proxy for the order-|k|^4 term in omega², is:

    x -0.252156, y -0.255772, z -0.256666,
    xy -0.161899, xyz -0.144740, skew -0.176975.

The direction dependence shows leading isotropic matching does not automatically eliminate the next derivative operators. The small nonzero polarization splitting at finite k shows the two low branches are degenerate only asymptotically in this model.

These are finite-k NUMERICAL data, not measured physical speed-of-light violations, nor a proof that a different choice of 160 positive weights could not tune particular quartic operators.

The physical conversion from dimensionless k to a measured momentum would require an independently derived lattice length a and energy/time normalization. There is NO justified numerical bound on any fundamental length scale from these toy percentages. The photon modes have not been demonstrated to couple to physically chiral Standard Model matter.

## Where this puts the W33 TOE program

The project now has an explicitly falsifiable obstruction: the existing fixed, finite 160-link Maxwell lattice is NOT an exact relativistic continuum theory. Its leading cone was constructed by choosing electric link weights, not dynamically predicted.

A viable physical completion must separately demonstrate:

1. **Lorentz restoration by continuum scaling.** Construct a family of W33-derived local models with length scale a→0, dynamics selecting electric/magnetic parameters, and a two-polarization dispersion converging on bounded physical momentum domains to a common speed with observationally viable birefringence and higher-order terms.
2. **One gauge + chiral matter action.** Supply a unitary interacting quantum action with genuine SU(3)xSU(2)xU(1) matter, exact anomalies cancellation, Ward identities, chirality, masses, and renormalization—not merely representations that share group orders.
3. **Einstein gravity as dynamics.** Introduce local canonical metric/matter variables, first-class Hamiltonian and diffeomorphism constraints, their closed algebra, positive physical energy and the correct two graviton helicities in a controlled limit. TOE51 Maxwell+160 scalars is not yet gravity.
4. **Constants and flavor predicted rather than fitted.** Derive moduli/vacuum, gauge couplings, alpha, Yukawas, strong CP, CKM and PMNS from the SAME action, with fewer free inputs than constraints; distinguish true predictions from numerology and previously fitted data.
5. **Independent physical prediction.** State at least one experimentally accessible out-of-sample quantity in measured units with uncertainty propagation. A graph spectral ratio matching a real constant is insufficient without a controlled mapping and appropriate quantum field theory.

**Scientific prior art:** Lattice band saturation, exact-vs-emergent relativistic dispersion, and EFT Lorentz-violation bounds are established. Review: Jacobson, Liberati, Mattingly (2005/06), arxiv:astro-ph/0505267, and Liberati/Maccione (2009), DOI 10.1146/annurev.nucl.010909.083640. No novelty is claimed for the generic analytic theorem; this pass implements and numerically tests it on the actual fixed W33 Maxwell model.

## Reproduce

    py -3 -m pytest -q tests/test_w33_20261013_toe54_physics_lorentz_no_go.py tests/test_w33_20261013_toe50_spectral_and_dual_decoder.py

Only stage the 4 explicitly named TOE54 source, JSON, report and test files. All existing collaborative working-tree changes must be preserved. No Holotrade files were accessed or modified.
