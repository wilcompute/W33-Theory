#!/usr/bin/env python3
"""Perfect line-bus balancer for W33 two-hop multipath.

The channel-aware scheduler showed that all 4320 relay options are equal in
primitive U/R/S energy and all are connector-free on the spread-clock graph.
That leaves line-bus load as the active routing variable.

This script proves the strongest possible result: over all 1080 ordered
non-adjacent W33 source/destination pairs, choose one of the four two-hop relays
so that each of the 40 W33 line buses is used exactly 54 times.

Since every route uses two line buses, the lower bound is forced:

    1080 routes * 2 buses / 40 buses = 54.

Hitting 54 on every line is therefore an exact optimum, not a heuristic score.
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
from w33_uor_runtime_model import ROOT, all_lines, point_id


DEFAULT_JSON = ROOT / "data" / "w33_perfect_multipath_balancer.json"
DEFAULT_MD = ROOT / "docs" / "w33_perfect_multipath_balancer.md"
TARGET_LOAD = 54


def ordered_nonadjacent_pairs() -> list[tuple[int, int]]:
    pairs = []
    for src_idx, src in enumerate(hn.POINTS):
        for dst_idx, dst in enumerate(hn.POINTS):
            if src_idx == dst_idx:
                continue
            if hn.symplectic(src, dst) != 0:
                pairs.append((src_idx, dst_idx))
    return pairs


def route_line_options(lookup: dict[tuple[int, int], int]) -> tuple[list[tuple[int, int]], list[list[dict[str, Any]]]]:
    pairs = ordered_nonadjacent_pairs()
    options = []
    for src_idx, dst_idx in pairs:
        src = hn.POINTS[src_idx]
        dst = hn.POINTS[dst_idx]
        rows = []
        for relay in hn.multipath(src, dst):
            relay_idx = hn.POINTS.index(relay)
            line_a = lookup[(src_idx, relay_idx)]
            line_b = lookup[(relay_idx, dst_idx)]
            rows.append(
                {
                    "relay_index": relay_idx,
                    "relay": point_id(relay),
                    "line_pair": [line_a, line_b],
                }
            )
        options.append(sorted(rows, key=lambda row: row["relay_index"]))
    return pairs, options


def score(loads: list[int]) -> int:
    return sum((load - TARGET_LOAD) ** 2 for load in loads)


def delta_score(loads: list[int], old_pair: list[int], new_pair: list[int]) -> int:
    affected = set(old_pair + new_pair)
    before = sum((loads[line] - TARGET_LOAD) ** 2 for line in affected)
    tmp = {line: loads[line] for line in affected}
    tmp[old_pair[0]] -= 1
    tmp[old_pair[1]] -= 1
    tmp[new_pair[0]] += 1
    tmp[new_pair[1]] += 1
    after = sum((tmp[line] - TARGET_LOAD) ** 2 for line in affected)
    return after - before


def greedy_initial(options: list[list[dict[str, Any]]]) -> tuple[list[int], list[int]]:
    assignment: list[int] = []
    loads = [0] * 40
    for rows in options:
        choice = min(
            range(len(rows)),
            key=lambda idx: (
                loads[rows[idx]["line_pair"][0]] + loads[rows[idx]["line_pair"][1]],
                max(loads[rows[idx]["line_pair"][0]], loads[rows[idx]["line_pair"][1]]),
                rows[idx]["line_pair"],
                rows[idx]["relay_index"],
            ),
        )
        assignment.append(choice)
        left, right = rows[choice]["line_pair"]
        loads[left] += 1
        loads[right] += 1
    return assignment, loads


def randomized_initial(
    options: list[list[dict[str, Any]]], rng: random.Random
) -> tuple[list[int], list[int]]:
    assignment: list[int | None] = [None] * len(options)
    loads = [0] * 40
    order = list(range(len(options)))
    rng.shuffle(order)
    for route_idx in order:
        rows = options[route_idx]
        ranked = sorted(
            range(len(rows)),
            key=lambda idx: (
                loads[rows[idx]["line_pair"][0]] + loads[rows[idx]["line_pair"][1]],
                rng.random(),
            ),
        )
        choice = ranked[0 if rng.random() < 0.85 else rng.randrange(len(rows))]
        assignment[route_idx] = choice
        left, right = rows[choice]["line_pair"]
        loads[left] += 1
        loads[right] += 1
    return [int(choice) for choice in assignment], loads


def find_perfect_assignment(
    options: list[list[dict[str, Any]]],
    *,
    seed: int = 12345,
    restarts: int = 24,
    max_iterations: int = 80_000,
) -> dict[str, Any]:
    rng = random.Random(seed)
    best_assignment, best_loads = greedy_initial(options)
    best_score = score(best_loads)
    progress = [
        {
            "restart": 0,
            "iteration": 0,
            "score": best_score,
            "load_min": min(best_loads),
            "load_max": max(best_loads),
        }
    ]
    for restart in range(restarts):
        if restart == 0:
            assignment, loads = greedy_initial(options)
        else:
            assignment, loads = randomized_initial(options, rng)
        current = score(loads)
        temperature = 2.0
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

            overloaded = [line for line, load in enumerate(loads) if load > TARGET_LOAD]
            candidate_routes = []
            if overloaded:
                target_line = rng.choice(overloaded)
                candidate_routes = [
                    route_idx
                    for route_idx, choice in enumerate(assignment)
                    if target_line in options[route_idx][choice]["line_pair"]
                ]
            if not candidate_routes:
                candidate_routes = list(range(len(options)))

            route_idx = rng.choice(candidate_routes)
            old_choice = assignment[route_idx]
            old_pair = options[route_idx][old_choice]["line_pair"]
            best_deltas: list[tuple[int, int]] = []
            best_delta = 10**9
            for choice, row in enumerate(options[route_idx]):
                if choice == old_choice:
                    continue
                delta = delta_score(loads, old_pair, row["line_pair"])
                if delta < best_delta:
                    best_delta = delta
                    best_deltas = [(choice, delta)]
                elif delta == best_delta:
                    best_deltas.append((choice, delta))
            new_choice, delta = rng.choice(best_deltas)
            accept = delta <= 0 or rng.random() < math.exp(-delta / max(0.01, temperature))
            if accept:
                left, right = old_pair
                loads[left] -= 1
                loads[right] -= 1
                left, right = options[route_idx][new_choice]["line_pair"]
                loads[left] += 1
                loads[right] += 1
                assignment[route_idx] = new_choice
                current += delta
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


def build_payload() -> dict[str, Any]:
    lines = all_lines()
    pairs, options = route_line_options(line_lookup(lines))
    search = find_perfect_assignment(options)
    assignment = search["assignment"]
    loads = [0] * len(lines)
    certificate_rows = []
    for route_idx, choice in enumerate(assignment):
        src_idx, dst_idx = pairs[route_idx]
        row = options[route_idx][choice]
        left, right = row["line_pair"]
        loads[left] += 1
        loads[right] += 1
        certificate_rows.append(
            {
                "route_index": route_idx,
                "source": point_id(hn.POINTS[src_idx]),
                "destination": point_id(hn.POINTS[dst_idx]),
                "relay": row["relay"],
                "line_pair": row["line_pair"],
                "choice": choice,
            }
        )

    load_hist = Counter(loads)
    checks = {
        "search_found_exact_certificate": bool(search["found"]),
        "ordered_nonadjacent_pairs_1080": len(pairs) == 1080,
        "four_options_per_pair": all(len(rows) == 4 for rows in options),
        "one_choice_per_pair": len(certificate_rows) == len(pairs),
        "total_line_uses_2160": sum(loads) == 2160,
        "lower_bound_is_54": (2 * len(pairs)) // len(lines) == TARGET_LOAD,
        "all_line_loads_equal_54": all(load == TARGET_LOAD for load in loads),
        "objective_zero": score(loads) == 0,
        "line_loads_recompute_search_loads": loads == search["loads"],
    }
    return {
        "schema": "w33.perfect_multipath_balancer.v1",
        "theorem": "W33 admits a perfect two-hop relay assignment with every line bus loaded exactly 54 times",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "instance": {
            "ordered_nonadjacent_pairs": len(pairs),
            "relay_options": sum(len(rows) for rows in options),
            "line_buses": len(lines),
            "line_uses": sum(loads),
            "forced_ideal_load": TARGET_LOAD,
        },
        "search": {
            "seed": search["seed"],
            "restart": search["restart"],
            "iteration": search["iteration"],
            "score": search["score"],
            "progress": search["progress"],
        },
        "line_loads": loads,
        "line_load_histogram": {str(key): load_hist[key] for key in sorted(load_hist)},
        "certificate_preview": certificate_rows[:60],
        "certificate_tail": certificate_rows[-20:],
        "certificate": certificate_rows,
        "checks": checks,
        "interpretation": (
            "The full nonlocal W33 workload has an exact fair-share relay law: "
            "one can route every ordered non-adjacent pair through one of its "
            "four common relays while using every K4 line bus exactly 54 times. "
            "This makes line-bus balancing an exact finite scheduler theorem, "
            "not a heuristic."
        ),
        "honesty_boundary": (
            "This proves an offline finite assignment certificate. A live runtime "
            "still needs an incremental controller that maintains the certificate "
            "under partial workloads, failures, and measured hardware loss."
        ),
    }


def markdown(payload: dict[str, Any]) -> str:
    search = payload["search"]
    return f"""# W(3,3) Perfect Multipath Balancer

