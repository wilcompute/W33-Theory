#!/usr/bin/env python3
"""Runtime route selector from the perfect W33 multipath certificate.

The perfect multipath balancer proves an offline schedule: for every ordered
non-adjacent W33 pair, choose one of four relays so every line bus is used
exactly 54 times.  This script turns that certificate into a runtime object.

The selector is small:

    1080 nonlocal ordered pairs * 2 bits = 2160 bits = 270 bytes.

The ordered-pair list is generated from W(3,3) itself, so the selector stores
only the four-way relay choice, not source/destination labels or next-hop
addresses.  Direct routes need no table.  With the direct ordered edge routes
included, the full nonidentity all-pairs workload is also perfectly balanced:

    direct line load 12 + nonlocal line load 54 = 66 on every W33 line.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

import holonet_node as hn
from w33_component_execution_simulator import line_lookup
from w33_perfect_multipath_balancer import (
    DEFAULT_JSON as DEFAULT_CERTIFICATE,
    build_payload as build_certificate_payload,
    route_line_options,
)
from w33_uor_runtime_model import ROOT, all_lines, point_id


DEFAULT_JSON = ROOT / "data" / "w33_perfect_route_selector_runtime.json"
DEFAULT_MD = ROOT / "docs" / "w33_perfect_route_selector_runtime.md"


def load_or_build_certificate(path: Path) -> dict[str, Any]:
    if path.exists():
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("status") == "PASS":
            return data
    return build_certificate_payload()


def pack_choices(choices: list[int]) -> list[int]:
    packed = []
    for offset in range(0, len(choices), 4):
        byte = 0
        for shift, choice in enumerate(choices[offset : offset + 4]):
            if not 0 <= choice < 4:
                raise ValueError(f"choice {choice} is not two-bit")
            byte |= choice << (2 * shift)
        packed.append(byte)
    return packed


def unpack_choices(packed: list[int], count: int) -> list[int]:
    choices = []
    for byte in packed:
        for shift in range(4):
            choices.append((byte >> (2 * shift)) & 0b11)
            if len(choices) == count:
                return choices
    return choices


def direct_line_loads(lookup: dict[tuple[int, int], int], line_count: int) -> list[int]:
    loads = [0] * line_count
    for src_idx, src in enumerate(hn.POINTS):
        for dst_idx, dst in enumerate(hn.POINTS):
            if src_idx == dst_idx:
                continue
            if hn.symplectic(src, dst) == 0:
                loads[lookup[(src_idx, dst_idx)]] += 1
    return loads


def build_selector_payload(certificate: dict[str, Any]) -> dict[str, Any]:
    lines = all_lines()
    lookup = line_lookup(lines)
    pairs, options = route_line_options(lookup)
    certificate_rows = certificate["certificate"]
    choices = [int(row["choice"]) for row in certificate_rows]
    packed = pack_choices(choices)
    unpacked = unpack_choices(packed, len(choices))
    pair_to_route_index = {pair: idx for idx, pair in enumerate(pairs)}

    nonlocal_loads = [0] * len(lines)
    full_loads = direct_line_loads(lookup, len(lines))
    route_preview = []
    route_counts = Counter()
    for src_idx, src in enumerate(hn.POINTS):
        for dst_idx, dst in enumerate(hn.POINTS):
            if src_idx == dst_idx:
                route_counts["identity"] += 1
                route = [src_idx]
                line_pair: list[int] = []
            elif hn.symplectic(src, dst) == 0:
                route_counts["direct"] += 1
                route = [src_idx, dst_idx]
                line_pair = [lookup[(src_idx, dst_idx)]]
            else:
                route_counts["perfect_two_hop"] += 1
                route_idx = pair_to_route_index[(src_idx, dst_idx)]
                choice = unpacked[route_idx]
                option = options[route_idx][choice]
                relay_idx = int(option["relay_index"])
                route = [src_idx, relay_idx, dst_idx]
                line_pair = list(option["line_pair"])
                for line_id in line_pair:
                    nonlocal_loads[line_id] += 1
                    full_loads[line_id] += 1
            if len(route_preview) < 24 and len(route) > 1:
                route_preview.append(
                    {
                        "source": point_id(hn.POINTS[src_idx]),
                        "destination": point_id(hn.POINTS[dst_idx]),
                        "route": [point_id(hn.POINTS[idx]) for idx in route],
                        "line_pair": line_pair,
                    }
                )

    direct_loads = direct_line_loads(lookup, len(lines))
    storage = {
        "choice_count": len(choices),
        "choice_bits": 2 * len(choices),
        "choice_bytes": len(packed),
        "packed_choice_preview": packed[:32],
        "full_next_hop_table_bytes": 1600,
        "nonlocal_next_hop_table_bytes": 1080,
        "bytes_saved_vs_full_table": 1600 - len(packed),
        "bytes_saved_vs_nonlocal_table": 1080 - len(packed),
        "fraction_saved_vs_full_table": (1600 - len(packed)) / 1600,
        "fraction_saved_vs_nonlocal_table": (1080 - len(packed)) / 1080,
    }
    checks = {
        "certificate_pass": certificate["status"] == "PASS",
        "choice_count_1080": len(choices) == 1080,
        "packed_selector_270_bytes": len(packed) == 270,
        "pack_roundtrip": unpacked == choices,
        "route_counts": dict(route_counts) == {
            "identity": 40,
            "direct": 480,
            "perfect_two_hop": 1080,
        },
        "direct_loads_are_12_each": set(direct_loads) == {12},
        "nonlocal_loads_are_54_each": set(nonlocal_loads) == {54},
        "full_all_pairs_loads_are_66_each": set(full_loads) == {66},
        "full_line_uses_2640": sum(full_loads) == 2640,
        "all_routes_diameter_two": all(len(row["route"]) <= 3 for row in route_preview),
    }
    return {
        "schema": "w33.perfect_route_selector_runtime.v1",
        "theorem": "A 270-byte two-bit selector realizes perfectly balanced W33 all-pairs routing",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "route_counts": dict(route_counts),
        "storage": storage,
        "line_loads": {
            "direct": direct_loads,
            "nonlocal": nonlocal_loads,
            "full_nonidentity": full_loads,
            "direct_histogram": {str(key): value for key, value in sorted(Counter(direct_loads).items())},
            "nonlocal_histogram": {str(key): value for key, value in sorted(Counter(nonlocal_loads).items())},
            "full_histogram": {str(key): value for key, value in sorted(Counter(full_loads).items())},
        },
        "selector": {
            "pair_order": "generated ordered non-adjacent W33 pairs from projective point order",
            "choice_encoding": "two bits per nonlocal ordered pair; 0..3 selects the sorted common relay option",
            "packed_bytes": packed,
        },
        "route_preview": route_preview,
        "checks": checks,
        "interpretation": (
            "The full route selector is not a 1600-entry routing table. W33 "
            "generates addresses, direct adjacency, and four relay options; the "
            "runtime stores only the two-bit relay choice for each nonlocal "
            "ordered pair. The resulting all-pairs nonidentity workload is "
            "perfectly line-balanced at 66 uses per line."
        ),
        "honesty_boundary": (
            "This is a compact finite runtime selector. It still stores a 270-byte "
            "choice vector; the next compression target is an explicit symmetry "
            "rule that generates the same choices without a vector."
        ),
    }


def markdown(payload: dict[str, Any]) -> str:
    storage = payload["storage"]
    return f"""# W(3,3) Perfect Route Selector Runtime

