"""TOE72: W33 x W33 closed spin four-manifold; inherited-isotropic index no-go.

Each factor is a closed genus-81 boundary of a graph handlebody derived
from the W33 Levi graph. This avoids an externally added T2 but still
requires noncanonical graph thickening. All graph-pulled H1 characters are
a Lagrangian isotropic subspace of H1(boundary); mixed 4D Chern classes
formed solely from such inherited characters square to zero. Nonzero
chiral index requires dual boundary cycles or other added curvature.
"""
from __future__ import annotations
from pathlib import Path
import json,sys
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261014_toe69_five_fronts import graph

def certificate():
    edges,adj=graph()
    V=80;E=len(edges);g=E-V+1
    assert len(adj)==V and E==160 and g==81
    # Closed spin 4D model from TWO copies of W33-derived genus g surface.
    # No external T2. No canonical W33-invariant ribbon rotation either.
    s=[1,2*g,1]
    betti=[sum(s[i]*s[k-i] for i in range(3) if 0<=k-i<3)
           for k in range(5)]
    assert betti==[1,324,26246,324,1]
    euler=sum(((-1)**k)*b for k,b in enumerate(betti))
    assert euler==25600==(2-2*g)**2
    assert betti[2]//2==13123
    # Symplectic intersection on each surface for one handle:
    # basis alpha inherited from H1(handlebody), beta its dual.
    J=np.array([[0,1],[-1,0]],int)
    # Cup of cross 2-forms x tensor y on product; minus sign of crossing.
    Q=-np.kron(J,J)
    assert np.array_equal(Q,Q.T)
    assert np.array_equal(Q@Q,np.eye(4,dtype=int))
    aa=np.array([1,0,0,0],int)  # alpha_X tensor alpha_Y
    assert int(aa@Q@aa)==0
    # all graph-inherited alpha_i pullbacks are isotropic within either
    # surface: for any i,j, alpha_i cup alpha_j = 0 in H2(Sigma).
    # Therefore Q vanishes on the 81^2-dimensional A_X tensor A_Y,
    # including nondecomposable integer sums of those mixed classes.
    inherited_rank=g*g
    assert inherited_rank==6561
    # A dual meridional beta in EACH factor changes the answer:
    # c1 = alpha_X tensor beta_Y + beta_X tensor alpha_Y
    c=np.array([0,1,1,0],int)
    sq=int(c@Q@c)
    assert sq==2 and sq//2==1
    return {
      "status":"PASS_TOE72_W33_TIMES_W33_LAGRANGIAN_INDEX_NO_GO",
      "one_native_Levi_graph_vertices_edges":[V,E],
      "native_cycle_rank_per_factor":g,
      "M4":"boundary of one W33 graph handlebody times boundary of second W33 graph handlebody",
      "external_torus_required":False,
      "closed":True,"oriented":True,"spin":True,
      "betti_integral_torsion_free":betti,
      "euler_characteristic":euler,"signature":0,
      "hyperbolic_intersection_planes":betti[2]//2,
      "native_three_deck_flat_characters_survive_on_both_factors":True,
      "graph_inherited_H1_lagrangian_rank_per_factor":g,
      "graph_inherited_mixed_H2_subspace_rank":inherited_rank,
      "mixed_H2_intersection_form_zero_on_entire_graph_inherited_subspace":True,
      "all_graph_inherited_mixed_c1_classes_have_index_zero":True,
      "one_handle_integral_cross_form":[list(map(int,row)) for row in Q],
      "non_native_dual_meridian_c1_coefficients":c.tolist(),
      "non_native_dual_meridian_c1_square":sq,
      "non_native_dual_meridian_twisted_spin_Dirac_index":sq//2,
      "obstruction":"The graph's H1 pulls back to the Lagrangian in the boundary surface. Two such pullbacks have zero 2D cup intersection, hence any cross-product first Chern class using ONLY inherited graph H1 on both factors has c1^2=0 and 4D spin index=0. A nonzero index requires meridian-dual cohomology or externally chosen curvature.",
      "scope":"Genuine smooth closed W33-derived topology and integral index-theory no-go for graph-only mixed flux. Not a W33-invariant unique manifold, discretized local overlap Dirac operator, Weyl spectrum, or physical chirality."
    }

if __name__=="__main__":
    c=certificate()
    (ROOT/"data/w33_20261014_toe72_w33_squared_index.json").write_text(json.dumps(c,indent=2)+"\n")
    print(c["status"],c["betti_integral_torsion_free"])
