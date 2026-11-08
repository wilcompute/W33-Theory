# Five boundary bridges: compact gauge, E6 Pfaffian, quantum speed, one-photon cost, and S7 integrity

**Date:** 2026-11-08. **Producer:** analysis/w33_20261108_five_boundary_bridges.py. **Tests:** tests/test_w33_20261108_five_boundary_bridges.py (19 focused cases). **CI:** .github/workflows/w33_20261108_five_boundary_bridges.yml.

**Verification:** The independent server-side checks passed for the exact gauge characteristic polynomials at three momenta, a synthetic finite complex Pfaffian identity and corank-one counterexample, q=5 Hermitian null hopping and its Taylor bound, and 27-mode Gaussian unitarity. The user-authorized desktop stopped responding before the entire native 81-state and S7 file-backed suite could be run. GitHub CI is queued. **The 19-case full-suite success and a native E6/PPD certificate are NOT claimed yet.**

## 1. A real three-space mode-count completion from the prior native four-space cone

**Prior ownership:** The actual 135-link periodic-cover gauge propagation, 105 short-face rows, extra mixed loops, engineered common cone and proof boundaries were already established in analysis/2026-10-27_native_gauge_propagation_completion.md and analysis/2026-10-28_three_mixed_loop_minimal_maxwell.md. The more recent 108-edge static-triangle obstruction does not supersede them.

Use the published native harmonic metric and engineered leading magnetic symbol:

\[
M=\begin{pmatrix}10&5&-6&0\\5&10&0&-6\\-6&0&12&-6\\0&-6&-6&12\end{pmatrix},
\quad
K(k)=\frac{(k^TMk)M-(Mk)(Mk)^T}{27}.
\]

The generalized spectrum has one gauge zero and three degenerate transverse squared frequencies \(k^TMk/27\), for nonzero four-space k in the leading continuum expansion. **Assume** an external compactification selecting k4=0. The fourth component is then a Wilson-line scalar under the reduced periodic gauge symmetry; it does not disappear by gauge fixing.

**Supplied**, not derived, a Wilson-holonomy effective potential with quadratic term \(\mu^2 A_4^2/2\) on this zero-mode theory. Since \((M^{-1})_{44}=5/27\), the exact spectrum becomes

\[
\boxed{0_{\rm gauge},\quad
  \lambda(k),\quad \lambda(k),\quad
  \lambda(k)+5\mu^2/27},\qquad
\lambda(k)=k^TMk/27,\quad k_4=0.
\]

Two transverse 3D modes remain; one scalar receives a gap. For the illustrative input \(\mu^2=1/5\), the gap is 1/27. Exact independent SymPy checks: k=(1,0,0,0) gives 10/27 and 11/27; k=(1,2,3,0) gives 142/27 and 143/27; k=(2,-1,1,0) gives 2/3 and 19/27. The determinant of M is 2916.

**Critical limitation:** An \(A_4^2\) mass is not a local invariant of unrestricted 4D gauge transformations, since at k4≠0 it breaks the gauge null direction. A legitimate UV theory must generate it through a periodic, gauge-invariant Wilson-loop effect, with charges and matter specified. The compactification, potential, physical units and coupling are supplied. This is a mathematical completion, not a photon discovery.

## 2. E6 rank-three scalar repair has an augmented Pfaffian-square and no automatic CP solution

**Prior ownership:** The actual 1,620 signed records and rank-78 skew 81×81 E6 mass map originate in analysis/w33_pass11218_e8_cubic_cartan_kernel.py; a single nonholomorphic E6-invariant-form rank-one perturbation was already supplied by analysis/w33_20261001_dflat_cartan_mass_loop.py. The 2026-11-08 five-physics-gates script already exhibited generic three-spurion rank81. This pass adds a corank-specific augmented-Pfaffian diagnostic and a counterexample that prevents an overly broad theorem.

For every 81×81 skew matrix M of corank **at least 3** and arbitrary complex 81×3 U,

\[
\boxed{\det(M+UU^T)=
\operatorname{Pf}\begin{pmatrix}M&U\\-U^T&0_{3}\end{pmatrix}^{2}.}
\]

One proof brings M by congruence to a nondegenerate 78×78 skew block and a zero 3×3 block. With only three rank-one insertions, all lower-order determinant terms vanish. The remaining term is the square of the augmented signed Pfaffian minor sum. The result extends to lower rank by polynomial continuity. This is a specific application of established Pfaffian algebra, not a claim to original discovery.

**Essential adversarial exact example:** For 3×3 skew M with M12=2 and corank one, and U with rows (1,2,3),(2,0,1),(3,-1,2), det(M+UU^T)=105 whereas the six-by-six augmented Pfaffian squared is 49. So an unconditional statement for *any* skew M is **false**. The code now explicitly tests this failure.

For a true corank-three mass map, the determinant phase is **twice the augmented Pfaffian phase**. Rephasing one scalar column rotates the Pfaffian linearly and the determinant twice. This does not force real masses or theta-bar=0. The full native 84×84 floating certificate is authored, but its execution on the user's native 1,620 records is still awaiting the desktop/CI check. A physical conclusion would require gauge charges, chiral quark branching, anomaly accounting, a D/F-flat dynamical vacuum and radiative strong-CP calculation.

## 3. Strict null locality enforces a time–energy floor even without symmetry

If a Hermitian H has an off-diagonal pair H_ij=0 and the evolution is supposed to give uniform amplitude q^-3/2 there, then

\[
|e^{-itH}_{ij}|=|(e^{-itH}-I+itH)_{ij}|
\le \frac{t^2\|H\|_{\rm op}^2}{2},
\]

where the inequality is the scalar Taylor bound for Hermitian functional calculus. Thus

