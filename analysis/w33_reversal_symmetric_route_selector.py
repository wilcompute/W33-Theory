#!/usr/bin/env python3
"""Reversal-symmetric W33 route selector.

The first perfect selector stored one two-bit choice for each ordered nonlocal
pair:

    1080 ordered pairs * 2 bits = 270 bytes.

This verifier asks for the stronger architecture law: choose one relay for each
unordered nonlocal pair, then use the same relay in both directions.  The target
line load is forced:

    540 unordered pairs * 2 line buses / 40 buses = 27.

If every line is hit exactly 27 times in the unordered schedule, the ordered
schedule is automatically perfect at 54, and direct routes lift the full
nonidentity workload to 66 on every line.  The runtime selector then becomes

    540 choices * 2 bits = 1080 bits = 135 bytes.
"""

from __future__ import annotations

import argparse
import json
import math
import random
from collections import Counter
from pathlib import Path
from typing import Any

import holonet_node as hn
from w33_component_execution_simulator import line_lookup
from w33_perfect_route_selector_runtime import direct_line_loads, pack_choices, unpack_choices
from w33_uor_runtime_model import ROOT, all_lines, point_id


DEFAULT_JSON = ROOT / "data" / "w33_reversal_symmetric_route_selector.json"
DEFAULT_MD = ROOT / "docs" / "w33_reversal_symmetric_route_selector.md"
TARGET_UNORDERED_LOAD = 27


def unordered_nonadjacent_options(
    lookup: dict[tuple[int, int], int],
) -> tuple[list[tuple[int, int]], list[list[dict[str, Any]]]]:
    """Return unordered nonadjacent pairs and their four common-relay options."""

    pairs: list[tuple[int, int]] = []
    options: list[list[dict[str, Any]]] = []
    for src_idx, src in enumerate(hn.POINTS):
        for dst_idx in range(src_idx + 1, len(hn.POINTS)):
            dst = hn.POINTS[dst_idx]
            if hn.symplectic(src, dst) == 0:
                continue
            rows = []
            for relay in hn.multipath(src, dst):
                relay_idx = hn.POINTS.index(relay)
                rows.append(
                    {
                        "relay_index": relay_idx,
                        "relay": point_id(relay),
                        "line_pair": [lookup[(src_idx, relay_idx)], lookup[(relay_idx, dst_idx)]],
                    }
                )
            options.append(sorted(rows, key=lambda row: row["relay_index"]))
            pairs.append((src_idx, dst_idx))
    return pairs, options


def load_score(loads: list[int]) -> int:
    return sum((load - TARGET_UNORDERED_LOAD) ** 2 for load in loads)


def greedy_assignment(
    options: list[list[dict[str, Any]]], order: list[int]
) -> tuple[list[int], list[int]]:
    assignment: list[int | None] = [None] * len(options)
    loads = [0] * 40
    for route_idx in order:
        rows = options[route_idx]
        choice = min(
            range(4),
            key=lambda idx: (
                loads[rows[idx]["line_pair"][0]] + loads[rows[idx]["line_pair"][1]],
                max(loads[rows[idx]["line_pair"][0]], loads[rows[idx]["line_pair"][1]]),
                rows[idx]["line_pair"],
                rows[idx]["relay_index"],
            ),
        )
        assignment[route_idx] = choice
        for line_id in rows[choice]["line_pair"]:
            loads[line_id] += 1
    return [int(choice) for choice in assignment], loads


def delta_score(loads: list[int], old_pair: list[int], new_pair: list[int]) -> int:
    affected = set(old_pair + new_pair)
    before = sum((loads[line] - TARGET_UNORDERED_LOAD) ** 2 for line in affected)
    tmp = {line: loads[line] for line in affected}
    for line in old_pair:
        tmp[line] -= 1
    for line in new_pair:
        tmp[line] += 1
    after = sum((tmp[line] - TARGET_UNORDERED_LOAD) ** 2 for line in affected)
    return after - before


