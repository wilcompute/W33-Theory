"""Item 1: an exact proof that the 432 pentads are strongly unextendible (Pass 12637 found it numerically).
A state v is unbiased to the stabiliser basis of a line L iff <W_u> = 0 for every Pauli W_u in the class of L.  So v is unbiased to all
5 bases of a pentad iff its Pauli weights a_u = |<W_u>|^2 vanish on the 20 points the pentad covers (both W_u and W_u^2 = W_{2u}).
Pure-state identity (characteristic function of a pure state; checked numerically below on random pure states, and shown to FAIL for a
mixed state as control):  sum_u a_u omega^{[u,v]} = D a_v  for every v, with D = 9, a_0 = 1.
With a_u = a_{-u}, per projective point p (two Paulis) the sum becomes linear with coefficients 2 (if [p,q] = 0) or -1 (else).
LP feasibility: a_0 = 1, a_p >= 0 supported on the 20 uncovered points, the 40 + 1 linear equations.  Infeasible => no pure state =>
strongly unextendible, PROVED.  Certificate: an exact rational Farkas vector y with y^T A >= 0 on the support and y^T b < 0, checked in
exact arithmetic (fractions).  Controls: the LP must be FEASIBLE for 4 bases of a complete spread and for each 4-subset of the pentad.
usage: py -3 analysis/w33_strong_umub_certificate.py"""
import itertools, json, os
from fractions import Fraction as Fr
import numpy as np
from scipy.optimize import linprog
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
import contextlib, io
ns = {"__name__": "x", "__file__": os.path.join(HERE, "w33_pentad_umub.py")}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open(os.path.join(HERE, "w33_pentad_umub.py"), encoding="utf-8").read().split("# --- (3)")[0], ns)
P, lines, w, pauli, maxsets, disj = ns["P"], ns["lines"], ns["w"], ns["pauli"], ns["maxsets"], ns["disj"]
D = 9
# --- check the identity on random states (pure: holds; mixed: fails)
allu = [u for u in itertools.product(range(3), repeat=4)]
Wm = {u: pauli(u) for u in allu}
om = np.exp(2j * np.pi / 3)
def sympl(u, v):
    return (u[0] * v[2] - u[2] * v[0] + u[1] * v[3] - u[3] * v[1]) % 3
def ident_err(rho):
    a = {u: abs(np.trace(rho @ Wm[u])) ** 2 for u in allu}
    return max(abs(sum(a[u] * om ** sympl(u, v) for u in allu) - D * a[v]) for v in allu)
rng = np.random.default_rng(1)
psi = rng.standard_normal(9) + 1j * rng.standard_normal(9); psi /= np.linalg.norm(psi)
pure_err = ident_err(np.outer(psi, psi.conj()))
M = rng.standard_normal((9, 3)) + 1j * rng.standard_normal((9, 3)); rho_m = M @ M.conj().T; rho_m /= np.trace(rho_m)
mixed_err = ident_err(rho_m)
print("identity error: pure %.2e | mixed (control, must be large) %.2e" % (pure_err, mixed_err))

# --- LP per line set
def lp_matrix(cover):
    sup = [p for p in range(40) if p not in cover]            # allowed nonzero weights (projective points)
    # equations for every point q (and q = 0): a_0 * 1 + sum_p a_p * c(p, q) = D * a_q  (a_q = 0 if q covered)
    def c(p, q):
        return 2 if w(P[p], P[q]) == 0 else -1
    rows, rhs = [], []
    # q = 0: sum over all u of a_u = D  ->  1 + 2 * sum_p a_p = 9
    rows.append([2 for p in sup]); rhs.append(D - 1)
    for q in range(40):
        row = [c(p, q) - (D if p == q else 0) for p in sup]
        rows.append(row); rhs.append(-1)                         # a_0 term moved to the right: -1
    return sup, rows, rhs
def solve(cover):
    sup, A, b = lp_matrix(cover)
    r = linprog(np.zeros(len(sup)), A_eq=np.array(A, float), b_eq=np.array(b, float), bounds=[(0, None)] * len(sup), method="highs")
    return r.status, sup, A, b
def farkas(A, b):
    # find y with y^T A >= 0 (componentwise) and y^T b = -1  (proves Ax = b, x >= 0 infeasible)
    m, n = len(A), len(A[0])
    r = linprog(np.zeros(m), A_ub=-np.array(A, float).T, b_ub=np.zeros(n), A_eq=np.array([b], float), b_eq=[-1.0], bounds=[(None, None)] * m, method="highs")
    if r.status != 0:
        return None
    y = [Fr(v).limit_denominator(10 ** 6) for v in r.x]
    ok = all(sum(y[i] * A[i][j] for i in range(m)) >= 0 for j in range(n)) and sum(y[i] * b[i] for i in range(m)) < 0
    return y if ok else None
