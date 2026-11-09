# Native H27 Wilson-orbit mass selection: no isolated symmetric scalar, two doublets instead

**Date:** November 8, 2026.  
**Producer:** analysis/w33_20261108_h27_symmetrized_wilson_rank.py  
**Regression suite:** tests/test_w33_20261108_h27_symmetrized_wilson_rank.py (nine passing on authorized desktop).  
**CI:** .github/workflows/w33_20261108_h27_wilson_mass.yml.  
**Certificate:** data/w33_20261108_h27_symmetrized_wilson_rank.json (exact rational strings and integer charge lattices).

**Claim class:** Exact representation-theoretic selection rule for a *declared* positive, compact Wilson-loop potential on the existing four-holonomy space. **Not** a derivation of a physical photon, Higgs mass, compactification, E6 vacuum, gravitational scale or TOE.

## What's new relative to the parallel work

Pass 11991 already owns the **native 27-element H27 action** on the four real harmonic holonomies, its two inequivalent real two-dimensional C3 character planes, and the positive electric/acoustic metric. The November 8 coupled-scalar continuation already finds two doubly degenerate mass poles on the externally fixed equal four-period torus, and the latest native temporal Gauss report points out that selecting 105 independent magnetic face constraints with equal weights breaks 26/27 controller actions even though weighting all 1287 short faces equally preserves the full group. The prior four-dimensional-to-three-dimensional gauge bridge assumed a supplied quadratic mass for one selected Wilson scalar; the subsequent full-band scalar loop dynamically induces a periodic potential but does not select the compactification.

This pass asks a different exact question: **can a positive mass term for precisely one selected holonomy coordinate preserve the full native H27 controller?** We construct the symmetry orbit, its integer charge lattice and generalized spectrum for all four coordinate choices. The answer is **no**. Symmetry averaging an arbitrary chosen rank-one Wilson Hessian gives rank two or rank four, never rank one.

## 1. Exact finite group average

Let R_g be the native integer 4-by-4 action from data/w33_pass11991_native_four_period_cover.json. Its 27 controller elements act through **nine distinct matrices** on this four-holonomy representation (the central kernel acts trivially).

Choose a standard coordinate covector e_i and propose the positive periodic orbit potential

\[
V_i(\Theta)=\frac{\mu^2}{27}\sum_{g\in H_{27}}
\left[1-\cos((R_g^Te_i)^T\Theta)\right].
\]

Every term is a nonnegative, integer-charged Wilson cosine with gauge-periodic arguments. The Hessian at the trivial holonomy is \(\mu^2B_i\), where

\[
B_i=\frac1{27}\sum_{g\in H_{27}}(R_g^Te_i)(R_g^Te_i)^T.
\]

Direct enumeration gives **orbit charge counts [3,3,9,9]** and **Hessian ranks [2,2,4,4]**. All symmetry orbit charges repeat uniformly: 9 times each for the first two coordinates, 3 times each for the last two.

For either coordinate i=1 or i=2 (one-indexed),

\[
B_1=B_2=\frac1{27}
\begin{pmatrix}
18&9&0&0\\
9&18&0&0\\
0&0&0&0\\
0&0&0&0
\end{pmatrix}, \qquad \operatorname{rank}B_1=2.
\]

For i=3 or i=4,

\[
\boxed{
B_3=B_4=\frac1{27}
\begin{pmatrix}
12&6&-9&0\\
6&12&0&-9\\
-9&0&18&-9\\
0&-9&-9&18
\end{pmatrix}
},\quad \det B_4=\frac1{81}>0.
\]

Thus one selected Wilson direction either *gaps a two-dimensional sector* or gaps the *entire* four-dimensional static holonomy space. It cannot gap just one H27-invariant static mode.

## 2. Doublet mass ratios in the native kinetic metric

For the prior equal-period [2,2,2,2] case, and supplied g=1 kinetic convention, the exact electric inertia is the existing metric G=M/2, with

\[
M=\begin{pmatrix}
10&5&-6&0\\5&10&0&-6\\-6&0&12&-6\\0&-6&-6&12
\end{pmatrix}.
\]

