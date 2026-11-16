"""Pass 12682: the stabiliser of an orbit-A order-4 group in H = (SL(2,8) x SL(2,8)) x| Frobenius (order 504 by orbit-stabiliser,
Pass 12681).  Enumerates H, keeps the elements fixing the group S_A = <(12,53), (53,33)> (the Pass 12660 stabiliser), and reports:
element-order histogram (compared with SL(2,8): orders 1,2,3,7,9 with 1,63,56,216,168), whether the projections to the two SL(2,8)
factors are injective (a 'diagonal' subgroup), Frobenius content, and the induced action on S_A^perp/S_A = F_2^8 (orbits on the 255
points, invariant quadratic forms).   usage: py -3 analysis/w33_f8_orbitA_symmetry.py"""
import collections, contextlib, io, json, os
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
G = {"__name__": "x", "__file__": os.path.join(HERE, "w33_f8_torus_global_origin.py")}
src = open(os.path.join(HERE, "w33_f8_torus_global_origin.py"), encoding="utf-8").read()
with contextlib.redirect_stdout(io.StringIO()):
    exec(src[: src.index("norm=[]")], G)
mm, tp, tomat, tolabel, frob, SL, covered, comm = (G[k] for k in ("mm", "tp", "tomat", "tolabel", "frob", "SL", "covered", "comm"))
_g = [tuple(int(t) for t in g.split(",")) for g in os.environ.get("SYMGENS", "12,53;53,33").split(";")]
SA = [_g[0], _g[1], (_g[0][0] ^ _g[1][0], _g[0][1] ^ _g[1][1])]
SAset = set(SA)
def act(el, lab):
    g, h, f = el; y = mm(mm(g, tomat(*lab)), tp(h))
    for _ in range(f): y = frob(y)
    return tolabel(y)
stab = []
for g in SL:
    gA = [mm(g, tomat(*l)) for l in SA]
    for h in SL:
        hT = tp(h)
        for f in range(3):
            ok = True
            for m in gA:
                y = mm(m, hT)
                for _ in range(f): y = frob(y)
                if tolabel(y) not in SAset: ok = False; break
            if ok: stab.append((g, h, f))
print("stabiliser order:", len(stab), flush=True)
labels = [(u, v) for u in range(64) for v in range(64) if (u, v) != (0, 0)]
def as_perm(el): return tuple(act(el, l) for l in labels)
perms = {el: as_perm(el) for el in stab}
idx = {l: i for i, l in enumerate(labels)}
def order(el):
    p = perms[el]; cur = list(range(len(labels))); P = [idx[x] for x in p]; k = 0
    while True:
        cur = [P[c] for c in cur]; k += 1
        if cur == list(range(len(labels))): return k
orders = collections.Counter(order(el) for el in stab)
left = len({el[0] for el in stab}); right = len({el[1] for el in stab}); frobs = collections.Counter(el[2] for el in stab)
print("element orders:", dict(sorted(orders.items())), "| distinct left factors", left, "right factors", right, "| Frobenius exponents", dict(frobs), flush=True)
# induced action on S_A^perp / S_A
Sg = [(0, 0)] + SA
perp = [l for l in labels if all(comm(l, s) for s in SA)]
cos = {}
for l in perp: cos.setdefault(min((l[0] ^ s[0], l[1] ^ s[1]) for s in Sg), []).append(l)
reps = [k for k in cos if k != (0, 0)]
rep_of = {l: min((l[0] ^ s[0], l[1] ^ s[1]) for s in Sg) for l in perp}
seen = set(); orb_sizes = []
for k in reps:
    if k in seen: continue
    o = {rep_of[act(el, k)] for el in stab}; seen |= o; orb_sizes.append(len(o))
wt = {k: sum(covered(x) for x in cos[k]) for k in reps}
orbit_weights = []
seen = set()
for k in reps:
    if k in seen: continue
    o = {rep_of[act(el, k)] for el in stab}; seen |= o; orbit_weights.append((len(o), sorted({wt[x] for x in o})))
print("orbits on the 255 effective points (size, weights):", sorted(orbit_weights), flush=True)
SL28 = {1: 1, 2: 63, 3: 56, 7: 216, 9: 168}
res = dict(order=len(stab), element_orders={str(k): v for k, v in sorted(orders.items())}, matches_SL28_profile=dict(orders) == SL28,
           distinct_left=left, distinct_right=right, frobenius=dict(frobs), effective_orbits=sorted(orbit_weights))
json.dump(res, open(os.path.join(ROOT, "data", "w33_f8_orbitA_symmetry.json" if os.environ.get("SYMGENS", "12,53;53,33") == "12,53;53,33" else "w33_f8_stab_" + os.environ["SYMGENS"].replace(",", "_").replace(";", "__") + ".json"), "w"), indent=1, default=str)
