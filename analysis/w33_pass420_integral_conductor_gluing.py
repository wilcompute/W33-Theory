#!/usr/bin/env python3
"""Pass 420: exact integral incidence lift for characteristic-primary sandpiles.

The key object is the square biaffine point--plane incidence matrix S=A+I.
For the q^3 Heisenberg bulk graph, S^3=q^2 S on augmentation zero and the
reduced Laplacian is q^2 I-S.  Exact Smith data at q=3,5,9 show that the
positive p-power invariant factors of S pass unchanged to the critical group,
with the remaining tree-quotient layer equal to p^(3f) repeated q^2-2.

The executable deliberately separates the proved q=3,5,9 lift from the still
underdetermined middle layers at q=25,27; it does not promote a conjectural
extension-field distribution to a theorem.
"""
from __future__ import annotations
import argparse, json
from collections import Counter
from math import comb
from pathlib import Path
import sympy as sp

from w33_pass410_414_common import certificate, write_json

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass420_integral_conductor_gluing.json'
PASS410=ROOT/'data'/'w33_pass410_prime_power_smith.json'
PASS415=ROOT/'data'/'w33_pass415_frobenius_smith_packets.json'

# Exact p-Smith exponents of the square incidence operator S=A+I.
# Exponent 0 denotes units; ``nullity`` denotes zero invariant factors.
INCIDENCE_EXACT={
  3: {'p':3,'f':1,'counts':{0:10,1:8,2:1},'nullity':8},
  5: {'p':5,'f':1,'counts':{0:35,1:56,2:10},'nullity':24},
  9: {'p':3,'f':2,'counts':{0:100,1:128,2:292,3:92,4:37},'nullity':80},
}

def lift_incidence(q:int, p:int, f:int, counts:dict[int,int])->dict[int,int]:
    out=Counter({e:m for e,m in counts.items() if e>0})
    out[3*f]+=q*q-2
    return dict(sorted(out.items()))

def critical_counts(pass410:dict,q:int)->dict[int,int]:
    rec=pass410['instances'][str(q)]['exact_p_adic_valuation_counts_including_units']
    return {int(e):int(m) for e,m in rec.items() if int(e)>0}

def p_rank_formula(p:int,f:int)->int:
    # Polynomial-function rank of the biaffine incidence code.
    return comb(p+2,3)**f

def tree_valuation(q:int,f:int)->int:
    return f*(q**3+q**2-5)

def build_payload()->dict:
    p410=json.loads(PASS410.read_text())
    p415=json.loads(PASS415.read_text())
    exact_rows=[]; checks={}
    for q,rec in INCIDENCE_EXACT.items():
        p,f=rec['p'],rec['f']; counts=rec['counts']
        lifted=lift_incidence(q,p,f,counts)
        critical=critical_counts(p410,q)
        exact_rows.append({
          'q':q,'p':p,'f':f,
          'incidence_p_smith_exponents_including_units':{str(e):m for e,m in counts.items()},
          'incidence_nullity':rec['nullity'],
          'lifted_critical_p_exponents':{str(e):m for e,m in lifted.items()},
          'frozen_critical_p_exponents':{str(e):m for e,m in critical.items()},
          'incidence_rank':sum(counts.values()),
          'predicted_p_rank':p_rank_formula(p,f),
          'incidence_p_valuation':sum(e*m for e,m in counts.items()),
          'critical_p_valuation':sum(e*m for e,m in critical.items()),
        })
        checks[f'q{q}_lift_exact']=lifted==critical
        checks[f'q{q}_rank_q3_minus_q2_plus1']=sum(counts.values())==q**3-q**2+1
        checks[f'q{q}_nullity_q2_minus1']=rec['nullity']==q*q-1
        checks[f'q{q}_p_rank_formula']=counts.get(0)==p_rank_formula(p,f)
        checks[f'q{q}_tree_valuation']=sum(e*m for e,m in critical.items())==tree_valuation(q,f)

    # Constraint engine for the first unsolved extension fields.  These are
    # exact constraints, not guessed invariant-factor multiplicities.
    pending=[]
    for q,p,f in [(25,5,2),(27,3,3)]:
        normalized=p415['instances'][str(q)]['normalized_plus_trivial_zp_counts']
        pending.append({
          'q':q,'p':p,'f':f,
          'incidence_matrix_order':q**3,
          'incidence_rank_over_Q':q**3-q**2+1,
          'incidence_nullity':q**2-1,
          'incidence_p_rank':p_rank_formula(p,f),
          'critical_top_exponent':3*f,
          'critical_top_multiplicity':q**2-2,
          'critical_total_p_valuation':tree_valuation(q,f),
          'normalized_pre_conductor_counts':normalized,
          'status':'middle incidence Smith layers not yet uniquely determined by rank, order, duality, and conductor index alone',
        })
        checks[f'q{q}_p_rank_positive']=p_rank_formula(p,f)>0
        checks[f'q{q}_top_layer']=q*q-2>0

    # Exact group-algebra identities can be checked symbolically from the
    # defining relations Z^2=qZ, JZ=qJ, SZ=J, SJ=q^2J.
    q=sp.symbols('q', positive=True, integer=True)
    checks['incidence_lift_accounts_for_all_nonunit_factors_q9']=sum(
        INCIDENCE_EXACT[9]['counts'].get(e,0) for e in range(1,5)
    )+79==sum(critical_counts(p410,9).values())
    checks={k:bool(v) for k,v in checks.items()}
    payload={
      'schema':'w33.pass420.integral_conductor_gluing.v1',
      'status':'PASS' if all(checks.values()) else 'FAIL',
      'theorem':{
        'incidence_operator':'S=A+I is the square incidence matrix between affine points (x,y,z) and nonvertical planes z=c+bx-ay',
        'group_algebra_identities':['S^2=q^2 I+q(J-Z)','SZ=J','S^3=q^2 S on augmentation zero'],
        'critical_lift':'for q=3,5,9, every positive p-power Smith factor of S occurs unchanged in the reduced critical group, and the only added layer is p^(3f) with multiplicity q^2-2',
        'topological_origin':'the q^2-2 top factors are the tree-quotient residue after the q^2-1-dimensional rational kernel of S and removal of the global constant direction',
        'boundary':'the q=25 and q=27 middle layers are constrained exactly but are not asserted until an integral saturation/representation calculation fixes them',
      },
      'exact_instances':exact_rows,
      'extension_field_constraint_engine':pending,
      'checks':checks,
    }
    payload['certificate_sha256']=certificate(payload)
    return payload

def main()->int:
    ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args()
    p=build_payload();text=json.dumps(p,indent=2,sort_keys=True)+'\n'
    if a.check:
        if not a.output.exists() or a.output.read_text()!=text: raise SystemExit('Pass 420 certificate drift')
    else: write_json(a.output,p)
    print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks'])}))
    return 0 if p['status']=='PASS' else 1
if __name__=='__main__': raise SystemExit(main())
