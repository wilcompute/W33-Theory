"""Scan `scripts/` for files that may have fragile imports when executed as scripts.

This helper lists Python files under `scripts/` that use absolute
`from scripts.x import ...` statements and that also contain a
`if __name__ == "__main__"` guard — these are the best candidates
for adding the try/except relative/absolute import compatibility pattern.

Run this with the repo venv's python from the repository root.
"""
from __future__ import annotations

import re
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"

ABS_IMPORT_RE = re.compile(r"^\s*from\s+scripts\.", re.M)
REL_IMPORT_RE = re.compile(r"^\s*from\s+\.\w+", re.M)
MAIN_GUARD_RE = re.compile(r"if\s+__name__\s*==\s*[\"']__main__[\"']\s*:")

report_lines = []
files_scanned = 0
fragile = []

for p in sorted(SCRIPTS_DIR.rglob("*.py")):
    try:
        text = p.read_text(encoding="utf-8")
    except Exception:
        continue
    files_scanned += 1
    uses_abs = bool(ABS_IMPORT_RE.search(text))
    uses_rel = bool(REL_IMPORT_RE.search(text))
    has_main = bool(MAIN_GUARD_RE.search(text))
    if uses_abs and has_main and not uses_rel:
        fragile.append(p.relative_to(ROOT))

report_lines.append(f"Scanned {files_scanned} files under scripts/")
report_lines.append("")
report_lines.append("Files that use 'from scripts.*' and have a __main__ guard but no relative 'from .' imports:")
if fragile:
    for f in fragile:
        report_lines.append(f" - {f}")
else:
    report_lines.append(" (none detected)")

out_path = SCRIPTS_DIR / "fragile_imports_report.txt"
out_path.write_text("\n".join(report_lines, encoding="utf-8"), encoding="utf-8")

print("\n".join(report_lines))
print(f"\nWrote report to: {out_path}")

sys.exit(0)
