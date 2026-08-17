#!/usr/bin/env python3
"""Pass5364--5371: recursively audit the live W33 publication frontier.

The original current-frontier auditor assumed a flat manifest.  The live source
is now nested, and all three canonical papers also share one post-manifest tail.
This verifier checks those publication objects as an explicit source DAG using
the v2 publication contract while retaining the old v1 ledger as archival
must-remain-reachable data.

Scope: source reachability, uniqueness, shared-tail consolidation, and public
materialization only.  No mathematical, hardware, laboratory, empirical, or
physical claim is certified.
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
PUBLIC_SOURCE_ALIASES = {
    "analysis/BT3528_BT3534_borel_star_moore_transplant_index_insert.html":
        "analysis/BT3528_BT3534_borel_star_moore_functor_transplant_index_insert.html",
    "analysis/PASS4544_4551_module_cubic_zeta_index_insert.html":
        "analysis/PASS4544_4551_module_cubic_enumerator_zeta_index_insert.html",
}
# Historical v1 theorem names are archival evidence, but a few were explicitly
# superseded by collision-safe canonical wrappers.  Keep the old spelling in the
# ledger and resolve it here rather than rewriting history or requiring duplicate
# live theorem leaves.  Pass3996's own reconciler declared this exact migration.
MANIFEST_SOURCE_ALIASES = {
    "analysis/BT3989_BT3996_physical_incidence_photon_breakthrough_insert":
        "analysis/BT3989_BT3996_physical_photon_causal_memory_insert",
}
PUBLIC_SECTION_ALIASES = {
    ("id", "bt3418-3429-clebsch-d5-supplement"):
        ("marker", "<!-- BT3418-BT3429-CLEBSCH-D5-SUPPLEMENT -->"),
    ("id", "pass4579-4586-o8plus-exceptional-bridge"):
        ("id", "pass4579-4586-o8plus-exceptional"),
    ("id", "pass4624-4631-packet-incidence-f4-h10"):
        ("id", "pass4624-4631-packet-incidence-f4"),
}


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


def build_shared_tail(tail_item: str, forbidden: set[str]) -> dict:
    path = tex_path(tail_item)
    assert path.is_file(), path
    leaves = parse_inputs(path)
    assert leaves, "shared frontier tail is empty"
    assert len(leaves) == len(set(leaves)), "duplicate theorem insert in shared frontier tail"
    normalized = []
    for item in leaves:
        child = tex_path(item)
        assert child.is_file(), child
        normalized.append(rel_tex(child))
    overlap = sorted(set(normalized) & forbidden)
    assert not overlap, ("shared tail overlaps current-frontier root", overlap)
    return {
        "root": rel_tex(path),
        "sha256": sha256(path),
        "leaf_count": len(normalized),
        "leaves": normalized,
        "overlap_with_frontier": overlap,
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
    resolved_sections: list[dict] = []
    source_aliases: dict[str, str] = {}
    section_aliases: dict[str, str] = {}
    for section in sections:
        section = dict(section)
        original_source = section["source"]
        section["source"] = PUBLIC_SOURCE_ALIASES.get(original_source, original_source)
        if section["source"] != original_source:
            source_aliases[original_source] = section["source"]
        original_key = (section["kind"], section["token"])
        section["kind"], section["token"] = PUBLIC_SECTION_ALIASES.get(
            original_key,
            original_key,
        )
        if (section["kind"], section["token"]) != original_key:
            section_aliases[f"{original_key[0]}:{original_key[1]}"] = (
                f"{section['kind']}:{section['token']}"
            )
        key = (section["kind"], section["token"])
        assert key not in seen, ("duplicate public token", key)
        seen.add(key)
        source = ROOT / section["source"]
        assert source.is_file(), source
        resolved_sections.append(section)
    return resolved_sections, {
        "legacy_count": len(legacy.get("public_sections", [])),
        "extensions": extension_meta,
        "local_count": len(local),
        "source_aliases": source_aliases,
        "section_aliases": section_aliases,
        "total_count": len(sections),
    }


def audit(require_index: bool = True) -> dict:
    contract = load_json(CONTRACT)
    assert contract.get("schema") == "w33.publication_frontier_contract.v2"
    legacy_path = ROOT / contract["legacy_contract"]
    legacy = load_json(legacy_path)

    root_item = contract["frontier_root"].removesuffix(".tex")
    tail_item = contract["shared_wrapper_tail"].removesuffix(".tex")
    root_marker = rf"\input{{{root_item}}}%"
    tail_marker = rf"\input{{{tail_item}}}%"
    dag = build_frontier_dag(root_item)
    leaf_set = set(dag["leaves"])
    tail = build_shared_tail(tail_item, leaf_set)
    tail_set = set(tail["leaves"])
    reachable = leaf_set | set(dag["manifest_nodes"])

    # Historical v1 was a flat manifest contract.  Once the source became
    # nested it ceased to be a direct-child list, but its entries remain a
    # useful must-remain-reachable archival subset.  Record rather than hide
    # any duplicate entries that accumulated in that historical ledger.
    legacy_required = list(legacy.get("required_ordered_inputs", []))
    counts = Counter(legacy_required)
    legacy_duplicates = {k: v for k, v in sorted(counts.items()) if v > 1}
    legacy_unique = list(dict.fromkeys(legacy_required))
    legacy_aliases = {
        item: MANIFEST_SOURCE_ALIASES[item]
        for item in legacy_unique
        if item in MANIFEST_SOURCE_ALIASES
    }
    resolved_legacy = [MANIFEST_SOURCE_ALIASES.get(item, item) for item in legacy_unique]
    # A current-frontier leaf may be a collision-safe wrapper around an older
    # theorem insert.  Count the wrapped theorem as reachable without promoting
    # every ordinary theorem insert into a recursive manifest node.
    wrapped_legacy: dict[str, str] = {}
    for parent in dag["leaves"]:
        for child in parse_inputs(tex_path(parent)):
            if child in resolved_legacy:
                wrapped_legacy[child] = parent
    missing_legacy = [
        item for item in resolved_legacy
        if item not in reachable and item not in wrapped_legacy
    ]
    assert not missing_legacy, missing_legacy

    wrappers = {}
    for wrapper_name, body_name in contract["front_doors"].items():
        wrapper = ROOT / wrapper_name
        body = ROOT / body_name
        assert wrapper.is_file() and body.is_file()
        text = wrapper.read_text(encoding="utf-8")
        direct = parse_inputs(wrapper)
        assert len(direct) == len(set(direct)), (wrapper_name, "duplicate direct include")
        assert text.count(root_marker) == 1, wrapper_name
        assert text.count(tail_marker) == 1, wrapper_name
        assert direct.index(root_item) < direct.index(tail_item), (wrapper_name, "tail must follow frontier root")
        assert direct.count(body_name.removesuffix(".tex")) + direct.count(body_name) == 1, wrapper_name

        explicit = [
            item for item in direct
            if item not in {root_item, tail_item, body_name, body_name.removesuffix(".tex")}
        ]
        duplicate_root = sorted(set(explicit) & leaf_set)
        duplicate_tail = sorted(set(explicit) & tail_set)
        assert not duplicate_root, (wrapper_name, duplicate_root)
        assert not duplicate_tail, (wrapper_name, duplicate_tail)
        wrappers[wrapper_name] = {
            "sha256": sha256(wrapper),
            "body": body_name,
            "manifest_references": text.count(root_marker),
            "shared_tail_references": text.count(tail_marker),
            "explicit_manuscript_specific_inserts": len(explicit),
            "duplicate_manifest_leaves": duplicate_root,
            "duplicate_shared_tail_leaves": duplicate_tail,
        }

    sections, public_contract = configured_public_sections(contract, legacy)
    index_path = ROOT / contract["public_index"]
    index_status = {
        "required": require_index,
        "path": str(index_path.relative_to(ROOT)),
        "contract": public_contract,
    }
    if require_index:
        index_text = index_path.read_text(encoding="utf-8")
        index_counts = {
            f"{section['kind']}:{section['token']}": section_count(index_text, section)
            for section in sections
        }
        bad = {k: v for k, v in index_counts.items() if v != 1}
        assert not bad, bad
        index_status["section_counts"] = index_counts
        index_status["section_count"] = len(index_counts)
        index_status["sha256"] = sha256(index_path)
    else:
        index_status["section_count"] = len(sections)
        index_status["materialization_check"] = "SKIPPED"

    return {
        "schema": "w33.pass5364_5371.publication_dag_audit.v2",
        "status": "PASS_PUBLICATION_DAG_EXACT_ONCE",
        "contract": str(CONTRACT.relative_to(ROOT)),
        "legacy_contract": str(legacy_path.relative_to(ROOT)),
        "frontier": {
            "root": dag["root"],
            "manifest_nodes": dag["manifest_node_count"],
            "leaf_inserts": dag["leaf_count"],
            "legacy_required_count": len(legacy_required),
            "legacy_unique_count": len(legacy_unique),
            "legacy_duplicate_entries": legacy_duplicates,
            "legacy_manifest_aliases": legacy_aliases,
            "legacy_wrapped_inputs": wrapped_legacy,
            "shared_tail": tail,
        },
        "front_doors": wrappers,
        "public_index": index_status,
        "boundary": (
            "This audit certifies source reachability, exact-once manuscript consolidation, "
            "and public-section materialization only. It does not certify mathematical claims, "
            "hardware, laboratory evidence, or physical interpretation."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", type=Path)
    parser.add_argument(
        "--allow-unmaterialized-index",
        action="store_true",
        help="Audit source DAG and contract before docs/index.html is reconciled.",
    )
    args = parser.parse_args()
    report = audit(require_index=not args.allow_unmaterialized_index)
    if args.report:
        args.report.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
