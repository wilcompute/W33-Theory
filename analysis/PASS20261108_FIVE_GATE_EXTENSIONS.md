# Five physics gates, plus H27: exact extensions and empirical boundary

> **CORRECTION / PHYSICAL WITHDRAWAL — PASS12632, 2026-11-08.** Section 5's DES/KiDS shear and S8 Shapley *model ranking* is withdrawn because it used the defective CLASS scalar-field nonlinear spectrum. The old chi-square arithmetic is only a historical replay, NOT valid physical evidence. Sections 1–4 and 6 retain their separately scoped mathematical/synthetic status. See `analysis/PASS12632_HALOFIT_SCF_BUG.md` and `analysis/PASS20261108_FIVE_PHYSICAL_FALSIFIERS.md`.

Date: 2026-11-08. Producer: `analysis/w33_20261108_five_gate_extensions.py`. Regression: `tests/test_w33_20261108_five_gate_extensions.py`. Machine-generated certificate: `data/w33_20261108_five_gate_extensions.json`.

**Status:** Five independent follow-on physics gates executed against the *native* W33 repository plus a sixth exact-arithmetic H27 orbit audit. Geometry and E6 claims below are mathematical identities or numerical consistency witnesses, not a constructed photon, confirmed unification theory, successful strong-CP solution, or detection of new cosmology. The photonic study is explicitly synthetic; the shear study replays existing fixed-background certificates, not raw survey likelihoods.

## 1. Local magnetic weights cannot repair the 46-mode harmonic sector

For the actual 27-vertex, 108-edge, 36-face complex, incidence matrices obey
`B1 B2=0`, `rank B1=26`, `B2^T B2=3I36`. The cochain Hodge dimensions are
\[
108=26_{\mathrm{gradient}}+46_{\mathrm{harmonic}}+36_{\mathrm{coexact}}.
\]
For *every* positive diagonal face stiffness `W`,
\[
K_W=B_2WB_2^T,\quad \operatorname{rank}K_W=36,\quad
\operatorname{spec}_{>0}K_W=\{3w_i\}_{i=1}^{36}.
\]
Thus weighting the existing triangle terms changes the 36 frequencies but cannot restore the missing dispersion of the 46 physical harmonic modes. The producer tests nonuniform weights 0.5 to 1.5 and the full eigenspectrum.

A gauge-invariant positive rank-\(r\) perturbation can lift at most \(r\) of those modes. Even an idealized **rank-four** lift leaves \(46-4=42\) harmonic zero modes. The script constructs an actual gauge-orthogonal rank-four projector achieving the upper bound on lifted rank and preserving the 26 gradient gauge directions.

This is a **conditional comparison**, not a physical embedding: the recently certified four-dimensional H27 holonomy carrier is not proven to be a subrepresentation of the Maxwell 46-dimensional harmonic carrier. The new cross-gate no-go says any such rank-four-only attempt is insufficient.

## 2. A time-dependent perturbation budget for the null-local finite clock

The earlier symmetric-background theorem for strictly null-supported, translation-invariant and \(SL_2(q)\)-congruence-covariant Hermitian \(H_0\) gives at the chosen output
\[
|U_0(T)_{0d}|\le 2/q^2.
\]
Let \(H(t)=H_0+E(t)\) with any integrable Hermitian \(E(t)\), including noncommuting or translation-breaking control. Duhamel implies
\[
\|U(T)-U_0(T)\|_{\rm op}\le\int_0^T\|E(t)\|_{\rm op}\,dt.
\]
Perfect uniform amplitudes of magnitude \(q^{-3/2}\) therefore **require**
\[
\boxed{\int_0^T \|E(t)\|_{\rm op}\,dt\ge
\max(0,q^{-3/2}-2/q^2).}
\]
This extends the constant-perturbation bound to arbitrary coherent time-dependent drives, not to a general no-go for all local clock Hamiltonians. The necessary q=5 budget is \((\sqrt5-2)/25\approx0.0094427\). This is an operator-action lower bound; it does not supply an optimizer or experimentally calibrated clock.

## 3. An exact determinant/Pfaffian identity for the native E6 rank-78 mass tensor

Reconstruct the native 81-by-81 complex alternating mass tensor from **1,620 signed cubic records**, with rank 78. Let \(U\) consist of three separate independently chosen 81-component complex spurions. For \(T=\operatorname{diag}(t_1,t_2,t_3)\):
\[
\boxed{
\det(M+UTU^T)=t_1t_2t_3
\det\begin{pmatrix}M&U\\-U^T&0_3\end{pmatrix}.
}
\]
**Proof:** The determinant of \(M+\sum_jt_ju_ju_j^T\) is multiaffine in the three \(t_j\). Every term of degree less than three vanishes because a rank-78 matrix plus fewer than three rank-one matrices is singular in dimension 81. Its single degree-three coefficient equals the determinant of the 84-dimensional alternating augmentation, by direct determinant expansion. The latter is a **Pfaffian square**.

Native numerical replay compares the augmented determinant to four distinct positive coefficient triples, with both log-magnitude and complex phase residuals below \(10^{-6}\). In particular the determinant phase is independent of positive spurion **magnitudes** and is approximately -2.66729529948 rad for the frozen synthetic complex VEVs. Their phases and alignment can change the coefficient. This neither computes the physical \(\bar\theta\) nor resolves strong CP; a physical scalar potential, SM matter branching, CKM/PMNS, anomalies, and loop-order analysis remain absent.

