#!/usr/bin/env python3
"""
Build explicit sparse transfer operators from tetra flux J:=dF to 90-line observables.

This produces the field-equation-layer artifact bundle referenced by the complete draft:
  - W33_transfer_operators_J_to_lines_and_mode_injection_bundle.zip

Operators over Z3:
  - M : Z3^{9450} -> Z3^{90}   (boundary moment / line-face attachment)
  - Z : Z3^{9450} -> Z3^{90}   (bulk shadow via curved-triangle edges -> nonisotropic lines)

Conventions:
  - tetrahedra are indexed by tet_index from tetra_coboundary_dF_dPhi_9450.csv
  - line_id is the 0..89 indexing from nonisotropic_lines_90.csv
  - flat faces are exactly the triangle 3-subsets of nonisotropic lines (360 total)

Outputs include:
  - operator_M_coo.csv, operator_Z_coo.csv
  - tetrahedra_J_dF_9450.csv (a,b,c,d,J,flat_face_count,attached_line_id_if_boundary)
  - line_vectors_from_MZJ_mod3.csv  (m_raw, m_aug, z)
  - mode_injection_by_orbit_and_flux.csv and mode_injection_aggregate_by_orbit.csv
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
    A = Ameet.astype(np.float64)
    S = S.astype(np.float64)
    wA, vA = np.linalg.eigh(A)
    groups_A = _cluster_eigs_to_int(wA)

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
        "--vacuum-mode-bundle",
        type=Path,
        default=ROOT / "W33_vacuum_line_scheme_mode_decomposition_bundle.zip",
        help="Optional: used only for cross-checking computed (m,z) vectors.",
    )
    ap.add_argument(
        "--out",
        type=Path,
        default=ROOT / "W33_transfer_operators_J_to_lines_and_mode_injection_bundle.zip",
    )
    args = ap.parse_args()

    # --- Load tetrahedra and J := dF
    trows = _read_csv_from_zip(args.holonomy_phase_decomp, "tetra_coboundary_dF_dPhi_9450.csv")
    tets = [tuple(map(int, [r["a"], r["b"], r["c"], r["d"]])) for r in trows]
    J = np.array([mod3(int(r["dF"])) for r in trows], dtype=np.int16)
    if len(tets) != 9450:
        raise SystemExit(f"Expected 9450 tetrahedra, got {len(tets)}")

    # --- Load nonisotropic lines; build maps
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

    # --- Determine attached line for boundary tets and build operator COO
    def faces_of_tet(a: int, b: int, c: int, d: int) -> list[tuple[int, int, int]]:
        return [(b, c, d), (a, c, d), (a, b, d), (a, b, c)]

    m_rows: list[dict[str, int]] = []
    z_rows: list[dict[str, int]] = []
    tet_rows: list[dict[str, int]] = []

    m_raw = np.zeros(90, dtype=np.int16)
    z_vec = np.zeros(90, dtype=np.int16)
    z_cols: list[list[tuple[int, int]]] = [[] for _ in range(len(tets))]

    flat_face_count = np.zeros(len(tets), dtype=np.int16)
    attached_line = np.full(len(tets), -1, dtype=np.int32)

    for ti, (a, b, c, d) in enumerate(tets):
        faces = faces_of_tet(a, b, c, d)
        flat = [triple_to_line.get(tri) for tri in faces if tri in triple_to_line]
        flat_count = len(flat)
        flat_face_count[ti] = flat_count

        if flat_count == 1:
            attached_line[ti] = int(flat[0])
            m_rows.append({"row_line_id": int(flat[0]), "col_tet_index": ti, "value_mod3": 1})
            jv = int(J[ti])
            if jv:
                m_raw[int(flat[0])] = mod3(int(m_raw[int(flat[0])]) + jv)
        elif flat_count not in (0, 4):
            raise SystemExit(f"Unexpected flat_face_count={flat_count} for tet_index={ti}")

        # Z operator column aggregation for this tet
        local: dict[int, int] = {}
        for tri in faces:
            if tri in triple_to_line:
                continue
            x, y, z = tri
            for e in ((x, y), (x, z), (y, z)):
                ee = tuple(sorted(e))
                lid = edge_to_line.get(ee)
                if lid is None:
                    raise SystemExit(f"Edge {ee} missing from edge_to_line")
                local[lid] = mod3(local.get(lid, 0) + 1)

        for lid, coeff in sorted(local.items()):
            if coeff == 0:
                continue
            z_rows.append({"row_line_id": int(lid), "col_tet_index": ti, "value_mod3": int(coeff)})
            z_cols[ti].append((int(lid), int(coeff)))
            jv = int(J[ti])
            if jv:
                z_vec[int(lid)] = mod3(int(z_vec[int(lid)]) + coeff * jv)

        tet_rows.append(
            {
                "tet_index": ti,
                "a": a,
                "b": b,
                "c": c,
                "d": d,
                "J_dF_mod3": int(J[ti]),
                "flat_face_count": int(flat_count),
                "attached_line_id_if_boundary": int(attached_line[ti]),
            }
        )

    # augmentation projection for m
    m_sum = int(np.sum(m_raw) % MOD3)
    m_aug = m_raw.copy()
    if m_sum:
        m_aug[0] = mod3(int(m_aug[0]) - m_sum)
    if int(np.sum(m_aug) % MOD3) != 0:
        raise SystemExit("Failed to project m to augmentation (sum=0)")

    if int(np.sum(z_vec) % MOD3) != 0:
        raise SystemExit("z_vec expected to be in augmentation (sum=0)")

    # --- Orbit decomposition on tetrahedra (geometric, independent of J)
    gen_obj = _read_json_from_zip(args.orbits_bundle, "generator_permutations.json")
    gens: list[list[int]] = gen_obj["point_perms"]
    if len(gens) != 10:
        raise SystemExit("Expected 10 Aut(W33) generators")

    tet_index = {tet: i for i, tet in enumerate(tets)}
    tet_perm: list[np.ndarray] = []
    for g in gens:
        mp = np.empty(len(tets), dtype=np.int32)
        for i, tet in enumerate(tets):
            img = tuple(sorted(g[v] for v in tet))
            mp[i] = tet_index[img]
        tet_perm.append(mp)

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

    order_old = sorted(range(len(orbits)), key=lambda o: len(orbits[o]), reverse=True)
    remap = {old: new for new, old in enumerate(order_old)}
    orbit_id = np.array([remap[int(x)] for x in orbit_id_raw], dtype=np.int32)
    orbit_sizes = {new: len(orbits[old]) for new, old in enumerate(order_old)}
    orbit_name = {0: "bulk_flat0", 1: "boundary_flat1", 2: "vacuum_line4"}

    # --- Mode projectors
    with zipfile.ZipFile(args.line_scheme_bundle) as zf:
        raw_npz = zf.read("scheme_matrices.npz")
    scheme = np.load(io.BytesIO(raw_npz))
    Ameet = scheme["Ameet"].astype(np.int16)
    S = scheme["S"].astype(np.int16)
    projectors = _compute_mode_projectors(Ameet=Ameet, S=S)
    mode_order = ["(+,32)", "(+,2)", "(+,-4)", "(-,8)", "(-,-4)"]

    # --- Build injection tables by orbit and flux value
    inj_rows = []
    agg_rows = []
    m_class: dict[tuple[int, int], np.ndarray] = {(oid, jv): np.zeros(90, dtype=np.int16) for oid in orbit_sizes for jv in (1, 2)}
    z_class: dict[tuple[int, int], np.ndarray] = {(oid, jv): np.zeros(90, dtype=np.int16) for oid in orbit_sizes for jv in (1, 2)}

    for ti in range(n):
        jv = int(J[ti])
        if jv not in (1, 2):
            continue
        oid = int(orbit_id[ti])
        key = (oid, jv)

        lid_att = int(attached_line[ti])
        if lid_att != -1:
            m_class[key][lid_att] = mod3(int(m_class[key][lid_att]) + jv)

        for lid, coeff in z_cols[ti]:
            z_class[key][lid] = mod3(int(z_class[key][lid]) + coeff * jv)

    for oid in sorted(orbit_sizes):
        m_acc = np.zeros(90, dtype=np.int16)
        z_acc = np.zeros(90, dtype=np.int16)
        for jv in (1, 2):
            m_cls = m_class[(oid, jv)]
            z_cls = z_class[(oid, jv)]
            m_acc = (m_acc + m_cls) % MOD3
            z_acc = (z_acc + z_cls) % MOD3

            m_center = mean_remove(z3_to_real(m_cls))
            z_center = mean_remove(z3_to_real(z_cls))
            m_fracs, m_energy = _mode_energy_fractions(projectors, m_center)
            z_fracs, z_energy = _mode_energy_fractions(projectors, z_center)

            row = {
                "orbit_id": oid,
                "orbit_name": orbit_name[oid],
                "orbit_size": orbit_sizes[oid],
                "J_value": jv,
                "num_tetra_with_this_J": int(np.sum((orbit_id == oid) & (J == jv))),
                "m_sum_mod3": int(np.sum(m_cls) % MOD3),
                "z_sum_mod3": int(np.sum(z_cls) % MOD3),
                "m_total_energy": m_energy,
                "z_total_energy": z_energy,
            }
            for mode in mode_order:
                row[f"m_frac_{mode}"] = m_fracs[mode]
            for mode in mode_order:
                row[f"z_frac_{mode}"] = z_fracs[mode]
            inj_rows.append(row)

        m_center = mean_remove(z3_to_real(m_acc))
        z_center = mean_remove(z3_to_real(z_acc))
        m_fracs, m_energy = _mode_energy_fractions(projectors, m_center)
        z_fracs, z_energy = _mode_energy_fractions(projectors, z_center)
        row = {
            "orbit_id": oid,
            "orbit_name": orbit_name[oid],
            "orbit_size": orbit_sizes[oid],
            "m_sum_mod3": int(np.sum(m_acc) % MOD3),
            "z_sum_mod3": int(np.sum(z_acc) % MOD3),
            "m_total_energy": m_energy,
            "z_total_energy": z_energy,
        }
        for mode in mode_order:
            row[f"m_frac_{mode}"] = m_fracs[mode]
        for mode in mode_order:
            row[f"z_frac_{mode}"] = z_fracs[mode]
        agg_rows.append(row)

    # --- Cross-check against vacuum mode decomposition bundle if present
    crosscheck = {"vacuum_mode_bundle_present": args.vacuum_mode_bundle.exists()}
    if args.vacuum_mode_bundle.exists():
        try:
            rows = _read_csv_from_zip(args.vacuum_mode_bundle, "line_vectors_mod3.csv")
            m_ref = np.array([int(r["m_aug_mod3"]) for r in rows], dtype=np.int16) % MOD3
            z_ref = np.array([int(r["z_mod3"]) for r in rows], dtype=np.int16) % MOD3
            crosscheck["matches_m_aug"] = bool(np.array_equal(m_aug, m_ref))
            crosscheck["matches_z"] = bool(np.array_equal(z_vec, z_ref))
            crosscheck["m_aug_mismatches"] = int(np.count_nonzero((m_aug - m_ref) % MOD3))
            crosscheck["z_mismatches"] = int(np.count_nonzero((z_vec - z_ref) % MOD3))
        except Exception as e:
            crosscheck["error"] = f"{type(e).__name__}: {e}"

    # --- Write bundle
    out_dir = ROOT / "_out_transfer_ops"
    if out_dir.exists():
        for p in out_dir.iterdir():
            p.unlink()
        out_dir.rmdir()
    out_dir.mkdir()

    _write_csv(out_dir / "operator_M_coo.csv", ["row_line_id", "col_tet_index", "value_mod3"], m_rows)
    _write_csv(out_dir / "operator_Z_coo.csv", ["row_line_id", "col_tet_index", "value_mod3"], z_rows)
    _write_csv(
        out_dir / "tetrahedra_J_dF_9450.csv",
        ["tet_index", "a", "b", "c", "d", "J_dF_mod3", "flat_face_count", "attached_line_id_if_boundary"],
        tet_rows,
    )

    line_rows = []
    for lid in range(90):
        line_rows.append(
            {
                "line_id": lid,
                "points": line_points[lid],
                "m_raw_mod3": int(m_raw[lid]),
                "m_aug_mod3": int(m_aug[lid]),
                "z_mod3": int(z_vec[lid]),
            }
        )
    _write_csv(
        out_dir / "line_vectors_from_MZJ_mod3.csv",
        ["line_id", "points", "m_raw_mod3", "m_aug_mod3", "z_mod3"],
        line_rows,
    )

    _write_csv(
        out_dir / "mode_injection_by_orbit_and_flux.csv",
        [
            "orbit_id",
            "orbit_name",
            "orbit_size",
            "J_value",
            "num_tetra_with_this_J",
            "m_sum_mod3",
            "z_sum_mod3",
            "m_total_energy",
            "z_total_energy",
            *(f"m_frac_{m}" for m in mode_order),
            *(f"z_frac_{m}" for m in mode_order),
        ],
        inj_rows,
    )
    _write_csv(
        out_dir / "mode_injection_aggregate_by_orbit.csv",
        [
            "orbit_id",
            "orbit_name",
            "orbit_size",
            "m_sum_mod3",
            "z_sum_mod3",
            "m_total_energy",
            "z_total_energy",
            *(f"m_frac_{m}" for m in mode_order),
            *(f"z_frac_{m}" for m in mode_order),
        ],
        agg_rows,
    )

    _write_json(
        out_dir / "report.json",
        {
            "inputs": {
                "holonomy_phase_decomp": args.holonomy_phase_decomp.name,
                "orbits_bundle": args.orbits_bundle.name,
                "line_scheme_bundle": args.line_scheme_bundle.name,
            },
            "counts": {
                "num_tetrahedra": len(tets),
                "J_hist": {str(k): int(v) for k, v in sorted(Counter(J.tolist()).items())},
                "flat_face_count_hist": {str(k): int(v) for k, v in sorted(Counter(flat_face_count.tolist()).items())},
                "orbit_sizes": orbit_sizes,
            },
            "crosscheck": crosscheck,
        },
    )

    readme = """\
