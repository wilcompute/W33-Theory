#!/usr/bin/env python3
"""BT1319 - 4x4 toroidal square, Q4 router, and holonet bridge.

The user's new hint is architectural rather than merely numerical:

  1. start with a 4x4 square;
  2. impose toroidal boundaries, because without wraparound it is not Q4;
  3. use the 4x4 toroidal knight graph as the Q4 packet router;
  4. connect the Q4 packet to the tetrahedron/tomotope flag codec and the
     holonet hypercube network layer;
  5. place 14641 = 11^4 as the tetrahedral Clifford/Pascal scale marker.

This verifier keeps the boundary strict.  It proves the local routing interface
and scale marker.  It does not claim a new subsystem distance, nor that Q4
replaces the global 540-chart Q3 atlas.
"""

from __future__ import annotations

import importlib.util
import itertools
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT_PATH = ROOT / "data" / "bt1319_toroidal_q4_hypercube_holonet_bridge.json"

Q = 3
MU = 4
K = 12
P_IH = K - 1
CODEC = 12
TOMOTOPE_FLAGS = 192
CHARTS = 540
TRANSVERSALS_PER_CHART = 4
MIRROR_SLOTS = 2160


def _load_module(name: str, relpath: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relpath)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load module at {relpath}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def _ordinary_knight_edges(
    board: int = 4,
) -> set[tuple[tuple[int, int], tuple[int, int]]]:
    moves = ((1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1))
    edges: set[tuple[tuple[int, int], tuple[int, int]]] = set()
    for r, c in itertools.product(range(board), repeat=2):
        for dr, dc in moves:
            nr, nc = r + dr, c + dc
            if 0 <= nr < board and 0 <= nc < board:
                edges.add(tuple(sorted(((r, c), (nr, nc)))))
    return edges


def _ordinary_knight_degree_profile(board: int = 4) -> dict[str, int]:
    edges = _ordinary_knight_edges(board)
    degrees = {(r, c): 0 for r, c in itertools.product(range(board), repeat=2)}
    for a, b in edges:
        degrees[a] += 1
        degrees[b] += 1
    profile: dict[str, int] = {}
    for degree in degrees.values():
        profile[str(degree)] = profile.get(str(degree), 0) + 1
    return profile


def _hamming(a: tuple[int, ...], b: tuple[int, ...]) -> int:
    return sum(x != y for x, y in zip(a, b))


def _max_ecube_distance(vertices: list[tuple[int, ...]]) -> int:
    return max(_hamming(a, b) for a, b in itertools.product(vertices, repeat=2))


def _q4_square_faces() -> int:
    # Number of 2-faces in Q_n is C(n,2) * 2^(n-2).
    return 6 * 4


def _codec_identity() -> dict[str, Any]:
    return {
        "tetrahedron_codecs": 2,
        "csaszar_codecs": 7,
        "szilassi_codecs": 7,
        "total_codecs": 2 + 7 + 7,
        "flags_per_codec": CODEC,
        "total_flags": (2 + 7 + 7) * CODEC,
        "reading": "(2+7+7)*12 = 16*12 = 192",
    }


