# Pass 11713 — three families on the two-qutrit levels: the family SU(3), its E₆ centraliser, and the grade of every family multiplet

Producer: `analysis/w33_pass11713_family_e6_grade_dictionary.py`
Certificate: `data/w33_pass11713_family_e6_grade_dictionary.json`
Regression: `tests/test_w33_pass11713_11716.py`

**Setting.** In the operator-type Standard Model of Pass 11707 the nine two-qutrit levels split **9 = 5 + 1 + 3**:
* five Georgi–Glashow levels;
* the vacuum level;
* three family levels.

The Codex track's Passes 11731 (bundle obstruction) and 11732 (the 3875 Yukawa channel) already use the same family SU(3) on levels 3, 4, 5. They are cited here and not re-derived. This pass closes the family direction reserved by the Claude track in 11713–11720.

## Found

The checks below hold on the worked configuration of Pass 11707, for each of the four possible vacuum levels.

* **Centraliser.** The operator SU(3)_F rotating the family levels has E₈ centraliser exactly **E₆** (72 roots). It contains the Standard Model roots and the Georgi–Glashow SU(5). This is E₈ ⊃ E₆ × SU(3)_F read as SU(9) ⊃ SU(6) × SU(3)_F, with 6 = GUT levels + vacuum level.
* **Families.** The 81 roots of (27, 3) form three families of 27, one per family level.
* **Grades.** **Each family is spread over all three grades** of e₈ = sl(9) ⊕ Λ³ ⊕ Λ³\*:

| grade | states | SU(5) content |
|---|---|---|
| three-fermion | 15 (two levels from GUT + vacuum, one family level) | 10 + 5 |
| operator | 6̄ (family level ← GUT/vacuum level) | 5̄ + 1 |
| three-hole | 6̄ | 5̄ + 1 |

* **Hypercharges.** The family states carry exactly the Georgi–Glashow hypercharges listed in the certificate.
* **Bracket structure.** The E₈ bracket of two *different* families lands in the third, (27̄, 3̄) with weight −e_h. Same-family brackets vanish. This is the ε_fgh structure; the symmetric family channel needs the 3875 (Pass 11732).

## The chiral W(3,3) vacuum branched on these levels

Branch the T⁶/Z₃ W(3,3) spectrum of Pass 11714 (3 × 84 untwisted, 27 × 9̄ twisted) under SU(5) × SU(3)_F.

* **One untwisted 84** gives (10̄,1) + (10,1) + (10,3) + (5,3) + (5,3̄) + (1,3̄) + (1,1).
* **Net tens.** The net tens of each plane are exactly **one family triplet (10, 3)**, because the (10,1) cancels the (10̄,1).
* **Totals.** Three planes give 9 = 3 × 3 net tens. These are balanced by 27 twisted 5̄ against 18 untwisted 5s.

## Scope

This is group theory on the explicit two-qutrit E₈. Which levels act as families in an actual vacuum is measured in Pass 11715. There, the three families of the W(3,3) Standard Models turn out to be the three untwisted *planes* (as Holotrade found), and not three family levels inside one plane.
