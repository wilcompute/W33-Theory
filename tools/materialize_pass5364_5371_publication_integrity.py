#!/usr/bin/env python3
"""Materialize the Pass5364--5371 publication-integrity card into docs/index.html."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "docs/index.html"
SOURCE = ROOT / "analysis/PASS5364_5371_publication_integrity_index_insert.html"
TOKEN = 'id="pass-5364-5371-publication-dag-integrity"'


def materialize() -> str:
    text = INDEX.read_text(encoding="utf-8")
    count = text.count(TOKEN)
    if count == 1:
        return "already_materialized"
    if count > 1:
        raise ValueError("duplicate Pass5364-5371 publication-integrity card")
    html = SOURCE.read_text(encoding="utf-8").rstrip() + "\n"
    lower = text.lower()
    pos = lower.rfind("</main>")
    if pos < 0:
        pos = lower.rfind("</body>")
    if pos < 0:
        raise ValueError("docs/index.html has no </main> or </body> insertion point")
    updated = text[:pos] + html + text[pos:]
    assert updated.count(TOKEN) == 1
    INDEX.write_text(updated, encoding="utf-8")
    return "inserted"


def main() -> None:
    mode = materialize()
    print(f"PASS Pass5364-5371 homepage card: {mode}")


if __name__ == "__main__":
    main()
