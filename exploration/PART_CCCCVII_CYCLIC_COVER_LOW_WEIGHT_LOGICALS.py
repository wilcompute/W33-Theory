#!/usr/bin/env python3
"""PART CCCCVII -- Cyclic Cover Low-Weight Logical Audit.

CCCCVI built valid triangle-flat cyclic covers for L=2,3.  This part answers
the next hardware question:

    did the native cover actually raise CSS distance?

Result: no.  The covers preserve local checks and commute, but they inherit
weight-3 X-logical witnesses from the W33 K4 line-star structure.  Therefore the
full CSS distance remains 3 for these simple covers.

Architecture consequence:
    cyclic covers alone are not enough.  To raise distance natively, the next
    layer must kill/gauge-fix the line-star X logicals, or use a cover voltage
    constrained specifically to destroy those inherited supports.
"""
from __future__ import annotations
import itertools, json
from pathlib import Path
from typing import Tuple
ROOT=Path(__file__).resolve().parents[1]
MOD=3
Vector=Tuple[int,int,int,int]

def ok(name, cond, value=None): return {"name":name,"passed":bool(cond),"value":value}
def mul(a,u): return tuple((a*u[i])%MOD for i in range(4))
def omega(x,y): return (x[0]*y[2]-x[2]*y[0]+x[1]*y[3]-x[3]*y[1])%MOD
def canon(v):
    for a in v:
        if a%MOD: return mul(1 if a==1 else 2,v)
    raise ValueError('zero')
def points():
    pts=[]; seen=set()
    for v in itertools.product(range(MOD), repeat=4):
        if v==(0,0,0,0): continue
        c=canon(v)
        if c not in seen: seen.add(c); pts.append(c)
    return pts
def build_graph():
    pts=points(); adj=[set() for _ in pts]
    for i,j in itertools.combinations(range(len(pts)),2):
        if omega(pts[i],pts[j])==0: adj[i].add(j); adj[j].add(i)
    return pts,adj
def edges(adj): return [(i,j) for i in range(len(adj)) for j in sorted(adj[i]) if i<j]
def triangles(adj): return [(i,j,k) for i,j,k in itertools.combinations(range(len(adj)),3) if j in adj[i] and k in adj[i] and k in adj[j]]
def bit(indices):
    x=0
    for i in indices: x ^= (1<<i)
    return x
def gf2_basis(rows):
    basis={}
    for r in rows:
        x=r
        while x:
            p=x.bit_length()-1
            if p not in basis:
                basis[p]=x; break
            x ^= basis[p]
    return basis
def reduce_by_basis(x,basis):
    y=x
    while y:
        p=y.bit_length()-1
        if p not in basis: return y
        y ^= basis[p]
    return 0
def in_kernel(rows,vec): return all(((r&vec).bit_count()%2)==0 for r in rows)

def rref_mod_rows(rows,ncols,p):
    A=[row[:] for row in rows]; r=0; piv=[]
    for c in range(ncols):
        pivrow=None
        for i in range(r,len(A)):
            if A[i][c]%p: pivrow=i; break
        if pivrow is None: continue
        A[r],A[pivrow]=A[pivrow],A[r]
        inv=pow(A[r][c]%p,p-2,p); A[r]=[(x*inv)%p for x in A[r]]
        for i in range(len(A)):
            if i!=r and A[i][c]%p:
                f=A[i][c]%p; A[i]=[(A[i][j]-f*A[r][j])%p for j in range(ncols)]
        piv.append(c); r+=1
    return A[:r],piv
def nullspace_mod(rows,ncols,p):
    rref,pivots=rref_mod_rows(rows,ncols,p); pivset=set(pivots); free=[c for c in range(ncols) if c not in pivset]; basis=[]
    for f in free:
        x=[0]*ncols; x[f]=1
        for row,piv in zip(rref,pivots): x[piv]=(-row[f])%p
        basis.append(x)
    return basis,pivots
def reduce_vec_mod(vec,basis,pivots,p):
    x=vec[:]
    for row,piv in zip(basis,pivots):
        if x[piv]%p:
            f=x[piv]%p; x=[(x[j]-f*row[j])%p for j in range(len(x))]
    return x
def triangle_matrix(adj,E,T,p):
    eidx={e:i for i,e in enumerate(E)}; rows=[]
    for i,j,k in T:
        row=[0]*len(E); row[eidx[(i,j)]]=(row[eidx[(i,j)]]+1)%p; row[eidx[(j,k)]]=(row[eidx[(j,k)]]+1)%p; row[eidx[(i,k)]]=(row[eidx[(i,k)]]-1)%p; rows.append(row)
    return rows
def coboundary_rows(adj,E,p):
    rows=[]
    for v in range(len(adj)):
        row=[0]*len(E)
        for ei,(a,b) in enumerate(E):
            if v==a: row[ei]=(row[ei]-1)%p
            elif v==b: row[ei]=(row[ei]+1)%p
        rows.append(row)
    return rows
def choose_voltage(adj,p):
    E=edges(adj); T=triangles(adj); ns,_=nullspace_mod(triangle_matrix(adj,E,T,p),len(E),p); cob,piv=rref_mod_rows(coboundary_rows(adj,E,p),len(E),p)
    for vec in ns:
        if any(vec) and any(reduce_vec_mod(vec,cob,piv,p)): return vec
    return ns[0] if ns else [0]*len(E)

