#!/usr/bin/env python3
"""Pass 414: cryptographically sealed independent-laboratory handoff packet."""
from __future__ import annotations

import argparse
import base64
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from typing import Any

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from cryptography.hazmat.primitives import serialization

from w33_pass410_414_common import canonical_json, certificate, write_json

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass414_independent_lab_packet.json"
FIXTURE = ROOT / "data" / "w33_pass414_nonclaim_custody_fixture.json"
TEMPLATE = ROOT / "data" / "w33_pass414_empty_handoff_manifest.json"

ROLES = ["protocol_owner", "acquisition_lab", "blind_key_custodian", "blinded_analyst", "independent_auditor"]


def parse_time(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("timezone required")
    return parsed.astimezone(timezone.utc)


def deterministic_private(role: str) -> Ed25519PrivateKey:
    seed = hashlib.sha256(("w33-pass414-nonclaim:" + role).encode()).digest()
    return Ed25519PrivateKey.from_private_bytes(seed)


def public_b64(private: Ed25519PrivateKey) -> str:
    raw = private.public_key().public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)
    return base64.b64encode(raw).decode()


def sign_envelope(role: str, artifact_type: str, payload: dict, signed_at: str) -> dict:
    private = deterministic_private(role)
    payload_bytes = canonical_json(payload)
    body = {
        "schema": "w33.pass414.signature-envelope.v1",
        "artifact_type": artifact_type,
        "payload_sha256": hashlib.sha256(payload_bytes).hexdigest(),
        "signed_at": signed_at,
        "signer_role": role,
        "public_key_ed25519_base64": public_b64(private),
    }
    signature = private.sign(canonical_json(body))
    return {**body, "signature_ed25519_base64": base64.b64encode(signature).decode()}


def verify_envelope(envelope: dict, payload: dict) -> bool:
    if envelope["payload_sha256"] != hashlib.sha256(canonical_json(payload)).hexdigest():
        return False
    public = Ed25519PublicKey.from_public_bytes(base64.b64decode(envelope["public_key_ed25519_base64"]))
    body = {k: v for k, v in envelope.items() if k != "signature_ed25519_base64"}
    try:
        public.verify(base64.b64decode(envelope["signature_ed25519_base64"]), canonical_json(body))
    except Exception:
        return False
    return True


def empty_template() -> dict:
    return {
        "schema": "w33.pass414.independent-lab-handoff.v1",
        "claim_mode": "physical_production",
        "study_id": None,
        "device_id": None,
        "roles": {role: {"organization": None, "contact": None, "public_key_ed25519_base64": None} for role in ROLES},
        "artifacts": {
            "frozen_protocol": {"path": None, "sha256": None, "signature_envelope": None},
            "accepted_bom": {"path": None, "sha256": None, "signature_envelope": None},
            "calibration_certificate": {"path": None, "sha256": None, "signature_envelope": None},
            "blinded_raw_counts": {"path": None, "sha256": None, "signature_envelope": None},
            "blinded_analysis": {"path": None, "sha256": None, "signature_envelope": None},
            "blind_key": {"path": None, "sha256": None, "signature_envelope": None},
            "unblinded_result": {"path": None, "sha256": None, "signature_envelope": None},
            "independent_audit": {"path": None, "sha256": None, "signature_envelope": None},
        },
        "timestamps": {
            "protocol_frozen_at": None,
            "bom_accepted_at": None,
            "calibrated_at": None,
            "acquisition_started_at": None,
            "acquisition_completed_at": None,
            "analysis_completed_at": None,
            "key_revealed_at": None,
            "audit_completed_at": None,
        },
        "physical_experiment_completed": False,
        "claim_eligible": False,
    }


