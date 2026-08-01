#!/usr/bin/env python3
"""Pass 1802 bounded Hoffman-resolution MILP falsifier.

This executable rebuilds the exact 4,860-variable model with the 405 octet
exact-eight cuts and standard nine-frame symmetry fixing.  A bounded solver run
is an experiment only: timeout, incumbent absence, or node counts are never
promoted to SAT/UNSAT evidence.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import platform
from pathlib import Path
from typing import Any

import numpy as np
import scipy
import scipy.sparse as sparse
from scipy.optimize import Bounds, LinearConstraint, milp

from w33_pass1801_1805_common import build_bockstein, build_geometry

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass1802_xor_milp_falsifier.json"


def array_hash(*arrays: np.ndarray) -> str:
    h = hashlib.sha256()
    for array in arrays:
        value = np.ascontiguousarray(array)
        h.update(str(value.dtype).encode())
        h.update(str(value.shape).encode())
        h.update(value.tobytes())
    return h.hexdigest()


def build_model() -> dict[str, Any]:
    data = build_geometry()
    bockstein = build_bockstein(data)
    M = data["M"]
    J = bockstein["J"]
    variables = 540 * 9

    rows: list[int] = []
    columns: list[int] = []
    values: list[float] = []
    rhs: list[float] = []
    row = 0

    for frame in range(540):
        for color in range(9):
            rows.append(row)
            columns.append(9 * frame + color)
            values.append(1.0)
        rhs.append(1.0)
        row += 1

    edge_frames = [np.flatnonzero(M[:, edge]) for edge in range(240)]
    for edge in range(240):
        for color in range(9):
            for frame in edge_frames[edge]:
                rows.append(row)
                columns.append(9 * int(frame) + color)
                values.append(1.0)
            rhs.append(1.0)
            row += 1

    for octet in range(45):
        frames = np.flatnonzero(J[:, octet])
        assert len(frames) == 72
        for color in range(9):
            for frame in frames:
                rows.append(row)
                columns.append(9 * int(frame) + color)
                values.append(1.0)
            rhs.append(8.0)
            row += 1

    A = sparse.csr_matrix(
        (values, (rows, columns)), shape=(row, variables), dtype=np.float64
    )
    b = np.array(rhs, dtype=np.float64)

    lower = np.zeros(variables, dtype=np.float64)
    upper = np.ones(variables, dtype=np.float64)
    fixed_variables: list[int] = []
    for color, frame in enumerate(edge_frames[0]):
        frame = int(frame)
        for other in range(9):
            upper[9 * frame + other] = 0.0
        variable = 9 * frame + color
        lower[variable] = upper[variable] = 1.0
        fixed_variables.append(variable)

    model_hash = array_hash(
        A.indptr.astype(np.int64),
        A.indices.astype(np.int64),
        A.data,
        b,
        lower,
        upper,
    )
    return {
        "A": A,
        "b": b,
        "lower": lower,
        "upper": upper,
        "M": M,
        "J": J,
        "fixed_variables": fixed_variables,
        "model": {
            "variables": variables,
            "binary_variables": variables,
            "equality_constraints": row,
            "frame_color_equations": 540,
            "edge_color_equations": 240 * 9,
            "octet_exact8_equations": 45 * 9,
            "symmetry_fixed_variables": 9,
            "matrix_nnz": int(A.nnz),
            "model_sha256": model_hash,
        },
    }


def solve(time_limit: float) -> dict[str, Any]:
    model = build_model()
    variables = model["model"]["variables"]
    result = milp(
        np.zeros(variables, dtype=np.float64),
        integrality=np.ones(variables, dtype=np.int8),
        bounds=Bounds(model["lower"], model["upper"]),
        constraints=LinearConstraint(model["A"], model["b"], model["b"]),
        options={"time_limit": float(time_limit), "presolve": True, "mip_rel_gap": 0.0},
    )

    incumbent = result.x is not None
    validation: dict[str, Any] | None = None
    if incumbent:
        rounded = np.rint(result.x).astype(np.int8).reshape(540, 9)
        validation = {
            "maximum_integrality_error": float(
                np.max(np.abs(result.x - np.rint(result.x)))
            ),
            "frame_sums": sorted(set(map(int, rounded.sum(axis=1)))),
            "edge_color_sums": sorted(
                set(map(int, (model["M"].T @ rounded).reshape(-1)))
            ),
            "octet_color_sums": sorted(
                set(map(int, (model["J"].T @ rounded).reshape(-1)))
            ),
        }

    payload = {
        "schema": "w33.pass1802.xor_milp_falsifier.v1",
        "status": "BOUNDED_EXPERIMENT",
        "model": model["model"],
        "solver": {
            "engine": "scipy.optimize.milp / HiGHS",
            "python": platform.python_version(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "time_limit_seconds": float(time_limit),
            "status_code": int(result.status),
            "message": str(result.message),
            "has_incumbent": bool(incumbent),
            "mip_node_count": (
                None
                if getattr(result, "mip_node_count", None) is None
                else int(result.mip_node_count)
            ),
            "mip_gap": (
                None
                if getattr(result, "mip_gap", None) is None
                else float(result.mip_gap)
            ),
        },
        "incumbent_validation": validation,
        "evidence_boundary": (
            "This is a bounded solver falsifier. A timeout, absent incumbent, or "
            "solver progress statistic is not a SAT or UNSAT certificate."
        ),
    }
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUT)
    parser.add_argument("--time-limit", type=float, default=20.0)
    parser.add_argument("--solve", action="store_true")
    parser.add_argument("--check-structure", action="store_true")
    args = parser.parse_args()

    if args.solve:
        payload = solve(args.time_limit)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n"
        )
        print(json.dumps(payload["solver"], sort_keys=True))
        return 0

    structural = build_model()["model"]
    if args.check_structure:
        frozen = json.loads(args.output.read_text())
        if frozen["model"] != structural:
            raise SystemExit("Pass 1802 MILP model drift")
    print(json.dumps(structural, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
