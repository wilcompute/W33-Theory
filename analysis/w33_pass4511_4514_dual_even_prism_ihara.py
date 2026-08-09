#!/usr/bin/env python3
"""Passes 4511, 4513--4514, 4516--4518.

Exact W(3,3) continuation after Passes 4495--4502:

4511  The 84,240 weight-4 words of the apartment-code dual span exactly the
      1,580-dimensional even-weight subcode.  Together with any odd weight-3
      prism word they generate all C^perp (dimension 1,581).  PGSp has nine
      weight-4 orbits; one PSp-regular orbit of size 25,920 already spans the
      whole even subcode and supplies all 366 dimensions missing from the
      prism span.
4513  The protected 240-orbit of Pass 4502 is identified by an explicit map:
      it is exactly {A_*(e_i+e_j): i~j}.  Hence it is the dual-W33 edge action,
      not an identification by cardinality.
4514  Primitive signed Hashimoto/Ihara Walsh polynomials C6,C7,C8 are computed
      exactly by a meet-in-the-middle diagonal trace plus PSp orbit transport.
      The certificate records all nonzero parity-support orbits and aggregate
      support-size profiles.
4516  The 2,160 triangular prisms form a 9-sheeted equivariant fiber over the
      240 edges.  An edge stabilizer of order 108 acts on its nine-prism fiber
      through 3^2:C4 of order 36, with kernel C3.
4517  A single weight-4 relation with trivial PSp stabilizer generates the full
      even dual subcode under its regular 25,920-element orbit.
4518  The degree-2 Walsh layer of C6 is zeta tomography: coefficient 252 on
      adjacent line pairs and 48 on disjoint pairs, so it reconstructs A_*.

All statements are finite binary combinatorics / graph zeta coefficients.  No
physical gauge field or E8-root identification is inferred.
"""
from __future__ import annotations

import itertools
import json
import math
from collections import Counter, defaultdict, deque
from pathlib import Path

import numpy as np

