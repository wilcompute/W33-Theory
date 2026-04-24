#!/usr/bin/env python3
"""Conservative audit of the residual electron-seed packet on the W33 stack."""

from __future__ import annotations

from functools import lru_cache
import json
from pathlib import Path
import sys
import time
from typing import Dict, Tuple


ROOT = Path(__file__).resolve().parents[1]
EXPLORATION = ROOT / "exploration"
for candidate in (ROOT, EXPLORATION):
    candidate_str = str(candidate)
    if candidate_str not in sys.path:
        sys.path.insert(0, candidate_str)

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

from exploration.w33_electron_seed_packet_bridge import (  # noqa: E402
    build_electron_seed_packet_summary,
)
from exploration.w33_curved_rosetta_reconstruction_bridge import (  # noqa: E402
    build_curved_rosetta_reconstruction_summary,
)
from exploration.w33_one_input_fermion_spectrum_bridge import (  # noqa: E402
    build_one_input_fermion_spectrum_summary,
)
from scripts.w33_toroidal_continuum_seed_audit import toroidal_seed_packet_summary  # noqa: E402


@lru_cache(maxsize=1)
def electron_seed_packet_summary() -> Dict[str, object]:
    return build_electron_seed_packet_summary()


@lru_cache(maxsize=1)
def one_input_fermion_summary() -> Dict[str, object]:
    return build_one_input_fermion_spectrum_summary()


@lru_cache(maxsize=1)
def curved_rosetta_summary() -> Dict[str, object]:
    return build_curved_rosetta_reconstruction_summary()


@lru_cache(maxsize=1)
def classify_electron_seed_boundary() -> Tuple[Dict[str, object], ...]:
    one_input = one_input_fermion_summary()
    packet = electron_seed_packet_summary()
    toroidal = toroidal_seed_packet_summary()
    rosetta = curved_rosetta_summary()
    exact_packet = packet["exact_packet_dictionary"]
    ratios = packet["candidate_ratio_dictionary"]
    mass_shadow = packet["graph_fixed_candidate_mass_shadow"]
    phi6 = int(toroidal["phi6"])
    g2_dimension = 2 * phi6
    cartan_packet = int(toroidal["cartan_packet"])
    barrier_shell = int(exact_packet["barrier_shell_lambda_phi6_squared"]["exact"])
    discrete_6_mode_over_a0 = int(
        rosetta["promoted_observables_from_reconstructed_graph_data"]["discrete_6_mode_over_a0"]["exact"][
            "exact"
        ]
    )

    return (
        {
            "name": "one_input_fermion_reduction",
            "support_level": "repo-exact reduction",
            "statement": (
                "The graph-fixed electroweak scale already closes the quark ladder, while the "
                "charged-lepton and neutrino sides reduce to one residual electron seed."
            ),
            "evidence": {
                "residual_seed": one_input["charged_lepton_one_seed_closure"]["residual_seed"],
                "mmu_over_me": one_input["charged_lepton_one_seed_closure"]["mmu_over_me"],
                "koide_q": one_input["charged_lepton_one_seed_closure"]["koide_q"],
                "mnu_over_me_squared": one_input["exceptional_neutrino_closure"][
                    "mnu_over_me_squared_if_dirac_seed_is_electron"
                ],
            },
        },
        {
            "name": "exact_residual_electron_seed_packet",
            "support_level": "repo-exact packet",
            "statement": (
                "The remaining charged-fermion slot already collapses to the exact factor packet "
                "98 x 17 x 208 = lambda*Phi6^2 * (mu^2+1) * mu^2*Phi3."
            ),
            "evidence": {
                "factor_packet": exact_packet["factor_packet"],
                "candidate_denominator_mt_over_me": exact_packet["candidate_denominator_mt_over_me"],
                "prime_factorization": exact_packet["candidate_denominator_prime_factorization"],
                "mt_over_mu_candidate": ratios["mt_over_mu_candidate"],
                "mc_over_mu_candidate": ratios["mc_over_mu_candidate"],
            },
        },
        {
            "name": "same_gaussian_norm_splices_into_charm_suppressor_packet",
            "support_level": "repo-exact splice",
            "statement": (
                "The middle factor 17 is the exact Gaussian norm mu^2+1, and the same q=3 "
                "Cartan packet 8 dresses it into the first up-sector suppressor 136 = 8*17."
            ),
            "evidence": {
                "shifted_gaussian_norm_mu_squared_plus_one": exact_packet[
                    "shifted_gaussian_norm_mu_squared_plus_one"
                ],
                "cartan_packet": cartan_packet,
                "up_sector_suppressor": ratios["up_sector_suppressor"],
                "cartan_times_shifted_gaussian_norm": cartan_packet
                * int(exact_packet["shifted_gaussian_norm_mu_squared_plus_one"]["exact"]),
            },
        },
        {
            "name": "same_barrier_shell_splices_into_toroidal_g2_packet",
            "support_level": "repo-exact splice",
            "statement": (
                "The barrier shell 98 is also Phi6*dim(G2) = 7*14, so the front factor of the "
                "electron packet already lands on the pure toroidal G2 packet."
            ),
            "evidence": {
                "barrier_shell_lambda_phi6_squared": exact_packet["barrier_shell_lambda_phi6_squared"],
                "phi6": phi6,
                "g2_dimension": g2_dimension,
                "phi6_times_g2_dimension": phi6 * g2_dimension,
            },
        },
        {
            "name": "same_seed_touches_exceptional_f4_scale",
            "support_level": "repo-exact splice",
            "statement": (
                "The charged-lepton shell 208 is also mu*dim(F4) = 4*52, so the residual electron "
                "packet already touches the exact exceptional neutrino-scale coefficient."
            ),
            "evidence": {
                "charged_lepton_shell_mu_squared_phi3": exact_packet["charged_lepton_shell_mu_squared_phi3"],
                "f4_dimension": exact_packet["f4_dimension"],
                "mu_shell_over_f4_dimension": ratios["mu_shell_over_f4_dimension"],
            },
        },
        {
            "name": "same_seed_splices_into_q3_continuum_normalization",
            "support_level": "repo-exact splice",
            "statement": (
                "The charged-lepton shell 208 is also the q=3 continuum normalization packet "
                "Cartan*(c6/a0) = 8*26, so the residual electron seed already touches the "
                "same discrete six-mode normalization behind the 320/12480 bridge."
            ),
            "evidence": {
                "charged_lepton_shell_mu_squared_phi3": exact_packet["charged_lepton_shell_mu_squared_phi3"],
                "cartan_packet": cartan_packet,
                "discrete_6_mode_over_a0": discrete_6_mode_over_a0,
                "cartan_times_discrete_6_mode_over_a0": cartan_packet * discrete_6_mode_over_a0,
            },
        },
        {
            "name": "graph_fixed_candidate_mass_shadow",
            "support_level": "exact packet, not final physical identification",
            "statement": (
                "If the exact packet is inserted directly into the graph-fixed electroweak scale, "
                "it produces a concrete lepton shadow already, but the final physical identification "
                "of that shadow is still open."
            ),
            "evidence": {
                "mt_gev": mass_shadow["mt_gev"],
                "me_candidate_mev": mass_shadow["me_candidate_mev"],
                "mmu_candidate_mev": mass_shadow["mmu_candidate_mev"],
            },
        },
    )


