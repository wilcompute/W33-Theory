from __future__ import annotations

import csv
import json
from pathlib import Path

import pytest
from w33_center_quad_gq42_e6_bridge import (
    build_center_quad_gq42_e6_bridge_summary,
    center_quad_pairing,
    center_quads,
    line_graph_triangles,
    quotient_incidence,
    quotient_lines,
    quotient_points,
    write_summary,
)


def test_center_quads_form_90_element_involutive_cover() -> None:
    quads = center_quads()
    pairing = center_quad_pairing()
    assert len(quads) == 90
    assert all(pairing[pairing[index]] == index for index in range(90))
    assert all(pairing[index] != index for index in range(90))
    assert len({tuple(sorted((index, pairing[index]))) for index in range(90)}) == 45


def test_quotient_points_are_45_antipodal_pairs_with_support_size_8() -> None:
    points = quotient_points()
    assert len(points) == 45
    assert all(len(point.support_vertices) == 8 for point in points)
    assert len({point.quad_pair for point in points}) == 45


def test_quotient_lines_are_27_five_point_partitions() -> None:
    lines = quotient_lines()
    assert len(lines) == 27
    assert all(len(line.point_ids) == 5 for line in lines)
    assert all(len(line.lifted_quads) == 10 for line in lines)
    quads = center_quads()
    for line in lines:
        seen = set()
        for quad_id in line.lifted_quads:
            quad = set(quads[quad_id])
            assert not (seen & quad)
            seen.update(quad)
        assert len(seen) == 40


def test_quotient_incidence_is_exact_dual_gq42() -> None:
    point_to_lines, line_to_points = quotient_incidence()
    assert len(point_to_lines) == 45
    assert len(line_to_points) == 27
    assert {len(lines) for lines in point_to_lines.values()} == {3}
    assert {len(points) for points in line_to_points.values()} == {5}
    assert sum(len(lines) for lines in point_to_lines.values()) == 135


def test_exceptional_line_graph_has_schlafli_complement_parameters() -> None:
    point_to_lines, line_to_points = quotient_incidence()
    adjacency = {line_id: set() for line_id in line_to_points}
    for lines in point_to_lines.values():
        a, b, c = lines
        adjacency[a].update((b, c))
        adjacency[b].update((a, c))
        adjacency[c].update((a, b))
    vertices = sorted(adjacency)
    assert {len(adjacency[v]) for v in vertices} == {10}
    adjacent_common = set()
    nonadjacent_common = set()
    edge_count = 0
    for index, left in enumerate(vertices):
        for right in vertices[index + 1 :]:
            common = len(adjacency[left] & adjacency[right])
            if right in adjacency[left]:
                adjacent_common.add(common)
                edge_count += 1
            else:
                nonadjacent_common.add(common)
    assert edge_count == 135
    assert adjacent_common == {1}
    assert nonadjacent_common == {5}


def test_45_quotient_points_equal_45_line_graph_triangles() -> None:
    point_to_lines, _ = quotient_incidence()
    assert len(line_graph_triangles()) == 45
    assert set(line_graph_triangles()) == {
        tuple(sorted(lines)) for lines in point_to_lines.values()
    }


def test_reconstruction_matches_archived_v13_incidence_counts() -> None:
    archive_path = Path(
        "bundles/v13_GQ42_reconstruction/center_quad_gq42_v13/gq42_incidence_check.json"
    )
    raw = archive_path.read_text(encoding="utf-8")
    if raw.startswith("version https://git-lfs.github.com/spec/"):
        pytest.skip("Git LFS payload missing for archived v13 incidence check")
    archived = json.loads(raw)

    point_to_lines, line_to_points = quotient_incidence()
    assert archived == {
        "n_points": len(point_to_lines),
        "n_lines": len(line_to_points),
        "points_per_line": len(next(iter(line_to_points.values()))),
        "lines_per_point": len(next(iter(point_to_lines.values()))),
        "incidences": sum(len(lines) for lines in point_to_lines.values()),
    }


def test_summary_records_exact_exceptional_bridge(tmp_path: Path) -> None:
    summary = build_center_quad_gq42_e6_bridge_summary()
    assert summary["status"] == "ok"
    assert summary["w33_seed"]["center_quads"] == 90
    assert summary["dual_gq42_incidence"] == {
        "points": 45,
        "lines": 27,
        "points_per_line": 5,
        "lines_per_point": 3,
        "incidences": 135,
    }
    assert summary["exceptional_graphs"]["point_graph_srg"]["edge_count"] == 270
    assert summary["exceptional_graphs"]["line_graph_srg"] == {
        "vertices": 27,
        "degree": 10,
        "lambda": 1,
        "mu": 5,
        "edge_count": 135,
        "degree_spectrum_singleton": True,
        "adjacent_common_singleton": True,
        "nonadjacent_common_singleton": True,
    }
    assert summary["exceptional_graphs"]["line_graph_triangles"] == 45
    assert summary["exceptional_graphs"]["points_equal_line_graph_triangles"] is True
    assert "direct exact bridge" in summary["bridge_verdict"]

    out = write_summary(tmp_path / "w33_center_quad_gq42_e6_bridge_summary.json")
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["status"] == "ok"
    assert data["quotient_cover"]["line_lift_partitions_all_40_w33_vertices"] is True
