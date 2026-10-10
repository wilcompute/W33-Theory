# TOE44 — Five independent fronts: sharp product-SIC bound, noisy W33 MUB, injected E6 CCZ, channel no-go, and CP-phase firewall

**10 October 2026.** This packet follows TOE43 and the Pass11884–11886 SU(9)/84 radiative-Higgs parallel result. It contains **theorems within a finite two-qutrit model, an exact ternary circuit identity, reproducible Monte Carlo, and an explicit EFT/CP limitation**. It does **not** certify an arbitrary-state SIC nonexistence theorem, functioning physical photonic hardware, unique CPTP identification, or a complete E8/SM radiative vacuum.

## Parallel commit and prior-art audit

Compared GitHub master to the TOE43 baseline (commit 73798484c) before changes. The sole new parallel commit at the start of TOE44 was Pass398's formula-search-universe ledger refresh (f34a203e). Pass11884–11886, already merged during TOE43, provides a gauge-vector and scalar-sector Coleman–Weinberg analysis for the Vinberg Cartan of SU(9)+84. It **anticipates the vector-only Witting value -6 log 3** and claims numerical Witting-ray selection; no duplicate claim is made here. TOE44 consulted the old native signed E6 45-triad source, TOE42's certified 520 parallelisms, TOE43's field9 SIC numerical candidate, explicit MUB and noise producers, and the 84 Higgs papers. Existing dirty repo files were not edited.

## 1. Sharp no-go for **pure product** elementary-abelian SICs

Producer: analysis/w33_20261010_toe44_product_sic_bound.py
Certificate: data/w33_20261010_toe44_product_sic_bound.json

Define the 40 projective two-qutrit Pauli powers \(q_p=2|\langle\psi|W_p|\psi\rangle|^2\). For a **pure product** \(\psi=a\otimes b\), let \(u_i=2|\langle a|W_i|a\rangle|^2\) and \(v_j=2|\langle b|W_j|b\rangle|^2\), indexed by the four projective single-qutrit Pauli classes each.

The 40 projective two-qutrit classes separate exactly into 4 A-local, 4 B-local, and 32 correlated classes. For every pair (i,j) there are two correlated projective Paulis, each with power \(u_iv_j/2\). Single-qutrit Parseval gives \(\sum_i u_i=\sum_jv_j=2\).

With \(U=\sum_i u_i^2\), \(V=\sum_jv_j^2\), Cauchy–Schwarz yields \(U,V\ge1\). Thus

\[
\sum_{p=1}^{40}q_p^2=U+V+\frac12 UV\ge\frac52,
\qquad
\boxed{\operatorname{Var}_{90\ \mathrm{frames}}\mathcal P_L
=\frac{\sum q_p^2-8/5}{135}\ge\frac1{150}.}
\]

The inequality is **sharp**. Let each local state be the Hesse fiducial \((0,1,-1)/\sqrt2\); its four single-qutrit Pauli powers all equal 1/2. Their tensor product attains variance exactly 1/150. Three hundred seeded random pure products passed the bound, and the 48-start TOE43 unrestricted numeric candidate had variance 0.00131687, less than 1/150, proving the nonconvex numerical optimizer has escaped the product sector.

**Consequence:** any \(\mathbb F_3^4\) two-qutrit Pauli-covariant SIC fiducial (if one exists) **must be entangled**. This is a rigorous *restricted* no-go, **not** proof that such SICs exist or do not exist for entangled states. The familiar cyclic \(\mathbb Z_9^2\) dimension-nine SICs do not automatically settle the elementary-abelian group case.

## 2. Ten-setting W33 purity test with basis-dependent SPAM and losses

Producer: analysis/w33_20261010_toe44_mub_spam.py
Certificate: data/w33_20261010_toe44_mub_spam.json

Independently enumerate the 40 W33 isotropic lines and construct an **exact ten-line symplectic spread containing the computational Z1,Z2 stabilizer line**. All 40 projective Paulis appear exactly once. Use the corresponding ten mutually unbiased bases, which form a projective 2-design.

Test the input \(\rho=\eta|00\rangle\langle00|+(1-\eta)I/9\), \(\eta=.62\). Its purity is \(P=(1+8\eta^2)/9=.4528\). In the computational basis its pair-outcome collision probability is \(c_0=\eta^2+(1-\eta^2)/9\); in the other nine MUBs it is 1/9. Hence \(\sum_b c_b=1+P\) exactly.

Each setting has its **own** symmetric nine-outcome confusion \(\epsilon_b\) from 5% to 13.5%, and per-copy loss from 4% to 24%. Only independently surviving two-copy pairs count. With \(m=900\) attempted *pairs* per basis, 2,400 seeded independent assay repetitions, measured pair collisions \(h_b\), and \(n_b\) valid pairs, use

\[
\widehat P=\sum_{b=1}^{10}\frac{h_b-\big[1-(1-\epsilon_b)^2\big]/9}
{(1-\epsilon_b)^2}-1,
\quad
\mathrm{Var}(\widehat P\mid n_b)=
\sum_b\frac{c_b^{\rm obs}(1-c_b^{\rm obs})}
{n_b(1-\epsilon_b)^4}.
\]

