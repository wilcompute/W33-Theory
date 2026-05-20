import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec is not None and spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_horizon_parity_floor_duality_packet():
    duality = _load_module(
        ROOT / "analysis" / "w33_horizon_parity_floor_duality.py",
        "w33_horizon_parity_floor_duality",
    )
    packet = duality.horizon_parity_floor_duality_packet()

    assert packet["horizon_parity_floor_duality_detected"]
    assert packet["horizon"]["total"] == 72
    assert packet["horizon"]["payload_edges"] == 66
    assert packet["horizon"]["parity_symbols"] == 6
    assert packet["horizon"]["parity_symbols_are_q_factorial"]
    assert packet["horizon"]["rate"]["fraction"] == "11/12"
    assert packet["horizon"]["redundancy"]["fraction"] == "1/12"
    assert packet["horizon"]["rate_plus_redundancy"]["fraction"] == "1"
    assert packet["horizon"]["rate_is_one_minus_floor"]

    floor = packet["floor_duals"]
    assert floor["all_equal"]
    assert floor["ym_substrate_floor"]["fraction"] == "1/12"
    assert floor["horizon_redundancy"]["fraction"] == "1/12"
    assert floor["normalized_chiral_discriminant_density"]["fraction"] == "1/12"
    assert floor["absolute_zeta_minus_one"]["fraction"] == "1/12"
    assert floor["valency_reciprocal"]["fraction"] == "1/12"

    chiral = packet["chiral_discriminant"]
    assert chiral["value"] == 31104
    assert chiral["closed_form"] == "72^2 * 6"
    assert chiral["normalized_by_horizon_cubed"]["fraction"] == "1/12"
    assert chiral["sqrt_form"] == "72 * sqrt(6)"

    grid = packet["grid_split"]
    assert grid["pure_edges"] == 30
    assert grid["corrected_mixed"] == 42
    assert grid["six_floor_rescales_grid_split_integrally"]
    assert grid["six_floor_times_pure_edges"]["fraction"] == "15"
    assert grid["six_floor_times_corrected_mixed"]["fraction"] == "21"

    cross = packet["cross_branch"]
    assert cross["ns_decay_over_floor"]["fraction"] == "2"
    assert cross["ns_decay_is_two_floor"]
    assert cross["horizon_redundancy_is_corrected_floor"]
    assert cross["payload_rate_is_chiral_rate"]
