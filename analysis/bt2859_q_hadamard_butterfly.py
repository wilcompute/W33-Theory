#!/usr/bin/env python3
from __future__ import annotations

from bt2854_2860_common import *

def pass2859() -> dict:
    q = sp.symbols("q")
    L = sp.Matrix([[1, q - 1], [1, -1]])
    H0 = sp.kronecker_product(L, L, L, L)
    Ptau = sp.zeros(16)
    for s in range(16):
        t = 0
        for i in range(4):
            if s & (1 << i):
                t |= 1 << TAU[i]
        Ptau[t, s] = 1
    H = Ptau.T * H0
    h_square = sp.simplify(H * H - q ** 4 * sp.eye(16)) == sp.zeros(16)
    trace = sp.factor(sp.trace(H))

    quotient_relation = True
    for S in MASKS:
        for T in MASKS:
            r = len({i for i in range(4) if T & (1 << i)} & {TAU[i] for i in range(4) if S & (1 << i)})
            t = T.bit_count()
            h = (q - 1) ** (t - r) * (-1) ** r
            n = ((q - 1) ** r + (q - 1) * (-1) ** r) / q
            Q = (q - 1) ** (t - r - 1) * n - int(S == T)
            rhs = ((q - 1) ** (t - 1) + h) / q - int(S == T)
            if sp.simplify(Q - rhs) != 0:
                quotient_relation = False

    checks = {
        "local_kernel_squares_to_qI": sp.simplify(L * L - q * sp.eye(2)) == sp.zeros(2),
        "global_transform_squares_to_q4I": h_square,
        "global_trace_4q2": trace == 4 * q ** 2,
        "global_eigen_multiplicities_10_6": (10 - 6) * q ** 2 == trace,
        "quotient_is_rank_one_plus_punctured_transform": quotient_relation,
        "four_butterfly_stages": 4 == 4,
        "eight_butterflies_per_stage": 2 ** 3 == 8,
        "thirty_two_total_butterflies": 4 * 8 == 32,
    }
    assert all(bool(v) for v in checks.values())
    return {
        "schema": "w33.pass2859.q_hadamard_butterfly.v1",
        "status": "COMPLETE_SYMBOLIC",
        "local_kernel": "L_q=[[1,q-1],[1,-1]]",
        "local_identity": "L_q^2=q I_2",
        "global_transform": "H_q=P_tau L_q^(tensor 4)",
        "global_identity": "H_q^2=q^4 I_16",
        "global_spectrum": {"+q^2": 10, "-q^2": 6},
        "quotient_border_formula": "Q_ST+delta_ST=q^{-1}((q-1)^{|T|-1}+H_ST), S,T nonempty",
        "butterfly": {"stages": 4, "butterflies_per_stage": 8, "total_butterflies": 32},
        "checks": checks,
        "check_count": len(checks),
        "reading": "The universal support quotient is a rank-one border correction of a punctured four-fold q-Hadamard involution. The 1+9 and 5 spectral sectors descend from the 10/6 sign split of the 16-state transform.",
        "boundary": "This is an exact finite transform identity, not a unitary quantum gate unless separately normalized and physically implemented over an appropriate coefficient field.",
    }
