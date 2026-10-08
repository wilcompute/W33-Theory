# Pass 11692 — the unbroken E₈ symmetry of an elementary two-qutrit tick: magic is needed for a Standard-Model-shaped centraliser

Producer: `analysis/w33_pass11692_tick_symmetry_in_e8.py` (argument: samples per case)
Certificate: `data/w33_pass11692_tick_symmetry_in_e8.json`
Regression: `tests/test_w33_pass11687_11696.py`

## Method

**The tick as an E₈ element.**
* A one-gate tick U = W(a)V_M T₁ (Pass 11350) is fixed to det 1, which puts it in SU(9). Its image in SU(9)/Z₃ sits in
  E₈ (Pass 11681).
* The Z₉/Z₃ ambiguity of that normalisation gives **three E₈ lifts**, and all three are scanned.

**Reading off the unbroken symmetry.** With eigenvalues λᵢ of U, the E₈ element's unbroken symmetry (centraliser) is
the Cartan of its torus plus exactly:
* the sl(9) roots eᵢ − eⱼ with λᵢ = λⱼ;
* the trivector roots ±(eᵢ + eⱼ + eₖ) with λᵢλⱼλₖ = 1.

Components are classified by (number of roots, rank). As calibration, T ⊗ I gives A₁ + E₆ and Z ⊗ I gives A₂ + E₆.

## Results

15 000 uniformly random (M, a) per case, each in all three lifts.

| | Cartan only | trinification A₂³ | SM-shaped A₂ + A₁ (su(3) ⊕ su(2) ⊕ u(1)⁵) |
|---|---|---|---|
| ticks with the magic gate (per lift) | ≈ 0.69 | ≈ 0.072 | **≈ 0.0020–0.0025** (30–38 per 15 000) |
| Clifford-only ticks (no T, per lift) | 0.05–0.09 | 0.03–0.06 | **0** (0 of 45 000) |

* **Magic ticks.** The commonest non-trivial unbroken symmetry is **trinification SU(3)³**.
* **Clifford ticks.** They keep larger symmetries (A₁ + A₂³, A₂ + A₅, A₁⁴, …) and never leave exactly A₂ + A₁ in the
  sample.

## Reading and scope

**Observation.** A single elementary tick of two qutrits, viewed as an E₈ group element, can have the shape of the
Standard Model gauge algebra (plus abelian factors) as its unbroken symmetry. In this sample, that happens only when the
tick contains the magic gate.

**Limits.**
* This is a sampled statement about centralisers of single group elements.
* It is not a proof that Clifford ticks can never produce it.
* It does not derive the Standard Model: nothing selects such a tick, and the abelian factors and charges are not
  matched to hypercharge here.
