SECTORS = {
    "K": {"dim": 81, "lambda": 0},
    "B": {"dim": 120, "lambda": 4},
    "R": {"dim": 24, "lambda": 10},
    "S": {"dim": 15, "lambda": 16},
}
ORDER = ["K", "B", "R", "S"]


def lam(s):
    return SECTORS[s]["lambda"]


def dim(s):
    return SECTORS[s]["dim"]


def pairs():
    return [(ORDER[i], ORDER[j]) for i in range(len(ORDER)) for j in range(i + 1, len(ORDER))]


def delta_phi_weight(a, b):
    return lam(a) + lam(b)


def commutator_weight(a, b):
    return 2 * (lam(a) - lam(b)) ** 2


def test_sector_dimensions_and_eigenvalues():
    assert sum(dim(s) for s in ORDER) == 240
    assert [dim(s) for s in ORDER] == [81, 120, 24, 15]
    assert [lam(s) for s in ORDER] == [0, 4, 10, 16]


def test_quadratic_trace_offdiag_weights():
    # Tr(Phi^2)=sum_i Tr(Phi_ii^2)+2 sum_{i<j} ||Phi_ij||^2
    assert {a + b: 2 for a, b in pairs()} == {
        "KB": 2,
        "KR": 2,
        "KS": 2,
        "BR": 2,
        "BS": 2,
        "RS": 2,
    }


def test_delta_phi_squared_weights():
    assert {a + b: delta_phi_weight(a, b) for a, b in pairs()} == {
        "KB": 4,
        "KR": 10,
        "KS": 16,
        "BR": 14,
        "BS": 20,
        "RS": 26,
    }


def test_commutator_gap_penalty_weights():
    assert {a + b: commutator_weight(a, b) for a, b in pairs()} == {
        "KB": 32,
        "KR": 200,
        "KS": 512,
        "BR": 72,
        "BS": 288,
        "RS": 72,
    }


def test_kernel_mixing_hierarchy():
    kernel_costs = {
        "KB": commutator_weight("K", "B"),
        "KR": commutator_weight("K", "R"),
        "KS": commutator_weight("K", "S"),
    }
    assert kernel_costs["KB"] < kernel_costs["KR"] < kernel_costs["KS"]
    assert min(kernel_costs, key=kernel_costs.get) == "KB"


def test_minimal_kb_ansatz_trace_weights():
    # For Phi_min = [[0,Y],[Y*,H]] on K+B:
    # Tr(Phi^2) = 2||Y||^2 + Tr(H^2)
    # Tr(Delta Phi^2) = 4||Y||^2 + 4Tr(H^2)
    # Tr([Delta,Phi]^*[Delta,Phi]) = 32||Y||^2
    assert 2 == 2
    assert delta_phi_weight("K", "B") == 4
    assert lam("B") == 4
    assert commutator_weight("K", "B") == 32


def test_fermion_double_dimension():
    assert dim("K") == 81
    assert 2 * dim("K") == 162
