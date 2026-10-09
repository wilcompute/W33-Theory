"""Gauge/hidden-SU2/twist necessary superpotential filters on the NEW
Pass11796 thirteen-VEV, full-field Z2 D-flat Higgs branch.
No claim of string R/space-group rule completeness or physical F-flatness.
"""
from pathlib import Path
from itertools import combinations_with_replacement
from collections import Counter
import gzip,json
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parents[1]
MODEL='Z6-II|Z6II_34__SM_20260917_1558'
SUP=['n_17','n_47','n_50','n_80','n_82','n_9','n_54','n_37','n_38','n_35','n_36','n_39','n_40']
DOUB={'n_35','n_36','n_39','n_40'}
def main():
    raw=json.load(gzip.open(ROOT/'data/w33_pass10960_heterotic_left_chiral_ledger.json.gz','rt'))[MODEL]
    fields={f['name']:f for f in raw['left']}
    par=json.load(open(ROOT/'data/w33_pass11796_parity_complete_abelian_higgs.json'))
    assert set(SUP)==set(par['symbolic_squared_VEV_norms'])
    charges={n:tuple(F(z) for z in x['q']) for n,x in fields.items()}
    kval={n:int(x['k']) for n,x in fields.items()}
    parity=par['all176_field_parities']
    out={};counts=Counter()
    def allowed(seq):
        q=tuple(sum(charges[n][i] for n in seq) for i in range(9))
        if any(q):return False,False,False
        pg=sum(kval[n] for n in seq)%6==0
        even=sum(parity[n] for n in seq)%2==0
        # Necessary and sufficient nonzero SU(2) singlet for <=4 factors:
        # no doublets, or two DISTINCT doublet superfields, or four
        # capable of pairings into distinct-field epsilon contractions.
        reps=[fields[n]['dim'].split(',') for n in seq]
        other_nonabelian=any(any(d!='1' for d in rep[:3]) for rep in reps)
        dd=[n for n,rep in zip(seq,reps) if rep[3]=='2']
        if len(dd)==0: su=True
        elif len(dd)==2: su=dd[0]!=dd[1]
        elif len(dd)==4:
            a,b,c,d=dd
            su=(a!=b and c!=d) or (a!=c and b!=d) or (a!=d and b!=c)
        else:su=False
        return True,pg,even and su and not other_nonabelian
    for degree in (2,3,4):
        for x in combinations_with_replacement(SUP,degree):
            gauge,sector,represent=allowed(x)
            if not gauge:continue
            counts['gauge_s'+str(degree)]+=1
            if sector:counts['pg_s'+str(degree)]+=1
            if sector and represent:
                counts['candidate_s'+str(degree)]+=1
                if degree==2:out.setdefault('bilinears',[]).append(list(x))
        if degree<=4:
            for x in combinations_with_replacement(SUP,degree-1):
                for n in fields:
                    if n in SUP:continue
                    gauge,sector,represent=allowed(x+(n,))
                    if not gauge:continue
                    counts['gauge_out'+str(degree)]+=1
                    if sector:counts['pg_out'+str(degree)]+=1
                    if sector and represent:
                        counts['candidate_out'+str(degree)]+=1
                        if degree==2:out.setdefault('one_outsider_bilinears',[]).append(list(x+(n,)))
    return dict(status='PASS',schema='w33.20261009.13vev_F_filter.v1',
        support=SUP,hidden_doublets=sorted(DOUB),charge_rank=8,
        enumeration_degree_max=4,candidate_counts=dict(counts),
        examples=out,
        no_constant_or_linear_support_terms=True,
        boundary='U1 neutrality exact, twist k sum and hidden SU2 contraction checked. Space-group, gamma, H-momentum/R-charge, oscillator, nonperturbative couplings and cancellations NOT checked. Degree-2 terms are gauge-eligible only, not proven generated.')
if __name__=='__main__':
    out=main()
    (ROOT/'data/w33_20261009_new_higgs_13vev_F_filter.json').write_text(json.dumps(out,indent=2)+'\n')
    print('COUNTS',out['candidate_counts'])
    print('BILINEARS',out['examples'].get('bilinears'))
