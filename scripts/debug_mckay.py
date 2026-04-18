#!/usr/bin/env python3
from __future__ import annotations

from fractions import Fraction
from pprint import pprint
from pathlib import Path
import sys

# ensure repo root and exploration are on sys.path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "exploration"))

from w33_mckay_thompson_eta_quotients import (
    ETA_QUOTIENT_PARAMS,
    _eta_quotient_no_pole,
    eta_quotient_laurent,
    dual_eta_quotient,
    mckay_thompson_T_pA,
    T_pA_REFERENCE_COEFFS,
)


def debug_one(p, k, N=6):
    print('\n--- p=', p, 'k=', k)
    inner = _eta_quotient_no_pole(p, k, N)
    print('inner len', len(inner), 'sample', [int(x) for x in inner[:8]])
    eta_q = eta_quotient_laurent(p, k, N)
    print('eta_q len', len(eta_q), 'sample', [int(x) for x in eta_q[:8]])
    dual = dual_eta_quotient(p, k, N)
    print('dual len', len(dual), 'sample', [int(x) for x in dual[:8]])
    coefs, c_p = mckay_thompson_T_pA(p, N)
    print('mckay coefs first 8 (q^-1..q^6):', [int(x) for x in coefs[:8]])
    print('c_p:', int(c_p))
    ref = T_pA_REFERENCE_COEFFS.get(p)
    if ref:
        print('reference q^1..q^5:', ref)
        got = [int(coefs[2 + j]) for j in range(len(ref))]
        print('got q^1..q^5:', got)
        diffs = [got[i] - ref[i] for i in range(len(ref))]
        print('diffs:', diffs)


def main():
    for p, k in ETA_QUOTIENT_PARAMS:
        debug_one(p, k, N=6)


if __name__ == '__main__':
    main()
