#!/usr/bin/env python3
"""Pass 419: adversarial rehearsal and hardened v2 laboratory custody."""
from __future__ import annotations

import argparse
import base64
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import tempfile
from typing import Any

import jsonschema
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey

from w33_pass410_414_common import canonical_json, certificate, write_json

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass419_adversarial_replication.json"
FIXTURE = ROOT / "data" / "w33_pass419_hardened_custody_fixture.json"
ATTACKS = ROOT / "data" / "w33_pass419_attack_matrix.json"
RAW = ROOT / "data" / "w33_pass419_nonclaim_raw_counts.jsonl"
SCHEMA = ROOT / "schemas" / "w33_pass419_hardened_handoff_v2.schema.json"

ROLES = ("protocol_owner", "acquisition_lab", "blind_key_custodian", "blinded_analyst", "independent_auditor")
ARTIFACTS = (
    "frozen_protocol",
    "accepted_bom",
    "calibration_certificate",
    "blinded_raw_counts",
    "blinded_analysis",
    "blind_key",
    "unblinded_result",
    "independent_audit",
)
ROLE_FOR = {
    "frozen_protocol": "protocol_owner",
    "accepted_bom": "independent_auditor",
    "calibration_certificate": "acquisition_lab",
    "blinded_raw_counts": "acquisition_lab",
    "blinded_analysis": "blinded_analyst",
    "blind_key": "blind_key_custodian",
    "unblinded_result": "blinded_analyst",
    "independent_audit": "independent_auditor",
}
BASE_TIMES = (
    "2026-07-18T09:00:00-04:00",
    "2026-07-18T09:20:00-04:00",
    "2026-07-18T09:40:00-04:00",
    "2026-07-18T10:30:00-04:00",
    "2026-07-18T11:00:00-04:00",
    "2026-07-18T11:15:00-04:00",
    "2026-07-18T11:30:00-04:00",
    "2026-07-18T12:00:00-04:00",
)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_payload(payload: dict) -> str:
    return sha256_bytes(canonical_json(payload))


def envelope_hash(envelope: dict) -> str:
    return sha256_bytes(canonical_json(envelope))


def parse_time(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("timezone required")
    return parsed.astimezone(timezone.utc)


def deterministic_private(role: str, namespace: str = "A") -> Ed25519PrivateKey:
    seed = hashlib.sha256(f"w33-pass419-{namespace}:{role}".encode()).digest()
    return Ed25519PrivateKey.from_private_bytes(seed)


def public_b64(private: Ed25519PrivateKey) -> str:
    raw = private.public_key().public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)
    return base64.b64encode(raw).decode()


def generate_raw_rows(count: int = 128) -> bytes:
    lines = []
    for row in range(count):
        record = {
            "blind_code": f"B{row % 4}",
            "epoch": row,
            "heralds": 1000 + 7 * row,
            "coincidences": 700 + (19 * row + 11) % 211,
            "gate_labels_present": False,
        }
        lines.append(json.dumps(record, sort_keys=True, separators=(",", ":")))
    return ("\n".join(lines) + "\n").encode()


def sign_envelope(body: dict, private: Ed25519PrivateKey) -> dict:
    signature = private.sign(canonical_json(body))
    return {**body, "signature_ed25519_base64": base64.b64encode(signature).decode()}


def verify_signature(envelope: dict) -> bool:
    try:
        public = Ed25519PublicKey.from_public_bytes(base64.b64decode(envelope["public_key_ed25519_base64"]))
        body = {key: value for key, value in envelope.items() if key != "signature_ed25519_base64"}
        public.verify(base64.b64decode(envelope["signature_ed25519_base64"]), canonical_json(body))
        return True
    except Exception:
        return False


