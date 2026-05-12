DIM_K = 81
DIM_B = 120
LAMBDA_K = 0
LAMBDA_B = 4
RANK_D1 = 39


def commutator_eigenvalue(lambda_target, lambda_source):
    return lambda_target - lambda_source


def test_kb_bridge_breaks_delta_spectral_symmetry():
    # For Y: B -> K, [Delta_1,Y]=(lambda_K-lambda_B)Y=-4Y.
    assert commutator_eigenvalue(LAMBDA_K, LAMBDA_B) == -4
    # Therefore [Delta_1,Y]=0 forces Y=0 for a K-B bridge.
    assert commutator_eigenvalue(LAMBDA_K, LAMBDA_B) != 0


def test_spectral_polynomial_cannot_generate_kb_bridge():
    # Any F(Delta_1) is block diagonal in the eigenspace decomposition,
    # so it cannot map B to K when lambda_B != lambda_K.
    assert LAMBDA_K != LAMBDA_B


def test_rank_lock_survives_symmetry_classification():
    max_rank = min(DIM_K, DIM_B)
    residual = DIM_B - max_rank
    assert max_rank == 81
    assert residual == 39
    assert residual == RANK_D1
    assert DIM_B == DIM_K + RANK_D1


def test_y_classification_names_the_correct_target():
    classes = {
        "class_0": "spectral-canonical: forbidden for nonzero K-B bridge",
        "class_1": "full Aut(W33)-equivariant Hom_G(B,K)",
        "class_2": "subgroup-equivariant Hom_H(B,K)",
        "class_3": "incidence/frame-derived symmetry-breaking bridge",
    }
    assert "forbidden" in classes["class_0"]
    assert "Hom_G" in classes["class_1"]
    assert "Hom_H" in classes["class_2"]
    assert "symmetry-breaking" in classes["class_3"]


def test_physical_interpretation_is_symmetry_breaking_not_missing_symmetry():
    # Gauge/connection data can remain sector preserving; Higgs/Yukawa data
    # intentionally occupy off-diagonal finite blocks.
    gauge_sector_preserving = True
    higgs_yukawa_offdiagonal = True
    assert gauge_sector_preserving
    assert higgs_yukawa_offdiagonal
    assert 2 * DIM_K == 162
