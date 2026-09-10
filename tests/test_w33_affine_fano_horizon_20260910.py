from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = ROOT / "analysis"
if str(ANALYSIS) not in sys.path:
    sys.path.insert(0, str(ANALYSIS))

from w33_affine_fano_information_horizon import build_result  # noqa: E402


def test_affine_fano_horizon_exact_kernel_and_all_n_law() -> None:
    data = build_result()
    assert data["status"] == "PASS"
    assert all(data["checks"].values())
    assert data["general_theorem"]["macro_decomposition"] == "PG(n,2)=AG(n,2) disjoint_union PG(n-1,2)"
    assert data["general_theorem"]["second_eigenvalue"] == "-3/(4*(4^n-1)) = -1/(4*|PG(n-1,4)|)"
    assert [r["n"] for r in data["dimension_census"]] == [1, 2, 3, 4, 5, 6]

    n3 = data["n3_information_horizon"]
    assert n3["global_microstates"] == 85
    assert n3["affine_microstates"] == 64
    assert n3["fano_infinity_microstates"] == 21
    assert n3["affine_macrostates"] == 8
    assert n3["fano_infinity_macrostates"] == 7
    assert n3["transition_matrix"] == {
        "A_to_A": "3/4",
        "A_to_F": "1/4",
        "F_to_A": "16/21",
        "F_to_F": "5/21",
    }
    assert n3["stationary_sector_weights"] == {"A": "64/85", "F": "21/85"}
    assert n3["eigenvalues"] == ["1", "-1/84"]
    assert n3["determinant"] == "-1/84"
    assert data["toroidal_84_echo"]["arithmetic_origin"] == "84=4*|PG(2,4)|=4*21"
