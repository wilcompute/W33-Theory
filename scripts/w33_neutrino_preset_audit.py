#!/usr/bin/env python3
"""Cross-preset audit for the W(3,3) neutrino fixed-point packet.

This audit separates two claims that had been implicitly conflated:

1. The legacy April 2026 numbers are reproducible from the NuFIT 5.3 baseline.
2. The lowest-sum fixed point survives when the solver is updated to the
   current official NuFIT 6.0 oscillation fits.

The exact outcome of this audit is modest but useful:
  the `1/mu` branch remains the minimum-sum solution in both NH and IH across
  the supported NuFIT presets, while the absolute sums shift only slightly.
"""

from __future__ import annotations

from functools import lru_cache
import json
from pathlib import Path
import sys
import time
from typing import Dict, Mapping


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

from scripts.SOLVE_RG_NEUTRINO import (
    CURRENT_PRESET_NAME,
    LEGACY_PRESET_NAME,
    OSCILLATION_PRESETS,
    build_payload,
)


def _ordering(results: Mapping[str, Mapping[str, object]], hierarchy: str) -> tuple[str, ...]:
    return tuple(
        label
        for label, _ in sorted(
            (
                (label, float(entry[hierarchy]["sum_meV"]))
                for label, entry in results.items()
                if hierarchy in entry
            ),
            key=lambda item: item[1],
        )
    )


def _hierarchy_sums(results: Mapping[str, Mapping[str, object]], hierarchy: str) -> Dict[str, float]:
    return {
        label: float(entry[hierarchy]["sum_meV"])
        for label, entry in results.items()
        if hierarchy in entry
    }


def _minimum_gap_mev(sums: Mapping[str, float]) -> float:
    ordered = sorted(float(value) for value in sums.values())
    return ordered[1] - ordered[0]


@lru_cache(maxsize=1)
def analyze() -> Dict[str, object]:
    preset_payloads = {
        preset_name: build_payload(preset_name)
        for preset_name in OSCILLATION_PRESETS
    }

    preset_records: Dict[str, object] = {}
    nh_orderings = set()
    ih_orderings = set()
    nh_minima = set()
    ih_minima = set()

    for preset_name, payload in preset_payloads.items():
        results = payload["results"]
        nh_sums = _hierarchy_sums(results, "NH")
        ih_sums = _hierarchy_sums(results, "IH")
        nh_order = _ordering(results, "NH")
        ih_order = _ordering(results, "IH")
        nh_orderings.add(nh_order)
        ih_orderings.add(ih_order)
        nh_minima.add(nh_order[0])
        ih_minima.add(ih_order[0])

        preset_records[preset_name] = {
            "preset": payload["preset"],
            "nh_sums_meV": nh_sums,
            "ih_sums_meV": ih_sums,
            "nh_ordering": nh_order,
            "ih_ordering": ih_order,
            "nh_minimum_label": nh_order[0],
            "ih_minimum_label": ih_order[0],
            "nh_minimum_gap_meV": _minimum_gap_mev(nh_sums),
            "ih_minimum_gap_meV": _minimum_gap_mev(ih_sums),
        }

    legacy = preset_records[LEGACY_PRESET_NAME]
    current = preset_records[CURRENT_PRESET_NAME]

    theorem = {
        "nh_minimum_is_always_1_over_mu": nh_minima == {"1/mu"},
        "ih_minimum_is_always_1_over_mu": ih_minima == {"1/mu"},
        "nh_fixed_point_ordering_is_stable_across_supported_presets": len(nh_orderings) == 1,
        "ih_fixed_point_ordering_is_stable_across_supported_presets": len(ih_orderings) == 1,
        "latest_official_nh_sum_at_1_over_mu_stays_near_101_meV": 100.0 < current["nh_sums_meV"]["1/mu"] < 102.0,
        "latest_official_ih_sum_at_1_over_mu_stays_near_110_meV": 109.0 < current["ih_sums_meV"]["1/mu"] < 111.0,
        "latest_official_shift_from_legacy_is_sub_mev_in_nh": abs(
            current["nh_sums_meV"]["1/mu"] - legacy["nh_sums_meV"]["1/mu"]
        ) < 1.0,
        "latest_official_shift_from_legacy_is_sub_mev_in_ih": abs(
            current["ih_sums_meV"]["1/mu"] - legacy["ih_sums_meV"]["1/mu"]
        ) < 1.0,
    }

    return {
        "status": "ok",
        "presets": preset_records,
        "cross_preset_theorem": theorem,
        "boundary_note": (
            "The neutrino layer is not an exact finite theorem in the same sense as the qutrit or "
            "spectral kernel. What is stable is narrower: across the legacy NuFIT 5.3 baseline and "
            "the current official NuFIT 6.0 tables, the W(3,3) fixed-point ordering does not move, "
            "and the `1/mu` branch remains the minimum-sum solution in both mass orderings."
        ),
    }


def main() -> None:
    started = time.time()
    payload = analyze()
    payload["analysis_duration_sec"] = round(time.time() - started, 6)

    output_dir = ROOT / "checks"
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    output_path = output_dir / f"PART_CXVI_neutrino_preset_audit_{timestamp}.json"
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    current = payload["presets"][CURRENT_PRESET_NAME]
    print("Neutrino preset audit")
    print(f"  Latest official preset: {current['preset']['label']}")
    print(f"  NH ordering: {' < '.join(current['nh_ordering'])}")
    print(f"  IH ordering: {' < '.join(current['ih_ordering'])}")
    print(
        "  Latest 1/mu sums: "
        f"NH={current['nh_sums_meV']['1/mu']:.6f} meV, "
        f"IH={current['ih_sums_meV']['1/mu']:.6f} meV"
    )
    print(f"  Wrote: {output_path}")


if __name__ == "__main__":
    main()
