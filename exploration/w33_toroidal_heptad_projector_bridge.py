"""Operator heptad from the seven toroidal realizations.

The raw toroidal realization file contains seven concrete Euclidean models:

    - 5 Csaszar realizations of the K7 torus triangulation,
    - 2 Szilassi realizations of the Heawood-dual torus.

The user hint was the right one: these are not just seven pictures.  Taking
the seven centered vertex/face-centroid shells and passing to their rank-3
projectors inside R^7 produces an exact operator heptad.  The heptad has the
same rigid packet counts that already appeared elsewhere in the repo:

    7 = 1 + 6  and  12 = 2 * 6.

This bridge proves the exact operator side of that statement:

    - all seven realizations produce rank-3 shell projectors;
    - the seven projectors are linearly independent, so they span a 7D heptad;
    - after subtracting the mean projector, the nontrivial shell is exactly 6D;
    - the 5 Csaszar and 2 Szilassi families keep their exact 5+2 span split;
    - the 6D centered shell matches the 6 undirected tetrahedral bridges;
    - the toroidal genus numerator 12 is the orientation double cover of that
      6D shell.

The geometric upshot is that the local Clifford packet wants to live on the
bivector/edge shell, not on a single realization chart.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
import math
import re
from pathlib import Path
import sys
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from exploration.w33_tetrahedral_chart_oscillator_bridge import build_summary as build_tetrahedral_summary
from exploration.w33_toroidal_genus_fourier_bridge import build_summary as build_genus_summary


REALIZATION_PATH = ROOT / "data" / "Toroidal-Polyhedra-Realizations.txt"
DEFAULT_OUTPUT_PATH = ROOT / "data" / "w33_toroidal_heptad_projector_bridge_summary.json"


@dataclass(frozen=True)
class GeometricRealization:
    family: str
    version: int
    shell_points: np.ndarray


def _safe_eval(expr: str, env: dict[str, float]) -> float:
    expression = expr.replace("^", "**").replace("sqrt", "math.sqrt")
    return float(eval(expression, {"__builtins__": {}}, {"math": math, **env}))


def _parse_realization_blocks(path: Path = REALIZATION_PATH) -> list[tuple[str, int, list[str]]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    header_re = re.compile(r"^(Csaszar|Szilassi) Polyhedron \(version (\d+)\)$")

    blocks: list[tuple[str, int, list[str]]] = []
    index = 0
    while index < len(lines):
        header = header_re.match(lines[index].strip())
        if header is None:
            index += 1
            continue

        family = header.group(1)
        version = int(header.group(2))
        block: list[str] = []
        index += 1
        while index < len(lines) and header_re.match(lines[index].strip()) is None:
            block.append(lines[index])
            index += 1
        blocks.append((family, version, block))

    return blocks


def _parse_geometric_realizations(path: Path = REALIZATION_PATH) -> list[GeometricRealization]:
    realizations: list[GeometricRealization] = []
    for family, version, block in _parse_realization_blocks(path):
        env: dict[str, float] = {}
        # Version 3 omits the explicit C0 assignment in the source file, but the
        # coordinate pattern and listed edge lengths fix it to 6*sqrt(2).
        if family == "Csaszar" and version == 3:
            env["C0"] = 6.0 * math.sqrt(2.0)

        vertices: list[list[float]] = []
        faces: list[tuple[int, ...]] = []

        for line in block:
            stripped = line.strip()
            if stripped.startswith("C") and "=" in stripped and not stripped.startswith("Cs"):
                key, rest = stripped.split("=", 1)
                rhs = rest.split("≈")[0].strip()
                if "=" in rhs:
                    rhs = rhs.split("=", 1)[1].strip()
                env[key.strip()] = _safe_eval(rhs, env)
                continue

            if stripped.startswith("V") and "=" in stripped:
                _, rest = stripped.split("=", 1)
                tokens = [token.strip() for token in rest.strip()[1:-1].split(",")]
                coordinates = []
                for token in tokens:
                    if re.fullmatch(r"[-+]?\d+(?:\.\d*)?", token):
                        coordinates.append(float(token))
                    else:
                        coordinates.append(_safe_eval(token, env))
                vertices.append(coordinates)
                continue

            if stripped.startswith("{"):
                faces.append(tuple(int(token) for token in re.findall(r"-?\d+", stripped)))

        vertex_array = np.asarray(vertices, dtype=float)
        if family == "Csaszar":
            shell_points = vertex_array
        else:
            shell_points = np.asarray(
                [vertex_array[list(face)].mean(axis=0) for face in faces],
                dtype=float,
            )
        shell_points = shell_points - shell_points.mean(axis=0, keepdims=True)
        realizations.append(
            GeometricRealization(
                family=family,
                version=version,
                shell_points=shell_points,
            )
        )

    return realizations


def _orthoprojector(shell_points: np.ndarray) -> np.ndarray:
    q, _ = np.linalg.qr(shell_points)
    return q @ np.conjugate(q).T


def _matrix_span_rank(matrices: list[np.ndarray]) -> int:
    flattened = np.stack([matrix.reshape(-1) for matrix in matrices], axis=1)
    return int(np.linalg.matrix_rank(flattened, tol=1e-10))


def build_summary() -> dict[str, Any]:
    realizations = _parse_geometric_realizations()
    labels = [f"{realization.family[0]}{realization.version}" for realization in realizations]
    projectors = [_orthoprojector(realization.shell_points) for realization in realizations]
    mean_projector = sum(projectors) / len(projectors)
    centered_projectors = [projector - mean_projector for projector in projectors]

    csaszar_projectors = [
        projector
        for realization, projector in zip(realizations, projectors)
        if realization.family == "Csaszar"
    ]
    szilassi_projectors = [
        projector
        for realization, projector in zip(realizations, projectors)
        if realization.family == "Szilassi"
    ]

    all_span_rank = _matrix_span_rank(projectors)
    centered_span_rank = _matrix_span_rank(centered_projectors)
    csaszar_span_rank = _matrix_span_rank(csaszar_projectors)
    szilassi_span_rank = _matrix_span_rank(szilassi_projectors)

    overlap_matrix = np.array(
        [[float(np.trace(left @ right).real) for right in projectors] for left in projectors],
        dtype=float,
    )
    centered_gram = np.array(
        [
            [
                float(np.vdot(left.reshape(-1), right.reshape(-1)).real)
                for right in centered_projectors
            ]
            for left in centered_projectors
        ],
        dtype=float,
    )

    tetrahedral = build_tetrahedral_summary()
    genus = build_genus_summary()
    undirected_bridge_count = tetrahedral["edge_transition_packet"]["undirected_edge_count"]
    directed_bridge_count = tetrahedral["edge_transition_packet"]["directed_edge_count"]
    genus_numerator = genus["genus_dictionary"]["primal_numerator_at_phi6"]

    csaszar_centered_rank = _matrix_span_rank(
        [
            projector - sum(csaszar_projectors) / len(csaszar_projectors)
            for projector in csaszar_projectors
        ]
    )
    szilassi_centered_rank = _matrix_span_rank(
        [
            projector - sum(szilassi_projectors) / len(szilassi_projectors)
            for projector in szilassi_projectors
        ]
    )
    csaszar_mean = sum(csaszar_projectors) / len(csaszar_projectors)
    szilassi_mean = sum(szilassi_projectors) / len(szilassi_projectors)
    family_separation = csaszar_mean - szilassi_mean
    centered_4_plus_1_plus_1_rank = _matrix_span_rank(
        [projector - csaszar_mean for projector in csaszar_projectors]
        + [projector - szilassi_mean for projector in szilassi_projectors]
        + [family_separation]
    )
    full_4_plus_3_rank = _matrix_span_rank(
        [projector - csaszar_mean for projector in csaszar_projectors]
        + [projector - szilassi_mean for projector in szilassi_projectors]
        + [family_separation, mean_projector]
    )

    summary: dict[str, Any] = {
        "realization_packet": {
            "labels": labels,
            "count": len(realizations),
            "families": {"Csaszar": len(csaszar_projectors), "Szilassi": len(szilassi_projectors)},
            "rank_per_realization": {
                label: int(np.linalg.matrix_rank(realization.shell_points, tol=1e-10))
                for label, realization in zip(labels, realizations)
            },
        },
        "projector_heptad": {
            "all_span_rank": all_span_rank,
            "centered_span_rank": centered_span_rank,
            "csaszar_span_rank": csaszar_span_rank,
            "szilassi_span_rank": szilassi_span_rank,
            "csaszar_centered_rank": csaszar_centered_rank,
            "szilassi_centered_rank": szilassi_centered_rank,
            "family_separation_rank": _matrix_span_rank([family_separation]),
            "centered_4_plus_1_plus_1_rank": centered_4_plus_1_plus_1_rank,
            "full_4_plus_3_rank": full_4_plus_3_rank,
            "mean_projector_trace": float(np.trace(mean_projector).real),
            "mean_projector_eigenvalues": [float(value) for value in np.linalg.eigvalsh(mean_projector)],
            "centered_gram_eigenvalues": [float(value) for value in np.linalg.eigvalsh(centered_gram)],
            "projector_overlap_matrix": overlap_matrix.tolist(),
        },
        "dictionary": {
            "phi6_realization_count": len(realizations),
            "centered_shell_dimension": centered_span_rank,
            "undirected_tetrahedral_bridge_count": undirected_bridge_count,
            "directed_tetrahedral_bridge_count": directed_bridge_count,
            "toroidal_genus_numerator": genus_numerator,
            "tetrahedral_bivector_dimension": math.comb(4, 2),
        },
        "toroidal_heptad_theorem": {
            "all_seven_realizations_define_rank_three_shell_projectors": all(
                int(np.linalg.matrix_rank(realization.shell_points, tol=1e-10)) == 3
                for realization in realizations
            ),
            "the_seven_realizations_span_an_exact_operator_heptad": all_span_rank == len(realizations),
            "subtracting_the_mean_projector_leaves_an_exact_six_dimensional_shell": centered_span_rank == 6,
            "the_five_csaszar_realizations_span_a_five_dimensional_family_shell": csaszar_span_rank == 5,
            "the_two_szilassi_realizations_span_a_two_dimensional_family_shell": szilassi_span_rank == 2,
            "the_centered_shell_refines_exactly_as_four_plus_one_plus_one": (
                csaszar_centered_rank == 4
                and szilassi_centered_rank == 1
                and centered_4_plus_1_plus_1_rank == centered_span_rank == 6
            ),
            "the_full_heptad_refines_exactly_as_four_plus_three": full_4_plus_3_rank == 7,
            "the_centered_heptad_shell_matches_the_six_undirected_tetrahedral_bridges": (
                centered_span_rank == undirected_bridge_count
            ),
            "the_centered_heptad_shell_matches_the_dimension_of_bivectors_in_four_dimensions": (
                centered_span_rank == math.comb(4, 2)
            ),
            "the_toroidal_genus_numerator_is_the_orientation_double_cover_of_the_centered_shell": (
                genus_numerator == 2 * centered_span_rank == directed_bridge_count
            ),
            "phi6_counts_both_the_realization_heptad_and_the_full_projector_span": (
                len(realizations) == all_span_rank == genus["genus_dictionary"]["phi6"]
            ),
        },
        "interpretation": (
            "The actual seven toroidal realizations carry an operator heptad, not just seven pictures. "
            "Their centered projector shell is exactly six-dimensional, which matches both the six "
            "undirected tetrahedral bridges and the six-dimensional bivector shell of a four-chart "
            "Clifford packet. The genus numerator 12 is then the oriented double cover of that shell. "
            "Even better, the heptad now carries both exact packet splits already hinted at elsewhere "
            "in the repo: 7 = 1 + 6 from mean plus centered shell, and 7 = 4 + 3 from the decomposition "
            "into a 4D Csaszar internal shell, a 1D Szilassi internal mode, a 1D primal-dual separation "
            "mode, and the scalar mean line."
        ),
    }
    return summary


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary["toroidal_heptad_theorem"], indent=2))


if __name__ == "__main__":
    main()
