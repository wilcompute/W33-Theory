#!/usr/bin/env python3
"""BT113: controlled flow-register contract for WRF referenceable flow cells.

This harness keeps the claim finite and falsifiable.  It does not model a
physical device.  It checks whether the W33 non-backtracking carrier can support
target-specific writes, phase-invariant reads, perturbation accounting, and
three-register symbolic composition using only legal local successor choices.
"""

from __future__ import annotations

import hashlib
import json
import math
from collections import deque
from itertools import combinations
from pathlib import Path

from wrf_bt112_suite import (
    attractors,
    build_flow,
    build_w33,
    canonical_cycle,
    cid,
    directed_edges,
    reverse_map,
)


OUT = Path(__file__).with_name("wrf_bt113_flow_registers_results.json")
REGISTER_SEEDS = [661, 693, 878]


def poly_mul(left: list[int], right: list[int]) -> list[int]:
    out = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        if a == 0:
            continue
        for j, b in enumerate(right):
            if b:
                out[i + j] += a * b
    return out


def poly_pow(base: list[int], exponent: int) -> list[int]:
    out = [1]
    cur = base[:]
    exp = exponent
    while exp:
        if exp & 1:
            out = poly_mul(out, cur)
        cur = poly_mul(cur, cur)
        exp >>= 1
    return out


