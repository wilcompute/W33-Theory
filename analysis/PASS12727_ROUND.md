# Pass 12727: a full-precision first layer cuts the ternary gap by about three quarters on both prose and code; A's rescue requires inflation below H_I ≈ 10⁵ GeV; B′'s dark fifth force is safely small; radiative brane terms deepen the SO(10) orbifold deficit; the summary page is refreshed

Claude track. **Not a theory of everything.**
- Scripts: `explore_pass12727_round.py` and `explore_pass12727_firstlayer.py` (≈50 min).
- Tests: `tests/test_toe_pass12727.py`, 4 tests passing.
- Page: [Quartic Zero Decision Map](https://claude.ai/artifact/P7DdJZNBnjeSPJgFZ4Wnoc), version 4, with status through Pass 12727.

## (3) Ternary training with a full-precision first layer
**Setup:** 2 layers, d = 64, 3000 steps, annealed-threshold curriculum. The fp32 references come from Pass 12726.

| corpus | fp32 | all-ternary | gap | ternary + fp32 layer 0 | gap | gap cut |
|---|---|---|---|---|---|---|
| prose | 2.660 | 3.094 | 0.435 | **2.779** | **0.120** | 72% |
| code | 2.187 | 2.941 | 0.755 | **2.368** | **0.181** | 76% |

- **Keeping only the first layer at full precision removes about three quarters of the ternary gap on both corpora,** including code, where all-ternary training failed to close it (Pass 12725). This confirms the per-layer diagnosis of Pass 12726.
- **Caveat:** in this 2-layer toy, layer 0 is half of the quantised weights. In deep models the first layer is a small fraction, so the memory cost of the rule shrinks with depth.
- **Practical recipe: fp first layer, ternary elsewhere.**

## (1) Isocurvature bound on A's rescue (θᵢ ≈ 0.992π)
- **Constraint:** P_iso/P_ad = (d ln Ω/dθ)²(H_I/2πf_a)²/P_ad < 0.038 (Planck), with P_ad = 2.1×10⁻⁹.
- **Results:**
  - f_a = 2.5×10¹⁰ GeV, θᵢ = 0.992π: d ln Ω/dθ = 9.7 → **H_I < 1.4×10⁵ GeV** (r < 3×10⁻¹⁹).
  - f_a = 1.7×10¹¹ GeV, θᵢ = 0.65π: H_I < 6×10⁶ GeV.
- **A survives only with low-scale inflation.** Primordial tensor modes are then unobservable. A detection of primordial gravitational waves at r ≳ 10⁻³ would exclude this rescue.

## (2) B′'s dark-sector fifth force
- **Size of the force:** the coupled component attracts itself with an extra 2β². Inside a halo, the fractional extra force is about 2β²f.
- **Results:** 0.036 (β = 0.3, f = 0.2), 0.040 (β = 0.2, f = 0.5) and 0.020 (β = 0.1, f = 1). All are below the ~0.1 bound on dark-only forces from tidal streams and dwarfs.
- **The minimal B′ dark sector passes.**

## (4) Radiatively generated brane kinetic terms (SO(10) orbifold)
- **Localised log coefficients:** ½(b_even − b_odd) at each fixed point, from the Pass 12725 parity classes. They are (2.4, 4, 0) on the Pati–Salam brane and (−2, −2, −2) on the SU(5)×U(1) brane (universal).
- **Shift:** at M_sR = 10 the radiative brane shifts are (0.15, 0.73, −0.73), which move the predicted α₃⁻¹ by **−1.88** (−2.22 at M_sR = 15).
- **The radiative brane terms are O(1), as expected, but in this estimate they add to the bulk deficit.** The total deficit becomes about −3.3, so a tree-level brane term of about +3.3 (≈ 4.5× its natural size) would be needed.
- **This weakens the repair proposed in Pass 12726.** The hybrid's orbifold doublet–triplet route is now disfavoured unless the brane terms are large or opposite in sign to this crude estimate.

## (5) Status refresh
- **Builder:** `build_toe_status.py` now records A's inflation bound (`A_HI`) and runs through Pass 12727.
- **Page:** it shows the low-scale-inflation condition for A and the brane-term finding for the hybrid.

## Status
- **A:** viable with near-π misalignment and H_I < 10⁵ GeV.
- **B′:** a three-part dark sector, a safe fifth force, a DESI fit, and a decisive Belle II test.
- **Hybrid:** doublet–triplet splitting is the open problem. The orbifold route is disfavoured (radiative brane terms deepen the deficit).
- **Ternary:** fp first layer plus ternary elsewhere recovers about 75% of the gap on prose and code.
