from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_module():
    path = ROOT / "analysis" / "w33_pass542_triality_icosahedral_hjelmslev.py"
    spec = importlib.util.spec_from_file_location("pass542", path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def payload():
    return load_module().payload()


def test_pass542_all_checks():
    p = payload()
    assert p["status"] == "PASS"
    assert len(p["checks"]) == 36
    assert all(p["checks"].values())


def test_d4_triality_cycle():
    p = payload()["triality"]
    assert p["sets"] == {"8v": 8, "8s+": 8, "8s-": 8}
    assert p["cycle"] == ["8v", "8s+", "8s-", "8v"]


def test_q5_icosahedral_scheme():
    p = payload()["polyhedral"]["p5"]
    assert p["classes"] == 12
    assert p["rotation_image"] == 60
    assert p["extended_image"] == 120
    assert p["scheme"] == [1, 5, 5]
    assert p["triangles"] == 20


def test_q5_odd_switch_no_go():
    p = payload()["odd_switch"]
    assert len(p["switched"]) == 5
    assert p["products"] == [4, 1]
    assert p["cycles"] == 12878


def test_z9_hjelmslev_bundle():
    p = payload()["z9_bundle"]
    assert p["classes"] == 40
    assert p["kernel"] == "C3^3"
    assert all(row["primitive"] == 9 and row["deep_fixed"] for row in p["fibres"])


def test_trace_triality_boundary():
    p = payload()["trace_boundary"]
    assert p["8v"] == "all even"
    assert p["8s"] == "odd 1 mod 6"
    assert p["aux"] == "odd 3,5 mod 6"
