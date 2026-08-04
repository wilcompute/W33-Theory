#!/usr/bin/env python3
"""Pass 3026: fail-closed SAT decision for the global 27-versus-28 question.

For the central D4 element r^2, every measured triangle returns the parity of faulty
edges on its boundary. Distinguishing all supports of weight at most two is equivalent to
requiring every nonzero edge set D of weight at most four to hit at least one selected
triangle in odd parity. Thus a 27-row solution exists only if the selected triangle
boundaries are a parity-check matrix whose kernel has binary minimum distance at least 5.

The CNF below is exact for that necessary central restriction. UNSAT proves that no full
D4 schedule of size 27 exists. SAT only supplies a central candidate, which is then checked
against all 48,826 group-valued hypotheses before any stronger status is emitted.
"""
from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path

from bt3025_3031_common import D4, EDGES, FAULTS, TRIANGLES, VERIFIED_28, hypotheses, syndrome

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "PART_BT3026_D4_FIXED_OPTIMUM_results.json"


def odd_triangles(edge_subset):
    subset = set(edge_subset)
    answer = []
    for triangle_index, triangle in enumerate(TRIANGLES):
        boundary = {
            tuple(sorted((triangle[0], triangle[1]))),
            tuple(sorted((triangle[0], triangle[2]))),
            tuple(sorted((triangle[1], triangle[2]))),
        }
        if len(boundary & subset) % 2:
            answer.append(triangle_index + 1)
    return answer


def base_clauses():
    clauses = []
    for weight in range(1, 5):
        for difference in itertools.combinations(EDGES, weight):
            clause = odd_triangles(difference)
            assert clause
            clauses.append(clause)
    assert len(clauses) == sum(__import__("math").comb(45, k) for k in range(1, 5))
    return clauses


def verify_full_d4(selected):
    syndromes = [syndrome(row, selected) for row in hypotheses()]
    return len(set(syndromes)) == 48_826


def verified_upper_bound():
    selected = [TRIANGLES.index(t) for t in VERIFIED_28]
    assert verify_full_d4(selected)
    return selected


def write_cnf(path):
    from pysat.card import CardEnc, EncType
    clauses = base_clauses()
    # Symmetry breaker: every nonempty schedule contains a triangle, and S10 is transitive
    # on triangles, so one selected row may be relabelled to (0,1,2).
    clauses.append([TRIANGLES.index((0,1,2)) + 1])
    cardinality = CardEnc.atmost(
        lits=list(range(1, 121)), bound=27, top_id=120, encoding=EncType.seqcounter
    )
    clauses.extend(cardinality.clauses)
    variables = max([120, cardinality.nv] + [abs(x) for row in clauses for x in row])
    with path.open("w") as handle:
        handle.write(f"p cnf {variables} {len(clauses)}\n")
        for clause in clauses:
            handle.write(" ".join(map(str, clause)) + " 0\n")
    return variables, len(clauses)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cnf", type=Path, default=ROOT / "data" / "bt3026_no27.cnf")
    parser.add_argument("--solve", action="store_true")
    parser.add_argument("--proof", type=Path, default=ROOT / "data" / "bt3026_no27.drup")
    args = parser.parse_args()

    args.cnf.parent.mkdir(exist_ok=True)
    variables, clauses = write_cnf(args.cnf)
    upper = verified_upper_bound()
    payload = {
        "schema": "w33.pass3026.d4_fixed_optimum.v1",
        "status": "SOURCE_COMPLETE_27_DECISION_PENDING",
        "central_difference_constraints": 164_220,
        "cnf_variables": variables,
        "cnf_clauses": clauses,
        "symmetry_breaker": "triangle (0,1,2) selected; valid by S10 transitivity",
        "verified_28_schedule": [list(TRIANGLES[i]) for i in upper],
        "verified_28_full_d4_unique": True,
        "current_exact_bounds": [23, 28],
        "claim_boundary": "UNSAT plus an independently checked proof establishes optimum 28. SAT establishes only a central-r2 candidate until full D4 verification succeeds.",
    }

    if args.solve:
        from pysat.solvers import Solver
        cnf = base_clauses()
        cnf.append([TRIANGLES.index((0,1,2)) + 1])
        from pysat.card import CardEnc, EncType
        card = CardEnc.atmost(lits=list(range(1,121)), bound=27, top_id=120, encoding=EncType.seqcounter)
        cnf.extend(card.clauses)
        with Solver(name="glucose4", bootstrap_with=cnf, with_proof=True) as solver:
            satisfiable = solver.solve()
            if satisfiable:
                model = solver.get_model()
                selected = [i for i in range(120) if i+1 in model]
                central_ok = len(selected) <= 27
                full_ok = central_ok and verify_full_d4(selected)
                payload.update({
                    "status": "SAT_FULL_D4_27_FOUND" if full_ok else "SAT_CENTRAL_ONLY_FULL_D4_REJECTED",
                    "sat_selected_count": len(selected),
                    "sat_schedule": [list(TRIANGLES[i]) for i in selected],
                    "sat_full_d4_unique": full_ok,
                })
            else:
                proof = solver.get_proof()
                args.proof.write_text("\n".join(proof) + "\n")
                payload.update({
                    "status": "UNSAT_REPORTED_PROOF_REQUIRES_INDEPENDENT_CHECK",
                    "proof_path": str(args.proof.relative_to(ROOT)),
                    "proof_lines": len(proof),
                })

    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({k: payload[k] for k in ("status","central_difference_constraints","cnf_variables","cnf_clauses")}, sort_keys=True))


if __name__ == "__main__":
    main()
