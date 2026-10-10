"""Passes 11831-11833: the finite AdS4 of two qutrits.

11831  The omega-traceless bivectors of the Pauli phase space F3^4 form a 5-dim quadratic space whose
       operators J_b = Omega^-1 B obey the Clifford relation J_a J_b + J_b J_a = 2 beta(a,b) I.  Its 121
       points are 40 null = Lagrangian contexts, 45 square = tensor factorisations, 36 non-square =
       Kramers time reversals (Pass 11210).  Orthogonality = anticommutation reproduces Pass 11210 (local
       in 15 splits, always as a swap), Pass 11177 (octet-disjoint = perfect-gate relation, 27 frames) and
       Rounds 23/24 (the 45 apartment sectors are the factorisations, graph J(4,2) x J(4,2)).
11832  The stabiliser of a Kramers reversal is SL(2,9).2 (order statistics of SL(2,9) exact), acting on its
       celestial sphere of 10 invariant Lagrangians = P^1(F9) as S6 = P Sigma L(2,9); splits have
       stabiliser 1152 and contexts 1296 (Spin(2,3) > Spin(1,3), Spin(2,2), parabolic with F9/F3 for C/R).
11833  The tangent space p^perp at a Kramers reversal is a finite Minkowski space: Lorentz orbits
       1 + 20 null + 30 + 30; the spinor map psi -> psi ^ J psi is 4:1 onto the 20 null vectors; the
       light-cone Cayley graph is SRG(81,20,1,6) (Brouwer-Haemers).  Two Kramers reversals compose to a
       Fourier-type element (orthogonal) or a unipotent tick (non-orthogonal); orthonormal 5-frames
       contain an even number of reversals: 27 (0+5), 270 (2+3), 135 (4+1).
"""

import functools
import itertools
import json
from collections import Counter

import numpy as np
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data" / "w33_pass11831_11833_finite_ads4.json"

P = 3
OM = np.array([[0, 0, 1, 0], [0, 0, 0, 1], [2, 0, 0, 0], [0, 2, 0, 0]], dtype=np.int64)  # omega(u,v)=u^T OM v
OMI = (-OM) % P  # OM^-1 = -OM
I4 = np.eye(4, dtype=np.int64)


def m(*a):
    r = a[0]
    for b in a[1:]:
        r = (r @ b) % P
    return r


def key(M):
    return tuple(int(x) for x in (M % P).flatten())


def om(u, v):
    return int(u @ OM @ v) % P


# ---------------- the 5-space of traceless bivectors ----------------
def skew(p):
    B = np.zeros((4, 4), dtype=np.int64)
    for (i, j), x in zip(itertools.combinations(range(4), 2), p):
        B[i, j] = x
        B[j, i] = -x
    return B % P


def proj(J):
    """canonical representative of +-J (first nonzero entry = 1)."""
    f = next(x for x in (J % P).flatten() if x)
    return key(J if f == 1 else (-J) % P)


def scalar_of(M):
    M = M % P
    c = M[0, 0]
    return int(c) if np.array_equal(M, c * I4 % P) else None


POINTS = {}
for p in itertools.product(range(P), repeat=6):
    if not any(p):
        continue
    J = m(OMI, skew(p))
    if int(np.trace(J)) % P:
        continue
    POINTS.setdefault(proj(J), J)
PTS = list(POINTS)
JM = {k: np.array(k, dtype=np.int64).reshape(4, 4) for k in PTS}
Q = {k: scalar_of(m(JM[k], JM[k])) for k in PTS}


@functools.lru_cache(maxsize=None)
def beta(a, b):
    s = scalar_of(m(JM[a], JM[b]) + m(JM[b], JM[a]))
    return None if s is None else (s * 2) % P  # 2*beta = s, 2^-1 = 2 mod 3


KIND = {0: "null", 1: "square", 2: "nonsquare"}


