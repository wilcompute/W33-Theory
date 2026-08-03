#!/usr/bin/env python3
"""Passes 2820-2824: exact blueprint hardening and support-codec boundary.

This verifier does three jobs:
1. imports the already-frozen Pass 2803-2806 certificates and checks the claims
   promoted into the public documents;
2. computes the new deterministic-refinement obstruction for the PG(3,2)
   support codec under the selected four-operation micro-ISA;
3. optionally audits the four canonical public documents after migration.

The support partition is geometrically exact but not an execution congruence.
Starting from 16 binary support masks, deterministic partition refinement under
F_p, CX_{p->f}, CX_{f->p}, and Z_p gives 16 -> 40 -> 78 -> 81 classes.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from itertools import product
from pathlib import Path
from typing import Callable, Iterable

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = DATA / "PART_BT2820_BT2824_BLUEPRINT_HARDENING_results.json"

Vector = tuple[int, int, int, int]
Matrix = tuple[tuple[int, int, int, int], ...]
Operation = Callable[[Vector], Vector]

F_P: Matrix = (
    (0, 2, 0, 0),
    (1, 0, 0, 0),
    (0, 0, 1, 0),
    (0, 0, 0, 1),
)
CX_PF: Matrix = (
    (1, 0, 0, 0),
    (0, 1, 0, 2),
    (1, 0, 1, 0),
    (0, 0, 0, 1),
)
CX_FP: Matrix = (
    (1, 0, 1, 0),
    (0, 1, 0, 0),
    (0, 0, 1, 0),
    (0, 2, 0, 1),
)


def load_json(name: str) -> dict:
    path = DATA / name
    if not path.exists():
        raise FileNotFoundError(path)
    return json.loads(path.read_text(encoding="utf-8"))


def matvec(matrix: Matrix, vector: Vector) -> Vector:
    return tuple(
        sum(matrix[row][col] * vector[col] for col in range(4)) % 3
        for row in range(4)
    )  # type: ignore[return-value]


def z_p(vector: Vector) -> Vector:
    return (vector[0], (vector[1] + 1) % 3, vector[2], vector[3])


def support_mask(vector: Vector) -> int:
    result = 0
    for index, coordinate in enumerate(vector):
        if coordinate:
            result |= 1 << (3 - index)
    return result


def mask_bits(mask: int) -> str:
    return f"{mask:04b}"


def class_histogram(partition: dict[Vector, int]) -> dict[str, int]:
    classes: dict[int, list[Vector]] = defaultdict(list)
    for vector, label in partition.items():
        classes[label].append(vector)
    return {
        str(size): count
        for size, count in sorted(Counter(map(len, classes.values())).items())
    }


def canonical_groups(partition: dict[Vector, int]) -> set[frozenset[Vector]]:
    classes: dict[int, set[Vector]] = defaultdict(set)
    for vector, label in partition.items():
        classes[label].add(vector)
    return {frozenset(group) for group in classes.values()}


def refine(
    states: Iterable[Vector],
    partition: dict[Vector, int],
    operations: tuple[Operation, ...],
) -> dict[Vector, int]:
    signatures: dict[tuple[int, tuple[int, ...]], int] = {}
    refined: dict[Vector, int] = {}
    for vector in states:
        signature = (
            partition[vector],
            tuple(partition[operation(vector)] for operation in operations),
        )
        refined[vector] = signatures.setdefault(signature, len(signatures))
    return refined


def compute_support_boundary() -> dict:
    states = list(product(range(3), repeat=4))
    operations: tuple[Operation, ...] = (
        lambda vector: matvec(F_P, vector),
        lambda vector: matvec(CX_PF, vector),
        lambda vector: matvec(CX_FP, vector),
        z_p,
    )

    partition = {vector: support_mask(vector) for vector in states}
    counts: list[int] = []
    histograms: list[dict[str, int]] = []

    while True:
        counts.append(len(set(partition.values())))
        histograms.append(class_histogram(partition))
        refined = refine(states, partition, operations)
        if canonical_groups(refined) == canonical_groups(partition):
            break
        partition = refined

    witness_a: Vector = (0, 1, 0, 0)
    witness_b: Vector = (0, 2, 0, 0)
    assert support_mask(witness_a) == support_mask(witness_b) == 0b0100
    assert support_mask(z_p(witness_a)) == 0b0100
    assert support_mask(z_p(witness_b)) == 0b0000

    assert counts == [16, 40, 78, 81]
    assert histograms == [
        {"1": 1, "2": 4, "4": 6, "8": 4, "16": 1},
        {"1": 7, "2": 29, "4": 4},
        {"1": 75, "2": 3},
        {"1": 81},
    ]

    return {
        "state_count": len(states),
        "initial_support_classes": 16,
        "initial_class_size_histogram": histograms[0],
        "deterministic_refinement_class_counts": counts,
        "refinement_histograms": histograms,
        "non_lumpability_witness": {
            "support_mask": "0100",
            "states": [list(witness_a), list(witness_b)],
            "operation": "Z_p",
            "next_support_masks": [
                mask_bits(support_mask(z_p(witness_a))),
                mask_bits(support_mask(z_p(witness_b))),
            ],
        },
        "interpretation": (
            "support-first readout/equitable geometry codec; full ternary phase "
            "is required for deterministic execution"
        ),
    }


def audit_documents() -> dict[str, bool]:
    w33 = (ROOT / "w33_paper.tex").read_text(encoding="utf-8")
    holo = (ROOT / "photonic_holonet.tex").read_text(encoding="utf-8")
    blueprint = (ROOT / "holonet_machine_blueprint.tex").read_text(encoding="utf-8")
    index = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
    registry = load_json("w33_pass_namespace_registry_v2.d/2820-2824.json")

    insert = r"\input{analysis/BT2820_BT2824_blueprint_hardening_insert}"
    checks = {
        "w33_inserted": insert in w33,
        "holonet_inserted": insert in holo,
        "blueprint_inserted": insert in blueprint,
        "blueprint_pass_range_current": "Passes 2700--2824" in blueprint,
        "blueprint_public_internal_isa_split": (
            ("public three-bit ISA" in blueprint or "eight-opcode, three-bit" in blueprint)
            and ("internal two-bit frame micro-ISA" in blueprint or "four-operation, two-bit" in blueprint)
        ),
        "blueprint_m36_protocol_promoted": (
            ("48 improving deep-grade branches" in blueprint or "$48$ improving deep-grade branches" in blueprint)
            and "No distillation protocol for $M_{36}$ is known" not in blueprint
        ),
        "blueprint_m36_boundary": (
            "not a fault-tolerant injection threshold" in blueprint
        ),
        "blueprint_sensor_scope": (
            "arbitrary $U(1)$ representatives require exponent $3^n$" in blueprint
        ),
        "blueprint_live_mixer": (
            "rtl/w33_pass2773_spread_mixer36_synth.sv" in blueprint
            and "historical dead source was removed" in blueprint
        ),
        "index_hardening_section": (
            'id="pass-2820-2824-blueprint-hardening"' in index
        ),
        "reservation_closed": registry.get("status") == "complete",
    }
    return checks


def build_result(audit: bool) -> dict:
    frontier = load_json("PART_BT2803_BT2807_FIVE_DEEP_FRONTIERS_results.json")
    support_lift = load_json(
        "PART_BT2808_PG32_TETRAHEDRAL_SUPPORT_LIFT_results.json"
    )

    prior = frontier["checks"]
    checks = {
        "micro_isa_linear_order": prior["isa_sp43"],
        "micro_isa_affine_order": prior["isa_asp43"],
        "micro_isa_four_operations": prior["isa_two_bit"],
        "m36_full_clifford_order": prior["m36_clifford_11520"],
        "m36_projector_count": (
            "codes_5355"
            in (ROOT / "analysis" / "bt2804_m36_clifford_decoder_distillation.py")
            .read_text(encoding="utf-8")
        ),
        "m36_deep_improving_48": prior["m36_deep_improving_48"],
        "m36_other_improving_zero": prior["m36_other_improving_zero"],
        "m36_decoder_is_h": prior["m36_explicit_protocol"],
        "sensor_odd_3": prior["sensor_odd_3"],
        "sensor_even_9": prior["sensor_even_9"],
        "transpose_q5_inner": prior["transpose_q5_inner"],
        "transpose_q7_outer": prior["transpose_q7_outer"],
        "transpose_cx_conjugacy": prior["transpose_cx_conjugacy"],
        "support_lift_43_checks": support_lift["check_count"] == 43,
        "support_lift_tomotope_capacity": (
            support_lift["checks"]["tomotope_profile_4_12_16_8"]
        ),
        "dead_mixer_removed": not (ROOT / "rtl" / "w33_spread_mixer36.sv").exists(),
        "live_mixer_present": (
            ROOT / "rtl" / "w33_pass2773_spread_mixer36_synth.sv"
        ).exists(),
    }
    assert all(checks.values()), [name for name, value in checks.items() if not value]

    support = compute_support_boundary()
    checks.update(
        {
            "support_refines_to_full_81": (
                support["deterministic_refinement_class_counts"]
                == [16, 40, 78, 81]
            ),
            "support_witness_is_nondeterministic": (
                support["non_lumpability_witness"]["next_support_masks"]
                == ["0100", "0000"]
            ),
        }
    )

    document_checks: dict[str, bool] = {}
    if audit:
        document_checks = audit_documents()
        checks.update(document_checks)
        assert all(document_checks.values()), [
            name for name, value in document_checks.items() if not value
        ]

    result = {
        "schema": "w33.pass2820_2824.blueprint_hardening.v1",
        "status": "COMPLETE_EXACT_COMPILED" if audit else "COMPLETE_EXACT_COMPILE_PENDING",
        "canonical_pass_range": "2820-2824",
        "check_count": len(checks),
        "checks": checks,
        "headline": (
            "The binary support shell is an exact geometric codec but not a "
            "lossless execution quotient: the selected four-operation micro-ISA "
            "refines 16 support classes through 40 and 78 classes to all 81 "
            "ternary frame states."
        ),
        "micro_isa": {
            "public_opcode_bits": 3,
            "public_opcode_count": 8,
            "internal_opcode_bits": 2,
            "internal_operation_count": 4,
            "selected_operations": ["F_p", "CX_p->f", "CX_f->p", "Z_p"],
            "linear_order": 51_840,
            "affine_order": 4_199_040,
            "hardware_boundary": (
                "72 LC / 60.80 MHz belongs to the public loadable full frame "
                "unit; the minimal four-operation engine needs separately "
                "observed synthesis/P&R evidence."
            ),
        },
        "m36": {
            "projector_count": 5_355,
            "logical_clifford_order": 11_520,
            "improving_deep_branches": 48,
            "improving_other_branches": 0,
            "explicit_protocol": {
                "input_ray": 5,
                "output_ray": 7,
                "stabilizers": ["IYZY", "YZXY"],
                "syndrome": [-1, 1],
                "decoder": "Hadamard on second logical qubit",
                "success_probability": "(p^2-2p+2)/4",
                "output_fidelity": "(5p^2-12p+8)/(4(p^2-2p+2))",
                "fidelity_gain": "p(p-1)(3p-2)/(4(p^2-2p+2))",
                "improvement_interval": "0<p<2/3",
            },
            "boundary": (
                "state-fidelity distillation, not a fault-tolerant injection "
                "threshold or asymptotic-yield theorem"
            ),
        },
        "support_codec": support,
        "sensor": {
            "finite_mu12_lift": {"odd_n": 3, "even_n": 9},
            "arbitrary_u1_representatives": "3^n",
        },
        "transpose": {
            "q5": "inner projective class",
            "q7": "outer diagonal class",
            "cx_direction_conjugacy": True,
        },
        "mixer": {
            "live_source": "rtl/w33_pass2773_spread_mixer36_synth.sv",
            "retired_source": "rtl/w33_spread_mixer36.sv",
        },
        "literature_boundary": {
            "tomotope": (
                "published f-vector is (4,12,16,8) with four tetrahedra and "
                "four hemioctahedra; the support-capacity identity is a "
                "separate repo theorem"
            ),
            "distillation": (
                "comparison protocols may change gate set or output family; "
                "Pass 2804 claims only the stated stabilizer-projector/logical-"
                "Clifford search class"
            ),
        },
        "source_sha256": {
            name: hashlib.sha256((DATA / name).read_bytes()).hexdigest()
            for name in (
                "PART_BT2803_BT2807_FIVE_DEEP_FRONTIERS_results.json",
                "PART_BT2808_PG32_TETRAHEDRAL_SUPPORT_LIFT_results.json",
            )
        },
    }
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--audit-docs", action="store_true")
    parser.add_argument("--verify-frozen", action="store_true")
    args = parser.parse_args()

    result = build_result(audit=args.audit_docs)
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"

    if args.verify_frozen:
        current = OUT.read_text(encoding="utf-8")
        if current != rendered:
            raise SystemExit(f"frozen certificate drift: {OUT}")
    else:
        OUT.write_text(rendered, encoding="utf-8")

    print(f"PASS {result['check_count']}/{result['check_count']}")
    print(result["headline"])


if __name__ == "__main__":
    main()
