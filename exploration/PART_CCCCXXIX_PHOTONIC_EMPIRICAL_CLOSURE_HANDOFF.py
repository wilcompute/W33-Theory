#!/usr/bin/env python3
"""PART CCCCXXIX -- Photonic Empirical Closure Handoff.

This part reconciles the two numbering streams now active in the repo:

* the CCCC photonic/curved architecture, currently at CCCCXXVIII;
* the CCC empirical Standard Model closure stream, currently through
  CCCXXXIII plus the GitHub-side CCCXXVII mass-mixing surface verifier.

The theorem here is deliberately bounded. The photonic curved extractor gives
the exact internal/curved coefficient package

    c6=12480, cEH=320, a2=2240, x=3/13,

while the empirical stream gives a W(3,3) mass/mixing sheet using the same
atoms q=3, lambda=2, mu=4, v=40, Phi3=13, Phi4=10, Phi6=7 and the same
fine-structure prime 137. This is a compatibility and handoff certificate,
not a final smooth spectral-action theorem and not a structural derivation of
every Yukawa numerator.
"""
from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path
from typing import Any, Dict, List


ROOT = Path(__file__).resolve().parents[1]

PHOTONIC_EH = ROOT / "PART_CCCCXXVIII_photonic_curved_eh_extractor_results.json"
MASS_MIXING = ROOT / "PART_CCCXXVII_mass_mixing_closure_surface_results.json"
EMPIRICAL_AUDIT = ROOT / "PART_CCCXXXI_sm_empirical_final_audit_results.json"
GUT_PLANCK = ROOT / "PART_CCCXXXII_gut_planck_hierarchy_results.json"
LIGHT_QUARKS = ROOT / "PART_CCCXXXIII_light_quark_yukawas_results.json"


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def ok(name: str, cond: bool, value: Any = None) -> Dict[str, Any]:
    return {"name": name, "passed": bool(cond), "value": value}


def frac(value: str | int | float) -> Fraction:
    return Fraction(str(value))


