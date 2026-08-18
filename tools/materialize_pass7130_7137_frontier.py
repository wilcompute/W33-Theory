#!/usr/bin/env python3
"""Idempotently materialize the Pass7130-7137 public frontier card.

The publication contract names docs/index.html as canonical; root index.html is maintained
in parallel. Duplicate section IDs fail closed and each target is handled independently.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = (ROOT / "docs" / "index.html", ROOT / "index.html")
TOKEN = "pass-7130-7137-q9-structural-attack"
SOURCE = ROOT / "analysis" / "PASS7130_7137_index_insert.html"


def place(path: Path, card: str) -> str:
    marker = f'id="{TOKEN}"'
    text = path.read_text(encoding="utf-8")
    n = text.count(marker)
    if n > 1:
        raise ValueError(f"duplicate {marker} in {path}")
    if n == 1:
        return "already_materialized"
    low = text.lower()
    pos = low.rfind("</main>")
    if pos < 0:
        pos = low.rfind("</body>")
    if pos < 0:
        raise ValueError(f"no </main> or </body> in {path}")
    out = text[:pos] + card.rstrip() + "\n" + text[pos:]
    assert out.count(marker) == 1
    path.write_text(out, encoding="utf-8")
    return "inserted"


def main() -> None:
    card = SOURCE.read_text(encoding="utf-8")
    assert card.count(f'id="{TOKEN}"') == 1
    for target in TARGETS:
        print(target.relative_to(ROOT), place(target, card))
    for target in TARGETS:
        assert target.read_text(encoding="utf-8").count(f'id="{TOKEN}"') == 1


if __name__ == "__main__":
    main()
