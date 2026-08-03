#!/usr/bin/env python3
"""Dependency-light exact core for Passes 2767-2771 over F_3."""
from __future__ import annotations

import itertools
import math
from collections import Counter, deque
from typing import Iterable, Sequence

Q = 3
Mat = tuple[tuple[int, ...], ...]
Vec = tuple[int, ...]

I4: Mat = tuple(tuple(int(i == j) for j in range(4)) for i in range(4))
J4: Mat = (
    (0, 1, 0, 0),
    (2, 0, 0, 0),
    (0, 0, 0, 1),
    (0, 0, 2, 0),
)
FP: Mat = ((0, 2, 0, 0), (1, 0, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1))
FF: Mat = ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 0, 2), (0, 0, 1, 0))
SP: Mat = ((1, 0, 0, 0), (1, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1))
SF: Mat = ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 1, 1))
CX: Mat = ((1, 0, 0, 0), (0, 1, 0, 2), (1, 0, 1, 0), (0, 0, 0, 1))


def mm(a: Mat, b: Mat) -> Mat:
    return tuple(
        tuple(sum(a[i][k] * b[k][j] for k in range(len(b))) % Q for j in range(len(b[0])))
        for i in range(len(a))
    )


def mv(a: Mat, v: Vec) -> Vec:
    return tuple(sum(a[i][k] * v[k] for k in range(len(v))) % Q for i in range(len(a)))


def tr(a: Mat) -> Mat:
    return tuple(tuple(a[j][i] for j in range(len(a))) for i in range(len(a[0])))


def mpow(a: Mat, n: int) -> Mat:
    if n < 0:
        return mpow(minv(a), -n)
    out = I4
    base = a
    while n:
        if n & 1:
            out = mm(out, base)
        base = mm(base, base)
        n >>= 1
    return out


def minv(a: Mat) -> Mat:
    n = len(a)
    aug = [list(a[i]) + [int(i == j) for j in range(n)] for i in range(n)]
    r = 0
    for c in range(n):
        p = next((i for i in range(r, n) if aug[i][c] % Q), None)
        if p is None:
            raise ValueError("singular matrix")
        aug[r], aug[p] = aug[p], aug[r]
        inv = 1 if aug[r][c] % Q == 1 else 2
        aug[r] = [(inv * x) % Q for x in aug[r]]
        for i in range(n):
            if i != r and aug[i][c] % Q:
                f = aug[i][c] % Q
                aug[i] = [(aug[i][j] - f * aug[r][j]) % Q for j in range(2 * n)]
        r += 1
    return tuple(tuple(row[n:]) for row in aug)


def rank(a: Mat) -> int:
    m = [list(row) for row in a]
    r = 0
    for c in range(len(m[0])):
        p = next((i for i in range(r, len(m)) if m[i][c] % Q), None)
        if p is None:
            continue
        m[r], m[p] = m[p], m[r]
        inv = 1 if m[r][c] % Q == 1 else 2
        m[r] = [(inv * x) % Q for x in m[r]]
        for i in range(len(m)):
            if i != r and m[i][c] % Q:
                f = m[i][c] % Q
                m[i] = [(m[i][j] - f * m[r][j]) % Q for j in range(len(m[0]))]
        r += 1
    return r


def sub(a: Mat, b: Mat) -> Mat:
    return tuple(tuple((a[i][j] - b[i][j]) % Q for j in range(len(a[0]))) for i in range(len(a)))


def mtrace(a: Mat) -> int:
    return sum(a[i][i] for i in range(len(a))) % Q


def order(a: Mat, limit: int = 200) -> int:
    x = I4
    for n in range(1, limit + 1):
        x = mm(x, a)
        if x == I4:
            return n
    raise ValueError("order exceeds limit")


def symplectic(a: Mat) -> bool:
    return mm(mm(tr(a), J4), a) == J4


