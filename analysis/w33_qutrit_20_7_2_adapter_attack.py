#!/usr/bin/env python3
"""Exact reconstruction and W33-adapter audit for the [[20,7,2]]_3 code.

Prakash--Saha (Quantum 9, 1768, 2025) define T_m <= F_3^(9m) from

  w = (0,1,2,0,1,2,...)

and v^(a), which is 1 on block a, 2 on the final block, and 0 elsewhere.
Puncturing coordinate 3j+1 in k blocks gives [[9m-k,k,2]]_3. For m=3,
k=7 this script reconstructs the resulting 9x20 matrix exactly:

  H1 = punctured v^(1),...,v^(7)      (7 logical rows)
  H0 = punctured w, v^(8)             (2 X-stabilizer rows)

It verifies the GF(3) invariants and independently finds a weight-2 logical-Z
witness while excluding weight-1 logical Z, reproducing d=2 for the Z sector.
It then audits the repository for the additional artifacts that would be needed
to call this a W33/Holonet fault-tolerant adapter.

The audit is intentionally fail closed. Reconstructing the external code is not
an encoding into W33. A W33 adapter requires an explicit 20-physical-qutrit
selector/intertwiner, stabilizer map, transversal-T packet schedule, and a noise /
threshold certificate for that mapped implementation.
"""
from __future__ import annotations

