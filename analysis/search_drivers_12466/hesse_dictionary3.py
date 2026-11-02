"""12521, third part.  (a) T_c-classes of uncovered codewords = flags (Hesse point, direction); of covered ones = (Hesse line, pair of pencil lines).
(b) codeword stabiliser in PSp(4,3) and derived-subgroup orbits, against 2026-08-29 (S5, 108 + 36 + 36 + 36).  (c) syndrome-controlled Weil: the 27-group
N acts by scalars on the 2-dim block and tracelessly (off centre) on the 3-dim blocks; on the reducible syndrome the absolute character is that of the
qutrit Weil representation of SL(2,3) (explicit F, D matrices), control: the irreducible 3-dim block fails the same test.  usage: py -3 hesse_dictionary3.py"""
import collections, itertools, json, runpy
import numpy as np
ns = runpy.run_path("braid_codewords.py")
pts, lines, gens, group, codewords, w, path, compose, lmap, T = (ns[k] for k in ("pts", "lines", "gens", "group", "codewords", "w", "path", "compose", "lmap", "T"))
c = path[4]; G = group(gens[:3]); e = tuple(range(40)); out = {}
Gl = {g: lmap(g) for g in G}; Tc = T(pts[c]); through_c = [j for j, L in enumerate(lines) if c in L]
act = lambda g, S: frozenset(Gl[g][j] for j in S)
flag_u, flag_c = collections.defaultdict(set), collections.defaultdict(set)
for S in codewords:
    st = [g for g in G if act(g, S) == S]
    cls = frozenset({S, act(Tc, S), act(Tc, act(Tc, S))})
    chosen = frozenset(j for j in S if j in through_c)
    I = [g for g in st if g != e and compose(g, g) == e]
    t3 = [g for g in st if g != e and compose(g, compose(g, g)) == e]
    if not chosen:
        fx = [j for j in through_c if Gl[t3[0]][j] == j]; assert len(I) == 1 and len(fx) == 1
        flag_u[(I[0], fx[0])].add(cls)
    else:
        flag_c[(frozenset(I), chosen)].add(cls)
out["uncovered_flags"] = len(flag_u); out["uncovered_classes_per_flag"] = sorted({len(v) for v in flag_u.values()})
out["covered_line_pair_labels"] = len(flag_c); out["covered_classes_per_label"] = sorted({len(v) for v in flag_c.values()})
# (b)
full = group([T(pts[i]) for i in range(40)])
S0 = codewords[0]; lm = {}
prof = collections.Counter()
for g in full:
    if frozenset(lmap(g)[j] for j in S0) == S0:
        p, n = g, 1
        while p != e: p = compose(g, p); n += 1
        prof[n] += 1
out["codeword_stabiliser_in_PSp43"] = dict(sorted(prof.items()))
Gs = list(G); gener = set()
gi = {g: tuple(np.argsort(g).tolist()) for g in gens[:3]}
der = [compose(compose(compose(a, b), tuple(np.argsort(a).tolist())), tuple(np.argsort(b).tolist())) for a, b in itertools.product(gens[:3] + [Tc], repeat=2)]
Dg = {e}; fr = [e]; seeds = list(G)[:60]
comms = set()
for a in seeds:
    for b in seeds:
        comms.add(compose(compose(compose(a, b), tuple(np.argsort(a).tolist())), tuple(np.argsort(b).tolist())))
    if len(comms) > 200: break
D = group(list(comms)[:30]); out["derived_order"] = len(D)
seen, orbs = set(), []
for S in codewords:
    if S in seen: continue
    o = {act(g, S) for g in D}; seen |= o; orbs.append((len(o), any(c in lines[j] for j in S)))
out["derived_orbits_(size,covered)"] = sorted(orbs)
# (c)
tl = runpy.run_path("tl_braid_iso_exact.py")
sn, blocks, ca = tl["seen"], tl["blocks"], tl["compose_act"]; pp = lambda a: tuple(x[0] for x in a); idp = pp(tl["I_act"])
dims = [b.shape[1] for b in blocks]; b1, b2 = dims.index(1), dims.index(2); b3 = dims.index(3)
def is_scalar(m): return np.allclose(m, m[0, 0] * np.eye(m.shape[0]), atol=1e-7)
keys = list(sn); ker2 = [a for a in keys if is_scalar(sn[a][b2])]
out["kernel_on_2_block_projective"] = len(ker2)
N = [a for a in ker2 if pp(ca(a, ca(a, a))) == idp]; out["N_order"] = len(N)
tr3 = collections.Counter(round(float(abs(np.trace(sn[a][b3]))), 5) for a in N); out["N_abs_trace_on_3_block"] = {str(k): v for k, v in tr3.items()}
invs = [a for a in keys if pp(a) != idp and pp(ca(a, a)) == idp]
out["involutions_same_projectively_on_2_block"] = len({tuple(np.round((sn[a][b2] / sn[a][b2][0, 0] if abs(sn[a][b2][0, 0]) > 1e-6 else sn[a][b2]).flatten(), 5).tolist()) for a in invs}) == 1
def abs_prof(traces): return sorted(collections.Counter(round(float(x), 4) for x in traces).items())
syn0 = [abs(np.trace(sn[a][b2]) + np.trace(sn[a][b1])) for a in keys]
out["N_coset_constant_on_syndrome0"] = all(len({round(abs(np.trace(sn[ca(n, a)][b2]) + np.trace(sn[ca(n, a)][b1])), 4) for n in N}) == 1 for a in keys[:40])
w3 = np.exp(2j * np.pi / 3); F = np.array([[w3 ** (j * k) for k in range(3)] for j in range(3)]) / np.sqrt(3); Dm = np.diag([w3 ** (2 * j * j) for j in range(3)])
ws = [np.eye(3, dtype=complex)]; ks = {tuple(np.round(ws[0] / ws[0][0, 0], 5).flatten().tolist())}; fr = ws[:]
def pk(m):
    i = np.argmax(np.abs(m) > 1e-6); return tuple((np.round(m / m.flat[i], 5) + 0).flatten().tolist())
ks = {pk(ws[0])}
while fr:
    nx = []
    for m in fr:
        for g in (F, Dm):
            h = g @ m
            if pk(h) not in ks: ks.add(pk(h)); ws.append(h); nx.append(h)
    fr = nx
out["weil_projective_order"] = len(ws)
wp = abs_prof(abs(np.trace(m)) for m in ws)
scale = len(keys) // (2 * len(ws)) if len(ws) else 0
ours = collections.Counter(round(float(x), 4) for x in syn0)
out["weil_abs_trace_profile"] = wp; out["syndrome0_abs_trace_profile"] = sorted(ours.items())
ctl = collections.Counter(round(float(abs(np.trace(sn[a][b3]))), 4) for a in keys); out["control_3_block_abs_trace_profile"] = sorted(ctl.items())
json.dump(out, open("hesse_dictionary3.json", "w"), indent=1, default=str); print(json.dumps(out, default=str))
