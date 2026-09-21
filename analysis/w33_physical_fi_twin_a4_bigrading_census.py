#!/usr/bin/env python3
"""Exact joint census of the physical FI Z3 grading and twin-A4 Z5 gluing.

This is a finite E8 root-set calculation.  It composes exactly two already
certified physical inputs:

* ``w33_physical_fi_e6_a2_z3_grading.py``: the FI Cartan projection t_A,
  whose adjoint root grades are 78+81+81;
* ``w33_physical_twin_a4_e8_index5_gluing.py``: two orthogonal physical A4
  systems with Z/5 discriminant gluing c_gauge = 3 c_center mod 5.

The script does not identify the two finite quotients.  It proves the opposite
at the only available root-set level: FI grade is not a function of the Z/5
class.  Since the grading is Z/3 and the gluing quotient is Z/5, no nontrivial
homomorphism relates the quotient groups.  The structures coexist as independent
bookkeeping data on the same 240 roots.
"""
from __future__ import annotations

import importlib.util
import itertools
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/w33_physical_fi_twin_a4_bigrading_census.json"


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


T = load(ROOT / "analysis/w33_physical_twin_a4_e8_index5_gluing.py", "twin")
Z = load(ROOT / "analysis/w33_physical_fi_e6_a2_z3_grading.py", "z3")


def fi_grade(root):
    t = Z.lin(Z.A4, Z.COEFF)
    return Z.dot(t, root) % 1


def main(write: bool = True):
    roots = list(Z.roots_e8())
    assert len(roots) == 240
    rows = Counter()
    for root in roots:
        center_norm = T.proj_norm(root, T.CENTER)
        gauge_norm = T.proj_norm(root, T.GAUGE)
        center_class = T.discr_class(root, T.CENTER)
        gauge_class = T.discr_class(root, T.GAUGE)
        rows[(str(fi_grade(root)), str(center_norm), str(gauge_norm), center_class, gauge_class)] += 1

    expected = {
        ("0", "0", "2", 0, 0): 20,
        ("0", "2", "0", 0, 0): 8,
        ("0", "4/5", "6/5", 1, 3): 20,
        ("0", "4/5", "6/5", 4, 2): 20,
        ("0", "6/5", "4/5", 2, 1): 5,
        ("0", "6/5", "4/5", 3, 4): 5,
        ("1/3", "2", "0", 0, 0): 6,
        ("1/3", "4/5", "6/5", 1, 3): 30,
        ("1/3", "6/5", "4/5", 2, 1): 30,
        ("1/3", "6/5", "4/5", 3, 4): 15,
        ("2/3", "2", "0", 0, 0): 6,
        ("2/3", "4/5", "6/5", 4, 2): 30,
        ("2/3", "6/5", "4/5", 2, 1): 15,
        ("2/3", "6/5", "4/5", 3, 4): 30,
    }
    assert dict(rows) == expected

    grade_totals = Counter()
    z5_totals = Counter()
    per_z5_grades = {}
    for key, count in rows.items():
        grade, center_norm, gauge_norm, center_class, gauge_class = key
        grade_totals[grade] += count
        z5_key = (center_norm, gauge_norm, center_class, gauge_class)
        z5_totals[z5_key] += count
        per_z5_grades.setdefault(z5_key, Counter())[grade] += count
    assert dict(grade_totals) == {"0": 78, "1/3": 81, "2/3": 81}
    assert sorted(z5_totals.values()) == [20, 20, 50, 50, 50, 50]
    assert all(gauge_class == (3 * center_class) % 5 for _, _, _, center_class, gauge_class in rows)

    mixed_classes_have_multiple_fi_grades = {
        "/".join(map(str, key)): sorted(grades)
        for key, grades in per_z5_grades.items()
        if key[2] != 0
    }
    assert all(len(grades) > 1 for grades in mixed_classes_have_multiple_fi_grades.values())

    out = {
        "schema": "w33.physical_fi_twin_a4_bigrading_census.v1",
        "status": "PASS_PHYSICAL_FI_TWIN_A4_BIGRADING_CENSUS",
        "headline": "The physical FI Z3 grading and the physical twin-A4 Z5 lattice gluing admit a complete exact 14-cell joint census on the same 240 E8 roots. FI grade totals are 78+81+81; the gluing totals are 20+20+50+50+50+50. Every mixed Z5 class occurs at more than one FI grade, so the FI grade is not a function of the discriminant class.",
        "joint_cells": [
            {"FI_grade": key[0], "center_norm2": key[1], "gauge_norm2": key[2],
             "center_class": key[3], "gauge_class": key[4], "count": value}
            for key, value in sorted(rows.items())
        ],
        "marginals": {
            "FI_Z3": dict(sorted(grade_totals.items())),
            "twin_A4_Z5": [
                {"center_norm2": key[0], "gauge_norm2": key[1], "center_class": key[2],
                 "gauge_class": key[3], "count": value}
                for key, value in sorted(z5_totals.items())
            ],
        },
        "independence_firewall": {
            "FI_grade_is_function_of_Z5_class": False,
            "mixed_Z5_class_to_FI_grades": mixed_classes_have_multiple_fi_grades,
            "coprime_quotient_orders": {"FI": 3, "E8_overlattice_gluing": 5, "gcd": 1},
            "statement": "This finite root-set result forbids identifying the FI Z3 quotient with the twin-A4 Z5 discriminant quotient. It does not forbid a relation mediated by additional structure, but none is supplied here.",
        },
        "provenance": [
            "analysis/w33_physical_fi_e6_a2_z3_grading.py",
            "analysis/w33_physical_twin_a4_e8_index5_gluing.py",
        ],
        "scope": "Exact finite E8 root arithmetic for the recorded physical flagship bases. No D/F-flat vacuum, CFT amplitude, phenomenological family assignment, or identification with the canonical W33 tetracode A2 is claimed.",
        "checks": {
            "all_240_roots_enumerated": sum(rows.values()) == 240,
            "joint_table_has_14_cells": len(rows) == 14,
            "FI_marginal_is_78_81_81": dict(grade_totals) == {"0": 78, "1/3": 81, "2/3": 81},
            "twin_A4_marginal_is_20_20_4x50": sorted(z5_totals.values()) == [20, 20, 50, 50, 50, 50],
            "Z5_gluing_law_holds": all(gauge_class == (3 * center_class) % 5 for _, _, _, center_class, gauge_class in rows),
            "FI_not_function_of_Z5_class": all(len(grades) > 1 for grades in mixed_classes_have_multiple_fi_grades.values()),
        },
    }
    assert all(out["checks"].values())
    if write:
        OUT.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))
    return out


if __name__ == "__main__":
    main(True)
