#!/usr/bin/env python3
"""Passes 4817 and 4823 — full PGSp action on the S3 moduli.

The binary sign deformations are not an opaque 64-bit parameter set: they are
H^1 of the 45-vertex GQ(4,2) point graph with all 270 base triangles filled,
over F2.  We build the exact PGSp action on this 64-dimensional quotient and
use Burnside on its finite image to count PGSp orbits of sign sectors.

For the A3 part, use the selected sign connection as a rank-one F3 local
system.  The deformation module is C1/im(d_tw), dimension 225.  Every PGSp
base automorphism is accompanied by the unique binary vertex gauge (root gauge
fixed) restoring the selected sign representative; this gives an exact signed
edge action and hence a 225-dimensional quotient action.  The selected S3
connection itself supplies an A3 cohomology class.  We test its projective
stabilizer and, crucially, the full PSp-fixed subspace.  If that fixed subspace
is one-dimensional, the selected projective line is the unique PSp-invariant
line and is therefore a genuine global orbit signature missing from the bare
triangle-holonomy rule.
"""
from __future__ import annotations
import itertools,json
from collections import deque
from pathlib import Path
import numpy as np
from w33_pass4756_4758_4760_dependency_cube_reconstruction import build_all
from w33_pass4716_selected270_bundle_connection import build_bundle,compose,invperm
from w33_pass4721_4724_support12_involution_square_root_cover import build_groups
ROOT=Path(__file__).resolve().parents[1]
OUT17=ROOT/'data/PART_W33_PASS4817_PGSP_S3_MODULI_ORBITS.json'
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
    R=[];piv={}
    for x in rows:
        y=int(x)
        while y:
            p=y.bit_length()-1
            if p in piv:y^=piv[p]
            else:piv[p]=y;R.append((p,y));break
    ps={p for p,r in R};free=[c for c in range(n) if c not in ps];out=[]
    # reduce to row-echelon with pivot descending; solve by direct parity.
    RR=sorted(R,reverse=True)
    for f in free:
        x=1<<f
        changed=True
        # Solve pivots from low to high by recomputing equation parity.
        for p,row in sorted(RR,key=lambda z:z[0]):
            if (row&x).bit_count()&1:x^=1<<p
        assert all(not ((r&x).bit_count()&1) for p,r in R)
        out.append(x)
    assert len(out)==n-len(R)
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
    def solve(x):
        y=int(x);c=0
        while y:
            p=y.bit_length()-1
            if p not in piv:return None
            y^=piv[p][0];c^=piv[p][1]
        return c
    return solve

def apply2(cols,x):
    y=0
    while x:
        b=x&-x;i=b.bit_length()-1;x^=b;y^=cols[i]
    return y

def compose2(A,B):return tuple(apply2(A,b) for b in B)

def matgroup2(gens,n):
    I=tuple(1<<i for i in range(n));seen={I};Q=deque([I])
    while Q:
        a=Q.popleft()
        for g in gens:
            c=compose2(g,a)
            if c not in seen:seen.add(c);Q.append(c)
    return seen

def fixed_dim2(M,n):return n-rank2([M[i]^(1<<i) for i in range(n)])

def rrefp(A,p=3):
    A=np.array(A,dtype=np.int64)%p;r=0;piv=[]
    for c in range(A.shape[1]):
        q=next((i for i in range(r,A.shape[0]) if A[i,c]%p),None)
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
        x=np.array(x,dtype=np.int64)%p
        nr=rankp(np.array(B+[x]),p)
        if nr>r:B.append(x);r=nr
    return B

def coordsp(B,p=3):
    M=np.column_stack(B)%p
    R,piv=rrefp(M.T,p)  # rows are basis vectors, pivots are ambient coords
    # Since B is a full basis of ambient space in our use, invert directly modulo p.
    assert M.shape[0]==M.shape[1]
    A=np.concatenate([M.copy(),np.eye(M.shape[0],dtype=np.int64)],axis=1)%p
    n=M.shape[0]
    r=0
    for c in range(n):
        q=next(i for i in range(r,n) if A[i,c])
        A[[r,q]]=A[[q,r]];A[r]=(A[r]*pow(int(A[r,c]),-1,p))%p
        for i in range(n):
            if i!=r and A[i,c]:A[i]=(A[i]-A[i,c]*A[r])%p
        r+=1
    Minv=A[:,n:]
    # M maps coordinate column -> ambient; inverse is Minv.
    return lambda x:(Minv@np.array(x,dtype=np.int64))%p

