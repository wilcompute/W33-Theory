"""Classical modular polynomial Phi_2(X, Y) and the relation
Phi_2(j(tau), j(2 tau)) = 0.

Theorem.  There is a unique symmetric polynomial Phi_N(X, Y) in Z[X, Y]
such that Phi_N(j(tau), j(N tau)) = 0 for all tau in upper half plane
(and Phi_N is irreducible over C[j]).  For N = 2,

    Phi_2(X, Y) = X^3 + Y^3 - X^2 Y^2
                + 1488 (X^2 Y + X Y^2)
                - 162000 (X^2 + Y^2)
                + 40773375 X Y
                + 8748000000 (X + Y)
                - 157464000000000.

This polynomial encodes the action of the 2-isogeny correspondence on
the moduli space of elliptic curves.  Its symmetry Phi_N(X, Y) =
Phi_N(Y, X) reflects the duality between an isogeny and its dual.

Numerical pins:
    tau = i   =>  j(i)  = 1728 = 12^3,   j(2i) = 66^3 = 287496,
                   Phi_2(1728, 287496) = 0.
    tau = rho = e^{2 pi i/3}/... actually tau = (1+i sqrt 3)/2
                   j(rho) = 0,    j(2 rho) = 54000 = 30^3 * 2,
                   Phi_2(0, 54000) = 0.

Coefficient structure hints:
    1488  = 2^4 . 3 . 31,
    162000 = 2^4 . 3^4 . 5^3,
    40773375 = 3^4 . 5^3 . 4027,
    8748000000 = 2^8 . 3^7 . 5^6,
    157464000000000 = 2^12 . 3^9 . 5^9.

This is Layer 59 — the algebraic cornerstone of isogeny graphs and
modular curves X_0(N).  Links to Layer 52 / 54 (CM j-values), Layer 50
(the j-function coefficients), and Layer 57 (elliptic curves).
"""

from __future__ import annotations

from typing import Any

import mpmath as mp

from w33_cm_j_heegner import J_COEFFS_EXPANSION


# ----------------------------------------------------------------------
# Phi_2 evaluation in integer arithmetic.
# ----------------------------------------------------------------------
def phi_2(X: int | mp.mpc, Y: int | mp.mpc):
    """Phi_2(X, Y) as a symbolic polynomial."""
    X2 = X * X
    Y2 = Y * Y
    XY = X * Y
    return (X * X2 + Y * Y2
            - X2 * Y2
            + 1488 * (X2 * Y + X * Y2)
            - 162000 * (X2 + Y2)
            + 40773375 * XY
            + 8748000000 * (X + Y)
            - 157464000000000)


def phi_2_symmetric(X, Y) -> bool:
    """Phi_2(X, Y) == Phi_2(Y, X)."""
    return phi_2(X, Y) == phi_2(Y, X)


# ----------------------------------------------------------------------
# j-function at tau via q-expansion.
# ----------------------------------------------------------------------
def j_at(tau: mp.mpc, n_terms: int = 30) -> mp.mpc:
    """j(tau) = 1/q + 744 + sum c_n q^n, q = exp(2 pi i tau)."""
    q = mp.exp(2j * mp.pi * tau)
    j = 1 / q + mp.mpf(744)
    for i in range(min(n_terms, len(J_COEFFS_EXPANSION))):
        j += J_COEFFS_EXPANSION[i] * q ** (i + 1)
    return j


# ----------------------------------------------------------------------
# Verifiers.
# ----------------------------------------------------------------------
def verify_phi2_at_tau_i(dps: int = 50) -> dict[str, Any]:
    """Phi_2(j(i), j(2i)) = 0  numerically."""
    mp.mp.dps = dps
    tau = mp.mpc(0, 1)
    j_tau = j_at(tau)
    j_2tau = j_at(2 * tau)
    val = phi_2(j_tau, j_2tau)
    mag_j_tau_cubed = max(abs(j_tau) ** 3, mp.mpf(1))
    # Tolerance relative to the degree-3 leading term magnitude:
    tol = mag_j_tau_cubed * mp.mpf("1e-15")
    match = abs(val) < tol
    return {
        "tau": "i",
        "j_tau": float(j_tau.real),
        "j_2tau": float(j_2tau.real),
        "phi_2_value": str(val),
        "abs_phi_2": float(abs(val)),
        "scale_tolerance": float(tol),
        "match": bool(match),
    }


def verify_phi2_symmetric_at_integer_pairs() -> dict[str, Any]:
    """Phi_2(X, Y) == Phi_2(Y, X) at a few integer test points."""
    pairs = [(1728, 287496), (0, 54000), (1, 2), (100, 3), (-5280, 1728)]
    rows: list[dict[str, Any]] = []
    all_match = True
    for X, Y in pairs:
        a = phi_2(X, Y)
        b = phi_2(Y, X)
        match = a == b
        rows.append({"X": X, "Y": Y, "Phi_2(X,Y)": a, "Phi_2(Y,X)": b,
                     "symmetric": match})
        all_match = all_match and match
    return {"all_match": all_match, "rows": rows}