def find_perfect_unordered_assignment(
    options: list[list[dict[str, Any]]],
    *,
    seed: int = 20260706,
    restarts: int = 8,
    max_iterations: int = 60_000,
) -> dict[str, Any]:
    """Deterministic local search for the exact 27-per-line certificate."""

    rng = random.Random(seed)
    identity_order = list(range(len(options)))
    best_assignment, best_loads = greedy_assignment(options, identity_order)
    best_score = load_score(best_loads)
    progress = [
        {
            "restart": "identity",
            "iteration": 0,
            "score": best_score,
            "load_min": min(best_loads),
            "load_max": max(best_loads),
        }
    ]

    for restart in range(restarts):
        order = list(range(len(options)))
        rng.shuffle(order)
        assignment, loads = greedy_assignment(options, order)
        current = load_score(loads)
        temperature = 2.0
        if current < best_score:
            best_score = current
            best_assignment = assignment.copy()
            best_loads = loads.copy()
            progress.append(
                {
                    "restart": restart,
                    "iteration": 0,
                    "score": best_score,
                    "load_min": min(best_loads),
                    "load_max": max(best_loads),
                }
            )

        for iteration in range(max_iterations):
            if current == 0:
                return {
                    "found": True,
                    "seed": seed,
                    "restart": restart,
                    "iteration": iteration,
                    "assignment": assignment,
                    "loads": loads,
                    "score": current,
                    "progress": progress,
                }

            overloaded = [line for line, load in enumerate(loads) if load > TARGET_UNORDERED_LOAD]
            if overloaded:
                target_line = rng.choice(overloaded)
                candidate_routes = [
                    route_idx
                    for route_idx, choice in enumerate(assignment)
                    if target_line in options[route_idx][choice]["line_pair"]
                ]
            else:
                candidate_routes = []
            if not candidate_routes:
                candidate_routes = list(range(len(options)))

            route_idx = rng.choice(candidate_routes)
            old_choice = assignment[route_idx]
            old_pair = options[route_idx][old_choice]["line_pair"]
            best_delta = 10**9
            best_choices: list[int] = []
            for choice, row in enumerate(options[route_idx]):
                if choice == old_choice:
                    continue
                delta = delta_score(loads, old_pair, row["line_pair"])
                if delta < best_delta:
                    best_delta = delta
                    best_choices = [choice]
                elif delta == best_delta:
                    best_choices.append(choice)

            new_choice = rng.choice(best_choices)
            accept = best_delta <= 0 or rng.random() < math.exp(
                -best_delta / max(0.01, temperature)
            )
            if accept:
                for line_id in old_pair:
                    loads[line_id] -= 1
                for line_id in options[route_idx][new_choice]["line_pair"]:
                    loads[line_id] += 1
                assignment[route_idx] = new_choice
                current += best_delta
                if current < best_score:
                    best_score = current
                    best_assignment = assignment.copy()
                    best_loads = loads.copy()
                    progress.append(
                        {
                            "restart": restart,
                            "iteration": iteration,
                            "score": best_score,
                            "load_min": min(best_loads),
                            "load_max": max(best_loads),
                        }
                    )
            temperature *= 0.99995

    return {
        "found": False,
        "seed": seed,
        "restart": None,
        "iteration": None,
        "assignment": best_assignment,
        "loads": best_loads,
        "score": best_score,
        "progress": progress,
    }


def actual_line_pair(src_idx: int, relay_idx: int, dst_idx: int, lookup: dict[tuple[int, int], int]) -> list[int]:
    return [lookup[(src_idx, relay_idx)], lookup[(relay_idx, dst_idx)]]


