"""12299: right-moving levels R^2/2 - 1/2 + dc(n) for every state of the parent (and the candidate brother); control: every massless-type
state must give 0.  If the engine's tachyon-labelled states (m = 21-24) also give 0 on both sides, they are level-matched massless
states and the label does not mean tachyonic (suspected engine labelling, to be confirmed against the engine's own tachyon mass)."""
import re, json, collections
from fractions import Fraction as F
v = [F(1, 6), F(1, 3), F(-1, 2)]
dc = lambda n: sum(F(1, 2) * ((n * x) % 1) * (1 - ((n * x) % 1)) for x in v)
def run(p):
    L = open(p).read().split('\n'); out = collections.Counter()
    for i, l in enumerate(L):
        if l.startswith('FIELD'):
            m = re.match(r'FIELD \d+ m=(\S+) k=\S+ mm=(\S+) n=(\S+) ', l)
            j = i + 1; Rs = []
            while j < len(L) and not L[j].startswith(('FIELD', 'END')):
                if L[j].startswith('R '):
                    Rs.append([F(x).limit_denominator(12) for x in L[j][2:].split(',')])
                j += 1
            kind = 'tachyon-type' if int(m.group(1)) in (21, 22, 23, 24) else 'massless-type'
            for R in Rs[:1]:
                lev = sum(x * x for x in R) / 2 - F(1, 2) + dc(int(m.group(3)))
                out[(kind, str(lev))] += 1
    return out
res = {}
for tag in ('ctrl', 'w6odd'):
    o = run(f'../search_drivers_12281/bro/Z6II_60_SM_20260917_810_v9__{tag}.nsoq')
    res[tag] = {str(k): v2 for k, v2 in o.items()}
    print(tag, dict(o))
json.dump(res, open('rlevels.json', 'w'), indent=1)
