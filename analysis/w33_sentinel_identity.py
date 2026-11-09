"""Item 2 (pen-and-paper proof) + item 1 (the pentad's 9-dim block).
Derivation: for a stabiliser basis, sum_e P_e (x) P_e = (1/9) sum_{g in G_L} g (x) g^dag, so M = sum_e A_e (x) A_e = (1/9) sum_{u in C} W_u (x) W_u^dag
over the 40 covered Pauli vectors C.  SWAP = (1/9) sum_{all u} W_u (x) W_u^dag, so on Sym^2: M = (8 - T_U)/9 with T_U over the 40 uncovered vectors.
P12523: the uncovered 20 points are covered exactly twice by 5 'sentinel' splits {b, b-perp}; each split gives sum_{u in <b> u <b-perp>, u != 0}
W_u (x) W_u^dag = 3 S_A + 3 S_B - 2 with S_A S_B = SWAP = 1 on Sym^2.  Hence M = (13 - 3 R)/9 on Sym^2, R = sum_{k=1}^5 S_k (S_k = S_A^k).
Claim: (R - 4)(R + 1) = 0 on Sym^2, i.e. spec(M) = {1/9, 16/9}.  Checks: (a) exactly 5 splits lie in the uncovered set and cover it twice;
(b) M = (13 - 3R)/9 numerically; (c) (R - 4)(R + 1) = 0; (d) the pairwise structure: S_k S_l + S_l S_k for k != l; (e) the 9-dim block = ker(R + 1).
usage: py -3 analysis/w33_sentinel_identity.py"""
import itertools, json, os
from collections import Counter
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
import contextlib, io
ns = {"__name__": "x", "__file__": os.path.join(HERE, "w33_pentad_umub.py")}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open(os.path.join(HERE, "w33_pentad_umub.py"), encoding="utf-8").read().split("# --- (3)")[0], ns)
P, lines, maxsets, pauli, bases = ns["P"], ns["lines"], ns["maxsets"], ns["pauli"], ns["bases"]
sb = {"__name__": "x", "__file__": os.path.join(HERE, "w33_pass12635_burkhardt_fan.py")}
exec(open(os.path.join(HERE, "w33_pass12635_burkhardt_fan.py"), encoding="utf-8").read().split("res = dict(")[0], sb)
splits = sb["splits"]
d = 9
Sw = np.zeros((81, 81))
for i in range(d):
    for j in range(d):
        Sw[i * d + j, j * d + i] = 1
Pi = (np.eye(81) + Sw) / 2
def span(pts):
    u = P[pts[0]]; v = next(P[q] for q in pts[1:] if not any(all((P[q][t] - x * u[t]) % 3 == 0 for t in range(4)) for x in range(3)))
    return [tuple((a * u[k] + c * v[k]) % 3 for k in range(4)) for a in range(3) for c in range(3)]
def S_local(b):
    return sum(np.kron(pauli(x), pauli(x).conj().T) for x in span(sorted(b))) / 3
res = {}
summary = Counter()
for S_ in maxsets[:432]:
    covered = frozenset().union(*[lines[L] for L in S_])
    unc = frozenset(range(40)) - covered
    sent = [(b, bp) for b, bp in splits if (b | bp) <= unc]
    cover2 = Counter(p for b, bp in sent for p in (b | bp))
    twice = len(sent) == 5 and set(cover2.values()) == {2} and set(cover2) == unc
    summary[("five_sentinels_cover_twice", twice)] += 1
res["sentinels"] = {str(k): v for k, v in summary.items()}
print("(a) exactly 5 sentinel splits covering the 20 uncovered points twice:", dict(summary))
# (b)-(e) on the first pentad
S_ = sorted(maxsets[0])
covered = frozenset().union(*[lines[L] for L in S_]); unc = frozenset(range(40)) - covered
sent = [(b, bp) for b, bp in splits if (b | bp) <= unc]
M = np.zeros((81, 81), complex)
for L in S_:
    for e in bases[L].T:
        A = np.outer(e, e.conj()) - np.eye(d) / d
        M += np.kron(A, A)
