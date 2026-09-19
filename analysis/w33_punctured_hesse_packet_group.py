#!/usr/bin/env python3
r"""Punctured-Hesse packet group behind the W33 CZ/Hashimoto 11-bin alphabet.

This pass strengthens the gauge-fixed CZ-context / Hashimoto-turn weld.

For odd prime q the moving CZ-context orbit labels, and independently the local
Hashimoto nonbacktracking choices, are

    F_q^2  disjoint_union  F_q^*.

Choose homogeneous coordinates [x:y:z] on PG(2,q) and delete the two points

    E_x = [1:0:0],   E_y = [0:1:0]

from the line at infinity z=0.  The remaining projective points are exactly

    affine:    [a:c:1],                 (a,c) in F_q^2
    infinity:  [1:s:0],                 s in F_q^*.

Thus the common moving alphabet is the two-punctured projective plane

    PG(2,q) \ {E_x,E_y},

of size q^2+q-1=k-1.

At q=3 this becomes 11=9+2.  The repository's frequency-bin compiler already
uses exactly nine Hesse bins H0..H8 plus two Hashimoto sidebands.  Its Hesse
metadata has route_trit=floor(h/3), phase_trit=h mod 3, hence it is already an
explicit affine-coordinate chart F_3^2.  The two sidebands can therefore be
placed on the two surviving infinity points [1:1:0], [1:2:0].  Which sideband
is assigned to which infinity point is an ABI gauge convention.

There is a second exact closure.  The setwise stabilizer in PGL(3,3) of the
deleted pair {E_x,E_y} is the affine monomial group

    F_3^2 semidirect D_8

of order 9*8=72.  Writing

    R = [[0,-1],[1,0]],    S = [[1,0],[0,-1]]

over F_3, D_8=<R,S | R^4=S^2=1, SRS=R^-1>.  The current packet-frame radix

    9 Hesse bins * 2 Hashimoto sectors * 4 probe slots = 72

therefore admits a group-native overlay

    (h, sector, probe) -> (translation t_h, S^sector R^probe).

This is a bijection from the 72 packet slots to the 72 projective symmetries of
the punctured plane.  The action has exactly two point-orbits of sizes 9 and 2:
the affine Hesse chart and the surviving infinity pair.  This makes the existing
9+2 compiler split an orbit decomposition, not merely a count match.

Boundary:
* the projective-plane and group statements are exact;
* the assignment gauge/chiral <-> the two surviving infinity points is a chosen
  ABI convention and may be swapped;
* the 72-slot group overlay is an optional exact control semantics.  It does not
  assert that the present optical hardware dynamically implements PGL(3,3), nor
  that the existing sector/probe meanings were originally derived from D8.
"""
from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_punctured_hesse_packet_group.json"


def inv(a: int, q: int) -> int:
    return pow(a % q, -1, q)


def canon(v: tuple[int, ...], q: int) -> tuple[int, ...]:
    j = next(i for i, x in enumerate(v) if x % q)
    z = inv(v[j], q)
    return tuple((z * x) % q for x in v)


def projective_points_2(q: int) -> list[tuple[int, int, int]]:
    return sorted(
        {
            canon((x, y, z), q)
            for x in range(q)
            for y in range(q)
            for z in range(q)
            if x or y or z
        }
    )


def dot3(a: tuple[int, int, int], b: tuple[int, int, int], q: int) -> int:
    return sum(x * y for x, y in zip(a, b)) % q


def mat2_mul(A: tuple[int, int, int, int], B: tuple[int, int, int, int], q: int):
    return tuple(
        sum(A[2 * i + k] * B[2 * k + j] for k in range(2)) % q
        for i in range(2)
        for j in range(2)
    )


def mat2_pow(A: tuple[int, int, int, int], n: int, q: int):
    out = (1, 0, 0, 1)
    for _ in range(n):
        out = mat2_mul(out, A, q)
    return out


def mat3_vec(M: tuple[int, ...], v: tuple[int, int, int], q: int):
    return tuple(
        sum(M[3 * i + j] * v[j] for j in range(3)) % q
        for i in range(3)
    )


def projective_act(M: tuple[int, ...], v: tuple[int, int, int], q: int):
    return canon(mat3_vec(M, v, q), q)


