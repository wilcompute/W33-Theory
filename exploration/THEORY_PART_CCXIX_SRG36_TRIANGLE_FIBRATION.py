#!/usr/bin/env python3
"""Pillar 119 (Part CCXIX): SRG36 Triangle Fibration over W33 Lines

The SRG(36,20,10,12) contains 1200 triangles, of which 120 are chosen as
'faces' (with holonomy 1 under a natural flat metric).  The remaining 1080
split into 240 odd non-faces (holonomy 1) and 840 even non-faces (holonomy 0).
The 240 odd non-faces fiber over 40 special faces with fiber size exactly 6.
The 40 special faces correspond bijectively to the 40 W33 lines, giving each
W33 line a canonical SRG triangle representative.  Every face (special or
ordinary) has exactly 10 preimages under the fibration map.  Special faces
have profile (6 odd + 3 even + 1 self) and ordinary faces have (0 odd + 9
even + 1 self).

Theorems:

T1  1200 SRG TRIANGLES: The SRG(36,20,10,12) contains 1200 triangles in
    total.  Of these: 120 are chosen as canonical faces, 240 are odd non-faces
    (holonomy 1), and 840 are even non-faces (holonomy 0).  Both chosen faces
    and odd non-faces carry holonomy 1; even non-faces carry holonomy 0.

T2  240 ODD NON-FACES FIBER OVER 40 SPECIAL FACES: The 240 odd non-face
    triangles fiber over exactly 40 special faces with fiber size exactly 6.
    Each odd non-face triangle maps to 3 face-images (one per edge); the 40
    special faces are the unique faces receiving at least one odd non-face
    preimage.  So 40 * 6 = 240 fibers.

T3  40 SPECIAL FACES = 40 W33 LINES: The 40 special faces correspond
    bijectively to the 40 W33 lines (projective lines of W(3,3)).  Each W33
    line contributes exactly one special face; ordinary faces are not
    associated with any single line.  Special faces have line_id unique and
    exhausting all 40 line ids.

T4  FACE PREIMAGE MAP HAS DEGREE 10: Every face (of the 120 chosen) has
    exactly 10 preimages under the fibration map.  All 120 faces have
    total_preimages = 10.

T5  SPECIAL FACE PROFILE (6+3+1): Each special face has:
    - 6 odd non-face preimages
    - 3 even non-face preimages
    - 1 self (the face itself)
    Total: 10.  All 40 special faces share this profile.

T6  ORDINARY FACE PROFILE (0+9+1): Each ordinary face has:
    - 0 odd non-face preimages
    - 9 even non-face preimages
    - 1 self (the face itself)
    Total: 10.  All 80 ordinary faces share this profile.
    The split: 40 special + 80 ordinary = 120 total faces.
"""

from __future__ import annotations

import csv
import io
import json
import zipfile
from collections import Counter
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parent
BUNDLE_NAME = "TOE_srg36_triangle_fibration_240_v01_20260227_bundle.zip"
BUNDLE_CANDIDATES = (
    ROOT / BUNDLE_NAME,
    REPO_ROOT / "archive" / "zip" / BUNDLE_NAME,
)
PREFIX = "TOE_srg36_triangle_fibration_240_v01_20260227/"

N_TRIANGLES = 1200
N_FACES = 120
N_ODD_NONFACE = 240
N_EVEN_NONFACE = 840
N_SPECIAL_FACES = 40
N_ORDINARY_FACES = 80
FIBER_SIZE = 6  # 240 / 40 = 6
PREIMAGE_DEGREE = 10  # each face has 10 preimages
SPECIAL_ODD = 6
SPECIAL_EVEN = 3
ORDINARY_ODD = 0
ORDINARY_EVEN = 9


def _load_bundle() -> dict:
    for path in BUNDLE_CANDIDATES:
        if path.exists():
            bundle = path
            break
    else:
        raise FileNotFoundError(
            "SRG36 triangle fibration bundle missing from "
            + ", ".join(str(path) for path in BUNDLE_CANDIDATES)
        )

    with zipfile.ZipFile(bundle) as zf:
        summary = json.loads(zf.read(PREFIX + "SUMMARY.json"))
        odd_raw = zf.read(PREFIX + "odd_nonface_triangles_240.csv").decode("utf-8")
        special_raw = zf.read(PREFIX + "special_faces_40.csv").decode("utf-8")
        preimage_raw = zf.read(PREFIX + "face_preimage_counts_120.csv").decode("utf-8")
    return {
        "summary": summary,
        "odd_rows": list(csv.DictReader(io.StringIO(odd_raw))),
        "special_rows": list(csv.DictReader(io.StringIO(special_raw))),
        "preimage_rows": list(csv.DictReader(io.StringIO(preimage_raw))),
    }


