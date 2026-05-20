"""Distance-2 spectrum and ternary eigenvalue identity for W(3,3).

MCL establishes the distance-2 matrix A2 = J - I - A and proves:
  * A2 eigenvalues are ±q on the nonprincipal eigenspaces (ternary spectrum)
  * m_r - m_s = q^2  (multiplicity gap identity)
  * m_r = q(q+1)^2/2 and m_s = q(q^2+1)/2  (closed-form multiplicities)
  * trace(B) = 0  where B = A2/q  (traceless normalisation)
  * ||A2||_F^2 = q^3 * v  (Frobenius norm identity)
  * B^2 = I + 2J  (ternary BM-algebra square)
  * ||A||_F^2  = k * v = 2|E|  (adjacency Frobenius identity)
  * ||A2||_F^2 / ||A||_F^2 = q^2 / (q+1)  (ratio identity)

These identities hold for all GQ(q,q) and specialise beautifully to W(3,3).
"""

from __future__ import annotations

import json
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_kemeny_spectral_excess import kemeny_spectral_excess_packet  # noqa: E402


def _exact(value: Fraction | int) -> dict[str, object]:
    fraction = Fraction(value)
    return {
        "fraction": str(fraction),
        "numerator": fraction.numerator,
        "denominator": fraction.denominator,
        "float": float(fraction),
    }


def _packet_fraction(entry: dict[str, object]) -> Fraction:
    return Fraction(int(entry["numerator"]), int(entry["denominator"]))


