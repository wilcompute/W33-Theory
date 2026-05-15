from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dccxvi_axis_syndrome_selector_codec_bridge import build_bridge


def test_dccxvi_summary_factors_local_and_global_codec() -> None:
    payload = build_bridge()
    summary = payload["summary"]

    assert summary["local_codec_size"] == 12
    assert summary["classical_axis_trits"] == 40
    assert summary["fusion_attempt_slots"] == 480
    assert summary["klm_primitive_slots"] == 960
    assert summary["all_identities_hold"] is True


def test_dccxvi_local_codec_is_axis_sign_role_product() -> None:
    codec = build_bridge()["local_codec"]

    assert codec["axis_alphabet"] == ["B12", "B23", "B31"]
    assert codec["sign_alphabet"] == ["+", "-"]
    assert codec["role_alphabet"] == ["accepted", "return"]
    assert len(codec["local_slots"]) == 3 * 2 * 2
    assert codec["factorization"] == "12 = 3 axes * 2 signs * 2 accepted/return roles"


def test_dccxvi_global_codec_layers_match_480_and_960() -> None:
    global_codec = build_bridge()["global_codec"]

    assert global_codec["vertices"] == 40
    assert global_codec["axis_layer_slots"] == 120
    assert global_codec["signed_axis_layer_slots"] == 240
    assert global_codec["fusion_attempt_slots"] == 480
    assert global_codec["klm_primitive_slots"] == 960


def test_dccxvi_selector_record_is_40_trits_not_12_ary_selector() -> None:
    selector = build_bridge()["selector_record"]

    assert selector["classical_selector_trits"] == 40
    assert selector["choices_per_trit"] == 3
    assert 2**63 < selector["selector_state_count"] < 2**64
    assert selector["fits_64_bit_envelope"] is True
    assert "sign and accepted/return role remain syndrome/frame layers" in selector["read"]


def test_dccxvi_layer_roles_separate_classical_quantum_syndrome_optical() -> None:
    roles = build_bridge()["layer_roles"]

    assert roles["classical_axis_selector"]["alphabet_size"] == 3
    assert roles["quantum_sign_frame"]["alphabet_size"] == 2
    assert roles["heralded_return_syndrome"]["alphabet_size"] == 2
    assert roles["klm_rail_lift"]["alphabet_size"] == 2


def test_dccxvi_qec_read_preserves_h1_tail() -> None:
    payload = build_bridge()
    qec = payload["qec_read"]

    assert qec["edge_qubits"] == 240
    assert qec["logical_h1"] == 81
    assert qec["css_identity"] == "39 + 120 + 81 = 240"
    assert all(payload["identities"].values())


def test_dccxvi_markdown_and_boundary_are_present() -> None:
    payload = build_bridge()
    text = (ROOT / "PART_DCCXVI_AXIS_SYNDROME_SELECTOR_CODEC_BRIDGE.md").read_text(
        encoding="utf-8"
    )

    assert "480 = 40 * 12 = 40 * 3 * 2 * 2" in text
    assert "does not model hardware noise rates" in payload["honesty_boundary"]


def test_dccxvi_index_exposes_axis_syndrome_codec() -> None:
    text = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")

    assert "Axis-Syndrome Selector\n              Codec Bridge" in text
    assert "<code>12=3&times;2&times;2</code>" in text
    assert "the selector trit chooses one of three Clifford" in text
