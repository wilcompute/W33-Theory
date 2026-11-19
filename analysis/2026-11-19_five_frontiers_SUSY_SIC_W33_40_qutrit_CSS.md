# Five TOE frontiers plus a new 40-qutrit W33 code: executable research audit

**Date:** 2026-11-19. **Status:** exact finite-field certificates, a classical N=1 SUSY gauge-model construction, explicit quantum-channel and lattice falsifiers. **Not** a TOE, SM vacuum, physical G2 compactification or hardware result.

## Provenance and collision audit

Continued from GitHub master 8dea889 (the parallel H27 torsion-gerbe A4/S4 four-clock theorem) after inspecting 8dea889, 84b0ad0 and fb96fb4, the 215-page Forty Points source (especially pp. 36-38), and the existing November 17/18 geometry and Dirac reports. **A concurrently landed local commit 867f70b also independently builds a stronger RENORMALIZABLE cubic anomaly-free SIC model** using ten fundamental/antifundamental pairs, a 45-meson-plus-one-baryon constraint, and a 98/106 Hessian rank. The present nine-pair construction is instead a lower-charged-field **nonrenormalizable effective model**, with a direct 19-baryon anchor chart; they are distinct models and neither is a realistic UV-complete sector. Concurrent work also contains the same SWAP causal-break memory witness, so our version is a reproducibility/noise-threshold check, not first discovery. Unrelated local dirty files are preserved.

**Important existing results we do not re-claim:** Pass4948 already derived the modular equation (A+I)^2=J over F3 and its 10,19,10 Loewy layers; Pass7733-7740 already proved that the classical [40,11,13]_3 and [40,10,18]_3 row spaces are independent of the 234 symplectic polarizations, and recorded the dual [40,29,6]_3. The preexisting W33 CSS [[240,81,...]]_3 uses *edges*, not the 40-point code below. The preceding 2026-11-18 report already proved the round S5 Dirac gap and emitted a sequential qutrit GHZ circuit. Forty Points already uses the *ninth-root* cubic qutrit gate. Our new work is explicitly an extension of these facts.

## Front 1. Classical anomaly-free supersymmetric SU3 Hesse-SIC model

We now provide a **holomorphic SU(3) gauge-invariant superpotential** rather than a nonholomorphic bosonic SIC-aligning potential.

Take nine fundamental chiral triplets Q_0,...,Q_8 and nine antifundamentals \\widetilde Q_0,...,\\widetilde Q_8. The cubic SU3 gauge anomaly coefficient is 9-9=0. Add 19 singlets S and 27 singlets T.

Set omega=exp(2pi i/3). Arrange nine triplet columns Q^0 in three groups:
- (0,1,-omega^k) for k=0,1,2;
- (-omega^k,0,1) for k=0,1,2;
- (1,-omega^k,0) for k=0,1,2.

Then Q^0 (Q^0)^dagger=6 I_3, each norm squared is 2, and all 36 distinct pairwise overlap magnitudes squared are 1. Thus the columns are an unnormalized Hesse SIC and their SU3 moment map is zero.

Pick independent anchor columns A=(0,3,7) (their determinant has squared magnitude 3). Let B_*=det(Q_0,Q_3,Q_7) and, for each six unanchored flavor k and a in {0,1,2}, let B_ka be the determinant formed by replacing anchor position a with Q_k. Let b_* and b_ka be these 19 numerical constants evaluated on Q^0.

The explicit holomorphic gauge-invariant EFT superpotential is

    W = [ S_* (B_* - b_*) + sum_{k,a} S_ka (B_ka - b_ka) ] / Lambda
        + sum_{i=0}^8 sum_{a in A} T_ia (Qtilde_i dot Q_a).

**Global classical F-flatness theorem.** F_S=0 forces all 19 baryonic minors to their prescribed values. The nonzero anchor minor defines G=Q_A (Q^0_A)^(-1), with det(G)=1. Cramer's rule using the 18 replacement minors fixes every other column, hence Q=GQ^0 for some G in SL(3,C). Since the three anchor columns span C^3, F_T=0 forces all nine antifundamentals Qtilde_i=0. Their own F_Qtilde equations then force all 27 T_ia=0. The analytic 19-by-27 baryonic Jacobian has full row rank 19 (machine checked, minimum singular value about 0.635), hence F_Q=0 forces all 19 S fields to zero. There are no additional classical F-flat branches.

