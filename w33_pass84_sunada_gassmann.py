#!/usr/bin/env python3
"""
Pass 84 -- W(3,3) and Q(4,3) are a Sunada-Gassmann pair.

Kac asked "can you hear the shape of a drum?"; Sunada gave isospectral, non-isometric manifolds
from Gassmann-equivalent (almost-conjugate) subgroups, and Perlis studied arithmetically
equivalent number fields (identical Dedekind zeta).  The cospectral, locally identical,
non-isomorphic pair W(3,3) / Q(4,3) (Pass 76) is the exact graph instance of this phenomenon, and
Passes 82/83 pin down what you CAN and CANNOT hear.

This pass verifies the four faces of "you cannot hear the shape" for the pair, directly:

  T1  Identical Ihara zeta: the non-backtracking counts N_m = Tr(B^m) agree for both graphs, all m
      (computed on both 480x480 Hashimoto operators, m=1..12).  Same zeta => same primes, same RH,
      same functional equation.
  T2  Identical spectral zeta: zeta_L(s) = sum_{lambda>0} lambda^{-s} over Laplacian eigenvalues is
      the same for both; its special values zeta_L(0)=n-1=39, zeta_L(-1)=2m=480, and the
      regularized determinant det'(L)=n*kappa are identical.
  T3  SAME class number kappa = 2^81*5^23 = #spanning trees, but DIFFERENT class group: the
      critical groups K(W) and K(Q) are non-isomorphic (Pass 82) -- the Gassmann phenomenon, where
      the arithmetic (class group) hears what the zeta cannot.
  T4  Hearing hierarchy: adjacency/Ihara/Bartholdi spectrum -- deaf; local neighbourhood/mu-graph
      -- deaf (Pass 76); ovoid number -- hears (7 vs 10, Pass 77); critical group -- hears (2-Sylow,
      Pass 82).

Self-contained on the committed Pass 73/76/82 spine.  ASCII-only.
"""
from __future__ import annotations

import json
from math import prod
from pathlib import Path

import numpy as np

from w33_pass73_prime_geodesics import build_graph, build_hashimoto
from w33_pass76_cospectral_mates import build_Q43

ROOT = Path(__file__).resolve().parent


def N_trace(A, maxm=12):
    _, B = build_hashimoto(A)
    Bp = np.identity(B.shape[0], dtype=np.int64)
    out = {}
    for m in range(1, maxm + 1):
        Bp = Bp @ B
        out[m] = int(np.trace(Bp))
    return out


def laplacian_spectral_zeta(A):
    """Laplacian eigenvalues (integers) and spectral-zeta special values."""
    lap = 12 * np.eye(A.shape[0]) - A
    ev = sorted(int(round(x)) for x in np.linalg.eigvalsh(lap))
    nonzero = [x for x in ev if x != 0]
    n = A.shape[0]
    # zeta_L(0) = # nonzero eigenvalues; zeta_L(-1) = sum of eigenvalues; det' = product
    return {
        "num_zero_eigenvalues": ev.count(0),
        "zeta_L_at_0": len(nonzero),  # = n-1 for a connected graph
        "zeta_L_at_minus_1": sum(nonzero),  # = 2m (trace of Laplacian)
        "regularized_det_prime_L": prod(nonzero),  # = n * kappa (Matrix-Tree)
    }