def cover_of(Ls):
    return frozenset().union(*[lines[L] for L in Ls])
results = {}
# controls
spread = None
def bk(R, Pc, X):
    global spread
    if spread is not None: return
    if not Pc and not X:
        if len(R) == 10: spread = sorted(R)
        return
    for v in list(Pc):
        bk(R | {v}, {u for u in Pc if disj[v][u]}, {u for u in X if disj[v][u]}); Pc = Pc - {v}; X = X | {v}
bk(set(), set(range(40)), set())
st, *_ = solve(cover_of(spread[:4]))
results["control_4_spread_bases_feasible"] = st == 0
pent = sorted(maxsets[0])
results["control_pentad_4subsets_feasible"] = [solve(cover_of(c))[0] == 0 for c in itertools.combinations(pent, 4)]
# all 432 pentads
cert = 0; infeasible = 0
for S in maxsets:
    st, sup, A, b = solve(cover_of(sorted(S)))
    if st == 2:
        infeasible += 1
        if farkas(A, b) is not None:
            cert += 1
results.update(n_pentads=len(maxsets), lp_infeasible=infeasible, exact_farkas_certificates=cert, pure_identity_err=pure_err, mixed_identity_err=mixed_err)
print(results)
json.dump(results, open(os.path.join(ROOT, "data", "w33_strong_umub_certificate.json"), "w"), indent=1, default=str)

# --- exact combinatorial proof attempt: zero forcing on the purity equation  D chi(w) = sum_u chi(u) chi(w-u) phase(u,w)  (|phase| = 1)
# For w with chi(w) = 0 forced, the surviving unordered pairs {u, w-u} (both possibly nonzero, u != w-u) must cancel; a single pair gives
# chi(u) chi(w-u) times (phase1 + phase2) != 0 (two cube roots of unity never sum to 0)  =>  chi(u) = 0 or chi(w-u) = 0: branch.
# u = w - u (u = -w) gives one term chi(-w)^2 => chi(-w) = 0.  A pure state has |chi| <= 1 and sum |chi|^2 = 9 => support >= 9 vectors.
VEC = [u for u in itertools.product(range(3), repeat=4)]
neg = lambda u: tuple((-x) % 3 for x in u)
sub = lambda a, b: tuple((x - y) % 3 for x, y in zip(a, b))
def proj(u):
    c = next(x for x in u if x); inv = pow(c, -1, 3); return tuple((x * inv) % 3 for x in u)
pidx = {p: i for i, p in enumerate(P)}
def zero_force(cover, limit=200000):
    Z0 = {u for u in VEC if any(u) and pidx[proj(u)] in cover}
    stats = dict(nodes=0, survivors=0)
    def rec(Z):
        stats["nodes"] += 1
        if stats["nodes"] > limit:
            return "limit"
        S = [u for u in VEC if u not in Z]
        if len(S) < 9:
            return "dead"
        Sset = set(S)
        changed = True
        while changed:
            changed = False
            for w in list(Z):
                if not any(w):
                    continue
                pairs = set()
                for u in S:
                    v = sub(w, u)
                    if v in Sset and u != v and any(u) or (v in Sset and u != v and not any(u)):
                        if v in Sset and u != v:
                            pairs.add(frozenset((u, v)))
                pairs = {pr for pr in pairs if not any(not any(x) for x in pr) or True}
                # the pair {0, w} is impossible since w in Z; drop pairs containing 0 only if the other is w (not in S anyway)
                if len(pairs) == 0:
                    continue
                if len(pairs) == 1:
                    a, b = tuple(next(iter(pairs)))
                    # branch: a = 0 or b = 0 (with their negatives, chi(-u) = conj chi(u))
                    r1 = rec(Z | {a, neg(a)}) if any(a) else "dead"
                    if r1 in ("alive", "limit"):
                        return r1
                    r2 = rec(Z | {b, neg(b)}) if any(b) else "dead"
                    return r2
        stats["survivors"] += 1
        return "alive"
    out = rec(frozenset(Z0))
    return out, stats["nodes"]
zf = {}
zf["control_4_spread"] = zero_force(cover_of(spread[:4]))
zf["control_pentad_4subset"] = zero_force(cover_of(list(itertools.combinations(pent, 4))[0]))
zf["pentads"] = __import__("collections").Counter(zero_force(cover_of(sorted(S)))[0] for S in maxsets[:24])
print("zero forcing: control 4 spread bases", zf["control_4_spread"], "| control pentad 4-subset", zf["control_pentad_4subset"], "| first 24 pentads", dict(zf["pentads"]))
results["zero_forcing"] = {k: str(v) for k, v in zf.items()}
json.dump(results, open(os.path.join(ROOT, "data", "w33_strong_umub_certificate.json"), "w"), indent=1, default=str)
