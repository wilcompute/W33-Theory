# Passes 11887–11889: the one-loop vacuum is a W(3,3) point: E₆ × SU(3)_family, with the Higgs in the family Cartan

Producer: `analysis/w33_pass11887_11889_e6_family_at_w33_point.py`
Certificate: `data/w33_pass11887_11889_e6_family_at_w33_point.json`
Regression: `tests/test_w33_pass11887_11889.py`
Track: Claude.

## Where this starts

Passes 11884–11886 found that SU(9) + 84, the ℤ₃-twisted half of E₈, has its one-loop vacuum at the 40 Witting rays
of the Vinberg Cartan, where SU(9) → SU(3)³. The same vev x is an element of e₈ = sl₉ ⊕ Λ³ ⊕ Λ⁶ (the bracket of
Pass 11681). This pass asks what x leaves unbroken inside the full E₈.

## 11887: the centraliser is E₆ ⊕ u(1)²

**At a Witting ray:**
* The centraliser of x in e₈ has dimension 80, with ℤ₃-grade dimensions (24, 28, 28).
* Its derived algebra is 78-dimensional and acts irreducibly on a 27-dimensional weight space (commutant dimension 1).
  The other dimension-78, rank-6 algebras, so(13) and sp(12), have no 27-dimensional irreducible representation, so
  the derived algebra is **e₆**.
* Its centre is 2-dimensional.

So z(x) = e₆ ⊕ u(1)², and its grade-0 part, su(3)³, is the trinification group already found inside SU(9). Within
E₆ that grading is E₆'s own trinification grading: 78 = 24 + 27 + 27̄.

**At a generic Cartan point:** the centraliser is 8-dimensional, with grades (0, 4, 4). That is a Cartan subalgebra of
E₈, and its grade-0 part is trivial, matching the finite SU(9) stabiliser of 11880.

## 11888: three families with family-triplet charges

Under z(x),

  248 = 80 ⊕ six 27-dimensional U(1)² weight spaces ⊕ six singlets.

**How the weights fit together:**
* Three of the 27-weights sum to zero. These are the weights of a **3 of SU(3)**.
* The other three are their negatives: the 27̄s.
* The six singlet weights are the pairwise differences of the three family weights: the six **roots of A₂**.

So 248 = (78,1) + (1,8) + (27,3) + (27̄,3̄) of E₆ × SU(3)_family, with SU(3)_family broken to its Cartan U(1)² by the
vev. **Three 27-generations appear, labelled by family charges.**

## 11889: the vacuum is a W(3,3) point

For each of the 40 Witting rays:
* exactly one W(3,3) point P has a Pauli operator that fixes all of z(x);
* its fixed algebra is 86-dimensional, E₆ ⊕ A₂ (the Pauli centraliser of a point, Pass 11687);
* the map from rays to points is a bijection, 40 ↔ 40.

Since u(1)² commutes with E₆ inside E₆ ⊕ A₂, the vev lies in the Cartan of that A₂.

**The one-loop vacuum is therefore a W(3,3) point, read as an E₈ symmetry: E₆ × SU(3)_family, with the twisted-sector
Higgs breaking the family SU(3) to U(1)².**

The corpus's static dictionary ("point ↦ E₆A₂", 11687; "three generations = (27,3)", Pass 231) is now the output of a
vacuum computation:
1. renormalizable flat direction (11881);
2. one-loop selection (11884);
3. centraliser (11887–11889).

## Correction, owed to TOE44 (b143f9524)

11885 called "the phase of κ in κI₁₂ + c.c." the CP datum. TOE44 shows that a lone complex κ₁₂ is removable by
rephasing x, since I₁₂(e^{iθ}x) = e^{12iθ}I₁₂(x). That is correct.

**The rephasing-invariant CP phase needs a second holomorphic invariant.** With κ₁₂I₁₂ + κ₁₈I₁₈ + c.c., the invariant
is arg(κ₁₂³/κ₁₈²), since I₁₂³ and I₁₈² both have degree 36. Otherwise CP violation must be **spontaneous**, i.e. come
from the vacuum value of the phase direction. Both I₁₂ and I₁₈ are nonzero at the Witting ray (11885), so the invariant
phase is well defined there. The CP statement of 11885 is corrected accordingly.

## Scope

* **What the 4d model gauges.** The E₆ ⊕ u(1)² is a centraliser *in E₈*. In the 4d SU(9) + 84 model only its grade-0
  part SU(3)³ is gauged. Making the full E₆ massless requires the grade-1 and grade-2 states (27, 27̄) to be gauge
  fields. That needs a higher-dimensional completion, e.g. E₈ gauge theory on T²/ℤ₃ with the W(3,3) twist, where the 84
  is an internal gauge-field component (gauge–Higgs unification) and special Wilson-line values can enhance the gauge
  group. This enhancement is a **hypothesis**; it is not computed here.
* **Chirality.** The 27s here are in the E₈ adjoint, which is real. 4d chirality must still come from the orbifold or
  geometry; the firewall of Pass 11859 stands.
* **No dynamics yet.** The family U(1)² charges are group theory at the vacuum. Masses, mixing and Yukawas are not
  computed.

## Next

1. The Hosotani (gauge–Higgs) one-loop potential for E₈ on T²/ℤ₃ with the 84 as Wilson line. Does it reproduce the
   Witting-ray selection and enhance SU(3)³ → E₆ × U(1)²?
2. Family U(1)² charges of the three 27s, combined with the near-cusp displacement, giving family hierarchies
   (11876's law in Higgs variables).
3. Fermion loops (the sign flip that could move the vacuum).

## Prior art

* E₈ ⊃ E₆ × SU(3) and the (27,3) family structure: standard. Corpus Pass 231 and 11687.
* Levi centralisers of semisimple elements: standard.
* Hosotani mechanism (1983); gauge–Higgs unification on orbifolds: standard.
* TOE44 (parallel track): the CP rephasing firewall, credited above.
* Corpus: 11681, 11687–11693, 11879–11886.
