#!/usr/bin/env python3
"""Pass 4594 -- the W33 outer similitude canonically selects one U6 factor.

Pass4583 found three PSp-invariant six-spaces in K27/K15 ~= U6+U6.  Here the
full commutant and the PGSp outer action are computed.  The PSp commutant has
16 elements and six units; those units realize all S3 permutations of the three
six-spaces, so no factor is canonical under PSp alone.  The actual W33 outer
similitude acts on the three as one fixed point plus a transposition.  Its unique
fixed six-space extends the inner image 25920 to an outer image 51840.
"""
from __future__ import annotations
import itertools,json
from pathlib import Path
import numpy as np
import w33_pass4583_wedge2_exceptional_six_bridge as p
from w33_pass4472_4479_apartment_module_thermo_ihara_pauli import build_geometry,build_line_perm,transvection_matrix

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4594_OUTER_CANONICAL_U6_FACTOR.json'

def rank2(A):
    A=np.asarray(A,dtype=np.uint8).copy();r=0
    for c in range(A.shape[1]):
        z=np.flatnonzero(A[r:,c])
        if not len(z):continue
        k=r+int(z[0]);A[[r,k]]=A[[k,r]]
        for i in np.flatnonzero(A[:,c]):
            if i!=r:A[i]^=A[r]
        r+=1
        if r==A.shape[0]:break
    return r

def nullspace(A):
    A=np.asarray(A,dtype=np.uint8).copy();m,n=A.shape;r=0;piv=[]
    for c in range(n):
        z=np.flatnonzero(A[r:,c])
        if not len(z):continue
        k=r+int(z[0]);A[[r,k]]=A[[k,r]]
        for i in np.flatnonzero(A[:,c]):
            if i!=r:A[i]^=A[r]
        piv.append(c);r+=1
        if r==m:break
    free=[c for c in range(n) if c not in piv];out=[]
    for f in free:
        x=np.zeros(n,dtype=np.uint8);x[f]=1
        for i,c in reversed(list(enumerate(piv))):x[c]=int(np.dot(A[i],x)%2)
        out.append(x)
    return out

def cols_matrix(cols,n):
    M=np.zeros((n,n),dtype=np.uint8)
    for j,c in enumerate(cols):
        for i in range(n):M[i,j]=(int(c)>>i)&1
    return M

def mat_cols(M):return tuple(sum(int(M[i,j])<<i for i in range(M.shape[0]) if M[i,j]) for j in range(M.shape[1]))

def centralizer_basis(gens,n):
    # unknown X[r,c], column-major index r+n*c; equations XG=GX.
    eq=[]
    for Gc in gens:
        G=cols_matrix(Gc,n)
        for r in range(n):
            for c in range(n):
                row=np.zeros(n*n,dtype=np.uint8)
                for k in range(n):
                    if G[k,c]:row[r+n*k]^=1
                    if G[r,k]:row[k+n*c]^=1
                eq.append(row)
    ns=nullspace(np.asarray(eq,dtype=np.uint8));return [v.reshape((n,n),order='F') for v in ns]

def image_subspace(S,cols,n):return p.rref([p.apply(cols,x) for x in S],n)

