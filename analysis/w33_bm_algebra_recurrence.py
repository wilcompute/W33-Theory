"""Bose-Mesner algebra matrix recurrence for W(3,3).

MCLIV: The SRG identity A^2 = (k-lambda-mu)*I + (lambda-mu)*A + mu*J
collapses to A^2 = 8I - 2A + 4J for W(3,3) = SRG(40,12,2,4).

This generates an exact 3-dimensional linear recurrence on the
Bose-Mesner coordinates: A^n = a_n*I + b_n*A + c_n*J

Recurrence step (from A^{n+1} = A * A^n = A*(a_n I + b_n A + c_n J)):
  a_{n+1} = (k-lambda-mu) * b_n            = 8 * b_n
  b_{n+1} = a_n + (lambda-mu) * b_n        = a_n - 2 * b_n
  c_{n+1} = mu * b_n + k * c_n             = 4 * b_n + 12 * c_n

Initial conditions: (a_0, b_0, c_0) = (1, 0, 0)

Key identities (exact, via BM algebra):
  n=0: A^0 = I
  n=1: A^1 = A
  n=2: A^2 = 8I - 2A + 4J         [SRG fundamental identity]
  n=3: A^3 = -16I + 12A + 40J
  n=4: A^4 = 96I - 40A + 528J
  n=5: A^5 = -320I + 176A + 3568J

Trace identity: trace(A^n) = v*(a_n + c_n) (since trace(I)=v, trace(A)=0, trace(J)=v)
This equals k^n + m_r*r^n + m_s*s^n  [spectral trace formula, verified in MCLIII].

Minimal polynomial (degree 3): m_A(x) = (x-12)(x-2)(x+4) = x^3 - 10x^2 - 32x + 96
So A^3 = 10*A^2 + 32*A - 96*I  [minimal polynomial recurrence, MCLIV.2].

Cross-check MCLIV.2 ↔ BM recurrence:
  10A^2 + 32A - 96I = 10*(8I-2A+4J) + 32A - 96I = 80I-20A+40J + 32A - 96I
                    = -16I + 12A + 40J = A^3  ✓

New invariants (fresh for MCLIV):
  * B_n := a_n + c_n  (coefficient of I in trace, divided by v)
    B_0 = 1, B_1 = 0, B_2 = 12 (= k), B_3 = 24, B_4 = 624
    B_n = (k^n + m_r*r^n + m_s*s^n) / v  [normalized spectral trace]
    B_2 = kv/v = k = 12 ✓
    B_3 = 960/40 = 24 ✓

  * b_n sequence: 0, 1, -2, 12, -40, 176, -640, ...
    b_{n+1} = a_n - 2*b_n,  a_n = 8*b_{n-1}  → b_{n+1} = 8*b_{n-1} - 2*b_n
    So {b_n} satisfies the 2-step recurrence: b_{n+1} + 2*b_n - 8*b_{n-1} = 0
    Characteristic roots: x^2 + 2x - 8 = 0 → (x+4)(x-2) = 0 → x = -4, 2 = s, r ✓
    General solution: b_n = alpha * r^n + beta * s^n = alpha * 2^n + beta * (-4)^n
    With b_0=0, b_1=1: alpha + beta = 0, 2*alpha - 4*beta = 1
    → alpha = 1/6, beta = -1/6 → b_n = (2^n - (-4)^n) / 6 = (r^n - s^n)/(r-s) ✓

  * a_n = 8*b_{n-1} = (8/6)*(2^{n-1} - (-4)^{n-1}) = (4/3)*(r^{n-1} - s^{n-1})
    For n=2: (4/3)*(2-(-4)) = (4/3)*6 = 8 ✓

  * c_n: from B_n = a_n + c_n and B_n = (k^n + m_r*r^n + m_s*s^n)/v
    c_n = B_n - a_n = spectral_trace(n)/v - 8*b_{n-1}
"""

from __future__ import annotations

