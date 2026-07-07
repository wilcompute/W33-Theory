"""Pass 71 master runner: executes Tracks D, E, F and cross-validates."""
from __future__ import annotations
import importlib
import json
import math
import sys
from pathlib import Path

TRACKS = [
    ("w33_pass71_trackD_css_matrices",   "w33_pass71_trackD_css_matrices.json"),
    ("w33_pass71_trackE_ihara_zeta",      "w33_pass71_trackE_ihara_zeta_poles.json"),
    ("w33_pass71_trackF_pmns_angles",     "w33_pass71_trackF_pmns_angles.json"),
]


def run_all() -> None:
    results = {}
    for module_name, output_file in TRACKS:
        mod = importlib.import_module(module_name)
        mod.main()
        p = Path(output_file)
        if not p.exists():
            print(f"[FAIL] {output_file} not written", file=sys.stderr)
            sys.exit(1)
        results[output_file] = json.loads(p.read_text())
        print(f"[PASS] {output_file}")

    # Cross-track assertions
    D = results["w33_pass71_trackD_css_matrices.json"]
    E = results["w33_pass71_trackE_ihara_zeta_poles.json"]
    F = results["w33_pass71_trackF_pmns_angles.json"]

    assert D["css_condition_satisfied"] is True, "CSS condition H_X * H_Z^T != 0"
    assert D["n_points"] == 40, "Expected 40 W(3,3) points"
    assert E["n_vertices"] == 40 and E["n_edges"] == 240, "W(3,3) graph dimensions wrong"
    assert E["grh_satisfied"] is True, "Graph-RH violated"
    assert F["spectral_parameters"]["k"] == 12, "Degree mismatch"

    print("\nAll Pass 71 tracks completed and cross-validated.")
    print(f"  Track D: CSS verified, d_lower = {D['d_lower_bound']}")
    print(f"  Track E: GRH satisfied = {E['grh_satisfied']}, radius = {E['grh_radius']:.6f}")
    print(f"  Track F: theta_12 = {F['w33_predictions']['theta_12_deg']:.2f} deg (PDG: {F['pdg_2024_values']['theta_12_deg']})")


if __name__ == "__main__":
    run_all()
