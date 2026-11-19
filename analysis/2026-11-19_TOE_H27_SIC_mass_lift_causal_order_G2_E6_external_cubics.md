# TOE continuation: H27 SIC mass repair, causal-order gauge, and a genuine G2/E6 cubic bridge

**2026-11-19 | Baseline: master c98ed7e233cac609cd2e99ed0860e633e5a8ae02.**

This is an independent **mathematical/finite-model falsification audit**, not a validated physical Theory of Everything, a G2 compactification, a 4D quantum gravity model, or a demonstrated photonic processor. Latest published master was unchanged at intake; the user's numerous unrelated local files were not modified or staged.

## 1. Causal-order representation obstruction

Existing repo work showed that a forward-triangular Dirac-like matrix D=mI-alpha A has gauge-sensitive inverse spectral response but a blind determinant. A subtler objection is that A need not be uniquely determined by the partial order if it is an arbitrary forward adjacency.

Exact exhaustive enumerations for **n=4**: 64 forward graphs, 40 distinct transitive closures, 14 causal orders having multiple graph presentations. For **n=5**: 1024 forward graphs, 357 distinct closures, **199 orders have multiple presentations**. Some presentations of the same causal order have inverse-response difference **3.093345460844697** at m=1.3, alpha=.6.

The 5-point total order has a unique four-link Hasse cover relation but ten transitive causal relations. Response Tr[(D†D)^-1] is **3.5559714510510645** on the four covers and **6.649316911895761** on all ten. The order is identical. Extracting transitive reduction (Hasse covers) from every presentation gives exactly equal response for all 357 orders. This is a *candidate canonical adjacency convention*, not an independently derived causal action or a suppression theorem for nonmanifoldlike causal sets. Literature: https://doi.org/10.1007/s41114-019-0023-1 and https://www.osti.gov/biblio/2419376.

## 2. H27-invariant mass lifting while preserving SIC AND MUB rays

Prior repo baseline: W0=sum_j(x_j^3-x_j^6/2) has 9 projective support-two F-flat SIC rays with one quadratic zero mode, and 9 projective support-three MUB rays, all gapped.

Construct instead

    W_lambda = W0 + lambda*x*y*z*(x^3+y^3+z^3-2).

This full polynomial is exactly invariant under the H27 qutrit cyclic shift and diagonal clock (checked polynomially modulo omega²+omega+1). At any original support-two stationary point, two coordinates have cube 1 and the third vanishes. The added term has zero value AND zero first derivatives. Thus all **27 support-two F-flat vectors, giving 9 SIC projective rays**, remain F-flat exactly for every lambda.

At (1,1,0) the exact holomorphic Hessian is

    H=[[-9,0,3lambda],[0,-9,3lambda],[3lambda,3lambda,0]]
    det(H)=162lambda².

For every nonzero real lambda, the former quadratic zero mode is lifted. Eigenvalues are -9, (-9 +/- sqrt(81+72lambda²))/2. At small lambda the light chiral mass is approximately 2lambda² and (canonical-Kähler/global-SUSY) scalar mass-squared approximately 4lambda^4: a double suppression from mixing, not an imposed soft mass. At lambda=0.25, every one of 27 SIC representatives remains F-flat within 1e-12, minimum Hessian singular value **0.12331050222673205**, SIC Gram residual below 1e-12.

The support-three **MUB projective geometry also survives exactly**, with complex radial rescalings. For u_ab=(1,omega^a,omega^b) and xi=omega^(a+b), define

    r³=(3-2lambda*xi)/(3-6lambda*xi).

Then v=r u_ab is F-flat when r is finite/nonzero. At lambda=0.25, all 9 projective rays retain three MUB bases; maximum F-residual 9e-15. Each of the 9 rays yields 3 related F-flat vectors from the cube roots. These support-three vacua are no longer at the original amplitude; in particular F_x(1,1,1)=4lambda. Additional stationary branches not exhaustively classified.

