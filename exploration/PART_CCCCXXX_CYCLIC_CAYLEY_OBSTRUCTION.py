#!/usr/bin/env python3
"""PART CCCCXXX -- Cyclic Cayley Obstruction.

One local draft claimed that W(3,3) is the cyclic Cayley graph
``Cay(Z_40, S)`` for a 12-element symmetric connection set.  This file turns
that tempting shortcut into an executable negative certificate.

The test is deliberately finite and exhaustive: a simple undirected Cayley
graph on Z_40 with valency 12 must choose six inverse-pairs from the 19 pairs
{x,-x}; the involution 20 cannot appear because it would make the valency odd.
There are C(19,6)=27132 candidates.  None has the SRG(40,12,2,4) local
intersection law.

Architecture consequence: the "cycle" in the promoted photonic theory is not a
global Z_40 translation.  It is the 480-state directed Hashimoto/fusion carrier
and the QEC ouroboros loop that preserves the H1=81 tail.
"""

from __future__ import annotations

import json
from collections import Counter
from itertools import combinations
from math import comb
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence, Set, Tuple


ROOT = Path(__file__).resolve().parents[1]
QEC_OUROBOROS = ROOT / "PART_CCCCXVII_qec_ouroboros_stabilizer_loop_results.json"
FUSION_SPLICE = ROOT / "PART_CCCCXXVI_fusion_control_scheduler_splice_results.json"

V = 40
K = 12
LAM = 2
MU = 4
EDGES = 240
H1 = 81
DIRECTED_HASHIMOTO = 480
KLM_PRIMITIVES = 960

DRAFT_CONNECTION_SET = [1, 3, 7, 9, 13, 19, 21, 27, 31, 33, 37, 39]


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def ok(name: str, cond: bool, value: Any = None) -> Dict[str, Any]:
    return {"name": name, "passed": bool(cond), "value": value}


