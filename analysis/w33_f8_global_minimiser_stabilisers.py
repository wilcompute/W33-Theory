"""Pass 12674: do all global minimisers of the F_8 regulus objective (nine MUBs of C^64) lie on Pauli code spaces?
From random starts in C^64 (L-BFGS, analytic gradients), keep runs converging to c8 = (47 - 32cos(2pi/9))/9 (within 1e-7), polish,
and compute each minimiser's Pauli stabiliser {P : |<P>| > 1 - 1e-6} (order, covered elements).  Also records the values reached
by the other runs.  Evidence for (not a proof of) the reduction 'global minimum = minimum over uncovered-stabiliser code spaces'.
usage: py -3 analysis/w33_f8_global_minimiser_stabilisers.py [starts]"""
import collections, json, math, os, sys, time
import numpy as np
from scipy.optimize import minimize
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
lsrc = open(os.path.join(HERE, "w33_f8_pauli_stabiliser_ladder.py"), encoding="utf-8").read()
gl = {"__name__": "x", "__file__": os.path.join(HERE, "w33_f8_pauli_stabiliser_ladder.py")}
exec(lsrc[: lsrc.index("res = {}")], gl)
fg, pauli, covered, C8 = gl["fg"], gl["pauli"], gl["covered"], gl["C8"]
STARTS = int(sys.argv[1]) if len(sys.argv) > 1 else 120
rng = np.random.default_rng(126740)
pc = lambda n: bin(n).count("1") & 1
labels = [(u, v) for u in range(64) for v in range(64) if (u, v) != (0, 0)]
cov = {k: covered(k) for k in labels}


def expectations(A):
    out = {}
    for (u, v) in labels:
        ph = np.array([(-1) ** pc(v & (x ^ u)) for x in range(64)])
        out[(u, v)] = np.vdot(A, ph * A[np.arange(64) ^ u])
    return out


vals = []; rec = []; t0 = time.time()
for s in range(STARTS):
    r = minimize(fg, rng.standard_normal(128), jac=True, method="L-BFGS-B", options=dict(maxiter=50000, gtol=1e-12, ftol=1e-16))
    c = r.fun * 64; vals.append(c)
    if abs(c - C8) < 1e-7:
        A = r.x[:64] + 1j * r.x[64:]; A /= np.linalg.norm(A)
        ex = expectations(A)
        stab = [k for k, e in ex.items() if abs(e) > 1 - 1e-6]
        # type of the stabiliser: covered-weight histogram of its cosets in S'^perp / S'
        Sg = [(0, 0)] + stab
        Sp = [k for k in labels if all(gl["comm"](k, t) for t in stab)]
        cos = {}
        for k in Sp: cos.setdefault(min((k[0] ^ t[0], k[1] ^ t[1]) for t in Sg), []).append(k)
        wh = collections.Counter(sum(cov.get(k, False) for k in c_) for kk, c_ in cos.items() if kk != (0, 0))
        rec.append(dict(order=len(stab) + 1, covered_in_stabiliser=sum(cov[k] for k in stab), weight_hist=sorted(wh.items()), stabiliser=[list(k) for k in stab]))
        print(f"start {s}: c8 reached, stabiliser order {len(stab) + 1}, covered in stabiliser {rec[-1]['covered_in_stabiliser']}  ({time.time() - t0:.0f}s)", flush=True)
hist = collections.Counter(round(v, 6) for v in vals)
res = dict(starts=STARTS, n_at_c8=len(rec), value_histogram={str(k): v for k, v in sorted(hist.items())},
           stabiliser_orders=dict(collections.Counter(r["order"] for r in rec)),
           weight_hist_types=dict(collections.Counter(str(r["weight_hist"]) for r in rec)), any_covered=any(r["covered_in_stabiliser"] for r in rec), records=rec)
print({k: v for k, v in res.items() if k != "records"}, flush=True)
json.dump(res, open(os.path.join(ROOT, "data", "w33_f8_global_minimiser_stabilisers.json" if STARTS == 150 else f"w33_f8_global_minimiser_stabilisers_{STARTS}.json"), "w"), indent=1)
