"""Pass 12675: the F_8 torus symmetry is a regular element of type E6(a1) in W(E6) = O^-(6,2), acting on E6/2E6.
Effective three-qubit phase space V = T^perp/T = F_2^6 (standard symplectic coordinates, w33_f8_codespace_effective_sos.py).
 (1) the nine Lagrangians L_t (covered Paulis of basis t in T^perp) and the unique symplectic sigma with sigma(L_i) = L_{i+1};
 (2) all 64 quadratic forms Q polarising to the symplectic form: which are sigma-invariant, their type (elliptic: 27 singular
     non-zero points, hyperbolic: 35), and how the coset weights and the Lagrangians sit relative to them;
 (3) sigma has minimal polynomial Phi_9 = x^6 + x^3 + 1, the characteristic polynomial of the regular class E6(a1) of W(E6)
     on the reflection representation (Carter); with an invariant elliptic Q, (V, Q) = E6/2E6 (27 + 36 = 63, cf. the repo's
     [1,27,36] E6/2E6 certificates) and sigma lies in O^-(6,2) = W(E6).
usage: py -3 analysis/w33_f8_torus_is_E6a1.py"""
import collections, itertools, json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
_argv = sys.argv; sys.argv = ["x", "T", "3"]
src = open(os.path.join(HERE, "w33_f8_codespace_effective_sos.py"), encoding="utf-8").read()
G = {"__name__": "x", "__file__": os.path.join(HERE, "w33_f8_codespace_effective_sos.py")}
exec(src[: src.index("rng = np.random.default_rng(1)")], G); sys.argv = _argv
Tperp, Tset, std, weights, lab, covered, nq = (G[k] for k in ("Tperp", "Tset", "std", "weights", "lab", "covered", "nq"))
N = 1 << nq; pc = lambda n: bin(n).count("1") & 1
lsrc = open(os.path.join(HERE, "w33_f8_pauli_stabiliser_ladder.py"), encoding="utf-8").read()
gl = {"__name__": "x", "__file__": os.path.join(HERE, "w33_f8_pauli_stabiliser_ladder.py")}
exec(lsrc[: lsrc.index("res = {}")], gl)
U, pauli = gl["U"], gl["pauli"]
def bases_of(k):
    P = pauli(*k).real
    return [i for i, Ut in enumerate(U) if np.allclose(D := Ut @ P @ Ut.T, np.diag(np.diag(D)))]
L = [set() for _ in range(9)]
for v in Tperp:
    if v in Tset: continue
    k = lab(v)
    if covered(k):
        for t in bases_of(k): L[t].add(std(v))
assert all(len(l_) == 7 for l_ in L)
pts = [(x, z) for x in range(N) for z in range(N) if (x, z) != (0, 0)]
enc = lambda p: p[0] | (p[1] << nq); dec = lambda e: (e & (N - 1), e >> nq)
form = lambda p, r: pc(p[0] & r[1]) ^ pc(p[1] & r[0])
# meet pattern and cycle order
M = [[len(L[i] & L[j]) for j in range(9)] for i in range(9)]
cyc = [0]
while len(cyc) < 9:
    nxt = [j for j in range(9) if M[cyc[-1]][j] == 3 and j not in cyc]; cyc.append(nxt[0])
assert M[cyc[-1]][cyc[0]] == 3
# sigma: linear symplectic map sending L[cyc[i]] -> L[cyc[i+1]] (backtracking on images of basis vectors e_1..e_6)
basis = [enc((1 << i, 0)) for i in range(nq)] + [enc((0, 1 << i)) for i in range(nq)]
target = {cyc[i]: cyc[(i + 1) % 9] for i in range(9)}
memb = {p: [t for t in range(9) if p in L[t]] for p in pts}
def apply(img, e):
    y = 0
    for i in range(2 * nq):
        if e >> i & 1: y ^= img[i]
    return y
sols = []
def ok(img):
    n_ = len(img)
    for i in range(n_):
        for j in range(n_):
            if form(dec(img[i]), dec(img[j])) != form(dec(basis[i]), dec(basis[j])): return False
    for m in range(1, 1 << n_):
        e = 0
        for i in range(n_):
            if m >> i & 1: e ^= basis[i]
        y = apply(img + [0] * (2 * nq - n_), e)
        if y == 0: return False
        for t in memb[dec(e)]:
            if dec(y) not in L[target[t]]: return False
    return True
