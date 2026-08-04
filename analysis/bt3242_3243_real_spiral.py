#!/usr/bin/env python3
from __future__ import annotations
import collections, itertools
import numpy as np
import sympy as sp

def mat_order_mod(M,p,limit=10000):
    I=np.eye(M.shape[0],dtype=int)%p; X=I.copy()
    for n in range(1,limit+1):
        X=(X@(M%p))%p
        if np.array_equal(X,I):return n
    return None

def matrix_group(gens,p):
    I=np.eye(gens[0].shape[0],dtype=int)%p
    key=lambda A:tuple(map(int,A.flatten()))
    out=[I]; seen={key(I)}; q=collections.deque([I])
    while q:
        g=q.popleft()
        for s in gens:
            z=(s@g)%p; k=key(z)
            if k not in seen:seen.add(k);out.append(z);q.append(z)
    return out

def spiral_controller():
    R=sp.Matrix([[0,-1,-1,0],[1,0,0,0],[1,0,0,-1],[0,0,1,0]])
    S=sp.Matrix([[0,1,0,0],[1,0,0,0],[0,0,0,1],[0,0,1,0]])
    G=sp.Matrix([[-2,0,0,-1],[0,-2,-1,0],[0,-1,2,0],[-1,0,0,2]])
    W0=sp.Matrix([[0,-1,0,0],[1,0,0,0],[0,0,0,1],[0,0,-1,0]])
    W1=sp.Matrix([[0,0,0,-1],[0,0,1,0],[0,-1,0,0],[1,0,0,0]])
    K=W0.inv()*W1
    checks={
      "det_one":R.det()==1,
      "reciprocal_charpoly":sp.factor(R.charpoly().as_expr())==sp.Symbol("lambda")**4+3*sp.Symbol("lambda")**2+1,
      "split_metric":R.T*G*R==G,
      "metric_signature":G.eigenvals()=={-sp.sqrt(5):2,sp.sqrt(5):2},
      "two_symplectic_forms":R.T*W0*R==W0 and R.T*W1*R==W1 and W0.det()==W1.det()==1,
      "complex_structure":K*K==-sp.eye(4) and R*K==K*R,
      "reversing_involution":S*S==sp.eye(4) and S*R*S==R.inv()
    }
    assert all(checks.values()),[k for k,v in checks.items() if not v]
    R2=np.array(R.tolist(),dtype=int)%2; S2=np.array(S.tolist(),dtype=int)%2
    A=(R2@R2)%2
    G12=matrix_group([R2,S2],2); G6=matrix_group([A,S2],2)
    assert len(G12)==12 and len(G6)==6 and mat_order_mod(R2,2)==6 and mat_order_mod(A,2)==3
    vectors=[np.array(v,dtype=int) for v in itertools.product(range(2),repeat=4)]
    subspaces=set()
    for u,v in itertools.combinations(vectors[1:],2):
        U=frozenset(tuple(map(int,x)) for x in (np.zeros(4,dtype=int),u,v,(u+v)%2))
        if len(U)==4:subspaces.add(U)
    invariant=[]
    for U in subspaces:
        if all(frozenset(tuple(map(int,(g@np.array(x))%2)) for x in U)==U for g in G6):
            invariant.append(U)
    assert len(invariant)==3
    U=sorted(invariant,key=lambda x:sorted(x))[0]; nz=sorted(x for x in U if any(x))
    elements=[]; perms=set()
    for k in range(3):
        Ak=np.linalg.matrix_power(A,k)%2
        elements.append((f"r{k}",Ak))
    for k in range(3):
        Ak=np.linalg.matrix_power(A,k)%2
        elements.append((f"sr{k}",(S2@Ak)%2))
    table=[]
    for label,M in elements:
        perm=tuple(nz.index(tuple(map(int,(M@np.array(x))%2))) for x in nz); perms.add(perm)
        table.append({"label":label,"permutation":list(perm),"matrix_rows":["".join(map(str,row)) for row in M.tolist()]})
    assert len(perms)==6
    return {
      "real_matrix":R.tolist(),
      "state_recurrence":["x0'=-x1-y0","x1'=x0","y0'=x0-y1","y1'=y0"],
      "characteristic_polynomial":"t^4+3t^2+1",
      "determinant":1,
      "split_metric":G.tolist(),"split_metric_signature":[2,2],"split_metric_determinant":int(G.det()),
      "invariant_symplectic_forms":[W0.tolist(),W1.tolist()],
      "commuting_complex_structure":K.tolist(),
      "reverser":S.tolist(),"infinite_group":"<R,S> is an infinite dihedral representation with S R S = R^-1",
      "finite_orders":{"mod2":mat_order_mod(np.array(R.tolist(),dtype=int),2),
                       "mod3":mat_order_mod(np.array(R.tolist(),dtype=int),3),
                       "mod5":mat_order_mod(np.array(R.tolist(),dtype=int),5),
                       "mod7":mat_order_mod(np.array(R.tolist(),dtype=int),7)},
      "mod2_dihedral_group_order":len(G12),
      "mod2_even_rotation_reflection_group_order":len(G6),
      "mod2_even_subgroup_is_S3":True,
      "invariant_binary_two_planes":len(invariant),
      "selected_plane_nonzero_vectors":[list(x) for x in nz],
      "six_matching_compiler_table":table,
      "bridge":"The six K3,3 matchings can be represented faithfully by <R^2,S> mod 2 acting on the three nonzero vectors of an invariant F2^2 plane."
    }
