import json
import subprocess
import sys
from pathlib import Path

import pytest

from tools.w33_rootword_uv_parser import W33RootwordParser

COMBINED_EDGE_ROOT_MAP = Path("artifacts/edge_to_e8_root_combined.json")

pytestmark = pytest.mark.skipif(
    not COMBINED_EDGE_ROOT_MAP.exists(),
    reason="optional consolidated edge-to-E8 root map is absent",
)


def is_rotation(a, b):
    # check if list b is any rotation or reversed rotation of a
    if len(a) != len(b):
        return False
    n = len(a)
    for s in range(n):
        if all(a[(i + s) % n] == b[i] for i in range(n)):
            return True
    rb = list(reversed(b))
    for s in range(n):
        if all(a[(i + s) % n] == rb[i] for i in range(n)):
            return True
    return False


SAMPLE_EDGE_ROOTS = [
    [-1, -1, -2, -2, -2, -2, -1, -1],
    [1, 1, 2, 2, 2, 2, 1, 1],
    [-1, -1, -1, -2, -2, -1, -1, 0],
    [1, 2, 3, 4, 3, 2, 1, 0],
    [-1, -3, -3, -5, -4, -3, -2, -1],
    [0, 0, 0, 1, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 0],
    [0, -1, -1, -1, -1, -1, 0, 0],
]


def build_minimal_rootwords(tmp_path: Path) -> list[dict]:
    outdir = tmp_path / "minimal_commutator_cycles"
    cmd = [
        sys.executable,
        "tools/compute_ordered_root_word_invariants.py",
        "--outdir",
        str(outdir),
        "--require-root-edges",
    ]
    run = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert run.returncode == 0, run.stderr

    return json.loads(
        (outdir / "minimal_holonomy_cycles_ordered_rootwords.json").read_text(
            encoding="utf-8"
        )
    )


def test_sample_cycle_parses_correctly():
    p = W33RootwordParser()
    out = p.parse(SAMPLE_EDGE_ROOTS)

    # sample expected values from repo minimal sample
    expected_cycle = [4, 23, 4, 24, 8, 5, 35, 30]
    assert len(out["cycle_vertices"]) == 8
    assert is_rotation(out["cycle_vertices"], expected_cycle)

    assert out["u_canonical"] == (1, 0)
    assert out["v_canonical"] == (1, 2)
    assert out["k_canonical"] == 1

    # basepoint p recovered as the intersection of the two N12 lines
    assert out.get("p") == (2, 2)


def test_parse_all_minimal_root_covered_cycles_no_exceptions(tmp_path: Path):
    p = W33RootwordParser()
    data = build_minimal_rootwords(tmp_path)
    assert data, "compute_ordered_root_word_invariants.py produced no cycles"
    for entry in data:
        assert entry.get("edge_roots_present") is True
        rw = entry["edge_roots"]
        out = p.parse(rw)
        assert isinstance(out["k_canonical"], int)
        assert len(out["cycle_vertices"]) == 8
        assert isinstance(out["u_canonical"], tuple)
        assert isinstance(out["v_canonical"], tuple)
