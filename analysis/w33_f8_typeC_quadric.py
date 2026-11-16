"""Pass 12677: is the 16-dim type-C code space (the unique type-C order-4 subgroup C of the torus group T) an E8/2E8 structure?
The global order-9 symmetry S: m -> g m h^T (g, h of order 9; w33_f8_torus_global_origin.py) normalises T, hence fixes C (T has a
unique type-C subgroup).  Induced map sigma_C on the effective 4-qubit phase space C^perp/C = F_2^8: order, fixed points, and all
256 quadratic forms polarising to the symplectic form that sigma_C preserves (hyperbolic O^+(8,2): 135 singular non-zero points,
as for E8/2E8 with W(E8)/{+-1} = O^+(8,2); elliptic: 119), and how the coset weights sit relative to them.
usage: py -3 analysis/w33_f8_typeC_quadric.py"""
import collections, contextlib, io, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
G = {"__name__": "x", "__file__": os.path.join(HERE, "w33_f8_torus_global_origin.py")}
src = open(os.path.join(HERE, "w33_f8_torus_global_origin.py"), encoding="utf-8").read()
with contextlib.redirect_stdout(io.StringIO()):
    exec(src[: src.index("from scipy.optimize import minimize\nel9")], G)
norm, rows_, act = G["norm"], G["rows"], G["act"]
el9 = [el for el, r in zip(norm, rows_) if r["cycle_type"] == [9]][0]
Smap = lambda lab: act(el9, lab)
_argv = sys.argv; sys.argv = ["x", "C", "3"]; os.environ["GENS"] = os.environ.get("TYPEGENS", "53,33;1,6")
E = {"__name__": "x", "__file__": os.path.join(HERE, "w33_f8_codespace_effective_sos.py")}
esrc = open(os.path.join(HERE, "w33_f8_codespace_effective_sos.py"), encoding="utf-8").read()
with contextlib.redirect_stdout(io.StringIO()):
    exec(esrc[: esrc.index("rng = np.random.default_rng(1)")], E)
sys.argv = _argv
Tperp, Tset, std, weights, lab, vec, nq = (E[k] for k in ("Tperp", "Tset", "std", "weights", "lab", "vec", "nq"))
N = 1 << nq; pc = lambda n: bin(n).count("1") & 1
FIXED = all(vec(Smap(lab(t))) in Tset for t in Tset)
if not FIXED:
    print("S does not fix this order-4 group"); sys.exit()
sig = {}
for v in Tperp:
    if v in Tset: continue
    p = std(v); q_ = std(vec(Smap(lab(v))))
    assert sig.get(p, q_) == q_; sig[p] = q_
pts = sorted(sig)
def order_(p):
    k = 1; x = sig[p]
    while x != p: x = sig[x]; k += 1
    return k
orders = collections.Counter(order_(p) for p in pts)
wt = {p: weights.get(p, 0) for p in pts}
res = []
for a in range(N):
    for b in range(N):
        Q = lambda p: pc(p[0] & p[1]) ^ pc(a & p[0]) ^ pc(b & p[1])
        if all(Q(sig[p]) == Q(p) for p in pts):
            nz = sum(1 for p in pts if Q(p) == 0)
            res.append(dict(a=a, b=b, singular=nz, type="hyperbolic (E8/2E8 type)" if nz == 135 else ("elliptic" if nz == 119 else str(nz)),
                            singular_by_weight={k: dict(collections.Counter(Q(p) for p in pts if wt[p] == k)) for k in sorted(set(wt.values()))}))
print("sigma_C: point orbit sizes", dict(orders), "| invariant quadratic forms:", len(res))
for r in res: print(r)
json.dump(dict(orbit_sizes={str(k): v for k, v in orders.items()}, invariant_forms=res, weight_classes={str(k): sum(1 for p in pts if wt[p] == k) for k in sorted(set(wt.values()))}),
          open(os.path.join(ROOT, "data", "w33_f8_type" + os.environ.get("TYPENAME", "C") + "_quadric.json"), "w"), indent=1)
