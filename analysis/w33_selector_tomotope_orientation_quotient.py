#!/usr/bin/env python3
"""Orientation quotient bridge between the W33 selector and Q6/tomotope slots.

The balanced selector exposes a clean count ladder:

    135 bytes -> 540 unordered routes -> 1080 ordered routes -> 2160 mirror slots.

The Q6/tomotope ABI already carries the same 2160 as

    45 polar sheets * 48 tomotope body slots.

This verifier records the exact factor alignment while keeping the boundary
honest: count compatibility is not yet an objectwise isomorphism of actions.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from w33_line_relay_balanced_route_selector import (
    DEFAULT_JSON as DEFAULT_SELECTOR_JSON,
    build_payload as build_selector_payload,
)
from w33_q6_tomotope_recursive_packet_abi import (
    DEFAULT_JSON as DEFAULT_Q6_JSON,
    build_payload as build_q6_payload,
)
from w33_uor_runtime_model import ROOT


DEFAULT_JSON = ROOT / "data" / "w33_selector_tomotope_orientation_quotient.json"
DEFAULT_MD = ROOT / "docs" / "w33_selector_tomotope_orientation_quotient.md"


def load_or_build(path: Path, builder) -> dict[str, Any]:
    if path.exists():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            if data.get("status") == "PASS":
                return data
        except json.JSONDecodeError:
            pass
    return builder()


def build_payload() -> dict[str, Any]:
    selector = load_or_build(DEFAULT_SELECTOR_JSON, build_selector_payload)
    q6 = load_or_build(DEFAULT_Q6_JSON, build_q6_payload)

    selector_bytes = int(selector["storage"]["choice_bytes"])
    unordered_routes = int(selector["storage"]["unordered_choice_count"])
    ordered_routes = 2 * unordered_routes
    mirror_slots = int(q6["local_abi"]["mirror_slots"])
    tomotope_body = int(q6["local_abi"]["tomotope_packet_blocks"])
    body_edges = int(q6["local_abi"]["q6_body_edges"])
    body_phases = int(q6["local_abi"]["body_pulse_phases"])
    polar_sheets = mirror_slots // tomotope_body

    ladder = {
        "selector_byte_planes": selector_bytes,
        "unordered_route_choices": unordered_routes,
        "ordered_route_choices": ordered_routes,
        "tomotope_mirror_slots": mirror_slots,
        "polar_sheets": polar_sheets,
        "tomotope_body_slots": tomotope_body,
        "q6_body_edges": body_edges,
        "body_pulse_phases": body_phases,
    }
    factorizations = {
        "selector_bytes": "135 = 45 * 3",
        "unordered_routes": "540 = 135 * 4 = 45 * 12",
        "ordered_routes": "1080 = 2 * 540 = 45 * 24",
        "mirror_slots": "2160 = 4 * 540 = 2 * 1080 = 16 * 135 = 45 * 48",
        "tomotope_body": "48 = 16 * 3",
    }
    checks = {
        "selector_pass": selector["status"] == "PASS",
        "q6_pass": q6["status"] == "PASS",
        "selector_bytes_135": selector_bytes == 135,
        "unordered_routes_540": unordered_routes == 540,
        "ordered_routes_1080": ordered_routes == 1080,
        "tomotope_body_48": tomotope_body == 48,
        "q6_body_identity_16_times_3": body_edges * body_phases == tomotope_body,
        "mirror_slots_2160": mirror_slots == 2160,
        "polar_sheet_factor_45": polar_sheets == 45,
        "selector_to_unordered_four_choices_per_byte": selector_bytes * 4 == unordered_routes,
        "unordered_to_ordered_time_reversal_double": unordered_routes * 2 == ordered_routes,
        "ordered_to_mirror_polar_double": ordered_routes * 2 == mirror_slots,
        "selector_bytes_to_mirror_16x": selector_bytes * 16 == mirror_slots,
        "polar_sheet_times_tomotope_body": polar_sheets * tomotope_body == mirror_slots,
    }
    return {
        "schema": "w33.selector_tomotope_orientation_quotient.v1",
        "theorem": "the 135-byte selector sits on the same 2160 orientation ladder as the Q6/tomotope ABI",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "ladder": ladder,
        "factorizations": factorizations,
        "checks": checks,
        "interpretation": (
            "The runtime selector, time reversal, and tomotope mirror ABI form one count "
            "ladder.  A selector byte packs four two-bit route choices; adding route "
            "orientation doubles 540 to 1080; adding the mirror/polar orientation doubles "
            "again to 2160, exactly the Q6/tomotope 45*48 mirror-slot count."
        ),
        "honesty_boundary": (
            "This is a verified factor and quotient alignment.  It does not yet prove an "
            "equivariant isomorphism between W33 route slots and tomotope flag symmetries."
        ),
    }


def markdown(payload: dict[str, Any]) -> str:
    facts = payload["factorizations"]
    ladder = payload["ladder"]
    return f"""# W(3,3) Selector / Tomotope Orientation Quotient

The balanced selector and the Q6/tomotope ABI share a single orientation ladder:

```text
{facts['selector_bytes']}
{facts['unordered_routes']}
{facts['ordered_routes']}
{facts['mirror_slots']}
{facts['tomotope_body']}
```

| Layer | Count |
|---|---:|
| Selector bytes | `{ladder['selector_byte_planes']}` |
| Unordered route choices | `{ladder['unordered_route_choices']}` |
| Ordered route choices | `{ladder['ordered_route_choices']}` |
| Tomotope mirror slots | `{ladder['tomotope_mirror_slots']}` |
| Polar sheets | `{ladder['polar_sheets']}` |
| Tomotope body slots | `{ladder['tomotope_body_slots']}` |

Interpretation: one selector byte stores four two-bit route choices.  Time
orientation doubles `540` to `1080`; mirror/polar orientation doubles again to
`2160 = 45 * 48`, the Q6/tomotope mirror-slot count.

Boundary: this proves a quotient/factor alignment.  The next target is an
actual equivariant map between route slots and tomotope flag symmetries.
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
    print(f"ladder: {payload['ladder']}")
    print(f"wrote: {args.json_out}")
    print(f"wrote: {args.md_out}")
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
