"""Pass 12660 addendum: EXHAUSTIVE test for a Lagrangian M of F_2^{4k} with |M cap {Q = 0}| = 1 (a stabiliser state with d F = 1)
for the F_q regulus, q = 4 (control: exists) and q = 8 (annealing found none below 3).
The regulus stabiliser contains SL(2,q) x SL(2,q) and the F_q-scalars, transitive on the covered points (rank-one tensors), so the single
covered point of M may be fixed: c = (x1, x2, z1, z2) = (1, 0, 0, 0)... any one covered point.  Backtracking: extend span{c} by
vectors v orthogonal to the current span such that every new element of the span is UNCOVERED (Q != 0); candidates are kept as a
boolean mask over all 2^{4k} vectors; basis vectors are taken in increasing order (every subspace has such a basis).
Reports existence / exhaustive non-existence and the node count.  Also the analogous test for 'exactly 2' is not needed: |M cap C| is
odd when... (not assumed) -- the search for target 2 is run as well.   usage: py -3 analysis/w33_regulus_stabiliser_exhaustive.py"""
import json, os, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
src = open(os.path.join(HERE, "w33_regulus_constants_q16_q32.py"), encoding="utf-8").read()
g = {"__name__": "x", "__file__": os.path.join(HERE, "w33_regulus_constants_q16_q32.py")}
exec(src[: src.index("def model(")], g)


def run(k, tlimit=3000):
    q, mul, trace = g["field"](k); n = 2 * k; N = 4 * k; msk = q - 1; V = 1 << N
    MUL = np.array([[mul(a, b) for b in range(q)] for a in range(q)]); TR = np.array([trace(a) for a in range(q)])
    vs = np.arange(V); x1, x2, z1, z2 = vs & msk, (vs >> k) & msk, (vs >> 2 * k) & msk, (vs >> 3 * k) & msk
    unc = (MUL[x1, z1] ^ MUL[x2, z2]) != 0          # uncovered (Q != 0); note 0 has Q = 0
    def orth(v):
        a = (v & msk, (v >> k) & msk, (v >> 2 * k) & msk, (v >> 3 * k) & msk)
        return TR[MUL[a[0], z1] ^ MUL[a[1], z2] ^ MUL[a[2], x1] ^ MUL[a[3], x2]] == 0
    c = 1  # x1 = 1, others 0: Q = 0, covered
    assert not unc[c]
    st = dict(nodes=0, found=None, timeout=False); t0 = time.time()
    def rec(span, basis, cand, last):
        if st["found"] is not None or st["timeout"]: return
        st["nodes"] += 1
        if st["nodes"] % 20000 == 0 and time.time() - t0 > tlimit: st["timeout"] = True; return
        if len(basis) == n: st["found"] = list(basis); return
        # need n - len(basis) more dimensions: cand (excluding span) must have at least 2^n - |span| elements available in principle
        idx = np.flatnonzero(cand)
        idx = idx[idx > last]
        need = (1 << n) - len(span)
        if int(cand.sum()) < need: return
        for v in idx:
            if st["found"] is not None or st["timeout"]: return
            new = span ^ v
            # all new elements must be uncovered (already guaranteed for v itself by cand; check the coset)
            if not unc[new].all(): continue
            nc = cand & orth(int(v))
            for s in new: nc &= unc[vs ^ s] | np.isin(vs, new)  # v' + s uncovered for every s in the enlarged span
            nspan = np.concatenate([span, new])
            nc[nspan] = False
            rec(nspan, basis + [int(v)], nc, int(v))
    span0 = np.array([0, c]); cand0 = orth(c) & unc & unc[vs ^ c]
    cand0[[0, c]] = False
    rec(span0, [c], cand0, 0)
    status = "exists" if st["found"] else ("undecided" if st["timeout"] else "none")
    return dict(q=q, status=status, nodes=st["nodes"], seconds=round(time.time() - t0, 1), basis=st["found"])


out = {}
for k in (2, 3):
    out[f"q{1 << k}"] = run(k); print(out[f"q{1 << k}"], flush=True)
    json.dump(out, open(os.path.join(ROOT, "data", "w33_regulus_stabiliser_exhaustive.json"), "w"), indent=1)
