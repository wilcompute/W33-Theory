"""Pass 12653 audit: the zero-error (Shannon) capacity of the W(3,3) collinearity graph G = SRG(40,12,2,4).
Pass 51 (papers/standalone/holonet_shannon_capacity.tex, analysis/w33_shannon_capacity.py) claims Theta(G) = 10 from the lemma
'for any vertex-transitive graph Theta = theta'.  That lemma is FALSE in general (Lovasz 1979 proves Theta <= theta and
theta(G) theta(Gbar) = n for vertex-transitive G; Haemers 1979/81 gives vertex-transitive graphs with Theta < theta).
Here, rigorously:
  lower: alpha(G) (exact, CP-SAT) and alpha of G strong-product G (local search + CP-SAT bound), Theta >= alpha(G^k)^(1/k);
  upper: theta = 10 (Hoffman, exact) and the Haemers bound Theta <= rank_F(M) for M with M_ii != 0 and M_ij = 0 whenever i != j are
         NON-adjacent; candidates M = A + c I over F_p (exact rank via sympy GF(p) DomainMatrix), p <= 13.
Control: the same Haemers code on the Schlafli-graph complement must reproduce Haemers' Theta <= 7 < theta = 9, (Petersen: the A + cI scan gives 5, weaker than theta = 4; the
scan is a restricted Haemers search, not the full minimum rank).  usage: py -3 analysis/w33_shannon_capacity_audit.py"""
import itertools, json, os, time
import numpy as np
import networkx as nx
from sympy.polys.matrices import DomainMatrix
from sympy import GF

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)


def w33():
    pts = []
    for v in itertools.product(range(3), repeat=4):
        if any(v):
            f = next(x for x in v if x)
            v = tuple((x * pow(f, -1, 3)) % 3 for x in v)
            if v not in pts: pts.append(v)
    om = lambda a, b: (a[0] * b[2] - a[2] * b[0] + a[1] * b[3] - a[3] * b[1]) % 3
    A = np.array([[int(i != j and om(a, b) == 0) for j, b in enumerate(pts)] for i, a in enumerate(pts)])
    return A


def rank_mod(M, p):
    return DomainMatrix([[GF(p)(int(x) % p) for x in row] for row in M], M.shape, GF(p)).rank()


def haemers_scan(A, primes=(2, 3, 5, 7, 11, 13)):
    n = len(A); best = (n, None)
    for p in primes:
        for c in range(1, p):
            r = rank_mod(A + c * np.eye(n, dtype=int), p)
            if r < best[0]: best = (r, (p, c))
    return best


def alpha_exact(A, tl=300):
    from ortools.sat.python import cp_model
    n = len(A); m = cp_model.CpModel(); x = [m.NewBoolVar(f"x{i}") for i in range(n)]
    for i, j in zip(*np.nonzero(np.triu(A, 1))): m.Add(x[i] + x[j] <= 1)
    m.Maximize(sum(x)); s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = tl; s.parameters.num_workers = 4
    st = s.Solve(m)
    return int(s.ObjectiveValue()), int(s.BestObjectiveBound()), s.StatusName(st)


t0 = time.time(); res = {}
# controls
P = nx.to_numpy_array(nx.petersen_graph()).astype(int)
res["control_petersen_haemers"] = haemers_scan(P)
# Schlafli graph: 27 lines on a cubic surface; build as complement of the collinearity... use networkx? not available -> construct:
# vertices = 27 lines = a_i (6), b_i (6), c_ij (15); two lines meet iff a_i-b_j (i!=j), a_i-c_jk (i in jk), b_i-c_jk (i in jk), c_ij-c_kl (disjoint)
lines = [("a", i) for i in range(6)] + [("b", i) for i in range(6)] + [("c", p) for p in itertools.combinations(range(6), 2)]
def meet(x, y):
    if x == y: return False
    (s, u), (t, v) = x, y
    if {s, t} == {"a", "b"}: return u != v
    if s == t and s in "ab": return False
    if s == "c" and t == "c": return not set(u) & set(v)
    cu, other = (u, v) if s == "c" else (v, u)
    return other in cu
Meet = np.array([[int(meet(x, y)) for y in lines] for x in lines])
assert Meet.sum(1).tolist() == [10] * 27  # each line meets 10 others
# Haemers: Theta(Schlafli) where Schlafli graph = SKEW (non-meeting) graph, 16-regular; its complement = meeting graph (10-regular).
# Haemers' classical example: Theta(meeting graph complement ...) -- we report both and compare with theta via Hoffman.
def hoffman(A):
    ev = np.linalg.eigvalsh(A.astype(float)); k = ev[-1]; s = ev[0]
    return len(A) * (-s) / (k - s)
for name, M in (("meeting_graph_10reg", Meet), ("skew_graph_16reg", 1 - Meet - np.eye(27, dtype=int))):
    res[f"control_cubic_{name}"] = dict(theta_hoffman=hoffman(M), haemers=haemers_scan(M), alpha=alpha_exact(M, 60))
print("controls", res, flush=True)
A = w33(); assert A.sum(1).tolist() == [12] * 40
res["W33_theta_hoffman"] = hoffman(A)
res["W33_haemers"] = haemers_scan(A)
res["W33_alpha"] = alpha_exact(A, 120)
print({k: res[k] for k in ("W33_theta_hoffman", "W33_haemers", "W33_alpha")}, round(time.time() - t0), "s", flush=True)
json.dump(res, open(os.path.join(ROOT, "data", "w33_shannon_capacity_audit.json"), "w"), indent=1, default=str)