**D-flatness theorem.** With Qtilde=0, the SU3 moment map vanishes iff GG^dagger is scalar. Since det G=1 and GG^dagger positive, GG^dagger=I, so G lies in SU(3). Therefore there is exactly **one classical supersymmetric vacuum modulo SU3 gauge transformations**, represented by the Hesse SIC.

**Mass-gap audit:** The full constraint Jacobian has rank 19+27=46 on 54 charged complex field components; the 100-by-100 superpotential Hessian has rank 92 and 8 null vectors, exactly the complexified SU3 gauge tangent dimension. Thus there are no ungauged classical chiral flat moduli at this point (a physical mass spectrum still requires Kähler normalization). Compared with parallel 867f70b, this uses nine rather than ten flavor pairs, but its baryon-singlet terms require an EFT suppression scale.

**Critical limitations:** all 19 complex baryon target values are tuned inputs, not dynamically selected; W contains higher-dimension operators suppressed by Lambda; gauge/matter quantum dynamics and UV completion are not established; 9+9 triplets are not the Standard Model spectrum; a chiral E8 embedding or phenomenological Yukawa derivation is not provided. This is a constructive *classical* proof, not an observed selection principle.

Certificate: analysis/toe_20261119_five_frontier_bridge.py and its regression tests.

## Front 2. Spin, G2 and flat-gauge chirality obstruction

The existing free quotient Y7=(S5(R) x T2)/H27 has fundamental group whose abelianization is Z^2; hence H^1(Y7,Z2)=(Z2)^2, giving **four spin structures** once the spin lift is fixed. The natural quotient metric has scalar curvature 20/R^2. Its Dirac operator satisfies the Lichnerowicz bound D^2>=5/R^2. A stronger *preexisting* round-product spectral argument gives |lambda|>=5/(2R) for all four spin structures and any unitary flat-twisted operator.

In particular, torsion H^3(Y7,Z)=(Z3)^2 and flat gerbe choices are **not** automatic massless charged fermion zero modes. The quotient has positive scalar curvature but two flat Ricci directions, consistent with the parallel topological obstruction to *positive Ricci* from infinite pi1. A nonflat gauge curvature, torsionful/supercovariant Dirac, singular ADE localization or different internal geometry remains open.

This front confirms and refines the spin-structure inventory of the prior Dirac work; the Dirac gap itself is not new.

## Front 3. Operational three-time quantum memory with a causal break

Let reference R and system S start in |Phi_3>=(|00>+|11>+|22>)/sqrt3 and let environment E start in |0>. SWAP(S,E) transfers entanglement from R-S into R-E; S becomes |0>. Perform a **causal break** by discarding S and preparing |0>, and then apply SWAP(S,E) again. An exact 3x3x3 tensor simulation restores |Phi_3> to R-S.

If the stored E is depolarized with probability p, the returned state is

    rho_RS=(1-p)|Phi_3><Phi_3|+p I9/9.

The partial-transpose negativity is **N=max(0,1-4p/3)**, surviving exactly for p<3/4. An environment restricted to classical entanglement-breaking information cannot restore entanglement with an isolated reference after the system causal break. This is an explicit entanglement-assisted *quantum memory* witness, not full process-tensor tomography or experimental proof.

## Front 4. Finite-graph versus Lorentzian continuum falsifier

For a 3D centered finite-difference scalar wave with isotropic grid scale a and Courant ratio r=c dt/a <=1/sqrt3,

    sin^2(omega dt/2)=r^2 sum_i sin^2(k_i a/2),
    omega^2=c^2|k|^2+(c^2 a^2/12)[r^2 |k|^4-sum_i k_i^4]+O(a^4).

The low-k dispersion approaches the Lorentzian wave equation, but the finite grid remains anisotropic at O(a^2): at r=1/sqrt3, a=0.2 and |k|=1, the body-diagonal mode is exactly omega=1 and the axial mode is smaller. This is a **toy continuum falsifier**, not Einstein dynamics.

More directly, W33 point adjacency has exact spectrum 12 (once), 2 (24-fold), -4 (15-fold). Its graph Laplacian eigenvalues are 0, 10, 16. A fixed 40-vertex W33 graph therefore has no sequence of arbitrarily low nonzero wavelengths; a physical continuum needs a justified refinement or thermodynamic limit and dynamical local constraints.

## Front 5. Exceptional/photonic qutrit universality gate audit

The projective one-qutrit Clifford group has order 9*SL(2,3)=216; the projective two-qutrit Clifford group has order 81*Sp(4,3)=4,199,040. Clifford-only H27/qutrit circuits do **not** establish universal quantum computation.