def punctured_plane(q: int):
    pts = projective_points_2(q)
    ex = (1, 0, 0)
    ey = (0, 1, 0)
    punctured = [p for p in pts if p not in {ex, ey}]
    affine_canon = sorted(p for p in punctured if p[2] != 0)
    infinity_canon = sorted(p for p in punctured if p[2] == 0)

    # Use the physically convenient affine-chart representatives [a:c:1] and
    # infinity representatives [1:s:0] in the public certificate.  The global
    # projective canonicalizer instead normalizes the *first* nonzero coordinate,
    # so compare only after canonicalization; equating the two representative
    # lists literally was the CI bug caught by the first replay.
    affine = sorted((a, cc, 1) for a in range(q) for cc in range(q))
    infinity = sorted((1, s, 0) for s in range(1, q))
    assert sorted({canon(p, q) for p in affine}) == affine_canon
    assert sorted({canon(p, q) for p in infinity}) == infinity_canon

    # Projective lines are dual projective coefficient triples.
    hist = Counter()
    line_rows = []
    for ell in pts:
        sub = sorted(p for p in punctured if dot3(ell, p, q) == 0)
        hist[len(sub)] += 1
        line_rows.append({"line": list(ell), "retained_points": [list(p) for p in sub]})

    expected_hist = {q - 1: 1, q: 2 * q, q + 1: q * (q - 1)}
    assert dict(sorted(hist.items())) == expected_hist
    return {
        "q": q,
        "deleted": [list(ex), list(ey)],
        "affine": [list(p) for p in affine],
        "infinity": [list(p) for p in infinity],
        "size": len(punctured),
        "line_size_histogram": {str(k): v for k, v in sorted(hist.items())},
        "expected_line_size_histogram": {str(k): v for k, v in sorted(expected_hist.items())},
        "line_rows": line_rows,
    }


def d8_linear_elements():
    q = 3
    I = (1, 0, 0, 1)
    R = (0, 2, 1, 0)  # [[0,-1],[1,0]]
    S = (1, 0, 0, 2)  # [[1,0],[0,-1]]
    rows = []
    for sector in range(2):
        for probe in range(4):
            L = mat2_mul(mat2_pow(S, sector, q), mat2_pow(R, probe, q), q)
            rows.append((sector, probe, L))
    assert len({L for _, _, L in rows}) == 8

    # D8 presentation.
    assert mat2_pow(R, 4, q) == I
    assert mat2_pow(S, 2, q) == I
    lhs = mat2_mul(mat2_mul(S, R, q), S, q)
    rhs = mat2_pow(R, 3, q)
    assert lhs == rhs
    return I, R, S, rows


def affine_projective_matrix(t: tuple[int, int], L: tuple[int, int, int, int]):
    a, b, c, d = L
    tx, ty = t
    return (a, b, tx, c, d, ty, 0, 0, 1)


def packet_group_72():
    q = 3
    _, R, S, d8 = d8_linear_elements()
    plane = punctured_plane(q)
    punct = [canon(tuple(p), q) for p in plane["affine"] + plane["infinity"]]
    deleted = {tuple(p) for p in plane["deleted"]}

    rows = []
    matrices = set()
    permutations = set()
    for h in range(9):
        route, phase = divmod(h, 3)
        t = (route, phase)
        for sector, probe, L in d8:
            M = affine_projective_matrix(t, L)
            assert M not in matrices
            matrices.add(M)
            assert {projective_act(M, p, q) for p in deleted} == deleted
            perm = tuple(punct.index(projective_act(M, p, q)) for p in punct)
            permutations.add(perm)
            slot = h * 8 + sector * 4 + probe
            rows.append(
                {
                    "packet_slot": slot,
                    "hesse_bin": h,
                    "route_trit": route,
                    "phase_trit": phase,
                    "hashimoto_sector_id": sector,
                    "probe_slot": probe,
                    "translation": [route, phase],
                    "linear_D8": [[L[0], L[1]], [L[2], L[3]]],
                }
            )
    rows.sort(key=lambda x: x["packet_slot"])
    assert [r["packet_slot"] for r in rows] == list(range(72))
    assert len(matrices) == len(permutations) == 72

    # Orbit decomposition on the 11 retained points.
    def orbit(seed):
        return {
            projective_act(M, seed, q)
            for M in matrices
        }

    seen = set()
    orbits = []
    for p in punct:
        if p in seen:
            continue
        o = orbit(p)
        seen |= o
        orbits.append(sorted(o))
    orbit_sizes = sorted(len(o) for o in orbits)
    assert orbit_sizes == [2, 9]

    # The affine 9-orbit and infinity 2-orbit are intrinsic.
    def chart_rep(p):
        # Present the two intrinsic orbits in the same chart gauge used by the
        # compiler certificate: affine points have z=1, surviving infinity
        # points have x=1.  Internally the action remains globally canonical.
        if p[2] % q:
            z = inv(p[2], q)
            return tuple((z * x) % q for x in p)
        x = inv(p[0], q)
        return tuple((x * y) % q for y in p)

    orbit_types = sorted(
        [
            {
                "size": len(o),
                "z_values": sorted({chart_rep(p)[2] for p in o}),
                "points": [list(p) for p in sorted(chart_rep(x) for x in o)],
            }
            for o in orbits
        ],
        key=lambda x: x["size"],
    )
    assert orbit_types[0]["z_values"] == [0]
    assert orbit_types[1]["z_values"] == [1]

    return {
        "order": 72,
        "structure": "F_3^2 semidirect D_8",
        "presentation": "D8=<R,S | R^4=S^2=1, SRS=R^-1>",
        "R": [[R[0], R[1]], [R[2], R[3]]],
        "S": [[S[0], S[1]], [S[2], S[3]]],
        "slot_rows": rows,
        "point_orbits": orbit_types,
        "orbit_sizes": orbit_sizes,
        "distinct_projective_permutations": len(permutations),
    }


