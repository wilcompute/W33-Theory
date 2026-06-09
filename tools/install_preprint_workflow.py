#!/usr/bin/env python3
"""BT587: local installer for the W33 preprint static-check workflow.

The connector could not write directly to .github/workflows, so this utility lets
a local checkout activate the workflow from the template committed under
analysis/.
"""
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "analysis" / "BT584_preprint_static_check_workflow_template.yml"
DST = ROOT / ".github" / "workflows" / "w33-preprint-static-check.yml"


def main() -> int:
    if not SRC.exists():
        print(f"missing workflow template: {SRC}", file=sys.stderr)
        return 2
    DST.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SRC, DST)
    print(f"installed workflow: {DST.relative_to(ROOT)}")
    print("run: bash tools/check_w33_preprint_static.sh")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
