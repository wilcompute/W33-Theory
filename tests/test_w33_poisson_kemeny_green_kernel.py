import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec is not None and spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_poisson_kemeny_green_kernel_packet():
    poisson = _load_module(
        ROOT / "analysis" / "w33_poisson_kemeny_green_kernel.py",
        "w33_poisson_kemeny_green_kernel",
    )
    packet = poisson.poisson_kemeny_green_kernel_packet()

    assert packet["poisson_kemeny_green_kernel_detected"]

    params = packet["parameters"]
    assert params["q"] == 3
    assert params["v"] == 40
    assert params["k"] == 12
    assert params["floor"]["fraction"] == "1/12"
    assert params["stationary_entry"]["fraction"] == "1/40"
    assert params["edges"] == 240
    assert params["nonedge_pairs"] == 540

    spectrum = packet["poisson_spectrum"]
    assert spectrum["P_eigenvalues"]["stationary"]["fraction"] == "1"
    assert spectrum["P_eigenvalues"]["positive"]["fraction"] == "1/6"
    assert spectrum["P_eigenvalues"]["negative"]["fraction"] == "-1/3"
    assert spectrum["Z_eigenvalues"]["stationary"]["fraction"] == "1"
    assert spectrum["Z_eigenvalues"]["positive"]["fraction"] == "6/5"
    assert spectrum["Z_eigenvalues"]["negative"]["fraction"] == "3/4"
    assert spectrum["centered_Z_minus_Pi_eigenvalues"]["stationary"]["fraction"] == "0"
    assert spectrum["multiplicities"] == {"stationary": 1, "positive": 24, "negative": 15}

    kernel = packet["poisson_kernel"]
    assert kernel["coefficients"]["I"]["fraction"] == "21/20"
    assert kernel["coefficients"]["A"]["fraction"] == "3/40"
    assert kernel["coefficients"]["J"]["fraction"] == "-19/800"
    assert kernel["entry_values"]["diagonal"]["fraction"] == "821/800"
    assert kernel["entry_values"]["adjacent"]["fraction"] == "41/800"
    assert kernel["entry_values"]["nonedge"]["fraction"] == "-19/800"
    assert kernel["shell_row_sum"]["fraction"] == "1"
    assert kernel["trace"]["fraction"] == "821/20"

    centered = packet["centered_poisson_kernel"]
    assert centered["coefficients"]["J"]["fraction"] == "-39/800"
    assert centered["entry_values"]["diagonal"]["fraction"] == "801/800"
    assert centered["entry_values"]["adjacent"]["fraction"] == "21/800"
    assert centered["entry_values"]["nonedge"]["fraction"] == "-39/800"
    assert centered["shell_row_sum"]["fraction"] == "0"
    assert centered["trace"]["fraction"] == "801/20"
    assert centered["diagonal_equals_kemeny_per_vertex"]

    kemeny = packet["kemeny"]
    assert kemeny["constant"]["fraction"] == "801/20"
    assert kemeny["trace_Z_minus_one"]["fraction"] == "801/20"
    assert kemeny["per_vertex"]["fraction"] == "801/800"

    hitting = packet["hitting_times"]
    assert hitting["adjacent"]["fraction"] == "39"
    assert hitting["nonedge"]["fraction"] == "42"
    assert hitting["nonedge_minus_adjacent"]["fraction"] == "3"
    assert hitting["nonedge_minus_adjacent_equals_q"]

    resistance = packet["commute_and_resistance"]
    assert resistance["commute_adjacent"]["fraction"] == "78"
    assert resistance["commute_nonedge"]["fraction"] == "84"
    assert resistance["effective_resistance_adjacent"]["fraction"] == "13/80"
    assert resistance["effective_resistance_nonedge"]["fraction"] == "7/40"
    assert resistance["kirchhoff_index"]["fraction"] == "267/2"
    assert resistance["kirchhoff_from_shell_counts"]
