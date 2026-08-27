#!/usr/bin/env python3
"""Pass10477-10484: explicit H(4) -> C13 quotient -> C6 quotient and the 27-state test.

Uses the exact 6x6 F4 G2(4) matrices frozen in Pass10453-10476.  Wilson's
standard-generator words construct an explicit 13:6 normalizer.  From one
certified H(4) line we regenerate its 1365-line G2(4) orbit, hence the full
20-regular H(4) point graph on PG(5,4).

The order-13 element has 105 projective cycles.  The order-6 complement acts on
those cycles with orbit lengths 1^3 2^6 3^6 6^12, giving 27 states.  We compute
the exact equitable quotient R of H(4) adjacency.

Two results are separated deliberately:
  * carrier bridge: the cyclic C105 torsor factors as C3 x C35, and the C6
    multiplier is identity on C3, so the 27 states canonically form nine triples;
  * transport no-go: R is weighted and has loops, with spectrum
      20^1, 7^8, (-1)^12, (-5)^6,
    hence it is neither the simple H27 graph nor the Schlaefli graph from
    Pass7629-7636.  The common nine-triple carrier survives; direct adjacency
    identification does not.
"""
from __future__ import annotations
from collections import Counter,deque
import itertools,json
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS10477_10484_H4_NORMALIZER_27STATE_QUOTIENT.json'

# F4 encoding 0,1,w,1+w -> 0,1,2,3 with w^2+w+1=0.
def mul(x,y):
    a=x&1;b=(x>>1)&1;c=y&1;d=(y>>1)&1
    return (a*c ^ b*d) | ((a*d ^ b*c ^ b*d)<<1)
def invs(x): assert x; return mul(x,x)
def eye(n=6): return np.eye(n,dtype=np.uint8)
def mm(A,B):
    A=np.array(A,dtype=np.uint8);B=np.array(B,dtype=np.uint8)
    C=np.zeros((A.shape[0],B.shape[1]),dtype=np.uint8)
    for i in range(A.shape[0]):
      for k in range(A.shape[1]):
        if A[i,k]:
          for j in range(B.shape[1]):
            if B[k,j]: C[i,j]^=mul(int(A[i,k]),int(B[k,j]))
    return C
def invm(A):
    A=np.array(A,dtype=np.uint8);n=A.shape[0];M=np.concatenate([A,eye(n)],1)
    for c in range(n):
      q=next(i for i in range(c,n) if M[i,c]);M[[c,q]]=M[[q,c]]
      u=invs(int(M[c,c]));M[c]=np.array([mul(int(x),u) for x in M[c]],dtype=np.uint8)
      for i in range(n):
        if i!=c and M[i,c]:
          t=int(M[i,c]);M[i]^=np.array([mul(t,int(x)) for x in M[c]],dtype=np.uint8)
    return M[:,n:]
def pw(A,n):
    if n<0:return pw(invm(A),-n)
    R=eye(A.shape[0]);X=np.array(A,dtype=np.uint8)
    while n:
      if n&1:R=mm(R,X)
      X=mm(X,X);n//=2
    return R
def conj(x,y): return mm(mm(invm(y),x),y)
def order(A,cap=5000):
    R=eye(A.shape[0])
    for k in range(1,cap+1):
      R=mm(R,A)
      if np.array_equal(R,eye(A.shape[0])):return k
    raise RuntimeError('order cap')
def scale(c,v): return np.array([mul(c,int(x)) for x in v],dtype=np.uint8)
def norm(v):
    v=np.array(v,dtype=np.uint8)
    for x in v:
      if x:return tuple(int(y) for y in scale(invs(int(x)),v))
    raise ValueError
def mv(A,v):return mm(A,np.array(v,dtype=np.uint8).reshape(-1,1))[:,0]

def cycles(p):
    seen=[False]*len(p);out=[]
    for i in range(len(p)):
      if seen[i]:continue
      C=[];j=i
      while not seen[j]:seen[j]=True;C.append(j);j=int(p[j])
      out.append(C)
    return out

