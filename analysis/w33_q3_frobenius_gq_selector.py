#!/usr/bin/env python3
"""q=3 selector: Frobenius count equals GQ(q,q) edge count."""
from __future__ import annotations

import json
from pathlib import Path


def gq_points(q: int) -> int:
    return (q + 1) * (q * q + 1)


def gq_degree(q: int) -> int:
    return q * (q + 1)


def gq_edges(q: int) -> int:
    return gq_points(q) * gq_degree(q) // 2


def frob(q: int) -> int:
    return q**5 - q


def build_payload() -> dict:
    tested = [1, 2, 3, 4, 5, 7, 11]
    rows = [{"q": n, "frobenius": frob(n), "gq_edges": gq_edges(n), "match": frob(n) == gq_edges(n)} for n in tested]
    matches = [r["q"] for r in rows if r["match"]]
    identities = {
        "only_q3_matches_tested_values": matches == [3],
        "q3_frobenius_is_240": frob(3) == 240,
        "q3_gq_edges_is_240": gq_edges(3) == 240,
        "q3_points_degree_edges": (gq_points(3), gq_degree(3), gq_edges(3)) == (40, 12, 240),
    }
    return {
        "theorem": "q3_frobenius_gq_selector",
        "equation": "q^5 - q = q(q+1)^2(q^2+1)/2",
        "symbolic_reduction": "for q>0, cancel q(q+1)(q^2+1), giving 2(q-1)=q+1, hence q=3",
        "selection_table": rows,
        "identities": identities,
        "all_identities_hold": all(identities.values()),
    }


def main() -> None:
    payload = build_payload()
    out = Path("data/w33_q3_frobenius_gq_selector.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
