#!/usr/bin/env python3
"""Pass5202: the q=5 P-footprint kernel is exactly the W-line incidence code.

Pass5201 defines the point/P-component incidence matrix F by F[p,C]=1 iff the
W-point p lies in the 2(q+1)-point K_{q+1,q+1} block of P component C.  It proves
that every W-line incidence vector lies in ker(F^T).

This producer reconstructs the P-component blocks independently from symplectic
polarity in PG(3,q): the P components are the unordered pairs {L,L^perp} of
non-isotropic projective lines.  Their unions have 2(q+1) points.  For q=3,5,7
we build all projective lines, classify isotropic/non-isotropic lines, pair the
non-isotropic lines under polarity, build F, and compute exact binary ranks.

The ranks are

  q=3: rank(F)=15, rank(W-line code)=25,
  q=5: rank(F)=65, rank(W-line code)=91,
  q=7: rank(F)=175, rank(W-line code)=225.

In each case rank(F)=q(q^2+1)/2 and the two ranks sum to
v=(q+1)(q^2+1).  Since the line code is already contained in ker(F^T), equality
follows objectwise in all three anchors.  In particular at q=5,

  ker(F^T)=LineCode(W(3,5);F2), dim=91.

Therefore the zero P-component-parity sector from Pass5201 has an exact gauge
normal form: its point-parity vector is a binary sum of W-line incidences and
can be killed by line-panel chamber-cut toggles.  This is an existence statement
for a gauge-equivalent representative; it does not claim the gauge move
preserves minimum chamber-leader cardinality.
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5202_P_FOOTPRINT_KERNEL_LINE_CODE.json'


def invmod(a,q): return pow(a,-1,q)

def canon(v,q):
    v=tuple(x%q for x in v)
    for x in v:
        if x:
            z=invmod(x,q)
            return tuple((z*y)%q for y in v)
    raise ValueError('zero vector')

def points(q):
    return sorted({canon(v,q) for v in itertools.product(range(q),repeat=4) if any(v)})

def symp(u,v,q):
    return (u[0]*v[2]-u[2]*v[0]+u[1]*v[3]-u[3]*v[1])%q

def span_line(u,v,q):
    return frozenset(canon(tuple((a*u[i]+b*v[i])%q for i in range(4)),q)
      for a,b in itertools.product(range(q),repeat=2) if a or b)

def projective_lines(P,q):
    D={}
    for u,v in itertools.combinations(P,2): D[span_line(u,v,q)]=None
    return list(D)

def basis(L,q):
    u=next(iter(L))
    for v in L:
        if v!=u and span_line(u,v,q)==L:return u,v
    raise AssertionError

def polar(L,P,q):
    u,v=basis(L,q)
    return frozenset(p for p in P if symp(p,u,q)==0 and symp(p,v,q)==0)

def gf2_rank(rows):
    piv={}
    for x in rows:
        while x:
            p=x.bit_length()-1
            if p in piv:x^=piv[p]
            else:piv[p]=x;break
    return len(piv)

def anchor(q):
    P=points(q);idx={p:i for i,p in enumerate(P)};L=projective_lines(P,q)
    iso=[];non=[]
    for ell in L:
        u,v=basis(ell,q)
        (iso if symp(u,v,q)==0 else non).append(ell)
    nonset=set(non);seen=set();pairs=[]
    for ell in non:
        if ell in seen:continue
        m=polar(ell,P,q)
        assert m in nonset and m!=ell and polar(m,P,q)==ell
        seen|={ell,m};pairs.append((ell,m))
    blocks=[a|b for a,b in pairs]
    assert {len(B) for B in blocks}=={2*(q+1)}

    Frows=[]
    for p in P:
        z=0
        for c,B in enumerate(blocks):
            if p in B:z|=1<<c
        Frows.append(z)
    assert {x.bit_count() for x in Frows}=={q*q}

    linerows=[]
    for ell in iso:
        z=0
        for p in ell:z|=1<<idx[p]
        linerows.append(z)
    assert {x.bit_count() for x in linerows}=={q+1}

    hist=Counter()
    for ell in iso:
        for B in blocks:
            t=len(ell&B);hist[t]+=1;assert t in (0,2)

    rf=gf2_rank(Frows);rl=gf2_rank(linerows);v=len(P)
    assert rf==q*(q*q+1)//2
    assert rl==(q+2)*(q*q+1)//2
    assert rf+rl==v
    return {'q':q,'PG_points':v,'PG_lines':len(L),'W_isotropic_lines':len(iso),
      'nonisotropic_lines':len(non),'polarity_pairs_P_components':len(pairs),
      'component_block_size':2*(q+1),'point_footprint_weight':q*q,
      'rank_F_over_F2':rf,'kernel_Ft_dimension':v-rf,
      'W_line_code_rank_over_F2':rl,'kernel_equals_line_code':True,
      'line_block_intersection_histogram':{str(k):x for k,x in sorted(hist.items())}}

def main():
    A={str(q):anchor(q) for q in (3,5,7)}
    out={'pass':5202,'status':'THEOREM_Q5_P_FOOTPRINT_KERNEL_EQUALS_W_LINE_CODE',
      'construction':'P components are reconstructed as polarity pairs {L,L^perp} of non-isotropic lines of PG(3,q); the component point block is L union L^perp.',
      'anchors':A,
      'q5_kernel':'For F in F2^{156 x 325}, rank(F)=65 and dim ker(F^T)=91. The 156 W-line incidence vectors span a 91-dimensional subspace of ker(F^T), so ker(F^T) is exactly the W(3,5) binary line incidence code.',
      'q5_gauge_normal_form':'By Pass5201, zero P-component parity means the point-parity vector a lies in ker(F^T). Hence a is a sum of W-line incidence vectors and can be removed by line-panel chamber-cut gauge toggles.',
      'cross_field_pattern':'The same exact rank complement and kernel equality are verified at q=3 and q=7: rank(F)=q(q^2+1)/2 and line-code rank=(q+2)(q^2+1)/2.',
      'boundary':'The q=3,5,7 statements are exhaustive finite computations from projective geometry. No all-odd-q binary-rank theorem is claimed from these anchors alone. The q5 gauge normal form need not preserve minimum chamber-leader weight. The minimum distance of im(F^T) and the zero-parity residual apartment sector remain open.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

if __name__=='__main__':main()