def build_manifest(
    raw_path: Path,
    *,
    namespace: str = "A",
    study_id: str = "PASS419-NONCLAIM-A",
    device_id: str = "NO-PHYSICAL-DEVICE-A",
    manifest_nonce: str = "4190aabbccddeeff0011223344556677",
    times: tuple[str, ...] = BASE_TIMES,
    payload_overrides: dict[str, dict] | None = None,
    key_collision: bool = False,
    claim_flags: tuple[bool, bool] = (False, False),
) -> dict:
    payload_overrides = payload_overrides or {}
    privates = {role: deterministic_private(role, namespace) for role in ROLES}
    if key_collision:
        privates["blind_key_custodian"] = privates["acquisition_lab"]

    roles = {
        role: {
            "organization": f"pass419-{namespace}-fixture",
            "contact": None,
            "public_key_ed25519_base64": public_b64(privates[role]),
        }
        for role in ROLES
    }

    raw_bytes = raw_path.read_bytes()
    raw_rows = len(raw_bytes.decode().splitlines())
    protocol = {
        "study_type": "nonclaim_test_fixture",
        "protocol": "Pass-409 four-gate Choi falsifier with Pass-413 twirl",
        "version": 2,
        "expected_raw_rows": 128,
        "required_gate_labels_present": False,
    }
    bom = {
        "study_type": "nonclaim_test_fixture",
        "accepted": True,
        "protocol_payload_sha256": sha256_payload(protocol),
        "exceptions": [],
    }
    calibration = {
        "study_type": "nonclaim_test_fixture",
        "protocol_payload_sha256": sha256_payload(protocol),
        "bom_payload_sha256": sha256_payload(bom),
        "mode_overlap": 0.96,
        "non_dark_fraction": 0.98,
    }
    raw_payload = {
        "study_type": "nonclaim_test_fixture",
        "external_path": str(raw_path.relative_to(ROOT)) if raw_path.is_relative_to(ROOT) else str(raw_path),
        "content_sha256": sha256_bytes(raw_bytes),
        "row_count": raw_rows,
        "gate_labels_present": False,
        "calibration_payload_sha256": sha256_payload(calibration),
    }
    analysis = {
        "study_type": "nonclaim_test_fixture",
        "raw_content_sha256": raw_payload["content_sha256"],
        "gate_labels_present": False,
        "analysis_sha256": sha256_bytes(b"pass419-blinded-analysis-v2"),
    }
    blind_key = {
        "study_type": "nonclaim_test_fixture",
        "mapping_sha256": sha256_bytes(b"pass419-separate-blind-key-v2"),
    }
    unblinded = {
        "study_type": "nonclaim_test_fixture",
        "analysis_payload_sha256": sha256_payload(analysis),
        "blind_key_payload_sha256": sha256_payload(blind_key),
        "physical_experiment_completed": claim_flags[0],
        "claim_eligible": claim_flags[1],
    }
    audit = {
        "study_type": "nonclaim_test_fixture",
        "hash_chain_verified": True,
        "role_separation_verified": True,
        "physical_experiment_completed": claim_flags[0],
        "claim_eligible": claim_flags[1],
    }

    payloads = {
        "frozen_protocol": protocol,
        "accepted_bom": bom,
        "calibration_certificate": calibration,
        "blinded_raw_counts": raw_payload,
        "blinded_analysis": analysis,
        "blind_key": blind_key,
        "unblinded_result": unblinded,
        "independent_audit": audit,
    }
    for artifact_type, override in payload_overrides.items():
        payloads[artifact_type] = {**payloads[artifact_type], **override}

    # Rebind dependent hashes after authorized payload changes.  This models an
    # insider who can legitimately re-sign their own artifact, allowing policy
    # attacks to be tested rather than merely failing on stale signatures.
    payloads["accepted_bom"]["protocol_payload_sha256"] = payloads["accepted_bom"].get(
        "protocol_payload_sha256", sha256_payload(payloads["frozen_protocol"])
    )
    payloads["calibration_certificate"].setdefault("protocol_payload_sha256", sha256_payload(payloads["frozen_protocol"]))
    payloads["calibration_certificate"].setdefault("bom_payload_sha256", sha256_payload(payloads["accepted_bom"]))
    payloads["blinded_raw_counts"].setdefault("calibration_payload_sha256", sha256_payload(payloads["calibration_certificate"]))
    payloads["blinded_analysis"].setdefault("raw_content_sha256", payloads["blinded_raw_counts"]["content_sha256"])
    payloads["unblinded_result"].setdefault("analysis_payload_sha256", sha256_payload(payloads["blinded_analysis"]))
    payloads["unblinded_result"].setdefault("blind_key_payload_sha256", sha256_payload(payloads["blind_key"]))

    artifacts = []
    predecessor = None
    for sequence, artifact_type in enumerate(ARTIFACTS):
        role = ROLE_FOR[artifact_type]
        private = privates[role]
        body = {
            "schema": "w33.pass419.signature-envelope.v2",
            "study_id": study_id,
            "device_id": device_id,
            "manifest_nonce": manifest_nonce,
            "sequence": sequence,
            "artifact_type": artifact_type,
            "signer_role": role,
            "predecessor_envelope_sha256": predecessor,
            "payload_sha256": sha256_payload(payloads[artifact_type]),
            "signed_at": times[sequence],
            "public_key_ed25519_base64": public_b64(private),
        }
        envelope = sign_envelope(body, private)
        artifacts.append({"artifact_type": artifact_type, "payload": payloads[artifact_type], "envelope": envelope})
        predecessor = envelope_hash(envelope)

    return {
        "schema": "w33.pass419.hardened-handoff.v2",
        "claim_mode": "nonclaim_test_fixture",
        "study_id": study_id,
        "device_id": device_id,
        "manifest_nonce": manifest_nonce,
        "roles": roles,
        "artifacts": artifacts,
        "physical_experiment_completed": claim_flags[0],
        "claim_eligible": claim_flags[1],
    }


