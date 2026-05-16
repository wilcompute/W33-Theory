"""Part DCCLXIX -- Octahedral Laplacian W(3,3) spectrum tests."""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dcclxix_octahedral_laplacian_w33_spectrum import (  # noqa: E402
    E_W33,
    F_EIGEN,
    LAM,
    MU,
    OUT_PATH,
    Q,
    build_bridge,
    chain_lift_octahedron_correspondence,
    laplacian_spectrum,
    matrix_tree_count,
    octahedron_adjacency,
    reduced_determinant,
    spectrum_w33_decomposition,
    tau_octahedron_closed_form,
    write_bridge,
)


def test_octahedron_adjacency_is_K_2_2_2():
    A = octahedron_adjacency()
    assert A.sum() == 24    # 12 edges * 2 directions
    for i in range(6):
        assert A[i].sum() == 4


def test_spectrum_is_0_4_4_4_6_6():
    spec = laplacian_spectrum()
    assert tuple(spec) == (0, 4, 4, 4, 6, 6)


def test_spectrum_eigenvalues_are_mu_and_q_factorial():
    spec = laplacian_spectrum()
    assert 4 == MU
    assert 6 == math.factorial(Q)
    assert spec.count(0) == 1
    assert spec.count(MU) == Q
    assert spec.count(math.factorial(Q)) == LAM


def test_total_multiplicity_eq_q_factorial():
    decomp = spectrum_w33_decomposition()
    assert decomp["total_multiplicity"] == 1 + Q + LAM == math.factorial(Q) == 6


def test_trace_equals_f_eigen_24():
    spec = laplacian_spectrum()
    trace = sum(spec)
    assert trace == 24 == F_EIGEN


def test_det_prime_eq_2304():
    spec = laplacian_spectrum()
    dp = reduced_determinant(spec)
    assert dp == 2304


def test_det_prime_eq_mu_q_qfact_lambda():
    spec = laplacian_spectrum()
    dp = reduced_determinant(spec)
    expected = MU ** Q * math.factorial(Q) ** LAM
    assert dp == expected == 2304


def test_tau_eq_384():
    spec = laplacian_spectrum()
    tau = matrix_tree_count(spec, 6)
    assert tau == 384


def test_tau_closed_form():
    closed = tau_octahedron_closed_form()
    assert closed["matches_384"] is True
    assert closed["evaluated"] == 384


def test_tau_eq_E8_density_denominator():
    """rho_8 = pi^4 / 384."""
    assert 384 == MU ** Q * math.factorial(Q) ** (LAM - 1)


def test_chain_lift_octahedron_V_eq_E_W33():
    chain = chain_lift_octahedron_correspondence()
    assert chain["across_40_W33_vertices"]["matches_E_W33_single_dir"] is True
    assert 40 * 6 == E_W33 == 240


def test_chain_lift_octahedron_E_eq_C1_prime():
    chain = chain_lift_octahedron_correspondence()
    assert chain["across_40_W33_vertices"]["matches_C1_prime_DCCLXVIII"] is True
    assert 40 * 12 == 480


def test_chain_lift_octahedron_F_eq_C2_prime():
    chain = chain_lift_octahedron_correspondence()
    assert chain["across_40_W33_vertices"]["matches_C2_prime_DCCLXVIII"] is True
    assert 40 * 8 == 320


def test_octahedron_subcell_total_eq_26_D_bosonic():
    """6 + 12 + 8 = 26 = D_bosonic (DCCXXVI)."""
    assert 6 + 12 + 8 == 26


def test_summary_all_identities_hold():
    b = build_bridge()
    assert b["summary"]["all_identities_hold"] is True


def test_identities_all_pass():
    b = build_bridge()
    failed = [k for k, v in b["identities"].items() if not v]
    assert failed == []


def test_theorem_and_one_line_present():
    b = build_bridge()
    assert "Laplacian" in b["theorem"]
    assert "tau(O)" in b["one_line"] or "spectrum" in b["one_line"]


def test_write_and_reload():
    out = write_bridge()
    assert out.exists()
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["summary"]["all_identities_hold"] is True


def test_json_has_expected_keys():
    if not OUT_PATH.exists():
        write_bridge()
    data = json.loads(OUT_PATH.read_text(encoding="utf-8"))
    for key in (
        "summary",
        "octahedron_adjacency",
        "octahedron_laplacian_spectrum",
        "spectrum_w33_decomposition",
        "trace_value",
        "det_prime_value",
        "tau_value",
        "tau_closed_form",
        "chain_lift_correspondence",
        "identities",
        "theorem",
        "one_line",
        "honesty_boundary",
    ):
        assert key in data
