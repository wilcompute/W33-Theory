# Passes 12363–12368: tachyons radius by radius, and the closure of the three-doublet non-SUSY Z6-II lineages

Claude track. Producer: `analysis/w33_pass12363_to_12368_all_radius_closure_z6ii.py`. Drivers: `analysis/search_drivers_12363/`
(winding geometries and the all-radius census), `analysis/search_drivers_12364/` (hypercharge searches) and
`analysis/search_drivers_12357/lift_exact.py` (all-orders lifting).

**Prior art (cited, not claimed).**

- **Literature:**
  - SO(16)×SO(16) orbifold Standard-Model-like models: Blaszczyk, Groot Nibbelink, Loukas and Ramos-Sánchez, arXiv:1407.6362.
  - No vanishing one-loop cosmological constant on non-SUSY toroidal orbifolds: Groot Nibbelink et al., arXiv:1710.09237.
- **In-corpus:**
  - 12322: the torsion window.
  - 12351–12362: the SM_2913 lineage and the sub-orbifold geometries.

## 12363: small radius, by winding sectors

**The method.** A winding-w string of the θ² sub-orbifold is the space-group element (g, l + w·e5). So the engine, fed constructing
elements shifted by w·e5, returns the states that become light as R5 → 0.

**Controls:**

- **W5 = 0:** winding changes nothing. The twisted sectors are identical; the engine relabels 24 untwisted neutral states.
- **W5 on, w = 2:** identical to w = 0, because W5² = 22 is even.

**The result:**

- **Odd winding** (w = −1, ±3, 5): 42 level-matched tachyons with m_R² = −1/6, identical for every odd w.
  - w = +1 trips an engine assertion and is not used.
- **SM_2913_v6** is therefore tachyonic for R5 < √(2/3)·√α′, from α′m²/4 = −1/6 + R5²/4.
  - It is also tachyonic for R5 > √(3/8)·√α′ (12359).
  - **There is no tachyon-free R5.**

## 12364: hypercharge searches

**Method.** An exact MILP:

- Y is orthogonal to every non-abelian root and to the anomalous U(1).
- Each field's Y comes from a finite set.
- The net chirality must be three SM generations, with everything else vector-like or hidden-chiral with Y = 0.

**Control.** On SM_2913_v6 it finds solutions, including the parent's k_Y = 5/3. A first version failed this control because of two bugs:

- the anomaly constraint was in the wrong basis;
- self-conjugate types were constrained.

Both are fixed.

**SM_574 (v0, v5, v6)** is small-R safe, and its hidden sector is an SU(5) family, 10 + 5̄.

- There is no solution, even after each relaxation:
  - dropping the anomaly condition;
  - widening the hidden values;
  - loosening every non-(3,2) value to (1/6)ℤ in [−1, 1].
- **Mechanism:** the coloured conditions together with Y-neutral hidden SU(5) states are already infeasible.

**SM_1105_v12** is large-R safe, but it carries net two SU(2)_L doublets that are triplets of a hidden SU(3)′. These are chiral exotics
for every hypercharge.

## 12365: SM_2618 keeps massless fractional charges

SM_2618 is small-R safe and has three generations with k_Y = 5/3.

- 12 of its 52 fractional-charge fermions cannot pair at any order: (3,1,∓1/6) triplets and (1,1,±1/2) singlets.
- **The test** is exact:
  - integer net singlet powers, with no degree bound and no positivity;
  - every translation sector allowed, the most permissive form of the rule. Further rules only forbid more.
- **Control:** SM_2913_v6 lifts 52/52 at all orders.

## 12366: all-radius census of the 99 tachyon-free parents (twisted channels)

**Torus e3e4:** clean at large and small radius in 99/99.

**Torus e5e6:**

| large-R tachyonic | small-R tachyonic | parents |
|---|---|---|
| no | no | 18 |
| no | yes | 29 |
| yes | no | 34 |
| yes | yes | 18 |

The 18 all-radius-clean parents (SM_1474 ×6, SM_2678 ×12) carry no three net (3,2) doublets.

| lineage (three net (3,2)) | large R5 | small R5 | verdict |
|---|---|---|---|
| SM_2913 v6–v8 | tachyonic (12) | tachyonic (42) | no tachyon-free radius |
| SM_2503 ×6 | tachyonic | tachyonic | no tachyon-free radius |
| SM_2618 v0–v3 | tachyonic (24) | clean | window R5 < √(3/8), but 12 fractional fermions massless at all orders |
| SM_574 ×3 | tachyonic | clean | no three-generation hypercharge |
| SM_1105_v12 | clean | tachyonic | Y-independent chiral exotics |

## 12367: three generations versus radius stability

- None of the 17 three-doublet parents is clean at all radii; 18 of the other 82 are.
  - The hypergeometric chance of this is 0.023. That is suggestive only.
- Every parent carries both W3 and W5, because the route built them in. So no Wilson-line contrast is available in this sample.

## 12368: closure (on this sample)

Every three-doublet lineage of the 99 tachyon-free non-SUSY Z6-II parents fails.

**Not covered:**

- the untwisted-sector winding channels (the engine cannot take a translated untwisted element; 12352's necessary condition stands);
- the non-SUSY vertex rule (moot after closure);
- models outside the 99.
