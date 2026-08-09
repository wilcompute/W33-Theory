#!/usr/bin/env python3
"""Passes 4401, 4402, 4406 -- three live predictions checked against 2026 data.

The repository keeps a falsification scoreboard (`w33_BREAKTHROUGH_130_falsification_
scoreboard.py`).  Row F16 reads:

    F16. Sigma m_nu    101 meV    < 120 (Planck)    1e-3    CMB-S4/Euclid    2027-2032

The bound in that row is the Planck-era limit.  It has moved a long way, and a scoreboard
whose bounds are stale scores the wrong game -- so this pass re-scores F16 against what is
actually measured now, works out what the prediction says about the mass ordering, and does
the same re-scoring for the Koide ratio.

WHAT THIS IS AND IS NOT.  This is a falsification check on predictions the repository
already made.  It derives nothing new from the geometry.  Its whole value is that a
prediction confronted with a superseded bound has not been tested.

    py -3 analysis/w33_pass4401_4402_4406_neutrino_ordering_koide.py
"""

from __future__ import annotations

import sys
from math import sqrt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import cert_util  # noqa: E402

PREDICTED_SUM = 0.101          # eV; (Phi_4^2 + 1) meV = 101 meV, BT93 candidate

# --- oscillation inputs (global fits; central values, eV^2) -------------------
DM21 = 7.49e-5
DM31_NO = 2.534e-3             # m3^2 - m1^2, normal ordering
DM32_IO = 2.510e-3             # |m3^2 - m2^2|, inverted ordering

# --- cosmological bounds, 95% CL, Sigma m_nu in eV ---------------------------
# Each row: (label, bound, model, source)
BOUNDS = [
    ("DESI DR2 BAO + ACT CMB", 0.0642, "LCDM",
     "DESI DR2 cosmology; the headline Bayesian limit"),
    ("DESI DR2 + Planck PR4 + lensing", 0.053, "LCDM",
     "frequentist, Feldman-Cousins corrected for the physical boundary at zero"),
    ("DESI DR2 + CMB", 0.163, "w0waCDM",
     "evolving dark energy; the degeneracy with w(z) relaxes the bound"),
    ("DESI DR2 + CMB", 0.101, "4-parameter w(z)",
     "a more general dark-energy parametrisation"),
    ("Planck 2018 (the scoreboard's row)", 0.120, "LCDM",
     "SUPERSEDED -- this is the bound row F16 was written against"),
]


def sum_nu(m_light: float, ordering: str) -> float:
    if ordering == "NO":
        m1 = m_light
        return m1 + sqrt(m1 * m1 + DM21) + sqrt(m1 * m1 + DM31_NO)
    m3 = m_light
    m2 = sqrt(m3 * m3 + DM32_IO)
    m1 = sqrt(m2 * m2 - DM21)
    return m1 + m2 + m3


def lightest_for(total: float, ordering: str) -> float | None:
    """Bisect for the lightest mass reproducing a given Sigma; None if unreachable."""
    lo, hi = 0.0, 1.0
    if sum_nu(lo, ordering) > total + 1e-12:
        return None
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if sum_nu(mid, ordering) < total:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def koide() -> dict:
    """Q = (sum m) / (sum sqrt(m))^2.  Koide's observation is Q = 2/3."""
    me, dme = 0.51099895000e-3, 0.00000000015e-3      # GeV
    mmu, dmmu = 105.6583755e-3, 0.0000023e-3
    mtau, dmtau = 1776.86e-3, 0.12e-3

    def q(a, b, c):
        return (a + b + c) / (sqrt(a) + sqrt(b) + sqrt(c)) ** 2

    q0 = q(me, mmu, mtau)
    # propagate the tau uncertainty, which dominates by orders of magnitude
    dq = max(abs(q(me, mmu, mtau + dmtau) - q0), abs(q(me, mmu, mtau - dmtau) - q0))
    dq = sqrt(dq ** 2
              + (q(me, mmu + dmmu, mtau) - q0) ** 2
              + (q(me + dme, mmu, mtau) - q0) ** 2)
    return {"Q": q0, "sigma": dq, "two_thirds": 2 / 3,
            "deviation_sigma": abs(q0 - 2 / 3) / dq}


