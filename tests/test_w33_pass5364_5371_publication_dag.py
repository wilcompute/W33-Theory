from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_auditor():
    path = ROOT / "analysis/w33_pass5364_publication_dag_audit.py"
    spec = importlib.util.spec_from_file_location("pass5364_publication_dag", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_recursive_frontier_and_shared_tail_are_unique():
    report = load_auditor().audit(require_index=False)
    assert report["status"] == "PASS"
    frontier = report["frontier"]
    assert frontier["manifest_node_count"] >= 2
    assert frontier["leaf_count"] == len(set(frontier["leaves"]))
    assert frontier["legacy_required_missing"] == []
    tail = report["shared_tail"]
    assert tail["leaf_count"] == 28
    assert tail["leaf_count"] == len(set(tail["leaves"]))
    assert tail["overlap_with_frontier"] == []


def test_three_front_doors_have_one_root_one_tail_and_one_body():
    contract = json.loads((ROOT / "data/w33_publication_frontier_contract_v2.json").read_text(encoding="utf-8"))
    root = r"\input{analysis/W33_CURRENT_FRONTIER_MANIFEST}%"
    tail = r"\input{analysis/W33_SHARED_FRONTIER_TAIL}%"
    for wrapper_name, body_name in contract["front_doors"].items():
        text = (ROOT / wrapper_name).read_text(encoding="utf-8")
        assert text.count(root) == 1
        assert text.count(tail) == 1
        assert text.index(root) < text.index(tail)
        assert text.count(rf"\input{{{body_name}}}") == 1


def test_public_contract_v2_sources_exist_and_tokens_are_unique():
    module = load_auditor()
    contract = module.load_json(module.CONTRACT)
    legacy = module.load_json(ROOT / contract["legacy_contract"])
    sections, meta = module.configured_public_sections(contract, legacy)
    keys = [(row["kind"], row["token"]) for row in sections]
    assert len(keys) == len(set(keys))
    assert meta["local_count"] == 1
    assert meta["total_count"] == len(sections)
    for row in sections:
        assert (ROOT / row["source"]).is_file()
