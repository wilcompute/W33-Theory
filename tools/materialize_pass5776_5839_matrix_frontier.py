#!/usr/bin/env python3
"""Materialize the Pass5776--5839 matrix-frontier cards into both public surfaces.

Unlike older one-packet materializers, this intentionally does not require root
index.html and docs/index.html to be byte-identical before the edit.  The publication
contract names docs/index.html as canonical, but both surfaces are maintained; each card
is inserted idempotently and duplicate IDs fail closed.
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = (ROOT / "docs" / "index.html", ROOT / "index.html")
CARDS = (
    ("pass-5776-5783-reye-latin-common-core", ROOT / "analysis" / "PASS5776_5783_index_insert.html"),
    ("pass-5792-5799-matrix-ring-transpose-outer", ROOT / "analysis" / "PASS5792_5799_index_insert.html"),
    ("pass-5816-5823-matrix-fourier-rank", ROOT / "analysis" / "PASS5816_5823_index_insert.html"),
    ("pass-5824-5831-integral-w9-lattices", ROOT / "analysis" / "PASS5824_5831_index_insert.html"),
    ("pass-5832-5839-normalizer-code-pauli-allq", ROOT / "analysis" / "PASS5832_5839_index_insert.html"),
)


def materialize_one(path: Path, token: str, html: str) -> str:
    marker = f'id="{token}"'
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
        raise AssertionError(f"failed uniqueness check for {marker} in {path}")
    path.write_text(updated, encoding="utf-8")
    return "inserted"


def main() -> None:
    for token, source in CARDS:
        html = source.read_text(encoding="utf-8")
        source_marker = f'id="{token}"'
        if html.count(source_marker) != 1:
            raise ValueError(f"source {source} must contain exactly one {source_marker}")
        for target in TARGETS:
            result = materialize_one(target, token, html)
            print(f"PASS {target.relative_to(ROOT)} {token}: {result}")
    for token, _ in CARDS:
        marker = f'id="{token}"'
        for target in TARGETS:
            count = target.read_text(encoding="utf-8").count(marker)
            if count != 1:
                raise AssertionError(f"{target}: expected one {marker}, got {count}")


if __name__ == "__main__":
    main()
