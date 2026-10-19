# Five additional W33/TOE research frontiers (19 October 2026)

**Status:** exact finite-dimensional bounds, constructive conditional auxiliary-field model, synthetic optical witness, explicit Clifford/sl9 representation map, and provenance audit. **Not** a completed TOE or measured physics.

## 1. Stable auxiliary sector gives a *conditional* negative interaction

Let s_p=sum_k w_(p,k), sum_p s_p=1, and Ebar be the 540 unordered noncommuting projective Pauli pairs. Introduce 540 **postulated**, massive real bosons x_(p,q) with m²>0 and

\[
H_{\rm aux}=\sum_{\{p,q\}\in Ebar}
[\tfrac12m^2x_{pq}^2-g\sqrt{4/3}\sqrt{s_ps_q}\,x_{pq}].
\]

Exactly completing the Gaussian squares gives

\[
H_{\rm eff}=-\frac{g^2}{2m^2}\mathcal C(s),\qquad
\mathcal C(s)=\frac43\sum_{\{p,q\}\in Ebar}s_ps_q,\qquad
\boxed{\kappa=-g^2/(2m^2)<0}.
\]

This is stable on the simplex and at any positive auxiliary temperature (the Gaussian determinant is weight-independent). **Crucial caveat:** the edge-specific nonlinear source has been *engineered*, not derived from physical photons, fermions, Standard Model fields, or the bare Pass 12055 Hamiltonian. Demonstration of consistency is not a prediction of nature.

## 2. Rigorous global negative-coupling region, all 120 rates

For 120 nonnegative weights w_a summing to one, Q=sum_a w_a P_a has 0<=Q<=I and Tr Q=3. Let beta=1/T, T>0, and F_*=-T log(3+6e^-beta) (single tick). Since x-x^n >= x(1-x) for x in [0,1], n>=2, the exponential series implies

\[
e^{\beta x}\le1+(e^\beta-1)x-(e^\beta-1-\beta)x(1-x).
\]

Summing across the nine eigenvalues of Q yields

\[
Z_*-Z\ge[1-(1+\beta)e^{-\beta}](3-\mathrm{Tr}Q^2).
\]

By the exact W33 projector-overlap census, 3-Tr Q² >=3*C(w). Finally -log x>=1-x implies

\[
\boxed{F_T(w)-F_*\ge a(T)\mathcal C(w)},\qquad
a(T)=\frac{3T[1-(1+1/T)e^{-1/T}]}{3+6e^{-1/T}}>0.
\]

Thus **for every T>0 and every 120-variable nonnegative simplex configuration**, if kappa >= -a(T), a single tick is a **certified global minimizer** of F_T+kappa*C. This is a sufficient, not necessary, condition. Sample sufficient lower coupling boundaries: T=.2: -0.189363; T=.5: -0.233733; T=1: -0.152234; T=2: -0.081520. Previous local instability at T=1 is -0.182088, so the rigorous global region remains smaller than the local-stability region.

Additionally, 4-start SLSQP over **all 120 independent rates** (not merely 40 outcome-restricted rates) at (T,kappa)=(.5,-.6),(1,-.3),(1,-.15) finds supports of size 7,7,1 respectively. These numerical optima are NOT global certificates.

## 3. Explicit gate route and synthetic noise controls

Let P=|0><0| tensor I_3, F=F_3 tensor I_3, CZ|a,b>=omega^(ab)|a,b>, G=CZ*F and Q=GPG†; choose commuting null R=I_3 tensor |0><0|. Their pairwise overlaps are **identical** (Tr PQ=Tr PR=1), while the squared commutators are 4/3 and zero. The exact normalized four-pulse echo deficit at theta=pi/2 is 8/27 for P,Q and zero for P,R.

Controlled exp(i theta Q) is compiled as *unconditional G*, a **controlled local |0>-phase**, and unconditional G†. Four controlled phase operations plus ancillary interferometry produce the trace witness; coherent gate compilation, not real optical hardware, was tested.