def main():
    g1=np.array([[3,0,0,1,2,0],[3,3,2,0,1,2],[2,0,0,0,0,2],[1,2,2,3,2,3],[2,0,1,2,0,0],[1,2,2,1,3,0]],dtype=np.uint8)
    g2=np.array([[3,1,2,2,1,1],[2,1,1,3,0,0],[2,3,1,0,3,0],[3,3,1,1,1,1],[3,2,1,1,2,1],[3,2,2,0,2,3]],dtype=np.uint8)
    assert (order(g1),order(g2),order(mm(g1,g2)))==(13,13,15)

    # Wilson Sec. 4.2 words.
    g3=pw(mm(pw(g1,4),g2),4)
    X=pw(mm(mm(mm(g1,g2),g1),pw(g2,2)),3)
    g4=conj(X,pw(g2,4))
    A=pw(mm(pw(mm(g3,g4),3),g4),3)
    B0=pw(mm(g3,g4),4);B0=mm(B0,g4);B0=mm(B0,g3);B0=mm(B0,g4);B0=mm(B0,pw(mm(g3,pw(g4,2)),2))
    g5=mm(mm(A,pw(B0,3)),invm(A))
    Y=mm(mm(mm(g3,g4),g3),pw(g4,2))
    g6=mm(pw(Y,-2),mm(pw(mm(mm(g3,g4),pw(Y,2)),5),pw(Y,2)))
    assert (order(g3),order(g4),order(g5),order(g6),order(mm(g5,g6)))==(2,5,2,3,13)
    g7=conj(g6,mm(g5,pw(g6,2)))
    g8=mm(mm(mm(g5,g7),g5),pw(g7,2)); n=mm(g5,g7)
    assert order(g8)==13 and order(n)==6 and np.array_equal(conj(g8,n),pw(g8,4))

    pts=[];seen=set()
    for v in itertools.product(range(4),repeat=6):
      if any(v):
        p=norm(v)
        if p not in seen:seen.add(p);pts.append(p)
    assert len(pts)==1365;pi={p:i for i,p in enumerate(pts)}
    def perm(A):return np.array([pi[norm(mv(A,p))] for p in pts],dtype=np.int32)
    pg1,pg2,pg8,pn=map(perm,(g1,g2,g8,n))

    # Certified H(4) line seed; its G2(4)-orbit has exactly 1365 lines.
    seed=tuple(sorted(pi[p] for p in [(0,0,0,0,0,1),(0,1,3,0,0,0),(0,1,3,0,0,1),(0,1,3,0,0,2),(0,1,3,0,0,3)]))
    L={seed};Q=deque([seed])
    while Q:
      e=Q.popleft()
      for p in (pg1,pg2):
        f=tuple(sorted(int(p[x]) for x in e))
        if f not in L:L.add(f);Q.append(f)
    assert len(L)==1365 and all(len(x)==5 for x in L)
    adj=[set() for _ in pts]
    for line in L:
      for x in line:adj[x].update(y for y in line if y!=x)
    assert set(map(len,adj))=={20}

    c13=cycles(pg8);assert Counter(map(len,c13))==Counter({13:105})
    cid={x:i for i,C in enumerate(c13) for x in C}
    W=np.zeros((105,105),dtype=np.int64)
    for i,C in enumerate(c13):
      x=C[0]
      for y in adj[x]:W[i,cid[y]]+=1
    assert set(map(int,W.sum(1)))=={20}
    pc=np.zeros(105,dtype=np.int32)
    for i,C in enumerate(c13):
      z={cid[int(pn[x])] for x in C};assert len(z)==1;pc[i]=next(iter(z))
    c6=cycles(pc);assert Counter(map(len,c6))==Counter({6:12,3:6,2:6,1:3})
    oid={x:i for i,C in enumerate(c6) for x in C}
    R=np.zeros((27,27),dtype=np.int64)
    for i,C in enumerate(c6):
      a=C[0]
      for b,w in enumerate(W[a]):
        if w:R[i,oid[b]]+=int(w)
    assert set(map(int,R.sum(1)))=={20}
    assert set(map(int,R.ravel()))=={0,1,2,3,4,6}
    assert int(np.count_nonzero(np.diag(R)))==16

    # Exact spectrum via a square-free annihilating polynomial and nullities.
    I=np.eye(27,dtype=np.int64);Z=I.copy()
    for lam in (20,7,-1,-5):Z=Z@(R-lam*I)
    assert not np.any(Z)
    def rankq(A):
      # exact rational rank is safe for 27x27 small integers
      import sympy as sp
      return int(sp.Matrix(A.tolist()).rank())
    mult={str(l):27-rankq(R-l*I) for l in (20,7,-1,-5)}
    assert mult=={'20':1,'7':8,'-1':12,'-5':6}

    # Build a primitive field multiplier alpha in F4[g8].
    pows=[eye(6)]
    for _ in range(5):pows.append(mm(pows[-1],g8))
    def sm(c,M):
      T=np.zeros_like(M)
      for i in range(6):
       for j in range(6):
        if M[i,j]:T[i,j]=mul(c,int(M[i,j]))
      return T
    alpha=sm(1,pows[3])^sm(1,pows[4])^sm(2,pows[5])
    assert order(alpha)==4095
    pa=perm(alpha);pac=np.zeros(105,dtype=np.int32)
    for i,C in enumerate(c13):
      z={cid[int(pa[x])] for x in C};assert len(z)==1;pac[i]=next(iter(z))
    assert Counter(map(len,cycles(pac)))==Counter({105:1})
    fixed=[i for i in range(105) if pc[i]==i];assert len(fixed)==3
    origin=fixed[0];lab=[];back={};x=origin
    for k in range(105):lab.append(x);back[x]=k;x=int(pac[x])
    assert x==origin and all(back[int(pc[lab[k]])]==(79*k)%105 for k in range(105))

    # C105 = C3 x C35.  The multiplier 79 is 1 mod3 and 9 mod35,
    # so the 27 C6-orbits canonically form nine triples.
    seen35=set();o35=[]
    for s in range(35):
      if s in seen35:continue
      O=[];x=s
      while x not in O:O.append(x);seen35.add(x);x=(79*x)%35
      o35.append(tuple(O))
    assert len(o35)==9 and Counter(map(len,o35))==Counter({6:4,3:2,2:2,1:1})
    o35id={x:i for i,O in enumerate(o35) for x in O}
    packets=Counter()
    for C in c6:
      labs=[back[x] for x in C]; rr={k%3 for k in labs};oo={o35id[k%35] for k in labs}
      assert len(rr)==len(oo)==1;packets[(next(iter(oo)),next(iter(rr)))]+=1
    assert len(packets)==27 and set(packets.values())=={1}

    old=json.loads((ROOT/'data/PART_W33_PASS7629_7636_SCHLAEFLI_H27_STEINBERG_COMPLEMENT.json').read_text())
    assert old['H27']['degree']==8 and old['Schlaefli']['parameters'][1]==16
    out={
      'schema':'w33.pass10477_10484.h4_normalizer_27state_quotient.v1','status':'PASS','passes':'10477-10484',
      'explicit_normalizer':{'g8_order':13,'complement_order':6,'conjugation':'g8^n=g8^4'},
      'H4':{'points':1365,'lines':1365,'degree':20},
      'C13_quotient':{'states':105,'weighted_degree':20,'cycle_length':13},
      'C6_on_105':{'orbit_lengths':{'1':3,'2':6,'3':6,'6':12},'state_count':27},
      'quotient27':{'weighted_degree':20,'entry_values':[0,1,2,3,4,6],'nonzero_diagonal_states':16,'spectrum':mult,'matrix':R.tolist()},
      'cyclic_torsor':{'primitive_alpha_order':4095,'projective_cycle_torsor':'C105','normalizer_multiplier_mod105':79,'equivalent_inverse_multiplier':4,'factorization':'C105 ~= C3 x C35','C35_multiplier':9,'C35_orbit_lengths':dict(Counter(map(len,o35))),'canonical_packet_structure':'9 packets x 3 states'},
      'comparison_to_pass7629_7636':{
        'common_carrier_feature':'both have 27 states canonically organized as nine triples',
        'H27_degree':8,'Schlaefli_degree':16,
        'direct_adjacency_identification':False,
        'reason':'the H4 normalizer quotient is weighted, has loops on 16 states, weighted degree 20, and spectrum 20^1 7^8 (-1)^12 (-5)^6; H27 and Schlaefli are loopless simple graphs of degrees 8 and 16'},
      'theorem':'The explicit 13:6 normalizer of canonical H(4) produces a 105-state C13 quotient and a 27-state C6 orbit quotient. Arithmetic of the C105 torsor canonically organizes those 27 states into nine triples, exactly matching the carrier architecture of the repo H27/Schlaefli transport. The induced H(4) adjacency is nevertheless a different weighted transport, so the bridge is carrier-level, not a direct graph isomorphism.',
      'boundary':'All finite-field, orbit, H(4), quotient-matrix and spectrum statements are exact. No H27/Schlaefli adjacency identification is claimed; it is explicitly falsified for the natural quotient adjacency.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','states':[105,27],'packets':'9x3','spectrum':mult,'direct_H27':False}))
if __name__=='__main__':main()
