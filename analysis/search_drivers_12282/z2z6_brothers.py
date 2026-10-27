"""12282 (positive SUSY test of the coprime-order rule): the 29 Z2xZ6-I Standard Models (12199; SUSY orbifolder 1.2.1).  W1, W2 have
order 2 on the SO(4) torus, which the Z6-I factor (twist 0, 1/6, -1/6) fixes; its order-2 element commutes with e1, so gcd(2,2) = 2 and
torsion is allowed.  B(e1, (theta'^k, f)) = k V_N.lam / 2: prediction -- among consistent W1 shifts the spectrum depends only on the
parity of V_N.lam.  Per model: control, an 'even' brother (V_N.lam even, other parities nonzero) and an 'odd' brother.
Consistency (prefactors gcd of orders 2, 6, 2): 2 W.V_M, 2 W.V_N, 2 W.W, 2 W1.W2 even."""
import random, json, sys, re
from fractions import Fraction as F
sys.path.insert(0, '../search_drivers_12267')
from mirage import fmt, e8_short
dot = lambda a, b: sum(x * y for x, y in zip(a, b))
even = lambda x: x.denominator == 1 and x % 2 == 0
R8 = [list(r) for r in e8_short(2) if sum(x * x for x in r) == 2]
Z8 = [F(0)] * 8
ROOTS = [r + Z8 for r in R8] + [Z8 + r for r in R8]
rng = random.Random(12282)
CAND = ROOTS + [[x + y for x, y in zip(rng.choice(ROOTS), rng.choice(ROOTS))] for _ in range(3000)]


def ok(rows):
    VM, VN, W1, W2 = rows[0], rows[1], rows[2], rows[3]
    for W, o in ((W1, W2), (W2, W1)):
        if any(W) and not (even(2 * dot(W, VM)) and even(2 * dot(W, VN)) and even(2 * dot(W, W)) and even(2 * dot(W, o))):
            return False
    return True


t = open('z2z6_sm.txt').read()
idx, lst = [], []
for k, blk in enumerate(t.split('begin model')[1:]):
    lab = re.search(r'Label:(\S+)', blk).group(1) + f'_{k:02d}'
    head = 'begin model' + blk.split('Shifts and Wilsonlines:')[0]
    rows = [[F(x) for x in r.replace(',', ' ').split()] for r in blk.split('Shifts and Wilsonlines:')[1].split('end model')[0].strip().split('\n') if r.strip()]
    if not any(rows[2]) or not ok(rows):
        continue
    e = dict(model=lab, files={})
    for tag, want_odd, other in (('even', False, True), ('odd', True, False)):
        for lam in CAND:
            p = dot(lam, rows[1])
            if p.denominator != 1 or (p % 2 == 1) != want_odd:
                continue
            if other and all((2 * dot(lam, rows[j])) % 4 == 0 for j in (0, 2, 3)):
                continue
            new = [r[:] for r in rows]
            new[2] = [x + y for x, y in zip(new[2], lam)]
            if ok(new):
                f = f'bro/{lab}__{tag}.txt'
                open(f, 'w', newline='\n').write(head + 'Shifts and Wilsonlines:\n' + '\n'.join(' '.join(fmt(x) for x in r) for r in new) + '\nend model\n')
                e['files'][tag] = f
                break
    f = f'bro/{lab}__ctrl.txt'
    open(f, 'w', newline='\n').write(head + 'Shifts and Wilsonlines:\n' + '\n'.join(' '.join(fmt(x) for x in r) for r in rows) + '\nend model\n')
    e['files']['ctrl'] = f
    idx.append(e)
    lst += ['/mnt/c/tmp/toe_wt/analysis/search_drivers_12282/' + q for q in e['files'].values()]
json.dump(idx, open('index.json', 'w'), indent=1)
open('list.txt', 'w', newline='\n').write('\n'.join(lst) + '\n')
print(len(idx), [sorted(e['files']) for e in idx][:2])