A synthetic binomial experiment with independent per-gate leakage 1%, ancilla visibility 95%, and ancilla bit-flip 1% has model visibility 0.894315, expected contrast 0.264982 and conservative Hoeffding shot count **1,998 per condition**. Across 4,000 independently generated synthetic repeats, the preselected threshold detected all synthetic signals and no synthetic shams. This does not assess coherent leakage, correlations, real hardware drift, or a built experiment. Experimental OTOC interferometry has substantial prior art (https://journals.aps.org/prxquantum/abstract/10.1103/PRXQuantum.5.010201).

## 4. Explicit Clifford-equivariant 80D operator-to-sl9 map

Define B_(p,1)=P_(p,0)-P_(p,1), B_(p,2)=P_(p,0)-P_(p,2) for the forty Pauli projective directions; these are an explicit real basis of Hermitian traceless 9x9 operators. Their per-point Gram matrix has inverse [[2,-1],[-1,2]]/9. The map Phi(c)=sum c_(p,j) B_(p,j) and the 80x80 real Clifford actions obtained by conjugating the basis obey

\[
\Phi(\rho_{80}(g)c)=U_g\Phi(c)U_g^\dagger
\]

on five explicit Clifford generators: one-qutrit Fourier, phase, controlled-Z, controlled-SUM, and SWAP. Maximum equivariance residual ~2e-14; Pauli-translation character -1. The Lambda³(C9) sector has dimension 84 and passed unitary and composition checks to ~2e-15.

Because the **standard** E8 A8 model decomposes as sl9+Lambda³9+Lambda⁶9 (dimensions 80+84+84), this constructs a concrete equivariant identification with the **sl9 sector** of that model. It is **not yet** a coordinate intertwiner to the repo's explicit E8 Chevalley basis, nor a proof of all exceptional mixed brackets. Its 80+84+84 prior art is in the existing W33 temporal SU9/E8 compiler.

## 5. Paper reference repair and operational falsifiability boundary

The previous Forty Points audit reported 23 aliases not resolved by a shallow path search. A second pass checked all tracked paths and commit histories in **both** W33 and Holotrade local repositories, resolving **19 to commits and 2 to source paths**. The two remaining filenames are frame_chirality_is_reversed_only_by_antiunitaries.py and w33_20261001_three_qutrit_fidelity_flag.py; neither was silently replaced. Locating a commit is NOT equivalent to proving what a citation says.

A complete two-qutrit gate-model test evaluated **all 780** unordered pairs of forty projective Pauli directions: exactly **240 commuting nulls** and **540 noncommuting echoes of 8/27** at calibrated theta=pi/2. Max floating-point residual 7.8e-16. This 240:540 / 0:8/27 law can falsify a *device-level* implementation, but is already predicted by ordinary two-qutrit quantum mechanics and **cannot independently test the user's proposed TOE**.

## Reproducibility

- analysis/w33_20261019_nextfive_gaussian_phase.py and data/w33_20261019_nextfive_gaussian_phase.json
- analysis/w33_20261019_nextfive_optics_su9.py and data/w33_20261019_nextfive_optics_su9.json
- analysis/w33_20261019_nextfive_evidence_prediction.py and data/w33_20261019_nextfive_evidence_prediction.json
- tests/test_w33_20261019_nextfive.py

**Physics firewall:** neither a naturally selected coupling, a unique physical E8 embedding, an actual optical device, a fully classified negative-kappa global phase diagram, nor a novel parameter-free TOE prediction has been obtained.


## Bonus: exact intrinsic fourth-order W33 incidence and sign

For two distinct projective Pauli directions and *positive rates* a,b, let P and Q be their rank-three eigenspace projectors. If they commute, the eigenvalues of aP+bQ are {a+b:1,a:2,b:2,0:4}. If they do not commute, the isoclinic rule PQP=P/3 gives eigenvalues {(a+b+sqrt((a-b)^2+4ab/3))/2:3,(a+b-sqrt((a-b)^2+4ab/3))/2:3,0:3}. The first three power traces agree, but the fourth differs:

\[
\operatorname{Tr}(aP+bQ_{\rm commute})^4-
\operatorname{Tr}(aP+bQ_{\rm noncommute})^4=\frac43a^2b^2.
\]

Indeed every cyclic mixed word reduces to r alternating PQ blocks: commuting pairs have trace 1; noncommuting pairs have trace 3^(1-r). Coefficients of the exponential Taylor series are nonnegative, and words with r>=2 are strictly lower for noncommuting pairs. Therefore for **any a,b>0,T>0**, the bare two-tick Gibbs free energy is strictly *lower* for commuting than noncommuting directions, not just at high temperature. For a+b=1, the large-T asymptotic is

\[
F_{\rm noncommute}-F_{\rm commute}
=\frac{a^2b^2}{162T^3}+O(T^{-4})>0.
\]

This sharpens the prior quadratic-order no-go: **W33 incidence is generated intrinsically at fourth order**, but its two-projector sign favors compatibility and does NOT derive the negative commutator coupling sought for a heptad phase. Reproduction: analysis/w33_20261019_nextfive_quartic_incidence.py → data/w33_20261019_nextfive_quartic_incidence.json.


### Further group-lift caveat for the SU9 model

The 84-dimensional exterior-cube composition test is functorial for arbitrary GL9 matrices. Promoting it to a **full E8 Lie-algebra automorphism** requires determinant-one representatives, compatible central phases, and preservation of the mixed brackets among sl9, Lambda3 and Lambda6. The current test does **not** check those E8 brackets or the Clifford central-extension cocycle; it establishes only the adjoint sl9 intertwiner and the independent exterior-cube functor test. No equivalence with a particular repository Chevalley basis is asserted.
