import json
from pathlib import Path

import numpy as np
import pytest

QCA_PATH = Path("data/w33_algebra_qca.json")
PROJECTIONS_PATH = Path("data/simple_edge_projections.json")


def load_qca():
    if not QCA_PATH.exists():
        pytest.skip(f"{QCA_PATH} is generated; run scripts/w33_algebra_qca.py")
    return json.loads(QCA_PATH.read_text(encoding="utf-8"))


def load_projections():
    if not PROJECTIONS_PATH.exists():
        pytest.skip(
            f"{PROJECTIONS_PATH} is generated; run scripts/chevalley_simple_edge_analysis.py"
        )
    return json.loads(PROJECTIONS_PATH.read_text(encoding="utf-8"))


def test_eps_balance():
    data = load_qca()
    eps = data["chevalley"]["eps_counts"]
    assert eps.get("1") == eps.get("-1"), "eps signs should balance"
    assert eps.get("1") == 3360


def test_simple_edge_grade_counts():
    data = load_qca()
    simples = data["chevalley"]["simple_edges"]
    grades = [s["grade"] for s in simples]
    assert grades.count("g1") == 4
    assert grades.count("g2") == 2
    assert grades.count("g0_e6") == 2


def test_g0_e6_common_vertex():
    data = load_qca()
    simples = data["chevalley"]["simple_edges"]
    g0 = [s for s in simples if s["grade"] == "g0_e6"]
    assert len(g0) == 2
    v0 = set(g0[0]["edge"])
    v1 = set(g0[1]["edge"])
    assert v0 & v1, "g0_e6 simple edges should share a vertex"


def test_degree_three_root_is_g1():
    data = load_qca()
    # reconstruct Cartan from simple root orbits
    rows = data["chevalley"]["simple_edges"]
    # cartan is fixed known matrix from E8 Sage order
    C = np.array(
        [
            [2, 0, -1, 0, 0, 0, 0, 0],
            [0, 2, 0, -1, 0, 0, 0, 0],
            [-1, 0, 2, -1, 0, 0, 0, 0],
            [0, -1, -1, 2, -1, 0, 0, 0],
            [0, 0, 0, -1, 2, -1, 0, 0],
            [0, 0, 0, 0, -1, 2, -1, 0],
            [0, 0, 0, 0, 0, -1, 2, -1],
            [0, 0, 0, 0, 0, 0, -1, 2],
        ],
        dtype=int,
    )
    degs = 2 - C.sum(axis=1)
    idx = int(np.where(degs == 3)[0][0])
    assert rows[idx]["grade"] == "g1"


def test_subspace0_dominance():
    proj = load_projections()
    sims = proj.get("simple_stats", [])
    for entry in sims:
        stats = entry.get("incident_stats", [])
        means = [m for m, M in stats]
        assert (
            means[0] > means[1] and means[0] > means[2]
        ), f"Subspace0 not dominating for root {entry['i']}: {means}"


def test_grade_average_ordering():
    proj = load_projections()
    sims = proj.get("simple_stats", [])
    grade_avgs = {}
    for entry in sims:
        g = entry["grade"]
        mean0 = entry["incident_stats"][0][0]
        mean2 = entry["incident_stats"][2][0]
        grade_avgs.setdefault(g, []).append((mean0, mean2))
    # compute average per grade
    avg = {g: np.mean(np.array(vals), axis=0) for g, vals in grade_avgs.items()}
    # expect g0_e6 has largest mean0 and mean2
    means0 = [(avg[g][0], g) for g in avg]
    means0.sort()
    assert means0[-1][1] == "g0_e6"
    means2 = [(avg[g][1], g) for g in avg]
    means2.sort()
    assert means2[-1][1] == "g0_e6"


def test_triangle_counts():
    proj = load_projections()
    sims = proj.get("simple_stats", [])
    counts = [entry["triangles"] for entry in sims]
    # all are >=22 and at least one equals 24
    assert min(counts) >= 22
    assert max(counts) == 24
    # at least one g0_e6 triangle count should equal the maximum
    g0 = [e["triangles"] for e in sims if e["grade"] == "g0_e6"]
    assert any(c == max(counts) for c in g0)


def test_variance_grade_order():
    proj = load_projections()
    sims = proj.get("simple_stats", [])
    # collect variance0 values
    var0 = [(e["incident_variance"][0], e["grade"]) for e in sims]
    var0.sort(reverse=True)
    # top two should be g0_e6
    assert var0[0][1] == "g0_e6"
    assert var0[1][1] == "g0_e6"
