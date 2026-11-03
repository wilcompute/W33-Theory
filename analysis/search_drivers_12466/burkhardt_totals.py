"""12530: the Burkhardt quartic from the two-qutrit Weil even sector.  For each sentinel H u H^perp, Pi_H = (1/3) sum_{x in H} D_x is the parity on one tensor factor; on the 5-dim even sector it is a reflection with mirror vector v_H.  Tests:
(1) the 45 mirrors: |<v, v'>| = 0 for disjoint sentinels, 1/2 otherwise; 27 orthogonal frames; (2) the unique quartic invariant F of the reflections (exact null-space dimension 1), and F is singular at all 45 v_H: the 45 nodes of the Burkhardt quartic; control: a random point is not;
(3) point c -> span of its 9 sentinels has rank 3, and F vanishes on it: the 40 j-planes, Hesse configuration on the nodes; line L -> span of its 4 planes, rank 4: the 40 Steiner primes (F restricted should split into 4 planes); (4) the 216 totals: rank of the 5 nodes, Gram determinant, and how the 10 Steiner primes of the codeword S meet;
compared with other 5-sets of mutually non-orthogonal nodes as a control.  usage: py -3 burkhardt_totals.py"""
import collections, itertools, json, runpy
import numpy as np
ns = runpy.run_path("braid_codewords.py")
pts, lines, codewords, w, compose, group, T = (ns[k] for k in ("pts", "lines", "codewords", "w", "compose", "group", "T"))
e = tuple(range(40)); P = group([T(pts[i]) for i in range(40)]); inv8 = [g for g in P if g != e and compose(g, g) == e and sum(g[i] == i for i in range(40)) == 8]
fix = sorted((frozenset(i for i in range(40) if g[i] == i) for g in inv8), key=sorted)
w3 = np.exp(2j * np.pi / 3); tau = w3 ** 2
X = np.roll(np.eye(3), 1, axis=0).astype(complex); Z = np.diag([1, w3, w3 ** 2])
def D1(a, b): return tau ** (a * b % 3) * np.linalg.matrix_power(X, a) @ np.linalg.matrix_power(Z, b)
def D(v): return np.kron(D1(v[0], v[2]), D1(v[1], v[3]))
def parts(f):
    f = sorted(f); a = f[0]; A = {a} | {b for b in f if w(pts[a], pts[b]) != 0}; return frozenset(A), frozenset(set(f) - A)
def span(idx):
    a, b = [pts[i] for i in list(idx)[:2]]
    return {tuple((s * a[k] + t * b[k]) % 3 for k in range(4)) for s in range(3) for t in range(3)}
Par = np.zeros((9, 9), dtype=complex)
for a, b in itertools.product(range(3), repeat=2): Par[3 * ((-a) % 3) + ((-b) % 3), 3 * a + b] = 1
vals, V = np.linalg.eigh((Par + Par.T) / 2); Ev = V[:, np.isclose(vals, 1)]; assert Ev.shape[1] == 5
mir = []
for f in fix:
    H, Hp = parts(f); assert len(H) == 4
    Pi = sum(D(v) for v in span(H)) / 3
    assert np.allclose(Pi @ Pi, np.eye(9)) and np.allclose(Pi @ Pi.conj().T, np.eye(9)), "Pi_H must be a unitary involution"
    r = Ev.conj().T @ Pi @ Ev; ev, U = np.linalg.eigh((r + r.conj().T) / 2)
    assert np.isclose(ev[0], -1) and np.allclose(ev[1:], 1), ev
    mir.append(U[:, 0])
mir = np.array(mir); G = np.abs(mir.conj() @ mir.T)
out = {}
pat = collections.Counter(); ok = True
for a, b in itertools.combinations(range(45), 2):
    d = not (fix[a] & fix[b]); ok &= abs(G[a, b] - (0 if d else 0.5)) < 1e-9
out["mirror_overlaps_0_if_disjoint_half_otherwise"] = bool(ok)
refl = [np.eye(5, dtype=complex) - 2 * np.outer(v, v.conj()) for v in mir]
# quartic invariants of the reflections: exact-rank null space on the 70 monomials
mons = list(itertools.combinations_with_replacement(range(5), 4))
def mono_eval(x): return np.array([np.prod(x[list(m)]) for m in mons])
rng = np.random.default_rng(5)
samples = (rng.normal(size=(160, 5)) + 1j * rng.normal(size=(160, 5)))
rows = []
for R in refl:
    for x in samples[:6]: rows.append(mono_eval(R @ x) - mono_eval(x))
