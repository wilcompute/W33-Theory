#!/usr/bin/env python3
"""Reconcile both Passes 3973-3980 certificates without touching protected docs/index.html."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "data/w33_current_frontier_manifest_v1.json"
OLD_INPUTS = {
    "analysis/BT3973_BT3980_extremal_mesh_photon_tensor_insert",
    "analysis/BT3973_BT3980_extremal_mesh_photon_tensor_monster_insert",
    "analysis/BT3973_BT3980_combined_extremal_mesh_photon_tensor_insert",
}
TEX_INPUT = "analysis/BT3973_BT3980_combined_extremal_mesh_photon_tensor_insert"
PUBLIC_SECTIONS = [
    {
        "kind": "id",
        "token": "bt3973-3980-extremal-mesh-photon",
        "source": "analysis/BT3973_BT3980_extremal_mesh_photon_tensor_index_insert.html",
    },
    {
        "kind": "id",
        "token": "bt3973-3980-extremal-mesh-photon-tensor",
        "source": "analysis/BT3973_BT3980_extremal_mesh_photon_tensor_monster_index_insert.html",
    },
]
PUBLIC_PAGES = [
    {
        "token": "passes-3973-3980-extremal-mesh-photon-tensor",
        "source": "docs/extremal-mesh-photon-tensor.html",
    },
    {
        "token": "passes-3973-3980-extremal-code-mesh-photon-tensor",
        "source": "docs/extremal-code-mesh-photon-tensor.html",
    },
]


def upsert_by_key(items: list, value: dict, key: str) -> bool:
    matches = [i for i, item in enumerate(items) if item[key] == value[key]]
    changed = False
    if matches:
        first = matches[0]
        if items[first] != value:
            items[first] = value
            changed = True
        for index in reversed(matches[1:]):
            del items[index]
            changed = True
    else:
        items.append(value)
        changed = True
    return changed


def integrate(path: Path = CONFIG) -> dict[str, object]:
    config = json.loads(path.read_text(encoding="utf-8"))
    previous = list(config["required_ordered_inputs"])
    config["required_ordered_inputs"] = [x for x in previous if x not in OLD_INPUTS]
    config["required_ordered_inputs"].append(TEX_INPUT)
    changed_inputs = config["required_ordered_inputs"] != previous
    changed_sections = any(upsert_by_key(config["public_sections"], entry, "token") for entry in PUBLIC_SECTIONS)
    changed_pages = any(upsert_by_key(config["standalone_public_pages"], entry, "token") for entry in PUBLIC_PAGES)
    path.write_text(json.dumps(config, separators=(",", ":")) + "\n", encoding="utf-8")
    return {
        "schema": "w33.pass3973_3980.dual_certificate_frontier_integration.v1",
        "status": "PASS",
        "changed": {
            "required_ordered_inputs": changed_inputs,
            "public_sections": changed_sections,
            "standalone_public_pages": changed_pages,
        },
        "protected_index_modified": False,
        "tex_input": TEX_INPUT,
        "public_sections": PUBLIC_SECTIONS,
        "standalone_pages": PUBLIC_PAGES,
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
    print("PASS Passes 3973-3980 dual-certificate frontier reconciliation")
    print(payload, end="")


if __name__ == "__main__":
    main()