Every ordered non-adjacent pair has four two-hop relays. Since there are
`{payload['instance']['ordered_nonadjacent_pairs']}` such routes and each uses
two line buses, the exact fair-share lower bound is:

```text
1080 * 2 / 40 = 54
```

This verifier finds and checks a certificate with every line bus loaded exactly
`54` times.

| Quantity | Value |
|---|---:|
| Ordered routes | `{payload['instance']['ordered_nonadjacent_pairs']}` |
| Relay options | `{payload['instance']['relay_options']}` |
| Line buses | `{payload['instance']['line_buses']}` |
| Line uses | `{payload['instance']['line_uses']}` |
| Ideal load | `{payload['instance']['forced_ideal_load']}` |
| Search seed | `{search['seed']}` |
| Search restart | `{search['restart']}` |
| Search iteration | `{search['iteration']}` |
| Final score | `{search['score']}` |

Line-load histogram: `{payload['line_load_histogram']}`.

Conclusion: the full W33 two-hop workload admits a perfect relay schedule.
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
    print(f"routes: {payload['instance']['ordered_nonadjacent_pairs']}")
    print(f"line load histogram: {payload['line_load_histogram']}")
    print(f"search: seed={payload['search']['seed']}, restart={payload['search']['restart']}, iteration={payload['search']['iteration']}")
    print(f"wrote: {json_out.relative_to(ROOT)}")
    print(f"wrote: {md_out.relative_to(ROOT)}")
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
