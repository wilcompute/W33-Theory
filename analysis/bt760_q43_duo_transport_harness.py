#!/usr/bin/env python3
"""BT760 — Q(4,3) duo-transport target harness.

This is the executable target-side half of the BT759 problem.  It rebuilds
Q(4,3), constructs the point-line incidence graph, enumerates oriented
apartments as simple incidence octagons, and verifies that the abstract
orientation reversal is an order-two, fixed-point-free operation on oriented
apartments.

It deliberately does NOT claim that BT750's local half-turn r^6 has already
been transported from the BT748 root-triple torsor into Q(4,3).  That final
claim requires an explicit transport table from root-triple torsor coordinates
to oriented Q(4,3) apartments.  If that table is not present, this verifier
writes a fail-closed pending status.
"""
from __future__ import annotations

import itertools
import json
from collections import defaultdict, Counter
from pathlib import Path

MOD = 3
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt760_q43_duo_transport_harness_summary.json"
TRANSPORT = ROOT / "data" / "bt760_root_torsor_to_q43_transport.json"


def inv(a: int) -> int:
    a %= MOD
    if a == 1:
        return 1
    if a == 2:
        return 2
    raise ZeroDivisionError(a)


def norm(v):
    v = tuple(x % MOD for x in v)
    for x in v:
        if x:
            s = inv(x)
            return tuple((s * y) % MOD for y in v)
    raise ValueError("zero vector")


def add(u, v):
    return tuple((a + b) % MOD for a, b in zip(u, v))


def smul(a, v):
    return tuple((a * x) % MOD for x in v)


def qform(v):
    x0, x1, x2, x3, x4 = v
    return (x0 * x1 + x2 * x3 + x4 * x4) % MOD


def projective_points(dim=5):
    pts = set()
    for v in itertools.product(range(MOD), repeat=dim):
        if any(v):
            pts.add(norm(v))
    return sorted(pts)


def projective_line(p, q):
    pts = set()
    for a in range(MOD):
        for b in range(MOD):
            if a or b:
                pts.add(norm(add(smul(a, p), smul(b, q))))
    return frozenset(pts)


def build_q43():
    pg = projective_points()
    qpts = [p for p in pg if qform(p) == 0]
    qset = set(qpts)
    lines = set()
    for p, q in itertools.combinations(qpts, 2):
        L = projective_line(p, q)
        if len(L) == 4 and L <= qset:
            lines.add(L)
    return qpts, sorted(lines, key=lambda L: sorted(L))


def incidence(qpts, lines):
    p_index = {p: i for i, p in enumerate(qpts)}
    point_to_lines = defaultdict(list)
    line_to_points = {}
    for li, L in enumerate(lines):
        line_to_points[li] = sorted(p_index[p] for p in L)
        for p in L:
            point_to_lines[p_index[p]].append(li)
    return point_to_lines, line_to_points


def canonical_cycle(seq):
    """Canonicalize an 8-cycle sequence of alternating tagged nodes."""
    n = len(seq)
    rots = [tuple(seq[i:] + seq[:i]) for i in range(n)]
    rev = list(reversed(seq))
    rots += [tuple(rev[i:] + rev[:i]) for i in range(n)]
    return min(rots)


def enumerate_apartments(qpts, lines):
    point_to_lines, line_to_points = incidence(qpts, lines)
    cycles = set()
    # Alternating point-line cycles p0,L0,p1,L1,p2,L2,p3,L3,p0.
    for p0 in range(len(qpts)):
        for L0 in point_to_lines[p0]:
            for p1 in line_to_points[L0]:
                if p1 == p0:
                    continue
                for L1 in point_to_lines[p1]:
                    if L1 == L0:
                        continue
                    for p2 in line_to_points[L1]:
                        if p2 in (p0, p1):
                            continue
                        for L2 in point_to_lines[p2]:
                            if L2 in (L0, L1):
                                continue
                            for p3 in line_to_points[L2]:
                                if p3 in (p0, p1, p2):
                                    continue
                                common = set(point_to_lines[p3]) & set(point_to_lines[p0])
                                for L3 in common:
                                    if L3 in (L0, L1, L2):
                                        continue
                                    seq = [('p', p0), ('l', L0), ('p', p1), ('l', L1), ('p', p2), ('l', L2), ('p', p3), ('l', L3)]
                                    cycles.add(canonical_cycle(seq))
    return sorted(cycles)


def orient(cyc):
    return tuple(cyc)


def reverse_orientation(ocyc):
    rev = tuple(reversed(ocyc))
    # Rotate so comparison is made from a canonical starting node but preserve orientation reversal.
    rots = [rev[i:] + rev[:i] for i in range(len(rev))]
    return min(rots)


def main():
    qpts, lines = build_q43()
    cycles = enumerate_apartments(qpts, lines)
    oriented = set()
    for c in cycles:
        oriented.add(orient(c))
        oriented.add(reverse_orientation(c))
    fixed = [c for c in oriented if reverse_orientation(c) == c]
    checks = {
        "q43_points_40": len(qpts) == 40,
        "q43_lines_40": len(lines) == 40,
        "apartments_nonempty": len(cycles) > 0,
        "orientation_doubles_unoriented_apartments": len(oriented) == 2 * len(cycles),
        "orientation_reversal_order_two": all(reverse_orientation(reverse_orientation(c)) == c for c in oriented),
        "orientation_reversal_fixed_point_free": len(fixed) == 0,
    }
    transport_status = "ready_for_transport_table" if TRANSPORT.exists() else "pending_transport_table"
    accepted = False
    boundary = "Target-side Q(4,3) mirror is verified, but BT750 r^6 is not identified until a root-torsor-to-apartment transport table is supplied."
    summary = {
        "theorem": "BT760 Q(4,3) duo-transport target harness",
        "q43_points": len(qpts),
        "q43_lines": len(lines),
        "unoriented_apartments": len(cycles),
        "oriented_apartments": len(oriented),
        "orientation_fixed_points": len(fixed),
        "transport_table": str(TRANSPORT.relative_to(ROOT)),
        "transport_status": transport_status,
        "accepted_plucker_duo_claim": accepted,
        "checks": checks,
        "all_target_checks_pass": all(checks.values()),
        "boundary": boundary,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    if not summary["all_target_checks_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
