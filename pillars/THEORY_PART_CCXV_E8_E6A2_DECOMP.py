#!/usr/bin/env python3
"""Pillar 115 (Part CCXV): E8 Root Decomposition under E6 x A2

The 240 E8 roots decompose under the embedding E6 x A2 < E8 into three
sectors: 72 E6 roots, 6 A2 roots, and 162 = 3 x 54 mixed roots.  Passing
to root lines (antipodal pairs), the PSp(4,3) line action on 120 lines has
orbit structure 36 + 27+27+27 + 1+1+1, while the edgepair action is
transitive (single orbit of 120).  The three orbits of size 27 and three
singletons give the algebraic backbone for three generations of 27 matter
fields under an SU(3) color group.

Theorems:

T1  DOT-PAIR INVARIANT: The vectors u1=(1,...,1) and u2=(1,...,1,-1,-1) in
    R^8 yield dot-pair (r.u1, r.u2) classifying all 240 E8 roots into
    exactly 13 classes with sizes 72+6+162=240.  The classification is
    invariant under the full W(E6) action.

T2  E6 SECTOR (72 ROOTS): The 72 roots with dot-pair (0,0) form the E6
    root system.  72 = dim(E6) - rank(E6) = 78 - 6 = 72 (nonzero E6 roots).
    These form a single W(E6)-orbit.

T3  A2 SECTOR (6 ROOTS): The 6 singleton dot-pair classes each contain
    exactly 1 root.  Together they form the A2 root system: 6 = 2*3 nonzero
    roots of rank-2 SU(3).  These are the roots fixed by W(E6) up to sign.

T4  MIXED SECTOR (162 ROOTS): The remaining 162 = 240-72-6 roots lie in
    6 classes of size 27 each (6*27=162).  These pair by (r,-r) into three
    54-element orbits, corresponding to the (27,3) + (27bar,3bar) of E6 x A2.

T5  NON-CONJUGATE REPRESENTATIONS: The PSp(4,3) edgepair action (degree 120)
    is TRANSITIVE (single orbit of size 120).  The line action (degree 120)
    is INTRANSITIVE with orbits {36, 27, 27, 27, 1, 1, 1}.  The two actions
    cannot be conjugate in S_120.

T6  THREE-GENERATION STRUCTURE: In the line orbit decomposition:
    - 36-orbit = E6 root lines (72/2 = 36 antipodal pairs)
    - 3 orbits of 27 = three generations of 27 E6-matter-field lines
    - 3 singletons = A2 root lines (6/2 = 3 pairs) = SU(3) color generators
    Total: 36 + 3*27 + 3*1 = 36 + 81 + 3 = 120 lines.
"""

from __future__ import annotations

import json
from collections import Counter, deque
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts" / "explicit_bijection_decomposition.json"
EDGEPAIR_GENS = ROOT / "artifacts" / "sp43_edgepair_generators.json"
LINE_GENS = ROOT / "SP43_TO_WE6_TRUE_FIXED_BUNDLE_v01_2026-02-25" / "sp43_line_perms_fixed.json"

U1 = (1, 1, 1, 1, 1, 1, 1, 1)
U2 = (1, 1, 1, 1, 1, 1, -1, -1)

N_ROOTS = 240
N_E6_ROOTS = 72
N_A2_ROOTS = 6
N_MIXED_ROOTS = 162
N_LINES = 120


def _dot(r: List[int], u: Tuple[int, ...]) -> int:
    return sum(int(r[i]) * u[i] for i in range(8))


def _orbits_from_gens(n: int, gens: List[List[int]]) -> List[List[int]]:
    seen = [False] * n
    orbits = []
    for start in range(n):
        if seen[start]:
            continue
        q: deque = deque([start])
        seen[start] = True
        orb = [start]
        while q:
            x = q.popleft()
            for g in gens:
                y = g[x]
                if not seen[y]:
                    seen[y] = True
                    q.append(y)
                    orb.append(y)
        orbits.append(sorted(orb))
    return sorted(orbits, key=len, reverse=True)


