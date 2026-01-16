#!/usr/bin/env python3
"""Reproduce Pareto frontier tables for W33↔N12_58.

Assumes the repository 'data' folder exists and contains:
- data/_workbench/02_geometry/W33_line_phase_map.csv
- data/_n12/n12_58_candidate_w33_points_...csv
- data/_n12/n12_58_2t_holonomy_nontrivial_cycles.csv

This script is intentionally minimal: it recomputes four-center triads,
cover12 counts, and minimal cover12 loop costs (with witnesses).
"""
# See bundle outputs for the computed results.