Ss = [S_local(b) for b, bp in sent]
R = sum(Ss)
on_sym = lambda X: Pi @ X @ Pi
res["b_M_equals_(13-3R)/9_on_Sym2"] = bool(np.allclose(on_sym(M), on_sym((13 * np.eye(81) - 3 * R) / 9), atol=1e-9))
res["c_(R-4)(R+1)=0_on_Sym2"] = bool(np.allclose(on_sym((R - 4 * np.eye(81)) @ (R + np.eye(81))), 0, atol=1e-9))
anti = Counter()
for k, l in itertools.combinations(range(5), 2):
    A = on_sym(Ss[k] @ Ss[l] + Ss[l] @ Ss[k])
    # express on Sym^2 as a + b(S_k + S_l) + c sum_{m != k,l} S_m ?  least-squares on the 5 S's and identity
    basis = [on_sym(np.eye(81))] + [on_sym(Sm) for Sm in Ss]
    Mt = np.array([B.ravel() for B in basis]).T
    coef, *_ = np.linalg.lstsq(Mt, A.ravel(), rcond=None)
    fit = np.allclose(Mt @ coef, A.ravel(), atol=1e-8)
    anti[(fit, tuple(np.round(coef.real, 6)))] += 1
res["d_anticommutator_structure"] = {str(k): v for k, v in anti.items()}
# (e) the 9-dim block = kernel of R + 1 on Sym^2 ?  compare with the top eigenspace of M
wM, VM = np.linalg.eigh((on_sym(M) + on_sym(M).conj().T) / 2)
top = VM[:, np.abs(wM - 16 / 9) < 1e-6]
wR, VR = np.linalg.eigh((on_sym(R) + on_sym(R).conj().T) / 2)
kerR = VR[:, np.abs(wR + 1) < 1e-6]
res["e_block_is_ker(R+1)"] = bool(top.shape[1] == kerR.shape[1] == 9 and np.allclose(top @ top.conj().T, kerR @ kerR.conj().T, atol=1e-8))
print("(b) M = (13 - 3R)/9 on Sym^2:", res["b_M_equals_(13-3R)/9_on_Sym2"], "| (c) (R-4)(R+1) = 0:", res["c_(R-4)(R+1)=0_on_Sym2"], "| (e) 9-dim block = ker(R+1):", res["e_block_is_ker(R+1)"])
print("(d) S_k S_l + S_l S_k on Sym^2 = a + sum c_m S_m (fit, coefficients [I, S_1..S_5]):", dict(anti))
json.dump(res, open(os.path.join(ROOT, "data", "w33_sentinel_identity.json"), "w"), indent=1, default=str)

# --- Jucys-Murphy test: are the 5 sentinel swaps (restricted to Sym^2) like the star transpositions (k 6) of S6?  orders of S_k S_l, and the
#     order of the group they generate (closure of 45x45 matrices on an orthonormal basis of Sym^2).
B = []
for i in range(d):
    for j in range(i, d):
        v = np.zeros(81, complex)
        if i == j: v[i * d + i] = 1
        else: v[i * d + j] = v[j * d + i] = 1 / np.sqrt(2)
        B.append(v)
B = np.array(B).T
Sr = [B.conj().T @ S @ B for S in Ss]
def order(Mx, cap=30):
    X = Mx.copy()
    for k in range(1, cap + 1):
        if np.allclose(X, np.eye(45), atol=1e-8): return k
        X = X @ Mx
    return None
res["involutions"] = all(np.allclose(S @ S, np.eye(45), atol=1e-8) for S in Sr)
res["pair_orders"] = sorted(Counter(order(Sr[k] @ Sr[l]) for k, l in itertools.combinations(range(5), 2)).items())
# group closure (cap 2000 elements)
key = lambda Mx: tuple(np.round(Mx, 6).ravel()[:120].view(float).round(5))
G = {key(np.eye(45)): np.eye(45)}
frontier = [np.eye(45)]
while frontier and len(G) < 3000:
    nxt = []
    for Mx in frontier:
        for S in Sr:
            Y = Mx @ S
            k_ = key(Y)
            if k_ not in G:
                G[k_] = Y; nxt.append(Y)
    frontier = nxt
