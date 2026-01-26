#!/usr/bin/env python3
"""
Build an explicit artifact bundle for the "holonomy vs. symplectic phase" result on Q.

Inputs (expected in repo root):
  - W33_holonomy_phase_test_bundle.zip
  - W33_quotient_closure_complement_and_noniso_line_curvature_bundle.zip
  - W33_H3_basis_89_Z3_on_clique_complex_bundle.zip
  - (optional) W33_minimal_Z3_flux_cycles_tetrahedra_bundle.zip (for cross-check)

Outputs:
  - W33_holonomy_phase_decomposition_bundle.zip

What this produces:
  - Edge 1-cochain a(p,q)=<v_p,v_q> on Q edges, and verification that δa = Φ.
  - Full tetrahedron coboundary J=dF table (9450 tetrahedra) and histograms.
  - A cohomology note: J=dF is always a 3-coboundary (hence 0 in H^3), so its 90-line
    weight coordinates (which parametrize H^3) are the zero vector.
"""

from __future__ import annotations

import csv
import io
import json
import zipfile
from collections import Counter
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def mod3(x: int) -> int:
    return x % 3


def _read_csv_from_zip(zip_path: Path, inner_path: str) -> list[dict[str, str]]:
    with zipfile.ZipFile(zip_path) as zf:
        with zf.open(inner_path) as raw:
            text = io.TextIOWrapper(raw, encoding="utf-8")
            return list(csv.DictReader(text))


def _read_json_from_zip(zip_path: Path, inner_path: str) -> object:
    with zipfile.ZipFile(zip_path) as zf:
        with zf.open(inner_path) as raw:
            return json.load(raw)


def _write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow(r)


def _write_json(path: Path, data: object) -> None:
    path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")


def _symp_pair(J: list[list[int]], v: list[int], w: list[int]) -> int:
    # v^T J w mod 3
    total = 0
    for i in range(4):
        for j in range(4):
            total += v[i] * J[i][j] * w[j]
    return mod3(total)


@dataclass(frozen=True)
class Inputs:
    test_bundle: Path = ROOT / "W33_holonomy_phase_test_bundle.zip"
    quotient_bundle: Path = ROOT / "W33_quotient_closure_complement_and_noniso_line_curvature_bundle.zip"
    h3_basis_bundle: Path = ROOT / "W33_H3_basis_89_Z3_on_clique_complex_bundle.zip"
    minimal_flux_bundle: Path = ROOT / "W33_minimal_Z3_flux_cycles_tetrahedra_bundle.zip"


