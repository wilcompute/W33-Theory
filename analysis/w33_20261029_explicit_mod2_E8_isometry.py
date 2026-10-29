#!/usr/bin/env python3
"""Explicit finite orthogonal-space map from W(3,3) adjacency logicals
to E8/2E8 in a simple-root basis. A basis choice is required: no canonical
pointwise/8-label map is claimed. Tests chosen symplectic transvections.
"""
from __future__ import annotations
from itertools import combinations
import json
from pathlib import Path
from w33_incidence_even_line_resolution_20261029 import make_geometry, rank_basis, add
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"w33_20261029_explicit_mod2_E8_isometry.json"
EDGES=[(0,1),(1,2),(2,3),(3,4),(4,5),(5,6),(2,7)]

def qE(x):
    return ((x.bit_count()+sum(((x>>i)&1)*((x>>j)&1) for i,j in EDGES))&1)
def qW(x):
    assert x.bit_count()%2==0
    return (x.bit_count()//2)&1
def polar(x,y,q):return q(x^y)^q(x)^q(y)
def independent_basis(vectors):
    chosen=[];b={}
    for x in vectors:
        if add(x,b):chosen.append(x)
    return chosen
def all_span(vs):
    x=[0]
    for v in vs:x.extend([u^v for u in x[:]])
    return x
def hyperbolic(vs,q):
    remaining=list(vs)
    pairs=[]
    while remaining:
        space=all_span(remaining)
        e=next(x for x in space if x and not q(x))
        f=next(x for x in space if polar(e,x,q)==1 and not q(x))
        pairs.append((e,f))
        projected=[x ^ (e if polar(x,f,q) else 0)
                   ^ (f if polar(x,e,q) else 0) for x in remaining]
        remaining=independent_basis([x for x in projected if x])
        assert len(remaining)==len(vs)-2*len(pairs)
    basis=[z for pair in pairs for z in pair]
    assert len(basis)==8
    for i in range(8):
        assert q(basis[i])==0
        for j in range(8):
            assert polar(basis[i],basis[j],q)==(int(i//2==j//2 and i!=j))
    return basis

def coordinate_decoder(stabilizers,basis):
    d={pivot:(row,0) for pivot,row in rank_basis(stabilizers).items()}
    for i,z in enumerate(basis):
        x=z; c=1<<i
        while x:
            j=x.bit_length()-1
            if j in d:
                row,label=d[j];x^=row;c^=label
            else:
                d[j]=(x,c);break
        else:raise AssertionError("dependent basis")
    def coords(x):
        c=0
        while x:
            j=x.bit_length()-1
            if j not in d:raise ValueError("not in span")
            row,label=d[j];x^=row;c^=label
        return c
    return coords

def matmul_col(columns,x):
    return __import__("functools").reduce(lambda a,j:a^columns[j],
                                  (j for j in range(len(columns)) if (x>>j)&1),0)
def make_e8_roots():
    neighbors={i:[] for i in range(8)}
    for i,j in EDGES:neighbors[i].append(j);neighbors[j].append(i)
    roots=set()
    for k in range(8):
        u=tuple(int(i==k) for i in range(8))
        roots.add(u);roots.add(tuple(-z for z in u))
    queue=list(roots);j=0
    while j<len(queue):
        x=queue[j];j+=1
        for k in range(8):
            d=2*x[k]-sum(x[n] for n in neighbors[k])
            y=list(x);y[k]-=d;y=tuple(y)
            if y not in roots:
                roots.add(y);queue.append(y)
        assert len(roots)<=240
    assert len(roots)==240
    residues={sum((x[i]%2)<<i for i in range(8)) for x in roots}
    assert len(residues)==120 and all(qE(x)==1 for x in residues)
    return roots,residues
def main():
    points,lines,lm,A,N,norm,omega=make_geometry(3)
    stabilizers=rank_basis(A)
    selected=[]
    full=stabilizers.copy()
    for z in [lm[0]^w for w in lm[1:]]:
        if add(z,full):selected.append(z)
    assert len(selected)==8
    hW=hyperbolic(selected,qW)
    hE=hyperbolic([1<<i for i in range(8)],qE)
    coordW=coordinate_decoder(A,hW)
    coordE=coordinate_decoder([],hE)
    def toE(x):
        c=coordW(x)
        return matmul_col(hE,c)
    assert len({toE(x) for x in all_span(hW)})==256
    assert all(qW(x)==qE(toE(x)) for x in all_span(hW))
    roots,root_residues=make_e8_roots()
    nonzero_classes={toE(x) for x in all_span(hW) if qW(x)}
    assert nonzero_classes==root_residues
    I={x:i for i,x in enumerate(points)}
    us=[(1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1),
        (1,0,1,0),(0,1,0,1),(1,0,0,1)]
    matrices=[]
    permutation_gens=[]
    matrix_gens=[]
    for u in us:
        permutation=[I[norm(tuple((x[k]+omega(x,u)*u[k])%3 for k in range(4)))]
                     for x in points]
        assert len(set(permutation))==40
        assert all(((A[i]>>j)&1)==((A[permutation[i]]>>permutation[j])&1)
                   for i in range(40) for j in range(40))
        def permute(mask):
            y=0
            while mask:
                t=mask & -mask
                y^=1<<permutation[t.bit_length()-1]
                mask^=t
            return y
        Wcolumns=[coordW(permute(x)) for x in hW]
        assert len(set(matmul_col(Wcolumns,x) for x in range(256)))==256
        # E8 columns = finite induced action conjugated by the explicit isometry.
        Ecolumns=[]
        for bit in range(8):
            c=coordE(1<<bit)
            Ecolumns.append(matmul_col(hE,matmul_col(Wcolumns,c)))
        assert all(qE(matmul_col(Ecolumns,x))==qE(x) for x in range(256))
        matrices.append({"transvection_u":list(u),"E8_simple_root_mod2_columns":Ecolumns,
                         "logical_hyperbolic_columns":Wcolumns})
        permutation_gens.append(tuple(permutation))
        matrix_gens.append(tuple(Ecolumns))
    # Entire 25,920-element projective symplectic group, not just seven checks.
    from collections import deque
    id_perm=tuple(range(40))
    id_mat=tuple(1<<i for i in range(8))
    seen={id_perm:id_mat}
    pending=deque([id_perm])
    while pending:
        cur=pending.popleft()
        mat=seen[cur]
        for g,gm in zip(permutation_gens,matrix_gens):
            new_perm=tuple(g[j] for j in cur)
            new_mat=tuple(matmul_col(gm,z) for z in mat)
            if new_perm in seen:
                assert seen[new_perm]==new_mat
            else:
                seen[new_perm]=new_mat
                pending.append(new_perm)
    assert len(seen)==25920
    assert len(set(seen.values()))==25920
    out={"scope":"explicit noncanonical finite quadratic-space isometry; not integral lattice or dynamical equivariance",
         "W33_logical_hyperbolic_representatives":hW,
         "E8_simple_root_hyperbolic_representatives":hE,
         "E8_Dynkin_edges":EDGES,"roots":len(roots),"root_mod2_antipodal_classes":len(root_residues),
         "nonzero_classes_q1":len(nonzero_classes),"checked_group_generators":matrices,
         "complete_group_order":len(seen),"faithful_mod2_action_order":len(set(seen.values())),
         "all_256_q_values_match":True}
    OUT.write_text(json.dumps(out,indent=2)+"\n",encoding="utf8")
    print("PASS: 256-class exact W33->E8/2E8 quadratic isometry; 120 root pairs;",len(matrices),"transvection generators")
if __name__=="__main__":main()
