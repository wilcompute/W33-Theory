# November 18–19 TOE research: what the H27 sextic SIC vacua do and do not solve

**Scope:** Exact follow-up to `analysis/toe_20261118_H27_S5T2_G2_sextic_center_sequential.py`, after reading `papers/forty_points/main.pdf` (215 pages; complete extracted-text SHA-256 `c60ee86445bdc62f9bcefd9b92fc8daf1eb28abecb5a7c9eadd1bfc9602ae4bc`) and inventory-scanning 372 master commits after 2026-11-11 22:49 EST. The patch inventory scans every diff byte and records each commit; it is not a claim that every theorem in 372 commits has been manually verified. The existing source already identifies the nine projective support-two F-flat vacua as a Weyl–Heisenberg SIC.

## 1. Exact F-terms: algebraic isolation does not imply a mass gap

For a single triplet, take
\[
W=\sum_{i=1}^3\left(x_i^3-\tfrac12x_i^6\right),\qquad
F_i=3x_i^2(1-x_i^3).
\]
Each coordinate is zero or a cube root of unity. Therefore there are exactly 64 affine stationary points, with support counts `[1,9,27,27]`. The 27 support-two vectors give nine projective rays (three vector phases per ray). For support size `k`, `W=k/2`; all 64 F-vacua have zero *global-SUSY F-term energy* with canonical Kähler metric, so the toy potential alone does not energetically select the SIC branch.

At `(x,y,z)=(1,1,0)`, the holomorphic Hessian is `diag(-9,-9,0)`: two massive and one *quadratically massless* chiral complex direction (up to coupling/mass normalization). The third direction is **not** a continuous exact modulus: its F term is `3z²+O(z^5)`, giving quartic `|z|^4` energy. Algebraic isolatedness and quadratic nondegeneracy must not be conflated.

## 2. A single SU(3) fundamental cannot be D-flat

For `tr(T_a T_b)=delta_ab/2`, the SU(3) completeness/Fierz identity gives
\[
\sum_{a=1}^8 (\phi^\dagger T_a\phi)^2
= \tfrac13 (\phi^\dagger\phi)^2.
\]
This is nonzero at every nonzero fundamental triplet; at `(1,1,0)` it is exactly `4/3`. Thus the SIC F-flat vector **by itself** cannot be a D-flat vacuum of a continuous SU(3) gauge theory with only that charged field and standard D terms.

A separate UV issue is stricter: the displayed `W` is H27-invariant but not SU(3)-gauge invariant. The SU(3) element `diag(-1,-1,1)` changes `W(1,0,0)=1/2` to `W(-1,0,0)=-3/2`. One must either realize the finite family symmetry after SU(3) Higgsing, provide covariant spurions/messenger fields, or construct a different gauge-invariant microscopic superpotential.

## 3. A mathematically exact SIC frame as a D-term compensator

Let \(\psi_{ab}=X^b Z^a(1,1,0)/\sqrt2\) for \(a,b\in\mathbb F_3\). The nine states obey
\[
|\langle\psi_j,\psi_k\rangle|^2 =
\begin{cases}1&j=k,\\1/4&j\neq k,\end{cases}
\qquad
\sum_{j=1}^9\psi_j\psi_j^\dagger=3I_3.
\]
For nine **independent** SU(3)-fundamental fields with identical norm, using the nine rays as candidate VEVs gives \(\sum_j \phi_j\phi_j^\dagger\propto I_3\) and **all eight D-terms vanish exactly**. Our unnormalized 9-vector frame has \(\sum_j v_jv_j^\dagger=6I_3\). This supplies a constructive moment-map compensation template, but not an SU(3)-invariant F-flat or physically selected vacuum. A generic equal-norm orthonormal frame also cancels the moment map; the SIC is a symmetric *overcomplete* choice, not a unique solution.

If H27 is gauged, its 27 affine support-two stationary points are symmetry-related representatives rather than 27 independently observable physical vacua. Projectivizing identifies the center phases to nine rays. If H27 is global, distinct degenerate configurations remain possible. Do not identify a projective qutrit measurement orbit with a collection of independent Higgs vacuum sectors without specifying which group is gauged.

## 4. Theory-of-everything relevance and falsifiers

This packet supports a **reusable bridge between quantum-information tight frames and moment-map reduction**, plus a concrete no-go for the single-triplet UV interpretation. It does not produce the SU(3)-invariant multitriplet superpotential, E6 charge compatibility, F/D-flat intersection, anomaly cancellation, chiral fermions, physical gauge spectrum, family Yukawas, singular G2 geometry, or gravitational dynamics. It also does not identify a novel SIC: the plus-fiducial qutrit SIC has appeared in prior quantum-information work (e.g. Planat and collaborators, *Magic informationally complete POVMs with permutations*, R. Soc. Open Sci. 2017).

### Reproduction

`python analysis/toe_20261119_sic_moment_map_audit.py`

`python analysis/toe_20261119_week_commit_patch_inventory.py`

Generated certificates: `data/toe_20261119_sic_moment_map_audit.json`, `data/toe_20261119_week_commit_patch_inventory.json`.

The finite source uses only existing H27 toy equations; no protected manuscript, source, or parallel tracked work was modified.
