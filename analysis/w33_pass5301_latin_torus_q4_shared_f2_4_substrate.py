#!/usr/bin/env python3
"""Pass5301: exact 16-cell F2^4 bridge among the Klein Latin chart, toroidal knight Q4, and Hoffman quotient.

The bridge is substrate-level, not an equality of graphs.  Label the 4x4 cells by
(r,c) in F2^2 x F2^2 = F2^4.  The Klein Latin square L(r,c)=r+c has the standard
affine-plane spread of the 15 nonzero translation directions into five PG(3,2)
lines: row, column, symbol, and two further direction lines corresponding to the
two additional orthogonal mates completing three MOLS(4).

The even-parastrophe affine group from Pass5300 has two direction orbits of sizes
9 and 6.  They are exactly the union of the first three spread lines and the last
two spread lines.  The repo's toroidal-knight graph is Q4 on the SAME 16 points,
but Q4 uses only the four basis directions {1,2,4,8}: two directions from the row
line and two from the column line.  The order-288 Hoffman/Latin-even quotient does
not preserve this four-direction set, hence it does not preserve Q4 edges.
"""
from __future__ import annotations
import itertools,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5301_LATIN_TORUS_Q4_F2_4_SUBSTRATE.json'

def rank(cols):
    piv={}
    for x in cols:
        while x:
            p=x.bit_length()-1
            if p in piv:x^=piv[p]
            else:piv[p]=x;break
    return len(piv)

def apply(A,x):
    y=0
    for i,e in enumerate((1,2,4,8)):
        if x&e:y^=A[i]
    return y

def latin_even_linear_group():
    S4=list(itertools.permutations(range(4)));S3=list(itertools.permutations(range(3)))
    def parity(p):return sum(p[i]>p[j] for i in range(len(p)) for j in range(i+1,len(p)))&1
    mats=set()
    for pi in S3:
        if parity(pi):continue
        for a in S4:
            for b in S4:
                mp={};cell=[0]*16;ok=True
                for r in range(4):
                    for c in range(4):
                        old=(r,c,r^c);R=a[old[pi[0]]];C=b[old[pi[1]]];t=old[pi[2]];s=R^C
                        if t in mp and mp[t]!=s:ok=False;break
                        mp[t]=s;cell[4*r+c]=4*R+C
                    if not ok:break
                if ok and len(mp)==4:
                    tr=cell[0];A=tuple(cell[e]^tr for e in (1,2,4,8))
                    assert rank(A)==4 and all(cell[x]==(apply(A,x)^tr) for x in range(16))
                    mats.add(A)
    assert len(mats)==18
    return mats

def orbit(mats,s):
    O={s};Q=[s]
    while Q:
        x=Q.pop()
        for A in mats:
            y=apply(A,x)
            if y not in O:O.add(y);Q.append(y)
    return O

def main():
    spread=[{1,2,3},{4,8,12},{5,10,15},{6,11,13},{7,9,14}]
    assert set().union(*spread)==set(range(1,16))
    assert sum(map(len,spread))==15 and all(len(L)==3 for L in spread)
    assert all((lambda a,b,c:a^b==c)(*sorted(L)) for L in spread)
    mats=latin_even_linear_group();rem=set(range(1,16));orbs=[]
    while rem:
        O=orbit(mats,next(iter(rem)));orbs.append(O);rem-=O
    assert sorted(map(len,orbs))==[6,9]
    O9=next(O for O in orbs if len(O)==9);O6=next(O for O in orbs if len(O)==6)
    assert O9==set().union(*spread[:3]) and O6==set().union(*spread[3:])
    q4={1,2,4,8}
    assert len(q4&spread[0])==2 and len(q4&spread[1])==2
    assert all(not(q4&L) for L in spread[2:])
    counter=next(A for A in mats if {apply(A,d) for d in q4}!=q4)
    image={apply(counter,d) for d in q4}
    assert image!=q4
    # Q4 has 16 translations times S4 permutations of its four basis directions.
    q4_aut=16*24
    assert 288%q4_aut!=0
    out={'pass':5301,'status':'THEOREM_LATIN_TOROIDAL_Q4_HOFFMAN_SHARE_F2_4_SUBSTRATE_BUT_NOT_EDGE_GEOMETRY',
      'vertices':16,'substrate':'F2^2 x F2^2 = F2^4',
      'latin_affine_spread':{
        'row':[1,2,3],'column':[4,8,12],'symbol':[5,10,15],
        'orthogonal_mate_1':[6,11,13],'orthogonal_mate_2':[7,9,14]},
      'interpretation':'The five PG(3,2) direction lines are the five parallel-class directions of the affine plane of order4; row+column plus three Latin-square symbol classes give a complete set of three MOLS(4).',
      'hoffman_latin_even_direction_orbits':[9,6],
      'orbit_identification':'9 = row+column+symbol direction lines; 6 = the two additional orthogonal-mate direction lines.',
      'toroidal_knight_Q4':{'direction_set':[1,2,4,8],'automorphism_order':q4_aut,
        'spread_intersection':'two basis directions from the row line and two from the column line'},
      'not_same_graph':{'linear_counterexample_columns':list(counter),'image_of_Q4_directions':sorted(image),
        'reason':'The order288 Hoffman/Latin-even affine quotient does not preserve the four Q4 directions; 288 also does not divide |Aut(Q4)|=384.'},
      'boundary':'Exact finite affine/code bridge. The toroidal knight Q4 and Hoffman/Latin symmetry use the same 16 points but different edge/incidence structures; no physical identification is asserted.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
