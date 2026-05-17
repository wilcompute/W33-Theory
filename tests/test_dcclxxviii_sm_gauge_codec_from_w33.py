"""Part DCCLXXVIII -- SM gauge codec from W(3,3) tests."""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dcclxxviii_sm_gauge_codec_from_w33 import (  # noqa: E402
    H_1,
    K,
    OUT_PATH,
    Q,
    build_bridge,
    chain_lift_matter_antimatter,
    octahedron_to_sm_correspondence,
    sm_gauge_decomposition,
    sm_total_dim,
    w33_as_universal_quantum_computer,
    write_bridge,
)


def test_SU3_dim_8_eq_2_to_q():
    sm = sm_gauge_decomposition()
    assert sm["SU(3)_C"]["dim"] == 8 == 2 ** Q


def test_SU2_dim_3_eq_q():
    sm = sm_gauge_decomposition()
    assert sm["SU(2)_L"]["dim"] == 3 == Q


def test_U1_dim_1():
    sm = sm_gauge_decomposition()
    assert sm["U(1)_Y"]["dim"] == 1


def test_SM_total_dim_eq_codec():
    assert sm_total_dim() == 12 == K


def test_8_plus_3_plus_1_eq_codec():
    assert 8 + 3 + 1 == K == 12


def test_8_gluons_eq_octahedron_faces():
    """8 gluons = 8 octahedron faces = 2^q sign-orientation patterns."""
    assert 8 == 2 ** Q


def test_3_W_bosons_eq_octahedron_axes():
    """3 W-bosons = 3 octahedron antipodal pairs = q axes."""
    assert 3 == Q


def test_octahedron_correspondence_5_rows():
    rows = octahedron_to_sm_correspondence()
    assert len(rows) == 5


def test_H_1_eq_81():
    assert H_1 == 81 == Q ** (Q + 1)


def test_H_1_prime_eq_162():
    chain = chain_lift_matter_antimatter()
    assert chain["H_1_prime"] == 162 == 2 * H_1


def test_chain_lift_exact_sequence():
    chain = chain_lift_matter_antimatter()
    assert "0 -> 81 -> 162 -> 81 -> 0" in chain["exact_sequence"]


def test_universal_qc_register_file_eq_81():
    uqc = w33_as_universal_quantum_computer()
    assert uqc["register_file"]["size"] == H_1 == 81


def test_universal_qc_instruction_set_eq_codec():
    uqc = w33_as_universal_quantum_computer()
    assert uqc["instruction_set"]["size"] == K == 12


def test_universal_qc_bus_width_eq_240():
    uqc = w33_as_universal_quantum_computer()
    assert uqc["bus_width"]["size"] == 240


def test_universal_qc_directed_eq_480():
    uqc = w33_as_universal_quantum_computer()
    assert uqc["directed_carrier"]["size"] == 480


def test_universal_qc_clock_eq_6():
    uqc = w33_as_universal_quantum_computer()
    assert uqc["clock"]["size"] == math.factorial(Q) == 6


def test_summary_all_identities_hold():
    b = build_bridge()
    assert b["summary"]["all_identities_hold"] is True


def test_identities_all_pass():
    b = build_bridge()
    failed = [k for k, v in b["identities"].items() if not v]
    assert failed == []


def test_theorem_and_one_line_present():
    b = build_bridge()
    assert "SM Gauge Codec" in b["theorem"]
    assert "codec" in b["one_line"]


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
        "sm_gauge_decomposition",
        "octahedron_to_sm_correspondence",
        "chain_lift_matter_antimatter",
        "w33_as_universal_quantum_computer",
        "identities",
        "theorem",
        "one_line",
        "honesty_boundary",
    ):
        assert key in data
