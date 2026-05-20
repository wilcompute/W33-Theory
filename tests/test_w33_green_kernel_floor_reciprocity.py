import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec is not None and spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_green_kernel_floor_reciprocity_packet():
    green = _load_module(
        ROOT / "analysis" / "w33_green_kernel_floor_reciprocity.py",
        "w33_green_kernel_floor_reciprocity",
    )
    packet = green.green_kernel_floor_reciprocity_packet()

    assert packet["green_kernel_floor_reciprocity_detected"]

    params = packet["parameters"]
    assert params["q"] == 3
    assert params["v"] == 40
    assert params["k"] == 12
    assert params["lambda"] == 2
    assert params["mu"] == 4
    assert params["nonneighbors"] == 27

    inverse = packet["inverse_coefficients"]
    assert inverse["I"]["fraction"] == "1/4"
    assert inverse["A"]["fraction"] == "1/8"
    assert inverse["J"]["fraction"] == "-1/24"
    assert inverse["formula"] == "A^-1 = I/4 + A/8 - J/24 = (6I + 3A - J)/24"

    scaled = packet["integer_scaled_inverse"]
    assert scaled["denominator"] == 24
    assert scaled["I"] == 6
    assert scaled["A"] == 3
    assert scaled["J"] == -1
    assert scaled["lhs_coefficients_after_srg_reduction"] == {"I": 24, "A": 0, "J": 0}
    assert scaled["verified"]

    entries = packet["entry_values"]
    assert entries["diagonal"]["fraction"] == "5/24"
    assert entries["adjacent"]["fraction"] == "1/12"
    assert entries["nonedge"]["fraction"] == "-1/24"

    shells = packet["shell_contributions"]
    assert shells["diagonal"]["fraction"] == "5/24"
    assert shells["adjacent_shell"]["fraction"] == "1"
    assert shells["nonedge_shell"]["fraction"] == "-9/8"
    assert shells["row_sum"]["fraction"] == "1/12"

    floor = packet["floor_equalities"]
    assert floor["all_equal"]
    assert floor["mcxli_mcxlii_floor"]["fraction"] == "1/12"
    assert floor["valency_reciprocal"]["fraction"] == "1/12"
    assert floor["green_adjacent_entry"]["fraction"] == "1/12"
    assert floor["green_row_sum"]["fraction"] == "1/12"

    reciprocity = packet["reciprocity"]
    assert reciprocity["diagonal_over_floor"]["fraction"] == "5/2"
    assert reciprocity["nonedge_over_floor"]["fraction"] == "-1/2"
    assert reciprocity["diagonal_is_five_halves_floor"]
    assert reciprocity["nonedge_is_minus_half_floor"]
    assert reciprocity["adjacent_minus_nonedge"]["fraction"] == "1/8"
    assert reciprocity["adjacent_minus_nonedge_is_1_over_2mu"]
    assert reciprocity["neighbor_shell_is_unit"]

    trace = packet["trace_data"]
    assert trace["trace_A_inverse"]["fraction"] == "25/3"
    assert trace["total_entry_sum"]["fraction"] == "10/3"
    assert trace["frobenius_square_trace_A_inverse_squared"]["fraction"] == "125/18"
