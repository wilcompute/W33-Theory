from __future__ import annotations

from pathlib import Path
import json

from exploration.w33_electron_seed_packet_bridge import (
    build_electron_seed_packet_summary,
    write_summary,
)
from scripts.w33_electron_seed_packet_audit import analyze, classify_electron_seed_boundary


def test_electron_seed_bridge_packages_the_exact_three_factor_packet(tmp_path: Path) -> None:
    summary = build_electron_seed_packet_summary()
    packet = summary["exact_packet_dictionary"]
    ratios = summary["candidate_ratio_dictionary"]
    theorem = summary["electron_seed_packet_theorem"]
    shadow = summary["graph_fixed_candidate_mass_shadow"]

    assert summary["status"] == "ok"
    assert packet["factor_packet"] == [98, 17, 208]
    assert packet["candidate_denominator_mt_over_me"]["exact"] == "346528"
    assert packet["candidate_denominator_prime_factorization"] == "2^5 * 7^2 * 13 * 17"
    assert ratios["me_over_mt_candidate"]["exact"] == "1/346528"
    assert ratios["mt_over_mu_candidate"]["exact"] == "1666"
    assert ratios["mc_over_mu_candidate"]["exact"] == "49/4"
    assert ratios["mu_shell_over_f4_dimension"]["exact"] == "4"

    assert theorem["barrier_shell_is_lambda_phi6_squared"] is True
    assert theorem["shifted_gaussian_norm_is_mu_squared_plus_one"] is True
    assert theorem["charged_lepton_shell_is_phi3_mu_squared"] is True
    assert theorem["charged_lepton_shell_is_mu_times_f4_dimension"] is True
    assert theorem["candidate_denominator_is_barrier_times_shift_times_muon_shell"] is True
    assert theorem["candidate_top_over_muon_is_barrier_times_shift"] is True
    assert theorem["candidate_charm_over_muon_is_phi6_squared_over_mu"] is True
    assert theorem["remaining_fermion_frontier_reduces_to_one_exact_three_factor_packet"] is True
    assert theorem["physical_electron_identification_remains_open"] is True

    assert shadow["mt_gev"]["exact"] == "123*sqrt(2)"
    assert round(shadow["me_candidate_mev"]["float"], 6) == 0.501975
    assert round(shadow["mmu_candidate_mev"]["float"], 6) == 104.410725

    out = tmp_path / "summary.json"
    write_summary(out)
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["exact_packet_dictionary"]["candidate_denominator_mt_over_me"]["exact"] == "346528"


def test_electron_seed_audit_keeps_the_boundary_honest() -> None:
    records = {record["name"]: record for record in classify_electron_seed_boundary()}
    payload = analyze()
    theorem = payload["electron_seed_boundary_theorem"]

    assert records["one_input_fermion_reduction"]["support_level"] == "repo-exact reduction"
    assert records["exact_residual_electron_seed_packet"]["support_level"] == "repo-exact packet"
    assert records["same_seed_touches_exceptional_f4_scale"]["support_level"] == "repo-exact splice"
    assert (
        records["graph_fixed_candidate_mass_shadow"]["support_level"]
        == "exact packet, not final physical identification"
    )

    assert payload["status"] == "ok"
    assert payload["record_names_exact_or_boundary"] == (
        "one_input_fermion_reduction",
        "exact_residual_electron_seed_packet",
        "same_seed_touches_exceptional_f4_scale",
        "graph_fixed_candidate_mass_shadow",
    )
    assert theorem["the_dimensionless_fermion_ladder_is_already_reduced_to_one_seed"] is True
    assert theorem["the_residual_seed_is_now_packaged_as_the_exact_factor_packet_98_17_208"] is True
    assert theorem["the_same_packet_splices_into_the_exact_f4_scale"] is True
    assert theorem["the_remaining_wall_is_physical_identification_not_missing_factor_arithmetic"] is True
    assert "98 x 17 x 208" in payload["boundary_note"]