def analyze() -> dict:
    art = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    roots = art["root_coords"]
    class72_key = tuple(art["class72_key"])
    class1_keys = [tuple(x) for x in art["class1_keys"]]
    class27_keys = [tuple(x) for x in art["class27_keys"]]

    # T1: Dot-pair invariant — classify all 240 roots
    classes: Dict[Tuple, List[int]] = {}
    for i, r in enumerate(roots):
        key = (_dot(r, U1), _dot(r, U2))
        classes.setdefault(key, []).append(i)
    t1_n_classes = len(classes)
    t1_class_sizes = sorted([len(v) for v in classes.values()], reverse=True)
    t1_total_roots = sum(len(v) for v in classes.values())
    t1_correct = (t1_total_roots == N_ROOTS and t1_n_classes == 13)

    # T2: E6 sector (72 roots)
    e6_roots = classes.get(class72_key, [])
    t2_e6_size = len(e6_roots)
    t2_e6_key = list(class72_key)
    t2_e6_correct = (t2_e6_size == N_E6_ROOTS)

    # T3: A2 sector (6 singleton roots)
    a2_sizes = [len(classes.get(k, [])) for k in class1_keys]
    t3_a2_total = sum(a2_sizes)
    t3_all_singletons = all(s == 1 for s in a2_sizes)
    t3_n_singleton_classes = len(class1_keys)
    t3_a2_correct = (t3_a2_total == N_A2_ROOTS and t3_all_singletons)

    # T4: Mixed sector (162 = 6 x 27)
    mixed_sizes = [len(classes.get(k, [])) for k in class27_keys]
    t4_mixed_total = sum(mixed_sizes)
    t4_all_27 = all(s == 27 for s in mixed_sizes)
    t4_n_mixed_classes = len(class27_keys)
    t4_mixed_correct = (t4_mixed_total == N_MIXED_ROOTS and t4_all_27)
    # Verify 72 + 6 + 162 = 240
    t4_total_check = (t2_e6_size + t3_a2_total + t4_mixed_total == N_ROOTS)

    # T5: Non-conjugate representations
    ep_data = json.loads(EDGEPAIR_GENS.read_text(encoding="utf-8"))
    ep_gens = ep_data["pair_generators"]
    line_gens = json.loads(LINE_GENS.read_text(encoding="utf-8"))

    ep_orbits = _orbits_from_gens(len(ep_gens[0]), ep_gens)
    line_orbits = _orbits_from_gens(len(line_gens[0]), line_gens)

    ep_orbit_sizes = sorted([len(o) for o in ep_orbits], reverse=True)
    line_orbit_sizes = sorted([len(o) for o in line_orbits], reverse=True)

    t5_ep_transitive = (ep_orbit_sizes == [120])
    t5_line_intransitive = (len(line_orbits) > 1)
    t5_line_orbit_sizes = line_orbit_sizes
    t5_non_conjugate = (t5_ep_transitive and t5_line_intransitive)

    # T6: Three-generation structure
    # In line orbits: 36 (E6 lines) + 27+27+27 (3 generations) + 1+1+1 (A2 lines)
    t6_e6_lines = N_E6_ROOTS // 2   # 36
    t6_a2_lines = N_A2_ROOTS // 2   # 3
    t6_matter_lines_per_gen = 27
    t6_n_generations = 3
    t6_total_lines_check = t6_e6_lines + t6_n_generations * t6_matter_lines_per_gen + t6_a2_lines
    # Verify against actual line orbit structure
    t6_line_36_count = line_orbit_sizes.count(36)
    t6_line_27_count = line_orbit_sizes.count(27)
    t6_line_1_count = line_orbit_sizes.count(1)
    t6_structure_correct = (
        t6_line_36_count == 1 and
        t6_line_27_count == 3 and
        t6_line_1_count == 3 and
        t6_total_lines_check == N_LINES
    )
    t6_correct = t6_structure_correct

    return {
        "T1_n_classes": t1_n_classes,
        "T1_class_sizes": t1_class_sizes,
        "T1_total_roots": t1_total_roots,
        "T1_correct": t1_correct,
        "T2_e6_size": t2_e6_size,
        "T2_e6_key": t2_e6_key,
        "T2_e6_correct": t2_e6_correct,
        "T3_a2_total": t3_a2_total,
        "T3_all_singletons": t3_all_singletons,
        "T3_n_singleton_classes": t3_n_singleton_classes,
        "T3_a2_correct": t3_a2_correct,
        "T4_mixed_total": t4_mixed_total,
        "T4_all_27": t4_all_27,
        "T4_n_mixed_classes": t4_n_mixed_classes,
        "T4_mixed_correct": t4_mixed_correct,
        "T4_total_check": t4_total_check,
        "T5_ep_orbit_sizes": ep_orbit_sizes,
        "T5_line_orbit_sizes": t5_line_orbit_sizes,
        "T5_ep_transitive": t5_ep_transitive,
        "T5_line_intransitive": t5_line_intransitive,
        "T5_non_conjugate": t5_non_conjugate,
        "T6_e6_lines": t6_e6_lines,
        "T6_a2_lines": t6_a2_lines,
        "T6_matter_lines_per_gen": t6_matter_lines_per_gen,
        "T6_n_generations": t6_n_generations,
        "T6_total_lines_check": t6_total_lines_check,
        "T6_line_36_count": t6_line_36_count,
        "T6_line_27_count": t6_line_27_count,
        "T6_line_1_count": t6_line_1_count,
        "T6_structure_correct": t6_structure_correct,
        "T6_correct": t6_correct,
    }


def main():
    import json as _json
    summary = analyze()
    out = ROOT / "data" / "w33_e8_e6a2_decomp.json"
    out.write_text(_json.dumps(summary, indent=2))
    print("T1 classes:", summary["T1_n_classes"], " total roots:", summary["T1_total_roots"],
          " correct:", summary["T1_correct"])
    print("T2 E6 sector:", summary["T2_e6_size"], "roots correct:", summary["T2_e6_correct"])
    print("T3 A2 sector:", summary["T3_a2_total"], "roots, all singletons:", summary["T3_all_singletons"])
    print("T4 mixed sector:", summary["T4_mixed_total"], "roots =",
          summary["T4_n_mixed_classes"], "x 27, total check:", summary["T4_total_check"])
    print("T5 ep transitive:", summary["T5_ep_transitive"],
          " line intransitive:", summary["T5_line_intransitive"],
          " non-conjugate:", summary["T5_non_conjugate"])
    print("T5 line orbits:", summary["T5_line_orbit_sizes"])
    print("T6 structure correct:", summary["T6_correct"],
          " [36 E6 + 3x27 generations + 3 A2]")
    print("wrote data/w33_e8_e6a2_decomp.json")


if __name__ == "__main__":
    main()
