# Forty Points — five physical fronts and an exact 27-mode cubic-root clock

**Date:** November 8, 2026. **Repository:** wilcompute/W33-Theory (master).  
**Producer:** [w33_20261108_forty_points_fivefronts.py](w33_20261108_forty_points_fivefronts.py).  
**Tests:** [focused regressions](../tests/test_w33_20261108_forty_points_fivefronts.py).  
**Workflow:** [CI certificate](../.github/workflows/w33_20261108_forty_points_fivefronts.yml).  
**Prospective freeze:** [27-mode null-clock registry](../data/w33_20261108_nullclock_prospective_registry.json).

**Evidence boundary.** Exact finite algebra, a constructed action, a conditional flavor model, a relative RG scale, an algebraic source audit, and a prospective optical engineering benchmark are different kinds of evidence. This pass does not derive alpha, measured particle masses, a Standard Model vacuum, Newton's constant or a physical continuum space-time.

## Document and corpus intake

The authorized desktop parsed **all 215 PDF pages** of [Forty Points](../papers/forty_points/main.pdf) into text (673,091 extractable characters, zero empty pages) and rendered thirteen representative pages to inspect figures and mathematical layout. The PDF binary SHA-256 was 003b75482b6584e20e83a55d9e9ba0a181f93b8dff0f94c1d615039c21213cbb. A separate GitHub Actions job independently verified 215 pages and **all twenty recursive TeX source files**, including main.tex, 15 narrative/appendix inputs and four TikZ figure fragments; its independent MuPDF extraction yielded 673,122 characters. Different extraction-version counts are not physical results.

The relevant pre-existing owners were read and credited: the September 24 null-history spectral clock (27 vertices, spectral order three), Pass11166 (the tick is Clifford but not a perfect scrambler), Pass11541 (the formally self-dual quadratic-shell association scheme), the October 19 absolute-scale no-go, the October 1 actual D-flat E6 81-by-81 mass pencil, and the CP/modular/heterotic no-go sections of this paper. On the desktop, the existing E6 mass-pencil script's --check **passed**, without changing its certified output.

## Outside-box theorem: the 27-mode clock is BH(27,3)

Label the 27 events by symmetric matrices over the three-element field:
\[
S=\begin{pmatrix}a&b\\b&c\end{pmatrix},\qquad q(S)=\det S=ac-b^2 .
\]
Join different S,T when q(S-T)=0. This graph has 27 vertices, degree 8, 108 edges and Laplacian spectrum \(0^1,6^{12},9^8,12^6\). Write \(\omega=\exp(2\pi i/3)\) and \(U=\exp(-2\pi iL/9)\).

**Exact formula obtained from the Fourier-residue census:**
\[
\boxed{\quad U_{S,T}=\frac{e^{-i\pi/6}}{\sqrt{27}}\,\omega^{1+q(S-T)}.\quad}
\]
Consequently all 729 transition probabilities equal \(1/27\), and \(U^3=I\). The scaled matrix \(\sqrt{27}e^{i\pi/6}U\) is a cubic-root complex Hadamard matrix, BH(27,3).

**Exact proof certificate.** Pick one representative of each of four pairs of nonzero null vectors ±n. For dual Fourier character k, let n0(k) count how many such representatives are orthogonal to k. The adjacency eigenvalue is \(3n_0(k)-4\); the tick eigenphase is \(\omega^{n_0(k)-4}\). In the finite inverse transform, the three residue counts \((C_0,C_1,C_2)\) are:

| Difference shell | Number of d | Residue counts | U amplitude |
| --- | ---: | --- | --- |
| d=0 | 1 | 9,12,6 | \(i\sqrt3/9\) |
| q(d)=0, d nonzero | 8 | 9,12,6 | \(i\sqrt3/9\) |
| q(d)=1 | 6 | 6,9,12 | \(-1/6-i\sqrt3/18\) |
| q(d)=2 | 12 | 12,6,9 | \(1/6-i\sqrt3/18\) |