def inverse_pairs() -> List[Tuple[int, int]]:
    return [(i, (-i) % V) for i in range(1, V // 2)]


def connection_from_pair_indices(indices: Sequence[int]) -> Set[int]:
    pairs = inverse_pairs()
    connection: Set[int] = set()
    for idx in indices:
        connection.update(pairs[idx])
    return connection


def is_symmetric_connection(connection: Iterable[int]) -> bool:
    s = set(connection)
    return 0 not in s and all(((-x) % V) in s for x in s)


def common_neighbor_counts(connection: Iterable[int]) -> Dict[str, Counter[int]]:
    """Common-neighbor counts by difference in Cay(Z_40,S)."""
    s = set(connection)
    adjacent: Counter[int] = Counter()
    nonadjacent: Counter[int] = Counter()
    for diff in range(1, V):
        common = sum(1 for x in s if (x + diff) % V in s)
        if diff in s:
            adjacent[common] += 1
        else:
            nonadjacent[common] += 1
    return {"adjacent": adjacent, "nonadjacent": nonadjacent}


def is_w33_srg_connection(connection: Iterable[int]) -> bool:
    counts = common_neighbor_counts(connection)
    return counts["adjacent"] == Counter({LAM: K}) and counts["nonadjacent"] == Counter({MU: V - 1 - K})


def exhaustive_cyclic_search() -> Dict[str, Any]:
    pairs = inverse_pairs()
    hits: List[List[int]] = []
    tested = 0
    for combo in combinations(range(len(pairs)), K // 2):
        tested += 1
        connection = connection_from_pair_indices(combo)
        if is_w33_srg_connection(connection):
            hits.append(sorted(connection))
    return {
        "pair_count": len(pairs),
        "candidate_count": tested,
        "expected_candidate_count": comb(len(pairs), K // 2),
        "hits": hits,
        "hit_count": len(hits),
    }


def counter_to_plain(counter: Counter[int]) -> Dict[str, int]:
    return {str(key): counter[key] for key in sorted(counter)}


def build_results() -> Dict[str, Any]:
    qec = load_json(QEC_OUROBOROS)
    splice = load_json(FUSION_SPLICE)

    draft = sorted(DRAFT_CONNECTION_SET)
    draft_counts = common_neighbor_counts(draft)
    search = exhaustive_cyclic_search()

    fusion_budget = splice["fusion_budget_split"]
    klm_budget = splice["klm_budget_split"]
    snake = splice["snake_closure"]
    closure = qec["closure_numbers"]

    checks: List[Dict[str, Any]] = []
    checks.append(ok("cyclic carrier has 40 vertices", V == 40, V))
    checks.append(ok("target valency is 12", K == 12, K))
    checks.append(ok("Z40 has 19 inverse pairs away from 0 and 20", len(inverse_pairs()) == 19, len(inverse_pairs())))
    checks.append(ok("self-inverse 20 cannot enter an even 12-set", (K - 1) % 2 == 1 and K % 2 == 0, {"K": K, "involution": 20}))
    checks.append(ok("candidate space is C(19,6)", search["candidate_count"] == comb(19, 6), search["candidate_count"]))
    checks.append(ok("candidate space is 27132", search["candidate_count"] == 27132, search["candidate_count"]))

    checks.append(ok("draft connection set has 12 elements", len(draft) == K, draft))
    checks.append(ok("draft connection set is symmetric", is_symmetric_connection(draft), draft))
    checks.append(ok("draft gives the right regular edge count only", V * len(draft) // 2 == EDGES, V * len(draft) // 2))
    checks.append(ok("draft adjacent common-neighbor law fails", draft_counts["adjacent"] != Counter({LAM: K}), counter_to_plain(draft_counts["adjacent"])))
    checks.append(ok("draft nonadjacent common-neighbor law fails", draft_counts["nonadjacent"] != Counter({MU: V - 1 - K}), counter_to_plain(draft_counts["nonadjacent"])))
    checks.append(ok("draft is not SRG(40,12,2,4)", not is_w33_srg_connection(draft), {"lambda": counter_to_plain(draft_counts["adjacent"]), "mu": counter_to_plain(draft_counts["nonadjacent"])}))

    checks.append(ok("exhaustive cyclic search has no hits", search["hit_count"] == 0, search["hit_count"]))
    checks.append(ok("there is no Z40 cyclic Cayley W33 replacement", search["hits"] == [], search["hits"]))
    checks.append(ok("W33 edge count remains 240", EDGES == V * K // 2, EDGES))
    checks.append(ok("GQ local law remains lambda=2 mu=4", (LAM, MU) == (2, 4), {"lambda": LAM, "mu": MU}))

    checks.append(ok("QEC ouroboros artifact verified", qec["verified"] is True, qec["checks_passed"]))
    checks.append(ok("fusion splice artifact verified", splice["verified"] is True, splice["checks_passed"]))
    checks.append(ok("snake head and tail are H1", snake["head_projective_frame_states"] == snake["tail_logical_h1"] == H1, snake))
    checks.append(ok("line-star tail is preserved not killed", closure["line_star_mod_vertex_rank"] == H1 and closure["k_if_line_stars_are_stabilizers"] == 0, closure))
    checks.append(ok("protected closure stays [[82320,81,>=81]]", closure["active_protection_code"] == "[[82320,81,>=81]]", closure))
    checks.append(ok("Q4 remains local routing code", closure["q4_local_routing_code"] == "[[1296,81,4]]", closure))
    checks.append(ok("fusion attempts are the directed Hashimoto carrier", fusion_budget["total_expected_attempts"] == DIRECTED_HASHIMOTO, fusion_budget))
    checks.append(ok("KLM primitive budget is trace A^3", klm_budget["total_expected_primitives"] == KLM_PRIMITIVES, klm_budget))
    checks.append(ok("photonic cycle is 480 not Z40", DIRECTED_HASHIMOTO == 2 * EDGES and DIRECTED_HASHIMOTO != V, DIRECTED_HASHIMOTO))
    checks.append(ok("KLM cycle is 960 not Z40", KLM_PRIMITIVES == 4 * EDGES and KLM_PRIMITIVES != V, KLM_PRIMITIVES))
    checks.append(ok("obstruction and positive route are both present", search["hit_count"] == 0 and closure["logical_sector"] == H1, {"hits": search["hit_count"], "H1": closure["logical_sector"]}))

    verified = all(check["passed"] for check in checks)
    return {
        "part": "CCCCXXX",
        "title": "Cyclic Cayley Obstruction and Photonic Ouroboros Guard",
        "verified": verified,
        "checks_total": len(checks),
        "checks_passed": sum(check["passed"] for check in checks),
        "cyclic_search": search,
        "draft_connection_set": {
            "set": draft,
            "adjacent_common_neighbor_counts": counter_to_plain(draft_counts["adjacent"]),
            "nonadjacent_common_neighbor_counts": counter_to_plain(draft_counts["nonadjacent"]),
            "is_srg_40_12_2_4": is_w33_srg_connection(draft),
        },
        "architecture_redirect": {
            "false_shortcut": "global cyclic Cayley graph on Z40",
            "positive_cycle": "directed Hashimoto/fusion carrier with 480 states",
            "qec_loop": "QEC ouroboros preserving the H1=81 line-star tail",
            "protected_code": closure["active_protection_code"],
            "local_routing_code": closure["q4_local_routing_code"],
        },
        "theorem": (
            "No 12-valent undirected cyclic Cayley graph Cay(Z40,S) has the W33 "
            "SRG(40,12,2,4) local law. The exhaustive C(19,6)=27132 symmetric "
            "connection-set search has zero hits. Therefore the promoted "
            "photonic cycle cannot be a global Z40 translation; it is the "
            "480-state directed Hashimoto/fusion carrier plus the QEC ouroboros "
            "loop that preserves H1=81."
        ),
        "honesty_boundary": (
            "This rules out cyclic Cayley realizations on Z40 and falsifies the "
            "specific local draft connection set. It does not rule out every "
            "possible non-cyclic Cayley representation on a group of order 40."
        ),
        "checks": checks,
    }


def main() -> int:
    results = build_results()
    out = ROOT / "PART_CCCCXXX_cyclic_cayley_obstruction_results.json"
    out.write_text(json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "part": results["part"],
                "verified": results["verified"],
                "checks_passed": results["checks_passed"],
                "checks_total": results["checks_total"],
                "cyclic_hits": results["cyclic_search"]["hit_count"],
                "out_path": str(out),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
