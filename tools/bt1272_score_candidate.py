#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

REQ = ["candidate_id", "closure_order", "word_diameter", "edge_split", "diameter_endpoint_first_set_histogram", "labelled_channel_spread"]
ORDER = ["closure51840", "diameter14", "polar_path_P4P4", "unique_all_channel_endpoint", "labelled_nonzero_spread"]


def score(c):
    missing = [k for k in REQ if k not in c]
    if missing:
        return {"candidate_id": c.get("candidate_id", "missing"), "schema_ok": False, "band": "fail", "missing_fields": missing}
    e = c["edge_split"]
    h = c["diameter_endpoint_first_set_histogram"]
    g = {
        "closure51840": c["closure_order"] == 51840,
        "diameter14": c["word_diameter"] == 14,
        "polar_path_P4P4": e.get("polar_graph") == "P4" and e.get("nonpolar_graph") == "P4",
        "unique_all_channel_endpoint": h == {"8": 1},
        "labelled_nonzero_spread": c["labelled_channel_spread"] > 0,
    }
    miss = [x for x in ORDER if not g[x]]
    s = len(ORDER) - len(miss)
    band = "pass" if s == 5 else ("review" if g["closure51840"] and s >= 2 else "fail")
    return {"candidate_id": c["candidate_id"], "schema_ok": True, "band": band, "score": s, "missing_gates": miss, "gates": g}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("candidate", type=Path)
    ap.add_argument("--out", type=Path)
    ns = ap.parse_args()
    result = score(json.loads(ns.candidate.read_text(encoding="utf-8")))
    text = json.dumps(result, indent=2) + "\n"
    if ns.out:
        ns.out.parent.mkdir(parents=True, exist_ok=True)
        ns.out.write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()
