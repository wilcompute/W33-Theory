#!/usr/bin/env python3
"""Idempotently consolidate current-frontier wrappers and reconcile public sections."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "data/w33_current_frontier_manifest_v1.json"
MANIFEST_INPUT = r"\input{analysis/W33_CURRENT_FRONTIER_MANIFEST}%"


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
    for item in required_inputs:
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
    for section in config["public_sections"]:
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
        "schema": "w33.bt3376_3389.integration.v1",
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
