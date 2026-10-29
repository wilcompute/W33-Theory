# Passes 12357–12362: sub-orbifolds, a tachyon correction, thresholds, a minimal singlet set and proton decay for SM_2913

Claude track. Producer: `analysis/w33_pass12357_to_12362_sub_orbifolds_thresholds_vacuum_proton.py`. Drivers:
`analysis/search_drivers_12357/` (12357, 12358, 12360) and `analysis/search_drivers_12359/` (12359, 12361).

## Correction to 12352 (pushed in 27990054e)

**Withdrawn:** "tachyon-free … for radii above about √2·√α′" and "large radii safe".

- The 6D theory of the θ²-fixed torus e5e6 has tachyons, with m_R² = −1/6, in the Witten θ² and θ⁴ sectors.
  - For SM_2913_v6 the engine's verbose solver counts 12 of them.
- The order-2 Wilson line W5 removes them only at zero momentum.
  - So they carry half-integer e5 momentum.
  - They return for R5 > √(3/8)·√α′ ≈ 0.61·√α′.
- This is the threshold of the torsion window of Pass 12322; here the Wilson line itself produces it.
- 12352 had assumed integer momenta.
- The small-R5 side stays open. The 12352 level minima there are necessary conditions, and the projections of winding states are not
  computed.

**Census over the 99 tachyon-free parents (12324).**

| torus | parents with 6D tachyons | notes |
|---|---|---|
| e5e6 | 52 | all W5-shifted (0 with the line on); includes all seven three-generation models (SM_2618: 24, SM_2913: 12) |
| e3e4 | 0 | — |

The only three-doublet parent clean on both tori is SM_1105_v12. Its parent's hypercharge gives chiral exotics (12351).

## 12359: sub-orbifold geometries, validated

The script `gen_geom.py` builds the geometry of the Witten × θ^s sub-orbifold from the space group. It enumerates constructing
elements in Λ / ((1 − θ^k)Λ + Λ^{θ^k}) modulo the sub point group, and generates the centralizers plane by plane.

**Checks:**

- **Regenerated parent:** s = 1 regenerates the shipped Z6-II geometry and reproduces SM_2913_v6 state for state (788/788, weights
  included).
- **Vector-like fermions:** both sub-orbifolds' 4D fermions are exactly vector-like (0 unpaired weights). The chiral parent has 214. A
  fixed torus means a 6D origin, which requires this.
- **Subset relation:** the Wilson-line-on spectra are weight-level subsets of the Wilson-line-off ones (0 violations).
- **Broken geometry:** a geometry with the fixed-torus translations deleted is rejected by the engine.

## 12359: thresholds cannot rescue k_Y = 5/3

Large-volume Dixon–Kaplunovsky–Louis form, with the coefficients taken from the 6D content (Wilson lines off) and c_i = |G_i|/|G|.

| torus | 6D coefficients (b_Y, b_2, b_3) | consequence |
|---|---|---|
| e5e6 | (80/3, 16, 16) = 16·(5/3, 1, 1) | exactly universal: cannot move sin²θ_W (compare Pass 12156 for T⁶/Z3) |
| e3e4 | (716/9, 220/3, 124/3) | wrong pattern |

- **No fit reaches the data:**
  - SM-only running leaves a residual of at least 8.7 in 1/α;
  - the full spectrum leaves at least 30.
- **Control:** the weight method reproduces 12355's (19/3, 13, 338/9) exactly.
- **Argued, not computed:** that the DKL form holds for this non-SUSY orbifold.
  - The linear large-volume term is power-law KK running, so it is robust.
  - The constant and log terms are not.

## 12361: the Casimir force on the tachyon-free torus

- **Phases:** each state's phase under the e3/e4 translations is read as P·W3 and P·W4.
  - Validation: the phase-0 components are exactly the Wilson-line-on spectrum (1376/1376).
- **E(1/3, 1/3) = −4/9 exactly.** The phase-trivial windings form an index-3 sublattice: a hexagonal lattice scaled by √3.
- **N_B,eff − N_F,eff = −304 + 1984/9 = −752/9.**
  - So the Casimir energy is positive.
  - The torus decompactifies unless the 6D vacuum energy A·Λ₆ is positive. That term is not computed; it needs the full partition
    function.
- **Torus e5e6** is confined to R5 < √(3/8) by its tachyons. That is the string scale, where no field-theory estimate applies.

## 12360: a minimal singlet set

- **The set:** 6 of the 80 SM-singlet scalars, ids 233, 294, 363, 382, 770 and 771.
- **What it does:** it gives full structural rank to every vector-like and fractional-charge block (Q 3, U 3, D 3, L 4, E 3, X 4, F 20, Z 4).
- **Minimality:** dropping any one of the six breaks a block.
- **Control:** only 1 of 100 random six-sets works.
- **What it is not:** a sufficient structural set, not a solved vacuum.
  - No potential is minimised.
  - Structural rank is an upper bound for coefficients that are not generic.

## 12357: mass matrices with the vector-like states

**Control.** At degree 0 the monomial MILP agrees with 12354's independent coupling test on 4080/4080 triples (48 of them allowed).

**Light masses.** All ten Higgs choices give three nonzero light masses per sector.

| singlets allowed | hierarchy |
|---|---|
| all 80 | every degree ≤ 5; light masses span at most ~1.5 decades |
| the 6-set, ε = 0.1, Higgs H6 | top O(1); down sector near observed (s, b); charm ~1.8 and up ~2.6 decades too heavy; e, μ too heavy |

With a common singlet ratio, no realistic up-sector hierarchy appears.

## 12358: proton decay and B − L

- **B − L is a gauged U(1).**
  - It is anomaly-free for every choice of its one free parameter: all five anomalies vanish identically.
- **Baryon number is not gauged.**
- **ΔB = ΔL = 1 four-fermion operators:**

  | operators | singlet degree |
  |---|---|
  | QQU*E*, QLU*D* | 0 |
  | QQQL, UUDE | 2 |

  - All four conserve B − L.
  - Suppressed by M_s², they are harmless.
- **Colour-triplet scalars:** 1 of 16 couples to both quark pairs and quark–lepton pairs, so it must be heavy.
- **The vacuum and B − L:**
  - The six-singlet set has B − L = 0, so U(1)_B−L is unbroken (a massless Z′).
  - 14 singlets carry B − L = ±2. Any one of them breaks U(1)_B−L to matter parity: every SM fermion has odd 3(B − L).

## Upper bounds

12357, 12358 and 12360 do not impose the non-SUSY vertex (H-momentum) rule, calibrated in Pass 11097. "Allowed" may still be
forbidden. The memory rule "impose all selection rules before ranking" applies.

## Synthesis (12362)

**Status of the SM_2913 lineage:**

- **Holds:**
  - three generations;
  - k_Y = 5/3;
  - liftable exotics, with a six-singlet set plus one B − L = 2 singlet for matter parity;
  - gauged, anomaly-free B − L.
- **Fails:**
  - large-radius tachyon-freedom on e5e6;
  - threshold-assisted unification;
  - a realistic up-sector hierarchy with a common ε.
- **Open:**
  - the small-R5 window;
  - the H-momentum rule;
  - Λ₆.
