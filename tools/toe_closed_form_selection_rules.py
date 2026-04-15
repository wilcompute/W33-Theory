#!/usr/bin/env python3
"""
TOE closed-form selection rules (SO(10)×U(1) + Z6 clock + W33 line fusion + firewall).

This tool is meant to *compress* the current “stack” into a small number of
machine-checkable rules.

What it proves/records:

  A) Exact SO(10)×U(1)_psi direction in E6 Cartan coordinates:
     - Solve for an integer vector c∈Z^6 such that for the 27 weights w_i (from
       artifacts/toe_sm_decomposition_27.json) we have:
           Qpsi(w_i) = c·w_i  (exactly)
     - This recovers the canonical 27→16_1 + 10_-2 + 1_4 split without any fitting.

  B) Extend Qpsi to *all 240 E8 root-channels* via trinification coordinates:
     - Each E8 root is stored as root_trin = (E6_part in Z^6, A2_part in Z^2)
       where the E6_part is already in the same coroot-eigenvalue basis as the 27 weights.
     - So we can define:
           Qpsi(root) = c · root_trin[:6]
     - This yields the expected charge-spectrum by grade:
         g0_e6:  40×0  + 16×(+3) + 16×(-3)
         g0_a2:  6×0
         g1:     48×(+1) + 30×(-2) + 3×(+4)
         g2:     48×(-1) + 30×(+2) + 3×(-4)

  C) W33 lines are A2 subsystems with a Z6 phase label (Coxeter orbit position).
     - For each of the 40 W33 lines (K4 cliques), the 6 edge-channels have phases {0..5}.
     - The line fusion law says: for each coupled line-pair (i,j), the 12 interacting
       pairs (α·β=-1) split into two output lines; moreover the output line is
       determined solely by d=(phase(α)-phase(β)) mod 6.

  D) Firewall “bad meet-edges” on the Schläfli 27 are exactly the meet-edges for which
     the W33-derived clock k6 is defined (a surprisingly clean characterization).

Outputs:
  - artifacts/toe_closed_form_selection_rules.json
  - artifacts/toe_closed_form_selection_rules.md
"""

from __future__ import annotations

import importlib.util
import json
import sys
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np

ROOT = Path(__file__).resolve().parents[1]

IN_SM = ROOT / "artifacts" / "toe_sm_decomposition_27.json"
IN_E8 = ROOT / "artifacts" / "e8_root_metadata_table.json"
IN_LINES = ROOT / "artifacts" / "w33_line_fusion_law.json"

OUT_JSON = ROOT / "artifacts" / "toe_closed_form_selection_rules.json"
OUT_MD = ROOT / "artifacts" / "toe_closed_form_selection_rules.md"


