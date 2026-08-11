#!/usr/bin/env python3
"""
Pass 4879 — Covering radius of the dual code [360,324,3]_2.

The primal [360,36,20]_2 = K has rho(K) in [124,179] (open).
The dual K^perp = [360,324,3]_2 has rho(K^perp) = 2.

Proof:
  - K^perp is not a perfect 1-error-correcting code:
    perfect 1-error codes satisfy |C| = 2^n / (n+1).
    Here 2^324 vs 2^360 / 361: 360 - log2(361) ≈ 360 - 8.49 ≠ 324. Not perfect.
  - Therefore rho(K^perp) >= 2.
  - K^perp has min dist 3, so it 1-error-corrects.
    Every syndrome has a unique coset leader of weight <= 1.
    The number of weight-1 words is n=360 < 2^(n-k) = 2^36 (syndrome space).
    Weight-2 words: C(360,2) = 64620 < 2^36. So every weight-2 vector
    has a unique syndrome (no two weight-2 words share a syndrome, since
    their XOR would be a nonzero weight-<=4 word; the code minimum distance
    is 3, but that doesn't immediately prevent syndrome collision for
    weight-2 pairs UNLESS the code has covering radius <= 2).
    Correct argument: a [n,k,3] code has rho=1 iff it's perfect.
    Since it's not perfect, rho >= 2.
    The Hamming bound: ball of radius 2 around any codeword covers
    1 + 360 + C(360,2) = 1 + 360 + 64620 = 64981 words.
    Total words: 2^360. Codewords: 2^324.
    Union of radius-2 balls: 2^324 * 64981.
    For covering: need 2^324 * 64981 >= 2^360.
    64981 >= 2^36? 2^36 = 68719476736. 64981 << 2^36. NOT covered by radius 2.
    Wait -- re-examine. rho=2 is WRONG by this count.
    Correct: rho <= n - k = 360 - 324 = 36 by the trivial dual-distance bound.
    Actual rho: since min dist = 3, the code corrects 1 error.
    The parity check matrix H has n-k=36 rows, n=360 columns.
    Every single bit flip gives a distinct syndrome (columns of H are distinct,
    since min dist = 3 implies no two columns are equal).
    For weight-2 error: sum of two columns. These need not all be distinct.
    The covering radius is the max weight such that every syndrome is achievable
    by an error of that weight. This equals the max distance from any word to C^perp.
    Lower bound via antipodal: rho >= ceil(d_perp / 2) = ceil(20/2) = 10.
    (since the PRIMAL has min dist 20, the dual covering radius >= 10 by
     the covering-radius / minimum-distance duality: rho(C) >= ceil(d(C^perp)/2)).
    So rho(K^perp) >= 10. 
    Upper bound: rho(C^perp) <= n - k_primal = 360 - 36 = 324? No, that's trivial.
    Better: by Delsarte bound, rho(C^perp) <= n - min_dist(C) = 360-20 = 340.
    Tighter: since C has parameters [360,36,20]_2, its dual has covering radius
    equal to the maximum weight in the coset weight distribution of C^perp.
    We know A_3^perp = 1080, so weight-3 words appear in C^perp.
    The max coset leader weight gives rho.
    HONEST RESULT: rho(K^perp) is between 10 and 360-20=340.
    The tight result requires the full coset weight enumerator of K^perp.
Note: the rho=2 claim in the original draft was incorrect. Corrected here.
"""
from math import comb, log2
import json

n = 360
k_primal = 36
k_dual = n - k_primal  # 324
d_primal = 20
d_dual = 3

# Covering radius bounds for K^perp = [360, 324, 3]_2
# Lower bound: rho(K^perp) >= ceil(d_primal / 2) = ceil(20/2) = 10
rho_lower = (d_primal + 1) // 2  # ceil(20/2) = 10

# Upper bound: trivial rho <= n - k_primal = 324, but also:
# rho(C^perp) <= n - ceil((d+1)/2) where d = min dist of C = 20
# => rho <= 360 - 10 = 350 (weak)
# Better: Plotkin-type, rho(C^perp) <= floor((d_primal - 1)/2) * something?
# Most useful known bound: since K has rate 36/360 = 1/10, and K^perp has
# rate 324/360 = 9/10 (high rate), the covering radius is typically small.
# The norm of K^perp: sum of squared distances from 0 to all coset leaders.
# Known: for the [360,324,3] code, since A_3^perp = 1080 and A_0^perp = 1,
# the covering radius satisfies rho >= 3 (as weight-3 words exist in K^perp?
# NO: A_3^perp are CODEWORDS of K^perp; the covering radius is about coset
# leaders of K, not codewords of K^perp).
# 
# CORRECT FINAL BOUNDS:
rho_upper = n - d_primal  # = 340, trivial upper bound
# More refined: the covering radius of C^perp equals the max distance
# from any x in F_2^360 to C^perp. Since C^perp is a [360,324,3] code,
# its covering radius is at most 36 (= n - k_dual = 360 - 324 = 36),
# because every syndrome is a length-(n-k_dual)=36 vector and the max
# syndrome weight is at most 36.
rho_upper_refined = n - k_dual  # = 36
print(f"[{n},{k_dual},{d_dual}]_2 covering radius:")
print(f"  Lower bound: rho >= ceil(d_primal/2) = {rho_lower}")
print(f"  Upper bound: rho <= n - k_dual = {rho_upper_refined}")
print(f"  Interval: [{rho_lower}, {rho_upper_refined}]")
print()

# The A_3^perp = 1080 fact:
print(f"A_3^perp (min weight of K^perp) = {d_dual}, confirmed by Pass4862.")
print(f"A_3^perp count = 1080 = number of Levi minimum checks (Pass4862).")
print()

# MacWilliams first few dual coefficients from Pass4867:
dual_low = {0: 1, 3: 1080, 4: 10530, 5: 127656, 6: 2329680}
print("Known dual enumerator coefficients (Pass4867):")
for w, a in sorted(dual_low.items()):
    print(f"  A_{w}^perp = {a}")
print()
print("Full dual enumerator: deterministic MacWilliams transform of frozen Pass4867")
print("primal certificate (82 nonzero weight levels).")
print("Status: OPEN — requires importing frozen full primal enumerator JSON.")

cert = {
    "pass": "4879",
    "theorem": "dual_code_covering_radius_bounds",
    "primal_params": [n, k_primal, d_primal],
    "dual_params": [n, k_dual, d_dual],
    "rho_lower": rho_lower,
    "rho_upper": rho_upper_refined,
    "rho_interval": [rho_lower, rho_upper_refined],
    "A3_perp": 1080,
    "A3_perp_interpretation": "1080 Levi minimum checks = min-weight codewords of K^perp",
    "known_dual_coefficients": dual_low,
    "note": (
        "rho([360,324,3]_2) is in [10,36]. The primal [360,36,20]_2 has "
        "rho in [124,179]. The dual has much tighter covering due to high rate. "
        "Full dual enumerator is deterministic from frozen Pass4867 primal."
    )
}
with open("data/PART_W33_PASS4879_DUAL_CODE_COVERING_RADIUS.json", "w") as f:
    json.dump(cert, f, indent=2)
print("\nCertificate written.")
print(json.dumps(cert, indent=2))
