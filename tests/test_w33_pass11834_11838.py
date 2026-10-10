"""Regression tests for Passes 11834-11838 (finite singletons, bulk modes, Poincare group, E8 centraliser, Lean)."""

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))

import w33_pass11831_11833_finite_ads4 as F  # noqa: E402
import w33_pass11834_11837_singletons_bulk_poincare_e8 as S  # noqa: E402

DATA = ROOT / "data"


def test_transvection_lift_is_exact():
    g = F.transvection(np.array((1, 0, 0, 1)))
    V = S.det1_order3(S.intertwiner(g))
    assert np.allclose(V @ V @ V, np.eye(9)) and abs(np.linalg.det(V) - 1) < 1e-9
    for v in F.VECS[::7]:
        assert np.allclose(V @ S.weyl(v) @ V.conj().T, S.weyl(g @ v % 3))


def test_certificate_singletons_and_bulk():
    c = json.load(open(DATA / "w33_pass11834_11837_singletons_bulk_poincare_e8.json"))
    w = c["weil"]
    assert w["order"] == 51840 and w["homomorphism_max_error"] < 1e-10 and w["clifford_action_max_error"] < 1e-10
    s = c["singletons"]
    assert s["norms"]["Rac"] == 1.0 and s["norms"]["Di"] == 1.0 and s["norms"]["Rac_vs_Di"] == 0.0
    b = s["bilinears"]
    assert b["Sym2 Rac"]["norm"] == 1.0 and b["Sym2 Rac"]["<kramers36>"] == 1.0 and b["Sym2 Rac"]["<contexts40>"] == 1.0
    assert b["Alt2 Rac"]["<kramers36>"] == 0.0 and b["Rac x Rac*"]["<kramers36>"] == 1.0
    assert s["Rac.Rac* + Di.Di* == 1 + C[40 points]"]
    bulk = c["bulk"]
    assert bulk["orthogonality_graph"]["spectrum"] == {"15": 1, "3": 15, "-3": 20}
    assert bulk["incidence_bulk_boundary"]["rank"] == 16 and bulk["incidence_bulk_splits"]["rank"] == 21
    seen = bulk["bulk_eigenspaces_seen_by_boundary"]
    assert seen["3"]["visible_from_boundary"] == 15 and seen["-3"]["visible_from_boundary"] == 0


def test_certificate_poincare_and_e8():
    c = json.load(open(DATA / "w33_pass11834_11837_singletons_bulk_poincare_e8.json"))
    p = c["poincare"]
    assert p["shell_sizes"] == {"null": 20, "split_type": 30, "kramers_type": 30}
    lg = p["little_groups"]
    assert lg["null"]["order"] == 36 and lg["null"]["order3_elements_commute"] and lg["null"]["n_linear_characters"] == 4
    assert lg["kramers_type"]["is_SL23_by_order_statistics"] and lg["split_type"]["is_SL23_by_order_statistics"]
    assert lg["kramers_type"]["n_classes"] == 7 and lg["null"]["n_classes"] == 12
    e = c["e8"]
    assert e["lorentz_SL29"]["total"] == 1 and e["lorentz_SL29"]["dims"] == {"sl9": 1, "wedge3": 0, "wedge3_dual": 0}
    assert e["content"]["sl9 (80)"]["<vectors80>"] == 5.0 and e["content"]["Lambda3 (84)"]["norm"] == 7.0


def test_lean_module():
    root = (ROOT / "formal" / "W33.lean").read_text(encoding="utf-8")
    assert "import W33.Pass11838CliffordQuadric" in root
    src = (ROOT / "formal" / "W33" / "Pass11838CliffordQuadric.lean").read_text(encoding="utf-8")
    for name in ("J_sq", "J_anticomm", "J_selfadjoint", "J_similitude", "kramers", "counts"):
        assert f"theorem {name}" in src
    assert "sorry" not in src
