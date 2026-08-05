from analysis.bt3404_3417_conic_torus_closure import build_certificate
from analysis.bt3407_magnetic_chromatic_search import build_certificate as magnetic_certificate
from analysis.bt3407_magnetic_exact_no_go import build_certificate as magnetic_exact_certificate


def test_conic_torus_closure():
    result = build_certificate()
    assert result["status"] == "PASS"
    assert all(result["checks"].values())
    assert result["sections"]["H1_covering_radius"]["improved_interval"] == [389, 436]
    assert result["sections"]["finite_null_conic"]["projective_stabilizer_order"] == 24
    assert result["sections"]["matrix_valued_torus"]["full_walk_factorization"]["set_bijection"].startswith("135 = 27 x 5")


def test_magnetic_search_smoke():
    result = magnetic_certificate(limit=3)
    assert result["status"] == "PASS"
    assert result["search"]["patterns_evaluated"] == 9
    assert result["best_ternary_phase"]["extremal_residual_max"] < 1e-8


def test_magnetic_exact_no_go():
    result = magnetic_exact_certificate()
    assert result["status"] == "PASS"
    assert all(result["checks"].values())
    assert result["ternary_phase"]["hoffman_ratio_numeric"] < 8
    assert result["real_signed"]["hoffman_ratio_numeric"] < 8