sv = np.linalg.svd(np.array(rows), compute_uv=True); nul = int(np.sum(sv[1] < 1e-9)); out["quartic_invariants_of_all_45_reflections"] = nul
assert nul == 1, nul
c = sv[2][-1].conj(); F = lambda x: mono_eval(x) @ c
out["F_invariant_under_all_45"] = bool(all(abs(F(R @ x) - F(x)) < 1e-8 for R in refl for x in samples[30:33]))
def grad(x):
    g = np.zeros(5, dtype=complex)
    for k, m in enumerate(mons):
        for i in set(m):
            mm = list(m); mult = mm.count(i); mm.remove(i); g[i] += c[k] * mult * np.prod(x[mm])
    return g
# mirrors: in the conjugate frame used by R^T
nodes = mir
out["max_grad_norm_at_45_nodes"] = float(max(np.linalg.norm(grad(v)) for v in nodes)); out["control_grad_norm_random"] = float(np.linalg.norm(grad(samples[50] / np.linalg.norm(samples[50]))))
out["max_F_at_nodes"] = float(max(abs(F(v)) for v in nodes))
# j-planes and Steiner primes
ranks = lambda A: int(np.linalg.matrix_rank(A, tol=1e-8))
planes = []; okp = True; maxF = 0
for c_ in range(40):
    idx = [i for i, f in enumerate(fix) if c_ in f]; assert len(idx) == 9
    A = nodes[idx]; rk = ranks(A); okp &= rk == 3; planes.append(np.linalg.svd(A)[2][:3].conj().T)
    for _ in range(4):
        y = planes[-1] @ (rng.normal(size=3) + 1j * rng.normal(size=3)); maxF = max(maxF, abs(F(y)) / np.linalg.norm(y) ** 4)
out["point_gives_rank_3_span_of_9_nodes"] = bool(okp); out["max_F_on_j_planes"] = float(maxF)
prime_rank = collections.Counter(); primes = []
for L in lines:
    A = np.hstack([planes[p] for p in L]); prime_rank[ranks(A)] += 1
    u, s, vh = np.linalg.svd(A); primes.append(u[:, -1])
out["line_gives_span_rank"] = dict(prime_rank)
out["nodes_in_a_steiner_prime"] = sorted({len({i for i, f in enumerate(fix) if any(p in f for p in L)}) for L in lines})
spread = []
for L in lines:
    A = np.hstack([planes[p] for p in L]); u, _, _ = np.linalg.svd(A); B4 = u[:, :4]
    forms = []
    for p in L:
        Q = B4.conj().T @ planes[p]; _, _, vh = np.linalg.svd(Q.conj().T); forms.append(vh[-1])    # vh[-1] z = 0 on the plane
    r = []
    for _ in range(12):
        z = rng.normal(size=4) + 1j * rng.normal(size=4); r.append(F(B4 @ z) / np.prod([f @ z for f in forms]))
    r = np.array(r); spread.append(float(np.abs(r - r[0]).max() / abs(r[0])))
out["steiner_prime_F_is_product_of_its_4_planes_max_spread"] = max(spread)
# reflection group of a total, by exact action on the 45 mirrors
def on_mirrors(R):
    r = []
    for v in nodes:
        u = R @ v; o = np.abs(nodes.conj() @ u); i = int(np.argmax(o)); assert abs(o[i] - 1) < 1e-8; r.append(i)
    return tuple(r)
mact = [on_mirrors(np.eye(5, dtype=complex) - 2 * np.outer(v, v.conj())) for v in nodes]
out["mirror_action_ok"] = True
def closure(gs, cap=60000):
    idn = tuple(range(45)); seen = {idn}; fr = [idn]
    while fr and len(seen) < cap:
        nx = []
        for g in fr:
            for h in gs:
                k = tuple(h[g[i]] for i in range(45))
                if k not in seen: seen.add(k); nx.append(k)
        fr = nx
    return seen
out["all_45_generate_projective_order"] = len(closure(mact))
# totals
codes = {}
for S in codewords:
    comp = set(range(40)) - set().union(*(set(lines[j]) for j in S)); codes[frozenset(i for i, f in enumerate(fix) if f <= comp)] = S
