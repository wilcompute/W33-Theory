#!/usr/bin/env python3
"""A *real 4D* Euclidean Regge action on the 1->5 subdivision of a 4-simplex.

Five boundary vertices e0=0,e1..e4 standard axes; one interior vertex
c=mean(vertices); five new 4-simplices, ten internal triangle hinges,
ten boundary triangles. S=Σ_bulk A(2pi-Σθ)+Σ_boundary A(pi-Σθ),
all angles derived from 4x4 edge-length Gram matrices. Differentiating
the Regge action (Schlafli identity) yields grad S=Σδ dA/dl for five
internal edges. Hessian at flat geometry has FOUR vertex-displacement
null modes and one physical-looking normal direction (rank1). Add
non-geometric internal edge-length perturbation -> curvature and
small nonzero pseudo-constraint eigenvalues: no exact nonlinear gauge.

Caveat: Euclidean *single simplex* with boundaries fixed, no Lorentzian
causal cones/ADM hypersurface Dirac algebra, no dynamical spacetime and
no identified H4/tomotope physical selection. Flat vertex gauge and
curved pseudoconstraints are STANDARD Regge literature (Bahr/Dittrich
2009, Dittrich/Hohn 2010, Hohn 2015).
"""
from __future__ import annotations
import itertools,json,math
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261104_regge_4simplex_1to5_action.json"
V=np.vstack((np.zeros(4),np.eye(4)))
C=np.mean(V,axis=0)
DIST2={(i,j):float(np.sum((V[i]-V[j])**2)) for i in range(5) for j in range(5)}
INTERIOR=list(itertools.combinations(range(5),2))
BOUNDARY=list(itertools.combinations(range(5),3))
def boundary_area(tri):
    a,b,c=tri
    u,v,w=DIST2[a,b],DIST2[a,c],DIST2[b,c]
    return math.sqrt(4*u*v-(u+v-w)**2)/4
def area_internal(x,a,b):
    u=x[a]**2;v=x[b]**2
    w=(u+v-DIST2[a,b])/2
    return .5*math.sqrt(u*v-w*w)
def act(x):
    x=np.asarray(x,dtype=float)
    grams={}
    for absent in range(5):
        indices=[i for i in range(5) if i!=absent]
        G=np.array([[(x[i]**2+x[j]**2-DIST2[i,j])/2 for j in indices] for i in indices])
        if np.linalg.eigvalsh(G)[0]<=0:raise ValueError("non-Euclidean length data")
        grams[absent]=(indices,np.linalg.inv(G))
    deficit={}
    for a,b in INTERIOR:
        ang=0.
        for absent in range(5):
            if absent in (a,b):continue
            indices,g=grams[absent]
            other=[k for k in indices if k not in (a,b)]
            i,j=[indices.index(k) for k in other]
            cosine=-g[i,j]/math.sqrt(g[i,i]*g[j,j])
            ang+=math.acos(float(np.clip(cosine,-1,1)))
        deficit[a,b]=2*math.pi-ang
    boundary_exterior={}
    for a,b,c in BOUNDARY:
        angles=0.
        for absent in range(5):
            if absent in (a,b,c):continue
            indices,g=grams[absent]
            other=next(k for k in indices if k not in (a,b,c))
            j=indices.index(other)
            cosine=float(np.sum(g[:,j])/math.sqrt(np.sum(g)*g[j,j]))
            angles+=math.acos(float(np.clip(cosine,-1,1)))
        boundary_exterior[a,b,c]=math.pi-angles
    areas={t:area_internal(x,*t) for t in INTERIOR}
    S=sum(areas[t]*delta for t,delta in deficit.items())+sum(
        boundary_area(t)*exterior for t,exterior in boundary_exterior.items())
    grad=np.zeros(5)
    for (a,b),delta in deficit.items():
        u=x[a]**2;v=x[b]**2
        z=(u+v-DIST2[a,b])/2
        area=areas[a,b]
        grad[a]+=delta*x[a]*(v-z)/(4*area)
        grad[b]+=delta*x[b]*(u-z)/(4*area)
    return S,grad,deficit
def hessian(x,h=3e-5):
    e=np.eye(5)
    J=np.column_stack([(act(x+h*e[j])[1]-act(x-h*e[j])[1])/(2*h) for j in range(5)])
    assert np.max(abs(J-J.T))<1e-3
    return .5*(J+J.T)
