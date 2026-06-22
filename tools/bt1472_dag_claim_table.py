#!/usr/bin/env python3
"""BT1472: convert the claim dependency DAG into a paper-ready TeX table."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DAG = ROOT / "data" / "bt1469_paper_claim_dependency_dag.json"
OUT_JSON = ROOT / "data" / "bt1472_dag_claim_table.json"
OUT_TEX = ROOT / "analysis" / "BT1472_dag_claim_table.tex"

LANGUAGE = {
    "exact_coordinate": "state exactly as finite coordinate fact",
    "exact_finite_arithmetic": "state exactly as finite count identity",
    "exact_finite_group": "state exactly as finite group classifier",
    "verified_finite_decoder": "state as verified finite decoder fact",
    "exact_runtime_abi": "state as runtime ABI contract",
    "numerical_structural_resonance": "label as structural/numerical resonance",
    "numerical_resonance": "label as numerical proximity only",
    "blocked_pending_transcription": "do not promote before formula transcription",
    "speculative_not_imported": "do not import as established claim",
}


def main() -> None:
    dag = json.loads(DAG.read_text(encoding="utf-8"))
    nodes = dag["nodes"] if "nodes" in dag else {}
    edges = dag["edges"] if "edges" in dag else []
    deps = {n: [] for n in nodes}
    for edge in edges:
        a = edge["from"] if isinstance(edge, dict) else edge[0]
        b = edge["to"] if isinstance(edge, dict) else edge[1]
        deps.setdefault(b, []).append(a)
    rows = []
    for n in dag.get("topological_order", list(nodes)):
        meta = nodes[n]
        rows.append({
            "node": n,
            "claim": meta["claim"],
            "tier": meta["tier"],
            "deps": deps.get(n, []),
            "allowed_language": LANGUAGE.get(meta["tier"], "state with caution"),
        })
    lines = [
        r"\begin{center}\small",
        r"\begin{tabular}{p{0.23\textwidth}p{0.18\textwidth}p{0.27\textwidth}p{0.22\textwidth}}",
        r"\toprule",
        r"Claim & Tier & Dependencies & Allowed paper language\\",
        r"\midrule",
    ]
    for r in rows:
        dep_text = ", ".join(r["deps"]) if r["deps"] else "root"
        claim = r["claim"].replace("_", r"\_")
        tier = r["tier"].replace("_", r"\_")
        deps_tex = dep_text.replace("_", r"\_")
        lang = r["allowed_language"].replace("_", r"\_")
        lines.append(f"{claim} & {tier} & {deps_tex} & {lang}\\")
    lines.extend([r"\bottomrule", r"\end{tabular}", r"\end{center}"])
    OUT_TEX.write_text("\n".join(lines) + "\n", encoding="utf-8")
    checks = {
        "rows_match_nodes": len(rows) == len(nodes),
        "tex_written": OUT_TEX.exists() and "Allowed paper language" in OUT_TEX.read_text(encoding="utf-8"),
        "has_blocked_language": any("do not promote" in r["allowed_language"] for r in rows),
        "has_exact_language": any(r["allowed_language"].startswith("state exactly") for r in rows),
        "root_is_szilassi": rows[0]["node"] == "N0_szilassi_coordinates",
    }
    result = {
        "bt": 1472,
        "title": "DAG-to-paper claim table",
        "verified": all(checks.values()),
        "tex_table": "analysis/BT1472_dag_claim_table.tex",
        "rows": rows,
        "checks": checks,
    }
    OUT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"bt": 1472, "verified": result["verified"], "rows": len(rows)}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