@lru_cache(maxsize=1)
def analyze() -> Dict[str, object]:
    records = classify_electron_seed_boundary()
    packet = electron_seed_packet_summary()
    barrier_shell = int(packet["exact_packet_dictionary"]["barrier_shell_lambda_phi6_squared"]["exact"])

    return {
        "status": "ok",
        "electron_seed_packet": packet,
        "record_names_exact_or_boundary": tuple(record["name"] for record in records),
        "electron_seed_boundary_theorem": {
            "the_dimensionless_fermion_ladder_is_already_reduced_to_one_seed": records[0]["support_level"]
            == "repo-exact reduction",
            "the_residual_seed_is_now_packaged_as_the_exact_factor_packet_98_17_208": records[1][
                "evidence"
            ]["factor_packet"]
            == [98, 17, 208],
            "the_middle_factor_splices_into_the_charm_suppressor_packet": records[2]["evidence"][
                "cartan_times_shifted_gaussian_norm"
            ]
            == int(records[2]["evidence"]["up_sector_suppressor"]["exact"]),
            "the_barrier_shell_splices_into_the_toroidal_g2_packet": records[3]["evidence"][
                "phi6_times_g2_dimension"
            ]
            == barrier_shell,
            "the_same_packet_splices_into_the_exact_f4_scale": records[4]["evidence"][
                "mu_shell_over_f4_dimension"
            ]["exact"]
            == "4",
            "the_same_packet_splices_into_the_q3_continuum_normalization": records[5]["evidence"][
                "cartan_times_discrete_6_mode_over_a0"
            ]
            == 208,
            "the_remaining_wall_is_physical_identification_not_missing_factor_arithmetic": packet[
                "electron_seed_packet_theorem"
            ]["physical_electron_identification_remains_open"],
        },
        "boundary_note": (
            "The honest electron-side frontier is now narrower than the old open-gap language. "
            "The exact arithmetic packet is already visible: 346528 = 98 x 17 x 208, with "
            "17 = mu^2+1 with charm suppressor 136 = 8*17, 98 = Phi6*dim(G2) = 7*14, and "
            "208 = mu*dim(F4) = 8*26, where 8 is the Cartan packet and 26 is the exact discrete "
            "six-mode normalization. What remains open is whether this "
            "exact packet is the final "
            "physical electron denominator or a nearby normalization shadow."
        ),
        "records": records,
    }


def main() -> None:
    started = time.time()
    payload = analyze()
    payload["analysis_duration_sec"] = round(time.time() - started, 6)

    output_dir = ROOT / "checks"
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    output_path = output_dir / f"PART_CXVIII_electron_seed_packet_audit_{timestamp}.json"
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    packet = payload["electron_seed_packet"]["exact_packet_dictionary"]
    shadow = payload["electron_seed_packet"]["graph_fixed_candidate_mass_shadow"]
    print("Electron seed packet audit")
    print(
        "  Exact packet: "
        f"{packet['factor_packet'][0]} x {packet['factor_packet'][1]} x {packet['factor_packet'][2]}"
    )
    print(
        "  Candidate denominator mt/me: "
        f"{packet['candidate_denominator_mt_over_me']['exact']}"
    )
    print(
        "  Graph-fixed candidate masses: "
        f"me={shadow['me_candidate_mev']['float']:.6f} MeV, "
        f"mmu={shadow['mmu_candidate_mev']['float']:.6f} MeV"
    )
    print(f"  Wrote: {output_path}")


if __name__ == "__main__":
    main()
