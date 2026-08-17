#!/usr/bin/env python3
"""Idempotently consolidate current-frontier wrappers and reconcile public sections."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "data/w33_current_frontier_manifest_v1.json"
PUBLIC_EXTENSION_PATH = ROOT / "data/w33_public_frontier_extension_pass4461_4464.json"
PUBLICATION_V2_PATH = ROOT / "data/w33_publication_frontier_contract_v2.json"
MANIFEST_INPUT = r"\input{analysis/W33_CURRENT_FRONTIER_MANIFEST}%"
PUBLIC_SOURCE_ALIASES = {
    "analysis/BT3528_BT3534_borel_star_moore_transplant_index_insert.html":
        "analysis/BT3528_BT3534_borel_star_moore_functor_transplant_index_insert.html",
    "analysis/PASS4544_4551_module_cubic_zeta_index_insert.html":
        "analysis/PASS4544_4551_module_cubic_enumerator_zeta_index_insert.html",
}
PUBLIC_SECTION_ALIASES = {
    ("id", "bt3418-3429-clebsch-d5-supplement"):
        ("marker", "<!-- BT3418-BT3429-CLEBSCH-D5-SUPPLEMENT -->"),
    ("id", "pass4579-4586-o8plus-exceptional-bridge"):
        ("id", "pass4579-4586-o8plus-exceptional"),
    ("id", "pass4624-4631-packet-incidence-f4-h10"):
        ("id", "pass4624-4631-packet-incidence-f4"),
}
SECTION_TAG_RE = re.compile(r"<(/?)section\b[^>]*>", re.IGNORECASE)


def consolidate_wrapper(text: str, required_inputs: list[str]) -> tuple[str, str]:
    lines = text.splitlines()
    direct_indices = [
        index for index, line in enumerate(lines)
        if any(rf"\input{{{item}}}" in line for item in required_inputs)
    ]
    if direct_indices:
        insertion = min(direct_indices)
        lines = [
            line for line in lines
            if not any(rf"\input{{{item}}}" in line for item in required_inputs)
        ]
        lines.insert(insertion, f"    {MANIFEST_INPUT}")
        mode = "consolidated_direct_inputs"
    elif sum(MANIFEST_INPUT in line for line in lines) == 1:
        mode = "already_consolidated"
    else:
        hook_close = next(
            (index for index in range(len(lines) - 1, -1, -1) if lines[index].strip() == "}%"),
            None,
        )
        if hook_close is None:
            raise ValueError("wrapper has neither current-frontier inputs nor a table-of-contents hook")
        lines.insert(hook_close, f"    {MANIFEST_INPUT}")
        mode = "inserted_at_hook_close"
    result = "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    if result.count(MANIFEST_INPUT) != 1:
        raise ValueError("manifest reference is not unique")
    # The v1 list is historical and may contain duplicate ledger entries; a
    # wrapper is consolidated when none of those theorem leaves remains direct.
    for item in dict.fromkeys(required_inputs):
        if rf"\input{{{item}}}" in result:
            raise ValueError(f"unconsolidated direct input: {item}")
    return result, mode


def public_count(text: str, kind: str, token: str) -> int:
    if kind == "id":
        return text.count(f'id="{token}"')
    if kind == "marker":
        return text.count(token)
    raise ValueError(f"unsupported public section kind: {kind}")


def integrate_public_section(text: str, html: str, kind: str, token: str) -> tuple[str, str]:
    count = public_count(text, kind, token)
    if count == 1:
        # A canonical card source is a single outer <section id="token">.  Keep
        # that card byte-current instead of mistaking mere presence for currency.
        # Full standalone pages and marker fragments intentionally stay on the
        # legacy presence-only path.
        source = html.strip()
        first = SECTION_TAG_RE.match(source)
        if kind == "id" and first and not first.group(1) and f'id="{token}"' in first.group(0):
            start = next(
                match.start()
                for match in SECTION_TAG_RE.finditer(text)
                if not match.group(1) and f'id="{token}"' in match.group(0)
            )
            depth = 0
            end = None
            for match in SECTION_TAG_RE.finditer(text, start):
                depth += -1 if match.group(1) else 1
                if depth == 0:
                    end = match.end()
                    break
            if end is None:
                raise ValueError(f"unterminated public section: {token}")
            if text[start:end] == source:
                return text, "already_materialized"
            return text[:start] + source + text[end:], "updated"
        return text, "already_materialized"
    if count > 1:
        raise ValueError(f"duplicate public section: {token}")
    lower = text.lower()
    position = lower.rfind("</main>")
    if position < 0:
        position = lower.rfind("</body>")
    if position < 0:
        raise ValueError("public index has no </main> or </body> insertion point")
    return text[:position] + html.rstrip() + "\n" + text[position:], "inserted"


def integrate_index(text: str, html: str) -> tuple[str, str]:
    """Compatibility helper for the BT3376--3389 section regression."""
    return integrate_public_section(
        text,
        html,
        "id",
        "bt3376-3389-cohomology-tau-frontier",
    )


def configured_public_sections(config: dict, root: Path) -> list[dict]:
    """Return canonical, extension, and v2-local public sections with collision checks."""
    sections = list(config["public_sections"])
    if PUBLIC_EXTENSION_PATH.is_file():
        extension = json.loads(PUBLIC_EXTENSION_PATH.read_text(encoding="utf-8"))
        if extension.get("schema") != "w33.public_frontier_extension.v1":
            raise ValueError("wrong public frontier extension schema")
        sections.extend(extension.get("public_sections", []))
    if PUBLICATION_V2_PATH.is_file():
        v2 = json.loads(PUBLICATION_V2_PATH.read_text(encoding="utf-8"))
        if v2.get("schema") != "w33.publication_frontier_contract.v2":
            raise ValueError("wrong publication v2 schema")
        sections.extend(v2.get("local_public_sections", []))

    seen: set[tuple[str, str]] = set()
    resolved_sections: list[dict] = []
    for section in sections:
        section = dict(section)
        section["source"] = PUBLIC_SOURCE_ALIASES.get(section["source"], section["source"])
        section["kind"], section["token"] = PUBLIC_SECTION_ALIASES.get(
            (section["kind"], section["token"]),
            (section["kind"], section["token"]),
        )
        key = (section["kind"], section["token"])
        if key in seen:
            raise ValueError(f"duplicate configured public section: {key}")
        seen.add(key)
        source = root / section["source"]
        if not source.is_file():
            raise ValueError(f"missing configured public section source: {section['source']}")
        resolved_sections.append(section)
    return resolved_sections


def integrate(root: Path = ROOT) -> dict:
    config = json.loads((root / "data/w33_current_frontier_manifest_v1.json").read_text(encoding="utf-8"))
    required = config["required_ordered_inputs"]
    wrapper_modes = {}
    for wrapper_name in config["front_doors"]:
        path = root / wrapper_name
        before = path.read_text(encoding="utf-8")
        after, mode = consolidate_wrapper(before, required)
        path.write_text(after, encoding="utf-8")
        wrapper_modes[wrapper_name] = {
            "mode": mode,
            "changed": after != before,
        }

    index_path = root / config["public_index"]
    before_index = index_path.read_text(encoding="utf-8")
    after_index = before_index
    section_modes = {}
    for section in configured_public_sections(config, root):
        source = root / section["source"]
        html = source.read_text(encoding="utf-8")
        after_index, mode = integrate_public_section(
            after_index,
            html,
            section["kind"],
            section["token"],
        )
        section_modes[section["token"]] = mode
    index_path.write_text(after_index, encoding="utf-8")

    return {
        "schema": "w33.bt3376_3389.integration.v2",
        "status": "PASS",
        "wrappers": wrapper_modes,
        "index": {
            "changed": after_index != before_index,
            "sections": section_modes,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    result = integrate()
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(payload, encoding="utf-8")
    print("PASS reconciled current-frontier manifest and public sections")
    print(payload, end="")


if __name__ == "__main__":
    main()
