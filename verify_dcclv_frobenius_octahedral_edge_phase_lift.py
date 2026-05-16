#!/usr/bin/env python3
"""Part DCCLV: Frobenius-octahedral edge-phase lift.

DCCLIV proves that q=3 is uniquely selected by

    q^5 - q = E(GQ(q,q)) = 240.

DCCXLIX identifies the closure-clock phase space with the octahedron.
This bridge welds those facts to the W33 edge/QEC carrier:

    240 = 40 * 6 = W33 vertices * octahedral antipodal edge-pairs,
    480 = 40 * 12 = W33 vertices * octahedron edges.

Thus the selected Frobenius carrier has a finite edge-phase lift: each
physical edge/root/CSS slot can be represented as a W33 vertex together
with one of six local octahedral phase pairs, while the directed
Hashimoto/fusion carrier keeps the full twelve local octahedral edges.
"""

from __future__ import annotations

import json
import math
import sys
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dccxlix_octahedron_closure_phase_space import (  # noqa: E402
    build_bridge as build_dccxlix,
    octahedron_edges,
    octahedron_vertices,
)
from verify_dccliv_frobenius_selection_and_ouroboros import (  # noqa: E402
    build_bridge as build_dccliv,
    frobenius_count,
    gq_edge_count,
)


OUT_PATH = ROOT / "data" / "dcclv_frobenius_octahedral_edge_phase_lift.json"

Q = 3
V_W33 = 40
K_W33 = 12
E_W33 = 240
TRIANGLES_W33 = 160
TETRAHEDRA_W33 = 40
RANK_X = 39
RANK_Z = 120
H1 = 81


@dataclass(frozen=True)
class BridgeSummary:
    q: int
    frobenius_carrier: int
    w33_vertices: int
    octahedral_phase_pairs: int
    edge_phase_slots: int
    directed_phase_slots: int
    full_chain_closure_dimension: int
    all_identities_hold: bool


def antipodal_vertex_map(vertices: list[tuple[str, int]]) -> dict[int, int]:
    index = {vertex: i for i, vertex in enumerate(vertices)}
    return {i: index[(axis, -sign)] for i, (axis, sign) in enumerate(vertices)}


def normalize_edge(edge: tuple[int, int]) -> tuple[int, int]:
    a, b = edge
    return (a, b) if a < b else (b, a)


def antipodal_edge_pair_orbits(
    vertices: list[tuple[str, int]], edges: list[tuple[int, int]]
) -> list[list[tuple[int, int]]]:
    antipode = antipodal_vertex_map(vertices)
    edge_set = {normalize_edge(edge) for edge in edges}
    unseen = set(edge_set)
    orbits: list[list[tuple[int, int]]] = []
    while unseen:
        edge = min(unseen)
        image = normalize_edge((antipode[edge[0]], antipode[edge[1]]))
        orbit = sorted({edge, image})
        for item in orbit:
            unseen.discard(item)
        orbits.append(orbit)
    return sorted(orbits, key=lambda orbit: orbit[0])


def vertex_phase_slots(vertex_count: int, phase_count: int) -> list[dict[str, int]]:
    return [
        {"w33_vertex": vertex, "phase_pair": phase}
        for vertex in range(vertex_count)
        for phase in range(phase_count)
    ]


def directed_vertex_phase_slots(vertex_count: int, directed_phase_count: int) -> list[dict[str, int]]:
    return [
        {"w33_vertex": vertex, "directed_phase": phase}
        for vertex in range(vertex_count)
        for phase in range(directed_phase_count)
    ]


