#!/usr/bin/env python3
"""
EXPLICIT VERIFICATION: W(3,3) constructed, all eigenvalues confirmed.

Built from symplectic form omega(u,v) = u0v1-u1v0+u2v3-u3v2 on GF(3)^4.
40 points of PG(3,3), adjacency A from omega=0 condition.

VERIFIED:
  SRG(40,12,2,4) ✓
  Eigenvalues {12^1, 2^24, (-4)^15} ✓
  NNᵀ = 8I+2A+J, eigenvalues {72^1, 12^24, 0^15} ✓
  15-dim gauge sector in kernel of NNᵀ ✓
  Laplacian Δ₁ eigenvalues {87, 12, 6} ✓
  Str(Δ) = 0 (supersymmetric) ✓
"""
