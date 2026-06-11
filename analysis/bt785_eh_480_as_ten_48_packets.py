#!/usr/bin/env python3
"""
BT785 - The 480 action as ten order-48 local packets.

GraphTheory.txt records five independent W33 derivations of the same action
number:

    2E = 480
    3T = 480
    Tr(A^2) = vk = 480
    Tr(L0) = vk = 480
    curvature integral = (1/kappa) * sum R = 6 * 80 = 480

BT781 found order 48 as the local cube/tomotope exchange unit.  BT785 records
and verifies the packet identity:

    480 = 10 * 48

where 10 is simultaneously k-r, the spectral gap, SO(10) vector dimension in
repo language, and the number of 48-packets needed to tile the directed-edge /
curvature action.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    q = 3
    v = 40
    k = 12
    lam = 2
    mu = 4
    edges = 240
    triangles = 160
    r = 2
    s = -4
    kappa_inv = 6
    vertex_scalar_curvature = 2
    total_scalar_curvature = v * vertex_scalar_curvature
    packet = 48

    derivations = {
        "directed_edges": 2 * edges,
        "oriented_triangles": 3 * triangles,
        "closed_2_walks_trace_A2": v * k,
        "vertex_laplacian_trace_L0": v * k,
        "curvature_integral": kappa_inv * total_scalar_curvature,
    }
    assert set(derivations.values()) == {480}

    gap = k - r
    assert gap == 10
    assert 480 == gap * packet
    assert packet == 4 * k
    assert packet == 2 * 24
    assert packet == 12 * mu
    assert packet == 16 * q
    assert packet == (q + 1) * k

    packets = {
        name: value // packet for name, value in derivations.items()
    }
    assert set(packets.values()) == {10}

    out = {
        "theorem": "BT785 EH action 480 equals ten local 48 packets",
        "W33_parameters": {"q": q, "v": v, "k": k, "lambda": lam, "mu": mu, "r": r, "s": s},
        "five_480_derivations": derivations,
        "local_packet_48": {
            "value": packet,
            "cube_chart_stabilizer": "BT781 Aut(Q3)=C2^3:S3 has order 48",
            "tomotope_derived_half": "BT781 Gamma(T)'=C2^4:C3 has order 48",
            "factorizations": {
                "4*k": 4 * k,
                "2*24": 2 * 24,
                "12*mu": 12 * mu,
                "16*q": 16 * q,
                "(q+1)*k": (q + 1) * k
            }
        },
        "packetization": {
            "spectral_gap_k_minus_r": gap,
            "480_as_gap_times_packet": "480 = (k-r) * 48 = 10 * 48",
            "packets_per_derivation": packets
        },
        "interpretation": {
            "short": "The W33 action quantum is ten copies of the cube/tomotope 48-unit.",
            "why_10": "10 = k-r is the W33 spectral gap and the repo SO(10)-vector slot.",
            "why_48": "48 is the local exchange unit between cube transport and tomotope orientation."
        }
    }

    path = ROOT / "data" / "bt785_eh_480_as_ten_48_packets.json"
    path.parent.mkdir(exist_ok=True)
    with path.open("w") as f:
        json.dump(out, f, indent=2)

    print("BT785 480 = 10 * 48")
    print(json.dumps(out, indent=2))
    print(f"wrote {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
