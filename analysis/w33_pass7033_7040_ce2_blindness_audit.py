#!/usr/bin/env python3
"""Passes 7033--7040: audit CE2 'normal-form' derivation for answer leakage.

This is a source-level evidence audit, not a replacement CE2 solver.  It makes a
strict distinction between:

  runtime blind: prediction does not read the target answer artifact while it is
                 producing a prediction;
  provenance blind: every coefficient used by the predictor was derived without
                    fitting to the target answer artifact.

A true no-answer-table replay needs both.
"""
from __future__ import annotations

import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "scripts" / "ce2_global_cocycle.py"
OUT = ROOT / "data" / "PART_W33_PASS7033_7040_CE2_BLINDNESS_AUDIT.json"

ROOT_FUNCS = [
    "_derive_tables_via_normal_form",
    "_derive_naive_tables",
    "_reconstruct_simple_family_sign_from_seed",
]
FORBIDDEN_RUNTIME = {
    "_simple_family_sign_map",
    "_committed_ce2_uv_map",
}
PROVENANCE_MARKERS = [
    "full 864-entry dataset",
    "fitting the actual deltas",
    "computed once by fitting",
    "build constant tables from sign map",
    "uses the *actual* sign map",
]


def called_names(node: ast.AST) -> set[str]:
    out = set()
    for n in ast.walk(node):
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name):
            out.add(n.func.id)
    return out


def main():
    text = SRC.read_text(encoding="utf-8")
    tree = ast.parse(text)
    funcs = {n.name:n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))}
    graph = {name:called_names(node) & set(funcs) for name,node in funcs.items()}

    def closure(root):
        seen=set(); stack=[root]
        while stack:
            f=stack.pop()
            if f in seen or f not in graph: continue
            seen.add(f); stack.extend(graph[f]-seen)
        return seen

    closures = {r:sorted(closure(r)) for r in ROOT_FUNCS}
    runtime_hits = {
        r:sorted(set(closures[r]) & FORBIDDEN_RUNTIME)
        for r in ROOT_FUNCS
    }
    marker_hits = {m:(m in text) for m in PROVENANCE_MARKERS}

    # Exact direct facts required by the current source.  These deliberately
    # fail closed if a future refactor removes or changes the leakage points.
    assert "_simple_family_sign_map" in graph["_derive_tables_via_normal_form"]
    assert "_simple_family_sign_map" in graph["_derive_naive_tables"]
    assert "uses the *actual* sign map" in text
    assert "full 864-entry dataset" in text
    assert "fitting the actual deltas" in text or "computed once by fitting" in text

    report = {
        "passes": list(range(7033,7041)),
        "source": str(SRC.relative_to(ROOT)),
        "definitions": {
            "runtime_blind": "No target answer artifact or answer-derived lookup is read while producing predictions.",
            "provenance_blind": "No coefficient or rule used by prediction was fitted/selected from the target answers."
        },
        "call_closures": closures,
        "runtime_answer_dependencies": runtime_hits,
        "source_marker_hits": marker_hits,
        "findings": {
            "derive_tables_via_normal_form_runtime_blind": False,
            "derive_naive_tables_runtime_blind": False,
            "current_delta_polynomials_provenance_blind": False,
            "current_constant_line_tables_provenance_blind": False,
            "seed_transport_is_structural_compression": True,
            "independent_no_answer_table_replay_closed": False
        },
        "verdict": "The current normal-form machinery is a strong structural compression of the 864 simple-family signs, but it is not an independent no-answer-table derivation: the advertised normal-form table builder reads _simple_family_sign_map, constant-line signs are built from that map, and delta polynomials are documented as fits to the full 864-entry dataset.",
        "required_next_certificate": [
            "derive seed coefficients from the E6/Heisenberg bracket rather than the target sign table",
            "derive delta law algebraically from the metaplectic/Heisenberg action rather than fitting it",
            "enumerate the simple-family domain structurally without reading answer keys",
            "freeze a prediction hash before opening ce2_sparse_local_solutions.json",
            "only then compare all predicted sparse rows to the committed target artifact"
        ],
        "boundary": "This does not refute the correctness of the existing predictor on its dataset; it refutes only the stronger claim of answer-independent derivation."
    }
    OUT.write_text(json.dumps(report,indent=2),encoding="utf-8")
    print(json.dumps(report,indent=2))
    return report

if __name__ == "__main__":
    main()
