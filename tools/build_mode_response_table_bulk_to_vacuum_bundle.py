#!/usr/bin/env python3
"""
Recompute the Aut(W33)-orbit decomposition of quotient tetrahedra and the induced
mode-resolved transfer to the 90-line vacuum sector.

This reproduces the bundle:
  - W33_mode_response_table_bulk_to_vacuum_bundle.zip

Inputs (all are existing local artifact bundles):
  - W33_holonomy_phase_decomposition_bundle.zip
      * tetra_coboundary_dF_dPhi_9450.csv   (provides tetrahedra and J := dF)
  - W33_orbits_squarezero_bundle.zip
      * generator_permutations.json         (10 Aut(W33) point generators on 40 vertices)
  - W33_nonisotropic_line_association_scheme_bundle.zip
      * nonisotropic_lines_90.csv           (line_id -> 4-point set)
      * scheme_matrices.npz                 (Ameet, S)  [only used to build mode projectors]

Two induced 90-line observables (both Z3-valued):
  - m_line (boundary moment):
      For each tetrahedron and each *flat* face (a,b,c) that lies on a nonisotropic line L,
      add J(tet) to m[L]. (Equivalently: sum J over tetrahedra incident to each line-face.)

  - z_line (bulk shadow):
      For each tetrahedron and each *curved* face (a,b,c), add J(tet) along its 3 edges.
      Each quotient edge (u,v) lies on a unique nonisotropic line L(u,v); add J to z[L(u,v)].

Mode energies:
  - Embed Z3 as {-1,0,1} via 2 -> -1.
  - Remove the real mean (kills the (+,32) constant mode).
  - Project into the 5 joint modes of (S, Ameet) and report energy fractions.
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import zipfile
from collections import Counter, deque
from itertools import combinations
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
MOD3 = 3


def mod3(x: int) -> int:
    return x % MOD3


def z3_to_real(v: np.ndarray) -> np.ndarray:
    """
    Embed Z3 -> R as {0,1,2} -> {0,1,-1}.
    """
    v = (v.astype(np.int16) % MOD3).copy()
    out = v.astype(np.float64)
    out[out == 2] = -1.0
    return out


def mean_remove(x: np.ndarray) -> np.ndarray:
    return x - float(np.mean(x)) * np.ones_like(x)


def _read_csv_from_zip(zip_path: Path, inner: str) -> list[dict[str, str]]:
    with zipfile.ZipFile(zip_path) as zf:
        with zf.open(inner) as raw:
            text = io.TextIOWrapper(raw, encoding="utf-8")
            return list(csv.DictReader(text))


def _read_json_from_zip(zip_path: Path, inner: str) -> object:
    with zipfile.ZipFile(zip_path) as zf:
        return json.loads(zf.read(inner).decode("utf-8"))


def _write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow(r)


def _write_json(path: Path, data: object) -> None:
    path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")


def _cluster_eigs_to_int(evals: np.ndarray, tol: float = 1e-6) -> dict[int, np.ndarray]:
    rounded = np.rint(evals).astype(int)
    if np.max(np.abs(evals - rounded)) > tol:
        bad = float(np.max(np.abs(evals - rounded)))
        raise ValueError(f"Eigenvalues not near integers (max deviation {bad})")
    out: dict[int, list[int]] = {}
    for i, w in enumerate(rounded):
        out.setdefault(int(w), []).append(i)
    return {k: np.array(v, dtype=int) for k, v in out.items()}


def _compute_mode_projectors(Ameet: np.ndarray, S: np.ndarray) -> dict[str, np.ndarray]:
    """
    Return orthogonal projectors for the 5 joint modes of (S, Ameet),
    labeled as '(+,32)', '(+,2)', '(+,-4)', '(-,8)', '(-,-4)'.
    """
    A = Ameet.astype(np.float64)
    S = S.astype(np.float64)
    wA, vA = np.linalg.eigh(A)
    groups_A = _cluster_eigs_to_int(wA)

    # Split each A-eigenspace by S.
    blocks: dict[tuple[int, int], np.ndarray] = {}
    for lamA, idxs in groups_A.items():
        V = vA[:, idxs]
        S_res = V.T @ (S @ V)
        wS, uS = np.linalg.eigh(S_res)
        groups_S = _cluster_eigs_to_int(wS)
        for epsS, jdxs in groups_S.items():
            if epsS not in (-1, 1):
                raise ValueError(f"Unexpected S eigenvalue {epsS}")
            Vc = V @ uS[:, jdxs]
            E = Vc @ Vc.T
            blocks[(lamA, epsS)] = E

    # Canonical mode labels
    want = {
        "(+,32)": (32, 1),
        "(+,2)": (2, 1),
        "(+,-4)": (-4, 1),
        "(-,8)": (8, -1),
        "(-,-4)": (-4, -1),
    }
    out: dict[str, np.ndarray] = {}
    for name, key in want.items():
        if key not in blocks:
            raise ValueError(f"Missing mode projector {name} for key {key}")
        out[name] = blocks[key]

    return out


def _mode_energy_fractions(projectors: dict[str, np.ndarray], v_centered: np.ndarray) -> tuple[dict[str, float], float]:
    energies: dict[str, float] = {}
    total = 0.0
    for name, E in projectors.items():
        comp = E @ v_centered
        e = float(np.dot(comp, comp))
        energies[name] = e
        total += e
    if total == 0.0:
        fracs = {name: 0.0 for name in energies}
    else:
        fracs = {name: energies[name] / total for name in energies}
    return fracs, total


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--holonomy-phase-decomp",
        type=Path,
        default=ROOT / "W33_holonomy_phase_decomposition_bundle.zip",
    )
    ap.add_argument(
        "--orbits-bundle",
        type=Path,
        default=ROOT / "W33_orbits_squarezero_bundle.zip",
    )
    ap.add_argument(
        "--line-scheme-bundle",
        type=Path,
        default=ROOT / "W33_nonisotropic_line_association_scheme_bundle.zip",
    )
    ap.add_argument(
        "--out",
        type=Path,
        default=ROOT / "W33_mode_response_table_bulk_to_vacuum_bundle.zip",
    )
    args = ap.parse_args()

    # --- Load tetrahedra and J := dF
    trows = _read_csv_from_zip(args.holonomy_phase_decomp, "tetra_coboundary_dF_dPhi_9450.csv")
    tets = [tuple(map(int, [r["a"], r["b"], r["c"], r["d"]])) for r in trows]
    J = np.array([mod3(int(r["dF"])) for r in trows], dtype=np.int16)
    if len(tets) != 9450:
        raise SystemExit(f"Expected 9450 tetrahedra, got {len(tets)}")
    tet_index = {tet: i for i, tet in enumerate(tets)}

    # --- Load nonisotropic lines; build (triple->line) and (edge->line) maps
    lrows = _read_csv_from_zip(args.line_scheme_bundle, "nonisotropic_lines_90.csv")
    line_points: list[str] = [""] * 90
    triple_to_line: dict[tuple[int, int, int], int] = {}
    edge_to_line: dict[tuple[int, int], int] = {}
    for r in lrows:
        lid = int(r["line_id"])
        pts = tuple(sorted(int(x) for x in r["points"].split()))
        line_points[lid] = " ".join(str(x) for x in pts)
        for tri in combinations(pts, 3):
            triple_to_line[tri] = lid
        for e in combinations(pts, 2):
            ee = tuple(sorted(e))
            prev = edge_to_line.get(ee)
            if prev is not None and prev != lid:
                raise SystemExit(f"Edge {ee} lies on two lines? {prev} and {lid}")
            edge_to_line[ee] = lid
    if len(triple_to_line) != 360:
        raise SystemExit(f"Expected 360 flat triples, got {len(triple_to_line)}")
    if len(edge_to_line) != 540:
        raise SystemExit(f"Expected 540 quotient edges, got {len(edge_to_line)}")

    # --- Load Aut(W33) generators on 40 points
    gen_obj = _read_json_from_zip(args.orbits_bundle, "generator_permutations.json")
    gens: list[list[int]] = gen_obj["point_perms"]
    if len(gens) != 10 or any(len(g) != 40 for g in gens):
        raise SystemExit("Expected 10 generators as 40-point permutations")

    # --- Precompute tetra permutation for each generator
    tet_perm: list[np.ndarray] = []
    for g in gens:
        mp = np.empty(len(tets), dtype=np.int32)
        for i, tet in enumerate(tets):
            img = tuple(sorted(g[v] for v in tet))
            mp[i] = tet_index[img]
        tet_perm.append(mp)

    # --- Orbit decomposition on tetrahedra
    n = len(tets)
    orbit_id_raw = np.full(n, -1, dtype=np.int32)
    orbits: list[list[int]] = []
    for i in range(n):
        if orbit_id_raw[i] != -1:
            continue
        oid = len(orbits)
        q = deque([i])
        orbit_id_raw[i] = oid
        members: list[int] = []
        while q:
            u = q.popleft()
            members.append(u)
            for mp in tet_perm:
                v = int(mp[u])
                if orbit_id_raw[v] == -1:
                    orbit_id_raw[v] = oid
                    q.append(v)
        orbits.append(members)

    # Canonicalize orbit ids by descending size (bulk=0, boundary=1, vacuum=2)
    order_old = sorted(range(len(orbits)), key=lambda o: len(orbits[o]), reverse=True)
    remap = {old: new for new, old in enumerate(order_old)}
    orbit_id = np.array([remap[int(x)] for x in orbit_id_raw], dtype=np.int32)
    orbits_canon = [orbits[old] for old in order_old]

    orbit_name = {0: "bulk_flat0", 1: "boundary_flat1", 2: "vacuum_line4"}

    # --- Precompute flat face count per tetra (for metadata)
    def faces_of_tet(a: int, b: int, c: int, d: int) -> list[tuple[int, int, int]]:
        return [(b, c, d), (a, c, d), (a, b, d), (a, b, c)]

    flat_face_count = np.zeros(n, dtype=np.int16)
    for i, (a, b, c, d) in enumerate(tets):
        cnt = 0
        for tri in faces_of_tet(a, b, c, d):
            if tri in triple_to_line:
                cnt += 1
        flat_face_count[i] = cnt

    # --- Compute class contributions (orbit_id, J_value) -> (m_vec, z_vec)
    classes = [(oid, jv) for oid in range(len(orbits_canon)) for jv in (1, 2)]
    m_class = {(oid, jv): np.zeros(90, dtype=np.int16) for (oid, jv) in classes}
    z_class = {(oid, jv): np.zeros(90, dtype=np.int16) for (oid, jv) in classes}
    class_counts = Counter()

    for i, (a, b, c, d) in enumerate(tets):
        jv = int(J[i])
        if jv not in (1, 2):
            continue
        oid = int(orbit_id[i])
        key = (oid, jv)
        class_counts[key] += 1

        faces = faces_of_tet(a, b, c, d)
        # m: add J on flat faces -> their line_id
        for tri in faces:
            lid = triple_to_line.get(tri)
            if lid is not None:
                m_class[key][lid] = mod3(int(m_class[key][lid]) + jv)

        # z: for curved faces, add J along their edges -> edge line_id
        for tri in faces:
            if tri in triple_to_line:
                continue
            x, y, z = tri
            for e in ((x, y), (x, z), (y, z)):
                ee = tuple(sorted(e))
                lid = edge_to_line.get(ee)
                if lid is None:
                    raise SystemExit(f"Edge {ee} missing from edge_to_line map")
                z_class[key][lid] = mod3(int(z_class[key][lid]) + jv)

    # --- Mode projectors from the scheme matrices
    raw_npz = _read_bytes = None
    with zipfile.ZipFile(args.line_scheme_bundle) as zf:
        raw_npz = zf.read("scheme_matrices.npz")
    scheme = np.load(io.BytesIO(raw_npz))
    Ameet = scheme["Ameet"].astype(np.int16)
    S = scheme["S"].astype(np.int16)
    projectors = _compute_mode_projectors(Ameet=Ameet, S=S)
    mode_order = ["(+,32)", "(+,2)", "(+,-4)", "(-,8)", "(-,-4)"]

    # --- Build outputs
    out_dir = ROOT / "_out_mode_response_table"
    if out_dir.exists():
        for p in out_dir.iterdir():
            p.unlink()
        out_dir.rmdir()
    out_dir.mkdir()

    # orbit_metadata.json
    orbit_meta = []
    for oid, members in enumerate(orbits_canon):
        jc = Counter(int(J[i]) for i in members)
        fc = Counter(int(flat_face_count[i]) for i in members)
        example = list(min((tets[i] for i in members)))
        orbit_meta.append(
            {
                "orbit_id": oid,
                "size": len(members),
                "J_counts": {str(k): int(v) for k, v in sorted(jc.items())},
                "flat_face_counts": {str(k): int(v) for k, v in sorted(fc.items())},
                "example": example,
            }
        )
    _write_json(out_dir / "orbit_metadata.json", orbit_meta)

    # line_contributions_long.csv
    line_rows = []
    for (oid, jv) in classes:
        mv = m_class[(oid, jv)]
        zv = z_class[(oid, jv)]
        for lid in range(90):
            mc = int(mv[lid]) % MOD3
            zc = int(zv[lid]) % MOD3
            if mc == 0 and zc == 0:
                continue
            line_rows.append(
                {
                    "line_id": lid,
                    "points": line_points[lid],
                    "orbit_id": oid,
                    "orbit_name": orbit_name[oid],
                    "J_value": jv,
                    "m_contrib": mc,
                    "z_contrib": zc,
                }
            )
    _write_csv(
        out_dir / "line_contributions_long.csv",
        ["line_id", "points", "orbit_id", "orbit_name", "J_value", "m_contrib", "z_contrib"],
        line_rows,
    )

    # class_counts_summary.csv + mode_response_by_orbit_and_flux.csv
    class_count_rows = []
    class_mode_rows = []
    for oid in range(len(orbits_canon)):
        for jv in (1, 2):
            key = (oid, jv)
            mv = m_class[key].astype(np.int16) % MOD3
            zv = z_class[key].astype(np.int16) % MOD3
            class_count_rows.append(
                {
                    "orbit_id": oid,
                    "orbit_name": orbit_name[oid],
                    "J_value": jv,
                    "num_tets": int(class_counts.get(key, 0)),
                    "m_sum_mod3": int(np.sum(mv) % MOD3),
                    "z_sum_mod3": int(np.sum(zv) % MOD3),
                    "m_nonzero_lines": int(np.count_nonzero(mv)),
                    "z_nonzero_lines": int(np.count_nonzero(zv)),
                }
            )

            # Energies / fractions in the 5 modes
            m_center = mean_remove(z3_to_real(mv))
            z_center = mean_remove(z3_to_real(zv))
            m_fracs, m_energy = _mode_energy_fractions(projectors, m_center)
            z_fracs, z_energy = _mode_energy_fractions(projectors, z_center)

            row = {
                "orbit_id": oid,
                "orbit_name": orbit_name[oid],
                "orbit_size": len(orbits_canon[oid]),
                "J_value": jv,
                "num_tetra_with_this_J": int(class_counts.get(key, 0)),
                "m_nonzero_lines": int(np.count_nonzero(mv)),
                "z_nonzero_lines": int(np.count_nonzero(zv)),
                "m_total_energy": m_energy,
                "z_total_energy": z_energy,
            }
            for mode in mode_order:
                row[f"m_frac_{mode}"] = m_fracs[mode]
            for mode in mode_order:
                row[f"z_frac_{mode}"] = z_fracs[mode]
            class_mode_rows.append(row)

    _write_csv(
        out_dir / "class_counts_summary.csv",
        ["orbit_id", "orbit_name", "J_value", "num_tets", "m_sum_mod3", "z_sum_mod3", "m_nonzero_lines", "z_nonzero_lines"],
        class_count_rows,
    )

    _write_csv(
        out_dir / "mode_response_by_orbit_and_flux.csv",
        [
            "orbit_id",
            "orbit_name",
            "orbit_size",
            "J_value",
            "num_tetra_with_this_J",
            "m_nonzero_lines",
            "z_nonzero_lines",
            "m_total_energy",
            "z_total_energy",
            *(f"m_frac_{m}" for m in mode_order),
            *(f"z_frac_{m}" for m in mode_order),
        ],
        class_mode_rows,
    )

    # mode_response_aggregate_by_orbit.csv
    agg_rows = []
    for oid in range(len(orbits_canon)):
        mv = (m_class[(oid, 1)] + m_class[(oid, 2)]) % MOD3
        zv = (z_class[(oid, 1)] + z_class[(oid, 2)]) % MOD3
        m_center = mean_remove(z3_to_real(mv))
        z_center = mean_remove(z3_to_real(zv))
        m_fracs, m_energy = _mode_energy_fractions(projectors, m_center)
        z_fracs, z_energy = _mode_energy_fractions(projectors, z_center)
        row = {
            "orbit_id": oid,
            "orbit_name": orbit_name[oid],
            "orbit_size": len(orbits_canon[oid]),
            "m_sum_mod3": int(np.sum(mv) % MOD3),
            "z_sum_mod3": int(np.sum(zv) % MOD3),
            "m_nonzero_lines": int(np.count_nonzero(mv)),
            "z_nonzero_lines": int(np.count_nonzero(zv)),
            "m_total_energy": m_energy,
            "z_total_energy": z_energy,
        }
        for mode in mode_order:
            row[f"m_frac_{mode}"] = m_fracs[mode]
        for mode in mode_order:
            row[f"z_frac_{mode}"] = z_fracs[mode]
        agg_rows.append(row)

    _write_csv(
        out_dir / "mode_response_aggregate_by_orbit.csv",
        [
            "orbit_id",
            "orbit_name",
            "orbit_size",
            "m_sum_mod3",
            "z_sum_mod3",
            "m_nonzero_lines",
            "z_nonzero_lines",
            "m_total_energy",
            "z_total_energy",
            *(f"m_frac_{m}" for m in mode_order),
            *(f"z_frac_{m}" for m in mode_order),
        ],
        agg_rows,
    )

    # notes.txt
    notes = """\
