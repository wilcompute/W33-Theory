import importlib.util
from pathlib import Path
import sympy as s

ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location("p11607",ROOT/"analysis/w33_pass11607_hesse_cp_weyl_selector.py")
M=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(M)

# One exact computation feeds all independent assertions below.  This avoids
# repeating the expensive 32x32 Clifford calculation without weakening coverage.
RESULT=M.diagonal_selector()
FLAVOR=RESULT["flavor"]
SPIN=RESULT["spin10"]


def test_sign_isotypic_minimal_degree():
    assert FLAVOR["anti_invariant_dimensions_by_bloch_degree_0_to_6"]=={str(i):(1 if i==6 else 0) for i in range(7)}
    assert FLAVOR["minimal_anti_invariant_field_degree"]==12


def test_pin_lift_flips_chirality_and_normalizes_so10():
    assert SPIN["chirality_spectrum"]=={"+1":16,"-1":16}
    assert SPIN["bivectors_checked"]==45
    assert SPIN["adjoint_order"]==2


def test_hesse_vacuum_split_is_twelve_plus_twelve():
    assert FLAVOR["vacuum_rays"]==24
    assert FLAVOR["vacuum_W_multiplicities"]==[12,12]


def test_positive_filter_has_one_exact_weyl_kernel_per_vacuum():
    for row in RESULT["vacuum_rows"]:
        assert row["zero_multiplicity"]==16
        assert row["gapped_multiplicity"]==16
        assert row["zero_chirality"]==-row["W_sign"]
        assert row["gapped_chirality"]==row["W_sign"]
    assert RESULT["field_degree"]["linear_diagonal_portal"]==12
    assert RESULT["field_degree"]["manifestly_positive_exact_kernel_filter"]==24


def test_exact_gap_coefficient():
    c=s.Rational(15,343)
    assert all(s.sympify(row["gap_coefficient_times_lambda_rho12"])==4*c*c for row in RESULT["vacuum_rows"])