def build_payload() -> dict[str, Any]:
    lines = all_lines()
    lookup = line_lookup(lines)
    pairs, options = unordered_nonadjacent_options(lookup)
    search = find_perfect_unordered_assignment(options)
    choices = [int(choice) for choice in search["assignment"]]
    packed = pack_choices(choices)
    unpacked = unpack_choices(packed, len(choices))
    pair_to_route_index = {pair: idx for idx, pair in enumerate(pairs)}

    unordered_loads = [0] * len(lines)
    relay_loads = [0] * len(hn.POINTS)
    certificate_rows = []
    for route_idx, choice in enumerate(choices):
        src_idx, dst_idx = pairs[route_idx]
        row = options[route_idx][choice]
        for line_id in row["line_pair"]:
            unordered_loads[line_id] += 1
        relay_loads[int(row["relay_index"])] += 1
        certificate_rows.append(
            {
                "route_index": route_idx,
                "source": point_id(hn.POINTS[src_idx]),
                "destination": point_id(hn.POINTS[dst_idx]),
                "relay": row["relay"],
                "relay_index": row["relay_index"],
                "line_pair": row["line_pair"],
                "choice": choice,
            }
        )

    direct_loads = direct_line_loads(lookup, len(lines))
    nonlocal_ordered_loads = [2 * load for load in unordered_loads]
    full_loads = [
        direct + nonlocal_load for direct, nonlocal_load in zip(direct_loads, nonlocal_ordered_loads)
    ]
    route_counts = Counter()
    reverse_checks = []
    route_preview = []
    for src_idx, src in enumerate(hn.POINTS):
        for dst_idx, dst in enumerate(hn.POINTS):
            if src_idx == dst_idx:
                route_counts["identity"] += 1
            elif hn.symplectic(src, dst) == 0:
                route_counts["direct"] += 1
            else:
                route_counts["reversal_symmetric_two_hop"] += 1
                key = (src_idx, dst_idx) if src_idx < dst_idx else (dst_idx, src_idx)
                route_idx = pair_to_route_index[key]
                choice = unpacked[route_idx]
                relay_idx = int(options[route_idx][choice]["relay_index"])
                line_pair = actual_line_pair(src_idx, relay_idx, dst_idx, lookup)
                reverse_checks.append(
                    {
                        "pair": [src_idx, dst_idx],
                        "unordered_index": route_idx,
                        "relay_index": relay_idx,
                        "line_set": sorted(line_pair),
                    }
                )
                if len(route_preview) < 24:
                    route_preview.append(
                        {
                            "source": point_id(src),
                            "destination": point_id(dst),
                            "route": [point_id(src), point_id(hn.POINTS[relay_idx]), point_id(dst)],
                            "line_pair": line_pair,
                        }
                    )

    reverse_ok = True
    seen: dict[tuple[int, int], dict[str, Any]] = {}
    for row in reverse_checks:
        src_idx, dst_idx = row["pair"]
        reverse = (dst_idx, src_idx)
        if reverse in seen:
            reverse_row = seen[reverse]
            if (
                row["relay_index"] != reverse_row["relay_index"]
                or row["line_set"] != reverse_row["line_set"]
            ):
                reverse_ok = False
                break
        seen[(src_idx, dst_idx)] = row

    storage = {
        "unordered_choice_count": len(choices),
        "ordered_nonlocal_route_count": 2 * len(choices),
        "choice_bits": 2 * len(choices),
        "choice_bytes": len(packed),
        "packed_choice_preview": packed[:32],
        "previous_ordered_selector_bytes": 270,
        "bytes_saved_vs_ordered_selector": 270 - len(packed),
        "fraction_saved_vs_ordered_selector": (270 - len(packed)) / 270,
        "full_next_hop_table_bytes": 1600,
        "bytes_saved_vs_full_table": 1600 - len(packed),
        "fraction_saved_vs_full_table": (1600 - len(packed)) / 1600,
    }
    checks = {
        "search_found_exact_certificate": bool(search["found"]),
        "unordered_pair_count_540": len(choices) == 540,
        "ordered_nonlocal_pair_count_1080": 2 * len(choices) == 1080,
        "packed_selector_135_bytes": len(packed) == 135,
        "pack_roundtrip": unpacked == choices,
        "unordered_loads_are_27_each": set(unordered_loads) == {27},
        "ordered_nonlocal_loads_are_54_each": set(nonlocal_ordered_loads) == {54},
        "direct_loads_are_12_each": set(direct_loads) == {12},
        "full_all_pairs_loads_are_66_each": set(full_loads) == {66},
        "route_counts": dict(route_counts)
        == {"identity": 40, "direct": 480, "reversal_symmetric_two_hop": 1080},
        "same_relay_under_route_reversal": reverse_ok,
        "fair_share_identity": 540 * 2 // 40 == TARGET_UNORDERED_LOAD,
    }
    return {
        "schema": "w33.reversal_symmetric_route_selector.v1",
        "theorem": (
            "A reversal-symmetric 135-byte selector realizes perfectly balanced "
            "W33 all-pairs routing"
        ),
        "status": "PASS" if all(checks.values()) else "FAIL",
        "route_counts": dict(route_counts),
        "search": {
            "seed": search["seed"],
            "restart": search["restart"],
            "iteration": search["iteration"],
            "score": search["score"],
            "progress": search["progress"],
        },
        "storage": storage,
        "line_loads": {
            "unordered_nonlocal": unordered_loads,
            "ordered_nonlocal": nonlocal_ordered_loads,
            "direct": direct_loads,
            "full_nonidentity": full_loads,
            "unordered_histogram": {str(k): v for k, v in sorted(Counter(unordered_loads).items())},
            "ordered_nonlocal_histogram": {
                str(k): v for k, v in sorted(Counter(nonlocal_ordered_loads).items())
            },
            "direct_histogram": {str(k): v for k, v in sorted(Counter(direct_loads).items())},
            "full_histogram": {str(k): v for k, v in sorted(Counter(full_loads).items())},
        },
        "relay_core_usage": {
            "loads": relay_loads,
            "histogram": {str(k): v for k, v in sorted(Counter(relay_loads).items())},
            "average": sum(relay_loads) / len(relay_loads),
            "minimum": min(relay_loads),
            "maximum": max(relay_loads),
            "forced_integer_split_if_balanced": {"13": 20, "14": 20},
            "status": "frontier_not_optimized",
        },
        "selector": {
            "pair_order": "generated unordered non-adjacent W33 pairs from projective point order",
            "choice_encoding": "two bits per unordered nonlocal pair; both directions share the relay",
            "packed_bytes": packed,
        },
        "certificate_preview": certificate_rows[:60],
        "certificate_tail": certificate_rows[-20:],
        "certificate": certificate_rows,
        "route_preview": route_preview,
        "checks": checks,
        "interpretation": (
            "The nonlocal scheduler factors through route reversal.  A single "
            "unordered relay choice hits every line bus exactly 27 times; the "
            "two time orientations double that to the previously required 54. "
            "Direct routes contribute 12 more, yielding the h=6/K12 total 66."
        ),
        "honesty_boundary": (
            "This halves the selector vector but remains a finite choice vector. "
            "It does not yet prove a closed-form affine or group-equivariant "
            "formula for the 540 choices.  The emitted certificate balances line "
            "buses perfectly; relay-core balancing is recorded as a separate "
            "frontier rather than silently claimed."
        ),
    }


