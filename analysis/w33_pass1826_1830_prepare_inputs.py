#!/usr/bin/env python3
"""Prepare deterministic inputs for Passes 1828 and 1829 exact C++ workers."""
from __future__ import annotations
import sys
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
from w33_pass1801_1805_common import build_geometry

D = build_geometry()
K = np.asarray(D["K"], dtype=np.uint8)
columns = [tuple(map(int, np.flatnonzero(K[:, e]))) for e in range(240)]
assert all(len(c) == 3 for c in columns) and len(set(columns)) == 240

sig_path = ROOT / "data" / "w33_pass1829_syndromes240.txt"
sig_path.write_text("\n".join(str(sum(1 << i for i in c)) for c in columns) + "\n")

adj = [0] * 45
pair_masks = [[0] * 45 for _ in range(45)]
for a, b, c in columns:
    for x, y in ((a, b), (a, c), (b, c)):
        adj[x] |= 1 << y
        adj[y] |= 1 << x
    pair_masks[a][b] |= 1 << c; pair_masks[b][a] |= 1 << c
    pair_masks[a][c] |= 1 << b; pair_masks[c][a] |= 1 << b
    pair_masks[b][c] |= 1 << a; pair_masks[c][b] |= 1 << a
layer_path = ROOT / "data" / "w33_pass1828_hypergraph_input.txt"
with layer_path.open("w") as fh:
    fh.write("\n".join(map(str, adj)) + "\n")
    for row in pair_masks:
        fh.write(" ".join(map(str, row)) + "\n")
print(sig_path)
print(layer_path)
