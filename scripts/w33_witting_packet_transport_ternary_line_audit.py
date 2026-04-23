#!/usr/bin/env python3
"""Exact ternary-line audit for the Witting packet transport shadow.

This chains the packet-side transport path-groupoid result to the exact
ternary homological code already present on W33:

1. the packet-side mod-3 transport shadow has a unique invariant line;
2. the W33 ternary homological CSS code has exactly 81 logical qutrits;
3. tensoring them gives a canonical 81-dimensional packet-transport-stable
   matter sector;
4. keeping the full reduced A2 fiber gives 162, matching the exact internal
   dimension already present in the finite spectral-action layer.
"""

from __future__ import annotations

from functools import lru_cache
import json
from pathlib import Path
import sys
import time
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
for candidate in (ROOT, ROOT / "scripts", ROOT / "exploration", ROOT / "pillars"):
    candidate_str = str(candidate)
    if candidate_str not in sys.path:
        sys.path.insert(0, candidate_str)

from exploration.w33_flat_ac_spectral_action import build_flat_product_summary  # noqa: E402
from exploration.w33_ternary_homological_code_bridge import build_ternary_homological_code_summary  # noqa: E402
from scripts.w33_witting_packet_transport_path_groupoid_audit import analyze as path_groupoid_analyze  # noqa: E402


@lru_cache(maxsize=1)
def analyze() -> dict[str, Any]:
    transport = path_groupoid_analyze()
    ternary = build_ternary_homological_code_summary()
    flat = build_flat_product_summary()

    logical_qutrits = ternary["ternary_css_code"]["logical_qutrits"]
    invariant_line_rank = transport["ternary_reduction"]["common_fixed_subspace_dimension"]
    full_reduced_fiber_rank = 2
    canonical_sector_dimension = logical_qutrits * invariant_line_rank
    matter_flavour_dimension = logical_qutrits * full_reduced_fiber_rank
    internal_dimension = flat["coefficients"]["internal_dimension"]

    theorem = {
        "the_packet_transport_shadow_has_a_unique_ternary_invariant_line": (
            transport["real_local_system"]["common_fixed_subspace_dimension"] == 0
            and transport["ternary_reduction"]["common_fixed_subspace_dimension"] == 1
            and transport["ternary_reduction"]["unique_invariant_projective_line"] == [1, 2]
        ),
        "the_w33_ternary_homological_code_has_exactly_81_logical_qutrits": (
            ternary["ternary_css_code"]["field"] == "F3"
            and logical_qutrits == 81
        ),
        "tensoring_the_packet_transport_line_with_the_homological_code_gives_a_canonical_81dimensional_sector": (
            canonical_sector_dimension == 81
        ),
        "keeping_the_full_reduced_a2_fiber_gives_162_matching_the_flat_internal_dimension": (
            matter_flavour_dimension == 162
            and matter_flavour_dimension == internal_dimension
        ),
    }
    theorem["the_witting_packet_transport_shadow_selects_the_canonical_ternary_matter_line"] = all(
        theorem.values()
    )

    return {
        "status": "ok",
        "transport_side": {
            "real_flat_section_dimension": transport["real_local_system"]["common_fixed_subspace_dimension"],
            "ternary_flat_section_dimension": transport["ternary_reduction"]["common_fixed_subspace_dimension"],
            "invariant_line": transport["ternary_reduction"]["unique_invariant_projective_line"],
            "quotient_character_values": transport["ternary_reduction"]["quotient_character_values"],
        },
        "matter_side": {
            "homological_field": ternary["ternary_css_code"]["field"],
            "logical_qutrits": logical_qutrits,
            "canonical_transport_stable_sector_dimension": canonical_sector_dimension,
        },
        "combined_sector": {
            "full_reduced_a2_fiber_rank": full_reduced_fiber_rank,
            "matter_flavour_dimension": matter_flavour_dimension,
            "flat_internal_dimension": internal_dimension,
            "matches_flat_internal_dimension_exactly": matter_flavour_dimension == internal_dimension,
        },
        "packet_transport_ternary_line_theorem": theorem,
        "bridge_verdict": (
            "The packet transport shadow now locks directly to the qutrit matter side. The mod-3 packet "
            "path-groupoid has a unique invariant line, the W33 ternary homological code has exactly 81 logical "
            "qutrits, tensoring them gives a canonical 81-dimensional packet-transport-stable matter sector, and "
            "keeping the full reduced A2 fiber gives 162, matching the exact internal dimension already present in "
            "the finite spectral-action layer."
        ),
    }


def main() -> int:
    timer = time.perf_counter()
    payload = analyze()
    output_dir = ROOT / "checks"
    output_dir.mkdir(exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    output_path = output_dir / f"PART_CXXXVII_witting_packet_transport_ternary_line_audit_{timestamp}.json"
    output_path.write_text(json.dumps(payload, indent=2, default=int), encoding="utf-8")

    print("W33 Witting packet transport ternary-line audit")
    for key, value in payload["packet_transport_ternary_line_theorem"].items():
        print(f"  [{'PASS' if value else 'FAIL'}] {key}")
    print(f"  Wrote: {output_path}")
    print(f"  Runtime: {time.perf_counter() - timer:.3f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