Transfer operators from tetra flux J:=dF to 90-line observables

This bundle constructs two explicit Z3-linear maps:
  - M (boundary moment): adds J(t) to the unique attached nonisotropic line for boundary tetrahedra (flat_face_count=1)
  - Z (bulk shadow): for each curved face of a tetrahedron t, pushes J(t) along the 3 edges of that face, mapping each edge to its unique nonisotropic line.

Files:
  - operator_M_coo.csv, operator_Z_coo.csv
      Sparse COO representation (row_line_id, col_tet_index, value_mod3).
  - tetrahedra_J_dF_9450.csv
      Full tetra list with J and boundary attachment metadata.
  - line_vectors_from_MZJ_mod3.csv
      Resulting m_raw, m_aug (sum=0 gauge), and z vectors on the 90 lines.
  - mode_injection_by_orbit_and_flux.csv, mode_injection_aggregate_by_orbit.csv
      Mode-energy fractions (after embedding 2->-1 and mean-removal) by tetra orbit and flux sign.
  - report.json
"""
    (out_dir / "README.txt").write_text(readme, encoding="utf-8")

    out_zip: Path = args.out
    if out_zip.exists():
        out_zip.unlink()
    with zipfile.ZipFile(out_zip, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for p in sorted(out_dir.iterdir()):
            zf.write(p, arcname=p.name)

    for p in out_dir.iterdir():
        p.unlink()
    out_dir.rmdir()

    print(f"Wrote {out_zip}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
