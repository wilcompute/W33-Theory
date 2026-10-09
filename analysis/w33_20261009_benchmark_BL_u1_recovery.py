"""Recover published B-L as a linear form on the local orbifolder 9 U1 charges.

Use exact rational left-chiral SP charge vectors and independent gauge-weight
P readout as anchor, after the explicit Weyl root-isometry. A consistency
failure is reported rather than bypassed. Do not assume unique coordinates.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict
import gzip,json
import sympy as s
import w33_20261009_benchmark_BL_weight_probe as B
ROOT=Path(__file__).resolve().parents[1]
NAME=B.NAME
def recover():
    raw=json.load(gzip.open(ROOT/'data/w33_pass10960_heterotic_left_chiral_ledger.json.gz','rt'))
    fields={f['name']:f for f in raw['Z6-II|'+NAME]['left']}
    t=B.derived_vector()
    file=Path.home()/'orb'/'scan'/'cp2'/'out'/(NAME+'.w')
    observed={}
    for line in file.read_text().splitlines():
        if not line.startswith('W '):continue
        label=line.split()[1]
        if label not in fields or 'P=' not in line:continue
        p=[float(x) for x in line.split('P=',1)[1].split()[0].split(',')]
        if len(p)!=16:continue
        val=sum(float(a)*b for a,b in zip(t,p))
        rational=F(val).limit_denominator(216)
        assert abs(val-float(rational))<1e-6,(label,val,rational)
        if label in observed:assert observed[label]==rational,(label,observed[label],rational)
        observed[label]=rational
    A=s.Matrix([[s.Rational(q) for q in fields[label]['q']] for label in observed])
    b=s.Matrix([s.Rational(str(x)) for x in observed.values()])
    print('anchors',len(observed),'rank',A.rank(),'aug_rank',A.row_join(b).rank())
    if A.rank()!=A.row_join(b).rank():
        return dict(status='INCONSISTENT_ANCHORS',anchors=len(observed))
    solved,params=A.gauss_jordan_solve(b)
    particular=solved.subs({p:0 for p in params})
    pred={}
    for f in fields.values():
        base=f['name'].rsplit('_',1)[0]
        if base not in ('q','bu','bd','be','n'):continue
        pred[f['name']]=str((s.Matrix([[s.Rational(q) for q in f['q']]])*particular)[0])
    cert=json.load(open(ROOT/'data/w33_pass10960_matter_even_dflat_closure.json'))
    witness=cert['models']['Z6-II|'+NAME]['dflat_witness']
    print('coordinates',list(map(str,particular)),'degrees freedom',len(params))
    print('q/bu/bd/be',{role:{k:v for k,v in pred.items() if k.startswith(role+'_')} for role in ('q','bu','bd','be')})
    print('Dflat witness B-L',{x:pred.get(x) for x in witness})
    return dict(status='PASS',observed_anchor_count=len(observed),
        rank=A.rank(),basis_coefficients=[str(x) for x in particular],
        degrees_freedom=len(params),predicted_BminusL=pred,
        dflat_witness=cert['models']['Z6-II|'+NAME]['dflat_witness'],
        dflat_BminusL={x:pred.get(x) for x in witness},
        scope='Gauge-weight projections derived from benchmark tBL and recovered Weyl map. Verify family assignment and legitimate inversion before claiming a physical vacuum.')
if __name__=='__main__':
    x=recover()
    (ROOT/'data/w33_20261009_benchmark_BL_u1_recovery.json').write_text(json.dumps(x,indent=2)+'\n')