Mode-response table construction

We decompose the tetrahedra (K4 cliques) of the quotient Q into Aut(W33)-orbits:
  - orbit 0 (bulk_flat0):     flat_face_count = 0
  - orbit 1 (boundary_flat1): flat_face_count = 1
  - orbit 2 (vacuum_line4):   flat_face_count = 4  (the 90 nonisotropic lines themselves; J=0)

We compute J := dF on each tetrahedron and split by J in {1,2}.

Two induced 90-line observables (both Z3-valued):
  - m_line (boundary moment):
      add J(tet) to the unique nonisotropic line_id of any flat face of tet.

  - z_line (bulk shadow):
      for each curved face triangle of tet, add J(tet) along its 3 edges;
      each quotient edge (u,v) lies on a unique nonisotropic line L(u,v).

Mode energies:
  - embed Z3 as {-1,0,1} via 2 -> -1
  - remove the real mean (kills the (+,32) mode)
  - report energy fractions in the 5 joint (S, Ameet) modes
"""
    (out_dir / "notes.txt").write_text(notes, encoding="utf-8")

    # Zip it up
    out_zip: Path = args.out
    if out_zip.exists():
        out_zip.unlink()
    with zipfile.ZipFile(out_zip, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for p in sorted(out_dir.iterdir()):
            zf.write(p, arcname=p.name)

    # cleanup
    for p in out_dir.iterdir():
        p.unlink()
    out_dir.rmdir()

    print(f"Wrote {out_zip}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

