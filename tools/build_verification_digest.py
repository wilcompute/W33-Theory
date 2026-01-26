#!/usr/bin/env python3
"""Build a verification digest from existing JSON artifacts.

Produces:
- artifacts/verification_digest.md
- artifacts/verification_digest.json
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_MD = ROOT / "artifacts" / "verification_digest.md"
OUT_JSON = ROOT / "artifacts" / "verification_digest.json"


def load_json(path: Path):
    if not path.exists():
        return None
    with path.open() as f:
        return json.load(f)


def summarize_baseline_audit(data):
    if not data:
        return None
    summary = {
        "num_exprs": data.get("global", {}).get("num_exprs"),
        "tolerances_pct": data.get("tolerances_pct"),
        "targets": {},
        "config": data.get("config", {}),
    }
    for name, t in data.get("targets", {}).items():
        summary["targets"][name] = {
            "hits": t.get("hits", {}),
            "top_example": (t.get("top") or [None])[0],
        }
    return summary


def summarize_baseline_suite(data):
    if not data:
        return None
    suite = {}
    for mode, payload in data.get("suite", {}).items():
        results = payload.get("results", {})
        suite[mode] = {
            "num_exprs": results.get("num_exprs"),
            "tolerances_pct": results.get("tolerances_pct"),
            "targets": {
                name: {"hits": t.get("hits", {})}
                for name, t in (results.get("targets") or {}).items()
            },
            "config": payload.get("config", {}),
        }
    return suite


def summarize_sage_incidence(data):
    if not data:
        return None
    inc = data.get("incidence", {})
    h1 = data.get("h1_action", {})
    matrices = h1.get("generator_matrices") or []
    h1_dim = len(matrices[0]) if matrices else None
    return {
        "field": data.get("field"),
        "group_order": inc.get("group_order"),
        "structure": inc.get("structure_description"),
        "is_abelian": inc.get("is_abelian"),
        "is_solvable": inc.get("is_solvable"),
        "num_generators": len(inc.get("generators") or []),
        "h1_dim": h1_dim,
        "h1_num_matrices": len(matrices),
    }


def summarize_verification_results(data):
    if not data:
        return None
    return {
        "timestamp": data.get("timestamp"),
        "verified_count": len(data.get("verified") or []),
        "failed_count": len(data.get("failed") or []),
        "verification_rate": data.get("verification_rate"),
        "verified": data.get("verified") or [],
        "failed": data.get("failed") or [],
    }


def summarize_final_table(data):
    if not data:
        return None
    entries = data.get("entries", [])
    by_tier = {}
    max_error = None
    max_error_entry = None
    for e in entries:
        tier = e.get("tier")
        by_tier[tier] = by_tier.get(tier, 0) + 1
        err_pct = e.get("error_pct")
        if err_pct is not None:
            if max_error is None or err_pct > max_error:
                max_error = err_pct
                max_error_entry = e
    return {
        "generated_at": data.get("generated_at"),
        "entry_count": len(entries),
        "by_tier": by_tier,
        "max_error_pct": max_error,
        "max_error_entry": max_error_entry,
    }


def build_markdown(summary: dict) -> str:
    lines = []
    lines.append("# Verification Digest")
    lines.append("")
    lines.append("Auto-generated summary of verification artifacts and baseline audits.")
    lines.append("")

    sage = summary.get("sage_incidence")
    if sage:
        lines.append("## Sage incidence + H1")
        lines.append("")
        lines.append(f"- Field: {sage.get('field')}")
        lines.append(f"- Group order: {sage.get('group_order')}")
        lines.append(f"- Structure: {sage.get('structure')}")
        lines.append(f"- Abelian: {sage.get('is_abelian')}")
        lines.append(f"- Solvable: {sage.get('is_solvable')}")
        lines.append(f"- Generators: {sage.get('num_generators')}")
        lines.append(f"- H1 dimension: {sage.get('h1_dim')}")
        lines.append(f"- H1 matrices: {sage.get('h1_num_matrices')}")
        lines.append("")

    final_table = summary.get("final_table")
    if final_table:
        lines.append("## Final summary table (computed)")
        lines.append("")
        lines.append(f"- Generated at: {final_table.get('generated_at')}")
        lines.append(f"- Entries: {final_table.get('entry_count')}")
        lines.append(f"- By tier: {final_table.get('by_tier')}")
        if final_table.get("max_error_entry"):
            me = final_table["max_error_entry"]
            lines.append(
                "- Max error: {:.2f}% ({})".format(
                    final_table.get("max_error_pct"), me.get("quantity")
                )
            )
        lines.append("")

    baseline = summary.get("baseline_audit")
    if baseline:
        lines.append("## Baseline audit (expression search)")
        lines.append("")
        lines.append(f"- Expressions evaluated: {baseline.get('num_exprs')}")
        lines.append(f"- Tolerances (%): {baseline.get('tolerances_pct')}")
        for name, t in (baseline.get("targets") or {}).items():
            hits = t.get("hits")
            if hits:
                lines.append(f"- {name} hits: {hits}")
        lines.append("")

    suite = summary.get("baseline_suite")
    if suite:
        lines.append("## Baseline suite (strict/medium)")
        lines.append("")
        for mode, payload in suite.items():
            lines.append(f"- {mode}: {payload.get('num_exprs')} expressions")
            targets = payload.get("targets", {})
            for name, t in targets.items():
                hits = t.get("hits")
                if hits:
                    lines.append(f"  - {name} hits: {hits}")
        lines.append("")

    verify = summary.get("verification_results")
    if verify:
        lines.append("## Repo verification results")
        lines.append("")
        lines.append(f"- Timestamp: {verify.get('timestamp')}")
        lines.append(f"- Verified count: {verify.get('verified_count')}")
        lines.append(f"- Failed count: {verify.get('failed_count')}")
        lines.append(f"- Verification rate: {verify.get('verification_rate')}")
        if verify.get("verified"):
            lines.append("- Verified sample:")
            for item in verify.get("verified")[:10]:
                lines.append(f"  - {item}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    summary = {
        "sage_incidence": summarize_sage_incidence(
            load_json(ROOT / "data" / "w33_sage_incidence_h1.json")
        ),
        "baseline_audit": summarize_baseline_audit(
            load_json(ROOT / "data" / "w33_baseline_audit_results.json")
        ),
        "baseline_suite": summarize_baseline_suite(
            load_json(ROOT / "data" / "w33_baseline_suite_results.json")
        ),
        "verification_results": summarize_verification_results(
            load_json(ROOT / "data" / "w33_verification_results.json")
        ),
        "final_table": summarize_final_table(
            load_json(ROOT / "artifacts" / "final_summary_table.json")
        ),
        "generated_at": "2026-01-26",
    }

    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text(build_markdown(summary), encoding="utf-8")
    OUT_JSON.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print(f"Wrote {OUT_MD}")
    print(f"Wrote {OUT_JSON}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
