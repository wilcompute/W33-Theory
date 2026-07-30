"""Regression locks for the transparent Pass 1142-1147 runtime boundary."""
from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]
BUNDLE_RUNTIME = ROOT / "scripts" / "pass1142_1146_bundle_runtime.py"
GAP_SOURCE = (
    ROOT / "analysis" / "w33_pass1147_schlaefli_steinberg_fourier_bridge.g"
)
CERTIFICATE = (
    ROOT / "data" / "w33_pass1147_schlaefli_steinberg_fourier_bridge.json"
)

sys.path.insert(0, str(ROOT))

from scripts import build_540_occurrence_registry as registry
from scripts import pass1142_1146_bundle_runtime as quarantine


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_bundle_fingerprint_is_known_corrupt_and_execution_is_impossible() -> None:
    report = quarantine.inspect_bundle()
    assert report["status"] == "KNOWN_CORRUPT_QUARANTINED"
    assert report["known_corrupt_match"] is True
    assert report["strict_base64_valid"] is False
    assert report["source_execution_enabled"] is False
    assert report["observed"] == {
        "byte_size": 20023,
        "length_mod_4": 3,
        "sha256": (
            "ea2c81f514a38ca8f4ac7a2b4e1c5d6e7af05539721ffc2ae75f8a79ad610897"
        ),
        "ellipsization_offset": 10000,
    }

    namespace = {"sentinel": object()}
    sentinel = namespace["sentinel"]
    with pytest.raises(quarantine.BundleQuarantinedError):
        quarantine.execute_member("analysis/anything.py", namespace)
    assert namespace == {"sentinel": sentinel}

    tree = ast.parse(BUNDLE_RUNTIME.read_text(encoding="utf-8"))
    called_names = {
        node.func.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
    }
    assert not {"exec", "eval", "compile"}.intersection(called_names)
    assert "tarfile" not in BUNDLE_RUNTIME.read_text(encoding="utf-8")


def test_legacy_entrypoints_no_longer_import_the_bundle_executor() -> None:
    for relative in (
        "analysis/w33_pass1142_1146_exact.py",
        "analysis/w33_pass1142_1146_intertwiner.py",
        "analysis/w33_pass1142_1146_release_compiler.py",
        "scripts/build_540_occurrence_registry.py",
        "scripts/build_pass1142_1146_pdf.py",
        "scripts/migrate_shifted_adjacency_descendants.py",
    ):
        text = (ROOT / relative).read_text(encoding="utf-8")
        assert "pass1142_1146_bundle_runtime" not in text
        assert "execute_member(" not in text