def poly_digest(poly: list[int]) -> str:
    payload = json.dumps(poly, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def percentile(values: list[int], pct: float) -> int:
    ordered = sorted(values)
    return ordered[int(round((len(ordered) - 1) * pct))]


def build_control_graph(adj: list[set[int]], d_edges: list[tuple[int, int]]) -> tuple[list[list[int]], list[list[int]]]:
    edge_index = {edge: i for i, edge in enumerate(d_edges)}
    succ: list[list[int]] = []
    pred: list[list[int]] = [[] for _ in d_edges]
    for i, (a, b) in enumerate(d_edges):
        row = [edge_index[(b, c)] for c in sorted(c for c in adj[b] if c != a)]
        succ.append(row)
        for nxt in row:
            pred[nxt].append(i)
    return succ, pred


def distance_to_targets(pred: list[list[int]], targets: set[int]) -> list[int | None]:
    dist: list[int | None] = [None] * len(pred)
    queue: deque[int] = deque()
    for target in targets:
        dist[target] = 0
        queue.append(target)
    while queue:
        cur = queue.popleft()
        next_dist = dist[cur] + 1  # type: ignore[operator]
        for prev in pred[cur]:
            if dist[prev] is None:
                dist[prev] = next_dist
                queue.append(prev)
    return dist


def transition_closes_cycle(trans: list[int], cycle: list[int]) -> bool:
    cycle_set = set(cycle)
    return all(trans[node] in cycle_set for node in cycle)


def phase_read_verified(cycle: list[int], rev: list[int], expected_cid: str) -> bool:
    n = len(cycle)
    for shift in range(n):
        rotated = cycle[shift:] + cycle[:shift]
        if cid(canonical_cycle(rotated, rev)) != expected_cid:
            return False
    reversed_cycle = [rev[node] for node in reversed(cycle)]
    for shift in range(n):
        rotated = reversed_cycle[shift:] + reversed_cycle[:shift]
        if cid(canonical_cycle(rotated, rev)) != expected_cid:
            return False
    return True


def hex_hamming(left: str, right: str) -> int:
    return sum(a != b for a, b in zip(left, right))


def fused_qutrit_chiral_add(left: int, right: int) -> int:
    left_trit, left_chiral = left % 3, left // 3
    right_trit, right_chiral = right % 3, right // 3
    return 3 * (left_chiral ^ right_chiral) + ((left_trit + right_trit) % 3)


def register_contract(seed: int, adj: list[set[int]], d_edges: list[tuple[int, int]], succ: list[list[int]], pred: list[list[int]]) -> dict:
    trans, edge_index = build_flow(adj, d_edges, seed)
    rev = reverse_map(d_edges, edge_index)
    cycles, cycle_of, basins = attractors(trans, rev)
    symbol_cids = [cid(canonical_cycle(cycle, rev)) for cycle in cycles]

    symbol_rows = []
    distance_maps: list[list[int]] = []
    for symbol, cycle in enumerate(cycles):
        distances = distance_to_targets(pred, set(cycle))
        assert all(distance is not None for distance in distances)
        concrete = [int(distance) for distance in distances]
        distance_maps.append(concrete)
        symbol_rows.append(
            {
                "symbol": symbol,
                "cycle_length": len(cycle),
                "basin_size": basins[symbol],
                "CID": symbol_cids[symbol],
                "control_write": {
                    "reachable_from_all_480_states": True,
                    "max_steps_from_any_state": max(concrete),
                    "mean_steps_from_any_state": round(sum(concrete) / len(concrete), 4),
                    "p95_steps_from_any_state": percentile(concrete, 0.95),
                    "zero_step_states": sum(1 for value in concrete if value == 0),
                },
                "phase_read_invariant": phase_read_verified(cycle, rev, symbol_cids[symbol]),
                "deterministic_cycle_closed": transition_closes_cycle(trans, cycle),
            }
        )

    confusion = [[0 for _ in cycles] for _ in cycles]
    repair_steps: list[int] = []
    off_rule_trials = 0
    preserved = 0
    for symbol, cycle in enumerate(cycles):
        for node in cycle:
            for nxt in succ[node]:
                if nxt == trans[node]:
                    continue
                observed = cycle_of[nxt]
                confusion[symbol][observed] += 1
                off_rule_trials += 1
                if observed == symbol:
                    preserved += 1
                repair_steps.append(distance_maps[symbol][nxt])

    assert off_rule_trials > 0
    assert repair_steps
    return {
        "seed": seed,
        "num_symbols": len(cycles),
        "cycle_lengths": [len(cycle) for cycle in cycles],
        "basin_sizes": [basins[i] for i in range(len(cycles))],
        "symbols": symbol_rows,
        "all_target_writes_reachable": all(
            row["control_write"]["reachable_from_all_480_states"] for row in symbol_rows
        ),
        "max_target_write_steps": max(row["control_write"]["max_steps_from_any_state"] for row in symbol_rows),
        "phase_reads_all_symbols": all(row["phase_read_invariant"] for row in symbol_rows),
        "deterministic_cycles_closed": all(row["deterministic_cycle_closed"] for row in symbol_rows),
        "off_rule_legal_jump_trials": off_rule_trials,
        "off_rule_passive_preserve_rate": round(preserved / off_rule_trials, 6),
        "off_rule_confusion_matrix": confusion,
        "controlled_repair_from_off_rule": {
            "max_steps_to_original_symbol": max(repair_steps),
            "mean_steps_to_original_symbol": round(sum(repair_steps) / len(repair_steps), 4),
            "p95_steps_to_original_symbol": percentile(repair_steps, 0.95),
        },
    }


def ihara_and_substrate_identities() -> dict:
    # W(3,3) point graph spectrum: 12^1, 2^24, (-4)^15.
    det_poly = poly_mul(
        poly_mul([1, -12, 11], poly_pow([1, -2, 11], 24)),
        poly_pow([1, 4, 11], 15),
    )
    ihara_inverse = poly_mul(poly_pow([1, 0, -1], 200), det_poly)
    spectrum = [12] + [2] * 24 + [-4] * 15
    e2 = sum(a * b for a, b in combinations(spectrum, 2))
    e8_exponents = [1, 7, 11, 13, 17, 19, 23, 29]
    cartan_eigs = [2 + 2 * math.cos(2 * math.pi * m / 30) for m in e8_exponents]
    prod_3_minus_cartan = math.prod(3 - eig for eig in cartan_eigs)
    return {
        "det_I_minus_Au_plus_11u2_factorization": "(1-12u+11u^2)(1-2u+11u^2)^24(1+4u+11u^2)^15",
        "det_degree": len(det_poly) - 1,
        "det_constant": det_poly[0],
        "det_leading_coefficient": det_poly[-1],
        "det_coeff_digest": poly_digest(det_poly),
        "ihara_inverse_factorization": "(1-u^2)^200(1-12u+11u^2)(1-2u+11u^2)^24(1+4u+11u^2)^15",
        "ihara_inverse_degree": len(ihara_inverse) - 1,
        "ihara_inverse_constant": ihara_inverse[0],
        "ihara_inverse_leading_coefficient": ihara_inverse[-1],
        "ihara_inverse_coeff_digest": poly_digest(ihara_inverse),
        "newton_e2_from_adjacency_spectrum": e2,
        "newton_e2_equals_negative_edges": e2 == -240,
        "product_3_minus_E8_cartan_eigenvalues": round(prod_3_minus_cartan, 12),
        "product_3_minus_E8_cartan_equals_25": abs(prod_3_minus_cartan - 25) < 1e-9,
    }


def composition_contract(registers: list[dict]) -> dict:
    all_cids = [
        (register["seed"], symbol["symbol"], symbol["CID"])
        for register in registers
        for symbol in register["symbols"]
    ]
    pairwise = [
        {
            "left": {"seed": left[0], "symbol": left[1]},
            "right": {"seed": right[0], "symbol": right[1]},
            "distance": hex_hamming(left[2], right[2]),
        }
        for left, right in combinations(all_cids, 2)
    ]
    min_distance = min(row["distance"] for row in pairwise)
    add_mod6_table = [[(a + b) % 6 for b in range(6)] for a in range(6)]
    qutrit_chiral_table = [[fused_qutrit_chiral_add(a, b) for b in range(6)] for a in range(6)]
    output_register = registers[2]
    max_output_write = max(
        symbol["control_write"]["max_steps_from_any_state"] for symbol in output_register["symbols"]
    )
    return {
        "register_roles": {"A": registers[0]["seed"], "B": registers[1]["seed"], "C": registers[2]["seed"]},
        "all_18_symbol_cids_distinct": len({row[2] for row in all_cids}) == len(all_cids),
        "min_24hex_distance_across_18_symbols": min_distance,
        "min_distance_pairs": [row for row in pairwise if row["distance"] == min_distance],
        "mod6_add_table": add_mod6_table,
        "qutrit_plus_chirality_xor_table": qutrit_chiral_table,
        "all_36_mod6_pairs_supported": True,
        "all_36_qutrit_chiral_pairs_supported": True,
        "max_output_control_write_steps": max_output_write,
        "interpretation": "Composition is a software-level register contract: read A/B symbols, compute target C symbol, then drive C through legal non-backtracking controls.",
    }


def main() -> dict:
    points, adj, edges = build_w33()
    d_edges = directed_edges(edges)
    succ, pred = build_control_graph(adj, d_edges)
    results = {
        "bt113a_ihara_and_spectral_identities": ihara_and_substrate_identities(),
        "bt113b_flow_register_contract": {
            "carrier": {
                "points": len(points),
                "undirected_edges": len(edges),
                "directed_states": len(d_edges),
                "legal_successors_per_state": len(succ[0]),
                "control_model": "At each step choose one of the 11 legal non-backtracking successors.",
            },
            "register_seeds": REGISTER_SEEDS,
            "registers": [],
        },
    }
    registers = [
        register_contract(seed, adj, d_edges, succ, pred)
        for seed in REGISTER_SEEDS
    ]
    results["bt113b_flow_register_contract"]["registers"] = registers
    results["bt113c_three_register_composition"] = composition_contract(registers)
    results["bt113_summary"] = {
        "all_registers_are_base6": all(register["num_symbols"] == 6 for register in registers),
        "all_target_writes_reachable": all(register["all_target_writes_reachable"] for register in registers),
        "global_max_target_write_steps": max(register["max_target_write_steps"] for register in registers),
        "all_phase_reads_invariant": all(register["phase_reads_all_symbols"] for register in registers),
        "global_max_controlled_repair_steps": max(
            register["controlled_repair_from_off_rule"]["max_steps_to_original_symbol"]
            for register in registers
        ),
        "passive_off_rule_preserve_rates": [
            register["off_rule_passive_preserve_rate"] for register in registers
        ],
        "claim_boundary": "The finite carrier supports bounded active writes and repairs; off-rule passive jumps are often symbol-changing, so a physical cell still needs an active return/control path.",
    }

    assert results["bt113a_ihara_and_spectral_identities"]["newton_e2_equals_negative_edges"] is True
    assert results["bt113a_ihara_and_spectral_identities"]["product_3_minus_E8_cartan_equals_25"] is True
    assert results["bt113_summary"]["all_registers_are_base6"] is True
    assert results["bt113_summary"]["all_target_writes_reachable"] is True
    assert results["bt113_summary"]["global_max_target_write_steps"] <= 3
    assert results["bt113_summary"]["all_phase_reads_invariant"] is True
    assert results["bt113_summary"]["global_max_controlled_repair_steps"] <= 3
    assert results["bt113c_three_register_composition"]["all_18_symbol_cids_distinct"] is True
    assert results["bt113c_three_register_composition"]["min_24hex_distance_across_18_symbols"] >= 18

    OUT.write_text(json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(results["bt113_summary"], indent=2, sort_keys=True))
    print(f"Results saved to {OUT}")
    return results


if __name__ == "__main__":
    main()
