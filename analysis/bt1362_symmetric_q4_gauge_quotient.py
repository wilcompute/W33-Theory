#!/usr/bin/env python3
"""BT1362: a symmetric Q4 gauge quotient for the holonet router.

BT1341 proved a valid [[32,4,4]] gauge quotient for the Q4 edge code.
BT1344 then showed that its particular quotient is generic under the full
4-cube automorphism group.  This verifier promotes the next structural layer:
there is also a valid [[32,4,4]] quotient whose stabilizer contains the full
translation group C2^4 and a cyclic order-four rotation of the coordinate axes.

The resulting stabilizer is C2^4 : C4 of order 64, and the quotient orbit has
six elements, the six cyclic orders of the four Q4 axes.
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.bt1341_q4_gauge_quotient_3244 import (  # noqa: E402
    N,
    basis_list,
    build_cube,
    combo,
    dot,
    in_span,
    min_distance_x,
    min_distance_z,
    nullspace,
    rank,
)
from tools.bt1344_canonicalize_q4_quotient import (  # noqa: E402
    build_cube as build_cube_with_edges,
)
from tools.bt1344_canonicalize_q4_quotient import edge_perm, permute_mask

OUT = ROOT / "data" / "bt1362_symmetric_q4_gauge_quotient.json"

GENERIC_BT1341_QUOTIENT = [0x79B8, 0x7A2E, 0x9EA1, 0xADA0]
SYMMETRIC_QUOTIENT = [0x024A, 0x4805, 0xBDBE, 0x11D31]
CYCLIC_AXIS_PERMS = {
    (0, 1, 2, 3),
    (1, 2, 3, 0),
    (2, 3, 0, 1),
    (3, 0, 1, 2),
}


def span_key(rows: list[int], n: int) -> tuple[int, ...]:
    """Canonical key by enumerating the entire tiny F2 row span."""

    basis = basis_list(rows, n)
    return tuple(sorted(combo(mask, basis) for mask in range(1 << len(basis))))


def same_span(a_rows: list[int], b_rows: list[int], n: int) -> bool:
    """Rank-and-containment rowspace equality over F2."""

    a_basis = basis_list(a_rows, n)
    b_basis = basis_list(b_rows, n)
    return len(a_basis) == len(b_basis) and all(
        in_span(row, a_basis) for row in b_basis
    )


def quotient_span(rows: list[int]) -> set[int]:
    basis = basis_list(rows, 17)
    return {combo(mask, basis) for mask in range(1, 1 << len(basis))}


def low_weight_dual_obstructions(
    cycle_basis: list[int], hx_basis: list[int]
) -> set[int]:
    bad: set[int] = set()
    for w in range(1, 4):
        for c in itertools.combinations(range(N), w):
            m = sum(1 << i for i in c)
            if in_span(m, hx_basis):
                continue
            f = 0
            for j, cyc in enumerate(cycle_basis):
                if dot(m, cyc):
                    f |= 1 << j
            if f:
                bad.add(f)
    return bad


def make_cycle_coordinate_lookup(cycle_basis: list[int]) -> dict[int, int]:
    return {combo(mask, cycle_basis): mask for mask in range(1 << len(cycle_basis))}


def active_functional_transform(f: int, cols: list[int]) -> int:
    """Active action on quotient constraints: row f maps to f A."""

    out = 0
    for j, col in enumerate(cols):
        if dot(f, col):
            out |= 1 << j
    return out


def coordinate_action_columns(
    cycle_basis: list[int],
    coord_lookup: dict[int, int],
    verts,
    edges,
    edge_key,
    perm: tuple[int, int, int, int],
    flip: int,
) -> list[int]:
    ep = edge_perm(verts, edges, edge_key, perm, flip)
    return [coord_lookup[permute_mask(cyc, ep)] for cyc in cycle_basis]


def quotient_orbit_and_stabilizer(
    quotient_rows: list[int],
    cycle_basis: list[int],
    coord_lookup: dict[int, int],
    verts,
    edges,
    edge_key,
) -> tuple[set[tuple[int, ...]], list[dict[str, object]]]:
    original = span_key(quotient_rows, len(cycle_basis))
    orbit: set[tuple[int, ...]] = set()
    stabilizer: list[dict[str, object]] = []
    for perm in itertools.permutations(range(4)):
        perm4 = tuple(perm)
        for flip in range(16):
            cols = coordinate_action_columns(
                cycle_basis, coord_lookup, verts, edges, edge_key, perm4, flip
            )
            transformed = [
                active_functional_transform(row, cols) for row in quotient_rows
            ]
            key = span_key(transformed, len(cycle_basis))
            orbit.add(key)
            if key == original:
                stabilizer.append({"perm": list(perm4), "flip": flip})
    return orbit, stabilizer


def stabilizer_preserves_hz(
    hz: list[int],
    verts,
    edges,
    edge_key,
    stabilizer: list[dict[str, object]],
) -> bool:
    for entry in stabilizer:
        perm = tuple(entry["perm"])
        flip = int(entry["flip"])
        ep = edge_perm(verts, edges, edge_key, perm, flip)
        transformed = [permute_mask(row, ep) for row in hz]
        if not same_span(hz, transformed, N):
            return False
    return True


def hz_stabilizer_size(hz: list[int], verts, edges, edge_key) -> int:
    count = 0
    for perm in itertools.permutations(range(4)):
        perm4 = tuple(perm)
        for flip in range(16):
            ep = edge_perm(verts, edges, edge_key, perm4, flip)
            if same_span(hz, [permute_mask(row, ep) for row in hz], N):
                count += 1
    return count


def build_code_payload(quotient_rows: list[int]) -> dict[str, object]:
    hx, faces = build_cube()
    cycle_basis = basis_list(faces, N)
    hx_basis = basis_list(hx, N)
    bad = low_weight_dual_obstructions(cycle_basis, hx_basis)

    q_span = quotient_span(quotient_rows)
    kernel_coords = nullspace(quotient_rows, len(cycle_basis))
    hz = [combo(u, cycle_basis) for u in kernel_coords]
    hz_basis = basis_list(hz, N)
    dx, xw = min_distance_x(hz, hx_basis)
    dz, zw = min_distance_z(hx, hz_basis)

    return {
        "cycle_basis": cycle_basis,
        "hx": hx,
        "hx_basis": hx_basis,
        "bad": bad,
        "kernel_coords": kernel_coords,
        "hz": hz,
        "hz_basis": hz_basis,
        "dx": dx,
        "dz": dz,
        "xw": xw,
        "zw": zw,
        "checks": {
            "raw_cycle_rank_17": rank(faces, N) == 17,
            "hx_rank_15": rank(hx, N) == 15,
            "quotient_rank_4": rank(quotient_rows, len(cycle_basis)) == 4,
            "quotient_avoids_weight_lt4_dual_obstructions": q_span.isdisjoint(bad),
            "hz_rank_13": rank(hz, N) == 13,
            "commutes": all(dot(a, b) == 0 for a in hx for b in hz),
            "k_is_4": N - rank(hx, N) - rank(hz, N) == 4,
            "x_distance_4": dx == 4,
            "z_distance_4": dz == 4,
        },
    }


def supports(mask: int | None) -> list[int]:
    if mask is None:
        return []
    return [i for i in range(N) if (mask >> i) & 1]


def build_result() -> dict[str, object]:
    payload = build_code_payload(SYMMETRIC_QUOTIENT)
    generic_payload = build_code_payload(GENERIC_BT1341_QUOTIENT)
    cycle_basis = payload["cycle_basis"]
    verts, edges, edge_key, _faces = build_cube_with_edges()
    coord_lookup = make_cycle_coordinate_lookup(cycle_basis)

    symmetric_orbit, symmetric_stabilizer = quotient_orbit_and_stabilizer(
        SYMMETRIC_QUOTIENT, cycle_basis, coord_lookup, verts, edges, edge_key
    )
    generic_orbit, generic_stabilizer = quotient_orbit_and_stabilizer(
        GENERIC_BT1341_QUOTIENT, cycle_basis, coord_lookup, verts, edges, edge_key
    )

    expected_stabilizer = [
        {"perm": list(perm), "flip": flip}
        for perm in sorted(CYCLIC_AXIS_PERMS)
        for flip in range(16)
    ]
    expected_stabilizer_set = {
        (tuple(entry["perm"]), entry["flip"]) for entry in expected_stabilizer
    }
    actual_stabilizer_set = {
        (tuple(entry["perm"]), entry["flip"]) for entry in symmetric_stabilizer
    }

    hz = payload["hz"]
    hz_stab_size = hz_stabilizer_size(hz, verts, edges, edge_key)

    checks = dict(payload["checks"])
    checks.update(
        {
            "generic_bt1341_stabilizer_is_1": len(generic_stabilizer) == 1
            and len(generic_orbit) == 384,
            "symmetric_stabilizer_order_64": len(symmetric_stabilizer) == 64,
            "symmetric_orbit_size_6": len(symmetric_orbit) == 6,
            "orbit_stabilizer_384": len(symmetric_orbit) * len(symmetric_stabilizer)
            == 384,
            "stabilizer_is_all_translations_times_c4_axis_cycle": actual_stabilizer_set
            == expected_stabilizer_set,
            "hz_rowspace_has_same_64_stabilizer": hz_stab_size == 64,
            "stabilizer_preserves_hz_rowspace": stabilizer_preserves_hz(
                hz, verts, edges, edge_key, symmetric_stabilizer
            ),
        }
    )

    result = {
        "bt": 1362,
        "title": "Symmetric Q4 gauge quotient and cyclic-axis holonet clock",
        "verified": all(checks.values()),
        "code": {
            "n": N,
            "rank_hx": rank(payload["hx"], N),
            "rank_hz": rank(payload["hz"], N),
            "k": N - rank(payload["hx"], N) - rank(payload["hz"], N),
            "dx": payload["dx"],
            "dz": payload["dz"],
        },
        "quotient": {
            "symmetric_functionals_hex": [hex(x) for x in SYMMETRIC_QUOTIENT],
            "generic_bt1341_functionals_hex": [hex(x) for x in GENERIC_BT1341_QUOTIENT],
            "kernel_coordinate_basis_hex": [hex(x) for x in payload["kernel_coords"]],
            "hz_rows_hex": [hex(x) for x in payload["hz"]],
            "x_weight4_witness_edges": supports(payload["xw"]),
            "z_weight4_witness_edges": supports(payload["zw"]),
            "bad_weight_lt4_dual_functional_count": len(payload["bad"]),
        },
        "symmetry": {
            "cube_automorphism_group_order": 384,
            "generic_bt1341_active_orbit_size": len(generic_orbit),
            "generic_bt1341_active_stabilizer_size": len(generic_stabilizer),
            "symmetric_active_orbit_size": len(symmetric_orbit),
            "symmetric_active_stabilizer_size": len(symmetric_stabilizer),
            "hz_rowspace_stabilizer_size": hz_stab_size,
            "stabilizer_structure": "C2^4 : C4",
            "stabilizer_generators": {
                "translations": "all 16 Q4 bit flips",
                "axis_cycle": [1, 2, 3, 0],
            },
            "stabilizer_elements": symmetric_stabilizer,
            "cyclic_axis_order_count": 6,
        },
        "checks": checks,
        "interpretation": (
            "BT1341's original [[32,4,4]] quotient is valid but generic.  "
            "The BT1362 quotient proves the same code parameters while keeping "
            "a 64-element affine cyclic stabilizer C2^4:C4.  Architecturally, "
            "the Q4 packet router can be gauge-fixed to a cyclic four-axis "
            "clock; the remaining six-element orbit is exactly the choice of "
            "cyclic ordering of the four hypercube axes."
        ),
        "boundary": (
            "This is a finite binary Q4 gauge-quotient theorem.  It does not "
            "by itself identify the quotient with the full W33, tomotope, or "
            "Clifford algebra action; those are the next objectwise intertwiners."
        ),
    }
    return result


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=OUT)
    ns = ap.parse_args()
    result = build_result()
    ns.out.parent.mkdir(parents=True, exist_ok=True)
    ns.out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "bt": result["bt"],
                "verified": result["verified"],
                "code": result["code"],
                "stabilizer": result["symmetry"]["stabilizer_structure"],
                "stabilizer_order": result["symmetry"][
                    "symmetric_active_stabilizer_size"
                ],
                "orbit_size": result["symmetry"]["symmetric_active_orbit_size"],
            },
            indent=2,
        )
    )
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