def resolve_external(path_value: str) -> Path:
    path = Path(path_value)
    return path if path.is_absolute() else ROOT / path


def verify_manifest(manifest: dict, *, validate_schema: bool = True) -> list[str]:
    errors: list[str] = []
    if validate_schema:
        try:
            jsonschema.validate(manifest, json.loads(SCHEMA.read_text()))
        except Exception as exc:
            errors.append(f"schema:{type(exc).__name__}")

    if manifest.get("schema") != "w33.pass419.hardened-handoff.v2":
        errors.append("manifest_schema")
    if manifest.get("claim_mode") == "nonclaim_test_fixture" and (
        manifest.get("physical_experiment_completed") or manifest.get("claim_eligible")
    ):
        errors.append("nonclaim_flags")

    roles = manifest.get("roles", {})
    role_keys = [roles.get(role, {}).get("public_key_ed25519_base64") for role in ROLES]
    if len(role_keys) != len(set(role_keys)):
        errors.append("role_key_collision")

    artifacts = manifest.get("artifacts", [])
    if len(artifacts) != len(ARTIFACTS):
        errors.append("artifact_count")
        return sorted(set(errors))

    predecessor = None
    signed_times = []
    payloads: dict[str, dict] = {}
    for sequence, (expected_type, record) in enumerate(zip(ARTIFACTS, artifacts)):
        artifact_type = record.get("artifact_type")
        payload = record.get("payload", {})
        envelope = record.get("envelope", {})
        payloads[artifact_type] = payload
        if artifact_type != expected_type:
            errors.append("artifact_order")
        if envelope.get("sequence") != sequence:
            errors.append("sequence")
        if envelope.get("artifact_type") != artifact_type:
            errors.append("envelope_artifact_type")
        if envelope.get("study_id") != manifest.get("study_id"):
            errors.append("study_binding")
        if envelope.get("device_id") != manifest.get("device_id"):
            errors.append("device_binding")
        if envelope.get("manifest_nonce") != manifest.get("manifest_nonce"):
            errors.append("nonce_binding")
        expected_role = ROLE_FOR.get(artifact_type)
        if envelope.get("signer_role") != expected_role:
            errors.append("signer_role")
        registered_key = roles.get(expected_role, {}).get("public_key_ed25519_base64")
        if envelope.get("public_key_ed25519_base64") != registered_key:
            errors.append("role_key_registry")
        if envelope.get("payload_sha256") != sha256_payload(payload):
            errors.append("payload_hash")
        if envelope.get("predecessor_envelope_sha256") != predecessor:
            errors.append("predecessor_chain")
        if not verify_signature(envelope):
            errors.append("signature")
        try:
            signed_times.append(parse_time(envelope["signed_at"]))
        except Exception:
            errors.append("timestamp_format")
        predecessor = envelope_hash(envelope)

    if len(signed_times) == len(ARTIFACTS) and any(a >= b for a, b in zip(signed_times, signed_times[1:])):
        errors.append("timestamp_order")

    protocol = payloads.get("frozen_protocol", {})
    bom = payloads.get("accepted_bom", {})
    calibration = payloads.get("calibration_certificate", {})
    raw = payloads.get("blinded_raw_counts", {})
    analysis = payloads.get("blinded_analysis", {})
    key = payloads.get("blind_key", {})
    result = payloads.get("unblinded_result", {})
    audit = payloads.get("independent_audit", {})

    if bom.get("protocol_payload_sha256") != sha256_payload(protocol):
        errors.append("bom_protocol_binding")
    if calibration.get("protocol_payload_sha256") != sha256_payload(protocol):
        errors.append("calibration_protocol_binding")
    if calibration.get("bom_payload_sha256") != sha256_payload(bom):
        errors.append("calibration_bom_binding")
    if raw.get("calibration_payload_sha256") != sha256_payload(calibration):
        errors.append("raw_calibration_binding")
    if raw.get("gate_labels_present") is not False or analysis.get("gate_labels_present") is not False:
        errors.append("key_leakage_policy")

    try:
        raw_path = resolve_external(raw["external_path"])
        raw_bytes = raw_path.read_bytes()
        actual_rows = len(raw_bytes.decode().splitlines())
        if sha256_bytes(raw_bytes) != raw.get("content_sha256"):
            errors.append("raw_external_hash")
        if actual_rows != raw.get("row_count"):
            errors.append("raw_manifest_row_count")
        if actual_rows != protocol.get("expected_raw_rows"):
            errors.append("raw_protocol_row_count")
    except Exception:
        errors.append("raw_external_missing")

    if analysis.get("raw_content_sha256") != raw.get("content_sha256"):
        errors.append("analysis_raw_binding")
    if result.get("analysis_payload_sha256") != sha256_payload(analysis):
        errors.append("result_analysis_binding")
    if result.get("blind_key_payload_sha256") != sha256_payload(key):
        errors.append("result_key_binding")
    if manifest.get("claim_mode") == "nonclaim_test_fixture" and any(
        item.get("physical_experiment_completed") or item.get("claim_eligible")
        for item in (result, audit)
    ):
        errors.append("artifact_nonclaim_flags")
    if audit.get("hash_chain_verified") is not True or audit.get("role_separation_verified") is not True:
        errors.append("audit_policy")

    return sorted(set(errors))