import json
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_ihara_zeta import ihara_zeta_packet, spectral_trace_L  # noqa: E402


def bm_step(a: Fraction, b: Fraction, c: Fraction,
            alpha: int, beta: int, mu: int, k: int) -> tuple[Fraction, Fraction, Fraction]:
    """One step of the Bose-Mesner recurrence.

    alpha = k - lambda - mu, beta = lambda - mu for the SRG.
    """
    a1 = alpha * b
    b1 = a + beta * b
    c1 = mu * b + k * c
    return a1, b1, c1


def bm_sequence(n_max: int, v: int, k: int, lam: int, mu: int) -> list[tuple[Fraction, Fraction, Fraction]]:
    """Return BM coordinates (a_n, b_n, c_n) for n = 0 .. n_max."""
    alpha = k - lam - mu   # coefficient of I in A^2 formula
    beta = lam - mu        # coefficient of A in A^2 formula (note: lam - mu, which is neg here)
    # Initial: A^0 = I, A^1 = A
    coords = [(Fraction(1), Fraction(0), Fraction(0))]
    # Step 0→1:
    a, b, c = Fraction(0), Fraction(1), Fraction(0)
    coords.append((a, b, c))
    for _ in range(2, n_max + 1):
        a, b, c = bm_step(a, b, c, alpha, beta, mu, k)
        # Wait: the recurrence step is A^{n+1} = A * A^n = A*(a_n I + b_n A + c_n J)
        # = a_n * A + b_n * A^2 + c_n * AJ
        # = a_n * A + b_n * (alpha*I + beta*A + mu*J) + c_n * k * J   [AJ = kJ for regular]
        # = b_n*alpha * I + (a_n + b_n*beta) * A + (b_n*mu + c_n*k) * J
        # So: a_{n+1} = alpha*b_n, b_{n+1} = a_n + beta*b_n, c_{n+1} = mu*b_n + k*c_n
        # But I'm starting from coords[-1] = (a_n, b_n, c_n):
        prev_a, prev_b, prev_c = coords[-2]  # a_{n-1}
        cur_a, cur_b, cur_c = coords[-1]    # a_n
        new_a = alpha * cur_b
        new_b = cur_a + beta * cur_b
        new_c = mu * cur_b + k * cur_c
        coords.append((Fraction(new_a), Fraction(new_b), Fraction(new_c)))
    return coords


