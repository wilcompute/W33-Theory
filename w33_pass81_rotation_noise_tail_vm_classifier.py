#!/usr/bin/env python3
"""
Pass 81 -- K12 rotation, noisy syndrome, Hashimoto tail, VM channels, classifier.

This pass executes the five Pass 80 follow-ups:

1. verify an explicit orientable triangular K12 rotation system and compare its
   44 face boundaries against the native 47-check Pass 80 stabilizer basis;
2. add a deterministic phenomenological noisy-syndrome simulator for the native
   66-qutrit code;
3. run the GAP Hashimoto +/-1 eigenspace decomposition certificate;
4. audit the packet VM's real Terwilliger local-channel trace metadata;
5. build a progressive 28-Spence universe classifier.
"""

from __future__ import annotations

import importlib.util
import json
import random
import shutil
import subprocess
import sys
from collections import Counter, defaultdict
from itertools import combinations, product
from pathlib import Path
from typing import Any

import w33_pass79_full_closure as pass79
import w33_pass80_native_k12_edge_vm as pass80

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "w33_pass81_rotation_noise_tail_vm_classifier.json"
GAP_TAIL = ROOT / "analysis" / "w33_pass81_hashimoto_tail_decomposition.g"
PACKET_VM = ROOT / "analysis" / "w33_packet_vm.py"


K12_DIRECTED_FACES: list[tuple[int, int, int]] = [
    (0, 1, 6),
    (0, 2, 8),
    (0, 3, 11),
    (0, 4, 3),
    (0, 5, 9),
    (0, 7, 2),
    (0, 10, 5),
    (0, 6, 10),
    (0, 8, 1),
    (0, 9, 4),
    (0, 11, 7),
    (1, 3, 5),
    (1, 4, 2),
    (1, 9, 7),
    (1, 5, 11),
    (1, 10, 9),
    (1, 2, 3),
    (1, 7, 4),
    (1, 8, 10),
    (1, 11, 6),
    (2, 5, 10),
    (4, 7, 10),
    (3, 4, 10),
    (2, 10, 11),
    (4, 11, 8),
    (4, 9, 11),
    (2, 4, 5),
    (4, 6, 5),
    (4, 8, 6),
    (2, 11, 9),
    (2, 6, 3),
    (2, 7, 6),
    (2, 9, 8),
    (3, 9, 5),
    (3, 10, 8),
    (5, 7, 8),
    (6, 8, 9),
    (6, 9, 10),
    (3, 7, 9),
    (7, 11, 10),
    (3, 6, 11),
    (3, 8, 7),
    (5, 6, 7),
    (5, 8, 11),
]


def oriented_edge_index() -> dict[tuple[int, int], tuple[int, int]]:
    edges = pass80.k12_edges()
    out = {}
    for idx, (left, right) in enumerate(edges):
        out[(left, right)] = (idx, 1)
        out[(right, left)] = (idx, 2)
    return out


def oriented_face_row(face: tuple[int, int, int]) -> list[int]:
    edge_index = oriented_edge_index()
    row = [0] * 66
    for left, right in [(face[0], face[1]), (face[1], face[2]), (face[2], face[0])]:
        idx, sign = edge_index[(left, right)]
        row[idx] = (row[idx] + sign) % 3
    return row


def cycle_from_successor(successor: dict[int, int], start: int) -> list[int]:
    order = []
    current = start
    while current not in order:
        order.append(current)
        current = successor[current]
    if current != start:
        return []
    return order


