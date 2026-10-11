# Pass 11914: the Higgs is the flavour lever — shared-Q universality, the anarchic spread phase, the class selection

Producer: `analysis/w33_pass11914_higgs_is_the_flavour_lever.py`
Certificate: `data/w33_pass11914_higgs_is_the_flavour_lever.json`
Regression: `tests/test_w33_pass11914.py`
Track: Claude.

## 1. Shared-Q universality: the geometric route to the up/down mismatch is closed

**Setup.**
* The two-qutrit home: genus-2 Siegel thetas in toy units, Ω = i[[25.25, 4.57], [4.57, 16]].
* Q's families are an eigenspace of the Pauli Z₂.
* The right-handed families are an eigenspace of **any of the 40 W(3,3) Pauli points**, with any eigenvalue.
* The Higgs is localised in any of the 9 classes.

**Result.** Over all **2,214 full-rank configurations** the Gaussian invariant m₁m₂/m₃² takes a single value,
10^(−7.6557 … −7.6553). It is fixed by Q's family direction alone.

**Consequence.** Q is shared by the up and down Yukawas, as in SU(5). So with localised Higgs fields, no choice of
right-handed W(3,3) eigenspaces gives the observed I_down/I_up ≈ 716 (Pass 11910; TOE49 requirement (a)).

## 2. The spread phase is anarchic

**Setup.** TOE48's minimal Higgs potential has two phases: either one Higgs mode is occupied, or all six modes are, with
equal norm and flat phases. Take H_u localised (the Pass 11906 up fit, reproduced: 3.60·10⁻³ and 1.70·10⁻³) and H_d in
the six-mode phase. Exact flux-(3,3,6) overlaps were used, with 600 random phase choices and three Wilson lines.

**Result (medians, CKM in mass-ordered labels):**

| | m_s/m_b | m_d/m_s | V_us | V_cb | V_ub |
|---|---|---|---|---|---|
| spread H_d | 0.84 | 0.70 | 0.58 | 0.58 | 0.58 |
| data (M_Z) | 0.019 | 0.053 | 0.225 | 0.041 | 0.0037 |

So the down masses are nearly degenerate and every CKM element is ≈ 1/√3 (trimaximal). The pattern resembles lepton
mixing, not quark mixing.

## 3. The class selection forbids radiative admixture

**Result.** The loop-induced Higgs-mode mass matrix Tr(Y_k Y_k′†) has these sizes:
* between different ℤ₃ classes: zero (1.0·10⁻¹⁵);
* within a class: nonzero (≥ 0.046).

**Reason.** The magnetic-translation ℤ₃ is exact, so cross-class Higgs mixing is forbidden at every order. Within-class
mixing (k ↔ k+3) gives no CKM, because each Yukawa matrix keeps one entry per row.

**Consequence.** The small cross-class admixture that Cabibbo-sized mixing needs therefore requires **explicit breaking
of the magnetic-translation symmetry**. Symmetric Higgs potentials give only the localised phase (no mixing) or the
spread phase (anarchy).

## Corrections acknowledged (parallel TOE49, d3c7321f9)

* **Pass 11910's CKM statistic.** Its "Cabibbo-sized" number was the fourth-largest |V| entry, not the mass-ordered V_us.
  Its CKM illustration also used two different τ, while the minimal home shares one. TOE49's mass-ordered scan of that
  ansatz (6,336 points) found none with V_us, V_cb and V_ub all within a factor of 2 of the data. Item 2 here uses
  mass-ordered labels.
* **Pass 11909's Q-band is scheme-dependent.** A finite matching counterterm absorbs it. Its physical content is the
  matched coefficient of the Σ|Y|² Higgs-mass term, which must be small compared with the quartic. It is not the value
  of Q/m̃. The reading "the hierarchy needs a small top-sector Wilson-line-dependent Higgs-mass term" stands; the band in
  Q does not.

## Reading

The flavour problem of the two-qutrit home reduces to the Higgs:
* the **geometry** fixes one invariant per shared Q (item 1);
* the **symmetric Higgs phases** give either no mixing or anarchy (item 2);
* the **exact class symmetry** forbids the small admixture radiatively (item 3).

A realistic quark sector needs a sector-dependent Higgs profile that breaks the magnetic-translation ℤ₃ explicitly but
weakly. That is a sharp requirement on the UV completion.

## Prior art

* TOE46, TOE48, TOE49 (parallel track).
* Corpus: 11904–11912.
* Cremades–Ibáñez–Marchesano.
* Abe–Kobayashi–Ohki et al. (multi-Higgs magnetized fits).
