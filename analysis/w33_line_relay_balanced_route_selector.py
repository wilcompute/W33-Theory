#!/usr/bin/env python3
"""Line-and-relay balanced reversal-symmetric W33 route selector.

The prior reversal-symmetric selector proved the 135-byte runtime state:

    540 unordered nonlocal pairs * 2 bits = 135 bytes.

This verifier promotes the stronger certificate: the same 135-byte selector can
balance both the 40 line buses and the 40 relay cores.

Forced shares:

    line buses: 540 routes * 2 bus hits / 40 = 27 each.
    relay cores: 540 routes / 40 = 13.5, so the best integer split is
                 20 cores at 13 and 20 cores at 14.

The assignment below is a compact certificate.  The verifier regenerates the
W33 unordered nonlocal pair order and four relay choices, then checks the line
and relay histograms from scratch.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

import holonet_node as hn
from w33_component_execution_simulator import line_lookup
from w33_perfect_route_selector_runtime import direct_line_loads, pack_choices, unpack_choices
from w33_reversal_symmetric_route_selector import (
    TARGET_UNORDERED_LOAD,
    actual_line_pair,
    unordered_nonadjacent_options,
)
from w33_uor_runtime_model import ROOT, all_lines, point_id


DEFAULT_JSON = ROOT / "data" / "w33_line_relay_balanced_route_selector.json"
DEFAULT_MD = ROOT / "docs" / "w33_line_relay_balanced_route_selector.md"


EXACT_CHOICES = [
    1, 0, 3, 2, 2, 1, 3, 0, 0, 2, 2, 1, 1, 1, 1, 0, 3, 2, 3, 1, 2, 2, 1, 1,
    0, 0, 3, 3, 2, 1, 3, 0, 0, 2, 0, 3, 2, 2, 0, 3, 0, 1, 0, 2, 2, 1, 1, 1,
    1, 2, 0, 3, 2, 0, 2, 3, 1, 1, 3, 1, 2, 3, 1, 1, 0, 3, 1, 1, 3, 3, 0, 3,
    2, 1, 3, 3, 3, 2, 3, 3, 0, 2, 2, 1, 2, 1, 3, 3, 0, 0, 2, 3, 0, 0, 2, 2,
    3, 2, 0, 1, 2, 0, 3, 0, 3, 0, 0, 0, 1, 3, 1, 0, 2, 3, 2, 3, 1, 0, 3, 2,
    0, 1, 1, 1, 0, 3, 0, 0, 1, 1, 0, 3, 2, 0, 2, 3, 3, 1, 3, 2, 2, 2, 3, 1,
    2, 0, 0, 0, 2, 3, 2, 1, 3, 0, 0, 3, 3, 1, 3, 1, 1, 2, 0, 3, 0, 0, 3, 1,
    1, 3, 3, 0, 3, 0, 3, 0, 3, 1, 0, 0, 3, 0, 1, 1, 0, 1, 0, 1, 0, 2, 1, 3,
    3, 3, 2, 2, 3, 3, 2, 1, 3, 1, 2, 0, 1, 0, 0, 2, 3, 2, 3, 2, 3, 2, 1, 2,
    2, 1, 0, 2, 1, 2, 1, 1, 0, 1, 0, 1, 3, 1, 3, 2, 0, 2, 1, 3, 1, 3, 1, 3,
    2, 3, 1, 0, 3, 2, 1, 3, 3, 1, 1, 1, 1, 2, 3, 0, 0, 0, 0, 0, 1, 3, 1, 1,
    3, 2, 1, 2, 1, 3, 2, 0, 3, 0, 0, 0, 1, 1, 0, 0, 0, 0, 2, 3, 0, 1, 0, 2,
    0, 2, 0, 3, 3, 2, 1, 1, 3, 3, 2, 2, 1, 0, 2, 2, 2, 3, 2, 1, 2, 2, 2, 0,
    2, 1, 0, 3, 3, 3, 0, 1, 0, 3, 0, 0, 2, 1, 2, 1, 0, 2, 3, 0, 1, 3, 2, 0,
    3, 2, 2, 2, 0, 3, 3, 2, 2, 0, 1, 0, 3, 2, 2, 1, 3, 2, 2, 1, 3, 3, 1, 0,
    2, 3, 0, 3, 1, 3, 2, 3, 1, 0, 0, 0, 0, 2, 0, 0, 1, 2, 0, 2, 2, 3, 1, 3,
    0, 2, 3, 3, 0, 2, 3, 2, 0, 0, 0, 1, 1, 0, 2, 0, 3, 2, 2, 3, 0, 0, 0, 3,
    2, 2, 3, 1, 3, 1, 3, 2, 1, 0, 1, 0, 2, 0, 1, 2, 2, 0, 3, 0, 1, 3, 2, 3,
    0, 3, 1, 1, 3, 1, 1, 2, 3, 0, 2, 0, 2, 2, 1, 1, 3, 1, 2, 1, 1, 1, 0, 3,
    1, 2, 3, 2, 3, 3, 3, 1, 0, 1, 0, 2, 0, 0, 0, 3, 1, 1, 0, 0, 1, 3, 2, 1,
    0, 1, 0, 3, 0, 3, 3, 0, 1, 1, 0, 3, 1, 3, 1, 1, 3, 0, 2, 0, 2, 3, 2, 0,
    1, 3, 0, 1, 1, 0, 3, 1, 3, 2, 2, 3, 3, 3, 0, 2, 3, 0, 1, 0, 2, 1, 2, 0,
    0, 2, 0, 0, 3, 0, 3, 1, 3, 1, 2, 2,
]


REPAIR_FROM_NEAR_CERTIFICATE = [
    {"route": 122, "old": 2, "new": 1, "old_tuple": [12, 36, 11], "new_tuple": [4, 33, 10]},
    {"route": 196, "old": 0, "new": 3, "old_tuple": [4, 31, 10], "new_tuple": [22, 15, 38]},
    {"route": 93, "old": 3, "new": 0, "old_tuple": [15, 22, 38], "new_tuple": [12, 36, 11]},
]


def build_payload() -> dict[str, Any]:
    lines = all_lines()
    lookup = line_lookup(lines)
    pairs, options = unordered_nonadjacent_options(lookup)
    choices = list(EXACT_CHOICES)
    packed = pack_choices(choices)
    unpacked = unpack_choices(packed, len(choices))
    pair_to_route_index = {pair: idx for idx, pair in enumerate(pairs)}

    unordered_line_loads = [0] * len(lines)
    relay_loads = [0] * len(hn.POINTS)
    certificate_rows = []
    for route_idx, choice in enumerate(choices):
        src_idx, dst_idx = pairs[route_idx]
        row = options[route_idx][choice]
        for line_id in row["line_pair"]:
            unordered_line_loads[line_id] += 1
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
    ordered_nonlocal_loads = [2 * load for load in unordered_line_loads]
    full_loads = [
        direct + nonlocal_load for direct, nonlocal_load in zip(direct_loads, ordered_nonlocal_loads)
    ]
    reverse_ok = True
    reverse_rows: dict[tuple[int, int], dict[str, Any]] = {}
    for src_idx, src in enumerate(hn.POINTS):
        for dst_idx, dst in enumerate(hn.POINTS):
            if src_idx == dst_idx or hn.symplectic(src, dst) == 0:
                continue
            key = (src_idx, dst_idx) if src_idx < dst_idx else (dst_idx, src_idx)
            route_idx = pair_to_route_index[key]
            choice = choices[route_idx]
            relay_idx = int(options[route_idx][choice]["relay_index"])
            row = {
                "relay_index": relay_idx,
                "line_set": sorted(actual_line_pair(src_idx, relay_idx, dst_idx, lookup)),
            }
            rev = reverse_rows.get((dst_idx, src_idx))
            if rev and rev != row:
                reverse_ok = False
            reverse_rows[(src_idx, dst_idx)] = row

    checks = {
        "choice_count_540": len(choices) == 540,
        "packed_selector_135_bytes": len(packed) == 135,
        "pack_roundtrip": unpacked == choices,
        "all_choices_are_two_bit": all(0 <= choice < 4 for choice in choices),
        "unordered_line_loads_are_27_each": Counter(unordered_line_loads) == {27: 40},
        "relay_loads_are_forced_13_14_split": Counter(relay_loads) == {13: 20, 14: 20},
        "ordered_nonlocal_loads_are_54_each": Counter(ordered_nonlocal_loads) == {54: 40},
        "direct_loads_are_12_each": Counter(direct_loads) == {12: 40},
        "full_loads_are_66_each": Counter(full_loads) == {66: 40},
        "same_relay_under_route_reversal": reverse_ok,
        "fair_share_identities": (
            540 * 2 // 40 == TARGET_UNORDERED_LOAD
            and 540 // 40 == 13
            and 540 % 40 == 20
        ),
    }
    return {
        "schema": "w33.line_relay_balanced_route_selector.v1",
        "theorem": "A 135-byte W33 selector balances both line buses and relay cores",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "storage": {
            "unordered_choice_count": len(choices),
            "choice_bits": 2 * len(choices),
            "choice_bytes": len(packed),
            "packed_choice_preview": packed[:32],
            "previous_ordered_selector_bytes": 270,
            "bytes_saved_vs_ordered_selector": 135,
            "full_next_hop_table_bytes": 1600,
            "bytes_saved_vs_full_table": 1465,
        },
        "line_loads": {
            "unordered_nonlocal": unordered_line_loads,
            "ordered_nonlocal": ordered_nonlocal_loads,
            "direct": direct_loads,
            "full_nonidentity": full_loads,
            "unordered_histogram": {str(k): v for k, v in sorted(Counter(unordered_line_loads).items())},
            "ordered_nonlocal_histogram": {
                str(k): v for k, v in sorted(Counter(ordered_nonlocal_loads).items())
            },
            "direct_histogram": {str(k): v for k, v in sorted(Counter(direct_loads).items())},
            "full_histogram": {str(k): v for k, v in sorted(Counter(full_loads).items())},
        },
        "relay_core_usage": {
            "loads": relay_loads,
            "histogram": {str(k): v for k, v in sorted(Counter(relay_loads).items())},
            "average": sum(relay_loads) / len(relay_loads),
            "forced_integer_split": {"13": 20, "14": 20},
            "status": "balanced",
        },
        "selector": {
            "pair_order": "generated unordered non-adjacent W33 pairs from projective point order",
            "choice_encoding": "two bits per unordered nonlocal pair; both directions share the relay",
            "packed_bytes": packed,
        },
        "repair_note": {
            "from_near_certificate": "line-perfect frontier was repaired by a 3-move cycle preserving relay counts",
            "moves": REPAIR_FROM_NEAR_CERTIFICATE,
        },
        "certificate_preview": certificate_rows[:60],
        "certificate_tail": certificate_rows[-20:],
        "certificate": certificate_rows,
        "checks": checks,
        "interpretation": (
            "The W33 nonlocal router has a dual fair-share law.  As an unordered "
            "time-reversal quotient, 540 routes use every line exactly 27 times "
            "and use relay points in the forced 13/14 split.  Expanding both "
            "time directions gives the earlier 54 nonlocal line law; direct "
            "incidence then closes the h=6 value 66."
        ),
        "honesty_boundary": (
            "This is an exact finite certificate for balanced runtime state.  It "
            "still does not provide a closed-form equivariant formula for the "
            "540 two-bit choices."
        ),
    }


def markdown(payload: dict[str, Any]) -> str:
    return f"""# W(3,3) Line-and-Relay Balanced Route Selector

