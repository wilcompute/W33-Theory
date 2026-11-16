"""Pass 12678: clean-quadric census for uncovered order-4 Pauli groups of the F_8 regulus (control for Pass 12677's type-C E8/2E8).
For an order-4 uncovered isotropic group S' (types A, B, C by coset-weight histogram, Pass 12674-12675), the effective phase space
S'^perp/S' = F_2^8 carries the coset weights n.  A quadratic form Q polarising to the symplectic form is 'clean' if every covered
coset (n > 0) is Q-singular; its type is hyperbolic (135 singular non-zero points, E8/2E8 type) or elliptic (119).
Computed for random uncovered order-4 groups (all types) without assuming any symmetry: the number of clean forms of each kind, per type.
usage: py -3 analysis/w33_f8_clean_quadric_census.py [samples]"""
import collections, json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
lsrc = open(os.path.join(HERE, "w33_f8_pauli_stabiliser_ladder.py"), encoding="utf-8").read()
gl = {"__name__": "x", "__file__": os.path.join(HERE, "w33_f8_pauli_stabiliser_ladder.py")}
exec(lsrc[: lsrc.index("res = {}")], gl)
covered, comm = gl["covered"], gl["comm"]
SAMPLES = int(sys.argv[1]) if len(sys.argv) > 1 else 300
rng = np.random.default_rng(12678)
pc = lambda n: bin(n).count("1") & 1
labels = [(u, v) for u in range(64) for v in range(64) if (u, v) != (0, 0)]
COV = {k for k in labels if covered(k)}
vec = lambda k: (k[0] << 6) | k[1]; lab = lambda v: (v >> 6, v & 63)
form = lambda a, b: 0 if comm(lab(a), lab(b)) else 1
TYPE = {((0, 156), (1, 63), (2, 36)): "A", ((0, 138), (1, 99), (2, 18)): "B", ((0, 165), (1, 54), (2, 27), (3, 9)): "C"}
def analyse(g1, g2):
    Sset = {0, vec(g1), vec(g2), vec(g1) ^ vec(g2)}
    Tperp = [v for v in range(1, 1 << 12) if all(form(v, t) == 0 for t in Sset if t)]
    # coset weights
    cos = {}
    for v in Tperp:
        cos.setdefault(min(v ^ t for t in Sset), []).append(v)
    wh = tuple(sorted(collections.Counter(sum(lab(x) in COV for x in c_) for k, c_ in cos.items() if k).items()))
    # symplectic basis of the quotient
    def indep(basis, v):
        piv = []
        for b in basis + [v]:
            x = b
            for p in piv: x = min(x, x ^ p)
            if x == 0: return False
            piv.append(x); piv.sort(reverse=True)
        return True
    base = [vec(g1), vec(g2)]; E_, F_ = [], []
    while len(E_) < 4:
        e = next(v for v in Tperp if all(form(v, x) == 0 for x in E_ + F_) and indep(base + E_ + F_, v))
        f = next(v for v in Tperp if form(e, v) == 1 and all(form(v, x) == 0 for x in E_ + F_))
        E_.append(e); F_.append(f)
    std = lambda v: (sum(form(v, F_[i]) << i for i in range(4)), sum(form(E_[i], v) << i for i in range(4)))
    wpts = {}
    for k, c_ in cos.items():
        if k: wpts[std(k)] = sum(lab(x) in COV for x in c_)
    clean = collections.Counter()
    for a in range(16):
        for b in range(16):
            Q = lambda p: pc(p[0] & p[1]) ^ pc(a & p[0]) ^ pc(b & p[1])
            if all(Q(p) == 0 for p, w in wpts.items() if w > 0):
                nz = sum(1 for p in wpts if Q(p) == 0)
                clean["hyperbolic" if nz == 135 else ("elliptic" if nz == 119 else str(nz))] += 1
    return TYPE.get(wh, str(wh)), dict(clean)
res = collections.defaultdict(lambda: collections.Counter()); counts = collections.Counter(); reps = {}
for name, (g1, g2) in (("rep A", ((12, 53), (53, 33))), ("rep B", ((12, 53), (52, 39))), ("rep C", ((53, 33), (1, 6)))):
    t, cl = analyse(g1, g2); reps[name] = dict(type=t, clean=cl); print(name, t, cl, flush=True)
unc = [k for k in labels if k not in COV]
done = 0
while done < SAMPLES:
    g1 = unc[rng.integers(len(unc))]; g2 = unc[rng.integers(len(unc))]
    if g1 == g2 or not comm(g1, g2): continue
    g3 = (g1[0] ^ g2[0], g1[1] ^ g2[1])
    if g3 == (0, 0) or g3 in COV: continue
    t, cl = analyse(g1, g2); counts[t] += 1
    res[t][str(sorted(cl.items()))] += 1; done += 1
print("random uncovered order-4 groups by type:", dict(counts), flush=True)
for t in res: print(" ", t, "clean-form profiles:", dict(res[t]), flush=True)
json.dump(dict(reps=reps, type_counts=dict(counts), clean_profiles={t: dict(v) for t, v in res.items()}, samples=SAMPLES),
          open(os.path.join(ROOT, "data", "w33_f8_clean_quadric_census.json"), "w"), indent=1)
