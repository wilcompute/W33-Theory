#!/usr/bin/env python3
"""BT114: actuator-limited control and finite read windows for WRF flow cells.

BT113 proved a register contract with an ideal 11-way local control choice.
BT114 asks whether that contract survives a smaller global control alphabet and
whether symbols can be read from short trace windows instead of whole cycles.
The model is still finite software evidence, not a physical device model.
"""

from __future__ import annotations

import itertools
import json
import math
from collections import deque
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
from wrf_bt113_flow_registers import REGISTER_SEEDS, build_control_graph, hex_hamming, percentile


OUT = Path(__file__).with_name("wrf_bt114_active_trace_io_results.json")


def restricted_predecessors(succ: list[list[int]], ports: tuple[int, ...]) -> list[list[int]]:
    pred: list[list[int]] = [[] for _ in succ]
    for src, row in enumerate(succ):
        for port in ports:
            pred[row[port]].append(src)
    return pred


def distance_to_targets(pred: list[list[int]], targets: set[int]) -> list[int | None]:
    dist: list[int | None] = [None] * len(pred)
    queue: deque[int] = deque()
    for target in targets:
        dist[target] = 0
        queue.append(target)
    while queue:
        cur = queue.popleft()
        cur_dist = dist[cur]
        assert cur_dist is not None
        for prev in pred[cur]:
            if dist[prev] is None:
                dist[prev] = cur_dist + 1
                queue.append(prev)
    return dist


def load_registers(adj: list[set[int]], d_edges: list[tuple[int, int]]) -> list[dict]:
    registers = []
    for seed in REGISTER_SEEDS:
        trans, edge_index = build_flow(adj, d_edges, seed)
        rev = reverse_map(d_edges, edge_index)
        cycles, cycle_of, basins = attractors(trans, rev)
        registers.append(
            {
                "seed": seed,
                "trans": trans,
                "rev": rev,
                "cycles": cycles,
                "cycle_of": cycle_of,
                "basins": basins,
                "cids": [cid(canonical_cycle(cycle, rev)) for cycle in cycles],
            }
        )
    return registers


def score_ports(
    succ: list[list[int]],
    registers: list[dict],
    ports: tuple[int, ...],
) -> dict | None:
    pred = restricted_predecessors(succ, ports)
    symbol_rows = []
    all_write_distances: list[int] = []
    all_repair_distances: list[int] = []
    for register in registers:
        register_rows = []
        for symbol, cycle in enumerate(register["cycles"]):
            distances = distance_to_targets(pred, set(cycle))
            if any(distance is None for distance in distances):
                return None
            concrete = [int(distance) for distance in distances]
            repair_distances = []
            for node in cycle:
                for nxt in succ[node]:
                    if nxt != register["trans"][node]:
                        repair_distances.append(int(distances[nxt]))
            all_write_distances.extend(concrete)
            all_repair_distances.extend(repair_distances)
            register_rows.append(
                {
                    "symbol": symbol,
                    "max_write_steps": max(concrete),
                    "mean_write_steps": round(sum(concrete) / len(concrete), 4),
                    "p95_write_steps": percentile(concrete, 0.95),
                    "max_repair_steps_from_off_rule_jump": max(repair_distances),
                    "mean_repair_steps_from_off_rule_jump": round(
                        sum(repair_distances) / len(repair_distances), 4
                    ),
                    "p95_repair_steps_from_off_rule_jump": percentile(repair_distances, 0.95),
                }
            )
        symbol_rows.append({"seed": register["seed"], "symbols": register_rows})

    return {
        "ports": list(ports),
        "port_count": len(ports),
        "all_target_writes_reachable": True,
        "global_max_target_write_steps": max(all_write_distances),
        "global_mean_target_write_steps": round(sum(all_write_distances) / len(all_write_distances), 4),
        "global_p95_target_write_steps": percentile(all_write_distances, 0.95),
        "global_max_repair_steps_from_off_rule_jump": max(all_repair_distances),
        "global_mean_repair_steps_from_off_rule_jump": round(
            sum(all_repair_distances) / len(all_repair_distances), 4
        ),
        "global_p95_repair_steps_from_off_rule_jump": percentile(all_repair_distances, 0.95),
        "binary_command_bits_per_step": math.ceil(math.log2(len(ports))),
        "worst_case_binary_command_bits": max(all_write_distances) * math.ceil(math.log2(len(ports))),
        "per_register_symbols": symbol_rows,
    }


