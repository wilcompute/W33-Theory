"""Pass 12672: EXACT statements from the Galois structure of the Pass 12671 witness rho (entries in K = Q(g, sqrt3, i), g = 2cos(2pi/9)).
tau: g -> g^2 - 2 (2cos t -> 2cos 2t) generates Gal(Q(g)/Q) = Z/3; extended to K fixing sqrt3 and i, it commutes with complex
conjugation.  Hermiticity, tr = 1, rho^2 = rho and criticality ([G(rho), rho] = 0 with G(rho) = sum_t U_t^T diag(2 p_t) U_t the
gradient operator of sum p^2) are polynomial identities over Q, so tau(rho), tau^2(rho) are again pure critical states with
64F = tau(c8), tau^2(c8): the three roots of 243c^3 - 3807c^2 + 17577c - 23941.  All checked here in exact arithmetic (no floats).
usage: py -3 analysis/w33_f8_galois_conjugate_witnesses.py"""
import json, os
from fractions import Fraction
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
wsrc = open(os.path.join(HERE, "w33_f8_exact_witness.py"), encoding="utf-8").read()
W = {"__name__": "x", "__file__": os.path.join(HERE, "w33_f8_exact_witness.py")}
exec(wsrc[: wsrc.index("# --- exact basis distributions")], W)
rho, kmatmul, conjT, DEN, trace, mul = W["rho"], W["kmatmul"], W["conjT"], W["DEN"], W["trace"], W["mul"]
# tau on the Q(g)-triple (coefficients of 1, g, g^2): g -> g^2 - 2, g^2 -> 4 - g - g^2
TAU = np.array([[1, -2, 4], [0, 0, -1], [0, 1, -1]], dtype=object)   # column e: image of basis e in (1, g, g^2)


def tau(M):
    out = np.zeros_like(M)
    for blk in range(4):           # blocks (s^b i^c), each a Q(g)-triple
        for e in range(3):
            for f in range(3):
                if TAU[f, e]: out[3 * blk + f] = out[3 * blk + f] + TAU[f, e] * M[3 * blk + e]
    return out


Xi = np.array([[1 - 2 * trace(mul(a, b)) for b in range(8)] for a in range(8)], dtype=object)
Phi = [np.array([[1 - 2 * trace(mul(tt, mul(a, b))) for b in range(8)] for a in range(8)], dtype=object) for tt in range(8)]
Us = []
for tt in range(9):
    if tt == 0: U8 = np.eye(64, dtype=object) * 8
    else:
        U8 = np.zeros((64, 64), dtype=object)
        for xx in range(64):
            E = np.zeros((8, 8), dtype=object); E[xx // 8, xx % 8] = 1
            U8[:, xx] = (Xi.dot(E * Phi[tt - 1]).dot(Xi)).ravel()
    Uk = np.zeros((12, 64, 64), dtype=object); Uk[0] = U8; Us.append(Uk)


def check(R, label):
    herm = all((conjT(R)[e] == R[e]).all() for e in range(12))
    tr = [sum(R[e][y, y] for y in range(64)) for e in range(12)]
    R2 = kmatmul(R, R); idem = all((R2[e] == DEN * R[e]).all() for e in range(12))
    total = [Fraction(0)] * 12; G = np.zeros((12, 64, 64), dtype=object)
    for Uk in Us:
        M = kmatmul(kmatmul(Uk, R), conjT(Uk))        # 64 DEN U rho U^T
        p = np.array([[M[e][k, k] for k in range(64)] for e in range(12)], dtype=object)   # 64 DEN p_k
        for k in range(64):
            pk = p[:, k].reshape(12, 1, 1)
            sq = kmatmul(pk, pk)
            for e in range(12): total[e] += Fraction(int(sq[e][0, 0]), (64 * DEN) ** 2)
        D = np.zeros((12, 64, 64), dtype=object)
        for e in range(12):
            for k in range(64): D[e][k, k] = p[e, k]
        G = G + kmatmul(kmatmul(conjT(Uk), D), Uk)      # proportional to the gradient operator (positive factor)
    comm = kmatmul(G, R) - kmatmul(R, G)
    critical = all((comm[e] == 0).all() for e in range(12))
    c = [64 * (total[e] - (Fraction(9, 64) if e == 0 else 0)) for e in range(12)]
    out = dict(hermitian=bool(herm), trace_one=bool(tr[0] == DEN and all(v == 0 for v in tr[1:])), idempotent=bool(idem),
               critical=bool(critical), c=[str(v) for v in c[:3]], c_rest_zero=all(v == 0 for v in c[3:]))
    print(label, out, flush=True); return out


g = lambda a, b: [Fraction(a, 9), Fraction(b, 9), Fraction(0)]
res = {}
R = rho
for n in range(3):
    o = check(R, f"tau^{n}(rho)")
    # expected 64F = tau^n((47 - 16 g)/9): g -> g^2 - 2 -> -g^2 - g + 2
    expect = [["47/9", "-16/9", "0"], ["79/9", "0", "-16/9"], ["5/3", "16/9", "16/9"]][n]
    o["expected"] = expect; o["matches"] = o["c"] == [str(Fraction(x)) for x in expect]
    res[f"tau{n}"] = o; R = tau(R)
import math
gm = 2 * math.cos(2 * math.pi / 9)
for k, o in res.items():
    a, b, cc = (float(Fraction(x)) for x in o["c"]); o["numeric"] = a + b * gm + cc * gm * gm
print({k: (o["matches"], round(o["numeric"], 10)) for k, o in res.items()}, flush=True)
res["all_exact"] = all(o["hermitian"] and o["trace_one"] and o["idempotent"] and o["critical"] and o["matches"] and o["c_rest_zero"] for o in res.values() if isinstance(o, dict))
print("ALL EXACT (three pure critical states, values = the three cubic roots):", res["all_exact"])
json.dump(res, open(os.path.join(ROOT, "data", "w33_f8_galois_conjugate_witnesses.json"), "w"), indent=1)
