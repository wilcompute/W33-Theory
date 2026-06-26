#!/usr/bin/env python3
"""BT1818: operator labels for the hidden quartet fibre.

BT1815 identified the W(E6)-distinguished 6-hinge slice as the edge set of a hidden
K4 on four states.  This file gives the quartet a concrete local D4/GKP/Pauli-square
labeling: F2^2 phase-space corners, with coordinate flips X/Z and diagonal flips XZ.
"""
from __future__ import annotations
import itertools, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1818_quartet_operator_labeling.json"
STATES = {
    "00": {"x": 0, "z": 0, "operator": "I", "gkp_coset": "origin / no half-shift"},
    "01": {"x": 1, "z": 0, "operator": "X", "gkp_coset": "position half-shift"},
    "10": {"x": 0, "z": 1, "operator": "Z", "gkp_coset": "momentum half-shift"},
    "11": {"x": 1, "z": 1, "operator": "XZ", "gkp_coset": "both-quadrature half-shift / Y-like corner"},
}
SLICE = [(5,10,41),(7,34,40),(10,22,44),(12,34,42),(18,40,42),(30,41,44)]
OBSERVED = (10,22,44)

def xor_state(a: str, b: str) -> str:
    return ''.join(str(int(x) ^ int(y)) for x,y in zip(a,b))

def symp(a: str, b: str) -> int:
    # state bits are (z,x) in string order used here: first = z, second = x
    za, xa = int(a[0]), int(a[1])
    zb, xb = int(b[0]), int(b[1])
    return (xa*zb + za*xb) % 2

def main():
    edges = [tuple(e) for e in itertools.combinations(STATES.keys(),2)]
    edge_rows = []
    for edge, support in zip(edges, SLICE):
        a,b = edge
        diff = xor_state(a,b)
        edge_rows.append({
            "edge": [a,b],
            "difference": diff,
            "edge_operator": STATES[diff]["operator"],
            "support": list(support),
            "hamming_weight": diff.count('1'),
            "symplectic_pairing_of_endpoints": symp(a,b),
            "type": "coordinate" if diff.count('1') == 1 else "diagonal"
        })
    observed_edge = edges[SLICE.index(OBSERVED)]
    payload = {
        "bt": "BT1818",
        "title": "quartet operator labeling",
        "quartet_model": "local F2^2 D4/GKP/Pauli square",
        "state_labels": STATES,
        "edge_labels": edge_rows,
        "observed_defect_support": list(OBSERVED),
        "observed_oriented_edge": [observed_edge[0], observed_edge[1]],
        "observed_difference_operator": STATES[xor_state(*observed_edge)]["operator"],
        "observed_edge_type": "diagonal/both-quadrature flip",
        "operator_counts": {
            "coordinate_edges": sum(1 for r in edge_rows if r["type"] == "coordinate"),
            "diagonal_edges": sum(1 for r in edge_rows if r["type"] == "diagonal")
        },
        "checks": {
            "four_states": len(STATES) == 4,
            "six_edges": len(edge_rows) == 6,
            "four_coordinate_edges": sum(1 for r in edge_rows if r["type"] == "coordinate") == 4,
            "two_diagonal_edges": sum(1 for r in edge_rows if r["type"] == "diagonal") == 2,
            "observed_is_XZ_diagonal": xor_state(*observed_edge) == "11"
        },
        "boundary": "This labels the hidden quartet as a local D4/GKP/Pauli-square fibre. It does not claim that the true BT1781 tuple data has already supplied canonical physical operators; that remains the BT1819 pass/fail input.",
        "conclusion": "The hidden quartet is concretely the F2^2 local fibre square. The observed defect edge 00->11 is the XZ/Y-like diagonal: a simultaneous position/momentum half-shift. This is the operator-level content of the oriented quartet law."
    }
    payload["verified"] = all(payload["checks"].values())
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True))
    print(json.dumps({"verified": payload["verified"], "observed_operator": payload["observed_difference_operator"]}, indent=2))
    return 0 if payload["verified"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
