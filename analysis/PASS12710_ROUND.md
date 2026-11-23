# Pass 12710: B′'s extra dimension is ≥10⁸ below lab gravity reach; B′'s y′ prediction needs a mediator portal |λ_HY| ≲ 0.04; warping makes B′ degenerate with the hybrid; the hybrid's evidence hinges on (M_VL/M_GUT)²; flag-respecting gluings of the W33 tetrahedra never make a 3-manifold

Claude track. Follows Pass 12709. **Not a theory of everything.**
- Script: `toe_pass12710_round.py` (≈1 min).
- Certificate: `data/toe_pass12710_round.json`.
- Tests: `tests/test_toe_pass12710.py`, 5 tests passing.

## (1) Short-range gravity cannot see B′
- **Expected signal:** one flat dimension gives a Yukawa term with α = 8/3 (2n in another convention) and λ = R.
- **Sensitivity floor:** published bounds at 10–200 nm are given only as figures (1704.02920). The floor was therefore estimated from first principles:
  - the Yukawa pressure between gold half-spaces, 2πGρ²αλ²e⁻¹ at d = λ;
  - against the Casimir pressure π²ħc/240d⁴;
  - with 1% precision and a 10³–10⁴ isoelectronic suppression.

| λ = R | Casimir (Pa) | Yukawa at α = 1 (Pa) | α floor (isoelectronic) | gap to α = 8/3 |
|---|---|---|---|---|
| 8.8 nm | 2×10⁵ | 4×10⁻¹⁸ | 5×10¹⁶ | ≥ 2×10¹⁶ |
| 88 nm | 22 | 4×10⁻¹⁶ | 5×10¹⁰ | ≥ 2×10¹⁰ |
| 200 nm | 0.8 | 2×10⁻¹⁵ | 4×10⁸ | ≥ 10⁸ |
| 1 μm (excluded window, for scale) | 10⁻³ | 6×10⁻¹⁴ | 2×10⁴ | ≥ 8×10³ |

**The surviving dark dimension is 8–16 orders of magnitude below any foreseeable laboratory gravity test.** B′ can be tested only through y′ (FCC), B → ψ + baryon (Belle II) and MeV cosmology.

## (2) The B-mesogenesis mediator and B′'s prediction
- **The mediator must be a scalar.** The operator ψbud needs a coloured scalar Y(3, 1, −1/3). B′'s vectorlike fermions cannot mediate it at tree level.
- **What Y does to the running:**
  - it changes the gauge running (Δb₃ = 1/6, Δb_Y = 1/9);
  - its Higgs portal λ_HY|H|²|Y|² adds 3Kλ_HY² to β_λ.

| M_Y | λ_HY | y′_B (R = 0.088 μm) | shift vs no mediator |
|---|---|---|---|
| 2 TeV | 0 | 0.5053 | +0.0051 (gauge only) |
| 2 TeV | 0.03 | 0.5072 | +0.0069 |
| 2 TeV | 0.1 | 0.5243 | +0.024 |
| 2 TeV | 0.3 | 0.627 | +0.126 |
| 5 TeV | 0 / 0.1 | 0.5039 / 0.5215 | +0.0036 / +0.021 |

**B′ keeps its y′ prediction at FCC-era precision only if |λ_HY| ≲ 0.042.**
- A portal radiatively induced by Y's quark couplings, ~y_t²y_Y²/16π², is small enough.
- A tree-level O(0.1) portal turns y′ into a free parameter.
- The gauge-only shift (+0.004 to +0.005) belongs in B′'s central value. Over the surviving R range it gives **y′_B′ ≈ 0.492–0.510**.

## (3) The hybrid in the evidence table
dy′/dm_t = 0.050 GeV⁻¹ at M_SS = 10¹⁰ GeV.