def subspace_key(vecs):
    """canonical key of the span of vecs (all nonzero vectors, sorted)."""
    vecs = [np.array(v, dtype=np.int64) % P for v in vecs]
    span = set()
    for c in itertools.product(range(P), repeat=len(vecs)):
        w = sum(ci * v for ci, v in zip(c, vecs)) % P
        if w.any():
            span.add(tuple(int(x) for x in w))
    return tuple(sorted(span))


VECS = [np.array(v, dtype=np.int64) for v in itertools.product(range(P), repeat=4) if any(v)]


def kernel(M):
    return _kernel(key(M))


@functools.lru_cache(maxsize=None)
def _kernel(k):
    M = np.array(k, dtype=np.int64).reshape(4, 4)
    return [v for v in VECS if not (M @ v % P).any()]


def kspan_list(K):
    """a kernel list already holds every nonzero vector of the subspace."""
    return tuple(sorted(tuple(int(x) for x in v) for v in K))


def kspan(M):
    return kspan_list(kernel(M))


def is_lagrangian(sk):
    vs = [np.array(v) for v in sk]
    return all(om(a, b) == 0 for a in vs for b in vs)


def classify():
    out = {"n_points": len(PTS), "counts": Counter(KIND[Q[k]] for k in PTS if Q[k] is not None)}
    assert all(Q[k] is not None for k in PTS), "J^2 not scalar"
    # Clifford relation on all pairs
    assert all(beta(a, b) is not None for a in PTS for b in PTS), "Clifford relation fails"
    out["clifford_relation_all_pairs"] = True
    lag, fac, kra = set(), set(), 0
    for k in PTS:
        J = JM[k]
        if Q[k] == 0:
            K = kernel(J)
            assert len(K) == 8
            im = {tuple(int(x) for x in (J @ v % P)) for v in VECS} - {(0, 0, 0, 0)}
            sk = tuple(sorted(tuple(int(x) for x in v) for v in K))
            assert set(im) == set(sk) and is_lagrangian(sk)
            lag.add(sk)
        elif Q[k] == 1:
            assert np.array_equal(m(J.T, OM, J), OM)  # symplectic involution
            Ep, Em = kernel(J - I4), kernel(J + I4)
            assert len(Ep) == 8 and len(Em) == 8
            assert all(om(a, b) == 0 for a in Ep for b in Em)
            assert any(om(a, b) for a in Ep for b in Ep)  # nondegenerate
            fac.add(frozenset([kspan_list(Ep), kspan_list(Em)]))
        else:
            assert np.array_equal(m(J.T, OM, J), (-OM) % P)  # anti-symplectic, J^2=-1
            kra += 1
    out.update(lagrangians=len(lag), factorisations=len(fac), kramers=kra)
    return out


# ---------------- Sp(4,3) ----------------
def transvection(v):
    v = v.reshape(4, 1)
    return (I4 - v @ v.T @ OM) % P


def group():
    gens = [transvection(np.array(v)) for v in [(1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1), (1, 1, 0, 0), (1, 0, 0, 1)]]
    for g in gens:
        assert np.array_equal(m(g.T, OM, g), OM)
    seen = {key(I4): I4}
    frontier = [I4]
    while frontier:
        nxt = []
        for h in frontier:
            for g in gens:
                x = m(g, h)
                k = key(x)
                if k not in seen:
                    seen[k] = x
                    nxt.append(x)
        frontier = nxt
    return list(seen.values())


def inv(g):
    return m(OMI, g.T, OM)


def act(g, k):
    return proj(m(g, JM[k], inv(g)))


def order(g):
    x, n = g, 1
    while not np.array_equal(x, I4):
        x, n = m(x, g), n + 1
    return n


def stabilisers(G):
    res = {}
    for kind in (0, 1, 2):
        k0 = next(k for k in PTS if Q[k] == kind)
        orb = {act(g, k0) for g in G}
        stab = [g for g in G if act(g, k0) == k0]
        res[KIND[kind]] = dict(orbit=len(orb), stabiliser=len(stab))
    return res