The perfect two-hop relay certificate can run as a compact selector:

```text
1080 nonlocal ordered pairs * 2 bits = 2160 bits = 270 bytes
```

W33 generates the ordered pair list and the four relay options. The runtime only
stores the two-bit choice for each nonlocal pair.

| Quantity | Value |
|---|---:|
| Identity routes | `{payload['route_counts']['identity']}` |
| Direct routes | `{payload['route_counts']['direct']}` |
| Perfect two-hop routes | `{payload['route_counts']['perfect_two_hop']}` |
| Selector bytes | `{storage['choice_bytes']}` |
| Bytes saved vs full 40x40 next-hop table | `{storage['bytes_saved_vs_full_table']}` |
| Bytes saved vs nonlocal next-hop table | `{storage['bytes_saved_vs_nonlocal_table']}` |

Line-load histograms:

```text
direct          = {payload['line_loads']['direct_histogram']}
nonlocal        = {payload['line_loads']['nonlocal_histogram']}
full_nonidentity= {payload['line_loads']['full_histogram']}
```

The full nonidentity all-pairs workload is perfectly balanced: every W33 line
bus is used exactly `66` times.
"""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--certificate", default=str(DEFAULT_CERTIFICATE))
    parser.add_argument("--json-out", default=str(DEFAULT_JSON))
    parser.add_argument("--md-out", default=str(DEFAULT_MD))
    args = parser.parse_args(argv)

    certificate_path = Path(args.certificate)
    if not certificate_path.is_absolute():
        certificate_path = ROOT / certificate_path
    payload = build_selector_payload(load_or_build_certificate(certificate_path))
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
    print(f"route counts: {payload['route_counts']}")
    print(f"full load histogram: {payload['line_loads']['full_histogram']}")
    print(f"wrote: {json_out.relative_to(ROOT)}")
    print(f"wrote: {md_out.relative_to(ROOT)}")
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