The frozen run gave estimated mean **0.4538078613**, true 0.4528, uncalibrated bias **-0.0324445874**, predicted conditional standard error roughly **0.0500**, and **95.958%** empirical nominal-95% Gaussian confidence coverage.

**Boundary:** Noise is **trusted and basis-dependent but symmetric**, loss is independent of the observed outcome, and calibration is assumed exact. We do not yet model asymmetric confusion, state drift, photon loss conditional on output mode or SPAM confidence calibration. The traditional MUB 2-design purity estimator is prior art; the concrete W33-spread/SPAM control packet is the implementation here.

## 3. Exact 45-term native E6 CCZ synthesis with **magic-state injection**

Producer: analysis/w33_20261010_toe44_exact_ccz_7R.py
Certificate: data/w33_20261010_toe44_ternary_ccz_compiler.json

Let \(a,b,c\in\mathbb F_3\), \(f(x)=[x]_3^3\bmod9\), \(\zeta_9=\exp(2\pi i/9)\), \(\omega=\zeta_9^3\), and the genuinely non-Clifford **single-qutrit** gate \(R|x\rangle=\zeta_9^{f(x)}|x\rangle\) = diag\((1,\zeta_9,\zeta_9^{-1})\). Clifford SUM maps \((a,b)\mapsto(a,a+b\bmod3)\).

The **exact integer identity modulo 9**

\[
f(a+b+c)-f(a+b)-f(a+c)-f(b+c)+f(a)+f(b)+f(c)\equiv6abc
\]

therefore implements each cubic three-qutrit phase \(\mathrm{CCZ}^s|abc\rangle=\omega^{sabc}|abc\rangle\), \(s=\pm1\), by computing seven nonempty subset sums, applying **seven \(R^{\pm1}\)** gates, and uncomputing:

**Per signed CCZ:** 7 R gates + 10 Clifford SUM gates, no persistent logical ancilla. Verified exactly on **all 27 three-qutrit computational basis states** for **both** signs. Each gate restores all input trits. Applied to the repository's **actual 45 signed E6 triads** (22 positive, 23 negative), not a substitute cubic.

An explicit **deterministic ideal gate-teleportation/injection** for each R^k was also proved on **all nine (input x, measurement m) pairs** for each \(k=\pm1\):

1. Prepare \(|M_k\rangle=R^{-k}|+\rangle\) on a fresh qutrit, \(|+\rangle=3^{-1/2}\sum_y|y\rangle\).
2. Apply Clifford SUM from data to the magic ancilla.
3. Measure ancilla in computational Z; outcome \(m=0,1,2\) occurs with probability 1/3, independently of the data.
4. Apply the **outcome-dependent diagonal qutrit Clifford** \(C_{m,k}\), with phase exponent \(\omega^{-q_{m,k}(x)}\), where
\[
q_{m,k}(x)=\frac{-k f(m-x)-k f(x)+k f(m)}3\bmod3.
\]
The numerator is divisible by 3 for all x,m and \(q_{m,k}\) is quadratic mod3 (so the correction is Clifford). Conditioned on measurement, the data experiences exactly \(R^k\) up to a global phase. All correction tables are frozen.

**Full 45-gate packet, unoptimized:**
- **315** non-Clifford magic states \(|M_{\pm1}\rangle\), consumed once each;
- **450** direct Clifford SUM gates implementing seven subset phases;
- **315** additional Clifford SUM gates for injections (**765 SUM total**);
- **315** ancilla Z measurements + **315** conditional diagonal Clifford corrections;
- ideal abstract pre-injection primitive depth **85** if the 45 triples remain in five groups of nine disjoint triples, excluding measurement latency and injection depth.

This is an **exact algebraic gate compilation with explicit magic consumption**, not evidence that the machine can distill clean magic states in a photonic channel, nor a demonstrated leakage, logical threshold or loss budget.

## 4. Rigorous CPTP channel-identification no-go for phase-free W33 powers

Producer: analysis/w33_20261010_toe44_channel_identifiability.py
Certificate: data/w33_20261010_toe44_channel_identifiability.json

Let \(0<\eta<1\) and \(U=\mathrm{diag}(1,1,-1,1,\ldots,1)\). Define two explicit CPTP channels

\[
\mathcal E_0(\rho)=\eta\rho+(1-\eta)I/9,\quad
\mathcal E_1(\rho)=\eta U\rho U^\dagger+(1-\eta)I/9.
\]

At the first input \(|00\rangle\), both outputs are **exactly identical**, proving no set of measurements on a **single fixed input** can identify the channel.

At the *second* input \(|\phi_+\rangle=(|01\rangle+|02\rangle)/\sqrt2\), the channels differ by **trace distance \(\eta=.63\)**: the unitary converts \(|\phi_+\rangle\) to the orthogonal \(|\phi_-\rangle\).

**Stronger result:** for this pair of probe inputs, all **40 projective W33 Pauli powers** \(q_p=2|\mathrm{Tr}(\rho W_p)|^2\) are *identical* for the two channels — consequently all W33 \(-4\) projector amplitudes, variances and arbitrary higher **polynomials in the Pauli powers** are also identical, even though the second output states are distinct. At that second probe, the complex Pauli expectation vectors differ by 0.63 in at least one component.

