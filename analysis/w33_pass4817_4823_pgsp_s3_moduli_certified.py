#!/usr/bin/env python3
"""Passes 4817 and 4823 — certified induced PGSp modules on S3 moduli.

This verifier deliberately avoids enumerating the astronomical full orbit sets.
It builds the exact induced generator matrices on:

  (a) the 64-dimensional F2 sign-cohomology quotient of the triangle-filled
      GQ(4,2) point graph; and
  (b) the 225-dimensional sign-twisted F3 quotient C1/im(d_tw).

It computes PSp/PGSp fixed and coinvariant dimensions, verifies that the selected
binary sign sector is fixed by the full group, and follows the selected A3
exponent class in the twisted quotient.  Since PSp(4,3) is perfect, a PSp-stable
projective F3 line is fixed vectorwise; if the PSp fixed space is one-dimensional
this gives an exact unique global signature for the selected S3 connection.
"""
from __future__ import annotations
import itertools,json
from collections import deque
from pathlib import Path
import numpy as np
from w33_pass4756_4758_4760_dependency_cube_reconstruction import build_all
from w33_pass4716_selected270_bundle_connection import build_bundle,compose
from w33_pass4721_4724_support12_involution_square_root_cover import build_groups
ROOT=Path(__file__).resolve().parents[1]
OUT17=ROOT/'data/PART_W33_PASS4817_PGSP_S3_MODULI_MODULE.json'
OUT23=ROOT/'data/PART_W33_PASS4823_SELECTED_CONNECTION_INVARIANT_LINE.json'

def pmask(m,p):
    y=0;x=int(m)
    while x:
        b=x&-x;i=b.bit_length()-1;x^=b;y|=1<<p[i]
    return y

def parity(p):return sum(p[i]>p[j] for i in range(3) for j in range(i+1,3))&1

def rank2(vals):
    piv={}
    for x in vals:
        y=int(x)
        while y:
            p=y.bit_length()-1
            if p in piv:y^=piv[p]
            else:piv[p]=y;break
    return len(piv)

def basis2(vals):
    piv={};out=[]
    for x in vals:
        y=int(x)
        while y:
            p=y.bit_length()-1
            if p in piv:y^=piv[p]
            else:piv[p]=y;out.append(y);break
    return out

def null2(rows,n):
    R=[int(x) for x in rows if x];rr=0;pivs=[]
    for col in reversed(range(n)):
        q=next((i for i in range(rr,len(R)) if (R[i]>>col)&1),None)
        if q is None:continue
        R[rr],R[q]=R[q],R[rr]
        for i in range(len(R)):
            if i!=rr and ((R[i]>>col)&1):R[i]^=R[rr]
        pivs.append(col);rr+=1
    R=R[:rr];free=[c for c in range(n) if c not in set(pivs)];out=[]
    for f in free:
        x=1<<f
        for row,p in zip(R,pivs):
            if (row&x).bit_count()&1:x|=1<<p
        assert all(not ((r&x).bit_count()&1) for r in rows);out.append(x)
    return out

def extend2(B,S):
    B=list(B);r=rank2(B)
    for x in S:
        if rank2(B+[x])>r:B.append(x);r+=1
    return B

def solver2(B):
    piv={}
    for i,b in enumerate(B):
        y=int(b);c=1<<i
        while y:
            p=y.bit_length()-1
            if p in piv:y^=piv[p][0];c^=piv[p][1]
            else:piv[p]=(y,c);break
        assert y
    def sol(x):
        y=int(x);c=0
        while y:
            p=y.bit_length()-1
            if p not in piv:return None
            y^=piv[p][0];c^=piv[p][1]
        return c
    return sol

def rows_from_cols(cols,n):
    rows=[0]*n
    for j,c in enumerate(cols):
        y=int(c)
        while y:
            b=y&-y;i=b.bit_length()-1;y^=b;rows[i]|=1<<j
    return rows

def rrefp(A,p=3):
    A=np.array(A,dtype=np.int64)%p;r=0;piv=[]
    for c in range(A.shape[1]):
        q=next((i for i in range(r,A.shape[0]) if A[i,c]),None)
        if q is None:continue
        A[[r,q]]=A[[q,r]];A[r]=(A[r]*pow(int(A[r,c]),-1,p))%p
        for i in range(A.shape[0]):
            if i!=r and A[i,c]:A[i]=(A[i]-A[i,c]*A[r])%p
        piv.append(c);r+=1
    return A,piv

