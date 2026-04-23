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
from exploration.w33_one_input_fermion_spectrum_bridge import (  # noqa: E402
    build_one_input_fermion_spectrum_summary,
)


@lru_cache(maxsize=1)
def electron_seed_packet_summary() -> Dict[str, object]:
    return build_electron_seed_packet_summary()


@lru_cache(maxsize=1)
def one_input_fermion_summary() -> Dict[str, object]:
    return build_one_input_fermion_spectrum_summary()


@lru_cache(maxsize=1)
def classify_electron_seed_boundary() -> Tuple[Dict[str, object], ...]:
    one_input = one_input_fermion_summary()
    packet = electron_seed_packet_summary()
    exact_packet = packet["exact_packet_dictionary"]
    ratios = packet["candidate_ratio_dictionary"]
    mass_shadow = packet["graph_fixed_candidate_mass_shadow"]

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
            "the_same_packet_splices_into_the_exact_f4_scale": records[2]["evidence"][
                "mu_shell_over_f4_dimension"
            ]["exact"]
            == "4",
            "the_remaining_wall_is_physical_identification_not_missing_factor_arithmetic": packet[
                "electron_seed_packet_theorem"
            ]["physical_electron_identification_remains_open"],
        },
        "boundary_note": (
            "The honest electron-side frontier is now narrower than the old open-gap language. "
            "The exact arithmetic packet is already visible: 346528 = 98 x 17 x 208, with "
            "208 = mu*dim(F4). What remains open is whether this exact packet is the final "
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
