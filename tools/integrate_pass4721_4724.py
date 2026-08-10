#!/usr/bin/env python3
"""Idempotently materialize the Passes 4721--4726 theorem cards into docs/index.html."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "docs" / "index.html"
CARDS = [
    (
        ROOT / "analysis" / "PASS4721_4724_support12_involution_square_root_cover_index_insert.html",
        'id="pass4721-4724-support12-involution-cover"',
    ),
    (
        ROOT / "analysis" / "PASS4725_4726_involution_residue_dual_code_index_insert.html",
        'id="pass4725-4726-involution-residue-dual-code"',
    ),
]


def insert_one(text: str, source: Path, token: str) -> tuple[str, str]:
    count = text.count(token)
    if count == 1:
        return text, "already_materialized"
    if count > 1:
        raise RuntimeError(f"duplicate theorem card in docs/index.html: {token}")
    html = source.read_text(encoding="utf-8").rstrip() + "\n"
    lower = text.lower()
    pos = lower.rfind("</main>")
    if pos < 0:
        pos = lower.rfind("</body>")
    if pos < 0:
        raise RuntimeError("docs/index.html has no </main> or </body> insertion point")
    return text[:pos] + html + text[pos:], "inserted"


def integrate() -> dict[str, str]:
    text = INDEX.read_text(encoding="utf-8")
    modes: dict[str, str] = {}
    for source, token in CARDS:
        text, mode = insert_one(text, source, token)
        modes[token] = mode
    INDEX.write_text(text, encoding="utf-8")
    check = INDEX.read_text(encoding="utf-8")
    for _source, token in CARDS:
        if check.count(token) != 1:
            raise RuntimeError(f"theorem card failed uniqueness check: {token}")
    return modes


def main() -> int:
    modes = integrate()
    for token, mode in modes.items():
        print(f"PASS {token}: {mode}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
