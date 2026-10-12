# Pass 11931: the theta-zero law of the blow-up-protected Higgs needs the Eisenstein flux

Producer: `analysis/w33_pass11931_theta_zero_needs_eisenstein_flux.py`
Certificate: `data/w33_pass11931_theta_zero_needs_eisenstein_flux.json`
Regression: `tests/test_w33_pass11931.py`
Track: Claude. This is a robustness test of Pass 11930.

## Test

At the Eisenstein point Ω = ω·1, every symmetric det-3 flux N is compatible and ρ-invariant. For each of the 12
det-3 forms with entries ≤ 4, I took:
* the channel N × N, with mediator flux 2N (12 modes);
* the mediator modes vanishing at all 9 ρ-fixed points;
* the spectrum of random members of that protected space.

## Result

| flux class | forms | fixed-point rank | protected dim | spectrum |
|---|---|---|---|---|
| A₂ (Eisenstein norm form): A₂, A₂′ | 2 | 8 | 4 | **(1, 1, 0) exactly** (deviation ~10⁻¹⁴) |
| x² + 3y² | 10 | 6 | 6 | generic, deviation from (1, 1, 0) between 0.5 and 0.9 |

## Reading

**When the law holds.** The theta-zero law of the blow-up-protected mediator holds only when flux lattice and complex
structure are **Eisenstein together**. Of the two classes of det-3 binary forms (Pass 11915), only the A₂ class supports
it.

**What follows for Pass 11930.** The conditional inverted-ordering reading inherits this condition. It is a property of
the A₂ flux at the Eisenstein point, the same pairing the W(3,3) structure singles out elsewhere (Passes 11897 and 11916),
and not of generic magnetized orbifolds.
