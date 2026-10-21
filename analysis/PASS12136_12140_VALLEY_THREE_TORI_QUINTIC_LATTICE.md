# Passes 12136–12140: S002's saddle, the three-torus engine on T115, a protected doublet, the complete fraction-free search

Claude track. Producer: `analysis/w33_pass12136_to_12140_valley_three_tori_quintic_lattice.py`. Drivers and frozen
outputs: `analysis/search_drivers_12136/`. Engines are those of Passes 11106 and 11107, extended here.

## 12136: below Im T_WL = 0.7, Λ turns around

**Convergence.** At T\* = ρ, the winding cut-offs K = 2 and K = 3 agree to 10⁻⁸ at 0.8i.

**Potential along the imaginary axis.**

| T_WL | 0.9i | 0.8i | 0.6i | 0.55i | 0.5i | 0.4i |
|---|---|---|---|---|---|---|
| Λ/M⁴ | 170.1 | 145.3 | 115.8 | **115.4** | 119.6 | 149.0 |

So there is a **minimum near Im T_WL ≈ 0.55**, and Λ is still positive there.

**Tachyons.** The 11107 enumerator, with raised cut-offs, finds the whole axis from 3i down to 0.3i tachyon-free. Its
control (model 2: Δ = −0.2113) is reproduced.

## 12140: the axis is a ridge, not a valley

**Off the axis at Im 0.55.** The same level turns tachyonic, linearly in |Re T_WL|:

| Re T_WL | 0 | 0.05 | 0.1 | 0.3 | 0.5 |
|---|---|---|---|---|---|
| Δ | none | −0.025 | −0.047 | −0.110 | −0.131 |

The level is **marginal exactly on the axis**, so the B-field direction is tachyonic there.

**Off the axis at Im 0.9.** The strip is wider: Re 0.1 is clean and Re 0.2 is tachyonic. Λ falls off the axis
(170.1 → 168.5 at Re 0.1), so the axis is a ridge.

**Conclusion.** The axis minimum is a saddle. The negative Λ values off the axis (−132 at 0.3 + 0.55i, −441 at
0.5 + 0.55i) lie in the tachyonic region and are **void**: their integrand grows.

## 12137: the one-loop engine on three Wilson-line tori; T115

**The extension.**

- `wl3.WLPartN` generalises the 11106 lattice sum to t Wilson-line tori, with the 3^t coset sum vectorised.
- Control: S002, with its free torus treated as a third torus with W = 0, reproduces the two-torus engine to 2·10⁻¹⁰.
- The 11107 enumerator is generalised the same way. Control: S002's 56 states at ρ with Δ = −1/18, and none at 2i.

**T115.** All three of its tori carry Wilson lines. Its integrand is modular invariant to 10⁻¹³.

| T_WL (all three tori) | 3i | 2i | 1.75i | 1.5i | 1.25i | i | 0.8i | ρ |
|---|---|---|---|---|---|---|---|---|
| Λ/M⁴ | — | +987.6 | +663.8 | — | — | void | — | — |
| tachyons | none | none | none | 10 (Δ = −0.067) | 12 (−0.139) | 16 (−(3−√3)/6) | 16 (−0.269) | 56 (−1/6) |

- The tachyon onset lies between 1.75i and 1.5i.
- Λ > 0 and falling at every tachyon-free point.
- The value Λ < 0 at (i, i, i) is void: that point is tachyonic and the integrand grows.

## 12138: T115's last light doublet is structurally protected

Adding quintic ψψ⟨s⟩⟨s⟩⟨s⟩ terms (gauge and space-group rules; 24 new entries) leaves the doublet mass matrix at rank 5
of 6. The pattern of allowed entries has **structural rank 5**: it fails Hall's matching condition. So no choice of
coefficients lifts the last vector-like lepton doublet at any order up to quintic. A selection-rule block structure
protects it.

## 12139: the complete fraction-free search, and a correction to 12126

**Method.** This uses the criterion of 12131.

- A fraction-free Y needs v = q ± λ ∈ E8×E8.
- v·r is fixed for every nonabelian root r.
- Enumerate all lattice vectors with N ≤ 12, half by half. The E8 shells 1, 240, …, 60480 come out exact.
- Hash-join the two halves on the colour-singlet charge residues.

**Control.** Every strict (12121-type) fraction-free hypercharge that commutes with all nonabelian factors is
recovered: 19/19.

**Correction to 12126.** Its fraction-free counts (11/22/4/14, and "none in S002") were complete only inside the strict
search class. The lattice search finds:

| model | fraction-free hypercharges (commuting) |
|---|---|
| S033 | 4 |
| S053 | 45 |
| T115 | 59 |
| S002 | **3** (k_Y = 41/3) |

All of them sit on the k_Y = 5/3 + 4n law, so the law of 12131 and its root test are unaffected.

**The 104 A8 models of 11095.**

- Fraction-free hypercharges exist in **102 of 104**: 10,920 of them up to N ≤ 12.
- **Every one has k_Y ≥ 17/3**; the minimum, 17/3, is reached in 81 models.
- None has k_Y = 5/3.

So on both routes, charge quantisation costs k_Y ≥ 17/3. The canonical k_Y = 5/3 of the A8 models always comes with
fractionally charged states.
