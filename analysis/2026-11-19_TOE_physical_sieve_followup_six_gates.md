# TOE physics sieve: six deeper gates beyond geometry numerology

**Date:** 2026-11-19. **Research goal:** physical unification—global chiral matter, a natural quantum vacuum, dynamical Einstein geometry, operational quantum-information consistency, and predicted couplings/masses. **Not a solved TOE.** The repo W33-Theory is used only to store and compare research; no W33 assumption enters this pass.

## Independent review and claim-status boundary

Started from local/GitHub master `5b45a41af`. Read the actual Nov 19 reports `analysis/2026-11-19_E8_nonproportional_PW_vacuum_gates.md`, `analysis/2026-11-19_model_independent_TOE_consistency_sieve.md`, and `analysis/2026-11-19_TOE_five_physical_gates_beyond_W33.md`. The E8 report supplies, as **inputs**, six 16s and three conjugate 16bars, local index three, rank-two bare 16–16–10 Yukawas, anomalous Abelian currents, and obstructed noncompact D/F-flat vacuum. It already remarks that the local model has no compact dynamical gravity completion. The model-independent sieve already proves U(1) charge-mixing ambiguity, one-loop SM gauge mismatch, provisional neutrino minima, CPL dark-energy facts, ghost-pole warnings and Tsirelson's bound. **Parallel update:** during this pass commit `f6a01555` established additional native E8 holonomy, degree-four C-field torsion and an obstruction to hosting the Standard Model inside its particular compact centralizer. Subsequent independent commit `67c1c650` evaluates a two-loop SM/top-Yukawa running benchmark and split-GUT thresholds; our exact rational *degenerate-complete-multiplet* argument and formal one-loop threshold sensitivity are narrower and distinct, not competing two-loop predictions. Those are the parallel assistant's results, not ours; they further motivate global anomaly/correct-gauge-spectrum tests rather than replacing our present physical gates. The previous five physical gates already prove a compact Euler/index problem, a one-loop asymptotically free SU4 matter-content parent, and one-photon exponential mode requirements.

**New precise increments:** explicit U(9) unitary mapping between physically inequivalent *labeled* SIC and non-SIC tight frames; IR conformal scaling of baryons in the undeformed SU4 parent; discrete Hodge exact-vs-nonexact compact cohomology; gravity matter HH algebra with variable q(x) and its failure to equal full D when q is dynamic; transparent event-ready sample-size and channel-mixture bounds; exact rational complete-SU5 multiplet no-go; alpha_s sensitivity of the formally exact SM/MSSM threshold; two-neutrino-seesaw rank contrast. These results are conditional extensions of known mathematical/QFT principles, with no unsupported priority claim.

## Gate 1: global chirality must survive compact geometry, not only local Morse analysis

For any compact, connected, oriented Riemannian three-manifold **without boundary**, suppose the Cartan Higgs field is a globally exact, coclosed one-form `phi=df` (in particular harmonic: `d phi=delta phi=0`). Integrating by parts gives

    integral_M |df|² vol = integral_M f (delta df) vol = 0.

Thus `df=0` identically. **A nontrivial globally exact harmonic Cartan profile simply does not exist on that compact base.** This strengthens the previous Euler-characteristic obstruction. It is the Hodge-theory maximum principle; a nonexact harmonic 1-form can exist when b1(M)>0, and singular/source-bearing or nonabelian gauge-covariant Higgs data need not obey this exact argument.

A discrete cochain test uses an independent 3x3x3 periodic cubic torus (27 vertices, 81 directed positive edges). The incidence D: C^0 -> C^1 has rank26; the only exact harmonic 0-cochain is a constant. The identity `f^T D^T D f=||D f||²` holds numerically. A constant winding x-edge 1-cochain has `D^T omega=0` and is *not* exact, illustrating the alternative of a global nontrivial H1 class. This is an illustration; the continuum proof above stands independently.

