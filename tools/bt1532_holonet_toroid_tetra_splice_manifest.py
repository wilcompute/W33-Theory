#!/usr/bin/env python3
"""BT1532: release/splice manifest for the exact toroidal/tetra/tomotope packet BT1513--BT1529."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1532_holonet_toroid_tetra_splice_manifest.json"
MD = ROOT / "analysis" / "BT1532_holonet_toroid_tetra_splice_manifest.md"
TEX = ROOT / "analysis" / "BT1532_holonet_toroid_tetra_splice_manifest.tex"

PACKET = [
    "analysis/BT1513_toroidal_7_21_3_bridge.md",
    "analysis/BT1514_BT1516_toroid_cocycle_fixture.md",
    "analysis/BT1517_BT1519_szilassi_cocycle_fixture.md",
    "analysis/BT1520_BT1522_szilassi_sector_transport.md",
    "analysis/BT1523_BT1526_toroid_transport_tetra.md",
    "analysis/BT1527_BT1529_dual_tetra_tomotope.md",
    "analysis/BT1530_tetrahedral_orientation_sign_refinement.md",
    "analysis/BT1531_eight_packet_d4_action_model.md",
]

DATA = [
    "data/bt1513_toroidal_7_21_3_bridge.json",
    "data/bt1520_full_szilassi_face_list_importer.json",
    "data/bt1521_fixed_hexagon_sector_fiber_test.json",
    "data/bt1526_csaszar_all_five_tetra_audit.json",
    "data/bt1527_dual_incidence_isomorphism.json",
    "data/bt1528_tetrahedral_carrier_realization.json",
    "data/bt1529_tomotope_192_assembly_test.json",
    "data/bt1530_tetrahedral_orientation_sign_refinement.json",
    "data/bt1531_eight_packet_d4_action_model.json",
]

SPLICE_ORDER = [
    {"order": 1, "insert": "analysis/BT1510_BT1513_holonet_insert.tex", "tier": "count resonance plus toroidal bridge target"},
    {"order": 2, "insert": "analysis/BT1514_BT1516_holonet_insert.tex", "tier": "incidence-compatible bridge plus cocycle and fixture validation"},
    {"order": 3, "insert": "analysis/BT1517_BT1519_holonet_insert.tex", "tier": "concrete fixed Szilassi anchor plus fixture materializer"},
    {"order": 4, "insert": "analysis/BT1520_BT1522_holonet_insert.tex", "tier": "full Szilassi importer plus transported-gauge prototype"},
    {"order": 5, "insert": "analysis/BT1523_BT1526_holonet_insert.tex", "tier": "Szilassi incidence, Csaszar all-five, tetra bridge"},
    {"order": 6, "insert": "analysis/BT1527_BT1529_holonet_insert.tex", "tier": "dual incidence, K4 carrier, tomotope 192 assembly"},
]

BLOCKED = [
    "unique label-preserving Szilassi-to-BT1504 embedding",
    "metric equivalence of Csaszar/Szilassi realizations with K4",
    "abstract tomotope polytope isomorphism",
    "regular D4 action fixes tetrahedral ground packet",
]


def main() -> None:
    existing_packet = [p for p in PACKET if (ROOT / p).exists()]
    existing_data = [p for p in DATA if (ROOT / p).exists()]
    json_verified = []
    for p in existing_data:
        try:
            json_verified.append(json.loads((ROOT / p).read_text(encoding="utf-8")).get("verified") is True)
        except Exception:
            json_verified.append(False)
    checks = {
        "all_packet_notes_exist": len(existing_packet) == len(PACKET),
        "all_data_exist": len(existing_data) == len(DATA),
        "all_json_verified": len(json_verified) == len(DATA) and all(json_verified),
        "six_splice_steps": [r["order"] for r in SPLICE_ORDER] == [1, 2, 3, 4, 5, 6],
        "blocked_claims_four": len(BLOCKED) == 4,
        "tomotope_packet_included": any("1527_BT1529" in r["insert"] for r in SPLICE_ORDER),
    }
    result = {
        "bt": 1532,
        "title": "Holonet toroid/tetra/tomotope splice manifest",
        "verified": all(checks.values()),
        "packet": PACKET,
        "data": DATA,
        "splice_order": SPLICE_ORDER,
        "blocked_claims": BLOCKED,
        "interpretation": "BT1513--BT1531 are ready as the preferred exact toroidal/tetra/tomotope packet for the next Holonet splice, with blocked theorem boundaries explicit.",
        "honesty_boundary": "This manifest does not rewrite photonic_holonet.tex or rebuild the PDF; it records the release splice packet and claim firewall.",
        "checks": checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    md = ["# BT1532 Holonet Toroid/Tetra/Tomotope Splice Manifest", "", "Preferred exact packet before the next PDF rebuild:", ""]
    for row in SPLICE_ORDER:
        md.append(f"{row['order']}. `{row['insert']}` — {row['tier']}.")
    md.extend(["", "Blocked claims:", ""])
    for b in BLOCKED:
        md.append(f"- {b}")
    MD.write_text("\n".join(md) + "\n", encoding="utf-8")
    TEX.write_text("\\begin{center}\\small\nBT1532: BT1513--BT1531 form the preferred toroidal/tetra/tomotope splice packet; full embedding, metric equivalence, and abstract tomotope isomorphism remain blocked.\\\n\\end{center}\n", encoding="utf-8")
    print(json.dumps({"bt": 1532, "verified": result["verified"], "splices": len(SPLICE_ORDER)}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