\[
\boxed{|t|\|H\|_{\rm op}\ge\sqrt2\,q^{-3/4}.}
\]

At q=5 the value is 0.42294850537622564. Unlike the preceding affine-GL2 no-go, this holds for any Hermitian H with one forbidden direct transition: arbitrary complex couplings, no translation symmetry, arbitrary anisotropy. It is a **necessary speed/resource bound, not a proof of no mixing at all times**. The independent server-side complex 24-null-hop convolution control gave off-support amplitudes 0.000036539, 0.000146895, 0.000930597 for normalized times 0.05, 0.1, 0.25, safely below respective ceilings 0.00125, 0.005, 0.03125.

## 4. Non-Clifford one-photon phases do not establish scalable BQP

**Prior ownership:** analysis/w33_20260924_photonic_universality_architecture_atlas.py had already identified 3^n single-photon orthogonal modes for n qutrits. The 2026-10-23 single-photon recursive-register study independently warns of exponentially many independently accessible time-bin addresses.

The phase \(T=\operatorname{diag}(1,\zeta_9,\zeta_9^{-1})\) is a mathematical **non-Clifford** gate relative to the logical qutrit stabilizer structure. In a one-photon path-mode implementation, however, it is simply a diagonal phase-shifter: arbitrary one-particle paths still form an N-vector, and passive optical gates are N×N unitaries. A classical emulator updates this vector and samples ordinary projective adaptive measurements with outcome-dependent feedforward in time polynomial in N and gate count. Non-Clifford Wigner magic therefore does **not** make a single-particle, polynomial-mode optical circuit asymptotically quantum hard.

An injective n-qutrit register requires **N>=3^n modes**: 3 qutrits=27 modes; 5=243; 10=59,049; 15=14,348,907; 20=3,486,784,401. Independent server-side verification of the frozen 27×27 Gauss-convolution unitary gave a matrix-unitarity residual below 10^-15. The authored test also simulates ninth-root phases, one addressed projective measurement and conditioned feedforward.

This does not constrain genuinely interacting stationary quantum memories, nonlinear photon–matter gates, multiphoton resources, unbounded CV systems, or probabilities conditioned on exponentially rare events. For a scalable **single flying-photon bus**, a stationary register and verified entangling interface are necessary additions, not optional decorations.

External context: Aaronson–Arkhipov, *The Computational Complexity of Linear Optics*, Theory of Computing 9 (2013), https://www.theoryofcomputing.org/articles/v009a004/; Moyano-Fernández and Garcia-Escartin, *Linear optics only allows every possible quantum operation for one photon or one port*, Optics Communications 382 (2017).

## 5. Frozen S7 tomography and KLT PPD evidence integrity

The S7 tomographic shear-tilt **forecast**, not a new measurement, was already frozen in analysis/toe_uv/prereg_tilt.json with a companion SHA256. The new code checks that signature and extracts a *derived* amplitude-independent low/high contrast without altering the frozen claim:

\[
D=\log\!\frac{(\xi_+^{\rm low}/\xi_+^{\rm high})_{\rm CPL}}
                 {(\xi_+^{\rm low}/\xi_+^{\rm high})_{\rm fading}}
=\log(1+r_{00})-\log(1+r_{\rm highest}).
\]

Using only frozen ratios gives **D_DES = -0.042088887293098426** and **D_KiDS = -0.0505380482685487**. Common overall amplitude factors cancel, but tomographic calibration/redshift and survey cross-covariance do not. These are *predictions generated from already fitted data*, not independent held-out validation of S7.

The concurrent KLT PPD snapshots show differing accepted draw counts and CLASS solver failures:
- BAO KLT f=0.25 inflation-width-one: 18 accepted, 6 solver failures.
- SN KLT f=0.25 width-one: 12 accepted, 12 failures.
- SN KLT width-two: 10 accepted, 14 failures.

A failed CLASS shooting bracket is not a mathematical nonexistence result. Unequal accepted samples and potentially nonrandom missingness prevent calibrated log-score comparisons without a common sampling/likelihood protocol. The full original KiDS/DES likelihoods, nuisance covariance, overlapping footprint and genuinely future shear release remain necessary.

## What has actually been accomplished

**Committed:** A source module covering five orthogonal fronts, 19 adversarial tests, a GitHub Actions workflow, and this report. Exact source-independent checks of the compact gauge spectrum, null-local speed and one-photon 27-mode unitarity have succeeded. The Pfaffian identity was separately validated on synthetic exact/numerical examples and restricted after a counterexample. **Not verified:** the full native 81-state E6 numerical run, source-backed S7 SHA file check, and all 19 integrated tests; the authorized desktop stopped responding and GitHub Actions remained queued. These should not be marked passed by a later report without a successful execution receipt.

### Top five independent further investigations

1. Derive an actual Wilson-holonomy potential from native compact U(1) charged-matter loops and verify 2+1 splitting on the entire 135-link Bloch operator, not merely its leading 4×4 metric.
2. Use the 84-dimensional augmented Pfaffian to track a **real physical quark** determinant and its anomalous CP rephasings in an anomaly-checked E6 vacuum.
3. Optimize complex null-supported H subject to an explicitly normalized time–energy bound, separating exact algebraic obstructions from numerical local minima.
4. Demonstrate a reusable photon–stationary-memory entangling gate or multiphoton fusion primitive with success rate/loss/QEC, rather than just deterministic one-particle phase shifters.
5. Score frozen S7 on independent DES Y6/HSC/KiDS COSEBI/Euclid data with complete covariance and repair KLT shooting selection bias before interpreting model comparisons.

**No physical particle, measured mass, cosmological detection, quantum computational advantage or TOE is claimed.**