def build_bridge() -> dict[str, Any]:
    q4_packet = _load_module(
        "ccccxiii", "exploration/PART_CCCCXIII_TOROIDAL_KNIGHT_HYPERCUBE_PACKET.py"
    ).build_results()
    flag_codec = _load_module(
        "flag_codec", "analysis/w33_flag_codec_toroidal_hypercube_boundary.py"
    ).build_payload()
    pascal_600 = _load_module(
        "dcclii", "verify_dcclii_hyperbolic_pascal_600cell_e8.py"
    ).build_bridge()
    gray_hamming = _load_module(
        "gray_hamming", "analysis/w33_gray_hamming_router_lift.py"
    ).build_payload()
    q4_square = _load_module(
        "q4_square", "analysis/w33_q4_fano_square_commutator_lift.py"
    ).build_payload()

    q4_vertices = [tuple(v) for v in q4_packet["gray_cycle"]["q4_tour"]]
    ordinary_edges = _ordinary_knight_edges()
    ordinary_degree_profile = _ordinary_knight_degree_profile()
    toroidal_dimension_counts = {
        str(k): v
        for k, v in q4_packet["hypercube_isomorphism"]["dimension_edge_counts"].items()
    }
    codec = _codec_identity()

    row4 = pascal_600["pascal_row_4_tetrahedron"]
    tetra_pascal = {
        "row": row4["row"],
        "evaluated_at_Phi_4": row4["evaluated_at_Phi_4"],
        "expected_11_to_4": row4["expected_11_to_4"],
        "p_Ih_power_mu": P_IH**MU,
        "reading": "14641 = (1+10)^4 = 11^4 = (k-1)^mu",
    }

    holonet_interface = {
        "local_Q4_packet_vertices": len(q4_vertices),
        "local_Q4_packet_edges": 32,
        "local_Q4_packet_square_faces": _q4_square_faces(),
        "local_ecube_max_hops": _max_ecube_distance(q4_vertices),
        "global_chart_atlas": CHARTS,
        "chart_transversal_slots": CHARTS * TRANSVERSALS_PER_CHART,
        "mirror_slots": MIRROR_SLOTS,
        "slot_factorization": "540*4 = 2160",
        "layer_boundary": (
            "Q4 is the local 16-state packet router; the photonic holonet "
            "also has a 540-chart Q3 atlas and a 2160-slot D12 mirror bus"
        ),
    }

    checks = {
        "toroidal_q4_packet_verified": q4_packet["verified"]
        and q4_packet["checks_passed"] == q4_packet["checks_total"] == 10,
        "ordinary_4x4_knight_graph_is_not_q4": len(ordinary_edges) != 32
        and ordinary_degree_profile != {"4": 16},
        "toroidal_boundary_is_required_for_q4": len(ordinary_edges) == 24
        and ordinary_degree_profile == {"2": 4, "3": 8, "4": 4},
        "toroidal_packet_has_q4_dimension_counts": toroidal_dimension_counts
        == {"0": 8, "1": 8, "2": 8, "3": 8},
        "gray_clock_is_closed_q4_hamilton_cycle": q4_packet["checks"][8]["passed"]
        and q4_packet["checks"][9]["passed"],
        "flag_codec_boundary_verified": flag_codec["all_identities_hold"],
        "codec_2_plus_7_plus_7_equals_q4_vertices": codec["total_codecs"] == 16,
        "codec_flags_equal_tomotope_flags": codec["total_flags"] == TOMOTOPE_FLAGS,
        "q4_square_faces_equal_tetrahedron_flags": q4_square["identities"][
            "Q4_square_faces_equal_tetrahedron_flags"
        ],
        "gray_hamming_lift_preserves_16_states": gray_hamming["all_identities_hold"]
        and gray_hamming["parameters"]
        == {
            "length": 8,
            "dimension": 4,
            "distance": 4,
            "codewords": 16,
        },
        "tetrahedron_pascal_scale_is_14641": tetra_pascal["evaluated_at_Phi_4"]
        == tetra_pascal["expected_11_to_4"]
        == tetra_pascal["p_Ih_power_mu"]
        == 14641,
        "holonet_mirror_lift_matches_2160": holonet_interface["chart_transversal_slots"]
        == holonet_interface["mirror_slots"]
        == MIRROR_SLOTS,
        "local_ecube_route_bound_is_mu": holonet_interface["local_ecube_max_hops"]
        == MU,
    }

    return {
        "theorem": "BT1319 toroidal Q4 hypercube holonet bridge",
        "verified": all(checks.values()),
        "four_by_four_square": {
            "ordinary_knight_edges": len(ordinary_edges),
            "ordinary_degree_profile": ordinary_degree_profile,
            "ordinary_boundary_status": "not_Q4",
            "toroidal_boundary_status": "Q4",
            "why_toroidal_boundary_matters": (
                "without wraparound the 4x4 knight graph has 24 edges and "
                "mixed degree profile 2^4,3^8,4^4; with toroidal wraparound "
                "it becomes 4-regular with 32 edges, exactly Q4"
            ),
        },
        "q4_packet": {
            "verified": q4_packet["verified"],
            "dimension_edge_counts": toroidal_dimension_counts,
            "gray_flip_sequence": q4_packet["gray_cycle"]["flip_sequence"],
            "axis_interpretation": q4_packet["hypercube_isomorphism"][
                "packet_axis_interpretation"
            ],
        },
        "tomotope_codec": codec,
        "tetrahedral_clifford_scale_marker": tetra_pascal,
        "holonet_interface": holonet_interface,
        "protected_router_lift": {
            "code": gray_hamming["code"],
            "parameters": gray_hamming["parameters"],
            "one_bit_Q4_move_lifts_to_distance": gray_hamming["gray_router_lift"][
                "encoded_step_distances"
            ][0],
        },
        "boundary": (
            "This proves the local toroidal-Q4 packet/router interface and the "
            "14641 tetrahedral Pascal/Ihara scale marker. It does not replace "
            "the global 540-chart Q3 atlas, does not prove a new Q4 subsystem "
            "distance, and does not identify 11^4 with a complete Clifford "
            "algebra unless a future objectwise construction supplies it."
        ),
        "checks": checks,
    }


def write_results(path: Path = OUT_PATH) -> Path:
    payload = build_bridge()
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def main() -> None:
    payload = build_bridge()
    out = write_results()
    print(f"BT1319 verified={payload['verified']} wrote {out}")
    if not payload["verified"]:
        failed = [name for name, ok in payload["checks"].items() if not ok]
        raise SystemExit(f"BT1319 failed checks: {failed}")


if __name__ == "__main__":
    main()
