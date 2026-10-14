# TOE67 — Continuous all-temperature W33 flux selection and symmetry no-go

**Date:** 14 October 2026. **Layer:** exact finite graph, static free fermions. The physical Theory of Everything remains open.

## Repository novelty and prior work

TOE61 proved all-positive-temperature flux selection for eight discrete Z2 corners. TOE62 proved selection over the continuous U(1)^3 torus only for the leading high-temperature term. TOE65/66 established a rational native-edge counterexample under hopping disorder. TOE67 proves **all-positive-temperature selection over every continuous flat phase for uniform native hopping**, using exact integer certificates. The theorem is particular to the selected 80-site W33 Levi graph, rather than a new general theorem superseding Lieb's planar flux theorem (Phys. Rev. Lett. 73, 2158, 1994, DOI 10.1103/PhysRevLett.73.2158).

## Exact uniform-hopping theorem

Let B(theta) be the 40-by-40 point-line hopping block of the 80-vertex W33 Levi graph. Of its 160 nonzero incidence entries, precisely the three selected fundamental chords **59, 93 and 139** have phases exp(i theta_j); the remaining entries are 1. Write H(theta)=[0,-B;-B*,0].

The unphased W33 incidence block has squared-singular spectrum 16(1), 6(24), 0(15). A rank-three update leaves rank B(theta) at most 28, so at least 12 singular values stay zero. The corresponding update in B B* has rank at most six, preserving at least 18 eigenvalues equal to 6. Consequently,

\[
\det(xI-BB^*)=x^{12}(x-6)^{18}Q_{10}(x;\theta),\qquad
\det(I+tBB^*)=(1+6t)^{18}\sum_{k=0}^{10}e_k(\theta)t^k.
\]

Only ten squared-singular eigenvalues can move. The coefficients e0...e3 are the phase-independent integers (1,52,1116,12960).

### Why a finite exact calculation proves all continuous angles

Cauchy–Binet expresses every coefficient of det(I+tBB*) as a sum of squared minors. Each of the three phase variables occurs in **one** matrix entry, so each minor is affine separately in each complex phase. Squaring gives Laurent Fourier support only at frequencies (-1,0,+1) along each axis. The phase-independent factor (1+6t)^18 does not enlarge that support.

We regenerated the exact Gaussian-integer characteristic polynomial at all **64** 4th-root phase triples (each exp(i theta_j) one of 1,i,-1,-i), verified exact divisibility by x^12(x-6)^18 and performed a discrete Fourier transform using integer arithmetic. Because support is bounded by 1 and the sampling lattice has 4 points per coordinate, **the reconstruction is mathematically exact with no aliasing**, not a numerical trigonometric fit. All 27 Fourier mode coefficient vectors, 64-sample digest and strict margins are frozen in the accompanying JSON.

Let delta=theta-(pi,pi,pi). For each coefficient k, the exact reconstructed Fourier series gives

\[
e_k(\pi)-e_k(\pi+\delta)=\sum_{n\sim-n}
2c_{kn}(-1)^{n_1+n_2+n_3}[1-\cos(n\cdot\delta)].
\]

For any mode n supported on m≤3 coordinates, the half-angle triangle inequality and Cauchy–Schwarz give

\[
1-\cos(n\cdot\delta)\le m\sum_{j:n_j\ne0}(1-\cos\delta_j).
\]

Keeping positive single-axis modes, bounding negative cross modes and discarding additional positive terms produces **strict** integer margins:

| coefficient | axis-1 margin | axis-2 margin | axis-3 margin |
|---:|---:|---:|---:|
| e4 | 150 | 138 | 138 |
| e5 | 3664 | 3344 | 3344 |
| e6 | 32936 | 29664 | 29664 |
| e7 | 135088 | 121056 | 121056 |
| e8 | 235968 | 221568 | 221568 |
| e9 | 94848 | 89088 | 89088 |
| e10 | 13728 | 13728 | 13728 |

Therefore each e_k, k≥4, is uniquely maximized at theta=(pi,pi,pi) modulo 2pi. Coefficients e0...e3 are constant. This proves the **global spectral inequality**

\[
\boxed{\det(I+tB_\pi B_\pi^*)>\det(I+tB_\theta B_\theta^*)}
\]

