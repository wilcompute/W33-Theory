#!/usr/bin/env python3
"""Pass5627: identify the actual symmetry domain of the signed q=3 deck 16.

The 16 Segre projective events are only a carrier inside PG(3,3), not a
PSp(4,3)-invariant set.  This verifier builds PSp(4,3) from symplectic
transvections, computes the Segre setwise stabilizer, then repeats the calculation
upstairs in Sp(4,3) on vector representatives.

The vector stabilizer acts on the deck-odd basis by signed monomial matrices.  Its
central -I acts as -I_16.  Therefore this signed representation cannot descend to
PSp(4,3), whereas any ordinary PSp module (including either Pass332 D5 half-spin
16) pulls back with central -I acting trivially.  Dimension 16 is not an
identification.
"""
from __future__ import annotations
import itertools, json, math
from collections import Counter
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5627_DECK_STABILIZER_SPINOR_NO_GO.json'
Q=3
J=np.array([[0,1,0,0],[-1,0,0,0],[0,0,0,1],[0,0,-1,0]],dtype=int)%Q

def norm(v):
    v=tuple(int(x)%Q for x in v)
    for a in v:
        if a:
            z=pow(a,-1,Q); return tuple((z*x)%Q for x in v)
    raise ValueError('zero vector')

def B(x,y):
    x=np.array(x,dtype=int); y=np.array(y,dtype=int)
    return int(x@J@y)%Q

def p1(): return [(1,t) for t in range(Q)]+[(0,1)]
def segre(u,v): return norm((u[0]*v[0],u[1]*v[1],u[0]*v[1],-u[1]*v[0]))
def compose(a,b): return tuple(a[b[i]] for i in range(len(a)))
def perm_order(p):
    seen=[False]*len(p); ans=1
    for i in range(len(p)):
        if seen[i]: continue
        j=i;n=0
        while not seen[j]: seen[j]=True;j=p[j];n+=1
        ans=math.lcm(ans,n)
    return ans

def projective_points():
    return sorted({norm(v) for v in itertools.product(range(Q),repeat=4) if any(v)})

def trans_perm(v,pts,index):
    return tuple(index[norm(tuple((x[i]+B(x,v)*v[i])%Q for i in range(4)))] for x in pts)

def closure_perm(gens,n):
    e=tuple(range(n)); G={e}; front=[e]
    while front:
        x=front.pop()
        for s in gens:
            y=compose(s,x)
            if y not in G: G.add(y);front.append(y)
    return G

def trans_mat(v):
    v=np.array(v,dtype=int)%Q; jv=J@v%Q
    M=(np.eye(4,dtype=int)+np.outer(v,jv))%Q
    return tuple(int(x) for x in M.flat)
def arr(M): return np.array(M,dtype=int).reshape(4,4)
def mcomp(a,b): return tuple(int(x) for x in ((arr(a)@arr(b))%Q).flat)
def closure_mat(gens):
    e=tuple(int(x) for x in np.eye(4,dtype=int).flat); G={e};front=[e]
    while front:
        x=front.pop()
        for s in gens:
            y=mcomp(s,x)
            if y not in G: G.add(y);front.append(y)
    return G

def apply(M,v): return tuple(int(x) for x in (arr(M)@np.array(v,dtype=int)%Q))

def main():
    pts=projective_points(); assert len(pts)==40; pi={p:i for i,p in enumerate(pts)}
    seed=[(1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1),(1,0,1,0)]
    PG=closure_perm([trans_perm(v,pts,pi) for v in seed],40); assert len(PG)==25920
    P=p1(); S=[segre(u,v) for u in P for v in P]; assert len(set(S))==16
    Sind={pi[x] for x in S}
    pstab=[g for g in PG if {g[i] for i in Sind}==Sind]; assert len(pstab)==48
    order_hist=Counter(perm_order(g) for g in pstab)
    assert order_hist==Counter({1:1,2:19,3:8,4:12,6:8})

    SG=closure_mat([trans_mat(v) for v in seed]); assert len(SG)==51840
    Sset=set(S); vst=[M for M in SG if {norm(apply(M,v)) for v in S}==Sset]; assert len(vst)==96
    si={v:i for i,v in enumerate(S)}
    def signed_action(M):
        p=[];sg=[]
        for v in S:
            y=apply(M,v); ny=norm(y); p.append(si[ny])
            k=next(i for i,z in enumerate(ny) if z)
            a=(y[k]*pow(ny[k],-1,Q))%Q; assert a in (1,2)
            sg.append(1 if a==1 else -1)
        return tuple(p),tuple(sg)
    chars=[]
    for M in vst:
        p,s=signed_action(M); chars.append(sum(s[i] for i in range(16) if p[i]==i))
    ch=Counter(chars); assert ch==Counter({0:78,4:8,-4:8,16:1,-16:1})
    inner=sum(x*x for x in chars)//len(chars); assert inner==8
    minusI=tuple(int(x) for x in ((-np.eye(4,dtype=int))%Q).flat); assert minusI in vst
    p,s=signed_action(minusI); assert p==tuple(range(16)) and set(s)=={-1}

    out={
      'pass':5627,'status':'SIGNED_DECK16_IS_STABILIZER_SPINORIAL_NOT_PSP_HALFSPIN',
      'PSp43_order':len(PG),'Segre_projective_points':16,'PSp_Segre_stabilizer_order':len(pstab),
      'PSp_stabilizer_element_orders':{str(k):v for k,v in sorted(order_hist.items())},
      'Sp43_order':len(SG),'vector_Segre_stabilizer_order':len(vst),'central_kernel_order':2,
      'signed_deck16_character_histogram':{str(k):v for k,v in sorted(ch.items())},
      'signed_character_self_inner_product':inner,
      'central_minus_I_action':'-I_16',
      'theorem':'The Segre 16 is not PSp(4,3)-invariant. Its deck-odd vector lift is a genuine central-sign representation of the 96-element Sp preimage of the 48-element projective carrier stabilizer, and central -I acts as -I_16.',
      'D5_halfspin_no_go':'Any ordinary PSp(4,3) module pulled back to Sp(4,3) has central -I in the kernel. Pass332 half-spins are ordinary PSp modules. Hence the signed deck16 cannot be equivariantly identified with either D5 half-spin16.',
      'physics_boundary':'This is a finite double-valued/spinorial central-sign property on the carrier stabilizer. It is not a Spin(3,1) representation, a spin-statistics theorem, or a Standard Model generation.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__': main()