sig_spread = 0.0; group_order = collections.Counter(); star_ok = True; subsystem = collections.Counter(); subs = set()
tr = collections.Counter(); dets = collections.Counter(); prim_int = collections.Counter(); triple = collections.Counter(); Fmon = collections.Counter()
for C, S in codes.items():
    idx = sorted(C); A = nodes[idx]; tr[ranks(A)] += 1
    Gm = A.conj() @ A.T; dets[round(float(abs(np.linalg.det(Gm))), 6)] += 1
    for a, b, d in itertools.combinations(range(5), 3): triple[round(float(np.angle(Gm[a, b] * Gm[b, d] * Gm[d, a]) / np.pi), 4)] += 1
    A10 = np.array([primes[j] for j in sorted(S)]); prim_int[ranks(A10)] += 1
    grp = len(closure([mact[i] for i in idx])); group_order[grp] += 1
    # phases: the 5 nodes can be rephased so that all mutual inner products are +1/2 (A5 star)
    ph = [1] + [np.conj(Gm[0, k]) / abs(Gm[0, k]) for k in range(1, 5)]
    Gp = np.array([[np.conj(ph[a]) * Gm[a, b] * ph[b] for b in range(5)] for a in range(5)]); star_ok &= np.allclose(np.abs(Gp), (np.eye(5) + 1) / 2) and np.allclose(Gp, (np.eye(5) + 1) / 2)
    # the 15 mirrors of the total's double-six: closure of the 5 under reflection
    orb = set(idx); fr = list(idx)
    while fr:
        nx = []
        for i in fr:
            for j in idx:
                k = mact[j][i]
                if k not in orb: orb.add(k); nx.append(k)
        fr = nx
    subsystem[len(orb)] += 1; subs.add(frozenset(orb))
    # the classical form: map v_i -> e_0 - e_i into sigma_1 = 0 in C^6; F must become a constant times sigma_4
    Dv = np.array([nodes[i] * ph[k] for k, i in enumerate(idx)])              # rephased nodes: mutual inner products +1/2 on the conjugate-linear Gram
    def sigma4(y): return sum(np.prod(y[list(c4)]) for c4 in itertools.combinations(range(6), 4))
    ratios = []
    for _ in range(6):
        cc = rng.normal(size=5) + 1j * rng.normal(size=5); x = Dv.T @ cc
        y = np.zeros(6, dtype=complex); y[0] = cc.sum(); y[1:] = -cc
        ratios.append(F(x) / sigma4(y))
    r = np.array(ratios); sig_spread = max(sig_spread, float(np.abs(r - r[0]).max() / abs(r[0])))
out["F_equals_const_sigma4_max_spread_over_216"] = sig_spread; out["total_reflection_group_order"] = dict(group_order); out["total_is_A5_star_gram"] = bool(star_ok); out["total_mirror_closure_size"] = dict(subsystem); out["distinct_subsystems"] = len(subs)
out["total_node_rank"] = dict(tr); out["total_gram_abs_det"] = {str(k): v for k, v in dets.items()}; out["total_triple_phase_over_pi"] = {str(k): v for k, v in sorted(triple.items())}; out["rank_of_the_10_Steiner_primes_of_S"] = dict(prim_int)
# control: all other 5-sets of pairwise non-orthogonal nodes, a sample
others = collections.Counter(); oth_det = collections.Counter(); rs = np.random.default_rng(9); checked = 0
nonorth = [[b for b in range(45) if b != a and fix[a] & fix[b]] for a in range(45)]
while checked < 3000:
    pick = [int(rs.integers(45))]
    while len(pick) < 5:
        cand = [b for b in nonorth[pick[0]] if all(fix[b] & fix[p] for p in pick) and b not in pick]
        if not cand: break
        pick.append(int(rs.choice(cand)))
    if len(pick) < 5: continue
    fs = frozenset(pick)
    if fs in codes: continue
    A = nodes[sorted(pick)]; others[ranks(A)] += 1; oth_det[round(float(abs(np.linalg.det(A.conj() @ A.T))), 6)] += 1; checked += 1
out["control_other_5_sets_rank"] = dict(others); out["control_other_5_sets_abs_det_top"] = {str(k): v for k, v in oth_det.most_common(6)}
print(json.dumps(out, default=str)); json.dump(out, open("burkhardt_totals.json", "w"), indent=1, default=str)
