#!/usr/bin/env python3
"""Pass 2309: exact nonlinear-signature feasibility test for a nine-cover resolution.

The model is a necessary quotient of the full frame-disjointness problem.  It asks
whether nine globally realizable Pass-1825 signature vectors can sum to the
uniform octet capacity 12*1_45.  A negative CP-SAT result rules out chi(H)=9;
a positive result is only a signature skeleton and must be lifted to compatible
frame covers.
"""
from __future__ import annotations

import argparse
import base64
import gzip
import hashlib
import json
from pathlib import Path

from ortools.sat.python import cp_model

ROOT = Path(__file__).resolve().parents[1]
SIGNATURES = ROOT / "data" / "w33_pass1825_signatures720.json.gz.b64"
CERTIFICATE = ROOT / "data" / "w33_pass1821_1825_complete_cover_signature.json"
DEFAULT_OUT = ROOT / "data" / "w33_pass2309_signature_resolution_solver.json"
EXPECTED_SIGNATURE_SHA256 = "5c3e60271e6108b8df1537b59416b008f3cd4d40cf7a14a5f1b1d90150cc3304"


def canonical_sha256(value: object) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def load_inputs() -> tuple[list[list[int]], list[int], dict]:
    cert = json.loads(CERTIFICATE.read_text())
    assert cert["status"] == "PASS"
    assert cert["pass1825_solver_export"]["signature_sha256"] == EXPECTED_SIGNATURE_SHA256
    payload = json.loads(
        gzip.decompress(base64.b64decode(SIGNATURES.read_text())).decode()
    )
    signatures = [[int(x) for x in row] for row in payload["signatures"]]
    labels = [int(x) for x in payload["class_labels"]]
    assert payload["shape"] == [720, 45]
    assert len(signatures) == len(labels) == 720
    assert all(len(row) == 45 for row in signatures)
    assert all(sum(row) == 60 for row in signatures)
    assert all(0 <= x <= 4 for row in signatures for x in row)
    assert len({tuple(row) for row in signatures}) == 720
    return signatures, labels, cert


def solve(signatures: list[list[int]], labels: list[int], seconds: float) -> dict:
    model = cp_model.CpModel()
    count = [model.new_int_var(0, 9, f"x_{i}") for i in range(720)]
    used = [model.new_bool_var(f"u_{i}") for i in range(720)]
    for i in range(720):
        model.add(count[i] >= used[i])
        model.add(count[i] <= 9 * used[i])
    model.add(sum(count) == 9)
    for coordinate in range(45):
        model.add(
            sum(signatures[i][coordinate] * count[i] for i in range(720)) == 12
        )
    # Prefer a witness with as many distinct signature vectors as possible.  This
    # objective does not alter feasibility and makes any positive skeleton easier
    # to lift to distinct exact covers.
    model.maximize(sum(used))

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = seconds
    solver.parameters.num_search_workers = 8
    solver.parameters.random_seed = 2310
    solver.parameters.log_search_progress = True
    status = solver.solve(model)
    name = solver.status_name(status)

    selected = []
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        for i, var in enumerate(count):
            multiplicity = int(solver.value(var))
            if multiplicity:
                selected.append(
                    {
                        "signature_index": i,
                        "class_label": labels[i],
                        "multiplicity": multiplicity,
                        "signature": signatures[i],
                    }
                )
        total = [
            sum(item["multiplicity"] * item["signature"][j] for item in selected)
            for j in range(45)
        ]
        assert total == [12] * 45
        assert sum(item["multiplicity"] for item in selected) == 9
    else:
        total = None

    exact_negative = status == cp_model.INFEASIBLE
    witness_positive = status in (cp_model.OPTIMAL, cp_model.FEASIBLE)
    result = {
        "schema": "w33.pass2309.signature_resolution_solver.v1",
        "status": (
            "PASS_SIGNATURE_QUOTIENT_INFEASIBLE"
            if exact_negative
            else "PASS_SIGNATURE_QUOTIENT_FEASIBLE_WITNESS"
            if witness_positive
            else "BOUNDARY_SIGNATURE_QUOTIENT_UNKNOWN"
        ),
        "input": {
            "signature_count": 720,
            "signature_shape": [720, 45],
            "signature_sha256": EXPECTED_SIGNATURE_SHA256,
            "global_cover_count": 3_547_800,
            "global_signature_count": 720,
        },
        "model": {
            "variables": "720 integer multiplicities x_i in [0,9] plus 720 support bits",
            "cover_count_equation": "sum_i x_i = 9",
            "octet_capacity_equations": "sum_i x_i*t_i[o] = 12 for all 45 octets",
            "capacity_derivation": "540 degree-one frame/octet incidences divided uniformly over 45 octets",
            "objective": "maximize the number of distinct selected signature vectors",
            "time_limit_seconds": seconds,
        },
        "solver": {
            "engine": "OR-Tools CP-SAT",
            "status": name,
            "wall_time_seconds": solver.wall_time,
            "branches": solver.num_branches,
            "conflicts": solver.num_conflicts,
            "objective_value": solver.objective_value if witness_positive else None,
            "best_objective_bound": solver.best_objective_bound,
        },
        "selected_signature_multiset": selected,
        "selected_sum": total,
        "checks": {
            "all_720_signatures_unique": len({tuple(x) for x in signatures}) == 720,
            "each_signature_sum_60": all(sum(x) == 60 for x in signatures),
            "uniform_target_sum_540": sum([12] * 45) == 540,
            "solver_returned_decisive_or_bounded_status": name
            in {"OPTIMAL", "FEASIBLE", "INFEASIBLE", "UNKNOWN"},
            "positive_witness_rechecks": (not witness_positive)
            or (total == [12] * 45 and sum(x["multiplicity"] for x in selected) == 9),
        },
        "theorem": (
            "No nine-cover resolution exists, because even the complete 720-vector nonlinear signature quotient is infeasible."
            if exact_negative
            else "The complete nonlinear signature quotient admits a nine-signature capacity witness; this sharply narrows but does not solve frame-level compatibility."
            if witness_positive
            else "The bounded run did not decide the complete nonlinear signature quotient."
        ),
        "boundary": (
            "INFEASIBLE is an exact obstruction to chi(H)=9."
            if exact_negative
            else "A signature witness is necessary but not sufficient: selected signatures must still be represented by nine pairwise frame-disjoint exact covers."
            if witness_positive
            else "UNKNOWN is not evidence for feasibility or infeasibility; increase resources or add exact decomposition cuts."
        ),
    }
    assert all(result["checks"].values())
    result["sha256_without_hash_field"] = canonical_sha256(result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seconds", type=float, default=300.0)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    signatures, labels, _ = load_inputs()
    result = solve(signatures, labels, args.seconds)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "solver_status": result["solver"]["status"],
        "selected_types": len(result["selected_signature_multiset"]),
        "certificate": result["sha256_without_hash_field"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