def build_lifted_css(L):
    pts,adj=build_graph(); E=edges(adj); T=triangles(adj); eidx={e:i for i,e in enumerate(E)}; g=choose_voltage(adj,L); n=len(E)*L
    def q(ei,t): return ei*L+(t%L)
    Hx=[]
    for v in range(len(adj)):
        for t in range(L):
            inds=[]
            for w in sorted(adj[v]):
                e=tuple(sorted((v,w))); ei=eidx[e]; ge=g[ei]
                inds.append(q(ei,t if v==e[0] else t-ge))
            Hx.append(bit(inds))
    Hz=[]
    for i,j,k in T:
        eij=eidx[(i,j)]; ejk=eidx[(j,k)]; eik=eidx[(i,k)]
        for t in range(L): Hz.append(bit([q(eij,t),q(ejk,t+g[eij]),q(eik,t)]))
    return {"L":L,"n":n,"adj":adj,"E":E,"T":T,"eidx":eidx,"voltage":g,"Hx":Hx,"Hz":Hz}

def no_weight_1_2_logicals(kernel_rows,stab_basis,n):
    for w in (1,2):
        for comb in itertools.combinations(range(n),w):
            v=bit(comb)
            if in_kernel(kernel_rows,v) and reduce_by_basis(v,stab_basis)!=0:
                return False,{"weight":w,"witness":comb}
    return True,None

def find_weight3_x_logical(c):
    adj,E,eidx,L,Hx,Hz=c['adj'],c['E'],c['eidx'],c['L'],c['Hx'],c['Hz']; bx=gf2_basis(Hx)
    # Search K4 line-star patterns: triples of edges incident at the same vertex whose other endpoints form a triangle.
    for v in range(len(adj)):
        nbs=sorted(adj[v])
        for a,b,d in itertools.combinations(nbs,3):
            if b in adj[a] and d in adj[a] and d in adj[b]:
                base_edges=[tuple(sorted((v,a))),tuple(sorted((v,b))),tuple(sorted((v,d)))]
                base_idx=[eidx[e] for e in base_edges]
                for fibers in itertools.product(range(L), repeat=3):
                    q=[base_idx[i]*L+fibers[i] for i in range(3)]
                    x=bit(q)
                    if in_kernel(Hz,x) and reduce_by_basis(x,bx)!=0:
                        return {"found":True,"weight":3,"vertex":v,"other_vertices":[a,b,d],"base_edges":base_edges,"fibers":fibers,"qubits":q}
    return {"found":False}

def audit_cover(L):
    c=build_lifted_css(L); bx=gf2_basis(c['Hx']); bz=gf2_basis(c['Hz']); k=c['n']-len(bx)-len(bz)
    nox,wx=no_weight_1_2_logicals(c['Hz'],bx,c['n'])
    noz,wz=no_weight_1_2_logicals(c['Hx'],bz,c['n'])
    x3=find_weight3_x_logical(c)
    return {"L":L,"n":c['n'],"rank_X":len(bx),"rank_Z":len(bz),"k":k,"no_X_logicals_weight_1_2":nox,"no_Z_logicals_weight_1_2":noz,"x_weight3_logical":x3,"distance_conclusion":"d=3 because d_X=3" if nox and noz and x3.get('found') else "inconclusive"}

def build_results():
    a2=audit_cover(2); a3=audit_cover(3); checks=[]
    checks.append(ok('L=2 cover audit has n=480',a2['n']==480,a2))
    checks.append(ok('L=3 cover audit has n=720',a3['n']==720,a3))
    checks.append(ok('L=2 no weight 1/2 X logicals',a2['no_X_logicals_weight_1_2'] is True,a2))
    checks.append(ok('L=3 no weight 1/2 X logicals',a3['no_X_logicals_weight_1_2'] is True,a3))
    checks.append(ok('L=2 no weight 1/2 Z logicals',a2['no_Z_logicals_weight_1_2'] is True,a2))
    checks.append(ok('L=3 no weight 1/2 Z logicals',a3['no_Z_logicals_weight_1_2'] is True,a3))
    checks.append(ok('L=2 has weight-3 X logical',a2['x_weight3_logical'].get('found') is True,a2['x_weight3_logical']))
    checks.append(ok('L=3 has weight-3 X logical',a3['x_weight3_logical'].get('found') is True,a3['x_weight3_logical']))
    verified=all(c['passed'] for c in checks)
    return {"part":"CCCCVII","title":"Cyclic Cover Low-Weight Logical Audit","verified":verified,"checks_total":len(checks),"checks_passed":sum(c['passed'] for c in checks),"cover_audits":{"L2":a2,"L3":a3},"architecture_upgrade":"Shows that the valid triangle-flat cyclic covers do not by themselves raise CSS distance: inherited K4 line-star weight-3 X logicals survive for L=2 and L=3.","theorem":"For the tested triangle-flat non-coboundary cyclic covers, no weight-1 or weight-2 logicals exist, but weight-3 X logicals do exist. Therefore the full CSS distance remains d=3 for L=2 and L=3.","honesty_boundary":"This audits deterministic covers selected by the solver. It does not prove all possible cyclic voltage covers have distance 3; it proves these natural triangle-flat covers do.","checks":checks}

def main():
    r=build_results(); out=ROOT/'PART_CCCCVII_cyclic_cover_low_weight_logicals_results.json'; out.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n',encoding='utf-8'); print(json.dumps({"part":r['part'],"verified":r['verified'],"checks_passed":r['checks_passed'],"checks_total":r['checks_total'],"out_path":str(out)},indent=2))
if __name__=='__main__': main()
