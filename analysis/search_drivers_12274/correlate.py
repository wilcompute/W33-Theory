"""12274: B on every commuting pair for all 320 relabellings of 12271, against the measured spectrum change."""
import json, collections, sys
sys.path.insert(0, '.')
from torsion_B import nonzero_B, diff_relabel
R = '../search_drivers_12271/'
per = json.load(open(R + 'relabel_cmp.json'))['per']
oddc = {}
import sys as _s
_s.path.insert(0, '../search_drivers_12267')
from cmp_census import load
for i in range(40):
    o = load(R + f'oddc/{i:03d}_o.nsoq')
    for j in range(2):
        x = load(R + f'relabel/oddc{i:03d}_r{j}.nsoq')
        oddc[f'oddc{i:03d}_r{j}'] = 'identical' if (o[0] == x[0] and o[1] == x[1]) else 'changed'
src = {'even': (R + 'even/{i:03d}_o.txt', 'Z2xZ2'), 'ctrl': (R + 'even/{i:03d}_s0.txt', 'Z2xZ2'),
       'odd': ('../search_drivers_12267/census/{i:04d}_o.txt', 'Z3'), 'oddc': (R + 'oddc/{i:03d}_o.txt', 'Z3')}
tab = collections.Counter(); rows = []
for tag, (pat, geo) in src.items():
    for i in range(40):
        for j in range(2):
            lab = f'{tag}{i:03d}_r{j}' if tag != 'odd' else f'odd{i:04d}_r{j}'
            r0, S, lam = diff_relabel(pat.format(i=i), R + f'relabel/{lab}.txt')
            n, vals = nonzero_B(r0, geo, S, lam)
            if tag == 'oddc':
                ch = oddc[lab]
            else:
                ch = 'identical' if per[lab][0] == 'identical' else 'changed'
            k = (tag, 'B=0' if n == 0 else 'B!=0', ch)
            tab[k] += 1
            rows.append(dict(lab=lab, S=S, nonzeroB=n, values=dict(vals), spectrum=ch))
for k, v in sorted(tab.items()):
    print(k, v)
json.dump(dict(table={str(k): v for k, v in tab.items()}, rows=rows), open('correlate.json', 'w'), indent=1)