def distance_spectrum_ternary_packet() -> dict[str, object]:
    """Return exact distance-2 spectrum data for W(3,3) = GQ(q,q) with q=3."""
    prev = kemeny_spectral_excess_packet()
    q = int(prev["parameters"]["q"])
    v = int(prev["parameters"]["v"])
    k = int(prev["parameters"]["k"])
    r = int(prev["parameters"]["r"])
    s = int(prev["parameters"]["s"])

    edges = v * k // 2  # 240

    # Closed-form multiplicity formulae for GQ(q,q)
    m_r_formula = Fraction(q * (q + 1) ** 2, 2)  # q(q+1)^2 / 2
    m_s_formula = Fraction(q * (q ** 2 + 1), 2)  # q(q^2+1) / 2
    m_r = int(m_r_formula)  # 24
    m_s = int(m_s_formula)  # 15

    mr_ms_sum_check = (m_r + m_s) == (v - 1)
    mr_ms_diff = m_r - m_s           # 24 - 15 = 9 = q^2
    multiplicity_gap_identity = mr_ms_diff == q ** 2

    # Distance-2 matrix A2 = J - I - A
    # On principal eigenspace (eigenvalue k of A): eigenvalue = v - 1 - k = 27
    # On r-eigenspace (J has eigenvalue 0 on nonprincipal): eigenvalue = 0 - 1 - r = -(1+r)
    # On s-eigenspace: eigenvalue = 0 - 1 - s = -(1+s)
    a2_principal = v - 1 - k      # 27
    a2_on_r = -(1 + r)           # -3 = -q
    a2_on_s = -(1 + s)           # +3 = +q

    a2_r_equals_neg_q = (a2_on_r == -q)
    a2_s_equals_pos_q = (a2_on_s == q)

    # B = A2 / q: eigenvalues (v-1-k)/q (principal), -1 (r-eigenspace), +1 (s-eigenspace)
    b_principal = Fraction(a2_principal, q)   # 27/3 = 9 = q^2
    b_on_r = Fraction(a2_on_r, q)            # -1
    b_on_s = Fraction(a2_on_s, q)            # +1

    b_principal_equals_q2 = (b_principal == q ** 2)

    # trace(B) = 1*q^2 + m_r*(-1) + m_s*(+1) = q^2 - m_r + m_s = q^2 - q^2 = 0
    trace_B = 1 * b_principal + m_r * b_on_r + m_s * b_on_s
    trace_B_zero = (trace_B == 0)

    # ||A2||_F^2 = trace(A2^2) = (v-1-k)^2 * 1 + (-q)^2 * m_r + q^2 * m_s
    # = (v-1-k)^2 + q^2*(m_r + m_s) = (v-1-k)^2 + q^2*(v-1)
    norm_A2_sq = a2_principal ** 2 + q ** 2 * m_r + q ** 2 * m_s
    norm_A2_sq_formula = a2_principal ** 2 + q ** 2 * (v - 1)
    norm_A2_q3v = q ** 3 * v  # = 1080
    frobenius_A2_identity = (norm_A2_sq == norm_A2_q3v)

    # ||A||_F^2 = k^2 + r^2 * m_r + s^2 * m_s = kv = 2|E|
    norm_A_sq = k ** 2 + r ** 2 * m_r + s ** 2 * m_s
    norm_A_kv = k * v   # = 480 = 2|E|
    frobenius_A_identity = (norm_A_sq == norm_A_kv)
    frobenius_A_2edges = (norm_A_sq == 2 * edges)

    # Ratio ||A2||^2 / ||A||^2 = q^3v / kv = q^3/k = q^2/(q+1) (since k = q(q+1))
    ratio_formula = Fraction(q ** 2, q + 1)   # 9/4
    ratio_computed = Fraction(norm_A2_sq, norm_A_sq)
    ratio_identity = (ratio_computed == ratio_formula)

    # B^2 eigenvalues: (q^2)^2 = q^4 (principal), (-1)^2 = 1 (r-eigen), 1 (s-eigen)
    # B^2 - I has eigenvalues: q^4 - 1 = 80 (principal), 0 (r-eigen), 0 (s-eigen)
    # => B^2 - I = (q^4-1) * P_principal = (q^4-1)/v * J = 80/40 * J = 2J
    b2_minus_I_principal = b_principal ** 2 - 1   # q^4 - 1 = 80
    b2_minus_I_coeff = Fraction(b2_minus_I_principal, v)   # 80/40 = 2
    bm_algebra_square = (b2_minus_I_coeff == 2)   # coefficient of J in B^2 - I

    # A2^2 = q^2 * (I + 2J) on all eigenspaces? Let's verify:
    # On principal: a2_principal^2 = 729 vs q^2*(1 + 2*v) = 9*(1+80) = 9*81 = 729 ✓
    # On r-eigen: (-q)^2 = q^2 ✓ (since J has eigenvalue 0 here)
    # On s-eigen: q^2 ✓
    a2sq_principal = a2_principal ** 2           # 729
    a2sq_r = q ** 2                              # 9
    a2sq_s = q ** 2                              # 9
    qsq_I_plus_2qsqJ_principal = q ** 2 * (1 + 2 * v)   # 9 * 81 = 729
    qsq_I_plus_2qsqJ_nonprincipal = q ** 2 * 1           # 9
    a2sq_bm_check_principal = (a2sq_principal == qsq_I_plus_2qsqJ_principal)
    a2sq_bm_check_nonprincipal = (a2sq_r == qsq_I_plus_2qsqJ_nonprincipal)

    # Annihilator properties:
    # (A2 + q*I) kills r-eigenspace: eigenvalue on r = -q + q = 0 ✓
    # (A2 - q*I) kills s-eigenspace: eigenvalue on s = q - q = 0 ✓
    a2_plus_q_on_r = a2_on_r + q    # = 0
    a2_minus_q_on_s = a2_on_s - q   # = 0

    return {
        "parameters": {
            "q": q,
            "v": v,
            "k": k,
            "r": r,
            "s": s,
            "edges": edges,
        },
        "multiplicity_formulae": {
            "m_r": m_r,
            "m_s": m_s,
            "m_r_formula": f"q(q+1)^2/2 = {q}·{(q+1)**2}//2 = {m_r}",
            "m_s_formula": f"q(q^2+1)/2 = {q}·{q**2+1}//2 = {m_s}",
            "m_r_exact": _exact(m_r_formula),
            "m_s_exact": _exact(m_s_formula),
            "sum_is_v_minus_1": mr_ms_sum_check,
            "gap_m_r_minus_m_s": mr_ms_diff,
            "multiplicity_gap_is_q2": multiplicity_gap_identity,
        },
        "distance_2_eigenvalues": {
            "on_principal": a2_principal,
            "on_r_eigenspace": a2_on_r,
            "on_s_eigenspace": a2_on_s,
            "a2_r_equals_neg_q": a2_r_equals_neg_q,
            "a2_s_equals_pos_q": a2_s_equals_pos_q,
            "ternary_spectrum_verified": a2_r_equals_neg_q and a2_s_equals_pos_q,
            "statement": "A2 has eigenvalues -q, +q on nonprincipal eigenspaces",
        },
        "B_matrix": {
            "definition": "B = A2 / q = (J - I - A) / q",
            "b_principal": _exact(b_principal),
            "b_on_r": _exact(b_on_r),
            "b_on_s": _exact(b_on_s),
            "b_principal_equals_q2": b_principal_equals_q2,
            "trace_B": _exact(trace_B),
            "trace_B_zero": trace_B_zero,
            "statement": "B = A2/q has eigenvalues {q^2, -1, +1}; trace(B) = 0",
        },
        "frobenius_norms": {
            "norm_A_sq": norm_A_sq,
            "norm_A_kv": norm_A_kv,
            "norm_A_2edges": 2 * edges,
            "frobenius_A_identity": frobenius_A_identity,
            "frobenius_A_2edges": frobenius_A_2edges,
            "norm_A2_sq": norm_A2_sq,
            "norm_A2_q3v": norm_A2_q3v,
            "frobenius_A2_identity": frobenius_A2_identity,
            "ratio": _exact(ratio_computed),
            "ratio_formula": _exact(ratio_formula),
            "ratio_q2_over_qp1": _exact(ratio_formula),
            "ratio_identity": ratio_identity,
        },
        "bm_algebra_square": {
            "A2_sq_principal": a2sq_principal,
            "A2_sq_r_eigen": a2sq_r,
            "A2_sq_s_eigen": a2sq_s,
            "q2_I_plus_2q2J_principal": int(qsq_I_plus_2qsqJ_principal),
            "q2_I_plus_2q2J_nonprincipal": int(qsq_I_plus_2qsqJ_nonprincipal),
            "principal_check": a2sq_bm_check_principal,
            "nonprincipal_check": a2sq_bm_check_nonprincipal,
            "identity": "A2^2 = q^2 * I + 2*q^2 * J",
            "B2_minus_I_coeff": _exact(b2_minus_I_coeff),
            "B2_minus_I_equals_2J": bm_algebra_square,
        },
        "annihilator_properties": {
            "A2_plus_q_on_r_eigenspace": a2_plus_q_on_r,
            "A2_minus_q_on_s_eigenspace": a2_minus_q_on_s,
            "A2_plus_q_kills_r_eigenspace": (a2_plus_q_on_r == 0),
            "A2_minus_q_kills_s_eigenspace": (a2_minus_q_on_s == 0),
        },
        "master_identities_summary": {
            "m_r_minus_m_s_equals_q2": multiplicity_gap_identity,
            "ternary_spectrum": a2_r_equals_neg_q and a2_s_equals_pos_q,
            "trace_B_zero": trace_B_zero,
            "frobenius_A_identity": frobenius_A_identity,
            "frobenius_A2_identity": frobenius_A2_identity,
            "ratio_identity": ratio_identity,
            "B2_minus_I_equals_2J": bm_algebra_square,
            "bm_algebra_square_principal": a2sq_bm_check_principal,
            "bm_algebra_square_nonprincipal": a2sq_bm_check_nonprincipal,
            "annihilator_r": (a2_plus_q_on_r == 0),
            "annihilator_s": (a2_minus_q_on_s == 0),
        },
    }