| SM m_t prior width | hybrid, light Q+U from a symmetry | hybrid, two tunings (M_VL/M_GUT)² | B′ (Pass 12709) |
|---|---|---|---|
| 15 GeV | 0.75 | 1.4×10⁻²⁷ | 0.044 |
| 5 GeV | 0.25 | 4.7×10⁻²⁸ | 0.015 |
| 2 GeV | 0.10 | 1.9×10⁻²⁸ | 0.006 |

- **Light Q+U is the deciding question.** The 650+78 vacua of Pass 12705 keep Q+U light only by two tuned couplings, a doublet–triplet-type problem. If the tuning is counted, the hybrid is dead in Bayesian terms. If a symmetry explains it, the hybrid is the best-supported completion, at 0.1–0.75, though still not above the SM.
- **Next for the hybrid:** a symmetry (missing-partner or pseudo-Goldstone type) that leaves exactly Q+U light.

## (4) Warped throats at fixed KK spacing (1 eV)
- **The bound constrains the spacing.** The 2610.01825 bound applies to the spacing m_KK, and the species scale depends on the warp:
  - M_Pl² = (M₅³/k)(1 − e^{−2kL});
  - m₁ ≈ x·k/(e^{kL} − 1), with x going from π (flat) to 3.83 (RS), an interpolation.

| kL | L (μm) | M₅ (GeV) | IR cutoff (GeV) | y′ (SM on UV brane) | y′ (SM on IR brane) |
|---|---|---|---|---|---|
| 0 (flat) | 0.62 | 9.8×10⁸ | 9.8×10⁸ | 0.505 | 0.505 |
| 1 | 0.41 | 1.5×10⁹ | 5.5×10⁸ | 0.498 | 0.516 |
| 3 | 0.12 | 3.1×10⁹ | 1.5×10⁸ | 0.486 | 0.542 |
| 10 | 3×10⁻⁴ | 3.2×10¹⁰ | 1.5×10⁶ | **0.457** | 0.683 |
| 20 | 3×10⁻⁸ | 9×10¹¹ | 1.9×10³ | 0.433 | — |

- **The flat limit reproduces Pass 12707.**
- **SM on the UV brane:** warping lowers y′ and **crosses the hybrid's 0.470 near kL ≈ 7**.
- **SM on the IR brane:** warping raises y′.
- **Consequence:** B′ predicts y′ only for a fixed throat geometry and SM location. A warped B′ can mimic the hybrid at FCC, which weakens the discrimination of Passes 12707–12709 unless the dark dimension is nearly flat.

## (5) Gluing the W33 tetrahedra into a closed 3-manifold (the triangle programme)
- **Faces are flags.** The 160 faces are exactly the flags (p, L): the triangle L∖{p}.
- **Flag-respecting gluings:** at each point p, its 4 lines are paired (3 matchings) and the two faces are glued by any bijection (6 choices).
- **Search:** 400 random such pairings.

| quantity | result | needed for a 3-manifold |
|---|---|---|
| faces after gluing | 80 every time (closed 3-pseudomanifold) | 80 |
| vertex classes | **1** (all 40 points collapse) | any |
| edge classes | 1–8 (χ = 33–40) | 41 (χ = 0) |
| vertex link | χ = −64 or similar, not a sphere | a 2-sphere |

**Flag-respecting face pairings of W33 never give a 3-manifold.**
- **Why:** each gluing identifies points across lines through p. W33's collinearity graph is connected, so all points become one vertex and the edges collapse.
- **Consequence:** building a smooth 3-geometry from W33's tetrahedra requires gluings that do not respect the point–line incidence, or a larger building (for example Sp(6,3), whose chambers are 2-simplices) instead.
- **Answer to the triangle question:** triangles can make any shape, but this particular ternary object resists being made into a manifold.

## Status
- **A:** unchanged.
- **B′:** y′ ≈ 0.49–0.51 for a flat dimension and a small mediator portal.
  - It is lab-gravity invisible.
  - It is testable at Belle II and FCC.
  - Warping or a large portal removes the prediction.
- **Hybrid:** either the best of the completions, if a symmetry keeps exactly Q+U light, or excluded by tuning.
- **No completion beats the SM today.**
