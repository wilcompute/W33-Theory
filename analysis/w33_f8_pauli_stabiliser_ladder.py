"""Pass 12671: the Pauli-stabiliser ladder of the F_8 regulus minimum (nine MUBs of C^64, CZ model of Pass 12659).
Pass 12660 (w33_f8_minimiser_structure.py) found that the numerical minimiser has a Pauli stabiliser S of order 4, all uncovered.
Here: (1) minimise F restricted to the 16-dim joint eigenspace of S; (2) for every coset R of S in S^perp and both signs, minimise
on the 8-dim eigenspace of <S, R> and count those attaining c8 = (47 - 32cos(2pi/9))/9; (3) from three such rank-3 groups, try every
further commuting Pauli (both signs) and record whether any rank-4 group (4-dim eigenspace) attains c8.
Convention: (P(u,v) psi)[x] = (-1)^{v.(x^u)} psi[x^u], x = 8a + b as six bits.   usage: py -3 analysis/w33_f8_pauli_stabiliser_ladder.py"""
import collections, json, math, os
import numpy as np
from scipy.optimize import minimize
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
src = open(os.path.join(HERE, "w33_regulus_constants_q16_q32.py"), encoding="utf-8").read()
gl = {"__name__": "x", "__file__": os.path.join(HERE, "w33_regulus_constants_q16_q32.py")}
exec(src[: src.index("rng = np.random")], gl)
q, mul, trace = gl["field"](3); _, fg = gl["model"](3)
C8 = (47 - 32 * math.cos(2 * math.pi / 9)) / 9
rng = np.random.default_rng(126710)
pc = lambda n: bin(n).count("1") & 1
Xi = np.array([[1 - 2 * trace(mul(a, b)) for b in range(8)] for a in range(8)], float)
Phi = np.array([[[1 - 2 * trace(mul(t, mul(a, b))) for b in range(8)] for a in range(8)] for t in range(8)], float)


def pauli(u, v):
    M = np.zeros((64, 64), complex)
    for x in range(64): M[x, x ^ u] = (-1) ** pc(v & (x ^ u))
    return M


def herm(k):
    R = pauli(*k); return R if np.allclose(R, R.conj().T) else 1j * R


U = [np.eye(64)]
for t in range(8):
    Ut = np.zeros((64, 64))
    for x in range(64):
        e = np.zeros((8, 8)); e.flat[x] = 1; Ut[:, x] = (Xi @ (e * Phi[t]) @ Xi / 8).ravel()
    U.append(Ut)
covered = lambda k: any(np.allclose(D := Ut @ pauli(*k) @ Ut.T, np.diag(np.diag(D))) for Ut in U)
comm = lambda p, r: (pc(p[0] & r[1]) ^ pc(p[1] & r[0])) == 0


def space(gens):  # gens: list of (label, sign); joint +1 eigenspace of sign * herm(label)
    Pr = np.eye(64, dtype=complex)
    for k, s in gens: Pr = Pr @ (np.eye(64) + s * herm(k)) / 2
    w, V = np.linalg.eigh((Pr + Pr.conj().T) / 2); return V[:, w > 0.5]


def minval(B, n):
    m = B.shape[1]

    def f(w):
        A = B @ (w[:m] + 1j * w[m:]); val, gr = fg(np.concatenate([A.real, A.imag]))
        G = B.conj().T @ (gr[:64] + 1j * gr[64:]); return val, np.concatenate([G.real, G.imag])
    return sorted(minimize(f, rng.standard_normal(2 * m), jac=True, method="L-BFGS-B", options=dict(maxiter=30000, gtol=1e-13, ftol=1e-17)).fun * 64
                  for _ in range(n))


# S = <-i P(12,53), P(53,33)>: the order-4 stabiliser of Pass 12660 in this coordinate system.  herm((12,53)) = +i P(12,53),
# so the minimiser's +1 eigenspace of -i P(12,53) is sign -1 here.
assert np.allclose(herm((12, 53)), 1j * pauli(12, 53))
gS = [((12, 53), -1), ((53, 33), 1)]
Sgrp = [(0, 0), (12, 53), (53, 33), (12 ^ 53, 53 ^ 33)]
assert not any(covered(k) for k in Sgrp[1:]) and comm(Sgrp[1], Sgrp[2])
res = {}
B16 = space(gS); vals16 = minval(B16, 40)
res["rank2"] = dict(dim=B16.shape[1], starts=40, hits=sum(abs(v - C8) < 1e-7 for v in vals16), best=vals16[0])
print("rank 2 (S):", res["rank2"], flush=True)
cos = {}
for u in range(64):
    for v in range(64):
        if all(comm((u, v), s) for s in Sgrp[1:]):
            cos.setdefault(min((u ^ s[0], v ^ s[1]) for s in Sgrp), []).append((u, v))
wts = collections.Counter(sum(covered(p) for p in c) for k, c in cos.items() if k != (0, 0))
res["cosets"] = dict(n=len(cos), covered_weight_histogram={str(k): v for k, v in sorted(wts.items())})
hist = collections.Counter(); hits = []
for k in cos:
    if k == (0, 0): continue
    for s in (1, -1):
        v = minval(space(gS + [(k, s)]), 6)[0]; hist[round(v, 6)] += 1
        if abs(v - C8) < 1e-7: hits.append((k, s))
res["rank3"] = dict(dim=8, groups_tested=2 * (len(cos) - 1), attaining_c8=len(hits), value_histogram={str(k): v for k, v in sorted(hist.items())},
                    hit_cosets_all_uncovered=all(not any(covered(p) for p in cos[k]) for k, _ in hits))
print("rank 3:", res["rank3"], flush=True)
r4 = 0; tested4 = 0
for par in hits[:3]:
    gens = gS + [par]
    for k in cos:
        if k in ((0, 0), par[0]) or not comm(k, par[0]): continue
        for s in (1, -1):
            B = space(gens + [(k, s)])
            if B.shape[1] == 0: continue
            tested4 += 1
            if abs(minval(B, 4)[0] - C8) < 1e-7: r4 += 1
res["rank4"] = dict(parents=3, groups_tested=tested4, attaining_c8=r4)
print("rank 4:", res["rank4"], flush=True)
json.dump(res, open(os.path.join(ROOT, "data", "w33_f8_pauli_stabiliser_ladder.json"), "w"), indent=1)
