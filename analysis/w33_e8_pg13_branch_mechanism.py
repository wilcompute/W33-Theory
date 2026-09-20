#!/usr/bin/env python3
"""Representation-theoretic origin of the PG(1,3) E8 deficiency rule.

Under A8=sl9,
    e8 = sl9 + Lambda^3(9) + Lambda^6(9),
and the rho grading is exactly the branch label 0,1,2.

The four Lie-bracket mechanisms are:
  sl9 x sl9          -> sl9          (commutator)
  sl9 x Lambda^k     -> Lambda^k     (natural action)
  Lambda^3 x Lambda^3 -> Lambda^6    (wedge), and dual 6x6->3
  Lambda^3 x Lambda^6 -> sl9         (contraction), and reversed 6x3->sl9

Loading the exact 18x18 rank tensor proves:

* all 144 mixed sl9/exterior natural-action products are target-surjective;
* the sl9 commutator contributes exactly 4 deficient products:
    2 neutral-direction and 2 a-axis;
* the two wedge maps contribute exactly 16 deficient products, all on the two
  diagonal projective directions [1:1],[1:2]:
    12 deficiency-one + 4 deficiency-two;
* the two contraction maps contribute exactly 20 deficient products:
    4 on the rho-axis [1:0] and 16 on the diagonal lines, all deficiency-one.

Thus the four points of PG(1,3)
    [0:1], [1:0], [1:1], [1:2]
are not an empirical after-the-fact partition.  They distinguish which SU(9)
branch map can fail to span a charged target slice:
    a-axis       -> sl9 commutator,
    rho-axis     -> Lambda3/Lambda6 contraction,
    diagonals    -> wedge plus contraction.

The neutral five-dimensional defect remains the center u(1)^5 of the neutral
A2+A1+u(1)^5 algebra.
"""
from __future__ import annotations
import json
from collections import Counter,defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_e8_pg13_branch_mechanism.json'

def parse(s):return tuple(map(int,s.split(',')))

def direction(x,y):
    r,a,_=x;s,c,_=y
    if (r,a)==(0,0) and (s,c)==(0,0):return 'neutral'
    if r==s==0 and a and c and (a+c)%3==0:return '[0:1]_a_axis'
    if a==c==0 and r and s and (r+s)%3==0:return '[1:0]_rho_axis'
    if r and a and s and c and (r*c-a*s)%3==0:
        # the common line slope a/r = 1 or 2
        slope=(a*pow(r,-1,3))%3
        return f'[1:{slope}]_diagonal'
    return 'generic'

def mechanism(r,s):
    if r==0 and s==0:return 'commutator_sl9_sl9'
    if 0 in (r,s):return 'natural_sl9_action'
    if r==s:return 'wedge_exterior_same_branch'
    return 'contraction_L3_L6'

def main(write=True):
    p=json.loads((ROOT/'data/w33_e8_holonomy_bracket_rank_tensor.json').read_text())
    q=json.loads((ROOT/'data/w33_e8_bracket_deficiency_formula.json').read_text())
    assert p['status']=='PASS_COMPLETE_18x18_BRACKET_TENSOR'
    assert q['status']=='PASS_CLOSED_PROJECTIVE_DEFICIENCY_FORMULA'
    S=[parse(x) for x in p['sector_order']]

    mech=defaultdict(lambda:{'pairs':0,'deficient':0,'distribution':Counter(),'directions':Counter()})
    branch=defaultdict(lambda:{'pairs':0,'deficient':0,'distribution':Counter()})
    defective=[]
    for i,x in enumerate(S):
      for j,y in enumerate(S):
        d=int(p['deficiency_matrix'][i][j])
        m=mechanism(x[0],y[0])
        M=mech[m];M['pairs']+=1;M['distribution'][d]+=1
        B=branch[f'{x[0]}{y[0]}'];B['pairs']+=1;B['distribution'][d]+=1
        if d:
            M['deficient']+=1;M['directions'][direction(x,y)]+=1
            B['deficient']+=1
            defective.append((m,direction(x,y),d))

    assert mech['natural_sl9_action']['pairs']==144
    assert mech['natural_sl9_action']['deficient']==0

    assert mech['commutator_sl9_sl9']['pairs']==36
    assert mech['commutator_sl9_sl9']['deficient']==4
    assert mech['commutator_sl9_sl9']['directions']==Counter({'neutral':2,'[0:1]_a_axis':2})

    assert mech['wedge_exterior_same_branch']['pairs']==72
    assert mech['wedge_exterior_same_branch']['deficient']==16
    assert mech['wedge_exterior_same_branch']['distribution']==Counter({0:56,1:12,2:4})
    assert mech['wedge_exterior_same_branch']['directions']==Counter({'[1:1]_diagonal':8,'[1:2]_diagonal':8})

    assert mech['contraction_L3_L6']['pairs']==72
    assert mech['contraction_L3_L6']['deficient']==20
    assert mech['contraction_L3_L6']['distribution']==Counter({0:52,1:20})
    assert mech['contraction_L3_L6']['directions']==Counter({'[1:1]_diagonal':8,'[1:2]_diagonal':8,'[1:0]_rho_axis':4})

    assert len(defective)==40

    def freeze(D):
        return {k:{
          'pairs':v['pairs'],'deficient':v['deficient'],
          'distribution':{str(a):b for a,b in sorted(v['distribution'].items())},
          **({'directions':dict(sorted(v['directions'].items()))} if 'directions' in v else {})
        } for k,v in sorted(D.items())}

    out={
      'schema':'w33.e8_pg13_branch_mechanism.v1',
      'status':'PASS_PG13_BRANCH_MECHANISM',
      'headline':'The PG(1,3) bracket-deficiency law is the shadow of the A8 branching e8=sl9+Lambda3+Lambda6. All 144 mixed sl9/exterior natural-action products are surjective. The 40 defects split exactly into 4 sl9-commutator defects (neutral/a-axis), 16 exterior-wedge defects (the two diagonal projective lines), and 20 Lambda3/Lambda6 contraction defects (rho-axis plus diagonals).',
      'A8_branching':{
        'rho0':'sl9','rho1':'Lambda^3(9)','rho2':'Lambda^6(9)',
        'dimensions':'80+84+84=248'},
      'bracket_mechanisms':freeze(mech),
      'rho_branch_pair_census':freeze(branch),
      'projective_dictionary':{
        '[0:1]':'W3/a axis; only sl9 commutator defects',
        '[1:0]':'rho branch axis; only Lambda3-Lambda6 contraction defects',
        '[1:1]':'diagonal; wedge and contraction defects',
        '[1:2]':'diagonal; wedge and contraction defects'},
      'structural_explanation':'The rho coordinate is not interchangeable with the W3 charge coordinate: rho chooses the SU9 representation branch, while a grades weights inside each branch. That is why the two coordinate axes obey different parity rules even though the final arithmetic support is PG(1,3).',
      'neutral_center':'The unique deficiency-five neutral-neutral product is [A2+A1+u1^5,A2+A1+u1^5]=A2+A1; the missing five dimensions are the Abelian center.',
      'parents':['data/w33_e8_holonomy_bracket_rank_tensor.json','data/w33_e8_bracket_deficiency_formula.json'],
      'checks':{'natural_action_144_surjective':True,'commutator_defects4':True,
                'wedge_defects16':True,'contraction_defects20':True,
                'total_defects40':True,'PG13_dictionary_exact':True}}
    if write:OUT.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2));return out

if __name__=='__main__':main(True)