def main():
    pts,pidx,lines,lidx,_,A,_,_,_=build_geometry();A=np.asarray(A,dtype=np.uint8);j=(1<<40)-1
    cols=[]
    for c in range(40):
        m=0
        for r in np.flatnonzero(A[:,c]):m|=1<<int(r)
        cols.append(m)
    edges=[(i,k) for i in range(40) for k in range(i+1,40) if A[i,k]]
    B9=[j]
    for i,k in edges:
        x=cols[i]^cols[k]
        if p.rank(B9+[x],40)>len(B9):B9.append(x)
        if len(B9)==9:break
    sol9=p.solver(B9);v8=lambda x:sol9(x)>>1
    cand=[build_line_perm(transvection_matrix(v),pts,pidx,lines,lidx) for v in pts]
    pgens=[];G={tuple(range(40))}
    for g in cand:
        if g in G:continue
        pgens.append(g);G=p.perm_group(pgens)
        if len(G)==25920:break
    outerM=np.diag([1,2,1,2])%3; outerp=build_line_perm(outerM,pts,pidx,lines,lidx)
    G8=[[v8(p.pmask(b,g)) for b in B9[1:]] for g in pgens]
    O8=[v8(p.pmask(b,outerp)) for b in B9[1:]]
    # wedge representation and invariant K27/K15 as in Pass4583.
    pairs=[(i,k) for i in range(8) for k in range(i+1,8)];idx={z:i for i,z in enumerate(pairs)}
    def wedge(v,w):
        z=0
        for a,b in pairs:
            if ((((v>>a)&1)&((w>>b)&1))^(((v>>b)&1)&((w>>a)&1))):z|=1<<idx[(a,b)]
        return z
    WG=[[wedge(g[i],g[k]) for i,k in pairs] for g in G8]; WO=[wedge(O8[i],O8[k]) for i,k in pairs]
    spans={}
    for i in range(28):
        S=p.cyclic(1<<i,WG,28);spans.setdefault(len(S),S)
    K16,K27=spans[16],spans[27]
    G16=p.subactions(list(K16),WG,28);S15=None
    for i in range(16):
        S=p.cyclic(1<<i,G16,16)
        if len(S)==15:S15=S;break
    assert S15 is not None
    K15=[p.apply(list(K16),x) for x in S15];B27=p.choose_basis(K15,K27,28)
    Q12=p.quotient_actions(B27,15,WG,28); O12=p.quotient_actions(B27,15,[WO],28)[0]
    sub6=set()
    for x in range(1,1<<12):
        S=p.cyclic(x,Q12,12)
        if len(S)==6:sub6.add(p.rref(S,12))
    six=sorted(sub6);assert len(six)==3
    sidx={S:i for i,S in enumerate(six)}
    op=[]
    for S in six:op.append(sidx[image_subspace(S,O12,12)])
    assert sorted(op)==[0,1,2] and sum(op[i]==i for i in range(3))==1

    CB=centralizer_basis(Q12,12);assert len(CB)==4
    perms=set();units=0
    for m in range(1<<4):
        X=np.zeros((12,12),dtype=np.uint8)
        for i,B in enumerate(CB):
            if (m>>i)&1:X^=B
        if rank2(X)!=12:continue
        units+=1;xc=mat_cols(X);perms.add(tuple(sidx[image_subspace(S,xc,12)] for S in six))
    assert units==6 and len(perms)==6
    fixed=op.index(next(i for i in range(3) if op[i]==i));S=list(six[fixed]);sol=p.solver(S)
    G6=[[sol(p.apply(g,b)) for b in S] for g in Q12]
    O6=[sol(p.apply(O12,b)) for b in S]
    assert len(p.lin_group(G6,6))==25920 and len(p.lin_group(G6+[O6],6))==51840
    out={'pass':4594,'PSp':{'six_submodules':3,'commutant_dimension_F2':4,'commutant_elements':16,'commutant_units':6,
      'unit_action_on_three_submodules':'all six permutations = S3','canonical_factor_under_PSp':False},
      'PGSp_outer':{'permutation_on_three_submodules':op,'cycle_type':'1+2','unique_fixed_factor':fixed,
        'fixed_factor_inner_image_order':25920,'fixed_factor_outer_image_order':51840,'canonical_outer_stable_factor':True},
      'theorem':'The three Pass4583 U6 factors form a projective line for the PSp commutant GL(2,2)=S3; the actual W33 outer similitude fixes exactly one factor and swaps the other two, canonically selecting a PGSp-stable U6 target.',
      'boundary':'The commutant S3 is an internal multiplicity-space symmetry. It is not identified with geometric D4 triality without a separate explicit intertwiner.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