def check_frequency_compiler():
    freq = json.loads((ROOT / "data" / "w33_frequency_bin_hashimoto_compiler.json").read_text())
    assert freq["verified"] is True
    plan = freq["frequency_plan"]
    probe = freq["probe_budget"]

    hesse = plan["hesse_bins"]
    side = plan["hashimoto_sidebands"]
    assert len(hesse) == 9 and len(side) == 2 and plan["total_bins"] == 11

    hrows = []
    for row in hesse:
        h = row["bin_index"]
        route, phase = divmod(h, 3)
        assert row["route_trit"] == route
        assert row["phase_trit"] == phase
        hrows.append(
            {
                "label": row["label"],
                "bin_index": h,
                "affine_coordinate": [route, phase, 1],
            }
        )

    # This assignment is a coordinate convention; swapping the two rows is equally valid.
    side_rows = [
        {
            "label": side[0]["label"],
            "sector": side[0]["sector"],
            "projective_coordinate": [1, 1, 0],
            "assignment_scope": "ABI convention; may be swapped with the other infinity point",
        },
        {
            "label": side[1]["label"],
            "sector": side[1]["sector"],
            "projective_coordinate": [1, 2, 0],
            "assignment_scope": "ABI convention; may be swapped with the other infinity point",
        },
    ]

    packet_frame_slots = (
        probe["hesse_phase_bins_per_packet"]
        * probe["sector_count"]
        * probe["runtime_slots_per_phase_probe"]
    )
    assert packet_frame_slots == 72
    return {
        "source_verified": True,
        "total_bins": plan["total_bins"],
        "hesse_bins": hrows,
        "sidebands": side_rows,
        "packet_frame_factorization": "9*2*4=72",
        "packet_frame_slots": packet_frame_slots,
        "source_certificate": "data/w33_frequency_bin_hashimoto_compiler.json",
    }


def check_cz_hashimoto_weld():
    weld = json.loads((ROOT / "data" / "w33_cz_hashimoto_orbit_weld.json").read_text())
    assert weld["status"] == "PASS_GAUGE_FIXED_GATE_ROUTE_WELD"
    q3 = next(r for r in weld["controls"] if r["q"] == 3)
    assert q3["cz_counts"]["nonfixed_orbits_total"] == 11
    assert q3["cz_counts"]["intersecting_nonfixed_orbits"] == 2
    assert q3["cz_counts"]["transverse_nonfixed_orbits"] == 9
    assert q3["hashimoto_counts"] == {"same_line": 2, "off_line": 9, "total": 11}
    return {
        "source_verified": True,
        "moving_alphabet": "F_3^2 disjoint_union F_3^*",
        "branch_counts": {"affine": 9, "infinity": 2, "total": 11},
        "source_certificate": "data/w33_cz_hashimoto_orbit_weld.json",
    }


