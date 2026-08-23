#!/usr/bin/env python3
"""Pass7917-7924 (outside-box): genuine Leech linking similitudes split 234 W33 polarities as 36+36+81+81.

Pass7901 used the full projective stabilizer of the canonical rank-2 top form K and
found two orbits 72+162 on the 234 W33 polarities.  Not every projective symmetry
lifts to a similitude of the actual mixed (3/9)-torsion linking pairing.  The lift
condition is det(A)=det(D) on the two GL2(3) diagonal blocks.  Its projective top
image has order 46656 and splits the moduli into four orbits
    36_+, 36_-, 81_+, 81_-,
where +/- is exactly the Pfaffian family of Pass7725.

Internally, the overlap-60 graph on either 36-orbit is 3 K_{3,3,3,3}; on either
81-orbit it is SRG(81,24,9,6).  Cross-degrees for W33 edge overlaps 60/78/96 are
also constant, so the four fibres form an exact coherent quotient.

The decomposition 234=36+36+81+81 is numerically identical to E8 minus a chosen
A2: 72 E6 roots plus the two 81 charged sectors.  That is recorded as an explicit
object-map target, not promoted as an E8 identification.
"""
from __future__ import annotations
import itertools,json
from collections import Counter,deque
from pathlib import Path
import numpy as np
from sympy.combinatorics import Permutation,PermutationGroup

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS7917_7924_LEECH_SIMILITUDE_234_FOUR_ORBITS.json'

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

def fkey(M):
    M=np.asarray(M,dtype=int)%3
    z=[int(M[i,j]) for i,j in ((0,1),(0,2),(0,3),(1,2),(1,3),(2,3))]
    if next(x for x in z if x)==2:M=(-M)%3;z=[int(M[i,j]) for i,j in ((0,1),(0,2),(0,3),(1,2),(1,3),(2,3))]
    return tuple(z)
def pf(k):
    a,b,c,d,e,f=k;return (a*f-b*e+c*d)%3

def srg(A):
    n=len(A);ks=set(map(int,A.sum(1)));assert len(ks)==1;k=ks.pop();la=set();mu=set()
    for i,j in itertools.combinations(range(n),2):
        z=int(A[i]@A[j]);(la if A[i,j] else mu).add(z)
    return [n,k,sorted(la),sorted(mu)]

