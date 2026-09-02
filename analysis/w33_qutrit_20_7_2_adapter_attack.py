#!/usr/bin/env python3
"""Exact reconstruction and W33-adapter audit for the [[20,7,2]]_3 code.

The external Prakash--Saha code is reconstructed exactly. The W33 spine now
contains four deliberately separated evidence classes:

* literal 20-edge monomial/zero-extension CSS embedding: proved impossible;
* general GF(3)-linear symplectic embedding: explicit and exact;
* W33 edge-line-graph routing plus mapped syndrome/decoder: executable;
* calibrated optical locality and a physical stochastic threshold: still open.

A topological route compiler or a phenomenological pseudothreshold experiment is
not silently promoted into a physical fault-tolerance certificate. FT admission
also remains blocked by the separately audited missing canonical [[66,8,3]]_3
substrate witness.
"""
from __future__ import annotations

import itertools
import json
from pathlib import Path
from typing import Any

import w33_qutrit_20_7_2_edge_css_no_go as edge_nogo
import w33_qutrit_20_7_2_symplectic_embedding as symembed

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
        if a[r][c] == 2:
            a[r] = [(2 * x) % 3 for x in a[r]]
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
    punctured = {3 * j for j in range(k)}
    keep = [i for i in range(n0) if i not in punctured]
    restrict = lambda row: [row[i] for i in keep]
    h1 = [restrict(v) for v in vs[:k]]
    h0 = [restrict(w), restrict(vs[k])]
    return {
        "m": m,
        "k": k,
        "punctured_1_indexed": [i + 1 for i in sorted(punctured)],
        "kept_1_indexed": [i + 1 for i in keep],
        "H1": h1,
        "H0": h0,
        "H": h1 + h0,
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
    # Local imports are intentional. packet_decoder imports build_20_7_2 from
    # this module; by the time this audit executes the module is fully loaded,
    # avoiding import-time recursion while allowing executable evidence checks.
    import w33_qutrit_20_7_2_w33_route_compiler as route_compiler
    import w33_qutrit_20_7_2_packet_decoder as packet_decoder
    import w33_qutrit_20_7_2_threshold as threshold_experiment

    literal_no_go = edge_nogo.verify()
    literal_class_impossible = (
        literal_no_go.get("status") == "PASS"
        and literal_no_go.get("decision") == "UNSAT_LITERAL_CSS_MONOMIAL_20_TO_240"
    )
    symplectic = symembed.verify()
    symplectic_verified = symplectic.get("status") == "PASS" and symplectic.get("checks", {}).get("ABt_identity") is True

    route_cert = route_compiler.verify()
    decoder_cert = packet_decoder.verify()
    threshold_cert = threshold_experiment.verify()
    topological_locality_verified = (
        route_cert.get("status") == "PASS"
        and route_cert.get("checks", {}).get("every_two_qutrit_primitive_is_line_graph_local") is True
    )
    mapped_decoder_verified = decoder_cert.get("status") == "PASS"
    pseudothreshold_verified = threshold_cert.get("status") == "PASS"

    # These remain deliberately false. The route compiler proves locality on an
    # abstract shared-W33-point interaction graph; the threshold script itself
    # says it is phenomenological. Neither is a calibrated optical certificate.
    locality_optical_compiler_verified = False
    mapped_threshold_certificate_present = False

    pass78 = ROOT / "w33_pass78_equivariant_closure.json"
    pass78_text = pass78.read_text(encoding="utf-8") if pass78.exists() else ""
    substrate_66_witness_missing = (
        "does not find or construct a canonical [[66,8,3]]_3 generator/stabilizer witness" in pass78_text
    )

    standin = ROOT / "analysis/holonet_qec_demo.py"
    standin_text = standin.read_text(encoding="utf-8") if standin.exists() else ""
    tport = ROOT / "analysis/w33_qutrit_t_teleportation_port.py"
    magic_scheduler = ROOT / "analysis/w33_magic_resource_scheduler.py"

    blockers = []
    if not symplectic_verified:
        blockers.append("general nonlocal symplectic [[20,7,2]]_3 -> W33 edge-CSS embedding did not verify")
    if not topological_locality_verified:
        blockers.append("W33 shared-point nearest-neighbour route compiler did not verify")
    if not locality_optical_compiler_verified:
        blockers.append("topological W33 routing is not yet a calibrated optical locality/noise-propagation certificate")
    if not mapped_decoder_verified:
        blockers.append("mapped [[20,7,2]]_3 syndrome/decoder certificate did not verify")
    if pseudothreshold_verified and not mapped_threshold_certificate_present:
        blockers.append("routed-exposure pseudothreshold experiment exists, but no calibrated physical mapped threshold certificate exists")
    elif not pseudothreshold_verified:
        blockers.append("mapped routed-exposure pseudothreshold experiment did not verify")
    if substrate_66_witness_missing:
        blockers.append("the architecture's cited [[66,8,3]]_3 substrate still lacks a canonical generator/stabilizer witness in the audited spine")

    adapter_enabled = (
        symplectic_verified
        and locality_optical_compiler_verified
        and mapped_decoder_verified
        and mapped_threshold_certificate_present
        and not substrate_66_witness_missing
    )
    return {
        "explicit_encoding_map_present": symplectic_verified,
        "general_nonlocal_symplectic_embedding_verified": symplectic_verified,
        "general_nonlocal_symplectic_embedding": symplectic,
        "topological_w33_route_compiler_verified": topological_locality_verified,
        "topological_w33_route_certificate": route_cert,
        "locality_optical_compiler_verified": locality_optical_compiler_verified,
        "mapped_packet_decoder_present": (ROOT / "analysis/w33_qutrit_20_7_2_packet_decoder.py").exists(),
        "mapped_packet_decoder_verified": mapped_decoder_verified,
        "mapped_packet_decoder_certificate": decoder_cert,
        "mapped_pseudothreshold_experiment_present": (ROOT / "analysis/w33_qutrit_20_7_2_threshold.py").exists(),
        "mapped_pseudothreshold_experiment_verified": pseudothreshold_verified,
        "mapped_pseudothreshold_experiment": threshold_cert,
        "mapped_threshold_certificate_present": mapped_threshold_certificate_present,
        "literal_edge_css_monomial_no_go": literal_no_go,
        "literal_edge_css_monomial_class_impossible": literal_class_impossible,
        "closed_embedding_class": "20-edge monomial/zero-extension CSS X->X",
        "surviving_ft_frontier": "calibrate the verified shared-W33-point route primitives, add fault-propagating syndrome/readout noise and a physical threshold certificate, and supply the missing canonical [[66,8,3]]_3 substrate witness",
        "mapped_decoder_paths": ["analysis/w33_qutrit_20_7_2_packet_decoder.py"],
        "mapped_threshold_experiment_paths": ["analysis/w33_qutrit_20_7_2_threshold.py"],
        "physical_threshold_certificate_paths": ["data/w33_qutrit_20_7_2_physical_threshold.json"],
        "exact_single_qutrit_t_port_present": tport.exists(),
        "magic_scheduler_present": magic_scheduler.exists(),
        "exact_5_qutrit_standin_present": "[[5,1,3]]_3" in standin_text,
        "substrate_66_canonical_witness_missing": substrate_66_witness_missing,
        "blockers": blockers,
        "adapter_enabled": adapter_enabled,
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
        "literal_edge_css_monomial_class_closed_by_no_go": audit["literal_edge_css_monomial_class_impossible"],
        "general_nonlocal_symplectic_embedding_exists": audit["general_nonlocal_symplectic_embedding_verified"],
        "topological_w33_routing_exists": audit["topological_w33_route_compiler_verified"],
        "mapped_decoder_exists_and_verifies": audit["mapped_packet_decoder_verified"],
        "pseudothreshold_experiment_exists_but_is_not_physical_certificate": audit["mapped_pseudothreshold_experiment_verified"] and not audit["mapped_threshold_certificate_present"],
        "w33_ft_adapter_remains_fail_closed": not audit["adapter_enabled"],
    }
    return {
        "schema": "w33.qutrit-20-7-2-adapter-audit.v5",
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
        "decision": "REFUSE_FAULT_TOLERANT_ADAPTER_PENDING_OPTICAL_LOCALITY_PHYSICAL_THRESHOLD_AND_66_SUBSTRATE",
        "interpretation": "The code, nonlocal symplectic embedding, topological W33 route compiler, and fail-closed mapped decoder now verify. A routed-exposure pseudothreshold experiment is present but is explicitly not a calibrated physical threshold. Fault-tolerant admission therefore remains refused, additionally preserving the separate [[66,8,3]]_3 substrate blocker.",
        "next_required_witness": "Calibrate the shared-W33-point primitive interaction and syndrome/readout path, propagate a physical qutrit loss/leakage/depolarizing model through that circuit to a threshold certificate, and close the canonical [[66,8,3]]_3 substrate witness.",
    }


if __name__ == "__main__":
    payload = verify()
    print(json.dumps(payload, indent=2))
    raise SystemExit(0 if payload["status"] == "PASS" else 1)