def bt(img):
    if len(img) == 2 * nq: sols.append(list(img)); return
    for y in range(1, N * N):
        img.append(y)
        if ok(img): bt(img)
        img.pop()
bt([])
assert len(sols) == 1
sig = sols[0]; S = lambda p: dec(apply(sig, enc(p)))
# minimal polynomial check
def powmap(k):
    out = list(range(N * N))
    for _ in range(k): out = [enc(S(dec(e))) if e else 0 for e in out]
    return out
def S_k(e, k):
    for _ in range(k): e = enc(S(dec(e)))
    return e
phi9 = all(S_k(b, 6) ^ S_k(b, 3) ^ b == 0 for b in basis)
fixed = sum(1 for p in pts if S(p) == p)
orbits = []
seen = set()
for p in pts:
    if p in seen: continue
    o = [p]; q_ = S(p)
    while q_ != p: o.append(q_); q_ = S(q_)
    seen |= set(o); orbits.append(o)
# quadratic forms Q_{a,b}(x,z) = x.z + a.x + b.z
wt = {p: weights.get(p, 0) for p in pts}
res_q = []
for a in range(N):
    for b in range(N):
        Q = lambda p: pc(p[0] & p[1]) ^ pc(a & p[0]) ^ pc(b & p[1])
        inv = all(Q(S(p)) == Q(p) for p in pts)
        nz = sum(1 for p in pts if Q(p) == 0)
        if inv:
            byw = {k: dict(collections.Counter(Q(p) for p in pts if wt[p] == k)) for k in sorted(set(wt.values()))}
            lag = [sum(1 for p in L[t] if Q(p) == 0) for t in range(9)]
            res_q.append(dict(a=a, b=b, type="elliptic" if nz == 27 else ("hyperbolic" if nz == 35 else str(nz)), singular=nz,
                              singular_by_weight=byw, singular_points_per_Lagrangian=lag))
print("sigma: order", 9, "fixed points", fixed, "Phi_9(sigma) = 0:", phi9, "orbit sizes", sorted(len(o) for o in orbits))
print("sigma-invariant quadratic forms:", len(res_q))
for r in res_q: print(r)
out = dict(phi9=phi9, fixed_points=fixed, orbit_sizes=sorted(len(o) for o in orbits), cycle=cyc, invariant_forms=res_q,
           weight_classes={str(k): sum(1 for p in pts if wt[p] == k) for k in sorted(set(wt.values()))})
json.dump(out, open(os.path.join(ROOT, "data", "w33_f8_torus_is_E6a1.json"), "w"), indent=1, default=str)
# ---- tritangent check: in each Lagrangian, do the 3 singular points sum to zero (three lines of a tritangent plane)?
qa = res_q[0]["a"]; qb = res_q[0]["b"]
Qf = lambda p: pc(p[0] & p[1]) ^ pc(qa & p[0]) ^ pc(qb & p[1])
trit = []
for t in range(9):
    sing = [p for p in L[t] if Qf(p) == 0]
    s0 = (sing[0][0] ^ sing[1][0] ^ sing[2][0], sing[0][1] ^ sing[1][1] ^ sing[2][1])
    trit.append(s0 == (0, 0))
# singular points: incidence counts with the nine planes = coset weight?
sing_pts = [p for p in pts if Qf(p) == 0]
inc_ok = all(sum(p in L[t] for t in range(9)) == wt[p] for p in pts)
# all tritangent triples of E6/2E6: triples of singular points summing to zero, pairwise non-orthogonal? count them
triples = [tr for tr in itertools.combinations(sing_pts, 3) if (tr[0][0] ^ tr[1][0] ^ tr[2][0], tr[0][1] ^ tr[1][1] ^ tr[2][1]) == (0, 0)]
print("each basis carries a zero-sum triple of singular points:", trit, "| weight = number of bases containing the point:", inc_ok,
      "| zero-sum triples of singular points in E6/2E6:", len(triples))
out.update(tritangent_per_basis=trit, weight_equals_incidence=inc_ok, zero_sum_singular_triples=len(triples))
json.dump(out, open(os.path.join(ROOT, "data", "w33_f8_torus_is_E6a1.json"), "w"), indent=1, default=str)
# ---- sigma-orbits on the 45 tritangent planes; which orbit the nine bases form
tri_set = [frozenset(tr) for tr in triples]
basis_planes = {frozenset(p for p in L[t] if Qf(p) == 0) for t in range(9)}
orbs = []; seen_ = set()
for tp in tri_set:
    if tp in seen_: continue
    o = [tp]; nx = frozenset(S(p) for p in tp)
    while nx != tp: o.append(nx); nx = frozenset(S(p) for p in nx)
    seen_ |= set(o); orbs.append(o)
