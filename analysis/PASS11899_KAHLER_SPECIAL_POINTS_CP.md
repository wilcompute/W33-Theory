# Pass 11899: the symmetric Kähler vacua of two ℤ₃ tori, their W(3,3) dictionary, and CP

Producer: `analysis/w33_pass11899_kahler_special_points_cp.py`
Certificate: `data/w33_pass11899_kahler_special_points_cp.json`
Regression: `tests/test_w33_pass11899.py`
Track: Claude.

## Setting

Passes 11897–11898 established that, on T⁴/ℤ₃, the moduli-dependent twisted couplings are five even weight-1 theta
functions of the Hermitian Kähler matrix Z. These fill ℙ⁴, and the duality group acts there through the Burkhardt group
PSp(4,3), of order 25920.

A modular-invariant potential has critical points wherever the residual symmetry is nontrivial (Cvetič–Font–Ibáñez–Lüst–
Quevedo). These special points are therefore the candidate symmetric vacua.

CP acts on the Kähler moduli as Z → −Z̄, and on the thetas as complex conjugation: θ(−Z̄) = conj θ(Z).

## Results

**The special points.** There are 13805 isolated special points (one-dimensional eigenspaces of group elements), in
11 orbits:

| projective stabiliser | orbit | W(3,3) object fixed | where |
|---|---|---|---|
| 648 | 40 | one line (no point) | **the cusps**: the orbit contains θ at infinity |
| 576 | 45 | one split {P, P^⊥} (no point, no line) | interior: the 45 tensor factorisations (the Burkhardt nodes) |
| 162 | 160 | one point and one line through it | interior: the **flags** |
| 120 | 216 | none | interior |
| 108 | 240 | one point | interior |
| 48 | 540 | one split | interior |
| 36 | 720 | one line and one split | interior |
| 16 | 1620 | one split | interior |
| 12 | 2160 | one point and one split | interior |
| 9 | 2880 | a flag | interior |
| 5 | 5184 | none | interior (Im Z min = sin 36°: a ℤ₅ point) |

**Cusps.**
* The 40 cusps (large-volume limits) are the 40 lines of W(3,3), i.e. the 40 maximal commuting Pauli sets.
* At a cusp the couplings become diagonal in that context.
* Along iyI, θ approaches the cusp with defect 1 − |θ₀|/|θ| decreasing exponentially in y.

**Interior points.** The ten non-cusp orbits are reached at finite moduli: Newton converges to residual 10⁻¹², with
Im Z positive definite.

**CP.** Every special orbit is CP-conserving: conj θ lies in the group orbit of θ, to 10⁻¹⁵.
* Generic Kähler points are CP-violating (control: 1 − overlap between 2·10⁻⁵ and 2·10⁻²).
* Their CP violation decreases exponentially toward the cusp: 4·10⁻³, 2.6·10⁻⁵, 1.4·10⁻⁷ along a ray with Im Z scaled
  by 1, 2, 3.

## What this says

* **Same conclusion as the Siegel case.** For the Kähler moduli, as for the Siegel fixed points of Pass 11874, the
  symmetric vacua are CP-conserving. CP violation in the twisted couplings needs the moduli displaced from every
  symmetric point. That violation is exponentially small at large volume.
* **The cusp ties back to Pass 11884.** The radiative selection there put the vacuum on a cusp, the most symmetric
  limit. In Kähler language this is large volume, where the theta texture is maximally hierarchical and CP is
  restored.
* **One parameter, two effects.** Distance from the cusp controls both the family hierarchy (the same e^{−2π Im Z/3}
  suppression as Pass 11891) and the size of CP violation. In the Kähler picture these are one parameter, not two.
* **Every W(3,3) incidence object appears as a symmetric vacuum.**
  * lines → cusps;
  * flags → the 160;
  * points → the 240;
  * factorisations → the 45 Burkhardt nodes.

## Not established

* No potential is minimised. Whether any of these points is a *minimum* depends on the non-perturbative superpotential.
  Known genus-1 analyses put minima near, not at, the fixed points (e.g. T ≈ 1.2), which would break CP slightly.
* The equivalence used is in ℙ⁴, i.e. modulo Γ(√−3) and the deck involution Z → Zᵀ of 11898.
* The interior coordinates are numerical (several look algebraic: entries ½ ± i/(2√3); ymin = 1/(2√3), 1/5, sin 36°).
  They are not identified in closed form.

## Prior art

* Cvetič–Font–Ibáñez–Lüst–Quevedo (1991): fixed points are extrema of modular-invariant potentials.
* Novichkov–Penedo–Petcov and Feruglio: hierarchies near fixed points.
* Burkhardt (1891), Todd, Hunt (*The geometry of some special arithmetic quotients*): the Burkhardt configurations,
  including the 45 nodes and the 40 j-planes / Steiner primes.
* Corpus:
  * 11874 (Siegel fixed points CP-conserving);
  * 11884/11891 (cusp selection, hierarchy ∝ δ);
  * 11831 (40 contexts + 45 splits + 36);
  * 11897–11898.
