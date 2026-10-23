"""12199b: refined triviality.  A Wilson line W_2t in Gamma still enters the projection through half-integer phases, so the
translation pairs fixed points with identical spectra only if every product of W_2t with the shifts and the other Wilson
lines is EVEN.  Test on the 29 Z2xZ6-I SMs: for each WL-trivial plane-1 direction, parity of the products vs the parity of the
net quark doublets in the paired (odd-k) sectors."""
import json, re
from fractions import Fraction as F
txt = open('C:/tmp/toe_round/stype/z2z6_sm.txt').read()
cen = json.load(open('z2z6census.json'))
dot = lambda a, b: sum(x * y for x, y in zip(a, b))
def in_e8(v):
    return (all(x.denominator == 1 for x in v) or all(x.denominator == 2 for x in v)) and sum(v) % 2 == 0
out = {}
for blk in txt.split('begin model')[1:]:
    lab = re.search(r'Label:(\S+)', blk).group(1)
    rows = [[F(x.strip(',')) for x in s.replace(',', ' ').split()] for s in blk.split('Shifts and Wilsonlines:')[1].split('end model')[0].strip().splitlines()]
    V1, V2, W1, W2 = rows[0], rows[1], rows[2], rows[3]
    key = [k for k in cen if k.endswith('__' + lab)][0]
    for name, w in (('W1', W1), ('W2', W2), ('W1+W2', [a + b for a, b in zip(W1, W2)])):
        if not (in_e8(w[:8]) and in_e8(w[8:])):
            continue
        others = [V1, V2] + [x for x in rows[2:] if x is not w]
        prods = [dot(w, o) for o in (V1, V2, W1, W2)] + [dot(w, w) / 2]
        even = all(p.denominator == 1 and p % 2 == 0 for p in prods)
        out[key + ':' + name] = dict(products=[str(p) for p in prods], all_even=even, odd_net=cen[key]['odd'])
for k, v in out.items():
    print(k, v)
agree = all(v['all_even'] == (v['odd_net'] % 2 == 0) for v in out.values())
print('criterion (all products even) <=> paired-sector net even:', agree, len(out))
json.dump(dict(cases=out, agree=agree), open('refined.json', 'w'), indent=1)
