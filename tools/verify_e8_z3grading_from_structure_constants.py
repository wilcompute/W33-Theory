#!/usr/bin/env python3
"""
Verify that the exported E8 structure constants respect the standard Z3-graded
trinification decomposition:

  e8 = g0 ⊕ g1 ⊕ g2
  g0 = e6 ⊕ a2
  g1 = 27 ⊗ 3
  g2 = 27̄ ⊗ 3̄

using only:
  - artifacts/e8_structure_constants_w33_discrete.json  (248-dim bracket table)
  - artifacts/e8_root_metadata_table.json               (grade labels per root)

Checks
------
1) Grading preservation: for every nonzero bracket term [x,y] -> z, we have
   grade(z) ≡ grade(x)+grade(y) (mod 3) with grade(g0)=0, grade(g1)=1, grade(g2)=2.
2) Direct-sum split in grade-0 roots:
   - [g0_e6_root, g0_a2_root] = 0
   - [g0_e6_root, g0_e6_root] outputs only (Cartan or g0_e6 roots)
   - [g0_a2_root, g0_a2_root] outputs only (Cartan or g0_a2 roots)

Outputs
-------
  - artifacts/verify_e8_z3grading_from_structure_constants.json
  - artifacts/verify_e8_z3grading_from_structure_constants.md
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]
IN_SC = ROOT / "artifacts" / "e8_structure_constants_w33_discrete.json"
IN_META = ROOT / "artifacts" / "e8_root_metadata_table.json"
OUT_JSON = ROOT / "artifacts" / "verify_e8_z3grading_from_structure_constants.json"
OUT_MD = ROOT / "artifacts" / "verify_e8_z3grading_from_structure_constants.md"


Pair = Tuple[int, int]
Root = Tuple[int, ...]


def _load_grade_map() -> Dict[Root, str]:
    meta = json.loads(IN_META.read_text(encoding="utf-8"))
    rows = meta["rows"]
    out: Dict[Root, str] = {}
    for r in rows:
        rt = tuple(int(x) for x in r["root_orbit"])
        out[rt] = str(r["grade"])
    if len(out) != 240:
        raise RuntimeError(f"Expected 240 root grades; got {len(out)}")
    return out


def _grade_value(label: str) -> int:
    if label.startswith("g0"):
        return 0
    if label == "g1":
        return 1
    if label == "g2":
        return 2
    raise ValueError(f"Unknown grade label: {label}")


def _describe_basis_idx(
    idx: int, cartan_dim: int, roots: List[List[int]], grade_by_root: Dict[Root, str]
) -> Dict[str, object]:
    if idx < cartan_dim:
        return {"kind": "h", "h_index_1based": idx + 1, "grade": "g0"}
    r = idx - cartan_dim
    rt = tuple(int(x) for x in roots[r])
    gl = grade_by_root[rt]
    return {"kind": "e", "root_index": r, "root_orbit": list(rt), "grade": gl}


def main() -> None:
    grade_by_root = _load_grade_map()

    sc = json.loads(IN_SC.read_text(encoding="utf-8"))
    basis = sc["basis"]
    n = int(basis["n"])
    cartan_dim = int(basis["cartan_dim"])
    roots: List[List[int]] = basis["roots"]
    if n != 248 or cartan_dim != 8 or len(roots) != 240:
        raise RuntimeError(
            f"Unexpected basis sizing: n={n} cartan_dim={cartan_dim} roots={len(roots)}"
        )

    # Precompute grade label/value for each basis index.
    grade_label_by_idx: List[str] = ["g0"] * n
    grade_value_by_idx: List[int] = [0] * n
    for i in range(cartan_dim, n):
        rt = tuple(int(x) for x in roots[i - cartan_dim])
        gl = grade_by_root[rt]
        grade_label_by_idx[i] = gl
        grade_value_by_idx[i] = _grade_value(gl)

    brackets: Dict[str, List[List[int]]] = sc["brackets"]

    term_violations = 0
    first_term_violation: Dict[str, object] | None = None
    terms_checked = 0

    # Direct-sum split checks restricted to root-root brackets.
    ds_violations = {
        "noncommuting_e6_a2": 0,
        "e6_mixes_into_a2": 0,
        "a2_mixes_into_e6": 0,
    }
    first_ds_violation: Dict[str, object] | None = None

    for key, terms in brackets.items():
        i_str, j_str = key.split(",")
        i, j = int(i_str), int(j_str)
        gi = grade_value_by_idx[i]
        gj = grade_value_by_idx[j]
        target = (gi + gj) % 3

        for k, c in terms:
            terms_checked += 1
            gk = grade_value_by_idx[int(k)]
            if gk != target:
                term_violations += 1
                if first_term_violation is None:
                    first_term_violation = {
                        "pair": [i, j],
                        "pair_basis": [
                            _describe_basis_idx(i, cartan_dim, roots, grade_by_root),
                            _describe_basis_idx(j, cartan_dim, roots, grade_by_root),
                        ],
                        "term": [int(k), int(c)],
                        "term_basis": _describe_basis_idx(
                            int(k), cartan_dim, roots, grade_by_root
                        ),
                        "expected_grade_mod3": int(target),
                        "actual_grade_mod3": int(gk),
                    }

        # Direct-sum checks for root-root brackets only (ignore Cartan-root brackets).
        if i < cartan_dim or j < cartan_dim:
            continue
        li = grade_label_by_idx[i]
        lj = grade_label_by_idx[j]

        # [g0_e6, g0_a2] = 0
        if (li == "g0_e6" and lj == "g0_a2") or (li == "g0_a2" and lj == "g0_e6"):
            # Any nonzero term is a violation (even Cartan).
            if terms:
                ds_violations["noncommuting_e6_a2"] += 1
                if first_ds_violation is None:
                    first_ds_violation = {
                        "kind": "noncommuting_e6_a2",
                        "pair": [i, j],
                        "pair_basis": [
                            _describe_basis_idx(i, cartan_dim, roots, grade_by_root),
                            _describe_basis_idx(j, cartan_dim, roots, grade_by_root),
                        ],
                        "terms": terms[:12],
                    }
            continue

        # [g0_e6,g0_e6] outputs only g0_e6 roots (or Cartan)
        if li == "g0_e6" and lj == "g0_e6":
            for k, c in terms:
                if int(k) < cartan_dim:
                    continue
                if grade_label_by_idx[int(k)] != "g0_e6":
                    ds_violations["e6_mixes_into_a2"] += 1
                    if first_ds_violation is None:
                        first_ds_violation = {
                            "kind": "e6_mixes_into_a2",
                            "pair": [i, j],
                            "pair_basis": [
                                _describe_basis_idx(
                                    i, cartan_dim, roots, grade_by_root
                                ),
                                _describe_basis_idx(
                                    j, cartan_dim, roots, grade_by_root
                                ),
                            ],
                            "term": [int(k), int(c)],
                            "term_basis": _describe_basis_idx(
                                int(k), cartan_dim, roots, grade_by_root
                            ),
                        }
                    break
            continue

        # [g0_a2,g0_a2] outputs only g0_a2 roots (or Cartan)
        if li == "g0_a2" and lj == "g0_a2":
            for k, c in terms:
                if int(k) < cartan_dim:
                    continue
                if grade_label_by_idx[int(k)] != "g0_a2":
                    ds_violations["a2_mixes_into_e6"] += 1
                    if first_ds_violation is None:
                        first_ds_violation = {
                            "kind": "a2_mixes_into_e6",
                            "pair": [i, j],
                            "pair_basis": [
                                _describe_basis_idx(
                                    i, cartan_dim, roots, grade_by_root
                                ),
                                _describe_basis_idx(
                                    j, cartan_dim, roots, grade_by_root
                                ),
                            ],
                            "term": [int(k), int(c)],
                            "term_basis": _describe_basis_idx(
                                int(k), cartan_dim, roots, grade_by_root
                            ),
                        }
                    break

    ok = (term_violations == 0) and all(v == 0 for v in ds_violations.values())
    out = {
        "status": "ok" if ok else "fail",
        "paths": {
            "structure_constants": IN_SC.relative_to(ROOT).as_posix(),
            "root_metadata": IN_META.relative_to(ROOT).as_posix(),
        },
        "counts": {
            "n": n,
            "cartan_dim": cartan_dim,
            "root_dim": len(roots),
            "nonzero_bracket_pairs_i_lt_j": len(brackets),
            "bracket_terms_checked": int(terms_checked),
            "grade_term_violations": int(term_violations),
            "direct_sum_violations": {k: int(v) for k, v in ds_violations.items()},
        },
        "first_grade_violation": first_term_violation,
        "first_direct_sum_violation": first_ds_violation,
    }

    OUT_JSON.write_text(
        json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    md: List[str] = []
    md.append("# E8 Z3-grading verification (from W33-discrete structure constants)\n")
    md.append(f"- status: `{out['status']}`")
    md.append(f"- bracket terms checked: `{terms_checked}`")
    md.append(f"- grading violations: `{term_violations}`")
    md.append(f"- direct-sum violations: `{out['counts']['direct_sum_violations']}`\n")
    md.append(f"- JSON: `{OUT_JSON.relative_to(ROOT).as_posix()}`")
    OUT_MD.write_text("\n".join(md).rstrip() + "\n", encoding="utf-8")

    print(
        f"status={out['status']} terms_checked={terms_checked} wrote={OUT_JSON.relative_to(ROOT).as_posix()}"
    )
    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
