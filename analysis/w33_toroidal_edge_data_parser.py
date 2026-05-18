#!/usr/bin/env python3
"""Parse toroidal Csaszar/Szilassi realization edge-data from repo text.

The realization/edge data is bundled in

    data/Toroidal-Polyhedra-Realizations.txt

rather than being only in the coordinate PDF.  This parser extracts the edge
length class counts and multiplicities for all seven known 3D realizations:

    Csaszar: 5 realizations, edge-type counts 10,9,9,8,9
    Szilassi: 2 realizations, edge-type counts 12,11

and writes a clean JSON ledger to

    data/w33_toroidal_edge_data_bridge.json

This makes the edge-spectrum layer directly consumable by later W33/TQC
scripts instead of relying on hard-coded constants in exploratory notebooks.
"""
from __future__ import annotations

import json
import math
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REALIZATION_PATH = ROOT / "data" / "Toroidal-Polyhedra-Realizations.txt"
OUTPUT_PATH = ROOT / "data" / "w33_toroidal_edge_data_bridge.json"

Q = 3
LAMBDA = 2
MU = 4
F = 24
PHI4 = Q * Q + 1
PHI6 = Q * Q - Q + 1
H1 = Q ** (Q + 1)


@dataclass(frozen=True)
class EdgeClass:
    index: int
    multiplicity: int
    expression: str
    approx: float | None


@dataclass(frozen=True)
class RealizationEdgeSpectrum:
    family: str
    version: int
    declared_edges: int
    declared_edge_type_count: int
    parsed_edge_type_count: int
    multiplicity_sum: int
    edge_classes: list[EdgeClass]


def _safe_eval_expression(expr: str, env: dict[str, float] | None = None) -> float | None:
    """Evaluate simple numeric/sqrt expressions from the source text.

    Returns None when the expression intentionally contains exact symbolic data
    that this lightweight parser should preserve but not evaluate.
    """
    if env is None:
        env = {}
    cleaned = (
        expr.replace("−", "-")
        .replace("–", "-")
        .replace("^", "**")
        .replace("sqrt", "math.sqrt")
        .strip()
    )
    cleaned = cleaned.split("≈")[0].strip()
    try:
        return float(eval(cleaned, {"__builtins__": {}}, {"math": math, **env}))
    except Exception:
        return None


def _split_blocks(text: str) -> list[tuple[str, int, str]]:
    header = re.compile(r"^(Csaszar|Szilassi) Polyhedron \(version (\d+)\)$", re.MULTILINE)
    matches = list(header.finditer(text))
    blocks: list[tuple[str, int, str]] = []
    for idx, match in enumerate(matches):
        start = match.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        blocks.append((match.group(1), int(match.group(2)), text[start:end]))
    return blocks


def parse_edge_spectra(path: Path = REALIZATION_PATH) -> list[RealizationEdgeSpectrum]:
    text = path.read_text(encoding="utf-8")
    spectra: list[RealizationEdgeSpectrum] = []

    for family, version, block in _split_blocks(text):
        edge_header = re.search(r"Edges:\s*(\d+)\s*\((\d+)\s+different lengths\)", block)
        if edge_header is None:
            raise ValueError(f"Missing edge header for {family} version {version}")
        declared_edges = int(edge_header.group(1))
        declared_edge_type_count = int(edge_header.group(2))

        env: dict[str, float] = {}
        for assignment in re.finditer(r"^(C\d+)\s*=\s*([^\n]+)$", block, re.MULTILINE):
            key = assignment.group(1)
            rhs = assignment.group(2).split("=")[-1].strip()
            val = _safe_eval_expression(rhs, env)
            if val is not None:
                env[key] = val

        edge_classes: list[EdgeClass] = []
        for line in block.splitlines():
            stripped = line.strip()
            edge_match = re.match(r"Edge\s+(\d+)\s+\((\d+)\):\s*(.+)$", stripped)
            if edge_match is None:
                continue
            index = int(edge_match.group(1))
            multiplicity = int(edge_match.group(2))
            rest = edge_match.group(3).strip()
            expression = rest.split("≈")[0].strip()
            approx = None
            if "≈" in rest:
                approx_text = rest.split("≈", 1)[1].strip().split()[0]
                try:
                    approx = float(approx_text)
                except Exception:
                    approx = _safe_eval_expression(expression, env)
            else:
                approx = _safe_eval_expression(expression, env)
            edge_classes.append(EdgeClass(index, multiplicity, expression, approx))

        spectra.append(
            RealizationEdgeSpectrum(
                family=family,
                version=version,
                declared_edges=declared_edges,
                declared_edge_type_count=declared_edge_type_count,
                parsed_edge_type_count=len(edge_classes),
                multiplicity_sum=sum(edge.multiplicity for edge in edge_classes),
                edge_classes=edge_classes,
            )
        )
    return spectra


