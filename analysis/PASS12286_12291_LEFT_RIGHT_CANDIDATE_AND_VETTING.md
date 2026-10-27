# Passes 12286–12291: a tachyon-free left-right candidate, the Z2×Z6-I brothers vetted, the literature

Claude track. Producer: `analysis/w33_pass12286_to_12291_left_right_candidate_and_vetting.py`. Drivers:
`search_drivers_12286` (left-right candidate) and `_12287` (vetting).

## 12286: the left-right candidate

**The model.** Z6II_60_SM_20260917_810_v9 (v4 is identical in chiral content), with W6 = λ and V0·λ odd: the Scherk–Schwarz brother
of 12280/12281.

- **Gauge group:** SU(3) × SU(2)_a × SU(2)_b × SU(8) × U(1)⁵.
- **Strict engine:** 466 fields, **no tachyons** (the parent has 16), and the anomaly check passes.

**The hypercharge.** SU(2)_L = SU(2)_a, the factor whose doublets are *not* halved, and Y = T3R + Y′. The quark conditions leave one
free direction t. The value **t = −1/148** is the unique scanned value with no chiral fractional charge. There the net chiral content
is:

| | count |
|---|---|
| Q | 3 |
| u_R | 3 (2 in SU(2)_R doublets + 1 singlet) |
| d_R | 3 (2 + 1) |
| L | 3 |
| e_R | 3 (2 + 1) |
| ν_R | 2 |
| chiral states of fractional charge | **0** |

**Further checks:**

- **Higgs candidates:** 14 SU(2)_L doublets with |Y| = ½, 10 bidoublets, and 14 SU(2)_R doublets that can break SU(2)_R × U(1) to Y.
- **Anomalies:** Tr Y = 0.
- **Normalisation:** k_Y = 8/3 (sin²θ_W = 3/11 at the string scale), not 5/3.

**Caveats:**

- 96 fermion and 102 scalar fields have fractional charge. They are vector-like and would have to be lifted.
- Tachyon-free only at the orbifold point; the moduli are not studied.
- The one-loop potential is not computed.
- The SM analyser of 12180 identifies SU(2)_L with the *other* factor, whose doublets are halved. So 12180's lemma stands. Its
  closure ("no three-generation Scherk–Schwarz interpolation") depends on that identification, and this candidate uses the other one.
  It is a **candidate**, not a Standard Model, until the vector-like exotics and the vacuum are addressed.

## 12287: the twelve Z2×Z6-I brothers vetted

Every renormalisable QL d^c and u^c d^c d^c was checked for gauge and space-group invariance by the engine, then by the R rule
(N = (2, 6, 6)). The R rule removed nothing in any model. With no positive control, the counts are **upper bounds** from gauge and
space group only.

- Brothers do not systematically help: they trade with their parents.
- **Three lineages pass the renormalisable proton test**: SM_128, SM_808 and SM_2579, parents and brothers alike, have no QL d^c
  (SM_128 has no u^c d^c d^c either).
- The other nine fail it.

## 12288: literature

Brother models and generalized discrete torsion are established:

- Plöger, Ramos-Sánchez, Ratz, Vaudrevange, hep-th/0702176;
- the Bonn theses, arXiv:0812.3503 and 0812.3560;
- Z2×Z2 torsion after resolution, arXiv:2211.01397.

So the coprime-order rule of 12282 **restates known constraints**, verified here on the corpus. What is the corpus's own:

- the censuses;
- the 12 Z2×Z6-I brothers (new to the corpus; no Z2×Z6-I brother catalogue was found, which does not prove none exists);
- this left-right candidate.

## 12289–12291

The rule on an unseen geometry is **not done** this round. The bug report (unsent) and the main-checkout file remain user decisions.
