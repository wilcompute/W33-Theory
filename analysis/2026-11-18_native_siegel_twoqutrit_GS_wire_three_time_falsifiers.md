# Native W33 dual-parabolic two-qutrit gates, E6 boundary/GS constraints, winding multiplicities, and genuine multitime memory

**Research date: November 18, 2026.** Verified computational and mathematical tests. **Not** a theory of everything, a complete G2 compactification, a physical 4D chiral Dirac index, a proof of universal M-theory winding instability, or a demonstrated quantum-optical device.

## Inputs and novelty controls

The starting revision was a74c57e5f61701e2166e4b3a6984858ee8c2a010. All the relevant recent commits on master were checked, including the native W33 Sp4(3) point and line unipotent radicals and the E6 16_-3 quartic bilinear. Historical repository materials were read directly:
- analysis/2026-09-22_address_operator_h27_intertwiner_obstruction.md already PROVES that the 27-dimensional regular H27 carrier is not isomorphic to the 27-dimensional E6 trinification/operator carrier under the same group action. The former has center eigenspace dimensions (9,9,9); the latter has (0,27,0). Maximum H27-equivariant linear map rank is9.
- analysis/2026-10-14_toe79_canonical_opposite_octagon_torsor.md already gives the canonical W33 27-noncollinear-point H27 torsor and its native 27-octagon/cubic-line bridge.
- analysis/PASS11043_COMMUTANT_DRESSING_REGULAR_H27.md already supplies a nine-dimensional multiplicity/commutant dressing to convert a 27D carrier into a regular H27 action.
- analysis/PASS11869_11873_SIEGEL_LEVEL3_TWO_QUTRITS.md and analysis/2026-10-10_toe38_parallel_siegel_maxwell_module_breakthroughs.md already identify the Sp4(3) genus-two theta and two-qutrit Clifford relationship.

**Therefore no general novelty is claimed for the 27-point regular H27 action, the center obstruction, or the Siegel/Clifford relationship.** This packet contributes a direct exhaustive identification between the *specific native W33 line-parabolic radical* from commit a74c57e5 and the full 27 symmetric quadratic Clifford gates, including exact point-line radical intersection sizes; and independently derives operator-domain/anomaly/physics constraints and reproduces a recent multitime witness with a new visibility-budget formula.

## Front A — a concrete native W33 symplectic two-qutrit gate family

Constructed the native 40 points of W(3,3) as projective lines in F3^4 with symplectic form u0 v1-u1 v0+u2 v3-u3 v2. Generated PSp4(3) from all 40 symplectic transvections (order 25920), and used its point and line stabilizers with their exact Sylow-3 normal cores.

For a fixed point p, 40 points split into p (1), its12 collinear neighbors, and27 noncollinear points. The point-parabolic normal H27 acts with orbit pattern

    [1,3,3,3,3,27],

and acts freely/transitively on the 27 far points. Its center cycles the27 in nine disjoint 3-cycles. This checks the old 40=13+27 address construction, already present in the repo, not a new underlying geometry theorem.

For the canonical totally isotropic plane L=span((1,0,0,0),(0,0,1,0)), we independently construct **all** matrices

    g_B(q1,p1,q2,p2)
       =(q1+a p1+b p2, p1, q2+b p1+c p2, p2)
    B=[[a,b],[b,c]], (a,b,c) in F3^3.

They are 27 distinct symplectic transformations of the native projective points and preserve L. Their induced permutations of all 40 lines are *EXACTLY* the 27 elements of the previously computed line stabilizer's largest normal 3-subgroup. This is a conjugacy-free equality on actual native W33 labels, not only an abstract group-order match. All 729 products obey g_B g_C=g_(B+C).

The canonical two-qutrit diagonal phase representation is

    U_B|x,y> = omega^[2(a x²+2 b x y+c y²)] |x,y>
    omega=exp(2*pi*i/3), x,y in F3.

