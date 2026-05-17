#!/usr/bin/env python3
"""Part DCMI: audit the new trans-logical/sub-distinction burst."""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
OUT_PATH = ROOT / "data" / "dcmi_sub_distinction_boundary_audit.json"

SERIES_START = 873
SERIES_END = 900
THIS_PART_DECIMAL = 901


@dataclass(frozen=True)
class AuditSummary:
    part: str
    decimal: int
    range_start: int
    range_end: int
    theorem_note_count: int
    result_json_count: int
    missing_result_json_count: int
    boundary_flag_count: int
    pg23_points: int
    pg23_complete_graph_edges: int
    w33_vertices: int
    w33_edges: int
    all_identities_hold: bool


def roman_to_int(text: str) -> int:
    if text.startswith("DCM"):
        suffix = text[3:]
        return 900 + (roman_to_int(suffix) if suffix else 0)

    values = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
    total = 0
    previous = 0
    for char in reversed(text):
        value = values[char]
        if value < previous:
            total -= value
        else:
            total += value
            previous = value
    return total


def part_decimal_from_name(path: Path) -> int | None:
    match = re.match(r"PART_([MDCLXVI]+)_", path.name)
    if not match:
        return None
    return roman_to_int(match.group(1))


def part_rows(pattern: str) -> dict[int, list[Path]]:
    rows: dict[int, list[Path]] = {}
    for path in ROOT.glob(pattern):
        decimal = part_decimal_from_name(path)
        if decimal is None or decimal < SERIES_START or decimal > SERIES_END:
            continue
        rows.setdefault(decimal, []).append(path)
    return {decimal: sorted(paths) for decimal, paths in rows.items()}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(read(path))