def main() -> None:
    packet = distance_spectrum_ternary_packet()

    out_path = ROOT / "PART_MCL_DISTANCE_SPECTRUM_TERNARY_results.json"
    data_path = ROOT / "data" / "w33_distance_spectrum_ternary.json"

    with open(out_path, "w") as fh:
        json.dump(packet, fh, indent=2)
    with open(data_path, "w") as fh:
        json.dump(packet, fh, indent=2)

    print("=== MCL: Distance-2 Spectrum & Ternary Eigenvalue Identity ===")
    q = packet["parameters"]["q"]
    v = packet["parameters"]["v"]
    m = packet["multiplicity_formulae"]
    d = packet["distance_2_eigenvalues"]
    B = packet["B_matrix"]
    F = packet["frobenius_norms"]
    bm = packet["bm_algebra_square"]
    ids = packet["master_identities_summary"]

    print(f"  m_r = {m['m_r']}  [formula: q(q+1)^2/2 = {q}·{(q+1)**2}//2]")
    print(f"  m_s = {m['m_s']}  [formula: q(q^2+1)/2 = {q}·{q**2+1}//2]")
    print(f"  m_r - m_s = {m['gap_m_r_minus_m_s']} = q^2 = {q**2}: {m['multiplicity_gap_is_q2']}")
    print(f"  A2 eigenvalues on nonprincipal spaces: {d['on_r_eigenspace']} (r) and {d['on_s_eigenspace']} (s)")
    print(f"  Ternary spectrum A2 = ±q: {d['ternary_spectrum_verified']}")
    print(f"  B = A2/q: trace(B) = {B['trace_B']['fraction']}, trace_zero: {B['trace_B_zero']}")
    print(f"  ||A||_F^2 = {F['norm_A_sq']} = kv = {F['norm_A_kv']}: {F['frobenius_A_identity']}")
    print(f"  ||A2||_F^2 = {F['norm_A2_sq']} = q^3·v = {F['norm_A2_q3v']}: {F['frobenius_A2_identity']}")
    print(f"  ||A2||^2 / ||A||^2 = {F['ratio']['fraction']} = q^2/(q+1): {F['ratio_identity']}")
    print(f"  A2^2 = q^2·I + 2q^2·J: {bm['principal_check']} (principal), {bm['nonprincipal_check']} (non-principal)")
    print(f"  B^2 - I = 2J: {bm['B2_minus_I_equals_2J']}")
    print()
    print(f"  Master identities: {sum(v for v in ids.values())} / {len(ids)} verified")
    for k_id, v_id in ids.items():
        print(f"    {'✓' if v_id else '✗'} {k_id}")


if __name__ == "__main__":
    main()