All27 different matrices are represented. The generators B=diag(1,0),diag(0,1) implement *local quadratic phases* on each qutrit; the off-diagonal B12=1 gives omega^(x y), exactly an **entangling controlled-Z** on two qutrits. The previously named W33 Siegel radical is thus concretely compiled to two local phase gates and one CZ, checked on the same group elements and multiplication table.

The two O3 radicals are *different* subgroups inside PSp4(3). Their intersection, on native point permutations, has order **9 when the point lies on the chosen isotropic line**, and **1 for the tested nonincident point**. The two radicals have distinct abstract types: point H27 is non-Abelian (center and commutator order3), line radical is Abelian C3^3. An arbitrary comparison of order27 subgroups must not identify them.

The E6 regular/operator center mismatch is retained explicitly: W33 regular center eigenspaces are 9,9,9, whereas the already-established E6 trinification 27 carries scalar center omega, multiplicities 0,27,0. Thus an invertible H27-equivariant 27x27 intertwiner is impossible; maximum rank9. A genuine physical compiler must use the pre-existing commutant dressing, a different symmetry action, or non-equivariant selection. This packet **does not** construct the missing E6 physical coupling, a new 27D unitary intertwiner, or quantum optics hardware.

References: native W33 repo earlier passes cited above; Sp4 Siegel unipotent as symmetric matrices, https://www.sciencedirect.com/science/article/abs/pii/S0022404925001999; Steinberg/Siegel-Weil finite representation material, https://arxiv.org/abs/2401.16933.

## Front B — genuine boundary-domain sensitivity versus the wire's cohomology index

The earlier wire code computed a relative de Rham complex on M=(solid torus) minus m balls with r selected relative spheres and obtained b1=r,b2=m-r. It is neither a spinor Dirac calculation nor a physical APS problem. To test the assumption that such indices are automatic consequences of the underlying space, this pass constructs a *different actual graded Dirac-type operator* in a simpler setting, D=[[0,Q†],[Q,0]] with Q the finite difference on a chain of nine links:

    (Q v)_i=v_(i+1)-2v_i.

The *same nine-edge interval* with three compatible adjoint operator domains yields:

    boundary domain                 dim ker Q    dim ker Q†    index
    free both endpoints                  1             0         +1
    one fixed endpoint                   0             0          0
    both endpoints fixed                 0             1         -1.

All values follow from exact integer matrix ranks and rectangular rank-nullity. This is the finite-algebra form of the Fredholm boundary index identity; the full graded D is Hermitian for each adjoint-paired domain. On a closed circle, Q is a square matrix and index0 for every nonzero twist, even when the boundary multiplier t=2^9 creates a simultaneous right and left zero mode. A complex flat multiplier by itself does NOT produce unpaired chirality on a compact, boundaryless circle.

This is an explicit counterexample to conflating a chosen relative cohomology count with a physically necessary spinor index. It is **not** a solution of the 7D G2 flux-coupled spinor/APS problem and does not prove the current wire model wrong. It states the missing input precisely: a gauge-compatible operator domain and its physical origin, including eta and anomaly inflow.

Source context: Pantev-Wijnholt G2 Higgs bundles https://arxiv.org/abs/0905.1968; local G2 models https://link.springer.com/article/10.1007/JHEP05%282021%29002; singular G2 anomaly inflow https://www.sciencedirect.com/science/article/abs/pii/S0550321303007399.

## Front C — a restricted single-axion Green-Schwarz normalization gate

For three complete localized spinor16_-3 families the net left-handed fermion traces of the extra Psi generator, using a standard SU5 fundamental Dynkin index T(5)=1/2, are:

    A_SU3²Psi=A_SU2²Psi=3/5 A_Y²Psi=-18,
    A_gravPsi=-144,
    Tr(a Chi+b Psi)^3=-432 b(5a²+3b²).

The previous packet correctly noted factorization through Psi, which permits *a priori* a suitably coupled generalized GS axion.

As an additional **explicitly restricted, conditional** check, impose the 4D weakly coupled *heterotic universal* GS normalization

    A_G / k_G = A_grav / 24.

In the given charge/trace convention this requires

    -18/k_G = -144/24 = -6  -> k_G=3.

