from __future__ import annotations

import importlib.util
import gzip
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("bt2762", ROOT / "analysis" / "bt2762_five_frontiers.py")
MOD = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MOD)


def test_transpose_and_fourier_direction_reversal():
    cx_rev = MOD.mm(MOD.mm(MOD.TRANSPOSE, MOD.CX_PF), MOD.TRANSPOSE)
    f_synth = MOD.mm(MOD.inv(MOD.F_F), MOD.F_P)
    assert MOD.mm(MOD.TRANSPOSE, MOD.TRANSPOSE) == MOD.I
    assert MOD.mm(MOD.mm(MOD.tr(MOD.TRANSPOSE), MOD.J), MOD.TRANSPOSE) == tuple(
        tuple((-x) % 3 for x in row) for row in MOD.J
    )
    assert MOD.mm(MOD.mm(f_synth, MOD.CX_PF), MOD.inv(f_synth)) == cx_rev


def test_d12_contract_and_magic_handshake():
    d12 = [(r, s) for r in range(6) for s in range(2)]
    assert len({MOD.d12_mul(a, b) for a in d12 for b in d12}) == 12
    assert all(
        MOD.d12_mul(MOD.d12_mul(a, b), c) == MOD.d12_mul(a, MOD.d12_mul(b, c))
        for a in d12 for b in d12 for c in d12
    )
    state = {
        "frame": (0, 0, 0, 0),
        "mirror": (0, 0),
        "magic_pending": False,
        "magic_ray": 0,
        "magic_consumed": 0,
        "fault": False,
        "retired": False,
    }
    req = MOD.isa_step(state, 7, 35)
    assert req["magic_pending"] and not req["retired"]
    ack = MOD.isa_step(req, 0, magic_ack=True)
    assert ack["magic_consumed"] == 1 and ack["retired"]
    assert MOD.isa_step(state, 7, 36)["fault"]


def test_frozen_certificates_are_complete():
    cert = json.loads((ROOT / "data" / "PART_BT2762_BT2766_FIVE_FRONTIERS_results.json").read_text(encoding="utf-8"))
    atlas = json.loads(gzip.decompress((ROOT / 'data' / 'PART_BT2764_SP43_GEOMETRIC_GATE_CLASS_ATLAS.json.gz').read_bytes()))
    assert all(cert["checks"].values())
    assert cert["centralizer"]["structure"] == "C6 x C3 x S3"
    assert cert["isa"]["magic_grade_map_bt822_order"].count(0) == 8
    assert cert["isa"]["magic_grade_map_bt822_order"].count(1) == 24
    assert cert["isa"]["magic_grade_map_bt822_order"].count(2) == 4
    assert atlas["group_order"] == 51840
    assert atlas["class_count"] == 34
    assert atlas["carrier_sizes"]["apartments"] == 1620
    assert sum(row["size"] for row in atlas["rows"]) == 51840
    assert atlas["projective_signature_count"] == 15


def test_physical_qutrit_sum_permutation():
    cert = json.loads((ROOT / "data" / "PART_BT2762_BT2766_FIVE_FRONTIERS_results.json").read_text(encoding="utf-8"))
    perm = cert["physical_sum_compiler"]["permutation"]
    assert sorted(perm) == list(range(9))
    for f in range(3):
        for t in range(3):
            assert perm[3 * f + t] == 3 * f + ((t + f) % 3)
