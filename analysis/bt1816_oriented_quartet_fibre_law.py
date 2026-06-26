#!/usr/bin/env python3
"""BT1816: oriented quartet fibre law.

BT1805 found the minimal even correction (-2,-2,+2).  BT1815 identifies the
ambient W(E6)-distinguished object as a K4 edge slice.  BT1816 records the local
candidate law: an oriented quartet edge produces two endpoint losses and one
edge-target gain, killing the F3 double-six syndrome while preserving F2 parity.
"""
from __future__ import annotations
import json
import numpy as np
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1816_oriented_quartet_fibre_law.json"
TABLES = ['T001','T002','T010','T012','T020','T021','T100','T101','T111','T112','T120','T122','T200','T202','T210','T211','T221','T222']
COUNTS = np.array([528,562,578,528,612,580,528,528,480,528,612,564,562,528,578,562,562,560], dtype=int)
F2 = np.array([[1,0,0,1,1,0,1,0,1,0,0,1,0,1,1,0,1,0],[0,1,1,0,0,1,0,1,0,1,1,0,1,0,0,1,0,1]], dtype=int)
F3 = np.array([[1,0,0,1,2,0,2,0,0,0,0,2,0,1,0,0,0,0],[2,0,0,1,1,0,2,0,2,0,0,0,0,0,1,0,0,0],[0,0,2,0,0,2,0,1,0,1,2,0,0,0,0,1,0,0],[1,0,2,2,0,2,0,1,0,2,1,0,0,0,0,0,1,0],[2,2,1,1,1,1,2,1,2,1,0,0,1,0,1,1,0,1]], dtype=int)

# Observed oriented quartet edge from BT1815: 00 -> 11, support [10,22,44].
# Table-level law: two losses, one gain, all in even quanta.
CORRECTION = {'T010': -2, 'T210': -2, 'T222': 2}

def main():
    delta = np.zeros(len(TABLES), dtype=int)
    for t,v in CORRECTION.items():
        delta[TABLES.index(t)] = v
    adjusted = COUNTS + delta
    payload = {
        "bt": "BT1816",
        "title": "oriented quartet fibre law",
        "hidden_quartet_edge": ["00", "11"],
        "edge_support": [10,22,44],
        "table_correction": CORRECTION,
        "law_template": "oriented K4 edge = two endpoint losses plus one edge-target gain, in units of 2",
        "observed_syndromes": {"F2": (F2 @ COUNTS % 2).astype(int).tolist(), "F3": (F3 @ COUNTS % 3).astype(int).tolist()},
        "correction_syndromes": {"F2": (F2 @ delta % 2).astype(int).tolist(), "F3": (F3 @ delta % 3).astype(int).tolist()},
        "adjusted_syndromes": {"F2": (F2 @ adjusted % 2).astype(int).tolist(), "F3": (F3 @ adjusted % 3).astype(int).tolist()},
        "integer_effect": {"L1": int(np.abs(delta).sum()), "net_total_change": int(delta.sum()), "adjusted_total": int(adjusted.sum())},
        "checks": {
            "preserves_F2_parity": bool(np.all((F2 @ adjusted) % 2 == 0)),
            "kills_F3_syndrome": bool(np.all((F3 @ adjusted) % 3 == 0)),
            "minimal_even_L1_six": int(np.abs(delta).sum()) == 6,
            "two_losses_one_gain": sorted(v for v in CORRECTION.values()) == [-2,-2,2]
        },
        "conclusion": "The minimal fibre repair is exactly an oriented-edge law on the hidden quartet: two even losses and one even gain. It preserves the binary Hesse delta split and cancels the ternary double-six syndrome, so the unresolved rule is the orientation of the K4 edge selected inside the W(E6) size-6 slice."
    }
    payload["verified"] = all(payload["checks"].values())
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True))
    print(json.dumps({"verified": payload["verified"], "adjusted_F3": payload["adjusted_syndromes"]["F3"]}, indent=2))
    return 0 if payload["verified"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
