#!/usr/bin/env python3
"""PART CCCCXXVIII -- Photonic Curved Einstein-Hilbert Extractor.

CCCCXXVII attaches the protected photonic runtime to explicit curved 4D
operators. This certificate connects that handoff to the exact coefficient
machinery already present in the repo:

    projector channel -> residue channel -> three-sample extractor
    -> finite spectral reconstruction -> Rosetta / Weinberg roundtrip.

The conservative reading is important. This does not prove the final
Einstein-Hilbert spectral-action asymptotic theorem. It proves the sharper
finite statement now available: once the protected photonic kernel is paired
with CP2_9 or K3_16, the curved refinement tower already contains exact
discrete projectors and residues that recover

    c_6 = 12480, c_EH = 320, a2 = 2240, x = 3/13.
"""
from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path
from typing import Any, Dict, Iterable, List

from w33_curved_continuum_extractor_bridge import build_curved_continuum_extractor_summary
from w33_curved_finite_spectral_reconstruction_bridge import (
    build_curved_finite_spectral_reconstruction_summary,
)
from w33_curved_mode_projector_bridge import build_curved_mode_projector_bridge_summary
from w33_curved_mode_residue_bridge import build_curved_mode_residue_bridge_summary
from w33_curved_rosetta_reconstruction_bridge import build_curved_rosetta_reconstruction_summary
from w33_curved_roundtrip_closure_bridge import build_curved_roundtrip_closure_summary
from w33_curved_weinberg_lock_bridge import build_curved_weinberg_lock_bridge_summary


ROOT = Path(__file__).resolve().parents[1]

HANDOFF = ROOT / "PART_CCCCXXVII_photonic_curved_product_handoff_results.json"

EXPECTED_DF2_SPECTRUM = {"0": 82, "4": 320, "10": 48, "16": 30}


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def ok(name: str, cond: bool, value: Any = None) -> Dict[str, Any]:
    return {"name": name, "passed": bool(cond), "value": value}


def exact(entry: Dict[str, Any]) -> str:
    return str(entry["exact"])


def frac(value: str | int | Fraction) -> Fraction:
    return Fraction(value)


def stringify_keys(mapping: Dict[Any, Any]) -> Dict[str, Any]:
    return {str(key): value for key, value in mapping.items()}


def all_true(mapping: Dict[str, Any]) -> bool:
    return all(value is True for value in mapping.values())


def flattened_continuum_samples(continuum: Dict[str, Any]) -> List[Dict[str, Any]]:
    return [
        {"seed_name": seed["seed_name"], **sample}
        for seed in continuum["seeds"]
        for sample in seed["samples"]
    ]


def projector_seed_names(projector: Dict[str, Any]) -> List[str]:
    return [seed["seed_name"] for seed in projector["seeds"]]


def all_projector_samples_match(projector: Dict[str, Any]) -> bool:
    for seed in projector["seeds"]:
        for sample in seed["projector_samples"]:
            if sample["projected_120"] != sample["expected_120"]:
                return False
            if sample["projected_6"] != sample["expected_6"]:
                return False
            if sample["projected_1"] != sample["expected_1"]:
                return False
    return True


def residue_seed_names(residue: Dict[str, Any]) -> List[str]:
    return [seed["seed_name"] for seed in residue["seed_residue_data"]]


def all_promoted_observables_match(rosetta: Dict[str, Any]) -> bool:
    return all(
        entry["matches_public_value"] is True
        for entry in rosetta["promoted_observables_from_reconstructed_graph_data"].values()
    )


def sample_steps(samples: Iterable[Dict[str, Any]]) -> List[int]:
    return [int(sample["step"]) for sample in samples]


def explicit_seed_name(name: str) -> str:
    return {"CP2": "CP2_9", "K3": "K3_16"}.get(name, name)


