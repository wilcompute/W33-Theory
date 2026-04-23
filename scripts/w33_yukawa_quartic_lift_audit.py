#!/usr/bin/env python3
"""Exact quartic-lift audit for the residual Yukawa packet."""

from __future__ import annotations

from functools import lru_cache
import json
from pathlib import Path
import sys
import time
from typing import Dict


ROOT = Path(__file__).resolve().parents[1]
EXPLORATION = ROOT / "exploration"
for candidate in (ROOT, EXPLORATION):
    candidate_str = str(candidate)
    if candidate_str not in sys.path:
        sys.path.insert(0, candidate_str)

from w33_yukawa_quartic_lift_bridge import (  # noqa: E402
    build_yukawa_quartic_lift_summary,
)


@lru_cache(maxsize=1)
def analyze() -> Dict[str, object]:
    payload = build_yukawa_quartic_lift_summary()
    records = payload["quartic_lift_packet"]["records"]
    payload["quartic_record_names"] = tuple(records)
    return payload


def main() -> None:
    started = time.time()
    payload = analyze()
    payload["analysis_duration_sec"] = round(time.time() - started, 6)

    output_dir = ROOT / "checks"
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    output_path = output_dir / f"PART_CXII_exact_yukawa_quartic_lift_audit_{timestamp}.json"
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    records = payload["quartic_lift_packet"]["records"]
    mixed = payload["mixed_positive_root_relation"]

    print("Exact Yukawa quartic lift audit")
    print(
        "  Variables: "
        f"{payload['quartic_lift_packet']['scaled_signed_variable']}, "
        f"{payload['quartic_lift_packet']['scaled_squared_variable']}"
    )
    for name, record in records.items():
        print(
            f"  {name}: {record['quartic_polynomial']} "
            f"({record['galois_group_label']}, order {record['galois_group_order']})"
        )
    print(
        "  Quadratic overlap: "
        f"{payload['quartic_pair_relation']['shared_quadratic_subfield_squarefree_parts']}"
    )
    print(
        "  Root-field compositum degree: "
        f"{payload['quartic_root_field_relation']['compositum_degree']}"
    )
    print(
        "  Splitting-field compositum degree: "
        f"{payload['quartic_splitting_field_relation']['compositum_degree']}"
    )
    print(
        "  Splitting-field Galois group: "
        f"{payload['quartic_splitting_field_relation']['compositum_galois_group']}"
    )
    print(
        "  Mixed product/ratio degrees: "
        f"{mixed['product_packet']['degree']}, {mixed['ratio_packet']['degree']}"
    )
    print(
        "  Mixed squared product/ratio degrees: "
        f"{mixed['product_squared_packet']['degree']}, {mixed['ratio_squared_packet']['degree']}"
    )
    print(
        "  Mixed sum degree: "
        f"{mixed['sum_packet']['degree']}"
    )
    print("  Signed packet: two exact D4 quartic lifts")
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()