our = [i for i, o in enumerate(orbs) if set(o) == basis_planes]
# line orbits (27 singular points) and their weights
line_orbits = []
seen_ = set()
for p in sing_pts:
    if p in seen_: continue
    o = [p]; q_ = S(p)
    while q_ != p: o.append(q_); q_ = S(q_)
    seen_ |= set(o); line_orbits.append(sorted({wt[x] for x in o}))
print("sigma-orbits on the 45 tritangent planes:", sorted(len(o) for o in orbs), "| the nine bases form one orbit:", len(our) == 1,
      "| line orbits (weights):", line_orbits)
out.update(tritangent_orbit_sizes=sorted(len(o) for o in orbs), bases_form_one_orbit=len(our) == 1, line_orbit_weights=line_orbits)
json.dump(out, open(os.path.join(ROOT, "data", "w33_f8_torus_is_E6a1.json"), "w"), indent=1, default=str)
# ---- trinification test: are the three sigma-orbits of lines Steiner trihedral pairs (3x3 grids)?
# Two distinct lines meet iff B(p,q) = 0 (each line is skew to 16 lines, B = 1, and meets 10).
B = lambda p, r: 1 - form(p, r)
meet_deg = collections.Counter(sum(B(p, r) for r in sing_pts if r != p) for p in sing_pts)
orbit_sets = []
seen_ = set()
for p in sing_pts:
    if p in seen_: continue
    o = [p]; q_ = S(p)
    while q_ != p: o.append(q_); q_ = S(q_)
    seen_ |= set(o); orbit_sets.append(o)
def is_rook(o):
    deg = [sum(B(a, b) for b in o if b != a) for a in o]
    if set(deg) != {4}: return False, deg
    # rook graph K3 x K3: every edge in exactly one triangle-clique of size 3; check that the meet graph's maximal cliques are 6 triangles
    import itertools as it
    tri = [t for t in it.combinations(o, 3) if all(B(a, b) for a, b in it.combinations(t, 2))]
    return len(tri) == 6, deg
rook = [is_rook(o)[0] for o in orbit_sets]
# each row/column triangle of a trihedral pair is a tritangent plane: count triangles that are zero-sum
tri_planes = sum(1 for o in orbit_sets for t in itertools.combinations(o, 3) if all(B(a, b) for a, b in itertools.combinations(t, 2)) and
                 (t[0][0] ^ t[1][0] ^ t[2][0], t[0][1] ^ t[1][1] ^ t[2][1]) == (0, 0))
print("line meet degrees:", dict(meet_deg), "| the three sigma-orbits of lines are 3x3 grids (Steiner trihedral pairs):", rook,
      "| row/column triangles that are tritangent planes:", tri_planes, "of 18")
out.update(line_meet_degrees={str(k): v for k, v in meet_deg.items()}, line_orbits_are_trihedral_pairs=rook, grid_triangles_tritangent=tri_planes)
json.dump(out, open(os.path.join(ROOT, "data", "w33_f8_torus_is_E6a1.json"), "w"), indent=1, default=str)
# ---- structure inside each sigma-orbit of lines: meet degrees, meet triangles, and cross-orbit meeting numbers
inside = []
for o in orbit_sets:
    deg = sorted(sum(B(a, b) for b in o if b != a) for a in o)
    tri_ = [t for t in itertools.combinations(o, 3) if all(B(a, b) for a, b in itertools.combinations(t, 2))]
    zs = sum(1 for t in tri_ if (t[0][0] ^ t[1][0] ^ t[2][0], t[0][1] ^ t[1][1] ^ t[2][1]) == (0, 0))
    inside.append(dict(weight=wt[o[0]], meet_degrees=deg, meet_triangles=len(tri_), tritangent_triangles=zs))
cross = [[sum(B(a, b) for b in orbit_sets[j]) for j in range(3)] for a in [orbit_sets[i][0] for i in range(3)]]
print("inside orbits:", inside, "| meet numbers of one line with each orbit:", cross)
out.update(line_orbit_structure=inside, line_cross_meetings=cross)
json.dump(out, open(os.path.join(ROOT, "data", "w33_f8_torus_is_E6a1.json"), "w"), indent=1, default=str)
