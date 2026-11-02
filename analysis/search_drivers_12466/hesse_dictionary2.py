"""12521, second half (corrects two tests of hesse_dictionary.py, whose 'direction' test was vacuous and whose P_c phases came from mixed blocks):
(1) the real eigenspaces of the conserved Pauli P_c, with the braid rep on each; (2) the direction of a translation = the line through c it fixes
POINTWISE, against the pair of lines through c chosen by a covered codeword; (3) the 12 duals of the Hesse lines are 4 MUBs (control: overlaps 0, 1/3,
not 1/4).  usage: py -3 hesse_dictionary2.py"""
import collections, itertools, json, runpy
import numpy as np
ns = runpy.run_path("braid_codewords.py")
pts, lines, gens, group, codewords, w, path, compose, lmap, T = (ns[k] for k in ("pts", "lines", "gens", "group", "codewords", "w", "path", "compose", "lmap", "T"))
c = path[4]; G = group(gens[:3]); e = tuple(range(40)); out = dict(c=c)
Gl = {g: lmap(g) for g in G}; Tc = T(pts[c]); through_c = [j for j, L in enumerate(lines) if c in L]
inv = [g for g in G if g != e and compose(g, g) == e]
rel = collections.Counter(); perline = collections.defaultdict(collections.Counter)
for S in codewords:
    chosen = frozenset(j for j in S if j in through_c)
    if not chosen: continue
    st = [g for g, l in Gl.items() if frozenset(l[j] for j in S) == S]
    t3 = [g for g in st if g != e and compose(g, compose(g, g)) == e]
    assert len(t3) == 2 and len(chosen) == 2
    g = t3[0]
    fixed_ptwise = [j for j in through_c if all(g[p] == p for p in lines[j])]
    moved_pencil = [j for j in through_c if Gl[g][j] != j]
    rel[(tuple(sorted(chosen)) , tuple(fixed_ptwise))] += 1
    out.setdefault("order3_fixes_pencil", set()).add(len(moved_pencil) == 0)
    out.setdefault("pointwise_fixed_count", set()).add(len(fixed_ptwise))
    if fixed_ptwise: out.setdefault("direction_in_chosen_pair", collections.Counter())[fixed_ptwise[0] in chosen] += 1
out = {k: (sorted(v) if isinstance(v, set) else {str(a): b for a, b in v.items()} if isinstance(v, collections.Counter) else v) for k, v in out.items()}
out["codewords_per_pair_and_direction"] = sorted(set(rel.values()))
tl = runpy.run_path("tl_braid_iso_exact.py")
R, vecs, PM, gen_act, vid, seen, blocks = (tl[k] for k in ("R", "vecs", "PM", "gen_act", "vid", "seen", "blocks"))
v = next(v for v in vecs if any(v) and all(a[vid[v]][0] == vid[v] for a in gen_act)); Pc = PM[vid[v]]
out["Pc_commutes_with_generators"] = [bool(np.allclose(r @ Pc, Pc @ r)) for r in R[:3]]
ev, U = np.linalg.eig(Pc); vals = collections.defaultdict(list)
for i, x in enumerate(ev): vals[complex(np.round(x, 6))].append(i)
spaces = []
for x, idx in vals.items():
    Q, _ = np.linalg.qr(U[:, idx]); rs = [Q.conj().T @ r @ Q for r in R[:3]]
    leak = max(np.linalg.norm(r @ Q - Q @ (Q.conj().T @ r @ Q)) for r in R[:3])
    d = len(idx); K = np.vstack([np.kron(np.eye(d), m) - np.kron(m.T, np.eye(d)) for m in rs]); comm = int(np.sum(np.linalg.svd(K)[1] < 1e-8))
    spaces.append(dict(eigenvalue_phase=round(float(np.angle(x) / (2 * np.pi / 3)), 6), dim=d, leak=round(float(leak), 9), commutant_dim=comm, traces_R0=str(np.round(np.trace(rs[0]), 5)), traces_R0R1=str(np.round(np.trace(rs[0] @ rs[1]), 5))))
out["Pc_eigenspaces"] = spaces
I_act = tl["I_act"]; ca = tl["compose_act"]; pp = lambda a: tuple(x[0] for x in a); idp = pp(I_act)
invs = [a for a in seen if pp(a) != idp and pp(ca(a, a)) == idp]
bi = next(i for i, b in enumerate(blocks) if b.shape[1] == 3)
vs = {}
for a in invs:
    m = seen[a][bi]; ev2, V = np.linalg.eig(m)
    i0 = next(i for i in range(3) if sum(abs(ev2[i] - ev2[j]) < 1e-7 for j in range(3)) == 1)
    vs[a] = V[:, i0] / np.linalg.norm(V[:, i0])
keys = list(vs)
lines_ = []
for a, b, d in itertools.combinations(keys, 3):
    A = np.array([vs[a], vs[b], vs[d]]).T
    if np.linalg.matrix_rank(A, tol=1e-7) == 2: lines_.append((a, b, d))
out["collinear_SIC_triples_rank2"] = len(lines_)
duals = []
for t in lines_:
    A = np.array([vs[x] for x in t]).conj(); duals.append(np.linalg.svd(A)[2].conj().T[:, -1])
ov = collections.Counter(round(float(abs(np.vdot(x, y)) ** 2), 6) for x, y in itertools.combinations(duals, 2))
out["dual_state_overlaps"] = {str(k): n for k, n in ov.items()}
ov2 = collections.Counter(round(float(abs(np.vdot(x, vs[k])) ** 2), 6) for x in duals for k in keys)
out["dual_vs_SIC_overlaps"] = {str(k): n for k, n in ov2.items()}
json.dump(out, open("hesse_dictionary2.json", "w"), indent=1, default=str); print(json.dumps(out, default=str))
