#!/usr/bin/env python3
"""Pass 2309: solve the nine-cover problem in the complete 720-signature quotient.

This is an exact integer feasibility problem on the frozen Pass-1825 nonlinear
signatures.  A feasible answer is only a signature-level witness; frame-level
pairwise disjointness remains a separate condition.  An INFEASIBLE answer from
CP-SAT closes the quotient but is still reported as a computational certificate,
not as a handwritten proof.
"""
from __future__ import annotations

import argparse
import base64
import gzip
import hashlib
import json
from math import gcd
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SIG_B64 = ROOT / "data" / "w33_pass1825_signatures720.json.gz.b64"
CERT = ROOT / "data" / "w33_pass1821_1825_complete_cover_signature.json"


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


def solve(vectors: list[list[int]], target: list[int], time_limit: float) -> dict[str, Any]:
    from ortools.sat.python import cp_model

    model = cp_model.CpModel()
    x = [model.NewIntVar(0, 9, f"x_{i}") for i in range(len(vectors))]
    model.Add(sum(x) == 9)
    for j in range(45):
        model.Add(sum(vectors[i][j] * x[i] for i in range(len(vectors))) == target[j])

    # Prefer a compressed witness.  This does not change feasibility and makes
    # any positive certificate easier to inspect and lift to frame level.
    used = [model.NewBoolVar(f"u_{i}") for i in range(len(vectors))]
    for xi, ui in zip(x, used):
        model.Add(xi <= 9 * ui)
        model.Add(xi >= ui)
    model.Minimize(sum(used))

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
        "objective_is_support_size": True,
    }
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        selected = [(i, solver.Value(x[i])) for i in range(len(x)) if solver.Value(x[i])]
        total = [sum(mult * vectors[i][j] for i, mult in selected) for j in range(45)]
        assert sum(mult for _, mult in selected) == 9
        assert total == target
        norms = {96: 0, 104: 0, 120: 0, 128: 0}
        for i, mult in selected:
            n2 = sum(z * z for z in vectors[i])
            norms[n2] = norms.get(n2, 0) + mult
        out.update(
            {
                "feasible": True,
                "support_size": len(selected),
                "selected": [
                    {
                        "index": i,
                        "multiplicity": mult,
                        "norm2": sum(z * z for z in vectors[i]),
                        "signature": vectors[i],
                    }
                    for i, mult in selected
                ],
                "weighted_signature_class_counts": {str(k): v for k, v in sorted(norms.items()) if v},
                "exact_sum": total,
                "witness_sha256": canonical_hash(selected),
                "boundary": "This is a nine-signature multiset summing to the universal capacity. It is not yet nine pairwise frame-disjoint exact covers.",
            }
        )
    else:
        out.update(
            {
                "feasible": False if status_name == "INFEASIBLE" else None,
                "boundary": "INFEASIBLE closes the complete nonlinear signature quotient computationally. UNKNOWN does not decide it.",
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
    result = solve(vectors, target, args.time_limit)
    result.update(
        {
            "schema": "w33.pass2309.signature_resolution_quotient.v1",
            "signature_count": len(vectors),
            "signature_shape": [len(vectors), 45],
            "target": target,
            "target_sum": sum(target),
            "source_signature_sha256": cert["pass1825_solver_export"]["signature_sha256"],
            "checks": {
                "720_unique_signatures": True,
                "all_signatures_sum_60": True,
                "target_is_12_times_one": True,
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