Since \(1+\omega+\omega^2=0\), the table proves the boxed formula without floating point. Separately reconstructing the full 27-by-27 matrix numerically verifies the kernel, flatness and order-three property near machine precision. Pairwise row orthogonality also follows from a nontrivial finite character sum of a nondegenerate quadratic form.

**The subtle chart change.** Put \(t=(a+c)/2,\ x=(a-c)/2,\ y=b\), valid over F3. Then \(q=t^2-x^2-y^2\). In this diagonal chart the unitary factors, up to a global phase, into three single-qutrit Clifford chirps
\[
H_\sigma(j,k)=3^{-1/2}\omega^{\sigma(j-k)^2},\qquad
U_{\rm diag}=\omega e^{-i\pi/6}(H_+\otimes H_-\otimes H_-).
\]
But this is a **nonlocal tensor-coordinate change**. In the original (a,b,c) qutrit factors, \(U|000\rangle\) contains one trit of entanglement between a and c and leaves b pure. This agrees with Pass11166's prior nonlocal information-flow result. A chart-dependent factorization is not an assertion that the native physical operation is local.

**Interferometric prediction without phase-gauge ambiguity:** the normalized 2-input/2-output closed plaquette equals
\[
\frac{U_{ac}U_{bd}U_{ad}^*U_{bc}^*}{|U_{ac}U_{bd}U_{ad}^*U_{bc}^*|}
=\omega^{B(a-b,d-c)},
\]
where \(B(v,w)=q(v+w)-q(v)-q(w)\). Three frozen plaquettes take values \(\omega,\omega^2,1\). They complement the 729 flat output probabilities.

**Priority firewall.** Existing passes already prove the spectral clock, Clifford character and exact quadratic association scheme. A targeted result/formula search found no explicit BH(27,3) quadratic kernel and all-pairs flat-mixing proof in the repository, but this is standard finite Gaussian harmonic analysis. The claim is a **new explicit certificate and optical interpretation in this repo**, not priority over classical mathematics.

## Front 1. A gauge-invariant finite action, but no alpha derivation

The null graph has exactly 36 edge-disjoint triangular faces. Oriented boundary maps satisfy
\[
\partial_1\partial_2=0,\quad
\mathrm{rank}\partial_1=26,\quad
\mathrm{rank}\partial_2=36,\quad
\dim H^1=108-26-36=46.
\]
For edge potential A take \(F=\partial_2^TA\) and \(S_g=(4g^2)^{-1}\|F\|^2\).
It is invariant under \(A\mapsto A+\partial_1^T\lambda\), verified with nontrivial deterministic fields. But g=1 and g=2 obey all identical incidence and gauge identities while changing the action by a factor four. The gauge coupling remains a **free normalization**: physical alpha requires a normalized matter charge, kinetic action and RG prescription. The 46 harmonic 1-cycles do not imply 46 photons.

## Front 2. Sparse qutrit Nelson–Barr mass block (conditional) and native E6 check

The repository's existing actual signed E6 mass pencil and D-flat normalization passed its independent --check on the authorized desktop. Its 81-by-81 skew Yukawa map has not been identified with down-quark masses. A new *toy* 3+1 Nelson–Barr example instead uses
\[
Y_d=\operatorname{diag}(1,2,4)+(X+X^T)/3,\qquad
M_d=\begin{pmatrix}Y_d&0\\(1,\omega,-1)&5\end{pmatrix},
\]
where X is the cyclic qutrit shift. Exact symbolic calculation yields
\[
\boxed{\det M_d=985/27>0}
\]
and, in a real diagonal up-type basis, for the Hermitian Schur complement of the heavy mass-squared block,
\[
\boxed{\operatorname{Im}[(H_{\rm eff})_{12}(H_{\rm eff})_{23}(H_{\rm eff})_{31}]
=-170449\sqrt3/571536\ne0.}
\]
The same CP witness is zero for a real vectorlike row. Thus a complex qutrit-root row and tree-level real mass determinant can coexist in a concrete 4-by-4 example, consistent with **the already-known Nelson–Barr mechanism**. The entries, heavy scale, up-sector choice and phase are **inputs**. No actual E6 embedding, vacuum selection, anomaly closure, measured CKM/PMNS vector, or radiative strong-CP protection has been shown. See Murai–Nakayama (JHEP 11 (2024) 098), and the 2025 Nelson–Barr EFT one-loop matching paper (JHEP 09 (2025) 162): the loop/quality problem cannot be ignored.