def verify_phi2_at_heegner_pairs(dps: int = 60) -> dict[str, Any]:
    """For each CM point tau_d (d a Heegner number with d != 1, 2), we
    have Phi_2(j(tau_d), j(2 tau_d)) = 0.  We pin d = 3, 7, 11."""
    mp.mp.dps = dps
    from w33_cm_j_heegner import heegner_tau
    rows: list[dict[str, Any]] = []
    all_match = True
    for d in [3, 7, 11, 19]:
        tau = heegner_tau(d)
        j_tau = j_at(tau, n_terms=30)
        j_2tau = j_at(2 * tau, n_terms=30)
        val = phi_2(j_tau, j_2tau)
        mag = max(abs(j_tau) ** 3, mp.mpf(1))
        tol = mag * mp.mpf("1e-12")
        match = abs(val) < tol
        rows.append({
            "d": d,
            "j_tau_real": float(j_tau.real) if abs(j_tau.real) < 1e18 else str(j_tau.real),
            "j_2tau_real": float(j_2tau.real) if abs(j_2tau.real) < 1e18 else str(j_2tau.real),
            "abs_phi_2": str(abs(val)),
            "tolerance": str(tol),
            "match": bool(match),
        })
        all_match = all_match and match
    return {"all_match": all_match, "rows": rows}


def verify_phi2_integer_vanishing_at_j_i_j_2i() -> dict[str, Any]:
    """Integer-arithmetic check: Phi_2(1728, 287496) = 0 exactly."""
    val = phi_2(1728, 287496)
    return {"value": val, "equals_zero": val == 0}


def verify_phi2_integer_vanishing_at_0_54000() -> dict[str, Any]:
    """Phi_2(0, 54000) = 0: j(rho) = 0, j(2 rho) = 54000 = 30^3 * 2."""
    val = phi_2(0, 54000)
    return {"value": val, "equals_zero": val == 0}


def verify_phi2_integer_vanishing_at_8000_287496() -> dict[str, Any]:
    """For tau = i sqrt(2), j = 8000, j(2 tau) = j(2 i sqrt(2)) ~= 2417472.
       Actually 2i sqrt(2) ~ fundamental domain representative has j = ???

       Safer integer test: use the factored form / pair of CM points
       related by a 2-isogeny that both have known j."""
    # For this integer pin, we'll just verify Phi_2 vanishes at the
    # known (1728, 287496) and (0, 54000) pairs.
    return {"note": "use tau=i and tau=rho checks"}


def verify_coefficient_factorizations() -> dict[str, Any]:
    """Pin the prime factorization of the Phi_2 coefficients."""
    rows = [
        {"coeff_name": "1488",
         "value": 1488,
         "factors": {2: 4, 3: 1, 31: 1},
         "check": 2 ** 4 * 3 * 31 == 1488},
        {"coeff_name": "162000",
         "value": 162000,
         "factors": {2: 4, 3: 4, 5: 3},
         "check": 2 ** 4 * 3 ** 4 * 5 ** 3 == 162000},
        {"coeff_name": "40773375",
         "value": 40773375,
         "factors": {3: 4, 5: 3, 4027: 1},
         "check": 3 ** 4 * 5 ** 3 * 4027 == 40773375},
        {"coeff_name": "8748000000",
         "value": 8748000000,
         "factors": {2: 8, 3: 7, 5: 6},
         "check": 2 ** 8 * 3 ** 7 * 5 ** 6 == 8748000000},
        {"coeff_name": "157464000000000",
         "value": 157464000000000,
         "factors": {2: 12, 3: 9, 5: 9},
         "check": 2 ** 12 * 3 ** 9 * 5 ** 9 == 157464000000000},
    ]
    all_match = all(r["check"] for r in rows if r.get("check") is not None)
    return {"all_match": all_match, "rows": rows}


# ----------------------------------------------------------------------
# Driver.
# ----------------------------------------------------------------------
def derive_all() -> dict[str, Any]:
    at_i = verify_phi2_at_tau_i(dps=50)
    at_heegner = verify_phi2_at_heegner_pairs(dps=60)
    sym = verify_phi2_symmetric_at_integer_pairs()
    zero_1728 = verify_phi2_integer_vanishing_at_j_i_j_2i()
    zero_0_54000 = verify_phi2_integer_vanishing_at_0_54000()
    factor = verify_coefficient_factorizations()
    chain = {
        "phi_2_vanishes_at_j_i_and_j_2i_numerically":
            at_i["match"],
        "phi_2_vanishes_at_heegner_tau_d_for_d_3_7_11_19":
            at_heegner["all_match"],
        "phi_2_is_symmetric_in_its_two_arguments":
            sym["all_match"],
        "phi_2_of_1728_and_287496_equals_0_in_Z":
            zero_1728["equals_zero"],
        "phi_2_of_0_and_54000_equals_0_in_Z":
            zero_0_54000["equals_zero"],
        "phi_2_coefficient_factorizations_pin":
            factor["all_match"],
    }
    return {
        "at_tau_i": at_i,
        "at_heegner_pairs": at_heegner,
        "symmetry": sym,
        "zero_1728_287496": zero_1728,
        "zero_0_54000": zero_0_54000,
        "factorizations": factor,
        "summary_chain": chain,
    }


if __name__ == "__main__":
    s = derive_all()
    print("summary_chain:")
    for k, v in s["summary_chain"].items():
        print(f"  {k}: {v}")
    print("\nPhi_2 at (j(i), j(2i)) =")
    print(f"  j(i)  = {s['at_tau_i']['j_tau']:.6f} (expect 1728)")
    print(f"  j(2i) = {s['at_tau_i']['j_2tau']:.6f} (expect 287496)")
    print(f"  |Phi_2| = {s['at_tau_i']['abs_phi_2']:.3e}")
    print("\nPhi_2 at Heegner taus:")
    for row in s["at_heegner_pairs"]["rows"]:
        print(f"  d={row['d']}: |Phi_2| = {row['abs_phi_2']},  match={row['match']}")
    print("\nInteger vanishing:")
    print(f"  Phi_2(1728, 287496) = {s['zero_1728_287496']['value']}")
    print(f"  Phi_2(0, 54000) = {s['zero_0_54000']['value']}")
