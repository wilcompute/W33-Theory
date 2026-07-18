#!/usr/bin/env python3
"""Pass 443: exact section-sensitive spectrum and critical-group classification at q=3."""
from __future__ import annotations
import argparse,itertools,json
from collections import Counter
from pathlib import Path
import sympy as sp
from sympy.matrices.normalforms import smith_normal_form
from sympy.polys.domains import ZZ

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass443_section_sensitive_smith_classification.json'
ELEMS=[(a,b,c) for a in range(3) for b in range(3) for c in range(3)]
EIDX={e:i for i,e in enumerate(ELEMS)}
PAIRS=[((0,1),(0,2)),((1,0),(2,0)),((1,1),(2,2)),((1,2),(2,1))]

def hmul(g,h):return ((g[0]+h[0])%3,(g[1]+h[1])%3,(g[2]+h[2]-g[0]*h[1]+h[0]*g[1])%3)
def hinv(g):return ((-g[0])%3,(-g[1])%3,(-g[2])%3)

def graph(offsets):
    S=[]
    for (v,nv),c in zip(PAIRS,offsets):S.extend([(v[0],v[1],c),(nv[0],nv[1],(-c)%3)])
    A=[[0]*27 for _ in range(27)]
    for i,g in enumerate(ELEMS):
        for s in S:A[i][EIDX[hmul(g,s)]]=1
    return sp.Matrix(A)

def curl(offsets):
    c0,c1,c2,c3=offsets
    return ((c2-c0-c1)%3,(c3-2*c0-c1)%3)

def word(gt,g,h):
    a,b,c=gt;k=(c+a*b)%3;z=hmul(hmul(g,h),hmul(hinv(g),hinv(h)));r=(0,0,0)
    for _ in range(a):r=hmul(r,g)
    for _ in range(b):r=hmul(r,h)
    for _ in range(k):r=hmul(r,z)
    return r

def automorphisms():
    noncentral=[g for g in ELEMS if g[:2]!=(0,0)];out=[]
    for g in noncentral:
        span=set()
        for a in range(3):
            for c in range(3):
                e=(0,0,0)
                for _ in range(a):e=hmul(e,g)
                for _ in range(c):e=hmul(e,(0,0,1))
                span.add(e)
        for h in noncentral:
            if h not in span:out.append((g,h))
    return out

def act(gh,offs):
    g,h=gh;S=[]
    for (v,nv),c in zip(PAIRS,offs):S.extend([(v[0],v[1],c),(nv[0],nv[1],(-c)%3)])
    S2={word(s,g,h) for s in S};out=[]
    for v,_ in PAIRS:
        hits=[s for s in S2 if s[:2]==v]
        if len(hits)!=1:return None
        out.append(hits[0][2])
    return tuple(out)

def orbit(seed,auts):
    seen={seed};front=[seed]
    while front:
        nxt=[]
        for x in front:
            for a in auts:
                y=act(a,x)
                if y is not None and y not in seen:seen.add(y);nxt.append(y)
        front=nxt
    return seen

def snf_factors(A):
    L=sp.diag(*[sum(A[i,j] for j in range(27)) for i in range(27)])-A
    D=smith_normal_form(L[:-1,:-1],domain=ZZ)
    return Counter(abs(int(D[i,i])) for i in range(26) if D[i,i] not in (0,1,-1))

def tree_order(factors):
    out=1
    for x,n in factors.items():out*=x**n
    return out

def classify(rep):
    x=sp.symbols('x');A=graph(rep);char=sp.factor(A.charpoly(x).as_expr());fac=snf_factors(A)
    return {'representative':rep,'curl':curl(rep),'adjacency_characteristic_polynomial':str(char),
      'critical_group_factors':{str(k):v for k,v in sorted(fac.items())},'spanning_tree_order':tree_order(fac)}

def build_payload():
    sections=list(itertools.product(range(3),repeat=4));flat=[s for s in sections if curl(s)==(0,0)];curved=[s for s in sections if curl(s)!=(0,0)]
    auts=automorphisms();O0=orbit((0,0,0,0),auts);Ob=orbit(curved[0],auts)
    F=classify((0,0,0,0));B=classify(curved[0]);x=sp.symbols('x')
    expectedF=sp.factor((x-8)*(x-2)**12*(x+1)**8*(x+4)**6)
    expectedB=sp.factor((x-8)*(x+1)**14*(x*x-x-11)**6)
    checks={'nine_flat_sections':len(flat)==9,'seventy_two_curved_sections':len(curved)==72,
      'curl_is_complete_orbit_invariant':O0==set(flat) and Ob==set(curved) and len(auts)==432,
      'flat_characteristic_polynomial':sp.expand(sp.sympify(F['adjacency_characteristic_polynomial']))==sp.expand(expectedF),
      'curved_characteristic_polynomial':sp.expand(sp.sympify(B['adjacency_characteristic_polynomial']))==sp.expand(expectedB),
      'flat_critical_group':F['critical_group_factors']=={'3':4,'6':4,'18':1,'54':1,'216':6},
      'curved_critical_group':B['critical_group_factors']=={'3':1,'9':4,'27':3,'135':5,'405':1},
      'flat_tree_spectral_checksum':F['spanning_tree_order']==2**24*3**31,
      'curved_tree_spectral_checksum':B['spanning_tree_order']==3**37*5**6}
    return {'schema':'w33.pass443.section_sensitive_smith_classification.v1','status':'PASS' if all(checks.values()) else 'FAIL',
      'theorem':{'flatness':'a section c is linear iff delta=(c2-c0-c1,c3-2c0-c1)=(0,0)',
       'orbits':'Aut(H_3) has exactly two orbits on inverse-closed sections: 9 flat and 72 curved',
       'spectral_jump':'flat spectrum 8^1,2^12,(-1)^8,(-4)^6; curved spectrum 8^1,(-1)^14, roots of x^2-x-11 each with multiplicity 6',
       'smith_jump':'curvature changes both rational spectrum and integral critical group; there are no cospectral/non-Smith-equivalent sections at q=3'},
      'classes':{'flat':F,'curved':B},'checks':checks}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=build_payload();text=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
    if a.check:
        if not a.output.exists() or a.output.read_text()!=text:raise SystemExit('Pass 443 certificate drift')
    else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(text)
    print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks'])}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
