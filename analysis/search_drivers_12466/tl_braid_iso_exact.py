"""12516 (exact): Clifford elements are determined mod scalars by their exact action on the 81 two-qutrit Paulis with cube-root phases.
Represent each element of the B4 image of the TL6 / SU(2)_4 braid generators that way, compose in integers, and compare with the
transvection group G (648) on the 40 directions.  The 3-dim irreducible block (Cui-Wang one-qutrit model) is carried as 3x3 matrices
along the BFS tree; its projective image order = |group| / |{elements acting as scalars on the block}|.  usage: py -3 tl_braid_iso_exact.py"""
import json, itertools, collections
import numpy as np
src = open("tl_braid_iso.py", encoding="utf-8").read().split("U4 = generate(R[:3])")[0]
exec(src)
vecs = [tuple(v) for v in itertools.product(range(3), repeat=4)]
vid = {v: i for i, v in enumerate(vecs)}
PM = [pauli(v) for v in vecs]
sixth = [np.exp(2j * np.pi * k / 6) for k in range(6)]
def action(U):
    act = []
    for v in vecs:
        M = U @ PM[vid[v]] @ U.conj().T
        for j, Q in enumerate(PM):
            c = np.trace(Q.conj().T @ M) / 9
            if abs(abs(c) - 1) < 1e-6:
                k = int(np.argmin([abs(c - z) for z in sixth])); act.append((j, k)); break
        else:
            raise ValueError("not Clifford")
    return tuple(act)
gen_act = [action(r) for r in R[:3]]
def compose_act(a, b):                # (a after b): b sends v -> c_b P_j, then a sends P_j -> c_a P_k
    return tuple((a[j][0], (kb + a[j][1]) % 6) for (j, kb) in b)
I_act = tuple((i, 0) for i in range(81))
# blocks from the commutant (as in tl_braid_iso.py)
rows = [np.kron(np.eye(9), r) - np.kron(r.T, np.eye(9)) for r in R[:3]]
K = np.vstack(rows); sv = np.linalg.svd(K); comm_dim = int(np.sum(sv[1] < 1e-8)); ns = sv[2].conj().T[:, -comm_dim:]
rng = np.random.default_rng(0); c = ns @ (rng.normal(size=comm_dim) + 1j * rng.normal(size=comm_dim))
H = c.reshape(9, 9, order="F"); H = H + H.conj().T; vals, V = np.linalg.eigh(H)
groups = collections.defaultdict(list)
for v, i in zip(np.round(vals, 5), range(9)): groups[v].append(i)
blocks = [V[:, idx] for idx in groups.values()]
bgens = [[B.conj().T @ r @ B for r in R[:3]] for B in blocks]
seen = {I_act: [np.eye(B.shape[1], dtype=complex) for B in blocks]}; fr = [I_act]
while fr:
    nx_ = []
    for a in fr:
        for gi, g in enumerate(gen_act):
            b = compose_act(g, a)
            if b not in seen:
                seen[b] = [bg[gi] @ m for bg, m in zip(bgens, seen[a])]; nx_.append(b)
    fr = nx_
order_U4 = len(seen)
# projection to the 40 directions (projective points of F3^4): v and 2v identified
def dir_index(v):
    f = next(x for x in v if x); s = pow(f, -1, 3); return tuple(x * s % 3 for x in v)
dirs = sorted({dir_index(v) for v in vecs if any(v)})
def point_perm(a):
    return tuple(dirs.index(dir_index(vecs[a[vid[d]][0]])) for d in dirs)
pp = {point_perm(a) for a in seen}
def is_scalar(m):
    d = m.shape[0]; return np.allclose(m, m[0, 0] * np.eye(d), atol=1e-7)
block_info = []
for bi, B in enumerate(blocks):
    ker = sum(1 for a, ms in seen.items() if is_scalar(ms[bi]))
    block_info.append(dict(dim=B.shape[1], kernel=ker, projective_image_order=order_U4 // ker))
out = dict(U4_order_mod_scalars=order_U4, point_image_order=len(pp), injective_on_points=(len(pp) == order_U4),
           transvection_group_order=len(group(gens[:3])), commutant_dim=comm_dim, blocks=block_info)
print(json.dumps(out)); json.dump(out, open("tl_braid_iso_exact.json", "w"), indent=1)