Nine **independently postulated** triplets chosen from the three rescaled MUB bases have a sum of outer products proportional to the identity, because amplitudes are constant within each orthogonal MUB basis. This supplies a conditional traceless moment-map template, NOT an SU3-gauged F-flat theory: the superpotential has finite H27 symmetry only; no full SU3 or E8-invariant superpotential or dynamical gauge completion follows. Other blockers: Kähler metric, mass units, family overlaps, vacuum choice, SUSY breaking, realistic Yukawas and anomaly/flux constraints.

The previous undeformed straight-line BPS domain-wall tension T=1 CANNOT be carried over without proving a new coupled BPS solution. The deformation also shifts superpotential critical values at support-three vacua.

## 3. Standard Model / Spin(10) anomaly gate

An exact rational left-handed Weyl census for one standard family Q,u^c,d^c,L,e^c,nu^c checks 5 local anomaly sums (gravity²U1, U1³, SU3²U1, SU2²U1, SU3³) and the SU2 Witten doublet parity. All vanish and there are 4 doublets counted with color multiplicity, hence no Witten obstruction.

Removing the neutral sterile nu^c still leaves all anomalies zero; omitting charged e^c does not. Gauge anomaly cancellation alone does NOT predict the sterile neutrino, exactly 3 families, an SO10 16 spectrum or absence of mirrors. This is known Standard Model consistency reproduced independently, not an original physics prediction.

## 4. CP-odd SU3 Wilson holonomy interferometry

For a fixed SU3 holonomy W and a controllable coherent reference arm,

    B_phi=W+exp(i phi)I_3
    I(phi)=Tr(B_phi B_phi†)=6+2Re(exp(-i phi)Tr W).

Phases 0 and pi/2 reconstruct respectively the real and imaginary parts of Tr W. For eigenphases (.6,1.5,-2.1), Tr W=0.3912267119775237+0.6989280933502161i, reconstruction residual 3.33e-16. W and W† give identical zero-phase singular-value spectra but opposite imaginary-trace readout; pi/2 intensity difference is 4 Im Tr W.

The full *complex* fundamental trace determines a single classical SU3 conjugacy class via its characteristic polynomial z³-tz²+conj(t)z-1; it is not full reconstruction of a gauge field. Characters of 6 and 8 satisfy chi_6=t²-conj(t), chi_8=|t|²-1. Local gauge-frame invariance checked across 24 random SU3 frames. This is established interferometric/group-theory prior art; no optical implementation, kinetic dynamics, or actual E8 matter coupling has been derived. References: https://www.nature.com/articles/s41467-019-10974-8 and https://onlinelibrary.wiley.com/doi/10.1002/prop.70156.

## 5. Operational qutrit conditional entanglement is NOT full genuine quantum memory

For rho_v=v|GHZ3><GHZ3|+(1-v)rho_dephased, measure the earliest emitted qutrit in the Fourier-plus basis and condition on the outcome. The subsequent two-qutrit density matrix has entanglement negativity exactly N=v, even though every unconditioned pairwise output marginal is independent of v.

For global white noise rho_v=v|GHZ3><GHZ3|+(1-v)I_27/27, the conditional state is isotropic and N=max(0,(4v-1)/3). Thus conditional entanglement is witnessed at visibility **v>1/4**. Multiple parameter values numerically match exact partial-transpose eigenvalue formulas.

This is a usable **localizable-entanglement witness**, NOT proof of genuine three-time quantum memory. It lacks intervention slots/process-tensor causality and classical-memory exclusion. See https://arxiv.org/abs/2611.17268 and https://journals.aps.org/prxquantum/abstract/10.1103/92c4-g7qs.

## 6. EXTERNAL rigorous G2-to-E6 bridge and independent small calculations

A major external advance is Sergey Grigorian, **Exceptional cubics on 7-manifolds**, arXiv:2611.21589, posted 2026-11-16:
https://arxiv.org/html/2611.21589