A canonical level-one equal-coupling dilaton axion does NOT satisfy this *specific* universality condition without additional matter or alternate normalization. This does **not** rule out M-theory G2 inflow, a general nonuniversal 4D axion, Green-Schwarz counterterms, multiple axions or redefined charges. Crucially the number three for k_G appears *even with one, two or five complete identically charged 16s*; it is NOT a derivation of three physical generations. Actual UV anomaly cancellation and axion quantization remain undone.

Source convention literature: https://doi.org/10.1103/PhysRevD.111.015048; https://escholarship.org/uc/item/2t41z808; also G2 anomaly paper above.

## Front D — count actual BF-unsafe lattice winding vectors, not only modular area

The previous conditional mixed winding branch used

    lambda_(u,v)=3*pi*r*|u+v*tau|²/Im(tau), r=N0/N,
    m_minus² L²=lambda-2-sqrt(4+16lambda), BF threshold -4.

Thus mode (u,v)!=0 is BF-unsafe precisely when 0<lambda<12. The earlier modular-area analysis integrated over shape; that is not a count of unstable fields for a *particular* shape.

Enumerating all integer vectors |u|,|v|<=12, certified exhaustive for r>=0.35 in both reference shapes, gives the following **oriented** counts for the branch:

    ratio r       tau=i (square)       tau=e^(i*pi/3) (hex)
       0.35             8                      12
       0.50             8                       6
       0.75             4                       6
       1.00             4                       6
       1.05             4                       6
       1.20             4                       0
       1.30             0                       0
       2.00             0                       0.

At r=1, the hexagonal torus has SIX shortest directed unstable winding vectors (three +/- pairs), whereas the square has FOUR (two +/- pairs). At r=1.2 hex is stable within this branch but square still has four BF-unsafe vectors, so a statement of "stable flux ratio" without the modular shape is misleading. Critical ratios are exactly r_crit(square norm n)=4/(pi*n) and r_crit(hex norm n)=2sqrt3/(pi*n), where hex n=u²+uv+v². For every fixed finite ratio, arbitrarily deep cusp moduli remain unstable in this conditional branch.

**Warning**: +/- oriented windings may be paired by a physical reality condition; these are lattice vectors, not a claim of independent dynamical tachyon fields. The mass formula is conditional and neither the real corrected M-theory spectrum nor backreaction is supplied.

## Front E — genuine *three-time* quantum memory, with a falsifiable visibility threshold

