#!/usr/bin/env python3
"""Materialize the corrected Pass5776--5855 matrix-frontier cards.

The earlier Pass5832--5839 matrix card is a namespace-collision artifact.  A queued
legacy workflow may still materialize it after this correction, so every corrected run
first removes that stale section if present.  The two public surfaces are handled
independently; no byte-for-byte mirror assumption is made.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = (ROOT / "docs" / "index.html", ROOT / "index.html")
STALE = "pass-5832-5839-normalizer-code-pauli-allq"
CARDS = (
    ("pass-5776-5783-reye-latin-common-core", ROOT / "analysis" / "PASS5776_5783_index_insert.html"),
    ("pass-5792-5799-matrix-ring-transpose-outer", ROOT / "analysis" / "PASS5792_5799_index_insert.html"),
    ("pass-5816-5823-matrix-fourier-rank", ROOT / "analysis" / "PASS5816_5823_index_insert.html"),
    ("pass-5824-5831-integral-w9-lattices", ROOT / "analysis" / "PASS5824_5831_index_insert.html"),
    ("pass-5848-5855-normalizer-code-pauli-allq", ROOT / "analysis" / "PASS5848_5855_index_insert.html"),
)


def remove_stale(text: str, path: Path) -> tuple[str, str]:
    marker = f'id="{STALE}"'
    count = text.count(marker)
    if count > 1:
        raise ValueError(f"duplicate stale collision card {marker} in {path}")
    if count == 0:
        return text, "absent"
    pattern = re.compile(
        r'\s*<section\s+id="pass-5832-5839-normalizer-code-pauli-allq"\b.*?</section>\s*',
        re.DOTALL,
    )
    updated, removed = pattern.subn("\n", text, count=1)
    if removed != 1 or marker in updated:
        raise ValueError(f"could not remove exactly one stale collision card from {path}")
    return updated, "removed"


def materialize_one(text: str, path: Path, token: str, html: str) -> tuple[str, str]:
    marker = f'id="{token}"'
    count = text.count(marker)
    if count == 1:
        return text, "already_materialized"
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
    return updated, "inserted"


def main() -> None:
    card_html = []
    for token, source in CARDS:
        html = source.read_text(encoding="utf-8")
        marker = f'id="{token}"'
        if html.count(marker) != 1:
            raise ValueError(f"source {source} must contain exactly one {marker}")
        card_html.append((token, html))

    for target in TARGETS:
        text = target.read_text(encoding="utf-8")
        text, stale_status = remove_stale(text, target)
        print(f"PASS {target.relative_to(ROOT)} stale-{STALE}: {stale_status}")
        for token, html in card_html:
            text, status = materialize_one(text, target, token, html)
            print(f"PASS {target.relative_to(ROOT)} {token}: {status}")
        target.write_text(text, encoding="utf-8")

    for target in TARGETS:
        text = target.read_text(encoding="utf-8")
        if f'id="{STALE}"' in text:
            raise AssertionError(f"stale collision card survived in {target}")
        for token, _ in CARDS:
            count = text.count(f'id="{token}"')
            if count != 1:
                raise AssertionError(f"{target}: expected one {token}, got {count}")


if __name__ == "__main__":
    main()
