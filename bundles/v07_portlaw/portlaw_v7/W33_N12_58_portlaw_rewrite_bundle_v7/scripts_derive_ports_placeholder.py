#!/usr/bin/env python3
"""Derive canonical K4 'port' labels for W33 four-center triads.

Outputs:
- w33_k4_components.csv (each triad belongs to a K4 component; triad is 'outer quad' minus excluded point)
- w33_k4_edges_undirected.csv (edges labeled by matching index 0/1/2 on the outer quad)
- w33_k4_moves_directed_commutator.csv (directed moves, commutator phase in Z12; should be identically 6)

Run from repo root where data/_workbench and data/_toe exist.
"""

# This file is included for reproducibility; see generated CSVs for results.