res["group_order"] = len(G)
print("involutions:", res["involutions"], "| orders of S_k S_l:", res["pair_orders"], "| order of generated group:", res["group_order"], "(S6 = 720)")
json.dump(res, open(os.path.join(ROOT, "data", "w33_sentinel_identity.json"), "w"), indent=1, default=str)
# redo closure with a full-matrix key (the truncated key collided)
key2 = lambda Mx: hash(np.round(Mx * 1e5).astype(np.int64).tobytes())
G2 = {key2(np.eye(45)): np.eye(45)}
frontier = [np.eye(45)]
while frontier and len(G2) < 5000:
    nxt = []
    for Mx in frontier:
        for S in Sr:
            Y = Mx @ S
            Y = np.round(Y, 9)
            k_ = key2(Y)
            if k_ not in G2:
                G2[k_] = Y; nxt.append(Y)
    frontier = nxt
res["group_order_full_key"] = len(G2)
# character: traces of the generated group elements -> compare with S6 conjugacy class structure via trace multiset of products of generators
print("order of generated group (full key):", len(G2), "(S6 = 720)")
json.dump(res, open(os.path.join(ROOT, "data", "w33_sentinel_identity.json"), "w"), indent=1, default=str)
# Coxeter-type presentation of S6 by star transpositions: t_k^2 = 1, (t_k t_l)^3 = 1, (t_k t_l t_k t_m)^2 = 1 (k, l, m distinct)
I45 = np.eye(45)
rel2 = all(np.allclose(S @ S, I45, atol=1e-8) for S in Sr)
rel3 = all(np.allclose(np.linalg.matrix_power(Sr[k] @ Sr[l], 3), I45, atol=1e-8) for k, l in itertools.permutations(range(5), 2))
relq = all(np.allclose(np.linalg.matrix_power(Sr[k] @ Sr[l] @ Sr[k] @ Sr[m], 2), I45, atol=1e-8) for k, l, m in itertools.permutations(range(5), 3))
# faithfulness: the representation is nontrivial on A6 iff some 3-cycle (t_k t_l) acts nontrivially (true: order 3); S6 has no quotient
# with order-3 images of 3-cycles other than S6 itself, so the group is S6.
tr = dict(identity=45.0, transposition=float(np.trace(Sr[0]).real), three_cycle=float(np.trace(Sr[0] @ Sr[1]).real))
res.update(star_relations=dict(t2=rel2, t3=rel3, quad=relq), traces=tr)
print("star-transposition relations of S6: t^2", rel2, "| (t_k t_l)^3", rel3, "| (t_k t_l t_k t_m)^2", relq, "| traces", tr)
json.dump(res, open(os.path.join(ROOT, "data", "w33_sentinel_identity.json"), "w"), indent=1, default=str)
# the 15 transpositions t_k t_l t_k (k != l) and t_k: are they all swap operators of splits?  which splits?
Sall = [B.conj().T @ S_local(b) @ B for b, bp in splits]
def which(Mx):
    return [s for s, Sm in enumerate(Sall) if np.allclose(Sm, Mx, atol=1e-8)]
sent_idx = [which(S)[0] if which(S) else None for S in Sr]
trans = {}
for k, l in itertools.combinations(range(5), 2):
    trans[(k, l)] = which(Sr[k] @ Sr[l] @ Sr[k])
fifteen = set(sent_idx) | {v[0] for v in trans.values() if v}
res["sentinel_split_indices"] = sent_idx
res["transposition_splits"] = {str(k): v for k, v in trans.items()}
res["fifteen_splits"] = sorted(fifteen)
print("sentinel splits:", sent_idx, "| all 10 conjugate transpositions are split swaps:", all(len(v) == 1 for v in trans.values()), "| distinct splits:", len(fifteen))
# are these 15 the splits swapped by the Kramers reversal of this codeword?  theta = reflection in alpha; on splits: a split is 'swapped' if theta maps b <-> b-perp
json.dump(res, open(os.path.join(ROOT, "data", "w33_sentinel_identity.json"), "w"), indent=1, default=str)
