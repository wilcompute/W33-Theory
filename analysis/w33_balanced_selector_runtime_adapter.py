#!/usr/bin/env python3
"""Runtime adapter for the 135-byte balanced W33 route selector.

The earlier perfect runtime selector stored one two-bit choice for each ordered
nonlocal pair: 270 bytes.  The line-and-relay balanced selector stores one
choice for each unordered nonlocal pair: 135 bytes.  This file exposes that
selector as a route API.

Direct routes are generated from W(3,3) incidence.  Nonlocal routes use the
same relay in both time directions, so route reversal is built into the runtime
contract rather than patched afterward.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

import holonet_node as hn
from w33_component_execution_simulator import line_lookup
from w33_line_relay_balanced_route_selector import (
    DEFAULT_JSON as DEFAULT_SELECTOR_JSON,
    build_payload as build_selector_payload,
)
from w33_reversal_symmetric_route_selector import unordered_nonadjacent_options
from w33_uor_runtime_model import ROOT, all_lines, point_id


DEFAULT_JSON = ROOT / "data" / "w33_balanced_selector_runtime_adapter.json"
DEFAULT_MD = ROOT / "docs" / "w33_balanced_selector_runtime_adapter.md"


def load_or_build_selector(path: Path) -> dict[str, Any]:
    if path.exists():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            if data.get("status") == "PASS":
                return data
        except json.JSONDecodeError:
            pass
    return build_selector_payload()


def selector_runtime(selector: dict[str, Any]) -> dict[str, Any]:
    lines = all_lines()
    lookup = line_lookup(lines)
    pairs, options = unordered_nonadjacent_options(lookup)
    choices = [int(row["choice"]) for row in selector["certificate"]]
    pair_to_route_index = {pair: idx for idx, pair in enumerate(pairs)}
    return {
        "lines": lines,
        "lookup": lookup,
        "pairs": pairs,
        "options": options,
        "choices": choices,
        "pair_to_route_index": pair_to_route_index,
    }


def balanced_route(
    src_idx: int, dst_idx: int, runtime: dict[str, Any]
) -> tuple[list[int], list[int], int | None]:
    """Return the W33 route, line IDs, and relay index for a point pair."""

    if src_idx == dst_idx:
        return [src_idx], [], None

    src = hn.POINTS[src_idx]
    dst = hn.POINTS[dst_idx]
    lookup = runtime["lookup"]
    if hn.symplectic(src, dst) == 0:
        return [src_idx, dst_idx], [lookup[(src_idx, dst_idx)]], None

    key = (src_idx, dst_idx) if src_idx < dst_idx else (dst_idx, src_idx)
    route_index = runtime["pair_to_route_index"][key]
    choice = runtime["choices"][route_index]
    option = runtime["options"][route_index][choice]
    relay_idx = int(option["relay_index"])
    return (
        [src_idx, relay_idx, dst_idx],
        [lookup[(src_idx, relay_idx)], lookup[(relay_idx, dst_idx)]],
        relay_idx,
    )


def build_payload() -> dict[str, Any]:
    selector = load_or_build_selector(DEFAULT_SELECTOR_JSON)
    runtime = selector_runtime(selector)
    route_counts = Counter()
    nonlocal_line_loads = Counter()
    direct_line_loads = Counter()
    full_line_loads = Counter()
    relay_loads_unordered = Counter()
    reversal_ok = True
    route_preview = []

    unordered_seen = set()
    for src_idx, src in enumerate(hn.POINTS):
        for dst_idx, dst in enumerate(hn.POINTS):
            route, line_ids, relay_idx = balanced_route(src_idx, dst_idx, runtime)
            if src_idx == dst_idx:
                route_counts["identity"] += 1
            elif hn.symplectic(src, dst) == 0:
                route_counts["direct"] += 1
                direct_line_loads.update(line_ids)
                full_line_loads.update(line_ids)
            else:
                route_counts["reversal_symmetric_two_hop"] += 1
                nonlocal_line_loads.update(line_ids)
                full_line_loads.update(line_ids)
                key = tuple(sorted((src_idx, dst_idx)))
                if key not in unordered_seen:
                    unordered_seen.add(key)
                    relay_loads_unordered.update([relay_idx])
                reverse_route, reverse_lines, reverse_relay = balanced_route(dst_idx, src_idx, runtime)
                if reverse_relay != relay_idx or sorted(reverse_lines) != sorted(line_ids):
                    reversal_ok = False

            if len(route_preview) < 24 and len(route) > 1:
                route_preview.append(
                    {
                        "source": point_id(hn.POINTS[src_idx]),
                        "destination": point_id(hn.POINTS[dst_idx]),
                        "route": [point_id(hn.POINTS[idx]) for idx in route],
                        "line_ids": line_ids,
                        "relay_index": relay_idx,
                    }
                )

    checks = {
        "selector_pass": selector["status"] == "PASS",
        "choice_count_540": len(runtime["choices"]) == 540,
        "choice_bytes_135": selector["storage"]["choice_bytes"] == 135,
        "route_counts": dict(route_counts) == {
            "identity": 40,
            "direct": 480,
            "reversal_symmetric_two_hop": 1080,
        },
        "direct_loads_are_12_each": Counter(direct_line_loads.values()) == {12: 40},
        "ordered_nonlocal_loads_are_54_each": Counter(nonlocal_line_loads.values()) == {54: 40},
        "full_loads_are_66_each": Counter(full_line_loads.values()) == {66: 40},
        "relay_loads_for_unordered_layer_are_13_14": Counter(relay_loads_unordered.values())
        == {13: 20, 14: 20},
        "same_relay_under_route_reversal": reversal_ok,
        "all_routes_have_diameter_at_most_two": all(
            len(row["route"]) <= 3 for row in route_preview
        ),
    }
    return {
        "schema": "w33.balanced_selector_runtime_adapter.v1",
        "theorem": "the 135-byte balanced selector is a runtime route adapter",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "route_counts": dict(route_counts),
        "storage": {
            "choice_count": len(runtime["choices"]),
            "choice_bytes": selector["storage"]["choice_bytes"],
            "choice_bits": selector["storage"]["choice_bits"],
            "full_next_hop_table_bytes": 1600,
            "bytes_saved_vs_full_table": 1600 - selector["storage"]["choice_bytes"],
            "bytes_saved_vs_ordered_selector": selector["storage"][
                "bytes_saved_vs_ordered_selector"
            ],
        },
        "line_loads": {
            "direct_histogram": {
                str(k): v for k, v in sorted(Counter(direct_line_loads.values()).items())
            },
            "ordered_nonlocal_histogram": {
                str(k): v for k, v in sorted(Counter(nonlocal_line_loads.values()).items())
            },
            "full_histogram": {
                str(k): v for k, v in sorted(Counter(full_line_loads.values()).items())
            },
        },
        "relay_usage": {
            "unordered_histogram": {
                str(k): v for k, v in sorted(Counter(relay_loads_unordered.values()).items())
            },
            "boundary": "relay balancing is counted on the unordered nonlocal layer",
        },
        "route_preview": route_preview,
        "checks": checks,
        "interpretation": (
            "The runtime can keep the generated W33 address/incidence machinery and replace "
            "the ordered 270-byte selector with one 135-byte reversal-symmetric selector. "
            "Direct routes need no state; nonlocal routes share one relay in both time directions."
        ),
        "honesty_boundary": (
            "This adapter still executes on a classical host in the verifier.  It specifies "
            "the finite routing ABI for a Holonet VM node, not a hardware speedup by itself."
        ),
    }


def markdown(payload: dict[str, Any]) -> str:
    storage = payload["storage"]
    return f"""# W(3,3) Balanced Selector Runtime Adapter

