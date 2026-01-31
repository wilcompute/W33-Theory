#!/usr/bin/env python3
"""Generate a predictions comparison report and write artifacts/predictions_report.json and .md
This script is CI-friendly and always exits 0 (it reports pass/fail per-item)."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PRED = ROOT / "data" / "predictions.json"
REF = ROOT / "tests" / "reference_values.json"
OUT_DIR = ROOT / "artifacts"
OUT_DIR.mkdir(exist_ok=True)
OUT_JSON = OUT_DIR / "predictions_report.json"
OUT_MD = OUT_DIR / "predictions_report.md"


def load_json(p):
    with open(p, "r", encoding="utf-8") as fh:
        return json.load(fh)


def main():
    predictions = load_json(PRED)
    references = load_json(REF)

    items = {}
    passed = 0
    total = 0

    for key, v in predictions.items():
        total += 1
        pred = float(v["value"])
        pred_tol = float(v.get("tolerance", 0))
        ref = float(references.get(key, {}).get("value", float("nan")))
        ref_unc = float(references.get(key, {}).get("uncertainty", 0))
        allowed = max(pred_tol, 3 * ref_unc)
        diff = abs(pred - ref) if not (ref != ref) else None
        ok = (diff is not None) and (diff <= allowed)
        if ok:
            passed += 1
        items[key] = {
            "pred": pred,
            "pred_tol": pred_tol,
            "ref": ref,
            "ref_unc": ref_unc,
            "allowed": allowed,
            "diff": diff,
            "pass": bool(ok),
        }

    report = {
        "summary": {"total": total, "passed": passed, "failed": total - passed},
        "items": items,
    }

    with open(OUT_JSON, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2, default=str)

    # Write a small Markdown summary
    lines = []
    lines.append(f"# Predictions Report\n\n")
    lines.append(f"**Passed: {passed}/{total}**\n\n")
    lines.append(
        "| Key | Prediction | Reference | Δ | Allowed | Result |\n|---|---:|---:|---:|---:|---:|\n"
    )
    for k, it in items.items():
        pred = it["pred"]
        ref = it["ref"]
        diff = it["diff"]
        allowed = it["allowed"]
        res = "✅" if it["pass"] else "❌"
        lines.append(f"| {k} | {pred} | {ref} | {diff} | {allowed} | {res} |\n")

    with open(OUT_MD, "w", encoding="utf-8") as fh:
        fh.writelines(lines)

    # Merge this report into a verification digest for easier human consumption
    try:
        from datetime import datetime

        digest_path = OUT_DIR / "verification_digest.json"
        digest_md = OUT_DIR / "verification_digest.md"
        ts = datetime.utcnow().isoformat() + "Z"

        # load or create digest
        digest = {"reports": {}}
        if digest_path.exists():
            with open(digest_path, "r", encoding="utf-8") as fh:
                try:
                    digest = json.load(fh)
                except Exception:
                    digest = {"reports": {}}

        digest["reports"]["predictions"] = {
            "timestamp": ts,
            "summary": report["summary"],
            "items": report["items"],
        }

        with open(digest_path, "w", encoding="utf-8") as fh:
            json.dump(digest, fh, indent=2, default=str)

        # Update a simple markdown digest (append or create)
        md_lines = []
        md_lines.append(f"# Verification Digest\n\n")
        md_lines.append(f"## Predictions (updated {ts})\n\n")
        md_lines.append(f"**Passed: {passed}/{total}**\n\n")
        md_lines.append(
            "| Key | Prediction | Reference | Δ | Allowed | Result |\n|---|---:|---:|---:|---:|---:|\n"
        )
        for k, it in items.items():
            md_lines.append(
                f"| {k} | {it['pred']} | {it['ref']} | {it['diff']} | {it['allowed']} | {'✅' if it['pass'] else '❌'} |\n"
            )

        with open(digest_md, "w", encoding="utf-8") as fh:
            fh.writelines(md_lines)

    except Exception as e:
        print(f"Warning: failed to update verification digest: {e}")

    print(f"Wrote {OUT_JSON} and {OUT_MD}. {passed}/{total} passed.")


if __name__ == "__main__":
    main()
