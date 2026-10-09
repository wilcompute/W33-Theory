"""Necessary F-flatness screen for the exact six-singlet FI-cancelling support.

Enumerate gauge-neutral superpotential monomials of total degree <= 9,
either supported-only (type A) or exactly one outside field (type B).
Also report sector twist k mod 6 necessary condition. No geometry/fixed-point
space-group/R-charge/gamma/oscillator selection rules are imposed.
"""
from pathlib import Path
from itertools import combinations_with_replacement
from collections import Counter
from fractions import Fraction as F
import json,gzip
ROOT=Path(__file__).resolve().parents[1]
MODEL='Z6-II|Z6II_34__SM_20260917_1558'
SUPPORT=['n_1','n_19','n_54','n_56','n_80','n_82']
def certificate(max_degree=9):
    raw=json.load(gzip.open(ROOT/'data/w33_pass10960_heterotic_left_chiral_ledger.json.gz','rt'))[MODEL]
    fields={f['name']:f for f in raw['left']}
    assert all(f in fields for f in SUPPORT)
    q={k:tuple(F(x) for x in v['q']) for k,v in fields.items()}
    k={j:int(v['k']) for j,v in fields.items()}
    def charges(combo):
        return tuple(sum(q[name][i] for name in combo) for i in range(9))
    examples={'A_all':[], 'B_all':[], 'A_point_group':[], 'B_point_group':[]}
    counts=Counter()
    outsiders=sorted(set(fields)-set(SUPPORT))
    for degree in range(1,max_degree+1):
        for comb in combinations_with_replacement(SUPPORT,degree):
            Q=charges(comb);K=sum(k[n] for n in comb)%6
            if all(v==0 for v in Q):
                counts['A_all']+=1
                if len(examples['A_all'])<12:examples['A_all'].append(comb)
                if K==0:
                    counts['A_point_group']+=1
                    if len(examples['A_point_group'])<12:examples['A_point_group'].append(comb)
            if degree+1>max_degree:continue
            for n in outsiders:
                if all(Q[i]+q[n][i]==0 for i in range(9)):
                    counts['B_all']+=1
                    if len(examples['B_all'])<12:examples['B_all'].append(comb+(n,))
                    if (K+k[n])%6==0:
                        counts['B_point_group']+=1
                        if len(examples['B_point_group'])<12:examples['B_point_group'].append(comb+(n,))
    return dict(status='PASS',max_degree=max_degree,source=MODEL,
        support=SUPPORT,all_fields=len(fields),counts=dict(counts),examples={j:[list(x) for x in v] for j,v in examples.items()},
        result_scope='Gauge charge exact and point-group k necessary only. No full Z6-II space-group/fixed-point, H-momentum, R-charge, gamma selection, physical superpotential coefficients, or cancellations. Absence through a degree is a rigorous gauge-only obstruction within the selected support; presence is NOT proof of generated couplings or F obstruction.')
if __name__=='__main__':
    x=certificate()
    (ROOT/'data/w33_20261009_six_vev_F_term_gate.json').write_text(json.dumps(x,indent=2)+'\n')
    print(x)