The line-and-relay balanced selector is now exposed as a route API.

```text
540 unordered nonlocal pairs * 2 bits = 135 bytes
```

Direct W33 routes are generated from the symplectic adjacency law.  Nonlocal
routes use the same relay in both directions, so reversal symmetry is part of
the ABI.

| Quantity | Value |
|---|---:|
| Selector bytes | `{storage['choice_bytes']}` |
| Bytes saved vs full table | `{storage['bytes_saved_vs_full_table']}` |
| Identity routes | `{payload['route_counts']['identity']}` |
| Direct routes | `{payload['route_counts']['direct']}` |
| Two-hop routes | `{payload['route_counts']['reversal_symmetric_two_hop']}` |

Load histograms:

```text
direct          = {payload['line_loads']['direct_histogram']}
ordered nonlocal= {payload['line_loads']['ordered_nonlocal_histogram']}
full            = {payload['line_loads']['full_histogram']}
relay unordered = {payload['relay_usage']['unordered_histogram']}
```

Boundary: this is a routing ABI and verifier, not a claim that the host CPU gets
quantum speedup merely by running the Python adapter.
"""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json-out", default=str(DEFAULT_JSON))
    parser.add_argument("--md-out", default=str(DEFAULT_MD))
    args = parser.parse_args(argv)

    payload = build_payload()
    Path(args.json_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.json_out).write_text(json.dumps(payload, indent=2), encoding="utf-8")
    Path(args.md_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.md_out).write_text(markdown(payload), encoding="utf-8")

    print(f"status: {payload['status']}")
    print(f"selector bytes: {payload['storage']['choice_bytes']}")
    print(f"route counts: {payload['route_counts']}")
    print(f"full line histogram: {payload['line_loads']['full_histogram']}")
    print(f"wrote: {args.json_out}")
    print(f"wrote: {args.md_out}")
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
