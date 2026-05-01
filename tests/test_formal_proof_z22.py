from __future__ import annotations

import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
A_GAUGE = ((2, 0, 0, 1, 2), (0, 0))  # diag(-1,1) in gauge coords
Z22 = (2, 2)


def _pack_witnesses(rows):
    packed = []
    for row in rows:
        line = tuple(sorted((int(p[0]), int(p[1])) for p in row["line"]))
        z = int(row.get("z", 0))
        sign = int(row.get("sign_pm1", row.get("sign", 1)))
        packed.append((line, z, sign))
    return tuple(sorted(packed))


def _transform_packed(packed, affine_elem, z_map):
    import tools.analyze_e6_f3_trilinear_symmetry_breaking as analyze

    mat, shift = affine_elem
    out = []
    for line, z, sign in packed:
        mapped_line = tuple(sorted(analyze._map_point(mat, shift, p) for p in line))
        mapped_z = int(analyze._map_z(z_map, z))
        out.append((mapped_line, mapped_z, int(sign)))
    return tuple(sorted(out))


def test_formal_proof_z22_no_invariant_reps() -> None:
    import tools.analyze_e6_f3_trilinear_symmetry_breaking as analyze

    classified = (
        ROOT
        / "artifacts"
        / "min_cert_census_medium_2026_02_10"
        / "e6_f3_trilinear_min_cert_exact_hessian_full_with_geotypes.json"
    )
    trilinear_map = ROOT / "artifacts" / "e6_f3_trilinear_map.json"
    if not classified.exists() or not trilinear_map.exists():
        pytest.skip(
            "Missing generated E6 trilinear census/map artifacts for Z22 invariant-rep enumeration"
        )
    payload = json.loads(classified.read_text(encoding="utf-8"))
    reps = payload.get("representatives", [])

    # canonical affine flag from product sign
    lines, sign_field = analyze._load_sign_field(trilinear_map)
    product_sign = analyze._line_product_signs(lines, sign_field)
    flag = analyze._line_product_flag_geometry_check(lines, product_sign, [])
    point = flag.get("missing_point") or flag.get(
        "unique_missing_point_from_negative_lines"
    )
    direction = flag.get("full_positive_direction") or flag.get(
        "distinguished_direction_all_positive"
    )
    assert point is not None and direction is not None

    adapted_gauges = analyze._line_product_adapted_gauges(lines, point, direction)

    # pulled-back A elements
    pulled_as = []
    for g in adapted_gauges:
        g_inv = analyze._inverse_affine(g)
        A = analyze._compose_affine(analyze._compose_affine(g_inv, A_GAUGE), g)
        pulled_as.append(A)

    invariant_found = []

    for idx, entry in enumerate(reps):
        rows = entry.get("canonical_repr") or []
        packed = _pack_witnesses(rows)
        for A in pulled_as:
            # fixed lines under A
            mat, shift = A
            fixed_lines = set()
            for line, z, sign in packed:
                mapped_line = tuple(
                    sorted(analyze._map_point(mat, shift, p) for p in line)
                )
                if mapped_line == line:
                    fixed_lines.add(line)

            # closure test on z labels for fixed lines
            closure_ok = True
            for L in fixed_lines:
                zs = {z for (line, z, sign) in packed if line == L}
                mapped_zs = {analyze._map_z(Z22, z) for z in zs}
                if not mapped_zs.issubset(zs):
                    closure_ok = False
                    break
            if not closure_ok:
                continue

            # full transform equality if closure passes
            transformed = _transform_packed(packed, A, Z22)
            if transformed == packed:
                invariant_found.append({"index": idx, "A": A})

    assert (
        invariant_found == []
    ), f"Found invariant representatives under diag(-1,1)+z=(2,2): {invariant_found}"


def test_symbolic_exclude_z22_via_x0() -> None:
    """Short symbolic check: L = x=0 fixed by diag(-1,1) leads to contradiction
    under z_map=(2,2) using closed-form product/sign rules."""
    import tools.analyze_e6_f3_trilinear_symmetry_breaking as analyze

    # vertical line x=0
    L = tuple(sorted(((0, 0), (0, 1), (0, 2))))
    lines = analyze._all_affine_lines()
    assert L in lines

    a, b, c = analyze._normalized_line_abc(L)
    assert (a, b, c) == (1, 0, 0)

    # product sign closed form: P(L)=+1 iff b*c==0
    P = 1 if (b * c) % 3 == 0 else -1

    # full-sign closed form predicts s(L,1)
    s1 = analyze._predict_full_sign_closed_form(L, 1)

    assert P == 1
    assert s1 == -1
    assert (
        P != s1
    ), "Symbolic contradiction failed: P(L) should not equal s(L,1) for z=(2,2)"
