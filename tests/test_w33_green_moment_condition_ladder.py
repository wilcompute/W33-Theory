import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec is not None and spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_green_moment_condition_ladder_packet():
    ladder_module = _load_module(
        ROOT / "analysis" / "w33_green_moment_condition_ladder.py",
        "w33_green_moment_condition_ladder",
    )
    packet = ladder_module.green_moment_condition_ladder_packet()

    assert packet["green_moment_condition_ladder_detected"]

    params = packet["parameters"]
    assert params["q"] == 3
    assert params["v"] == 40
    assert params["k"] == 12
    assert params["floor"]["fraction"] == "1/12"

    moments = packet["green_moments"]
    assert moments["total_entry_sum"]["fraction"] == "10/3"
    assert moments["trace_A_inverse"]["fraction"] == "25/3"
    assert moments["inverse_frobenius_square"]["fraction"] == "125/18"
    assert moments["trace_over_total"]["fraction"] == "5/2"
    assert moments["total_equals_v_floor"]
    assert moments["trace_equals_100_floor"]
    assert moments["frobenius_square_equals_1000_floor_squared"]

    ladder = packet["floor_scaled_ladder"]
    assert ladder["total_over_floor"]["fraction"] == "40"
    assert ladder["trace_over_floor"]["fraction"] == "100"
    assert ladder["inverse_frobenius_over_floor_square"]["fraction"] == "1000"
    assert ladder["positive_integer_ladder"] == [40, 100, 1000]
    assert ladder["trace_is_five_halves_total"]
    assert ladder["inverse_frobenius_is_ten_floor_trace"]
    assert ladder["inverse_frobenius_is_twenty_five_floor_total"]
    assert ladder["inverse_frobenius_over_floor_trace"]["fraction"] == "10"
    assert ladder["inverse_frobenius_over_floor_total"]["fraction"] == "25"

    adjacency = packet["adjacency_dual"]
    assert adjacency["adjacency_frobenius_square"]["fraction"] == "480"
    assert adjacency["adjacency_frobenius_square_equals_v_over_floor"]
    assert adjacency["adjacency_frobenius_square_times_floor"]["fraction"] == "40"

    conditioning = packet["conditioning"]
    assert conditioning["spectral_condition_number"]["fraction"] == "6"
    assert conditioning["spectral_condition_number_is_one_over_two_floor"]
    assert conditioning["spectral_condition_number_times_floor"]["fraction"] == "1/2"
    assert conditioning["frobenius_condition_square"]["fraction"] == "10000/3"
    assert conditioning["q_scaled_frobenius_condition_square"]["fraction"] == "10000"
    assert conditioning["q_scaled_frobenius_condition_square_equals_trace_ratio_square"]
