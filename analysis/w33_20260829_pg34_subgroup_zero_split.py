#!/usr/bin/env python3
"""Exact subgroup-breaking hierarchy for the 85-state chiral coupling.

For H <= PSp(4,3), an H-equivariant 40x45 coupling is constant on H-orbits
of cross pairs.  We construct that full orbital matrix space and exhibit exact
finite-field rank witnesses.  For the sentinel-circuit stabilizer S5 we also
decompose the two permutation characters explicitly, so its rank ceiling is
proved rather than inferred from random specialization.
"""
from __future__ import annotations
import itertools,json
from pathlib import Path
from collections import Counter

from w33_20260829_216_clifford_torsor_nogo import (
    geometry,supports_from_N,closure_paired,norm,form,porder
)
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_20260829_PG34_SUBGROUP_ZERO_SPLIT.json'
P=1000003

def rank_mod(A,p=P):
    M=[[x%p for x in r] for r in A];m=len(M);n=len(M[0]);r=0
    for c in range(n):
        q=next((i for i in range(r,m) if M[i][c]),None)
        if q is None:continue
        M[r],M[q]=M[q],M[r];inv=pow(M[r][c],p-2,p);M[r]=[(x*inv)%p for x in M[r]]
        for i in range(m):
            if i==r or not M[i][c]:continue
            a=M[i][c];M[i]=[(M[i][j]-a*M[r][j])%p for j in range(n)]
        r+=1
        if r==m:break
    return r

def parity(p):
    return sum(p[i]>p[j] for i in range(len(p)) for j in range(i+1,len(p)))&1

def cycle_type(p):
    seen=set();parts=[]
    for i in range(len(p)):
        if i in seen:continue
        j=i;n=0
        while j not in seen:seen.add(j);n+=1;j=p[j]
        parts.append(n)
    return tuple(sorted(parts,reverse=True))

def cross_orbit_index(H):
    rem={(i,j) for i in range(40) for j in range(45)};idx={};sizes=[];k=0
    while rem:
        seed=min(rem);O={(h[0][seed[0]],h[1][seed[1]]) for h in H}
        for x in O:idx[x]=k
        sizes.append(len(O));rem-=O;k+=1
    assert len(idx)==1800
    return idx,sorted(sizes)

def witness_rank(idx,norb,seed):
    x=(seed*1664525+1013904223)%P;coeff=[]
    for _ in range(norb):
        x=(1664525*x+1013904223)%P;coeff.append(1+x%(P-1))
    M=[[coeff[idx[(i,j)]] for j in range(45)] for i in range(40)]
    return rank_mod(M)