def main():
    P=sorted({canon(v) for v in itertools.product(range(3),repeat=4) if any(v)});assert len(P)==40
    forms={}
    for a,b,c,d,e,f in itertools.product(range(3),repeat=6):
        M=np.array([[0,a,b,c],[-a,0,d,e],[-b,-d,0,f],[-c,-e,-f,0]],dtype=int)%3
        if rank_mod(M)==4:forms[fkey(M)]=M if fkey(M)==(a,b,c,d,e,f) else (-M)%3
    assert len(forms)==234
    keys=sorted(forms);ki={k:i for i,k in enumerate(keys)}

    s1=np.array([[1,1],[0,1]],int)%3;s2=np.array([[0,2],[1,0]],int)%3;flip=np.array([[2,0],[0,1]],int)%3;I=np.eye(2,dtype=int)%3
    gens=[]
    for A in (s1,s2):gens.append(np.block([[A,np.zeros((2,2),int)],[np.zeros((2,2),int),I]])%3)
    for D in (s1,s2):gens.append(np.block([[I,np.zeros((2,2),int)],[np.zeros((2,2),int),D]])%3)
    gens.append(np.block([[flip,np.zeros((2,2),int)],[np.zeros((2,2),int),flip]])%3) # simultaneous det=-1
    for i in range(2):
      for j in range(2):
        C=np.zeros((2,2),int);C[i,j]=1;gens.append(np.block([[I,np.zeros((2,2),int)],[C,I]])%3)
    perms=[]
    for g in gens:
        p=[ki[fkey((g.T@forms[k]@g)%3)] for k in keys];assert sorted(p)==list(range(234));perms.append(p)
    G=PermutationGroup([Permutation(p) for p in perms]);assert int(G.order())==46656
    orbs=sorted([sorted(map(int,o)) for o in G.orbits()],key=lambda O:(len(O),pf(keys[O[0]])))
    assert [len(O) for O in orbs]==[36,36,81,81]
    assert [(len(O),pf(keys[O[0]])) for O in orbs]==[(36,1),(36,2),(81,1),(81,2)]

    edges=[]
    for k in keys:
        M=forms[k];E=set()
        for i,u in enumerate(P):
          U=np.array(u,dtype=int)
          for j in range(i+1,40):
            if int(U@M@np.array(P[j],dtype=int))%3==0:E.add((i,j))
        assert len(E)==240;edges.append(frozenset(E))

    internal=[]
    for O in orbs:
        n=len(O);A=np.zeros((n,n),dtype=np.int8)
        for i in range(n):
          for j in range(i+1,n):
            if len(edges[O[i]]&edges[O[j]])==60:A[i,j]=A[j,i]=1
        pars=srg(A);spec=Counter(round(float(x),8) for x in np.linalg.eigvalsh(A.astype(float)))
        if n==36:
            assert pars==[36,9,[6],[0,9]] and spec==Counter({0.0:24,-3.0:9,9.0:3})
            typ='3 K_{3,3,3,3}'
        else:
            assert pars==[81,24,[9],[6]] and spec==Counter({-3.0:56,6.0:24,24.0:1})
            typ='SRG(81,24,9,6)'
        internal.append({'size':n,'pfaffian':pf(keys[O[0]]),'overlap60_graph':typ,'spectrum':{str(k):v for k,v in spec.items()}})

    # Constant cross-degrees for overlap values 60,78,96.
    cross={}
    for a in range(4):
      for b in range(a+1,4):
        Oa,Ob=orbs[a],orbs[b];row=[]
        for i in Oa:
            c=Counter(len(edges[i]&edges[j]) for j in Ob);row.append((c[60],c[78],c[96]))
        assert len(set(row))==1;cross[f'{len(Oa)}_{pf(keys[Oa[0]])}--{len(Ob)}_{pf(keys[Ob[0]])}']=list(row[0])
    expected={
      '36_1--36_2':[18,0,18],
      '36_1--81_1':[27,54,0],
      '36_1--81_2':[54,0,27],
      '36_2--81_1':[54,0,27],
      '36_2--81_2':[27,54,0],
      '81_1--81_2':[48,0,33]}
    assert cross==expected

    out={
      'schema':'w33.pass7917_7924.leech_similitude_234_four_orbits.v1','status':'PASS','passes':'7917-7924','outside_box':True,
      'linking_similitude_projective_top_group_order':46656,
      'lift_condition':'det(A)=det(D) on the two GL2(3) blocks; this is index two inside the full projective stabilizer used in Pass7901',
      'polarization_orbits':[{'size':36,'pfaffian':1},{'size':36,'pfaffian':2},{'size':81,'pfaffian':1},{'size':81,'pfaffian':2}],
      'internal_overlap60_graphs':internal,'cross_degree_order':'entries are degrees for W33 edge-overlap [60,78,96]','cross_degrees':cross,
      'E8_target':'234=240-6 and the orbit sizes 36+36+81+81 reproduce the cardinality pattern of E8\\A2 = 72 E6 roots + 81 + 81 charged roots after a 36+36 sign split.',
      'theorem':'The actual symmetries that lift from the mixed Leech linking module refine the 72+162 parabolic split of the 234 W33 polarities into four Pfaffian-labelled orbits 36,36,81,81 with a rigid coherent overlap quotient.',
      'claim_boundary':'The orbit-size pattern is exact. No bijection to E8 roots is claimed until an objectwise map intertwining a common subgroup/action is constructed.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','group':46656,'orbits':[36,36,81,81],'cross':cross}))
if __name__=='__main__':main()
