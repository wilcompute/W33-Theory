# Pass 4569 — two scoreboard rows were falsified by the numbers printed beside them

A full re-scoring of `w33_BREAKTHROUGH_130_falsification_scoreboard.py` against 2026 data
found the expected staleness — but the two most serious findings are not staleness at all.
**Two rows were already dead when the board was written, and the board contains the
refuting numbers.**

## F6 — α⁻¹ is excluded at 13,566 σ, and a rounding hid it

The row reads:

```
F6. alpha^-1    137 + 1/28    137.036 (CODATA)    1e-12    CODATA    ongoing
```

| | value |
|---|---|
| predicted `137 + 1/28` | 137.035714286 |
| CODATA 2022 | 137.035999177 ± 0.000000021 |
| difference | 0.000284891 |
| **discrepancy** | **13,566 σ** |

The prediction is wrong in the **fourth decimal place**. The row survives only because the
observed value is quoted as `137.036` — rounded to three decimals, at which point both
numbers read 137.036 and the disagreement vanishes. At six decimals they are
137.035714 and 137.035999, and they never agreed.

This is not a bound that moved. **The row was refuted at the moment it was typed**, by a
constant that has been known to this precision since long before the board existed. The
`1e-12` in the precision column makes it worse: it asserts the comparison is meaningful at
a part in 10¹², while the quoted bound is stated to a part in 10⁵.

## F1 — proton decay, falsified by the bound in its own row

```
F1. tau_proton    ~10^33 yr    > 1.6e34 (SK)    1e35 (HypK)    Hyper-K    2030-2040
```

The prediction is `~10³³ yr`. The bound **printed in the same row** is `> 1.6 × 10³⁴ yr`.
The prediction is sixteen times *below* the limit the row itself records, and it is scored
as pending a 2030–2040 test.

Current Super-Kamiokande limits, all above the prediction:

| mode | limit | exposure |
|---|---|---|
| p → e⁺π⁰ | > 2.4 × 10³⁴ yr | 450 kton·yr |
| p → μ⁺π⁰ | > 1.6 × 10³⁴ yr | |
| p → e⁺η | > 1.4 × 10³⁴ yr | 0.373 Mton·yr (2024) |
| p → e⁺π⁰π⁰ | > 7.2 × 10³³ yr | 0.401 Mton·yr (2026) |

## The class both belong to

Neither row failed because the world moved. Both failed a comparison **the board itself had
all the numbers to perform**. That is the untested-premise mode (`CLAUDE.md` failure mode 6)
in its purest form: a comparison computed and displayed without checking it was licensed —
here, without checking whether the two quantities being compared were even quoted to
compatible precision.

## Four rows cannot be falsified at all

F10 (WIMP at 2143 GeV), F12 (3.215 TeV scalar), F13 (γ-line at 2.142 TeV) and F14 (GW at
~22 GHz) each predict **a mass or a frequency and nothing else** — no cross section, no rate,
no amplitude. No experiment can exclude them however sensitive it becomes. Scoring them
"ALLOWED" would be exactly the error the failure-mode guard exists to prevent; the correct
verdict is **not falsifiable as stated**.

The mirror problem: F3 (`T_ν/T_CMB = (4/11)^⅓`) and F5 restate consequences of the Standard
Model and of quantum mechanics respectively. They cannot discriminate this theory from the
textbook, so agreement carries no evidential weight either.

**So of sixteen rows, six are not tests.** That is the number worth acting on, more than any
individual verdict.

## One row moved toward the theory

**F7, the Higgs mass.** PDG 2026 now lists **125.13 ± 0.11 GeV**, down from 125.20 ± 0.11.
The prediction of exactly `5³ = 125` improves from 1.8 σ to **1.2 σ**.

The caveat matters: the PDG error carries a scale factor S = 1.5. Unscaled (± 0.073) the
tension is still ≈ 1.8 σ. So the improvement is partly a change in how the disagreement
*between experiments* is handled, not purely a change in the central value — and the honest
statement is that F7 remains the board's tightest live, model-independent test.

## Also updated

- **F15** is stale in the other direction: the board says "no test / 2030+", but electroweak
  precision reached 1.2 × 10⁻⁴ in 2024 (CMS m_W = 80360.2 ± 9.9 MeV vs SM 80357 ± 6), six
  years early, and found no anomaly.
- **F4** (ΔH₀ = q! = 6) fits SH0ES − Planck at 0.3 σ but only 1.1 σ against DESI's
  68.53 ± 0.80. If local H₀ keeps falling this row goes into tension.
- **F2**'s stored bound ("> 1 TeV") is not a bound on a trilinear coupling at all; the row is
  ill-formed. Recast as κ_λ ≈ 0.50, it sits inside ATLAS's −0.71 < κ_λ < 6.1.

## Evidence boundary

The α and proton-decay arithmetic is exact and was recomputed here independently of the
survey. The experimental limits are quoted from the sources listed in the survey and were
not re-derived. The claim that F10/F12/F13/F14 are unfalsifiable is a statement about **the
rows as written** — a fuller model supplying a cross section would make them testable, and
whether the underlying theory supplies one is not assessed here. No row of the scoreboard
file was edited; this is an appended finding.
