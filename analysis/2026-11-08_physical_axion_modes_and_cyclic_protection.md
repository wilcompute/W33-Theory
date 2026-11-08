# Physical axion modes and a conditional cyclic-partner alternative

The recent running-coupling calculations need a physical mass-eigenmode construction. A single mixed cosine does not provide the proposed varying dark-matter mass along its relaxed light direction. A separate, published cyclic-partner mechanism does provide varying physical particle masses with a suppressed vacuum harmonic. This packet computes a supplied benchmark, rather than identifying that extra field inventory with W33 or solving the TOE.

## What changed and what was actually read

The six incoming commits from `db5c05e9280ea73e7839f38780106489d71b59c3` through `b68a706b16fbcafe3899e896bc8e4b7f425df47d` were read in full, including the clock producer, corrected plaquettes, nine tests, workflow, CLASS patch, stored controls and preregistration. Their net change is eleven files and659 added lines. They were fast-forward integrated without modifying them. Four further commits through `9e0aa0b7246dcd67f98820848c425c61ddfc66b3` arrived on the shared branch and were also read in full: the729-channel registry, catalog rational-alias scanner, tenth test and full five-front report. The final focused replay includes that tenth incoming test. The stored CLASS likelihood controls are upstream computations, not reproduced here. The new workflow automates extraction of215 PDF pages and recursive TeX coverage; that is not human reading or proof verification.

This continuation additionally read full extracted PDF text pages85–96, with the unchanged PDF SHA256 `003b75482b6584e20e83a55d9e9ba0a181f93b8dff0f94c1d615039c21213cbb`. Cumulative personal text coverage is pages1–96 of215. These pages distinguish internal Albert/Spin symmetry from physical spacetime, and hosted Standard-Model structures from a selected viable vacuum. Full weekly and full manuscript reading remain unfinished.

Prior owners include `analysis/toe_uv/monodromy_running.py` at `31f833f38`, `analysis/PASS12627_MCMC_SHEAR_RADIATIVE.md`, the November3 radiative/mechanism audits and `analysis/2026-11-05_native_boundary_axion_and_two_UV_repairs.md`. The known Sp43 order list, including18, already appears in `analysis/w33_BREAKTHROUGH_542_sylow_maximal_substrate_GAP.py`; its other physical/Sylow interpretations are not used. Result searches also covered the index and py/json/md/tex material with a2MB cap. Searches are not a novelty proof.

## 1. Canonical fields expose the missing interaction

Take canonical kinetic terms and the explicitly declared potential

\[
V=\Lambda^4[1-\cos(a/f+\phi/F)].
\]

With \(s=\sqrt{F^2+f^2}\), the orthonormal coordinates
\(h=(Fa+f\phi)/s\), \(\ell=(-fa+F\phi)/s\) give phase \(sh/(fF)\). Therefore the Hessian has rank one, eigenvalues zero and \(\Lambda^4(f^{-2}+F^{-2})\cos(sh/fF)\). On the stable trough \(h=0\), the heavy mass is independent of \(\ell\). Holding \(a=0\) while changing \(\phi\) generally leaves that trough; \(\partial_a V\ne0\). A coordinate second derivative at that point is insufficient to identify the mass of a relaxed physical dark-matter mode. The flat direction also has no supplied nonconstant dark-energy potential.

