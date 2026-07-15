#!/usr/bin/env python3
"""Pass 263: who else is on the light cone?  A survey of all four sectors.

Pass 257 showed the charged leptons are NULL for the S3-invariant Lorentzian
form eta = 2 P_singlet - I (signature (1,2)) -- Koide's Q = 2/3 exactly.  Is the
light cone a universal feature of the substrate's mass vectors, or a
charged-lepton accident?  This witness surveys every sector.

The key structural fact used throughout:
    Q(z) = |z|^2 / (z.u)^2 = 1/(3 cos^2 theta)   with u = (1,1,1),
so for NON-NEGATIVE masses Q is confined to
    Q in [1/3, 1),
    Q = 1/3  <=>  fully degenerate (z parallel to the singlet, timelike);
    Q -> 1   <=>  one mass dominating (maximally hierarchical);
    Q = 2/3  <=>  NULL (the light cone), theta = 45 deg.

For the NEUTRINOS the absolute scale is unknown but the splittings are measured,
so we can ASK THE SUBSTRATE A QUESTION: is there any lightest-mass value m_min
that puts the neutrino vector on the cone?  If yes, the light-cone condition
PREDICTS the absolute neutrino mass scale (testable against cosmology).  We scan
m_min over both orderings and report the attainable range of Q.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass263_lightcone_survey.json"

# charged leptons: pole masses (MeV)
LEPTONS = {"e": 0.51099895000, "mu": 105.6583755, "tau": 1776.86}
# quarks (MeV, MS-bar; scale-dependent, used indicatively)
UP = {"u": 2.16, "c": 1270.0, "t": 172760.0}
DOWN = {"d": 4.67, "s": 93.4, "b": 4180.0}
# neutrino mass-squared splittings (eV^2)
DM21 = 7.53e-5
DM31_NO = 2.453e-3
DM32_IO = -2.536e-3


def Q_of(masses):
    z = np.array([math.sqrt(m) for m in masses], dtype=float)
    return float(np.sum(z ** 2) / (np.sum(z) ** 2)), z


def theta_of(z):
    u = np.ones(3) / math.sqrt(3.0)
    return math.degrees(math.acos(float(np.dot(z, u) / np.linalg.norm(z))))


def null_defect(z):
    u = (np.ones(3) / math.sqrt(3.0)).reshape(3, 1)
    eta = 2 * (u @ u.T) - np.eye(3)
    return float(z @ eta @ z) / float(z @ z)


def nu_masses(m_min, ordering):
    if ordering == "NO":
        m1 = m_min
        m2 = math.sqrt(m1 ** 2 + DM21)
        m3 = math.sqrt(m1 ** 2 + DM31_NO)
    else:  # IO: m3 is lightest
        m3 = m_min
        m2 = math.sqrt(m3 ** 2 + abs(DM32_IO))
        m1 = math.sqrt(m2 ** 2 - DM21)
    return [m1, m2, m3]


def main():
    checks = {}
    sectors = {}

    # ---- charged leptons: on the cone
    Ql, zl = Q_of(list(LEPTONS.values()))
    sectors["charged_leptons"] = {
        "Q": Ql, "theta_deg": theta_of(zl), "null_defect": null_defect(zl),
        "on_cone": bool(abs(Ql - 2 / 3) < 1e-4),
    }
    checks["leptons_on_cone"] = sectors["charged_leptons"]["on_cone"]

    # ---- quarks: off the cone
    Qu, zu = Q_of(list(UP.values()))
    Qd, zd = Q_of(list(DOWN.values()))
    sectors["up_quarks"] = {"Q": Qu, "theta_deg": theta_of(zu),
                            "null_defect": null_defect(zu),
                            "on_cone": bool(abs(Qu - 2 / 3) < 1e-2)}
    sectors["down_quarks"] = {"Q": Qd, "theta_deg": theta_of(zd),
                              "null_defect": null_defect(zd),
                              "on_cone": bool(abs(Qd - 2 / 3) < 1e-2)}
    checks["up_quarks_off_cone"] = not sectors["up_quarks"]["on_cone"]
    checks["down_quarks_off_cone"] = not sectors["down_quarks"]["on_cone"]

    # ---- the Q window for non-negative masses is [1/3, 1)
    rng = np.random.default_rng(3)
    win_ok = True
    for _ in range(5000):
        m = rng.uniform(0, 10, 3)
        Qr, _ = Q_of(m)
        if not (1 / 3 - 1e-9 <= Qr < 1.0 + 1e-9):
            win_ok = False
            break
    checks["Q_window_third_to_one"] = win_ok
    # degenerate => 1/3 ; single dominant => -> 1
    checks["degenerate_gives_third"] = abs(Q_of([1, 1, 1])[0] - 1 / 3) < 1e-12
    checks["dominant_approaches_one"] = Q_of([1e-12, 1e-12, 1.0])[0] > 0.99

    # ---- NEUTRINOS: can any mass scale put them on the cone?
    nu = {}
    for ordering in ("NO", "IO"):
        qs = []
        grid = np.concatenate([np.zeros(1), np.logspace(-5, 0.5, 4000)])
        for m_min in grid:
            Qn, _ = Q_of(nu_masses(float(m_min), ordering))
            qs.append(Qn)
        qs = np.array(qs)
        qmax, qmin = float(qs.max()), float(qs.min())
        reachable = bool(qmin - 1e-6 <= 2 / 3 <= qmax + 1e-6)
        nu[ordering] = {
            "Q_at_zero_lightest": float(qs[0]),
            "Q_max_over_scale": qmax,
            "Q_min_over_scale": qmin,
            "two_thirds_reachable": reachable,
            "masses_at_zero_lightest_eV": nu_masses(0.0, ordering),
        }
        checks[f"nu_{ordering}_cannot_reach_two_thirds"] = not reachable
    sectors["neutrinos"] = nu

    # the maximum neutrino Q is attained at zero lightest mass (max hierarchy)
    checks["nu_NO_max_at_zero"] = abs(
        nu["NO"]["Q_max_over_scale"] - nu["NO"]["Q_at_zero_lightest"]) < 1e-6
    # and it falls short of 2/3
    checks["nu_NO_max_below_two_thirds"] = nu["NO"]["Q_max_over_scale"] < 2 / 3
    checks["nu_IO_max_below_two_thirds"] = nu["IO"]["Q_max_over_scale"] < 2 / 3

    all_pass = all(v for v in checks.values() if isinstance(v, bool))
    payload = {
        "schema": "w33.pass263.lightcone_survey.v1",
        "status": "PASS" if all_pass else "FAIL",
        "structure": {
            "Q_identity": "Q = 1/(3 cos^2 theta), u = (1,1,1) the S3 singlet",
            "window": "for non-negative masses Q in [1/3, 1): 1/3 = degenerate "
                      "(timelike), 2/3 = NULL (light cone), ->1 = one dominant",
        },
        "sectors": sectors,
        "neutrino_verdict": (
            "DECISIVE NEGATIVE: the neutrinos can NOT be placed on the light "
            "cone at any absolute mass scale. Q is maximised at zero lightest "
            f"mass (maximum hierarchy), giving only Q = {nu['NO']['Q_max_over_scale']:.4f} "
            f"(normal) and {nu['IO']['Q_max_over_scale']:.4f} (inverted), both "
            "short of 2/3; increasing the scale drives Q toward the degenerate "
            "value 1/3. The measured splittings are simply not hierarchical "
            "enough. So the light-cone condition does NOT fix the neutrino mass "
            "scale -- it excludes the neutrinos from the cone entirely."
        ),
        "reading": (
            "The light cone of the family clock is a CHARGED-LEPTON phenomenon, "
            "not a universal law of the substrate's mass vectors. The charged "
            "leptons sit on it to five digits; the up quarks (Q = 0.849) and "
            "down quarks (Q = 0.731) sit off it; and the neutrinos cannot reach "
            "it for ANY absolute scale, in either ordering, because their "
            "measured splittings cap Q below 2/3. This is a sharp, falsifiable "
            "negative that kills the natural 'everything is null' extrapolation "
            "and leaves the charged-lepton nullness as the single fact needing "
            "explanation -- consistent with Pass 236/259, where it is the "
            "charged leptons (not quarks, not neutrinos) that align to the "
            "family clock."
        ),
        "checks": {k: bool(v) for k, v in checks.items() if isinstance(v, bool)},
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
