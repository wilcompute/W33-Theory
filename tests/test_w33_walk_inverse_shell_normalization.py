import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec is not None and spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_walk_inverse_shell_normalization_packet():
    walk_module = _load_module(
        ROOT / "analysis" / "w33_walk_inverse_shell_normalization.py",
        "w33_walk_inverse_shell_normalization",
    )
    packet = walk_module.walk_inverse_shell_normalization_packet()

    assert packet["walk_inverse_shell_normalization_detected"]

    params = packet["parameters"]
    assert params["q"] == 3
    assert params["v"] == 40
    assert params["k"] == 12
    assert params["floor"]["fraction"] == "1/12"
    assert params["nonneighbors"] == 27

    normalization = packet["normalization"]
    assert normalization["transition_matrix"] == "P = A/12"
    assert normalization["inverse_relation"] == "P^-1 = 12 A^-1"
    assert normalization["integer_scaled_relation"] == "2 P^-1 = 6I + 3A - J"
    assert normalization["inverse_identity"] == "P(6I + 3A - J) = 2I"
    assert normalization["floor_recovered_as_adjacent_entry_over_k"]

    entries = packet["entry_values"]
    assert entries["diagonal"]["fraction"] == "5/2"
    assert entries["adjacent"]["fraction"] == "1"
    assert entries["nonedge"]["fraction"] == "-1/2"
    assert entries["twice_diagonal"]["fraction"] == "5"
    assert entries["twice_adjacent"]["fraction"] == "2"
    assert entries["twice_nonedge"]["fraction"] == "-1"

    shells = packet["shell_contributions"]
    assert shells["diagonal"]["fraction"] == "5/2"
    assert shells["adjacent_shell"]["fraction"] == "12"
    assert shells["nonedge_shell"]["fraction"] == "-27/2"
    assert shells["row_sum"]["fraction"] == "1"

    moments = packet["raw_walk_inverse_moments"]
    assert moments["total_entry_sum"]["fraction"] == "40"
    assert moments["trace_P_inverse"]["fraction"] == "100"
    assert moments["frobenius_square_P_inverse"]["fraction"] == "1000"
    assert moments["positive_integer_ladder"] == [40, 100, 1000]
    assert moments["equals_mcxliv_floor_scaled_ladder"]

    spectrum = packet["spectrum"]
    assert spectrum["P_eigenvalues"]["trivial"]["fraction"] == "1"
    assert spectrum["P_eigenvalues"]["positive"]["fraction"] == "1/6"
    assert spectrum["P_eigenvalues"]["negative"]["fraction"] == "-1/3"
    assert spectrum["P_inverse_eigenvalues"]["trivial"]["fraction"] == "1"
    assert spectrum["P_inverse_eigenvalues"]["positive"]["fraction"] == "6"
    assert spectrum["P_inverse_eigenvalues"]["negative"]["fraction"] == "-3"
    assert spectrum["multiplicities"] == {"trivial": 1, "positive": 24, "negative": 15}
    assert spectrum["spectral_trace"]["fraction"] == "100"
    assert spectrum["spectral_frobenius_square"]["fraction"] == "1000"
    assert spectrum["spectral_moments_match_shell_moments"]

    integer = packet["integer_shell_kernel"]
    assert integer["kernel"] == "2P^-1"
    assert integer["diagonal"] == 5
    assert integer["adjacent"] == 2
    assert integer["nonedge"] == -1
    assert integer["row_sum"] == 2
    assert integer["trace"] == 200
    assert integer["frobenius_square"] == 4000
