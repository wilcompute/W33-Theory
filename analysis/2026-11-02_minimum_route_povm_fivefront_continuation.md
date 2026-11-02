# Five-front continuation: minimum-route designs, finite quantum measurements, and the TOE boundary

**Date:** 2026-11-02. **Status:** exact finite calculations and finite-dimensional operator algebra; no continuum or particle-physics identification.  
**Reproducers:** `analysis/w33_20261102_povm_spectrum_and_duality.py`, `analysis/w33_20261102_q5_route_orbit_moments.py`, `analysis/w33_20261102_forty_points_full_page_audit.py`.  
**Certificates:** `data/w33_20261102_povm_spectrum_and_duality.json`, `data/w33_20261102_q5_route_orbit_moments.json`, `data/w33_20261102_forty_points_complete_page_audit.json`.

## Prior-result ownership

Pass 173 and Passes 12482–12483 already established the 216 minimal route supports and the inequivalent 45 address supports. The 216-point cubic frame and its W33 line-reconstruction identity were independently committed in `d28feb4` and its report. Parallel Passes 12523–12526, including `aff33d8b`, supply the bijection to synthematic totals, 36 double-sixes, and the decomposition into 36 regular 5-simplices. The present work does **not** claim those discoveries anew. It derives an explicit quantum measurement, exact operator-space spectrum, cross-incidence census, symplectic covariance, and a higher-field orbit certificate.

## Front 1: a valid 216-outcome quantum POVM, but not general-state tomography

Let `H` be the 216×40 point-coverage matrix of the 216 minimum 10-line route supports, and `Z=2H-J`. Every row of `Z` has squared length 40, and `Z^T Z=360 E_{24}`, where `E_{24}` is the positive-eigenvalue primitive idempotent of the W33 point graph.

Choose any orthonormal coordinates for the 24-dimensional image of `E_{24}`, and let `u_s` denote the unit vector obtained by projecting row `Z_s/sqrt(40)` into those coordinates. Then

\[
\sum_{s=1}^{216}|u_s\rangle\langle u_s|=9I_{24},
\qquad E_s=\frac19|u_s\rangle\langle u_s|,
\qquad \sum_s E_s=I_{24}.
\]

Thus the 216 vectors give a rank-one POVM in an **abstract 24-dimensional Hilbert space**, with `Tr(E_s I/24)=1/216`. The isometric analysis map `V: C^24 -> C^216` defined by its rows `u_s^\dagger/3` gives an explicit Naimark construction. Nothing here says the POVM has been compiled into a single-photon optical instrument.

The **effect-operator Gram** matrix is

\[
G_{st}=\operatorname{tr}(E_s E_t)=\frac{(Z_s\cdot Z_t)^2}{129600}.
\]

Its integer numerator `K_{st}=(Z_s·Z_t)^2` has the *exact* characteristic spectrum

\[
\operatorname{spec}(K)=14400^1,3168^{24},2304^{80},768^{81},576^{15},0^{15}.
\]

The reproducer certifies this over the integers: a six-factor annihilating polynomial vanishes modulo eight distinct primes, whose combined modulus is greater than twice a rigorous matrix-entry bound; ranks of `K-\lambda I` modulo a prime distinguishing all six roots certify multiplicities over the rationals. The squared-Gram rank is therefore **201**, not 576: these effects do not span all Hermitian operators on `C^24` (nor all 300 real-symmetric ones). They cannot be informationally complete for arbitrary 24-dimensional quantum states. The earlier 588-sample guarantee remains a **classical full-label-oracle** bound, not a bound on optical photons.

## Front 2: exact address/route cross-incidence

Let `M` contain the 45 projective minimum address supports of weight eight, now read as 45×40 binary point vectors. Exhaustive enumeration of the two distinct binary kernels gives

\[
M^TM=8I+2A_{\rm point}+J,
\qquad (M H^T)_{ij}\in\{0,4,6\}.
\]

Among all `45×216=9720` pairs the overlap 0 occurs 1080 times, overlap 4 occurs 6480 times, and overlap 6 occurs 2160 times. Each address minimum has total incidence 864 with the route coverages, and each route coverage total incidence 180 with the address minima. These are exact cross-relations between two *inequivalent* carriers; they are not a W33 self-duality.

## Front 3: the full W(3,5) minimum-route orbit

Using the existing prime-field builder and the already certified 20-line minimum witness, a new independent point-transvection traversal generated all **4,875** members of that witness's orbit under `PSp(4,5)`. Each support covers exactly 60 of 156 points twice (96 points zero times). Each point is covered by exactly 1,875 supports. For its 4,875×156 binary coverage matrix `H_5`,