SL29_ORDERS = {1: 1, 2: 1, 3: 80, 4: 90, 5: 144, 6: 80, 8: 180, 10: 144}


def lorentz(G):
    """stabiliser of one Kramers point: centraliser = SL(2,9), action on its celestial sphere."""
    k0 = next(k for k in PTS if Q[k] == 2)
    J0 = JM[k0]
    stab = [g for g in G if act(g, k0) == k0]
    cent = [g for g in stab if np.array_equal(m(g, J0), m(J0, g))]
    anti = [g for g in stab if np.array_equal(m(g, J0), (-m(J0, g)) % P)]
    cent_orders = Counter(order(g) for g in cent)
    centre = [g for g in cent if all(np.array_equal(m(g, h), m(h, g)) for h in cent[:60])]
    # celestial sphere: J0-invariant 2-planes
    planes = set()
    for a in VECS:
        for b in VECS:
            sk = subspace_key([a, b])
            if len(sk) == 8:
                planes.add(sk)
    inv_planes = [sk for sk in planes if all(tuple(int(x) for x in (J0 @ np.array(v) % P)) in sk for v in sk)]
    # same as null points orthogonal to k0 ?
    nullperp = set()
    for k in PTS:
        if Q[k] == 0 and beta(k, k0) == 0:
            nullperp.add(tuple(sorted(tuple(int(x) for x in v) for v in kernel(JM[k]))))
    idx = {sk: i for i, sk in enumerate(inv_planes)}

    def perm(g):
        return tuple(idx[tuple(sorted(tuple(int(x) for x in (g @ np.array(v) % P)) for v in sk))] for sk in inv_planes)

    perms = {perm(g) for g in stab}

    def porder(p):
        n, x = 1, p
        while x != tuple(range(len(p))):
            x, n = tuple(p[i] for i in x), n + 1
        return n

    image_orders = Counter(porder(p) for p in perms)
    cent_image = {perm(g) for g in cent}
    return dict(
        stabiliser=len(stab), centraliser=len(cent), anticentraliser=len(anti),
        centraliser_element_orders=dict(sorted(cent_orders.items())),
        centraliser_is_SL29_by_order_statistics=dict(cent_orders) == SL29_ORDERS,
        centre_size=len(centre),
        celestial_sphere_size=len(inv_planes), celestial_all_lagrangian=all(is_lagrangian(s) for s in inv_planes),
        celestial_equals_orthogonal_null_points=set(inv_planes) == nullperp,
        image_on_sphere=len(perms), image_of_centraliser=len(cent_image),
        image_element_orders=dict(sorted(image_orders.items())),
        image_is_S6_PSigmaL29=set(image_orders) == {1, 2, 3, 4, 5, 6},
    )


def pair_relations():
    """beta-relations between point classes, and the composition law of two Kramers reversals."""
    rel = Counter()
    for a, b in itertools.combinations(PTS, 2):
        rel[(KIND[Q[a]], KIND[Q[b]]) if Q[a] <= Q[b] else (KIND[Q[b]], KIND[Q[a]]), beta(a, b) != 0] += 1
    k0 = next(k for k in PTS if Q[k] == 2)
    f0 = next(k for k in PTS if Q[k] == 1)
    per = {}
    for name, x0 in (("kramers", k0), ("factorisation", f0)):
        per[name] = {f"{KIND[c]}_{'orth' if o else 'nonorth'}": sum(1 for k in PTS if k != x0 and Q[k] == c and (beta(k, x0) == 0) == o)
                     for c in (0, 1, 2) for o in (True, False)}
    comp = Counter()
    for a, b in itertools.combinations([k for k in PTS if Q[k] == 2], 2):
        M = m(JM[a], JM[b])
        assert np.array_equal(m(M.T, OM, M), OM)  # product of two reversals is symplectic
        bt = beta(a, b)
        if bt == 0:
            comp["orthogonal: M^2=-1 (Fourier type)"] += int(np.array_equal(m(M, M), (-I4) % P))
        else:
            N = (M - bt * I4) % P
            comp["beta!=0: (M-beta)^2=0 (unipotent tick)"] += int(not m(N, N).any() and N.any())
    lines = Counter()
    for a, b in itertools.combinations(PTS, 2):
        if Q[a] == 2 and Q[b] == 2:
            n0 = sum(1 for x, y in [(1, 0), (0, 1), (1, 1), (1, 2)] if Q[proj((x * JM[a] + y * JM[b]) % P)] == 0)
            lines[("orth" if beta(a, b) == 0 else "nonorth", n0)] += 1
    return dict(pair_counts={f"{k[0][0]}-{k[0][1]}|{'nonorth' if k[1] else 'orth'}": v for k, v in sorted(rel.items())},
                per_point=per, kramers_composition=dict(comp),
                kramers_line_null_points={f"{a}:{n}": v for (a, n), v in sorted(lines.items())})


