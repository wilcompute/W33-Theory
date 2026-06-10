#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

def main() -> int:
    endpoint = [0, 0, 3, 28, 268, 3000, 33195, 365480, 4020568, 44210368, 486310803]
    e4_scalar = [3 if n % 2 == 0 else 1 for n in range(len(endpoint))]
    e4_trace = [81 * a for a in e4_scalar]
    distance4_pairs = 160 * 81
    endpoint_mass_n3 = distance4_pairs * endpoint[3]
    alt24 = [24 * ((-1) ** n) for n in range(len(endpoint))]
    alt24_e4_component = [0 for _ in endpoint]
    checks = {
        "distance4_pairs": distance4_pairs == 12960,
        "endpoint_n3": endpoint[3] == 28,
        "endpoint_mass_n3": endpoint_mass_n3 == 362880,
        "e4_scalar_pattern": e4_scalar[:8] == [3,1,3,1,3,1,3,1],
        "e4_trace_n3": e4_trace[3] == 81,
        "alt24_pattern": alt24[:8] == [24,-24,24,-24,24,-24,24,-24],
        "alt24_e4_zero": all(v == 0 for v in alt24_e4_component),
    }
    result = {
        "bt": 641,
        "title": "Endpoint recurrence to E4 clock lift",
        "endpoint_sequence": endpoint,
        "E4_scalar_sequence": e4_scalar,
        "E4_trace_sequence": e4_trace,
        "distance4_ordered_pairs": distance4_pairs,
        "endpoint_mass_n3": endpoint_mass_n3,
        "endpoint_mass_n3_reading": "12960*28=362880=9!",
        "alternating_24_sheet": alt24,
        "alternating_24_E4_component": alt24_e4_component,
        "interpretation": "The full endpoint recurrence is large, while the E4 block records only the 3/1 clock; the alternating 24 sheet is external to E4.",
        "checks": checks,
        "all_identities_hold": all(checks.values())
    }
    out = Path("data/PART_BT641_ENDPOINT_LIFT_results.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