def main():
    _, Aw = build_graph()
    _, Aq = build_Q43()

    # T1 -- identical Ihara N_m
    Nw = N_trace(Aw, 12)
    Nq = N_trace(Aq, 12)
    ihara_identical = Nw == Nq

    # T2 -- identical spectral zeta special values
    zw = laplacian_spectral_zeta(Aw)
    zq = laplacian_spectral_zeta(Aq)
    spectral_zeta_identical = zw == zq
    kappa = zw["regularized_det_prime_L"] // 40  # det'(L) = n*kappa
    n = 40
    m_edges = 240

    # T3 -- same class number, different class group (from Pass 82)
    p82 = json.loads((ROOT / "w33_pass82_critical_group.json").read_text())
    KW = p82["critical_group_W33"]["invariant_factors"]
    KQ = p82["critical_group_Q43"]["invariant_factors"]
    same_class_number = (
        p82["critical_group_W33"]["order"] == p82["critical_group_Q43"]["order"]
    )
    different_class_group = KW != KQ

    checks = {
        "T1_identical_Ihara_zeta_N_m": ihara_identical,
        "T2_identical_spectral_zeta": spectral_zeta_identical,
        "T2_zeta_L_0_is_n_minus_1_39": zw["zeta_L_at_0"] == n - 1 == 39,
        "T2_zeta_L_minus1_is_2m_480": zw["zeta_L_at_minus_1"] == 2 * m_edges == 480,
        "T2_det_prime_L_is_n_kappa": zw["regularized_det_prime_L"] == n * kappa,
        "T3_same_class_number": same_class_number,
        "T3_different_class_group": different_class_group,
        "T3_class_number_is_2^81_5^23": kappa == (2**81) * (5**23),
    }
    all_ok = all(checks.values())

    hearing = [
        ["adjacency / Ihara / Bartholdi spectrum", "DEAF (identical)"],
        ["spectral zeta special values", "DEAF (identical)"],
        ["local neighbourhood + mu-graph (Pass 76)", "DEAF (both 4K3 / 4K1)"],
        ["class number kappa (spanning trees)", "DEAF (both 2^81*5^23)"],
        ["ovoid number alpha (Pass 77)", "HEARS (7 vs 10)"],
        ["critical group / class group (Pass 82)", "HEARS (2-Sylow differs)"],
    ]

    print("=" * 74)
    print("PASS 84 -- W(3,3) AND Q(4,3): A SUNADA-GASSMANN PAIR")
    print("=" * 74)
    print(f"[T1] identical Ihara N_m for m=1..12: {ihara_identical}")
    print(f"     N_3={Nw[3]} N_5={Nw[5]} N_12={Nw[12]} (both graphs)")
    print(f"[T2] spectral zeta identical: {spectral_zeta_identical}")
    print(
        f"     zeta_L(0)={zw['zeta_L_at_0']}=n-1  zeta_L(-1)={zw['zeta_L_at_minus_1']}=2m  "
        f"det'(L)={zw['regularized_det_prime_L']}=n*kappa"
    )
    print(
        f"[T3] SAME class number kappa=2^81*5^23; DIFFERENT class group: {different_class_group}"
    )
    print(f"     K(W) factors {KW}")
    print(f"     K(Q) factors {KQ}")
    print()
    print("Can you hear the shape of W(3,3)?  The hearing hierarchy:")
    for probe, verdict in hearing:
        print(f"   {probe:<44} {verdict}")
    print()
    print("checks:")
    for k, v in checks.items():
        print(f"   {'OK ' if v else 'XX '} {k}")
    print()
    print("=" * 74)
    print(f"STATUS: {'PASS' if all_ok else 'FAIL'}")
    print("=" * 74)

    payload = {
        "schema": "w33.pass84.sunada_gassmann.v1",
        "status": "PASS" if all_ok else "FAIL",
        "T1_ihara": {
            "N_m_W": {str(k): v for k, v in Nw.items()},
            "N_m_Q": {str(k): v for k, v in Nq.items()},
            "identical": ihara_identical,
        },
        "T2_spectral_zeta": {
            "W": zw,
            "Q": zq,
            "identical": spectral_zeta_identical,
            "special_values": {
                "zeta_L(0)": zw["zeta_L_at_0"],
                "zeta_L(-1)": zw["zeta_L_at_minus_1"],
                "det_prime_L": zw["regularized_det_prime_L"],
                "n_times_kappa": n * kappa,
            },
        },
        "T3_class_group": {
            "class_number_kappa": kappa,
            "same_class_number": same_class_number,
            "K_W": KW,
            "K_Q": KQ,
            "different_class_group": different_class_group,
        },
        "hearing_hierarchy": hearing,
        "reading": (
            "W(3,3) and Q(4,3) are the graph analogue of Sunada-isospectral manifolds / "
            "arithmetically equivalent number fields: identical Ihara AND spectral zeta and "
            "identical class number 2^81*5^23, yet different class group (critical group, "
            "2-Sylow). The arithmetic hears what the spectrum -- and even local geometry -- "
            "cannot; only the ovoid number and the critical group distinguish the pair."
        ),
        "checks": checks,
    }
    (ROOT / "w33_pass84_sunada_gassmann.json").write_text(json.dumps(payload, indent=2))
    print("[wrote] w33_pass84_sunada_gassmann.json")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
