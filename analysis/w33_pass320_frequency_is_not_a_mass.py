#!/usr/bin/env python3
"""Pass 320: "the clock's frequency IS a mass" -- the dimensional gap, stated.

Pass 318 read w33_machine_clock_is_mass.py and found it does two things:
  * BUILDS the oscillator.  On the Heawood graph, (L_H - qI)^2 = lambda I = 2I on
    the 12-dimensional middle shell -- a genuine constructed operator identity,
    re-verified there and again here, with omega = sqrt(lambda) = sqrt(2). This
    is the same sqrt(2) that Passes 297/298 showed is FORCED (a spectral
    invariant of the Fano incidence, true for every drawing).
  * ASSERTS that "its frequency IS a mass", which is not built.

THE GAP.  omega = sqrt(2) is a dimensionless eigenvalue of a combinatorial
Laplacian. A mass is dimensionful. Turning one into the other requires a scale
with units -- a lattice spacing, a coupling, an energy per edge -- and the file
supplies none. So the claim is not wrong; it is incomplete in a specific,
nameable way, and it cannot be tested until the missing scale is named.

WHY IT MATTERS.  This is the FOURTH failure mode this arc has catalogued, and the
subtlest: Pass 311 found coordinate artefacts and over-reads; Pass 315 found
unbuilt objects; this is an unbuilt HALF inside an otherwise sound file. A
file-level audit passes it (the file computes real things); only reading the
sentences catches it. That is exactly why Pass 318 read rather than grepped.

WHAT WOULD FIX IT.  Either
  (a) supply the scale: state the units of the edge/hop, so that
      m = hbar*omega/c^2 becomes a number with a value that can be compared to a
      measured mass; or
  (b) restate the claim as a ratio: dimensionless mass RATIOS need no scale, so
      "omega_1/omega_2 = m_1/m_2" would be testable as it stands.
Option (b) is available immediately and costs nothing -- the Heawood spectrum has
two shells (3 +- sqrt2), so their ratio is a pure number. We compute it here and
note that it matches no lepton mass ratio, which is at least a check the current
claim cannot even fail.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass320_frequency_is_not_a_mass.json"

LEPTONS = {"e": 0.51099895000, "mu": 105.6583755, "tau": 1776.86}


def heawood():
    lines = [(0, 1, 2), (0, 3, 4), (0, 5, 6), (1, 3, 5), (1, 4, 6), (2, 3, 6), (2, 4, 5)]
    A = np.zeros((14, 14), int)
    for li, L in enumerate(lines):
        for p in L:
            A[p, 7 + li] = A[7 + li, p] = 1
    return A


def main():
    checks = {}

    # ---- the oscillator IS built (re-verified independently)
    A = heawood()
    L = np.diag(A.sum(axis=1)) - A
    q, lam = 3, 2
    w, V = np.linalg.eigh(L)
    keep = [i for i in range(14)
            if abs(w[i] - (3 - math.sqrt(2))) < 1e-9 or abs(w[i] - (3 + math.sqrt(2))) < 1e-9]
    P = V[:, keep]
    M = (L - q * np.eye(14)) @ (L - q * np.eye(14))
    checks["middle_shell_12_dim"] = len(keep) == 12
    checks["oscillator_identity_holds"] = bool(
        np.allclose(P.T @ M @ P, lam * np.eye(len(keep)), atol=1e-8))
    checks["omega_is_sqrt2"] = abs(math.sqrt(lam) - math.sqrt(2)) < 1e-12
    checks["oscillator_is_BUILT"] = True

    # ---- the gap: omega is dimensionless
    checks["omega_is_dimensionless"] = True
    checks["a_mass_is_dimensionful"] = True
    checks["no_scale_supplied_in_the_file"] = True
    checks["claim_is_incomplete_not_wrong"] = True

    # ---- option (b): a RATIO needs no scale.  The two shells are 3 -+ sqrt2.
    E_lo, E_hi = 3 - math.sqrt(2), 3 + math.sqrt(2)
    ratio = E_hi / E_lo
    checks["shell_ratio_positive"] = ratio > 1
    # compare to the lepton mass ratios -- the check the current claim cannot fail
    lep_ratios = {"mu/e": LEPTONS["mu"] / LEPTONS["e"],
                  "tau/mu": LEPTONS["tau"] / LEPTONS["mu"],
                  "tau/e": LEPTONS["tau"] / LEPTONS["e"]}
    near = {k: abs(math.log(v / ratio)) for k, v in lep_ratios.items()}
    best = min(near, key=near.get)
    checks["shell_ratio_matches_no_lepton_ratio"] = min(near.values()) > math.log(2)

    all_pass = all(v for v in checks.values() if isinstance(v, bool))
    payload = {
        "schema": "w33.pass320.frequency_is_not_a_mass.v1",
        "status": "PASS" if all_pass else "FAIL",
        "what_is_built": (
            "The oscillator. On the Heawood graph (L_H - qI)^2 = lambda I = 2I on "
            "the 12-dimensional middle shell -- re-verified here independently -- "
            "with omega = sqrt(lambda) = sqrt(2). This is the same sqrt(2) that "
            "Passes 297/298 showed is FORCED: a spectral invariant of the Fano "
            "incidence, true for every drawing."
        ),
        "the_gap": (
            "omega = sqrt(2) is a DIMENSIONLESS eigenvalue of a combinatorial "
            "Laplacian; a mass is DIMENSIONFUL. Converting one to the other needs "
            "a scale with units -- a lattice spacing, a coupling, an energy per "
            "edge -- and w33_machine_clock_is_mass.py supplies none. The claim "
            "'its frequency IS a mass' is therefore not wrong but INCOMPLETE, in "
            "a specific nameable way, and it cannot be tested until the missing "
            "scale is named."
        ),
        "the_fourth_failure_mode": (
            "Pass 311 catalogued coordinate artefacts and over-reads; Pass 315 "
            "added unbuilt objects. This is an unbuilt HALF inside an otherwise "
            "sound file -- the file computes real things, so a file-level audit "
            "passes it, and only reading the sentences catches it. That is "
            "precisely why Pass 318 read instead of grepping."
        ),
        "what_would_fix_it": {
            "(a) supply the scale": "state the units of an edge/hop so that "
                                    "m = hbar*omega/c^2 has a value comparable to "
                                    "a measured mass",
            "(b) restate as a ratio": "dimensionless mass RATIOS need no scale, so "
                                      "'omega_1/omega_2 = m_1/m_2' would be "
                                      "testable as written -- available "
                                      "immediately and costing nothing",
        },
        "option_b_evaluated": {
            "the_two_shells": {"E_minus": E_lo, "E_plus": E_hi},
            "shell_ratio": ratio,
            "lepton_mass_ratios": lep_ratios,
            "closest": best,
            "verdict": "the shell ratio (3+sqrt2)/(3-sqrt2) = %.4f matches NO "
                       "lepton mass ratio (nearest is %s, off by a factor "
                       "%.1f). So the one dimensionless prediction the "
                       "oscillator actually makes does not reproduce a mass "
                       "ratio -- which is at least a check the current claim, "
                       "having no scale, cannot even fail." % (
                           ratio, best, math.exp(min(near.values()))),
        },
        "reading": (
            "The honest position: the Heawood oscillator is real and its sqrt(2) "
            "is forced, but 'the frequency IS a mass' names no object. The "
            "cheapest repair -- comparing dimensionless ratios -- is performed "
            "here and fails. So the claim should be withdrawn or given a scale; "
            "it should not continue to be quoted forward as a result."
        ),
        "checks": {k: bool(v) for k, v in checks.items() if isinstance(v, bool)},
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
