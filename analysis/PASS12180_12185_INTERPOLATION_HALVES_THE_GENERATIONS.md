# Passes 12180–12185: interpolation halves the generations

Claude track. Producer: `analysis/w33_pass12180_to_12185_interpolation_halves_the_generations.py`. Drivers:
`analysis/search_drivers_12180/` (`ss_z6ii.py`, `sscontent.py`, `oddgen.py`), `analysis/search_drivers_12181/`
(`clockfam.py`), and `analysis/search_drivers_12174/thermal.py`.

## 12180: the Scherk–Schwarz census on Z6-II

Z6-II is the one W(3,3) family whose translations allow a Scherk–Schwarz interpolation (Pass 12177).

**Method (exact).** At large radius, each parent SUSY multiplet is split by χ = exp(2πi p·V0): its bosons survive if
χ = +1, its fermions if χ = −1. This is precisely the Witten-untwisted projection of the non-free Z2W×Z6-II model with
the same V0. In the sectors that rotate the translated plane (θ, θ³, θ⁵), the translation pairs fixed points, and each
pair keeps one boson and one fermion.

**Control.** The total Witten-untwisted state count is independent of V0 (70/70 parents), as the splitting requires.

**Result.** 70 parents (W6 = 0) × 20 split V0 = 1400 interpolations.

- n_B − n_F always lies in 8ℤ, between −80 and 464.
- There are **3 exact Bose–Fermi degeneracies**, all in Z6II_59 SM_20260917_1105.
- One of them (v12) keeps an SU(3)×SU(2)-type factor and is tachyon-free as a non-free model.

## 12180b/c: the generations decide it

**Every W6 = 0 parent has (even, odd) = (1, 2) net quark doublets.** The translation halves the odd sectors, so at
most 1 + 2/2 = 2 generations survive at large radius, for every V0. The degenerate v12 point has exactly 2.

Dimension-weighted census of all 128 parents (an earlier count by multiplet lines missed a family triplet; corrected
before commit):

| (even, odd) net quark doublets | parents |
|---|---|
| (1, 2) | 117 |
| (2, 1) | 10 |
| (3, 0) | 1 |

The single all-even parent, SM_2751 (an untwisted family triplet), has zero odd-sector chirality in every species.
It is excluded by a separate lemma:

- θ reverses the order-2 plane, so g⁻¹θgθ⁻¹ is the translation −2t.
- That translation's gauge embedding is V0 − V0 = 0, yet it must equal −W_{2t}.
- So a translation needs W_{2t} ∈ Γ. In SM_2751, W5, W6 and W5 + W6 all lie outside Γ.

**Closure: no Z6-II W(3,3) Standard Model has a three-generation Scherk–Schwarz interpolation.** Bose–Fermi
degeneracy is reachable (3/1400), but never with three generations.

## 12181: clock Witten shifts on every family

| family | bases | Wilson-line draws | tachyon-free |
|---|---|---|---|
| Z6-I | 6 | 1800 | 0 |
| Z3×Z3 | 6 | 1800 | 0 |
| Z12-I | 6 | 1800 | 0 |

Every base is tachyonic at the orbifold point. This is the theorem of Pass 12178 (the zero-winding state p = V0)
holding beyond Z3.

## 12182: twisted 10_H sample

150 new draws give 53 SU(5)×U(1) models, 21 of them with three generations, and **0 scalar 10s**. The cumulative
sample is now 0/238. Fermion 10s are present, which is the control. This remains a sample, not a theorem.

## 12183: the clock instability is not the Hagedorn instability

A state of the 9D interpolation is physical iff it is level matched, n·w = ½ − p²/2 − N.

| class | tachyonic radii | tachyon |
|---|---|---|
| V = 0 (thermal ensemble) | 2 − √2 < R < 2 + √2 | heterotic Hagedorn (control) |
| clock×clock, split×0 | all R < 2√2 | p = V0 |
| split×split | none (massless at R = √2) | – |

The two instabilities differ in momentum and in critical radius, by a factor 1.207, and the clock one has no upper edge.

## 12184: which split the vacuum picks (cited)

This is answered by Pass 12089 and is not re-derived here. On the E6 clock vacuum, 27 of the 135 split parities (the
factorisations through the event) leave SO(10), with the 16 odd and the 10 even.

## 12185: synthesis

Z6-II is the only W(3,3) family/route that admits interpolation. There the generations split 1 + 2 between the sectors
the translation does not and does pair. Super-no-scale and three generations exclude each other on this class.
