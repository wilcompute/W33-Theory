# TOE45 — W33 cusp collision tomography, the exact 90-versus-40 variance gap, and the Wilson-point selector

**10 October 2026 (research pass).** Baseline: TOE44 commit b143f9524b92e01aad3c1b266b5b45c4e50d9acb. New math below is exact in the finite *two-qutrit Pauli* setting and independent of any actual string compactification. This is a tested synthesis, not proof of a Theory of Everything.

## What changed since TOE44: full change inventory and source audit

GitHub comparison from TOE44 to the starting HEAD b4477e7942665855a5fcbecfbb5a129bfe51d7fc found **37 commits, 54 changed files**, with roughly 25,861 lines added and 27 removed. The added material includes 12 Pass11887–11904 prose reports, their 12 Python producers, 12 tests, numerical certificates, two large frozen orbifolder model-census snapshots, a formula-search-universe ledger refresh, and physics/ledger/PDF updates to *Forty Points*. **All twelve new research reports were read**, the exact changed-file inventory was examined, and the mathematical arguments were checked against selected full implementation source files (11899, 11900, 11903, 11904) plus frozen certificates. This is *not* a claim that all 25,000 changed lines of code and generated JSON were manually line-audited, or that every lengthy optimization was rerun. The specific new construction and tests below are fully replayed.

### Key source conclusions and their scope

| Repo pass | What the new source reports | Important scientific boundary |
|---|---|---|
| 11887–11889 | At a Witting ray, centraliser in full E8 is E6 + u(1)^2; SU(9) compact Higgs only gauges the grade-zero SU(3)^3; group 248 contains (27,3)+(27bar,3bar) | E8 gauge enhancement needs a higher-dimensional completion; chirality is not implied by an E8 adjoint |
| 11890–11892 | Field-content-dependent vacuum phase diagram (bosonic, SUSY, Hosotani and fermionic regimes) | Minimal Hosotani bosonic model actually selects unbroken SU(9), not trinification; different matter/soft terms give different minima |
| 11893 | Heterotic Z3 radiative trinification branch yields (3,3,3) and coloured exotics, not three physical SM families | Corrected SU2 embeddings include a three-doublet case that also carries exotic coloured quartets |
| 11894–11896 | Z6 local model can have a SU3xSU2xU1 stabiliser but wrong matter; actual CZ3 Wilson line makes visible flat directions SM charged | SM gauge algebra does not establish an SM vacuum or acceptable chiral matter |
| 11897–11899 | Neutral Hermitian Kahler moduli, two-qutrit Weil representation and **40 W33 lines as symmetric cusp contexts**; 40 cusp orbit has projective stabiliser 648 | Orbifold zero modes and the theta couplings are an indirect mathematical interpretation, *not* quantum measurement devices; no stabilising potential |
| 11900–11903 | **One nontrivial Wilson holonomy is a W33 point** with projective centraliser 648; 491 frozen SO(16)^2 Z3 models split into 339 antisymmetric-up and 152 local SU5-ten up-degenerate cases | No up-quark escape in this *specified scan at renormalisable order*; other compactifications, Higgs mixing, threshold effects and non-renormalisable couplings are not excluded globally |
| 11904 | Magnetized T4 theta mode model with a continuous Wilson line permits first-order splitting; finite heterotic Z3 theta splitting has cubic protection; a theta zero locks remaining two magnitudes | Magnetized construction is not a full realistic SM spectrum, and the near-cusp numerical mass-ratio match uses two adjustable parameters for two ratios |

**Cross-repo:** The connected Holotrade master still has its latest listed commit b0264880d7c5 (26 September 2026), which predates TOE44. Its frame-bundle carrier result is a mathematical 243 = 3 x 81 decomposition; no later Holotrade commit was detected. This pass writes only to W33-Theory.

## Exact theorem 1: the **40-cusp collision measurement** of W33

Let P be the 40 projective nonidentity Paulis in F3^4 (nonzero symplectic vectors modulo ±), and let L run over the 40 maximal commuting projective lines (totally isotropic planes). Put

- N_{L,p} = 1 if p belongs to L, else 0;
- A = adjacency of the W33 symplectic point graph with spectrum (12^1, 2^24, -4^15);
- q_p = 2 |Tr(rho W_p)|^2 for any positive trace-one 9x9 density matrix rho;
- C_L = sum_{j=1}^9 [Tr(rho Pi_{L,j})]^2, the **collision probability** for two independent nine-outcome projective measurements in stabilizer basis L.

**Known mathematical input** (see Pass4952): N is a 40x40 {0,1}-incidence operator, N^T N = 4 I + A, with singular-spectrum-squared 16^1 + 6^24 + 0^15 and rank 25. The dual geometry need not be identified pointwise with the points.

