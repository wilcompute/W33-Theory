# Five-front follow-through: harmonic sectors, E6 rank obstruction, higher-q no-go, provenance and 27-mode optics

**November 8, 2026.** Code: analysis/w33_20261108_fivefront_continuation.py. Tests: tests/test_w33_20261108_fivefront_continuation.py. GitHub workflow: .github/workflows/w33_20261108_fivefront_continuation.yml. JSON certificate: data/w33_20261108_fivefront_continuation.json (also in CI artifact).

This is **mathematical and conditional physics research**. No measured coupling, mass hierarchy, gauge boson, physical vacuum, gravity theory or validated laboratory device is claimed.

## 1. Gauge selection: the exact 46-mode representation

For the 27-vertex affine null complex over F3, choose four representative null directions. At each translation character k the edge-chain space has dimension four, the triangular face-boundary rank is n0(k), and the vertex-boundary rank is one for k nontrivial and zero for k trivial. Thus dim H1(k) = 4 - n0(k) - 1_{k nonzero}. The exact character census is one trivial character with zero harmonic dimension, eight with dimension two, twelve with dimension one and six with dimension three. Total: **46 = 8+8+12+18**.

Under the common PGL(2,3) = S4 clock symmetry, the nonzero character orbits have sizes 4,4,12,6 and harmonic multiplicities 2,2,1,3. The trivial translation character has **zero** harmonic dimension, so the 46-dimensional H1 contains no translation-fixed mode. A photon selector must introduce further physical structure, symmetry breaking or a different complex. It is incorrect to label all 46 modes photons.

Owner context: papers/forty_points/sec04_time.tex, analysis/w33_20260924_null_history_spectral_clock.py, analysis/w33_pass11541_history_quadratic_shell_scheme.py and the preceding PASS20261108_FORTY_POINTS_FIVE_FRONTS.md.

## 2. Actual E6 mass rank versus conditional Nelson–Barr loop sensitivity

The existing native fixture data/w33_20261001_dflat_cartan_mass_loop.json has a skew 81×81 E6 mass operator of rank **78**. Its nonholomorphic dimension-five rank-one correction reaches **79**, leaving **two zero singular values**. Thus the determinant of the full operator is zero, and its strong-CP determinant phase is undefined without a justified light-sector projection and further mass terms. This is a rank obstruction for the **specified native pencil**, not a no-go for all E6 flavor models.

Separately, a fully symbolic four-state Nelson–Barr witness uses a real symmetric Y = diag(1,2,4)+(X+X^T)/3, vectorlike row (1,omega,-1), heavy mass 5 and a zero upper-right 3×1 block. Its unperturbed determinant is 985/27, positive and real. Introducing one **hypothetical real upper-right term** deltaM[0,3] = epsilon gives the exact first-order phase sensitivity

\[
\left.\partial_\epsilon\arg\det(M+\epsilon\,\delta M)\right|_{\epsilon=0}
=\operatorname{Im}\operatorname{Tr}(M^{-1}\delta M)
=\frac{33\sqrt3}{1970}\simeq0.02901405.
\]

If the illustrative external bound 1e-10 is imposed on this phase and no other correction cancels it, the insertion must satisfy |epsilon| about 3.45e-9 or smaller in the toy normalization. This is **not** a computed one-loop coefficient, not a valid native E6 insertion yet, and not a quark-mass prediction. The next obstacle is to derive the symmetry or UV mechanism that forbids/suppresses the insertion. Useful external references: Phys Rev D 108 (2023) 015010, DOI 10.1103/PhysRevD.108.015010; Phys Rev D 114 (2026) 015025, DOI 10.1103/sy92-fyjf.

## 3. Higher-q uniform-mixing theorem: special role of three

Let q be an **odd prime power** and take the unweighted Cayley graph on Sym2(Fq) whose distinct matrices S,T are adjacent exactly when det(S-T)=0. It has q^3 vertices, valency q^2-1 and four adjacency eigenspaces with eigenvalues q^2-1, -1, q-1, -(q+1).

For one of the two non-null displacement classes, quadratic Gauss summation gives spectral-projector character coefficients

\[
(1,\ q-1,\ -q,\ 0).
\]

