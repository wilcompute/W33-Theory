#!/usr/bin/env sage
"""
W33 is NOT a generalized quadrangle, but has the same parameters.
What kind of incidence structure is it?

With 4 common neighbors for non-collinear pairs, this suggests
a highly connected structure. Let's explore more deeply.
"""

from sage.all import *
import json
import numpy as np

with open("claude_workspace/data/w33_sage_incidence_h1.json") as f:
    data = json.load(f)

# Load W33 lines
from lib.w33_io import W33DataPaths, load_w33_lines
from pathlib import Path
import sys

here = Path('.').resolve()
sys.path.insert(0, str(here / 'claude_workspace'))

paths = W33DataPaths.from_this_file(str(here / 'claude_workspace' / 'w33_sage_incidence_and_h1.py'))
lines = load_w33_lines(paths)

n_points = 40
n_lines = 40

print("=== Deep Dive into W33 Incidence Structure ===")
print()

# Build incidence matrix
incidence = np.zeros((n_points, n_lines), dtype=int)
for line_idx, pts in enumerate(lines):
    for p in pts:
        incidence[p, line_idx] = 1

print(f"Incidence matrix shape: {incidence.shape}")
print(f"Total incidences: {np.sum(incidence)} = 40 lines × 4 points = {40*4}")

# Collinearity matrix: C[i,j] = number of common lines through i and j
collinearity = incidence @ incidence.T
print()
print("Collinearity matrix (# common lines between points):")
diag = np.diag(collinearity)
off_diag = collinearity - np.diag(diag)
print(f"  Diagonal entries (lines per point): {set(diag)}")
print(f"  Off-diagonal entries: {set(off_diag.flatten())}")

# Two points are collinear iff they share at least one line
collinear_pairs = np.sum(off_diag > 0) // 2
non_collinear_pairs = n_points * (n_points - 1) // 2 - collinear_pairs
print(f"  Collinear pairs: {collinear_pairs}")
print(f"  Non-collinear pairs: {non_collinear_pairs}")

# Distribution of collinearity values
from collections import Counter
off_diag_vals = [off_diag[i,j] for i in range(n_points) for j in range(i+1, n_points)]
print(f"  Value distribution: {Counter(off_diag_vals)}")

# Line concurrence matrix: L[i,j] = number of common points on lines i and j
concurrence = incidence.T @ incidence
print()
print("Line concurrence matrix (# common points between lines):")
diag_l = np.diag(concurrence)
off_diag_l = concurrence - np.diag(diag_l)
print(f"  Diagonal entries (points per line): {set(diag_l)}")
print(f"  Off-diagonal entries: {set(off_diag_l.flatten())}")

off_diag_l_vals = [off_diag_l[i,j] for i in range(n_lines) for j in range(i+1, n_lines)]
print(f"  Value distribution: {Counter(off_diag_l_vals)}")

# This is interesting! Let's look at the eigenvalues of these matrices
print()
print("=== Spectral Analysis ===")

# Eigenvalues of collinearity matrix
eig_col = np.linalg.eigvalsh(collinearity)
eig_col_rounded = [round(e, 4) for e in sorted(eig_col, reverse=True)]
print(f"Collinearity matrix eigenvalues: {Counter(eig_col_rounded)}")

# The point graph (collinearity graph) has adjacency matrix where
# A[i,j] = 1 if points are collinear
point_graph_adj = (off_diag > 0).astype(int)
eig_point = np.linalg.eigvalsh(point_graph_adj)
eig_point_rounded = [round(e, 2) for e in sorted(eig_point, reverse=True)]
print(f"Point graph eigenvalues: {Counter(eig_point_rounded)}")

# Check if strongly regular
print()
print("=== Checking if Point Graph is Strongly Regular ===")

# SRG parameters: (v, k, λ, μ)
# v = number of vertices
# k = degree (each vertex has k neighbors)
# λ = each pair of adjacent vertices has λ common neighbors
# μ = each pair of non-adjacent vertices has μ common neighbors

v = n_points
k = np.sum(point_graph_adj[0])  # degree of vertex 0

# Compute λ and μ
lambda_vals = []
mu_vals = []
for i in range(n_points):
    for j in range(i+1, n_points):
        common = np.sum(point_graph_adj[i] * point_graph_adj[j])
        if point_graph_adj[i,j] == 1:
            lambda_vals.append(common)
        else:
            mu_vals.append(common)

lambda_set = set(lambda_vals)
mu_set = set(mu_vals)

print(f"v = {v}, k = {k}")
print(f"λ (common neighbors of adjacent pairs): {lambda_set}")
print(f"μ (common neighbors of non-adjacent pairs): {mu_set}")

if len(lambda_set) == 1 and len(mu_set) == 1:
    lam = list(lambda_set)[0]
    mu = list(mu_set)[0]
    print(f"\n★ Point graph is Strongly Regular Graph SRG({v}, {k}, {lam}, {mu}) ★")
    
    # Check eigenvalues formula for SRG
    # Eigenvalues are: k (with mult 1), and two others r, s
    # r + s = λ - μ
    # rs = μ - k
    print(f"\nSRG eigenvalue check:")
    print(f"  λ - μ = {lam - mu}")
    print(f"  μ - k = {mu - k}")
    
    # The eigenvalues r, s satisfy x^2 - (λ-μ)x + (μ-k) = 0
    disc = (lam - mu)**2 - 4*(mu - k)
    print(f"  Discriminant = {disc}")
    if disc >= 0:
        r = ((lam - mu) + np.sqrt(disc)) / 2
        s = ((lam - mu) - np.sqrt(disc)) / 2
        print(f"  Eigenvalues r = {r}, s = {s}")

# Let's see what famous SRG this might be
print()
print("=== Identifying the SRG ===")
print("Known SRGs with v=40:")
print("  - Paley graph P(41) has v=40... no wait, that's 41")
print("  - Symplectic graph Sp(4,3)...")

# Check block design properties
print()
print("=== Block Design Analysis ===")
# W33 as a design: 40 points, 40 blocks (lines), each block has 4 points
# Each point is in 4 blocks
# What about λ (pairs covered)?

# Count how many lines contain each pair
pair_coverage = {}
for line_idx, pts in enumerate(lines):
    pts_list = sorted(pts)
    for i in range(len(pts_list)):
        for j in range(i+1, len(pts_list)):
            pair = (pts_list[i], pts_list[j])
            pair_coverage[pair] = pair_coverage.get(pair, 0) + 1

print(f"Pair coverage distribution: {Counter(pair_coverage.values())}")
lambda_design = list(set(pair_coverage.values()))
if len(lambda_design) == 1:
    print(f"W33 is a 2-({n_points}, 4, {lambda_design[0]}) design")

# The complement
print()
print("=== Complement Analysis ===")
# Non-collinear pairs
non_collinear = [(i,j) for i in range(n_points) for j in range(i+1, n_points) if off_diag[i,j] == 0]
print(f"Number of non-collinear pairs: {len(non_collinear)}")
print(f"Expected for GQ(3,3): Each point has 4×3=12 collinear points, so 40-1-12=27 non-collinear")
print(f"Per point: {len(non_collinear) * 2 / n_points} non-collinear points")
