#!/usr/bin/env python3
"""Idempotently register Passes 3973-3980 without modifying the protected docs/index.html blob."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

# This file is intentionally a generated-manifest reconciler: it updates metadata only.
ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "data/w33_current_frontier_manifest_v1.json"
TEX_INPUT = "analysis/BT3973_BT3980_extremal_mesh_photon_tensor_insert"
PUBLIC_SECTION = {
    "kind": "id",
    "token": "bt3973-3980-extremal-mesh-photon",
    "source": "analysis/BT3973_BT3980_extremal_mesh_photon_tensor_index_insert.html",
}
PUBLIC_PAGE = {
    "token": "passes-3973-3980-extremal-mesh-photon-tensor",
    "source": "docs/extremal-mesh-photon-tensor.html",
}


def append_unique(items: list, value, key=None) -> bool:
    if key is None:
        if value in items:
            return False
    else:
        matches = [item for item in items if item[key] == value[key]]
        if matches:
            if matches != [value]:
                raise ValueError(f"conflicting {key} entry: {matches} versus {value}")
            return False
    items.append(value)
    return True


def integrate(path: Path = CONFIG) -> dict[str, object]:
    config = json.loads(path.read_text(encoding="utf-8"))
    changed = {
        "required_ordered_inputs": append_unique(config["required_ordered_inputs"], TEX_INPUT),
        "public_sections": append_unique(config["public_sections"], PUBLIC_SECTION, "token"),
        "standalone_public_pages": append_unique(config["standalone_public_pages"], PUBLIC_PAGE, "token"),
    }
    path.write_text(json.dumps(config, separators=(",", ":")) + "\n", encoding="utf-8")
    return {
        "schema": "w33.pass3973_3980.frontier_integration.v1",
        "status": "PASS",
        "changed": changed,
        "protected_index_modified": False,
        "tex_input": TEX_INPUT,
        "public_section": PUBLIC_SECTION,
        "standalone_page": PUBLIC_PAGE,
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
    print("PASS Passes 3973-3980 frontier manifest reconciliation")
    print(payload, end="")


if __name__ == "__main__":
    main()
