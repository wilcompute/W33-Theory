#!/usr/bin/env python3
"""Factor the characteristic-3 PGSp sign inversion into two exact pieces.

Inputs already frozen on master establish:
  1. over Q the explicit PGSp/PSp outer involution acts on the St81
     multiplicity space through J81 = diag(1,1,-1), in the deterministic
     primitive frame (projectively normalized with primitive 0 positive);
  2. after the chosen integral W33-building chain injections are reduced mod 3,
     the two rational-even primitive maps have source outer transport -S,
     while the rational-odd primitive map has +S.

This script performs the missing exact bookkeeping.  For primitive i define

    r_i  = normalized rational multiplicity sign from J81,
    m_i  = solved modular chain-map sign relative to building outer S,
    eta_i = m_i / r_i in F3^x = {+1,-1}.

If eta_i is independent of i, the apparent parity reversal is not three
unrelated accidents: it is one uniform relative outer character carried by the
chosen integral chain-injection normalization.  The product law is

    modular sign = injection factor * rational multiplicity sign.

The factor is normalization-dependent by one global projective sign, while its
uniformity and the product relation are invariant statements.  This is finite
representation/chain arithmetic only.
"""
from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROUTER = ROOT / 'data/PART_W33_20260902_PGSP_OUTER_M3_ROUTER.json'
MOD3 = ROOT / 'data/PART_W33_20260902_MOD3_PGSP_EXTENSION_TWIN.json'
OUT = ROOT / 'data/PART_W33_20260902_MOD3_OUTER_SIGN_FACTORIZATION.json'


def q(s):
    return Fraction(str(s))


def sign_of(x: Fraction) -> int:
    if x > 0:
        return 1
    if x < 0:
        return -1
    raise ValueError('zero cannot define a projective parity sign')


def relation_sign(name: str) -> int:
    if name == '+S':
        return 1
    if name == '-S':
        return -1
    raise ValueError(f'unsupported solved outer relation: {name!r}')


def main():
    router = json.loads(ROUTER.read_text())
    mod = json.loads(MOD3.read_text())
    assert router['status'] == 'PASS'
    assert mod['status'] == 'PASS' and mod['field'] == 'F3'
    assert mod['allThreeImagesOuterInvariant'] is True

    Jraw = router['St81']['projectiveConjugatorJ']
    J = [[q(x) for x in row] for row in Jraw]
    assert len(J) == 3 and all(len(row) == 3 for row in J)
    assert all(J[i][j] == 0 for i in range(3) for j in range(3) if i != j)
    assert all(J[i][i] != 0 for i in range(3))

    # Projective normalization: primitive 0 is +.  This is exactly the
    # normalization used when the current rational router theorem is stated.
    scale = J[0][0]
    diag = [J[i][i] / scale for i in range(3)]
    assert all(abs(x) == 1 for x in diag)
    rational = [sign_of(x) for x in diag]
    assert rational == [1, 1, -1]

    tr = mod['solvedTransports']
    even = relation_sign(tr['obstructionCommonEvenReduction']['relationToBuildingOuterS'])
    odd = relation_sign(tr['obstructionOddReduction']['relationToBuildingOuterS'])
    modular = [even, even, odd]
    assert modular == [-1, -1, 1]

    eta = [modular[i] * rational[i] for i in range(3)]  # inverse=r_i for signs
    assert eta[0] == eta[1] == eta[2]
    uniform = eta[0]
    assert uniform == -1
    assert all(modular[i] == uniform * rational[i] for i in range(3))

    # In F3 notation -1 is 2.  Freeze both human and field forms.
    out = {
        'schema': 'w33.20260902.mod3-outer-sign-factorization.v1',
        'status': 'PASS',
        'field': 'F3',
        'rationalInput': {
            'certificate': str(ROUTER.relative_to(ROOT)),
            'projectiveJ81': Jraw,
            'normalization': 'divide by J81[0,0], so primitive 0 has sign +1',
            'primitiveMultiplicitySigns': rational,
        },
        'mod3Input': {
            'certificate': str(MOD3.relative_to(ROOT)),
            'primitiveChainMapSignsRelativeToBuildingS': modular,
            'primitive0And1Source': 'obstructionCommonEvenReduction',
            'primitive2Source': 'obstructionOddReduction',
        },
        'factorization': {
            'relativeInjectionFactorByPrimitive': eta,
            'uniformRelativeInjectionFactor': uniform,
            'uniformRelativeInjectionFactorF3': uniform % 3,
            'productLaw': 'm_i = eta * r_i for i=0,1,2',
            'verifiedForAllThreePrimitives': True,
        },
        'theorem': (
            'In the deterministic normalization of the rational St81 multiplicity frame, '
            'the rational outer signs (+,+,-) and the solved modular chain-map signs (-,-,+) '
            'differ by one uniform factor eta=-1. Thus the characteristic-3 sign reversal '
            'factorizes exactly as modular PGSp sign = (uniform outer-odd integral-injection '
            'factor) x (rational multiplicity sign).'
        ),
        'normalizationBoundary': (
            'J81 is projective, so multiplying J81 by -1 moves one global sign between the '
            'rational factor and eta. The invariant content is that the quotient m_i/r_i is '
            'constant across all three primitive channels and the product law holds exactly.'
        ),
        'physicsBoundary': (
            'The signs are finite PGSp-extension data for explicit chain maps. They are not '
            'by themselves spacetime parity, chirality, charge conjugation, or a particle label.'
        ),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'status': 'PASS', 'rational': rational, 'modular': modular,
                      'eta': eta, 'uniform': uniform}, sort_keys=True))


if __name__ == '__main__':
    main()