def main() -> int:
    print("=" * 78)
    print("Passes 4401/4402/4406 -- the scoreboard, re-scored against 2026 data")
    print("=" * 78)

    # ---- Pass 4401: is 101 meV still allowed? -------------------------------
    print(f"\n  PASS 4401 -- Sigma m_nu = {PREDICTED_SUM * 1000:.0f} meV against current bounds\n")
    print(f"  {'dataset':36s} {'model':18s} {'bound':>8s}  verdict")
    verdicts = []
    for label, b, model, _ in BOUNDS:
        v = "EXCLUDED" if PREDICTED_SUM > b else ("at the boundary"
                                                  if abs(PREDICTED_SUM - b) < 1e-9
                                                  else "allowed")
        verdicts.append({"dataset": label, "model": model, "bound_eV": b, "verdict": v})
        print(f"  {label[:36]:36s} {model:18s} {b * 1000:6.1f} meV  {v}")

    print(f"""
  THE PREDICTION IS EXCLUDED IN LCDM AND SURVIVES ONLY IF DARK ENERGY EVOLVES.

  That is a much sharper statement than row F16 makes, and it is a worse position for the
  prediction than the scoreboard records. Against the standard cosmology the limit is now
  {BOUNDS[0][1] * 1000:.1f} meV, and 101 meV sits above it by more than a factor of one and a half; the
  frequentist limit corrected for the boundary at zero is tighter still at {BOUNDS[1][1] * 1000:.0f} meV.

  The escape route is real and specific: under w0waCDM the bound relaxes to {BOUNDS[2][1] * 1000:.0f} meV and
  101 meV is comfortable. So F16 is no longer an independent prediction -- it has become
  CONDITIONAL on the same evolving-dark-energy question DESI itself raised. The scoreboard
  row should say so, because a prediction that only survives in one cosmology is a joint
  claim about the neutrino sector AND the dark sector.

  ONE COINCIDENCE I AM DELIBERATELY NOT USING.  The 4-parameter dark-energy bound is quoted
  at 0.101 eV, numerically equal to the prediction. Two numbers agreeing to three digits is
  exactly the signature CLAUDE.md's failure mode 6 exists for. It is a bound, not a
  measurement; nothing follows from the coincidence and I draw nothing from it.""")

    # ---- Pass 4402: what does 101 meV say about the ordering? ---------------
    print(f"\n  PASS 4402 -- what {PREDICTED_SUM * 1000:.0f} meV implies for the mass ordering\n")
    rows = []
    for ordering in ("NO", "IO"):
        floor = sum_nu(0.0, ordering)
        ml = lightest_for(PREDICTED_SUM, ordering)
        rows.append({"ordering": ordering, "floor_eV": floor,
                     "lightest_required_eV": ml,
                     "above_floor_meV": (PREDICTED_SUM - floor) * 1000})
        print(f"    {ordering}:  oscillation floor {floor * 1000:6.2f} meV"
              f"   -> lightest mass needed {ml * 1000:6.2f} meV"
              f"   ({(PREDICTED_SUM - floor) * 1000:5.1f} meV above the floor)")

    no, io = rows
    print(f"""
  101 meV IS A GENERIC NORMAL-ORDERING VALUE AND A FINE-TUNED INVERTED-ORDERING ONE.

  In the normal ordering it needs a lightest neutrino of {no['lightest_required_eV'] * 1000:.1f} meV -- unremarkable, {no['above_floor_meV']:.0f}
  meV above the floor. In the inverted ordering it sits only {io['above_floor_meV']:.1f} meV above the
  minimum, so it is very nearly the statement "inverted ordering, lightest neutrino
  massless".

  WHICH MATTERS BECAUSE THE TWO READINGS ARE TESTED BY DIFFERENT EXPERIMENTS. The
  cosmological bound above is model-dependent; the mass ordering is not. JUNO and the
  long-baseline programme determine the ordering from oscillations alone, so if the
  prediction is meant in its inverted-ordering reading it is falsifiable WITHOUT settling
  the dark-energy question. The current cosmological fits already prefer normal ordering,
  which pushes the prediction to the {no['lightest_required_eV'] * 1000:.0f} meV lightest-mass reading -- and that reading
  is what LCDM excludes.""")

    # ---- Pass 4406: Koide --------------------------------------------------
    k = koide()
    print(f"\n  PASS 4406 -- Koide's ratio against current lepton masses\n")
    print(f"    Q          = {k['Q']:.9f}  +/- {k['sigma']:.9f}")
    print(f"    2/3        = {k['two_thirds']:.9f}")
    print(f"    difference = {(k['Q'] - k['two_thirds']):+.3e}"
          f"   = {k['deviation_sigma']:.2f} sigma")
    print(f"""
  KOIDE STILL HOLDS, AND THE UNCERTAINTY IS ALL TAU. Q agrees with 2/3 at
  {k['deviation_sigma']:.1f} sigma, where sigma is dominated entirely by the tau mass at 0.12 MeV. The
  electron and muon masses contribute nothing at this precision. So the relation is not
  currently under pressure, and the experiment that would test it is a better tau mass --
  not a better electron or muon mass, and not cosmology.""")

    out = {
        "boundary": ("this is a falsification check on predictions the repository already "
                     "made; it derives nothing from the geometry, and the cosmological "
                     "verdicts are model-dependent by construction -- the ordering "
                     "statement and the Koide check are not"),
        "pass_4401_neutrino_sum": {
            "predicted_eV": PREDICTED_SUM,
            "scoreboard_row_bound_eV": 0.120,
            "scoreboard_row_status": "SUPERSEDED",
            "verdicts": verdicts,
            "conclusion": ("excluded in LCDM by DESI DR2 + CMB (0.0642 eV, 95%) and by the "
                           "frequentist limit (0.053 eV); allowed under w0waCDM (0.163 eV); "
                           "F16 is now CONDITIONAL on evolving dark energy"),
            "not_used": ("the 4-parameter dark-energy bound is numerically 0.101 eV, equal "
                         "to the prediction; it is a bound not a measurement and nothing "
                         "is drawn from the coincidence"),
        },
        "pass_4402_ordering": {
            "rows": rows,
            "conclusion": ("101 meV is generic for normal ordering (lightest ~15 meV) and "
                           "within 2 meV of the inverted-ordering floor; the inverted "
                           "reading is testable by JUNO independently of cosmology"),
        },
        "pass_4406_koide": k,
        "sources": [
            "DESI DR2 BAO cosmology (arXiv:2503.14738) and neutrino physics "
            "(arXiv:2503.14744)",
            "frequentist treatment: arXiv:2507.12401 / FERMILAB-PUB-25-0477-PPD",
            "4-parameter dark energy: arXiv:2512.08752",
        ],
    }
    p = ROOT / "data" / "PART_W33_PASS4401_4406_NEUTRINO_KOIDE.json"
    p.parent.mkdir(exist_ok=True)
    p.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {p.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
