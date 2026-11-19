# Five physics interfaces beyond E8 linked-wire topology

**2026-11-18.** Reproducible mathematical and conditional model checks. This does not establish a TOE, a global G2 compactification, physical fermion chirality or experimental quantum memory.

## Intake and prior art

At intake GitHub and authorized local TheHeavyCrown master were both a3ec818a3487952698fd18e06bbdaf2ae9ede6ec, staging empty, with 19 preexisting tracked modifications owned by parallel workflows. We inspected the previous full-248 E8 LES/Psi weak-G2/MUB report and the relevant portions of the harmonic PW tilted localizer. Prior work already established E8's (E6 x SU3)/Z3 global center, order-nine SU3 Clifford linked-wire holonomy, matter/conjugate relative Betti (81,0) in each, E6 gauge centralizer dimension14 after a Psi Wilson phase, and the four qutrit MUB entanglement dimensionality witness.

Outside references reviewed before developing the calculations:
- Acharya and Witten, Chiral Fermions from Manifolds of G2 Holonomy, https://arxiv.org/abs/hep-th/0109152 ; singular G2 spaces, charged chirality
- Bilal and Metzger, Anomalies in M-theory on singular G2-manifolds, https://arxiv.org/abs/hep-th/0303243 ; local anomaly cancellation
- Witten, Anomaly Cancellation on Manifolds of G2 Holonomy, https://arxiv.org/abs/hep-th/0108165 ; bulk inflow
- M2/AdS4 flux quantization review, https://academic.oup.com/ptep/article/2020/11/11B102/5875990
- Smooth domain wall fermion zero modes, https://academic.oup.com/ptep/article/2025/2/023A01/7920790
- Beyer et al (2026), Observation of Genuine Multi-Time Quantum Memory, https://arxiv.org/abs/2611.17268
- A Guide to Higher-Order Quantum Operations, https://journals.aps.org/prxquantum/abstract/10.1103/92c4-g7qs

## Front I. Conjugate cohomology versus physical chiral spinors

Earlier E8 cochain results establish equality of conjugate local-system Betti numbers with the SAME relative boundary. This says nothing decisive about the left/right decomposition of a real higher-dimensional spinor. To isolate exactly what is missing, consider a minimal effective Jackiw-Rebbi domain-wall pair for mu>0:

    D_plus = d/dx + mu tanh(x),
    D_minus = -d/dx + mu tanh(x).

D_plus has exactly one normalizable zero mode sech(x)^mu; the formal D_minus zero mode cosh(x)^mu diverges. Exact normalization:

    integral_R sech(x)^(2mu) dx = sqrt(pi) Gamma(mu)/Gamma(mu+1/2).

The producer verifies this for mu=1,2,3,4,5. Reversing the mass m(x) -> -m(x) flips the index +1 to -1. Three positive-kink channels have index3 if THREE channels are put in; three reversed channels have -3, and the formal direct sum has net0. The number three is inserted, not predicted.

An E8 248 real representation may produce left Weyl fields with right-conjugate CPT partners without adding three unwanted propagating opposite-handed mirror fields. The 7D spinor charged Dirac operator, APS/domain boundary constraints, C/Majorana conditions, eta invariant and local anomaly inflow are required before an actual chiral spectrum can be claimed. The 1D kink is only a constructive toy for this distinction.

## Front II. E6 27 native anomaly cancellation does not cancel gauged SU3-family anomaly

The complete E6 fundamental branches as 27=16_1+10_-2+1_4 under SO10 x U1Psi. Exact charge sums:

    Tr Psi =16*1+10*(-2)+1*4=0,
    Tr Psi^3 =16*1^3+10*(-2)^3+1*4^3=0.

The SU5 cubic anomaly contributions from 16 -> 10+5bar+1 and vector10 ->5+5bar are +1,-1,+1,-1, summing zero. Complete E6 multiplets are substantially better behaved than retaining only an adjoint chiral 16_-3 under an extra U1Psi.

But if the family SU3 is genuinely gauged, one left-handed (27,3) has 27 fundamental SU3 triplets. In A(3)=1 normalization,

    A_SU3family_cubed(27,3)=+27,
    A_SU3family_cubed(27bar,3bar)=-27.

The pair cancels this continuous anomaly only when counted as independent left-handed Weyl representations. To retain just the desired one, derive actual local inflow, additional anomaly-canceling matter or a different gauge structure. Gauging ONLY finite H27 requires a separate discrete/global anomaly analysis; SU3 anomaly +27 cannot be blindly transferred to H27.

The Acharya-Witten and Bilal-Metzger references emphasize local anomalies at individual G2 singularities, not just a global family count. Nothing here calculates a real anomaly-inflow coefficient.

## Front III. Quantized M2 flux: a scale that W33 topology alone cannot choose

For the actual round S7 classical Freund-Rubin AdS4 control,

    R_S7=2L, F4=(3/L)vol_AdS4, Vol(S7_R)=pi^4 R^7/3.

