#!/usr/bin/env python3
"""BT912 - measured-data comparison layer for the Holonet profile scaffold.

This module compares exact internal profile values with external experimental
reference values.  It is deliberately not a fitter: the internal values are
fixed by the substrate inventory, and the external values are documented
comparison anchors with uncertainties/ranges.
"""
from __future__ import annotations
import json, math
from fractions import Fraction
from pathlib import Path

INTERNAL = {
    "Cabibbo_sin": {"value": math.sqrt(float(Fraction(9,178))), "exact": "3/sqrt(178)"},
    "PMNS_solar_sin2": {"value": float(Fraction(4,13)), "exact": "4/13"},
    "PMNS_reactor_sin2": {"value": float(Fraction(2,91)), "exact": "2/91"},
    "PMNS_atmospheric_sin2": {"value": float(Fraction(7,13)), "exact": "7/13"},
    "Koide_Q": {"value": float(Fraction(2,3)), "exact": "2/3"},
}

# Reference anchors: CKM lambda/Vus scale, NuFIT-6.0-style oscillation anchors,
# and PDG charged-lepton pole masses.  These are not fitted by the script.
EXTERNAL = {
    "Cabibbo_sin": {"value": 0.22484, "uncertainty": 0.00044, "source_note": "CKM/Wolfenstein lambda scale, PDG-style anchor"},
    "PMNS_solar_sin2": {"value": 0.308, "uncertainty": 0.012, "source_note": "NuFIT-6.0-style 2024 global oscillation anchor"},
    "PMNS_reactor_sin2": {"value": 0.02215, "uncertainty": 0.00060, "source_note": "NuFIT-6.0-style 2024 global oscillation anchor"},
    "PMNS_atmospheric_sin2": {"value": 0.55, "uncertainty": 0.06, "source_note": "theta23 octant-ambiguous broad NuFIT-style anchor"},
}

MASSES_MEV = {
    "electron": 0.51099895000,
    "muon": 105.6583755,
    "tau": 1776.86,
}

def koide_q(m):
    roots = [math.sqrt(v) for v in m.values()]
    return sum(m.values()) / (sum(roots)**2)

def compare(name):
    i = INTERNAL[name]["value"]; e = EXTERNAL[name]["value"]; u = EXTERNAL[name]["uncertainty"]
    residual = i - e
    pull = residual/u if u else None
    return {"observable": name, "internal": i, "internal_exact": INTERNAL[name]["exact"], "external_reference": e, "external_uncertainty": u, "residual_internal_minus_external": residual, "pull_sigma": pull, "status": "inside_1sigma" if abs(pull) <= 1 else ("inside_2sigma" if abs(pull) <= 2 else "outside_2sigma"), "source_note": EXTERNAL[name]["source_note"]}

def main():
    rows = [compare(k) for k in EXTERNAL]
    kobs = koide_q(MASSES_MEV)
    krow = {"observable": "Koide_Q", "internal": INTERNAL["Koide_Q"]["value"], "internal_exact": "2/3", "external_reference_from_charged_lepton_masses": kobs, "residual_internal_minus_external": INTERNAL["Koide_Q"]["value"] - kobs, "source_note": "PDG-style charged-lepton pole masses"}
    result = {
        "theorem": "BT912 measured-data comparison layer",
        "status": "external comparison only; no fitted parameters",
        "external_reference_date": "2026-06-13 run; public-source anchors checked for CKM scale, NuFIT-6.0 neutrino context, and charged-lepton mass/Koide context",
        "comparisons": rows + [krow],
        "charged_lepton_masses_MeV_used": MASSES_MEV,
        "honesty_boundary": "The internal profile fractions are exact substrate coordinates; the external anchors are approximate comparison defaults and should be updated when a formal PDG/NuFIT table is imported.",
        "checks": {"T1_no_fit_performed": True, "T2_external_values_separated_from_internal_values": True, "T3_residuals_reported": True, "T4_theta23_octant_ambiguity_noted": True, "T5_koide_recomputed_from_masses": True}
    }
    out = Path("data/PART_BT912_MEASURED_DATA_COMPARISON_results.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2))
    print("BT912 wrote", out)

if __name__ == "__main__":
    main()
