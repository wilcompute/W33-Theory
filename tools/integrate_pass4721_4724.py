#!/usr/bin/env python3
"""Idempotently materialize the Passes 4721--4724 theorem card into docs/index.html."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "docs" / "index.html"
SOURCE = ROOT / "analysis" / "PASS4721_4724_support12_involution_square_root_cover_index_insert.html"
TOKEN = 'id="pass4721-4724-support12-involution-cover"'


def integrate() -> str:
    text = INDEX.read_text(encoding="utf-8")
    count = text.count(TOKEN)
    if count == 1:
        return "already_materialized"
    if count > 1:
        raise RuntimeError("duplicate Pass 4721--4724 theorem cards in docs/index.html")
    html = SOURCE.read_text(encoding="utf-8").rstrip() + "\n"
    lower = text.lower()
    pos = lower.rfind("</main>")
    if pos < 0:
        pos = lower.rfind("</body>")
    if pos < 0:
        raise RuntimeError("docs/index.html has no </main> or </body> insertion point")
    INDEX.write_text(text[:pos] + html + text[pos:], encoding="utf-8")
    check = INDEX.read_text(encoding="utf-8")
    if check.count(TOKEN) != 1:
        raise RuntimeError("Pass 4721--4724 theorem card failed uniqueness check")
    return "inserted"


def main() -> int:
    mode = integrate()
    print(f"PASS pass4721-4724 index materializer: {mode}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