Using the exact real two-dimensional character projectors P_A and P_B, the Hessian is

\[
B_1=G\,\frac29 P_A,\qquad
B_4=G\left(\frac2{27}P_A+\frac19P_B\right).
\]

These identities were verified **entry by entry with rational arithmetic**, not fitted from eigenvalues. Hence the exact generalized squared-frequency spectra, in units of the supplied \(\mu^2\), are

\[
\operatorname{spec}(G^{-1}B_1)=\{0,0,2/9,2/9\},
\]
\[
\boxed{\operatorname{spec}(G^{-1}B_4)=\{2/27,2/27,1/9,1/9\}.}
\]

The two doublets are inequivalent real representations. A full H27-invariant positive quadratic deformation is scalar on each irreducible plane; nonzero rank one or three is forbidden. This does **not** imply a continuum Lorentz two-polarization photon or real-world particle degeneracy.

## 3. Stronger integer-lattice statement: the nine charges select a unique minimum

The integer Smith normal form of the nine distinct e4 orbit-charge rows is

\[
\operatorname{SNF}(Q_4)=\operatorname{diag}(1,1,1,1).
\]

Their \(\mathbb Z\)-linear span is therefore **all of \(\mathbb Z^4\)**. Since all nine cosine terms are nonnegative and simultaneously zero only when each charge phase is an integer multiple of \(2\pi\), the potential V4 has exactly **one global minimum on the four-holonomy torus**:

\[
\Theta\equiv(0,0,0,0)\pmod{2\pi}.
\]

For the first two coordinates, the charge lattice has rank two with SNF diag(1,1), leaving a continuous two-torus of minima. This is a global topological distinction, stronger than the local Hessian rank alone: a full-rank Hessian can still permit several inequivalent periodic minima, whereas the primitive Smith invariants exclude them here.

## 4. What this means for the four-to-three-dimensional proposal

The prior demonstration of two transverse 3D gauge modes plus one gapped Wilson scalar was explicitly conditional on compactifying the fourth axis and adding a selected Wilson-line mass. **If that potential must retain the full equal-torus H27 action, its rank-one mass is forbidden**. The H27-invariant orbit average instead yields two massive doublets. A physically meaningful model must therefore choose and document a symmetry-breaking compactification, matter charge asymmetry, or background that allows one distinguished compact direction.

This is not a contradiction of the prior scalar one-loop results, which already show the equal four-period scalar action yields symmetry-protected doublets. It is a precise consistency requirement explaining *why a one-scalar compactification is an additional physical assumption*, not a consequence of H27 symmetry.

The recent native 135-link report makes a parallel point for magnetic terms: linear independence of 105 chosen constraints does not imply that giving each the same coefficient is H27 invariant. The Wilson-orbit analysis independently reveals the same **action versus basis** selection issue in the compact scalar mass sector.

## Evidence and directions

Inputs are only the repository's committed Pass11991 exact matrices/metric. An authorized Windows desktop ran **9/9** focused regressions in C:\Temp, leaving the working checkout and parallel uncommitted files untouched. GitHub CI independently validates these formulas when its workflow completes; desktop results alone do not imply CI success.

**Five independent experiments:**
1. Search symmetry-breaking compactification orbits that distinguish one primitive period and classify their stabilizers, dynamical mass patterns and radius selection.
2. Test all-face H27-invariant magnetic weights *together with* the engineered small-momentum propagation cone; preserving zero-momentum symmetry does not guarantee identical dispersion slopes.
3. Couple nonuniform, gauge-charge-consistent scalar inventories and compute full native 135-link temporal Gauss Ward identities at nonzero external momenta, rather than extrapolating from k=0.
4. Find a rank-three E6 mass mechanism from a specified F/D-flat, anomaly-free vacuum without determinant-phase tuning.
5. Check the new S8 DES/KiDS high-z prediction with a source-preserving, nonlinear power/geometry attribution and fully calibrated raw survey covariance.
