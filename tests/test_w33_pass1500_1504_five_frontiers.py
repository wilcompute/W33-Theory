from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "w33_pass1500_1504_five_frontiers.json"
EXPECTED_CERT_SHA = "757b01bacbfc157484851ec76cc3322204116c3aeb9cdf81851a2dbee1a56b3e"
EXPECTED_WORKERS = {
    "1500": "ccdc1e773121897bf87c03d7eaf40dd46b9daf0272f45b779c76fba643f6f3e6",
    "1501": "45ffc89206d187b1d6ed8bf6d74f19580ec6aaf8e89fe76d2145b1e53bd4add2",
    "1502": "cf30ef9d35441f22a1cb39380fb3bcdd00ae73cf592d2b7b337a0d4823b1b564",
    "1503": "c96cd9f52681256db4795e1c17fc8352951fa11f02a0d354d2b0efe52611328d",
    "1504": "60105b7a9d3b73cc714d5b828c5a9a6296af0fa383247884ba109ee60c137956",
}


def payload():
    return json.loads(CERT.read_text(encoding="utf-8"))


def test_certificate_digest_and_schema():
    assert hashlib.sha256(CERT.read_bytes()).hexdigest() == EXPECTED_CERT_SHA
    data = payload()
    assert data["schema"] == "w33.pass1500_1504.five_frontiers.v1"
    assert data["status"] == "PASS"
    assert data["worker_sha256"] == EXPECTED_WORKERS


def test_modular_ext_quivers():
    p = payload()["pass1500_modular_ext_quivers"]
    assert p["p2_vertex_count"] == 13
    assert p["p2_arrow_dimension_sum"] == 15
    assert p["p2_radical_power_dimensions"] == [45, 16, 0]
    assert p["p2_loewy_layers"] == [38, 29, 16]
    assert p["p3_vertex_count"] == 5
    assert p["p3_arrow_dimension_sum"] == 14
    assert p["p3_radical_power_dimensions"] == [72, 49, 27, 14, 4, 0]
    assert p["p3_loewy_layers"] == [11, 23, 22, 13, 10, 4]


def test_tensor_fourier_exactness():
    p = payload()["pass1501_tensor_fourier"]
    assert p["block_dimensions"] == [1, 2, 2, 4, 4, 8, 8, 2, 4, 12, 12, 24, 32, 5]
    assert p["exact_inverse_verified"] is True
    assert p["inverse_constructed_blockwise"] is True
    assert p["tensor_basis_U"]["sha256"] == "58b5c1cdc2aefd67a4efde0221f4a708b8e1267b5eb4bad8e1a586bf02ff84b7"
    assert p["tensor_inverse_Uinv"]["sha256"] == "bb75dd295832c7a76fd0a72268ac328fbd437676670bef6ecc64cb1fb12fc160"


def test_bridge_census():
    p = payload()["pass1502_bridge_classification"]
    assert p["family_size"] == 96
    assert p["sheet_rank_distribution"] == {"70": 4, "76": 1, "81": 19}
    assert p["bridge_rank_distribution"] == {"70": 16, "76": 4, "81": 76}
    assert p["rank81_full_on_all_14_sources"] == 57
    assert p["rank81_terminal_dimension_loss"] == 19
    assert p["all_rank81_sheets_equal_steinberg"] is True


def test_maximal_overorder():
    p = payload()["pass1503_maximal_overorder"]
    assert p["orbital_order_contained"] is True
    assert p["global_index_factorization"] == {"2": 36, "3": 113}
    assert p["maximal_discriminant"] == "1"
    assert p["discriminant_index_identity_verified"] is True
    assert p["p_maximal_at_2_and_3"] is True


def test_linking_algebra():
    p = payload()["pass1504_linking_algebra"]
    assert p["rank81_gauge_bridges"] == 76
    assert p["independent_bridge_dimension"] == 75
    assert p["relation_dimension"] == 1
    assert p["relation_support"] == 12
    assert p["relation_exact_over_Z"] is True
    assert p["collective_selector_image_rank"] == 120
    assert p["collective_cycle_detection_rank"] == 81
    assert p["left_corner_dimension"] == 120 * 120
    assert p["right_corner_dimension"] == 81 * 81
    assert p["bridge_bimodule_dimension"] == 120 * 81
    assert p["linking_envelope_dimension"] == 201 * 201
    assert p["strict_morita_context"] is True


def test_canonical_source_namespace():
    source = "\n".join(
        path.read_text(encoding="utf-8")
        for path in [
            ROOT / "analysis" / "w33_pass1500_1504_five_frontiers.py",
            *sorted((ROOT / "analysis" / "pass1500_1504").glob("*.py")),
        ]
    )
    assert "Pass 141" not in source
    assert "Pass 142" not in source
    assert "pass1410_1414" not in source


def test_report_and_registry_certificate_lock():
    digest = hashlib.sha256(CERT.read_bytes()).hexdigest()
    report = (ROOT / "analysis" / "BT1500_BT1504_five_frontiers.md").read_text(encoding="utf-8")
    registry = json.loads((ROOT / "data" / "w33_pass_namespace_registry_v2.d" / "1500-1504.json").read_text(encoding="utf-8"))
    assert digest in report
    block = registry["canonical_blocks"][0]
    assert block["range"] == "1500-1504"
    assert block["compact_certificate_sha256"] == digest
    assert block["worker_sha256"] == EXPECTED_WORKERS