def find_minimal_actuator(succ: list[list[int]], registers: list[dict]) -> dict:
    valid_counts: dict[str, int] = {}
    best_rows: list[dict] = []
    for port_count in range(1, 4):
        valid = []
        for ports in itertools.combinations(range(len(succ[0])), port_count):
            scored = score_ports(succ, registers, ports)
            if scored is not None:
                valid.append(scored)
        valid_counts[str(port_count)] = len(valid)
        if valid:
            valid.sort(
                key=lambda row: (
                    row["global_max_target_write_steps"],
                    row["global_mean_target_write_steps"],
                    row["ports"],
                )
            )
            best_rows = valid
            break

    assert best_rows
    best = best_rows[0]
    return {
        "minimal_global_port_count": best["port_count"],
        "valid_subsets_by_port_count_until_minimum": valid_counts,
        "best_global_ports": best["ports"],
        "best_global_ports_interpretation": (
            "Ports are canonical neighbor-rank selectors in the finite W33 carrier; "
            "they are not yet physical pins or voltages."
        ),
        "valid_minimal_subset_count": len(best_rows),
        "best": best,
        "normalized_control_cost": (
            "One abstract actuator token per restricted non-backtracking transition; "
            "binary command bits use ceil(log2(port_count)). No joule-scale device energy is claimed."
        ),
    }


def cyclic_windows(cycle: list[int], length: int) -> list[tuple[int, ...]]:
    return [
        tuple(cycle[(start + offset) % len(cycle)] for offset in range(length))
        for start in range(len(cycle))
    ]


def all_labeled_windows(registers: list[dict], length: int) -> list[tuple[tuple[int, int], tuple[int, ...]]]:
    rows = []
    for register in registers:
        for symbol, cycle in enumerate(register["cycles"]):
            label = (register["seed"], symbol)
            rows.extend((label, window) for window in cyclic_windows(cycle, length))
    return rows


def collision_count(rows: list[tuple[tuple[int, int], tuple[object, ...]]]) -> tuple[int, int]:
    owner: dict[tuple[object, ...], tuple[int, int]] = {}
    collisions = 0
    for label, pattern in rows:
        previous = owner.get(pattern)
        if previous is not None and previous != label:
            collisions += 1
        owner.setdefault(pattern, label)
    return collisions, len(owner)


def erased_patterns(window: tuple[int, ...], max_erasures: int) -> list[tuple[object, ...]]:
    patterns: list[tuple[object, ...]] = [window]
    for erasures in range(1, max_erasures + 1):
        for positions in itertools.combinations(range(len(window)), erasures):
            row: list[object] = list(window)
            for position in positions:
                row[position] = None
            patterns.append(tuple(row))
    return patterns


def gapped_windows(cycle: list[int], length: int, max_missed_between_samples: int) -> list[tuple[int, ...]]:
    windows = []
    increments = range(1, max_missed_between_samples + 2)
    for start in range(len(cycle)):
        for gaps in itertools.product(increments, repeat=length - 1):
            idx = start
            row = [cycle[idx % len(cycle)]]
            for gap in gaps:
                idx += gap
                row.append(cycle[idx % len(cycle)])
            windows.append(tuple(row))
    return windows


def min_exact_window(registers: list[dict], max_length: int = 12) -> dict:
    for length in range(1, max_length + 1):
        rows = all_labeled_windows(registers, length)
        collisions, unique = collision_count(rows)
        if collisions == 0:
            return {"min_window": length, "total_windows": len(rows), "unique_patterns": unique}
    raise AssertionError("no exact unique read window found")


def min_window_with_erasures(registers: list[dict], max_erasures: int, max_length: int = 12) -> dict:
    for length in range(max_erasures + 1, max_length + 1):
        rows: list[tuple[tuple[int, int], tuple[object, ...]]] = []
        for label, window in all_labeled_windows(registers, length):
            rows.extend((label, pattern) for pattern in erased_patterns(window, max_erasures))
        collisions, unique = collision_count(rows)
        if collisions == 0:
            return {
                "max_erasures": max_erasures,
                "min_window": length,
                "total_patterns": len(rows),
                "unique_patterns": unique,
            }
    raise AssertionError("no erasure-robust read window found")


def min_cross_hamming(rows: list[tuple[tuple[int, int], tuple[int, ...]]]) -> dict:
    best_distance = len(rows[0][1]) + 1
    best_pairs = []
    for left, right in itertools.combinations(rows, 2):
        if left[0] == right[0]:
            continue
        distance = sum(a != b for a, b in zip(left[1], right[1]))
        if distance < best_distance:
            best_distance = distance
            best_pairs = [
                {
                    "left": {"seed": left[0][0], "symbol": left[0][1]},
                    "right": {"seed": right[0][0], "symbol": right[0][1]},
                    "distance": distance,
                }
            ]
        elif distance == best_distance and len(best_pairs) < 4:
            best_pairs.append(
                {
                    "left": {"seed": left[0][0], "symbol": left[0][1]},
                    "right": {"seed": right[0][0], "symbol": right[0][1]},
                    "distance": distance,
                }
            )
    return {"min_cross_hamming": best_distance, "example_pairs": best_pairs}


