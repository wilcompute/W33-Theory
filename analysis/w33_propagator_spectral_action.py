#!/usr/bin/env python3
"""
Pass 1140: exact propagator computations from the corrected W(3,3) spectrum.

{shifted-adjacency:corrected}

Given spec(D) = {11: 1, 1: 24, -5: 15}, computes:
  - Positive heat trace K(beta) = Tr exp(-beta D^2)
  - The signed semigroup Tr exp(-beta D), explicitly not called heat
  - Unambiguous zeta data for |D| and D^2
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
from fractions import Fraction
from pathlib import Path

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


def signed_semigroup_trace(beta: float) -> float:
    """Tr exp(-beta D); this grows on the -5 eigenspace."""
    return sum(mult * math.exp(-ev * beta) for ev, mult in EIGENVALUES.items())


def positive_heat_trace(beta: float) -> float:
    """Tr exp(-beta D^2), the positive heat trace."""
    return sum(
        mult * math.exp(-(ev * ev) * beta)
        for ev, mult in EIGENVALUES.items()
    )


def absolute_zeta(s: complex) -> complex:
    """Tr |D|^{-s}; unlike D^{-s}, this needs no spectral cut."""
    if isinstance(s, int):
        if s >= 0:
            return sum(
                mult * Fraction(1, abs(ev) ** s)
                for ev, mult in EIGENVALUES.items()
            )
        return sum(mult * (abs(ev) ** (-s)) for ev, mult in EIGENVALUES.items())
    return sum(mult * (abs(ev) ** (-s)) for ev, mult in EIGENVALUES.items())


def squared_zeta(s: complex) -> complex:
    """Tr (D^2)^{-s}."""
    if isinstance(s, int):
        if s >= 0:
            return sum(
                mult * Fraction(1, (ev * ev) ** s)
                for ev, mult in EIGENVALUES.items()
            )
        return sum(mult * ((ev * ev) ** (-s)) for ev, mult in EIGENVALUES.items())
    return sum(mult * ((ev * ev) ** (-s)) for ev, mult in EIGENVALUES.items())


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
    def poly_mul(p, q):
        res = [Fraction(0)] * (len(p) + len(q) - 1)
        for i, a in enumerate(p):
            for j, b in enumerate(q):
                res[i + j] += a * b
        return res
    
    def poly_power(root, exp, degree):
        """Compute (1 + root*x)^exp up to degree."""
        p = [Fraction(0)] * (min(exp, degree) + 1)
        for k in range(len(p)):
            p[k] = Fraction(math.comb(exp, k)) * (root ** k)
        return p

    deg = max_order
    p1 = poly_power(Fraction(-11), 1, deg)
    p2 = poly_power(Fraction(-1), 24, deg)
    p3 = poly_power(Fraction(5), 15, deg)

    prod = poly_mul(p1, p2)[: deg + 1]
    prod = poly_mul(prod, p3)[: deg + 1]

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
    
    # Positive heat and signed semigroup at sample beta values.
    beta_values = [0.0, 0.1, 0.5, 1.0, 2.0]
    heat_samples = {
        str(round(b, 3)): round(positive_heat_trace(b), 8)
        for b in beta_values
    }
    signed_samples = {
        str(round(b, 3)): round(signed_semigroup_trace(b), 8)
        for b in [0.0, 0.1, 0.5, 1.0, 2.0]
    }
    
    # Projector rank verification (rational arithmetic)
    # P_11 rank = Tr(P_11) = f(11) for f = projector polynomial / scalar
    # Tr(P_11) = Tr((D-I)(D+5I)/160) = (1/160)*(Tr D^2 + 4*Tr D - 5*Tr I)
    trD = true_moments[1]  # -40
    trD2 = true_moments[2]  # 520
    trI = 40
    rank_P11_check = Fraction(trD2 + 4*trD - 5*trI, 160)
    rank_P1_check = Fraction(-(trD2 - 6*trD - 55*trI), 60)
    rank_Pm5_check = Fraction(trD2 - 12*trD + 11*trI, 96)
    
    report = {
        'schema': 'w33.pass1140.corrected_propagator.v1',
        'status': 'PASS',
        'true_spectrum': {'eigenvalues_multiplicities': str(EIGENVALUES)},
        'quarantined_historical_spectrum': {
            'eigenvalues_multiplicities': str(FALSE_EIGENVALUES),
            'status': 'RETRACTED',
        },
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
        'positive_heat_trace': {
            'formula': 'exp(-121*b)+24*exp(-b)+15*exp(-25*b)',
            'samples': heat_samples,
        },
        'signed_semigroup_trace': {
            'formula': 'exp(-11*b)+24*exp(-b)+15*exp(5*b)',
            'is_positive_heat': False,
            'samples': signed_samples,
        },
        'zeta_semantics': {
            'absolute': 'zeta_|D|(s)=11^(-s)+24+15*5^(-s)',
            'squared': 'zeta_D2(s)=121^(-s)+24+15*25^(-s)',
            'signed_requires_spectral_cut': True,
        },
        'selection_rule_summary': {
            'eigenspaces': '1 + 24 + 15 = 40',
            'historical_false': '16 + 10 + 6 = 32 (wrong dimension)',
            'propagator_poles': [11, 1, -5],
            'recurrence_coefficients': [7, 49, -55],
        },
        'all_checks_pass': (
            total_mult_true == 40
            and not recurrence_errors
            and [rank_P11_check, rank_P1_check, rank_Pm5_check]
            == [1, 24, 15]
        ),
    }

    out = Path(__file__).parent.parent / 'data' / \
          'PROPAGATOR_2026_07_27_spectral_action.json'
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    print('Dimension check (true/false):', total_mult_true, '/', total_mult_false)
    print('True Tr D^0..5:', true_moments[:6])
    print('Recurrence errors:', recurrence_errors)
    print('Projector ranks:', rank_P11_check, rank_P1_check, rank_Pm5_check)
    print('det(I-xD) first 5 coefficients:', det_coeffs[:5])
    print('Report written to', out)


if __name__ == '__main__':
    main()
