#!/usr/bin/env python3
"""Materialize the Pass5840--5847 matrix/doily addendum card into both public surfaces."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOKEN = "pass-5840-5847-matrix-doily-radon-addendum"
SOURCE = ROOT / "analysis" / "PASS5840_5847_index_insert.html"
TARGETS = (ROOT / "docs" / "index.html", ROOT / "index.html")


def materialize(path: Path, html: str) -> str:
    marker = f'id="{TOKEN}"'
    text = path.read_text(encoding="utf-8")
    count = text.count(marker)
    if count == 1:
        return "already_materialized"
    if count > 1:
        raise ValueError(f"duplicate {marker} in {path}")
    lower = text.lower()
    pos = lower.rfind("</main>")
    if pos < 0:
        pos = lower.rfind("</body>")
    if pos < 0:
        raise ValueError(f"{path} has no </main> or </body> insertion point")
    updated = text[:pos] + html.rstrip() + "\n" + text[pos:]
    if updated.count(marker) != 1:
        raise AssertionError(f"failed uniqueness check for {marker}")
    path.write_text(updated, encoding="utf-8")
    return "inserted"


def main() -> None:
    html = SOURCE.read_text(encoding="utf-8")
    marker = f'id="{TOKEN}"'
    if html.count(marker) != 1:
        raise ValueError(f"source must contain exactly one {marker}")
    for target in TARGETS:
        print(f"PASS {target.relative_to(ROOT)}: {materialize(target, html)}")
    for target in TARGETS:
        count = target.read_text(encoding="utf-8").count(marker)
        if count != 1:
            raise AssertionError(f"{target}: expected one {marker}, got {count}")


if __name__ == "__main__":
    main()