def bm_algebra_packet() -> dict[str, object]:
    prev = ihara_zeta_packet()
    q = int(prev["parameters"]["q"])
    v = int(prev["parameters"]["v"])
    k = int(prev["parameters"]["k"])
    r = int(prev["parameters"]["r"])
    s = int(prev["parameters"]["s"])
    m_r = int(prev["parameters"]["m_r"])
    m_s = int(prev["parameters"]["m_s"])
    lam = 2    # lambda = number of common neighbours for adjacent pair in SRG
    mu = 4     # mu = number of common neighbours for non-adjacent pair in SRG

    alpha = k - mu         # = 8  (coefficient of b_n in a_{n+1} = (k-mu)*b_n)
    beta = lam - mu        # = -2

    # Generate BM coordinates for n = 0..7
    n_max = 7
    # Manual recurrence from scratch:
    coords: list[tuple[Fraction, Fraction, Fraction]] = [(Fraction(1), Fraction(0), Fraction(0))]
    a, b, c = Fraction(0), Fraction(1), Fraction(0)
    coords.append((a, b, c))
    for _ in range(2, n_max + 1):
        prev_a, prev_b, prev_c = coords[-1]
        new_a = Fraction(alpha) * prev_b
        new_b = coords[-2][0] + Fraction(beta) * prev_b  # a_{n-1} + beta*b_{n-1}... wait
        # Recurrence: a_{n+1} = alpha*b_n, b_{n+1} = a_n + beta*b_n, c_{n+1} = mu*b_n + k*c_n
        # Here the 'prev' IS a_n, so:
        cur_a, cur_b, cur_c = coords[-1]
        next_a = Fraction(alpha) * cur_b
        next_b = cur_a + Fraction(beta) * cur_b
        next_c = Fraction(mu) * cur_b + Fraction(k) * cur_c
        coords.append((next_a, next_b, next_c))
    # coords[0] = (1, 0, 0), coords[1] = (0, 1, 0), etc.
    # But wait my loop is off — let me redo from scratch properly:
    coords = [(Fraction(1), Fraction(0), Fraction(0)),
              (Fraction(0), Fraction(1), Fraction(0))]
    while len(coords) <= n_max:
        a_n, b_n, c_n = coords[-1]
        na = Fraction(alpha) * b_n
        nb = a_n + Fraction(beta) * b_n
        nc = Fraction(mu) * b_n + Fraction(k) * c_n
        coords.append((na, nb, nc))

    # Verify against expected values
    expected = [
        (Fraction(1), Fraction(0), Fraction(0)),   # n=0
        (Fraction(0), Fraction(1), Fraction(0)),   # n=1
        (Fraction(8), Fraction(-2), Fraction(4)),  # n=2: 8I - 2A + 4J
        (Fraction(-16), Fraction(12), Fraction(40)),   # n=3
        (Fraction(96), Fraction(-40), Fraction(528)),  # n=4
    ]
    bm_match = all(coords[n] == expected[n] for n in range(len(expected)))

    # Trace check: trace(A^n) = v*(a_n + c_n) for all n
    trace_from_bm = [int(v * (coords[n][0] + coords[n][2])) for n in range(n_max + 1)]
    trace_spectral = [spectral_trace_L(k, r, s, m_r, m_s, n) for n in range(n_max + 1)]
    trace_match = (trace_from_bm == trace_spectral)

    # b_n closed form: b_n = (r^n - s^n) / (r - s) = (2^n - (-4)^n) / 6
    r_minus_s = r - s   # = 6
    b_n_formula = [Fraction(r**n - s**n, r_minus_s) for n in range(n_max + 1)]
    b_n_actual = [coords[n][1] for n in range(n_max + 1)]
    b_n_match = (b_n_formula == b_n_actual)

    # a_n from b_n: a_n = alpha * b_{n-1} for n >= 1, and a_0 = 1 (initial condition)
    a_n_formula = [Fraction(1)] + [Fraction(alpha) * b_n_formula[n - 1] for n in range(1, n_max + 1)]
    a_n_actual = [coords[n][0] for n in range(n_max + 1)]
    a_n_match = (a_n_formula == a_n_actual)

    # Minimal polynomial: A^3 = 10*A^2 + 32*A - 96*I
    # Check: using BM coords, is A^3 = 10*A^2 + 32*A^1 - 96*A^0 ?
    # LHS = coords[3] = (-16, 12, 40)
    # RHS: 10*(8,-2,4) + 32*(0,1,0) - 96*(1,0,0) = (80,-20,40) + (0,32,0) + (-96,0,0) = (-16, 12, 40) ✓
    min_poly_lhs = coords[3]
    min_poly_rhs = (10 * coords[2][0] + 32 * coords[1][0] - 96 * coords[0][0],
                    10 * coords[2][1] + 32 * coords[1][1] - 96 * coords[0][1],
                    10 * coords[2][2] + 32 * coords[1][2] - 96 * coords[0][2])
    min_poly_check = (min_poly_lhs == min_poly_rhs)

    # Spectral B_n = trace(A^n)/v = a_n + c_n
    B_n = [int(trace_spectral[n]) for n in range(n_max + 1)]
    B_n_expected = [40, 0, 480, 960, 24960, 76800, 2661120, 10137600]  # verify a few
    # Actually compute: trace(A^n)/v — these are the per-vertex average closed walk counts
    B_normalized = [Fraction(trace_spectral[n], v) for n in range(n_max + 1)]

    # Check B_2 = k = 12
    B2_check = (B_normalized[2] == k)
    # Check B_3 = 2*lambda*k/... actually B_3 = trace(A^3)/v = 960/40 = 24 = lambda*k
    B3_check = (B_normalized[3] == Fraction(lam * k))  # 24 ✓

    master_identities = {
        "bm_coordinates_n0_to_4": bm_match,
        "trace_bm_equals_trace_spectral": trace_match,
        "b_n_closed_form": b_n_match,
        "a_n_from_b_n": a_n_match,
        "minimal_polynomial_A3_eq_10A2_32A_minus_96I": min_poly_check,
        "B2_normalized_trace_equals_k": B2_check,
        "B3_normalized_trace_equals_lambda_k": B3_check,
    }

    return {
        "parameters": {
            "q": q,
            "v": v,
            "k": k,
            "r": r,
            "s": s,
            "m_r": m_r,
            "m_s": m_s,
            "lambda": lam,
            "mu": mu,
            "alpha_coeff": alpha,
            "beta_coeff": beta,
        },
        "bm_coordinates": {
            f"n_{n}": {
                "a": str(coords[n][0]),
                "b": str(coords[n][1]),
                "c": str(coords[n][2]),
                "expression": f"{coords[n][0]}*I + ({coords[n][1]})*A + {coords[n][2]}*J",
            }
            for n in range(n_max + 1)
        },
        "fundamental_identity": {
            "A_squared": "8I - 2A + 4J",
            "formula": f"A^2 = (k-lambda-mu)*I + (lambda-mu)*A + mu*J = {alpha}I + {beta}A + {mu}J",
            "parameters": f"k={k}, lambda={lam}, mu={mu}",
        },
        "b_n_analysis": {
            "closed_form": f"b_n = (r^n - s^n)/(r-s) = (2^n - (-4)^n)/6",
            "characteristic_roots": [r, s],
            "r_minus_s": r_minus_s,
            "first_8_values": [str(b_n_formula[n]) for n in range(n_max + 1)],
            "match": b_n_match,
        },
        "minimal_polynomial": {
            "expression": "x^3 - 10x^2 - 32x + 96 = (x-12)(x-2)(x+4)",
            "recurrence": "A^3 = 10*A^2 + 32*A - 96*I",
            "verified": min_poly_check,
        },
        "normalized_traces": {
            f"B_{n}": str(B_normalized[n]) for n in range(n_max + 1)
        },
        "spectral_traces": {
            f"trace_A_{n}": trace_spectral[n] for n in range(n_max + 1)
        },
        "master_identities_summary": master_identities,
    }


