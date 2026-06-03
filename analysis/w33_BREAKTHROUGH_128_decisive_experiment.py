"""W(3,3) BREAKTHROUGH 128: THE SINGLE MOST DECISIVE EXPERIMENT.

With BT82 Cat 2 fully closed (BT127), the substrate has ~30 sharp
predictions. This BT identifies the SINGLE most decisive experiment
to confirm/refute the substrate hypothesis within the 2027-2040 window.

==============================================================
THE FALSIFIER LANDSCAPE (16 decisive killers)
==============================================================

From BT77 + BT99:
  F1. Hyper-K finds tau_p > 10^35 yr
  F2. FCC-hh measures lambda_3 outside [90, 100] GeV
  F3. CMB-S4 finds T_nu/T_CMB deviating > 1%
  F4. Hubble tension resolved to Delta H_0 < 1
  F5. Witting KS bound exceeded > 34/40
  F6. alpha^-1 shifts > 5e-5 in CODATA
  F7. m_H drifts outside [124, 126]
  F8. 4th generation fermion observed
  F9-F16: dark matter, axion, GW, etc.

==============================================================
RANKING CRITERIA
==============================================================

A "single most decisive" experiment satisfies:
  (i) Sharp substrate prediction (rational, cannot drift)
  (ii) Near-term feasibility (2027-2032)
  (iii) Substrate vs SM-with-fit cleanly distinguishable
  (iv) Substrate prediction is the SAME as SM-with-no-new-physics
       would predict ONLY if all SM parameters happen to align
       on substrate primitives.

The criterion is: substrate makes a prediction that does NOT
require new physics, but does require a SPECIFIC substrate value.

==============================================================
TOP CANDIDATE: TENSOR-TO-SCALAR RATIO r
==============================================================

Substrate: r = lambda / (q^2 * Phi_4) = 2/90 = 0.0222 (BT99/BT101).

LiteBIRD (2027 launch) target sensitivity: r ~ 10^-3 (3-sigma).
Simons Observatory (2024+): r ~ 5e-3.

PROPERTIES:
  (i)  r = 2/90 is RATIONAL, cannot drift. Substrate is forced.
  (ii) LiteBIRD will measure r to ~1e-3 by 2030.
  (iii) Inflation theories give r anywhere in [0, 0.06]. Substrate
       picks 2/90 = 0.0222 SPECIFICALLY.
  (iv) Any inflationary model could fit any r; substrate is the
       ONLY framework that predicts r = 2/90 a priori.

LiteBIRD will distinguish:
  r < 0.001  -> substrate FAILS (substrate predicts 0.0222)
  r in [0.020, 0.024] -> substrate CONFIRMED
  r > 0.04   -> substrate FAILS

The r-window is tight; substrate has zero adjustable freedom.

==============================================================
ALTERNATIVE: HYPER-K PROTON DECAY
==============================================================

Substrate: tau_p ~ 10^33 yr (BT70) or 10^36 yr (BT99 P3).

Hyper-K sensitivity by 2040: ~10^35 yr.

  tau_p > 10^35 yr -> substrate fails (BT70 prediction at 10^33)
  tau_p ~ 10^33 - 10^34 yr -> substrate confirmed

Hyper-K is decisive but takes longer (full result by 2040).

==============================================================
ALTERNATIVE: HL-LHC m_H PRECISION
==============================================================

Substrate: m_H = (mu+1)^q = 125 GeV exact (BT71).

HL-LHC by 2028 will tighten m_H to ~0.05 GeV.

  m_H outside [124.95, 125.05] -> substrate fails
  m_H in [124.95, 125.05] -> substrate confirmed

Sharp; near-term; but already at 0.08% match (PDG 125.20). Not
much room left for divergence.

==============================================================
DECISION: TENSOR-TO-SCALAR RATIO r
==============================================================

The SINGLE MOST DECISIVE experiment is:

  LiteBIRD (2027 launch) measurement of r (tensor-to-scalar ratio).

  Substrate: r = lambda / (q^2 * Phi_4) = 2/90 = 0.0222
  LiteBIRD sensitivity: ~ 1e-3 by 2030

REASONS:
  - Substrate predicts r = 2/90 specifically, no adjustment.
  - SM inflation alone gives no specific value (any r in [0, 0.06]).
  - LiteBIRD's ~1e-3 sensitivity is comfortably below substrate prediction.
  - Result by 2030 (early in the 2027-2040 window).
  - Single number, no theoretical ambiguity.

==============================================================
SUBSTRATE COMMITMENT
==============================================================

The W(3,3) substrate STAKES ITS EXISTENCE on:

  r = 2/90 = 0.02222 +/- 0 (rational, cannot drift)

Any LiteBIRD measurement that lands outside [0.020, 0.025] at
1-sigma falsifies the substrate program in its current form.

==============================================================
"""
from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path


