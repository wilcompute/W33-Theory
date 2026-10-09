"""All-degree one-outsider F-term gauge screen for the six-field FI support.

The six 9-component rational support charge vectors have rank six.
Consequently for ANY named outsider X, gauge neutrality fixes at most
one exponent vector n in Qsupport*n = -Q_X; it is integral/nonnegative
or no such holomorphic monomial can exist. This is exhaustive at ALL orders.
"""
from pathlib import Path
from fractions import Fraction
import json,gzip
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
MODEL='Z6-II|Z6II_34__SM_20260917_1558'
SUPPORT=['n_1','n_19','n_54','n_56','n_80','n_82']
def main():
    dat=json.load(gzip.open(ROOT/'data/w33_pass10960_heterotic_left_chiral_ledger.json.gz','rt'))[MODEL]
    fields={x['name']:x for x in dat['left']}
    q={n:sp.Matrix([sp.Rational(a) for a in v['q']]) for n,v in fields.items()}
    mat=sp.Matrix.hstack(*(q[n] for n in SUPPORT))
    assert mat.rank()==6
    sol=[]
    for name,raw in fields.items():
        if name in SUPPORT:continue
        try:
            n,params=mat.gauss_jordan_solve(-q[name])
        except ValueError:
            continue
        assert not params
        if not all(z.q==1 and z>=0 for z in n):continue
        ns=tuple(int(z) for z in n)
        deg=1+sum(ns)
        sector=(int(raw['k'])+sum(ns[i]*int(fields[t]['k']) for i,t in enumerate(SUPPORT)))%6
        row=dict(outside=name,exponents=dict((SUPPORT[i],v) for i,v in enumerate(ns) if v),
            total_degree=deg,point_group_sector_mod6=sector,
            outsider_multiplicity=raw.get('dim'),representation=raw.get('dim'))
        assert mat*n+q[name]==sp.zeros(9,1)
        sol.append(row)
    sol.sort(key=lambda z:(z['total_degree'],z['outside']))
    return dict(status='PASS',schema='w33.20261009.all_degree_one_outsider.v1',
        support_charge_rank=6,outside_tested=len(fields)-6,
        all_order_candidates=len(sol),max_observed_degree=max((z['total_degree'] for z in sol),default=0),
        point_group_sector_zero=sum(z['point_group_sector_mod6']==0 for z in sol),
        monomials=sol,
        theorem='Full support Q matrix has trivial nullspace. For each outsider, at most one rational exponent solution exists. The scan of ALL 170 outsiders is thus complete for holomorphic monomials with exactly one field outside the VEV support, with no imposed degree cutoff.',
        boundary='Necessary gauge invariance and basic point-group only. No fixed-point selection, H momentum, R charges, oscillator, gamma, and no superpotential coefficients, F-flatness proof or cancellation with two-or-more outsiders.')
if __name__=='__main__':
    d=main()
    (ROOT/'data/w33_20261009_all_order_one_outsider_F_gate.json').write_text(json.dumps(d,indent=2)+'\n')
    print('ALL_ORDER',d['all_order_candidates'],'MAXDEG',d['max_observed_degree'],'PGZERO',d['point_group_sector_zero'])
    print([(x['outside'],x['total_degree']) for x in d['monomials']])