def build_results() -> Dict[str, Any]:
    handoff = load_json(HANDOFF)
    projector = build_curved_mode_projector_bridge_summary()
    residue = build_curved_mode_residue_bridge_summary()
    continuum = build_curved_continuum_extractor_summary()
    finite = build_curved_finite_spectral_reconstruction_summary()
    roundtrip = build_curved_roundtrip_closure_summary()
    rosetta = build_curved_rosetta_reconstruction_summary()
    weinberg = build_curved_weinberg_lock_bridge_summary()

    continuum_samples = flattened_continuum_samples(continuum)
    finite_package = finite["reconstructed_finite_dirac_package"]
    finite_hodge = finite["reconstructed_hodge_data"]
    finite_geometry = finite["reconstructed_graph_geometry"]
    roundtrip_finite = roundtrip["reconstructed_finite_package"]
    roundtrip_coeffs = roundtrip["roundtrip_curved_coefficients"]

    df2_spectrum = stringify_keys(finite_package["df2_spectrum"])
    roundtrip_df2_spectrum = stringify_keys(roundtrip_finite["df2_spectrum"])

    discrete_eh = frac(continuum["finite_profile"]["expected_discrete_eh"]["exact"])
    continuum_eh = frac(continuum["finite_profile"]["expected_continuum_eh"]["exact"])
    topological_a2 = frac(continuum["finite_profile"]["a2"]["exact"])
    master_x = frac(weinberg["master_variable"]["exact"]["exact"])

    coefficient_package = {
        "discrete_eh": str(discrete_eh),
        "continuum_eh": str(continuum_eh),
        "rank39_normalization": f"{discrete_eh} / 39 = {continuum_eh}",
        "topological_a2": str(topological_a2),
        "topological_ratio": str(topological_a2 / continuum_eh),
        "discrete_to_continuum_ratio": str(discrete_eh / continuum_eh),
        "master_variable": str(master_x),
        "weinberg_roundtrip": str(master_x * discrete_eh / continuum_eh),
    }

    checks: List[Dict[str, Any]] = []
    checks.append(ok("CCCCXXVII handoff artifact is verified", handoff["verified"] is True, handoff["checks_passed"]))
    checks.append(ok("handoff preserved protected photonic code", handoff["protected_finite_kernel"]["active_code"] == "[[82320,81,>=81]]", handoff["protected_finite_kernel"]))
    checks.append(ok("handoff boundary stays conservative", "not the final Einstein-Hilbert spectral-action asymptotic theorem" in handoff["honesty_boundary"], handoff["honesty_boundary"]))

    checks.append(ok("mode projector builder is ok", projector["status"] == "ok", projector["bridge_verdict"]))
    checks.append(ok("mode residue builder is ok", residue["status"] == "ok", residue["bridge_verdict"]))
    checks.append(ok("continuum extractor builder is ok", continuum["status"] == "ok", continuum["bridge_verdict"]))
    checks.append(ok("finite spectral reconstruction builder is ok", finite["status"] == "ok", finite["bridge_verdict"]))
    checks.append(ok("roundtrip closure builder is ok", roundtrip["status"] == "ok", roundtrip["bridge_verdict"]))
    checks.append(ok("curved Rosetta reconstruction builder is ok", rosetta["status"] == "ok", rosetta["bridge_verdict"]))
    checks.append(ok("curved Weinberg lock builder is ok", weinberg["status"] == "ok", weinberg["bridge_verdict"]))

    checks.append(ok("tower characteristic polynomial is exact", projector["tower_characteristic_polynomial"] == "x^3 - 127x^2 + 846x - 720", projector["tower_characteristic_polynomial"]))
    checks.append(ok("shift projectors isolate 120, 6, and 1 modes", projector["shift_projectors"] == {"P_120": "((E-6)(E-1))/13566", "P_6": "-((E-120)(E-1))/570", "P_1": "((E-120)(E-6))/595"}, projector["shift_projectors"]))
    checks.append(ok("projector finite a0 is 480", exact(projector["finite_profile"]["a0"]) == "480", projector["finite_profile"]))
    checks.append(ok("projector finite a2 is 2240", exact(projector["finite_profile"]["a2"]) == "2240", projector["finite_profile"]))
    checks.append(ok("projector finite EH coefficient is 12480", exact(projector["finite_profile"]["einstein_hilbert_coefficient"]) == "12480", projector["finite_profile"]))
    checks.append(ok("projector covers CP2_9 and K3_16", projector_seed_names(projector) == ["CP2_9", "K3_16"], projector_seed_names(projector)))
    checks.append(ok("projector recurrence holds on both curved seeds", all(seed["recurrence_holds"] is True for seed in projector["seeds"]), projector["seeds"]))
    checks.append(ok("projector samples match all expected mode amplitudes", all_projector_samples_match(projector), projector["seeds"]))
    checks.append(ok("projector extracts c6=12480 on both seeds", all(exact(seed["eh_extracted_coefficient"]) == "12480" for seed in projector["seeds"]), projector["seeds"]))
    checks.append(ok("projector rank-39 normalization extracts 320", all(exact(seed["continuum_eh_from_rank_39_lock"]) == "320" for seed in projector["seeds"]), projector["seeds"]))

    checks.append(ok("residue generating function has the three pole channels", residue["generating_function"]["formula"] == "A/(1 - 120 z) + B/(1 - 6 z) + C/(1 - z)", residue["generating_function"]))
    checks.append(ok("residue finite EH coefficient is 12480", exact(residue["finite_profile"]["einstein_hilbert_coefficient"]) == "12480", residue["finite_profile"]))
    checks.append(ok("residue covers CP2_9 and K3_16", residue_seed_names(residue) == ["CP2_9", "K3_16"], residue_seed_names(residue)))
    checks.append(ok("residue over six-mode extracts c6=12480", all(exact(seed["eh_from_residue_over_six_mode"]) == "12480" for seed in residue["seed_residue_data"]), residue["seed_residue_data"]))
    checks.append(ok("residue rank-39 normalization extracts 320", all(exact(seed["continuum_eh_after_rank39_normalization"]) == "320" for seed in residue["seed_residue_data"]), residue["seed_residue_data"]))

    checks.append(ok("continuum extractor finite a0 is 480", exact(continuum["finite_profile"]["a0"]) == "480", continuum["finite_profile"]))
    checks.append(ok("continuum extractor finite a2 is 2240", exact(continuum["finite_profile"]["a2"]) == "2240", continuum["finite_profile"]))
    checks.append(ok("continuum extractor discrete EH is 12480", exact(continuum["finite_profile"]["expected_discrete_eh"]) == "12480", continuum["finite_profile"]))
    checks.append(ok("continuum extractor normalized EH is 320", exact(continuum["finite_profile"]["expected_continuum_eh"]) == "320", continuum["finite_profile"]))
    checks.append(ok("continuum extractor has six curved samples", len(continuum_samples) == 6, continuum_samples))
    checks.append(ok("continuum samples run steps 0,1,2 on each seed", sample_steps(continuum_samples) == [0, 1, 2, 0, 1, 2], continuum_samples))
    checks.append(ok("all continuum samples extract c6=12480", all(exact(sample["discrete_eh"]) == "12480" for sample in continuum_samples), continuum_samples))
    checks.append(ok("all continuum samples extract cEH=320", all(exact(sample["continuum_eh"]) == "320" for sample in continuum_samples), continuum_samples))
    checks.append(ok("all continuum samples extract a2=2240", all(exact(sample["topological_a2"]) == "2240" for sample in continuum_samples), continuum_samples))

    checks.append(ok("finite reconstruction recovers graph dimensions", finite_geometry["q"] == 3 and finite_geometry["edge_count"] == 240 and finite_geometry["triangle_count"] == 160 and finite_geometry["tetrahedron_count"] == 40, finite_geometry))
    checks.append(ok("finite reconstruction edge count matches vk/2", finite_geometry["edge_count_matches_srg_formula_vk_over_2"] is True, finite_geometry))
    checks.append(ok("finite reconstruction recovers Betti b1=81", finite_hodge["betti_numbers"] == {"b0": 1, "b1": 81, "b2": 0, "b3": 0}, finite_hodge["betti_numbers"]))
    checks.append(ok("finite reconstruction recovers boundary ranks", finite_hodge["boundary_ranks"] == {"rank_d1": 39, "rank_d2": 120, "rank_d3": 40}, finite_hodge["boundary_ranks"]))
    checks.append(ok("finite reconstruction scalar channel is 4", finite_hodge["coexact_and_high_degree_scalar_channel"] == 4, finite_hodge))
    checks.append(ok("finite reconstruction recovers DF2 spectrum", df2_spectrum == EXPECTED_DF2_SPECTRUM, df2_spectrum))
    checks.append(ok("finite reconstruction recovers moments 480,2240,17600", finite_package["seeley_dewitt_moments"] == {"a0_f": 480, "a2_f": 2240, "a4_f": 17600}, finite_package["seeley_dewitt_moments"]))
    checks.append(ok("finite reconstruction matches live internal package", all_true(finite["matches_live_internal_package"]), finite["matches_live_internal_package"]))
    checks.append(ok("finite reconstruction samples are constant", finite["all_samples_constant"] is True, finite["sample_reconstructions"]))

    checks.append(ok("roundtrip recovers same DF2 spectrum", roundtrip_df2_spectrum == EXPECTED_DF2_SPECTRUM, roundtrip_df2_spectrum))
    checks.append(ok("roundtrip recovers moments 480,2240,17600", {key: roundtrip_finite[key] for key in ("a0_f", "a2_f", "a4_f")} == {"a0_f": 480, "a2_f": 2240, "a4_f": 17600}, roundtrip_finite))
    checks.append(ok("roundtrip coefficient package is 320,12480,2240,3/13", exact(roundtrip_coeffs["continuum_eh_from_finite"]) == "320" and exact(roundtrip_coeffs["discrete_eh_from_finite"]) == "12480" and exact(roundtrip_coeffs["topological_from_finite"]) == "2240" and exact(roundtrip_coeffs["master_variable_from_roundtrip"]) == "3/13", roundtrip_coeffs))
    checks.append(ok("roundtrip matches curved extractor profile", all_true(roundtrip["matches_curved_extractor_profile"]), roundtrip["matches_curved_extractor_profile"]))
    checks.append(ok("roundtrip closes every curved sample", roundtrip["all_samples_close_exactly"] is True, roundtrip["sample_roundtrips"]))

    checks.append(ok("Rosetta reconstructs q=3", rosetta["reconstructed_cyclotomic_data"]["q"] == 3, rosetta["reconstructed_cyclotomic_data"]))
    checks.append(ok("Rosetta reconstructs Phi3=13 and Phi6=7", exact(rosetta["reconstructed_cyclotomic_data"]["phi3"]) == "13" and exact(rosetta["reconstructed_cyclotomic_data"]["phi6"]) == "7", rosetta["reconstructed_cyclotomic_data"]))
    checks.append(ok("Rosetta reconstructs SRG(40,12,2,4)", rosetta["reconstructed_srg_data"] == {"v": 40, "k": 12, "lambda": 2, "mu": 4}, rosetta["reconstructed_srg_data"]))
    checks.append(ok("Rosetta reconstructs spectrum (12,2,-4)", rosetta["reconstructed_spectral_data"] == {"k": 12, "r": 2, "s": -4}, rosetta["reconstructed_spectral_data"]))
    checks.append(ok("Rosetta matches live data", all_true(rosetta["matches_live_rosetta_data"]), rosetta["matches_live_rosetta_data"]))
    checks.append(ok("Rosetta promoted observables all match", all_promoted_observables_match(rosetta), rosetta["promoted_observables_from_reconstructed_graph_data"]))
    checks.append(ok("Rosetta samples are constant", rosetta["all_samples_constant"] is True, rosetta["sample_reconstructions"]))

    checks.append(ok("Weinberg master variable is 3/13", exact(weinberg["master_variable"]["exact"]) == "3/13", weinberg["master_variable"]))
    checks.append(ok("Weinberg curved formula is x = 9 * c_EH,cont / c_6", weinberg["curved_reconstruction_formula"] == "x = 9 * c_EH,cont / c_6", weinberg["curved_reconstruction_formula"]))
    checks.append(ok("Weinberg reconstruction matches on all curved samples", all(sample["matches_master_variable"] is True and exact(sample["reconstructed_x"]) == "3/13" for sample in weinberg["curved_samples"]), weinberg["curved_samples"]))
    checks.append(ok("Weinberg exceptional reconstruction matches", weinberg["exceptional_reconstruction"]["matches_master_variable"] is True and exact(weinberg["exceptional_reconstruction"]["reconstructed_x"]) == "3/13", weinberg["exceptional_reconstruction"]))

    checks.append(ok("rank-39 lock is exact", discrete_eh == 39 * continuum_eh, coefficient_package))
    checks.append(ok("topological ratio is Phi6=7", topological_a2 / continuum_eh == 7, coefficient_package))
    checks.append(ok("discrete-to-continuum ratio is 39", discrete_eh / continuum_eh == 39, coefficient_package))
    checks.append(ok("curved Weinberg roundtrip gives 9", master_x * discrete_eh / continuum_eh == 9, coefficient_package))

    verified = all(check["passed"] for check in checks)
    return {
        "part": "CCCCXXVIII",
        "title": "Photonic Curved Einstein-Hilbert Extractor",
        "verified": verified,
        "checks_total": len(checks),
        "checks_passed": sum(check["passed"] for check in checks),
        "coefficient_package": coefficient_package,
        "protected_photonic_handoff": {
            "source_part": "CCCCXXVII",
            "active_code": handoff["protected_finite_kernel"]["active_code"],
            "h1_logical": handoff["protected_finite_kernel"]["h1_logical"],
            "selector_trits": handoff["protected_finite_kernel"]["selector_trits"],
            "edge_carrier": handoff["protected_finite_kernel"]["edge_carrier"],
            "curved_seeds": handoff["curved_external_seeds"],
            "logical_harmonic_channels": handoff["logical_harmonic_channels"],
        },
        "extractor_stack": {
            "projector_polynomial": projector["tower_characteristic_polynomial"],
            "shift_projectors": projector["shift_projectors"],
            "residue_generating_function": residue["generating_function"]["formula"],
            "continuum_formula": continuum["extractor_formulas"]["continuum_eh"],
            "curved_sample_count": len(continuum_samples),
            "curved_sample_seeds": sorted({explicit_seed_name(sample["seed_name"]) for sample in continuum_samples}),
        },
        "finite_roundtrip": {
            "chain_dimensions": {
                "c0": finite_geometry["line_count"],
                "c1": finite_geometry["edge_count"],
                "c2": finite_geometry["triangle_count"],
                "c3": finite_geometry["tetrahedron_count"],
            },
            "boundary_ranks": finite_hodge["boundary_ranks"],
            "betti_numbers": finite_hodge["betti_numbers"],
            "df2_spectrum": df2_spectrum,
            "seeley_dewitt_moments": finite_package["seeley_dewitt_moments"],
        },
        "inverse_rosetta": {
            "q": rosetta["reconstructed_cyclotomic_data"]["q"],
            "phi3": exact(rosetta["reconstructed_cyclotomic_data"]["phi3"]),
            "phi6": exact(rosetta["reconstructed_cyclotomic_data"]["phi6"]),
            "srg": rosetta["reconstructed_srg_data"],
            "spectrum": rosetta["reconstructed_spectral_data"],
        },
        "architecture_upgrade": (
            "The CCCCXXVII finite-to-curved handoff now has an exact EH "
            "coefficient extractor attached to it. The protected photonic "
            "runtime supplies H1=81, the [[82320,81,>=81]] code, and the "
            "40-trit selector; the curved CP2_9/K3_16 refinement tower supplies "
            "projectors and residues that recover c6=12480, cEH=320, a2=2240, "
            "and x=3/13 exactly."
        ),
        "theorem": (
            "On each explicit curved seed, three successive refinement samples "
            "split into 120-, 6-, and 1-mode channels. The 6-mode projector and "
            "the corresponding residue both recover c6=12480, rank-39 "
            "normalization gives cEH=320, and the same samples reconstruct the "
            "finite package D_F^2={0^82,4^320,10^48,16^30} with moments "
            "(480,2240,17600). The Rosetta inverse recovers SRG(40,12,2,4), "
            "Phi3=13, Phi6=7, and x=3/13."
        ),
        "honesty_boundary": (
            "This is an exact coefficient-extractor and roundtrip theorem for "
            "the current finite-plus-curved package. It is still not the final "
            "Einstein-Hilbert spectral-action asymptotic theorem for a smooth "
            "continuum limit."
        ),
        "checks": checks,
    }


def main() -> int:
    results = build_results()
    out = ROOT / "PART_CCCCXXVIII_photonic_curved_eh_extractor_results.json"
    out.write_text(json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "part": results["part"],
                "verified": results["verified"],
                "checks_passed": results["checks_passed"],
                "checks_total": results["checks_total"],
                "discrete_eh": results["coefficient_package"]["discrete_eh"],
                "continuum_eh": results["coefficient_package"]["continuum_eh"],
                "master_variable": results["coefficient_package"]["master_variable"],
                "out_path": str(out),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
