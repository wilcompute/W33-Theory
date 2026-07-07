from collections import Counter

from analysis import bt1807_defect_phase_plane_transversal_design as bt1807


def test_w33_substrate_constants():
    pts, adj, lines = bt1807.build_w33()
    assert len(pts) == 40
    assert len(lines) == 40
    assert {sum(row) for row in adj} == {12}
    assert sum(sum(row) for row in adj) // 2 == 240


def test_each_center_has_td43_escape_surface():
    pts, adj, lines = bt1807.build_w33()
    for center in range(40):
        rows, neighbors, safe = bt1807.vector_table(center, pts, adj)
        groups = bt1807.star_lines(center, lines)
        group_id = {x: gi for gi, group in enumerate(groups) for x in group}
        assert len(rows) == 9
        assert len(safe) == 27
        assert len(neighbors) == 12
        assert len(groups) == 4
        assert all(len(group) == 3 for group in groups)
        assert set(Counter(x for row in rows for x in row["triad"]).values()) == {1}
        assert set(Counter(x for row in rows for x in row["quad"]).values()) == {3}
        for row in rows:
            assert sorted(group_id[x] for x in row["quad"]) == [0, 1, 2, 3]
            assert not any(adj[a][b] for i, a in enumerate(row["quad"]) for b in row["quad"][i + 1:])


def test_cheap_exits_cover_directed_edges_three_times():
    pts, adj, _ = bt1807.build_w33()
    directed = Counter()
    for center in range(40):
        rows, _, _ = bt1807.vector_table(center, pts, adj)
        for row in rows:
            for target in row["quad"]:
                directed[(center, target)] += 1
    assert len(directed) == 480
    assert set(directed.values()) == {3}
