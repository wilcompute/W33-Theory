#!/usr/bin/env python3
"""Export the measurement contract for a future physical accelerator epoch.

This file intentionally creates *no* calibration measurement.  It derives a
content-addressed request from the already certified receipt-preserving
accelerator macro and names exactly what a physical calibration authority would
have to measure and sign before Holotrade may call the accelerator physically
calibrated.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from w33_attested_accelerator_macro import build as build_accelerator

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "W33_ACCELERATOR_CALIBRATION_REQUEST.json"


def digest(value: Any) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"), default=str).encode()
    return "sha256:" + hashlib.sha256(raw).hexdigest()


def build() -> dict[str, Any]:
    cert = build_accelerator()
    body = {
        "schema": "w33.accelerator-calibration-request.v1",
        "acceleratorCertificateDigest": cert["acceleratorCertificateDigest"],
        "calibrationEpoch": cert["calibrationEpoch"],
        "machineType": cert["machineType"],
        "symplecticFrameDigest": cert["symplecticFrameDigest"],
        "steinbergActionDigest": cert["steinbergActionDigest"],
        "sequentialGroupEndpointDigest": cert["sequentialGroupEndpointDigest"],
        "executableTimeOrder": cert["executableTimeOrder"],
        "requiredMeasurementFields": [
            "deviceIdentityDigest",
            "measuredTransferMatrixDigest",
            "rawMeasurementSetDigest",
            "sampleCount",
            "observedMaxInfidelityPpm",
            "observedMaxLeakagePpm",
            "measuredAt",
            "sourceClass",
            "calibrationAuthorityKeyId",
        ],
        "requiredSourceClassForPhysicalAdmission": "hardware-measured",
        "thresholdOwnership": "Holotrade deployment policy supplies fidelity/leakage/sample thresholds; W33 does not fabricate device tolerances.",
    }
    return {**body, "calibrationRequestDigest": digest(body)}


def verify() -> dict[str, Any]:
    row = build()
    cert = build_accelerator()
    checks = {
        "request_binds_exact_accelerator_certificate": row["acceleratorCertificateDigest"] == cert["acceleratorCertificateDigest"],
        "request_binds_software_calibration_epoch": row["calibrationEpoch"] == cert["calibrationEpoch"],
        "request_binds_corrected_symplectic_frame": row["symplecticFrameDigest"] == cert["symplecticFrameDigest"],
        "request_binds_exact_steinberg_action": row["steinbergActionDigest"] == cert["steinbergActionDigest"],
        "no_physical_measurement_is_fabricated": cert["physicalCalibrationEvidenceDigest"] is None,
        "physical_source_class_is_explicit": row["requiredSourceClassForPhysicalAdmission"] == "hardware-measured",
        "request_is_content_addressed": row["calibrationRequestDigest"] == digest({k: v for k, v in row.items() if k != "calibrationRequestDigest"}),
    }
    return {
        "schema": "w33.accelerator-calibration-request-verification.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "request": row,
        "boundary": "This is an evidence ABI only. It supplies no transfer matrix, fidelity, leakage, device identity, sample count, measurement timestamp, or physical calibration claim.",
    }


if __name__ == "__main__":
    out = verify()
    OUT.write_text(json.dumps(out["request"], indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=2, sort_keys=True))
    raise SystemExit(out["status"] != "PASS")