One easy characteristic-three trap is that j^3=j *modulo 3*, so diag(omega^(j^3)) is just Pauli Z. **But** the actual gate already in Forty Points (p.37) is diag(zeta9^(j^3))=diag(1,zeta9,zeta9^8), where zeta9=exp(2pi i/9). This is genuinely non-Clifford. Our test verifies that its conjugation of X cannot be proportional to any qutrit Pauli. The ninth-root distinction is already made in the paper and is **not** a new physics claim. A physical logical non-Clifford gate, magic injection and threshold are still required.

## Additional front 6. An asymmetric W33-to-Leech 40-qutrit CSS bridge

Let A be the **40-point** W33 collinearity adjacency, and J the 40-by-40 all-ones matrix. The strongly regular identity gives over the integers

    (A+I)^2=9I+4J,

so over F3, with H_X=A+I and H_Z=A+I-J,

    H_X H_Z^T = (A+I)[(A+I)-J] = J - J = 0.

Exact F3 Gaussian elimination yields rank(H_X)=11 and rank(H_Z)=10. Consequently the associated stabilizer code has n=40 and k=40-11-10=19 logical **qutrits**.

**Exact distance certificate:**
1. Enumerate every projective X and Z Pauli error of support weights 1,2,3. Each has a nonzero syndrome: d_X and d_Z are at least 4.
2. Four points [0,1,2,3], forming one W33 line in the fixed projective ordering, support an X operator with H_Z x=0. Its vector is outside row(H_X), shown by a rank jump from 11 to 12. Therefore d_X=4.
3. A meet-in-middle exhaustive normalized-syndrome collision search over all weights 1-2 versus 1-3 proves ker(H_X) has **no** weight-4 or weight-5 vector. The explicit Z vector with coefficient 1 at [0,1,2] and 2 at [4,9,11] lies in ker(H_X) but not row(H_Z) (rank jump 10 to 11). Therefore d_Z=6.

We obtain the **asymmetric CSS stabilizer code**

    [[40,19,4]]_3   with   (d_X,d_Z)=(4,6).

The prior Pass7733-7740 result gives row(H_X)=C11 and row(H_Z)=C10 *independently of which of 234 symplectic polarities is selected*. Accordingly, this CSS check **space** is also polarization independent. This pairing and its explicit quantum-distance certification extend the existing classical W33/Leech code weld; we do not claim discovery of the prior classical codes or priority over all literature.

This 40-qutrit code is **not** the 240-edge [[240,81,...]]_3 code, and does not automatically yield a decoder, quantum memory hardware or physical spacetime.

## Reproduce

    python analysis/toe_20261119_five_frontier_bridge.py
    python analysis/toe_20261119_w33_40_qutrit_css.py
    python -m unittest discover -s tests -p test_toe_20261119_five_frontier_bridge.py -v
    python -m unittest discover -s tests -p test_toe_20261119_w33_40_qutrit_css.py -v

JSON records: data/toe_20261119_five_frontier_bridge.json and data/toe_20261119_w33_40_qutrit_css.json.

Reference notes: SQCD D-flat quotient and invariant coordinates: https://doi.org/10.1007/978-3-032-09219-9_18 ; Lichnerowicz and flat twist: https://math.uchicago.edu/~amathew/dirac.pdf ; process tensors/causal breaks: https://journals.aps.org/prxquantum/abstract/10.1103/92c4-g7qs ; qutrit Clifford+T: https://www.mathstat.dal.ca/~neilr/Papers/Rgate.pdf . These are external background, not claims that prior papers contain our particular toy model or quantum code.

## Five independent next falsifiers

1. **UV and quantum stability:** quantize the anomaly-free SIC EFT and check its beta functions, mass spectrum, singlet threshold corrections and E8-representation compatibility. Resolve whether the tuned b_I constants can arise dynamically.
2. **Geometric chiral fermions:** replace flat H27 backgrounds by a specified nonflat gauge connection or singular ADE locus; compute a genuine charged Dirac index/kernel and anomaly-inflow contribution.
3. **Experimental time-memory witness:** construct a physically implementable qutrit SWAP/photonic-delay causal-break experiment and optimize the partial-transpose witness under photon loss, heralding and finite samples.
4. **Emergent gravity:** build a refinement family of W33 graphs with an explicit local Lorentzian action, then compute the Hamiltonian/diffeomorphism constraint brackets; reject models whose continuum limit fails closure.
5. **Quantum code hardware:** design a decoder and measurement schedule for the [[40,19,4]]_3, benchmark finite-shot logical error rates, and test fault-tolerant injected T9 gates without confusing the code with the 240-edge construction.