This does not reject multi-axion monodromy. The cited [D’Amico–Hamill–Kaloper model](https://arxiv.org/html/1605.00996v3) uses several cosine terms and normal modes, with a potentially interacting ultralight component. Selected model/normal-mode sections were read; the full paper was not read. For its declared three-term potential

\[
V=A(1-\cos(a/f))+B(1-\cos(\phi/F))+C(1-\cos(a/f-n\phi/F)),
\]

our direct differentiation at the vacuum gives

\[
H=\begin{pmatrix}(A+C)/f^2&-nC/(fF)\\-nC/(fF)&(B+n^2C)/F^2\end{pmatrix},\qquad
\det H={AB+BC+An^2C\over f^2F^2}.
\]

These extra terms change the problem. Unequal decay constants are retained throughout; the potential itself is the differentiation authority.

A declared quadratic pin \(\Lambda^4\kappa(a/f)^2/2\) makes the relaxation condition \(\kappa\alpha+\sin(\alpha+u)=0\), where \(\alpha=a/f,u=\phi/F\). For \(c=\cos(\alpha+u)\), eliminating the stationary heavy coordinate produces the Schur curvature \(\kappa c/[F^2(\kappa+c)]\), with light kinetic factor \(Z=1+[fc/(F(\kappa+c))]^2\). We compute the full heavy eigenvalue and its derivative along the normalized trough tangent. Both negligible and very strong pinning suppress its response in this example. Pinning cannot simply be asserted while retaining the original spectrum.

The75 supplied pinning points are numerical illustrations. Two independent Minkowski evolutions with different light velocities agree in their heavy histories to1.1e-13; heavy energy drift is9.9e-11. This tests the exact flat direction, not cosmological evolution.

## 2. A useful, limited curvature–coupling inequality

For canonical fields with \(V=\sum_i A_i[1-\cos(q_i\cdot x)]\), assume every \(w_i=A_i\cos(q_i\cdot x)>0\), a nondegenerate heavy eigenvalue \(\lambda_H\), heavy unit eigenvector \(e_H\), and any canonical unit direction \(u\). Hellmann–Feynman gives

\[
\partial_u\lambda_H=-\sum_i w_i\tan\theta_i\,(q_i\cdot e_H)^2(q_i\cdot u).
\]

Cauchy–Schwarz and \(\sum_iw_i(q_i\cdot e_H)^2=\lambda_H\) imply

\[
|M_P\partial_u\log m_H|\le {M_P\over2}
\sqrt{{u^THu\over\lambda_H}}\,
\max_i|(q_i\cdot e_H)\tan\theta_i|.
\]

This is an application of standard identities, not a newly discovered general no-go theorem. A large positive-branch hierarchy suppresses the response unless the charge/phase factor compensates. Negative cosine weights, cancellations, hilltops, changing field metrics and finite-density trajectories require separate treatment. A4096-point three-cosine scan with \(u=e_L\) reaches maximum ratio0.934912 of the bound. An initial scan mistakenly allowed a negative second cosine at n=1 and failed; the sampling range was corrected to satisfy the stated premise. The failure was retained in the reading/execution record, not relabeled a physical counterexample.

## 3. The incoming CLASS mass law has a separate zero-parameter control

Commit `d4c3be9c75c6f428fdf4840712ed8e8ca305adbc` supplies the phenomenological law \(m^2/m_0^2=\cos(\theta_0+F_i\phi)/\cos\theta_0\), \(\tan\theta_0=2b_0/F_i\). A numerically stable identity is

\[
{m^2\over m_0^2}=\cos(F_i\phi)-2b_0\phi\,\operatorname{sinc}(F_i\phi),\quad
\lim_{F_i\to0^+}{m\over m_0}=\sqrt{1-2b_0\phi}.
\]

At fixed nonzero \(b_0\), this is not \(\exp(-b_0\phi)\). The implementation explicitly switches to that exponential when \(F_i<10^{-12}\); it is a useful separately selected fading control, not a continuous limit. The upstream preregistration already recognizes the running floor \(db/d\phi=F_i^2/2+2b^2\); this packet supplies a stable mass-law check and clarifies code-control scope. The patch's Fi=0 agreement validates recovery of that switched phenomenology, not the missing two-field action or radiative protection. No CLASS run or refit is claimed here.

## 4. A constructive protected-spectrum benchmark

[Delaunay–Lee–Yin–Yu](https://arxiv.org/html/2610.30253v1) give cyclic Dirac partners with \(m_k=M\sqrt{1+\epsilon^2+2\epsilon\cos(\theta+2\pi k/N)}\). The complete spectrum suppresses the leading vacuum harmonic to order \(\epsilon^N\); equal populations also suppress the collective mass response. Their internally equilibrated mass-dependent populations can evade the latter cancellation. Relevant model and population equations were read, not the entire paper. This mechanism is theirs, not a W33 result.

We supply \(M=16\,\mathrm{keV}\), \(f=M_P=2.435\times10^{27}\,\mathrm{eV}\), \(H_0=1.44667\times10^{-33}\,\mathrm{eV}\), and individual \(b(\pi/2)=0.053\). These fix \(\epsilon=0.05314971931113116\). The leading one-loop curvature envelope divided by \(H_0^2\) is:

| N | leading envelope | exact curvature at theta=0 |
|---|---:|---:|
|12|8.89948e10|8.86085e10|
|18|1825.48|1816.80|
|20|5.06334|5.03885|
|21|0.267029|0.265728|
|22|0.0140929|0.0140238|
|23|0.000744251|0.000740576|

The first below-one leading estimate is N=21; this is weaker than a much-less-than-one requirement. Exact100-digit Coleman–Weinberg differentiation checks the displayed phase and additional phases; it is not an all-phase exact upper bound or a complete loop/operator audit. Additional scalar interactions and symmetry-breaking operators remain unaudited.

Freeze nonrelativistic equilibrium weights \(\eta_k\propto m_k(\theta_i)^{3/2}\exp[-m_k(\theta_i)/T_d]\) at supplied \(\theta_i=0.37\). Differentiate the subsequent mean mass with these weights fixed. For N=21, decreasing \(T_d/M\) from0.1 to0.003 increases its fractional rms from0.00829 to0.03652 and maximum \(|b_{\rm eff}|\) from0.01172 to0.05183. Uniform-population values reach floating-point noise and are not measurements of the exponentially tiny harmonic. An independent actual server V8 calculation agrees with the local result. This demonstrates a conditional response, not the conversion rate, abundance, temperature history or realized scalar excursion.

## 5. Which native finite group could supply that cyclic symmetry?

We enumerate every symplectic basis over F3:80 choices for a,27 for its conjugate b,8 nonzero c in their orthogonal complement,3 for d. All51840 matrices are distinct and preserve J. Multiplying by a multiplier-two similitude constructs the second GSp coset; quotient orders stop at either +I or -I and central pairs are counted once.

| Explicit group | size | maximal element order |
|---|---:|---:|
|Sp(4,3)|51840|18|
|PSp(4,3)|25920|12|
|PGSp(4,3)|51840|12|

The Sp list was already known in the repo. The distinction between the two size51840 groups prevents an incorrect group identification. Under the specific requirement that the protecting cyclic symmetry be generated by one element of one of these groups, none supplies N>=21. An added global symmetry, larger Clifford extension, different representation system or additional fields is a different construction and is not ruled out. The sixteen-keV fermion replication benchmark also cannot be identified with the previous scalar-transport particles merely by sharing a mass number. The guard's rare size matches were checked against `data/w33_pass1065_schur_cocycle.json` and the flagged prior discriminant/D4/spectral certificates: these confirm prior group-size ownership, not a protected mass model. Its same-order warning matches our explicit statement that equal size does not identify the groups.

There is a concrete enlargement rather than only a negative screen. Choose an order-eight matrix in Sp(4,3), whose fourth power is -I4, and the order-three transvection [[1,1],[0,1]] in Sp(2,3). Their symplectic direct sum is an explicit6-by-6 matrix of order24. No smaller positive power is even a scalar plus/minus identity on the full space, so its projective order is also24. The saved matrix and alternating form are checked by modular multiplication. Thus three-qutrit symplectic labels support a Z24 subgroup even though the original two-qutrit/W33 space does not. This standard direct-sum construction is not new finite-group theory. The same supplied one-loop benchmark at N=24 gives a leading curvature envelope about3.93e-5 times H0 squared. This is a feasible algebraic starting point for an enlarged candidate, not an identification of that subgroup with24 physical fermion partners, anomaly-safe vertices or a full radiative completion.

## Validation and next physical boundary

Sources, generated JSON, independent server controls and focused tests accompany this report. Test/guard outcomes and exact hashes are recorded in the publication manifest. Remote Desktop Commander executed the group, axion and cyclic-partner producers on TheHeavyCrown; server V8 independently computed spectra, threshold and population controls while those jobs ran. No measured coupling or absolute mass is derived. The important open object is one explicit action specifying its fields, symmetry, allowed operators, conversion processes, thermal trajectory and cosmological perturbations. A successful likelihood fit to a supplied mass law would not fill those gaps.
