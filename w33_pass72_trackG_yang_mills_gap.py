"""Pass 72 Track G: Yang-Mills mass gap numerical lower bound.

Uses W(3,3) spectral gap data to derive a graph-scale lower bound and
records both dimensionless and normalized physical-unit placeholders.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

HBAR_C_GEV_FM = 0.1973269804


def main() -> None:
    k = 12
    lambda_gauge = 2.0
    lambda_fermion = -4.0
    delta_graph = lambda_gauge - lambda_fermion
    lattice_spacing_a = 1.0 / math.sqrt(k)
    inverse_a = 1.0 / lattice_spacing_a
    mass_gap_natural = delta_graph * inverse_a
    mass_gap_gev = mass_gap_natural * HBAR_C_GEV_FM

    payload = {
        "track": "G",
        "title": "W33 Yang-Mills mass gap lower bound",
        "degree_k": k,
        "lambda_gauge": lambda_gauge,
        "lambda_fermion": lambda_fermion,
        "delta_graph_units": delta_graph,
        "lattice_spacing_a": lattice_spacing_a,
        "inverse_lattice_spacing": inverse_a,
        "mass_gap_lower_natural_units": mass_gap_natural,
        "mass_gap_lower_GeV_if_a_in_fm": mass_gap_gev,
        "formula": "Delta * (1/a)",
        "reference": "BREAKTHROUGH_BT679_YANG_MILLS_MASS_GAP.md"
    }

    Path("w33_pass72_trackG_yang_mills_gap.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