def test_explicit_file_registry_is_deterministic_and_refuses_ambiguity(
    tmp_path: Path,
) -> None:
    tagged = tmp_path / "tagged.md"
    tagged.write_text(
        "\n".join(
            [
                "540 {540:point-nonedge}",
                "540 {540:double-six-nonincident}",
                "540 {540:gq42-arc}",
                "540 {540:outer-4c}",
                "540 {540:line-nonedge}",
                "540 {540:mixed}",
                "540 {540:unrelated}",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    first = registry.canonical_bytes(
        registry.build_registry(tmp_path, ["tagged.md"])
    )
    second = registry.canonical_bytes(
        registry.build_registry(tmp_path, ["tagged.md"])
    )
    assert first == second
    payload = json.loads(first)
    assert payload["status"] == "PASS"
    assert payload["literal_occurrences"] == 7
    assert [
        occurrence["category"]
        for occurrence in payload["records"][0]["occurrences"]
    ] == [
        "point-nonedge",
        "double-six-nonincident",
        "gq42-arc",
        "outer-4c",
        "line-nonedge",
        "both",
        "unrelated",
    ]

    tagged.write_text(tagged.read_text(encoding="utf-8") + "plain text\n")
    third = registry.canonical_bytes(
        registry.build_registry(tmp_path, ["tagged.md"])
    )
    assert third != first

    ambiguous = tmp_path / "ambiguous.md"
    ambiguous.write_text("The unlabelled value is 540.\n", encoding="utf-8")
    failed = registry.build_registry(tmp_path, ["ambiguous.md"])
    assert failed["status"] == "NEEDS_TAGGING"
    assert failed["ambiguous_occurrences"] == 1


def test_retired_migration_commands_never_modify_registered_files() -> None:
    ledger = json.loads(
        (
            ROOT / "data" / "w33_shifted_adjacency_retraction_ledger.json"
        ).read_text(encoding="utf-8")
    )
    paths = [
        ROOT / relative
        for relative in ledger["known_descendants"]
        if (ROOT / relative).is_file()
    ]
    before = {path: _sha256(path) for path in paths}

    rejected = subprocess.run(
        [
            sys.executable,
            "scripts/migrate_shifted_adjacency_descendants.py",
            "--apply",
        ],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=30,
    )
    assert rejected.returncode != 0
    assert "--apply is disabled" in rejected.stdout
    assert {path: _sha256(path) for path in paths} == before

    checked = subprocess.run(
        [
            sys.executable,
            "scripts/migrate_shifted_adjacency_descendants.py",
            "--check-only",
        ],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=240,
    )
    assert checked.returncode == 0, checked.stdout[-4000:]
    report = json.loads(checked.stdout)
    assert report["status"] == "PASS"
    assert report["read_only"] is True
    assert report["violations"] == []
    assert {path: _sha256(path) for path in paths} == before


def test_workflows_are_validation_only() -> None:
    workflows = (
        ROOT / ".github" / "workflows" / "pass1142_1146_exact_release.yml",
        ROOT / ".github" / "workflows" / "pass1142_1146_pr_materialize.yml",
        ROOT / ".github" / "workflows" / "bootstrap_pass1137_1141.yml",
    )
    forbidden = (
        "contents: write",
        "pull-requests: write",
        "git config",
        "git add",
        "git commit",
        "git push",
        "--apply",
        "--write-report",
        "--json-out",
        "base64 --decode",
        "tar -x",
        "build_pass1142_1146_pdf.py",
    )
    for workflow in workflows:
        text = workflow.read_text(encoding="utf-8")
        assert "contents: read" in text
        for token in forbidden:
            assert token not in text, f"{workflow.name} contains {token!r}"


def test_pdf_builder_fails_closed() -> None:
    completed = subprocess.run(
        [sys.executable, "scripts/build_pass1142_1146_pdf.py"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=30,
    )
    assert completed.returncode != 0
    assert "PDF generation is quarantined" in completed.stdout


@pytest.mark.skipif(
    shutil.which("gap") is None or not GAP_SOURCE.is_file(),
    reason="checked-in Pass 1147 GAP producer is required",
)
def test_wrapper_executes_gap_producer_without_mutating_checked_in_certificate() -> None:
    before = CERTIFICATE.read_bytes() if CERTIFICATE.is_file() else None
    completed = subprocess.run(
        [sys.executable, "analysis/w33_pass1142_1146_exact.py"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=300,
    )
    assert completed.returncode == 0, completed.stdout[-4000:]
    report = json.loads(completed.stdout)
    assert report["status"] == "PASS"
    assert report["gap_source_executed"] is True
    after = CERTIFICATE.read_bytes() if CERTIFICATE.is_file() else None
    assert after == before


@pytest.mark.skipif(
    not CERTIFICATE.is_file(),
    reason="checked-in Pass 1147 certificate is required",
)
def test_all_compatibility_wrappers_validate_the_checked_in_certificate() -> None:
    for relative in (
        "analysis/w33_pass1142_1146_exact.py",
        "analysis/w33_pass1142_1146_intertwiner.py",
        "analysis/w33_pass1142_1146_release_compiler.py",
    ):
        completed = subprocess.run(
            [
                sys.executable,
                relative,
                "--certificate",
                str(CERTIFICATE),
            ],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=30,
        )
        assert completed.returncode == 0, completed.stdout
        report = json.loads(completed.stdout)
        assert report["status"] == "PASS"
        assert report["gap_source_executed"] is False
