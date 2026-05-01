import json
import subprocess
import sys


def test_reconstruction_equivariance(tmp_path, capsys):
    # run the reconstruction script and capture output
    result = subprocess.run(
        [sys.executable, "tools/reconstruct_w33_e8_mapping.py"],
        capture_output=True,
        text=True,
    )
    out = result.stdout + result.stderr
    assert "reconstruction succeeded" in out
    assert "stabilizer of edge 0 has size 216" in out

    # also double-check the mapping file matches expectations
    with open("data/w33_e8_mapping.json") as f:
        orig = json.load(f)
    from tools.reconstruct_w33_e8_mapping import (
        build_W33,
        edge_orbit_from_transvections,
    )

    vertices, edges = build_W33()
    orig_map = [orig[str(i)] for i in range(len(edges))]
    edge_orbit = edge_orbit_from_transvections(vertices, edges)

    assert len(edges) == 240
    assert len(edge_orbit) == len(edges)
    assert sorted(orig_map) == list(range(len(edges)))
