#!/usr/bin/env python3
"""Pass 4626 -- explicit outer descent cocycle for the nonsplit 6|6 module.

Pass4623 proved that Q12=K27/K15 splits as U6+U6 over PSp(4,3) but not over
PGSp(4,3).  Here the obstruction is made concrete.  Relative to one PSp direct
sum Q12=U+W with U the unique outer-stable six-space, all inner generators are
block diagonal.  The W33 outer involution is block upper triangular with a
rank-six off-diagonal block B:W->U.  Hom_PSp(W,U) has dimension one, so the two
PSp-equivariant complements form an F2 torsor; the outer involution exchanges
them.  This is the unique nonzero affine C2 descent cocycle on that torsor.
"""
from __future__ import annotations
import itertools,json
from pathlib import Path
import numpy as np
import w33_pass4583_wedge2_exceptional_six_bridge as p
from w33_pass4594_outer_canonical_u6_factor import rank2, nullspace
from w33_pass4472_4479_apartment_module_thermo_ihara_pauli import build_geometry,build_line_perm,transvection_matrix

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4626_OUTER_U6_DESCENT_COCYCLE.json'

def cols_matrix(cols,n):
    M=np.zeros((n,n),dtype=np.uint8)
    for j,c in enumerate(cols):
        for i in range(n):M[i,j]=(int(c)>>i)&1
    return M

def hom_dimension(GU,GW):
    # X:W->U and GU X = X GW, 36 binary unknowns in column-major order.
    eq=[]
    for A,D in zip(GU,GW):
        for r in range(6):
            for c in range(6):
                row=np.zeros(36,dtype=np.uint8)
                for k in range(6):
                    if A[r,k]:row[k+6*c]^=1
                    if D[k,c]:row[r+6*k]^=1
                eq.append(row)
    return 36-rank2(np.asarray(eq,dtype=np.uint8))

def main()->int:
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
    assert len(G)==25920
    outerM=np.diag([1,2,1,2])%3;outerp=build_line_perm(outerM,pts,pidx,lines,lidx)
    G8=[[v8(p.pmask(b,g)) for b in B9[1:]] for g in pgens]
    O8=[v8(p.pmask(b,outerp)) for b in B9[1:]]

    pairs=[(i,k) for i in range(8) for k in range(i+1,8)];idx={z:i for i,z in enumerate(pairs)}
    def wedge(v,w):
        z=0
        for a,b in pairs:
            if ((((v>>a)&1)&((w>>b)&1))^(((v>>b)&1)&((w>>a)&1))):z|=1<<idx[(a,b)]
        return z
    WG=[[wedge(g[i],g[k]) for i,k in pairs] for g in G8];WO=[wedge(O8[i],O8[k]) for i,k in pairs]
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
    Q12=p.quotient_actions(B27,15,WG,28);O12=p.quotient_actions(B27,15,[WO],28)[0]

    sub6=set()
    for x in range(1,1<<12):
        S=p.cyclic(x,Q12,12)
        if len(S)==6:sub6.add(p.rref(S,12))
    six=sorted(sub6);assert len(six)==3 and all(p.rank(list(six[i])+list(six[k]),12)==12 for i in range(3) for k in range(i+1,3))
    sidx={S:i for i,S in enumerate(six)}
    image=lambda S,g:p.rref([p.apply(g,x) for x in S],12)
    outer_perm=[sidx[image(S,O12)] for S in six]
    assert outer_perm==[0,2,1]

    U=list(six[0]);W=list(six[1]);basis=U+W;sol=p.solver(basis)
    def in_basis(g):return [sol(p.apply(g,b)) for b in basis]
    inner=[cols_matrix(in_basis(g),12) for g in Q12];outer=cols_matrix(in_basis(O12),12)
    assert all(not M[:6,6:].any() and not M[6:,:6].any() for M in inner)
    assert not outer[6:,:6].any()
    B=outer[:6,6:];br=rank2(B);assert br==6
    GU=[M[:6,:6] for M in inner];GW=[M[6:,6:] for M in inner]
    hd=hom_dimension(GU,GW);assert hd==1

    # The three invariant six-spaces are U and exactly two complements to U.
    # Hom_G(W,U)=F2 therefore acts simply transitively on the two complements;
    # the outer involution exchanges them, giving the nonzero affine cocycle.
    out={
      'pass':4626,
      'module':'Q12=K27/K15',
      'PSp_splitting':{'U_dimension':6,'W_dimension':6,'inner_generators_block_diagonal':True,'Hom_PSp_W_to_U_dimension':1,'PSp_invariant_six_spaces':3},
      'outer':{'action_on_three_six_spaces':[0,2,1],'preserves_U':True,'swaps_two_complements':True,'lower_left_block_zero':True,'off_diagonal_B_rank':br,'off_diagonal_B_matrix':B.astype(int).tolist()},
      'cocycle':{'coefficient_torsor':'Hom_PSp(W,U)=F2','restriction_to_PSp':'zero','outer_generator':'nonzero element','H1_C2_F2':'one-dimensional; displayed class is nonzero','interpretation':'the two PSp-equivariant complements form an F2 torsor and outer translation exchanges them'},
      'comparison_boundary':'This obstruction vanishes on PSp and lives entirely in outer descent. It is therefore a different mechanism from earlier apartment section obstructions already nonsplit on PSp; no equality of cohomology classes is inferred from dimensions.',
      'theorem':'The PGSp nonsplit 6|6 extension has an explicit one-bit outer descent obstruction: in a PSp direct-sum basis the inner action is block diagonal, while the outer involution carries a full-rank six-by-six off-diagonal block and exchanges the two PSp complements. The complement torsor has Hom dimension one, so this is the unique nonzero affine C2 cocycle on that torsor.',
      'boundary':'This computes the descent class inside the PSp-split extension problem; it does not claim a complete global computation of Ext^1_PGSp(U6,U6).'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