def analyze() -> dict:
    data = _load_bundle()
    summary = data["summary"]
    odd_rows = data["odd_rows"]
    special_rows = data["special_rows"]
    preimage_rows = data["preimage_rows"]

    # T1: 1200 triangles split as 120 + 240 + 840
    t1_triangles_total = summary["triangles_total"]
    t1_faces_chosen = summary["faces_chosen"]
    hol_counts = summary["holonomy_counts"]
    t1_chosen_hol1 = hol_counts.get("chosen_faces_hol1", 0)
    t1_nonface_hol1 = hol_counts.get("nonface_hol1", 0)
    t1_nonface_hol0 = hol_counts.get("nonface_hol0", 0)
    t1_correct = (
        t1_triangles_total == N_TRIANGLES
        and t1_faces_chosen == N_FACES
        and t1_chosen_hol1 == N_FACES
        and t1_nonface_hol1 == N_ODD_NONFACE
        and t1_nonface_hol0 == N_EVEN_NONFACE
        and t1_nonface_hol1 + t1_nonface_hol0 + t1_chosen_hol1 == N_TRIANGLES
    )

    # T2: 240 odd non-faces fiber over 40 special faces
    t2_n_odd = len(odd_rows)
    # Each odd nonface carries a line_id; 6 odd nonfaces share each line_id
    line_id_counts = Counter(int(r["line_id"]) for r in odd_rows)
    t2_n_special = len(line_id_counts)  # 40 distinct line_ids
    t2_all_fiber_size_6 = all(v == FIBER_SIZE for v in line_id_counts.values())
    t2_fiber_size = FIBER_SIZE if t2_all_fiber_size_6 else 0
    t2_correct = (
        t2_n_odd == N_ODD_NONFACE
        and t2_n_special == N_SPECIAL_FACES
        and t2_all_fiber_size_6
    )

    # T3: 40 special faces = 40 W33 lines
    t3_n_special = len(special_rows)
    # Each special face has a unique line_id
    line_ids = sorted(int(r["line_id"]) for r in special_rows)
    t3_line_ids_unique = len(set(line_ids)) == t3_n_special
    t3_line_ids_range = min(line_ids) == 0 and max(line_ids) == 39
    t3_all_lines_covered = set(line_ids) == set(range(N_SPECIAL_FACES))
    t3_correct = (
        t3_n_special == N_SPECIAL_FACES and t3_line_ids_unique and t3_all_lines_covered
    )

    # T4: Face preimage map has degree 10
    preimage_counts = [int(r["total_preimages"]) for r in preimage_rows]
    t4_n_faces = len(preimage_rows)
    t4_all_degree_10 = all(c == PREIMAGE_DEGREE for c in preimage_counts)
    t4_preimage_dist = dict(Counter(preimage_counts))
    t4_correct = t4_n_faces == N_FACES and t4_all_degree_10

    # T5: Special face profile (6 odd + 3 even + 1 self)
    special_profiles = [
        (int(r["odd_nonface_preimages"]), int(r["even_nonface_preimages"]), 1)  # self
        for r in preimage_rows
        if int(r["odd_nonface_preimages"]) > 0
    ]
    t5_n_special = len(special_profiles)
    t5_all_odd_6 = all(p[0] == SPECIAL_ODD for p in special_profiles)
    t5_all_even_3 = all(p[1] == SPECIAL_EVEN for p in special_profiles)
    t5_all_total_10 = all(
        p[0] + p[1] + p[2] == PREIMAGE_DEGREE for p in special_profiles
    )
    t5_correct = (
        t5_n_special == N_SPECIAL_FACES
        and t5_all_odd_6
        and t5_all_even_3
        and t5_all_total_10
    )

    # T6: Ordinary face profile (0 odd + 9 even + 1 self)
    ordinary_profiles = [
        (int(r["odd_nonface_preimages"]), int(r["even_nonface_preimages"]), 1)  # self
        for r in preimage_rows
        if int(r["odd_nonface_preimages"]) == 0
    ]
    t6_n_ordinary = len(ordinary_profiles)
    t6_all_odd_0 = all(p[0] == ORDINARY_ODD for p in ordinary_profiles)
    t6_all_even_9 = all(p[1] == ORDINARY_EVEN for p in ordinary_profiles)
    t6_all_total_10 = all(
        p[0] + p[1] + p[2] == PREIMAGE_DEGREE for p in ordinary_profiles
    )
    t6_special_plus_ordinary = t5_n_special + t6_n_ordinary
    t6_correct = (
        t6_n_ordinary == N_ORDINARY_FACES
        and t6_all_odd_0
        and t6_all_even_9
        and t6_all_total_10
        and t6_special_plus_ordinary == N_FACES
    )

    return {
        # T1
        "T1_triangles_total": t1_triangles_total,
        "T1_faces_chosen": t1_faces_chosen,
        "T1_chosen_hol1": t1_chosen_hol1,
        "T1_nonface_hol1": t1_nonface_hol1,
        "T1_nonface_hol0": t1_nonface_hol0,
        "T1_correct": t1_correct,
        # T2
        "T2_n_odd": t2_n_odd,
        "T2_n_special": t2_n_special,
        "T2_fiber_size": t2_fiber_size,
        "T2_all_fiber_size_6": t2_all_fiber_size_6,
        "T2_correct": t2_correct,
        # T3
        "T3_n_special": t3_n_special,
        "T3_line_ids_unique": t3_line_ids_unique,
        "T3_all_lines_covered": t3_all_lines_covered,
        "T3_correct": t3_correct,
        # T4
        "T4_n_faces": t4_n_faces,
        "T4_all_degree_10": t4_all_degree_10,
        "T4_preimage_dist": t4_preimage_dist,
        "T4_correct": t4_correct,
        # T5
        "T5_n_special": t5_n_special,
        "T5_all_odd_6": t5_all_odd_6,
        "T5_all_even_3": t5_all_even_3,
        "T5_all_total_10": t5_all_total_10,
        "T5_correct": t5_correct,
        # T6
        "T6_n_ordinary": t6_n_ordinary,
        "T6_all_odd_0": t6_all_odd_0,
        "T6_all_even_9": t6_all_even_9,
        "T6_all_total_10": t6_all_total_10,
        "T6_special_plus_ordinary": t6_special_plus_ordinary,
        "T6_correct": t6_correct,
    }


