# Passes 11714–11716 — the W(3,3) heterotic vacua read in two-qutrit levels: chirality, 2+1 family levels, the top Yukawa as the nine-level determinant, and doublet–triplet splitting as the plane split of one level pair

Producer: `analysis/w33_pass11714_11716_heterotic_two_qutrit_levels.py` (`--from-orbifolder` regenerates the frozen input in WSL)
Frozen orbifolder input: `data/w33_pass11714_orbifolder_frozen_states.json`, `data/w33_pass11714_z3_vacuum_orbifolder_summary.txt`, `data/w33_pass11714_z3_vacuum_model.txt`
Certificate: `data/w33_pass11714_11716_heterotic_two_qutrit_levels.json`
Regression: `tests/test_w33_pass11713_11716.py`

## Why these two objects are one object

The two-qutrit E₈ of Pass 11681 is

  e₈ = sl(9) ⊕ Λ³C⁹ ⊕ Λ³C⁹\*

that is, operators, three-fermion states and three-hole states.

The W(3,3) heterotic twist is the A8 Kac class (Passes 10979 and 11089; Holotrade 68df33f). Its order-three gauge shift has centraliser **SU(9)**, and the roots outside it are **84 + 84̄**: exactly that decomposition.

So the heterotic gauge lattice and the two-qutrit Lie algebra are the same object. The SU(9) levels of the string are the nine two-qutrit levels.

## 11714 — the T⁶/Z₃ W(3,3) vacuum is the two-qutrit E₈ made chiral

orbifolder 1.2 was run on the shift (⅙⁷, ⅚; 0⁷, ⅔) over Z₃ on SU(3)³. Its raw output is frozen in the summary file listed above.

| sector | spectrum |
|---|---|
| untwisted | 3 (84, 1) + 3 (1, 14) + 3 (1, 64) |
| twisted T(2,0) | **27 (9̄, 1)** |

The gauge group is SU(9) × SO(14) × U(1), with an anomalous U(1) of trace 3888.

**Reading.**
* **The untwisted 84s.** The SU(9)-charged untwisted matter is the **three-fermion grade** of the two-qutrit E₈, once per complex plane.
* **The 27 fixed points.** The 27 fixed points of T⁶/Z₃ are A₂³/(1 − ω) = F₃³, the basis of three qutrits. Each carries one dual two-qutrit state.
* **Anomaly cancellation.** The SU(9) anomaly cancels as **3 · A(Λ³C⁹) = 3 · 9 = 27 = number of fixed points**. The formula A(Λ³Cⁿ) = (n − 3)(n − 6)/2 is checked by explicit weights.
* **Chirality.** Four-dimensional chirality comes from locking the E₈ Z₃ grading (three-fermion versus three-hole) to the rotation of the internal planes. That ingredient is outside E₈ itself, which is why the Distler–Garibaldi obstruction to E₈ "theories of everything" (cited in Pass 11725) does not apply to it.

**Prior art.** The SU(9) × SO(14) × U(1) Z₃ model is a classical member of the Z₃ orbifold classification. Pass 11089 loaded it as the supersymmetric control. The level/plane reading is what is added here.

## 11715 — census of the 87 Z6-I W(3,3) Standard Models

These are the 87 parents of Pass 11089 and Holotrade 5b3f3ad, re-run in orbifolder.

| step | count |
|---|---|
| models | 87 |
| an A8 (SU(9)) half in the θ² shift 2V | 47 |
| SM SU(3) × SU(2) inside that SU(9) (colour on 3 levels, weak on 2, four flavour levels left) | 30 |
| all three net quark doublets untwisted, i.e. three-fermion states colour ∧ weak ∧ o | **28** |

In **all 28**:

* **Flavour-level partition {a} | {b} | {c, d}.** The untwisted 10-type states (Q, u^c, e^c) use the single levels a and b. The untwisted 5-type states use the pair {c, d}. The two sets are disjoint and cover all four flavour levels.
* **2+1 family levels with a swap.** The two quark doublets from the degenerate G2 planes 1, 2 share one flavour level. The one from the order-three "qutrit" plane 3 uses the other. Q and u^c (and e^c) swap levels between plane 3 and planes 1, 2.

The flagship SM_20260917_3 shows the pattern concretely. In SU(9) levels:
* colour is {2, 5, 7} and weak is {0, 6};
* the flavour levels are {1, 3, 4, 8};
* the 10s use levels 1 and 4, and the 5s use the pair {3, 8}.

The model's own hypercharge (Holotrade certificate) on the levels is

  6Y = 2 (colour), −3 (weak), 0 (flavour levels).

This is the **Georgi–Glashow hypercharge vanishing on the four non-GUT levels**, i.e. the vacuum-annihilating hypercharge singled out abstractly in Pass 11708 (with Codex 11723's caveat on vector neutrality).

**Prior art.** Holotrade 3caf15e and ade6ba9 own "the three families are the three untwisted planes" and the species-by-plane table, 87/87. What is added here is the SU(9) level labelling: which levels carry which families, and the swap.

## 11716 — the couplings in levels

**The cubic coupling is the two-qutrit bracket.** The cubic coupling of three untwisted fields is the E₈ structure constant. For three-fermion states it is Pass 11681's bracket [x, y] = ∗(x ∧ y). It is therefore nonzero exactly when the three level sets **partition the nine levels**, and then |coupling| = g, with the sign of the permutation.

**The top Yukawa.** In all 28 models, gauge-invariant couplings

  Q (planes 1, 2) · u^c (planes 1, 2) · H (plane 3)

exist, with H = weak ∧ c ∧ d. There are 24 weight-level couplings in each model, and every one partitions the nine levels. So **y_top = g is the nine-level determinant**: Q fills colour, weak and a; u^c fills two colour levels and b; H fills weak, c and d.

**Doublet–triplet splitting.** H (plane 3) and its colour partner T = colour ∧ c ∧ d (planes 1, 2) are the weak and colour halves of **one level-pair multiplet ∧{c, d}** (28/28). The missing-partner doublet–triplet splitting of Holotrade a6f1cae is the plane split of that one multiplet.

**Prior art.** The cubic top y_top = g is Holotrade 93b34e1/3caf15e (57/60). The determinant reading is what is added here.

## Scope

These are dictionary statements on actual orbifolder spectra.

**Not claimed:**
* a new vacuum;
* F- or D-flatness;
* any mass other than the cubic top;
* a dynamics that selects these models.

The Codex track's all-order obstructions on the Z6-II benchmark (Passes 11797–11801) concern a different model class and are untouched.

The two models among the 30 whose untwisted sector gives net 4 doublets are excluded from the 28 and listed in the certificate.
