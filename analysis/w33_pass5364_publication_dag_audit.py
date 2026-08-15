#!/usr/bin/env python3
"""Pass5365: recursively audit the live W33 publication-frontier DAG.

The original current-frontier auditor was written while
analysis/W33_CURRENT_FRONTIER_MANIFEST.tex was flat.  The live manifest is now a
wrapper around W33_CURRENT_FRONTIER_MANIFEST_THROUGH_4864 plus later inserts.
A flat direct-input comparison therefore became stale and, more importantly,
could not detect the same theorem insert being reachable through both the
nested legacy manifest and a new direct edge.

This verifier treats the publication layer as a directed acyclic graph:

  front-door wrapper -> current frontier root -> nested frontier manifests -> leaves.

It checks exact file reachability, cycle freedom, leaf uniqueness, wrapper
single-entry semantics, legacy-required reachability, and the configured public
index tokens.  It deliberately does not certify mathematical or physical claims.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "data/w33_current_frontier_manifest_v1.json"
INPUT_RE = re.compile(r"\\input\{([^}]+)\}%?")
ROOT_MANIFEST = "analysis/W33_CURRENT_FRONTIER_MANIFEST"
ROOT_MARKER = rf"\input{{{ROOT_MANIFEST}}}%"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tex_path(item: str) -> Path:
    rel = Path(item)
    if rel.suffix == "":
        rel = rel.with_suffix(".tex")
    return ROOT / rel


def rel_tex(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    return rel[:-4] if rel.endswith(".tex") else rel


def parse_inputs(path: Path) -> list[str]:
    return INPUT_RE.findall(path.read_text(encoding="utf-8"))


def is_nested_manifest(path: Path) -> bool:
    return path.name.startswith("W33_CURRENT_FRONTIER_MANIFEST")


def build_frontier_dag(root_item: str = ROOT_MANIFEST) -> dict:
    root = tex_path(root_item)
    assert root.is_file(), root

    nodes: dict[str, list[str]] = {}
    incoming: dict[str, list[str]] = defaultdict(list)
    leaves: list[str] = []
    manifest_nodes: list[str] = []

    def walk(path: Path, stack: tuple[str, ...]) -> None:
        node = rel_tex(path)
        if node in stack:
            raise AssertionError(f"frontier include cycle: {' -> '.join(stack + (node,))}")
        manifest_nodes.append(node)
        children = parse_inputs(path)
        nodes[node] = list(children)
        next_stack = stack + (node,)
        for child in children:
            child_path = tex_path(child)
            assert child_path.is_file(), child_path
            child_key = rel_tex(child_path)
            incoming[child_key].append(node)
            if is_nested_manifest(child_path):
                walk(child_path, next_stack)
            else:
                leaves.append(child_key)

    walk(root, ())

    duplicate_leaves = {
        leaf: parents
        for leaf, parents in sorted(incoming.items())
        if not is_nested_manifest(tex_path(leaf)) and len(parents) != 1
    }
    assert not duplicate_leaves, duplicate_leaves
    assert len(leaves) == len(set(leaves)), "duplicate leaf theorem insert in frontier DAG"
    assert len(manifest_nodes) == len(set(manifest_nodes)), "manifest node reached more than once"

    return {
        "root": root_item,
        "manifest_nodes": manifest_nodes,
        "nodes": nodes,
        "leaves": leaves,
        "leaf_count": len(leaves),
        "manifest_node_count": len(manifest_nodes),
        "incoming": {k: v for k, v in sorted(incoming.items())},
    }


def section_count(index_text: str, section: dict) -> int:
    token = section["token"]
    if section["kind"] == "id":
        return index_text.count(f'id="{token}"')
    if section["kind"] == "marker":
        return index_text.count(token)
    raise ValueError(f"unsupported public section kind: {section['kind']}")


def audit(require_index: bool = True) -> dict:
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    dag = build_frontier_dag(config["tex_manifest"].removesuffix(".tex"))
    reachable = set(dag["leaves"]) | set(dag["manifest_nodes"])

    # The v1 list predates nesting.  It remains valuable as a historical
    # must-remain-reachable subset, but it is no longer the direct child list.
    legacy_required = list(config.get("required_ordered_inputs", []))
    assert len(legacy_required) == len(set(legacy_required))
    missing_legacy = [item for item in legacy_required if item not in reachable]
    assert not missing_legacy, missing_legacy

    wrappers = {}
    leaf_set = set(dag["leaves"])
    for wrapper_name, body_name in config["front_doors"].items():
        wrapper = ROOT / wrapper_name
        body = ROOT / body_name
        assert wrapper.is_file() and body.is_file()
        text = wrapper.read_text(encoding="utf-8")
        direct = parse_inputs(wrapper)
        assert text.count(ROOT_MARKER) == 1, wrapper_name
        assert direct.count(body_name.removesuffix(".tex")) + direct.count(body_name) == 1, wrapper_name

        explicit_frontier = [
            item for item in direct
            if item != ROOT_MANIFEST and item not in {body_name, body_name.removesuffix(".tex")}
        ]
        duplicate_frontier = sorted(set(explicit_frontier) & leaf_set)
        assert not duplicate_frontier, (wrapper_name, duplicate_frontier)
        wrappers[wrapper_name] = {
            "sha256": sha256(wrapper),
            "body": body_name,
            "manifest_references": text.count(ROOT_MARKER),
            "explicit_nonmanifest_inserts": len(explicit_frontier),
            "duplicate_manifest_leaves": duplicate_frontier,
        }

    index_path = ROOT / config["public_index"]
    index_status = {"required": require_index, "path": str(index_path.relative_to(ROOT))}
    if require_index:
        assert index_path.is_file(), index_path
        index_text = index_path.read_text(encoding="utf-8")
        observed = {
            section["token"]: section_count(index_text, section)
            for section in config["public_sections"]
        }
        assert all(count == 1 for count in observed.values()), observed
        index_status.update({"sha256": sha256(index_path), "sections": observed})

    return {
        "schema": "w33.publication_frontier_dag.v1",
        "pass": 5365,
        "status": "PASS",
        "boundary": "Publication reachability only; no mathematical, hardware, laboratory, or physical claim is certified here.",
        "frontier": {
            "root": dag["root"],
            "manifest_nodes": dag["manifest_nodes"],
            "manifest_node_count": dag["manifest_node_count"],
            "leaf_count": dag["leaf_count"],
            "leaves": dag["leaves"],
            "legacy_required_count": len(legacy_required),
            "legacy_required_missing": missing_legacy,
        },
        "wrappers": wrappers,
        "index": index_status,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", type=Path)
    parser.add_argument("--allow-unmaterialized-index", action="store_true")
    args = parser.parse_args()
    report = audit(require_index=not args.allow_unmaterialized_index)
    payload = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(payload, encoding="utf-8")
    print(
        "PASS publication DAG "
        f"manifests={report['frontier']['manifest_node_count']} "
        f"leaves={report['frontier']['leaf_count']}"
    )
    print(payload, end="")


if __name__ == "__main__":
    main()