def main():
    D0=build_all();X=build_bundle();pts=D0['pts'];lines=D0['lines'];sing=D0['selected135'];packets=X['packets'];G45=X['G45'];sig=X['sig']
    pidx={p:i for i,p in enumerate(pts)};pgens,PSp,full=build_groups(pts,pidx,lines);assert len(PSp)==25920 and len(full)==51840
    outer=next(g for g in full if g not in PSp);fullgens=list(pgens)+[outer]
    all40=(1<<40)-1;rep=lambda x:min(int(x),int(x)^all40);sidx={int(x):i for i,x in enumerate(sing)};packet_of={s:p for p,T in enumerate(packets) for s in T}
    def packet_perm(g):
        sp=[sidx[rep(pmask(sing[i],g))] for i in range(135)]
        q=[]
        for T in packets:
            vals={packet_of[sp[s]] for s in T};assert len(vals)==1;q.append(next(iter(vals)))
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
    cuts=[]
    for v in range(45):cuts.append(sum(1<<ei[tuple(sorted((v,w)))] for w in G45[v]))
    Bb=basis2(cuts);assert len(Bb)==44 and all(not any((t&b).bit_count()&1 for t in trows) for b in Bb)
    BZ=extend2(Bb,Z);assert len(BZ)==108;Hbasis=BZ[44:];solZ=solver2(BZ)
    def edgeperm_mask(x,p):
        y=0
        while x:
            b=x&-x;j=b.bit_length()-1;x^=b;u,v=edges[j];e=tuple(sorted((p[u],p[v])));y^=1<<ei[e]
        return y
    H2=[]
    for p in perms:
        cols=[]
        for b in Hbasis:
            c=solZ(edgeperm_mask(b,p));assert c is not None and c>>108==0;cols.append((c>>44)&((1<<64)-1))
        H2.append(tuple(cols))
    pfix=64-rank2([H2[k][j]^(1<<j) for k in range(len(pgens)) for j in range(64)])
    qfix=64-rank2([H2[k][j]^(1<<j) for k in range(len(H2)) for j in range(64)])
    pcoin=64-rank2([H2[k][j]^(1<<j) for k in range(len(pgens)) for j in range(64)])  # rank of augmentation columns; same expression gives coinvariant dim
    qcoin=64-rank2([H2[k][j]^(1<<j) for k in range(len(H2)) for j in range(64)])
    image=matgroup2(H2,64)
    burn=sum(1<<fixed_dim2(M,64) for M in image)
    assert burn%len(image)==0;sign_orbits=burn//len(image)

    # Selected sign representative p_e and twisted coboundary D over F3.
    psign=np.array([parity(sig[e]) for e in edges],dtype=np.int64)
    Dt=np.zeros((270,45),dtype=np.int64)
    for r,(u,v) in enumerate(edges):Dt[r,v]=1;Dt[r,u]=(-1 if psign[r]==0 else 1)%3
    assert rankp(Dt,3)==45
    Db=[Dt[:,j] for j in range(45)];std=[np.eye(270,dtype=np.int64)[:,j] for j in range(270)]
    BF=extendp(Db,std,3);assert len(BF)==270;coord=coordsp(BF,3);Qbasis=BF[45:]

    # Decompose actual S3 voltages as r^a s^p.
    r3=(1,2,0);s3=(1,0,2);ID=(0,1,2)
    rp=[ID,r3,compose(r3,r3)]
    table={(a,p):compose(rp[a],s3 if p else ID) for a in range(3) for p in range(2)}
    invtab={v:k for k,v in table.items()};assert len(invtab)==6
    avec=np.array([invtab[sig[e]][0] for e in edges],dtype=np.int64)
    acoord=coord(avec)[45:]%3;assert np.any(acoord)

    H3=[]
    projective_scalars=[]
    for gi,p in enumerate(perms):
        # Permuted sign cochain on new canonical edges.
        pnew=np.zeros(270,dtype=np.int64);old_to_new=[]
        for j,(u,v) in enumerate(edges):
            a,b=p[u],p[v];en=tuple(sorted((a,b)));k=ei[en];pnew[k]=psign[j];old_to_new.append((k,a,b))
        # q gauge satisfying pnew = psign + dq, q[0]=0.
        qv=[None]*45;qv[0]=0;Q=deque([0])
        while Q:
            u=Q.popleft()
            for v in sorted(G45[u]):
                if qv[v] is None:
                    k=ei[tuple(sorted((u,v)))];qv[v]=(qv[u]+int(pnew[k])+int(psign[k]))&1;Q.append(v)
        assert all(q is not None for q in qv)
        assert all(((qv[u]+qv[v]+int(psign[j]))&1)==int(pnew[j]) for j,(u,v) in enumerate(edges))
        def T1(x):
            y=np.zeros(270,dtype=np.int64)
            for j,val in enumerate(np.asarray(x,dtype=np.int64)%3):
                if not val:continue
                u,v=edges[j];fu,fv=p[u],p[v];k=ei[tuple(sorted((fu,fv)))]
                coeff=(-1 if qv[fv] else 1)
                if fu>fv:coeff*=(-1 if psign[k]==0 else 1)  # inversion when canonical orientation reverses
                y[k]=(y[k]+coeff*int(val))%3
            return y
        # Exact quotient well-definedness.
        for d in Db:
            c=coord(T1(d));assert not np.any(c[45:])
        cols=[]
        for b in Qbasis:cols.append(coord(T1(b))[45:]%3)
        M=np.column_stack(cols)%3;H3.append(M)
        y=(M@acoord)%3
        if np.array_equal(y,acoord):projective_scalars.append(1)
        elif np.array_equal(y,(-acoord)%3):projective_scalars.append(2)
        else:projective_scalars.append(0)
    assert all(projective_scalars)
    # PSp fixed subspace and full PGSp fixed subspace over F3.
    Ip=np.eye(225,dtype=np.int64)
    pstack=np.vstack([(M-Ip)%3 for M in H3[:len(pgens)]])
    qstack=np.vstack([(M-Ip)%3 for M in H3])
    pfix3=225-rankp(pstack,3);qfix3=225-rankp(qstack,3)
    # PSp is perfect; the selected projective line must be fixed vectorwise. Verify and test uniqueness.
    assert all(s==1 for s in projective_scalars[:len(pgens)])
    selected_outer_scalar=projective_scalars[-1]
    selected_line_unique=(pfix3==1)

    out17={'pass':4817,'binary_sign_module':{'field':'F2','dimension':64,'PSp_fixed_dimension':pfix,'PGSp_fixed_dimension':qfix,
        'PSp_coinvariant_dimension':pcoin,'PGSp_coinvariant_dimension':qcoin,'induced_group_image_order':len(image),
        'PGSp_orbits_on_all_sign_sectors':int(sign_orbits),'Burnside_numerator':str(burn)},
      'selected_sign_sector':{'PGSp_stabilizer_order':51840,'orbit_size':1},
      'twisted_F3_module':{'dimension':225,'PSp_fixed_dimension':pfix3,'PGSp_fixed_dimension':qfix3,
        'selected_projective_line_fixed_by_PGSp':True,'outer_scalar_on_selected_line':int(selected_outer_scalar)},
      'global_projective_orbit_boundary':'The complete PGSp orbit census on all points of PG(224,3) is not enumerated; the induced generators and the selected-line stabilizer/fixed-space data are exact.',
      'theorem':'The full PGSp action on the 64-dimensional binary sign-cohomology quotient is explicit, allowing an exact Burnside count of sign-sector orbits. The selected binary sign sector is a PGSp-fixed point. The selected nonabelian A3 deformation class is a PGSp-stable projective line in the exact 225-dimensional twisted F3 quotient.',
      'boundary':'Exact finite module/orbit statement. The huge PG(224,3) point-orbit census is left as a finite computation rather than inferred.'}
    OUT17.write_text(json.dumps(out17,indent=2,sort_keys=True)+'\n')
    out23={'pass':4823,'selected_A3_line':{'PSp_fixed_subspace_dimension':pfix3,'unique_PSp_invariant_line':selected_line_unique,
        'PGSp_projective_stabilizer_order':51840,'outer_scalar':int(selected_outer_scalar)},
      'signature':'the selected S3 connection is the projective line of its A3 exponent class inside twisted H1(F3); uniqueness is certified iff the PSp fixed subspace has dimension one',
      'theorem':('The selected connection is singled out globally by the unique PSp-invariant projective line in the 225-dimensional twisted deformation module.' if selected_line_unique else 'The selected connection lies on a PSp-invariant projective line, but the PSp fixed subspace has dimension greater than one; this invariant does not uniquely select it.'),
      'boundary':'This is a finite group-cohomology orbit signature, not a continuum gauge invariant.'}
    OUT23.write_text(json.dumps(out23,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'4817':out17,'4823':out23},indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
