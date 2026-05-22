"""Part MCXCIV: Reye horizon symmetry-genus reciprocity lock.

Continuation of MCXCII-MCXCIII.

MCXCII gives the orientable K12 horizon packet:
  genus g = 6, code parity r = 6, payload k = 66, total n = 72.

MCXCIII gives common-spine symmetry packet:
  |Aut(Reye)| = 576,
  |Aut(Tomotope)| = 96.

New reciprocity lock:
  |Aut(Reye)|/|Aut(T)| = g = r = 6,
  n = k + g = 66 + 6 = 72,
  |Aut(Reye)| = g*|Aut(T)| = r*|Aut(T)|.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _load(path: Path) -> dict[str, object]:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def reye_horizon_symmetry_genus_reciprocity_packet() -> dict[str, object]:
    mcxcii = _load(ROOT / "PART_MCXCII_REYE_K12_ORIENTABLE_HORIZON_COMPLETION_results.json")
    mcxciii = _load(ROOT / "PART_MCXCIII_REYE_TOMOTOPE_24CELL_COMMON_SPINE_results.json")

    genus = int(mcxcii["surface"]["genus"])                              # 6
    payload = int(mcxcii["horizon_code"]["payload"])                     # 66
    parity = int(mcxcii["horizon_code"]["parity"])                       # 6
    total = int(mcxcii["horizon_code"]["total"])                         # 72
    k12_edges = int(mcxcii["surface"]["E"])                              # 66

    aut_reye = int(mcxciii["symmetry_lock"]["reye_automorphism_order"])  # 576
    aut_tomotope = int(mcxciii["tomotope_match"]["tomotope_automorphism_order"])  # 96

    ratio = aut_reye // aut_tomotope

    checks = {
        "mcxcii_genus_is_6": genus == 6,
        "mcxcii_parity_is_6": parity == 6,
        "mcxcii_code_splits_as_66_plus_6": total == payload + parity == 72,
        "mcxcii_payload_is_k12_edges": payload == k12_edges == 66,
        "mcxciii_symmetry_is_576_over_96": aut_reye == 576 and aut_tomotope == 96,
        "symmetry_ratio_is_6": ratio == 6,
        "symmetry_ratio_equals_genus": ratio == genus,
        "symmetry_ratio_equals_parity": ratio == parity,
        "reye_symmetry_equals_genus_times_tomotope_symmetry": aut_reye == genus * aut_tomotope,
        "reye_symmetry_equals_parity_times_tomotope_symmetry": aut_reye == parity * aut_tomotope,
        "total_code_equals_payload_plus_symmetry_ratio": total == payload + ratio,
    }

    return {
        "part": "MCXCIV",
        "theorem": "Reye horizon symmetry-genus reciprocity lock",
        "horizon_packet": {
            "genus": genus,
            "payload": payload,
            "parity": parity,
            "total": total,
            "identity": "72 = 66 + 6 with genus=6",
        },
        "symmetry_packet": {
            "aut_reye": aut_reye,
            "aut_tomotope": aut_tomotope,
            "ratio": ratio,
            "identity": "576/96 = 6",
        },
        "reciprocity_lock": {
            "identity": "|Aut(Reye)|/|Aut(T)| = genus = parity = 6 and 72 = 66 + 6",
        },
        "finite_universality_surrogate": {
            "statement": "horizon redundancy equals both topological genus and symmetry lift ratio of the shared Reye spine",
            "boundary": "finite incidence/topology/symmetry reciprocity; not a continuum dynamics theorem",
        },
        "claim_boundary": "finite symmetry-genus-code reciprocity law on MCXCII-MCXCIII packets",
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def main() -> None:
    packet = reye_horizon_symmetry_genus_reciprocity_packet()
    out_path = ROOT / "PART_MCXCIV_REYE_HORIZON_SYMMETRY_GENUS_RECIPROCITY_results.json"
    with open(out_path, "w", encoding="utf-8") as handle:
        json.dump(packet, handle, indent=2)

    print("=== Part MCXCIV: Reye Horizon Symmetry-Genus Reciprocity Lock ===")
    print(packet["horizon_packet"]["identity"])
    print(packet["symmetry_packet"]["identity"])
    print(packet["reciprocity_lock"]["identity"])
    print(f"verified: {packet['n_verified']} / {len(packet['checks'])}")


if __name__ == "__main__":
    main()
