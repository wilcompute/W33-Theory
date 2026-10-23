"""12230: the statistics selection of the twisted 10s, read off the projection rule.  For every massless field of a twisted-10 model
(nsoq dump: left weights W in 16 dims, right weights R in 4 dims, sector labels k, Witten mm, n): per sector, the set of values
(W.V0 - R0) mod 1 over all (W, R) pairs, R0 the spacetime component (integral for bosons, half-integral for fermions).  If it is a
single constant c per sector, the rule is R0 = W.V0 - c mod 1; the twisted 10s have W.V0 integral (12225), so they are fermions iff
c = 1/2 in their sectors."""
import json, re, sys
from fractions import Fraction as Fr
from collections import defaultdict
path, model = sys.argv[1], sys.argv[2]
V0 = [Fr(x.strip(',')) for x in open(model).read().split('Shifts and Wilsonlines:')[1].strip().split('\n')[0].replace(',', ' ').split()]
fields, cur = [], None
for l in open(path):
    if l.startswith('FIELD'):
        m = re.match(r'FIELD (\d+) m=(\d+) k=(\d+) mm=(\d+) n=(\d+) .*dim=(\S+)', l)
        cur = dict(m=int(m.group(2)), k=int(m.group(3)), w=int(m.group(4)), n=int(m.group(5)), dim=m.group(6), R=[], W=[])
        fields.append(cur)
    elif l.startswith('R ') and cur is not None:
        cur['R'].append([Fr(x).limit_denominator(24) for x in l[2:].split(',')])
    elif l.startswith('W ') and cur is not None:
        cur['W'].append([Fr(x).limit_denominator(24) for x in l[2:].split(',')])
spacetime = None
for f in fields:
    if f['m'] in (19, 20) and f['R']:
        halves = [i for i in range(4) if all(r[i].denominator == 2 for r in f['R'])]
        if halves:
            spacetime = halves
            break
sector = defaultdict(set)
stat = defaultdict(set)
tens = []
for f in fields:
    if not f['R'] or not f['W']:
        continue
    for W in f['W'][:4]:
        wv = sum(a * b for a, b in zip(W, V0)) % 1
        for R in f['R']:
            sector[(f['k'], f['w'], f['n'])].add(str((wv - R[0]) % 1))
            stat[(f['k'], f['w'], f['n'])].add(('F' if f['m'] in (19, 20) else 'B', str(R[0] % 1)))
    if '10' in f['dim'].split(',')[0].lstrip('-') or any(d.lstrip('-') == '10' for d in f['dim'].split(',')):
        tens.append(dict(m=f['m'], sector=(f['k'], f['w'], f['n']), WV0=str(sum(a * b for a, b in zip(f['W'][0], V0)) % 1), R0=str(f['R'][0][0] % 1)))
out = dict(component_used=0, candidate_spacetime_index=spacetime,
           sectors={str(k): sorted(v) for k, v in sector.items()}, statistics_vs_R0={str(k): sorted(v) for k, v in stat.items()}, tens=tens)
print('sectors with a single (W.V0 - R0) mod 1:', sum(1 for v in sector.values() if len(v) == 1), 'of', len(sector))
for k, v in sorted(sector.items()):
    print(k, sorted(v), sorted(stat[k]))
print('10 states:', tens[:12])
json.dump(out, open('selection.json', 'w'), indent=1, default=str)
