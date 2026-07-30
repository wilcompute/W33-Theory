#!/usr/bin/env python3
"""Small, readable runner for the GAP-owned Pass 1147 certificate."""
from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
GAP_SOURCE = (
    ROOT / "analysis" / "w33_pass1147_schlaefli_steinberg_fourier_bridge.g"
)
CERTIFICATE = (
    ROOT / "data" / "w33_pass1147_schlaefli_steinberg_fourier_bridge.json"
)
REQUIRED_SECTIONS = (
    "directed_schlaefli",
    "steinberg_transform",
    "a2_color_torsor",
    "enhanced_map",
    "residual_representation",
)


class TransparentCertificateError(RuntimeError):
    """Raised when the checked-in source or its certificate fails validation."""


def load_certificate(
    path: Path,
    required_sections: Iterable[str] = REQUIRED_SECTIONS,
) -> dict[str, Any]:
    try:
        certificate = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise TransparentCertificateError(
            f"cannot read Pass 1147 certificate {path}: {exc}"
        ) from exc
    if certificate.get("status") != "PASS":
        raise TransparentCertificateError(
            f"Pass 1147 certificate is not PASS: {certificate.get('status')!r}"
        )
    schema = certificate.get("schema")
    if not isinstance(schema, str) or not schema.startswith("w33.pass1147."):
        raise TransparentCertificateError(
            f"unexpected Pass 1147 schema: {schema!r}"
        )
    missing = [name for name in required_sections if name not in certificate]
    if missing:
        raise TransparentCertificateError(
            "Pass 1147 certificate is missing section(s): " + ", ".join(missing)
        )
    return certificate


def run_gap_certificate(timeout: int = 240) -> tuple[dict[str, Any], str]:
    """Run GAP in a temporary directory, leaving the checkout untouched."""

    gap = shutil.which("gap")
    if gap is None:
        raise TransparentCertificateError("GAP is required for Pass 1147")
    if not GAP_SOURCE.is_file():
        raise TransparentCertificateError(
            f"checked-in Pass 1147 GAP source is missing: {GAP_SOURCE}"
        )

    with tempfile.TemporaryDirectory(prefix="w33-pass1147-") as directory:
        scratch = Path(directory)
        (scratch / "data").mkdir()
        output = scratch / "w33_pass1147_schlaefli_steinberg_fourier_bridge.json"
        environment = os.environ.copy()
        completed = subprocess.run(
            [gap, "-q", str(GAP_SOURCE)],
            cwd=scratch,
            env=environment,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=timeout,
        )
        if completed.returncode != 0:
            raise TransparentCertificateError(
                "Pass 1147 GAP producer failed:\n" + completed.stdout[-4000:]
            )
        certificate_path = (
            scratch
            / "data"
            / "w33_pass1147_schlaefli_steinberg_fourier_bridge.json"
        )
        certificate = load_certificate(certificate_path)
        return certificate, completed.stdout


def obtain_certificate(
    path: Path | None,
    required_sections: Iterable[str],
) -> tuple[dict[str, Any], bool, str]:
    """Load an explicit certificate or execute its transparent GAP producer."""

    if path is not None:
        return load_certificate(path, required_sections), False, ""
    certificate, stdout = run_gap_certificate()
    missing = [name for name in required_sections if name not in certificate]
    if missing:
        raise TransparentCertificateError(
            "Pass 1147 certificate is missing section(s): " + ", ".join(missing)
        )
    return certificate, True, stdout
