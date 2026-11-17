# TOE physics audit — full E6 Lie stabilizer, near-equal KK asymptotics, R4 control, discrete flux and adaptive qutrit witness

**Date:** 16 November 2026. **Scientific status:** exact finite algebra and topology results, conditional asymptotic physics, synthetic statistics. **No completed TOE, computed 11D eight-derivative action, full unequal-flux KK operator, dynamical Standard Model vacuum, worldsheet winding spectrum, or real photon data.**

## Repo provenance and source checks

Used live `wilcompute/W33-Theory` and authorized local `C:\Repos\Theory of Everything`. Initial head was `a574c9f102e194300a2bb64be0d4129c0a065192`; other research tracks continued pushing commits while this work ran. Read the repo's `analysis/2026-11-16_D9_mtheory_uplift.md`, `analysis/2026-11-16_Tpq_coupled_warp_branch.md`, `analysis/2026-11-16_Tpq_warp_mtheory_lift.md`, previous BF and K-theory audits, `analysis/2026-11-16_fivefront_robust_BF_Tdual_spin_E6_optics.md`, and pre-existing H27 scripts `analysis/w33_pass5727_5730_torsion_family_heisenberg.py` and `analysis/w33_20261008_torus_H27_flat_flux.py`. No older scientific claim is silently presented as an original discovery.

Relevant public context: Particle Data Group *Grand Unified Theories* (2025), https://ccwww.kek.jp/pdg/2025/reviews/rpp2025-rev-guts.pdf ; *The E6 route to multicomponent dark matter* (2025), https://doi.org/10.1140/epjc/s10052-025-15043-7 ; *Dynamics of E6 chiral gauge theories* (2025), https://journals.aps.org/prd/abstract/10.1103/cksl-66x7 ; the mathematical T-duality literature https://arxiv.org/abs/hep-th/0306062 ; Gubser–Mitra type AdS5 compactification stability literature; qutrit MUB/process-tensor methods in the earlier repo reports.

## 1. Near-equal flux: first-order geometry and a CONDITIONAL KK mass prediction

Earlier work found an exactly physical, sphere-odd scalar–Maxwell mode on the **equal** M-theory product, with square torus first momentum `lambda0=3pi` and `m0² L²=3pi-2-sqrt(4+48pi)=-5.016944081307837...`. The actual `N1 != N2` physical gauge-constrained operator has **not** been diagonalized.

For positive integer periods `(N1,N2,N0)=(N+1,N,N)`, use the earlier exact period relation
`(N1/N2)^2=eta*(2-eta)^2/[(1-eta)*(1+eta)^2]`, `eta=1/2+3/(2N)+O(N^-2)`,
`k2=4(2-eta)` and
`area(T2)/L²=16pi(N+1)/[N*k2*sqrt(8eta)]`.
The square-torus first eigenvalue therefore has a new, exact, geometric expansion

`lambda1(N)=3pi*(1-1/(2N))+O(N^-2).`

At fixed mean mixed-flux period, exchange of the two sphere factors sends `eta-1/2` to its negative. For an **isolated physical eigenbranch that remains smooth through this exchange**, the odd anisotropy perturbation cannot contribute to the first derivative of that eigenvalue. Consequently its first-order continuation must be

`m² L² = m0² L² - [3pi/2]*(1-8/sqrt(4+48pi))/N + O(N^-2)`
`         = -5.0169440813 -1.6823331959/N +O(N^-2).`

**Falsifiability boundary:** The program evaluates the exact torus geometry and the equal-formula **proxy**, but NOT the full unequal-flux eigenmass. The displayed physical eigenvalue expansion additionally requires smooth constrained gauge fixing, an isolated branch, and the sphere-interchange symmetry. A full matrix derivation must test the (O(N^{-2})) sector and possible mode crossings. No explicit finite N threshold is certified.

Producer `analysis/toe_20261116_nearequal_KK_firstorder_exchange.py`; JSON `data/toe_20261116_nearequal_KK_firstorder_exchange.json`.

## 2. What eight-derivative corrections can and cannot rescue

The prior rigorous classical theorem for **equal** fluxes `N0=N1=N2=N` gives, for every flat torus shape, a scalar–Maxwell BF gap at least
`delta*=sqrt(4+32pi sqrt(3))-2pi sqrt(3)-2 = 0.463541850418787...`.
The quantized AdS radius obeys `(L/lp)^3=(9pi/2)N`.

If — and ONLY if — the **entire** corrected canonically normalized physical fluctuation operator has perturbation norm at most `C(lp/L)^6`, the Rayleigh quotient guarantees a BF-unstable mode whenever

`C<delta*(9pi*N/2)^2 = 92.6432374114*N^2.`

This is a conditional perturbation-operator inequality, NOT a derivation of the M-theory `R^4+G4` completion or its coefficient. It is complementary to the older nearly equal homogeneous threshold `3645pi²/4`: that threshold concerns a different mode.

