#!/usr/bin/env python3
"""Fail-closed audit of the nested W33 current-frontier publication DAG.

Pass5366 replaces the obsolete flat-manifest comparison with the recursive
Pass5365 verifier while retaining this historical command-line entry point for
workflows and downstream tools.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDITOR = ROOT / "analysis/w33_pass5364_publication_dag_audit.py"


def _load_recursive_auditor():
    spec = importlib.util.spec_from_file_location("w33_pass5364_publication_dag_audit", AUDITOR)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def audit(require_index: bool = True) -> dict:
    module = _load_recursive_auditor()
    return module.audit(require_index=require_index)


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
        "PASS current-frontier DAG audit "
        f"manifests={report['frontier']['manifest_node_count']} "
        f"leaves={report['frontier']['leaf_count']}"
    )
    print(payload, end="")


if __name__ == "__main__":
    main()