The reversal-symmetric selector can balance both physical resources:

```text
540 unordered nonlocal routes * 2 line hits / 40 lines = 27 per line
540 unordered nonlocal routes / 40 relay cores = 13.5
```

Since relay hits are integral, the best possible relay distribution is
`20` cores at `13` and `20` cores at `14`.  The verifier finds exactly that.

| Resource | Histogram |
|---|---|
| Unordered line buses | `{payload['line_loads']['unordered_histogram']}` |
| Relay cores | `{payload['relay_core_usage']['histogram']}` |
| Ordered nonlocal line buses | `{payload['line_loads']['ordered_nonlocal_histogram']}` |
| Full all-pairs line buses | `{payload['line_loads']['full_histogram']}` |

Storage remains `135` bytes:

```text
540 choices * 2 bits = 1080 bits = 135 bytes
```

The full line-load law is still:

```text
66 = 12 + 2*27
```

Interpretation: W33 routing has a time-reversal quotient that balances wires,
and the same quotient can balance relay cores at the forced integer fair-share
split.  This is the current best compact runtime object.

Boundary: this is a finite certificate, not yet a closed-form group-equivariant
formula for the choice vector.
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
    print(f"line histogram: {payload['line_loads']['unordered_histogram']}")
    print(f"relay histogram: {payload['relay_core_usage']['histogram']}")
    print(f"full line histogram: {payload['line_loads']['full_histogram']}")
    print(f"wrote: {json_out.relative_to(ROOT)}")
    print(f"wrote: {md_out.relative_to(ROOT)}")
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
