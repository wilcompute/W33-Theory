# From an order-24 clock to a declared particle action: conversions and quality

The order-24 witness of `75f2a7e0268374bdb533dc4ac49c1fac1b723672` now has an explicit regular24-orbit label map, a declared24-fermion action, and coupled population/energy equations. A larger finite symmetry can enforce the desired bilinear pattern. Pair conversions generate a substantial mass response in the declared classical moment closure. The same model fails a generic leading scalar-operator quality screen. These results change the design requirements; they do not establish a viable TOE.

## Evidence, ownership and reading

The starting files `toe_20261108_native_cyclic_orders.py`, `toe_20261108_cyclic_partner_control.py`, their JSON and the physical-eigenmode report were reread. The November5 native-boundary axion report and the prior PQ-quality formula were checked: they already require protection of the full added field inventory. The scalar moment packet `6fcbfcb99` supplies prior number/energy methodology for a different sector; its particles are not identified with these fermions.

The cyclic spectrum and population mechanism belong to [Delaunay–Lee–Yin–Yu2610.30253](https://arxiv.org/html/2610.30253v1). The additional work here is the stated mediator inventory and its conversion/energy calculation. [Garny–Heisig–Lülf–Vogl1705.09292, sectionIII](https://arxiv.org/html/1705.09292v2) supplies standard coupled-conversion and classical thermal-average context. We use neither its particle model nor its relic-density conclusion. Selected equations/sections were read, not either complete paper.

The scalar quality calculation is standard EFT, already used in `toe_20261105_pq_quality_gauge_obstruction.py`. [Cheek–Fowlie–Herrera2606.14098, sectionIII](https://arxiv.org/html/2606.14098v1) gives the canonical scalar convention and operator curvature. Treating coefficients as order one is a hypothesis about UV effects, not a calculation of quantum gravity. [Korbelář–Tolar2606.08215, introduction/section2](https://arxiv.org/html/2606.08215v1) reviews the odd-dimensional Clifford semidirect structure; the finite-group construction below is standard orbit/induction mathematics, not a new group theorem.

Result-specific repository searches included the covariance construction, conversion/heating terms, quality numbers and17496. The integer17496 already occurs in optical probability numerators and a q9 orbit count. The October29 three-photon report and q9 certificate were inspected; no identification of those objects with this group follows from equal integers. Search caps and reading limitations are retained in the intake receipt. No priority claim is made.

Full extracted manuscript text pages97–104 was read, with page98 also rendered and visually inspected. This brings cumulative personal text coverage to1–104 of215 pages of the unchanged PDF `003b75482b6584e20e83a55d9e9ba0a181f93b8dff0f94c1d615039c21213cbb`. These pages explain why gauge-level selection rules, a vacuum and allowed operators must be checked together. Their string-census theorems were read as manuscript claims, not independently re-proved here. Complete weekly/PDF reading remains unfinished.

## 1. A regular cyclic orbit and a bilinear-protecting extension

Let M be the saved6-by-6 symplectic matrix of order24. Its orbit on seed `(0,0,0,1,0,1)` contains24 distinct vectors and24 distinct projective labels. Assign a Dirac fermion psi_k to q_k=M^k q_0. This names an actual label permutation, not a derivation of particles from qudit states.

Define a24-dimensional representation

\[
D(x)_{kk}=\exp(2\pi i\,q_k\cdot x/3),\qquad
(C\psi)_k=\psi_{k+1},\qquad x\in\mathbb F_3^6.
\]

Direct generator checks give \(CD(x)C^{-1}=D(M^Tx)\). All729 additive character signatures are distinct, and the24 permutation cosets have different supports. This is a faithful representation of \(G=\mathbb F_3^6\rtimes C_{24}\), of order17496. It is a subgroup construction using enlarged three-qutrit affine symplectic labels; it is distinct from the original two-qutrit W33 group and from the27-dimensional qudit state representation.

Take Phi neutral under the additive subgroup and transforming as \(\exp(2\pi i/24)\) under C. Both Dirac chiralities transform in the displayed representation. The distinct q_k forbid every off-diagonal Dirac bilinear. No q_i+q_j vanishes, so Majorana bilinears are also forbidden. Neutral Phi, dark-Higgs and SM-Higgs insertions cannot repair a nonzero additive charge. The cyclic generator then enforces a universal bare mass and linear Phi Yukawa weights proportional to \(\exp(2\pi i k/24)\).

This replaces the simpler Z24-only model's extra global flavor-number assumption at the bilinear level. If G is posited as a finite gauge symmetry, its vectorlike fermions admit a gauge-invariant Dirac mass/regulator; this does not construct a microscopic finite-gauge or gravitational sector.

It also does not forbid everything. There are99 distinct unordered pair-sum classes; explicitly \(q_0+q_1=q_8+q_{17}\) over F3. A cyclic orbit sum of a current-current operator converting those pairs is symmetry allowed. Such additional dimension-six coefficients are not selected by G and are not included in the universal-vector-only collision model. Phi^24 remains invariant under the entire group.

## 2. A specified renormalizable mediator model

On supplied four-dimensional spacetime introduce a U1_D gauge vector A, a charge-one complex dark Higgs S, neutral Phi, and24 SM-singlet Dirac fermions of vector charge+1. Add canonical kinetic terms, bounded radial potentials \(\lambda_\Phi(|\Phi|^2-f^2/2)^2\), \(\lambda_S(|S|^2-v_D^2/2)^2\), and

\[
\mathcal L_m=-\sum_k[(M+y\omega^k\Phi)\bar\psi_{kL}\psi_{kR}+\mathrm{h.c.}],
\quad\omega=e^{2\pi i/24}.
\]

For \(\Phi=f e^{i\varphi/f}/\sqrt2\), the physical masses are the published cyclic spectrum \(m_k=M\sqrt{1+\epsilon^2+2\epsilon\cos(\varphi/f+2\pi k/24)}\), with \(\epsilon=yf/(\sqrt2M)\). Left-handed gauge charges+1,-1 cancel the continuous cubic and mixed gravitational gauge anomalies pairwise. This must not be confused with the classical shift current: Phi->exp(i alpha)Phi and psi_R->exp(-i alpha)psi_R at M=0 has mixed U1_D-squared anomaly coefficient24. No exact quantum global shift symmetry is asserted; magnetic/UV sectors require separate analysis.

Choose \(m_A=g_Dv_D=10\,\mathrm{MeV}\) and a heavy dark radial scalar. In the nonrelativistic formation epoch these states cannot be produced on shell. Integrating out A gives \(-G_D J_\mu J^\mu/2\), \(G_D=g_D^2/m_A^2\), with \(J=\sum_k\bar\psi_k\gamma\psi_k\). It permits \(\psi_i\bar\psi_i\leftrightarrow\psi_j\bar\psi_j\) without changing any species' net particle-minus-antiparticle charge. Elastic scattering is present, but its full kinetic-equilibrium hierarchy is not solved.

The baseline Z24 action has accidental independent fermion vector numbers only after choosing its allowed off-diagonal terms absent. The finite extension supplies an explicit bilinear alternative; higher four-fermion operators remain a separate UV assumption. Allowed scalar portals, gauge kinetic mixing, finite-gauge sectors, radial hierarchies, abundance production and cosmological vacuum energy are not fixed. The positive moment results assume a sufficiently small scalar-breaking potential so that its phase is frozen during formation; they cannot be combined with a generic huge Phi^24 term as a self-consistent cosmology.

## 3. Actual conversion kernel and coupled energy equation

For the displayed vector contact operator, the unpolarized, distinct-flavor tree cross section is

\[
\frac{\sigma_{ij}(s)}{G_D^2}=
\frac{(s+2m_i^2)(s+2m_j^2)}{12\pi s}
\sqrt{\frac{s-4m_j^2}{s-4m_i^2}}.
\]

An independent Dirac-matrix trace calculation verifies this normalization. The classical thermal reaction density is

\[
\gamma_{ij}=\frac{g_i g_{\bar i}T}{32\pi^4}
\int_{4\max(m_i,m_j)^2}^\infty ds\,
\sigma_{ij}(s)(s-4m_i^2)\sqrt s\,K_1(\sqrt s/T).
\]

It is symmetric under i<->j. Downhill rates are evaluated with a generalized Laguerre quadrature and detailed balance supplies the uphill rates. Threshold differences are factored before evaluation; standard scaled-Bessel asymptotics avoid large-argument library NaNs. An initial failed producer is recorded, not treated as physical evidence. Independent server V8 integration evaluates K through its hyperbolic integral and uses nested Simpson quadrature for the full rate; it agrees with local controls.

Use particle-only density n_p, antiparticles equally numerous, \(\eta_i=n_i/n_p\), and \(n_p\propto a^{-3}\). Each pair conversion removes one particle and one antiparticle, so

\[
\eta'_i=-\frac{n_p}{H}\sum_{j\ne i}
\langle\sigma v\rangle_{ij}
[\eta_i^2-(n_i^{eq}/n_j^{eq})^2\eta_j^2],
\quad '=d/d\log a.
\]

The antisymmetric pair implementation conserves \(\sum_i\eta_i\). Detailed balance and decreasing fixed-temperature relative entropy are tested. Under a common classical kinetic temperature,

\[
E_i=m_iK_1(m_i/T)/K_2(m_i/T)+3T,\quad C_i=dE_i/dT,
\qquad
T'={-3T-\sum_i E_i\eta'_i\over\sum_i\eta_i C_i}.
\]

This follows from \(\rho'+3(\rho+P)=0\), not an imposed cooling law. Subtracting one common rest energy in the composition term avoids cancellation. An independently integrated work variable checks conservation of \(\sum_i\eta_iE_i+\int3T\,d\log a\).

## 4. Supplied benchmark: populations, heating and memory

Inputs are M=16keV, epsilon=0.05314971931113116, formation phase0.37, initial T_D/M=0.1, T_D/T_gamma=0.1, particle yield0.00137, g_rho=3.36 and g_s=3.91. Antiparticles carry the same yield. A supplied radiation+matter background uses equality temperature0.8eV. These fix the initial abundance; the calculation does not predict it. The scalar phase remains fixed, and all24 initial populations are uniform in the baseline.

Let strength=\((n_{p,0}/H_{rad,0})G_D^2 M^2\). Evolve to log(a/a0)=12, where supplied T_gamma=0.0983eV. The frozen response differentiates masses with final populations held fixed and f=MP; it is available field-space response, not a solved scalar trajectory.

| strength | g_D for10MeV mediator | final T_D/M | max available absolute beta_eff |
|---:|---:|---:|---:|
|0 (disconnected control)|0|4.763e-12|floating-point floor|
|1|0.004012|6.142e-9|0.003330|
|10|0.007134|2.397e-8|0.019102|
|100|0.012686|3.223e-8|0.039877|
|1000|0.022560|2.400e-8|0.049665|

For strength100, omitting conversion heating gives T_D/M=4.786e-12 and beta_eff=0.040830. Its integrated first-law residual is0.04089 in units M; the energy-conserving solution's residual is3.63e-10. Similar mass responses can therefore hide radically different kinetic histories. The exact classical mean speed at the final point is2.92e-4 c with heating versus3.56e-6 c without it. These are moment diagnostics; no free-streaming cutoff, transfer function or observational exclusion is inferred while scattering and kinetic closure remain unresolved.

Rate-grid/quadrature refinement changes final population L1 by4.81e-8; an independent BDF solver changes it by9.72e-8. Initial equilibrium populations instead of uniform populations change final L1 by0.01244 and temperature by-4.01percent: the chosen strength has not erased all memory. Extending the endpoint to log(a/a0)=14 changes L1 by1.21e-6. Physical rows have maximum MB zero-momentum occupation below0.033; that supports dilution but does not prove common-temperature kinetic equilibrium or eliminate percent-scale quantum corrections.

## 5. The scalar quality–excursion obstruction

Even the finite extension allows

\[
\Delta V=c\,\Phi^{24}/M_P^{20}+\mathrm{h.c.}
\]

For general leading degree N and r=f/MP, its phase-uniform curvature envelope is

\[
Q_N={\max|\Delta V''|\over H_0^2}
=2N^2|c|(M_P/H_0)^2r^{N-2}2^{-N/2}.
\]

At f=MP and coefficient1, Q24=10^119.90. Requiring Q24<1 instead gives r<3.54763e-6. Keeping the supplied local beta(pi/2)=0.053 then needs epsilon about1.88e-7, whose entire available log mass ratio is only3.76e-7.

A supplied illustrative integrated change0.053*0.3=0.0159 requires at least \(\log[(1+\epsilon)/(1-\epsilon)]\ge0.0159\), since any positive population-weighted mean lies between M(1-epsilon) and M(1+epsilon). On the small-epsilon local-beta branch this implies epsilon>=0.00794983 and r>=0.149987. At that minimum r, Q24=10^101.77455. The first generic leading degree whose unit-coefficient envelope falls below H0 squared is130. This is a necessary amplitude comparison, not a constant-beta cosmological trajectory or a measured excursion constraint.

Forbidding just Phi^24 is insufficient: Phi^25 Phi* and Phi^26(Phi*)^2 are also Z24-invariant and phase breaking. Their degrees26 and28 are explicitly enumerated. All dangerous lower-degree mixed operators must be controlled. At r=1 the analogous leading-degree threshold is842. These numbers depend on the chosen canonical normalization, coefficient and cutoff; small coefficients, gauge-origin Wilson lines, locality, cancellations or other UV structure can alter the conclusion. The result rejects generic unit-coefficient protection by this finite symmetry alone, not all axion completions or the published loop mechanism.

## Reproducibility and remaining physics

The matching source files, JSON, independent server code and focused tests are published together; validation and guard outcomes are in the manifest. Remote Desktop Commander ran the action/quality and conversion producers and ODE controls on TheHeavyCrown while server V8 performed independent thermal integrals and algebra/quality controls. The decisive missing tasks are a genuine suppression mechanism for allowed scalar operators, a justified full reaction inventory, momentum-dependent kinetic evolution and scalar/metric perturbations. The current action, finite symmetry and thermal calculation are explicit conditional modules, not one verified Standard-Model-plus-gravity theory.
