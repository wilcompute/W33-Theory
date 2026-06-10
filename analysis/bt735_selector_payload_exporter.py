#!/usr/bin/env python3
"""BT735 — deterministic selector payload exporter.

Regenerates the three selected mask-1110 sparse selector payloads:
  011_far    -> 1110_r0
  101_middle -> 1110_r1
  110_active -> 1110_r2

This removes the need to hand-paste large gzip+base64 row streams.  The
construction is derived directly from BT713: W(3,3) is built as the symplectic
polar graph on PG(3,3), centered local K3,3 rectangles are lifted through all
common-center gauges, and one residual channel is selected from each 1110 mask
fiber.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from itertools import combinations, product
from pathlib import Path
import argparse
import base64
import gzip
import hashlib
import json

P = 1_000_003
MASK = (1, 1, 1, 0)
CHANNELS = [(0, "011_far"), (1, "101_middle"), (2, "110_active")]


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
    return (x[0] * y[2] - x[2] * y[0] + x[1] * y[3] - x[3] * y[1]) % 3


def build():
    pts = points()
    adj = [[False] * 40 for _ in range(40)]
    edges = []
    for i, j in combinations(range(40), 2):
        if symp(pts[i], pts[j]) == 0:
            adj[i][j] = adj[j][i] = True
            edges.append((i, j))
    assert len(edges) == 240

    lines = [tuple(q) for q in combinations(range(40), 4)
             if all(adj[i][j] for i, j in combinations(q, 2))]
    assert len(lines) == 40

    through = defaultdict(list)
    edge_line = {}
    for li, line in enumerate(lines):
        for p in line:
            through[p].append(li)
        for a, b in combinations(line, 2):
            edge_line[tuple(sorted((a, b)))] = li
    assert all(len(through[p]) == 4 for p in range(40))

    centers = {}
    for x, y in combinations(range(40), 2):
        if not adj[x][y]:
            cs = tuple(sorted(c for c in range(40) if adj[x][c] and adj[y][c]))
            assert len(cs) == 4
            centers[tuple(sorted((x, y)))] = cs

    flags = sorted((p, li) for li, line in enumerate(lines) for p in line)
    flag_index = {f: i for i, f in enumerate(flags)}
    assert len(flags) == 160
    return adj, lines, through, edge_line, centers, flag_index


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


def oriented_sparse_row(edge_set, flag_index):
    graph = defaultdict(list)
    edge_for = {}
    for p, li in edge_set:
        a = ("p", p)
        b = ("l", li)
        graph[a].append(b)
        graph[b].append(a)
        edge_for[frozenset((a, b))] = (p, li)
    for u in graph:
        graph[u].sort()
    start = min(graph)
    prev = None
    cur = start
    nxt = graph[start][0]
    row = {}
    for _ in range(8):
        flag = edge_for[frozenset((cur, nxt))]
        sign = 1 if cur[0] == "p" and nxt[0] == "l" else -1
        row[flag_index[flag]] = sign
        prev, cur = cur, nxt
        if cur == start:
            break
        nxt = next(x for x in graph[cur] if x != prev)
    assert len(row) == 8
    return tuple(sorted(row.items()))


def gf_rank_sparse(rows, p=P) -> int:
    pivots = {}
    for row in rows:
        r = {c: v % p for c, v in row if v % p}
        while r:
            c = min(r)
            if c not in pivots:
                inv = pow(r[c], p - 2, p)
                pivots[c] = {k: (v * inv) % p for k, v in r.items()}
                break
            factor = r[c]
            for k, v in pivots[c].items():
                nv = (r.get(k, 0) - factor * v) % p
                if nv:
                    r[k] = nv
                elif k in r:
                    del r[k]
    return len(pivots)


def selected_sheet_rows():
    adj, lines, through, edge_line, centers, flag_index = build()
    masks = [
        (1, 1, 1, 0), (1, 1, 0, 1), (1, 0, 1, 1), (0, 1, 1, 1),
        (1, 1, 0, 0), (1, 0, 0, 1), (0, 1, 1, 0), (0, 0, 1, 1),
    ]
    sheet_rows = {(m, r): [] for m in masks for r in range(3)}
    unique_cycles = Counter()
    rectangles = 0

    for c in range(40):
        for li, lj in combinations(through[c], 2):
            A = tuple(sorted(set(lines[li]) - {c}))
            B = tuple(sorted(set(lines[lj]) - {c}))
            for aa in combinations(A, 2):
                for bb in combinations(B, 2):
                    rect_edges = [tuple(sorted(e)) for e in [
                        (aa[0], bb[0]), (aa[1], bb[0]),
                        (aa[1], bb[1]), (aa[0], bb[1]),
                    ]]
                    per_mask = defaultdict(list)
                    for gauges in product(*(centers[e] for e in rect_edges)):
                        paths = [path_edges(x, y, g, edge_line)
                                 for (x, y), g in zip(rect_edges, gauges)]
                        cycle = xor_path_edges(paths)
                        if is_simple_levi_8_cycle(cycle):
                            mask = tuple(1 if g == c else 0 for g in gauges)
                            row = oriented_sparse_row(cycle, flag_index)
                            per_mask[mask].append((tuple(sorted(cycle)), row, cycle))
                            unique_cycles[cycle] += 1
                    assert set(per_mask) == set(masks)
                    for mask in masks:
                        vals = sorted(per_mask[mask], key=lambda t: t[0])
                        assert len(vals) == 3
                        for residual_index, (_, row, _) in enumerate(vals):
                            sheet_rows[(mask, residual_index)].append(row)
                    rectangles += 1

    assert rectangles == 2160
    assert len(unique_cycles) == 1620
    assert Counter(unique_cycles.values()) == Counter({32: 1620})
    return {r: sheet_rows[(MASK, r)] for r, _ in CHANNELS}


def row_stream(rows) -> bytes:
    text = "\n".join(
        ",".join(f"{c}:{'+' if s > 0 else '-'}" for c, s in row)
        for row in rows
    ) + "\n"
    return text.encode()


def payload(rows, channel, residual_index):
    raw = row_stream(rows)
    gz = gzip.compress(raw, mtime=0)
    return {
        "theorem": "BT735 Selector Payload Exporter",
        "selected_mask": "1110",
        "channel": channel,
        "sheet": f"1110_r{residual_index}",
        "row_count": len(rows),
        "columns": 160,
        "entries_per_row": 8,
        "row_stream_format": "one row per line; comma-separated col:+ or col:- pairs",
        "compression": "gzip+base64",
        "uncompressed_sha256": hashlib.sha256(raw).hexdigest(),
        "compressed_sha256": hashlib.sha256(gz).hexdigest(),
        "uncompressed_bytes": len(raw),
        "compressed_bytes": len(gz),
        "rank_mod_1000003": gf_rank_sparse(rows),
        "payload_b64_gzip": base64.b64encode(gz).decode(),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="data/generated_selectors", help="output directory")
    ap.add_argument("--no-payload", action="store_true", help="write only the summary JSON")
    args = ap.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    rows_by_r = selected_sheet_rows()
    summary = {
        "theorem": "BT735 Selector Payload Exporter",
        "selected_mask": "1110",
        "channels": [],
    }
    for residual_index, channel in CHANNELS:
        p = payload(rows_by_r[residual_index], channel, residual_index)
        summary["channels"].append({k: p[k] for k in p if k != "payload_b64_gzip"})
        if not args.no_payload:
            path = out / f"PART_BT735_SELECTOR_1110_{channel.split('_')[0]}_COMPRESSED_ROWS.json"
            path.write_text(json.dumps(p, separators=(",", ":")) + "\n")
    (out / "PART_BT735_SELECTOR_EXPORT_SUMMARY.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