## 4. Correlated optical phase noise: gauge common mode versus physical differential mode

For \(N\) otherwise identical rails with zero-mean multivariate Gaussian phase vector with covariance \(C\), the mean normalized coherent-overlap fidelity is exactly
\[
\boxed{\mathbb E[F]=\frac{1}{N^2}
\sum_{j,k}\exp[-(C_{jj}+C_{kk}-2C_{jk})/2].}
\]
For equal marginal variance \(\sigma^2\) and equicorrelation \(\rho\):
\[
\mathbb E[F]=\frac1N+\left(1-\frac1N\right)e^{-\sigma^2(1-\rho)}.
\]
The code evaluates \(N=27\), \(\sigma=0.30\) rad, \(\rho=0,0.5,0.9,1\) and compares seeded 15,000-shot synthetic Monte Carlo to exact expectations. A fully common phase (\(\rho=1\)) is **unobservable in this interferometric fidelity**, while differential jitter degrades fidelity. Uniform independent erasure/survival \(\eta=0.7\) multiplies *unconditional* success-weighted fidelity by \(\eta\) but not conditional fidelity. No physical integrated 27-port apparatus, photon source, loss matrix, or heralding experiment was demonstrated.

External established anchor: Gross's finite-dimensional Hudson theorem, arXiv:quant-ph/0602001. This gate extends the *noise model*, not the existing proof that ninth-root cubic phase is a qutrit non-Clifford magic resource.

## 5. Exact S8 nonlinear hybrid score replay, without empirical overclaim

Independently re-evaluate the repository's freshly frozen S8 four-model hybrid table. Let \(F\) be fading power+geometry, \(C\) CPL power+geometry, \(P\) CPL power with fading geometry, and \(G\) fading power with CPL geometry. Then
\[
\Delta=C-F,\quad I=C-P-G+F,
\]
\[
\operatorname{Shapley}_{\rm power}=\tfrac12[(P-F)+(C-G)],\quad
\operatorname{Shapley}_{\rm geometry}=\tfrac12[(G-F)+(C-P)].
\]
Their sum equals \(\Delta\) **exactly**, but naive baseline one-factor effects do not add because the interaction is nonzero.

For full, frozen fixed-background χ² differences CPL-minus-fading:
- DES Y3: \(\Delta=2.88448\), Shapley power \(=1.57720\), geometry \(=1.30729\), interaction \(=-1.24824\).
- KiDS-Legacy: \(\Delta=4.50343\), power \(=2.82995\), geometry \(=1.67348\), interaction \(=-0.73082\).

Separately evaluated low/high/mixed tomographic χ² blocks **do not add to the full-data χ² difference**. The source numbers therefore cannot be turned into a marginal significance by assuming independent bins. These are replayed numerical certificate identities, not a new likelihood, evidence ratio, calibrated posterior predictive uncertainty, or independent survey cross-covariance. See source `data/w33_20261108_S8_hybrid_shapley_audit.json` and KiDS-Legacy extended-cosmology publication arXiv:2512.11041.

## 6. Extra: independent H27 integer Smith and generalized mass replay

Recompute Smith normal forms of the integer Wilson-charge orbit matrices and generalized eigenvalues of each mass Hessian against the native positive electric metric \(G\), using SymPy and SciPy (rather than copying the eigenvalues from the source certificate).

- First two coordinate orbits: SNF \([1,1]\); Hessian rank 2; generalized spectrum \(0^2\oplus(2/9)^2\).
- Last two: SNF \([1,1,1,1]\); rank 4; generalized spectrum \((2/27)^2\oplus(1/9)^2\).
- Unit SNF of the latter certifies a unique compact Wilson-cosine minimum modulo \(2\pi\), **conditional on** the supplied positive coupling and the exact orbit charge set.

No dynamics selecting that coupling, compactification radius, electromagnetic field identification, physical vacuum, or continuum prediction is derived.

## Reproduction and exclusions

Run:
`py -3 analysis/w33_20261108_five_gate_extensions.py`
and
`py -3 -m pytest -q tests/test_w33_20261108_five_gate_extensions.py`.

Independent source ledger:
- `analysis/PASS20261108_FIVE_PHYSICS_GATES.md` (previous five-gate baseline).
- `data/w33_20261108_S8_hybrid_shapley_audit.json` (parallel nonlinear shear replay).
- `data/w33_20261108_h27_symmetrized_wilson_rank.json` (parallel Wilson orbit certificate).
- `analysis/w33_20261108_s4_harmonic_qdual.py` and `analysis/w33_pass11218_e8_cubic_cartan_kernel.py` (native complexes).
- Gross (2006): https://arxiv.org/abs/quant-ph/0602001
- KiDS-Legacy (2025): https://arxiv.org/abs/2512.11041
- Nelson–Barr determinant/loop caveats: https://doi.org/10.1103/PhysRevD.108.015010

**Evidence grading:** finite linear algebra and determinant identity (exact); H27 certificate reconstructed and checked (exact finite); seeded optical simulation (synthetic); cosmology four-case algebra (exact within a committed numerical likelihood evaluation); physical TOE claims (unproven).
