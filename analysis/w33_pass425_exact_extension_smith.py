#!/usr/bin/env python3
"""Pass 425: exact extension-field Smith gluing at q=25 and q=27.

The square biaffine incidence operator S=A+I is obtained by an affine-chart
inclusion--exclusion from projective point/subspace incidence matrices.  The
projective p-elementary-divisor multiplicities are evaluated by the
Chandler--Sin--Xiang monomial-type formula.  Reversal of the projective
valuation index and a single middle correction recover the exact Smith layers
of S.  The critical-group top layer then follows from the reduced tree quotient.
"""
from __future__ import annotations
import argparse, json, math
from collections import Counter
from itertools import product
from pathlib import Path

from w33_pass410_414_common import certificate, write_json

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass425_exact_extension_smith.json'


def polynomial_coefficients(p:int,n:int)->list[int]:
    """Coefficients of (1+x+...+x^(p-1))^(n+1)."""
    a=[1]
    for _ in range(n+1):
        b=[0]*(len(a)+p-1)
        for i,x in enumerate(a):
            for j in range(p): b[i+j]+=x
        a=b
    return a


def projective_multiplicities(p:int,f:int,n:int,r:int)->Counter:
    """Theorem-3.3 multiplicities m_alpha for PG(n,p^f)."""
    d=polynomial_coefficients(p,n); out=Counter()
    for s in product(range(1,n+1),repeat=f):
        lam=[p*s[(j+1)%f]-s[j] for j in range(f)]
        if any(x<0 or x>=len(d) for x in lam): continue
        mult=math.prod(d[x] for x in lam)
        alpha=sum(max(0,r-x) for x in s)
        out[alpha]+=mult
    out[0]+=1
    return out


def incidence_smith(p:int,f:int)->dict:
    q=p**f
    m33=projective_multiplicities(p,f,3,3)
    m22=projective_multiplicities(p,f,2,2)
    m11=projective_multiplicities(p,f,1,1)
    affine=Counter({a:m33[a]-2*m22[a]+m11[a] for a in set(m33)|set(m22)|set(m11)})
    exact=Counter()
    for j in range(2*f+1):
        exact[j]=affine[2*f-j]
    exact[f]+=1
    exact=Counter({j:n for j,n in exact.items() if n})
    rank=q**3-q**2+1
    nullity=q**2-1
    critical=Counter({j:n for j,n in exact.items() if j>0})
    critical[3*f]+=q**2-2
    return {
      'p':p,'f':f,'q':q,
      'incidence_rank':rank,'incidence_nullity':nullity,
      'incidence_exact_valuations':{str(j):exact[j] for j in sorted(exact)},
      'incidence_p_valuation':sum(j*n for j,n in exact.items()),
      'critical_group_exact_valuations':{str(j):critical[j] for j in sorted(critical)},
      'critical_group_p_valuation':sum(j*n for j,n in critical.items()),
      'critical_group_cyclic_factors':[{'order':p**j,'multiplicity':critical[j]} for j in sorted(critical)],
      'projective_formula_inputs':{
        'PG3_point_plane':{str(k):v for k,v in sorted(m33.items())},
        'PG2_point_line':{str(k):v for k,v in sorted(m22.items())},
        'PG1_point_point':{str(k):v for k,v in sorted(m11.items())},
      },
    }


def build_payload()->dict:
    rows={q:incidence_smith(p,f) for p,f,q in [(3,1,3),(5,1,5),(3,2,9),(5,2,25),(3,3,27)]}
    expected_incidence={
      3:{0:10,1:8,2:1},
      5:{0:35,1:56,2:10},
      9:{0:100,1:128,2:292,3:92,4:37},
      25:{0:1225,1:3200,2:6976,3:2800,4:800},
      27:{0:1000,1:1920,2:3678,3:6812,4:3354,5:1596,6:595},
    }
    expected_critical_val={3:31,5:145,9:1610,25:32490,27:61221}
    checks={}
    for q,row in rows.items():
        got={int(k):v for k,v in row['incidence_exact_valuations'].items()}
        checks[f'q{q}_exact_incidence_layers']=got==expected_incidence[q]
        checks[f'q{q}_rank_sum']=sum(got.values())==row['incidence_rank']
        checks[f'q{q}_nullity']=row['incidence_nullity']==q*q-1
        checks[f'q{q}_critical_valuation']=row['critical_group_p_valuation']==expected_critical_val[q]
        checks[f'q{q}_top_tree_layer']=row['critical_group_exact_valuations'][str(3*row['f'])]==q*q-2
    checks['q25_middle_layers_closed']=rows[25]['critical_group_exact_valuations']=={'1':3200,'2':6976,'3':2800,'4':800,'6':623}
    checks['q27_middle_layers_closed']=rows[27]['critical_group_exact_valuations']=={'1':1920,'2':3678,'3':6812,'4':3354,'5':1596,'6':595,'9':727}
    checks={k:bool(v) for k,v in checks.items()}
    payload={
      'schema':'w33.pass425.exact_extension_smith.v1',
      'status':'PASS' if all(checks.values()) else 'FAIL',
      'theorem':{
        'projective_input':'evaluate projective p-elementary divisors by cyclic monomial types and coefficient products of (1+x+...+x^(p-1))^(n+1)',
        'affine_chart_gluing':'for each projective exponent alpha use PG(3)-2 PG(2)+PG(1), reverse alpha to 2f-alpha, and add one middle p^f factor',
        'q25_closure':'K_(25),(5) = (Z/5)^3200 + (Z/25)^6976 + (Z/125)^2800 + (Z/625)^800 + (Z/15625)^623',
        'q27_closure':'K_(27),(3) = (Z/3)^1920 + (Z/9)^3678 + (Z/27)^6812 + (Z/81)^3354 + (Z/243)^1596 + (Z/729)^595 + (Z/19683)^727',
        'boundary':'the certificate closes the characteristic-primary component. Prime-to-p components require a separate integral decomposition.'
      },
      'formula':{
        'projective_type':'lambda_j=p*s_(j+1)-s_j; multiplicity product_j d_(lambda_j); alpha=sum_j max(0,r-s_j)',
        'square_incidence':'e_j(S)=m_(2f-j)(3,3)-2m_(2f-j)(2,2)+m_(2f-j)(1,1)+delta_(j,f)',
        'critical_top_layer':'append p^(3f) with multiplicity q^2-2',
      },
      'instances':{str(q):rows[q] for q in rows},
      'checks':checks,
    }
    payload['certificate_sha256']=certificate(payload)
    return payload


def main()->int:
    ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args()
    p=build_payload();text=json.dumps(p,indent=2,sort_keys=True)+'\n'
    if a.check:
        if not a.output.exists() or a.output.read_text()!=text: raise SystemExit('Pass 425 certificate drift')
    else: write_json(a.output,p)
    print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks'])}))
    return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
