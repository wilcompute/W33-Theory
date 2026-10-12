# Pass 11933: radiative selection + the residual ℤ₃ give an ε-independent neutrino relation — inverted ordering with m₃ ≈ 1.3 meV

Producer: `analysis/w33_pass11933_radiative_neutrino_relation.py`
Certificate: `data/w33_pass11933_radiative_neutrino_relation.json`
Regression: `tests/test_w33_pass11933.py`
Track: Claude. Builds on Passes 11928–11932.

## Setting

* The A₂ dual pair at (and near) the Eisenstein point Ω = ω·1.
* The Weinberg channel L·L, with a mediator of flux 2A₂′ (12 modes).
* Two dynamical inputs:
  * **radiative selection**: the mediator takes the direction of maximal coupling, the top eigenspace of the Gram matrix
    C = Σ Y_ab Y_ab*;
  * a vacuum respecting the residual ℤ₃.

## Results

**1. The radiative top space.** The Gram top space is exactly 3-dimensional (the flavour qutrit). It contains **charges 0
and 2 only**: charge 1 is radiatively disfavoured (Gram 0.79 against 1). Its intersections with the charge sectors are
1-dimensional (charge 0) and 2-dimensional (charge 2).

**2. All symmetric directions give (1, 1, 0).** Every ℤ₃-symmetric radiative direction gives (1, 1, 0) exactly at
Ω = ω.

**3. Near the point.**
* **Charge 0.** The pair stays degenerate: the split is below 10⁻⁵ at ε = 10⁻². There is no solar splitting at this order,
  so this direction is excluded.
* **Charge 2.** **Both** the pair splitting and the light mass scale as **ε²**, with log-slopes 2.00 ± 0.01 over 24
  directions and deformation directions.

**4. The relation.** Because both scale the same way, ε cancels:

  **m₃/m₁ = κ · Δm²₂₁/Δm²₃₁,  κ ≈ 0.9 (5–95%: 0.5–2.5).**

## Reading

**The prediction.** An **inverted ordering with m₃ ≈ 1.3 meV** (0.8–3.8 meV) for m₁ ≈ 49.5 meV.

**What it rests on.**
* The A₂ flux near the Eisenstein point.
* Radiative selection of the mediator.
* A ℤ₃-respecting vacuum.

It needs no value of ε and no blow-up sign. The charge-2 direction is forced by the data: the charge-0 alternative gives no
solar splitting.

**How to test it.**
* JUNO and DUNE will measure the ordering. Current global fits mildly prefer normal ordering.
* For inverted ordering, m_ββ ≈ 15–50 meV.
* An m₃ of about 1 meV is below near-term direct reach, but it fixes Σm_ν ≈ 0.10 eV, which cosmology is approaching.

**Open.** A derivation of radiative selection beyond the leading-coupling argument, and of the ℤ₃-respecting vacuum.

## Caveat (Pass 11934)

Applied uniformly to every Yukawa channel, the same radiative + residual-ℤ₃ principle gives (1, 1, 0) in the up, down
and charged-lepton sectors too. Those give top = charm, m_b = m_s and m_τ = m_μ, which are excluded. The inverted-ordering
reading therefore needs a reason specific to the neutrino mediator. It is **not** a consequence of a universal selection
rule.
