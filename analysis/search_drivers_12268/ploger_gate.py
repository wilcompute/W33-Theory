"""12268: Ploger (7d)-(7f) pre-check for model files handed to the stock non-SUSY orbifolder, whose CheckModularInvariance skips the
Wilson-line product conditions (the failure flag sits inside `if (info) if (verbose)`, and verbose is hard-coded false; see
nonsusy_orbifolder_strict.patch).  Mirrors the engine's prefactors: gcd of the geometry's orders (Z2^W: 2, Z_N: N, Wilson lines: their
allowed order).  usage: py -3 ploger_gate.py FILE...   -> prints PASS / FAIL <conditions> per model; exit 1 if any fail."""
import math, re, sys
from fractions import Fraction as F
dot = lambda a, b: sum(x * y for x, y in zip(a, b))
even = lambda x: x.denominator == 1 and x % 2 == 0


def check(rows, orders=(2, 3, 1), wl_order=3):
    shifts, W = rows[:3], rows[3:9]
    bad = []
    for a, w in enumerate(W):
        if not any(w):
            continue
        for s, n in zip(shifts, orders):
            if any(s) and not even(math.gcd(n, wl_order) * dot(w, s)):
                bad.append(f'7d W{a + 1}.V')
        for b in range(a, 6):
            if any(W[b]) and not even(wl_order * dot(w, W[b])):
                bad.append(f'7e/7f W{a + 1}.W{b + 1}')
    return bad


def models(text):
    for blk in text.split('begin model')[1:]:
        lab = re.search(r'Label:(\S+)', blk)
        body = blk.split('Shifts and Wilsonlines:')[1].split('end model')[0]
        rows = [[F(x) for x in r.replace(',', ' ').split()] for r in body.strip().split('\n') if r.strip()]
        yield (lab.group(1) if lab else '?'), rows


if __name__ == '__main__':
    bad_any = False
    for f in sys.argv[1:]:
        for lab, rows in models(open(f).read()):
            b = check(rows)
            bad_any |= bool(b)
            print(lab, 'PASS' if not b else 'FAIL ' + ' '.join(b))
    sys.exit(1 if bad_any else 0)
