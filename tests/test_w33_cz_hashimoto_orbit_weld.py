from __future__ import annotations
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "analysis" / "w33_cz_hashimoto_orbit_weld.py"

spec = importlib.util.spec_from_file_location("cz_hashimoto_weld", MOD)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)


def test_q3_gate_route_weld():
    r = mod.weld(3)
    assert r["gq"] == {"contexts": 40, "collinearity_degree_k": 12, "hashimoto_outdegree": 11}
    assert r["cz_counts"]["nonfixed_orbits_total"] == 11
    assert r["cz_counts"]["intersecting_nonfixed_orbits"] == 2
    assert r["cz_counts"]["transverse_nonfixed_orbits"] == 9
    assert r["hashimoto_counts"] == {"same_line": 2, "off_line": 9, "total": 11}
    assert r["weld"]["mapping_entries"] == 11
    assert r["cyclotomic"]["equal"] is True


def test_all_q_controls_and_branch_identity():
    for q in (3, 5, 7, 11):
        r = mod.weld(q)
        k = q * (q + 1)
        assert r["gq"]["hashimoto_outdegree"] == k - 1
        assert r["cz_counts"]["nonfixed_orbits_total"] == k - 1
        assert r["cz_counts"]["intersecting_nonfixed_orbits"] == q - 1
        assert r["cz_counts"]["transverse_nonfixed_orbits"] == q * q
        assert r["hashimoto_counts"]["same_line"] == q - 1
        assert r["hashimoto_counts"]["off_line"] == q * q
        assert all(r["checks"].values())


def test_cyclotomic_fixed_context_lock_is_q3_only_in_controls():
    vals = [mod.weld(q)["cyclotomic"]["equal"] for q in (3, 5, 7, 11)]
    assert vals == [True, False, False, False]
    for q in (3, 5, 7, 11):
        r = mod.weld(q)
        assert r["cyclotomic"]["Phi6_minus_fixed"] == q * (q - 3)