def kramers_locality():
    """Pass 11210: a Kramers reversal is local in exactly 15 of 45 splits, always as a swap.
    Claim: local in split f  <=>  J_p, J_f anticommute (beta=0), and then J_p swaps the two factors."""
    ok, cnt = True, Counter()
    for p in [k for k in PTS if Q[k] == 2]:
        n = 0
        for f in [k for k in PTS if Q[k] == 1]:
            Ep = kspan(JM[f] - I4)
            Em = kspan(JM[f] + I4)
            img = tuple(sorted(tuple(int(x) for x in (JM[p] @ np.array(v) % P)) for v in Ep))
            local = img in (Ep, Em)
            swap = img == Em
            orth = beta(p, f) == 0
            ok &= (local == orth) and (not local or swap)
            n += local
        cnt[n] += 1
    return dict(local_iff_orthogonal_and_always_swap=bool(ok), splits_per_reversal=dict(cnt))


def apartments():
    """Rounds 23/24: 1620 point-C4 apartments, 45 components of 36 under 'share 3 rays'.
    Claim: an apartment = a factorisation plus a pair of rays in each factor, component = factorisation,
    component graph = J(4,2) x J(4,2) (Cartesian)."""
    pts = {}
    for v in VECS:
        f = next(x for x in v if x)
        w = tuple(int(x) for x in (v * (1 if f == 1 else 2) % P))
        pts[w] = np.array(w)
    plist = list(pts)
    col = {(a, b): om(pts[a], pts[b]) == 0 for a in plist for b in plist}
    aps = set()
    for p1 in plist:
        for p2 in plist:
            if p2 == p1 or not col[p1, p2]:
                continue
            for p3 in plist:
                if p3 in (p1, p2) or not col[p2, p3] or col[p1, p3]:
                    continue
                for p4 in plist:
                    if p4 not in (p1, p2, p3) and col[p3, p4] and col[p4, p1] and not col[p2, p4]:
                        aps.add(frozenset([p1, p2, p3, p4]))
    aps = list(aps)
    # factorisation label of an apartment: span of the two non-collinear pairs
    def label(a):
        a = list(a)
        x = a[0]
        y = next(b for b in a[1:] if not col[x, b])
        rest = [b for b in a if b not in (x, y)]
        return frozenset([subspace_key([pts[x], pts[y]]), subspace_key([pts[rest[0]], pts[rest[1]]])])
    labs = Counter(label(a) for a in aps)
    # share-3 graph components
    n = len(aps)
    idx = {a: i for i, a in enumerate(aps)}
    adj = [[] for _ in range(n)]
    for i, a in enumerate(aps):
        for j in range(i + 1, n):
            if len(a & aps[j]) == 3:
                adj[i].append(j)
                adj[j].append(i)
    comp, seen = [], set()
    for i in range(n):
        if i in seen:
            continue
        st, c = [i], []
        seen.add(i)
        while st:
            u = st.pop()
            c.append(u)
            for w in adj[u]:
                if w not in seen:
                    seen.add(w)
                    st.append(w)
        comp.append(c)
    comp_is_label = all(len({label(aps[i]) for i in c}) == 1 for c in comp)
    c0 = comp[0]
    A = np.zeros((len(c0), len(c0)))
    pos = {u: t for t, u in enumerate(c0)}
    for u in c0:
        for w in adj[u]:
            A[pos[u], pos[w]] = 1
    ev = Counter(int(round(x)) for x in np.linalg.eigvalsh(A))
    j42 = {4: 1, 0: 3, -2: 2}
    cart = Counter()
    for a, ma in j42.items():
        for b, mb in j42.items():
            cart[a + b] += ma * mb
    return dict(apartments=n, factorisation_labels=len(labs), apartments_per_label=sorted(set(labs.values())),
                components=len(comp), component_sizes=sorted({len(c) for c in comp}), degree=sorted({len(x) for x in adj}),
                component_equals_factorisation=comp_is_label,
                component_spectrum=dict(sorted(ev.items(), reverse=True)),
                equals_J42_box_J42=dict(ev) == dict(cart))