This can be derived by calculating the character sum over the nontrivial dual null cone (= q-1 on the chosen anisotropic class) and using both Fourier orthogonality and the identity A(0,d)=0 for nonadjacent d. Hence for **every real time t**, with L=(q^2-1)I-A,

\[
U_t(0,d)=q^{-3}[1+(q-1)e^{-iq^2t}-q e^{-i(q^2-q)t}]
\quad\Rightarrow\quad
|U_t(0,d)|\le2/q^2.
\]

Uniform mixing would require absolute amplitude q^{-3/2} for every pair. Since 2/q^2 < q^{-3/2} whenever q>4, **exact instantaneous uniform mixing of this unweighted null-graph family is impossible for all odd prime powers q >=5, at any time**. The q=3 case is not excluded and achieves uniform mixing at 2pi/9. Independent Fourier enumeration verified q=3,5,7,11, covering 27,125,343,1331 vertices.

The conclusion does **not** cover weighted graphs, other Hamiltonians, all finite-geometry continua, or actual physical Lorentz invariance. Related general background: Godsil, Mullin and Roy, *Uniform Mixing and Association Schemes* (2017), DOI 10.37236/4745; Coutinho and Guo, *Selected open problems in continuous-time quantum walks* (2024), DOI 10.1515/spma-2024-0025. We claim a repo-specific derivation and certificate, not uninvestigated priority over published quantum-walk mathematics.

## 4. Source and provenance audit, with a strict honesty boundary

The producer checks four specified current sources (constants derivation catalog, standalone constants companion, docs website and Forty Points physics TeX) for six candidate/formula/status families, retaining path and line number. On the authorized desktop, **nine** source lines matched.

These are **current source-line witnesses**, not earliest originating commits, not a 37,506-file historical or semantic ledger, and not independent evidence for any measured constant. Current file presence cannot substitute for a chronological, rename-aware Git audit. A future full-history task is separately required before assigning first discovery ownership.

## 5. Structured 27-rail optical compiler and two synthetic controls

Label three independent logical qutrit coordinates (a,b,c). Apply two reversible SUM operations, c <- c+2a then a <- a+2c (mod 3, with updated c). This gives the diagonal quadratic chart (t,b,x) with det = t^2-b^2-x^2. Write H_sigma(i,j)=omega^[sigma(i-j)^2]/sqrt(3). Then the exact spectral-clock unitary is

\[
U=\omega e^{-i\pi/6}P^{-1}(H_+\otimes H_-\otimes H_-)P.
\]

In a 27-rail implementation this is **four SUM permutation networks, 27 three-port tritters** (nine repetitions of each local gate) and local phase adjustments. Each three-port unitary admits an upper bound of three two-mode MZI blocks: **81 MZIs** across local layers versus **351** for a generic arbitrary 27×27 mesh, excluding routing, crossings and loss. No non-Clifford state or gate is required. The exact 27×27 matrix residual is about 2.24e-16.

Synthetic controls: a local 0.08-radian tritter error changes some predicted port probability by about 0.00590; a 0.03-radian tick-time drift changes a probability by about 0.00235. No actual photonic chip or lab measurement was operated. Ordinary quantum mechanics predicts the same clock if the specified circuit is physically implemented.

## Verification

The authorized Windows desktop fast-forwarded to the new source/tests without altering existing uncommitted work, generated the five-front certificate, and returned **13/13 focused tests passed**. GitHub Actions will independently test and publish the certificate. Preserve the distinction between GitHub CI success, desktop tests, exact arithmetic and physical observation.

## Five independent research next steps

1. Construct a genuine E6 charge and field-sector projection from the 81×81 mass pencil; test UV loop-induced strong CP.
2. Search weighted finite-light-cone Hamiltonians that evade the proven unweighted no-go and have credible continuum dispersion.
3. Use the 46-mode S4 harmonic census to design and falsify a unique matter-coupled gauge selector.
4. Build a full-history, rename-aware and scheme-aware derivation provenance database for constant candidates.
5. Produce a fabrication-level 27-port circuit layout, realistic phase/loss/noise budget and preregistered blinded optical experiment.
