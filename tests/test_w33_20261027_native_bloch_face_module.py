"""Independent checks of native translated loops and the propagation repair."""
import sys
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "analysis"))
import w33_20261027_native_bloch_face_module as audit


def test_exact_generic_rank_and_commutator_closure():
    B, V, edges, lookup, nbr = audit.geometry()
    _, periods, comm = audit.deck_loops(edges, V)
    assert round(np.linalg.det(periods)) == 1
    assert [len(f) for f in comm] == [16] * 6
    for face in comm:
        vertex = 0
        position = np.zeros(4, dtype=int)
        for e, sign in face:
            a, b = edges[e] if sign == 1 else edges[e][::-1]
            assert vertex == a
            vertex = b
            position += sign * V[e]
        assert vertex == 0 and not position.any()
    faces, _ = audit.enumerate_faces(V, lookup, nbr)
    assert audit.modular_witness(faces + comm, V, edges)["curl_rank"] == 108


def test_vertex_voltage_gauge_preserves_transverse_spectrum():
    B, V, edges, lookup, nbr = audit.geometry()
    faces, _ = audit.enumerate_faces(V, lookup, nbr)
    _, _, comm = audit.deck_loops(edges, V)
    faces += comm
    offsets = np.random.default_rng(10272026).integers(-2, 3, size=(27, 4))
    transformed = V + B @ offsets
    k = np.array([.17, -.23, .31, .11])
    eigen = []
    for voltage in (V, transformed):
        F = audit.curl(faces, voltage, k)
        D = audit.gradient(voltage, edges, k)
        assert np.max(abs(F @ D)) < 2e-12
        _, ev = audit.transverse(F, D)
        eigen.append(ev)
    assert np.max(abs(eigen[0] - eigen[1])) < 1e-10


def test_frozen_integral_and_effective_symbol_regression():
    import json
    d = json.loads((audit.ROOT / "data/w33_20261027_native_bloch_face_module.json").read_text())
    assert d["integral_selected105"]["nonzero_smith_invariants"] == {"1": 105}
    assert d["exact_generic_rank_witnesses"]["completed111"]["curl_rank"] == 108
    for rec in d["bloch_cases"][1:]:
        assert rec["selected105"]["physical_zero_modes"] == 3
        assert rec["completed111"]["physical_zero_modes"] == 0
    B, V, edges, _, _ = audit.geometry()
    _, periods, _ = audit.deck_loops(edges, V)
    result = audit.effective_symbol(B, V, periods, d["completed_scaling"])
    assert len(set(result["e1_numeric_squared_speeds"])) == 3


def test_engineered_metric_matches_scalar_symbol_and_sampled_limit():
    import json
    d = json.loads((audit.ROOT / "data/w33_20261027_native_bloch_face_module.json").read_text())
    B, V, edges, _, _ = audit.geometry()
    _, periods, _ = audit.deck_loops(edges, V)
    H, result = audit.matched_loop_metric(B, V, periods)
    assert np.linalg.eigvalsh(np.array(H, dtype=float)).min() > 0
    G = np.array(d["effective_symbol"]["harmonic_link_gram_M"], dtype=float)/27
    for ray in d["engineered_matched_scaling"]:
        n = np.array(ray["direction"])
        target = n @ G @ n
        first = np.array(ray["samples"][0]["lambda_over_t2"])
        last = np.array(ray["samples"][-1]["lambda_over_t2"])
        assert np.max(abs(last-target)) < np.max(abs(first-target))
        assert np.max(abs(last-target))/target < .01
