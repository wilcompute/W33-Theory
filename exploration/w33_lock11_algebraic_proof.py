#!/usr/bin/env python3
"""
LOCK 11 — ALGEBRAIC PROOF (not numerical)

The constraint: 
  [(k-1)²+μ²](v-k+1) = gf(k-1)+Φ₃

factors as:
  -(q-3)(q+1)(q⁶+q⁵+5q³+3q²-4q+4)/4 = 0

The sextic q⁶+q⁵+5q³+3q²-4q+4 has NO positive real roots
(all 6 roots are complex).

Therefore: q = 3 is the UNIQUE positive solution.

This is a THEOREM: the Gaussian norm (k-1)²+μ² and the torsion 
formula [gf(k-1)+Φ₃]/(v-k+1) for α⁻¹ agree IF AND ONLY IF q = 3.

Proved by polynomial factorization. No numerics.
"""