from w33_pass4495_4502_distance_prism_reconstruction import (
    J3, build_line_perm, geometry, perm_group, transvection3
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "PART_W33_PASS4511_4518_DUAL_EVEN_PRISM_IHARA.json"


def add_basis(piv: dict[int, int], x: int) -> bool:
    y = int(x)
    while y:
        p = y.bit_length() - 1
        if p in piv:
            y ^= piv[p]
        else:
            piv[p] = y
            return True
    return False


def rank_bits(rows) -> int:
    piv = {}
    for x in rows:
        add_basis(piv, int(x))
    return len(piv)


def compose(p, q):
    return tuple(p[q[i]] for i in range(len(q)))


def perm_mask(m: int, p) -> int:
    out = 0
    y = int(m)
    while y:
        b = y & -y
        i = b.bit_length() - 1
        out |= 1 << p[i]
        y -= b
    return out


def orbit_mask(seed: int, gens) -> set[int]:
    seen = {int(seed)}
    q = deque([int(seed)])
    while q:
        x = q.popleft()
        for g in gens:
            y = perm_mask(x, g)
            if y not in seen:
                seen.add(y)
                q.append(y)
    return seen


def orbit_support(seed, gens):
    seen = {tuple(seed)}
    q = deque([tuple(seed)])
    while q:
        x = q.popleft()
        for g in gens:
            y = tuple(sorted(g[i] for i in x))
            if y not in seen:
                seen.add(y)
                q.append(y)
    return seen


def graph_inv(mask: int, A: np.ndarray):
    vs = [i for i in range(len(A)) if (mask >> i) & 1]
    deg = sorted(sum(int(A[x, y]) for y in vs if y != x) for x in vs)
    edges = sum(int(A[x, y]) for x, y in itertools.combinations(vs, 2))
    triangles = sum(
        1 for t in itertools.combinations(vs, 3)
        if all(A[x, y] for x, y in itertools.combinations(t, 2))
    )
    seen = set(); comps = []
    for x in vs:
        if x in seen:
            continue
        stack = [x]; seen.add(x); n = 0
        while stack:
            a = stack.pop(); n += 1
            for y in vs:
                if y not in seen and A[a, y]:
                    seen.add(y); stack.append(y)
        comps.append(n)
    return {
        "support_size": len(vs), "induced_edges": edges,
        "degree_sequence": deg, "triangles": triangles,
        "component_sizes": sorted(comps),
    }


def relation_inv(supp, apmasks, A):
    masks = [apmasks[i] for i in supp]
    ints = sorted((masks[a] & masks[b]).bit_count()
                  for a, b in itertools.combinations(range(4), 2))
    union = 0
    for m in masks:
        union |= m
    inv = graph_inv(union, A)
    mult = Counter()
    for i in range(40):
        if (union >> i) & 1:
            mult[sum((m >> i) & 1 for m in masks)] += 1
    return {
        "union_lines": union.bit_count(),
        "apartment_intersections": ints,
        "union_edges": inv["induced_edges"],
        "union_degree_sequence": inv["degree_sequence"],
        "union_triangles": inv["triangles"],
        "line_multiplicity": {str(k): v for k, v in sorted(mult.items())},
    }


def point_perm(M, pts, pidx):
    out = []
    for p in pts:
        y = (np.asarray(M, dtype=int) @ np.asarray(p, dtype=int)) % 3
        z = tuple(int(a) for a in y)
        for a in z:
            if a:
                inv = 1 if a == 1 else 2
                z = tuple((inv * b) % 3 for b in z)
                break
        out.append(pidx[z])
    return tuple(out)


def build_groups(pts, pidx, lines):
    all_data = []
    for v in pts:
        M = transvection3(v)
        all_data.append((point_perm(M, pts, pidx), build_line_perm(M, pts, pidx, lines)))
    selected = []
    current = {tuple(range(40))}
    for pp, lp in all_data:
        trial = perm_group([x[1] for x in selected] + [lp])
        if len(trial) > len(current):
            selected.append((pp, lp)); current = trial
        if len(current) == 25920:
            break
    assert len(current) == 25920
    outer3 = np.diag([1, 2, 1, 2]) % 3
    outerp = build_line_perm(outer3, pts, pidx, lines)
    pgsp = perm_group([x[1] for x in selected] + [outerp])
    assert len(pgsp) == 51840
    return selected, current, outerp, pgsp


def point_graph(lines):
    A = np.zeros((40, 40), dtype=np.uint8)
    edge_line = {}
    for li, L in enumerate(lines):
        for u, v in itertools.combinations(sorted(L), 2):
            A[u, v] = A[v, u] = 1
            edge_line[(min(u, v), max(u, v))] = li
    return A, edge_line


def diagonal_nb_poly(start, n, dedges, nexts, revnexts):
    def half(steps, reverse=False):
        trans = revnexts if reverse else nexts
        cur = {(start, 0): 1}
        for _ in range(steps):
            nxt = defaultdict(int)
            for (st, mask), c in cur.items():
                for j, li in trans[st]:
                    nxt[(j, mask ^ (1 << li))] += c
            cur = nxt
        by = defaultdict(Counter)
        for (st, mask), c in cur.items():
            by[st][mask] += c
        return by
    a = n // 2; b = n - a
    f = half(a, False); r = half(b, True)
    out = Counter()
    for st in set(f) & set(r):
        for ma, ca in f[st].items():
            for mb, cb in r[st].items():
                out[ma ^ mb] += ca * cb
    return out


def global_orbit_coeffs(basepoly, line_gens):
    remaining = set(basepoly)
    rows = []
    while remaining:
        seed = next(iter(remaining))
        orb = orbit_mask(seed, line_gens)
        s = sum(basepoly.get(m, 0) for m in orb)
        num = 480 * s
        assert num % len(orb) == 0
        rows.append((orb, num // len(orb)))
        remaining -= orb
    return rows


def main() -> int:
    pts, pidx, lines, Astar, apartments, apmasks, H = geometry()
    apidx = {m: i for i, m in enumerate(apmasks)}

    # Weight-3 dual words: triangular-prism relations.
    triples = []
    for i in range(1620):
        mi = apmasks[i]
        for j in range(i + 1, 1620):
            k = apidx.get(mi ^ apmasks[j])
            if k is not None and j < k:
                triples.append((i, j, k))
    assert len(triples) == 2160
    prism_rows = [(1 << a) | (1 << b) | (1 << c) for a, b, c in triples]
    prism_basis = {}
    for x in prism_rows:
        add_basis(prism_basis, x)
    assert len(prism_basis) == 1215

    # Weight-4 dual words by equal apartment-pair XORs.
    buckets = defaultdict(list)
    for i in range(1620):
        mi = apmasks[i]
        for j in range(i + 1, 1620):
            buckets[mi ^ apmasks[j]].append((i, j))
    w4 = set()
    for pairs in buckets.values():
        if len(pairs) < 2:
            continue
        for a in range(len(pairs)):
            i, j = pairs[a]
            for b in range(a + 1, len(pairs)):
                r, s = pairs[b]
                if len({i, j, r, s}) == 4:
                    w4.add((1 << i) | (1 << j) | (1 << r) | (1 << s))
    assert len(w4) == 84240
    w4_basis = {}
    for x in w4:
        add_basis(w4_basis, x)
    assert len(w4_basis) == 1580
    combined = prism_basis.copy()
    for x in w4:
        add_basis(combined, x)
    assert len(combined) == 1581

    selected, psp, outerp, pgsp = build_groups(pts, pidx, lines)
    line_gens = [x[1] for x in selected]
    apgens = []
    for lp in line_gens + [outerp]:
        apgens.append(tuple(apidx[perm_mask(m, lp)] for m in apmasks))
    psp_apgens = apgens[:-1]; pg_apgens = apgens

    w4_supports = {tuple(i for i in range(1620) if (x >> i) & 1) for x in w4}
    def classify_orbits(gens):
        rem = set(w4_supports); out = []
        while rem:
            o = orbit_support(next(iter(rem)), gens)
            assert o <= w4_supports
            out.append(o); rem -= o
        return out
    psp_orbits = classify_orbits(psp_apgens)
    pg_orbits = classify_orbits(pg_apgens)
    assert sorted(map(len, psp_orbits)) == [1620,1620,3240,6480,6480,6480,6480,12960,12960,25920]
    assert sorted(map(len, pg_orbits)) == [1620,1620,3240,6480,6480,12960,12960,12960,25920]

    pg_profile = []
    for o in pg_orbits:
        vals = [sum(1 << i for i in s) for s in o]
        b = prism_basis.copy()
        for x in vals:
            add_basis(b, x)
        rep = next(iter(o))
        row = {
            "orbit_size": len(o), "span_rank": rank_bits(vals),
            "gain_over_prism_span": len(b) - 1215,
            **relation_inv(rep, apmasks, Astar),
        }
        pg_profile.append(row)
    pg_profile.sort(key=lambda d: (d["orbit_size"], d["union_lines"], d["union_edges"], d["union_triangles"]))

    regular = [o for o in psp_orbits if len(o) == 25920]
    assert len(regular) == 1
    regular_vals = [sum(1 << i for i in s) for s in regular[0]]
    assert rank_bits(regular_vals) == 1580
    regular_inv = relation_inv(next(iter(regular[0])), apmasks, Astar)

    # Pass 4513: prism image = edge image exactly.
    edge_images = {}
    edges = []
    for i, j in itertools.combinations(range(40), 2):
        if Astar[i, j]:
            edges.append((i, j))
            b = np.zeros(40, dtype=np.uint8); b[i] = b[j] = 1
            y = (Astar @ b) % 2
            edge_images[sum(int(z) << k for k, z in enumerate(y))] = (i, j)
    assert len(edge_images) == len(edges) == 240
    fibers = defaultdict(list)
    for a, b, c in triples:
        u = apmasks[a] | apmasks[b] | apmasks[c]
        bv = np.array([(u >> i) & 1 for i in range(40)], dtype=np.uint8)
        y = (Astar @ bv) % 2
        ym = sum(int(z) << k for k, z in enumerate(y))
        assert ym in edge_images
        e = edge_images[ym]
        assert not ((u >> e[0]) & 1) and not ((u >> e[1]) & 1)
        vs = [i for i in range(40) if (u >> i) & 1]
        assert sorted(sum(int(Astar[x, v]) for v in vs) for x in e) == [3, 3]
        fibers[e].append(u)
    assert len(fibers) == 240 and {len(v) for v in fibers.values()} == {9}

    def edge_suborbits(group, base):
        stab = [p for p in group if tuple(sorted((p[base[0]], p[base[1]]))) == base]
        rem = set(edges); sizes = []
        while rem:
            e = next(iter(rem))
            o = {tuple(sorted((p[e[0]], p[e[1]]))) for p in stab}
            sizes.append(len(o)); rem -= o
        return len(stab), sorted(sizes)
    psp_stab, psp_sub = edge_suborbits(psp, edges[0])
    pg_stab, pg_sub = edge_suborbits(pgsp, edges[0])
    assert (psp_stab, psp_sub) == (108, [1,1,2,2,18,18,18,18,27,27,54,54])
    assert (pg_stab, pg_sub) == (216, [1,1,4,18,18,18,18,27,27,108])

    # Pass 4516: nine-prism fiber action.
    base_edge = edges[0]; fiber = fibers[base_edge]; fidx = {u:i for i,u in enumerate(fiber)}
    estabs = [p for p in psp if tuple(sorted((p[base_edge[0]], p[base_edge[1]]))) == base_edge]
    fperms = set()
    for p in estabs:
        fperms.add(tuple(fidx[perm_mask(u, p)] for u in fiber))
    assert len(fperms) == 36 and len(estabs) == 108
    def porder(p):
        seen = [False]*len(p); ans = 1
        for i in range(len(p)):
            if not seen[i]:
                j=i; n=0
                while not seen[j]: seen[j]=True; n+=1; j=p[j]
                ans=math.lcm(ans,n)
        return ans
    orders = Counter(porder(p) for p in fperms)
    assert orders == Counter({4:18,2:9,3:8,1:1})
    identity = tuple(range(9)); translations = {identity} | {p for p in fperms if porder(p)==3}
    assert len(translations)==9
    assert all(compose(a,b) in translations for a in translations for b in translations)
    assert len({p[0] for p in translations})==9
    point_stab = [p for p in fperms if p[0]==0]
    assert len(point_stab)==4 and Counter(porder(p) for p in point_stab)==Counter({4:2,2:1,1:1})

    # Pass 4514: exact primitive Ihara/Walsh support orbits C6--C8.
    Apoint, edge_line = point_graph(lines)
    adj = [list(np.flatnonzero(Apoint[i])) for i in range(40)]
    dedges=[]; didx={}
    for u in range(40):
        for v in adj[u]: didx[(u,int(v))]=len(dedges); dedges.append((u,int(v)))
    nexts=[[] for _ in dedges]
    state_line=[]
    for u,v in dedges: state_line.append(edge_line[(min(u,v),max(u,v))])
    for i,(u,v) in enumerate(dedges):
        for w in adj[v]:
            if int(w)!=u:
                j=didx[(v,int(w))]; nexts[i].append((j,state_line[j]))
    rev=[[] for _ in dedges]
    for i,lst in enumerate(nexts):
        for j,_ in lst: rev[j].append((i,state_line[j]))
    # Verify directed-edge transitivity under the same PSp generators.
    base = dedges[0]; seen={base}; q=deque([base])
    point_gens=[x[0] for x in selected]
    while q:
        e=q.popleft()
        for g in point_gens:
            y=(g[e[0]],g[e[1]])
            if y not in seen: seen.add(y); q.append(y)
    assert len(seen)==480

    prime_orbits = {}
    total_expected = {5:36288,6:302880,7:2739840,8:26750160}
    for n in (5,6,7,8):
        basepoly = diagonal_nb_poly(0,n,dedges,nexts,rev)
        rows = global_orbit_coeffs(basepoly,line_gens)
        entries=[]
        for orb,cg in rows:
            rep=next(iter(orb)); val=cg
            if n==6 and rep==0: val-=960
            if n==8 and rep==0: val-=13920
            assert val % n == 0
            coeff=val//n
            if coeff:
                entries.append({"mask_orbit_size":len(orb),"coefficient":coeff,**graph_inv(rep,Astar)})
        assert sum(x["mask_orbit_size"]*x["coefficient"] for x in entries)==total_expected[n]
        prime_orbits[str(n)] = sorted(entries,key=lambda x:(x["support_size"],x["induced_edges"],x["coefficient"],x["mask_orbit_size"]))
    # Independent regression against Pass 4497 C5 decomposition.
    assert [(x["mask_orbit_size"],x["coefficient"],x["support_size"],x["induced_edges"])
            for x in prime_orbits["5"]] == [(2160,12,3,2),(5184,2,5,5)]

    support_summary={}
    for n in (6,7,8):
        d=defaultdict(lambda:{"PSp_orbits":0,"distinct_masks":0,"primitive_prime_classes":0})
        for x in prime_orbits[str(n)]:
            z=d[x["support_size"]];z["PSp_orbits"]+=1;z["distinct_masks"]+=x["mask_orbit_size"]
            z["primitive_prime_classes"]+=x["mask_orbit_size"]*x["coefficient"]
        support_summary[str(n)]={str(k):v for k,v in sorted(d.items())}

    c6_pairs=[x for x in prime_orbits["6"] if x["support_size"]==2]
    assert {(x["mask_orbit_size"],x["induced_edges"],x["coefficient"]) for x in c6_pairs} == {(240,1,252),(540,0,48)}

    out={
      "passes":[4511,4513,4514,4516,4517,4518],
      "4511_dual_completion":{
        "dual_dimension":1581,"prism_weight3_words":2160,"prism_span_rank":1215,
        "weight4_words":84240,"weight4_span_rank":1580,
        "weight4_span":"entire even-weight subcode of C^perp",
        "combined_weight3_weight4_span_rank":1581,"missing_beyond_prisms":366,
        "PGSp_weight4_orbit_sizes":sorted(len(o) for o in pg_orbits),
        "PSp_weight4_orbit_sizes":sorted(len(o) for o in psp_orbits),
        "PGSp_orbit_profile":pg_profile,
      },
      "4513_prism_edge_identification":{
        "identity":"protected(prism)=A_*(e_i+e_j) for a unique adjacent pair i~j",
        "protected_images":240,"prisms":2160,"fiber_size":9,
        "edge_endpoints_outside_prism":True,"each_edge_endpoint_meets_prism_lines":3,
        "PSp_edge_stabilizer_order":psp_stab,"PSp_suborbits":psp_sub,
        "PGSp_edge_stabilizer_order":pg_stab,"PGSp_suborbits":pg_sub,
        "conclusion":"the protected 240-set is equivariantly the dual-W33 edge action; no E8-root identification is used"
      },
      "4514_ihara_support_decomposition":{
        "primitive_orbits":{k:v for k,v in prime_orbits.items() if k in {"6","7","8"}},
        "support_size_summary":support_summary,
        "oriented_primitive_prime_counts":{"6":302880,"7":2739840,"8":26750160}
      },
      "4516_nine_sheet_prism_fiber":{
        "edge_stabilizer_order":108,"fiber_action_image_order":36,"kernel_order":3,
        "fiber_action_element_orders":{str(k):v for k,v in sorted(orders.items())},
        "normal_regular_translation_subgroup_order":9,"point_stabilizer_order":4,
        "group_identification":"C3^2:C4"
      },
      "4517_regular_weight4_seed":{
        "PSp_orbit_size":25920,"PSp_stabilizer_order":1,"orbit_span_rank":1580,
        "generates":"entire even-weight subcode of C^perp",
        "seed_geometry":regular_inv
      },
      "4518_sixth_ihara_tomography":{
        "degree2_coefficient_adjacent_pair":252,"degree2_coefficient_disjoint_pair":48,
        "adjacent_pairs":240,"disjoint_pairs":540,
        "matrix_identity":"offdiag Walsh coefficient matrix = 48*(J-I) + 204*A_*",
        "conclusion":"the degree-2 Walsh layer of primitive C6 reconstructs dual-W33 adjacency exactly"
      },
      "boundary":"Finite exact code/group/zeta statements only. The 240 edge identification is explicit; no other 240-set is identified by cardinality."
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("PASS 4511/4513-4514/4516-4518")
    print("  Cperp: prisms rank 1215; weight-4 even subcode rank 1580; together 1581")
    print("  prism protected 240 = dual-W33 edge action exactly; fiber 9 with 3^2:C4 image")
    print("  C6/C7/C8 primitive parity-support orbit counts:", {n:len(prime_orbits[str(n)]) for n in (6,7,8)})
    print("  C6 degree-2 coefficients: edge 252, nonedge 48 -> exact zeta tomography")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
