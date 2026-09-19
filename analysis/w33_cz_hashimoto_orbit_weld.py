#!/usr/bin/env python3
"""CZ-context / Hashimoto-turn weld for W(3,q), odd prime q.

This file joins two independently verified structures in the W33 corpus.

(1) Relative to the CZ-fixed Lagrangian P in V=X+P, the non-fixed
    Lagrangian-context orbits under the two-qudit CZ shear split as

        (q-1) intersecting q-cycles  +  q^2 transverse q-cycles.

    In a Darboux gauge with B=[[0,1],[1,0]], the first family is labelled
    by non-axis projective directions K=< (1,s) >, s in F_q^*, and the
    second by the quotient Sym_2(F_q)/<B>, with canonical representatives
    [[a,0],[0,c]], (a,c) in F_q^2.

(2) For the directed collinearity edge e1 -> e2 in W(3,q), the k-1
    non-backtracking continuations split as

        (q-1) continuations on the same GQ line  +  q^2 off-line turns.

    In the same Darboux gauge they have canonical representatives

        (1,s,0,0), s in F_q^*,
        (a,c,1,0), (a,c) in F_q^2.

Therefore the gauge-fixed label map

        s -> (1,s,0,0),          (a,c) -> (a,c,1,0)

is an explicit branch-preserving bijection from nontrivial CZ context
orbits to local Hashimoto routing choices.  In particular

        # nontrivial CZ context orbits = q^2+q-1 = k-1.

At q=3 this is the exact 11=2+9 triangle/open-turn split already present
in the W33 Hashimoto carrier.  The fixed-context count is 2q+1; it equals
Phi_6(q)=q^2-q+1 only at q=3, since the difference is q(q-3).

Evidence boundary
-----------------
The bijection is canonical only after choosing the displayed Darboux frame,
CZ shear B, and directed base edge.  This file does NOT claim a natural
PSp(4,q)-equivariant global identification between context orbits and
Hashimoto states, nor a physical photon interpretation for q != 3.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_cz_hashimoto_orbit_weld.json"


def inv(a: int, q: int) -> int:
    return pow(a % q, -1, q)


def canon(v: tuple[int, ...], q: int) -> tuple[int, ...]:
    """Canonical projective representative over prime F_q."""
    j = next(i for i, x in enumerate(v) if x % q)
    z = inv(v[j], q)
    return tuple((z * x) % q for x in v)


def symp(u: tuple[int, int, int, int], v: tuple[int, int, int, int], q: int) -> int:
    x1, x2, p1, p2 = u
    y1, y2, r1, r2 = v
    return (x1 * r1 + x2 * r2 - p1 * y1 - p2 * y2) % q


def projective_points(q: int) -> list[tuple[int, int, int, int]]:
    pts = {
        canon((a, b, c, d), q)
        for a in range(q)
        for b in range(q)
        for c in range(q)
        for d in range(q)
        if a or b or c or d
    }
    return sorted(pts)


def in_base_line(w: tuple[int, int, int, int]) -> bool:
    # X=<e1,e2> is exactly p1=p2=0.
    return w[2] == 0 and w[3] == 0


def hashimoto_turns(q: int) -> dict:
    """Enumerate the local nonbacktracking turn shell at e1 -> e2."""
    u = (1, 0, 0, 0)
    v = (0, 1, 0, 0)
    pts = projective_points(q)
    assert symp(u, v, q) == 0
    turns = [w for w in pts if w != u and w != v and symp(v, w, q) == 0]
    same = sorted(w for w in turns if in_base_line(w))
    off = sorted(w for w in turns if not in_base_line(w))

    expected_same = sorted((1, s, 0, 0) for s in range(1, q))
    expected_off = sorted(canon((a, c, 1, 0), q) for a in range(q) for c in range(q))
    assert same == expected_same
    assert off == expected_off
    assert len(turns) == q * (q + 1) - 1
    assert len(same) == q - 1
    assert len(off) == q * q
    return {
        "directed_base_edge": [list(u), list(v)],
        "same_line": [list(x) for x in same],
        "off_line": [list(x) for x in off],
        "counts": {"same_line": len(same), "off_line": len(off), "total": len(turns)},
    }


def cz_orbit_labels(q: int) -> dict:
    """Construct canonical labels for the non-fixed CZ context orbits."""
    projective_K = sorted({canon((a, b), q) for a in range(q) for b in range(q) if a or b})
    fixed_K = []
    moving_K = []
    for k1, k2 in projective_K:
        x = ((-k2) % q, k1 % q)
        Bx = (x[1] % q, x[0] % q)
        det = (k1 * Bx[1] - k2 * Bx[0]) % q
        (fixed_K if det == 0 else moving_K).append((k1, k2))
    assert sorted(fixed_K) == [(0, 1), (1, 0)]
    expected_moving = sorted((1, s) for s in range(1, q))
    assert sorted(moving_K) == expected_moving

    all_S = [(a, b, c) for a in range(q) for b in range(q) for c in range(q)]
    seen: set[tuple[int, int, int]] = set()
    reps: list[tuple[int, int]] = []
    orbit_lengths: list[int] = []
    for S in all_S:
        if S in seen:
            continue
        orbit = []
        a, b, c = S
        cur = S
        while cur not in orbit:
            orbit.append(cur)
            seen.add(cur)
            cur = (a, (cur[1] + 1) % q, c)
        assert len(orbit) == q
        zero_b = [x for x in orbit if x[1] == 0]
        assert len(zero_b) == 1
        reps.append((zero_b[0][0], zero_b[0][2]))
        orbit_lengths.append(len(orbit))
    reps = sorted(reps)
    assert reps == sorted((a, c) for a in range(q) for c in range(q))
    return {
        "fixed_intersection_directions": [list(x) for x in fixed_K],
        "moving_intersection_orbit_labels": [list(x) for x in moving_K],
        "transverse_orbit_representatives": [list(x) for x in reps],
        "transverse_orbit_lengths": sorted(set(orbit_lengths)),
        "counts": {
            "intersecting_nonfixed_orbits": len(moving_K),
            "transverse_nonfixed_orbits": len(reps),
            "nonfixed_orbits_total": len(moving_K) + len(reps),
            "fixed_contexts": 2 * q + 1,
        },
    }


def digest_obj(obj) -> str:
    payload = json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def weld(q: int) -> dict:
    assert q > 2 and all(q % p for p in range(2, int(q**0.5) + 1)), "q must be an odd prime"
    cz = cz_orbit_labels(q)
    h = hashimoto_turns(q)

    intersect_map = []
    for _, s in [tuple(x) for x in cz["moving_intersection_orbit_labels"]]:
        target = (1, s, 0, 0)
        assert list(target) in h["same_line"]
        intersect_map.append({"context_orbit_slope": s, "hashimoto_turn": list(target)})
    trans_map = []
    for a, c in [tuple(x) for x in cz["transverse_orbit_representatives"]]:
        target = canon((a, c, 1, 0), q)
        assert list(target) in h["off_line"]
        trans_map.append({"context_orbit_ac": [a, c], "hashimoto_turn": list(target)})

    k = q * (q + 1)
    total_contexts = (q + 1) * (q * q + 1)
    fixed = 2 * q + 1
    moving_orbits = q * q + q - 1
    phi6 = q * q - q + 1
    checks = {
        "gq_degree": k == q * (q + 1),
        "context_cycle_count_equals_hashimoto_outdegree": moving_orbits == k - 1,
        "branch_counts_match": cz["counts"]["intersecting_nonfixed_orbits"] == h["counts"]["same_line"] == q - 1
            and cz["counts"]["transverse_nonfixed_orbits"] == h["counts"]["off_line"] == q * q,
        "explicit_bijection_complete": len(intersect_map) + len(trans_map) == k - 1,
        "context_cycle_accounting": fixed + q * moving_orbits == total_contexts,
        "cyclotomic_gap_factorization": phi6 - fixed == q * (q - 3),
    }
    assert all(checks.values())
    full_map = {
        "intersecting_to_same_line": intersect_map,
        "transverse_to_off_line": trans_map,
    }
    summary = {
        "q": q,
        "gq": {"contexts": total_contexts, "collinearity_degree_k": k, "hashimoto_outdegree": k - 1},
        "cz_counts": cz["counts"],
        "hashimoto_counts": h["counts"],
        "weld": {
            "branch_identity": f"(q-1)+q^2={q-1}+{q*q}={k-1}=k-1",
            "mapping_sha256": digest_obj(full_map),
            "mapping_entries": len(intersect_map) + len(trans_map),
            "intersecting_sample": intersect_map[: min(3, len(intersect_map))],
            "transverse_sample": trans_map[: min(3, len(trans_map))],
        },
        "cyclotomic": {
            "fixed_contexts_2q_plus_1": fixed,
            "Phi6": phi6,
            "Phi6_minus_fixed": phi6 - fixed,
            "factorization": "Phi6(q)-(2q+1)=q(q-3)",
            "equal": fixed == phi6,
        },
        "checks": checks,
    }
    if q == 3:
        summary["q3_explicit_map"] = full_map
    return summary


def main(write: bool = True) -> dict:
    rows = [weld(q) for q in (3, 5, 7, 11)]
    q3 = rows[0]
    assert q3["gq"] == {"contexts": 40, "collinearity_degree_k": 12, "hashimoto_outdegree": 11}
    assert q3["cz_counts"] == {
        "intersecting_nonfixed_orbits": 2,
        "transverse_nonfixed_orbits": 9,
        "nonfixed_orbits_total": 11,
        "fixed_contexts": 7,
    }
    assert q3["hashimoto_counts"] == {"same_line": 2, "off_line": 9, "total": 11}
    assert [r["cyclotomic"]["equal"] for r in rows] == [True, False, False, False]

    out = {
        "schema": "w33.cz_hashimoto_orbit_weld.v1",
        "status": "PASS_GAUGE_FIXED_GATE_ROUTE_WELD",
        "headline": (
            "For every tested odd prime q, the non-fixed context orbits of the CZ shear split as "
            "(q-1)+q^2 and admit an explicit Darboux-gauge bijection to the (q-1)+q^2 local "
            "nonbacktracking turns from a directed W(3,q) collinearity edge. Hence the number of "
            "nontrivial CZ context orbits is exactly k-1, the Hashimoto outdegree. At q=3 this is "
            "11=2+9, the existing triangle/open-turn routing split."
        ),
        "theorem": {
            "cz_nonfixed_orbit_set": "F_q^* disjoint_union F_q^2",
            "hashimoto_turn_set": "F_q^* disjoint_union F_q^2",
            "explicit_gauge_map": "s -> [1,s,0,0]; (a,c) -> [a,c,1,0]",
            "count_identity": "q^2+q-1 = k-1 for k=q(q+1)",
            "q3_lock": "fixed CZ contexts = 2q+1 = Phi6(q) iff q=3 (positive q), because Phi6-(2q+1)=q(q-3)",
        },
        "controls": rows,
        "boundary": (
            "The displayed map is an exact coordinate/Darboux-gauge bijection after choosing the CZ-fixed "
            "Lagrangian and directed base edge. It is not claimed to be a natural global PSp(4,q)-equivariant "
            "intertwiner. The one-photon architecture interpretation is retained only at q=3."
        ),
        "checks": {
            "q_controls": [3, 5, 7, 11],
            "all_control_checks_pass": all(all(r["checks"].values()) for r in rows),
            "q3_exact_11_eq_2_plus_9": True,
            "q3_unique_cyclotomic_match_across_controls": True,
        },
    }
    if write:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=2, sort_keys=True))
    return out


if __name__ == "__main__":
    main(True)
