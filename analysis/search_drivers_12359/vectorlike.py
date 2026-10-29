"""12359 validation: the 4D massless fermions of a sub-orbifold with a fixed torus come from a 6D theory on T^2 and must be
vector-like -- the left-handed (m = 19) weight multiset is symmetric under w -> -w.  The chiral parent must fail (contrast)."""
import collections, json, sys
def weights(p, mcode=19):
    c = collections.Counter(); cur = None
    for l in open(p, errors='ignore'):
        if l.startswith('FIELD'):
            cur = int(l.split()[2][2:])
        elif l.startswith('W ') and cur == mcode:
            c[tuple(round(float(x), 6) + 0.0 for x in l[2:].split(','))] += 1
    return c
out = {}
for tag in ('parent', 'sub2', 'sub3'):
    c = weights(f'm2913v6_{tag}.nsoq')
    neg = collections.Counter({tuple(-x + 0.0 for x in w): n for w, n in c.items()})
    asym = sum((c - neg).values())
    out[tag] = dict(left_weights=sum(c.values()), unpaired=asym, vectorlike=asym == 0)
    print(tag, out[tag])
json.dump(out, open('vectorlike.json', 'w'), indent=1)
