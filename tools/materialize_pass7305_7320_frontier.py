#!/usr/bin/env python3
"""Idempotently materialize the Pass7305--7320 card on both public surfaces."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "analysis" / "PASS7305_7320_index_insert.html"
TARGETS = (ROOT / "index.html", ROOT / "docs" / "index.html")
TOKEN = "pass-7305-7320-intrinsic-naimark-pauli-scope"
MARKER = f'id="{TOKEN}"'
CARD = SOURCE.read_text(encoding="utf-8").rstrip() + "\n"


def materialize_text(text: str, *, front_door: bool) -> tuple[str, str]:
    """Return one-card text and insertion status without touching the filesystem."""

    count = text.count(MARKER)
    if count > 1:
        raise ValueError(f"duplicate {MARKER}")
    if count == 1:
        return text, "already_materialized"

    if front_door:
        anchor = "</nav>"
        position = text.lower().find(anchor)
        if position < 0:
            raise ValueError("root front door has no </nav> anchor")
        position += len(anchor)
        output = text[:position] + "\n\n" + CARD + text[position:]
    else:
        position = text.lower().rfind("</main>")
        if position < 0:
            position = text.lower().rfind("</body>")
        if position < 0:
            raise ValueError("long-form site has no </main> or </body> anchor")
        output = text[:position] + CARD + text[position:]

    if output.count(MARKER) != 1:
        raise AssertionError("materialization did not produce exactly one card")
    return output, "inserted"


def place(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    output, mode = materialize_text(text, front_door=path == ROOT / "index.html")
    if output != text:
        path.write_text(output, encoding="utf-8")
    return mode


def main() -> int:
    if CARD.count(MARKER) != 1:
        raise ValueError("source card must contain its marker exactly once")
    for target in TARGETS:
        print(target.relative_to(ROOT), place(target))
    for target in TARGETS:
        if target.read_text(encoding="utf-8").count(MARKER) != 1:
            raise AssertionError(f"card count is not one in {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
