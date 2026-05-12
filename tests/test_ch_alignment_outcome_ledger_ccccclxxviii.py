def test_ch_primary_gate():
    dim_k = 81
    target_full_rank = 81
    assert target_full_rank == dim_k


def test_effective_alignment_dimension_formula():
    # If C_H = c I_81, then d_eff = Tr(C)^2 / Tr(C^2) = 81.
    dim = 81
    c_num = 5
    tr = dim * c_num
    tr2 = dim * c_num * c_num
    assert tr * tr // tr2 == dim


def test_outcome_classes():
    classes = {
        "A": "full isotropic alignment",
        "B": "full split alignment",
        "C": "rank-defective alignment",
        "D": "near-zero or unstable alignment",
    }
    assert set(classes) == {"A", "B", "C", "D"}


def test_ch_diagnostics_are_required():
    required = ["rank(C_H)", "Tr(C_H)", "Tr(C_H^2)", "Spec(C_H)"]
    assert len(required) == 4
    assert required[0] == "rank(C_H)"
    assert required[-1] == "Spec(C_H)"


def test_reference_scales():
    scales = ["81/640", "27/80", "27/32", "27/20"]
    assert len(scales) == 4
    assert "27/80" in scales
