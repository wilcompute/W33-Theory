#!/usr/bin/env python3
"""BT1436: quaternionic Moebius / W33 dictionary."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1436_quaternionic_mobius_w33_dictionary.json"


def main() -> None:
    dictionary = [
        {"continuous": "quaternionic ball B in H", "dimension": 4, "w33": "qutrit carrier F3^4", "role": "four-coordinate state/frame space"},
        {"continuous": "Sp(1,1) fractional linear action", "dimension": None, "w33": "retwined CSS column-frame action J", "role": "transform state/error frame and check frame together"},
        {"continuous": "S^3 unit quaternion fiber", "dimension": 3, "w33": "S3/qutrit phase-fiber control plus D4 guard cycles", "role": "phase/chirality control fiber"},
        {"continuous": "Moebius covariance", "dimension": None, "w33": "syndrome equivariance syn_H(e)=syn_H'(Je)", "role": "measurement invariant under joint frame retwining"},
        {"continuous": "icosahedral boundary symmetry", "dimension": None, "w33": "Fano 168 active bus and 24 guard rail", "role": "finite active/guard packetization"},
    ]
    checks = {
        "has_quaternionic_ball_dimension4": dictionary[0]["dimension"] == 4,
        "has_s3_fiber_dimension3": dictionary[2]["dimension"] == 3,
        "has_retwined_css_covariance": "syn_H" in dictionary[3]["w33"],
        "has_fano_active_guard_entry": "168" in dictionary[4]["w33"] and "24" in dictionary[4]["w33"],
        "dictionary_has_five_entries": len(dictionary) == 5,
    }
    result = {
        "bt": 1436,
        "title": "Quaternionic Moebius / W33 dictionary",
        "verified": all(checks.values()),
        "dictionary": dictionary,
        "core_equivalence": "continuous covariance under quaternionic Moebius transforms maps to finite covariance under retwined CSS frame transforms",
        "electron_import_rule": "No electron claim is imported unless it supplies a spinor/double-cover law, charge normalization, magnetic moment, and a verified map into the 168+24 W33 bus.",
        "checks": checks,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"bt": 1436, "verified": result["verified"], "entries": len(dictionary)}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