def resign_manifest(manifest: dict, namespace: str = "A") -> dict:
    """Re-sign a mutated manifest while preserving its role registry.

    Used only by the adversarial fixture to distinguish policy failures from
    trivial stale-signature failures.
    """
    result = deepcopy(manifest)
    predecessor = None
    for sequence, record in enumerate(result["artifacts"]):
        role = ROLE_FOR[record["artifact_type"]]
        private = deterministic_private(role, namespace)
        body = {
            "schema": "w33.pass419.signature-envelope.v2",
            "study_id": result["study_id"],
            "device_id": result["device_id"],
            "manifest_nonce": result["manifest_nonce"],
            "sequence": sequence,
            "artifact_type": record["artifact_type"],
            "signer_role": role,
            "predecessor_envelope_sha256": predecessor,
            "payload_sha256": sha256_payload(record["payload"]),
            "signed_at": record["envelope"]["signed_at"],
            "public_key_ed25519_base64": public_b64(private),
        }
        record["envelope"] = sign_envelope(body, private)
        predecessor = envelope_hash(record["envelope"])
    return result


def build_attack_matrix(base: dict, second_study: dict) -> list[dict]:
    attacks: list[tuple[str, dict, str]] = []

    mutated = deepcopy(base)
    mutated["artifacts"][5]["envelope"]["signed_at"] = "2026-07-18T10:00:00-04:00"
    attacks.append(("timestamp_substitution", mutated, "signature"))

    mutated = deepcopy(base)
    mutated["artifacts"][3]["payload"]["gate_labels_present"] = True
    mutated = resign_manifest(mutated)
    attacks.append(("authorized_key_leakage", mutated, "key_leakage_policy"))

    mutated = deepcopy(base)
    mutated["artifacts"][2] = deepcopy(second_study["artifacts"][2])
    attacks.append(("cross_study_calibration_replay", mutated, "study_binding"))

    mutated = deepcopy(base)
    foreign = build_manifest(
        RAW,
        namespace="C",
        study_id=base["study_id"],
        device_id="FOREIGN-DEVICE-C",
        manifest_nonce=base["manifest_nonce"],
    )
    mutated["artifacts"][2] = deepcopy(foreign["artifacts"][2])
    attacks.append(("cross_device_replay", mutated, "device_binding"))

    collision = build_manifest(RAW, key_collision=True)
    attacks.append(("role_key_collision", collision, "role_key_collision"))

    mutated = deepcopy(base)
    mutated["artifacts"][2]["payload"]["protocol_payload_sha256"] = "0" * 64
    mutated = resign_manifest(mutated)
    attacks.append(("authorized_calibration_substitution", mutated, "calibration_protocol_binding"))

    with tempfile.NamedTemporaryFile("wb", suffix=".jsonl", delete=False) as handle:
        deleted_path = Path(handle.name)
        handle.write(b"\n".join(RAW.read_bytes().splitlines()[:-1]) + b"\n")
    mutated = deepcopy(base)
    mutated["artifacts"][3]["payload"]["external_path"] = str(deleted_path)
    # Keep original hash and row count: detects unsigned byte deletion.
    mutated = resign_manifest(mutated)
    attacks.append(("selective_row_deletion", mutated, "raw_external_hash"))

    resigned_short = build_manifest(deleted_path)
    attacks.append(("authorized_resigned_row_deletion", resigned_short, "raw_protocol_row_count"))

    mutated = deepcopy(base)
    mutated["artifacts"][4], mutated["artifacts"][5] = mutated["artifacts"][5], mutated["artifacts"][4]
    attacks.append(("artifact_reordering", mutated, "artifact_order"))

    early_times = list(BASE_TIMES)
    early_times[5] = "2026-07-18T10:50:00-04:00"
    early_key = build_manifest(RAW, times=tuple(early_times))
    attacks.append(("early_key_release", early_key, "timestamp_order"))

    mutated = deepcopy(base)
    mutated["manifest_nonce"] = "f" * 32
    attacks.append(("manifest_nonce_substitution", mutated, "nonce_binding"))

    forged = build_manifest(RAW, claim_flags=(True, True))
    attacks.append(("nonclaim_flag_forgery", forged, "nonclaim_flags"))

    rows = []
    for name, manifest, expected in attacks:
        errors = verify_manifest(manifest, validate_schema=False)
        rows.append({
            "attack": name,
            "accepted": not errors,
            "expected_rejection": expected,
            "rejection_reasons": errors,
            "expected_reason_observed": expected in errors,
        })
    try:
        deleted_path.unlink(missing_ok=True)
    except Exception:
        pass
    return rows