For traceless symmetric 7x7 tensors h, the two G2-invariant cubics

    C0=Tr(h³)
    Cphi=phi_abc phi_def h^ad h^be h^cf

give N_lambda=C0+lambda Cphi. **The paper proves** E6 stabilizer dimension78 and equivalence to the Albert cubic norm precisely at lambda=(1 +/- i sqrt7)/8; generic symmetry G2 dimension14, and the pure trace case SO7 dimension21. It supplies explicit E6 reductions of the complexified rank27 bundle and a fiber-level geometric bridge to the minuscule E6 27. The claim is the author's theorem, NOT a repository discovery.

Our independent calculation: construct the 7 signed Fano triples of the G2 3-form, i.e. 42 nonzero oriented tensor entries. For 32 real unit-vector line basepoints u and h=7uuᵀ-I, find C0=210 within 2e-13 and Cphi=84 within 5e-14. Hence N_lambda(h)=210+84lambda=42(5+2lambda), matching the author's exact basepoint normalization. SymPy independently verifies the critical quadratic 8lambda²-2lambda+1=0 and its complex roots. This does NOT verify the full Lie stabilizer or global differential geometry.

Another recent EXTERNAL paper is Daniel Corey, **The E6-Grassmannian, its minuscule Coxeter matroids, and the lines on a cubic surface**, arXiv:2611.19606, posted 2026-11-14 (updated Nov 17):
https://arxiv.org/abs/2611.19606

It proves a classification of **1,335,373** E6 minuscule Coxeter matroids into **230** Weyl orbits and a tritangent-exchange characterization. We did not independently enumerate those matroids.

To cross-check classical E6 geometry independently, build the 27 cubic-surface lines (6 E_i, 6 Q_i, 15 L_ij) and 45 tritangent triples (30 E_i-L_ij-Q_j plus 15 perfect matchings). Every line belongs to 5 tritangents and meets 10 others, with 135 unique intersecting pairs. The line-intersection graph is exactly strongly regular (27,10,1,5), with spectrum **10¹, 1²⁰, (-5)⁶**, as numerically and combinatorially verified.

**Parameter warning:** the G2/E6 complex critical lambda values have NO established physical or algebraic identification with the H27 mass-lifting lambda=.25. Both occur in separate polynomial families on different representation spaces. Similar notation is not a derived unification.

## Independent reproduction

    python analysis/toe_20261119_five_orthogonal_vacuum_causal_memory_SU3_anomaly.py
    python analysis/toe_20261119_G2_E6_Fano27_45_tritangent_crosscheck.py
    python -m unittest discover -s tests -p test_toe_20261119_H27_masslift_causal_order_G2_E6_bridge.py -v
    python -m unittest discover -s tests -p "test_toe_20261119_*.py" -q

Certificates:

- data/toe_20261119_five_orthogonal_causal_H27_qutrit_SU3_anomaly.json
- data/toe_20261119_G2_E6_Fano_cubic27_45_tritangents_crosscheck.json

## Five independent best follow-up tests

1. Build an E8-legal H27 mass-lifting UV completion, including genuine E6xSU3 invariant messenger operators, full F/D flatness, anomaly closure, physical Kähler normalizations, and *selection* of the nine SIC vacuum.
2. Derive causal propagation from a poset-intrinsic operator or physical edge degrees of freedom, with chiral unitary matter, continuum Lorentz behavior and nonmanifold-history entropy suppression.
3. Use Grigorian's exact G2-to-E6 cubic map to construct a CHARGED 7D Dirac zero-mode map and a compactification with real physical 4D chiral spectrum. Gauge fibers alone are not gauge bosons.
4. Build qutrit multi-time process-tensor tomography and a semidefinite classical-memory exclusion witness with intervention-controlled causal constraints, not only heralded GHZ entanglement.
5. Realize a physically calibrated two-phase SU3 Wilson interferometer, study phase/reference errors and multiple noncommuting loops, and connect observable characters to dynamically derived E6/SU3 matter.
