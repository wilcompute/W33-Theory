"""12299b: across 20 census parents with engine 'excited tachyon' (m = 23/24) states: left level P^2/2 + N - 1 + dc and right level
R^2/2 - 1/2 + dc for every state; controls: every massless-type state must give 0 on both sides."""
import re, glob, json, collections
from fractions import Fraction as F
v = [F(1, 6), F(1, 3), F(-1, 2)]
dc = lambda n: sum(F(1, 2) * ((n * x) % 1) * (1 - ((n * x) % 1)) for x in v)
tab = collections.Counter(); n_models = 0
for p in sorted(glob.glob('../search_drivers_12281/bro/*__ctrl.nsoq')):
    L = open(p).read().split('\n')
    if not any(' m=23 ' in l or ' m=24 ' in l for l in L if l.startswith('FIELD')):
        continue
    n_models += 1
    for i, l in enumerate(L):
        if not l.startswith('FIELD'):
            continue
        m = re.match(r'FIELD \d+ m=(\S+) k=\S+ mm=\S+ n=(\S+) ', l)
        j = i + 1; W = R = None; N = F(0)
        while j < len(L) and not L[j].startswith(('FIELD', 'END')):
            t = L[j]
            if t.startswith('W ') and W is None: W = [F(x).limit_denominator(48) for x in t[2:].split(',')]
            if t.startswith('R ') and R is None: R = [F(x).limit_denominator(12) for x in t[2:].split(',')]
            if t.startswith('O '): N += abs(F(re.search(r' N=(\S+)', t).group(1)).limit_denominator(12))
            j += 1
        if W is None or R is None:
            continue
        n = int(m.group(2))
        lev = (sum(x * x for x in W) / 2 + N - 1 + dc(n), sum(x * x for x in R) / 2 - F(1, 2) + dc(n))
        kind = 'excited-tachyon label' if int(m.group(1)) in (23, 24) else 'massless-type'
        tab[(kind, str(lev[0]), str(lev[1]))] += 1
    if n_models == 20:
        break
print(n_models, 'models'); [print(v2, k) for k, v2 in sorted(tab.items())]
json.dump(dict(models=n_models, table={str(k): v2 for k, v2 in tab.items()}), open('excited_check.json', 'w'), indent=1)