The previous qutrit Bell witness only tested whether a specified effective *one-time* channel preserved entanglement. Entanglement-breaking channels can still participate in genuinely quantum *multitime* processes (Vieira et al, PRR 2025 https://arxiv.org/abs/2402.16789), so that is insufficient as a universal memory classification.

We independently implemented the newly released exact qubit triple of **Beyer et al, Observation of Genuine Multi-Time Quantum Memory, submitted November 12, 2026, arXiv:2611.17268v1** (https://arxiv.org/html/2611.17268v1). These are an amplitude-damping channel of strength gamma at t1, a z-dephasing channel of strength p at t2, and an x-dephasing channel of strength p at t3.

The paper proves that all pairs are compatible with some (pair-specific) classical memory whenever p >=(1-sqrt(1-gamma))/2, yet that a common classical three-time memory model cannot realize the triple. Rather than just quote the result, the code reconstructs **all three pairwise CPTP decompositions** using the authors' explicit Kraus formulas (Appendix C):
- t1,t2: standard two damping Kraus operators plus conditional reverse-jump and z-dephasing;
- t1,t3: the +/- unitary-rotated damping Kraus basis followed by conditional y-rotations and x-dephasing;
- t2,t3: a classical record of the phase flip undoing z-dephasing followed by x-dephasing.

For four independent values (gamma,p)=(.36,.20),(.64,.30),(.25,.14),(.81,.40), every decomposed map matches the corresponding target qubit channel's **entire Choi matrix** within 2.3e-16, while the joint witness gives W3=-gamma<0. This is a genuine pairwise-classical/triple-quantum separation, but the theorem and construction are explicitly from the November 2026 published paper, not novel research by us.

A further engineering calculation is an original simple noise-budget corollary for this *particular fixed-axis witness*. If the two later channels each suffer independent isotropic Bloch visibility factor eta, then the square-root fidelities of their protected antipodal output pairs become sqrt(1-eta²). The same axes give

    W3(axis z,x)=2sqrt(1-eta²)-gamma.

At gamma=.36 this axes-based certificate remains negative iff

    eta > sqrt(1-(gamma/2)²) = 0.983666610188635.

The threshold is demanding (less than approximately1.633% Bloch visibility loss), but it refers only to this sufficient orthogonal-axis witness and this noise model; optimizing over axes or other witnesses could improve experimental tolerance. Subsequent depolarizing channels are CPTP post-processings and preserve each previously exhibited pairwise classical explanation. This yields a practical calibration target for a future optical implementation without pretending such hardware was measured. It also suggests combining our existing qutrit anytime-valid E-process with *independent* full three-time tomography rather than conflating their interpretations.

## Files and test strategy

Additive outputs generated on the authorized computer TheHeavyCrown:

- analysis/toe_20261118_native_W33_dual27_twoqutrit_siegel_crosscheck.py
- data/toe_20261118_native_W33_dual27_twoqutrit_siegel_crosscheck.json
- analysis/toe_20261118_TOE_phys_falsifiers_anomaly_winding_multitime.py
- data/toe_20261118_TOE_phys_falsifiers_anomaly_winding_multitime.json
- tests/test_toe_20261118_W33_Clifford_GS_Dirac_genuine_multitime.py
- analysis/2026-11-18_native_siegel_twoqutrit_GS_wire_three_time_falsifiers.md (this report).

Run the two producer scripts directly from repository root and the named unittest. No existing tracked file is modified by the producers; their new JSON names are unique. The repository is concurrently used by other assistants. The preexisting modified tracked files MUST remain untouched and outside staging.

## Five most consequential independent next checks

1. **Actual wire/G2 chiral spinor operator**: derive the physical twisted seven-dimensional Dirac complex, spin structure, mass defect, source terms and gauge-invariant APS/local boundary projectors; compute index, eta correction and conserved currents. Falsify the three-family expectation if domains are not physically allowed.
2. **UV Green–Schwarz and E6 vacuum**: explicitly produce the chiral matter/inflow and *quantized* coefficients required to cancel both mixed non-Abelian and gravitational Psi anomalies, then solve coupled 78+27bar+27 Higgs superpotential with genuine compactification zero modes and Yukawa overlap matrices.
3. **Native parabolic-to-E6 compiler**: exploit the exact Siegel C3³ = two-qutrit quadratic-phase group, its order9 intersection with point H27, and the prior Pass11043 commutant dressing to build a SOURCE-verified gauge-equivariant operator map that respects E6 charge, rather than an impossible direct regular27<->operator27 equivalence.
4. **Full corrected string/M stability**: compute normalized complete KK/winding masses and actual correction operator norms (including radius shifts/backreaction); compare square vs hex BF mode counts and their multiplicities under valid physical reality conditions and flux quantization.
5. **Operational multitime memory trial**: implement the Beyer et al three-time channel-tomography controls with qutrit optical channels only after deriving an appropriate d=3 witness/SDP, calibrate conditional heralding efficiency and execute an anytime martingale test under explicit detector nulls.

**Summary:** The most interesting combined W33 structure is now *explicitly computational*: the point-parabolic Heisenberg H27 supplies the regular 27-address shell, the line-parabolic C3³ supplies a complete 27-element entangling/local two-qutrit Clifford phase gate family, and their intersections depend on W33 point–line incidence. Those are well-defined finite quantum-information resources; turning them into physical three-family spacetime/gauge dynamics remains unproved. The strongest physical falsifier is the boundary-domain and anomaly-normalization dependence, while the newest experimentally actionable bridge is the genuine three-time memory witness with a quantitative visibility budget.