def _load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Failed to import {name} from {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def _load_json(path: Path) -> Dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, data: Dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _write_md(path: Path, lines: List[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def _cartan_unit_e8_sage_order() -> np.ndarray:
    # Gram matrix in the E8 simple-root coefficient basis used by root_orbit.
    return np.array(
        [
            [2, 0, -1, 0, 0, 0, 0, 0],
            [0, 2, 0, -1, 0, 0, 0, 0],
            [-1, 0, 2, -1, 0, 0, 0, 0],
            [0, -1, -1, 2, -1, 0, 0, 0],
            [0, 0, 0, -1, 2, -1, 0, 0],
            [0, 0, 0, 0, -1, 2, -1, 0],
            [0, 0, 0, 0, 0, -1, 2, -1],
            [0, 0, 0, 0, 0, 0, -1, 2],
        ],
        dtype=int,
    )


def _ip_orbit_coeffs(a: Tuple[int, ...], b: Tuple[int, ...], C: np.ndarray) -> int:
    return int(sum(a[i] * int(C[i, j]) * b[j] for i in range(8) for j in range(8)))


def solve_qpsi_cartan_vector() -> Dict[str, object]:
    """
    Recover an integer vector c in Z^6 such that Qpsi3 = c·w exactly
    for the 27 weights w in artifacts/toe_sm_decomposition_27.json.
    """
    sm = _load_json(IN_SM)
    per = sm.get("per_vertex")
    if not (isinstance(per, list) and len(per) == 27):
        raise RuntimeError("Invalid toe_sm_decomposition_27.json: per_vertex")

    W = np.array([r["w"] for r in per], dtype=float)  # (27,6)
    q = np.array([r["Qpsi3"] for r in per], dtype=float)  # (27,)
    if W.shape != (27, 6):
        raise RuntimeError(f"Unexpected weight matrix shape {W.shape}")

    # Least squares (no intercept). This recovers exact integers in this repo.
    c, *_ = np.linalg.lstsq(W, q, rcond=None)
    ci = np.rint(c).astype(int)
    resid = np.max(np.abs(W @ ci - q))
    if resid > 1e-9:
        raise RuntimeError(
            f"Failed to recover integer Qpsi vector; max residual {resid}"
        )

    # Reduce by gcd to a primitive integer vector.
    g = int(np.gcd.reduce(np.abs(ci)))
    if g <= 0:
        raise RuntimeError("Bad gcd for Qpsi vector")
    c_prim = (ci // g).tolist()
    if np.max(np.abs(W @ np.array(c_prim, dtype=int) - q)) > 1e-9:
        raise RuntimeError("Primitive reduction broke exactness (unexpected)")

    # Record charge histogram.
    q_hist = Counter(int(x) for x in (W @ np.array(c_prim, dtype=int)).tolist())

    return {
        "c_vec": [int(x) for x in c_prim],
        "gcd_reduction": int(g),
        "qpsi_histogram": dict(sorted(q_hist.items())),
        "expected_histogram": {"-2": 10, "1": 16, "4": 1},
    }


def analyze_e8_root_channels(c_vec: List[int]) -> Dict[str, object]:
    meta = _load_json(IN_E8)
    rows = meta.get("rows")
    if not isinstance(rows, list) or len(rows) != 240:
        raise RuntimeError("Invalid e8_root_metadata_table.json: rows")

    c = np.array(c_vec, dtype=int)
    by_grade: Dict[str, Counter[int]] = {}
    all_hist: Counter[int] = Counter()
    sample: List[Dict[str, object]] = []

    for r in rows:
        rt = r["root_trin"]
        if not (isinstance(rt, list) and len(rt) == 8):
            raise RuntimeError("Bad root_trin entry")
        qpsi = int(c @ np.array(rt[:6], dtype=int))
        grade = str(r["grade"])
        by_grade.setdefault(grade, Counter())[qpsi] += 1
        all_hist[qpsi] += 1

        if len(sample) < 5:
            sample.append(
                {
                    "edge": r["edge"],
                    "grade": grade,
                    "phase_z6": int(r["phase_z6"]),
                    "Qpsi": qpsi,
                    "root_trin": rt,
                }
            )

    expected = {
        "g0_e6": {0: 40, -3: 16, 3: 16},
        "g0_a2": {0: 6},
        "g1": {1: 48, -2: 30, 4: 3},
        "g2": {-1: 48, 2: 30, -4: 3},
    }
    matches = {
        g: dict(sorted(ct.items())) == expected.get(g, {}) for g, ct in by_grade.items()
    }

    return {
        "all_histogram": dict(sorted(all_hist.items())),
        "by_grade_histogram": {
            g: dict(sorted(ct.items())) for g, ct in by_grade.items()
        },
        "expected_by_grade": {
            g: {str(k): int(v) for k, v in expected[g].items()} for g in expected
        },
        "matches_expected": matches,
        "sample": sample,
    }


def analyze_w33_lines_and_fusion(c_vec: List[int]) -> Dict[str, object]:
    meta = _load_json(IN_E8)
    rows = meta.get("rows")
    if not isinstance(rows, list) or len(rows) != 240:
        raise RuntimeError("Invalid e8_root_metadata_table.json: rows")

    edge_to_row = {tuple(sorted(r["edge"])): r for r in rows}
    root_orbit_to_row = {tuple(int(x) for x in r["root_orbit"]): r for r in rows}
    if len(edge_to_row) != 240 or len(root_orbit_to_row) != 240:
        raise RuntimeError("Expected bijection for edge/root mappings")

    c = np.array(c_vec, dtype=int)
    C8 = _cartan_unit_e8_sage_order()

    lines = _load_json(IN_LINES).get("per_line")
    if not isinstance(lines, list) or len(lines) != 40:
        raise RuntimeError("Invalid w33_line_fusion_law.json: per_line")
    line_vertices = [tuple(int(x) for x in entry["line"]) for entry in lines]

    # Build per-line phase->root_orbit and per-line edge list.
    line_phase_to_root_orbit: List[Dict[int, Tuple[int, ...]]] = []
    line_edge_list: List[List[Tuple[int, int]]] = []
    for L in line_vertices:
        elist = [tuple(sorted(e)) for e in combinations(L, 2)]
        phase_to_root: Dict[int, Tuple[int, ...]] = {}
        for e in elist:
            row = edge_to_row[e]
            phase_to_root[int(row["phase_z6"])] = tuple(
                int(x) for x in row["root_orbit"]
            )
        if set(phase_to_root.keys()) != set(range(6)):
            raise RuntimeError("Line does not realize all 6 phases")
        line_phase_to_root_orbit.append(phase_to_root)
        line_edge_list.append(elist)

    # Per-line pattern summaries.
    line_patterns: Counter[str] = Counter()
    per_line: List[Dict[str, object]] = []
    for i, elist in enumerate(line_edge_list):
        grade_ct: Counter[str] = Counter()
        q_ct: Counter[int] = Counter()
        q_by_phase: Dict[int, int] = {}
        for e in elist:
            row = edge_to_row[e]
            grade_ct[str(row["grade"])] += 1
            q = int(c @ np.array(row["root_trin"][:6], dtype=int))
            q_ct[q] += 1
            q_by_phase[int(row["phase_z6"])] = q
        patt = (
            f"grades={dict(sorted(grade_ct.items()))} qpsi={dict(sorted(q_ct.items()))}"
        )
        line_patterns[patt] += 1
        if len(per_line) < 10:
            per_line.append(
                {
                    "i": i,
                    "line": list(line_vertices[i]),
                    "grade_hist": dict(sorted(grade_ct.items())),
                    "Qpsi_by_phase": [q_by_phase[p] for p in range(6)],
                }
            )

    # Phase-resolved fusion rule + Qpsi additivity check.
    # Iterate all coupled pairs via cross-ip pattern (12,12,12).
    coupled_pairs = 0
    diff_pattern_counts: Counter[Tuple[int, ...]] = Counter()
    diff_to_out_is_deterministic = True
    qpsi_additivity_ok = True

    # Edge->line index lookup.
    edge_to_line: Dict[Tuple[int, int], int] = {}
    for li, elist in enumerate(line_edge_list):
        for e in elist:
            edge_to_line[e] = li
    if len(edge_to_line) != 240:
        raise RuntimeError("Expected 240 edges in edge_to_line map")

    # Precompute root-orbit vector lookup for output.
    for i in range(40):
        for j in range(i + 1, 40):
            # Cross-ip pattern between the two A2 sets (6x6).
            patt = Counter()
            for ra in line_phase_to_root_orbit[i].values():
                for rb in line_phase_to_root_orbit[j].values():
                    patt[_ip_orbit_coeffs(ra, rb, C8)] += 1
            cross = (patt.get(0, 0), patt.get(-1, 0), patt.get(1, 0))
            if cross == (36, 0, 0):
                continue
            if cross != (12, 12, 12):
                raise RuntimeError(
                    f"Unexpected cross-ip pattern {cross} for lines {(i,j)}"
                )

            coupled_pairs += 1
            diff_counts = [0] * 6
            diff_to_out: Dict[int, int] = {}

            for pa, ra in line_phase_to_root_orbit[i].items():
                for pb, rb in line_phase_to_root_orbit[j].items():
                    if _ip_orbit_coeffs(ra, rb, C8) != -1:
                        continue
                    d = (pa - pb) % 6
                    diff_counts[d] += 1
                    rc = tuple(int(ra[k] + rb[k]) for k in range(8))
                    out_row = root_orbit_to_row.get(rc)
                    if out_row is None:
                        raise RuntimeError("Missing sum-root (should not happen in E8)")
                    out_edge = tuple(sorted(out_row["edge"]))
                    out_line = edge_to_line[out_edge]

                    if d in diff_to_out and diff_to_out[d] != out_line:
                        diff_to_out_is_deterministic = False
                    diff_to_out[d] = out_line

                    # Qpsi additivity: q(α+β)=q(α)+q(β).
                    qa = int(
                        c @ np.array(out_row["root_trin"][:6], dtype=int)
                    )  # q of γ
                    qlhs = qa
                    qrhs = int(
                        c
                        @ np.array(
                            edge_to_row[tuple(sorted(out_row["edge"]))]["root_trin"][
                                :6
                            ],
                            dtype=int,
                        )
                    )
                    # qrhs is same as qlhs (sanity)
                    if qlhs != qrhs:
                        qpsi_additivity_ok = False
                    # check qγ = qα + qβ using root_trin:
                    q_alpha = int(
                        c
                        @ np.array(
                            edge_to_row[tuple(sorted(out_row["edge"]))]["root_trin"][
                                :6
                            ],
                            dtype=int,
                        )
                    )
                    # The above is redundant; compute directly from ra/rb in trinification coords:
                    qa2 = int(
                        c @ np.array([0, 0, 0, 0, 0, 0], dtype=int)
                    )  # placeholder
                    _ = qa2  # keep linters quiet
                    # We have the full trin coords for α,β,γ in the metadata table:
                    q_a = int(
                        c @ np.array(root_orbit_to_row[ra]["root_trin"][:6], dtype=int)
                    )
                    q_b = int(
                        c @ np.array(root_orbit_to_row[rb]["root_trin"][:6], dtype=int)
                    )
                    q_g = int(c @ np.array(out_row["root_trin"][:6], dtype=int))
                    if q_g != q_a + q_b:
                        qpsi_additivity_ok = False

            diff_pattern_counts[tuple(diff_counts)] += 1

    return {
        "line_pattern_counts": dict(line_patterns),
        "per_line_examples": per_line,
        "fusion": {
            "coupled_pairs": int(coupled_pairs),
            "diff_pattern_counts": {
                str(k): int(v) for k, v in diff_pattern_counts.items()
            },
            "diff_to_output_line_deterministic": bool(diff_to_out_is_deterministic),
            "Qpsi_additivity_ok": bool(qpsi_additivity_ok),
        },
    }


def analyze_firewall_clock_and_qpsi() -> Dict[str, object]:
    toe_dynamics = _load_module(ROOT / "tools" / "toe_dynamics.py", "toe_dynamics_cf")

    sm = _load_json(IN_SM)
    per = sm.get("per_vertex")
    if not (isinstance(per, list) and len(per) == 27):
        raise RuntimeError("Invalid toe_sm_decomposition_27.json: per_vertex")
    qpsi_by_v = {int(r["i"]): int(r["Qpsi3"]) for r in per}
    field_by_v = {int(r["i"]): str(r["field"]) for r in per}

    skew, meet = toe_dynamics.load_schlafli_graph()
    fw = toe_dynamics.load_firewall_bad_edges()
    bad = set(fw.bad_edges)

    # Count k6-defined edges by class.
    k6_defined_skew = 0
    k6_defined_good_meet = 0
    k6_defined_bad_meet = 0
    k6_skew_hist: Counter[int] = Counter()
    k6_bad_hist: Counter[int] = Counter()

    for i in range(27):
        for j in range(i + 1, 27):
            k6 = toe_dynamics.schlafli_edge_clock_k6(i, j)
            has = k6 is not None
            is_bad = (i, j) in bad
            if skew[i, j]:
                if has:
                    k6_defined_skew += 1
                    k6_skew_hist[int(k6)] += 1
            if meet[i, j]:
                if is_bad:
                    if has:
                        k6_defined_bad_meet += 1
                        k6_bad_hist[int(k6)] += 1
                else:
                    if has:
                        k6_defined_good_meet += 1

    # Sanity totals.
    n_skew = int(skew.sum() // 2)
    n_meet = int(meet.sum() // 2)
    if n_skew != 216 or n_meet != 135:
        raise RuntimeError(
            f"Unexpected Schläfli edge counts: skew={n_skew} meet={n_meet}"
        )
    if len(bad) != 27:
        raise RuntimeError("Expected 27 firewall bad edges")

    characterization_ok = (
        k6_defined_skew == n_skew
        and k6_defined_bad_meet == 27
        and k6_defined_good_meet == 0
    )

    # Qpsi pair histogram on bad edges.
    qpsi_pair_hist: Counter[Tuple[int, int]] = Counter()
    field_pair_hist: Counter[Tuple[str, str]] = Counter()
    for u, v in bad:
        a = qpsi_by_v[u]
        b = qpsi_by_v[v]
        qpsi_pair_hist[tuple(sorted((a, b)))] += 1
        fa = field_by_v[u]
        fb = field_by_v[v]
        field_pair_hist[tuple(sorted((fa, fb)))] += 1

    return {
        "counts": {
            "schlafli_skew_edges": n_skew,
            "schlafli_meet_edges": n_meet,
            "firewall_bad_meet_edges": 27,
            "k6_defined_on_skew_edges": k6_defined_skew,
            "k6_defined_on_bad_meet_edges": k6_defined_bad_meet,
            "k6_defined_on_good_meet_edges": k6_defined_good_meet,
        },
        "k6_histograms": {
            "skew_edges": dict(sorted(k6_skew_hist.items())),
            "bad_meet_edges": dict(sorted(k6_bad_hist.items())),
        },
        "characterization": {
            "statement": "A Schläfli pair has a defined W33-derived k6 clock iff it is a skew edge OR a firewall-bad meet edge.",
            "ok": bool(characterization_ok),
        },
        "bad_edge_qpsi_pairs": {
            str(k): int(v) for k, v in sorted(qpsi_pair_hist.items())
        },
        "bad_edge_field_pairs_top20": [
            {"pair": list(k), "count": int(v)}
            for k, v in field_pair_hist.most_common(20)
        ],
    }


def main() -> None:
    qpsi = solve_qpsi_cartan_vector()
    c_vec = [int(x) for x in qpsi["c_vec"]]

    e8 = analyze_e8_root_channels(c_vec)
    lines = analyze_w33_lines_and_fusion(c_vec)
    fw = analyze_firewall_clock_and_qpsi()

    out: Dict[str, object] = {
        "status": "ok",
        "qpsi": qpsi,
        "e8_root_channels": e8,
        "w33_lines_and_fusion": lines,
        "firewall_clock": fw,
        "sources": {
            "toe_sm_decomposition_27": IN_SM.relative_to(ROOT).as_posix(),
            "e8_root_metadata_table": IN_E8.relative_to(ROOT).as_posix(),
            "w33_line_fusion_law": IN_LINES.relative_to(ROOT).as_posix(),
            "toe_dynamics": "tools/toe_dynamics.py",
        },
    }

    _write_json(OUT_JSON, out)

    md: List[str] = []
    md.append("# TOE closed-form selection rules")
    md.append("")
    md.append(f"- status: `{out['status']}`")
    md.append("")
    md.append("## SO(10)×U(1)_psi (exact)")
    md.append(f"- `c_vec = {c_vec}` (so that `Qpsi3 = c·w` exactly on the 27 weights)")
    md.append(
        f"- Qpsi histogram on 27: `{qpsi['qpsi_histogram']}` (expected 16×1, 10×(-2), 1×4)"
    )
    md.append("")
    md.append("## E8 root-channel Qpsi spectrum by grade")
    md.append(f"- all: `{e8['all_histogram']}`")
    for g, ct in e8["by_grade_histogram"].items():
        md.append(
            f"- {g}: `{ct}` (matches expected: `{e8['matches_expected'].get(g)}`)"
        )
    md.append("")
    md.append("## W33 line fusion (phase-resolved)")
    md.append(f"- coupled line pairs: `{lines['fusion']['coupled_pairs']}`")
    md.append(
        f"- diff→output-line deterministic: `{lines['fusion']['diff_to_output_line_deterministic']}`"
    )
    md.append(
        f"- Qpsi additivity on all interacting pairs: `{lines['fusion']['Qpsi_additivity_ok']}`"
    )
    md.append("")
    md.append("## Firewall clock characterization (Schläfli 27)")
    md.append(f"- counts: `{fw['counts']}`")
    md.append(f"- characterization ok: `{fw['characterization']['ok']}`")
    md.append(
        f"- k6 histogram on bad meet edges: `{fw['k6_histograms']['bad_meet_edges']}`"
    )
    md.append("")
    md.append(f"- JSON: `{OUT_JSON.relative_to(ROOT).as_posix()}`")
    _write_md(OUT_MD, md)

    print(f"wrote {OUT_JSON.relative_to(ROOT).as_posix()}")


if __name__ == "__main__":
    main()
