#!/usr/bin/env python3
"""Pass 2309: independently re-execute and refine the 720-signature quotient.

Pass 1831 already proved that the complete nonlinear signature polytope contains
a nine-distinct-vector solution. Pass 1835 proved that the full PSp orbit of
that displayed solution has no lift to nine pairwise-disjoint exact covers.
This pass does not reclaim those results. It verifies the frozen witness against
the compressed 720-row export, then solves the exact integer model while
minimizing signature support. Any new witness is explicitly separated from the
frame-level lifting problem.
"""
from __future__ import annotations

import argparse
import base64
import gzip
import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SIG_B64 = ROOT / "data" / "w33_pass1825_signatures720.json.gz.b64"
CERT = ROOT / "data" / "w33_pass1821_1825_complete_cover_signature.json"
KNOWN = ROOT / "data" / "w33_pass1831_signature_resolution.json"
NO_LIFT = ROOT / "data" / "w33_pass1835_signature_lift_obstruction.json"


def canonical_hash(obj: Any) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def load_vectors() -> list[list[int]]:
    payload = json.loads(gzip.decompress(base64.b64decode(SIG_B64.read_text().strip())).decode())
    if isinstance(payload, list):
        vectors = payload
    elif isinstance(payload, dict):
        vectors = None
        for key in ("signatures", "vectors", "data", "rows"):
            value = payload.get(key)
            if isinstance(value, list):
                vectors = value
                break
        if vectors is None and payload and all(isinstance(v, list) for v in payload.values()):
            vectors = list(payload.values())
        if vectors is None:
            raise ValueError(f"unsupported signature payload keys: {sorted(payload)}")
    else:
        raise TypeError(type(payload))
    vectors = [[int(x) for x in row] for row in vectors]
    assert len(vectors) == 720
    assert all(len(row) == 45 for row in vectors)
    assert len({tuple(row) for row in vectors}) == 720
    assert all(sum(row) == 60 for row in vectors)
    return vectors


def derive_target(cert: dict[str, Any]) -> list[int]:
    block = cert["pass1823_packing_signature_obstruction"]
    packing = block["packing_signatures"]
    residual = block["residual_capacity"]
    target = [sum(row[j] for row in packing) + residual[j] for j in range(45)]
    assert target == [12] * 45
    return target


def verify_known(vectors: list[list[int]], target: list[int]) -> dict[str, Any]:
    known = json.loads(KNOWN.read_text())
    no_lift = json.loads(NO_LIFT.read_text())
    witness = known["integer_witness"]
    indices = [int(i) for i in witness["support_indices"]]
    rows = witness["vectors"]
    assert len(indices) == len(rows) == 9
    assert all(vectors[i] == row for i, row in zip(indices, rows))
    assert [sum(row[j] for row in rows) for j in range(45)] == target
    assert no_lift["search"]["status"] == "UNSAT"
    assert no_lift["signature_resolution_orbit"]["inner_setwise_stabilizer_order"] == witness["setwise_stabilizer_order"]
    return {
        "support_indices": indices,
        "vectors": rows,
        "class_composition": witness["class_composition"],
        "witness_sha256": known["witness_sha256"],
        "setwise_stabilizer_order": witness["setwise_stabilizer_order"],
        "inner_orbit_size": no_lift["signature_resolution_orbit"]["inner_orbit_size"],
        "cover_level_lift": {
            "status": no_lift["search"]["status"],
            "nodes": no_lift["search"]["nodes"],
            "dead_ends": no_lift["search"]["dead_ends"],
            "trace_fnv64": no_lift["search"]["trace_fnv64"],
        },
    }


