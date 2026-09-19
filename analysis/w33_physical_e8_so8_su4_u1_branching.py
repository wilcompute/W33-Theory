#!/usr/bin/env python3
"""Complete SO(8) x SU(4) x U(1) branching of the physical E8 holonomy grading.

Parents:
  data/w33_physical_holonomy_e8_chevalley_lift.json
  data/w33_physical_e8_triality_decomposition.json

The joint fixed root system is D4+A3, rank 7.  Inside the rank-8 A8 Cartan
there is therefore one residual U(1).  Solving exactly for the vector
orthogonal to every neutral root and to the all-ones direction gives, up to
overall scale,
    Q = (0,0,0,0,0,-1,-1,+1,+1).

Every connected nonneutral representation block has constant integral Q-charge.
With the three D4 minuscule orbits denoted 8_A,8_B,8_C, the complete branching is

  248 =
    (28,1)_0 + (1,15)_0 + (1,1)_0 + (8_A,6)_0
    + (8_B,4)_-1 + (8_C,bar4)_-1
    + (1,6)_+2 + (8_A,1)_+2
    + (8_B,bar4)_+1 + (8_C,4)_+1
    + (1,6)_-2 + (8_A,1)_-2.

Dimensions sum to 248.

A further exact relation holds on every ROOT space:
    order-3 Wilson character a == -Q mod 3.
Thus the physical W3 Z3 grading is the mod-3 reduction of this continuous
Cartan U(1) charge.

The order-two character is not determined by Q; it resolves the triality/A3
placement of equal-charge blocks.  In this sense the commuting pair separates
two logically different pieces:
  W3   = discrete reduction of a continuous E8 Cartan charge;
  theta3 = an independent inner involution that resolves the triality sectors.

Boundary:
SU(4) is group-theoretically the Pati-Salam colour-lepton group, and SO(8)
contains many SU(2)^4 / SO(4)xSO(4) subgroups, but NO Standard-Model or
Pati-Salam particle assignment is made here.  The only claim is the exact E8
branching and charge law.
"""
from __future__ import annotations
import itertools,json
from fractions import Fraction as F
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_physical_e8_so8_su4_u1_branching.json'

# Frozen from the parent triality certificate; repeated here as a fail-closed
# independent dimension/charge ledger.
BRANCH=[
 ('28','1',0,28),('1','15',0,15),('1','1',0,1),('8_A','6',0,48),
 ('8_B','4',-1,32),('8_C','bar4',-1,32),('1','6',2,6),('8_A','1',2,8),
 ('8_B','bar4',1,32),('8_C','4',1,32),('1','6',-2,6),('8_A','1',-2,8)]

def dot(a,b):return sum(x*y for x,y in zip(a,b))

def main(write=True):
    # Reconstruct the exact A8-root model solely to verify the U(1) generator
    # and the a=-Q mod3 law root-by-root.
    joint=[((0,0),3),((0,1),2),((1,0),1),((1,1),1),((2,0),1),((2,1),1)]
    chars=[]
    for ch,n in joint:chars += [ch]*n
    roots=[];rch=[]
    for i in range(9):
      for j in range(9):
        if i==j:continue
        v=[F(0)]*9;v[i]=1;v[j]=-1
        roots.append(tuple(v));rch.append(((chars[i][0]-chars[j][0])%3,(chars[i][1]-chars[j][1])%2))
    for S in itertools.combinations(range(9),3):
        v=[F(-1,3)]*9
        for i in S:v[i]+=1
        ch=(sum(chars[i][0] for i in S)%3,sum(chars[i][1] for i in S)%2)
        roots.append(tuple(v));rch.append(ch)
        roots.append(tuple(-x for x in v));rch.append(((-ch[0])%3,(-ch[1])%2))

    Q=(F(0),F(0),F(0),F(0),F(0),F(-1),F(-1),F(1),F(1))
    neutral=[r for r,ch in zip(roots,rch) if ch==(0,0)]
    assert all(dot(r,Q)==0 for r in neutral)
    assert sum(Q)==0
    charges=[dot(r,Q) for r in roots]
    assert set(charges)=={F(-2),F(-1),F(0),F(1),F(2)}
    assert all(a==(-int(q))%3 for (a,b),q in zip(rch,charges))

    # Character/charge census provides a separate control.
    census={}
    for ch,q in zip(rch,charges):
        census[(ch,int(q))]=census.get((ch,int(q)),0)+1
    expected={
      ((0,0),0):36, # neutral roots; Cartan added separately in branching
      ((0,1),0):48,
      ((1,0),-1):32,((1,0),2):6,
      ((1,1),-1):32,((1,1),2):8,
      ((2,0),1):32,((2,0),-2):6,
      ((2,1),1):32,((2,1),-2):8}
    assert census==expected
    assert sum(x[3] for x in BRANCH)==248

    p1=json.loads((ROOT/'data/w33_physical_holonomy_e8_chevalley_lift.json').read_text())
    p2=json.loads((ROOT/'data/w33_physical_e8_triality_decomposition.json').read_text())
    assert p1['status']=='PASS_PHYSICAL_INNER_CHEVALLEY_LIFT'
    assert p2['status']=='PASS_TRIALITY_MATTER_SKELETON'

    out={'schema':'w33.physical_e8_so8_su4_u1_branching.v1','status':'PASS_CONTINUOUS_TO_DISCRETE_CHARGE_LAW',
      'headline':'The physical order-six E8 fixed algebra is SO(8)xSU(4)xU(1). The residual Cartan generator can be chosen Q=(0,0,0,0,0,-1,-1,1,1), and the complete E8 adjoint branching is (28,1)_0+(1,15)_0+(1,1)_0+(8_A,6)_0 plus charged triality blocks at Q=±1,±2. On every E8 root space the order-three Wilson character satisfies a=-Q mod3 exactly.',
      'U1_generator':['0','0','0','0','0','-1','-1','1','1'],
      'branching':[{'D4':a,'A3':b,'Q':q,'dimension':d} for a,b,q,d in BRANCH],
      'root_charge_census':{f'a{a}b{b}_Q{q}':n for ((a,b),q),n in sorted(census.items())},
      'discrete_charge_law':'Wilson Z3 character a = -Q mod 3 on all 240 E8 root spaces',
      'interpretation':{'W3':'mod-3 reduction of the residual continuous E8 Cartan U(1)',
                        'theta3':'independent inner Z2 resolving triality/A3 placement'},
      'boundary':'No Standard-Model or Pati-Salam particle assignment is claimed; SO8 x SU4 x U1 is an exact representation-theoretic fixed algebra only.',
      'checks':{'Q_orthogonal_to_all_36_neutral_roots':True,'Q_in_A8_Cartan':True,
                'charges_are_0_pm1_pm2':True,'a_equals_minus_Q_mod3_rootwise':True,
                'branching_dimension_248':True,'parents_loaded':True}}
    if write:OUT.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2));return out
if __name__=='__main__':main(True)