## Front 3. Dimensional transmutation worked, but a physical absolute scale is not fixed

Choose as an **external assumption** the one-loop beta equation \(\mu\,dg/d\mu=-b_0g^3/(16\pi^2)\). Then
\[
\Lambda=\mu_{\rm ref}\exp[-8\pi^2/(b_0g^2(\mu_{\rm ref}))].
\]
The code evaluates nine supplied combinations with b0 in 7,9,11 and g-squared in 1/4,1/2,1. These give nonzero but widely different scale ratios. A physical reference, matter content and coupling boundary condition are still independent inputs. Dimensional transmutation does not rescue an absolute-scale claim made from a finite graph alone. This does **not** rule out a richer UV theory that fixes the boundary dynamically.

## Front 4. Canonical arithmetic provenance with source lines

The source provides a safe AST-based exact-rational parser (no eval and no arbitrary function execution). It reduces hand-selected competing alpha/weak-angle formulas to canonical Fractions, rejects malformed or executable expressions, and scans the **entire existing natural-constants catalog** for additional parseable rational/additive corrections, grouping arithmetically identical aliases with source line witnesses. It does not treat identical numbers for different observables as one physical derivation, and does not normalize all TeX symbols, loops, thresholds, or units. The full repository's pre-existing syntactic 37,506-file formula census remains the selection/multiplicity firewall. The CODATA-2022 alpha residuals for three alternatives remain approximately -4.40, +0.23 and +210.64 standard deviations; post-hoc switching is not prospective physics.

## Front 5. Pre-frozen optical protocol for the 27-mode clock

The [preregistration JSON](../data/w33_20261108_nullclock_prospective_registry.json) fixes all 27 input rows, all 729 probability cells at exactly 1/27, four shell sums (1/27,8/27,6/27,12/27), three closed plaquette phases (omega, omega-squared, unity), a minimum of 5000 heralded accepted detections per input, calibration, a joint multinomial/Holm rule, and concrete graph/time/loss comparators. **No laboratory counts have yet been acquired.** Building the specified circuit would test ordinary quantum-mechanical predictions for a finite geometry. It cannot distinguish a TOE from standard QM by itself.

## Verification receipt

- Authorized Windows desktop: initial nine source tests **9/9 passed**; native D-flat E6 mass-pencil --check passed independently; all 215 PDF pages parsed and representative pages rendered.
- GitHub Actions run [42492600401](https://github.com/wilcompute/W33-Theory/actions/runs/42492600401): **success**, nine tests plus independent PDF/TeX recursive coverage and uploaded machine-readable research certificates.
- A tenth regression for catalog-wide rational aliases was subsequently added; require its later CI success before claiming that extended parser is certified.
- Existing dirty files in the authorized local repository are unrelated parallel work and were not overwritten or staged.

## Five best independent next steps

1. **Gauge-mode selection:** classify the 46 finite gauge harmonic modes as modules under the actual clock/Albert stabilizer, then test whether a unique light sector can be isolated without injecting a coupling.
2. **Actual E6–Nelson–Barr bridge:** map explicit chiral E6 representations and the D-flat 81-field mass pencil into a valid vectorlike block and compute the first radiative strong-CP correction.
3. **Higher-q and continuum:** test the quadratic-flat-clock condition over odd finite fields and graph towers, and whether their small-momentum spectra yield a controlled emergent Lorentzian propagation law.
4. **Algebraic source graph:** expand exact formula aliasing to parameterized symbolic/renormalization comparisons, chronological proof ownership and retractions; quarantine all target-contaminated expressions.
5. **Optical realization and independent holdout:** build a 27-port architecture with plaquette interferometry and a closed calibration plan, then collect data with no post-hoc graph relabeling or tick adjustments.