def main():
    import json as _json

    summary = analyze()
    out = ROOT / "data" / "w33_srg36_triangle_fibration.json"
    out.write_text(_json.dumps(summary, indent=2))
    print(
        "T1 triangles: total=%d faces=%d odd_nonface=%d even_nonface=%d correct:%s"
        % (
            summary["T1_triangles_total"],
            summary["T1_faces_chosen"],
            summary["T1_nonface_hol1"],
            summary["T1_nonface_hol0"],
            summary["T1_correct"],
        )
    )
    print(
        "T2 fibration: odd=%d special=%d fiber_size=%d correct:%s"
        % (
            summary["T2_n_odd"],
            summary["T2_n_special"],
            summary["T2_fiber_size"],
            summary["T2_correct"],
        )
    )
    print(
        "T3 special=lines: n=%d unique=%s covered=%s correct:%s"
        % (
            summary["T3_n_special"],
            summary["T3_line_ids_unique"],
            summary["T3_all_lines_covered"],
            summary["T3_correct"],
        )
    )
    print(
        "T4 degree-10 map: faces=%d all_10=%s correct:%s"
        % (summary["T4_n_faces"], summary["T4_all_degree_10"], summary["T4_correct"])
    )
    print(
        "T5 special profile (6+3+1): n=%d odd6=%s even3=%s correct:%s"
        % (
            summary["T5_n_special"],
            summary["T5_all_odd_6"],
            summary["T5_all_even_3"],
            summary["T5_correct"],
        )
    )
    print(
        "T6 ordinary profile (0+9+1): n=%d odd0=%s even9=%s total=%d correct:%s"
        % (
            summary["T6_n_ordinary"],
            summary["T6_all_odd_0"],
            summary["T6_all_even_9"],
            summary["T6_special_plus_ordinary"],
            summary["T6_correct"],
        )
    )
    print("wrote data/w33_srg36_triangle_fibration.json")


if __name__ == "__main__":
    main()