def frames():
    """orthogonal 5-frames of non-null points (finite Dirac gamma frames) and their composition."""
    nn = [k for k in PTS if Q[k] != 0]
    orth = {a: {b for b in nn if b != a and beta(a, b) == 0} for a in nn}
    hist = Counter()

    def ext(cur, cand):
        if len(cur) == 5:
            hist[sum(1 for x in cur if Q[x] == 2)] += 1
            return
        for c in sorted(cand):
            if c > cur[-1]:
                ext(cur + [c], cand & orth[c])

    for a in nn:
        ext([a], orth[a])
    return {f"{k}_kramers+{5 - k}_splits": v for k, v in sorted(hist.items())}

def octet(f):
    """the 8 projective points of W(3,3) lying in E+ or E- of the split f."""
    pts = set()
    for s in (1, -1):
        for v in kernel((JM[f] - s * I4) % P):
            fz = next(x for x in v if x)
            pts.add(tuple(int(x) for x in (v * (1 if fz == 1 else 2) % P)))
    return frozenset(pts)


def orth_equals_disjoint():
    S = [k for k in PTS if Q[k] == 1]
    oc = {f: octet(f) for f in S}
    assert all(len(o) == 8 for o in oc.values())
    ok = all((beta(a, b) == 0) == (not (oc[a] & oc[b])) for a, b in itertools.combinations(S, 2))
    # 27 all-split orthonormal frames partition the 40 points?
    orth = {a: {b for b in S if b != a and beta(a, b) == 0} for a in S}
    frames = set()
    for a in S:
        for c in itertools.combinations(sorted(orth[a]), 4):
            if all(beta(x, y) == 0 for x, y in itertools.combinations(c, 2)):
                frames.add(frozenset((a,) + c))
    part = all(len(set().union(*[oc[f] for f in fr])) == 40 for fr in frames)
    return dict(orthogonal_iff_octets_disjoint=bool(ok), all_split_frames=len(frames), frames_partition_40_points=bool(part))


def vec_key(J):
    return key(J % P)


