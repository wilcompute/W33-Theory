"""Independent regression assertions for Pass 11766; computation memoized once."""
import importlib.util
import json
from pathlib import Path
import sympy as s

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("p11766", ROOT/"analysis/w33_pass11766_compact_real_selector.py")
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
E8=mod.real_e8_grade_audit()
SPIN=mod.spin10_real_audit()

def test_e8_original_real_shell_obstruction():
    assert E8["compact_real_E8_adj_dimension"]==248
    assert E8["compact_real_branching"]=="86 fixed real + 81 real rotation planes"
    assert "interchanges" in E8["one_shell_complex_projector"]
    assert "real adjoint" in E8["real_kernel_obstruction"]

def test_real_symmetric_commutant_and_auxiliary_split():
    J=mod.J
    assert J.T==-J and J*J==-s.eye(2)
    S=s.kronecker_product(J,J)
    assert S.T==S and S*S==s.eye(4)
    assert ((s.eye(4)+S)/2).rank()==2
    assert ((s.eye(4)-S)/2).rank()==2
    assert E8["doubled_matter_dimension"]==324
    assert all(row["matter_kernel_real_dimension"]==162 for row in E8["vacuum_rows"])
    assert all(row["neutral_kernel_real_dimension"]==172 for row in E8["vacuum_rows"])

def test_actual_real_spin10_clifford_chirality():
    assert SPIN["actual_gamma_count"]==10
    assert SPIN["conjugate_Weyl_spaces"]=="ordinary complex conjugation exchanges Chi=+1 and Chi=-1"
    assert SPIN["gauge_invariance"]=="V commutes with all 45 Spin10 bivectors"

def test_repaired_exact_gap_and_dimensions():
    expected=s.Rational(900,117649)
    for row in SPIN["repaired_vacuum_rows"]:
        assert row["light_real_dimension"]==32
        assert row["heavy_real_dimension"]==32
        assert row["light_complex_dimension_given_aux_structure"]==16
        assert s.sympify(row["gap_over_lambda_rho12"])==expected
    for row in E8["vacuum_rows"]:
        assert s.sympify(row["matter_gap_over_lambda_rho12"])==expected

def test_frozen_certificate_is_exactly_source_bound():
    data=json.loads((ROOT/"data/PART_W33_PASS11766_COMPACT_REAL_SELECTOR.json").read_text())
    assert data["E8"]==E8 and data["Spin10"]==SPIN
    for path,digest in data["source_sha256"].items():
        assert mod.hash_source(path)==digest
    assert data["producer_sha256"]==mod.hashlib.sha256(
        (ROOT/"analysis/w33_pass11766_compact_real_selector.py").read_bytes().replace(b"\r\n",b"\n")
    ).hexdigest()
