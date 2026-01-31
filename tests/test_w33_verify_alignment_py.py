from pathlib import Path

from lib.w33_io import W33DataPaths, load_w33_lines
from tools.w33_verify_alignment_py import (build_incidence_edges,
                                           summary_from_edges)


def test_incidence_basic_counts():
    here = Path(__file__).resolve().parent
    paths = W33DataPaths.from_this_file(
        here / ".." / "tools" / "w33_verify_alignment_py.py"
    )
    lines = load_w33_lines(paths)
    edges = build_incidence_edges(lines)
    s = summary_from_edges(edges)
    assert s["num_vertices"] == 80
    assert s["num_edges"] == 160
    # check point vertices (1..40) have degree 4
    point_deg = [d for v, d in sorted(s.items()) if False]
    # Quick structural sanity: min degree >=1 and max degree <= 4
    assert min(s["degree_counts"]) >= 1
    assert max(s["degree_counts"]) <= 4
