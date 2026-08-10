#!/usr/bin/env python3
"""Summarize `artifacts/pysat_cryptosat_sweep_summary.json` into a concise report.
Writes:
  - artifacts/pysat_cryptosat_sweep_summary_report.json
  - artifacts/pysat_cryptosat_sweep_summary_report.md
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts"
IN = ART / "pysat_cryptosat_sweep_summary.json"
OUT_JSON = ART / "pysat_cryptosat_sweep_summary_report.json"
OUT_MD = ART / "pysat_cryptosat_sweep_summary_report.md"


def summarize():
    if not IN.exists():
        print("Missing summary input:", IN)
        return 1
    data = json.loads(IN.read_text(encoding="utf-8"))
    report = []
    issues = []
    for entry in data:
        w = entry.get("W_idx")
        xor = entry.get("xor_run", {})
        cnf = entry.get("cnf_only_run", {})
        xor_art = xor.get("artifact") if xor else None
        cnf_art = cnf.get("artifact") if cnf else None
        xor_sat = None if xor_art is None else xor_art.get("sat")
        xor_valid = None if xor_art is None else xor_art.get("valid")
        cnf_sat = None if cnf_art is None else cnf_art.get("sat")
        cnf_valid = None if cnf_art is None else cnf_art.get("valid")
        entry_report = {
            "W_idx": w,
            "xor_returncode": xor.get("returncode"),
            "xor_elapsed": xor.get("elapsed"),
            "xor_sat": xor_sat,
            "xor_valid": xor_valid,
            "cnf_returncode": cnf.get("returncode"),
            "cnf_elapsed": cnf.get("elapsed"),
            "cnf_sat": cnf_sat,
            "cnf_valid": cnf_valid,
            "cnf_sign_unsat_cores": cnf.get("sign_unsat_cores"),
        }
        report.append(entry_report)
        # detect tune-worthy differences
        if xor_valid is True and cnf_valid is False:
            issues.append((w, "XOR valid but CNF indicates sign unsat core"))
        if xor_valid is False and cnf_valid is True:
            issues.append((w, "CNF valid but XOR run did not find valid signs"))
    OUT_JSON.write_text(
        json.dumps({"report": report, "issues": issues}, indent=2), encoding="utf-8"
    )

    # write a short markdown
    lines = []
    lines.append("# PySAT+CryptoMiniSat XOR sweep summary")
    lines.append("")
    lines.append("| W | XOR sat | XOR valid | CNF sat | CNF valid | Note |")
    lines.append("|---:|:---:|:---:|:---:|:---:|:---|")
    for r in report:
        note = ""
        if r["W_idx"] in [x[0] for x in issues]:
            note = "; ".join([i[1] for i in issues if i[0] == r["W_idx"]])
        lines.append(
            f"| {r['W_idx']} | {r['xor_sat']} | {r['xor_valid']} | {r['cnf_sat']} | {r['cnf_valid']} | {note} |"
        )
    if issues:
        lines.append("")
        lines.append("## Issues of interest")
        for w, msg in issues:
            lines.append(f"- W={w}: {msg}")

    OUT_MD.write_text("\n".join(lines, encoding="utf-8"), encoding="utf-8")
    print("Wrote", OUT_JSON, "and", OUT_MD)
    return 0


if __name__ == "__main__":
    raise SystemExit(summarize())