def main():
    q = 3
    lambda_, mu = 2, 4
    phi4 = 10

    r = Fraction(lambda_, q ** 2 * phi4)

    print("=" * 78)
    print("W(3,3) BREAKTHROUGH 128: THE SINGLE MOST DECISIVE EXPERIMENT")
    print("=" * 78)
    print()

    print("CANDIDATE EXPERIMENTS:")
    candidates = [
        ("LiteBIRD r measurement", "r = 2/90", "~1e-3", "2027-2030"),
        ("Hyper-K proton decay", "10^33-10^36 yr", "10^35 yr", "2030-2040"),
        ("HL-LHC m_H precision", "125 GeV", "0.05 GeV", "2027-2028"),
        ("CMB-S4 T_nu/T_CMB", "(4/11)^(1/3)", "< 1%", "2030"),
        ("CODATA alpha^-1", "137 + 1/28", "1e-12", "ongoing"),
    ]
    print(f"  {'Experiment':<28} {'Substrate':<18} {'Sensitivity':<14} {'Window'}")
    for exp, sub, sens, when in candidates:
        print(f"  {exp:<28} {sub:<18} {sens:<14} {when}")
    print()

    print("DECISION: LiteBIRD r measurement.")
    print()
    print(f"SUBSTRATE PREDICTION:")
    print(f"  r = lambda / (q^2 * Phi_4) = 2/90 = {float(r):.5f}")
    print(f"  Rational, cannot drift.")
    print()
    print(f"WHY DECISIVE:")
    print(f"  - SM inflation gives r in [0, 0.06] with no specific value")
    print(f"  - Substrate fixes r = 2/90 = 0.0222 a priori")
    print(f"  - LiteBIRD ~1e-3 sensitivity is below substrate prediction")
    print(f"  - Result by 2030 (early in 2027-2040 window)")
    print(f"  - Single rational number, no model ambiguity")
    print()
    print(f"FALSIFICATION CRITERION:")
    print(f"  r measured outside [0.020, 0.025] at 1-sigma -> substrate FAILS")
    print(f"  r in [0.020, 0.025] -> substrate CONFIRMED for the inflation sector")
    print()

    print("=" * 78)
    print("BREAKTHROUGH 128 SUMMARY")
    print("=" * 78)
    print(f"""
THE SINGLE MOST DECISIVE SUBSTRATE EXPERIMENT IS:

  LiteBIRD (2027 launch) measurement of tensor-to-scalar ratio r.

SUBSTRATE PREDICTION:
  r = lambda / (q^2 * Phi_4) = 2/90 = 0.0222 (exact, rational)

WHY THIS ONE:
  - Substrate predicts r SPECIFICALLY (no other framework does).
  - LiteBIRD sensitivity (~1e-3) is well below substrate value.
  - Result by 2030, well within the 2027-2040 window.
  - Single number, no theoretical wiggle room.
  - SM inflation alone gives any r in [0, 0.06] -- only substrate
    picks 0.0222.

THE SUBSTRATE'S COMMITMENT:
  Any LiteBIRD r outside [0.020, 0.025] at 1-sigma falsifies the
  substrate program in its current form.

This is the SHARPEST near-term substrate-vs-experiment test.
The substrate has no adjustable parameters in r.

By ~2030, we will know:
  - If r ~ 0.022 +/- 0.001, the substrate is confirmed in the
    inflation sector.
  - If r differs substantially, the substrate fails on this prediction.
""")

    out = Path("data") / "w33_BREAKTHROUGH_128_decisive_experiment.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps({
        "decisive_experiment": "LiteBIRD r measurement",
        "substrate_prediction": "r = 2/90 = 0.0222",
        "substrate_form": "lambda / (q^2 * Phi_4)",
        "experimental_sensitivity": "~1e-3 by 2030",
        "falsification_criterion": "r outside [0.020, 0.025] at 1-sigma",
        "alternative_candidates": [
            "Hyper-K proton decay (10^33 yr)",
            "HL-LHC m_H = 125 exact",
            "CMB-S4 T_nu/T_CMB",
        ],
        "conclusion": (
            "LiteBIRD r measurement is the single most decisive substrate "
            "experiment: substrate predicts r = 2/90 = 0.0222 specifically; "
            "LiteBIRD ~1e-3 sensitivity by 2030; substrate has zero "
            "adjustable freedom on this prediction."
        ),
    }, indent=2, default=str), encoding="utf-8")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