def build_payload() -> dict[str, Any]:
    spectra = parse_edge_spectra()
    counts = [s.declared_edge_type_count for s in spectra]
    csaszar = [s for s in spectra if s.family == "Csaszar"]
    szilassi = [s for s in spectra if s.family == "Szilassi"]
    cs_counts = [s.declared_edge_type_count for s in csaszar]
    sz_counts = [s.declared_edge_type_count for s in szilassi]

    cs_sum = sum(cs_counts)
    sz_sum = sum(sz_counts)
    total_sum = sum(counts)

    identities = {
        "seven_realizations": len(spectra) == PHI6 == 7,
        "five_plus_two": len(csaszar) == Q + LAMBDA == 5 and len(szilassi) == LAMBDA == 2,
        "all_have_21_edges": all(s.declared_edges == 21 and s.multiplicity_sum == 21 for s in spectra),
        "edge_type_counts": counts == [10, 9, 9, 8, 9, 12, 11],
        "csaszar_sum_45": cs_sum == math.comb(PHI4, 2) == 45,
        "szilassi_sum_23": sz_sum == F - 1 == 23,
        "total_sum_68": total_sum == MU * 17 == 68,
        "distinct_counts_mod12": sorted({c % 12 for c in counts}) == [8, 9, 10, 11, 0],
    }

    return {
        "summary": {
            "source": str(REALIZATION_PATH.relative_to(ROOT)),
            "realization_count": len(spectra),
            "edge_type_counts": counts,
            "csaszar_edge_type_counts": cs_counts,
            "szilassi_edge_type_counts": sz_counts,
            "csaszar_sum": cs_sum,
            "szilassi_sum": sz_sum,
            "total_sum": total_sum,
            "all_identities_hold": all(identities.values()),
        },
        "spectra": [
            {
                **{k: v for k, v in asdict(spectrum).items() if k != "edge_classes"},
                "edge_classes": [asdict(edge_class) for edge_class in spectrum.edge_classes],
            }
            for spectrum in spectra
        ],
        "closed_forms": {
            "realization_packet": "5 Csaszar + 2 Szilassi = 7 = Phi6",
            "all_edge_multiplicities": "Every realization has 21 edge instances",
            "csaszar_edge_type_sum": "10+9+9+8+9 = 45 = C(Phi4,2) = C(10,2)",
            "szilassi_edge_type_sum": "12+11 = 23 = f-1 = 24-1",
            "total_edge_type_sum": "45+23 = 68 = 4*17",
            "mod12_edge_type_packet": "edge-type counts occupy residues 8,9,10,11,0 mod 12 across the heptad",
        },
        "identities": identities,
        "theorem": (
            "Toroidal Edge-Data Ledger Theorem.  The repo's bundled toroidal "
            "realization text contains a seven-realization edge spectrum with "
            "edge-type counts 10,9,9,8,9,12,11.  The five Csaszar counts sum "
            "to 45=C(Phi4,2), the two Szilassi counts sum to 23=f-1, and "
            "all seven edge-type counts sum to 68=4*17.  Each realization still "
            "has 21 actual edge instances, so this is a metric-spectrum layer, "
            "not a combinatorial edge-count layer."
        ),
        "honesty_boundary": "This parser extracts the edge metadata present in the repo text. It does not claim that edge-type counts alone determine dynamics or physical observables.",
    }


def main() -> None:
    payload = build_payload()
    OUTPUT_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(payload["summary"], indent=2, sort_keys=True))
    print(f"wrote {OUTPUT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