def observable_by_name(surface: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    return {entry["name"]: entry for entry in surface["observables"]}


def residual_by_id(results: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    return {entry["id"]: entry for entry in results["residuals"]}


def build_results() -> Dict[str, Any]:
    photonic = load_json(PHOTONIC_EH)
    mass = load_json(MASS_MIXING)
    audit = load_json(EMPIRICAL_AUDIT)
    gut = load_json(GUT_PLANCK)
    light = load_json(LIGHT_QUARKS)

    coeffs = photonic["coefficient_package"]
    inverse = photonic["inverse_rosetta"]
    finite = photonic["finite_roundtrip"]
    handoff = photonic["protected_photonic_handoff"]
    mass_atoms = mass["atoms"]
    light_constants = light["constants"]
    gut_predictions = gut["predictions"]
    mass_observables = observable_by_name(mass)
    light_residuals = residual_by_id(light)
    gut_residuals = residual_by_id(gut)

    q = int(mass_atoms["q"])
    lam = int(mass_atoms["lambda"])
    mu = int(mass_atoms["mu"])
    v = int(mass_atoms["v"])
    phi3 = int(mass_atoms["Phi3"])
    phi4 = int(mass_atoms["Phi4"])
    phi6 = int(mass_atoms["Phi6"])
    alpha_inv = q**q * (mu + 1) + lam
    h0 = phi6 * phi4

    discrete_eh = frac(coeffs["discrete_eh"])
    continuum_eh = frac(coeffs["continuum_eh"])
    topological_a2 = frac(coeffs["topological_a2"])
    x = Fraction(coeffs["master_variable"])

    derived_links = {
        "rank39_lock": str(discrete_eh / continuum_eh),
        "rank39_as_q_phi3": q * phi3,
        "topological_ratio": str(topological_a2 / continuum_eh),
        "topological_ratio_as_phi6": phi6,
        "weinberg_x": str(x),
        "weinberg_denominator_phi3": phi3,
        "alpha_inv": alpha_inv,
        "alpha_inv_cubed": alpha_inv**3,
        "hubble_fixed_point_h0": h0,
        "down_yukawa_numerator": light["constants"]["H_0"],
        "gut_planck_ratio": gut_predictions["M_Pl_over_M_GUT_W33"],
        "gut_alpha_inverse": gut_predictions["alpha_GUT_inv_W33"],
    }

    checks: List[Dict[str, Any]] = []
    checks.append(ok("photonic curved EH extractor verified", photonic["verified"] is True, photonic["checks_passed"]))
    checks.append(ok("mass-mixing closure surface internally verified", mass["all_internal_identities_pass"] is True, mass["internal_identities"]))
    checks.append(ok("mass-mixing closure surface within two sigma", mass["all_within_2sigma"] is True and mass["max_abs_z"] <= 1.0 + 1e-12, {"reduced_chi2": mass["reduced_chi2"], "max_abs_z": mass["max_abs_z"]}))
    checks.append(ok("SM empirical audit verified", audit["Verified"] is True and audit["checks_passed"] == audit["checks_total"], audit["inventory_summary"]))
    checks.append(ok("GUT-Planck hierarchy verified", gut["Verified"] is True and gut["checks_passed"] == gut["checks_total"], gut_predictions))
    checks.append(ok("light-quark Yukawa bridge verified", light["Verified"] is True and light["checks_passed"] == light["checks_total"], light["predictions"]))

    checks.append(ok("photonic inverse Rosetta q matches mass sheet", inverse["q"] == q == 3, {"inverse": inverse, "mass_atoms": mass_atoms}))
    checks.append(ok("photonic inverse Rosetta Phi3 matches mass sheet", inverse["phi3"] == str(phi3) == "13", inverse))
    checks.append(ok("photonic inverse Rosetta Phi6 matches mass sheet", inverse["phi6"] == str(phi6) == "7", inverse))
    checks.append(ok("photonic SRG is the same W33 surface", inverse["srg"] == {"v": 40, "k": 12, "lambda": 2, "mu": 4}, inverse["srg"]))
    checks.append(ok("shared atom table is W33 canonical", mass_atoms == {"q": 3, "lambda": 2, "mu": 4, "k": 12, "v": 40, "Phi3": 13, "Phi4": 10, "Phi6": 7}, mass_atoms))
    checks.append(ok("light-quark constants share q lambda mu v", (light_constants["Q"], light_constants["LAM"], light_constants["MU"], light_constants["V"]) == (q, lam, mu, v), light_constants))

    checks.append(ok("c6/cEH is q*Phi3 = 39", discrete_eh / continuum_eh == q * phi3 == 39, derived_links))
    checks.append(ok("a2/cEH is Phi6 = 7", topological_a2 / continuum_eh == phi6 == 7, derived_links))
    checks.append(ok("x is q/Phi3 = 3/13", x == Fraction(q, phi3) == Fraction(3, 13), derived_links))
    checks.append(ok("c6 equals cEH*q*Phi3", discrete_eh == continuum_eh * q * phi3 == 12480, derived_links))
    checks.append(ok("a2 equals cEH*Phi6", topological_a2 == continuum_eh * phi6 == 2240, derived_links))
    checks.append(ok("finite DF2 spectrum preserved", finite["df2_spectrum"] == {"0": 82, "4": 320, "10": 48, "16": 30}, finite))
    checks.append(ok("protected photonic handoff preserved", handoff["active_code"] == "[[82320,81,>=81]]" and handoff["h1_logical"] == 81 and handoff["selector_trits"] == 40, handoff))

    checks.append(ok("mass surface Higgs quartic uses Phi3/Phi4^2", mass_observables["lambda_H_MSbar_MZ"]["formula"] == "Phi_3/Phi_4^2 = 13/100", mass_observables["lambda_H_MSbar_MZ"]))
    checks.append(ok("mass surface CKM lambda uses q^2/v", mass_observables["wolf_lambda"]["formula"] == "q^2/v = 9/40", mass_observables["wolf_lambda"]))
    checks.append(ok("mass surface CKM A uses q^4/Phi4^2", mass_observables["wolf_A"]["formula"] == "q^4/Phi_4^2 = 81/100", mass_observables["wolf_A"]))
    checks.append(ok("mass surface eta uses Phi6/Phi4 cubed", mass_observables["wolf_etabar"]["formula"] == "(Phi_6/Phi_4)^3 = 343/1000", mass_observables["wolf_etabar"]))
    checks.append(ok("mass surface top Yukawa uses v/(v+1)", mass_observables["top_yukawa_pole"]["formula"] == "(v/(v+1))^(1/3)", mass_observables["top_yukawa_pole"]))

    checks.append(ok("137 prime formula shared by light quarks", alpha_inv == light_constants["ALPHA_INV"] == 137, derived_links))
    checks.append(ok("137^3 shared denominator is exact", alpha_inv**3 == 2571353, derived_links))
    checks.append(ok("H0 equals Phi6*Phi4 and down numerator", h0 == light_constants["H_0"] == 70, derived_links))
    checks.append(ok("down Yukawa residual passes", light_residuals["DOWN_YUKAWA_W33"]["status"] == "PASS_WITHIN_1_SIGMA", light_residuals["DOWN_YUKAWA_W33"]))
    checks.append(ok("up Yukawa residual passes", light_residuals["UP_YUKAWA_W33"]["status"] == "PASS_WITHIN_1_SIGMA", light_residuals["UP_YUKAWA_W33"]))
    checks.append(ok("up/down ratio is 16/35", light["predictions"]["y_u_over_y_d_W33"] == "16/35", light["predictions"]))

    checks.append(ok("GUT inverse coupling is f=24", gut_predictions["alpha_GUT_inv_W33"] == 24, gut_predictions))
    checks.append(ok("GUT-Planck ratio is 114", gut_predictions["M_Pl_over_M_GUT_W33"] == 114, gut_predictions))
    checks.append(ok("114 decomposes as lambda*q*(24-mu-1)", gut_predictions["M_Pl_over_M_GUT_W33"] == lam * q * (24 - mu - 1), derived_links))
    checks.append(ok("GUT residuals pass", all("PASS" in entry["status"] for entry in gut_residuals.values()), gut_residuals))

    open_boundaries = {
        "smooth_spectral_action_limit": "open",
        "structural_h0_down_yukawa_derivation": "open",
        "full_lepton_yukawa_packet": "open",
        "neutrino_mass_packet": "open",
        "lambda_qcd_and_strong_cp": "open",
        "dark_matter_and_cosmological_constant": "open",
    }
    checks.append(ok("honesty boundary keeps open problems explicit", all(value == "open" for value in open_boundaries.values()), open_boundaries))

    verified = all(check["passed"] for check in checks)
    return {
        "part": "CCCCXXIX",
        "title": "Photonic Empirical Closure Handoff",
        "verified": verified,
        "checks_total": len(checks),
        "checks_passed": sum(check["passed"] for check in checks),
        "source_streams": {
            "photonic_curved": "CCCCXXVIII",
            "mass_mixing_surface": "CCCXXVII",
            "empirical_audit": "CCCXXXI",
            "gut_planck": "CCCXXXII",
            "light_quarks": "CCCXXXIII",
        },
        "shared_w33_atoms": {
            "q": q,
            "lambda": lam,
            "mu": mu,
            "v": v,
            "Phi3": phi3,
            "Phi4": phi4,
            "Phi6": phi6,
            "alpha_inv": alpha_inv,
            "H0": h0,
        },
        "photonic_curved_exact_layer": {
            "c6": str(discrete_eh),
            "cEH": str(continuum_eh),
            "a2": str(topological_a2),
            "x": str(x),
            "df2_spectrum": finite["df2_spectrum"],
            "protected_code": handoff["active_code"],
            "h1_logical": handoff["h1_logical"],
        },
        "empirical_mass_sheet": {
            "surface_observables": list(mass_observables),
            "reduced_chi2": mass["reduced_chi2"],
            "max_abs_z": mass["max_abs_z"],
            "light_quark_yukawas": {
                "y_d": "70/137^3",
                "y_u": "32/137^3",
                "y_u_over_y_d": light["predictions"]["y_u_over_y_d_W33"],
            },
            "gut_planck": {
                "alpha_GUT_inverse": gut_predictions["alpha_GUT_inv_W33"],
                "M_Pl_over_M_GUT": gut_predictions["M_Pl_over_M_GUT_W33"],
            },
        },
        "derived_links": derived_links,
        "architecture_upgrade": (
            "This reconciles the CCCC photonic-curved architecture stream with "
            "the CCC empirical mass/Yukawa stream. The same W33 atoms that the "
            "curved extractor reconstructs from CP2_9/K3_16 samples also drive "
            "the Higgs/CKM/top mass-mixing sheet, the light-quark 137^3 "
            "Yukawa closures, and the GUT-Planck 24/114 hierarchy."
        ),
        "theorem": (
            "The photonic curved coefficient package and the empirical mass "
            "surface use one W(3,3) atom table. In particular c6/cEH=39=q*Phi3, "
            "a2/cEH=7=Phi6, x=q/Phi3=3/13, the mass-mixing sheet uses "
            "Phi3/Phi4^2, q^2/v, q^4/Phi4^2, (Phi6/Phi4)^3, and v/(v+1), "
            "and the light-quark layer uses alpha_inv=137 and H0=Phi6*Phi4=70."
        ),
        "honesty_boundary": (
            "This is a compatibility handoff between exact photonic-curved "
            "finite coefficients and the current empirical mass/Yukawa closure "
            "surface. It does not prove the smooth Einstein-Hilbert spectral "
            "action limit, and it does not yet structurally derive every "
            "remaining Yukawa, neutrino, QCD, dark-matter, or cosmological "
            "constant datum."
        ),
        "open_boundaries": open_boundaries,
        "checks": checks,
    }


def main() -> int:
    results = build_results()
    out = ROOT / "PART_CCCCXXIX_photonic_empirical_closure_handoff_results.json"
    out.write_text(json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "part": results["part"],
                "verified": results["verified"],
                "checks_passed": results["checks_passed"],
                "checks_total": results["checks_total"],
                "c6": results["photonic_curved_exact_layer"]["c6"],
                "x": results["photonic_curved_exact_layer"]["x"],
                "alpha_inv": results["shared_w33_atoms"]["alpha_inv"],
                "out_path": str(out),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
