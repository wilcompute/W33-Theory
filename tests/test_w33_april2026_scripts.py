from __future__ import annotations

import json

from scripts.SOLVE_RG_NEUTRINO import (
    LEGACY_PRESET_NAME,
    W33_TARGETS,
    build_results,
    solve_IH,
    solve_NH,
    write_results,
)
from scripts.w33_tau_extended import TAU, verify_ring_formulas


def test_rg_neutrino_fixed_points_match_the_checked_artifact_values(tmp_path) -> None:
    results = build_results(preset_name=LEGACY_PRESET_NAME)

    assert tuple(results) == ("1/mu", "1/Phi6", "1/Phi3", "1/(2k-1)", "1/6")
    assert round(results["1/mu"]["NH"]["sum_meV"], 6) == 101.518066
    assert round(results["1/mu"]["IH"]["sum_meV"], 6) == 110.328209
    assert round(results["1/Phi6"]["NH"]["sum_meV"], 6) == 139.985997
    assert round(results["1/Phi3"]["IH"]["sum_meV"], 6) == 160.845646

    nh = solve_NH(W33_TARGETS["1/mu"], preset_name=LEGACY_PRESET_NAME)
    ih = solve_IH(W33_TARGETS["1/mu"], preset_name=LEGACY_PRESET_NAME)
    assert nh is not None and ih is not None
    assert round(nh["sum_meV"], 6) == 101.518066
    assert round(ih["sum_meV"], 6) == 110.328209

    output_path = write_results(results, tmp_path / "rg_neutrino_results.json", preset_name=LEGACY_PRESET_NAME)
    payload = json.loads(output_path.read_text(encoding="utf-8"))
    assert round(payload["1/6"]["NH"]["sum_meV"], 6) == 128.262091


def test_tau_ring_formulas_hold_on_the_live_legacy_packet() -> None:
    assert verify_ring_formulas() is True
    assert TAU[2] == -24
    assert TAU[3] == 252
    assert TAU[5] == 4830
    assert TAU[7] == -16744
    assert TAU[23] == 18643272