def main():
    x0=np.linalg.norm(V-C,axis=1)
    S0,g0,d0=act(x0)
    expected=3*math.pi/2+4*math.pi*math.sqrt(3)/3
    assert abs(S0-expected)<1e-11
    assert max(abs(v) for v in d0.values())<1e-11
    assert np.linalg.norm(g0)<1e-11
    # Four independent physical vertex translation tangent vectors.
    J=np.array([(C-V[i])/x0[i] for i in range(5)])
    assert np.linalg.matrix_rank(J)==4
    H0=hessian(x0)
    val=np.linalg.eigvalsh(H0)
    assert sum(abs(v)<1e-4 for v in val)==4
    assert abs(val[-1]-128)<.01
    assert np.linalg.norm(H0@J)<1e-4
    # Analytically predicted null normal: w=(2,sqrt19,sqrt19,sqrt19,sqrt19)
    normal=np.array([2]+[math.sqrt(19)]*4,dtype=float)/math.sqrt(80)
    assert np.max(abs(J.T@normal))<1e-12
    assert abs(normal@H0@normal-128)<.01
    # The flat family c'=c+delta in actual R4 leaves the full
    # Regge+boundary action independent of the chosen interior vertex.
    shifts=[(0,0,0,0),(.02,-.01,.01,-.01),(-.012,.02,.017,-.005)]
    for shift in shifts:
        cp=C+np.array(shift,dtype=float)
        S,g,dd=act(np.linalg.norm(V-cp,axis=1))
        assert abs(S-S0)<1e-11
        assert np.linalg.norm(g)<1e-10
        assert max(abs(v) for v in dd.values())<1e-10
    curved=[]
    for amp in (.001,.005,.01):
        x=x0+amp*normal
        S,g,dd=act(x)
        H=hessian(x,h=2e-5)
        eig=np.linalg.eigvalsh(H)
        # Four gauge directions become NONZERO under curvature.
        assert all(abs(v)>.01 for v in eig[:4])
        assert abs(S-S0)>.00001
        assert max(abs(v) for v in dd.values())>.02
        # First variation of action agrees independently with
        # Schlaefli-based Regge equation.
        idx=2;h=1e-6;e=np.eye(5)[idx]
        dS=(act(x+h*e)[0]-act(x-h*e)[0])/(2*h)
        assert abs(dS-g[idx])<1e-6
        curved.append(dict(normal_perturbation_length=amp,
          delta_action=S-S0,gradient_norm=float(np.linalg.norm(g)),
          max_internal_deficit_rad=max(abs(v) for v in dd.values()),
          action_Hessian_eigenvalues=[float(v) for v in eig],
          four_vertex_translation_hessian_zeros_lifted=True))
    result=dict(status="PASS_ACTION_DERIVED_4D_EUCLIDEAN_REGGE_FLAT_GAUGE_AND_CURVED_PSEUDOCONSTRAINTS",
      base_simplex_vertices_5=V.tolist(),
      inserted_interior_vertex=C.tolist(),
      new_4simplices=5,
      internal_2simplices_triangle_hinges=10,
      boundary_2simplices=10,
      dynamical_internal_edge_lengths=5,
      boundary_lengths_fixed=True,
      Euclidean_Regge_plus_boundary_action_formula="S=sum_internal A_h(2*pi-sum theta) + sum_boundary A_h(pi-sum theta)",
      flat_action_measured=S0,
      flat_action_exact="3*pi/2 + 4*pi*sqrt(3)/3",
      flat_internal_deficit_max=max(abs(v) for v in d0.values()),
      flat_Action_gradient_norm=float(np.linalg.norm(g0)),
      flat_action_Hessian_eigenvalues=[float(v) for v in val],
      four_flat_vertex_translation_gauge_tangent_directions=J.tolist(),
      flat_action_Hessian_rank_approx=1,
      analytic_orthogonal_normal_vector=normal.tolist(),
      single_nonzero_Hessian_eigen_approx_128=True,
      exact_4D_flat_vertex_motions_keep_action_constant=True,
      off_shell_curved_normal_perturbations=curved,
      exact_non_linear_Dirac_first_class_constraint_algebra_derived=False,
      Lorentzian_signature_or_causality_constructed=False,
      boundary="Only a single Euclidean 4-simplex 1-5 subdivision with fixed boundary. This is an action-derived finite control, not a Lorentzian metric, not full gravitational dynamics, and not an embedding of a 600-cell/tomotope gravity theory.",
      prior_art="Flat Regge vertex displacement nulls and curvature-induced pseudo-constraints are established in Bahr/Dittrich 2009 arxiv:0905.1670; Dittrich/Hohn 2010; Hohn 2015. Added here: numerical controlled derivation and rank/curvature tests in this explicit one-interior-vertex 4-simplex.")
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(result["status"],"flat Hessian",val,"curved",curved[1]["action_Hessian_eigenvalues"],flush=True)
    return result
if __name__=="__main__":main()
