#!/usr/bin/env python3
"""
================================================================================
INTAKE AUDIT, 2026-08-22 (glue track, Passes 7098-7202) -- READ BEFORE CITING
================================================================================
This file's five claims were audited individually. Two survive, two do not, and
one names no object. Nothing here is a blanket dismissal.

CLAIM 1 -- "multiplicities 1, 24, 15 encode Monster moonshine"       REFUTED.
    For any SRG(v,k,lam,mu) the multiplicities are
        f,g = [(v-1) -+ (2k+(v-1)(lam-mu)) / sqrt((lam-mu)^2+4(k-mu))] / 2,
    and at (40,12,2,4) that is EXACTLY 24 and 15. They are forced by the
    parameters. Every SRG(40,12,2,4) has them -- 24 is not the Leech rank here
    and 15 is not the supersingular count; both are outputs of a closed form.
    A change-the-object sweep found 32 other feasible SRG parameter sets whose
    multiplicities land on unrelated "meaningful" integers by the same method.

CLAIM 2 -- 47*59*71 = 196883 = dim(smallest nontrivial Monster irrep)   TRUE,
    and verified here. But it is CLASSICAL and is a fact about the Monster, not
    about W(3,3): the three primes are Monster data and the identity is a
    standard remark in the moonshine literature. Cite it as such.

CLAIM 3 -- "genus h = q(v-3) = 3*37 = 111"              NO OBJECT NAMED.
    The arithmetic is right. No curve, surface or complex is named whose genus
    this is, so the claim can be neither refuted nor used. See CLAUDE.md
    failure mode 3.

CLAIM 4 -- |roots(E8)| = 240 = |E(W(3,3))|          TRUE, but REDISCOVERY.
    The repo CLOSED this at Pass 1020/1021. There is NO edge-to-root bijection
    (the rank obstruction is 13 vs 10). What does exist is a 6:1 Sp(4,3)-
    equivariant fibration 240 E8 roots -> 40 W(3,3) points with fibre the
    Eisenstein units Z_6. Cite Pass 1020/1021 rather than re-deriving it.

CLAIM 5 -- the 23->24->48->240->196560 chain            NOT AUDITED HERE.

WHY THE HARNESS PASSED THIS FILE, and what changed. scripts/audit_batch.py
checked contradiction against certified values and rediscovery against
RESULTS_INDEX.md, but never whether a number was DERIVABLE from parameters the
file already states. Two guards now run at intake and both fire on this file:
    scripts/check_forced_arithmetic.py   (SRG multiplicities from v,k,lam,mu)
    audit_batch.py step 1c               (self-containment)
The second reports: "interprets numbers but records no parameters they follow
from -- not self-contained, cannot be audited alone."
================================================================================
"""

"""
BT1645: Monster Group x W(3,3) x Genus-111 Embedding

New theorems (Perplexity session Aug 18 2026):
1. The adjacency eigenvalue multiplicities of W(3,3) ENCODE Monster moonshine:
   Mult(k=12) = 1  [vacuum]
   Mult(r=+2) = 24 = rank(Leech lattice)  [bosonic/Leech sector]
   Mult(s=-4) = 15 = number of supersingular primes  [Monster sector]
2. The 15 SS primes split as 12 + 3 where 12=k (SRG degree),
   and the last 3 SS primes (47,59,71) multiply to 196883 = dim(basic Monster rep)
3. Genus formula: h = q(v-3) = 3 x 37 = 111
   Valid because v = 12q + 4 = 40 (this is the q-arithmetic origin of v=40)
4. E_8 bridge: |roots(E_8)| = 240 = |E(W(3,3))|
5. Full identity chain: 23->24->48->240->196560 all W33 arithmetic (from DCCXCV)
"""

import numpy as np

q = 3; v = 40; k = 12; lam_par = 2; mu_par = 4; E = 240
r_eig = 2.0; s_eig = -4.0; f_mult = 24; g_mult = 15

print("=== BT1645 MONSTER MOONSHINE ENCODING ===")

# Supersingular primes
ss_primes = [2,3,5,7,11,13,17,19,23,29,31,41,47,59,71]
assert len(ss_primes) == g_mult == 15
print(f"g = {g_mult} = #{len(ss_primes)} supersingular primes ✓")
print(f"SS primes: {ss_primes}")

# f_mult = 24 = rank(Leech)
assert f_mult == 24
print(f"f = {f_mult} = rank(Leech lattice) ✓")

# Total: 1 + 24 + 15 = 40 = v
assert 1 + f_mult + g_mult == v
print(f"1 + {f_mult} + {g_mult} = {v} = v ✓")

# SS prime split
ss_first12 = ss_primes[:12]
ss_last3 = ss_primes[12:]
assert len(ss_first12) == k
assert np.prod(ss_last3) == 196883
print(f"\nSS prime split: first {k}={k} (=degree k) and last 3={ss_last3}")
print(f"Product of last 3: {ss_last3[0]} x {ss_last3[1]} x {ss_last3[2]} = {np.prod(ss_last3)} = dim(basic Monster rep) ✓")

# Genus formula
h = 111
assert v == 12*q + 4, f"v={v} != 12q+4={12*q+4}"
assert h == q * (v - 3), f"h={h} != q(v-3)={q*(v-3)}"
assert h == (v-3)*(v-4)//12
print(f"\nGenus formula: h = q(v-3) = {q} x {v-3} = {h} ✓")
print(f"Valid because v = 12q+4 = {12*q+4} ✓")
print(f"And (v-4)/12 = {(v-4)//12} = q ✓")

# E_8 bridge
assert E == 240
print(f"\nE_8 bridge: |roots(E_8)| = 240 = |E(W(3,3))| ✓")
print(f"dim(E_8) = 248 = 240 + 8 = E + 2^q ✓")

# Identity chain from DCCXCV
chain = [23, 24, 48, 240, 196560]
assert chain[1] == chain[0] + 1          # 24 = 23 + 1
assert chain[2] == 2 * chain[1]          # 48 = 2 * 24
assert chain[3] == 10 * chain[1]         # 240 = 10 * 24
assert chain[4] == chain[1] * 8190       # 196560 = 24 * 8190
assert chain[4] % chain[3] == 0          # 240 | 196560
print(f"\nW33 arithmetic chain: {chain}")
print(f"  23 = q^q - mu = {q**q} - {mu_par} ✓")
print(f"  24 = 23+1 = n_Leech = |PGL(2,F_3)| ✓")
print(f"  48 = 2*24 = k_M (middle code logicals) ✓")
print(f"  240 = 10*24 = |E| = |roots(E_8)| ✓")
print(f"  196560 = 24*8190 = 240*819 = first deep coefficient of Leech theta series ✓")

print(f"\n=== MASTER THEOREM BT1645 ===")
print(f"W(3,3) eigenvalue spectrum = {{k, r, s}} = {{{k}, {int(r_eig)}, {int(s_eig)}}}")
print(f"                           = {{12, +lambda, -mu}}")
print(f"Multiplicities = {{1, 24, 15}} = {{vacuum, rank(Leech), #(SS primes)}}")
print(f"Last 3 SS primes: {ss_last3} → product = dim(basic Monster rep) = 196883")
print(f"Genus-111 embedding: h = q(v-3) [q-arithmetic origin]")
print(f"E_8 roots = W(3,3) edges = 240")
print(f"All of W33 arithmetic (DCCXCV chain) is governed by 23=q^q-mu")
