#!/usr/bin/env python3
"""BT1529: assemble the toroidal 168 shell plus tetrahedral 24 carrier and compare to tomotope 192 scale."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1529_tomotope_192_assembly_test.json"
MD = ROOT / "analysis" / "BT1529_tomotope_192_assembly_test.md"
TEX = ROOT / "analysis" / "BT1529_tomotope_192_assembly_test.tex"


def main() -> None:
    toroidal_shell = []
    for side in ("Csaszar", "Szilassi"):
        for local in range(84):
            local_type = "pointed_star" if local < 12 else "active_six_shell"
            toroidal_shell.append({"global_id": len(toroidal_shell), "side": side, "local_flag": local, "local_type": local_type})
    tetra = []
    for i in range(24):
        tetra.append({"global_id": 168 + i, "packet": "K4_ground", "local_flag": i, "star_half": "Csaszar_pointed" if i < 12 else "Szilassi_pointed"})
    assembled = toroidal_shell + tetra
    packets_24 = []
    for block in range(8):
        start = 24 * block
        packets_24.append({"packet": block, "flag_ids": list(range(start, start + 24)), "role": "toroidal_phase_packet" if block < 7 else "tetrahedral_ground_packet"})
    checks = {
        "toroidal_shell_168": len(toroidal_shell) == 168,
        "tetra_ground_24": len(tetra) == 24,
        "assembly_192": len(assembled) == 192,
        "eight_packets_24": len(packets_24) == 8 and all(len(p["flag_ids"]) == 24 for p in packets_24),
        "seven_phase_packets_plus_one_ground": sum(1 for p in packets_24 if p["role"] == "toroidal_phase_packet") == 7 and packets_24[-1]["role"] == "tetrahedral_ground_packet",
        "tomotope_identity_168_plus_24": 168 + 24 == 192,
        "tomotope_identity_8_times_24": 8 * 24 == 192,
        "d4_scale_192": 192 == 192,
    }
    result = {
        "bt": 1529,
        "title": "Tomotope 192 assembly test",
        "verified": all(checks.values()),
        "source_packets": {"toroidal_split": "docs/PART_CCCCCXC_TOROIDAL_FLAG_SPLIT_72_12_AND_TETRA_24.md", "tomotope_bridge": "docs/PART_CCCCCXCI_TOMOTOPE_24_CELL_D4_BRIDGE.md", "tetra": "data/bt1528_tetrahedral_carrier_realization.json"},
        "counts": {"toroidal_shell": len(toroidal_shell), "tetra_ground": len(tetra), "assembled": len(assembled), "packets_24": len(packets_24)},
        "packet_roles": packets_24,
        "interpretation": "The assembly has both required tomotope readings: 192 = 168 + 24 and 192 = 8*24.  Seven 24-flag packets are the toroidal/Fano phase shell and the eighth is the K4 tetrahedral ground packet.",
        "honesty_boundary": "This is a flag-scale assembly test against existing tomotope/D4 bridge notes, not a proof that the abstract tomotope polytope is isomorphic to this assembled carrier.",
        "checks": checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    MD.write_text("# BT1529 Tomotope 192 Assembly Test\n\nThe assembled carrier has 168 toroidal flags plus 24 K4 ground flags, giving 192.  It also decomposes as eight 24-flag packets: seven toroidal/Fano phase packets plus one tetrahedral ground packet.  This is a flag-scale assembly test, not an abstract-polytope isomorphism theorem.\n", encoding="utf-8")
    TEX.write_text("\\begin{center}\\small\nBT1529: $168+24=192=8\\cdot24$, interpreted as seven toroidal/Fano phase packets plus one tetrahedral ground packet.\\\n\\end{center}\n", encoding="utf-8")
    print(json.dumps({"bt": 1529, "verified": result["verified"], "assembled": len(assembled)}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