Using the standard unquotiented charge convention,

    N=[1/(2*pi*l_p)^6] integral_S7 (*F4)
     =2 L^6/(pi^2*l_p^6) integer.

Hence

    R_S7/l_p=(32*pi^2*N)^(1/6),
    L/l_p=(pi^2*N/2)^(1/6).

With the PREVIOUS restricted nearly-parallel G2 Ricci matching abs(tau0)=2/L, the necessary torsion magnitude obeys

    abs(tau0)*l_p=2/(pi^2*N/2)^(1/6).

The data certificate explicitly evaluates N=1,10,81,100,240,10000,1000000. A deliberately skeptical sanity check: N=81 gives R/l_p about5.4282; N=240 gives R/l_p about6.5054. Neither number is derived from W33 as actual flux or proves a controlled classical approximation. One needs a physical compactification with a defined closed 7-cycle, a quantized Page charge, sources and actual volume. Sixth-root N growth makes large curvature radii a nontrivial input. Do not confuse this round-S7 result with a solved singular G2 or E8 background.

## Front IV. Strong intrinsic qutrit entanglement at two times CAN be entirely Markovian

Earlier four local qutrit MUB measurements test P_match=(1+3F_Phi3)/4. States with Schmidt number at most2 must satisfy F<=2/3, hence P_match<=3/4. A positive result verifies a genuinely three-dimensional reference-memory entanglement resource. It does not test whether the whole multitime process has intrinsic quantum memory.

Construct an explicit two-interval qutrit process where each step has a fresh independent environment and channel

    Delta_t(rho)=t rho+(1-t)Tr(rho) I3/3, t=9/10.

The composition is exactly Delta_(t^2). A deterministic complex random-density matrix test verifies the equality for 12 samples to machine accuracy. The corresponding intervention-sensitive process tensor is Markovian by construction: the environment is refreshed independently after each step.

Nevertheless the normalized Choi state for ONE interval has F1=(1+8t)/9=41/45, and for the TWO-interval channel F2=(1+8t^2)/9=187/225. Both exceed2/3. The ideal four-MUB match probabilities are P1=14/15 and P2=131/150, both above3/4. Thus even winning the intrinsic-qutrit dimension witness repeatedly at different time separations says nothing by itself about genuine three-time quantum memory.

A proper follow-up must introduce calibrated mid-time interventions and reject every globally compatible classical-memory process, as in the genuinely multi-time work of Beyer et al. Process-tensor tomography or a newly derived qutrit-specific witness is still needed.

## Front V. A tempting compensating gauge charge rescues quartic PW symmetry but fails three-family selection

Previous quartic harmonic PW localizer f_n includes Re(w^(n+1)), with n index-one Morse points for adequate tilt, and the geometrical C3 rotation w -> omega*w makes the quartic n=3 monomial non-invariant.

Conditional outside-box repair: instead use a COMPLEX holomorphic field Phi_n(w)=w^(n+1) and let the same simultaneous geometric+internal C3 action include a gauge line character omega^q. Combined invariance is equivalent to

    n+1+q=0 mod3.

For quartic n=3, this requires q=2, the center character of the H27 SU3 family antitriplet in the conventional E8 global subgroup embedding (the triplet has q=1).

But q=2 admits n=3,6,9,12,..., and therefore does NOT uniquely predict three families. The code exhaustively verifies n2..n14. More importantly, no physical argument has yet IDENTIFIED the internal E8 center as a geometric rotation, supplied a global complex E8-valued Higgs section, or made the previous real harmonic Re(w^4) with linear tilt transform as required. This conditional symmetry repair is not evidence that the conjugate sector is physically preferred.

## Summary and next independent physics tests

The five mathematical checks are reproducible and sharpen four barriers: a legitimate 7D chirality problem rather than a Betti-number projection, local family anomalies even for complete E6 27s, independent quantized gravity flux and radius, and multitime quantum-memory criteria stronger than even two distinct Schmidt-number-three checks. They also show that compensating H27 center phases select n only modulo3.

Best independent next investigations: derive a charged G2/ADE fermion index and valid boundary domain; construct local anomaly inflow and a global E8 Higgs respecting the shared center; solve quantized 11D flux/sources with a physical large-radius spectrum; derive n=3 dynamically from equations rather than equivariant residues; and devise an intervention-sensitive intrinsically qutrit three-time witness that rejects the explicitly constructed Markov counterexample.

## Reproducibility

New unique files:
- analysis/toe_20261118_chirality_anomaly_FRflux_Markov_equivariant.py
- data/toe_20261118_chirality_anomaly_FRflux_Markov_equivariant.json
- tests/test_toe_20261118_chirality_anomaly_FRflux_Markov_equivariant.py
- analysis/2026-11-18_chiral_Dirac_27_anomalies_FRflux_Markov_qutrit_equivariance.md

Run the producer with python followed by python -m unittest discover -s tests -p test_toe_20261118_chirality_anomaly_FRflux_Markov_equivariant.py -v. Stage ONLY these four owned files, using git add -f for the gitignored data JSON. Preserve every unrelated dirty change from parallel work.
