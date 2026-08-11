#!/usr/bin/env python3
"""Pass 4827 — exact PGSp Burnside quotient of the 64-bit S3 sign sectors.

Pass4770 gives an affine 64-dimensional F2 space of sign solutions. Pass4817
proves the selected sign solution is fixed by full PGSp, so translation by that
solution identifies the affine action with the linear 64-dimensional
sign-cohomology module. We therefore enumerate only the finite matrix image of
PSp/PGSp on this module, never the 2^64 vectors, and apply Burnside exactly:

  #orbits = |G_im|^{-1} sum_g 2^{dim Fix(g)}.

The accompanying Pass4817/4823 producer is run first in the evidence workflow;
its 225-dimensional twisted-F3 fixed-space and selected-line data are imported
when present. A complete PG(224,3) orbit census is still not inferred from those
fixed spaces alone.
"""
from __future__ import annotations
import itertools,json
from collections import Counter,deque
from pathlib import Path
from w33_pass4756_4758_4760_dependency_cube_reconstruction import build_all
from w33_pass4716_selected270_bundle_connection import build_bundle
from w33_pass4721_4724_support12_involution_square_root_cover import build_groups
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4827_PGSP_SIGN_BURNSIDE.json'

def pmask(m,p):
    y=0;x=int(m)
    while x:
        b=x&-x;i=b.bit_length()-1;x^=b;y|=1<<p[i]
    return y

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
        out.append(x)
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
    def sol(x):
        y=int(x);c=0
        while y:
            p=y.bit_length()-1
            if p not in piv:return None
            y^=piv[p][0];c^=piv[p][1]
        return c
    return sol

def rows_from_cols(cols,n=64):
    rows=[0]*n
    for j,c in enumerate(cols):
        y=int(c)
        while y:
            b=y&-y;i=b.bit_length()-1;y^=b;rows[i]|=1<<j
    return rows

def apply_cols(cols,x):
    y=0
    while x:
        b=x&-x;i=b.bit_length()-1;x^=b;y^=cols[i]
    return y

def compose_cols(A,B):return tuple(apply_cols(A,c) for c in B)

def matrix_group(gens,n=64):
    I=tuple(1<<i for i in range(n));seen={I};Q=deque([I])
    while Q:
        a=Q.popleft()
        for g in gens:
            c=compose_cols(g,a)
            if c not in seen:seen.add(c);Q.append(c)
    return seen

def fixdim(M,n=64):
    rows=rows_from_cols(M,n)
    return n-rank2([rows[i]^(1<<i) for i in range(n)])

def main():
    D=build_all();X=build_bundle();pts=D['pts'];lines=D['lines'];sing=D['selected135'];packets=X['packets'];G45=X['G45']
    pidx={p:i for i,p in enumerate(pts)};pgens,PSp,full=build_groups(pts,pidx,lines);outer=next(g for g in full if g not in PSp);fullgens=list(pgens)+[outer]
    all40=(1<<40)-1;rep=lambda x:min(int(x),int(x)^all40);sidx={int(x):i for i,x in enumerate(sing)};packet_of={s:p for p,T in enumerate(packets) for s in T}
    def packet_perm(g):
        sp=[sidx[rep(pmask(sing[i],g))] for i in range(135)];q=[]
        for T in packets:
            z={packet_of[sp[s]] for s in T};assert len(z)==1;q.append(next(iter(z)))
        return tuple(q)
    perms=[packet_perm(g) for g in fullgens]
    edges=sorted(tuple(sorted(e)) for e in G45.edges());ei={e:i for i,e in enumerate(edges)}
    tris=sorted(set(tuple(sorted(t)) for t in X['projected']));trows=[]
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
        H2.append(tuple(cols))
    GP=matrix_group(H2[:len(pgens)]);GQ=matrix_group(H2)
    assert 25920%len(GP)==0 and 51840%len(GQ)==0
    def burn(G):
        C=Counter(fixdim(M) for M in G)
        S=sum(n*(1<<d) for d,n in C.items());assert S%len(G)==0
        return C,S//len(G)
    Cp,Op=burn(GP);Cq,Oq=burn(GQ)
    old={}
    p17=ROOT/'data/PART_W33_PASS4817_PGSP_S3_MODULI_MODULE.json';p23=ROOT/'data/PART_W33_PASS4823_SELECTED_CONNECTION_INVARIANT_LINE.json'
    if p17.exists():old['4817']=json.loads(p17.read_text())
    if p23.exists():old['4823']=json.loads(p23.read_text())
    out={'pass':4827,'sign_solution_space':{'affine_dimension':64,'translation_origin':'selected PGSp-fixed sign solution from Pass4817','PSp_matrix_image_order':len(GP),'PGSp_matrix_image_order':len(GQ),'PSp_kernel_order':25920//len(GP),'PGSp_kernel_order':51840//len(GQ)},
      'PSp_Burnside':{'fixed_dimension_census':dict(sorted(Cp.items())),'number_of_sign_sector_orbits':Op,'nonzero_orbits':Op-1},
      'PGSp_Burnside':{'fixed_dimension_census':dict(sorted(Cq.items())),'number_of_sign_sector_orbits':Oq,'nonzero_orbits':Oq-1},
      'twisted_F3_selected_line_data':old,
      'theorem':'Translation by the selected PGSp-fixed sign solution turns the 2^64 admissible sign sectors into the linear sign-cohomology module. Enumerating the finite matrix image and applying Burnside gives the exact PSp and PGSp orbit counts without enumerating any of the 2^64 vectors.',
      'boundary':'This completely quotients the binary sign sectors. The 225-dimensional twisted-F3 projective space is not globally orbit-enumerated here; only the exact Pass4817/4823 fixed-space and selected-line data are carried forward when materialized.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
