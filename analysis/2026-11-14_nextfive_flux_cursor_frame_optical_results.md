# Five further TOE research fronts — covariance, unequal quantized flux, autonomous H27, apartment fluctuations, detector-level photonics

**Research date:** 2026-11-14 (Eastern). **Status:** exact finite combinatorics and conditional classical Einstein–Maxwell theorems; independently checked numerical and detector-model simulations. **Not** a derivation of a complete theory of everything.

**Owned artifacts**
- \`analysis/toe_20261114_nextfive_f8_flux_cursor_frame_optical.py\`
- \`data/toe_20261114_five_full_fronts_exact_controls.json\`
- \`tests/test_toe_20261114_nextfive_exact_controls.py\`
- This report.

**Previous parent:** \`056c4fc9f348\`; the prior F8 two-copy PPT counterexample, the homogeneous AdS5 x S2 x S2 background, and the 27-state H27 four-pulse clock were already derived there. This pass *extends* rather than resets them. Concurrent GitHub commits must be checked before priority claims. Existing local dirty/staged work was not modified.

## 1. F8 global lower-bound front — the exact zero-PPT state passes every diagonal Pauli-covariance positivity test

The project has nine mutually unbiased Pauli classes in dimension d=64, covering 567 nonidentity Pauli labels, and exact algebraic **upper witness** \`c8 <= (47-32cos(2pi/9))/9 ~= 2.498508646688...\`. An exact global **matching lower** is not established. The prior symmetric PPT two-copy state \`rho2\` has \`Tr(rho2 K)=0\`, \`K=sum_{P covered}P tensor P\`, despite all product-pure states having nonnegative \`c8\`. This proves that PPT+swap-symmetry alone cannot certify a positive global bound, *not* that the PPT optimum equals zero.

Here we independently computed \`Tr(rho2 P tensor P)\` for **every one of the 4096 Hermitian Pauli labels**, including the phase factor \`(-1)^{u dot z}\` required when the Pauli has an odd number of Y factors. Exact rational Walsh transform gives:

| Pauli class | Count | Exact two-copy diagonal correlation |
|---|---:|---:|
| Identity | 1 | 1 |
| Covered | 567 | 0 |
| Uncovered, even binary Pauli parity | 1512 | 31/1512 |
| Uncovered, odd binary Pauli parity | 2016 | 1/63 |

The traceless Pauli correlation sum is \`1512*(31/1512)+2016*(1/63)=63\`, agreeing with the exact bosonic swap expectation identity \`sum_all Tr(rho2 P tensor P)=d Tr(rho2 Swap)=64\`.

The state is invariant under simultaneous Pauli conjugations, so its two-point Pauli covariance tensor is diagonal. **Every diagonal covariance eigenvalue is nonnegative**, including all the 2016 odd-parity directions (the complex Hermitian-Pauli phase is essential to get their sign right).

**Falsification:** A covariance-PSD filter, in addition to swap symmetry and PPT, does *not* remove this counterexample. The promising attack requires genuinely non-Gaussian/three-copy exchangeability constraints or pure-state polynomial identities. A 3-copy extension was **not** constructed or ruled out here, and the repo's stronger PPT/SOS bounds with additional constraints are not refuted.

**Independent literature:** Doherty, Parrilo, Spedalieri (2004), *Complete family of separability criteria*, https://doi.org/10.1103/PhysRevA.69.022308 ; associated SOS/sphere bounds https://doi.org/10.1007/s10107-020-01537-7 . These hierarchies are prior established methods, not a theorem proved by our F8 numerical code.

## 2. Coupled-compactification front — solve *all positive unequal integer charge ratios* in D=9 classical Einstein–Maxwell

**Assumptions:** nine-dimensional action \`S=int sqrt(-g)(R-F^2/4)\`, zero bare cosmological term, unwarped \`AdS5 x S2(r1) x S2(r2)\`, one abelian closed/co-closed 2-form \`F=f1 vol1 + f2 vol2\`, nonzero quantized magnetic charges \`N1,N2\`, common fixed electric charge e, and \`int_{S2_i}F=2pi N_i/e\`. Orthornormal magnetic fields are \`fi=Ni/(2e ri^2)\`.

Let \`t=r1^2/r2^2>0\`. The internal nine-dimensional Einstein equations, including the two flux stress terms, reduce **exactly** to

\`(N1/N2)^2 = t^2(t+6)/(6t+1)\`, with derivative \`3t(4t^2+13t+4)/(6t+1)^2>0\`.

The function increases from zero to infinity. **Thus every positive rational charge ratio, including all positive integer pairings, has exactly one positive-radius solution** on this product ansatz:

\`r2^2 = 5*N2^2*t/[8*e^2*(6t+1)]\`; \`r1^2=t*r2^2\`.

The external Einstein equation fixes the AdS radius L:

\`L^2/r1^2 = 20/(1+t)\`, \`L^2/r2^2 = 20*t/(1+t)\`.

We independently substitute both magnetic fields into all internal/external Einstein components for t=1/17, 1/3, 1, 9/4, 17 and for integer charge examples (1,1), (2,1), (7,2), (20,1), (100,1). Maxwell Bianchi/d*F vanish for constant product-sphere volume forms.

From the **Einstein-frame scalar kinetic metric** \`G_uv=diag(56/3,8)\` and the full two-radius potential Hessian at each stationary point, the physical generalized two-radion mass matrix in AdS units is

\`M L^2 = [[20, -60(t-1)/(7(t+1))], [-20(t-1)/(t+1), 36]]\`.

Its two eigenvalues are **exactly**

\`m_±^2 L^2 = 28 +/- 8 sqrt(1+(75/28)*((t-1)/(t+1))^2)\`.

For all t>0, the smaller eigenvalue exceeds \`28-8sqrt(103/28) = 12.656318...\`, substantially above the AdS5 BF bound \`-4\`. This is a new *specific branch* homogeneous-radion stability proof; not a proof of the whole coupled KK spectrum.

The minimally coupled probe scalar and the standard unwarped transverse-traceless spin-2 internal Laplacian have harmonic contributions

\`m_{l1,l2}^2 L^2= [20/(1+t)] l1(l1+1) + [20t/(1+t)] l2(l2+1)\`.

The first positive mode is **\`40min(1,t)/(1+t)\`**, which tends to zero as t→0 or ∞. With fixed t, rescaling both charges together enlarges all radii but leaves this KK/AdS ratio unchanged. Thus **positive homogeneous radion masses do not imply a uniformly gapped, parametrically scale-separated 5D effective theory**. At (N1,N2)=(100,1), t≈242.05165, the first probe gap has \`m² L²≈0.164574\`, while the smaller radion value remains ≈12.748.

**Caveats:** This uses the specified classical Einstein–Maxwell model, *not* the E6 exceptional field theory; it does not include all metric-Maxwell mixed scalar/vector/tensor harmonics, E6 embedding tensors, branes, anomalies or a dimensional scale derived from first principles. Brown & Dahlen (2014) previously developed the general stability spectrum for product-manifold Freund–Rubin flux compactifications: https://arxiv.org/abs/1310.6360 . We therefore claim the **explicit model-specific charge-branch formula and independent checks**, not the general novelty of flux-stabilized products.

## 3. H27 physical-generator front — autonomous 108-state quantum cursor and an exact locality barrier

Earlier: H27 has 27 regular states, X/Y four pulses give central Z of order three. Here put the step program into an internal **four-state cursor** \`c∈Z4\`: static unitary \`W:(g,c) -> (G_c g,c+1)\`, with a fixed program \`G_0=Y^-1,G_1=X^-1,G_2=Y,G_3=X\`. This avoids an externally changing pulse selector at the level of **discrete-time unitary dynamics**.

On every cursor sector \`W^4(g,c)=(Zg,c)\`, \`W^12=I\`. The exact 108-site permutation has **nine disjoint 12-cycles**, so the unitary Floquet eigenvalues are all 12th roots of unity, each ninefold. Every state is exactly reversible with a twelve-tick recurrence. The original H27 regular algebra is unchanged.

An exact Hermitian generator \`H=-Arg(W)\` exists by spectral calculus. On one 12-cycle, the numerical verification \`exp(-iH)=W\` passes at <1e-10 matrix norm; however the Hermitian matrix has **132 nonzero offdiagonal directed entries** (all pairs of distinct cycle vertices), versus only 24 for the nearest-neighbor 12-cycle. Thus taking the logarithm does **not** solve the sparse, autonomous continuous-time **local** Hamiltonian problem.

Separately, an order-three elementary translation \`U_X\` has explicit spectral projectors \`Π_k=(I+ω^{-k}U_X+ω^{-2k}U_X^2)/3\`; a Hermitian finite-duration pulse \`H_X=(2pi/3)(Π_2-Π_1)\` gives \`exp(-iH_X)=U_X\` exactly. The unit of duration, the generator's physical energy scale, and autonomous interaction mechanism remain externally specified. This is a programmable finite cursor and a clear locality constraint, **not** an observed time quantum or an energy-conserving physical device.

## 4. Frame-selection front — W33 incidence reconstructed from **annealed frame fluctuations**

**Prior art:** Pass4474 and TOE23 established the 1,620 symplectic W33 apartments and their association with projective four-ray frames and sparse local \`C3^4\` graphs. TOE23 already investigated finite invariant frame-hopping dynamics, which does *not* spontaneously select a unique frame. We do not re-claim those constructions.

We independently enumerate the 40 projective rays of F3^4. Every projective four-ray set with precisely two nonperpendicular disjoint pairs is a W33 apartment. There are **1,620**, each giving a unique symmetric set of **eight signed displacement generators** for a translation-invariant 8-regular graph on 81 affine addresses.

Exact two-neighbor apartment census (all 3160 unordered pairs of nonzero displacement vectors, computed by integer bitset intersections):

| Pair relation | Unordered pairs | Apartments containing both | Probability over uniform frame |
|---|---:|---:|---:|
| v and -v | 40 | 162 | 1/10 |
| Distinct projective directions, Ω(v,w)=0 | 960 | 27 | 1/60 |
| Ω(v,w)≠0 | 2160 | 6 | 1/270 |

Each fixed nonzero generator occurs in exactly **162/1620=1/10** of the apartment frames. Therefore the uniform annealed adjacency is **\`Abar=(J-I)/10\`**, a nonlocal weighted complete graph. Yet the pair-frequency classifier \`162/27/6\` recovers **the underlying symplectic collinearity relation with no classification errors**.

All 1620 8-neighbor Cayley graphs commute as abelian convolution operators on F3^4. Each has adjacency spectrum \`8^1,5^8,2^24,(-1)^32,(-4)^16\`. For any nontrivial Fourier character, a uniformly sampled apartment-frame adjacency eigenvalue has exact distribution \`Pr(5,2,-1,-4)=(1/10,3/10,2/5,1/5)\`, mean \`-1/10\`, variance **\`729/100\`**.

**Physics consequence / conditional veto:** A finite \`PSp(4,3)\`-invariant Gibbs or ground-state mixture that is itself invariant under the full transitive frame action cannot display a singled-out 8-neighbor adjacency in its first moment; its two-point ensemble data do retain W33. A specific frame, environmental pinning, or controlled infinite/thermodynamic limit remains needed to turn those fluctuations into a dynamically selected local geometry. No Lorentzian metric or Einstein field equation is derived.

## 5. Photonic detector-level front — optimized five-setting internal-GHZ witness

Use the earlier independently tested **five measurement settings** on one 16-mode photon: one computational rail readout and four equatorial parity settings. For *any* 16x16 state under trusted rail factoring,

\`A=1/4 Σ_{j=0}^3 (-1)^j <M(j*pi/4)^tensor4>=2 Re rho_{0,15}\`;

\`F_GHZ=(p0+p15+A)/2\`.

A fake GHZ-like state supported on rails 3 and 12 gives \`<X^tensor4>=1\` but \`F_GHZ=0\` and is rejected by this Fourier-filtered witness. This is an **internal one-photon factorization witness**, not nonlocal Bell violation between separate photons. The five-setting GHZ fidelity witness is established prior art; see https://www.nature.com/articles/s41534-024-00867-0 .

**Specified synthetic assumptions**, *not experimental measurements*: four 98%-survival optical preparation layers, four more 98%-survival equatorial analyzer layers, a 93%-efficient detector, accepted-event contamination bounded by 1% on each setting, calibrated conditional probability drift ≤0.005 on the Z endpoint probability and conditional parity bias ≤0.01 on each equatorial setting, plus independent accepted observations.

The joint conservative worst-case **fidelity bias** is \`(1/2)*0.01 + (4/8)*(2*0.01) + (1/2)*0.005 + (4/8)*0.01 =9/400=0.0225\`. A five-setting union-Hoeffding 99% confidence interval with target statistical fidelity halfwidth ≤0.055 is minimized at accepted-shot allocations approximately proportional to \`(coefficient * setting_survival)^(2/3)\`, yielding:
- **3,678 accepted events** for the computational setting;
- **2,195 accepted events each** for the four equatorial settings;
- **15,388 expected raw launches**, compared with **15,983** for the best equal-per-setting allocation at the same conservative width, detector and loss assumptions.

The frozen seeded synthetic accepted counts give \`Fhat≈0.947288\` and a conservative 99% one-sided conditional fidelity bound \`F≥0.869798\`, after both statistical and adversarial-systematic deductions. It clears the one-half threshold **under the model's explicitly assumed independent sampling, trusted calibration, erasure and selected-mode factorization**, not under arbitrary device-independent detector behavior.

NIST single-photon source/detector terminology: https://nvlpubs.nist.gov/nistpubs/ir/2023/NIST.IR.8486.pdf ; correlated-noise entanglement certification context: https://qutech.nl/wp-content/uploads/2020/10/Witnessing-entanglement-in-experiments-with-correlated-noise.pdf .

## Three additional independent implications

**A. Charge anisotropy versus dimensional reduction.** The unequal-flux branch has a homogeneous positive radion gap at all positive ratios, but its first KK probe mode can approach zero in AdS units. This decisively refutes *within this model* the shortcut "stabilized radii imply an effective five-dimensional spectral gap."

**B. A finite clock does not automatically yield a local Hamiltonian.** The 108-state static cursor removes external step scheduling in discrete time, but its exact spectral logarithm is long-range, so the locality problem remains tangible rather than semantic.

**C. Geometry as covariance, not mean.** The symmetric apartment ensemble has completely uniform nonlocal first moments while its exact two-point spatial covariance distinguishes W33 orthogonality. A microscopic selector could therefore be tested via fluctuations even when no preferred frame is visible in first-order observables.

## Additional executed falsifier — recover W33 from 10,000 sampled apartment couplings

Separate producer: \`analysis/toe_20261114_frame_fluctuation_sampling.py\`, certificate \`data/toe_20261114_frame_fluctuation_sampling.json\`, regression \`tests/test_toe_20261114_frame_sampling.py\`.

From the 1,620 exact apartment-generator eight-neighbor sets, draw independent uniformly random apartments **with replacement**, using seed 20261114. Estimate the conditional two-displacement co-occurrence probabilities for all 3,160 unordered pairs of 80 nonzero displacement vectors. Classify using the midpoints between the exact probability levels 1/10 (opposite), 1/60 (distinct symplectic-orthogonal), and 1/270 (nonorthogonal). **At 10,000 sampled frames, all 3,160 pair relationships were recovered correctly in this frozen seeded Monte Carlo experiment** (0 misclassifications). It is an experiment on a finite random combinatorial data model, not measured geometry in nature.

For a rigorous **sufficient**, not necessary, 99%-simultaneous correctness bound under iid uniform frame sampling, use a union bound and the two-sided Bernoulli Hoeffding inequality for all 3160 pair frequencies. The narrowest class gap is \`1/60-1/270=7/540\`. With midpoint threshold, the required deviation is less than \`7/1080\`. The conservative bound is

\`N >= ceil[log(2*3160/0.01) / (2*(7/1080)^2)] = 158972\` independent sampled frames.

This does not require the state to select an apartment permanently, but **does require an operational way to sample its coupling configuration**. If the physical apparatus only sees the first-moment averaged adjacency \`(J-I)/10\` and cannot resolve frame-conditioned two-neighbor correlations, the classifier is unavailable. None of this proves a dynamic symmetry-breaking phase transition or spacetime emergence.

## Audit boundaries and reproducer

The full producer asserts every finite count, rational covariance shell, Einstein equation, monotone charge branch and sampled Hamiltonian identity; the independent pytest suite separately checks fields, shell multiplicities, frame orbitals, sample allocation and false-positive controls.

\`\`\`powershell
py -3 analysis/toe_20261114_nextfive_f8_flux_cursor_frame_optical.py
py -3 -m pytest tests/test_toe_20261114_nextfive_exact_controls.py -q
\`\`\`

**Still open:** a global exact F8 lower bound matching Pass12671; a fully coupled 9D metric–Maxwell Kaluza–Klein stability spectrum, and genuine E6 ExFT embedding; physically local energy-conserving H27 clock dynamics; dynamical, robust symmetry reduction selecting one of 1620 sparse frames; measured optical calibration, multi-mode crosstalk and device-independent claims. The above mathematics does **not** solve the TOE.
