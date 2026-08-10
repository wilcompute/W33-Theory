#!/usr/bin/env python3
"""Pass 4628 -- the compatible F4 choices on U6 are the point-side W33 carrier.

Pass4592 reaches the hexacode/Golay bridge only after choosing a compatible F4
structure on the natural minus six-space U6.  This pass classifies that choice
space under the actual PGSp(4,3) action and keeps the action paired with W33
points and lines.

A compatible F4 structure is an unoriented pair {J,J^2}, where J is an
orthogonal fixed-point-free order-three operator, equivalently J^2+J+I=0.
There are 80 oriented J and 40 pairs.  For a representative, the centralizer in
PGSp has order 648 and the normalizer of <J> has order 1296.  Crucially that
normalizer fixes exactly one W33 point and no W33 line.  Hence the 40 compatible
F4 structures form exactly the point-side W33 G-set, by an explicit
stabilizer-fixed-point orbit map.
"""
from __future__ import annotations
import itertools,json
from collections import deque
from pathlib import Path
import numpy as np
import w33_pass4583_wedge2_exceptional_six_bridge as p
from w33_pass4594_outer_canonical_u6_factor import rank2
from w33_pass4472_4479_apartment_module_thermo_ihara_pauli import build_geometry,build_line_perm,transvection_matrix,norm3

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4628_F4_CHOICE_IS_W33_POINT_CARRIER.json'

def compose(a,b):return tuple(a[b[i]] for i in range(len(a)))
def point_perm(M,pts,pidx):
    out=[]
    for x in pts:
        y=(np.asarray(M,dtype=int)@np.asarray(x,dtype=int))%3
        out.append(pidx[norm3(tuple(map(int,y)))])
    return tuple(out)
def cols_matrix(cols,n):
    M=np.zeros((n,n),dtype=np.uint8)
    for j,c in enumerate(cols):
        for i in range(n):M[i,j]=(int(c)>>i)&1
    return M

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

    # Paired inner generators: same transvection gives point, line and U6 action.
    cand=[];pgens=[];Gperm={tuple(range(40))}
    for v in pts:
        M=transvection_matrix(v);lp=build_line_perm(M,pts,pidx,lines,lidx)
        if lp in Gperm:continue
        pgens.append((M,point_perm(M,pts,pidx),lp));Gperm=p.perm_group([z[2] for z in pgens])
        if len(Gperm)==25920:break
    assert len(Gperm)==25920
    linegens=[z[2] for z in pgens]
    G8=[[v8(p.pmask(b,g)) for b in B9[1:]] for g in linegens]
    outerM=np.diag([1,2,1,2])%3;outerp=build_line_perm(outerM,pts,pidx,lines,lidx)
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
    six=sorted(sub6);assert len(six)==3
    sidx={S:i for i,S in enumerate(six)}
    image=lambda S,g:p.rref([p.apply(g,x) for x in S],12)
    op=[sidx[image(S,O12)] for S in six];assert op==[0,2,1]
    U=list(six[0]);solU=p.solver(U)
    GU=[[solU(p.apply(g,b)) for b in U] for g in Q12]
    OU=[solU(p.apply(O12,b)) for b in U]
    GU=[cols_matrix(g,6) for g in GU];OU=cols_matrix(OU,6)

    # Generate PGSp faithfully while carrying both W33 permutations.
    inner_triples=[(GU[i],pgens[i][1],pgens[i][2]) for i in range(len(GU))]
    outer_triple=(OU,point_perm(outerM,pts,pidx),outerp)
    gens=inner_triples+[outer_triple]
    I=np.eye(6,dtype=np.uint8);ip=tuple(range(40));key=lambda M:bytes(M.ravel())
    group={key(I):(I,ip,ip)};Q=deque([(I,ip,ip)])
    while Q:
        M,pp,ll=Q.popleft()
        for X,xp,xl in gens:
            Z=(X@M)%2;z=(Z,compose(xp,pp),compose(xl,ll));k=key(Z)
            if k not in group:group[k]=z;Q.append(z)
    assert len(group)==51840

    # Oriented compatible F4 structures J satisfy Phi_3(J)=0.
    Z6=np.zeros((6,6),dtype=np.uint8)
    oriented=[z for z in group.values() if np.array_equal((z[0]@z[0]+z[0]+I)%2,Z6)]
    assert len(oriented)==80
    J=oriented[0][0];J2=(J@J)%2
    central=[];normal=[]
    for z in group.values():
        M=z[0]
        if np.array_equal((M@J)%2,(J@M)%2):central.append(z);normal.append(z)
        elif np.array_equal((M@J)%2,(J2@M)%2):normal.append(z)
    assert len(central)==648 and len(normal)==1296 and 51840//len(normal)==40
    fixed_points=[i for i in range(40) if all(z[1][i]==i for z in normal)]
    fixed_lines=[i for i in range(40) if all(z[2][i]==i for z in normal)]
    assert len(fixed_points)==1 and len(fixed_lines)==0

    old4592=json.loads((ROOT/'data/PART_W33_PASS4592_PAIRED_AXES_SIMPLEX_HEXACODE_GOLAY.json').read_text())
    old4615=json.loads((ROOT/'data/PART_W33_PASS4615_HEXACODE_SECTION_RECONSTRUCTS_MOG_SEXTET.json').read_text())
    assert 'chosen F4 structure' in old4592['structural_chain'] and old4615['sextet_completion']['valid_matchings']==1
    out={
      'pass':4628,
      'compatible_F4_structures':{'definition':'unoriented {J,J^2} with J^2+J+I=0 on the outer-stable U6','oriented_J':80,'unoriented_pairs':40,'centralizer_order':648,'normalizer_order':1296,'PGSp_orbit_size':40},
      'W33_intertwiner':{'normalizer_fixed_points':fixed_points,'normalizer_fixed_lines':fixed_lines,'carrier':'point-side W33','criterion':'the representative F4-structure normalizer fixes exactly one W33 point and no line; orbit-stabilizer gives the equivariant 40-to-40 bijection'},
      'Golay_MOG_bridge':{'Pass4592':'a compatible F4 structure is exactly the extra choice used before the hexacode [18,6,8] embedding','Pass4615':'the frozen chosen structure/embedding then uniquely reconstructs one Golay MOG sextet','new_reading':'W33 points parameterize the compatible F4 structures on U6'},
      'half_spinor_context':'The same U6 has the 27 singular plus 36 anisotropic coordinate split used by the concrete D4/cubic half-spinor lane; the three external degree-36 sheets do not themselves remove the F4 choice.',
      'theorem':'The noncanonical F4 step in the paired-axis Golay construction has an exact W33 parameter space: the 40 compatible F4 structures on the natural minus six-space form the point-side W33 PGSp G-set. A representative structure has unitary centralizer 648 and semilinear normalizer 1296 fixing a unique W33 point.',
      'boundary':'This identifies the F4-choice G-set. The frozen Golay coordinate embedding is not PGSp-equivariant and no O^-(6,2) subgroup of M24 is claimed.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
