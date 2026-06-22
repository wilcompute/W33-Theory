#!/usr/bin/env python3
"""BT1484: regenerate paper claim table from BT1481 E6-merged DAG."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from bt1481_e6_firewall_claim_dag_merge import main as rebuild_bt1481_dag  # noqa: E402

DAG = ROOT / "data" / "bt1481_e6_firewall_claim_dag_merge.json"
OUT_JSON = ROOT / "data" / "bt1484_e6_dag_claim_table_v2.json"
OUT_TEX = ROOT / "analysis" / "BT1484_e6_dag_claim_table_v2.tex"

LANGUAGE = {
    "exact_coordinate": "exact coordinate claim",
    "exact_finite_arithmetic": "exact finite arithmetic claim",
    "exact_finite_group": "exact finite group claim",
    "verified_finite_decoder": "verified decoder claim",
    "exact_runtime_abi": "runtime ABI contract",
    "exact_finite_structure": "exact finite structure claim",
    "numerical_structural_resonance": "resonance language only",
    "numerical_resonance": "numerical proximity only",
    "blocked_pending_transcription": "blocked until formula transcription",
    "speculative_not_imported": "not imported as established claim",
}


def main() -> None:
    dag = json.loads(DAG.read_text(encoding="utf-8"))
    if "nodes" not in dag or "edges" not in dag or "topological_order" not in dag:
        rebuild_bt1481_dag()
        dag = json.loads(DAG.read_text(encoding="utf-8"))
    nodes = dag["nodes"]
    edges = dag["edges"]
    deps = {n: [] for n in nodes}
    for e in edges:
        deps[e["to"]].append(e["from"])
    rows = []
    for n in dag["topological_order"]:
        meta = nodes[n]
        provenance = (
            "E6/CSS"
            if n.startswith("E") or any(d.startswith("E") for d in deps.get(n, []))
            else "CSS/finite"
        )
        rows.append(
            {
                "node": n,
                "claim": meta["claim"],
                "tier": meta["tier"],
                "dependencies": deps.get(n, []),
                "provenance": provenance,
                "allowed_language": LANGUAGE.get(meta["tier"], "cautious language"),
            }
        )
    lines = [
        r"\begin{center}\scriptsize",
        r"\begin{tabular}{p{0.18\textwidth}p{0.16\textwidth}p{0.18\textwidth}p{0.18\textwidth}p{0.20\textwidth}}",
        r"\toprule",
        r"Claim node & Tier & Provenance & Dependencies & Allowed language\\",
        r"\midrule",
    ]
    for r in rows:
        node = r["node"].replace("_", r"\_")
        tier = r["tier"].replace("_", r"\_")
        prov = r["provenance"].replace("_", r"\_")
        dep = (", ".join(r["dependencies"]) if r["dependencies"] else "root").replace(
            "_", r"\_"
        )
        lang = r["allowed_language"].replace("_", r"\_")
        lines.append(f"{node} & {tier} & {prov} & {dep} & {lang}\\")
    lines.extend([r"\bottomrule", r"\end{tabular}", r"\end{center}"])
    OUT_TEX.write_text("\n".join(lines) + "\n", encoding="utf-8")
    e_nodes = [r for r in rows if r["node"].startswith("E")]
    checks = {
        "dag_verified": dag.get("verified") is True,
        "row_count_matches_nodes": len(rows) == len(nodes),
        "has_four_e_nodes": len(e_nodes) == 4,
        "has_72_node": any(r["node"] == "E1_oriented_72_sector" for r in rows),
        "has_81_node": any(r["node"] == "E2_h1_81_closure" for r in rows),
        "has_c3_v4_node": any(r["node"] == "E3_c3_v4_grid" for r in rows),
        "blocked_language_present": any(
            "blocked" in r["allowed_language"] for r in rows
        ),
        "tex_written": OUT_TEX.exists()
        and "Provenance" in OUT_TEX.read_text(encoding="utf-8"),
    }
    result = {
        "bt": 1484,
        "title": "E6-DAG claim table v2",
        "verified": all(checks.values()),
        "source_dag": "data/bt1481_e6_firewall_claim_dag_merge.json",
        "tex_table": "analysis/BT1484_e6_dag_claim_table_v2.tex",
        "rows": rows,
        "interpretation": "Claim table v2 includes E6 provenance for the 72-sector, 81 closure, and C3 x V4 grid while preserving blocked-language gates.",
        "checks": checks,
    }
    OUT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(
        json.dumps(
            {"bt": 1484, "verified": result["verified"], "rows": len(rows)}, indent=2
        )
    )
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
