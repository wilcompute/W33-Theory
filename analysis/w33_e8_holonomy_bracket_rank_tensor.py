#!/usr/bin/env python3
"""Complete 18x18 E8 holonomy-sector bracket-rank tensor.

The commuting gradings rho (C3), W3 (C3), theta3 (C2) give
K=C3 x C3 x C2 and an 18-sector decomposition of E8.

This file builds all 240 E8 roots in the regular A8 model, adds the 8D Cartan
to the neutral sector, and computes for every ordered pair (chi,psi):
  * the target sector chi+psi,
  * whether the Lie bracket is nonzero,
  * the exact rank of the span [g_chi,g_psi] inside g_{chi+psi}.

Root-root brackets contribute e_{alpha+beta} when alpha+beta is a root and
H_alpha when beta=-alpha.  Neutral Cartan-root brackets contribute each root
space in the nonneutral factor.

Exact result:
  324/324 ordered products are nonzero;
  284 are target-surjective;
  deficiencies are 34x1, 5x2, 1x5.
The unique deficiency-five product is neutral-neutral:
  [A2+A1+u1^5,A2+A1+u1^5]=A2+A1,
so the five missing dimensions are exactly the central u(1)^5.

The full rank tensor is invariant under independent inversion of the two C3
coordinates, a C2 x C2 subgroup of Aut(C3^2); the 40 deficient ordered products
form 13 orbits under that exact symmetry.

This also sharpens the packet18 firewall: E8 sectors have canonical character
addition/fusion, whereas packet18=G/C4 is only a homogeneous space because C4
is nonnormal.  No multiplication-preserving identification can exist.
"""
from __future__ import annotations
import itertools,json
from collections import Counter,defaultdict
from fractions import Fraction as F
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_e8_holonomy_bracket_rank_tensor.json'
JOINT=[((0,0),3),((0,1),2),((1,0),1),((1,1),1),((2,0),1),((2,1),1)]
ZERO=(0,0,0)

def rank(rows):
    A=[list(map(F,r)) for r in rows if any(r)]
    if not A:return 0
    m,n=len(A),len(A[0]);rr=0
    for c in range(n):
        p=next((i for i in range(rr,m) if A[i][c]),None)
        if p is None:continue
        A[rr],A[p]=A[p],A[rr]
        z=A[rr][c];A[rr]=[x/z for x in A[rr]]
        for i in range(m):
            if i!=rr and A[i][c]:
                z=A[i][c];A[i]=[A[i][j]-z*A[rr][j] for j in range(n)]
        rr+=1
    return rr

def addc(x,y):return ((x[0]+y[0])%3,(x[1]+y[1])%3,(x[2]+y[2])%2)
def key(k):return '%d,%d,%d'%k

def build():
    chars=[]
    for ch,n in JOINT:chars += [ch]*n
    roots=[];labs=[]
    for i in range(9):
        for j in range(9):
            if i==j:continue
            v=[F(0)]*9;v[i]=1;v[j]=-1
            roots.append(tuple(v))
            labs.append((0,(chars[i][0]-chars[j][0])%3,(chars[i][1]-chars[j][1])%2))
    for S in itertools.combinations(range(9),3):
        v=[F(-1,3)]*9
        for i in S:v[i]+=1
        a=sum(chars[i][0] for i in S)%3
        b=sum(chars[i][1] for i in S)%2
        roots.append(tuple(v));labs.append((1,a,b))
        roots.append(tuple(-x for x in v));labs.append((2,(-a)%3,(-b)%2))
    assert len(roots)==len(set(roots))==240
    return roots,labs

