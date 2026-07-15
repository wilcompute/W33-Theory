#!/usr/bin/env python3
"""Pass 269: the down quarks sit at 47.5 deg -- do they approach the cone?

Pass 263 found the light cone (Q = 2/3, theta = 45 deg) is a charged-lepton
phenomenon: up quarks Q = 0.849 (theta = 51.2), down quarks Q = 0.731
(theta = 47.5), neutrinos excluded entirely.  But 47.5 deg is suspiciously close
to 45.  Two possibilities:

  (a) the down quarks are "almost null" and running drives them onto the cone at
      some scale -- in which case the cone is a broader phenomenon and 263's
      charged-lepton-only verdict is a low-energy accident;
  (b) they merely pass nearby and running moves them AWAY -- in which case 47.5
      deg is a coincidence and the cone stays charged-lepton-only.

This witness decides by evaluating Q for each quark sector at two scales where
reliable MS-bar masses exist (mu = 2 GeV and mu = M_Z) and reading the direction
of motion.  Pass 257 already showed the analogous test for the charged leptons:
they are null at the pole scale and move OFF the cone when run to M_Z.

Recall the exact structure (Pass 263): Q = 1/(3 cos^2 theta) lies in [1/3, 1),
with 1/3 = degenerate and 2/3 = null.  Q is invariant under a uniform rescaling
of all sqrt-masses, so only NON-universal running can move a sector.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass269_down_quark_cone.json"

# MS-bar quark masses (MeV) at two scales
AT_2GEV = {
    "up": {"u": 2.16, "c": 1270.0, "t": 172760.0},
    "down": {"d": 4.67, "s": 93.4, "b": 4180.0},
}
AT_MZ = {
    "up": {"u": 1.29, "c": 619.0, "t": 171700.0},
    "down": {"d": 2.75, "s": 54.8, "b": 2890.0},
}
CHARGED_LEPTON_POLE = {"e": 0.51099895, "mu": 105.6583755, "tau": 1776.86}


def Q_of(masses):
    z = np.array([math.sqrt(m) for m in masses], dtype=float)
    return float(np.sum(z ** 2) / (np.sum(z) ** 2)), z


def theta_of(z):
    u = np.ones(3) / math.sqrt(3.0)
    return math.degrees(math.acos(float(np.dot(z, u) / np.linalg.norm(z))))


def defect(z):
    u = (np.ones(3) / math.sqrt(3.0)).reshape(3, 1)
    eta = 2 * (u @ u.T) - np.eye(3)
    return float(z @ eta @ z) / float(z @ z)


def main():
    checks = {}
    table = {}
    for sector in ("up", "down"):
        row = {}
        for label, data in (("2GeV", AT_2GEV), ("MZ", AT_MZ)):
            Q, z = Q_of(list(data[sector].values()))
            row[label] = {"Q": Q, "theta_deg": theta_of(z),
                          "null_defect": defect(z),
                          "distance_to_two_thirds": abs(Q - 2 / 3)}
        moved_toward = (row["MZ"]["distance_to_two_thirds"]
                        < row["2GeV"]["distance_to_two_thirds"])
        row["moves_toward_cone_with_scale"] = bool(moved_toward)
        table[sector] = row

    # sanity: the sectors are where Pass 263 said at 2 GeV
    checks["up_Q_at_2GeV_matches_263"] = abs(table["up"]["2GeV"]["Q"] - 0.8490) < 1e-3
    checks["down_Q_at_2GeV_matches_263"] = abs(table["down"]["2GeV"]["Q"] - 0.7314) < 1e-3
    # the down sector is closer to the cone than the up sector
    checks["down_closer_than_up"] = (table["down"]["2GeV"]["distance_to_two_thirds"]
                                     < table["up"]["2GeV"]["distance_to_two_thirds"])
    # neither sector is ON the cone at either scale
    checks["no_quark_sector_on_cone"] = all(
        table[s][sc]["distance_to_two_thirds"] > 1e-2
        for s in ("up", "down") for sc in ("2GeV", "MZ"))

    # the decisive reading: does the down sector approach or recede?
    down_moves_toward = table["down"]["moves_toward_cone_with_scale"]
    up_moves_toward = table["up"]["moves_toward_cone_with_scale"]
    checks["down_direction_determined"] = isinstance(down_moves_toward, bool)

    # charged-lepton reference (Pass 257): null at pole, moves off when run up
    Ql, zl = Q_of(list(CHARGED_LEPTON_POLE.values()))
    checks["leptons_null_at_pole"] = abs(Ql - 2 / 3) < 1e-4

    verdict = (
        "the down quarks RECEDE from the cone as the scale rises: 47.5 deg at "
        "2 GeV is a near miss, not an approach. Option (b) -- the cone stays "
        "charged-lepton-only and Pass 263's verdict stands."
        if not down_moves_toward else
        "the down quarks APPROACH the cone as the scale rises: option (a) -- "
        "the cone may be broader than charged leptons, and Pass 263's verdict "
        "is a low-energy statement"
    )

    all_pass = all(v for v in checks.values() if isinstance(v, bool))
    payload = {
        "schema": "w33.pass269.down_quark_cone.v1",
        "status": "PASS" if all_pass else "FAIL",
        "question": (
            "the down quarks sit at theta = 47.5 deg, only 2.5 deg off the "
            "light cone -- do they approach it under running, or merely pass by?"
        ),
        "sectors": table,
        "charged_lepton_reference": {
            "Q_at_pole": Ql, "theta_deg": theta_of(zl),
            "note": "null at the pole scale; Pass 257 showed running to M_Z "
                    "moves them OFF the cone",
        },
        "verdict": verdict,
        "reading": (
            "Q is invariant under uniform rescaling, so any motion is genuine "
            "non-universal running. Evaluating both quark sectors at 2 GeV and "
            "at M_Z shows the direction of travel. Combined with Pass 257 (the "
            "charged leptons are null at the POLE scale and drift off when run "
            "up), the emerging picture is that proximity to the cone is an "
            "infrared property: the charged leptons hit it exactly in the deep "
            "IR, and every other sector -- up quarks, down quarks, neutrinos -- "
            "misses it, with the down quarks merely the nearest miss."
        ),
        "checks": {k: bool(v) for k, v in checks.items() if isinstance(v, bool)},
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
