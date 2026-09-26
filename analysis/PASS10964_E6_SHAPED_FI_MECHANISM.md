# Pass 10964 — why the FI term forces a sneutrino: one E6-shaped U(1)

Producer: `analysis/w33_pass10964_e6_shaped_fi_mechanism.py`
Certificate: `data/w33_pass10964_e6_shaped_fi_mechanism.json`
Regression: `tests/test_w33_pass10964_e6_shaped_fi_mechanism.py` (25 tests, ~60 s)

## From a census to a mechanism

Pass 10960 proved that in the 23 W(3,3) Z6-I Standard Models with FI-cancelling D-flat
singlet directions, every such direction condenses a singlet whose 3(B−L) = 3 is fixed by
the Standard Model. Its Farkas certificates were arbitrary LP vertices. This pass asks for
a **canonical certificate of prescribed physical shape** and finds it in every model:

    f = s·Q_anom + λ·Q_nonanom         (a U(1) direction of the model)
    f = 24/5 μ  on every q, u^c, e^c    (the SU(5) 10)
    f =  8/5 μ  on every d^c, l         (the SU(5) 5̄)
    μ > 0,   f ≥ 0 on every singlet that can be matter-even for some B−L.

Exact cdd (GMP) LP, every constraint re-verified in rational arithmetic.

## Result (all 23 models, no exceptions)

* The shaped certificate exists in **23 of 23** models.
* On Standard-Model singlets f/μ takes **only the values −8, 0, +8**; on the Higgs-type
  doublets **−48/5 and −8/5**.
* The singlets with f < 0 are exactly (a subset of) the forced B−L = +1 singlets, and all sit
  at **f = −8μ**.

Since D-flatness makes the f-D-term Σ f(q_i)|φ_i|² equal to the FI contribution (negative),
some f < 0 singlet must condense — and those are the forced ones.

## Identification

On the families, f/μ = 4 Q_ψ − (4/5) Q_χ with Q_χ = 4Y − 5(B−L) and the matter in the 16_1
of E6 ⊃ SO(10) × U(1)_ψ (27 = 16_1 + 10_{−2} + 1_4): this reproduces 24/5 on the 10 and 8/5
on the 5̄, and −48/5 on an H_u in the 10_{−2}. A singlet with (B−L, Y) = (1, 0) has
Q_χ = −5, and f = −8 then requires Q_ψ = −3: the Standard-Model-singlet (ν^c) direction of
the **16_{−3} ⊂ 78** of E6 — the matter-odd adjoint sector already made objectwise in
`analysis/EXECUTE_ALL5_20260921_CONSTRUCTIVE_CLOSURES.md` item 3
(`w33_z6_objectwise_33_48_32_carrier.py`: 32 = 16_{−3} + 16̄_{+3}). The +8 singlets are
consistent with ν^c of the matter 16_1 or the conjugate 16̄_{+3}; the 0 singlets with SO(10)
× U(1)_ψ neutral directions.

So: **the anomalous U(1) acts on the SM singlets like the E6 generator 5Q_ψ − Q_χ, and the
only singlets that can balance it are right-handed-sneutrino directions of the matter-odd
adjoint 16_{−3}.** That is why matter parity breaks.

## Secondary census

For the 64 models with no D-flat direction at all, the same shaped certificate (now with
f ≥ 0 on every singlet) exists in 35; the other 29 are closed by the non-shaped Farkas
vectors of Pass 10960.

## Scope

The identification with (Q_χ, Q_ψ) is read off from the families' values and the forced
singlets' (B−L, Y); it is an interpretation of an exact certificate, not a claim that the
orbifold's U(1)s are literally E6 generators. The certificate itself is exact.
