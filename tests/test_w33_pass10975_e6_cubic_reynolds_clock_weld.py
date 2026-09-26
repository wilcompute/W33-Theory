import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "p10975",
    ROOT / "analysis" / "w33_pass10975_e6_cubic_reynolds_clock_weld.py",
)
P = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(P)

CERT_PATH = ROOT / "data" / "w33_pass10975_e6_cubic_reynolds_clock_weld.json"
CERT = json.loads(CERT_PATH.read_text(encoding="utf-8"))


def test_certificate_replays_exactly():
    assert P.payload() == CERT


def test_clock_module_is_inside_27_coordinate_carrier():
    m = CERT["coordinate_module"]
    assert m["four_fibres_size"] == 6
    assert m["center_size"] == 3
    assert m["augmentation_dimension"] == 3
    assert m["all_48_GL23_lifts_equivariant_on_fibres"] is True
def test_signed_gauge_firewall_is_real():
    f = CERT["signed_gauge_firewall"]
    assert f["pure_coordinate_permutations_preserving_signed_cubic"] == 1
    assert f["GL23_support_operations_checked"] == 48
    assert f["binary_sign_equation_rank"] == 21
    assert f["homogeneous_sign_gauge_dimension"] == 6
    assert f["repairs_per_support_operation"] == 64


def test_reynolds_component_is_the_tetrahedral_selector():
    r = CERT["clock_restriction"]
    assert r["raw_is_S4_invariant"] is False
    assert r["reynolds_polynomial"] == (
        "-sum_i y_i^3 + sum_{i<j<k} y_i y_j y_k"
    )
    assert r["augmentation_constraint"] == "sum_i y_i = 0"
    assert r["augmentation_identity"] == "R(D)|_A = -(2/3) p3"
    assert r["coefficient"] == "-2/3"
    assert r["nonzero_projection"] is True


def test_firewall_center_is_the_bad_nine():
    assert CERT["checks"]["center_class_is_firewall_bad9"] is True
    assert CERT["support_geometry"]["triads_per_direction"] == 9
    assert CERT["support_geometry"]["direction_classes"] == 5
