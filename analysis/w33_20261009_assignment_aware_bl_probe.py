"""Assignment-aware B-L re-audit for 2008 benchmark gauge-congruent W33 candidate.

Crucial distinction: 10 bd-labelled representations comprise 4 standard -1/3
and 6 exotic +2/3 under the benchmark's B-L, so the Pass10960 all-bd=-1/3
gate has no solution for this candidate. We do not mutate the old ledger.
"""
from fractions import Fraction as F
from pathlib import Path
import gzip,json,re,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass10960_matter_even_dflat_closure as old
MODEL='Z6-II|Z6II_34__SM_20260917_1558'
GOOD_BD={'bd_3','bd_5','bd_9','bd_10'}
def run():
    ledger=json.load(gzip.open(ROOT/'data/w33_pass10960_heterotic_left_chiral_ledger.json.gz','rt'))
    ff=[]
    for f in ledger[MODEL]['left']:
        dims=f['dim'].split(',')
        ff.append(dict(name=f['name'],base=old.base_of(f['name']),
            trivial=all(abs(int(re.match(r'(-?\d+)',d).group(1)))==1 and 'adj' not in d for d in dims),
            dimprod=abs(__import__('math').prod(int(re.match(r'(-?\d+)',d).group(1)) for d in dims)),
            q=[F(q) for q in f['q']]))
    y=old.solve_affine([f['q'] for f in ff if f['base'] in old.SMY],
                       [old.SMY[f['base']] for f in ff if f['base'] in old.SMY])[0]
    sing=[f for f in ff if f['trivial'] and old.dot(y,f['q'])==0]
    types={}
    for f in sing:types.setdefault(tuple(f['q']),[]).append(f['name'])
    T=list(types)
    constraints=[(f['name'],f['q'],old.BL[f['base']]) for f in ff
                 if f['base'] in ('q','bu','be') or f['name'] in GOOD_BD]
    bl=old.solve_affine([x[1] for x in constraints],[x[2] for x in constraints])
    assert bl is not None
    x0,N=bl
    alpha=[3*old.dot(x0,t) for t in T]
    beta=[[3*old.dot(n,t) for n in N] for t in T]
    C=[t[0] for t in T]
    M=[list(t[1:]) for t in T]
    can=[i for i in range(len(T)) if any(beta[i]) or alpha[i].denominator!=1 or alpha[i].numerator%2==0]
    cover=old.farkas([C[i] for i in can],[M[i] for i in can])
    print('fields',len(ff),'singlets',len(sing),'types',len(T),
          'BL conditions',len(constraints),'nullity',len(N),
          'possible even types',len(can),'union flat',cover is None,flush=True)
    rays=old.cone_rays([M[i] for i in can]) if cover is None else []
    neg=0
    hit=None
    for ray in rays:
        support=[can[j] for j,w in enumerate(ray) if w]
        energy=sum(C[can[j]]*w for j,w in enumerate(ray))
        if energy>=0:continue
        neg+=1
        ok,reason=old.realizable([alpha[i] for i in support],[beta[i] for i in support])
        if ok:
            hit=dict(singlet_support=[types[T[i]][0] for i in support],
                 parity_t=reason['t'],
                 positive_coeffs={types[T[can[j]]][0]:str(-w/energy) for j,w in enumerate(ray) if w},
                 anomalous_charge_total='-1',
                 three_BminusL=[str(alpha[i]+old.dot(beta[i],[F(t) for t in reason['t']])) for i in support])
            break
    print('rays',len(rays),'FI cancelling scanned',neg,'candidate',hit,flush=True)
    return dict(extreme_rays=len(rays),fi_canceling_scanned=neg,
                even_Dflat_witness=hit,status='PROBE',BL_constraints=[x[0] for x in constraints],
        BL_nullspace_dim=len(N),types=len(T),ever_even_types=len(can),
        union_even_dflat_possible=cover is None,
        initial_Dflat_witness=[str(a) for a in old.dflat_witness(C,M)],
        x0=[str(t) for t in x0],N=[[str(t) for t in vec] for vec in N])
if __name__=='__main__':
    x=run()
    (ROOT/'data/w33_20261009_assignment_aware_bl_probe.json').write_text(json.dumps(x,indent=2)+'\n')