import itertools
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def mod3_rank(rows: list[list[int]]) -> int:
    if not rows:
        return 0
    a = [[x % 3 for x in row] for row in rows]
    r = 0
    for c in range(len(a[0])):
        pivot = next((i for i in range(r, len(a)) if a[i][c] % 3), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        inv = 1 if a[r][c] == 1 else 2
        a[r] = [(inv * x) % 3 for x in a[r]]
        for i in range(len(a)):
            if i != r and a[i][c] % 3:
                f = a[i][c]
                a[i] = [(x - f * y) % 3 for x, y in zip(a[i], a[r])]
        r += 1
        if r == len(a):
            break
    return r


def dot(a: list[int], b: list[int]) -> int:
    return sum(x * y for x, y in zip(a, b)) % 3


def triple(a: list[int], b: list[int], c: list[int]) -> int:
    return sum(x * y * z for x, y, z in zip(a, b, c)) % 3


def build_20_7_2() -> dict[str, Any]:
    m, k, n0 = 3, 7, 27
    w = [i % 3 for i in range(n0)]
    vs: list[list[int]] = []
    for a in range(1, 3 * m):
        row = [0] * n0
        for i in range(3 * (a - 1), 3 * a):
            row[i] = 1
        for i in range(n0 - 3, n0):
            row[i] = 2
        vs.append(row)

    # Paper uses 1-indexed coordinates 3j+1, 0 <= j < 3m-2.
    punctured = {3 * j for j in range(k)}
    keep = [i for i in range(n0) if i not in punctured]
    restrict = lambda row: [row[i] for i in keep]

    h1 = [restrict(v) for v in vs[:k]]
    h0 = [restrict(w), restrict(vs[k])]
    h = h1 + h0
    return {
        "m": m,
        "k": k,
        "punctured_1_indexed": [i + 1 for i in sorted(punctured)],
        "kept_1_indexed": [i + 1 for i in keep],
        "H1": h1,
        "H0": h0,
        "H": h,
    }


def z_logical_witnesses(h: list[list[int]], h0: list[list[int]]) -> dict[str, Any]:
    n = len(h[0])
    result: dict[str, Any] = {"weight1": None, "weight2": None}
    for weight in (1, 2):
        for support in itertools.combinations(range(n), weight):
            for values in itertools.product((1, 2), repeat=weight):
                z = [0] * n
                for q, value in zip(support, values):
                    z[q] = value
                if all(dot(row, z) == 0 for row in h0) and any(dot(row, z) != 0 for row in h):
                    result[f"weight{weight}"] = {
                        "support_0_indexed": list(support),
                        "values": list(values),
                        "vector": z,
                    }
                    break
            if result[f"weight{weight}"] is not None:
                break
    return result


def repo_adapter_audit() -> dict[str, Any]:
    canonical_map_paths = [
        ROOT / "data/w33_qutrit_20_7_2_encoding.json",
        ROOT / "analysis/w33_qutrit_20_7_2_encoding.py",
    ]
    decoder_paths = [
        ROOT / "analysis/w33_qutrit_20_7_2_packet_decoder.py",
        ROOT / "data/w33_qutrit_20_7_2_packet_decoder.json",
    ]
    threshold_paths = [
        ROOT / "analysis/w33_qutrit_20_7_2_threshold.py",
        ROOT / "data/w33_qutrit_20_7_2_threshold.json",
    ]
    explicit_map_present = any(p.exists() for p in canonical_map_paths)
    mapped_decoder_present = any(p.exists() for p in decoder_paths)
    mapped_threshold_present = any(p.exists() for p in threshold_paths)

    pass78 = ROOT / "w33_pass78_equivariant_closure.json"
    pass78_text = pass78.read_text(encoding="utf-8") if pass78.exists() else ""
    substrate_66_witness_missing = (
        "does not find or construct a canonical [[66,8,3]]_3 generator/stabilizer witness" in pass78_text
    )

    standin = ROOT / "analysis/holonet_qec_demo.py"
    standin_text = standin.read_text(encoding="utf-8") if standin.exists() else ""
    exact_5_qutrit_standin_present = "[[5,1,3]]_3" in standin_text

    tport = ROOT / "analysis/w33_qutrit_t_teleportation_port.py"
    magic_scheduler = ROOT / "analysis/w33_magic_resource_scheduler.py"

    blockers = []
    if not explicit_map_present:
        blockers.append("no explicit 20-physical-qutrit W33 selector/intertwiner artifact")
    if substrate_66_witness_missing:
        blockers.append("the architecture's cited [[66,8,3]]_3 substrate still lacks a canonical generator/stabilizer witness in the audited spine")
    if not mapped_decoder_present:
        blockers.append("no mapped [[20,7,2]]_3 stabilizer-measurement/decoder packet compiler")
    if not mapped_threshold_present:
        blockers.append("no mapped distillation noise/threshold certificate for the W33/Holonet implementation")

    return {
        "explicit_encoding_map_present": explicit_map_present,
        "mapped_packet_decoder_present": mapped_decoder_present,
        "mapped_threshold_certificate_present": mapped_threshold_present,
        "canonical_map_paths": [str(p.relative_to(ROOT)) for p in canonical_map_paths],
        "mapped_decoder_paths": [str(p.relative_to(ROOT)) for p in decoder_paths],
        "mapped_threshold_paths": [str(p.relative_to(ROOT)) for p in threshold_paths],
        "exact_single_qutrit_t_port_present": tport.exists(),
        "magic_scheduler_present": magic_scheduler.exists(),
        "exact_5_qutrit_standin_present": exact_5_qutrit_standin_present,
        "substrate_66_canonical_witness_missing": substrate_66_witness_missing,
        "blockers": blockers,
        "adapter_enabled": explicit_map_present and mapped_decoder_present and mapped_threshold_present and not substrate_66_witness_missing,
    }


def verify() -> dict[str, Any]:
    code = build_20_7_2()
    h, h1, h0 = code["H"], code["H1"], code["H0"]
    n = len(h[0])
    rank_h = mod3_rank(h)
    rank_h0 = mod3_rank(h0)
    logical_k = n - rank_h0 - (n - rank_h)

    pairwise_offdiag = all(dot(h[i], h[j]) == 0 for i in range(len(h)) for j in range(i + 1, len(h)))
    distinct_triples = all(triple(h[i], h[j], h[k]) == 0 for i in range(len(h)) for j in range(i + 1, len(h)) for k in range(j + 1, len(h)))
    cubic_norms = [sum(x ** 3 for x in row) % 3 for row in h]
    logical = z_logical_witnesses(h, h0)
    audit = repo_adapter_audit()

    checks = {
        "published_puncture_gives_9x20_matrix": len(h) == 9 and n == 20,
        "seven_logical_rows_two_x_stabilizer_rows": len(h1) == 7 and len(h0) == 2,
        "rank_H_is_9": rank_h == 9,
        "rank_H0_is_2": rank_h0 == 2,
        "css_encodes_7_qutrits": logical_k == 7,
        "H0_is_self_orthogonal": all(dot(a, b) == 0 for a in h0 for b in h0),
        "distinct_rows_are_pairwise_orthogonal": pairwise_offdiag,
        "distinct_triple_products_vanish": distinct_triples,
        "seven_logical_rows_have_nonzero_cubic_norm": cubic_norms[:7] == [2] * 7 and cubic_norms[7:] == [0, 0],
        "no_weight1_Z_logical": logical["weight1"] is None,
        "weight2_Z_logical_exists": logical["weight2"] is not None,
        "w33_adapter_remains_fail_closed": not audit["adapter_enabled"],
    }

    return {
        "schema": "w33.qutrit-20-7-2-adapter-audit.v2",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "external_code": {
            "parameters": "[[20,7,2]]_3",
            "source": "Prakash--Saha, Quantum 9, 1768 (2025), construction T_m with m=3,k=7",
            "punctured_coordinates_1_indexed": code["punctured_1_indexed"],
            "rank_H": rank_h,
            "rank_H0": rank_h0,
            "logical_qutrits": logical_k,
            "cubic_norms": cubic_norms,
            "weight2_logical_Z_witness": logical["weight2"],
        },
        "w33_adapter_audit": audit,
        "checks": checks,
        "decision": "REFUSE_FAULT_TOLERANT_ADAPTER",
        "interpretation": "The external [[20,7,2]]_3 triorthogonal code is reconstructed and verified exactly, but the repository does not yet contain the W33 physical-coordinate/stabilizer intertwiner, mapped packet decoder, and mapped threshold evidence required to call it a Holonet FT magic factory.",
        "next_required_witness": "Provide a 20-coordinate W33/Holonet selector plus an explicit map carrying H0/H1 into physical stabilizer/logical operators, compile its syndrome/distillation circuit to packets, and measure/prove a noise threshold for that mapped circuit.",
    }


if __name__ == "__main__":
    payload = verify()
    print(json.dumps(payload, indent=2))
    raise SystemExit(0 if payload["status"] == "PASS" else 1)