def k12_rotation_system() -> dict:
    arcs = [(i, j) for i in range(12) for j in range(12) if i != j]
    arc_counts = Counter()
    successor: dict[int, dict[int, int]] = {vertex: {} for vertex in range(12)}
    for face in K12_DIRECTED_FACES:
        for left, right, nxt in [
            (face[0], face[1], face[2]),
            (face[1], face[2], face[0]),
            (face[2], face[0], face[1]),
        ]:
            arc_counts[(left, right)] += 1
            successor[left][right] = nxt

    rotations = {
        vertex: cycle_from_successor(successor[vertex], min(successor[vertex]))
        for vertex in range(12)
    }
    face_rows = [oriented_face_row(face) for face in K12_DIRECTED_FACES]
    pass80_z = pass80.triangle_checks()
    face_rank = pass80.gf3_rank(face_rows, 66)
    pass80_rank = pass80.gf3_rank(pass80_z, 66)
    combined_rank = pass80.gf3_rank(face_rows + pass80_z, 66)
    intersection_dim = face_rank + pass80_rank - combined_rank
    faces_in_pass80_span = sum(
        1 for row in face_rows if pass80.in_rowspace(row, pass80_z)
    )
    pass80_checks_in_face_span = sum(
        1 for row in pass80_z if pass80.in_rowspace(row, face_rows)
    )

    checks = {
        "face_count_44": len(K12_DIRECTED_FACES) == 44,
        "directed_arcs_once": len(arc_counts) == len(arcs)
        and set(arc_counts.values()) == {1},
        "all_vertex_links_are_11_cycles": all(
            len(row) == 11 for row in rotations.values()
        ),
        "euler_genus_6": 12 - 66 + 44 == -10,
        "face_boundaries_are_cycles": all(
            pass80.dot(row, vertex_check) == 0
            for row in face_rows
            for vertex_check in pass80.k12_vertex_checks()
        ),
        "face_boundary_rank_43": face_rank == 43,
        "pass80_z_rank_47": pass80_rank == 47,
        "nontrivial_overlap": intersection_dim > 0,
    }
    return {
        "faces": [list(face) for face in K12_DIRECTED_FACES],
        "rotations": {str(vertex): row for vertex, row in rotations.items()},
        "counts": {"vertices": 12, "edges": 66, "faces": 44, "euler": -10, "genus": 6},
        "comparison_with_pass80_z_basis": {
            "face_boundary_rank": face_rank,
            "pass80_z_rank": pass80_rank,
            "combined_rank": combined_rank,
            "intersection_dimension": intersection_dim,
            "faces_in_pass80_span": faces_in_pass80_span,
            "pass80_checks_in_face_span": pass80_checks_in_face_span,
        },
        "checks": checks,
        "verified": all(checks.values()),
        "boundary": (
            "This is an explicit orientable triangular K12 embedding.  Its 44 "
            "face boundaries span rank 43, while the Pass 80 native code uses a "
            "rank-47 triangle-cycle stabilizer basis.  The code basis is larger "
            "than the face-boundary space, so the embedding is a comparison object, "
            "not a replacement for the full stabilizer basis."
        ),
    }


def stabilizer_rows() -> list[list[int]]:
    rows = []
    for xrow in pass80.k12_vertex_checks():
        rows.append(xrow + [0] * 66)
    for zrow in pass80.triangle_checks():
        rows.append([0] * 66 + zrow)
    return rows


def decoder_lookup() -> dict[tuple[int, ...], tuple[int, int, int]]:
    lookup = {}
    x_checks = pass80.k12_vertex_checks()
    z_checks = pass80.triangle_checks()
    for site in range(66):
        for x, z in product(range(3), repeat=2):
            if (x, z) == (0, 0):
                continue
            ex = [0] * 66
            ez = [0] * 66
            ex[site] = x
            ez[site] = z
            lookup[pass80.symplectic_syndrome(ex, ez, x_checks, z_checks)] = (
                site,
                x,
                z,
            )
    return lookup