def build_fixture() -> dict:
    times = {
        "protocol_frozen_at": "2026-07-18T09:00:00-04:00",
        "bom_accepted_at": "2026-07-18T09:30:00-04:00",
        "calibrated_at": "2026-07-18T10:00:00-04:00",
        "acquisition_started_at": "2026-07-18T10:30:00-04:00",
        "acquisition_completed_at": "2026-07-18T10:45:00-04:00",
        "analysis_completed_at": "2026-07-18T11:15:00-04:00",
        "key_revealed_at": "2026-07-18T11:30:00-04:00",
        "audit_completed_at": "2026-07-18T12:00:00-04:00",
    }
    payloads = {
        "frozen_protocol": {"study_type": "nonclaim_test_fixture", "protocol": "Pass-409 four-gate Choi falsifier", "version": 1},
        "accepted_bom": {"study_type": "nonclaim_test_fixture", "accepted": True, "exceptions": []},
        "calibration_certificate": {"study_type": "nonclaim_test_fixture", "mode_overlap": 0.96, "non_dark_fraction": 0.98},
        "blinded_raw_counts": {"study_type": "nonclaim_test_fixture", "rows": 128, "gate_labels_present": False, "content_sha256": hashlib.sha256(b"pass414-nonclaim-raw").hexdigest()},
        "blinded_analysis": {"study_type": "nonclaim_test_fixture", "gate_labels_present": False, "analysis_sha256": hashlib.sha256(b"pass414-nonclaim-analysis").hexdigest()},
        "blind_key": {"study_type": "nonclaim_test_fixture", "mapping_sha256": hashlib.sha256(b"pass414-nonclaim-key").hexdigest()},
        "unblinded_result": {"study_type": "nonclaim_test_fixture", "claim_eligible": False, "physical_experiment_completed": False},
        "independent_audit": {"study_type": "nonclaim_test_fixture", "hash_chain_verified": True, "role_separation_verified": True},
    }
    role_for = {
        "frozen_protocol": "protocol_owner",
        "accepted_bom": "independent_auditor",
        "calibration_certificate": "acquisition_lab",
        "blinded_raw_counts": "acquisition_lab",
        "blinded_analysis": "blinded_analyst",
        "blind_key": "blind_key_custodian",
        "unblinded_result": "blinded_analyst",
        "independent_audit": "independent_auditor",
    }
    time_for = {
        "frozen_protocol": times["protocol_frozen_at"],
        "accepted_bom": times["bom_accepted_at"],
        "calibration_certificate": times["calibrated_at"],
        "blinded_raw_counts": times["acquisition_completed_at"],
        "blinded_analysis": times["analysis_completed_at"],
        "blind_key": times["key_revealed_at"],
        "unblinded_result": times["key_revealed_at"],
        "independent_audit": times["audit_completed_at"],
    }
    artifacts = {}
    for artifact_type, payload in payloads.items():
        artifacts[artifact_type] = {
            "payload": payload,
            "payload_sha256": hashlib.sha256(canonical_json(payload)).hexdigest(),
            "signature_envelope": sign_envelope(role_for[artifact_type], artifact_type, payload, time_for[artifact_type]),
        }
    return {
        "schema": "w33.pass414.independent-lab-handoff.v1",
        "claim_mode": "nonclaim_test_fixture",
        "study_id": "PASS414-NONCLAIM-FIXTURE",
        "device_id": "NO-PHYSICAL-DEVICE",
        "roles": {role: {"organization": "nonclaim-fixture", "public_key_ed25519_base64": public_b64(deterministic_private(role))} for role in ROLES},
        "artifacts": artifacts,
        "timestamps": times,
        "physical_experiment_completed": False,
        "claim_eligible": False,
    }


def verify_fixture(fixture: dict) -> dict[str, bool]:
    times = {key: parse_time(value) for key, value in fixture["timestamps"].items()}
    signatures = all(
        verify_envelope(record["signature_envelope"], record["payload"])
        for record in fixture["artifacts"].values()
    )
    roles = {name: record["signature_envelope"]["signer_role"] for name, record in fixture["artifacts"].items()}
    checks = {
        "all_signatures_verify": signatures,
        "protocol_before_acquisition": times["protocol_frozen_at"] < times["acquisition_started_at"],
        "bom_before_acquisition": times["bom_accepted_at"] < times["acquisition_started_at"],
        "calibration_before_acquisition": times["calibrated_at"] < times["acquisition_started_at"],
        "acquisition_ordered": times["acquisition_started_at"] <= times["acquisition_completed_at"],
        "analysis_after_acquisition": times["analysis_completed_at"] > times["acquisition_completed_at"],
        "key_reveal_after_blinded_analysis": times["key_revealed_at"] > times["analysis_completed_at"],
        "audit_after_unblinding": times["audit_completed_at"] > times["key_revealed_at"],
        "raw_and_key_have_different_custodians": roles["blinded_raw_counts"] != roles["blind_key"],
        "analysis_and_key_have_different_custodians": roles["blinded_analysis"] != roles["blind_key"],
        "auditor_independent_of_acquisition": roles["independent_audit"] != roles["blinded_raw_counts"],
        "fixture_cannot_claim_physical_completion": fixture["physical_experiment_completed"] is False and fixture["claim_eligible"] is False,
    }
    return checks


