#!/usr/bin/env python3
"""EXACT rank8 packet-to-axis nullspace => A4+A4 => two E8 glues, exchanged by row/col swap.

The kernel of 25x60 icosian-axis packet incidence is the 8D rational
row/column zero-sum module. Normalize by 1/sqrt5 to get Euclidean
A4(root)⊕A4(root) of determinant 25. Its even unimodular index5
overlattices correspond to isotropic discriminant slopes ±2 mod5:
  L±=A4⊕A4+Z(omega1,±2omega1),
  omega1=(4,-1,-1,-1,-1)/5.
Build integral basis/Gram (det1, even) and all 240 norm2 roots by exact
fifths. The root classes mod2 give 120 anisotropic,135 singular:
the E8 root system and E8/2E8 quadratic shadow.

NEW structural selection fact for this native *frame-kernel* model:
row/col interchange exchanges the ± glues. Each is invariant under
(A5×A5), but neither is invariant under the full (A5×A5):C2
25-packet symmetry unless one adds a two-sheet datum or breaks C2.
Classical E8=A4^2 index5 gluing is PRIOR ART, not claimed new. The
link from user's exact 25x60 tomotope/600-cell packet incidence is
an independently verified concrete construction, not physics.
"""
from __future__ import annotations
import itertools,collections,json,sys,math
from pathlib import Path
import sympy as s
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT/"analysis") not in sys.path:sys.path.insert(0,str(ROOT/"analysis"))
from toe_20261104_pg34_icosian_quadric import geometry
OUT=ROOT/"data"/"toe_20261104_reye_kernel_a4a4_e8_glue.json"
w5=[4,-1,-1,-1,-1]
def a4roots_scaled5():
    arr=[]
    for i in range(5):
        for j in range(5):
            if i!=j:
                v=[0]*5;v[i]=5;v[j]=-5
                arr.append(tuple(v))
    assert len(arr)==20
    return arr
def weights_scaled5(k):
    assert k in (1,2,3,4)
    rows=[]
    for inds in itertools.combinations(range(5),k):
        v=[5-k if i in inds else -k for i in range(5)]
        assert sum(v)==0 and sum(a*a for a in v)==5*k*(5-k)
        rows.append(tuple(v))
    return rows
def roots_scaled5(slope):
    arr=[]
    roots=a4roots_scaled5()
    z=(0,)*5
    arr.extend([r+z for r in roots])
    arr.extend([z+r for r in roots])
    for k in range(1,5):
        p=weights_scaled5(k)
        q=weights_scaled5((slope*k)%5)
        arr.extend([u+v for u in p for v in q])
    assert len(arr)==240 and len(set(arr))==240
    assert all(sum(a*a for a in v)==50 for v in arr)
    return arr
def bases_scaled5(slope):
    assert slope in (2,3)
    std=[tuple((1 if i==j else -1 if i==j+1 else 0)*5
         for i in range(5)) for j in range(4)]
    basis=[v+(0,)*5 for v in std[:3]]+[(0,)*5+v for v in std]
    glue=w5+[(-2 if slope==3 else 2)*v for v in w5]
    basis.append(tuple(glue))
    B=s.Matrix.hstack(*(s.Matrix(v) for v in basis))
    assert B.shape==(10,8)
    G=B.T*B/25
    assert G.det()==1 and all(G[i,i]%2==0 for i in range(8))
    assert G==G.T and all(G[i,j].q==1 for i in range(8) for j in range(8))
    # Positive definite by physical Euclidean ten-coordinate embedding
    assert B.rank()==8
    return B,G
def integral_coordinates(B):
    inds=list((B.T).rref()[1])
    assert len(inds)==8
    Binv=B[inds,:].inv()
    def coords(v):
        u=Binv*s.Matrix([v[i] for i in inds])
        assert B*u==s.Matrix(v)
        return u
    return coords
