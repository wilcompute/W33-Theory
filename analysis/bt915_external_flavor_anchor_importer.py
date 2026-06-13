#!/usr/bin/env python3
"""BT915 - import versioned external flavor anchors and compare to exact profile values."""
from __future__ import annotations
import json, math
from fractions import Fraction
from pathlib import Path

ANCHOR_PATH = Path("data/external_flavor_anchors_20260613.json")
OUT = Path("data/PART_BT915_EXTERNAL_FLAVOR_ANCHOR_IMPORTER_results.json")
INTERNAL = {
    "Cabibbo_sin": {"value": math.sqrt(float(Fraction(9,178))), "exact": "3/sqrt(178)"},
    "PMNS_solar_sin2": {"value": float(Fraction(4,13)), "exact": "4/13"},
    "PMNS_reactor_sin2": {"value": float(Fraction(2,91)), "exact": "2/91"},
    "PMNS_atmospheric_sin2": {"value": float(Fraction(7,13)), "exact": "7/13"},
    "Koide_Q": {"value": float(Fraction(2,3)), "exact": "2/3"},
}

def koide_q(masses: dict[str,float]) -> float:
    roots = [math.sqrt(v) for v in masses.values()]
    return sum(masses.values()) / (sum(roots)**2)

def main() -> None:
    anchors = json.loads(ANCHOR_PATH.read_text(encoding="utf-8"))
    assert anchors["schema"] == "external_flavor_anchors/v1"
    source_keys = {s["key"] for s in anchors["sources"]}
    rows = []
    for name, ext in anchors["mixing_anchors"].items():
        assert ext["source_key"] in source_keys
        i = INTERNAL[name]["value"]
        residual = i - ext["value"]
        pull = residual / ext["uncertainty"]
        rows.append({"observable": name, "internal": i, "internal_exact": INTERNAL[name]["exact"], "external_reference": ext["value"], "external_uncertainty": ext["uncertainty"], "residual": residual, "pull_sigma": pull, "status": "inside_1sigma" if abs(pull) <= 1 else ("inside_2sigma" if abs(pull) <= 2 else "outside_2sigma"), "source_key": ext["source_key"]})
    masses = {k:v["value"] for k,v in anchors["charged_lepton_masses_MeV"].items()}
    k_ext = koide_q(masses)
    rows.append({"observable":"Koide_Q","internal":INTERNAL["Koide_Q"]["value"],"internal_exact":"2/3","external_reference_from_anchor_masses":k_ext,"residual":INTERNAL["Koide_Q"]["value"]-k_ext,"source_key":"PDG_style_lepton_masses_2024"})
    result = {"theorem":"BT915 external flavor anchor importer","anchor_file":str(ANCHOR_PATH),"schema":anchors["schema"],"version_date":anchors["version_date"],"status":"imported versioned external anchors; no fit performed","comparisons":rows,"checks":{"T1_schema_validated":True,"T2_source_keys_validated":True,"T3_external_anchors_versioned":True,"T4_residuals_recomputed_from_anchor_file":True,"T5_no_fitted_parameters":True}}
    OUT.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print("BT915 imported anchors and wrote", OUT)
if __name__ == "__main__": main()
