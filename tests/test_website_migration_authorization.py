import importlib.util
import json
from pathlib import Path

import pytest

P = Path(__file__).resolve().parents[1] / "tools/check_website_migration_authorization.py"
s = importlib.util.spec_from_file_location("lock", P)
lock = importlib.util.module_from_spec(s)
s.loader.exec_module(lock)


def put(root: Path, data: bytes) -> None:
    path = root / "docs/index.html"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def write_authorization(root: Path, old: bytes, new: bytes, archive_data: bytes | None = None) -> Path:
    previous_blob = lock.git_blob_sha(old)
    new_blob = lock.git_blob_sha(new)
    archive = root / "docs/archive/old.html"
    archive.parent.mkdir(parents=True, exist_ok=True)
    archive.write_bytes(old if archive_data is None else archive_data)
    authorization = {
        "schema": lock.AUTHORIZATION_SCHEMA,
        "authorized": True,
        "authorization_phrase": lock.AUTHORIZATION_PHRASE,
        "approved_by": "wilcompute",
        "reason": "test",
        "previous_blob": previous_blob,
        "new_blob": new_blob,
        "archive_path": "docs/archive/old.html",
        "archive_blob": previous_blob,
    }
    path = root / "data/website_migration_authorization.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(authorization), encoding="utf-8")
    return Path("data/website_migration_authorization.json")


def test_unchanged(tmp_path: Path) -> None:
    old = b"old\n"
    put(tmp_path, old)
    result = lock.validate_website_index(tmp_path, expected_blob=lock.git_blob_sha(old))
    assert result["authorization_used"] is False


def test_unauthorized_change(tmp_path: Path) -> None:
    old = b"old\n"
    put(tmp_path, b"new\n")
    with pytest.raises(lock.AuthorizationError):
        lock.validate_website_index(tmp_path, expected_blob=lock.git_blob_sha(old))


def test_standing_authorization_is_not_discovered(tmp_path: Path) -> None:
    old = b"old\n"
    new = b"new\n"
    put(tmp_path, new)
    write_authorization(tmp_path, old, new)
    with pytest.raises(lock.AuthorizationError, match="supplied explicitly"):
        lock.validate_website_index(tmp_path, expected_blob=lock.git_blob_sha(old))


def test_explicit_authorized_archived_change(tmp_path: Path) -> None:
    old = b"old\n"
    new = b"new\n"
    put(tmp_path, new)
    authorization_path = write_authorization(tmp_path, old, new)
    result = lock.validate_website_index(
        tmp_path,
        expected_blob=lock.git_blob_sha(old),
        authorization_path=authorization_path,
    )
    assert result["authorization_used"] is True


def test_wrong_archive_fails(tmp_path: Path) -> None:
    old = b"old\n"
    new = b"new\n"
    put(tmp_path, new)
    authorization_path = write_authorization(tmp_path, old, new, archive_data=b"wrong\n")
    with pytest.raises(lock.AuthorizationError):
        lock.validate_website_index(
            tmp_path,
            expected_blob=lock.git_blob_sha(old),
            authorization_path=authorization_path,
        )