def tangent_space(G):
    k0 = next(k for k in PTS if Q[k] == 2)
    J0 = JM[k0]
    cent = [g for g in G if np.array_equal(m(g, J0), m(J0, g))]
    stab = [g for g in G if act(g, k0) == k0]
    # all vectors of the 5-space orthogonal to J0 (as matrices), i.e. traceless self-adjoint J with J J0 + J0 J = 0
    basis_pts = [k for k in PTS if beta(k, k0) == 0]
    vecs = {vec_key(I4 * 0)}
    for k in basis_pts:
        for s in (1, 2):
            vecs.add(vec_key(s * JM[k]))
    vecs = sorted(vecs)
    assert len(vecs) == 81, len(vecs)
    Vm = {v: np.array(v, dtype=np.int64).reshape(4, 4) for v in vecs}
    Qv = {v: scalar_of(m(Vm[v], Vm[v])) for v in vecs}

    def orbits(H):
        seen, sizes = set(), []
        for v in vecs:
            if v in seen:
                continue
            orb = {vec_key(m(g, Vm[v], inv(g))) for g in H}
            seen |= orb
            sizes.append((len(orb), {0: "null", 1: "square", 2: "nonsquare"}[Qv[v]] if any(v) else "zero"))
        return sorted(sizes)

    lorentz_orbits = orbits(cent)
    full_orbits = orbits(stab)
    # light-cone Cayley graph on the 81 vectors: x ~ y iff x - y is a nonzero null vector
    null = [v for v in vecs if any(v) and Qv[v] == 0]
    idx = {v: i for i, v in enumerate(vecs)}
    Adj = np.zeros((81, 81), dtype=int)
    for v in vecs:
        for n in null:
            w = vec_key(Vm[v] + Vm[n])
            Adj[idx[v], idx[w]] = 1
    deg = set(Adj.sum(1))
    A2 = Adj @ Adj
    lam = {A2[i, j] for i in range(81) for j in range(81) if i != j and Adj[i, j]}
    mu = {A2[i, j] for i in range(81) for j in range(81) if i != j and not Adj[i, j]}
    ev = Counter(int(round(x)) for x in np.linalg.eigvalsh(Adj.astype(float)))
    # spinor map psi -> psi ^ J0 psi as an omega-traceless self-adjoint operator
    def spinor_square(psi):
        a, b = psi, (J0 @ psi) % P
        # skew form beta(x,y) = om(x,a) om(y,b) - om(x,b) om(y,a)  -> matrix B ; J = OM^-1 B
        oa, ob = (OM @ a) % P, (OM @ b) % P  # om(x,a) = x . (OM a)
        B = (np.outer(oa, ob) - np.outer(ob, oa)) % P
        return m(OMI, B)
    imgs = Counter()
    equiv = True
    for psi in VECS:
        S = spinor_square(psi)
        assert int(np.trace(S)) % P == 0
        imgs[vec_key(S)] += 1
    for g in cent[::37]:
        for psi in VECS[::7]:
            lhs = spinor_square((g @ psi) % P)
            rhs = m(g, spinor_square(psi), inv(g))
            equiv &= np.array_equal(lhs, rhs)
    image_is_null_cone = set(imgs) == set(null)
    return dict(
        tangent_vectors=81, null_vectors=len(null),
        lorentz_SL29_orbits=lorentz_orbits, full_stabiliser_orbits=full_orbits,
        light_cone_graph=dict(degree=sorted(int(d) for d in deg), lam=sorted(int(x) for x in lam), mu=sorted(int(x) for x in mu),
                              spectrum=dict(sorted(ev.items(), reverse=True))),
        spinor_map=dict(fibre_sizes=sorted(set(imgs.values())), image_is_null_cone=image_is_null_cone,
                        image_size=len(imgs), equivariant_sampled=bool(equiv)),
    )


def main():
    out = {"pass_ids": [11831, 11832, 11833]}
    out["classification"] = {k: (dict(v) if isinstance(v, Counter) else v) for k, v in classify().items()}
    G = group()
    out["group_order"] = len(G)
    out["stabilisers"] = stabilisers(G)
    out["lorentz"] = lorentz(G)
    out["pairs"] = pair_relations()
    out["kramers_locality"] = kramers_locality()
    out["orthogonality_vs_pass11177"] = orth_equals_disjoint()
    out["apartments"] = apartments()
    out["frames"] = frames()
    out["tangent"] = tangent_space(G)
    for k, v in out.items():
        print(k, json.dumps(v, default=str)[:600], flush=True)
    json.dump(out, open(DATA, "w"), indent=1, default=str)


if __name__ == "__main__":
    main()
