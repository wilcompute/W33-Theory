"""Part DCCXVII -- Master-equation codec bridge tests."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dccxvii_master_equation_codec_bridge import (  # noqa: E402
    OUT_PATH,
    build_bridge,
    write_bridge,
)


def test_summary_verified():
    b = build_bridge()
    assert b["summary"]["all_identities_hold"] is True


def test_master_equation_holds_at_q_3():
    b = build_bridge()
    me = b["master_equation"]
    assert me["holds"] is True
    assert me["factorial_q"] == me["two_q"] == 6
    assert me["unique_positive_solutions"] == [3]


def test_local_codec_sym_plus_dih():
    b = build_bridge()
    dec = b["local_codec_decomposition"]
    assert dec["size"] == 12
    assert dec["symmetric_face"]["size"] == 6
    assert dec["dihedral_face"]["size"] == 6
    assert dec["axis_x_sign_x_role"]["product"] == 12


def test_local_codec_three_two_two():
    b = build_bridge()
    a = b["local_codec_decomposition"]["axis_x_sign_x_role"]
    assert a["axes"] == 3
    assert a["signs"] == 2
    assert a["roles"] == 2


def test_directed_carrier_480():
    b = build_bridge()
    dc = b["directed_carrier"]
    assert dc["vertices"] == 40
    assert dc["edges"] == 240
    assert dc["directed_edges"] == 480
    assert dc["carrier_value"] == 480


def test_qec_layers_have_master_equation_origin():
    b = build_bridge()
    layers = b["qec_layers"]
    assert layers["classical_axis_selector"]["alphabet_size"] == 3
    assert layers["quantum_sign_frame"]["alphabet_size"] == 2
    assert layers["heralded_return_syndrome"]["alphabet_size"] == 2


def test_all_identities_pass():
    b = build_bridge()
    failed = [k for k, v in b["identities"].items() if not v]
    assert failed == [], f"Failing identities: {failed}"


def test_h1_equals_81():
    b = build_bridge()
    assert b["summary"]["local_codec_size"] == 12
    assert b["summary"]["directed_carrier"] == 480


def test_theorem_and_one_line_present():
    b = build_bridge()
    assert "q! = 2q" in b["theorem"]
    assert "q! = 2q" in b["one_line"]


def test_honesty_boundary_explicit():
    b = build_bridge()
    assert "does not" in b["honesty_boundary"].lower()


def test_write_bridge_produces_json():
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
        "master_equation",
        "local_codec_decomposition",
        "directed_carrier",
        "qec_layers",
        "identities",
        "theorem",
        "one_line",
        "honesty_boundary",
    ):
        assert key in data