Pauli Parseval in a maximal abelian group gives the **exact operational identity** for all rho:

\[
\boxed{\quad 9 C - {\bf1} = N q,\quad \overline C = (1+\mathrm{Tr}(\rho^2))/10.\quad}
\]

The second identity uses sum_p q_p = 9 Tr(rho²)-1 and each p occurring on four W33 lines. The 40 contexts are **not** a complete ten-MUB spread (as in TOE43/44): 40 overlapping bases are used, and only one aggregate collision statistic is retained from each basis.

## Exact theorem 2: a 40-cusp **pure-state Pauli-power inverse**

The TOE42 spectral identity for pure rho is Aq = 2q + 2·1, or equivalently q = 1/5·1 + q₂ with A q₂ = 2 q₂. Applying N^T N = 4I+A gives N^T N q₂ = 6q₂.

Since 9 C−1=Nq and N·1=4·1,

\[
\boxed{\quad q
 =\frac15 {\bf1}
 +\frac16 N^{\mathsf T}\left(9C-\frac95{\bf1}\right)
 \qquad (\rho^2=\rho).\quad}
\]

This reconstructs **all 40 Pauli powers**, not the 80 real phase-bearing Weyl expectations or the full pure density matrix up to physical ambiguities. On 64 seeded random pure 9-vectors the maximum error was 5.55e-16.

For mixed rho, with m=(9 Tr(rho²)-1)/40 and q=(m·1)+q₂+q₋₄, the same generalized linear inverse returns exactly m·1+q₂: **15 whole coordinates in q₋₄ lie in ker N and are invisible**.

## Exact theorem 3: the **virtual-qutrit purity / cusp-collision variance gap**

As in TOE41/42, let H be the 90x40 incidence matrix of **nondegenerate** symplectic 2-planes in F3^4. It satisfies H^T H = 8I + J - A, and virtual factor-purities are

\[
\mathcal P_F=\frac{1+(Hq)_F}{3}\qquad(F=1,\ldots,90).
\]

Let P₋₄ be the W33 -4 spectral projector and let Cbar be the mean of the 40 C_L. Decompose the centred q-m·1 = q₂+q₋₄. Orthogonality gives:

\[
\begin{aligned}
\mathrm{Var}_{F=1}^{90}(\mathcal P_F)
&=\frac{\|q_2\|^2+2\|q_{-4}\|^2}{135},\\
\frac1{10}\sum_{L=1}^{40}(C_L-\overline C)^2
&=\frac{\|q_2\|^2}{135}.
\end{aligned}
\]

Therefore **for every density matrix**,

\[
\boxed{\quad
\mathrm{Var}_{90}(\mathcal P_F)
-\frac1{10}\sum_{40 L}(C_L-\overline C)^2
=\frac2{135}\|P_{-4}q\|^2\ge0.
\quad}
\]

- For every **pure** state, TOE42 shows q₋₄=0, so the two experimentally definable variances **agree exactly**.
- For a mixed state, the gap can be strictly positive. This is a selective dark-sector diagnostic, **not** a complete mixedness witness: isotropically depolarized pure states also have q₋₄=0.
- The means obey exactly E_{40} C=(1+Tr rho²)/10 and E_{90} P_F=3(1+Tr rho²)/10.

This is a new cross-measurement synthesis of previously established incidence identities, not a claim to have first discovered generalized quadrangle incidence spectra or MUB projective 2-designs.

## Exact theorem 4: **physical no-go** for retrieving mixed W33 dark modes from 40 cusp collisions

A kernel vector alone might lie outside the physically allowed density-state images. Construct two **explicitly positive density matrices** to close that loophole.

Choose a real nonzero h=P₋₄(1,2,...,40) scaled to max |h_i|=1. Set t=1e-5, eps=2e-6 and take

\[
q_{\pm}=t\,{\bf1}\pm\epsilon h,\quad
q_0=t\,{\bf1}.
\]

All 40 entries are strictly positive. For each q define the Hermitian physical state

\[
\rho(q)=\frac19\left[I_9+\sum_{p=1}^{40}\sqrt{q_p/2}(W_p+W_p^\dagger)\right].
\]

Its projective Pauli powers are *exactly* q, by orthogonality of distinct Weyl classes. Positivity is not just numerically conjectural: all W_p are unitary and \(2\sum_p\sqrt{q_p/2}<1\), so the perturbation operator norm is <1 and rho is positive definite; its trace is one. The lowest numerically computed eigenvalues are about **0.107**, versus a conservative analytical lower bound from the norm inequality.

