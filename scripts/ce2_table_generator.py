#!/usr/bin/env python3
"""Regenerate CE2 simple-family coefficient tables from a single seed.

This script implements the table-free theorem described in the notes: every
polynomial pair (e,c0) is obtained from the seed direction d0=(1,0) by
lifting a symplectic transport on the Heisenberg coordinates and applying the
standard Weil normalization.  No lookup tables are used; the only inputs are

* the seed polynomials already present in ``ce2_global_cocycle``
* the 24 symplectic matrices from ``grade_weil_phase``
* the canonical quadratic refinement f(x,y)=2xy used by that module

Running the script prints a verification that the regenerated tables match the
hard-coded constants.  It also exposes the decoding rule for CE2 keys and
emphasises the t=1/t=2 regime condition.
"""

from __future__ import annotations

from itertools import product
from fractions import Fraction

try:
    # Prefer package-relative import when used as a module; fall back to
    # absolute import for direct script execution.
    from .ce2_global_cocycle import (
        _SIMPLE_FAMILY_WEIL_E_COEFF,
        _SIMPLE_FAMILY_WEIL_C0_COEFF,
        _f3_dot,
        _f3_omega,
        _f3_chi,
        _eval_f3_poly_sw,
        all_symplectic_matrices,
        compute_phase,
        apply_matrix,
        matinv,
    )
except Exception:  # pragma: no cover - fallback for direct script execution
    from scripts.ce2_global_cocycle import (
        _SIMPLE_FAMILY_WEIL_E_COEFF,
        _SIMPLE_FAMILY_WEIL_C0_COEFF,
        _f3_dot,
        _f3_omega,
        _f3_chi,
        _eval_f3_poly_sw,
        all_symplectic_matrices,
        compute_phase,
        apply_matrix,
        matinv,
    )

# finite-field helpers -------------------------------------------------------

def inv3(x: int) -> int:
    assert x % 3 in (1, 2)
    return x % 3  # 1^{-1}=1, 2^{-1}=2

F3 = [0, 1, 2]

# CE2 decoding ---------------------------------------------------------------

def decode_key_triplet(k: str) -> tuple[tuple[int, int], tuple[int, int], tuple[int, int]]:
    """Return ((c_i,c_j),(match_i,match_j),(other_i,other_j))."""
    parts = k.split(":")
    if len(parts) != 3:
        raise ValueError(f"bad key: {k}")
    def parse(p: str):
        a, b = p.split(",")
        return (int(a), int(b))
    return parse(parts[0]), parse(parts[1]), parse(parts[2])


def key_to_heisenberg(k: str) -> tuple[tuple[int,int,int], tuple[int,int,int], tuple[int,int,int]]:
    """Given a CE2 key compute (u_c,z_c),(u_m,z_m),(u_o,z_o) vectors."""
    from scripts.ce2_global_cocycle import _heisenberg_vec_maps
    e6id_to_vec, _ = _heisenberg_vec_maps()
    (c_i, _), (m_i, _), (o_i, _) = decode_key_triplet(k)
    return e6id_to_vec[c_i], e6id_to_vec[m_i], e6id_to_vec[o_i]


def determine_t(uc, um, uo) -> int:
    """t=1 iff u_m == u_o, else t=2."""
    return 1 if (um[0], um[1]) == (uo[0], uo[1]) else 2

# coordinate conversions ----------------------------------------------------

def sw_from_uc(uc: tuple[int, int], d: tuple[int,int]) -> tuple[int,int]:
    return (_f3_dot(uc, d), _f3_omega(uc, d))


def uc_from_sw(s: int, w: int, d: tuple[int,int]) -> tuple[int,int]:
    d1, d2 = d
    N = (d1*d1 + d2*d2) % 3
    Ninv = inv3(N)
    u1 = (Ninv*(s*d1 - w*d2)) % 3
    u2 = (Ninv*(s*d2 + w*d1)) % 3
    return (u1, u2)

# CE2 points rule (from conversation) --------------------------------------

def ce2_uv_from_uc(uc: tuple[int,int], d: tuple[int,int], t: int):
    """Return (u_m,u_o) according to t rule used in repo.

    t=1: u_m == u_o == u_c + d
    t=2: u_m = u_c + d, u_o = u_c
    """
    um = ((uc[0] + d[0]) % 3, (uc[1] + d[1]) % 3)
    uo = um if t == 1 else uc
    return um, uo

# mu cochain, explicit formula ---------------------------------------------

def mu_of_A(A: tuple[tuple[int,int],tuple[int,int]], u: tuple[int,int]) -> int:
    (a,b),(c,d) = A
    x,y = u
    term = (a*c*x*x + (a*d + b*c - 1)*x*y + b*d*y*y) % 3
    return (2*term) % 3

# generator -----------------------------------------------------------------

def regenerate_tables() -> dict[int, dict[tuple[int,int], dict[tuple[int,int],tuple[int,int,int]]]]:
    """Return dict[t][d][(s,w)] = (e,c0,bB) reproducing repo data."""
    d0 = (1,0)
    results = {1: {}, 2: {}}
    for t in (1, 2):
        for d in [(i,j) for i,j in product(F3,F3) if (i,j)!=(0,0)]:
            # choose a symplectic A with A*d0 == d
            A = next(M for M in all_symplectic_matrices() if apply_matrix(M, d0) == d)
            B = matinv(A)
            import numpy as _np
            B = _np.array(B, dtype=int)
            mu_B = compute_phase(A)
            mu_B[(0,0)] = 0
            table = {}
            for s, w in product(F3,F3):
                uc = uc_from_sw(s,w,d)
                s0, w0 = sw_from_uc(apply_matrix(B, uc), d0)
                e0 = _eval_f3_poly_sw(s0, w0, _SIMPLE_FAMILY_WEIL_E_COEFF[t][d0])
                c00 = _eval_f3_poly_sw(s0, w0, _SIMPLE_FAMILY_WEIL_C0_COEFF[t][d0])
                um, uo = ce2_uv_from_uc(uc, d, t)
                dz = (mu_B.get(um,0) + mu_B.get(uo,0)) % 3
                bB = B[0][1]
                table[(s,w)] = (e0, (c00+dz)%3, bB)
            results[t][d] = table
    return results


def verify_against_repo():
    regen = regenerate_tables()
    mismatches = []
    for t,d in regen.items():
        for dvec, table in d.items():
            repo_e = _SIMPLE_FAMILY_WEIL_E_COEFF[t][dvec]
            repo_c0 = _SIMPLE_FAMILY_WEIL_C0_COEFF[t][dvec]
            for s,w in product(F3,F3):
                e,c0,bB = table[(s,w)]
                e_repo = _eval_f3_poly_sw(s,w,repo_e)
                c0_repo = _eval_f3_poly_sw(s,w,repo_c0)
                if e != e_repo or c0 != c0_repo:
                    mismatches.append((t,dvec,s,w,e,c0,e_repo,c0_repo))
    return mismatches


if __name__ == "__main__":
    mism = verify_against_repo()
    if not mism:
        print("All tables regenerated exactly — no lookups remain.")
    else:
        print("Mismatches detected:")
        for m in mism[:10]:
            print(m)
        print(f"({len(mism)} total mismatches)")
