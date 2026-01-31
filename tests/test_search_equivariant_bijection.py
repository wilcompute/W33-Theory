import json
from pathlib import Path

from tools.e8_w33_bijection import (load_explicit_bijection,
                                    verify_bijective_mapping)
from tools.search_equivariant_bijection_hillclimb import local_search

ROOT = Path(__file__).resolve().parents[1]


def test_search_smoke_short_run(tmp_path):
    # Run a small, bounded search and ensure output artifact created and mapping valid
    out = local_search(iterations=2000, seed=42, time_limit=2.0)
    p = ROOT / "artifacts" / "equivariant_search_result.json"
    assert p.exists()

    data = json.loads(p.read_text(encoding="utf-8"))
    mapping = data.get("mapping")
    assert mapping is not None
    # mapping length / bijectivity
    assert len(mapping) == 240
    assert len(set(mapping)) == 240

    # sanity: best_score shouldn't be worse than baseline
    assert data.get("best_score", 0) >= data.get("baseline_score", 0)


def test_triangle_weight_increases_a2_triangle_count():
    # short run that tries to improve triangle count
    out = local_search(iterations=2000, seed=123, time_limit=2.0, triangle_weight=10)
    p = ROOT / "artifacts" / "equivariant_search_result.json"
    assert p.exists()
    res = json.loads(p.read_text(encoding="utf-8"))
    mapping = res["mapping"]

    # reconstruct triangles from adjacency
    from tools.search_equivariant_bijection_hillclimb import (
        build_adjacency_list, dot_matrix)

    _, adj = build_adjacency_list()
    triangles = []
    n = len(adj)
    for a in range(n):
        for b in range(a + 1, n):
            if not adj[a][b]:
                continue
            for c in range(b + 1, n):
                if adj[a][c] and adj[b][c]:
                    triangles.append((a, b, c))

    data = load_explicit_bijection()
    roots = data["root_coords"]
    dotm = dot_matrix(roots)

    def count_a2(m):
        cnt = 0
        for a, b, c in triangles:
            if (
                int(dotm[m[a], m[b]]) == -2
                and int(dotm[m[a], m[c]]) == -2
                and int(dotm[m[b], m[c]]) == -2
            ):
                cnt += 1
        return cnt

    baseline_map = [int(k) and int(v) for k, v in data["edge_to_root_index"].items()]
    # Build baseline mapping ordering by edge idx
    baseline_map = [data["edge_to_root_index"][str(i)] for i in range(len(mapping))]

    base_cnt = count_a2(baseline_map)
    new_cnt = count_a2(mapping)

    assert new_cnt >= base_cnt


def test_search_bijection_still_valid_after_run():
    # ensure original artifact remains a valid bijection
    data = load_explicit_bijection()
    ok, msg = verify_bijective_mapping(data)
    assert ok, msg
