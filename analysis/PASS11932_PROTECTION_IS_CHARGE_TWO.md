# Pass 11932: blow-up protection is residual ℤ₃ charge 2, and the theta-zero law is a charge-selection rule

Producer: `analysis/w33_pass11932_protection_is_charge_two.py`
Certificate: `data/w33_pass11932_protection_is_charge_two.json`
Regression: `tests/test_w33_pass11932.py`
Track: Claude. Sharpens Pass 11930.

## 1. Protection = charge 2

**The equality.** For the up mediator (flux 2A₂) and the Weinberg mediator (flux 2A₂′) at Ω = ω·1, Pass 11930 found a
4-dimensional space of modes vanishing at all 9 fixed points. That space **equals the ρ-charge-2 eigenspace**, with
projector distance about 10⁻¹⁵.

**Why.** Charge-2 modes vanish at every fixed point because no fixed point carries local phase 2 for these bundles.

**The contrast.** The down mediator (flux 4·1) has a 7-dimensional protected space that is not a single charge sector.

**What changes for Pass 11930.** Its assumption, positive localised blow-up masses, is replaced by a **discrete** one: the
mediator carries residual charge 2.

## 2. The theta-zero law is a selection rule

**The rule.** The generations carry charges (0, 0, 2) (Pass 11928). A charge-2 mediator couples only pairs with
q_a + q_b ≡ 2 (mod 3), i.e. only the (0, 2) pairs.

**The Yukawa.** In the generation charge basis it is therefore

  [[0, 0, x], [0, 0, y], [x, y, 0]],

with singular values √(|x|² + |y|²), √(|x|² + |y|²) and 0. That is **(1, 1, 0) exactly**.

**Checks.** The forbidden entries vanish to 10⁻¹⁵ for random charge-2 mediators, and the spectrum is (1, 1, 0).

## 3. Near the point

The broken ρ fills the forbidden entries at O(ε). This gives the scalings of Pass 11930:
* the pair splits linearly in ε;
* the light state appears at order ε².

## Reading

**The neutrino reading, restated.** Pass 11930's conditional neutrino reading becomes a charge assignment. If the
Weinberg mediator carries residual charge 2, then near the Eisenstein point:
* the ordering is inverted;
* m₃/m₁ ≈ 10⁻³;
* the solar splitting is linear in ε.
This is the theta-zero law of Pass 11904, now explained as a residual-charge selection rule.

**What remains to derive.** Why the mediator would carry charge 2. In an explicit orbifold that is a discrete twist
phase.