The particular f1 from the E8 noncompact localizer has three nondegenerate critical points with gradient indices (-1,-1,-1), so the local sum is -3. A globally smooth vector field on a closed oriented 3-manifold has total index Euler(M)=0. **The -3 needs global compensation or a change of assumptions.** This is a statement about the specific f1 local degree; it is NOT an identification of f1's degree with the entire E8 spinor chirality index, nor a universal no-go for singular G2 M-theory.

Relevant established literature: [Acharya–Witten, chiral G2 singularities](https://arxiv.org/abs/hep-th/0109152); [Braun et al., M-theory Higgs bundles](https://link.springer.com/article/10.1007/JHEP03%282019%29199); [Anomalies on singular G2 manifolds](https://arxiv.org/abs/hep-th/0303243).

## Gate 2: distinguish an intrinsic SIC from arbitrary flavor-frame coordinates

Let Q be a 3x9 matrix of unnormalized Hesse qutrit SIC columns and B be three copies each of sqrt(2)e1, sqrt(2)e2, sqrt(2)e3. Both have `Q Q^dag = B B^dag = 6 I3`; each column has norm squared2. But the SIC has 36 pairwise overlap squared values equal1, while B has 27 zero overlaps and nine overlaps equal4. The latter is NOT a SIC.

**Stronger theorem.** For any two 3x9 complex matrices A,B satisfying AA^dag=BB^dag=6I, there exists a right **unitary U in U(9)** with `AU=B`. Proof: A/sqrt6 and B/sqrt6 are isometric coframes; complete their respective three orthonormal rows to bases of C9 and compose the completion matrices. The code constructs the actual U using null-space completions and verifies U^dag U=I and QU=B with residual ~3e-16.

Consequently, **an exactly U(9)-flavor-invariant potential cannot energetically distinguish which physical flavor label realizes the Hesse SIC** while selecting only the right-unitary orbit. A mechanism purporting to derive SIC as a physically preferred frame must specify actual flavor-breaking invariants/interactions or relational observables that identify those labels. A global U(9) symmetry could relate the frames as degenerate vacua; absent a physical preferred flavor basis, calling just one a SIC is coordinate-dependent.

**UV parent obstruction refined.** The previously constructed vectorlike SU4, Nf=10 has one-loop `b0=3Nc-Nf=2>0`, but ordinary massless `N=1` SQCD with `6<Nf=10<12` sits in the proposed Seiberg conformal window. Assuming the ordinary undeformed interacting fixed point,

    R_Q = 1-Nc/Nf = 3/5,     Delta_Q=3R_Q/2=9/10,
    Delta_mes = 9/5,        Delta_B(Q^4) =18/5=3.6.

A bare baryon superpotential coupling `W~Q^4` is **irrelevant** (operator dimension>3), and `W~S Q^4` with a decoupled free singlet has dimension23/5=4.6, also irrelevant. This undermines the simplest hope that an AF parent *automatically* makes a baryonic SIC-selector grow strong toward the IR. These dimensions are **not** asserted for the prior tuned Higgsed/singlet-coupled model, which modifies the RG fixed point; mediator completions and proper F/D and RG checks remain open.

Relevant QFT background: [four-dimensional SQCD](https://link.springer.com/chapter/10.1007/978-3-032-09219-9_18); [conformal-window summary](https://qft.org/supersymmetry-duality/n1-duality-rg-scft/conformal-window-fixed-points/).

## Gate 3: a variable metric is not enough to obtain dynamical Einstein gravity

On a 1D curved spatial slice with **prescribed** positive spatial metric component q(x), a minimally coupled scalar with canonical pi_phi has Hamiltonian and matter diffeomorphism constraints

    H_m[N] = 1/2 int dx N (pi_phi² + (partial_x phi)²) / sqrt(q),
    D_m[xi] = int dx xi pi_phi partial_x phi.

The **exact classical Poisson bracket** (holding q fixed as external during this matter-matter calculation) is

    {H_m[N],H_m[M]} = D_m[(N M'-M N') / q].

The q^-1 is an actual nonconstant spatial metric structure function, unlike the constant-coefficient free-string example. We verify it on periodic samples using both centered and Fourier derivatives for N=32,64,128,256 and a nonconstant q(x). Centered differences converge but break Leibniz at finite spacing; low-frequency Fourier differentiation converges to numerical precision, while high-frequency aliasing again exposes the finite-resolution limit.

**A second no-go appears if one prematurely declares q dynamical.** A metric treated as a canonical field also has conjugate momentum p_q and contributes to the *full* spatial diffeomorphism constraint

    D_g = p_q q' - 2 (q p_q)'.

The matter-matter bracket above produces only D_m, **not** D_total=D_m+D_g. The script constructs a nonzero sample D_g. Therefore one cannot obtain a first-class gravity+matter theory by declaring a background variable: one needs a gravitational Hamiltonian and its brackets/cross terms. This is a precise **toy-sector closure failure**, not an impossibility theorem for GR. Still missing are the actual 3+1 ADM gravitational Hamiltonian, Dirac/hypersurface algebra including quantum anomalies, and a causal Lorentzian continuum limit.

Background: [hypersurface deformation algebra and metric dependence](https://link.springer.com/article/10.1007/s10714-024-03313-w).

## Gate 4: event-ready quantum-memory tests should have explicit statistical power

For the three-level SWAP memory under isotropic depolarizing storage rate p, conditional Bell fidelity is `F=1-8p/9`. If all prepared trials count and loss contributes zero Bell successes, and if the classical-only comparator is an entanglement-breaking input-output channel against a trusted isolated reference, the sufficient one-sided witness is

    eta F > 1/3,  i.e. eta > 1/[3(1-8p/9)].

For p=.20, this threshold is **15/37 ~0.4054054**, assuming the detector loss model and no bypass. We calculate this for efficiencies from .30 to1.0. At a *particular observed sample mean* s=eta F>1/3, the one-sided Hoeffding lower limit is `s - sqrt(log(1/alpha)/(2N))`. The file stores the N that would make this observed lower limit cross 1/3 **if the observed frequency equaled its expectation**. It is NOT guaranteed high power at that N: actual Bernoulli fluctuations, calibration and multiple tests need explicit power calculation. No-click trials are **failures**, not postselected away.

In the restrictive mixture channel `E=c E_ideal+(1-c) E_EB`, the observed Bell fidelity obeys `Fobs <= c+(1-c)/3` and therefore `c >= (3Fobs-1)/2`. For eta=.5 and p=.2 this necessary lower bound is approximately **0.1167**. This is not a model-independent lower bound on quantum capacity. The standard one-photon dimension theorem also remains: M one-excitation orthogonal modes cannot faithfully embed 2^n arbitrary amplitudes for n qubits unless M>=2^n. The operational physics program must confront loss, interventions, source independence and scalable addressing directly.

## Gate 5: measured gauge unification is insensitive to degenerate complete SU5 multiplets at one loop

In an N=1 SU5-normalized theory, compute exact chiral-superfield beta contributions (b1,b2,b3):

    5bar -> d^c:(3bar,1,1/3) + L:(1,2,-1/2): (1/2,1/2,1/2).
    10 -> Q:(3,2,1/6) + u^c:(3bar,1,-2/3) + e^c:(1,1,1):
            (3/2,3/2,3/2).

Thus an equal-mass vectorlike 5+5bar adds (1,1,1), and 10+10bar adds (3,3,3). **At one loop these universal shifts cancel from all differences** `alpha_i^-1-alpha_j^-1`. Adding degenerate *complete* SU5 representations alone cannot repair the observed one-loop SM three-coupling mismatch. Nondegenerate multiplet splitting, two-loop effects, or some other nonuniversal threshold is necessary. This is standard GUT matching mathematics, now an exact rational regression test for our proposed field spectrum.

With stated central input `alpha_em^-1(MZ)=127.930`, `sin²thetaW=.23122`, `alpha_s(MZ)=.1177`, `MZ=91.1876 GeV`, invert the two independent one-loop matching equations for a *sharp* SM-below/MSSM-above threshold and common meeting scale. The formal exact fit gives

    M_switch = 68.32673776 GeV (< MZ),
    M_GUT = 2.176861e16 GeV.

Thus **this particular one-loop spectrum with one common ABOVE-MZ MSSM threshold cannot exactly fit all three nominal central couplings**. A repeat with illustrative alpha_s={.1168,.1177,.1186} shifts the formal M_switch to ~{92.52,68.33,50.69} GeV. Uncertainties and heavy thresholds matter strongly: this is NOT a no-go for realistic SUSY unification or SU5, and is not a novel measured parameter prediction. For a hard 1 TeV threshold the inverse alpha3 mismatch persists.

Background: [PDG grand unified theories](https://pdg.lbl.gov/2025/reviews/rpp2025-rev-guts.pdf); [complete SU5 multiplet beta universality](https://link.springer.com/article/10.1140/epjc/s10052-025-14320-9).

## Sixth check: massless neutrino is not equivalent to a massless charged family

A type-I seesaw with **two** heavy right-handed neutrinos and generic full-rank 3x2 Dirac Yukawa matrix has

    m_nu = -M_D M_R^(-1) M_D^T,   rank(m_nu)<=2.

One active neutrino is massless at this tree level; unlike a tree-level massless charged fermion, this is not excluded by oscillation splittings. For the **provisional Bari 2026.a** splittings as already included in repository `8efe83ec`, lower normal/inverted sums are respectively ~0.05873 eV and ~0.09962 eV (when the lightest mass is zero). This comparison emphasizes that a rank-two *neutrino* model may remain viable, while the earlier local E8 rank-two *charged* Yukawa texture fails to reproduce all observed charged-fermion masses in the minimal bare mechanism. Radiative corrections, additional operators and experimental bounds must be tracked.

## Reproduction and rigorous scope

    python analysis/toe_20261119_toe_physical_sieve_followup.py
    python -m unittest discover -s tests -p test_toe_20261119_toe_physical_sieve_followup.py -v

The deterministic machine-readable output is `data/toe_20261119_toe_physical_sieve_followup.json`.

The script tests discrete Hodge rank/eigenvalues, actual local Morse Hessians, a 9x9 explicit unitary frame map, exact fractional superconformal dimensions, ADM matter bracket convergence and a missing gravitational momentum term, all-trial quantum witness bounds, exact rational SU5 beta universality, spectrum-threshold inversion, and generic two-heavy-neutrino seesaw rank. All results are **conditional known or derived mathematics**, not independent discovery of an E8 vacuum, gravity, neutrino mass model, or photons behaving beyond standard quantum theory.

## Five independent next experiments/constructions

1. Build an **actual compact singular-G2 and ADE gauge bundle**, with global charge-by-charge chiral index, local anomaly inflow, quantized fluxes and compactification Einstein equations; do not identify one local Morse degree with net four-dimensional families.
2. Construct a **flavor-physical RG-consistent SIC/particle vacuum**, specifying which interactions break flavor U9, an asymptotically free UV Lagrangian, full F/D equations, thresholds, realistic unbroken SM group, and full-rank charged Yukawas.
3. Derive the **complete 3+1 ADM gravity-plus-matter algebra and quantum anomaly**, including dynamical q,pq, correct causal light cones and a nonperturbative consistency criterion, rather than a matter-only constraint on a prescribed metric.
4. Test **event-ready qutrit process tomography with independently sealed reference and prepared-trial accounting**, compute statistical power and photon-loss loopholes, and give explicit resource scaling for arbitrary registers.
5. Run **two-loop actual measured-parameter fit with mass-split SU5/E8 thresholds**, proton-decay and neutrino operators, blinded predictions and uncertainties; complete multiplets at one degenerate mass are not enough.