**Crucial controlled-shape caveat:** An 11D torus with reduced shape `tau=x+iy` has shortest physical cycle radius
`R_min/lp=(L/lp)/sqrt(3pi*y)`.
The sphere radius is `L/(sqrt6 lp)`. To keep all cycles above a specified radius `r_cut*lp`, one requires `y <= (9pi N/2)^(2/3)/(3pi r_cut²)` plus the sphere bound. The classical *shape-uniform* gap does not mean an uncontrolled modular cusp supports a uniform 11D derivative expansion.

Producer `analysis/toe_20261116_8derivative_shape_control.py`; JSON `data/toe_20261116_8derivative_shape_control_certificate.json`.

## 3. M/IIB global flux labels: a genuinely conditional Heisenberg interface

Earlier M/IIB work established the circle-bundle fundamental group `pi1(Y)=Z_g` and a discrete M C-field translation subgroup `Gamma_g=Z_g x Z_g`, with `g=gcd(|N1|,|N2|)`. The older repo already constructs finite H27 in other qutrit and torsion contexts. Here we test a **new interface**: if physical translations acquired the standard nondegenerate projective cocycle, they would lift to the finite group

`H_g = {(a,b,c) mod g}`, multiplication
`(a,b,c)*(a',b',c')=(a+a',b+b',c+c'+b*a') mod g`,
order `g³`, center `Z_g`, quotient `Z_g²`, commutator `b*a'-b'*a`.

For g=3 the Schrödinger qutrit representation is exactly the existing H27, with matrix operators X,Z satisfying `ZX=omega XZ`; full 729 ordered group-product identities and standard qutrit Fourier/phase-Clifford identities pass. For coprime factors, Chinese remaindering gives `H_(gh)=H_g x H_h`; in particular `H6=H2 x H3`. Conversely `H9` is NOT `H3 x H3`, since their centers have different exponents.

The near-equal flux contrast is dramatic: `gcd(N,N)=N` whereas `gcd(N+1,N)=1`; the **candidate** finite Heisenberg model collapses from order `N³` to the trivial group while smooth local M-theory KK fluctuations can persist. Thus any model identifying the *entire* physical oscillator Hilbert space with these finite topological labels would fail.

**Major boundary:** A particular projective cocycle for the real C-field translation operators has NOT been extracted from their Wess–Zumino/Berry pairing. The H_g extension is a mathematically consistent conditional quantization, not a measured or derived physical commutator. Nor is it a novel rediscovery of the known abstract H27.

Producer `analysis/toe_20261116_M_IIB_flux_Heisenberg_CRT.py`; JSON `data/toe_20261116_M_IIB_flux_Heisenberg_CRT.json`.

## 4. Strongest result: FULL E6 cubic-invariant stabilizer and exact Standard Model embedding

**Important correction of an incomplete manifest-subgroup analysis.** With the (27) arranged into three (3x3) matrices `A,B,C`, the standard cubic invariant is
`I3=det A+det B+det C-Tr(ABC)`.
Construct all 45 distinct signed cubic monomials. Write a general infinitesimal `27x27` complex endomorphism `T` with 729 unknown entries. Requiring `dI3(x)(T*x)=0` for all x produces 2475 monomial-equation rows. **Exact rational elimination** gives rank 651 and therefore 78 derivations: the complex E6 Lie algebra. Independent computations modulo primes 101 and 103 give the same rank.

Choose two independent Higgs VEVs in the `(1,3,bar3)` sector:
`A1=v*(e3 e3^T)`, `A2=v*(e3 e2^T)`, plus aligned **conjugate 27bar partners**. The conjugate VEVs contribute opposite D-terms for each compact E6 generator, so D-flatness holds pairwise. Every linear combination of the two A-sector Higgs VEVs has rank <=1 and therefore zero adjugate, making its polarized determinant cubic F-derivatives zero **for the cubic-only Higgs terms**. Other superpotential operators might spoil F-flatness and have not been specified.

The full E6 infinitesimal stabilizer must annihilate both 27 vectors and both dual covectors. Add row/column constraints for coordinates 7,8. The exact rank rises to **705**, leaving **24** generators. From the original 72 E6 roots, **20** survive alongside four diagonal Cartan generators: the root type is **A4**, i.e. `su(5)`. The original manifest subgroup intersection had dimension four (`su2_L+u1`) plus color, but this was NOT the complete E6 stabilizer.

Add a diagonal **adjoint 78 Higgs** along the explicit generator `Y`:
`Y_L=diag(1,1,-2), Y_R=diag(4,-2,-2),Y_C=0`.
This generator preserves the two vector VEVs. Adding the adjoint commutation condition `[T,Y]=0` raises exact rank to **717**; only **12 generators** survive, specifically eight nonzero roots (A2 for color and A1 for weak) plus four Cartans. Thus at the Lie-algebra level, the stages are

`E6 (78) -> SU5 (24) -> SU3_C + SU2_L + U1 (12)`.

