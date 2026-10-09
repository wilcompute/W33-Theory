"""Probe whether published model-1 B-L survives the explicit gauge Weyl map.

Only checks candidate source massless weight P momentum; original orbifolder
W gauge-momentum lines are not automatically a supersymmetric vacuum map.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict
import gzip,json,re
ROOT=Path(__file__).resolve().parents[1]
NAME='Z6II_34__SM_20260917_1558'
BL=(F(0),F(0),F(0),F(0),F(0),F(-2,3),F(-2,3),F(-2,3),
    F(0),F(0),F(0),F(0),F(0),F(2),F(0),F(0))
def derived_vector():
    doc=json.loads((ROOT/'data/w33_20261009_e8_explicit_weyl_congruence.json').read_text())
    result=[]
    for side,wit in enumerate(doc['witnesses']):
        mat=[[F(q) for q in row] for row in wit['orthogonal_weyl_matrix']]
        vec=BL[side*8:(side+1)*8]
        result+= [sum(a*b for a,b in zip(row,vec)) for row in mat]
    return result
def main():
    t=derived_vector()
    ledger=json.load(gzip.open(ROOT/'data/w33_pass10960_heterotic_left_chiral_ledger.json.gz','rt'))
    names={f['name'] for f in ledger['Z6-II|'+NAME]['left']}
    f=Path.home()/'orb'/'scan'/'cp2'/'out'/(NAME+'.w')
    assert f.is_file(),f
    charges=defaultdict(set)
    for line in f.read_text().splitlines():
        if not line.startswith('W '):continue
        parts=line.split()
        name=parts[1]
        if name not in names:continue
        if 'P=' not in line:continue
        p=line.split('P=',1)[1].split()[0]
        coords=[float(x) for x in p.split(',')]
        if len(coords)!=16:continue
        value=sum(float(q)*x for q,x in zip(t,coords))
        charges[name].add(str(F(value).limit_denominator(108)) if abs(float(F(value).limit_denominator(108))-value)<1e-6 else 'FLOAT:'+str(value))
    exact={b: {k:sorted(charges[k]) for k in sorted(charges) if k.rsplit('_',1)[0]==b} for b in ('q','bu','bd','be')}
    print('t_BminusL candidate',list(map(str,t)))
    print('recovered weight fields',len(charges),'of',len(names))
    print('SM candidate B-L charges',json.dumps(exact,indent=2))
    return dict(status='PASS',candidate=NAME,benchmark_BminusL_transformed=[str(x) for x in t],
                charges=exact,weight_fields=len(charges),
                caveat='Requires physical field/sector identification under Z6 generator inversion and exact hypercharge matching; a gauge-space charge calculation is not a parity-preserving flat vacuum.')
if __name__=='__main__':
    out=main()
    (ROOT/'data/w33_20261009_benchmark_BL_weight_probe.json').write_text(json.dumps(out,indent=2)+'\n')
