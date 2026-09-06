#!/usr/bin/env python3
"""Idempotently fill missing cards in the canonical long-form public index.

This consumes the publication-frontier v2 contract and its registered
extensions. The root ``index.html`` is intentionally left as a curated front
door; ``docs/index.html`` is the complete contracted atlas.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_pass5364_publication_dag_audit import (  # noqa: E402
    CONTRACT,
    configured_public_sections,
    load_json,
    section_count,
)


TARGET = ROOT / "docs" / "index.html"


def contracted_sections() -> list[dict]:
    contract = load_json(CONTRACT)
    legacy = load_json(ROOT / contract["legacy_contract"])
    sections, _ = configured_public_sections(contract, legacy)
    return sections


def insertion_point(text: str) -> int:
    lower = text.lower()
    position = lower.rfind("</main>")
    if position < 0:
        position = lower.rfind("</body>")
    if position < 0:
        raise ValueError("canonical index has no </main> or </body> anchor")
    return position


def materialize_text(text: str, sections: list[dict]) -> tuple[str, list[str]]:
    inserted: list[str] = []
    for section in sections:
        count = section_count(text, section)
        key = f"{section['kind']}:{section['token']}"
        if count > 1:
            raise ValueError(f"duplicate contracted public section {key}")
        if count == 1:
            continue

        source = ROOT / section["source"]
        fragment = source.read_text(encoding="utf-8").rstrip() + "\n"
        if section_count(fragment, section) != 1:
            raise ValueError(f"source {source} does not contain exactly one {key}")
        position = insertion_point(text)
        text = text[:position] + fragment + text[position:]
        inserted.append(key)

    for section in sections:
        key = f"{section['kind']}:{section['token']}"
        if section_count(text, section) != 1:
            raise AssertionError(f"materialization failed for {key}")
    return text, inserted


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="report gaps without writing; exit nonzero when any remain",
    )
    args = parser.parse_args()

    original = TARGET.read_text(encoding="utf-8")
    output, inserted = materialize_text(original, contracted_sections())
    if args.check:
        if inserted:
            print("missing", len(inserted), *inserted, sep="\n")
            return 1
        print("PASS_PUBLICATION_CONTRACT_FULLY_MATERIALIZED")
        return 0

    if output != original:
        TARGET.write_text(output, encoding="utf-8")
    print(f"inserted={len(inserted)}")
    for key in inserted:
        print(key)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