def normalize_projective(v: Sequence[int]) -> Vec:
    w = tuple(x % Q for x in v)
    first = next((x for x in w if x), None)
    if first is None:
        raise ValueError("zero vector")
    scale = 1 if first == 1 else 2
    return tuple((scale * x) % Q for x in w)


def sp(u: Vec, v: Vec) -> int:
    return (u[0] * v[1] - u[1] * v[0] + u[2] * v[3] - u[3] * v[2]) % Q


def canonical_points() -> list[Vec]:
    return sorted({normalize_projective(v) for v in itertools.product(range(Q), repeat=4) if any(v)})


def canonical_lines(points: Sequence[Vec]) -> list[tuple[Vec, ...]]:
    out: set[tuple[Vec, ...]] = set()
    for i, u in enumerate(points):
        for v in points[i + 1 :]:
            if sp(u, v):
                continue
            line = {
                normalize_projective(tuple((a * u[k] + b * v[k]) % Q for k in range(4)))
                for a, b in itertools.product(range(Q), repeat=2)
                if a or b
            }
            if len(line) == 4:
                out.add(tuple(sorted(line)))
    return sorted(out)


def canonical_geometry() -> dict[str, list]:
    points = canonical_points()
    lines = canonical_lines(points)
    point_index = {p: i for i, p in enumerate(points)}
    line_index = {line: i for i, line in enumerate(lines)}
    flags = [(point_index[p], j) for j, line in enumerate(lines) for p in line]
    edges = sorted(
        {
            tuple(sorted((point_index[u], point_index[v])))
            for line in lines
            for u, v in itertools.combinations(line, 2)
        }
    )
    adjacency = [set() for _ in points]
    for u, v in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
    apartments: set[tuple[int, int, int, int]] = set()
    for a, c in itertools.combinations(range(len(points)), 2):
        if c in adjacency[a]:
            continue
        common = sorted(adjacency[a] & adjacency[c])
        for b, d in itertools.combinations(common, 2):
            if d in adjacency[b]:
                continue
            cyc = tuple(sorted((a, b, c, d)))
            apartments.add(cyc)
    assert len(points) == 40 and len(lines) == 40
    assert len(flags) == 160 and len(edges) == 240 and len(apartments) == 1620
    return {
        "points": points,
        "lines": lines,
        "flags": sorted(flags),
        "edges": edges,
        "apartments": sorted(apartments),
        "point_index": point_index,
        "line_index": line_index,
    }


def permutation_on_geometry(g: Mat, geom: dict[str, list]) -> dict[str, list[int]]:
    points: list[Vec] = geom["points"]
    lines: list[tuple[Vec, ...]] = geom["lines"]
    pidx = geom["point_index"]
    lidx = geom["line_index"]
    pp = [pidx[normalize_projective(mv(g, p))] for p in points]
    lp = []
    for line in lines:
        image = tuple(sorted(normalize_projective(mv(g, p)) for p in line))
        lp.append(lidx[image])
    fidx = {x: i for i, x in enumerate(geom["flags"])}
    epidx = {x: i for i, x in enumerate(geom["edges"])}
    apidx = {x: i for i, x in enumerate(geom["apartments"])}
    fp = [fidx[(pp[p], lp[l])] for p, l in geom["flags"]]
    ep = [epidx[tuple(sorted((pp[u], pp[v])))] for u, v in geom["edges"]]
    ap = [apidx[tuple(sorted(pp[x] for x in apt))] for apt in geom["apartments"]]
    return {"points": pp, "lines": lp, "flags": fp, "edges": ep, "apartments": ap}


def cycle_profile(perm: Sequence[int]) -> tuple[tuple[int, int], ...]:
    seen = [False] * len(perm)
    counter: Counter[int] = Counter()
    for i in range(len(perm)):
        if seen[i]:
            continue
        j = i
        n = 0
        while not seen[j]:
            seen[j] = True
            n += 1
            j = perm[j]
        counter[n] += 1
    return tuple(sorted(counter.items()))