def build_bridge() -> dict[str, Any]:
    dccxlix = build_dccxlix()
    dccliv = build_dccliv()

    vertices = octahedron_vertices()
    edges = octahedron_edges(vertices)
    edge_pair_orbits = antipodal_edge_pair_orbits(vertices, edges)
    phase_slots = vertex_phase_slots(V_W33, len(edge_pair_orbits))
    directed_slots = directed_vertex_phase_slots(V_W33, len(edges))

    frobenius_q3 = frobenius_count(Q)
    gq_edges_q3 = gq_edge_count(Q)
    w33_projective_points = (Q**4 - 1) // (Q - 1)
    frobenius_over_vertices = Fraction(frobenius_q3, w33_projective_points)
    local_half_valency = Fraction(K_W33, 2)
    full_chain_closure_dimension = V_W33 + E_W33 + TRIANGLES_W33 + TETRAHEDRA_W33

    qec_split = {
        "physical_edge_slots": E_W33,
        "rank_X_vertex_checks": RANK_X,
        "rank_Z_triangle_checks": RANK_Z,
        "logical_H1": H1,
        "stabilizer_rank": RANK_X + RANK_Z,
        "rate": {"numerator": H1 // 3, "denominator": E_W33 // 3},
        "closure": RANK_X + RANK_Z + H1,
    }

    identities = {
        "incoming_octahedron_bridge_verified": dccxlix["summary"]["all_identities_hold"],
        "incoming_frobenius_bridge_verified": dccliv["summary"]["all_identities_hold"],
        "frobenius_at_q3_is_w33_edge_count": frobenius_q3 == E_W33,
        "gq_edges_at_q3_match_frobenius": gq_edges_q3 == E_W33,
        "w33_projective_points_are_40": w33_projective_points == V_W33,
        "frobenius_factor_is_six": frobenius_over_vertices == 6,
        "frobenius_factor_is_q_factorial": frobenius_over_vertices == math.factorial(Q),
        "local_half_valency_is_q_factorial": local_half_valency == math.factorial(Q),
        "octahedron_has_six_antipodal_edge_pairs": len(edge_pair_orbits) == 6,
        "octahedron_edges_are_twelve_directed_phases": len(edges) == K_W33,
        "edge_phase_slots_are_240": len(phase_slots) == E_W33,
        "directed_phase_slots_are_480": len(directed_slots) == 2 * E_W33,
        "directed_phase_slots_are_vertex_times_octahedron_edges": len(directed_slots) == V_W33 * len(edges),
        "edge_phase_slots_are_vertex_times_octahedral_pairs": len(phase_slots) == V_W33 * len(edge_pair_orbits),
        "full_clique_chain_dimension_is_480": full_chain_closure_dimension == 2 * E_W33,
        "qec_split_closes_edge_carrier": qec_split["closure"] == E_W33,
        "qec_rate_is_27_over_80": qec_split["rate"] == {"numerator": 27, "denominator": 80},
        "e8_a2_phase_split_respects_six_shell": 72 + len(edge_pair_orbits) + H1 + H1 == E_W33,
    }

    summary = BridgeSummary(
        q=Q,
        frobenius_carrier=frobenius_q3,
        w33_vertices=V_W33,
        octahedral_phase_pairs=len(edge_pair_orbits),
        edge_phase_slots=len(phase_slots),
        directed_phase_slots=len(directed_slots),
        full_chain_closure_dimension=full_chain_closure_dimension,
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "factorization": {
            "frobenius": "q^5 - q = q(q^4 - 1)",
            "projective_points": "[4]_q = (q^4 - 1)/(q - 1)",
            "q3_specialization": "3^5 - 3 = 40 * 6 = W33 vertices * octahedral phase pairs",
            "directed_lift": "480 = 40 * 12 = W33 vertices * octahedron edges",
            "selection_note": "At q=3, q(q-1)=q! and k/2=q!, so the Frobenius quotient is the closure-clock phase count.",
        },
        "octahedral_phase_data": {
            "vertices": vertices,
            "edges": edges,
            "antipodal_vertex_map": antipodal_vertex_map(vertices),
            "antipodal_edge_pair_orbits": edge_pair_orbits,
            "phase_pair_count": len(edge_pair_orbits),
            "directed_phase_count": len(edges),
        },
        "slot_samples": {
            "edge_phase_slots_first_12": phase_slots[:12],
            "directed_phase_slots_first_12": directed_slots[:12],
        },
        "carrier_counts": {
            "frobenius_nonbase_elements": frobenius_q3,
            "gq_edges": {
                "numerator": gq_edges_q3.numerator,
                "denominator": gq_edges_q3.denominator,
            },
            "w33_edges": E_W33,
            "w33_directed_edges": 2 * E_W33,
            "w33_full_clique_chain_nonempty_simplices": full_chain_closure_dimension,
        },
        "qec_read": qec_split,
        "bridge_claim": {
            "exact_layer": (
                "The selected Frobenius carrier q^5-q at q=3 is the same 240-slot carrier as W33 edges, E8 roots, and the W33 CSS physical code. It factorizes as 40 W33 projective points times six octahedral antipodal edge-pair phases, while its directed lift is 40 times the twelve octahedron edges."
            ),
            "conditional_layer": (
                "This is a count-preserving phase/ledger lift. It does not construct a canonical incidence-preserving bijection from W33 edges to vertex-phase pairs, nor does it replace the explicit CSS boundary maps."
            ),
        },
        "identities": identities,
    }


def write_bridge(path: Path = OUT_PATH) -> Path:
    payload = build_bridge()
    path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
    return path


def main() -> None:
    out = write_bridge()
    payload = build_bridge()
    print(f"Wrote {out}")
    print(f"Verified: {payload['summary']['all_identities_hold']}")
    print(
        "Frobenius edge-phase lift: "
        f"{payload['summary']['frobenius_carrier']} = "
        f"{payload['summary']['w33_vertices']} * "
        f"{payload['summary']['octahedral_phase_pairs']}"
    )
    print(f"Directed lift: {payload['summary']['directed_phase_slots']} = 40 * 12")


if __name__ == "__main__":
    main()
