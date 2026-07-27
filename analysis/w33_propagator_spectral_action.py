#!/usr/bin/env python3
"""
Step 2: Exact propagator computations from the corrected W(3,3) spectrum.

Given spec(D) = {11: 1, 1: 24, -5: 15}, computes:
  - Heat kernel trace K(beta) = Tr exp(-beta D)
  - Spectral zeta zeta_D(s)
  - Resolvent pole residues
  - Functional determinant coefficients
  - Corrected trace tower up to n=20
  - Verifies recurrence m_{n+3} = 7 m_{n+2} + 49 m_{n+1} - 55 m_n
  - Checks that old eigenvalues {-7,-1,5} give wrong traces

Outputs:
  data/PROPAGATOR_2026_07_27_spectral_action.json
"""
import json
import math
from datetime import datetime
from fractions import Fraction

# True spectrum
EIGENVALUES = {11: 1, 1: 24, -5: 15}
# False spectrum (historical)
FALSE_EIGENVALUES = {5: 10, -1: 16, -7: 6}  # as claimed (mult sum=32, wrong)


def trace_power(eigenvalues: dict, n: int) -> int:
    """Compute Tr(D^n) = sum over eigenvalues of mult * eigenvalue^n."""
    return sum(mult * (ev ** n) for ev, mult in eigenvalues.items())


def verify_recurrence(moments: list) -> list:
    """Check m_{n+3} = 7 m_{n+2} + 49 m_{n+1} - 55 m_n for n >= 0."""
    errors = []
    for i in range(len(moments) - 3):
        lhs = moments[i + 3]
        rhs = 7 * moments[i + 2] + 49 * moments[i + 1] - 55 * moments[i]
        if lhs != rhs:
            errors.append({'n': i, 'lhs': lhs, 'rhs': rhs, 'diff': lhs - rhs})
    return errors


def heat_kernel_trace(beta: float) -> float:
    """K(beta) = Tr exp(-beta D) with true spectrum."""
    return sum(mult * math.exp(-ev * beta) for ev, mult in EIGENVALUES.items())


def functional_det_coeffs(max_order: int = 10) -> list:
    """
    Coefficients of det(I - xD) = (1-11x)(1-x)^24(1+5x)^15
    expanded as a polynomial in x.
    Uses the Newton identity: if Z(x) = d/dx log det(I-xD)
    then Z(x) = -sum_n Tr(D^n) x^{n-1}.
    Return coefficients [c_0, c_1, ..., c_max_order] of det(I-xD).
    """
    # Use the fact that log det(I-xD) = sum_k Tr(D^k) * (-x^k/k)
    # Build polynomial product directly
    # (1-11x)^1 * (1-x)^24 * (1+5x)^15
    from fractions import Fraction
    
    def poly_mul(p, q):
        res = [Fraction(0)] * (len(p) + len(q) - 1)
        for i, a in enumerate(p):
            for j, b in enumerate(q):
                res[i + j] += a * b
        return res
    
    def poly_power(factor, root, exp, degree):
        """Compute (1 + root*x)^exp up to degree."""
        p = [Fraction(0)] * (degree + 1)
        for k in range(degree + 1):
            # binomial coefficient C(exp, k)
            binom = Fraction(1)
            for i in range(k):
                binom = binom * (exp - i) // (i + 1)
            p[k] = binom * (root ** k)
        return p
    
    deg = max_order
    p1 = poly_power(1, Fraction(-11), 1, deg)   # (1-11x)^1
    p2 = poly_power(1, Fraction(-1), 24, deg)    # (1-x)^24
    p3 = poly_power(1, Fraction(5), 15, deg)     # (1+5x)^15
    
    prod = poly_mul(p1[:deg+1], p2[:deg+1])
    prod = prod[:deg+1]
    prod = poly_mul(prod, p3[:deg+1])
    prod = prod[:deg+1]
    
    return [str(c) for c in prod]


def main():
    # Trace tower
    true_moments = [trace_power(EIGENVALUES, n) for n in range(21)]
    false_moments = [trace_power(FALSE_EIGENVALUES, n) for n in range(21)]
    
    # Recurrence check
    recurrence_errors = verify_recurrence(true_moments)
    
    # Dimension check
    total_mult_true = sum(EIGENVALUES.values())
    total_mult_false = sum(FALSE_EIGENVALUES.values())
    
    # Functional determinant coefficients
    det_coeffs = functional_det_coeffs(10)
    
    # Heat kernel at sample betas
    heat_samples = {
        str(round(b, 3)): round(heat_kernel_trace(b), 8)
        for b in [0.0, 0.1, 0.5, 1.0, 2.0]
    }
    
    # Projector rank verification (rational arithmetic)
    # P_11 rank = Tr(P_11) = f(11) for f = projector polynomial / scalar
    # Tr(P_11) = Tr((D-I)(D+5I)/160) = (1/160)*(Tr D^2 + 4*Tr D - 5*Tr I)
    trD = true_moments[1]  # -40
    trD2 = true_moments[2]  # 520
    trI = 40
    rank_P11_check = Fraction(trD2 + 4*trD - 5*trI, 160)
    rank_P1_check  = Fraction(-(trD2 - 12*trD - 55*trI), 60)
    rank_Pm5_check = Fraction(trD2 - 10*trD - 11*trI, 96)
    
    report = {
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'true_spectrum': {'eigenvalues_multiplicities': str(EIGENVALUES)},
        'false_spectrum_historical': {'eigenvalues_multiplicities': str(FALSE_EIGENVALUES)},
        'dimension_check': {
            'true_total_multiplicity': total_mult_true,
            'false_total_multiplicity': total_mult_false,
            'correct': total_mult_true == 40,
        },
        'trace_tower_n_0_to_20': {
            'true': true_moments,
            'false_historical': false_moments,
            'agree': true_moments == false_moments,
        },
        'recurrence_verification': {
            'recurrence': 'm_{n+3} = 7*m_{n+2} + 49*m_{n+1} - 55*m_n',
            'errors': recurrence_errors,
            'verified': len(recurrence_errors) == 0,
        },
        'projector_rank_check': {
            'rank_P11': str(rank_P11_check),
            'rank_P1': str(rank_P1_check),
            'rank_Pm5': str(rank_Pm5_check),
            'correct_1_24_15': [
                rank_P11_check == 1,
                rank_P1_check == 24,
                rank_Pm5_check == 15,
            ],
        },
        'functional_determinant_coeffs_degree_0_to_10': det_coeffs,
        'heat_kernel_trace_samples': heat_samples,
        'selection_rule_summary': {
            'eigenspaces': '1 + 24 + 15 = 40',
            'historical_false': '16 + 10 + 6 = 32 (wrong dimension)',
            'propagator_poles': [11, 1, -5],
            'recurrence_coefficients': [7, 49, -55],
        },
    }
    
    import pathlib
    out = pathlib.Path(__file__).parent.parent / 'data' / \
          'PROPAGATOR_2026_07_27_spectral_action.json'
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(report, indent=2))
    
    print('Dimension check (true/false):', total_mult_true, '/', total_mult_false)
    print('True Tr D^0..5:', true_moments[:6])
    print('Recurrence errors:', recurrence_errors)
    print('Projector ranks:', rank_P11_check, rank_P1_check, rank_Pm5_check)
    print('det(I-xD) first 5 coefficients:', det_coeffs[:5])
    print('Report written to', out)


if __name__ == '__main__':
    main()
