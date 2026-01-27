import json
from itertools import product
from pathlib import Path
import pytest


def build_w33_edges():
    F3 = [0, 1, 2]
    vectors = [v for v in product(F3, repeat=4) if any(x != 0 for x in v)]

    proj_points = []
    seen = set()
    for v in vectors:
        v = list(v)
        for i in range(4):
            if v[i] != 0:
                inv = 1 if v[i] == 1 else 2
                v = tuple((x * inv) % 3 for x in v)
                break
        if v not in seen:
            seen.add(v)
            proj_points.append(v)

    def omega(x, y):
        return (x[0] * y[2] - x[2] * y[0] + x[1] * y[3] - x[3] * y[1]) % 3

    edges = set()
    for i in range(len(proj_points)):
        for j in range(i + 1, len(proj_points)):
            if omega(proj_points[i], proj_points[j]) == 0:
                edges.add((i, j))

    return edges


def test_e8_root_to_w33_edge_bijection():
    p = Path("artifacts_archive/e8_root_to_w33_edge.json")
    if not p.exists():
        pytest.skip("e8_root_to_w33_edge.json not found — run tools/sage_e8_root_edge_bijection.py")

    data = json.loads(p.read_text(encoding="utf-8"))

    root_to_edge = data.get("root_to_edge", {})
    assert len(root_to_edge) == 240

    edges = set()
    for edge in root_to_edge.values():
        assert isinstance(edge, list)
        assert len(edge) == 2
        a, b = edge
        assert a != b
        edges.add(tuple(sorted((a, b))))

    assert len(edges) == 240

    w33_edges = build_w33_edges()
    assert edges == w33_edges

    orbit_map = data.get("orbit_to_w33_vertex", {})
    assert len(orbit_map) == 40

    w33_vertices = data.get("w33_vertices", [])
    assert len(w33_vertices) == 40