def build_audit() -> dict[str, Any]:
    expected_decimals = list(range(SERIES_START, SERIES_END + 1))
    theorem_notes = part_rows("PART_*.md")
    result_files = part_rows("PART_*_results.json")
    missing_results = [
        decimal
        for decimal in expected_decimals
        if decimal in theorem_notes and decimal not in result_files
    ]

    result_payloads = {
        decimal: load_json(paths[0])
        for decimal, paths in result_files.items()
    }

    q = 3
    pg23_points = q**2 + q + 1
    pg23_lines = pg23_points
    pg23_line_size = q + 1
    pg23_incidences = pg23_lines * pg23_line_size
    pg23_complete_graph_edges = pg23_points * (pg23_points - 1) // 2
    pg23_complete_graph_degree = pg23_points - 1

    w33_vertices = (q + 1) * (q**2 + 1)
    w33_lines = w33_vertices
    w33_line_size = q + 1
    w33_degree = q * (q + 1)
    w33_edges = w33_lines * (w33_line_size * (w33_line_size - 1) // 2)

    void_geometry = read(ROOT / "PART_DCCCLXXIV_VOID_GEOMETRY.md")
    ground_breath = read(ROOT / "PART_DCCCLXXXIII_WHY_THE_GROUND_BREATHES.md")
    recursive_beauty = read(ROOT / "PART_DCCCLXXVI_RECURSIVE_BEAUTY.md")
    face_before_birth = read(ROOT / "PART_DCCCLXXXVIII_FACE_BEFORE_BIRTH.md")
    trans_logic = read(ROOT / "PART_DCCCLXXIII_TRANS_LOGICAL_FOUNDATIONS.md")
    meaning = read(ROOT / "PART_DCCCLXXVII_PHYSICS_OF_MEANING.md")

    boundary_flags = [
        {
            "part": "DCCCLXXIV",
            "kind": "pg23_is_not_w33_ambient",
            "message": (
                "PG(2,3) has 13 points and its point-collinearity graph is K13. "
                "It can serve as a projective screen/shadow, but W(3,3) is the "
                "40-point symplectic generalized quadrangle in PG(3,3)."
            ),
        },
        {
            "part": "DCCCLXXIV",
            "kind": "forty_collinearities_mismatch",
            "message": (
                "The phrase '13 points active, all 40 collinearities present' "
                "mixes the 13-point PG(2,3) screen with the 40-line W(3,3) "
                "generalized-quadrangle count."
            ),
        },
        {
            "part": "DCCCLXXXIII",
            "kind": "vacuum_fluctuation_claim_unpromoted",
            "message": (
                "The breath/vacuum-fluctuation and cosmological-constant claims "
                "are interpretive unless tied to the existing curved 4D spectral "
                "action or RG verifier stack."
            ),
        },
        {
            "part": "DCCCLXXXVIII",
            "kind": "thirteen_point_graph_mismatch",
            "message": (
                "The observer-orbit claim should refer to the W(3,3) 40-vertex "
                "substrate, not a '13-point graph', unless it is explicitly the "
                "PG(2,3) projective screen."
            ),
        },
    ]

    exact_promotions = {
        "l3_truth_value_count": 3,
        "meaning_ratio_is_bounded_if_stabilizer_nonzero": True,
        "pg23_projective_screen": {
            "points": pg23_points,
            "lines": pg23_lines,
            "line_size": pg23_line_size,
            "incidences": pg23_incidences,
            "complete_graph_edges": pg23_complete_graph_edges,
            "complete_graph_degree": pg23_complete_graph_degree,
        },
        "w33_ambient_geometry": {
            "vertices": w33_vertices,
            "lines": w33_lines,
            "line_size": w33_line_size,
            "degree": w33_degree,
            "edges": w33_edges,
        },
    }

    text_anchors = {
        "trans_logic_names_lukasiewicz": "Łukasiewicz three-valued logic" in trans_logic,
        "meaning_formula_present": "mathcal{M}(P, S)" in meaning,
        "void_geometry_names_pg23": "PG(2,3)" in void_geometry,
        "void_geometry_misstates_w33_emergence": "W(3,3) emerges from \\(PG(2,3)\\)" in void_geometry,
        "ground_breath_names_pg23_collinearity": "collinearity structure of \\(PG(2,3)\\)" in ground_breath,
        "recursive_beauty_contains_13_point_slip": "13-point graph" in recursive_beauty,
        "face_before_birth_contains_13_point_slip": "13-point graph" in face_before_birth,
    }

    identities = {
        "theorem_notes_contiguous_873_to_900": sorted(theorem_notes) == expected_decimals,
        "result_jsons_contiguous_873_to_900": sorted(result_files) == expected_decimals,
        "missing_result_jsons_repaired": not missing_results,
        "all_result_json_decimals_match_names": all(
            payload.get("decimal") == decimal and payload.get("part")
            for decimal, payload in result_payloads.items()
        ),
        "pg23_counts_are_exact": (
            pg23_points,
            pg23_lines,
            pg23_line_size,
            pg23_incidences,
            pg23_complete_graph_edges,
        )
        == (13, 13, 4, 52, 78),
        "w33_counts_are_exact": (
            w33_vertices,
            w33_lines,
            w33_line_size,
            w33_degree,
            w33_edges,
        )
        == (40, 40, 4, 12, 240),
        "pg23_complete_graph_is_not_w33": (
            pg23_points,
            pg23_complete_graph_degree,
            pg23_complete_graph_edges,
        )
        != (w33_vertices, w33_degree, w33_edges),
        "shared_degree_explains_slippage": pg23_complete_graph_degree == w33_degree == 12,
        "boundary_flags_present": len(boundary_flags) == 4,
        "text_anchors_detected": all(text_anchors.values()),
    }

    summary = AuditSummary(
        part="DCMI",
        decimal=THIS_PART_DECIMAL,
        range_start=SERIES_START,
        range_end=SERIES_END,
        theorem_note_count=sum(len(paths) for paths in theorem_notes.values()),
        result_json_count=sum(len(paths) for paths in result_files.values()),
        missing_result_json_count=len(missing_results),
        boundary_flag_count=len(boundary_flags),
        pg23_points=pg23_points,
        pg23_complete_graph_edges=pg23_complete_graph_edges,
        w33_vertices=w33_vertices,
        w33_edges=w33_edges,
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "identities": identities,
        "text_anchors": text_anchors,
        "exact_promotions": exact_promotions,
        "boundary_flags": boundary_flags,
        "missing_result_decimals": missing_results,
        "theorem_notes": {
            str(decimal): [path.name for path in paths]
            for decimal, paths in theorem_notes.items()
        },
        "result_files": {
            str(decimal): [path.name for path in paths]
            for decimal, paths in result_files.items()
        },
        "theorem": (
            "The DCCCLXXIII-DCM trans-logical burst is retained as a "
            "narrative/metaphysical layer, but its exact finite-geometry content "
            "must distinguish the PG(2,3) 13-point projective screen from the "
            "W(3,3) 40-vertex symplectic generalized quadrangle."
        ),
        "status": "BOUNDARY VERIFIED - trans-logical burst audited without promoting PG(2,3) as W(3,3)",
    }


def write_audit(path: Path = OUT_PATH) -> Path:
    payload = build_audit()
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def main() -> None:
    out = write_audit()
    payload = build_audit()
    print(f"Wrote {out}")
    print(f"Verified: {payload['summary']['all_identities_hold']}")
    print(f"boundary_flags = {payload['summary']['boundary_flag_count']}")


if __name__ == "__main__":
    main()