def binary_q(G,v):
    a=s.Matrix([int((v>>i)&1) for i in range(8)])
    return int((a.T*G*a)[0]//2)%2
def apply_perm(v,p,side):
    v=list(v)
    dest=list(v)
    for i in range(5):dest[5*side+p[i]]=v[5*side+i]
    return s.Matrix(dest)
def even_perm_generators():
    cycle5=(1,2,3,4,0)
    cycle3=(1,2,0,3,4)
    def cp(p,q):return tuple(p[q[i]] for i in range(5))
    group={(0,1,2,3,4)}
    while True:
        new=group|{cp(g,a) for g in group for a in (cycle5,cycle3)}
        if len(new)==len(group):break
        group=new
    assert len(group)==60
    return group,[cycle5,cycle3]
def main():
    pg=geometry()
    coords=[tuple(t) for t in pg["cell_grid_locations_25"]]
    membership=np.zeros((25,60),dtype=int)
    for rec in pg["reye_tangent_plane_records_25"]:
        for axis in rec["incidence_axes"]:membership[rec["cell_id"],axis]=1
    rowcol=np.zeros((25,8),dtype=int)
    for i,(r,c) in enumerate(coords):
        for j in range(4):
            rowcol[i,j]=(r==j)-(r==4)
            rowcol[i,j+4]=(c==j)-(c==4)
    # rowcol columns are 5-fold physical embeddings of 8 A4 roots,
    # but our chosen simple A4 basis in 10D is a different integral basis.
    assert np.linalg.matrix_rank(rowcol)==8 and not np.any(membership.T@rowcol)
    # 10D embedding T(u,v) = u_row + v_column has inner metric 5 times
    # A4⊕A4. It is exact over integer vectors.
    std=[(np.eye(5,dtype=int)[j]-np.eye(5,dtype=int)[j+1]) for j in range(4)]
    fs=[]
    for u,v in ([(x,np.zeros(5,dtype=int)) for x in std]+
                [(np.zeros(5,dtype=int),x) for x in std]):
        f=np.array([u[r]+v[c] for r,c in coords])
        assert np.linalg.norm(membership.T@f)<1e-12
        fs.append(f)
    Gram25=np.array([[(x@y) for y in fs] for x in fs])
    baseG=s.diag(s.eye(4)*2,s.eye(4)*2)
    for start in (0,4):
        for i in range(3):
            baseG[start+i,start+i+1]=-1
            baseG[start+i+1,start+i]=-1
    assert np.array_equal(Gram25,np.array(baseG*5,dtype=int))
    assert baseG.det()==25
    roots={}
    grp={}
    for slope in (2,3):
        B,G=bases_scaled5(slope)
        roots[slope]=roots_scaled5(slope)
        coord=integral_coordinates(B)
        classes=set()
        for v in roots[slope]:
            x=coord(v)
            assert all(t.q==1 for t in x)
            bit=sum((int(x[i])&1)<<i for i in range(8))
            assert binary_q(G,bit)==1
            classes.add(bit)
        assert len(classes)==120
        q0=sum(binary_q(G,v)==0 for v in range(256))
        assert q0==136
        # Every distinct root modulo plus/minus corresponds to one
        # anisotropic E8 mod2 class; 240 roots in 120 classes.
        grp[slope]=dict(basis_scaled5=B.tolist(),
            Gram_matrix=G.tolist(),Gram_determinant=int(G.det()),
            norm2_roots=len(roots[slope]),
            nonzero_anisotropic_mod2_classes=len(classes),
            nonzero_isotropic_mod2_classes=135,
            root_count_per_glue_coset={"0":40,"1":50,"2":50,"3":50,"4":50},
            even_unimodular=True)
    # Exactly two graph gluing slopes with slope²=-1 mod5.
    admissible=[a for a in range(1,5) if (a*a+1)%5==0]
    assert admissible==[2,3]
    # Every generator of A5 on rows or columns preserves BOTH E8 lattices.
    _,gen=even_perm_generators()
    for slope in (2,3):
        B,_=bases_scaled5(slope)
        coord=integral_coordinates(B)
        for side in (0,1):
            for permutation in gen:
                for i in range(8):
                    x=coord(apply_perm(B[:,i],permutation,side))
                    assert all(t.q==1 for t in x)
    Bplus,_=bases_scaled5(2)
    Bminus,_=bases_scaled5(3)
    cplus=integral_coordinates(Bplus);cminus=integral_coordinates(Bminus)
    def swap(x):return s.Matrix(list(x[5:])+list(x[:5]))
    for j in range(8):
        assert all(t.q==1 for t in cminus(swap(Bplus[:,j])))
        assert all(t.q==1 for t in cplus(swap(Bminus[:,j])))
    assert any(t.q!=1 for t in cplus(swap(Bplus[:,7])))
    # A packet-grid swap also acts on axes by inverse A5 permutation.
    axmap={tuple(z["permutation"]):int(z["axis_id"]) for z in pg["icosian_axis_permutations_60"]}
    cellmap={tuple(v):i for i,v in enumerate(coords)}
    for p,a in axmap.items():
        pinv=tuple(p.index(i) for i in range(5))
        b=axmap[pinv]
        orig={tuple(coords[i][j] for j in (0,1)) for i in range(25) if membership[i,a]}
        trans={(y,x) for x,y in orig}
        other={tuple(coords[i][j] for j in (0,1)) for i in range(25) if membership[i,b]}
        assert trans==other
    result=dict(status="PASS_E8_LATTICES_IN_REYE_PACKET_AXIS_KERNEL_WITH_TWO_SWAPPED_GLUES",
      packet_axis_matrix_shape=[25,60],packet_axis_kernel_dimension=8,
      normalized_kernel_root_lattice="A4 ⊕ A4",
      normalized_kernel_root_Gram_matrix=(baseG).tolist(),
      normalized_kernel_Gram_determinant=25,
      inner_product_scaling_of_row_col_zero_sum_5x5_basis=5,
      E8_overlattice_index=5,even_unimodular_rank=8,
      discriminant_isotropic_slope_solutions_mod5=admissible,
      plus_and_minus_E8_lattice_certificates=grp,
      each_E8_has_240_norm2_roots=True,
      each_E8_mod2_has_120_anisotropic_135_singular=True,
      A5xA5_preserves_both_E8_glues=True,
      row_column_interchange_exchanges_the_two_E8_glues=True,
      full_icosian_H4_packet_action_cannot_fix_one_E8_glue=True,
      no_invariant_single_glue_selection_without_sheet_choice=True,
      physical_candidate="Two E8 sheets are exchanged by the 5x5 packet-grid swap. It is tempting to interpret as past/future or chirality, but NO physical map to photon states, spacetime, gravity or generations has been supplied.",
      novelty_and_prior_art="E8 as index-five overlattice of A4⊕A4 and two isotropic glues is classical lattice theory; F4 25cells/60axes projective geometry is published. The new computed integration is that the eight-dimensional blind submodule of THIS exact 25x60 Reye–600cell frame incidence carries A4⊕A4, with explicit E8 glues and a swap obstruction.",
      absolute_limit="The lattice extension is a mathematical choice, not forced by the incidence M. H4 symmetry exchanges the two choices. It does not prove E8 particles or TOE.")
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True,default=int)+"\n",encoding="utf8")
    print(result["status"],"roots",grp[2]["norm2_roots"],"swap",result["row_column_interchange_exchanges_the_two_E8_glues"],flush=True)
    return result
if __name__=="__main__":main()