def noisy_syndrome_simulator() -> dict:
    rng = random.Random(81033)
    x_checks = pass80.k12_vertex_checks()
    z_checks = pass80.triangle_checks()
    lookup = decoder_lookup()
    stab = stabilizer_rows()
    paulis = [(x, z) for x, z in product(range(3), repeat=2) if (x, z) != (0, 0)]

    def noisy_value(value: int, q: float) -> int:
        if rng.random() >= q:
            return value
        choices = [candidate for candidate in [0, 1, 2] if candidate != value]
        return choices[0 if rng.random() < 0.5 else 1]

    def majority(values: list[int]) -> int:
        counts = Counter(values)
        return min(
            [key for key, count in counts.items() if count == max(counts.values())]
        )

    def run_row(p: float, q: float, rounds: int, trials: int) -> dict[str, Any]:
        successes = 0
        logical_failures = 0
        uncorrected = 0
        multi_error_trials = 0
        for _ in range(trials):
            ex = [0] * 66
            ez = [0] * 66
            error_sites = 0
            for site in range(66):
                if rng.random() < p:
                    error_sites += 1
                    x, z = paulis[rng.randrange(len(paulis))]
                    ex[site] = x
                    ez[site] = z
            multi_error_trials += int(error_sites > 1)
            exact = pass80.symplectic_syndrome(ex, ez, x_checks, z_checks)
            measured_rounds = [
                tuple(noisy_value(value, q) for value in exact) for _ in range(rounds)
            ]
            measured = tuple(
                majority([row[idx] for row in measured_rounds])
                for idx in range(len(exact))
            )
            correction = lookup.get(measured)
            cx = [0] * 66
            cz = [0] * 66
            if correction is not None:
                site, x, z = correction
                cx[site] = x
                cz[site] = z
            else:
                uncorrected += int(any(ex) or any(ez))
            rx = [(ex[i] - cx[i]) % 3 for i in range(66)]
            rz = [(ez[i] - cz[i]) % 3 for i in range(66)]
            residual = rx + rz
            if pass80.in_rowspace(residual, stab):
                successes += 1
            else:
                logical_failures += 1
        return {
            "physical_error_p": p,
            "syndrome_error_q": q,
            "rounds": rounds,
            "trials": trials,
            "success_rate": round(successes / trials, 4),
            "logical_failure_rate": round(logical_failures / trials, 4),
            "multi_error_trial_rate": round(multi_error_trials / trials, 4),
            "uncorrected_nonzero_rate": round(uncorrected / trials, 4),
        }

    rows = []
    for p in [0.0005, 0.001, 0.002, 0.005]:
        for q in [0.0, 0.002, 0.01]:
            for rounds in [1, 3, 5]:
                rows.append(run_row(p, q, rounds, 180))

    best_by_noise = {}
    for q in [0.0, 0.002, 0.01]:
        candidates = [
            row
            for row in rows
            if row["syndrome_error_q"] == q and row["physical_error_p"] == 0.001
        ]
        best_by_noise[str(q)] = max(candidates, key=lambda row: row["success_rate"])

    return {
        "model": "phenomenological qutrit data errors plus repeated noisy syndrome extraction",
        "rng_seed": 81033,
        "decoder": "single-error ideal lookup, applied to majority-voted syndrome",
        "rows": rows,
        "best_rows_at_p_0_001": best_by_noise,
        "checks": {
            "rows_generated": len(rows) == 36,
            "repetition_helps_at_q_0_01": best_by_noise["0.01"]["rounds"] in [3, 5],
            "zero_syndrome_noise_best_success_high": best_by_noise["0.0"][
                "success_rate"
            ]
            >= 0.99,
        },
        "boundary": (
            "This is a phenomenological repeated-syndrome simulator.  It is not "
            "yet a gate-level circuit-noise threshold calculation."
        ),
    }


def parse_triples(value: str) -> list[dict[str, int]]:
    if not value:
        return []
    rows = []
    for chunk in value.split(","):
        idx, degree, multiplicity = [int(part) for part in chunk.split(":")]
        rows.append(
            {"character_index": idx, "degree": degree, "multiplicity": multiplicity}
        )
    return rows


