import json
from pathlib import Path

import pandas as pd

BASE = (
    Path("archive/dirs/TOE_pocket20_K5_edgepair_cover_v01_20260227_bundle")
    / "TOE_pocket20_K5_edgepair_cover_v01_20260227"
)


def test_pocket20_summary():
    data = json.load(open(BASE / "summary.json"))
    assert data["num_pockets_containing_center"] == 105
    assert data["num_pockets_center_with_4_labeled_vertices"] == 90
    assert data["num_edgepairs"] == 45
    assert data["each_edgepair_has_two_completions"] is True


def test_orbit10_structure():
    data = json.load(open(BASE / "orbit10_lines_k5_structure.json"))
    records = data["orbit10_line_to_k5_edge_and_special_face"]
    # expect a list of ten records
    assert isinstance(records, list)
    assert len(records) == 10
    for rec in records:
        assert "line_id" in rec and "k5_edge" in rec


def test_vertex_edge_mapping():
    data = json.load(open(BASE / "srg_vertices20_to_k5edge.json"))
    assert len(data) == 20
    for edges in data.values():
        assert len(edges) == 2


def test_pocket_cover_csv():
    df = pd.read_csv(BASE / "pocket20_edgepair_cover.csv")
    # there are 90 records
    assert len(df) == 90
    # each edgepair appears twice
    counts = df[["k5_edge1", "k5_edge2"]].apply(tuple, axis=1).value_counts()
    assert all(c == 2 for c in counts)
