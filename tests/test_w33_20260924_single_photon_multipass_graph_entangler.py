import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis/w33_20260924_single_photon_multipass_graph_entangler.py"


def load_module():
    spec = importlib.util.spec_from_file_location("multipass10942", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def test_even_sweep_edge_triangle_numbers():
    mod = load_module()
    expected = {2: 1, 4: 3, 6: 6, 8: 10}
    for k, edges in expected.items():
        A = mod.adjacency_for_even_sweep(k)
        assert sum(int(A[i, j] != 0) for i in range(k) for j in range(i + 1, k)) == edges


def test_basis_amplitude_formula_through_eight_memories():
    mod = load_module()
    for k in (2, 4, 6, 8):
        error, _ = mod.verify_k(k, samples=24)
        assert error < mod.TOL


def test_measurement_dependence_is_only_local_x_frame():
    mod = load_module()
    assert mod.output_x_frame(2, 1) == [1, 0]
    assert mod.output_x_frame(4, 1) == [2, 0, 1, 0]
    assert mod.output_x_frame(6, 2) == [2, 0, 1, 0, 2, 0]


def test_four_memory_weighted_graph():
    mod = load_module()
    A = mod.adjacency_for_even_sweep(4)
    edges = {(i, j): int(A[i, j]) for i in range(4) for j in range(i + 1, 4) if A[i, j]}
    assert edges == {(0, 1): 1, (0, 3): 2, (2, 3): 1}