def solve(vectors: list[list[int]], target: list[int], known_indices: list[int], time_limit: float) -> dict[str, Any]:
    from ortools.sat.python import cp_model

    model = cp_model.CpModel()
    x = [model.NewIntVar(0, 9, f"x_{i}") for i in range(len(vectors))]
    model.Add(sum(x) == 9)
    for j in range(45):
        model.Add(sum(vectors[i][j] * x[i] for i in range(len(vectors))) == target[j])

    # Multiplicity is allowed because two different exact covers may have the
    # same nonlinear signature. Minimize the number of signature types used.
    used = [model.NewBoolVar(f"u_{i}") for i in range(len(vectors))]
    for xi, ui in zip(x, used):
        model.Add(xi <= 9 * ui)
        model.Add(xi >= ui)
    model.Minimize(sum(used))

    known_set = set(known_indices)
    for i in range(len(vectors)):
        model.AddHint(x[i], 1 if i in known_set else 0)
        model.AddHint(used[i], 1 if i in known_set else 0)

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = time_limit
    solver.parameters.num_search_workers = 8
    solver.parameters.random_seed = 2309
    solver.parameters.log_search_progress = True
    status = solver.Solve(model)
    status_name = solver.StatusName(status)
    out: dict[str, Any] = {
        "solver": "OR-Tools CP-SAT integer model",
        "status": status_name,
        "wall_time_seconds": solver.WallTime(),
        "branches": solver.NumBranches(),
        "conflicts": solver.NumConflicts(),
        "objective": "minimize number of used signature types",
        "objective_bound": solver.BestObjectiveBound() if status_name != "UNKNOWN" else None,
    }
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        selected = [(i, solver.Value(x[i])) for i in range(len(x)) if solver.Value(x[i])]
        total = [sum(mult * vectors[i][j] for i, mult in selected) for j in range(45)]
        assert sum(mult for _, mult in selected) == 9
        assert total == target
        norms: dict[int, int] = {}
        for i, mult in selected:
            n2 = sum(z * z for z in vectors[i])
            norms[n2] = norms.get(n2, 0) + mult
        out.update(
            {
                "feasible": True,
                "support_size": len(selected),
                "support_minimal_proved": status_name == "OPTIMAL",
                "selected": [
                    {
                        "index": i,
                        "multiplicity": mult,
                        "norm2": sum(z * z for z in vectors[i]),
                        "signature": vectors[i],
                    }
                    for i, mult in selected
                ],
                "weighted_signature_class_counts_by_norm2": {str(k): v for k, v in sorted(norms.items())},
                "exact_sum": total,
                "witness_sha256": canonical_hash(selected),
                "same_support_as_pass1831": selected == [(i, 1) for i in known_indices],
                "boundary": "This is a nine-signature multiset summing to the universal capacity. A new support still requires complete cover-orbit lifting; the known Pass-1831 orbit is already no-lift by Pass 1835.",
            }
        )
    else:
        out.update(
            {
                "feasible": None,
                "support_minimal_proved": False,
                "boundary": "UNKNOWN does not alter the known Pass-1831 feasible witness or its Pass-1835 no-lift certificate.",
            }
        )
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--time-limit", type=float, default=900.0)
    ap.add_argument("--write-json", type=Path)
    args = ap.parse_args()

    cert = json.loads(CERT.read_text())
    vectors = load_vectors()
    target = derive_target(cert)
    known = verify_known(vectors, target)
    result = solve(vectors, target, known["support_indices"], args.time_limit)
    result.update(
        {
            "schema": "w33.pass2309.signature_resolution_quotient.v1",
            "status_scope": "independent support-minimization re-execution",
            "signature_count": len(vectors),
            "signature_shape": [len(vectors), 45],
            "target": target,
            "target_sum": sum(target),
            "source_signature_sha256": cert["pass1825_solver_export"]["signature_sha256"],
            "prior_artifact_reconciliation": known,
            "checks": {
                "720_unique_signatures": True,
                "all_signatures_sum_60": True,
                "target_is_12_times_one": True,
                "pass1831_support_indices_match_blob": True,
                "pass1831_witness_exact": True,
                "pass1835_known_orbit_no_lift": known["cover_level_lift"]["status"] == "UNSAT",
                "selected_witness_exact_if_present": result.get("feasible") is not True or result.get("exact_sum") == target,
            },
        }
    )
    result["sha256_without_hash_field"] = canonical_hash(result)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.write_json:
        args.write_json.parent.mkdir(parents=True, exist_ok=True)
        args.write_json.write_text(text)
    print(text, end="")


if __name__ == "__main__":
    main()