def min_window_for_substitutions(registers: list[dict], substitutions: int, max_length: int = 14) -> dict:
    threshold = 2 * substitutions + 1
    for length in range(1, max_length + 1):
        rows = all_labeled_windows(registers, length)
        distance = min_cross_hamming(rows)
        if distance["min_cross_hamming"] >= threshold:
            return {
                "substitutions": substitutions,
                "min_window": length,
                "required_min_hamming": threshold,
                **distance,
            }
    raise AssertionError("no substitution-robust read window found")


def min_window_with_timing_gaps(
    registers: list[dict],
    max_missed_between_samples: int,
    max_length: int = 6,
) -> dict:
    for length in range(2, max_length + 1):
        rows: list[tuple[tuple[int, int], tuple[object, ...]]] = []
        for register in registers:
            for symbol, cycle in enumerate(register["cycles"]):
                label = (register["seed"], symbol)
                rows.extend((label, window) for window in gapped_windows(cycle, length, max_missed_between_samples))
        collisions, unique = collision_count(rows)
        if collisions == 0:
            return {
                "max_missed_between_samples": max_missed_between_samples,
                "min_window": length,
                "total_patterns": len(rows),
                "unique_patterns": unique,
            }
    raise AssertionError("no timing-gap-robust read window found")


def read_window_contract(registers: list[dict]) -> dict:
    total_cycle_states = sum(len(cycle) for register in registers for cycle in register["cycles"])
    symbol_count = sum(len(register["cycles"]) for register in registers)
    exact = min_exact_window(registers)
    substitutions = {
        str(errors): min_window_for_substitutions(registers, errors)
        for errors in (1, 2, 3)
    }
    erasures = {
        str(errors): min_window_with_erasures(registers, errors)
        for errors in (1, 2, 3)
    }
    timing_gaps = {
        str(gaps): min_window_with_timing_gaps(registers, gaps)
        for gaps in (1, 2)
    }
    return {
        "register_symbol_count": symbol_count,
        "cycle_phase_window_count": total_cycle_states,
        "symbol_payload_bits": round(math.log2(symbol_count), 4),
        "phase_window_bits": round(math.log2(total_cycle_states), 4),
        "raw_two_state_window_bits": round(2 * math.log2(480), 4),
        "exact_unique_read": exact,
        "substitution_robust_reads": substitutions,
        "erasure_robust_reads": erasures,
        "bounded_timing_gap_reads": timing_gaps,
        "interpretation": (
            "For the 18-symbol BT113 register bank, a short directed-state trace window "
            "identifies the register-symbol owner; the full attractor cycle is not needed for ordinary reads."
        ),
    }


def main() -> dict:
    points, adj, edges = build_w33()
    d_edges = directed_edges(edges)
    succ, _pred = build_control_graph(adj, d_edges)
    registers = load_registers(adj, d_edges)
    actuator = find_minimal_actuator(succ, registers)
    read_windows = read_window_contract(registers)
    result = {
        "bt114a_limited_actuator_contract": {
            "carrier": {
                "points": len(points),
                "undirected_edges": len(edges),
                "directed_states": len(d_edges),
                "full_legal_successors_per_state": len(succ[0]),
            },
            "register_seeds": REGISTER_SEEDS,
            **actuator,
        },
        "bt114b_finite_read_window_contract": read_windows,
        "bt114_summary": {
            "minimal_global_port_count": actuator["minimal_global_port_count"],
            "best_global_ports": actuator["best_global_ports"],
            "limited_actuator_max_write_steps": actuator["best"]["global_max_target_write_steps"],
            "limited_actuator_max_repair_steps": actuator["best"]["global_max_repair_steps_from_off_rule_jump"],
            "exact_read_window_states": read_windows["exact_unique_read"]["min_window"],
            "one_substitution_read_window_states": read_windows["substitution_robust_reads"]["1"]["min_window"],
            "one_erasure_read_window_states": read_windows["erasure_robust_reads"]["1"]["min_window"],
            "claim_boundary": (
                "BT114 replaces ideal 11-way local choice with a finite 3-port abstract actuator "
                "and replaces whole-cycle reads with short trace windows. Physical pin mapping, joules, "
                "latency, and device noise remain hardware work."
            ),
        },
    }

    assert result["bt114_summary"]["minimal_global_port_count"] == 3
    assert result["bt114_summary"]["best_global_ports"] == [0, 5, 6]
    assert result["bt114_summary"]["limited_actuator_max_write_steps"] == 7
    assert result["bt114_summary"]["limited_actuator_max_repair_steps"] == 7
    assert result["bt114b_finite_read_window_contract"]["exact_unique_read"]["min_window"] == 2
    assert result["bt114b_finite_read_window_contract"]["substitution_robust_reads"]["1"]["min_window"] == 4
    assert result["bt114b_finite_read_window_contract"]["erasure_robust_reads"]["1"]["min_window"] == 3
    assert result["bt114b_finite_read_window_contract"]["bounded_timing_gap_reads"]["2"]["min_window"] == 2

    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result["bt114_summary"], indent=2, sort_keys=True))
    print(f"Results saved to {OUT}")
    return result


if __name__ == "__main__":
    main()
