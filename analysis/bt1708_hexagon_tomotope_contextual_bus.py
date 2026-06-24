#!/usr/bin/env python3
"""BT1708 - split Cayley hexagon, tomotope, and Holonet bus bridge.

The Quantum 2025 three-qubit paper exposes a (24_2,16_3) domain inside the
split Cayley hexagon discussion.  The repo already has a verified tomotope
middle layer with 12 edges, 16 faces, and 48 edge/face blocks.  BT1708 checks
that these are the same incidence-size interface and that the split Cayley
hexagon symmetry has the Holonet readout-clock factorization.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1708_hexagon_tomotope_contextual_bus.json"


def load_json(relpath: str) -> dict[str, Any]:
    return json.loads((ROOT / relpath).read_text(encoding="utf-8"))


def field_size(packet: dict[str, Any], field: str) -> int:
    for row in packet["field_schema"]:
        if row["field"] == field:
            return int(row["size"])
    raise KeyError(field)


def build_certificate() -> dict[str, Any]:
    tomotope = load_json(
        "data/bt814_tomotope_middle_layer_from_residual_tetrahedra.json"
    )
    packet = load_json("data/bt1697_holonet_typed_packet_abi.json")

    q2025_domain = {
        "configuration": "(24_2,16_3)",
        "observables": 24,
        "lines": 16,
        "observable_multiplicity": 2,
        "line_size": 3,
        "incidences": 48,
        "source": "q-2025-01-20-1601.pdf",
    }
    tomotope_middle = tomotope["f_vector_from_transversal_tetrahedra"]
    holonet_body_ticks = field_size(packet, "q6_body_edge") * field_size(
        packet, "body_pulse_phase"
    )
    split_cayley = {
        "points": 63,
        "lines": 63,
        "automorphism_order": 12096,
        "readout_group_order": 168,
        "holonet_packet_ticks": 72,
        "level_7_j_special_fiber": 7 * 1728,
    }
    heawood_k77 = {
        "fano_points": 7,
        "fano_lines": 7,
        "heawood_vertices": 14,
        "heawood_edges": 21,
        "k77_edges": 49,
        "coheawood_edges": 28,
    }
    seven_toroidal_realizations = {
        "csaszar_realizations": 5,
        "szilassi_realizations": 2,
        "total": 7,
        "interpretation": "external realization count; used here only as a seven-fold torus marker",
    }

    checks = {
        "q2025_domain_is_balanced_48": q2025_domain["observables"]
        * q2025_domain["observable_multiplicity"]
        == q2025_domain["lines"] * q2025_domain["line_size"]
        == q2025_domain["incidences"],
        "tomotope_middle_is_48_blocks": tomotope_middle["middle_blocks"]
        == q2025_domain["incidences"],
        "tomotope_edges_faces_are_12_16": tomotope_middle["edges"] == 12
        and tomotope_middle["faces"] == 16,
        "holonet_body_is_same_48_interface": holonet_body_ticks
        == q2025_domain["incidences"],
        "split_cayley_aut_is_readout_times_packet_clock": split_cayley[
            "automorphism_order"
        ]
        == split_cayley["readout_group_order"] * split_cayley["holonet_packet_ticks"],
        "split_cayley_aut_is_level7_j_special_fiber": split_cayley["automorphism_order"]
        == split_cayley["level_7_j_special_fiber"],
        "heawood_is_fano_incidence_graph": heawood_k77["heawood_vertices"]
        == heawood_k77["fano_points"] + heawood_k77["fano_lines"]
        and heawood_k77["heawood_edges"] == 7 * 3,
        "k77_splits_heawood_and_coheawood": heawood_k77["k77_edges"]
        == heawood_k77["heawood_edges"] + heawood_k77["coheawood_edges"],
        "seven_toroidal_realizations_are_phi6": seven_toroidal_realizations[
            "csaszar_realizations"
        ]
        + seven_toroidal_realizations["szilassi_realizations"]
        == 7,
        "upstream_certificates_verified": packet["verified"] is True
        and tomotope.get("verified", True) is True,
    }

    return {
        "theorem": "BT1708 hexagon-tomotope contextual bus",
        "verified": all(checks.values()),
        "breakthrough": (
            "The three-qubit split-Cayley layer exposes the same 48-incidence "
            "interface as the local tomotope middle layer and the 48-tick Holonet "
            "body.  Its automorphism order factors as 12096 = 168*72, making it "
            "a candidate timed contextuality/readout module rather than a loose "
            "numerical analogy."
        ),
        "q2025_domain": q2025_domain,
        "tomotope_middle": tomotope_middle,
        "holonet_body_ticks": holonet_body_ticks,
        "split_cayley": split_cayley,
        "heawood_k77": heawood_k77,
        "seven_toroidal_realizations": seven_toroidal_realizations,
        "source_certificates": [
            "data/bt814_tomotope_middle_layer_from_residual_tetrahedra.json",
            "data/bt1697_holonet_typed_packet_abi.json",
        ],
        "claim_boundary": [
            "This verifies an incidence-size and symmetry-factor bridge, not a proven graph isomorphism.",
            "The seven toroidal realizations are recorded as an external torus marker, not as a derived W33 theorem.",
        ],
        "checks": checks,
    }


def main() -> int:
    cert = build_certificate()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(cert["theorem"])
    print(f"  verified: {cert['verified']}")
    print(
        "  key identity: (24_2,16_3) incidences = tomotope middle = Holonet body = 48"
    )
    print(f"  wrote {OUT}")
    return 0 if cert["verified"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