The six diagonal E6 Cartan directions reduce to four; the full E6 stabilizer is checked over Q and mod101/mod103. The one-27 hypercharges satisfy `Y_SM=-Y_integer/6` and branch into
`Q(3,2,1/6),u^c(bar3,1,-2/3),e^c(1,1,1),2 d^c(bar3,1,1/3),2 L(1,2,-1/2),H_u(1,2,+1/2),D(3,1,-1/3),2 N(1,1,0)`.
Exact rational sums give zero for `SU3^3`, `SU3²-U1`, `SU2²-U1`, `grav-U1`, `U1³`; six SU2 doublets also pass global Witten parity.

A separate exact manifest gauge-boson mass test with the two 27+27bar pairs gives 4 massless modes and 12 massive modes with square-mass multiplicities `4 x g²v²`, `7 x 2g²v²`, and `1 x (10/3)g²v²` in the chosen canonical convention. The adjoint VEV further lifts the 12 off-diagonal SU5 generators.

**What has NOT been established:** A complete scalar superpotential or its bounded stable minimum with both 27+27bar and adjoint, the adjoint F-term equations, rank-four global gauge-group quotient, mass of all exotic vectorlike (5+\bar5) fermions, three generations, realistic Yukawa couplings, precise vacuum scales, proton stability, or the emergence of these fields from W33. The branching matches established E6 group theory; the *exact cubic stabilizer construction and automated obstruction/adjoint test* are this packet's contribution.

Producers:
`analysis/toe_20261116_E6_two_Higgs_SM_stabilizer.py`,
`analysis/toe_20261116_E6_full_cubic_SM_stabilizer.py`.
JSON certificates in `data/` with matching stems.

## 5. A qutrit temporal-memory witness valid under adaptive non-IID separable sources

The prior four-MUB Bell identity gives a separable matched-basis sum at most two. Rather than fixing equal block counts and assuming IID, prepare the heralded reference/system state *before* secretly drawing an independent uniform current measurement setting among the four qutrit MUB pairs. Record each heralded trial as binary `Y_t=1` for click AND match, zero otherwise (including no-click).

If the present instrument's measured click-match effect is calibrated to be at most the ideal projector plus absolute error epsilon per setting, every separable prepared state, even one depending on arbitrary **past history**, has

`E[Y_t | history] <= 1/2 + epsilon`.

The bounded-difference supermartingale Hoeffding inequality therefore gives the **non-IID valid** rejection bound

`Pr( mean(Y) >= 1/2 + epsilon + u | separable adaptive null ) <= exp(-2 M u²)`.

This assumes the fresh setting choice cannot leak to the source *before state preparation*; it is NOT a device-independent Bell test or a guarantee against malicious setting-side channels. It avoids an IID null assumption and explicitly counts lost photons without fair-sampling postselection.

Only for power planning under stationary isotropic alternative `rho(v)=v Phi3+(1-v) I9/9` and independent pair efficiency eta is `E[Y]=eta(1+2v)/3`. A conservative alpha=.01,beta=.1 calculation at v=.75,eta=.70,epsilon=.01 gives **1,248 gross event-ready trials**. The synthetic program uses reproducible seeds, includes time-varying loss and visibility and a history-adaptive *separable* source. For the fixed 2,500-trial example, coherent synthetic source p-bound `3.03e-11` and adaptive separable control p-bound `1`. These numbers are NOT measured hardware outcomes.

Producer `analysis/toe_20261116_qutrit_randomized_memory_drift.py`; JSON `data/toe_20261116_qutrit_randomized_memory_drift.json`.

## Reproduction, peer review, and boundaries

Run each analysis producer directly, then:
`python -m unittest discover -s tests -p test_toe_20261116_full_E6_R4_charge_qutrit.py -v`.
The one test module contains **20 targeted tests** across the six programs, including a large exact cubic derivation calculation and prior results. Previous tensor/charge/qutrit suites may also be run independently.

Never present the full E6 stabilizer computation as a solved phenomenological vacuum, the conditional near-equal KK mass as an eigenvalue obtained from a full unequal-flux operator, or the synthetic event-ready statistics as optical evidence.

## Most consequential independent next problems

1. Derive the true unequal-flux constrained 11D KK matrix to order `1/N²` and check the exchange-symmetry eigenbranch.
2. Specify and solve a bounded SUSY superpotential for two 27+27bar pairs plus adjoint 78 and compute all scalar, Yukawa and gauge boson masses; test unbroken SM and proton constraints.
3. Compute the complete M-theory flux-dependent eight-derivative correction to the physical BF eigenvalue, including corrected backgrounds and spinor sectors.
4. Compute the actual C-field magnetic-translation cocycle/Wess–Zumino pairing and the remaining nonprimitive twisted-K extensions; only then promote candidate H_g to a physical charge operator algebra.
5. Implement calibrated qutrit MUB POVMs and independent delayed basis choice in hardware, then analyze an event-ready non-IID photon dataset with exact precommitted thresholds.