def build():
    controls = [punctured_plane(q) for q in (3, 5, 7, 11)]
    for row in controls:
        q = row["q"]
        assert row["size"] == q * q + q - 1
    group = packet_group_72()
    freq = check_frequency_compiler()
    weld = check_cz_hashimoto_weld()

    # |Stab_PGL(3,q)({two points})| = 2 q^2 (q-1)^2.
    # Matching the current 72-slot frame gives q(q-1)=6, hence q=3 for positive q.
    assert 2 * 3**2 * (3 - 1) ** 2 == 72

    checks = {
        "two_punctured_plane_size_is_k_minus_1": all(
            r["size"] == r["q"] ** 2 + r["q"] - 1 for r in controls
        ),
        "q3_is_9_plus_2": len(controls[0]["affine"]) == 9 and len(controls[0]["infinity"]) == 2,
        "q3_incidence_profile_is_2_1__3_6__4_6": controls[0]["line_size_histogram"]
        == {"2": 1, "3": 6, "4": 6},
        "packet_group_order_is_72": group["order"] == 72,
        "packet_group_is_faithful_on_11_points": group["distinct_projective_permutations"] == 72,
        "packet_group_orbits_are_9_and_2": group["orbit_sizes"] == [2, 9],
        "frequency_bins_are_exactly_9_plus_2": freq["total_bins"] == 11
        and len(freq["hesse_bins"]) == 9
        and len(freq["sidebands"]) == 2,
        "packet_frame_radix_is_group_order": freq["packet_frame_slots"] == group["order"] == 72,
        "parent_weld_is_9_plus_2": weld["branch_counts"] == {"affine": 9, "infinity": 2, "total": 11},
        "q3_unique_positive_integer_frame_match": all(
            (2 * q * q * (q - 1) * (q - 1) == 72) == (q == 3)
            for q in range(1, 20)
        ),
    }
    assert all(checks.values())

    return {
        "schema": "w33.punctured_hesse_packet_group.v1",
        "status": "PASS_TWO_PUNCTURE_PACKET_GROUP",
        "headline": (
            "The common CZ-context/Hashimoto moving alphabet F_q^2 disjoint_union F_q^* is exactly "
            "PG(2,q) with two points removed from the line at infinity. At q=3 the 11-bin frequency "
            "plan is therefore a two-punctured Hesse projective plane: 9 affine Hesse bins plus 2 "
            "surviving infinity points. The setwise PGL(3,3) stabilizer of the deleted pair is "
            "F_3^2 semidirect D8 of order 72, exactly the packet-frame radix 9*2*4. Its action on "
            "the 11 retained points has the intrinsic orbit split 9+2."
        ),
        "theorem": {
            "moving_alphabet": "PG(2,q) minus {[1:0:0],[0:1:0]} = F_q^2 disjoint_union F_q^*",
            "size": "q^2+q-1 = k-1",
            "line_profile": "one retained line of size q-1; 2q lines of size q; q(q-1) lines of size q+1",
            "pair_stabilizer_order": "2 q^2 (q-1)^2",
            "q3_pair_stabilizer": "F_3^2 semidirect D8, order 72",
            "q3_point_orbits": "9 affine Hesse points + 2 surviving infinity points",
            "packet_overlay": "(h,sector,probe) -> translation(route_trit,phase_trit) * S^sector R^probe",
        },
        "controls": [
            {
                "q": r["q"],
                "size": r["size"],
                "affine_count": len(r["affine"]),
                "infinity_count": len(r["infinity"]),
                "line_size_histogram": r["line_size_histogram"],
            }
            for r in controls
        ],
        "q3_geometry": {
            "deleted": controls[0]["deleted"],
            "affine": controls[0]["affine"],
            "infinity": controls[0]["infinity"],
            "size": controls[0]["size"],
            "line_size_histogram": controls[0]["line_size_histogram"],
        },
        "q3_group": {
            "order": group["order"],
            "structure": group["structure"],
            "presentation": group["presentation"],
            "R": group["R"],
            "S": group["S"],
            "point_orbits": group["point_orbits"],
            "orbit_sizes": group["orbit_sizes"],
            "distinct_projective_permutations": group["distinct_projective_permutations"],
            "slot_overlay": {
                "formula": "slot=8*h+4*sector+probe",
                "first_four": group["slot_rows"][:4],
                "last_four": group["slot_rows"][-4:],
            },
        },
        "frequency_compiler_bridge": freq,
        "cz_hashimoto_parent": weld,
        "checks": checks,
        "boundary": (
            "The finite projective geometry, stabilizer group and 72-slot bijection are exact. "
            "Assigning gauge/chiral to the two surviving infinity points is an ABI gauge choice and "
            "may be swapped. The group-native packet overlay is a new exact control semantics, not "
            "a claim that the present optical hardware physically implements PGL(3,3) dynamics."
        ),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()
    out = build()
    if args.write:
        OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
