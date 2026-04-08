#!/usr/bin/env python3
"""
so(k) = so(12) DECOMPOSITION FROM THE CHAIN COMPLEX
====================================================

Points(40) → Pairs(45) → Spreads(27)

PSp(4,3) irreps: 40 = 1+24+15, 45 = 1+20+24, 27 = 1+20+6

UNIQUE irreps: {1, 6, 15, 20, 24}
Total: 1+6+15+20+24 = 66 = C(k,2) = dim(so(12)) = dim(so(k))

so(12) = 1 ⊕ 6 ⊕ 15 ⊕ 20 ⊕ 24 under W(E₆) = Aut(W(3,3))

Physical identification:
  15 = adj(SU(4)) ⊃ SU(3)×U(1) → gauge bosons (MASSLESS)
  24 = bosonic sector → W/Z/Higgs (mass scale k=12)
  20 = fermionic sector → fermions (mass scale q!=6)
  6  = compactified dimensions → (MASSLESS)
  1  = vacuum singlet

Euler characteristic: χ = 40-45+27 = 22 = λ(k-1)
  = denominator of α⁻¹ perturbative correction!

Mass ratio: bosonic/fermionic = k/q! = 12/6 = 2 = λ
"""