def rankp(A,p=3):return len(rrefp(A,p)[1])

def extendp(B,S,p=3):
    B=[np.array(x,dtype=np.int64)%p for x in B];r=rankp(np.array(B),p) if B else 0
    for x in S:
        x=np.array(x,dtype=np.int64)%p;nr=rankp(np.array(B+[x]),p)
        if nr>r:B.append(x);r=nr
    return B

def inverse_mod(M,p=3):
    M=np.array(M,dtype=np.int64)%p;n=M.shape[0];assert M.shape==(n,n)
    A=np.concatenate([M,np.eye(n,dtype=np.int64)],axis=1)%p;r=0
    for c in range(n):
        q=next(i for i in range(r,n) if A[i,c]);A[[r,q]]=A[[q,r]]
        A[r]=(A[r]*pow(int(A[r,c]),-1,p))%p
        for i in range(n):
            if i!=r and A[i,c]:A[i]=(A[i]-A[i,c]*A[r])%p
        r+=1
    assert np.array_equal(A[:,:n],np.eye(n,dtype=np.int64));return A[:,n:]%p

def main():
    D0=build_all();X=build_bundle();pts=D0['pts'];lines=D0['lines'];sing=D0['selected135'];packets=X['packets'];G45=X['G45'];sig=X['sig']
    pidx={p:i for i,p in enumerate(pts)};pgens,PSp,full=build_groups(pts,pidx,lines);assert len(PSp)==25920 and len(full)==51840
    outer=next(g for g in full if g not in PSp);fullgens=list(pgens)+[outer]
    all40=(1<<40)-1;rep=lambda x:min(int(x),int(x)^all40);sidx={int(x):i for i,x in enumerate(sing)};packet_of={s:p for p,T in enumerate(packets) for s in T}
    def packet_perm(g):
        sp=[sidx[rep(pmask(sing[i],g))] for i in range(135)];q=[]
        for T in packets:
            z={packet_of[sp[s]] for s in T};assert len(z)==1;q.append(next(iter(z)))
        assert len(set(q))==45;return tuple(q)
    perms=[packet_perm(g) for g in fullgens]
    edges=sorted(tuple(sorted(e)) for e in G45.edges());ei={e:i for i,e in enumerate(edges)};assert len(edges)==270
    tris=sorted(set(tuple(sorted(t)) for t in X['projected']));assert len(tris)==270
    trows=[]
    for T in tris:
        m=0
        for e in itertools.combinations(T,2):m^=1<<ei[tuple(sorted(e))]
        trows.append(m)
    Z=null2(trows,270);assert len(Z)==108
    cuts=[sum(1<<ei[tuple(sorted((v,w)))] for w in G45[v]) for v in range(45)]
    Bb=basis2(cuts);assert len(Bb)==44;BZ=extend2(Bb,Z);assert len(BZ)==108;Hbasis=BZ[44:];sol=solver2(BZ)
    def edgeact(x,p):
        y=0
        while x:
            b=x&-x;j=b.bit_length()-1;x^=b;u,v=edges[j];y^=1<<ei[tuple(sorted((p[u],p[v])))]
        return y
    H2=[]
    for p in perms:
        cols=[]
        for b in Hbasis:
            c=sol(edgeact(b,p));assert c is not None;cols.append((c>>44)&((1<<64)-1))
        H2.append(cols)
    def fixed_dim(gens):
        eq=[]
        for M in gens:
            rows=rows_from_cols(M,64);eq += [rows[i]^(1<<i) for i in range(64)]
        return 64-rank2(eq)
    def coin_dim(gens):return 64-rank2([M[j]^(1<<j) for M in gens for j in range(64)])
    pfix,pcoin=fixed_dim(H2[:len(pgens)]),coin_dim(H2[:len(pgens)])
    qfix,qcoin=fixed_dim(H2),coin_dim(H2)

    # Twisted F3 quotient C1/im(d_tw).
    psign=np.array([parity(sig[e]) for e in edges],dtype=np.int64)
    Dt=np.zeros((270,45),dtype=np.int64)
    for r,(u,v) in enumerate(edges):Dt[r,v]=1;Dt[r,u]=(-1 if psign[r]==0 else 1)%3
    assert rankp(Dt,3)==45
    Db=[Dt[:,j] for j in range(45)];std=[np.eye(270,dtype=np.int64)[:,j] for j in range(270)]
    BF=extendp(Db,std,3);assert len(BF)==270;Mbas=np.column_stack(BF)%3;Minv=inverse_mod(Mbas,3);Qbasis=BF[45:]
    coord=lambda x:(Minv@np.asarray(x,dtype=np.int64))%3
    r3=(1,2,0);s3=(1,0,2);ID=(0,1,2);rp=[ID,r3,compose(r3,r3)]
    tab={(a,p):compose(rp[a],s3 if p else ID) for a in range(3) for p in range(2)};invtab={v:k for k,v in tab.items()};assert len(invtab)==6
    avec=np.array([invtab[sig[e]][0] for e in edges],dtype=np.int64);aclass=coord(avec)[45:]%3;assert np.any(aclass)
    H3=[];scalars=[]
    for p in perms:
        pnew=np.zeros(270,dtype=np.int64)
        for j,(u,v) in enumerate(edges):pnew[ei[tuple(sorted((p[u],p[v])))]]=psign[j]
        q=[None]*45;q[0]=0;Q=deque([0])
        while Q:
            u=Q.popleft()
            for v in sorted(G45[u]):
                if q[v] is None:
                    k=ei[tuple(sorted((u,v)))];q[v]=(q[u]+int(pnew[k])+int(psign[k]))&1;Q.append(v)
        assert all(z is not None for z in q)
        def T1(x):
            y=np.zeros(270,dtype=np.int64)
            for j,val in enumerate(np.asarray(x,dtype=np.int64)%3):
                if not val:continue
                u,v=edges[j];fu,fv=p[u],p[v];k=ei[tuple(sorted((fu,fv)))];co=-1 if q[fv] else 1
                if fu>fv:co*=(-1 if psign[k]==0 else 1)
                y[k]=(y[k]+co*int(val))%3
            return y
        for d in Db:assert not np.any(coord(T1(d))[45:])
        cols=[coord(T1(b))[45:]%3 for b in Qbasis];M=np.column_stack(cols)%3;H3.append(M)
        z=(M@aclass)%3
        if np.array_equal(z,aclass):scalars.append(1)
        elif np.array_equal(z,(-aclass)%3):scalars.append(2)
        else:scalars.append(0)
    assert all(scalars)
    I=np.eye(225,dtype=np.int64)
    pfix3=225-rankp(np.vstack([(M-I)%3 for M in H3[:len(pgens)]]),3)
    qfix3=225-rankp(np.vstack([(M-I)%3 for M in H3]),3)
    assert all(s==1 for s in scalars[:len(pgens)])  # PSp perfect: selected projective line is vectorwise fixed.
    unique=(pfix3==1)
    out17={'pass':4817,'sign_cohomology':{'field':'F2','dimension':64,'PSp_fixed_dimension':pfix,'PSp_coinvariant_dimension':pcoin,'PGSp_fixed_dimension':qfix,'PGSp_coinvariant_dimension':qcoin},
      'selected_sign_sector':{'PSp_fixed':True,'PGSp_fixed':True,'PGSp_stabilizer_order':51840},
      'twisted_deformation':{'field':'F3','dimension':225,'PSp_fixed_dimension':pfix3,'PGSp_fixed_dimension':qfix3,'selected_projective_line_PGSp_stable':True,'outer_scalar':int(scalars[-1])},
      'orbit_boundary':'The induced generator modules are exact, but the complete orbit census on all 2^64 sign sectors and all points of PG(224,3) is not enumerated.',
      'theorem':'The full PSp/PGSp generator actions on both finite deformation modules are explicit. The selected binary sign sector is fixed by PGSp and the selected A3 class spans a PGSp-stable projective line in twisted H1(F3).',
      'boundary':'Exact finite module/stabilizer theorem; global astronomical orbit enumeration remains open.'}
    OUT17.write_text(json.dumps(out17,indent=2,sort_keys=True)+'\n')
    out23={'pass':4823,'PSp_fixed_dimension_in_twisted_H1':pfix3,'PGSp_fixed_dimension_in_twisted_H1':qfix3,'selected_outer_scalar':int(scalars[-1]),'unique_PSp_invariant_line':unique,
      'theorem':('The selected S3 connection is singled out by the unique PSp-fixed line in the 225-dimensional twisted F3 deformation module.' if unique else 'The selected A3 class is PSp-fixed, but the PSp fixed space has dimension greater than one; this line alone does not uniquely select the connection.'),
      'boundary':'Finite cohomology orbit signature only; no continuum gauge interpretation.'}
    OUT23.write_text(json.dumps(out23,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'4817':out17,'4823':out23},indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