\[
H_5^T H_5=1200I+200A_{\rm point}+675J.
\]

After subtracting its column mean `60/156`, the covariance has eigenvalues `2000` (multiplicity 90) and `0` (multiplicity 66). This is exact integer incidence arithmetic, not a fitted spectral pattern.

**General tight-frame theorem (conditional on a complete orbit of coverage-{0,2} line sets).** In `W(3,q)`, let `v=(q+1)(q²+1)`, `m` be the number of lines in each selected even set, `t=m(q+1)/2` its number of twice-covered points, and `M` the size of its full symplectic orbit. If each member covers every point either 0 or 2 times, the centered orbit-coverage matrix `X=H-(t/v)J` obeys

\[
X^T X=\frac{Mt(1-t/v)}{f}\,E_+,
\qquad f=\frac{q(q+1)^2}{2}.
\]

**Proof:** `NN^T=(q+1)I+A`. The negative adjacency eigenspace, with eigenvalue `-(q+1)`, is in `ker N^T`, so `H` and its centered version have zero component there. The constant eigenspace is removed by centering. The remaining `PSp(4,q)`-invariant symmetric second moment commutes with the rank-three permutation action; since the centered positive eigenspace is its only surviving primitive component, it is a scalar multiple of `E_+`. Its trace, `Mt(1-t/v)`, determines the scalar. This makes the normalized centered orbit a spherical 2-design and a rank-one POVM carrier of dimension `f`. In particular `f=24` for `q=3`, `f=90` for `q=5`, and `f=224` for `q=7`; this round **has not** independently enumerated the complete `q=7` orbit.

## Front 4: Clifford symmetry and cubic orientation

The new executable checks **all 40 point-transvection generators** act covariantly on the 216 row states and their 40 measured sign coordinates. For a fixed W33 point, the 216 vectors divide into 108 containing that point and 108 not containing it. The sum of the 108 sign vectors containing it has coordinate profile `108^1,18^{12},(-12)^{27}`, reproducing the stabilizer's `1+12+27` geometry as a conditional frame statistic.

The invariant symmetric cubic

\[
C(x)=\sum_{s=1}^{216}(Z_s\cdot x)^3
\]

is nonzero and `PSp(4,3)`-invariant, with exact squared coefficient-tensor norm `27,371,520` in the standard 40-coordinate Euclidean convention. It does **not** select a preferred chiral sign: the full finite symmetry preserves the cubic. Independent parallel Pass 12526 refines the same carrier into 36 regular 5-simplices; the present proof is an effect-operator/conditional-cubic calculation instead.

## Front 5: test the Albert/E6 interpretation rather than infer it from dimensions

The 24-dimensional positive eigenspace has **no nonzero fixed vector** under the transitive rank-three point action. Therefore any **unital** commutative algebra structure on that 24-dimensional representation cannot be fully `PSp(4,3)`-equivariant, because the unit of a unital equivariant algebra must be fixed by every automorphism. This is a clean no-go for the *naive 24-dimensional unital Jordan/Albert identification*, not for equivariant nonunital cubic products, a 27-dimensional extension, or the separate Albert-algebra constructions in Sections 6–8 of *Forty Points*. To obtain a physical cubic interaction one must exhibit an explicit equivariant intertwiner, normalization, and coupling/kinetic terms, not merely a match of 216, 24, or 27.

## Full *Forty Points* reading coverage and outstanding physics

The checked local PDF has **215 pages** and SHA-256 `003b75482b6584e20e83a55d9e9ba0a181f93b8dff0f94c1d615039c21213cbb`; every page was text-extracted and indexed, with 673,091 extracted text characters and per-page checksums. All twelve core sections, the theorem/computation ledger, glossary, and bibliography were also fetched from GitHub TeX source. The epilogue explicitly names the remaining obstacles: a viable vacuum, dynamics, continuum gravity, chirality selection, physical chamber gates, quantitative masses/couplings, and hardware. This is **complete text coverage, not an independent verification of every published claim or a visual review of all printed figures**.

**External context:** Cui and Wang's *Universal quantum computation with metaplectic anyons* establishes universality only when suitable measurements accompany braiding; its braiding group alone is not universal. High-dimensional photonic experiments make mode-encoded demonstrations plausible research targets but do not realize this 24-mode POVM automatically. The exceptional Jordan cubic is a well-studied norm form; an explicit representation intertwiner and physical dynamics remain unproved bridges.

**Bottom line:** new testable exact combinatorics and a valid abstract POVM, not a solved TOE.