def main():
    pts,idxp,lines,N=geometry();supports,masks=supports_from_N(N)
    circuits=[]
    for cc in itertools.combinations(range(45),5):
        w=0
        for i in cc:w^=masks[i]
        if w==0:circuits.append(cc)
    assert len(circuits)==216

    gens40=[]
    for v in pts:
        for alpha in (1,2):
            p=[]
            for x in pts:
                z=alpha*form(x,v)%3;y=norm(tuple((x[k]+z*v[k])%3 for k in range(4)));p.append(idxp[y])
            gens40.append(tuple(p))
    si={S:i for i,S in enumerate(supports)};gens45=[]
    for p in gens40:gens45.append(tuple(si[frozenset(p[x] for x in S)] for S in supports))
    chosen=(18,62,77,10);G=closure_paired([gens40[i] for i in chosen],[gens45[i] for i in chosen]);assert len(G)==25920
    c0=tuple(circuits[0]);cset=set(c0)
    S5=[h for h in G if {h[1][x] for x in cset}==cset];assert len(S5)==120
    pos={x:i for i,x in enumerate(c0)}
    def p5(h):return tuple(pos[h[1][x]] for x in c0)
    A5=[h for h in S5 if parity(p5(h))==0];assert len(A5)==60
    S4=[h for h in S5 if p5(h)[0]==0];assert len(S4)==24
    A4=[h for h in S4 if parity(p5(h))==0];assert len(A4)==12
    V4=[h for h in A4 if porder(p5(h)) in (1,2)];assert len(V4)==4
    e=next(h for h in V4 if porder(p5(h))==1)
    g2=next(h for h in V4 if porder(p5(h))==2);C2=[e,g2]
    chain=[('PSp(4,3)',G),('S5',S5),('A5',A5),('S4',S4),('A4',A4),('V4',V4),('C2',C2),('1',[e])]

    # Exact S5 character decomposition. Classes are indexed by cycle type on
    # the stabilized five-circuit.  Rows are the seven irreps of S5.
    chars={
      '5':(1,{(1,1,1,1,1):1,(2,1,1,1):1,(2,2,1):1,(3,1,1):1,(3,2):1,(4,1):1,(5,):1}),
      '41':(4,{(1,1,1,1,1):4,(2,1,1,1):2,(2,2,1):0,(3,1,1):1,(3,2):-1,(4,1):0,(5,):-1}),
      '32':(5,{(1,1,1,1,1):5,(2,1,1,1):1,(2,2,1):1,(3,1,1):-1,(3,2):1,(4,1):-1,(5,):0}),
      '311':(6,{(1,1,1,1,1):6,(2,1,1,1):0,(2,2,1):-2,(3,1,1):0,(3,2):0,(4,1):0,(5,):1}),
      '221':(5,{(1,1,1,1,1):5,(2,1,1,1):-1,(2,2,1):1,(3,1,1):-1,(3,2):-1,(4,1):1,(5,):0}),
      '2111':(4,{(1,1,1,1,1):4,(2,1,1,1):-2,(2,2,1):0,(3,1,1):1,(3,2):1,(4,1):0,(5,):-1}),
      '11111':(1,{(1,1,1,1,1):1,(2,1,1,1):-1,(2,2,1):1,(3,1,1):1,(3,2):-1,(4,1):-1,(5,):1})}
    class_count=Counter(cycle_type(p5(h)) for h in S5);assert sum(class_count.values())==120
    perm40={};perm45={}
    for ct in class_count:
        vals=[h for h in S5 if cycle_type(p5(h))==ct]
        f40={sum(h[0][i]==i for i in range(40)) for h in vals};f45={sum(h[1][i]==i for i in range(45)) for h in vals}
        assert len(f40)==len(f45)==1;perm40[ct]=f40.pop();perm45[ct]=f45.pop()
    def mults(perm):
        out={}
        for name,(dim,ch) in chars.items():
            num=sum(class_count[ct]*perm[ct]*ch[ct] for ct in class_count);assert num%120==0;out[name]=num//120
        assert sum(chars[n][0]*m for n,m in out.items()) in (40,45);return out
    m40,m45=mults(perm40),mults(perm45)
    s5_ceiling=sum(chars[n][0]*min(m40[n],m45[n]) for n in chars);assert s5_ceiling==30

    rows=[]
    for name,H in chain:
        oi,sizes=cross_orbit_index(H);norb=1+max(oi.values());best=(-1,None)
        for seed in range(1,129):
            r=witness_rank(oi,norb,seed)
            if r>best[0]:best=(r,seed)
            if r==40:break
        r,seed=best
        exact=None
        if name=='PSp(4,3)': assert r==25;exact=25
        elif name=='S5': assert r==s5_ceiling;exact=s5_ceiling
        elif r==40: exact=40
        rows.append({'subgroup':name,'order':len(H),'crossPairOrbits':norb,'crossOrbitSizes':sizes,
          'rankWitness':r,'witnessSeed':seed,'provenMaximumRank':exact,
          'minimumChiralZeroModes':None if exact is None else 85-2*exact})

    out={'schema':'w33.20260829.pg34-subgroup-zero-split.v2','status':'PASS','chain':rows,
      'S5CharacterDecomposition':{'classCounts':{str(k):v for k,v in class_count.items()},'left40':m40,'right45':m45,
        'maximumEquivariantRank':s5_ceiling,'minimumZeroModes':85-2*s5_ceiling},
      'theorem':'Breaking PSp(4,3) to the sentinel-circuit S5 raises the permitted coupling rank from 25 to exactly 30, reducing protected zero modes from 35 to 25. Any later subgroup with an exhibited rank-40 witness leaves only the five index-protected modes.',
      'boundary':'Exact finite chiral-coupling/intertwiner statement. A symmetry-allowed perturbation is not asserted to be physically local or dynamically generated.'}
    OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,sort_keys=True))
if __name__=='__main__':main()
