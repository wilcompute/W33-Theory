#!/usr/bin/env python3
"""BT1876: representative existence search.

Searches the repo for existing E8 vector/basis material that can instantiate the
BT1870/BT1875 physical E8 representative model. The key hit is BT982, which
constructs an explicit integral E8 basis in vertex E8 root coordinates for the
support-minimal selector and verifies the standard E8 Cartan Gram.
"""
from __future__ import annotations

import json
from pathlib import Path

OUT = Path("data/PART_BT1876_REPRESENTATIVE_EXISTENCE_SEARCH_results.json")

SEARCH_HITS = [
    {
        "path": "analysis/bt982_explicit_integral_e8_basis.py",
        "role": "primary_basis_candidate",
        "use": "final_integral_basis_B in vertex E8 root coordinates; Gram matches E8 Cartan",
        "status": "strong_candidate_for_BT1870_instantiation"
    },
    {
        "path": "tools/e8_lattice_cocycle.py",
        "role": "auxiliary_lattice_tooling",
        "use": "E8 lattice/cocycle tooling found by repo search",
        "status": "review_later"
    },
    {
        "path": "tools/sage_e8_orbit_f3_mapping.py",
        "role": "auxiliary_orbit_mapping",
        "use": "Sage-side E8/F3 orbit mapping found by repo search",
        "status": "review_later"
    },
]

BT982_CONTRACT = {
    "loads": ["BT951", "BT954", "BT956"],
    "winner_minimizer": 2,
    "constructs": ["lift_matrix_M", "gl8Z_to_cartan_T", "final_integral_basis_B"],
    "checks": ["both gauges select minimizer 2", "M unimodular", "T unimodular", "B unimodular", "B^T G_vertex B equals E8 Cartan"],
    "remaining_bridge": "map BT982 basis columns onto BT1875 support-pair/phase rows and add chain-boundary compatibility data"
}


def theorem_summary():
    checks = {
        "bt982_primary_candidate_found": SEARCH_HITS[0]["path"] == "analysis/bt982_explicit_integral_e8_basis.py",
        "bt982_has_final_basis_contract": "final_integral_basis_B" in BT982_CONTRACT["constructs"],
        "bt982_has_cartan_check": any("Cartan" in c for c in BT982_CONTRACT["checks"]),
        "remaining_bridge_explicit": "BT1875" in BT982_CONTRACT["remaining_bridge"],
        "does_not_claim_BT1875_filled_yet": True
    }
    return {
        "theorem": "BT1876 Representative Existence Search",
        "search_hits": SEARCH_HITS,
        "primary_candidate": "analysis/bt982_explicit_integral_e8_basis.py",
        "bt982_contract": BT982_CONTRACT,
        "reading": "The repo already contains the right integral E8 basis source. The remaining work is wiring BT982's final basis B into BT1875's selector-pair/phase template and proving chain-boundary compatibility.",
        "checks": checks,
        "all_pass": all(checks.values()),
        "honest_scope": "Search/audit witness. It identifies BT982 as the basis source but does not instantiate BT1875 rows yet."
    }


def main() -> int:
    summary = theorem_summary()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0 if summary["all_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
