# W33 Round 13: Gaussian mediator, certified phase strip, SO(10) transport, detector budget, chiral anomaly firewall

**19 October 2026.** Five independent research tracks. Read master after Pass398 and Passes12076–12080; rebased in isolated worktree, leaving the main checkout's local modifications untouched. Exact finite algebra, rigorous bound, literature-sourced device benchmark, and hypotheses are distinguished throughout.

## 1. A microscopic positive Gaussian mediator: exact interaction and no-go

Starting from 1440 rank-two two-qutrit projectors Q and their 17 stabilizer relation classes (previous Round10–12), introduce a stable Hermitian traceless matrix auxiliary boson X with m²>0 and a source J(w)=sum_a w_a(Q_a-2I/9). A concrete toy potential is

V[X,w]=(m²/2)Tr(X²)-g Tr(XJ).

Complete the square: X*=g J/m², so V_eff(w)=-(g²/2m²)Tr[J(w)²]. The induced pair coefficient is -(g²/m²)[Tr(Qa Qb)-4/9]; its sign follows from the stable auxiliary action rather than an arbitrary phenomenological choice.

All rank-two Q satisfy Tr[(Q-2I/9)²]=14/9. By convexity, Tr[J(w)²]<=14/9 on the probability simplex; the attractive interaction **favors pure concentrated vacua, not multi-vacuum condensates**. For the 17 fixed-reference orbit representatives, ordinary overlap Tr(Q0Q) distinguishes only 7 values, and adding quartic Tr(Q0QQ0Q) raises that to 9 signatures, still not all 17. The exact noncommutation norm follows 2(Tr(PQ)-Tr(PQPQ)); it is likewise not a complete class invariant.

This specified mediator has a NEGATIVE overlap coefficient but NOT the required W33 tick commutator coefficient. Vacua and ticks are distinct: Pass12072 disproved Clifford-equivariant tick-clock identification. No physical boson has been detected and no fundamental theory follows.

Producer: analysis/w33_20261019_round13_auxiliary_mediator.py; certificate in data.

## 2. Exact RATIONAL nonzero temperature interval of global-threshold failure

Round12 certified an explicit rational 7-tick state beating the singleton at T=1 and local two-tick threshold kappa_local(T)=-(3/2)(1-exp(-1/T))/(3+6exp(-1/T)). The strict partition-function rational margin was ~0.00921526251. Let Zlower be Round12's rational Taylor lower bound for the heptad partition function and m the rational strict comparison margin. Via log(1+x)>=x/(1+x), the true energy advantage E_single-E_heptad at T=1 exceeds m/Zlower≈0.00072182780336.

For finite 9-dimensional Gibbs systems, derivative dF/dT=-S and 0<=S<=ln9, so the difference of the two free energies varies at rate at most ln9<3. Differentiate the exact local critical coupling:

kappa_local'(T)=(3/2)exp(-1/T)/[T²(1+2exp(-1/T))²].

On T in [9999/10000,10001/10000], the derivative <2. The fixed rational heptad has C<4/7. Thus the entire energy difference changes by less than 1/10000*(3+2C)=0.000414175176, leaving positive guaranteed singleton-minus-heptad margin >0.00030765262735. ALL constants controlling the theorem are exact rationals; only the standard analytic entropy inequalities and simple exponential derivative are used.

**Theorem:** For every T from 0.9999 through 1.0001, at the TWO-TICK local threshold the seven-tick state has STRICTLY lower Gibbs+commutator energy than the singleton. This is an exact continuous temperature interval, NOT a numerical phase grid. The full 120-variable global transition curve remains unknown, and finite-d Gibbs mixtures have no thermodynamic singular transition.

Producer: analysis/w33_20261019_round13_rigorous_temperature_strip.py.

## 3. Transport all THREE 1+10+16 graded SO(10) sector projectors through the classical Albert cubic map

Parallel Pass12076 established three clock-related D5 SO(10) embeddings, each branching 27=1+10_i+16_i, with 10_i comprising two other singlets plus one octet and 16_i the remaining two octets. The E6/Cayley–Dickson 27-coordinate map from Round12 is the exact invertible T with det -4096.

For i=0,1,2 form coordinate projectors P1_i,P10_i,P16_i on the Cayley chart 3 singlets+3 octets, then transport them by T P T^-1 to first-Tits 3x3 trinification coordinates. Verify exact orthogonality, idempotence, identity resolution, ranks (1,10,16) for EACH i. Construct the U1 grading H_i=4P1_i-2P10_i+P16_i. All 89 canonical cubic monomials are U1-neutral, including all octonion trilinear terms and norm terms.

Build the exact order-three cyclic automorphism C of singlets and octets; transport D=T C T^-1 and verify D³=I and D H_i D^-1=H_(i+1). This is a concrete three-sector representation-and-cubic symmetry computation.

