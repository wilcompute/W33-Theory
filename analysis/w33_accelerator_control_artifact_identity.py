#!/usr/bin/env python3
"""Derive the process-independent compiled-control cache identity for the selected accelerator macro."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from w33_attested_accelerator_macro import build as build_accelerator
from w33_steinberg_control_artifact_cache import build_artifact

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "W33_ACCELERATOR_CONTROL_ARTIFACT_IDENTITY.json"


def build() -> dict[str, Any]:
    cert = build_accelerator()
    artifact = build_artifact(
        basis_digest=cert["steinbergBasisDigest"],
        action_table_digest=cert["actionTableDigest"],
        steinberg_action_digest=cert["steinbergActionDigest"],
        executable_word=tuple(tuple(x) for x in cert["executableTimeOrder"]),
        calibration_epoch=cert["calibrationEpoch"],
    )
    checks = {
        "symplectic_frame_matches_accelerator": artifact["symplectic_frame_digest"] == cert["symplecticFrameDigest"],
        "basis_matches_accelerator": artifact["basis_digest"] == cert["steinbergBasisDigest"],
        "action_table_matches_accelerator": artifact["action_table_digest"] == cert["actionTableDigest"],
        "steinberg_action_matches_accelerator": artifact["steinberg_action_digest"] == cert["steinbergActionDigest"],
        "executable_word_matches_accelerator": artifact["executable_time_order"] == cert["executableTimeOrder"],
        "calibration_epoch_matches_accelerator": artifact["calibration_epoch"] == cert["calibrationEpoch"],
    }
    return {
        "schema": "w33.accelerator-control-artifact-identity.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "acceleratorCertificateDigest": cert["acceleratorCertificateDigest"],
        "controlArtifact": artifact,
        "theorem": "The controlArtifact.artifact_id is independent of process/continuation authority and is exactly keyed by corrected symplectic frame, Steinberg basis/table/action, executable time-order word and calibration epoch.",
        "boundary": "A matching cache key authorizes no process and proves no physical calibration. Continuation-specific authorization and measured calibration evidence remain separate.",
    }


if __name__ == "__main__":
    out = build()
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=2, sort_keys=True))
    raise SystemExit(out["status"] != "PASS")
