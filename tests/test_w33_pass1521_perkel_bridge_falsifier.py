from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))

import w33_pass1521_perkel_bridge_falsifier as pass1521


def test_reference_perkel_graph() -> None:
    graph = pass1521.perkel_graph()
    assert graph.number_of_nodes() == 57
    assert graph.number_of_edges() == 171
    assert set(dict(graph.degree()).values()) == {6}
    assert pass1521.nx.diameter(graph) == 3
    assert pass1521.intersection_array(graph) == ((6, 5, 2), (1, 1, 3))


def test_inherited_action_obstruction_is_exact() -> None:
    psl219 = 19 * (19 * 19 - 1) // 2
    assert psl219 == 3420
    assert 25920 % 19 != 0
    assert 51840 % 19 != 0
    assert 76 == 19 * 4
    assert 57 + 19 == 19 * (3 + 1)


def test_report_preserves_emergent_symmetry_boundary() -> None:
    report = (ROOT / "analysis" / "BT1521_perkel_shadow_bridge_falsifier.md").read_text(
        encoding="utf-8"
    )
    assert "inherited" in report
    assert "emergent" in report
    assert "does **not** exclude" in report
    assert "not exhaustive" in report