def build_payload() -> tuple[dict, dict, dict, bytes]:
    raw_bytes = generate_raw_rows()
    RAW.parent.mkdir(parents=True, exist_ok=True)
    RAW.write_bytes(raw_bytes)

    fixture = build_manifest(RAW)
    second = build_manifest(
        RAW,
        namespace="B",
        study_id="PASS419-NONCLAIM-B",
        device_id="NO-PHYSICAL-DEVICE-B",
        manifest_nonce="4190ffeeddccbbaa7766554433221100",
    )
    base_errors = verify_manifest(fixture)
    attack_rows = build_attack_matrix(fixture, second)

    attack_matrix = {
        "schema": "w33.pass419.attack_matrix.v1",
        "attacks": attack_rows,
        "all_attacks_rejected": all(not row["accepted"] for row in attack_rows),
        "all_expected_reasons_observed": all(row["expected_reason_observed"] for row in attack_rows),
    }
    attack_matrix["certificate_sha256"] = certificate(attack_matrix)

    checks = {
        "raw_fixture_has_128_rows": len(raw_bytes.decode().splitlines()) == 128,
        "base_manifest_schema_valid": not any(error.startswith("schema:") for error in base_errors),
        "base_manifest_independently_verifies": base_errors == [],
        "five_distinct_role_keys": len({fixture["roles"][role]["public_key_ed25519_base64"] for role in ROLES}) == 5,
        "eight_chain_bound_artifacts": len(fixture["artifacts"]) == 8,
        "every_signature_verifies": all(verify_signature(record["envelope"]) for record in fixture["artifacts"]),
        "all_twelve_attacks_rejected": len(attack_rows) == 12 and all(not row["accepted"] for row in attack_rows),
        "all_expected_rejection_reasons_observed": all(row["expected_reason_observed"] for row in attack_rows),
        "fixture_remains_nonclaim": fixture["physical_experiment_completed"] is False and fixture["claim_eligible"] is False,
    }
    checks = {key: bool(value) for key, value in checks.items()}

    payload = {
        "schema": "w33.pass419.adversarial_replication.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "finding": {
            "v1_boundary": "Pass-414 v1 signs each artifact independently but does not cryptographically bind study ID, device ID, manifest nonce, sequence, or predecessor; production use therefore requires the hardened v2 chain",
            "v2_resolution": "every signature binds study/device/nonce/sequence/predecessor, while the independent verifier enforces role-key uniqueness, cross-artifact hashes, raw-byte hashes, row counts, blindness, timestamp order, and nonclaim flags",
        },
        "hardened_contract": {
            "schema_path": "schemas/w33_pass419_hardened_handoff_v2.schema.json",
            "fixture_path": "data/w33_pass419_hardened_custody_fixture.json",
            "raw_fixture_path": "data/w33_pass419_nonclaim_raw_counts.jsonl",
            "attack_matrix_path": "data/w33_pass419_attack_matrix.json",
            "runbook_path": "docs/W33_PASS419_ADVERSARIAL_REPLICATION.md",
            "signature": "Ed25519 over canonical v2 envelope",
            "hash": "SHA-256",
            "chain_length": 8,
        },
        "attack_summary": {
            "count": len(attack_rows),
            "rejected": sum(not row["accepted"] for row in attack_rows),
            "attacks": [row["attack"] for row in attack_rows],
        },
        "physical_claim_boundary": "All keys, counts, signatures, and attacks are deterministic software fixtures. No physical acquisition occurred and no hardware claim is eligible.",
        "checks": checks,
    }
    payload["certificate_sha256"] = certificate(payload)
    fixture["certificate_sha256"] = certificate(fixture)
    return payload, fixture, attack_matrix, raw_bytes


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--output", type=Path, default=OUT)
    parser.add_argument("--fixture", type=Path, default=FIXTURE)
    parser.add_argument("--attacks", type=Path, default=ATTACKS)
    parser.add_argument("--raw", type=Path, default=RAW)
    args = parser.parse_args()
    payload, fixture, attack_matrix, raw_bytes = build_payload()
    expected = [
        (args.output, json.dumps(payload, indent=2, sort_keys=True) + "\n"),
        (args.fixture, json.dumps(fixture, indent=2, sort_keys=True) + "\n"),
        (args.attacks, json.dumps(attack_matrix, indent=2, sort_keys=True) + "\n"),
    ]
    if args.check:
        for path, text in expected:
            if not path.exists() or path.read_text() != text:
                raise SystemExit(f"Pass 419 artifact drift: {path}")
        if not args.raw.exists() or args.raw.read_bytes() != raw_bytes:
            raise SystemExit("Pass 419 raw fixture drift")
    else:
        write_json(args.output, payload)
        write_json(args.fixture, fixture)
        write_json(args.attacks, attack_matrix)
        args.raw.write_bytes(raw_bytes)
    print(json.dumps({"status": payload["status"], "checks": sum(payload["checks"].values()), "total": len(payload["checks"])}))
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
