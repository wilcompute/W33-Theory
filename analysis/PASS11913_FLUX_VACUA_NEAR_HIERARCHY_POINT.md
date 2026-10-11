# Pass 11913: type IIB flux vacua near the hierarchy point — within the tadpole bound the hierarchy moduli stay flat

Producer: `analysis/w33_pass11913_flux_vacua_near_hierarchy_point.py`
Certificate: `data/w33_pass11913_flux_vacua_near_hierarchy_point.json`
Regression: `tests/test_w33_pass11913.py`
Track: Claude.

## Question

Pass 11912 showed that the off-diagonal Siegel modulus Ω₁₂ can carry the up hierarchy. Can three-form fluxes stabilise
the period matrix at the hierarchy point? In physical units that point is Ω ≈ i[[4.21, 0.76], [0.76, ≥ 2.7]].

## Method

**Setting.** Type IIB on T⁶ = T⁴ × T², with complex structure T = blockdiag(Ω, τ₃) and axio-dilaton φ.

**Exterior algebra.** Exact, over the 20 integral 3-forms, with orientation dx₁dy₁dx₂dy₂dx₃dy₃. The flux is
G = F − φH, with F and H integer.

**Conditions.** A supersymmetric, imaginary-self-dual vacuum needs a primitive (2,1) flux:
* W = ∫G∧Ω = 0, ∫H∧Ω = 0, and ∂_{T_ab}W = 0 for all nine T_ab;
* primitivity J∧F = J∧H = 0, for the natural Kähler form J = i h_ab dz_a∧dz̄_b with h = (Im T)⁻¹.

At a rational target point these conditions are linear over ℚ in the 40 flux quanta.

**Search.** Rational null space, then LLL reduction, then small integer combinations. The tadpole is N = ∫F∧H. The
T⁶/ℤ₂ orientifold bound is N/2 + N_D3 = 16, so N ≤ 32; with even quanta the bound is stricter.

**Calibration.**
* A primitive (2,1) form gives N = +4 and W = 0.
* A (0,3) form gives W ≠ 0.

An earlier draft omitted primitivity. Without it, minimum-N fluxes exist (N = 2–12), but they are not imaginary
self-dual: no positive Kähler form makes them primitive. They were discarded.

## Results (search-based upper bounds)

| Ω/i (Ω₁₁, Ω₁₂, Ω₂₂) | φ/i | min N | rank at min N (all 10 / hierarchy block of 5) | min N with all 10 moduli fixed | m_c/m_t, m_u/m_c at Ω |
|---|---|---|---|---|---|
| (4, 1, 4) | 1 | **8** | 6 / **0** | 608 | 1.5·10⁻², 2.3·10⁻⁴ |
| (4, ½, 4) | 2 | 16 | 6 / 0 | 17 964 | 1.9·10⁻³, 1.5·10⁻² |
| (4, ¾, 3) | 2 | 48 | 6 / 0 | 27 392 | 5.3·10⁻³, 1.9·10⁻³ |
| (17/4, ¾, 5) | 2 | 68 | 6 / 0 | 514 148 | 3.2·10⁻³, 1.9·10⁻³ |

**Low tadpoles exist but fix the wrong moduli.** Primitive flux vacua exist at every tested point, and the smallest
tadpoles (8, 16) are within the bound. But these fluxes **leave the hierarchy moduli flat**: the holomorphic mass matrix
restricted to (Ω₁₁, Ω₁₂, Ω₂₂, τ₃, φ) has rank 0.

**Fixing everything costs far too much.** Fixing all ten complex moduli needs N in the hundreds at the simplest point
(608 in the certified run, 488 with another seed) and 10⁴–5·10⁵ nearer the hierarchy point. That is far above the
orientifold bound. The points closest to the observed up ratios have both the largest minimum tadpoles and the largest
full-fixing tadpoles.

## Reading

On the toroidal orientifold, the hierarchy point is **not flux-stabilisable within the tadpole budget**. The route of
Pass 11912 needs one of:
* a compactification with a much larger D3 budget, for example F-theory on a fourfold with χ/24 ≫ 16;
* another mechanism for the Siegel block, for example non-perturbative effects.

## Not established

* **Search bounds.** The minima are search-based upper bounds: coefficients in [−2, 2] on the reduced basis, plus 40,000
  random combinations. They are not proven minima.
* **Kähler form.** Primitivity is imposed with one natural Kähler form, h = (Im T)⁻¹. Other Kähler forms could change the
  minimum tadpoles.
* **Flux parity.** Orientifold quantisation (even fluxes, exotic O3 planes) is quoted, not modelled.

## Prior art

* Giddings–Kachru–Polchinski (2002).
* Kachru–Schulz–Trivedi (2003): the T⁶/ℤ₂ orientifold.
* Denef–Douglas (flux statistics).
* Corpus: 11912.
* TOE49 (parallel exact Siegel parity).