**Boundary:** This is a no-go against trying to identify *general channels* from phase-discarding power statistics of too few input probes. It does not prohibit standard informationally complete process tomography using enough well-chosen inputs and full complex Pauli expectation values, nor does it negate the TOE43 observation that many noise families have distinct \(-4\) norms.

## 5. E8 Higgs/Siegel CP-phase redundancy — exact effective-field-theory firewall

Producer: analysis/w33_20261010_toe44_e8_cp_cw_firewall.py
Certificate: data/w33_20261010_toe44_e8_cp_phase_firewall.json

The parallel Pass11879–11886 programme identifies degree-12 holomorphic invariant \(I_{12}(x)\), a potential Higgs phase and a one-loop Witting-ray selection. The correct CP assessment must distinguish **a nonzero complex parameter from a physically non-removable phase**.

Suppose the full scalar-only CP-even renormalizable potential \(V_0\) depends only on Hermitian contractions of one 84 field \(x\), and only **one** additional complex coupling \(\kappa_{12}I_{12}(x)+{\rm c.c.}\) is supplied, where \(I_{12}\) has a real-coefficient tensor in an appropriate CP convention. Because \(I_{12}(e^{i\theta}x)=e^{12i\theta}I_{12}(x)\), a **field-basis redefinition** removes \(\arg\kappa_{12}\) exactly. Equivalently a generalized CP conjugation \(x\mapsto e^{i\delta}x^*\) with \(\delta=-2\arg\kappa_{12}/12\) leaves the potential invariant. Verified for 30 random phases to residual \(<8\times10^{-15}\).

**Therefore a lone complex degree-12 coefficient is not, by itself, an explicit CP-violating observable.** The potential could still support **spontaneously** CP-breaking minima, which must be tested separately; and additional Yukawas can fix a phase convention.

With **both** independent terms \(\kappa_{12}I_{12}+\kappa_{18}I_{18}+\mathrm{c.c.}\), the rephasing-invariant relative coefficient datum is

\[
\arg(\kappa_{12}^{\,3}/\kappa_{18}^{\,2})=3\arg\kappa_{12}-2\arg\kappa_{18}.
\]

Within the explicitly assumed canonical real-polynomial CP convention, CP compatibility requires this angle to vanish mod \(\pi\). Two test choices produce CP-symmetric residual \(<6\times10^{-15}\) and incompatible CP residual **at least 0.216** over all twelve possible degree-12 CP branches. These are precise **scalar phase-sector tests**, not a Standard Model Jarlskog invariant.

**Complete one-loop field-theory calculation cannot be certified from the available parameters.** The preceding TOE43 independently computed vector-only spectra. The parallel Pass11884–11886 provides additional moment-map scalar-loop results, but **the fermionic representation/Yukawa mass matrices and renormalization prescriptions required for a full physical supertrace have not been fixed**. As a demonstration of missing physical input, TOE44's *explicitly hypothetical, not consistency-claimed* aligned-fermion spectrum can reverse the sign of vector-only shape selection by choosing its Yukawa strength. That toy model is a sensitivity control, not a discovered spectrum or counterexample to a fully specified gauge theory.

The relative phase of couplings, positive physical Hessians, gauge parameter via Nielsen identities, spontaneous CP, chirality, anomaly cancellation and particle masses remain open. The actual gauge/renormalization restrictions matter; see Nielsen (1975), doi:10.1016/0550-3213(75)90301-6, and Nielsen (2022), Phys. Rev. D 105, 093011.

## Reproduce

```bash
py -3 -m pytest -q tests/test_w33_20261010_toe44_five_fronts.py
```

The five producers and six focused tests regenerate exact integer checks, seeded Monte Carlo, and saved machine-readable certificates. TOE44 only stages its own newly named files; concurrent dirty research is preserved.

## Five strongest **independent** next steps

1. **Extend the SIC proof beyond products:** Test Schmidt-rank-2 subvarieties and exact rank-one polynomial elimination; attempt a global sum-of-squares lower bound for all entangled \(\mathbb F_3^4\) fiducials without conflating cyclic dimension-nine SICs.
2. **Calibrate a real ten-basis device:** Implement general nine-by-nine outcome confusion matrices, state-dependent loss, drift, tomography confidence intervals and a complete photon budget with representative hardware data.
3. **Make magic distillation explicit:** Choose a supported physical R gate platform, specify noisy \(|M_k\rangle\) production/injection, and rigorously propagate coherent and stochastic errors through all 315 injections and 765 SUMs to a logical fidelity threshold.
4. **Derive a minimum process-tomography design:** Determine the smallest input probe family and exact phase-bearing two-qutrit Pauli measurements needed to distinguish physically motivated W33 channel families under noise.
5. **Fix a full E8 matter action:** Supply fermion irreps, Yukawas, gauge fixing, scalar Hessian, anomalies and RG renormalization, then calculate the complete one-loop potential, phase vacuum, CP-odd invariants, masses and positive fluctuation spectrum.