def main(write=True):
    roots,labs=build();ridx={r:i for i,r in enumerate(roots)}
    keys=[(r,a,b) for r in range(3) for a in range(3) for b in range(2)]
    sec=defaultdict(list)
    for i,c in enumerate(labs):sec[c].append(i)
    dims={c:len(sec[c])+(8 if c==ZERO else 0) for c in keys}
    assert sum(dims.values())==248

    rows=[];rank_matrix=[];def_matrix=[];deficient=[]
    by_def=Counter()
    for x in keys:
        rr=[];dd=[]
        for y in keys:
            z=addc(x,y);outroots=set();cart=[]
            if x==ZERO:outroots.update(sec[y])
            if y==ZERO:outroots.update(sec[x])
            for i in sec[x]:
                a=roots[i]
                for j in sec[y]:
                    b=roots[j]
                    s=tuple(a[t]+b[t] for t in range(9))
                    if not any(s):
                        cart.append(a)
                    elif s in ridx:
                        outroots.add(ridx[s])
            cr=rank(cart)
            br=len(outroots)+cr
            deficiency=dims[z]-br
            assert br>0
            rec={'left':key(x),'right':key(y),'target':key(z),'rank':br,
                 'target_dim':dims[z],'deficiency':deficiency,
                 'root_output_rank':len(outroots),'cartan_output_rank':cr}
            rows.append(rec);rr.append(br);dd.append(deficiency);by_def[deficiency]+=1
            if deficiency:deficient.append(rec)
        rank_matrix.append(rr);def_matrix.append(dd)

    assert len(rows)==324 and len(deficient)==40
    assert by_def==Counter({0:284,1:34,2:5,5:1})
    nn=next(r for r in rows if r['left']==r['right']==key(ZERO))
    assert nn['rank']==11 and nn['target_dim']==16 and nn['deficiency']==5
    assert nn['root_output_rank']==8 and nn['cartan_output_rank']==3

    # Exact grading symmetries preserving dimensions and the whole rank tensor:
    # independent inversion rho->-rho and a->-a.
    mats=[(1,0,0,1),(1,0,0,2),(2,0,0,1),(2,0,0,2)]
    lookup={(r['left'],r['right']):r for r in rows}
    def ap(M,c):
        r,a,b=map(int,c.split(','))
        return ((M[0]*r+M[1]*a)%3,(M[2]*r+M[3]*a)%3,b)
    def ks(c):return key(c)
    for M in mats:
        assert all(dims[ap(M,c)]==dims[c] for c in keys)
        for rec in rows:
            X=ks(ap(M,tuple(map(int,rec['left'].split(',')))))
            Y=ks(ap(M,tuple(map(int,rec['right'].split(',')))))
            assert lookup[(X,Y)]['rank']==rec['rank']

    def orbit(rec):
        x=tuple(map(int,rec['left'].split(',')));y=tuple(map(int,rec['right'].split(',')))
        return frozenset((ks(ap(M,x)),ks(ap(M,y))) for M in mats)
    seen=set();orbits=[]
    for rec in deficient:
        p=(rec['left'],rec['right'])
        if p in seen:continue
        O=orbit(rec);seen|=O
        rep=min(O)
        r=lookup[rep]
        orbits.append({'size':len(O),'deficiency':r['deficiency'],
                       'representative':{'left':rep[0],'right':rep[1],
                                         'target':r['target'],'rank':r['rank'],
                                         'target_dim':r['target_dim']}})
    orbits.sort(key=lambda o:(o['deficiency'],o['size'],o['representative']['left'],o['representative']['right']))
    assert len(orbits)==13 and sum(o['size'] for o in orbits)==40

    packet=json.loads((ROOT/'data/w33_e8_holonomy_packet18_homogeneous_bridge.json').read_text())
    assert packet['status']=='PASS_TORSOR_BRIDGE__GROUP_IDENTIFICATION_KILLED'
    assert packet['positive_bridge']['C4_normal'] is False

    out={
      'schema':'w33.e8_holonomy_bracket_rank_tensor.v1',
      'status':'PASS_COMPLETE_18x18_BRACKET_TENSOR',
      'headline':'All 324 ordered products of the 18 C3xC3xC2 E8 holonomy sectors have nonzero Lie bracket. 284 products span their entire target sector; the exact deficiencies are 34 of one dimension, 5 of two dimensions, and one of five dimensions. The unique deficiency-five product is neutral-neutral and misses exactly the central u(1)^5. The 40 deficient products collapse to 13 orbits under independent inversion of the two C3 grading coordinates.',
      'sector_order':[key(c) for c in keys],
      'sector_dimensions':{key(c):dims[c] for c in keys},
      'rank_matrix':rank_matrix,'deficiency_matrix':def_matrix,
      'summary':{
        'ordered_products':324,'nonzero_products':324,'surjective_products':284,
        'deficient_products':40,'deficiency_distribution':{str(k):v for k,v in sorted(by_def.items())},
        'neutral_neutral':nn},
      'rank_tensor_symmetry':{
        'group':'C2 x C2','action':'independent inversion of rho and W3 C3 coordinates',
        'matrices_mod3':[list(M) for M in mats],'deficient_orbits':orbits,'orbit_count':13},
      'packet18_firewall':'The E8 sector set is a character group with canonical addition and everywhere-nonzero graded Lie fusion. packet18=G/C4 has no well-defined coset multiplication because C4 is nonnormal. Therefore the existing two-sheet F3^2 torsor bridge cannot be upgraded to a fusion-algebra/group identification.',
      'checks':{
        'roots240':True,'sector_sum248':True,'products324':True,'all_brackets_nonzero':True,
        'surjective284':True,'deficiency_34_5_1':True,'neutral_missing_u1_5':True,
        'tensor_C2xC2_symmetry':True,'deficient_orbits13':True}}
    if write:OUT.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
    return out
if __name__=='__main__':main(True)
