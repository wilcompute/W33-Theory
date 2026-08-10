#!/usr/bin/env python3
"""Pass 4766 -- the 45 support-12 rook grids define a [40,24,6] code whose minimum shell is the W33 point-edge carrier.

Let T be the 45x40 grid-line incidence from Pass4763 and C=row_2(T).  Rather than
enumerating 2^24 words, enumerate the 2^16-word dual and recover C by exact
MacWilliams transform.

The key geometric identification is exact.  If B is the 40x40 point-line incidence
matrix and p~q is a W33 point edge, then the symmetric difference of the two point
stars has weight 6.  The 240 such words are exactly C's 240 minimum words.

Moreover

  C = B^T(Even(F2^40_points)),
  C^perp = { y on lines : B y is constant }.

The 252 dual minimum words split into 216 kernel words (point degrees 0^20 2^20)
and exactly 36 spreads (point degrees 1^40).
"""
from __future__ import annotations
import itertools,json,math
from collections import Counter,defaultdict
from pathlib import Path
import numpy as np
from w33_pass4495_4502_distance_prism_reconstruction import geometry
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4766_GRID_CODE_POINT_EDGE_BRIDGE.json'

def basis(rows):
    piv={};out=[]
    for x in rows:
        y=int(x)
        while y:
            p=y.bit_length()-1
            if p in piv:y^=piv[p]
            else:piv[p]=y;out.append(int(x));break
    return out

def rank(rows):return len(basis(rows))
def contains(B,x):return rank(B+[int(x)])==len(B)
def nullspace(rows,n):
    # Reduced echelon equations with highest-bit pivots.
    piv={}
    for x in rows:
        y=int(x)
        while y:
            p=y.bit_length()-1
            if p in piv:y^=piv[p]
            else:
                for q,z in list(piv.items()):
                    if (z>>p)&1:piv[q]=z^y
                piv[p]=y;break
    free=[j for j in range(n) if j not in piv];out=[]
    for f in free:
        x=1<<f
        for p in sorted(piv):
            if ((piv[p]&x).bit_count()&1):x|=1<<p
        out.append(x)
    assert all(all(((r&x).bit_count()&1)==0 for r in rows) for x in out)
    return out

def enum(B):
    out=[0]
    for b in B:out += [x^b for x in out]
    return out

def kraw(n,w,j):
    return sum((-1)**i*math.comb(j,i)*math.comb(n-j,w-i) for i in range(max(0,w-(n-j)),min(w,j)+1))
def macwilliams(dual_hist,n,dual_size):
    A={}
    for w in range(n+1):
        z=sum(c*kraw(n,w,j) for j,c in dual_hist.items())
        assert z%dual_size==0;z//=dual_size
        if z:A[w]=z
    return A

def main()->int:
    pts,pidx,lines,A,apartments,_,_=geometry();A=np.asarray(A,dtype=np.uint8)
    through=[set() for _ in range(40)]
    for li,L in enumerate(lines):
        for p in L:through[p].add(li)
    # support-12 thickenings and unique partner grids
    edges=[(i,j) for i,j in itertools.combinations(range(40),2) if A[i,j]];eidx={e:k for k,e in enumerate(edges)}
    th=[];em=[]
    for ap in apartments:
        corners=set()
        for i,j in itertools.combinations(ap,2):
            z=lines[i]&lines[j]
            if z:corners|=set(z)
        U=set()
        for p in corners:U|=through[p]
        U=frozenset(U);th.append(U);m=0
        for i,j in itertools.combinations(sorted(U),2):
            if A[i,j]:m|=1<<eidx[(i,j)]
        em.append(m)
    partner=[None]*1620
    for i in range(1620):
        for j in range(i+1,1620):
            if (em[i]&em[j]).bit_count()==8:partner[i]=j;partner[j]=i
    grids=sorted({frozenset(th[i]|th[partner[i]]) for i in range(1620)},key=lambda U:tuple(sorted(U)));assert len(grids)==45
    tm=[sum(1<<x for x in U) for U in grids];C=basis(tm);assert len(C)==24
    D=nullspace(C,40);assert len(D)==16

    # Point-line incidence B and exact algebraic description.
    star=[sum(1<<l for l in through[p]) for p in range(40)]
    assert rank(star)==25
    point_edges=[]
    for p,q in itertools.combinations(range(40),2):
        if through[p]&through[q]:point_edges.append((p,q))
    assert len(point_edges)==240
    edge_words={star[p]^star[q] for p,q in point_edges};assert len(edge_words)==240 and {x.bit_count() for x in edge_words}=={6}
    assert all(contains(C,x) for x in edge_words)
    # Connected point graph: edge differences span B^T of the even coefficient hyperplane.
    assert rank(list(edge_words))==24

    def Bimage(y):
        z=0
        for p in range(40):
            if ((star[p]&y).bit_count()&1):z|=1<<p
        return z
    allp=(1<<40)-1
    assert all(Bimage(y) in (0,allp) for y in D)
    # Enumerate only the 2^16 dual; MacWilliams supplies the 2^24 primal spectrum.
    words=enum(D);assert len(words)==65536
    dh=Counter(x.bit_count() for x in words)
    expected_d={0:1,10:252,12:310,14:2700,16:7695,18:15480,20:12660,22:15480,24:7695,26:2700,28:310,30:252,40:1}
    assert dict(sorted(dh.items()))==expected_d
    ph=macwilliams(dh,40,len(words))
    expected_p={0:1,6:240,8:1485,10:27792,12:169600,14:707760,16:1909170,18:3491280,20:4162560,22:3491280,24:1909170,26:707760,28:169600,30:27792,32:1485,34:240,40:1}
    assert ph==expected_p and ph[6]==len(edge_words)

    min10=[x for x in words if x.bit_count()==10];assert len(min10)==252
    shells=Counter()
    for y in min10:
        deg=[]
        for p in range(40):deg.append(sum(1 for l in through[p] if (y>>l)&1))
        shells[tuple(sorted(Counter(deg).items()))]+=1
    assert shells==Counter({((0,20),(2,20)):216,((1,40),):36})
    spreads=[y for y in min10 if Bimage(y)==allp];assert len(spreads)==36

    out={'pass':4766,'grid_code':{'parameters':'[40,24,6]_2','weight_enumerator':{str(k):v for k,v in ph.items()}},
      'dual':{'parameters':'[40,16,10]_2','description':'{y : B y in <1_points>}','weight_enumerator':{str(k):v for k,v in sorted(dh.items())},
        'minimum_shell':{'total':252,'kernel_degree_0_2_words':216,'spreads':36}},
      'point_edge_bridge':{'point_edges':240,'star_difference_weight':6,'distinct_star_differences':240,'equals_complete_grid_code_minimum_shell':True,
        'formula':'w_{pq}=Star(p) XOR Star(q) for p~q'},
      'algebraic_description':{'C':'B^T(Even point coefficients)','rank_B':25,'rank_C':24,'dual_condition':'B y is either 0 or all-ones'},
      'theorem':'The 45 support-12 rook grids generate a [40,24,6]_2 code whose 240 minimum words are exactly the symmetric differences of point stars along the 240 W33 point edges. Its [40,16,10]_2 dual has 36 spreads and 216 kernel minimum words.',
      'boundary':'This is a code-mediated recovery of the point-edge G-set from line coordinates; it does not contradict Pass4765, which excludes a coordinate-level PSp bijection between point edges and line edges.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