def main() -> int:
    inp = Inputs()
    for p in [inp.test_bundle, inp.quotient_bundle, inp.h3_basis_bundle]:
        if not p.exists():
            raise FileNotFoundError(str(p))

    out_dir = ROOT / "_holonomy_phase_decomposition_tmp"
    out_dir.mkdir(exist_ok=True)

    # --- Load triangle-level data (F, Phi, D)
    tri_rows = _read_csv_from_zip(inp.test_bundle, "triangle_holonomy_vs_symplectic_phase.csv")
    if len(tri_rows) != 3240:
        raise ValueError(f"Expected 3240 triangles, got {len(tri_rows)}")

    F: dict[tuple[int, int, int], int] = {}
    Phi_given: dict[tuple[int, int, int], int] = {}
    D_given: dict[tuple[int, int, int], int] = {}
    for r in tri_rows:
        p, q, s = int(r["p"]), int(r["q"]), int(r["r"])
        key = (p, q, s)
        F[key] = mod3(int(r["F"]))
        Phi_given[key] = mod3(int(r["Phi"]))
        D_given[key] = mod3(int(r["D"]))

    # --- Symplectic reps and J form
    J = _read_json_from_zip(inp.test_bundle, "symplectic_form_J.json")
    assert isinstance(J, list)
    reps_rows = _read_csv_from_zip(inp.test_bundle, "projective_representatives_40.csv")
    reps: dict[int, list[int]] = {}
    for r in reps_rows:
        pid = int(r["point_id"])
        vec = [int(x) for x in r["vector_digits"].split()]
        if len(vec) != 4:
            raise ValueError(f"Bad vector_digits for point {pid}: {r['vector_digits']!r}")
        reps[pid] = [mod3(x) for x in vec]
    if len(reps) != 40:
        raise ValueError(f"Expected 40 representatives, got {len(reps)}")

    # Recompute Phi from symplectic form and reps, and check it matches the bundle CSV.
    Phi: dict[tuple[int, int, int], int] = {}
    phi_mismatches: list[dict[str, object]] = []
    for (p, q, r) in F:
        vp, vq, vr = reps[p], reps[q], reps[r]
        val = mod3(_symp_pair(J, vp, vq) + _symp_pair(J, vq, vr) + _symp_pair(J, vr, vp))
        Phi[(p, q, r)] = val
        if val != Phi_given[(p, q, r)]:
            phi_mismatches.append({"p": p, "q": q, "r": r, "phi_recomputed": val, "phi_csv": Phi_given[(p, q, r)]})
    if phi_mismatches:
        raise ValueError(f"Phi recomputation mismatches CSV on {len(phi_mismatches)} triangles")

    # Verify D = F - Phi mod 3 matches.
    d_mismatches: list[dict[str, object]] = []
    for key, fval in F.items():
        expected = mod3(fval - Phi[key])
        if expected != D_given[key]:
            p, q, r = key
            d_mismatches.append({"p": p, "q": q, "r": r, "D_expected": expected, "D_csv": D_given[key]})
    if d_mismatches:
        raise ValueError(f"D mismatch on {len(d_mismatches)} triangles")

    # --- Build edge 1-cochain a(p,q)=<v_p,v_q> on Q edges and verify δa = Phi
    edge_rows = _read_csv_from_zip(inp.quotient_bundle, "quotient_graph_edges_540.csv")
    if len(edge_rows) != 540:
        raise ValueError(f"Expected 540 quotient edges, got {len(edge_rows)}")
    a_edge: dict[tuple[int, int], int] = {}
    edge_out_rows: list[dict[str, object]] = []
    for r in edge_rows:
        p, q = int(r["p"]), int(r["q"])
        if p == q:
            raise ValueError("self-loop in quotient edge list")
        if p > q:
            p, q = q, p
        val = _symp_pair(J, reps[p], reps[q])
        a_edge[(p, q)] = val
        edge_out_rows.append({"p": p, "q": q, "a_symp": val})

    # δa(p,q,r) = a(q,r) - a(p,r) + a(p,q)
    da_mismatches: list[dict[str, object]] = []
    for (p, q, r) in Phi:
        def a(u: int, v: int) -> int:
            if u == v:
                return 0
            if u < v:
                return a_edge[(u, v)]
            return mod3(-a_edge[(v, u)])

        val = mod3(a(q, r) - a(p, r) + a(p, q))
        if val != Phi[(p, q, r)]:
            da_mismatches.append({"p": p, "q": q, "r": r, "delta_a": val, "Phi": Phi[(p, q, r)]})
    if da_mismatches:
        raise ValueError(f"δa != Phi on {len(da_mismatches)} triangles")

    # --- Compute tetrahedra coboundaries dF and dPhi using the canonical tetra index map
    tet_rows = _read_csv_from_zip(inp.h3_basis_bundle, "tetra_index_map_9450.csv")
    if len(tet_rows) != 9450:
        raise ValueError(f"Expected 9450 tetrahedra, got {len(tet_rows)}")

    def tri_val(co: dict[tuple[int, int, int], int], u: int, v: int, w: int) -> int:
        key = tuple(sorted((u, v, w)))
        return co[key]

    tetra_out: list[dict[str, object]] = []
    dF_counts: Counter[int] = Counter()
    dPhi_counts: Counter[int] = Counter()
    for row in tet_rows:
        idx = int(row["tet_index"])
        a, b, c, d = int(row["a"]), int(row["b"]), int(row["c"]), int(row["d"])
        # a<b<c<d by construction
        dF = mod3(tri_val(F, b, c, d) - tri_val(F, a, c, d) + tri_val(F, a, b, d) - tri_val(F, a, b, c))
        dPhi = mod3(tri_val(Phi, b, c, d) - tri_val(Phi, a, c, d) + tri_val(Phi, a, b, d) - tri_val(Phi, a, b, c))
        dF_counts[dF] += 1
        dPhi_counts[dPhi] += 1
        tetra_out.append(
            {
                "tet_index": idx,
                "a": a,
                "b": b,
                "c": c,
                "d": d,
                "dF": dF,
                "dPhi": dPhi,
                "d(F-Phi)": mod3(dF - dPhi),
            }
        )

    # Optional: cross-check against the minimal-flux bundle's nonzero tetra list.
    flux_crosscheck = {"performed": False}
    if inp.minimal_flux_bundle.exists():
        nonzero_rows = _read_csv_from_zip(inp.minimal_flux_bundle, "tetrahedra_flux_nonzero_3008.csv")
        seen = {(int(r["a"]), int(r["b"]), int(r["c"]), int(r["d"])): int(r["flux_dF"]) % 3 for r in nonzero_rows}
        mism = 0
        for row in tetra_out:
            key4 = (row["a"], row["b"], row["c"], row["d"])
            dF = int(row["dF"])
            if dF != 0:
                if key4 not in seen or seen[key4] != dF:
                    mism += 1
            else:
                if key4 in seen:
                    mism += 1
        flux_crosscheck = {"performed": True, "nonzero_expected": len(seen), "mismatches": mism}

    # --- Cohomology note
    # J := dF is, by definition, δ2(F). Therefore J is a 3-coboundary and represents 0 in H^3.
    # Any map that factors through H^3 (such as the 90-line weight map) sends J to 0.
    h3_coords = [0] * 89

    report = {
        "inputs": {
            "test_bundle": inp.test_bundle.name,
            "quotient_bundle": inp.quotient_bundle.name,
            "h3_basis_bundle": inp.h3_basis_bundle.name,
            "minimal_flux_bundle_present": inp.minimal_flux_bundle.exists(),
        },
        "triangle_counts": {
            "num_triangles": 3240,
            "F_hist": {str(k): v for k, v in sorted(Counter(F.values()).items())},
            "Phi_hist": {str(k): v for k, v in sorted(Counter(Phi.values()).items())},
            "D_hist": {str(k): v for k, v in sorted(Counter(D_given.values()).items())},
        },
        "tetra_counts": {
            "num_tetrahedra": 9450,
            "dF_hist": {str(k): v for k, v in sorted(dF_counts.items())},
            "dPhi_hist": {str(k): v for k, v in sorted(dPhi_counts.items())},
            "flux_crosscheck": flux_crosscheck,
        },
        "structural_results": {
            "Phi_is_exact": True,
            "Phi_potential_edge_1cochain": "a(p,q)=<v_p,v_q> (symplectic pairing)",
            "delta_a_equals_Phi": True,
            "Phi_is_closed": dPhi_counts.get(0, 0) == 9450 and len(dPhi_counts) == 1,
            "F_is_sourced": any(k != 0 for k in dF_counts.keys()),
            "J_equals_dF_is_coboundary": True,
            "H3_class_of_J": "0 (exact)",
            "H3_coordinates_of_J_in_basis_89": h3_coords,
            "line_weight_coordinates_of_J": "0 (because map factors through H^3)",
        },
    }

    # Write files
    _write_csv(out_dir / "edge_symplectic_pairing_on_Q_edges_540.csv", ["p", "q", "a_symp"], edge_out_rows)
    _write_csv(
        out_dir / "tetra_coboundary_dF_dPhi_9450.csv",
        ["tet_index", "a", "b", "c", "d", "dF", "dPhi", "d(F-Phi)"],
        tetra_out,
    )
    _write_json(out_dir / "holonomy_phase_decomposition_report.json", report)
    _write_json(out_dir / "H3_coordinates_of_dF.json", {"basis": "H3_basis_89", "coords": h3_coords})

    readme = """\
Holonomy / symplectic-phase decomposition artifacts

This bundle records the “holonomy vs. symplectic phase” computation on the 40-vertex quotient Q.

Key identities (all mod 3):
  - a(p,q) := <v_p, v_q> is a Z3 1-cochain on edges
  - Phi(p,q,r) = a(q,r) - a(p,r) + a(p,q) = δa is therefore exact (hence closed)
  - J := dF is, by definition, δ2(F), hence a 3-coboundary and cohomologically trivial in H^3

Files:
  - edge_symplectic_pairing_on_Q_edges_540.csv
  - tetra_coboundary_dF_dPhi_9450.csv
  - holonomy_phase_decomposition_report.json
  - H3_coordinates_of_dF.json
"""
    (out_dir / "README.txt").write_text(readme, encoding="utf-8")

    out_zip = ROOT / "W33_holonomy_phase_decomposition_bundle.zip"
    if out_zip.exists():
        out_zip.unlink()
    with zipfile.ZipFile(out_zip, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for p in sorted(out_dir.iterdir()):
            zf.write(p, arcname=p.name)

    # cleanup temp dir contents (leave dir for debugging? no, remove files)
    for p in out_dir.iterdir():
        p.unlink()
    out_dir.rmdir()

    print(f"Wrote {out_zip}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

