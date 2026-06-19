#!/usr/bin/env python3
"""BT1318 - C2-axis assignment for the seven toroidal realizations.

BT803/CCCCXXI prove the numerical heptad: five Csaszar realizations and
two Szilassi realizations.  The tempting next claim would be "the seven
metric realizations are the seven abstract half-turn axes."  The current
coordinate data does not prove that.  It proves a sharper and more honest
object-level fact:

  * the abstract Csaszar map has automorphism group C7:C6 of order 42;
  * it has exactly seven involutions, each fixing one Csaszar vertex;
  * the published metric Csaszar coordinates all use the same involution,
    fixing vertex 6;
  * the published Szilassi coordinates use the dual C2, fixing one face
    and no vertex.

So the data gives two family-level axis carriers, not a one-realization per
involution enumeration.
"""

from __future__ import annotations

import importlib.util
import itertools
import json
import sys
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]
OUT_PATH = ROOT / "data" / "bt1318_toroidal_c2_axis_assignment.json"


def _load_module(name: str, relpath: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relpath)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load module at {relpath}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def _face_set(faces: Iterable[Iterable[int]]) -> set[frozenset[int]]:
    return {frozenset(face) for face in faces}


def _map_faces(
    faces: list[tuple[int, ...]], perm: tuple[int, ...]
) -> set[frozenset[int]]:
    return {frozenset(perm[v] for v in face) for face in faces}


def _csaszar_map_automorphisms(c: Any) -> list[tuple[int, ...]]:
    target = _face_set(c.CSASZAR_FACES)
    autos: list[tuple[int, ...]] = []
    for perm in itertools.permutations(range(c.CSASZAR_V)):
        if _map_faces(c.CSASZAR_FACES, perm) == target:
            autos.append(tuple(perm))
    return autos


def _perm_order(perm: tuple[int, ...]) -> int:
    identity = tuple(range(len(perm)))
    cur = identity
    order = 0
    while True:
        order += 1
        cur = tuple(perm[i] for i in cur)
        if cur == identity:
            return order


def _orbits(n: int, perm: tuple[int, ...]) -> list[list[int]]:
    seen = [False] * n
    out: list[list[int]] = []
    for i in range(n):
        if seen[i]:
            continue
        orbit: list[int] = []
        j = i
        while not seen[j]:
            seen[j] = True
            orbit.append(j)
            j = perm[j]
        out.append(orbit)
    return out


def _fixed_points(perm: tuple[int, ...]) -> list[int]:
    return [i for i, image in enumerate(perm) if image == i]


def _face_perm(faces: list[tuple[int, ...]], perm: tuple[int, ...]) -> tuple[int, ...]:
    indexed = {frozenset(face): i for i, face in enumerate(faces)}
    image: list[int] = []
    for face in faces:
        mapped = frozenset(perm[v] for v in face)
        image.append(indexed[mapped])
    return tuple(image)