**Boundary:** We have NOT generated all forty roots of each SO(10) D5 nor shown the actual 120 E8 clock involutions act by these specific matrices. It is NOT an intertwiner between 120 Clifford ticks and 120 E8 clocks; Pass12072 forbids that equivariance. No physical family labeling or Yukawa masses determined.

Producer: analysis/w33_20261019_round13_so10_transport.py (all transported matrices in JSON).

## 4. SNSPD component benchmarks and an explicit hypothetical chip error budget

External device evidence:
- ACS Photonics 2025: https://pubs.acs.org/doi/10.1021/acsphotonics.5c00508 — a particular photon-number resolving superconducting detector reported approximately 98% system efficiency, 20 dark counts per second and 40 ps timing jitter.
- NIST / Optica 2020: https://www.nist.gov/publications/superconducting-nanowire-single-photon-detectors-98-system-detection-efficiency-1550-nm — another SNSPD achieved 98.0±0.5% efficiency near 1550 nm.

**NOT demonstrated by these sources:** An integrated 18-channel W33 photonic processor, equality of 18 detector channel efficiencies, coherent projector gates, or chip transmission. Those parameters remain unknown.

Design assumptions explicitly labeled: 18 detectors, 1 MHz pulses, 1 ns event gate, 98% individual detector efficiency, 20 cps per channel, assumed chip efficiency 2–60%, fringe visibility .9, uncalibrated contrast bias bound .02, independent drift floor σ=.01. For 810,000 source pulse/gate attempts, expected background from these component figures is 18×20 cps×1ns×810000=0.2916 gated dark events. Real free-running counts or longer gates differ. This is FAR below the intentionally harsh false-click replacement noise used in Round12 synthetic tests.

Use Round11 leading full-multinomial transfer estimator covariance σ=0.0057987 at 20,000 per setting, a conservative sqrt(2) paired signal-minus-null penalty, and 1/sqrt(collection efficiency) scaling. Minimum source pulses per setting to exceed a 5σ assumed margin are, respectively, about 29,404 for 2% chip, 5,881 for 10%, and a manually imposed 5,000 floor for chip 30%/60%. The predicted Z values are about 5.00,5.00,7.74,10.45. **These are engineering proxies, NOT experimentally substantiated significance.** Loss and mode-dependent Fisher information, detector dead time, pulse pile-up and calibration covariance still require measurements. An actual laboratory experiment is open.

Producer: analysis/w33_20261019_round13_photon_hardware_budget.py.

## 5. Chiral fermion mass protection: E6 27's exact anomaly ledger

Round12 showed the compact E7xSU2 (56,2) Weyl candidate is REAL and admits an invariant Majorana mass; anomaly cancellation alone does not protect chiral families.

Established GUT prior art: SO(10)'s complex 16 spinor has 16⊗16=10_s+120_a+126_s, with NO singlet; an unbroken SO(10) therefore forbids its bare Weyl mass, unlike 16⊗16bar, which contains a singlet. But isolated 16_1 under gauged SO(10)xU1 is anomalous: gravity-U1=16, cubic-U1=16 and SO10²U1 twice-index=2.

The complete E6 Weyl 27 branches as 16_1+10_(-2)+1_4. Verify exact anomaly cancellations:
- gravitational-U1: 16-20+4=0;
- U1³: 16-80+64=0;
- SO10²U1: 2*1+1*(-2)=0.

Also the SU5xU1χ spinor branching 16→10_(+1)+5bar_(-3)+1_(+5) cancels SU5³, SU5²U1χ, U1χ³ and gravitational-U1χ anomalies. The E6 cubic gauge-charge combinations 16·16·10 (1+1-2=0) and 10·10·1 (-2-2+4=0) are allowed. The full anomaly-safe 27 necessarily includes the 10 and singlet exotics; its multiplicity of three families, their masses after spontaneous breaking and compatibility with the chosen compact E7 gauge action are all OPEN.

Prior art: https://link.springer.com/article/10.1140/epjc/s10052-019-6878-1 and https://doi.org/10.1140/epjc/s10052-018-6388-6. New contribution here is an explicit reproducible constraint ledger, not original GUT representation theory.

Producer: analysis/w33_20261019_round13_chiral_anomaly_27.py.

## Reproducibility

Five producers and five corresponding JSON certificates in analysis/ and data/, plus tests/test_w33_20261019_round13.py. Respect the distinction between rigorous mathematical statements, numerics from conditional models, externally published component measurements and assumptions. **A parameter-free physical TOE, a full temperature critical curve, an experimental 8/27 measurement, a physical clock-to-tick bijection, and three protected observed families have not been derived.**
