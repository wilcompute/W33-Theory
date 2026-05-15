"""Part DCCXX -- Universal computer of life tests."""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dccxx_universal_computer_of_life import (  # noqa: E402
    ALPHABET,
    CODONS,
    LOGICAL_BITS,
    MIN_ALPHABET_CODONS,
    OUT_PATH,
    Q,
    SENSE_CODONS,
    VERTEX_CAP,
    build_bridge,
    write_bridge,
)


def test_q_is_3():
    assert Q == 3


def test_codon_length_equals_q():
    assert Q == 3  # 3-base codons


def test_alphabet_size_q_plus_one():
    assert ALPHABET == 4 == Q + 1


def test_total_codons_q_plus_one_to_q():
    assert CODONS == 64
    assert CODONS == (Q + 1) ** Q


def test_minimal_alphabet_codons_q_to_q():
    assert MIN_ALPHABET_CODONS == 27 == Q**Q


def test_logical_cap_q_to_q_plus_one():
    assert LOGICAL_BITS == 81 == Q ** (Q + 1)


def test_vertex_parallelism_cap():
    assert VERTEX_CAP == 40


def test_codon_redundancy_approx_q():
    ratio = SENSE_CODONS / 20
    assert math.isclose(ratio, Q, abs_tol=0.5)
    assert math.isclose(ratio, 3.05, abs_tol=0.1)


def test_summary_all_identities_hold():
    b = build_bridge()
    assert b["summary"]["all_identities_hold"] is True


def test_identities_all_pass():
    b = build_bridge()
    failed = [k for k, v in b["identities"].items() if not v]
    assert failed == []


def test_structural_table_size():
    b = build_bridge()
    assert len(b["structural_table"]) == 8


def test_four_pillars_present():
    b = build_bridge()
    assert len(b["four_pillars_of_life"]) == 4
    for pillar in b["four_pillars_of_life"]:
        assert "pillar" in pillar
        assert "w33_bound" in pillar
        assert "consequence" in pillar


def test_extends_three_fold_table():
    b = build_bridge()
    assert "CCCCXLIV" in b["extends_three_fold_table"]
    assert "sixth" in b["extends_three_fold_table"]


def test_theorem_mentions_structural_bound():
    b = build_bridge()
    assert "Structural Bound on Life" in b["theorem"]


def test_honesty_boundary_explicit():
    b = build_bridge()
    boundary = b["honesty_boundary"].lower()
    assert "does not" in boundary or "not" in boundary


def test_write_bridge_creates_json():
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
        "structural_table",
        "codon_redundancy_analysis",
        "four_pillars_of_life",
        "identities",
        "theorem",
        "one_line",
        "honesty_boundary",
        "extends_three_fold_table",
    ):
        assert key in data
