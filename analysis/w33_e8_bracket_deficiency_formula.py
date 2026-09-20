#!/usr/bin/env python3
"""Closed arithmetic formula for the complete E8 bracket deficiency tensor.

Parent:
  data/w33_e8_holonomy_bracket_rank_tensor.json

Write x=(r,a,b), y=(s,c,d) in C3^2 x C2.  The exact deficiency
  delta(x,y) = dim g_{x+y} - rank [g_x,g_y]
is:

1. Neutral C3^2 direction:
   x_3=y_3=(0,0)
     b=d=0 -> delta=5
     b=d=1 -> delta=2
     otherwise 0.

2. a-axis (r=s=0, a,c nonzero and opposite):
     delta=1 iff b=d=0.

3. rho-axis (a=c=0, r,s nonzero and opposite):
     delta=1 iff b=d.

4. Diagonal projective directions
   r,a,s,c all nonzero and det((r,a),(s,c))=0:
     delta=2 iff (r,a)=(s,c) and b=d=0;
     otherwise delta=1.

5. All other ordered pairs have delta=0.

This reproduces all 324 entries exactly, replacing the previous 13-orbit
exception table by a projective-line/parity rule.

Geometrically the four projective directions of PG(1,3) split into two axes
and two diagonal lines.  The two diagonal lines carry the uniform deficient
fusion pattern; the two coordinate axes are distinguished because the rho and
W3 gradings are not interchangeable in the physical E8 decomposition.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_e8_bracket_deficiency_formula.json'

def parse(s): return tuple(map(int,s.split(',')))

def deficiency(x,y):
    r,a,b=x; s,c,d=y

    if (r,a)==(0,0) and (s,c)==(0,0):
        if b==d==0: return 5
        if b==d==1: return 2
        return 0

    if r==s==0 and a and c and (a+c)%3==0:
        return 1 if b==d==0 else 0

    if a==c==0 and r and s and (r+s)%3==0:
        return 1 if b==d else 0

    if r and a and s and c and (r*c-a*s)%3==0:
        if (r,a)==(s,c) and b==d==0:
            return 2
        return 1

    return 0

def main(write=True):
    p=json.loads((ROOT/'data/w33_e8_holonomy_bracket_rank_tensor.json').read_text())
    assert p['status']=='PASS_COMPLETE_18x18_BRACKET_TENSOR'
    S=[parse(x) for x in p['sector_order']]

    pred=[]
    mismatch=[]
    counts={0:0,1:0,2:0,5:0}
    support={'neutral':0,'a_axis':0,'rho_axis':0,'diagonal':0}
    for i,x in enumerate(S):
        row=[]
        for j,y in enumerate(S):
            d=deficiency(x,y)
            row.append(d)
            counts[d]=counts.get(d,0)+1
            if d:
                r,a,b=x; s,c,e=y
                if (r,a)==(0,0) and (s,c)==(0,0):
                    support['neutral']+=1
                elif r==s==0:
                    support['a_axis']+=1
                elif a==c==0:
                    support['rho_axis']+=1
                else:
                    support['diagonal']+=1
            actual=int(p['deficiency_matrix'][i][j])
            if d!=actual:
                mismatch.append({'left':p['sector_order'][i],
                                 'right':p['sector_order'][j],
                                 'predicted':d,'actual':actual})
        pred.append(row)

    assert not mismatch
    assert pred==p['deficiency_matrix']
    assert counts=={0:284,1:34,2:5,5:1}
    assert support=={'neutral':2,'a_axis':2,'rho_axis':4,'diagonal':32}

    out={
      'schema':'w33.e8_bracket_deficiency_formula.v1',
      'status':'PASS_CLOSED_PROJECTIVE_DEFICIENCY_FORMULA',
      'headline':'The full 18x18 E8 bracket deficiency tensor has a closed PG(1,3)-plus-parity formula. All 324 entries are reproduced without the 13-record exception table: deficiencies occur only on the neutral direction, the two coordinate axes with distinct parity restrictions, and the two diagonal projective lines.',
      'formula':{
        'neutral':'(r,a)=(s,c)=(0,0): delta=5 for b=d=0; delta=2 for b=d=1; else 0',
        'a_axis':'r=s=0, a,c nonzero opposite: delta=1 iff b=d=0',
        'rho_axis':'a=c=0, r,s nonzero opposite: delta=1 iff b=d',
        'diagonal':'all C3 coordinates nonzero and r*c-a*s=0 mod3: delta=2 for identical C3 vector with b=d=0, otherwise delta=1',
        'else':'delta=0'},
      'projective_geometry':{
        'space':'PG(1,3)','directions':4,
        'coordinate_axes':2,'diagonal_lines':2,
        'deficient_support_counts':support},
      'deficiency_distribution':{str(k):v for k,v in counts.items()},
      'replay':{'ordered_pairs':324,'mismatches':0,'exact':True},
      'compression':{
        'old':'18 target dimensions + 13 exception records',
        'new':'18 target dimensions + fixed arithmetic branch rule',
        'lookup_table_entries_for_deficiency':0},
      'physical_reading':'The small fusion defects are controlled by the relative projective direction of the two C3 grading vectors and by theta3 parity. The five-dimensional neutral defect is exactly the central u(1)^5 already identified independently.',
      'boundary':'Exact arithmetic description of bracket ranks only. It does not determine structure constants or amplitudes.',
      'parent':'data/w33_e8_holonomy_bracket_rank_tensor.json',
      'checks':{'all324_exact':True,'distribution_284_34_5_1':True,
                'support_2_2_4_32':True,'no_exception_table_needed':True}}
    if write: OUT.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
    return out

if __name__=='__main__':
    main(True)
