"""Mod-12 genus selector as the 0/3/4/7 packet.

For the toroidal neighborly law

    g = (n - 3)(n - 4) / 12,

integrality is equivalent to a residue condition on n mod 12.  The exact
admissible residues are

    0, 3, 4, 7 (mod 12).

After the new heptad and mode-chart bridges, these four numbers are no longer
floating around independently:

    0 = trivial packet,
    3 = Fourier mode count,
    4 = chart count,
    7 = 3 + 4 = Phi6 heptad count.

This bridge records that exact arithmetic selector.  It does not claim the
residue classes are uniquely determined by local physics; it shows the same
packet that organizes the toroidal/tetrahedral/tomotope bridges is already the
full mod-12 admissibility set of the minimal-triangulation law.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

from exploration.w33_tetrahedral_fourier_clifford_bridge import build_summary as build_fourier_summary
from exploration.w33_toroidal_heptad_projector_bridge import build_summary as build_heptad_summary


DEFAULT_OUTPUT_PATH = ROOT / "data" / "w33_mod12_packet_selector_bridge_summary.json"


def admissible_residues(modulus: int = 12) -> list[int]:
    return [
        residue
        for residue in range(modulus)
        if ((residue - 3) * (residue - 4)) % modulus == 0
    ]


def build_summary() -> dict[str, Any]:
    fourier = build_fourier_summary()
    heptad = build_heptad_summary()

    chart_count = fourier["chirality_packet"]["positive_count"] + fourier["chirality_packet"]["negative_count"]
    mode_count = 3
    heptad_count = heptad["realization_packet"]["count"]
    residues = admissible_residues()

    summary: dict[str, Any] = {
        "modulus": 12,
        "admissible_residues": residues,
        "packet_counts": {
            "trivial": 0,
            "mode_count": mode_count,
            "chart_count": chart_count,
            "heptad_count": heptad_count,
        },
        "mod12_packet_selector_theorem": {
            "the_neighborly_genus_selector_has_exact_residues_0_3_4_7": residues == [0, 3, 4, 7],
            "the_nonzero_selector_residues_are_exactly_mode_chart_and_heptad_counts": (
                residues[1:] == [mode_count, chart_count, heptad_count]
            ),
            "the_heptad_residue_is_the_sum_of_mode_and_chart_counts": heptad_count == mode_count + chart_count,
        },
        "interpretation": (
            "The mod-12 admissibility set of the toroidal genus law is exactly the packet "
            "{0,3,4,7}. After the new bridges, those are precisely the trivial slot, the "
            "three local Fourier modes, the four chart vertices, and the 7-element heptad."
        ),
    }
    return summary


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary["mod12_packet_selector_theorem"], indent=2))


if __name__ == "__main__":
    main()
