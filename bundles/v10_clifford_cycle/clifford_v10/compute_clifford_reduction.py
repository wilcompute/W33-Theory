#!/usr/bin/env python3
"""Recompute the Clifford reduction of port words for the 5 nontrivial 2T cycles.

Reads:
- W33_N12_58_portlaw_rewrite_bundle_v7_20260112.zip
  -> cycle_witness_v3_holonomy_solver.csv

Writes:
- cycle_clifford_summary.csv
- cycle_step_ports_and_phases.csv
"""

import io
import math
import zipfile
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd

z7 = Path("/mnt/data/W33_N12_58_portlaw_rewrite_bundle_v7_20260112.zip")
with zipfile.ZipFile(z7, "r") as zf:
    wit = pd.read_csv(
        io.BytesIO(
            zf.read(
                "W33_N12_58_portlaw_rewrite_bundle_v7/cycle_witness_v3_holonomy_solver.csv"
            )
        )
    )


def cliff_mult(a_mask, a_sign, b_mask, b_sign):
    sign = a_sign * b_sign
    swaps = 0
    for j in range(3):
        if (b_mask >> j) & 1:
            swaps += bin(a_mask & ((1 << j) - 1)).count("1")
    if swaps % 2 == 1:
        sign *= -1
    return a_mask ^ b_mask, sign


def reduce_ports(ports):
    mask = 0
    sign = 1
    for p in ports:
        if p < 0:
            continue
        mask, sign = cliff_mult(mask, sign, 1 << p, 1)
    return mask, sign


def mask_to_str(mask):
    out = []
    for i in range(3):
        if (mask >> i) & 1:
            out.append(f"e{i}")
    return "1" if not out else "*".join(out)


rows = []
for c in sorted(wit.cycle_index.unique()):
    sub = wit[wit.cycle_index == c].sort_values("step")
    ports = sub.move_edge_matching_idx.tolist()
    moved = [p for p in ports if p != -1]
    mask, sign = reduce_ports(moved)
    rows.append(
        {
            "cycle_index": int(c),
            "length": int(len(sub)),
            "moves": int(len(moved)),
            "cliff_mask": int(mask),
            "cliff_element": ("-" if sign < 0 else "") + mask_to_str(mask),
        }
    )
pd.DataFrame(rows).to_csv("cycle_clifford_summary.csv", index=False)

# per-step export
step = []
for _, r in wit.iterrows():
    step.append(
        {
            "cycle_index": int(r.cycle_index),
            "step": int(r.step),
            "delta": int(r.delta),
            "rem_idx": int(r.rem_idx),
            "add_idx": int(r.add_idx),
            "move_port": int(r.move_edge_matching_idx),
            "triad_hol_mod12": int(r.triad_hol_mod12),
            "triad_phase": str(
                complex(np.exp(2j * math.pi * int(r.triad_hol_mod12) / 12))
            ),
        }
    )
pd.DataFrame(step).to_csv("cycle_step_ports_and_phases.csv", index=False)

print("Wrote cycle_clifford_summary.csv and cycle_step_ports_and_phases.csv")
