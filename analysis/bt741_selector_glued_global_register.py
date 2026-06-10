#!/usr/bin/env python3
"""
BT741 - Selector-glued global register (executes the BT740 boundary).

BT740 built the exact braid functor Phi : H_1(K33;F2) = F2^4 -> U(16) per
local chart (bit-flip = sigma^5 = Z, exact).  Its boundary asked for the
cycle-level statement: the BT718 canonical selector (mask 1110, channel
011/far = residual 0) assigns each of the 2160 centered rectangles a definite
Levi 8-cycle.  When two rectangles IN DIFFERENT CHARTS select the same Levi
cycle, their local register classes must be identified.  The global braid
register of W(3,3) is the quotient

    R_glob = ( sum over 240 charts of F2^4 ) / < embed(c_A, class_A(r_A))
                                                + embed(c_B, class_B(r_B)) :
                selected(r_A) = selected(r_B) >.

BT741 computes dim R_glob exactly over F2, plus diagnostics:

  * how many distinct Levi cycles the selected sheet hits,
  * the multiplicity profile (how many rectangles select each cycle),
  * the gluing-relation rank,
  * the same numbers for the full mask-1110 bundle (all 3 channels) and for
    all 24 sheets together, locating where the register collapses.

Per-chart class convention (BT740 T5): chart = (p, li, lj, A, B) with A, B
sorted; the chord basis bits of rectangle (aa, bb) are
    bit(i,j) = [pos_A(aa) contains i][pos_B(bb) contains j],  i,j in {1,2}.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from itertools import combinations, product
import json


def inv3(a: int) -> int:
    a %= 3
    if a == 1:
        return 1
    if a == 2:
        return 2
    raise ZeroDivisionError


def canon(v):
    for x in v:
        if x % 3:
            c = inv3(x)
            return tuple((c * y) % 3 for y in v)
    raise ValueError("zero vector")


def points():
    return sorted({
        canon((a, b, c, d))
        for a in range(3) for b in range(3) for c in range(3) for d in range(3)
        if (a, b, c, d) != (0, 0, 0, 0)
    })


def symp(x, y) -> int:
    return (x[0]*y[2] - x[2]*y[0] + x[1]*y[3] - x[3]*y[1]) % 3


def build():
    pts = points()
    adj = [[False] * 40 for _ in range(40)]
    for i, j in combinations(range(40), 2):
        if symp(pts[i], pts[j]) == 0:
            adj[i][j] = adj[j][i] = True
    lines = [tuple(q) for q in combinations(range(40), 4)
             if all(adj[i][j] for i, j in combinations(q, 2))]
    through = defaultdict(list)
    edge_line = {}
    for li, line in enumerate(lines):
        for p in line:
            through[p].append(li)
        for a, b in combinations(line, 2):
            edge_line[tuple(sorted((a, b)))] = li
    centers = {}
    for x, y in combinations(range(40), 2):
        if not adj[x][y]:
            cs = tuple(sorted(c for c in range(40) if adj[x][c] and adj[y][c]))
            assert len(cs) == 4
            centers[tuple(sorted((x, y)))] = cs
    return adj, lines, through, edge_line, centers


def path_edges(x, y, c, edge_line):
    lxc = edge_line[tuple(sorted((x, c)))]
    lcy = edge_line[tuple(sorted((c, y)))]
    return [(x, lxc), (c, lxc), (c, lcy), (y, lcy)]


def xor_path_edges(paths):
    cnt = Counter()
    for path in paths:
        for e in path:
            cnt[e] ^= 1
    return frozenset(e for e, v in cnt.items() if v)


def is_simple_levi_8_cycle(edge_set) -> bool:
    if len(edge_set) != 8:
        return False
    deg = Counter()
    graph = defaultdict(list)
    for p, li in edge_set:
        a = ("p", p)
        b = ("l", li)
        deg[a] += 1
        deg[b] += 1
        graph[a].append(b)
        graph[b].append(a)
    if len(deg) != 8 or any(d != 2 for d in deg.values()):
        return False
    start = next(iter(deg))
    seen = {start}
    stack = [start]
    while stack:
        u = stack.pop()
        for v in graph[u]:
            if v not in seen:
                seen.add(v)
                stack.append(v)
    return len(seen) == 8


def gf2_rank(rows) -> int:
    """rows: list of int bitmasks."""
    pivots = []
    rank = 0
    for r in rows:
        for p in pivots:
            r = min(r, r ^ p)
        if r:
            pivots.append(r)
            pivots.sort(reverse=True)
            rank += 1
    return rank


def main() -> None:
    adj, lines, through, edge_line, centers = build()

    all_masks = {
        (1,1,1,0), (1,1,0,1), (1,0,1,1), (0,1,1,1),
        (1,1,0,0), (1,0,0,1), (0,1,1,0), (0,0,1,1),
    }
    sel_mask = (1, 1, 1, 0)   # BT718 canonical
    sel_channel = 0           # 011/far = residual index 0 (BT721)

    charts = []
    for p in range(40):
        for li, lj in combinations(through[p], 2):
            A = tuple(sorted(set(lines[li]) - {p}))
            B = tuple(sorted(set(lines[lj]) - {p}))
            charts.append((p, li, lj, A, B))
    assert len(charts) == 240

    # selected[(chart_idx, rect_key)] = (cycle, class_bits)
    # sheet_records[sheet_key] = list of (chart_idx, class_bits, cycle)
    sheet_records = defaultdict(list)

    for ci, (p, li, lj, A, B) in enumerate(charts):
        for ai in combinations(range(3), 2):
            for bi in combinations(range(3), 2):
                aa = (A[ai[0]], A[ai[1]])
                bb = (B[bi[0]], B[bi[1]])
                rect_edges = [tuple(sorted(e)) for e in [
                    (aa[0], bb[0]), (aa[1], bb[0]),
                    (aa[1], bb[1]), (aa[0], bb[1]),
                ]]
                assert all(not adj[x][y] for x, y in rect_edges)
                # class bits over chords (i,j), i,j in {1,2}
                bits = 0
                k = 0
                for i in (1, 2):
                    for j in (1, 2):
                        if i in ai and j in bi:
                            bits |= (1 << k)
                        k += 1
                per_mask = defaultdict(list)
                for gauges in product(*(centers[e] for e in rect_edges)):
                    paths = [path_edges(x, y, g, edge_line)
                             for (x, y), g in zip(rect_edges, gauges)]
                    cycle = xor_path_edges(paths)
                    if is_simple_levi_8_cycle(cycle):
                        mask = tuple(1 if g == p else 0 for g in gauges)
                        per_mask[mask].append(cycle)
                assert set(per_mask) == all_masks
                for mask in all_masks:
                    cycles3 = sorted(per_mask[mask], key=lambda c: tuple(sorted(c)))
                    assert len(cycles3) == 3
                    for ch, cyc in enumerate(cycles3):
                        sheet_records[(mask, ch)].append((ci, bits, cyc))

    def glue(records):
        """Return (distinct_cycles, multiplicity_profile, relation_rank,
        global_dim, n_components, component_dims) for records
        (chart, class_bits, cycle)."""
        by_cycle = defaultdict(list)
        for ci, bits, cyc in records:
            by_cycle[cyc].append((ci, bits))
        mult = Counter(len(v) for v in by_cycle.values())
        relations = []
        # Union-find on charts to find gluing components.
        parent = list(range(240))

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        for sel in by_cycle.values():
            c0, b0 = sel[0]
            v0 = b0 << (4 * c0)
            for ci, bits in sel[1:]:
                relations.append(v0 ^ (bits << (4 * ci)))
                ra, rb = find(c0), find(ci)
                if ra != rb:
                    parent[ra] = rb
        rank = gf2_rank(relations)
        dim = 240 * 4 - rank
        comps = defaultdict(list)
        for c in range(240):
            comps[find(c)].append(c)
        # Per-component dim: 4*|comp| - rank(relations within comp).
        comp_dims = []
        for root, members in comps.items():
            mset = set(members)
            sub = []
            for sel in by_cycle.values():
                if find(sel[0][0]) != root:
                    continue
                c0, b0 = sel[0]
                v0 = b0 << (4 * c0)
                for ci, bits in sel[1:]:
                    sub.append(v0 ^ (bits << (4 * ci)))
            comp_dims.append(4 * len(members) - gf2_rank(sub))
        return (len(by_cycle), dict(sorted(mult.items())), rank, dim,
                len(comps), sorted(comp_dims))

    print("BT741 - selector-glued global register")
    print("=" * 68)
    print(f"charts=240, local register dim=4, ambient dim=960")
    print()

    type_a = [(1,1,1,0), (1,1,0,1), (1,0,1,1), (0,1,1,1)]
    type_b = [(1,1,0,0), (1,0,0,1), (0,1,1,0), (0,0,1,1)]

    def report(name, records):
        n_cyc, mult, rank, dim, ncomp, cdims = glue(records)
        print(f"{name}:")
        print(f"  records = {len(records)}, distinct cycles = {n_cyc}")
        print(f"  multiplicity profile = {mult}")
        print(f"  relation rank = {rank}, GLOBAL DIM = {dim}")
        print(f"  gluing components = {ncomp}, component dims = "
              f"{Counter(cdims) if len(cdims) > 8 else cdims}")
        print()
        return dict(records=len(records), distinct_cycles=n_cyc,
                    multiplicity={str(k): v for k, v in mult.items()},
                    relation_rank=rank, global_dim=dim,
                    components=ncomp,
                    component_dims={str(k): v
                                    for k, v in Counter(cdims).items()})

    results = {}
    rec_sel = sheet_records[(sel_mask, sel_channel)]
    assert len(rec_sel) == 2160
    results["bt718_sheet"] = report("BT718 sheet (1110, ch0=011/far)", rec_sel)

    rec_bundle = []
    for ch in range(3):
        rec_bundle.extend(sheet_records[(sel_mask, ch)])
    results["mask_1110_bundle"] = report("mask 1110 bundle (3 channels)",
                                         rec_bundle)

    rec_ta = []
    for m in type_a:
        for ch in range(3):
            rec_ta.extend(sheet_records[(m, ch)])
    results["type_a_bundle"] = report("Type-A orbit bundle (4 masks x 3 ch)",
                                      rec_ta)

    rec_tb = []
    for m in type_b:
        for ch in range(3):
            rec_tb.extend(sheet_records[(m, ch)])
    results["type_b_bundle"] = report("Type-B orbit bundle (4 masks x 3 ch)",
                                      rec_tb)

    # Every single-mask bundle, including the BT713 Hodge-defective 1001.
    mask_dims = {}
    for m in type_a + type_b:
        rec_m = []
        for ch in range(3):
            rec_m.extend(sheet_records[(m, ch)])
        n_cyc_m, _, rank_m, dim_m, ncomp_m, cdims_m = glue(rec_m)
        key = "".join(map(str, m))
        mask_dims[key] = dict(distinct_cycles=n_cyc_m, relation_rank=rank_m,
                              global_dim=dim_m, components=ncomp_m)
        print(f"mask {key} bundle: cycles={n_cyc_m}, rank={rank_m}, "
              f"dim={dim_m}, components={ncomp_m}")
    print()
    results["per_mask_bundles"] = mask_dims

    rec_all = []
    for key in sheet_records:
        rec_all.extend(sheet_records[key])
    results["all_24_sheets"] = report("all 24 sheets", rec_all)

    out = {
        "theorem": "BT741 Selector-glued global register",
        "ambient_dim": 960,
        **results,
    }
    with open("data/bt741_selector_glued_global_register.json", "w") as f:
        json.dump(out, f, indent=2, default=str)
    print("\nwrote data/bt741_selector_glued_global_register.json")


if __name__ == "__main__":
    main()
