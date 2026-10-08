"""Regression tests for exact point/line 27-state resistance profiles."""
from __future__ import annotations
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "w33_dual27_electrical",
    ROOT / "analysis" / "w33_20261008_dual_27_electrical_transport.py",
)
mod = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mod)

def test_exact_transport_firewall():
    payload = mod.compute()
    assert payload["status"].startswith("PASS_EXACT")
    p = payload["graphs"]["point_far_H27"]
    q = payload["graphs"]["line_transverse_null"]
    assert p["spectrum"] == q["spectrum"]
    assert p["kirchhoff_index"] == q["kirchhoff_index"] == "183/2"
    assert p["distance_histogram"] == {"1":108,"2":216,"3":27}
    assert q["distance_histogram"] == {"1":108,"2":243}
    assert p["resistance_histogram"] == {"13/54":108,"29/108":216,"5/18":27}
    assert q["resistance_histogram"] == {"13/54":108,"22/81":162,"43/162":81}
    assert p["pseudoinverse_diagonal"] == q["pseudoinverse_diagonal"] == "61/486"

def test_independent_rebuild():
    two = mod.build_graphs()
    assert len(two) == 2
    assert set(map(tuple,two["point_far_H27"])) != set(map(tuple,two["line_transverse_null"]))
    for a in two.values():
        assert mod.audit(a)["kirchhoff_index"] == "183/2"