def build_payload() -> tuple[dict, dict, dict]:
    fixture = build_fixture()
    checks = verify_fixture(fixture)
    template = empty_template()
    checks.update({
        "five_separate_roles": len(ROLES) == 5,
        "template_defaults_to_no_claim": template["physical_experiment_completed"] is False and template["claim_eligible"] is False,
        "template_contains_all_eight_artifacts": len(template["artifacts"]) == 8,
    })
    packet = {
        "schema": "w33.pass414.independent_lab_packet.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "roles": ROLES,
        "required_artifact_chain": [
            "frozen_protocol",
            "accepted_bom",
            "calibration_certificate",
            "blinded_raw_counts",
            "blinded_analysis",
            "blind_key",
            "unblinded_result",
            "independent_audit",
        ],
        "custody_rules": {
            "raw_counts_vs_blind_key": "must be held by different roles until blinded analysis is hash-frozen",
            "analyst_vs_key": "blinded analyst cannot possess the key before analysis completion",
            "auditor": "must not be the acquisition signer or blind-key custodian",
            "signatures": "Ed25519 over canonical envelope containing artifact SHA-256, role, type, and timestamp",
        },
        "production_runbook": [
            "populate the empty handoff manifest and public keys before protocol freeze",
            "freeze protocol and BOM; sign both before acquisition",
            "calibrate and sign the calibration certificate before acquisition",
            "acquire blinded counts with no gate labels and sign their raw-byte hash",
            "run blinded analysis and sign its hash before key release",
            "release the separately signed blind key",
            "unblind through Pass 397 without --test-mode",
            "independent auditor verifies every hash, signature, timestamp, role separation rule, and final claim boundary",
        ],
        "files": {
            "empty_manifest": "data/w33_pass414_empty_handoff_manifest.json",
            "nonclaim_signature_fixture": "data/w33_pass414_nonclaim_custody_fixture.json",
            "schema": "schemas/w33_pass414_independent_lab_handoff_v1.schema.json",
            "human_runbook": "docs/W33_PASS414_INDEPENDENT_LAB_HANDOFF.md",
        },
        "physical_claim_boundary": "No physical acquisition occurred in this release. Deterministic private keys and fixture payloads are test-only and must never be used in production.",
        "checks": checks,
    }
    packet["certificate_sha256"] = certificate(packet)
    fixture["certificate_sha256"] = certificate(fixture)
    template["template_sha256"] = certificate(template)
    return packet, fixture, template


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--output", type=Path, default=OUT)
    parser.add_argument("--fixture", type=Path, default=FIXTURE)
    parser.add_argument("--template", type=Path, default=TEMPLATE)
    args = parser.parse_args()
    packet, fixture, template = build_payload()
    expected = [
        (args.output, json.dumps(packet, indent=2, sort_keys=True) + "\n"),
        (args.fixture, json.dumps(fixture, indent=2, sort_keys=True) + "\n"),
        (args.template, json.dumps(template, indent=2, sort_keys=True) + "\n"),
    ]
    if args.check:
        for path, text in expected:
            if not path.exists() or path.read_text() != text:
                raise SystemExit(f"Pass 414 artifact drift: {path}")
    else:
        write_json(args.output, packet)
        write_json(args.fixture, fixture)
        write_json(args.template, template)
    print(json.dumps({"status": packet["status"], "checks": sum(packet["checks"].values()), "total": len(packet["checks"])}))
    return 0 if packet["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