def markdown(payload: dict[str, Any]) -> str:
    storage = payload["storage"]
    return f"""# W(3,3) Reversal-Symmetric Route Selector

The ordered perfect selector can be halved.  Instead of storing one two-bit
choice for each ordered nonlocal pair, choose one relay for each unordered pair
and run the same relay in both directions.

```text
540 unordered nonlocal pairs * 2 bits = 1080 bits = 135 bytes
```

The fair-share line load is forced:

```text
540 unordered routes * 2 line buses / 40 buses = 27
```

The verifier finds an exact certificate with every line bus loaded `27` times.
After adding both time orientations this is `54`, and direct routes add `12`, so
the full nonidentity workload still lands at `66` on every W33 line.

| Quantity | Value |
|---|---:|
| Unordered nonlocal choices | `{storage['unordered_choice_count']}` |
| Ordered nonlocal routes represented | `{storage['ordered_nonlocal_route_count']}` |
| Selector bytes | `{storage['choice_bytes']}` |
| Bytes saved vs ordered selector | `{storage['bytes_saved_vs_ordered_selector']}` |
| Bytes saved vs full 40x40 next-hop table | `{storage['bytes_saved_vs_full_table']}` |

Line-load histograms:

```text
unordered_nonlocal = {payload['line_loads']['unordered_histogram']}
ordered_nonlocal   = {payload['line_loads']['ordered_nonlocal_histogram']}
direct             = {payload['line_loads']['direct_histogram']}
full_nonidentity   = {payload['line_loads']['full_histogram']}
```

Interpretation: W33 routing has a time-reversal compression law.  The
`66 = 12 + 2*27` decomposition says direct incidence contributes the base
degree, while the nonlocal layer is two orientations of an exact genus-6/K12
fair-share scheduler.

Boundary: this is still a finite selector vector, not a closed-form affine rule.
The emitted certificate optimizes line-bus balance; relay-core usage is tracked
separately as `{payload['relay_core_usage']['histogram']}` against the ideal
integer split `{{"13": 20, "14": 20}}`.
"""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json-out", default=str(DEFAULT_JSON))
    parser.add_argument("--md-out", default=str(DEFAULT_MD))
    args = parser.parse_args(argv)

    payload = build_payload()
    json_out = Path(args.json_out)
    if not json_out.is_absolute():
        json_out = ROOT / json_out
    md_out = Path(args.md_out)
    if not md_out.is_absolute():
        md_out = ROOT / md_out
    json_out.parent.mkdir(parents=True, exist_ok=True)
    md_out.parent.mkdir(parents=True, exist_ok=True)
    json_out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    md_out.write_text(markdown(payload), encoding="utf-8")
    print(f"status: {payload['status']}")
    print(f"selector bytes: {payload['storage']['choice_bytes']}")
    print(f"search: {payload['search']}")
    print(f"full load histogram: {payload['line_loads']['full_histogram']}")
    print(f"wrote: {json_out.relative_to(ROOT)}")
    print(f"wrote: {md_out.relative_to(ROOT)}")
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
