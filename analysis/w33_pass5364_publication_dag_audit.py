#!/usr/bin/env python3
"""Pass5364--5371: recursively audit the live W33 publication frontier.

The original current-frontier auditor assumed a flat manifest.  The live source
is now nested, so publication integrity has to be checked as a DAG.  This
verifier uses the v2 publication contract while retaining the old v1 manifest
ledger as archival must-remain-reachable data.

Scope: source reachability, uniqueness, and public materialization only.  No
mathematical, hardware, laboratory, empirical, or physical claim is certified.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "data/w33_publication_frontier_contract_v2.json"
INPUT_RE = re.compile(r"\\input\{([^}]+)\}%?")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


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


def build_frontier_dag(root_item: str) -> dict:
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
        if node in manifest_nodes:
            raise AssertionError(f"manifest node reached more than once: {node}")
        manifest_nodes.append(node)
        children = parse_inputs(path)
        assert len(children) == len(set(children)), (node, "duplicate direct include")
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

    return {
        "root": rel_tex(root),
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


def configured_public_sections(contract: dict, legacy: dict) -> tuple[list[dict], dict]:
    sections = list(legacy.get("public_sections", []))
    extension_meta = {}
    for rel in contract.get("public_extension_contracts", []):
        path = ROOT / rel
        assert path.is_file(), path
        extension = load_json(path)
        assert extension.get("schema") == "w33.public_frontier_extension.v1", rel
        added = list(extension.get("public_sections", []))
        sections.extend(added)
        extension_meta[rel] = len(added)
    local = list(contract.get("local_public_sections", []))
    sections.extend(local)

    seen: set[tuple[str, str]] = set()
    for section in sections:
        key = (section["kind"], section["token"])
        assert key not in seen, ("duplicate public token", key)
        seen.add(key)
        source = ROOT / section["source"]
        assert source.is_file(), source
    return sections, {
        "legacy_count": len(legacy.get("public_sections", [])),
        "extensions": extension_meta,
        "local_count": len(local),
        "total_count": len(sections),
    }


def audit(require_index: bool = True) -> dict:
    contract = load_json(CONTRACT)
    assert contract.get("schema") == "w33.publication_frontier_contract.v2"
    legacy_path = ROOT / contract["legacy_contract"]
    legacy = load_json(legacy_path)

    root_item = contract["frontier_root"].removesuffix(".tex")
    root_marker = rf"\input{{{root_item}}}%"
    dag = build_frontier_dag(root_item)
    reachable = set(dag["leaves"]) | set(dag["manifest_nodes"])

    # Historical v1 was a flat manifest contract.  Once the source became
    # nested it ceased to be a direct-child list, but its entries remain a
    # useful must-remain-reachable archival subset.  Record rather than hide
    # any duplicate entries that accumulated in that historical ledger.
    legacy_required = list(legacy.get("required_ordered_inputs", []))
    counts = Counter(legacy_required)
    legacy_duplicates = {k: v for k, v in sorted(counts.items()) if v > 1}
    legacy_unique = list(dict.fromkeys(legacy_required))
    missing_legacy = [item for item in legacy_unique if item not in reachable]
    assert not missing_legacy, missing_legacy

    wrappers = {}
    leaf_set = set(dag["leaves"])
    for wrapper_name, body_name in contract["front_doors"].items():
        wrapper = ROOT / wrapper_name
        body = ROOT / body_name
        assert wrapper.is_file() and body.is_file()
        text = wrapper.read_text(encoding="utf-8")
        direct = parse_inputs(wrapper)
        assert len(direct) == len(set(direct)), (wrapper_name, "duplicate direct include")
        assert text.count(root_marker) == 1, wrapper_name
        assert direct.count(body_name.removesuffix(".tex")) + direct.count(body_name) == 1, wrapper_name

        explicit_frontier = [
            item for item in direct
            if item != root_item and item not in {body_name, body_name.removesuffix(".tex")}
        ]
        duplicate_frontier = sorted(set(explicit_frontier) & leaf_set)
        assert not duplicate_frontier, (wrapper_name, duplicate_frontier)
        wrappers[wrapper_name] = {
            "sha256": sha256(wrapper),
            "body": body_name,
            "manifest_references": text.count(root_marker),
            "explicit_nonmanifest_inserts": len(explicit_frontier),
            "duplicate_manifest_leaves": duplicate_frontier,
        }

    sections, public_contract = configured_public_sections(contract, legacy)
    index_path = ROOT / contract["public_index"]
    index_status = {
        "required": require_index,
        "path": str(index_path.relative_to(ROOT)),
        "contract": public_contract,
    }
    if require_index:
        assert index_path.is_file(), index_path
        index_text = index_path.read_text(encoding="utf-8")
        observed = {section["token"]: section_count(index_text, section) for section in sections}
        bad = {token: count for token, count in observed.items() if count != 1}
        assert not bad, bad
        index_status.update({"sha256": sha256(index_path), "sections": observed})

    return {
        "schema": "w33.publication_frontier_dag.v2",
        "pass_range": [5364, 5371],
        "status": "PASS",
        "boundary": contract["boundary"],
        "contract": {
            "path": str(CONTRACT.relative_to(ROOT)),
            "sha256": sha256(CONTRACT),
            "legacy_path": str(legacy_path.relative_to(ROOT)),
            "legacy_sha256": sha256(legacy_path),
        },
        "frontier": {
            "root": dag["root"],
            "manifest_nodes": dag["manifest_nodes"],
            "manifest_node_count": dag["manifest_node_count"],
            "leaf_count": dag["leaf_count"],
            "leaves": dag["leaves"],
            "legacy_required_original_count": len(legacy_required),
            "legacy_required_unique_count": len(legacy_unique),
            "legacy_required_duplicates": legacy_duplicates,
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
        f"leaves={report['frontier']['leaf_count']} "
        f"public={report['index']['contract']['total_count']}"
    )
    print(payload, end="")


if __name__ == "__main__":
    main()