Now N h = 0. Thus all 40 cusp collisions match for rho(q+), rho(q−), and rho(q0), and these states have exactly equal purity (because sum h=0). Yet rho(q+) and rho(q−) are distinct, with dark-sector-vector difference norm about **8.52e-6** and density-matrix Frobenius distance about **4.50e-4**. Their 40 collision discrepancies are <3e-20 numerically. The full nine-projector measurement collision relation was independently checked on selected contexts to <5e-17.

Even stronger, the constant baseline state rho(q0) has 90-factor purity variance virtually zero, while rho(q+) has variance **2.69037e-13**, despite **identical all-40 collision probabilities**. This directly measures the 15-dimensional inaccessible sector in principle.

The identity and inequality were further checked for **20** random Wishart full-rank density matrices, with maximum observed positive gap about **1.74094e-4**.

**Inference boundary:** only the 40 basis *collision scalars* are blind to this sector. Retaining the full nine-outcome distributions of enough commuting bases can reconstruct all complex Pauli amplitudes, as standard tomography demands.

## Exact theorem 5: the Wilson-holonomy point / cusp-context **4:36 selection rule**

The new Pass11900 family mechanism assigns the residual Wilson-line holonomy to one projective Pauli point p. The new Pass11899 modular description assigns each symmetric Kähler cusp to one maximal commuting Pauli line L.

W33 alone then forces:

- **4 out of 40** cusp contexts contain p; all four of their nonidentity Paulis commute with the holonomy.
- The other **36** contexts do not contain p. Each has **exactly one** of its four projective Paulis commuting with p; the remaining three fail.
- Across all point–cusp pairs, there are precisely **160 incident flags** and **1440 nonincident** combinations. The related 160-flag stabilizer 162 already appears in Pass11899.

This is a **holonomy-compatibility filter**, not a predicted count of physical Kähler minima. Commutation with a Wilson-line sector is only a **necessary kinematic condition** for simultaneous diagonalization, not sufficient for flavor mixing, an SM vacuum, or any real spectrum.

## Validation, reproducibility and credits

Files:
- Producer: analysis/w33_20261010_toe45_cusp_collision_reconstruction.py
- Certificate: data/w33_20261010_toe45_cusp_collision_tomography.json
- Tests: tests/test_w33_20261010_toe45_cusp_collisions.py

Run:

\`\`\`shell
py -3 -m pytest -q tests/test_w33_20261010_toe45_cusp_collisions.py
\`\`\`

The producer generates N, A, 40 isotropic lines, H, 90 nondegenerate planes, all Pauli matrices, exact integer spectral projectors, measured nine-outcome stabilizer projector collisions, 64 random pure cases, 20 random mixed cases, and positive analytic counterexample families from scratch.

Prior art **inside repo**: Pass4952, classical point–line incidence / rank 25; TOE41 and TOE42, 90 factor-purity and pure q in +2 eigenspace; TOE43/44, ten-MUB collision purity protocol; Pass11899, geometric cusps indexed by 40 lines; Pass11900, Wilson holonomy labelled by a point p. **Outside repo:** classical generalized quadrangle GQ(3,3) strongly regular spectral parameters and complete MUB/projective-2-design collision formulas are established mathematics (see DistanceRegular.org GQ(3,3) and randomized-measurement review Phys. Rep. 2024).

No conclusions in this report entail a Standard Model derivation, a dimensional continuum limit, measurement of a string cusp, or tested photonic hardware.

## Five best independent next steps

1. **Characterize *physical* dark-sector accessibility:** Classify which 15-mode perturbations around arbitrary full-rank two-qutrit states are realisable at fixed purity, and find sharp norm bounds under positivity and experimental noise.
2. **Implement both 90 and 40 measurements with an operational shot budget:** Generate Clifford conjugation circuits for all 90 nondegenerate virtual-factor frames and 40 isotropic stabilizer contexts, with loss/confusion, confidence bounds and an unbiased finite-shot estimator of the variance gap.
3. **Test Wilson-point selection against real orbifold coupling data:** Across the frozen Pass11903 491-model census, link each actual Wilson-point/line sector to the 4/36 cusp commutation filter and distinguish exact geometric incidence from physically allowed Yukawa terms.
4. **Independently audit magnetized flux normalisation and a full three-generation model:** Rebuild the Pass11904 theta hierarchy with actual flux intersection numbers, Higgs wavefunctions, kinetic normalization, CKM mixing and CP, then compare calibrated masses rather than arbitrary two-parameter ratios.
5. **Find a viable compactification/no-go beyond the scanned A8 class:** Test genuinely split local SU5-tens, vectorlike mixing, and nonrenormalizable Yukawas in physically consistent SO16² or heterotic E8×E8 examples; perform anomaly, D/F-flatness and SM-chirality validation instead of using a spectral coincidence alone.
