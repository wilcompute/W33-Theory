#!/usr/bin/env python3
"""BT1437: audit gate for importing Moebius-ball electron claims into W33."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1437_mobius_ball_electron_claim_audit.json"


def main() -> None:
    claims = [
        {"claim": "13 half-turn double helix", "status": "paper_claim", "w33_anchor": "Phi_3=13 and Fano/Klein order motifs", "import_status": "numeric resonance only"},
        {"claim": "12 slings arranged toward icosahedron vertices", "status": "paper_claim", "w33_anchor": "k=12 and active star-mesh valence", "import_status": "geometry resonance only"},
        {"claim": "24 denominator / guard hint", "status": "paper_claim", "w33_anchor": "24 guard rail and S4 point stabilizer", "import_status": "strong audit target"},
        {"claim": "electron g-factor from chiral Moebius ball", "status": "paper_claim", "w33_anchor": "retwined frame covariance", "import_status": "not imported; requires quantitative derivation"},
        {"claim": "electron as self-confined helical photon compaction", "status": "paper_claim", "w33_anchor": "single-photon holonet carrier", "import_status": "not imported; requires spin/charge/mass tests"},
    ]
    required_tests = [
        "charge normalization without fitted constants",
        "spin-1/2 / double-cover mechanism",
        "magnetic moment and anomalous g-factor formula with uncertainty comparison",
        "Compton-radius scale derivation",
        "covariance law equivalent to e -> J e and H -> H J^{-1}",
        "mapping into 168 active + 24 guard W33 bus",
        "falsifiable distinction from standard QED rather than post-hoc numerology",
    ]
    checks = {
        "has_five_claims": len(claims) == 5,
        "has_seven_required_tests": len(required_tests) == 7,
        "keeps_gfactor_not_imported": claims[3]["import_status"].startswith("not imported"),
        "keeps_electron_not_imported": claims[4]["import_status"].startswith("not imported"),
        "has_168_24_mapping_test": any("168 active + 24 guard" in test for test in required_tests),
        "has_qed_falsifiability_test": any("standard QED" in test for test in required_tests),
    }
    result = {
        "bt": 1437,
        "title": "Moebius-ball electron claim audit gate",
        "verified": all(checks.values()),
        "paper": {
            "title": "Golden Quartic Polynomial and Moebius-Ball Electron",
            "author": "Hans Hermann Otto",
            "journal": "Journal of Applied Mathematics and Physics 10, 1785-1812 (2022)",
            "doi": "10.4236/jamp.2022.105124",
        },
        "claim_ledger": claims,
        "required_import_tests": required_tests,
        "decision": "Do not import the electron model as physics. Import only the finite covariance and integer-resonance audit targets until the required tests are met.",
        "checks": checks,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"bt": 1437, "verified": result["verified"], "claims": len(claims), "tests": len(required_tests)}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
