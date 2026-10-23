"""12211: order-3 Scherk-Schwarz on T6/Z3, exhaustively.  theta = rotation v = (1/3, 1/3, -2/3) (spinor lift with sum 0).
A candidate theta' = rotation v' (every lift v'_j in {-1, -2/3, ..., 1}) plus an order-3 translation (12207).  Interpolation
requires every SUSY-breaking element theta^b theta'^a (a = 1, 2; b = 0, 1, 2) to act freely: some plane unrotated by it.
Then compute the phase of the theta-invariant 4D gravitino (internal spinor weights s = +-(1/2, 1/2, 1/2)) under theta':
a Z3 Scherk-Schwarz twist needs a primitive cube root of unity."""
import itertools, json
from fractions import Fraction as F
import cmath

v = (F(1, 3), F(1, 3), F(-2, 3))
lifts = [F(k, 3) for k in range(-3, 4)]
s_list = [(F(1, 2),) * 3, (F(-1, 2),) * 3]
assert all(sum(a * b for a, b in zip(s, v)).denominator == 1 for s in s_list)  # gravitino theta-invariant
out = []
for vp in itertools.product(lifts, repeat=3):
    if all((3 * x).denominator == 1 and (x % 1) == 0 for x in vp):
        continue  # pure translation: cannot act on the gravitino
    free = all(any(((b * v[j] + a * vp[j]) % 1) == 0 for j in range(3)) for a in (1, 2) for b in (0, 1, 2))
    if not free:
        continue
    phases = sorted({str(sum(a * b for a, b in zip(s, vp)) % 1) for s in s_list})
    out.append(dict(vp=[str(x) for x in vp], gravitino_phase_exponents=phases))
kinds = sorted({tuple(o['gravitino_phase_exponents']) for o in out})
print('free order-3 rotations (all lifts):', len(out), ' gravitino phase exponents occurring:', kinds)
prim = [o for o in out if any(p in ('1/3', '2/3') for p in o['gravitino_phase_exponents'])]
print('with a primitive cube-root gravitino phase:', len(prim))
json.dump(dict(free=out, phase_kinds=[list(k) for k in kinds], primitive=len(prim)), open('z3ss.json', 'w'), indent=1)