for **every real t>0** and **every other continuous U(1)^3 phase**. The positive Weierstrass factors for cosh convert this determinant ordering directly to strict **all-temperature** free-fermion ordering:

\[
\boxed{F_\beta(\pi,\pi,\pi)<F_\beta(\theta)}
\quad\text{for all }\beta>0,\quad\theta\ne(\pi,\pi,\pi)\bmod2\pi.
\]

The same proof works with an arbitrary **common real sublattice-staggered mass m**, since shifting squared energies by m² transforms the determinant as P(theta,m;t)=(1+m²t)^40 P(theta; t/(1+m²t)). It does NOT prove selection under arbitrary independent hopping disorder, gauge-field dynamics, interactions, nonflat connections, or continuum quantum field theory.

## New no-unique-free-vacuum obstruction

Rank B(theta)≤28 implies **at least 24 exactly zero one-particle energies** in the 80-band bipartite massless Hamiltonian at every flat phase. The exact active determinant at three pi shows **exactly** 24 there; at trivial flux rank B=25, giving exactly 30.

At canonical half filling with 40 spinless fermions and rank r, every negative level is filled and the remaining 40-r fermions may occupy any of 80-2r zero modes. Therefore the **massless free many-body ground-state degeneracy** is

\[
\binom{80-2r}{40-r}\ge\binom{24}{12}=\boxed{2,704,156},
\]

and at zero flux it is binomial(30,15)=155,117,520. In the grand-canonical ensemble the exact zero modes contribute residual entropy at least 24 k_B ln 2. Hence unique flux minimization is consistent with an enormous **nonunique gapless matter vacuum**. An actual gapped physical vacuum requires physics beyond this uniform massless three-deck free Hamiltonian.

## Full symplectic ribbon symmetry obstruction

TOE66 correctly constructed a closed genus-81 surface by doubling a chosen orientable ribbon thickening. But the native symplectic transvection centered at projective point 4 fixes point 0 and permutes its four incident isotropic lines by **[0,2,3,1]**, an order-three cycle. The symmetry group of any unoriented cyclic arrangement of four slots is D4, with element orders 1,2,4 only. Thus **no orientable ribbon cyclic ordering of the native Levi graph is invariant under all of PSp(4,3)**.

Independently, doubling the ribbon neighborhood of any connected graph produces genus E-V+1, whatever cyclic orders were chosen. For the W33 Levi graph, E-V+1=160-80+1=81. Therefore the doubled genus 81 is just the ordinary first Betti number, **not** evidence that native W33 symmetry uniquely selected this geometry. Subgroup-preserving rotations, emergent symmetry breaking and alternative cellulations remain open.

## Executable publication

- analysis/w33_20261014_toe67_continuous_all_beta_determinant.py — exact 64-characteristic-polynomial Fourier producer and rigorous trigonometric proof.
- analysis/w33_20261014_toe67_ribbon_symmetry_obstruction.py — native symplectic transvection and no-go.
- data/w33_20261014_toe67_continuous_all_beta_determinant.json — full 27-mode exact integer and margin certificate.
- data/w33_20261014_toe67_ribbon_symmetry_obstruction.json — order-three action certificate.
- tests/test_w33_20261014_toe67_continuous_all_beta.py — source regeneration, off-grid spectral checks, staggered-mass finite-temperature tests and flat-band no-go checks.

**Verification:** six dedicated independent server-side regression tests passed. The later published GitHub CI status is a separate check. Mathematical and physical claims remain properly separated.

## Five independent next physics directions

1. Generalize the exact determinant inequalities to **correlated native edge-product disorder**, keeping TOE64 and TOE66 bounds distinct.
2. Integrate **dynamical compact U(1) gauge fields and real fermionic interactions**, or produce a controlled counterexample.
3. Classify **proper-subgroup-preserving ribbon rotations** and test genuine selection dynamics after the full-PSp no-go.
4. Obtain a **native admissible four-dimensional overlap Dirac index** and anomaly-free Weyl representation content, not just a continuum index on an imposed product manifold.
5. Remove the **exact 24-fold single-particle flat-zero sector** with a symmetry-compatible local mechanism, establish an interacting gap and derive a falsifiable parameter-independent observable.

**The Theory of Everything itself remains unsolved.**
