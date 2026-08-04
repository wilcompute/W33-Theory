#!/usr/bin/env python3
"""Pass 3143: machine-auditable intake for parallel Pass 3125 rank-three candidates.

No input is typed as NO_INPUTS_DISCOVERED, never as a no-go result.  Every discovered
candidate is passed through the independent Pass 3134 certifier.  Malformed inputs fail
closed and cause a non-zero exit after the audit file is written.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = DATA / "PART_BT3143_RANK3_CANDIDATE_INTAKE_results.json"
CERTIFIER = ROOT / "analysis" / "bt3134_rank3_code_certifier.py"


def load_certifier():
    spec = importlib.util.spec_from_file_location("bt3134_certifier", CERTIFIER)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load Pass 3134 certifier")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def candidate_files():
    hits = []
    for path in DATA.glob("*.json"):
        name = path.name.lower()
        if "bt3125" in name and "rank3" in name and "candidate" in name:
            hits.append(path)
    return sorted(hits)


def main():
    files = candidate_files()
    certifier = load_certifier()
    audits = []
    malformed = 0
    accepted = 0
    total = 0
    for path in files:
        row = {"source": str(path.relative_to(ROOT)), "results": []}
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
            candidates = payload.get("candidates", [])
            if not isinstance(candidates, list):
                raise ValueError("top-level candidates must be a list")
            for candidate in candidates:
                result = certifier.certify(candidate)
                row["results"].append(result)
                accepted += int(result.get("accepted", False))
                total += 1
            row["candidate_count"] = len(candidates)
            row["accepted_count"] = sum(r.get("accepted", False) for r in row["results"])
        except Exception as exc:  # fail closed, but preserve the audit record
            malformed += 1
            row["error"] = f"{type(exc).__name__}: {exc}"
        audits.append(row)

    status = "NO_INPUTS_DISCOVERED" if not files else (
        "MALFORMED_INPUT_FAIL_CLOSED" if malformed else (
            "ACCEPTED_CANDIDATES_PRESENT" if accepted else "ALL_DISCOVERED_CANDIDATES_REJECTED"
        )
    )
    out = {
        "schema": "w33.pass3143.rank3_candidate_intake.v1",
        "status": status,
        "source_file_count": len(files),
        "candidate_count": total,
        "accepted_count": accepted,
        "malformed_source_count": malformed,
        "audits": audits,
        "boundary": "absence or rejection of discovered candidates is not a no-go theorem; only an accepted independently certified candidate may be promoted",
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=2, sort_keys=True))
    if malformed:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