def build_assignment() -> dict[str, Any]:
    c = _load_module("ccccxxi", "exploration/PART_CCCCXXI_TOROIDAL_FANO_BRIDGE.py")

    cs_autos = _csaszar_map_automorphisms(c)
    order_profile: dict[int, int] = {}
    for perm in cs_autos:
        order = _perm_order(perm)
        order_profile[order] = order_profile.get(order, 0) + 1

    involutions = sorted(perm for perm in cs_autos if _perm_order(perm) == 2)
    involution_fixed_vertices = [_fixed_points(perm) for perm in involutions]
    fixed_vertex_cover = sorted(
        vs[0] for vs in involution_fixed_vertices if len(vs) == 1
    )

    cs_axis = tuple(c.CSASZAR_C2_PERM)
    sz_axis = tuple(c.SZILASSI_C2_PERM)
    cs_face_axis = _face_perm(c.CSASZAR_FACES, cs_axis)
    sz_face_axis = _face_perm(c.SZILASSI_FACES, sz_axis)

    cs_metric_records = []
    for version, coords in sorted(c.CSASZAR_COORDS.items()):
        cs_metric_records.append(
            {
                "realization": f"C{version}",
                "c2_symmetric": bool(c._is_c2_symmetric(coords)),
                "fixed_vertex": _fixed_points(cs_axis),
                "vertex_orbits": _orbits(c.CSASZAR_V, cs_axis),
                "face_orbits": _orbits(c.CSASZAR_F, cs_face_axis),
            }
        )

    sz_metric_records = []
    for version, coords in sorted(c.SZILASSI_COORDS.items()):
        sz_metric_records.append(
            {
                "realization": f"S{version}",
                "c2_symmetric": bool(c._is_c2_symmetric(coords)),
                "fixed_vertices": _fixed_points(sz_axis),
                "fixed_faces": _fixed_points(sz_face_axis),
                "vertex_orbits": _orbits(c.SZILASSI_V, sz_axis),
                "face_orbits": _orbits(c.SZILASSI_F, sz_face_axis),
            }
        )

    checks = {
        "csaszar_abstract_map_aut_order_42": len(cs_autos) == 42,
        "csaszar_order_profile_is_C7_semidirect_C6": order_profile
        == {1: 1, 2: 7, 3: 14, 6: 14, 7: 6},
        "csaszar_has_seven_involutions": len(involutions) == 7,
        "every_csaszar_involution_fixes_one_vertex": all(
            len(vertices) == 1 for vertices in involution_fixed_vertices
        ),
        "csaszar_involutions_cover_all_vertices": fixed_vertex_cover
        == list(range(c.CSASZAR_V)),
        "published_csaszar_axis_is_one_involution": cs_axis in involutions,
        "published_csaszar_axis_fixes_vertex_6": _fixed_points(cs_axis) == [6],
        "all_metric_csaszar_realizations_use_same_axis": all(
            record["c2_symmetric"] and record["fixed_vertex"] == [6]
            for record in cs_metric_records
        ),
        "published_szilassi_axis_has_no_fixed_vertices": _fixed_points(sz_axis) == [],
        "published_szilassi_axis_fixes_one_face": _fixed_points(sz_face_axis) == [4],
        "all_metric_szilassi_realizations_use_same_dual_axis": all(
            record["c2_symmetric"] and record["fixed_faces"] == [4]
            for record in sz_metric_records
        ),
        "orbit_duality_is_4_7_vs_7_4": (
            len(_orbits(c.CSASZAR_V, cs_axis)),
            len(_orbits(c.CSASZAR_F, cs_face_axis)),
            len(_orbits(c.SZILASSI_V, sz_axis)),
            len(_orbits(c.SZILASSI_F, sz_face_axis)),
        )
        == (4, 7, 7, 4),
    }

    return {
        "theorem": "BT1318 toroidal C2-axis assignment",
        "verified": all(checks.values()),
        "csaszar_abstract_automorphism_group": {
            "order": len(cs_autos),
            "order_profile": {str(k): v for k, v in sorted(order_profile.items())},
            "structure_reading": "C7:C6; seven involutions, each fixing one vertex",
            "involutions": [list(perm) for perm in involutions],
            "involution_fixed_vertices": involution_fixed_vertices,
        },
        "metric_axis_records": {
            "csaszar": cs_metric_records,
            "szilassi": sz_metric_records,
            "csaszar_axis_perm": list(cs_axis),
            "csaszar_face_axis_perm": list(cs_face_axis),
            "szilassi_axis_perm": list(sz_axis),
            "szilassi_face_axis_perm": list(sz_face_axis),
        },
        "axis_assignment": {
            "current_data_proves": (
                "the five metric Csaszar realizations share the vertex-axis "
                "involution fixing vertex 6, while the two metric Szilassi "
                "realizations share the dual face-axis involution fixing face 4"
            ),
            "not_proved": (
                "the seven metric realizations are not currently distinguished "
                "as the seven abstract C2 involutions"
            ),
            "realization_to_involution_bijection_status": "not_proved_current_labels",
        },
        "checks": checks,
    }


def write_results(path: Path = OUT_PATH) -> Path:
    payload = build_assignment()
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def main() -> None:
    payload = build_assignment()
    out = write_results()
    print(f"BT1318 verified={payload['verified']} wrote {out}")
    if not payload["verified"]:
        failed = [name for name, ok in payload["checks"].items() if not ok]
        raise SystemExit(f"BT1318 failed checks: {failed}")


if __name__ == "__main__":
    main()
