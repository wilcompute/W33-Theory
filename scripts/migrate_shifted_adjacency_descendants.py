#!/usr/bin/env python3
"""Pass 1144 semantic migration with per-file transactional diagnostics.

The reviewed migration primitives live in the committed Pass-1142-1146 source
bundle. This driver loads them without auto-running the bundled CLI, applies the
migration one registered descendant at a time, records every action/error, and
fails closed when any file cannot be processed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.pass1142_1146_bundle_runtime import execute_member

_NS: dict[str, Any] = {
    "__name__": "w33_pass1144_migration_primitives",
    "__file__": str(ROOT / "scripts" / "migrate_shifted_adjacency_descendants.py"),
}
execute_member("scripts/migrate_shifted_adjacency_descendants.py", _NS)

TAG = _NS["TAG"]
LEDGER = ROOT / "data" / "w33_shifted_adjacency_retraction_ledger.json"
REPORT = ROOT / "data" / "w33_shifted_adjacency_migration_report.json"


def _kind(status: str, suffix: str) -> str:
    s = status.lower()
    if s.startswith("active_retraction_"):
        return "active"
    if "retracted" in s and any(
        x in s for x in ("primary", "generated", "synthesis", "descendant")
    ):
        return "pure"
    if "legacy_test_quarantined" in s:
        return "test"
    if suffix == ".py" and (
        "legacy_derivation" in s or "legacy_cross_reference" in s
    ):
        return "legacy_python"
    return "surface"


def migrate_one(path: Path, status: str) -> tuple[str, str, str]:
    before = path.read_bytes()
    before_sha = hashlib.sha256(before).hexdigest()
    if TAG.encode() in before:
        return "already_patched", before_sha, before_sha

    kind = _kind(status, path.suffix.lower())
    if kind == "active":
        raise RuntimeError(
            "ledger marks ACTIVE_RETRACTION but file lacks the retraction tag"
        )
    if kind == "pure":
        _NS["archive"](path)
        if path.suffix.lower() == ".py":
            _NS["py_stub"](path, status, before_sha)
        elif path.suffix.lower() == ".json":
            _NS["json_stub"](path, status, before_sha)
        else:
            _NS["patch_text"](path)
        action = "archived_and_replaced"
    elif kind == "test":
        _NS["quarantine_test"](path)
        action = "pytest_quarantined"
    elif kind == "legacy_python":
        _NS["guard_legacy_python"](path)
        action = "runtime_guarded"
    elif path.suffix.lower() == ".md":
        _NS["patch_markdown"](path)
        action = "visible_markdown_erratum"
    elif path.suffix.lower() == ".tex":
        _NS["patch_tex"](path)
        action = "visible_tex_erratum"
    elif path.suffix.lower() == ".py":
        _NS["guard_legacy_python"](path)
        action = "source_guarded"
    else:
        _NS["patch_text"](path)
        action = "plain_text_erratum"

    after_sha = hashlib.sha256(path.read_bytes()).hexdigest()
    return action, before_sha, after_sha


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--apply", action="store_true", help="Apply the registered migration"
    )
    args = parser.parse_args()
    if not args.apply:
        raise SystemExit("Pass --apply to perform the semantic migration")

    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    records: list[dict[str, Any]] = []
    changed = 0
    errors = 0
    for rel, status in ledger["known_descendants"].items():
        path = ROOT / rel
        if not path.exists():
            records.append(
                {"path": rel, "historical_status": status, "action": "missing"}
            )
            continue
        try:
            action, before_sha, after_sha = migrate_one(path, status)
            changed += int(before_sha != after_sha)
            records.append(
                {
                    "path": rel,
                    "historical_status": status,
                    "action": action,
                    "before_sha256": before_sha,
                    "after_sha256": after_sha,
                }
            )
        except Exception as exc:
            errors += 1
            records.append(
                {
                    "path": rel,
                    "historical_status": status,
                    "action": "ERROR",
                    "exception_type": type(exc).__name__,
                    "exception": str(exc),
                }
            )

    report = {
        "schema": "w33.pass1144.shifted_adjacency_migration.v2",
        "status": "PASS" if errors == 0 else "FAIL",
        "changed_files": changed,
        "error_count": errors,
        "records": records,
        "policy": (
            "Pure descendants are fail-closed stubs with Git-preserved originals; "
            "tests are explicit xfails; manuscript surfaces display a visible erratum."
        ),
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    summary = {
        "status": report["status"],
        "changed_files": changed,
        "error_count": errors,
        "errors": [r for r in records if r["action"] == "ERROR"],
        "report": str(REPORT.relative_to(ROOT)),
    }
    print(json.dumps(summary, indent=2))
    if errors:
        raise SystemExit(
            f"Pass 1144 migration failed for {errors} registered file(s)"
        )


if __name__ == "__main__":
    main()
