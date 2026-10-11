# Pass 11905: symmetric Wilson lines are degenerate, so the up hierarchy needs a non-symmetric Wilson-line vacuum

Producer: `analysis/w33_pass11905_symmetric_wilson_lines_degenerate.py`
Certificate: `data/w33_pass11905_symmetric_wilson_lines_degenerate.json`
Regression: `tests/test_w33_pass11905.py`
Track: Claude.

## Setting

As in Pass 11904: one family qutrit (flux 3 on the family torus) and a localised Higgs. The up-type masses are
(top, charm, up) = |θ[c/3, 0](z, Ω)| for c = 0, +1, −1, where z is the continuous Wilson-line argument.

## Theorem

**The group.** The level-3 Heisenberg–reflection group acts on z by three maps:
* z → z + 1;
* z → z + Ω/3, which shifts the characteristic c → c + 1;
* z → −z, which sends c → −c.

Its reflections z → −z + m + kΩ/3 fix the points

  **z = m/2 + kΩ/6**, with m ∈ {0, 1} and k ∈ ℤ₆.

**Statement.** At every such point two of the three masses coincide exactly. Which pair depends on k mod 3:

| k mod 3 | equal pair |
|---|---|
| 0 | charm = up (the light pair) |
| 1 | top = up |
| 2 | top = charm |

**Proof.** By the shift and reflection formulas, θ[a](−z + m + kΩ/3) = (unit phase)·θ[−a − k/3](z). At a fixed point
this gives |θ[a](z)| = |θ[−a − k/3](z)|, which pairs c ↔ −c − k (mod 3).

**Relation to Pass 11904.** The theta-zero law is the case k = 3, where in addition one theta vanishes.

## Checks

The test covers 16 random Ω × the 36 points (u + vΩ)/6.

| test | result |
|---|---|
| coincidence where u ∈ {0, 3} (the fixed points) | at every such point; the pair matches the theorem's table; worst gap 1.1·10⁻¹⁵ |
| coincidence where u ∉ {0, 3} (not fixed points) | none (smallest pair gap 0.018) |
| generic z (control) | spread 0.21 |

## Reading

Jacobi- or modular-invariant potentials for the Wilson-line modulus have their symmetric critical points exactly at
these fixed points. None of them can host m_t ≫ m_c ≫ m_u, because each forces a pair of equal masses.

In the Gaussian regime the fixed points sit at offsets δ ∈ {0, 1/6} (mod 1/3). These give either the locked light pair
or top = a light quark. The hierarchy point of Pass 11904 (δ ≈ 0.060) is not among them.

**So, in the magnetized home, the up hierarchy is a property of a generic, dynamically selected Wilson-line vacuum. It is
not selected by symmetry.** This is the sharpest form of the obstruction across the session:
* heterotic ℤ₃: locked by the local 10 (Pass 11903);
* magnetized: allowed, but never at a symmetric point.

## Not established

* **Which vacuum.** No potential for the Wilson line is minimised, so where it settles is open.
* **Other symmetric points.** Fixed points of the SL(2,ℤ) elliptic elements acting jointly on (z, Ω) at special Ω (ω, i)
  are not separately catalogued. The Heisenberg–reflection reflections are the ones that act on z at every Ω.

## Prior art

* Corpus: 11114 (Hesse), 11899 (symmetric Kähler points), 11904 (theta-zero law, Gaussian invariant).
* TOE45, the parallel track's audit (its next step 4: a full magnetized normalisation).
* Classical: theta-function shift and reflection formulas (Mumford, *Tata Lectures on Theta I*); the Jacobi group
  (Eichler–Zagier).
* Magnetized Yukawas with Wilson lines: Cremades–Ibáñez–Marchesano (2004).
