#!/usr/bin/env python3
"""Canonical entrypoint for the Pass 1144 semantic descendant migration."""
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.pass1142_1146_bundle_runtime import execute_member

execute_member("scripts/migrate_shifted_adjacency_descendants.py", globals())

# The source bundle was renumbered after a parallel Pass-1139 reservation landed.
# Normalize the generated schema at the canonical entrypoint boundary.
report_path = ROOT / "data" / "w33_shifted_adjacency_migration_report.json"
if report_path.exists():
    report = json.loads(report_path.read_text(encoding="utf-8"))
    report["schema"] = "w33.pass1144.shifted_adjacency_migration.v1"
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
