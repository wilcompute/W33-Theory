from __future__ import annotations

from scripts.SOLVE_RG_NEUTRINO import (
    CURRENT_PRESET_NAME,
    LEGACY_PRESET_NAME,
    build_results,
)
from scripts.w33_neutrino_preset_audit import analyze


def test_current_official_preset_keeps_1_over_mu_as_the_lowest_sum_branch() -> None:
    current = build_results(preset_name=CURRENT_PRESET_NAME)

    assert round(current["1/mu"]["NH"]["sum_meV"], 6) == 101.206465
    assert round(current["1/mu"]["IH"]["sum_meV"], 6) == 109.744386

    nh_order = sorted(
        ((label, entry["NH"]["sum_meV"]) for label, entry in current.items()),
        key=lambda item: item[1],
    )
    ih_order = sorted(
        ((label, entry["IH"]["sum_meV"]) for label, entry in current.items()),
        key=lambda item: item[1],
    )

    assert tuple(label for label, _ in nh_order) == ("1/mu", "1/6", "1/Phi6", "1/Phi3", "1/(2k-1)")
    assert tuple(label for label, _ in ih_order) == ("1/mu", "1/6", "1/Phi6", "1/Phi3", "1/(2k-1)")


def test_neutrino_preset_audit_proves_the_stable_cross_preset_ordering() -> None:
    payload = analyze()
    theorem = payload["cross_preset_theorem"]
    legacy = payload["presets"][LEGACY_PRESET_NAME]
    current = payload["presets"][CURRENT_PRESET_NAME]

    assert theorem["nh_minimum_is_always_1_over_mu"] is True
    assert theorem["ih_minimum_is_always_1_over_mu"] is True
    assert theorem["nh_fixed_point_ordering_is_stable_across_supported_presets"] is True
    assert theorem["ih_fixed_point_ordering_is_stable_across_supported_presets"] is True
    assert theorem["latest_official_shift_from_legacy_is_sub_mev_in_nh"] is True
    assert theorem["latest_official_shift_from_legacy_is_sub_mev_in_ih"] is True

    assert round(legacy["nh_sums_meV"]["1/mu"], 6) == 101.518066
    assert round(current["nh_sums_meV"]["1/mu"], 6) == 101.206465
    assert round(current["ih_sums_meV"]["1/mu"], 6) == 109.744386
