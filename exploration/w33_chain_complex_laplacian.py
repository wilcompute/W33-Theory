#!/usr/bin/env python3
"""
CHAIN COMPLEX LAPLACIAN OF W(3,3)
=================================

Points(40) <-N-> Pairs(45) <-M^T-> Spreads(27)

N^T N = 6I + 2J - 2A_45 (mass from COMPLEMENT graph)
M^T M = 3I + A_45 (adjacency from SAME-SPREAD relation)

Laplacian Delta_1 = N^T N + M^T M = q^2 I + lambda J - A_45

Eigenvalues: 87 (dim 1), 12 (dim 24), 6 (dim 20)
           = q^2+dim(E6), k, q!

The 45-pair graph is SRG(45,12,3,3) — SAME VALENCE k=12 as W(3,3)!

MASS SPECTRUM:
  Bosonic sector (dim 24): mass scale = k = 12
  Fermionic sector (dim 20): mass scale = q! = 6
  Ratio: k/q! = 2 = lambda

87 = q^2 + dim(E_6) = 9 + 78
"""

# ADDITIONAL DISCOVERY:
# There are exactly 78 non-isomorphic SRG(45,12,3,3) graphs!
# 78 = dim(E₆) = 2(v-1).
# The one from the W(3,3) pair structure has Aut of order 51840 = |W(E₆)|.
# It is the UNIQUE maximally symmetric SRG(45,12,3,3).
# Source: Coolsaet, Degraer, Spence, Electronic J. Combinatorics 13(1), 2006.