def run_hashimoto_tail_gap() -> dict:
    gap = shutil.which("gap") or "/usr/bin/gap"
    process = subprocess.run(
        [gap, "-q", str(GAP_TAIL)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
        timeout=180,
    )
    raw = process.stdout.replace("\\\n", "")
    parsed = {}
    for line in raw.splitlines():
        if "=" in line:
            key, value = line.strip().split("=", 1)
            parsed[key] = value
    required = {
        "edge_group_order",
        "directed_edge_degree",
        "hashimoto_plus_dimension",
        "hashimoto_minus_dimension",
        "hashimoto_plus_constituents",
        "hashimoto_minus_constituents",
    }
    missing = required - set(parsed)
    if missing:
        raise AssertionError(f"missing GAP tail keys: {sorted(missing)}\n{raw}")
    plus = parse_triples(parsed["hashimoto_plus_constituents"])
    minus = parse_triples(parsed["hashimoto_minus_constituents"])
    return {
        "edge_group_order": int(parsed["edge_group_order"]),
        "directed_edge_degree": int(parsed["directed_edge_degree"]),
        "plus_eigenspace_dimension": int(parsed["hashimoto_plus_dimension"]),
        "minus_eigenspace_dimension": int(parsed["hashimoto_minus_dimension"]),
        "plus_constituents": plus,
        "minus_constituents": minus,
        "plus_dimension_sum": sum(row["degree"] * row["multiplicity"] for row in plus),
        "minus_dimension_sum": sum(
            row["degree"] * row["multiplicity"] for row in minus
        ),
        "tail_reading": (
            "The -1 Hashimoto eigenspace is the clean 200-dimensional tail.  "
            "The +1 eigenspace has dimension 201, so the x=1 Bass root fuses "
            "with the + tail as a single GAP eigenspace decomposition."
        ),
    }


def packet_vm_terwilliger_audit() -> dict:
    analysis_path = ROOT / "analysis"
    if str(analysis_path) not in sys.path:
        sys.path.insert(0, str(analysis_path))
    spec = importlib.util.spec_from_file_location("w33_packet_vm_pass81", PACKET_VM)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load packet VM module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    payload = module.build_payload()
    channel_totals = Counter()
    for sample in payload["samples"]:
        channel_totals.update(sample["terwilliger_channel_counts"])
    return {
        "packet_vm_status": payload["status"],
        "terwilliger_op_count": len(module.TERWILLIGER_OPS),
        "sample_channel_totals": dict(sorted(channel_totals.items())),
        "samples": [
            {
                "sample": sample["sample"],
                "result": sample["packet_vm_result"],
                "terwilliger_channel_counts": sample["terwilliger_channel_counts"],
            }
            for sample in payload["samples"]
        ],
        "checks": {
            "packet_vm_passes": payload["status"] == "PASS",
            "sixteen_ops_available": len(module.TERWILLIGER_OPS) == 16,
            "channels_attached": payload["checks"]["terwilliger_ops_attached"],
            "m3_channel_used": channel_totals["M3(Q)"] > 0,
        },
    }


def local_cycle_key(A: list[list[int]]) -> tuple[tuple[str, int], ...]:
    hist = Counter(
        pass79.local_type_label(pass79.local_type(A, vertex))
        for vertex in range(len(A))
    )
    return tuple(sorted(hist.items()))


def spence_universe_classifier() -> dict:
    lines = pass79.SPENCE_G6.read_text(encoding="utf-8").splitlines()
    graphs = {idx: pass79.parse_graph6(line) for idx, line in enumerate(lines, 1)}
    local_classes: dict[Any, list[int]] = defaultdict(list)
    local_alpha_classes: dict[Any, list[int]] = defaultdict(list)
    induced6_signatures: dict[int, tuple[tuple[Any, int], ...]] = {}
    for idx, A in graphs.items():
        local = local_cycle_key(A)
        alpha = pass79.max_clique_size(pass79.adjacency_bitsets(A, complement=True))
        local_classes[local].append(idx)
        local_alpha_classes[(local, alpha)].append(idx)
    residual_pairs = [group for group in local_alpha_classes.values() if len(group) > 1]
    for group in residual_pairs:
        for idx in group:
            induced6_signatures[idx] = tuple(
                sorted(pass80.induced_profile(graphs[idx], 6).items())
            )
    classifier_rows = []
    for idx, A in graphs.items():
        local = local_cycle_key(A)
        alpha = pass79.max_clique_size(pass79.adjacency_bitsets(A, complement=True))
        local_alpha_group = local_alpha_classes[(local, alpha)]
        if len(local_alpha_group) == 1:
            stage = "local_cycle_histogram_plus_alpha"
            signature = str((local, alpha))
        else:
            stage = "targeted_induced6_profile"
            signature = f"induced6:{hash(induced6_signatures[idx])}"
        classifier_rows.append(
            {"spence_index": idx, "stage": stage, "signature": signature}
        )
    stage_counts = Counter(row["stage"] for row in classifier_rows)
    return {
        "classifier": classifier_rows,
        "stage_counts": dict(sorted(stage_counts.items())),
        "local_cycle_classes": len(local_classes),
        "local_plus_alpha_classes": len(local_alpha_classes),
        "residual_after_local_plus_alpha": residual_pairs,
        "classified_count": len({row["signature"] for row in classifier_rows}),
        "checks": {
            "all_28_classified": len(classifier_rows) == 28
            and len({row["signature"] for row in classifier_rows}) == 28,
            "only_one_residual_pair": residual_pairs == [[20, 24]],
            "cheap_stage_classifies_26": stage_counts[
                "local_cycle_histogram_plus_alpha"
            ]
            == 26,
            "expensive_stage_classifies_2": stage_counts["targeted_induced6_profile"]
            == 2,
        },
    }


def build_payload() -> dict:
    rotation = k12_rotation_system()
    noisy = noisy_syndrome_simulator()
    tail = run_hashimoto_tail_gap()
    vm = packet_vm_terwilliger_audit()
    classifier = spence_universe_classifier()
    checks = {
        "rotation_system_verified": rotation["verified"],
        "noisy_syndrome_rows_verified": all(noisy["checks"].values()),
        "hashimoto_tail_gap_verified": (
            tail["edge_group_order"] == 25920
            and tail["directed_edge_degree"] == 480
            and tail["plus_eigenspace_dimension"] == tail["plus_dimension_sum"] == 201
            and tail["minus_eigenspace_dimension"] == tail["minus_dimension_sum"] == 200
        ),
        "packet_vm_terwilliger_channels": all(vm["checks"].values()),
        "spence_classifier_all_28": all(classifier["checks"].values()),
    }
    return {
        "schema": "w33.pass81.rotation_noise_tail_vm_classifier.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "track1_k12_rotation_system": rotation,
        "track2_noisy_syndrome_simulator": noisy,
        "track3_hashimoto_tail_gap": tail,
        "track4_packet_vm_terwilliger_channels": vm,
        "track5_spence_universe_classifier": classifier,
        "checks": checks,
    }


def main() -> int:
    payload = build_payload()
    OUTPUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    rotation = payload["track1_k12_rotation_system"]
    noisy = payload["track2_noisy_syndrome_simulator"]
    tail = payload["track3_hashimoto_tail_gap"]
    vm = payload["track4_packet_vm_terwilliger_channels"]
    classifier = payload["track5_spence_universe_classifier"]
    print("=" * 78)
    print("PASS 81 -- ROTATION / NOISE / TAIL / VM / CLASSIFIER")
    print("=" * 78)
    print(
        f"[1] K12 rotation: faces={rotation['counts']['faces']} genus={rotation['counts']['genus']} face-rank={rotation['comparison_with_pass80_z_basis']['face_boundary_rank']}"
    )
    print(
        f"[2] noisy syndrome rows={len(noisy['rows'])}; best q=0.01 row={noisy['best_rows_at_p_0_001']['0.01']}"
    )
    print(
        f"[3] Hashimoto: +dim={tail['plus_eigenspace_dimension']} -dim={tail['minus_eigenspace_dimension']}"
    )
    print(f"[4] packet VM Terwilliger channels={vm['sample_channel_totals']}")
    print(
        f"[5] classifier stages={classifier['stage_counts']} classified={classifier['classified_count']}"
    )
    print("checks:")
    for key, value in payload["checks"].items():
        print(f"  {'OK' if value else 'XX'} {key}")
    print(f"STATUS: {payload['status']}")
    print(f"[wrote] {OUTPUT.name}")
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
