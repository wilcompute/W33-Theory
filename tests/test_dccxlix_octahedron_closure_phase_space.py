"""Part DCCXLIX -- Octahedron closure phase-space tests."""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dccxlix_octahedron_closure_phase_space import (  # noqa: E402
    CODEC,
    NILPOTENCE_INDEX,
    OUT_PATH,
    Q,
    TOMOTOPE_CELLS,
    build_bridge,
    closure_generator,
    closure_resolvent,
    line_graph_of_tetrahedron,
    octahedron_edges,
    octahedron_faces,
    octahedron_vertices,
    verify_nilpotence_index,
    write_bridge,
)


def test_octahedron_has_6_vertices():
    assert len(octahedron_vertices()) == 6


def test_octahedron_has_12_edges():
    verts = octahedron_vertices()
    edges = octahedron_edges(verts)
    assert len(edges) == 12


def test_octahedron_has_8_faces():
    verts = octahedron_vertices()
    faces = octahedron_faces(verts)
    assert len(faces) == 8


def test_f_vector_is_6_12_8():
    verts = octahedron_vertices()
    edges = octahedron_edges(verts)
    faces = octahedron_faces(verts)
    assert (len(verts), len(edges), len(faces)) == (6, 12, 8)


def test_euler_characteristic_2():
    verts = octahedron_vertices()
    edges = octahedron_edges(verts)
    faces = octahedron_faces(verts)
    euler = len(verts) - len(edges) + len(faces)
    assert euler == 2


def test_all_vertices_degree_4():
    verts = octahedron_vertices()
    edges = octahedron_edges(verts)
    for i in range(len(verts)):
        deg = sum(1 for e in edges if i in e)
        assert deg == 4


def test_three_axis_pairs():
    verts = octahedron_vertices()
    axes = {v[0] for v in verts}
    assert axes == {"B23", "B31", "B12"}
    assert len(axes) == 3 == Q


def test_octahedron_V_equals_q_factorial():
    assert 6 == math.factorial(Q)


def test_octahedron_V_equals_nilpotence_index():
    assert 6 == NILPOTENCE_INDEX


def test_octahedron_E_equals_codec():
    assert 12 == CODEC


def test_octahedron_F_equals_tomotope_cells():
    assert 8 == TOMOTOPE_CELLS


def test_line_graph_of_K4_is_octahedron():
    lg = line_graph_of_tetrahedron()
    assert lg["L_edge_count"] == 12
    assert lg["is_octahedron_edge_count"] is True


def test_closure_generator_nilpotent_at_6():
    G = closure_generator(6)
    P = np.eye(6)
    powers = [P.copy()]
    for _ in range(7):
        P = P @ G
        powers.append(P.copy())
    assert not np.allclose(powers[5], 0)
    assert np.allclose(powers[6], 0)


def test_closure_generator_matches_octahedron_V():
    nilp = verify_nilpotence_index()
    assert nilp["nilpotence_index"] == len(octahedron_vertices())


def test_resolvent_matches_neumann_series():
    G = closure_generator(6)
    R1 = closure_resolvent(1.0, 6)
    # (I - G) R(1) should equal I (matrix inverse)
    I = np.eye(6)
    assert np.allclose((I - G) @ R1, I, atol=1e-10)


def test_eight_faces_are_sign_patterns():
    """The 8 octahedron faces correspond to 2^3 = 8 sign patterns of the 3 axes."""
    verts = octahedron_vertices()
    faces = octahedron_faces(verts)
    assert len(faces) == 2 ** Q == 8


def test_summary_all_identities_hold():
    b = build_bridge()
    assert b["summary"]["all_identities_hold"] is True


def test_identities_all_pass():
    b = build_bridge()
    failed = [k for k, v in b["identities"].items() if not v]
    assert failed == []


def test_correspondence_three_layers():
    b = build_bridge()
    corr = b["correspondence"]
    assert set(corr.keys()) == {"clock_levels", "generator_transitions", "oscillator_modes"}
    assert corr["clock_levels"]["count"] == 6
    assert corr["generator_transitions"]["count"] == 12
    assert corr["oscillator_modes"]["count"] == 8


def test_theorem_and_one_line_present():
    b = build_bridge()
    assert "Phase-Space Theorem" in b["theorem"]
    assert "octahedron" in b["one_line"].lower()


def test_honesty_boundary_explicit():
    b = build_bridge()
    boundary = b["honesty_boundary"].lower()
    assert "does not" in boundary


def test_write_and_reload():
    out = write_bridge()
    assert out.exists()
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["summary"]["all_identities_hold"] is True


def test_json_has_expected_keys():
    if not OUT_PATH.exists():
        write_bridge()
    data = json.loads(OUT_PATH.read_text(encoding="utf-8"))
    for key in (
        "summary",
        "octahedron",
        "line_graph_check",
        "closure_clock_nilpotence_check",
        "correspondence",
        "identities",
        "theorem",
        "one_line",
        "honesty_boundary",
    ):
        assert key in data
