#!/usr/bin/env python3
"""Export one attestation-ready receipt-preserving accelerator certificate.

The Steinberg-safe macro theorem already proves finite-control equivalence for
all reported windows.  This module turns the strongest real-trace window into a
small cross-repository ABI object that Holotrade can bind into measured boot.

The certificate commits:
  * exact parent/child continuation tuple and generations;
  * receipt-chain and continuation-chain digests;
  * explicit HoloVM->Steinberg symplectic frame;
  * Steinberg basis/action-table identities;
  * sequential Sp(4,3) endpoint and Steinberg-81 action;
  * executable time-order transvection word;
  * calibration epoch namespace.

No physical calibration evidence is fabricated.  ``physicalCalibrationEvidenceDigest``
is null, so the certificate is suitable for software/control attestation only.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from w33_semantic_safe_photonic_macroop import trace
from w33_steinberg_control_artifact_cache import CALIBRATION_EPOCH, SYMPLECTIC_FRAME
from w33_steinberg_photonic_macro_refinement import verify as verify_refinement

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "W33_ATTESTED_ACCELERATOR_MACRO.json"


def digest(value: Any) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"), default=str).encode()
    return "sha256:" + hashlib.sha256(raw).hexdigest()


def build() -> dict[str, Any]:
    refinement = verify_refinement()
    if refinement["status"] != "PASS":
        raise AssertionError("Steinberg macro refinement is not green")
    _program, _memory, rows = trace()
    best = refinement["best_window"]
    start, width = int(best["start"]), int(best["width"])
    window = rows[start:start + width]
    if len(window) != width:
        raise AssertionError("selected accelerator window escaped real trace")
    body = {
        "schema": "w33.attested-accelerator-macro.v1",
        "machineType": "w33.circuit216.steinberg81",
        "parentContinuationRoot": window[0].parent.continuation_id,
        "childContinuationRoot": window[-1].child.continuation_id,
        "processId": window[0].parent.process_id,
        "generationBefore": window[0].parent.generation,
        "generationAfter": window[-1].child.generation,
        "windowStart": start,
        "windowWidth": width,
        "receiptChainDigest": best["receipt_chain_digest"],
        "continuationChainDigest": best["continuation_chain_digest"],
        "symplecticFrameDigest": digest(SYMPLECTIC_FRAME),
        "steinbergBasisDigest": refinement["basis_digest"],
        "actionTableDigest": refinement["action_table_digest"],
        "sequentialGroupEndpointDigest": best["sequential_group_endpoint_digest"],
        "steinbergActionDigest": best["steinberg_action_digest"],
        "executableTimeOrder": best["executable_time_order"],
        "naiveTransvections": best["naive_transvections"],
        "executableTransvections": best["executable_transvections"],
        "calibrationEpoch": CALIBRATION_EPOCH,
        "physicalCalibrationEvidenceDigest": None,
        "evidenceClass": "software-finite-control-equivalence",
    }
    return {**body, "acceleratorCertificateDigest": digest(body)}


def verify_certificate(cert: dict[str, Any]) -> dict[str, Any]:
    fresh = build()
    checks = {
        "schema_matches": cert.get("schema") == "w33.attested-accelerator-macro.v1",
        "content_digest_matches": cert.get("acceleratorCertificateDigest") == digest({k: v for k, v in cert.items() if k != "acceleratorCertificateDigest"}),
        "rebuild_is_deterministic": cert == fresh,
        "real_window_advances_generation_exactly_by_width": cert["generationAfter"] - cert["generationBefore"] == cert["windowWidth"],
        "receipt_and_continuation_chains_are_committed": cert["receiptChainDigest"].startswith("sha256:") and cert["continuationChainDigest"].startswith("sha256:"),
        "corrected_symplectic_frame_is_committed": cert["symplecticFrameDigest"] == digest(SYMPLECTIC_FRAME),
        "software_certificate_does_not_fake_physical_calibration": cert["physicalCalibrationEvidenceDigest"] is None,
    }
    return {
        "schema": "w33.attested-accelerator-macro-verification.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "certificate": cert,
        "theorem": "This content identity names one exact receipt-preserving finite-control accelerator substitution on the corrected Steinberg-81 frame and exact authenticated continuation interval.",
        "boundary": "The certificate proves software/group/representation equivalence only. Hardware-backed execution requires Holotrade measured-boot binding plus future non-null calibration evidence under an explicit physical policy.",
    }


def main() -> int:
    cert = build()
    OUT.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    result = verify_certificate(cert)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
