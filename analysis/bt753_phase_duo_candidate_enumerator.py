#!/usr/bin/env python3
"""BT753 — phase+duo root-natural candidate enumerator.

BT750 corrected the local selector target: a constant dihedral phase is not a
selector because every reflection fixes a central-half-turn duo {k, r^6 k},
and the two partners are different Levi octagons.  Therefore the selector
candidate must fix

    chirality epsilon in {0,1}, phase phi in {0,...,5}, duo delta in {0,1}.

This verifier enumerates the 24 local (epsilon, phase, duo) selectors across
all 2160 centered rectangles of W(3,3), records the selected Levi octagons, and
computes the first two BT751 tests:

  T1. one selected lift per rectangle;
  T2. rank of the signed selector rows over GF(1000003);
  T3. root-triple/involution hit distribution over the 540 canonical
      outer-involution class elements observed by the selected lifts.

Boundary: this is the phase+duo *local-coordinate* enumerator.  It does not yet
claim that any local phase numbering is globally canonical in the BT748
centralizer-torsor coordinates.  The next verifier should replace the local
phase numbering by a transported base-pair coordinate and add BT741 gluing.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from itertools import combinations, product
import argparse
import json
from pathlib import Path

MOD = 1_000_003


def inv3(a: int) -> int:
    a %= 3
    if a in (1, 2):
        return a
    raise ZeroDivisionError


def canon(v):
    for x in v:
        if x % 3:
            c = inv3(x)
            return tuple((c * y) % 3 for y in v)
    raise ValueError


def points():
    return sorted({
        canon((a, b, c, d))
        for a in range(3)
        for b in range(3)
        for c in range(3)
        for d in range(3)
        if (a, b, c, d) != (0, 0, 0, 0)
    })


def symp(x, y):
    return (x[0] * y[2] - x[2] * y[0] + x[1] * y[3] - x[3] * y[1]) % 3


def rank_mod(rows, ncols: int, p: int = MOD) -> int:
    """Sparse Gaussian elimination over GF(p).  rows are iterables of columns.

    Every selected Levi octagon row has coefficient +1 on its eight flag-edges.
    Rank is insensitive to row sign for the selector-span test, so this is the
    same rank target used by BT713/BT714.
    """
    pivots: dict[int, dict[int, int]] = {}
    rank = 0
    for cols in rows:
        row = {c: 1 for c in cols}
        while row:
            j = min(row)
            a = row[j] % p
            if a == 0:
                del row[j]
                continue
            if j not in pivots:
                inv = pow(a, p - 2, p)
                pivots[j] = {c: (v * inv) % p for c, v in row.items() if (v * inv) % p}
                rank += 1
                break
            fac = a
            piv = pivots[j]
            for c, v in piv.items():
                row[c] = (row.get(c, 0) - fac * v) % p
                if row[c] == 0:
                    row.pop(c, None)
    return rank


def inverse_perm(a):
    out = [0] * len(a)
    for i, x in enumerate(a):
        out[x] = i
    return tuple(out)


def key_repr(key) -> str:
    p, rect_pts, gs = key
    return repr((p, tuple(sorted(rect_pts)), tuple(sorted(gs))))


class W33:
    def __init__(self):
        self.pts = points()
        self.n = 40
        self.pt_index = {p: i for i, p in enumerate(self.pts)}
        self.ident = tuple(range(self.n))
        self.g_sim = self.matrix_perm([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 2, 0], [0, 0, 0, 2]])
        self.gens_psp = [self.transvection_perm(v) for v in self.pts]
        self.psp = self.generate_psp()
        self.adj = self.build_adj()
        self.lines = self.build_lines()
        self.line_index = {l: i for i, l in enumerate(self.lines)}
        self.through = defaultdict(list)
        self.edge_line = {}
        for li, l in enumerate(self.lines):
            for p in l:
                self.through[p].append(li)
            for a, b in combinations(sorted(l), 2):
                self.edge_line[(a, b)] = li
        self.flag_index = {(p, li): 4 * p + j for p in range(self.n) for j, li in enumerate(sorted(self.through[p]))}
        self.centers = {}
        for x, y in combinations(range(self.n), 2):
            if not self.adj[x][y]:
                self.centers[(x, y)] = tuple(sorted(c for c in range(self.n) if self.adj[x][c] and self.adj[y][c]))

    def matrix_perm(self, M):
        return tuple(
            self.pt_index[
                canon(tuple(sum(M[r][c] * x[c] for c in range(4)) % 3 for r in range(4)))
            ]
            for x in self.pts
        )

    def transvection_perm(self, v):
        out = []
        for x in self.pts:
            w = symp(x, v)
            out.append(self.pt_index[canon(tuple((x[k] + w * v[k]) % 3 for k in range(4)))])
        return tuple(out)

    def compose(self, a, b):
        return tuple(a[b[i]] for i in range(self.n))

    def generate_psp(self):
        psp = {self.ident}
        frontier = [self.ident]
        while frontier:
            nxt = []
            for g in frontier:
                for h in self.gens_psp:
                    gh = self.compose(h, g)
                    if gh not in psp:
                        psp.add(gh)
                        nxt.append(gh)
            frontier = nxt
        assert len(psp) == 25920
        return sorted(psp)

    def build_adj(self):
        adj = [[False] * self.n for _ in range(self.n)]
        for i, j in combinations(range(self.n), 2):
            if symp(self.pts[i], self.pts[j]) == 0:
                adj[i][j] = adj[j][i] = True
        return adj

    def build_lines(self):
        return [
            frozenset(q)
            for q in combinations(range(self.n), 4)
            if all(self.adj[i][j] for i, j in combinations(q, 2))
        ]

    def path_edges(self, x, y, c):
        lxc = self.edge_line[tuple(sorted((x, c)))]
        lcy = self.edge_line[tuple(sorted((c, y)))]
        return [(x, lxc), (c, lxc), (c, lcy), (y, lcy)]

    @staticmethod
    def xor_paths(paths):
        cnt = Counter()
        for path in paths:
            for e in path:
                cnt[e] ^= 1
        return frozenset(e for e, v in cnt.items() if v)

    @staticmethod
    def is_octagon(es):
        if len(es) != 8:
            return False
        deg = Counter()
        graph = defaultdict(list)
        for p, li in es:
            deg[("p", p)] += 1
            deg[("l", li)] += 1
            graph[("p", p)].append(("l", li))
            graph[("l", li)].append(("p", p))
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

    def act(self, g, key):
        p, rp, gs = key
        ng = []
        for e, c in gs:
            x, y = e
            ng.append((tuple(sorted((g[x], g[y]))), g[c]))
        return (g[p], frozenset(g[i] for i in rp), frozenset(ng))

    def order_of(self, g):
        o = 1
        cur = g
        while cur != self.ident:
            cur = self.compose(g, cur)
            o += 1
        return o

    def rectangle_records(self):
        """Yield all 2160 centered K3,3 rectangles with local data."""
        for p0 in range(self.n):
            for li0, lj0 in combinations(sorted(self.through[p0]), 2):
                A = tuple(sorted(self.lines[li0] - {p0}))
                B = tuple(sorted(self.lines[lj0] - {p0}))
                for aa in combinations(A, 2):
                    for bb in combinations(B, 2):
                        rect_edges = [
                            tuple(sorted(e))
                            for e in [(aa[0], bb[0]), (aa[1], bb[0]), (aa[1], bb[1]), (aa[0], bb[1])]
                        ]
                        rect_pts = frozenset(aa) | frozenset(bb)
                        yield p0, li0, lj0, rect_edges, rect_pts

    def lifts_for_rectangle(self, p0, rect_edges, rect_pts):
        lifts = []
        per_mask = defaultdict(list)
        for gauges in product(*(self.centers[e] for e in rect_edges)):
            cyc = self.xor_paths([self.path_edges(x, y, g) for (x, y), g in zip(rect_edges, gauges)])
            if self.is_octagon(cyc):
                mask = tuple(1 if g == p0 else 0 for g in gauges)
                per_mask[mask].append((tuple(sorted(cyc)), gauges))
        for mask, entries in per_mask.items():
            entries.sort()
            for ch, (_, gauges) in enumerate(entries):
                key = (p0, rect_pts, frozenset(zip(rect_edges, gauges)))
                flags = tuple(sorted(self.flag_index[e] for e in self.xor_paths([self.path_edges(x, y, g) for (x, y), g in zip(rect_edges, gauges)])))
                lifts.append({"key": key, "mask": mask, "channel": ch, "flags": flags})
        assert len(lifts) == 24
        return lifts

    def stabilizers_for_rectangle(self, p0, li0, lj0, rect_pts):
        def stab_rect(g):
            if g[p0] != p0:
                return False
            if frozenset(g[i] for i in rect_pts) != rect_pts:
                return False
            imgl = frozenset(self.line_index[frozenset(g[i] for i in self.lines[li])] for li in (li0, lj0))
            return imgl == frozenset((li0, lj0))

        stabP = [g for g in self.psp if stab_rect(g)]
        stabO = [self.compose(h, self.g_sim) for h in self.psp if stab_rect(self.compose(h, self.g_sim))]
        assert len(stabP) == 12 and len(stabO) == 12
        return stabP, stabO

    def label_rectangle_lifts(self, p0, li0, lj0, rect_edges, rect_pts):
        lifts = self.lifts_for_rectangle(p0, rect_edges, rect_pts)
        stabP, stabO = self.stabilizers_for_rectangle(p0, li0, lj0, rect_pts)
        zc = [g for g in stabP if self.order_of(g) == 2]
        assert len(zc) == 1
        z = zc[0]
        rgens = [g for g in stabP if self.order_of(g) == 12]
        assert rgens
        r = min(rgens)
        rinv = inverse_perm(r)

        invols = [g for g in stabO if self.order_of(g) == 2]
        assert len(invols) == 12

        # D12 reflection-class/phase coordinates by conjugation under r.
        unassigned = {tuple(t) for t in invols}
        phase_map = {}
        eps_by_class = {}
        while unassigned:
            base = min(unassigned)
            orbit = []
            cur = base
            for m in range(6):
                if cur not in orbit:
                    orbit.append(cur)
                cur = self.compose(rinv, self.compose(cur, r))
            orbit_set = set(orbit)
            unassigned -= orbit_set
            # Determine chirality/parity of this reflection class by fixed lifts.
            weights = []
            for t in orbit_set:
                fixed = [L for L in lifts if self.act(t, L["key"]) == L["key"]]
                assert len(fixed) == 2
                weights.extend(sum(L["mask"]) % 2 for L in fixed)
            assert len(set(weights)) == 1
            eps = weights[0]
            eps_by_class[base] = eps
            for m, t in enumerate(orbit):
                phase_map[t] = (eps, m)

        # Assign each lift: its reflection, epsilon, phase, and central duo bit.
        fixed_by_t = defaultdict(list)
        for t in invols:
            for L in lifts:
                if self.act(t, L["key"]) == L["key"]:
                    fixed_by_t[tuple(t)].append(L)
        for t, fixed in fixed_by_t.items():
            assert len(fixed) == 2
            fixed_sorted = sorted(fixed, key=lambda L: key_repr(L["key"]))
            # Check BT750 duo relation.
            assert self.act(z, fixed_sorted[0]["key"]) == fixed_sorted[1]["key"]
            assert self.act(z, fixed_sorted[1]["key"]) == fixed_sorted[0]["key"]
            eps, phase = phase_map[t]
            for duo, L in enumerate(fixed_sorted):
                L["epsilon"] = eps
                L["phase"] = phase
                L["duo"] = duo
                L["involution"] = t
        assert all("epsilon" in L for L in lifts)
        return lifts


def enumerate_candidates(limit_rectangles: int | None = None):
    w = W33()
    candidate_rows = {(e, ph, d): [] for e in (0, 1) for ph in range(6) for d in (0, 1)}
    candidate_taus = {(e, ph, d): [] for e in (0, 1) for ph in range(6) for d in (0, 1)}
    rectangles = 0
    for p0, li0, lj0, rect_edges, rect_pts in w.rectangle_records():
        labeled = w.label_rectangle_lifts(p0, li0, lj0, rect_edges, rect_pts)
        by_label = {(L["epsilon"], L["phase"], L["duo"]): L for L in labeled}
        assert set(by_label) == set(candidate_rows)
        for label, L in by_label.items():
            candidate_rows[label].append(L["flags"])
            candidate_taus[label].append(L["involution"])
        rectangles += 1
        if limit_rectangles is not None and rectangles >= limit_rectangles:
            break

    out = {
        "theorem": "BT753 phase+duo candidate enumeration",
        "rectangles_processed": rectangles,
        "candidate_count": 24,
        "boundary": (
            "Local phase numbering is defined by the deterministic D12 generator at each rectangle. "
            "The next BT754/BT756 layer should transport a single base-pair coordinate globally "
            "through BT748 centralizer torsor coordinates and add BT741 gluing."
        ),
        "candidates": {},
    }
    for label in sorted(candidate_rows):
        rows = candidate_rows[label]
        taus = candidate_taus[label]
        tau_dist = Counter(taus)
        hit_dist = Counter(tau_dist.values())
        out["candidates"][str(label)] = {
            "selected_rows": len(rows),
            "rank_mod_1000003": rank_mod(rows, 160) if limit_rectangles is None else None,
            "root_triples_hit": len(tau_dist),
            "root_hit_distribution": {str(k): v for k, v in sorted(hit_dist.items())},
            "root_uniform_4": (len(tau_dist) == 540 and set(hit_dist) == {4}) if limit_rectangles is None else None,
        }
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit-rectangles", type=int, default=None, help="debug limit")
    ap.add_argument("--out", default="data/bt753_phase_duo_candidate_enumerator.json")
    args = ap.parse_args()
    out = enumerate_candidates(args.limit_rectangles)
    path = Path(args.out)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
