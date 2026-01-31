#!/usr/bin/env python3
"""Build a simple verification dashboard by combining digest and reports.
Writes artifacts/verification_dashboard.md"""
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts" / "verification_dashboard.md"
DIGEST = ROOT / "artifacts" / "verification_digest.md"
PRED = ROOT / "artifacts" / "predictions_report.md"
ART_DIR = ROOT / "artifacts"


def build():
    lines = []
    lines.append("# Verification Dashboard")
    lines.append("")
    lines.append(f"Generated: {datetime.utcnow().isoformat()}Z")
    lines.append("")

    if DIGEST.exists():
        lines.append("## Verification Digest")
        lines.append("")
        lines.extend(DIGEST.read_text(encoding="utf-8").splitlines())
        lines.append("")

    if PRED.exists():
        lines.append("## Predictions Report")
        lines.append("")
        lines.extend(PRED.read_text(encoding="utf-8").splitlines())
        lines.append("")

    lines.append("## Sage artifacts present")
    lines.append("")
    files = sorted([p for p in ART_DIR.iterdir() if p.is_file()])
    lines.append("| File | Size (bytes) |")
    lines.append("|---|---:|")
    for f in files:
        lines.append(f"| {f.name} | {f.stat().st_size} |")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    build()
