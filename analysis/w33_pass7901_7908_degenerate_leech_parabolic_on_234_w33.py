#!/usr/bin/env python3
"""Pass7901-7908 (outside-box): the canonical rank-2 Leech form acts on the 234 W33 polarities.

Pass7725 classifies 234 projective nondegenerate alternating forms on PG(3,3),
each a labelled W33 polarity.  Pass7861 supplies a canonical *degenerate* rank-2
alternating form K from multiplication by 3 in the corrected Leech module.
This verifier computes the projective stabilizer P(K) and its orbits on all 234
W33 polarities.  There are exactly two: 72 and 162.  The 162 orbit is precisely
those polarities for which one of M+K or M-K drops to rank 2; the 72 orbit is the
transverse class for which both remain nondegenerate.  Their W33 graphs meet the
canonical degenerate orthogonality relation in 96 and 78 edges respectively.

The numerical split 72+162 matches the E8=A2 + E6 + charged-root decomposition
72+(81+81), but no objectwise E8 identification is claimed here.
"""
from __future__ import annotations
import itertools,json
from collections import Counter,deque
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS7901_7908_DEGENERATE_LEECH_PARABOLIC_ON_234_W33.json'

def canon(v):
    v=tuple(int(x)%3 for x in v)
    for x in v:
        if x:return tuple(((1 if x==1 else 2)*y)%3 for y in v)
    raise ValueError

def rank_mod(A,p=3):
    M=np.asarray(A,dtype=int).copy()%p;m,n=M.shape;r=0
    for c in range(n):
        z=next((i for i in range(r,m) if M[i,c]),None)
        if z is None:continue
        M[[r,z]]=M[[z,r]];M[r]=(M[r]*pow(int(M[r,c]),-1,p))%p
        for i in range(m):
            if i!=r and M[i,c]:M[i]=(M[i]-int(M[i,c])*M[r])%p
        r+=1
    return r

def key(M):
    M=np.asarray(M,dtype=int)%3
    z=[int(M[i,j]) for i,j in ((0,1),(0,2),(0,3),(1,2),(1,3),(2,3))]
    first=next(x for x in z if x)
    if first==2:M=(-M)%3;z=[int(M[i,j]) for i,j in ((0,1),(0,2),(0,3),(1,2),(1,3),(2,3))]
    return tuple(z)

def main():
    P=sorted({canon(v) for v in itertools.product(range(3),repeat=4) if any(v)});assert len(P)==40
    forms={}
    for a,b,c,d,e,f in itertools.product(range(3),repeat=6):
        M=np.array([[0,a,b,c],[-a,0,d,e],[-b,-d,0,f],[-c,-e,-f,0]],dtype=int)%3
        if rank_mod(M)==4:forms[key(M)]=M if key(M)==(a,b,c,d,e,f) else (-M)%3
    assert len(forms)==234
    keys=sorted(forms);idx={k:i for i,k in enumerate(keys)}
    K=np.array([[0,1,0,0],[-1,0,0,0],[0,0,0,0],[0,0,0,0]],dtype=int)%3

    # Projective stabilizer of K: block matrices [[A,0],[C,D]] with A,D in GL2(3),
    # C arbitrary, modulo the two scalar matrices. Order=48^2*3^4/2.
    GL=[]
    for z in itertools.product(range(3),repeat=4):
        A=np.array(z,dtype=int).reshape(2,2)%3
        if rank_mod(A)==2:GL.append(A)
    assert len(GL)==48
    stabilizer_order=48*48*81//2;assert stabilizer_order==93312

    g1=np.array([[1,1],[0,1]],int)%3;g2=np.array([[0,1],[1,0]],int)%3;g3=np.array([[2,0],[0,1]],int)%3;I=np.eye(2,dtype=int)%3
    gens=[]
    for A in (g1,g2,g3):gens.append(np.block([[A,np.zeros((2,2),int)],[np.zeros((2,2),int),I]])%3)
    for D in (g1,g2,g3):gens.append(np.block([[I,np.zeros((2,2),int)],[np.zeros((2,2),int),D]])%3)
    for i in range(2):
      for j in range(2):
        C=np.zeros((2,2),int);C[i,j]=1;gens.append(np.block([[I,np.zeros((2,2),int)],[C,I]])%3)
    for g in gens:
        q=(g.T@K@g)%3
        assert key(q)==key(K)

    perms=[]
    for g in gens:
        p=[]
        for k in keys:p.append(idx[key((g.T@forms[k]@g)%3)])
        assert sorted(p)==list(range(234));perms.append(p)
    seen=set();orbs=[]
    for s in range(234):
        if s in seen:continue
        O={s};q=[s];seen.add(s)
        while q:
            x=q.pop()
            for p in perms:
                y=p[x]
                if y not in O:O.add(y);seen.add(y);q.append(y)
        orbs.append(sorted(O))
    assert sorted(map(len,orbs))==[72,162]

    Dg=np.zeros((40,40),dtype=np.int8)
    for i,u in enumerate(P):
      U=np.array(u,dtype=int)
      for j in range(i+1,40):
        if int(U@K@np.array(P[j],dtype=int))%3==0:Dg[i,j]=Dg[j,i]=1
    assert int(Dg.sum()//2)==294

    signatures=Counter();orbit_sig=[]
    for O in orbs:
        sig=Counter()
        for i in O:
            M=forms[keys[i]]
            A=np.zeros((40,40),dtype=np.int8)
            for x,u in enumerate(P):
              U=np.array(u,dtype=int)
              for y in range(x+1,40):
                if int(U@M@np.array(P[y],dtype=int))%3==0:A[x,y]=A[y,x]=1
            overlap=int(np.sum(np.triu(A*Dg,1)))
            drops=sum(rank_mod((M+s*K)%3)==2 for s in (1,2))
            sig[(overlap,drops)]+=1
        orbit_sig.append(sig)
    assert sorted(orbit_sig,key=lambda c:sum(c.values()))==[Counter({(78,0):72}),Counter({(96,1):162})]

    out={
      'schema':'w33.pass7901_7908.degenerate_leech_parabolic_on_234_w33.v1','status':'PASS','passes':'7901-7908','outside_box':True,
      'canonical_rank2_form':'multiplication-by-3 form K from Pass7861','projective_stabilizer_order':stabilizer_order,
      'stabilizer_structure':'3^4 : (GL2(3) x GL2(3)) modulo common scalar center',
      'action_on_234_polarities':{'orbit_sizes':[72,162],'orbit72':'both M+K and M-K have rank 4; W33/degenerated-form edge overlap 78','orbit162':'exactly one of M+K,M-K has rank 2; edge overlap 96'},
      'E8_numerical_echo':'72 and 162=81+81 are exactly the E6-root and charged-root counts in the E8 relative-A2 decomposition. This equality is recorded as a target for an objectwise intertwiner, not as an identification.',
      'theorem':'The Leech-intrinsic degenerate alternating form reduces the 234 possible W33 polarizations to two canonical parabolic orbits of sizes 72 and 162. Thus the corrected 3-adic filtration supplies substantial selection structure even though it does not choose a unique W33 polarity.',
      'claim_boundary':'Exact projective-group orbit theorem. The 72/162 equality with E8 shell counts is not promoted beyond a structural numerical echo until an equivariant object map is built.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','orbits':[72,162],'stabilizer':93312,'overlaps':[78,96]}))
if __name__=='__main__':main()
