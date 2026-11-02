"""12524: the syndrome-controlled Pauli, as an operator identity on the 9-dim space.  Generate the B4 image as 9x9 unitaries; N = the 27 elements acting by scalars on the reducible syndrome.  With Pi_s the P_c
eigenprojectors and X a Pauli with X P_c X^-1 = w P_c (it permutes the syndromes), test for each u in N:
  (i)  u = lam * sum_s Pi_s L^{e(s)}-type: u restricted to syndrome 0 is scalar;
  (ii) after transport by X, the block on syndrome s+1 equals (block on syndrome s)-power law: block_2 ~ block_1^2 up to phase, with block_1 a logical Pauli (Weyl-Heisenberg, traceless unless scalar);
  (iii) the map u -> block_1 is onto the 9 Weyl operators mod phase.
Control: an element of G outside N fails (i).  usage: py -3 syndrome_theorem.py"""
import collections, json, runpy
import numpy as np
tl = runpy.run_path("tl_braid_iso_exact.py")
R, vecs, PM, gen_act, vid, seen, ca = (tl[k] for k in ("R", "vecs", "PM", "gen_act", "vid", "seen", "compose_act"))
v = next(v for v in vecs if any(v) and all(a[vid[v]][0] == vid[v] for a in gen_act)); Pc = PM[vid[v]]
w3 = np.exp(2j * np.pi / 3); Pc3 = Pc @ Pc @ Pc; assert np.allclose(Pc3, Pc3[0, 0] * np.eye(9))
root = Pc3[0, 0] ** (1 / 3); phases = [root * w3 ** k for k in range(3)]
Pi = {x: sum((Pc / x) ** 0 if False else np.linalg.matrix_power(Pc / x, k) for k in range(3)) / 3 for x in phases}
assert all(np.allclose(Pi[x] @ Pi[x], Pi[x]) and abs(np.trace(Pi[x]) - 3) < 1e-8 for x in phases)
Q = {}
for x in phases:
    u_, s_, _ = np.linalg.svd(Pi[x]); Q[x] = u_[:, :3]
act0 = tl["I_act"]; mats = {act0: np.eye(9, dtype=complex)}; fr = [act0]
while fr:
    nx = []
    for a in fr:
        for g, r in zip(gen_act, R[:3]):
            b = ca(g, a)
            if b not in mats: mats[b] = r @ mats[a]; nx.append(b)
    fr = nx
assert len(mats) == 648
rs = [x for x in phases if np.linalg.matrix_rank(np.vstack([np.kron(np.eye(3), Q[x].conj().T @ r @ Q[x]) - np.kron((Q[x].conj().T @ r @ Q[x]).T, np.eye(3)) for r in R[:3]]), tol=1e-8) == 7][0]
others = [x for x in phases if x != rs]
scal = lambda m: np.allclose(m, m[0, 0] * np.eye(m.shape[0]), atol=1e-7)
blk = lambda A, x: Q[x].conj().T @ A @ Q[x]
pp = lambda a: tuple(t[0] for t in a); idp = pp(act0)
N = [a for a, A in mats.items() if scal(blk(A, rs))]; out = dict(elements_scalar_on_reducible_syndrome=len(N))
N = [a for a in N if pp(ca(a, ca(a, a))) == idp]; out["N"] = len(N)
X = next(PM[vid[w_]] for w_ in vecs if any(w_) and not np.allclose(PM[vid[w_]] @ Pc, Pc @ PM[vid[w_]]))
s1, s2 = others
if not np.allclose(X @ Pi[s1] @ X.conj().T, Pi[s2]): X = X @ X
assert np.allclose(X @ Pi[s1] @ X.conj().T, Pi[s2])
Tr = Q[s2].conj().T @ X @ Q[s1]; assert np.allclose(Tr.conj().T @ Tr, np.eye(3))
tr_law = collections.Counter(); weyl = set()
for a in N:
    A = mats[a]; b1 = blk(A, s1); b2 = Tr.conj().T @ blk(A, s2) @ Tr
    t = np.trace(b1.conj().T @ b1 @ b1 ) 
    def same(p, r):
        k = np.trace(r.conj().T @ p) / 3; return abs(abs(k) - 1) < 1e-6
    tr_law[("b2~b1^2", same(b2, b1 @ b1)), ("b2~b1^-1", same(b2, b1.conj().T)), ("b2~b1", same(b2, b1))] += 1
    key = None
    for k in weyl:
        if same(b1, mats_b1[k]): key = k; break
    if key is None:
        if not weyl: mats_b1 = {}
        key = len(weyl); weyl.add(key); mats_b1[key] = b1
out["power_law_counts"] = {str(k): v for k, v in tr_law.items()}; out["distinct_block_ops_mod_phase"] = len(weyl)
ops = list(mats_b1.values()); out["orthogonal_operator_basis"] = all(abs(np.trace(a.conj().T @ b)) < 1e-6 for i, a in enumerate(ops) for b in ops[:i])
outside = [a for a in mats if a not in set(N)]
out["outside_N_scalar_on_reducible"] = sum(scal(blk(mats[a], rs)) for a in outside)
out["reducible_phase"] = str(rs); print(json.dumps(out)); json.dump(out, open("syndrome_theorem.json", "w"), indent=1)
