"""12364 certificate: hypercharge searches (SM_574 v0/v5/v6 infeasible under the base, wide-hidden, no-anomaly and loose value sets;
control SM_2913_v6 feasible in base and loose modes, recovering its parent's k_Y = 5/3) and the Y-independent chirality of SM_1105_v12
(net (1,2;3bar') doublets of the hidden SU(3)').  Mechanism for SM_574: the coloured conditions (three Q, u^c, d^c, no other chiral
coloured state) together with Y-neutrality / vector-likeness of the hidden SU(5) states are already infeasible ('only' runs)."""
import json, os, re, collections, glob
out = {}
for f in sorted(glob.glob('ysearch_*.json')):
    d = json.load(open(f)); out[f[8:-5]] = dict(solutions=len(d['solutions']), kY=[s['kY'] for s in d['solutions']])
m = 'Z6II_59_SM_20260917_1105_v12'; p = f'../search_drivers_12302/bro/{m}__ctrl.nsoq'
c = collections.Counter()
for l in open(p, errors='ignore'):
    mm = re.match(r'FIELD \d+ m=19 k=\S+ mm=\S+ n=\S+ lat=\S+ dim=(\S*)', l)
    if mm: c[tuple(int(re.match(r'-?\d+', x).group(0)) for x in mm.group(1).split(','))] += 1
cj = lambda d: tuple(-x if abs(x) > 2 else x for x in d)
out['SM_1105_v12_net_(1,2,3bar,1)'] = c[(1, 2, -3, 1)] - c[(1, 2, 3, 1)]
print(json.dumps(out, indent=1)); json.dump(out, open('summary.json', 'w'), indent=1)
