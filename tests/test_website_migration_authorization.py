import importlib.util
import json
from pathlib import Path

import pytest

MODULE_PATH = Path(__file__).resolve().parents[1] / "tools/check_website_migration_authorization.py"
spec = importlib.util.spec_from_file_location("website_lock", MODULE_PATH)
website_lock = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(website_lock)


def write_index(root: Path, data: bytes) -> Path:
    path = root / "docs/index.html"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return path


def test_unchanged_index_passes(tmp_path: Path):
    original = b"authoritative website\n"; expected = website_lock.git_blob_sha(original)
    write_index(tmp_path, original)
    result = website_lock.validate_website_index(tmp_path, expected_blob=expected)
    assert result["status"] == "PASS_RESTORED_INDEX_UNCHANGED" and result["authorization_used"] is False


def test_changed_index_without_authorization_fails(tmp_path: Path):
    original = b"authoritative website\n"; expected = website_lock.git_blob_sha(original)
    write_index(tmp_path, b"replacement\n")
    with pytest.raises(website_lock.AuthorizationError):
        website_lock.validate_website_index(tmp_path, expected_blob=expected)


def test_exact_archived_migration_passes(tmp_path: Path):
    original = b"authoritative website\n"; replacement = b"approved replacement\n"
    expected = website_lock.git_blob_sha(original); actual = website_lock.git_blob_sha(replacement)
    write_index(tmp_path, replacement)
    archive = tmp_path / "docs/archive/original.html"; archive.parent.mkdir(parents=True, exist_ok=True); archive.write_bytes(original)
    authorization = {"schema": website_lock.AUTHORIZATION_SCHEMA, "authorized": True, "authorization_phrase": website_lock.AUTHORIZATION_PHRASE, "approved_by": "wilcompute", "reason": "Explicit test migration", "previous_blob": expected, "new_blob": actual, "archive_path": "docs/archive/original.html", "archive_blob": expected}
    auth_path = tmp_path / "data/website_migration_authorization.json"; auth_path.parent.mkdir(parents=True, exist_ok=True); auth_path.write_text(json.dumps(authorization), encoding="utf-8")
    result = website_lock.validate_website_index(tmp_path, expected_blob=expected)
    assert result["status"] == "PASS_EXPLICIT_INDEX_MIGRATION_AUTHORIZATION" and result["authorization_used"] is True


def test_archive_must_match_previous_blob(tmp_path: Path):
    original = b"authoritative website\n"; replacement = b"approved replacement\n"
    expected = website_lock.git_blob_sha(original); actual = website_lock.git_blob_sha(replacement)
    write_index(tmp_path, replacement)
    archive = tmp_path / "docs/archive/original.html"; archive.parent.mkdir(parents=True, exist_ok=True); archive.write_bytes(b"not the original\n")
    authorization = {"schema": website_lock.AUTHORIZATION_SCHEMA, "authorized": True, "authorization_phrase": website_lock.AUTHORIZATION_PHRASE, "approved_by": "wilcompute", "reason": "Bad archive negative control", "previous_blob": expected, "new_blob": actual, "archive_path": "docs/archive/original.html", "archive_blob": expected}
    auth_path = tmp_path / "data/website_migration_authorization.json"; auth_path.parent.mkdir(parents=True, exist_ok=True); auth_path.write_text(json.dumps(authorization), encoding="utf-8")
    with pytest.raises(website_lock.AuthorizationError):
        website_lock.validate_website_index(tmp_path, expected_blob=expected)
