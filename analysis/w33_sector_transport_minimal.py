#!/usr/bin/env python3
import json
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# W33 adjacency eigenvalues and multiplicities.
sectors = {
    'E1': {'lambda': 12, 'multiplicity': 1},
    'E24': {'lambda': 2, 'multiplicity': 24},
    'E15': {'lambda': -4, 'multiplicity': 15},
}

k = 12
branch = k - 1

# One-step point transport K1 = A / 12.
k1 = {name: Fraction(d['lambda'], k) for name, d in sectors.items()}

# Two-step nonbacktracking closure K2 = (A^2 - k I)/(k*(k-1)).
k2 = {
    name: Fraction(d['lambda'] * d['lambda'] - k, k * branch)
    for name, d in sectors.items()
}

# Nonbacktracking spectral polynomials p_n(lambda), normalized by k*(k-1)^(n-1).
def nb_value(lam, n):
    if n == 0:
        return Fraction(1, 1)
    if n == 1:
        return Fraction(lam, k)
    p0, p1 = 1, lam
    for _ in range(2, n + 1):
        p0, p1 = p1, lam * p1 - branch * p0
    return Fraction(p1, k * (branch ** (n - 1)))

ladder = {
    str(n): {name: str(nb_value(d['lambda'], n)) for name, d in sectors.items()}
    for n in range(0, 9)
}

checks = {
    'k_is_12': k == 12,
    'branch_is_11': branch == 11,
    'k1_values': k1 == {'E1': Fraction(1,1), 'E24': Fraction(1,6), 'E15': Fraction(-1,3)},
    'k2_values': k2 == {'E1': Fraction(1,1), 'E24': Fraction(-2,33), 'E15': Fraction(1,33)},
    'e15_two_step_denominator': k2['E15'].denominator == 33,
}

out = {
    'all_checks_passed': all(checks.values()),
    'checks': checks,
    'k': k,
    'branch': branch,
    'one_step_K1': {name: str(v) for name, v in k1.items()},
    'two_step_K2': {name: str(v) for name, v in k2.items()},
    'nonbacktracking_ladder': ladder,
    'main_identity': 'E15 two-step point transport coefficient is 1/33 = 1/(3*11).',
}

out_path = ROOT / 'data' / 'w33_sector_transport_minimal.json'
out_path.parent.mkdir(parents=True, exist_ok=True)
out_path.write_text(json.dumps(out, indent=2, sort_keys=True) + '\n')
print(json.dumps(out, indent=2, sort_keys=True))
raise SystemExit(0 if out['all_checks_passed'] else 1)