def geometry_signature(g: Mat, geom: dict[str, list]) -> tuple:
    perms = permutation_on_geometry(g, geom)
    return tuple(cycle_profile(perms[name]) for name in ("points", "lines", "flags", "edges", "apartments"))


def symmetric_generators() -> list[tuple[str, Mat]]:
    basic = [("Fp", FP), ("Ff", FF), ("Sp", SP), ("Sf", SF), ("CX", CX)]
    out: list[tuple[str, Mat]] = []
    for name, g in basic:
        out.append((name, g))
        gi = minv(g)
        if gi != g:
            out.append((name + "^-1", gi))
    return out


def generate_group(with_words: bool = False) -> tuple[list[Mat], dict[Mat, tuple[Mat | None, str | None]], dict[Mat, int]]:
    gens = symmetric_generators()
    parent: dict[Mat, tuple[Mat | None, str | None]] = {I4: (None, None)}
    dist: dict[Mat, int] = {I4: 0}
    q = deque([I4])
    while q:
        x = q.popleft()
        for name, g in gens:
            y = mm(x, g)
            if y not in parent:
                parent[y] = (x, name)
                dist[y] = dist[x] + 1
                q.append(y)
    group = list(parent)
    assert len(group) == 51840
    if not with_words:
        parent = {}
    return group, parent, dist


def recover_word(g: Mat, parent: dict[Mat, tuple[Mat | None, str | None]]) -> list[str]:
    out: list[str] = []
    x = g
    while x != I4:
        prev, name = parent[x]
        assert prev is not None and name is not None
        out.append(name)
        x = prev
    out.reverse()
    return out


def conjugacy_classes(group: Sequence[Mat]) -> list[list[Mat]]:
    unseen = set(group)
    generators = [g for _, g in symmetric_generators()]
    classes: list[list[Mat]] = []
    while unseen:
        seed = min(unseen)
        orbit = {seed}
        q = deque([seed])
        while q:
            x = q.popleft()
            for s in generators:
                y = mm(mm(minv(s), x), s)
                if y not in orbit:
                    orbit.add(y)
                    q.append(y)
        unseen.difference_update(orbit)
        classes.append(sorted(orbit))
    classes.sort(key=lambda c: (len(c), c[0]))
    assert len(classes) == 34 and sum(map(len, classes)) == 51840
    return classes


def centralizer(group: Sequence[Mat], target: Mat) -> list[Mat]:
    return sorted(g for g in group if mm(g, target) == mm(target, g))


def right_cosets(group: Sequence[Mat], subgroup: Sequence[Mat]) -> tuple[list[list[Mat]], dict[Mat, int]]:
    unseen = set(group)
    cosets: list[list[Mat]] = []
    owner: dict[Mat, int] = {}
    while unseen:
        seed = min(unseen)
        coset = sorted(mm(seed, h) for h in subgroup)
        idx = len(cosets)
        for x in coset:
            owner[x] = idx
        unseen.difference_update(coset)
        cosets.append(coset)
    assert len(cosets) * len(subgroup) == len(group)
    return cosets, owner


def matrix_json(a: Mat) -> list[list[int]]:
    return [list(row) for row in a]


def profile_json(profile: tuple[tuple[int, int], ...]) -> dict[str, int]:
    return {str(k): v for k, v in profile}


def phase_code(z: complex, tol: float = 1e-5) -> dict[str, int | str]:
    if abs(z) < tol:
        return {"phase_mod4": 0, "twice_log3_magnitude": 0, "zero": 1}
    phase = math.atan2(z.imag, z.real)
    phase_mod4 = int(round(2 * phase / math.pi)) % 4
    twice_exp = int(round(2 * math.log(abs(z), 3)))
    recon = (1j ** phase_mod4) * (3 ** (twice_exp / 2))
    if abs(z - recon) > tol * max(1.0, abs(z)):
        raise AssertionError(f"unrecognized phase sensor value {z!r}, recon={recon!r}")
    return {"phase_mod4": phase_mod4, "twice_log3_magnitude": twice_exp, "zero": 0}