def main() -> None:
    packet = bm_algebra_packet()

    out_path = ROOT / "PART_MCLIV_BM_ALGEBRA_RECURRENCE_results.json"
    data_path = ROOT / "data" / "w33_bm_algebra_recurrence.json"

    with open(out_path, "w") as fh:
        json.dump(packet, fh, indent=2)
    with open(data_path, "w") as fh:
        json.dump(packet, fh, indent=2)

    print("=== MCLIV: Bose-Mesner Algebra Matrix Recurrence ===")
    print(f"  Fundamental: A^2 = {packet['fundamental_identity']['A_squared']}")
    print()
    for n in range(6):
        bm = packet["bm_coordinates"][f"n_{n}"]
        print(f"  A^{n} = {bm['expression']}")
    print()
    bn = packet["b_n_analysis"]
    print(f"  b_n closed form: {bn['closed_form']}")
    print(f"  b_n match: {bn['match']}")
    print()
    mp = packet["minimal_polynomial"]
    print(f"  Minimal poly: {mp['expression']}")
    print(f"  Recurrence: {mp['recurrence']}")
    print(f"  Verified: {mp['verified']}")
    print()
    ids = packet["master_identities_summary"]
    total_ok = sum(v2 for v2 in ids.values())
    print(f"  Master identities: {total_ok} / {len(ids)} verified")
    for k_id, v_id in ids.items():
        print(f"    {'✓' if v_id else '✗'} {k_id}")


if __name__ == "__main__":
    main()
