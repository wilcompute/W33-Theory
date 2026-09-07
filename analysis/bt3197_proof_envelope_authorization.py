#!/usr/bin/env python3
"""Pass 3197: fail-closed proof-envelope authorization contract."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "PART_BT3197_PROOF_ENVELOPE_AUTHORIZATION_results.json"
REQUIRED_FIELDS = (
    "schema", "candidate", "engine_provenance", "source_provenance",
    "shard_provenance", "independent_certifier", "projector_witness",
    "pauli_spectrum", "logical_frame", "success_probability",
    "magic_witness", "accepted_error_series",
)


def canonical(payload: dict) -> bytes:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("ascii")


def authorize(envelope: dict) -> dict:
    fields = envelope.get("fields", {})
    present = set(fields)
    missing = sorted(set(REQUIRED_FIELDS) - present)
    extras = sorted(present - set(REQUIRED_FIELDS))
    expected = envelope.get("expected_sha256", "")
    computed = hashlib.sha256(canonical(fields)).hexdigest()
    shard = fields.get("shard_provenance", {})
    shard_ok = (
        isinstance(shard.get("index"), int)
        and isinstance(shard.get("count"), int)
        and shard["count"] > 0
        and 0 <= shard["index"] < shard["count"]
    )
    cert = fields.get("independent_certifier", {})
    accepted = bool(cert.get("accepted"))
    cert_ok = bool(cert.get("passed"))
    schema_ok = fields.get("schema") == "w33.proof_carrying_m36_candidate.v1"
    reasons = []
    if missing: reasons.append("missing_fields")
    if extras: reasons.append("unknown_fields")
    if expected != computed: reasons.append("digest")
    if not shard_ok: reasons.append("shard")
    if not accepted: reasons.append("not_accepted")
    if not cert_ok: reasons.append("independent_certifier")
    if not schema_ok: reasons.append("schema")
    return {"authorized": not reasons, "reasons": reasons, "computed_sha256": computed}


def fixture() -> dict:
    fields = {
        "schema": "w33.proof_carrying_m36_candidate.v1",
        "candidate": {"name": "synthetic_protocol_fixture"},
        "engine_provenance": {"sha256": "0" * 64},
        "source_provenance": {"sha256": "1" * 64},
        "shard_provenance": {"index": 9, "count": 256},
        "independent_certifier": {"passed": True, "accepted": True, "schema": "w33.pass3134.rank3_certifier.v1"},
        "projector_witness": {"sha256": "2" * 64},
        "pauli_spectrum": {"sha256": "3" * 64},
        "logical_frame": {"sha256": "4" * 64},
        "success_probability": "1/8",
        "magic_witness": {"weyl_negativity": "1/16", "product_stabilizer_fidelity_lower_bound": "3/4"},
        "accepted_error_series": {"first_order": "2/3", "second_order": "5/9"},
    }
    return {"fields": fields, "expected_sha256": hashlib.sha256(canonical(fields)).hexdigest()}


def main() -> None:
    good = fixture()
    good_result = authorize(good)
    assert good_result["authorized"]

    digest_bad = json.loads(json.dumps(good))
    digest_bad["fields"]["candidate"]["name"] = "tampered"
    digest_result = authorize(digest_bad)
    assert not digest_result["authorized"] and "digest" in digest_result["reasons"]

    incomplete = json.loads(json.dumps(good))
    del incomplete["fields"]["projector_witness"]
    incomplete["expected_sha256"] = hashlib.sha256(canonical(incomplete["fields"])).hexdigest()
    incomplete_result = authorize(incomplete)
    assert not incomplete_result["authorized"] and "missing_fields" in incomplete_result["reasons"]

    rejected = json.loads(json.dumps(good))
    rejected["fields"]["independent_certifier"]["accepted"] = False
    rejected["expected_sha256"] = hashlib.sha256(canonical(rejected["fields"])).hexdigest()
    rejected_result = authorize(rejected)
    assert not rejected_result["authorized"] and "not_accepted" in rejected_result["reasons"]

    result = {
        "schema": "w33.pass3197.proof_envelope_authorization.v1",
        "required_field_count": len(REQUIRED_FIELDS),
        "required_fields": list(REQUIRED_FIELDS),
        "positive_control": good_result,
        "digest_tamper_control": digest_result,
        "missing_witness_control": incomplete_result,
        "rejected_candidate_control": rejected_result,
        "rtl_contract": "The hardware gate receives a cryptographically computed digest and expected digest, checks equality, field completeness, duplicate rejection, provenance, shard bounds and independent acceptance before authorization.",
        "boundary": "The committed RTL is the fail-closed envelope/authorization gate and digest comparator. SHA-256 computation itself remains an upstream accelerator or software service; no accepted physical M36 candidate is asserted."
    }
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"authorized_positive": True, "negative_controls": 3}, sort_keys=True))


if __name__ == "__main__":
    main()
