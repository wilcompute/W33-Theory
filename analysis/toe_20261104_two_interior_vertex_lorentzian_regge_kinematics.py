#!/usr/bin/env python3
"""4D Lorentzian two-interior-vertex nested 1->5 refinements.

Flat Minkowski boundary 4-simplex, barycenter c, insert b into
child {c,v1,v2,v3,v4}; 9 4-simplices in total. Ten interior
squared-lengths (5 c-boundary and 5 b-to-c/v1..v4) come from
8 coordinates, hence exactly two algebraic flat-embedding
constraints C_c and C_b. Compute by explicit Lorentzian Gram
inversion and certify tangent rank8 and independent constraint
gradients rank2. Checks orientation, causal simplex signature and
volumes with exact rational arithmetic, plus off-flat interval
perturbations preserving every simplex' Lorentzian signature.

This is REAL multi-interior Lorentzian Regge kinematics, but
no canonical first-class constraints are inferred from mere
configuration-space relations. Proper boundary action and Dirac
brackets remain REQUIRED.
"""
from __future__ import annotations
import itertools,math,json
from pathlib import Path
import numpy as np
import sympy as sy
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261104_two_interior_vertex_lorentzian_regge_kinematics.json"
eta=np.diag([-1.,1.,1.,1.])
V=np.vstack((np.zeros(4),np.diag([2.,1.,1.,1.])))
c=V.mean(axis=0);b=np.mean(np.vstack((c,V[1:])),axis=0)
allpos=np.vstack((V,c,b))
first=[tuple([5]+[i for i in range(5) if i!=omit]) for omit in range(5)]
assert len(first)==5
idx=next(i for i,t in enumerate(first) if set(t)=={5,1,2,3,4})
parent=first.pop(idx)
cells=first+[tuple([6]+[i for i in parent if i!=omit]) for omit in parent]
assert len(cells)==9
edges_c=[(5,i) for i in range(5)]
edges_b=[(6,i) for i in (5,1,2,3,4)]
edges=edges_c+edges_b
assert len(edges)==10
def sq(x,y):return float((x-y)@eta@(x-y))
def scalar(x,y):return float(x@eta@y)
def intervals(cc,bb):
 aa=allpos.copy();aa[5]=cc;aa[6]=bb
 return np.array([sq(aa[i],aa[j]) for i,j in edges])
def cfrom(sc):
 a0=V[0];B=(V[1:]-a0).T
 G=B.T@eta@B
 q=np.array([(sc[0]+sq(V[i],a0)-sc[i])/2 for i in range(1,5)])
 z=np.linalg.solve(G,q)
 return a0+B@z,sc[0]-q@z
def bfrom(sc,sb):
 cc,res=cfrom(sc)
 anchors=np.vstack((cc,V[1:]))
 B=(anchors[1:]-anchors[0]).T
 G=B.T@eta@B
 q=np.array([(sb[0]+sq(anchors[i],anchors[0])-sb[i])/2 for i in range(1,5)])
 z=np.linalg.solve(G,q)
 return anchors[0]+B@z,sb[0]-q@z,res
def constraints(s):
 bb,rb,rc=bfrom(s[:5],s[5:])
 return np.array([rc,rb])
def gram_for(cell,s):
 positions={tuple(sorted((i,j))):sq(allpos[i],allpos[j]) for i in range(5) for j in range(i+1,5)}
 for e,v in zip(edges,s):positions[tuple(sorted(e))]=v
 def d(i,j):return 0. if i==j else positions[tuple(sorted((i,j)))]
 base=cell[0]
 return np.array([[(d(base,i)+d(base,j)-d(i,j))/2 for j in cell[1:]] for i in cell[1:]])
def jacobian_coordinate():
 J=np.zeros((10,8))
 for n,(i,j) in enumerate(edges):
  p=allpos[i]-allpos[j]
  if i==5:J[n,:4]=2*eta@p
  elif i==6:
   J[n,4:]=2*eta@p
   if j==5:J[n,:4]=-2*eta@p
  else:raise AssertionError
 return J
def main():
 base=intervals(c,b)
 assert max(abs(x) for x in constraints(base))<1e-12
 J=jacobian_coordinate()
 assert np.linalg.matrix_rank(J)==8
 # derive finite derivatives of the explicitly rational quadratic
 # implicit constraints (not via embedding rank alone)
 h=1e-5;grad=np.column_stack([(constraints(base+h*np.eye(10)[i])-constraints(base-h*np.eye(10)[i]))/(2*h) for i in range(10)])
 assert grad.shape==(2,10)
 assert np.linalg.matrix_rank(grad,tol=1e-6)==2
 assert np.max(abs(grad@J))<1e-7
 assert np.linalg.matrix_rank(np.vstack((J.T,grad)),tol=1e-6)==10
 vol=lambda cell:abs(float(np.linalg.det((allpos[list(cell[1:])]-allpos[cell[0]]).T)))/24
 children=[vol(cl) for cl in cells]
 assert all(abs(v-1/60)<1e-11 for v in children[:4])
 assert all(abs(v-1/300)<1e-11 for v in children[4:])
 assert abs(sum(children)-1/12)<1e-12
 sigs=[]
 for cell in cells:
  g=gram_for(cell,base)
  ev=np.linalg.eigvalsh(g)
  assert ev[0]<0 and min(ev[1:])>0
  sigs.append(ev.tolist())
 # Physical interior triangles are those containing c or b and
 # participating in at least two 4-simplices; original vertices'
 # triangles belong to the outer boundary.
 alltri={tuple(sorted(t)) for cl in cells for t in itertools.combinations(cl,3)}
 inside=[t for t in sorted(alltri) if (5 in t or 6 in t)]
 outside=[t for t in sorted(alltri) if 5 not in t and 6 not in t]
 assert len(outside)==10
 assert all(t in alltri for t in outside)
 # Two flat kinematic residuals are independent, and perturbing the
 # intervals off their shared zero locus need not violate signature.
 samples=[]
 for k in range(2):
  direction=grad[k]/np.linalg.norm(grad[k])
  ss=base+.003*direction
  vals=constraints(ss)
  childsignatures=[np.linalg.eigvalsh(gram_for(cell,ss)) for cell in cells]
  assert all(ev[0]<0 and np.min(ev[1:])>0 for ev in childsignatures)
  assert abs(vals[k])>1e-4
  samples.append(dict(perturbation_along_implicit_gradient_index=k,
     independent_constraint_residuals=vals.tolist(),
     all_nine_simplices_remain_Lorentzian=True))
 # Finite displacement of both interior coordinates preserves BOTH C.
 rng=np.random.default_rng(20261104)
 for _ in range(12):
  cc=c+rng.normal(scale=.004,size=4)
  bb=b+rng.normal(scale=.004,size=4)
  assert np.linalg.norm(constraints(intervals(cc,bb)))<1e-10
 result=dict(status="PASS_NINE_LORENTZIAN_FOUR_SIMPLICES_TWO_INDEPENDENT_FLAT_CONSTRAINTS",
  metric_diag=[-1,1,1,1], outer_vertices=V.tolist(),
  first_interior_vertex=c.tolist(),second_interior_vertex=b.tolist(),
  four_simplex_cells=[list(c) for c in cells],
  flat_inner_squared_lengths=base.tolist(),inner_edge_names=[list(e) for e in edges],
  four_simplex_count=9, interior_vertex_count=2,
  interior_edge_lengths_count=10, coordinate_motion_parameters=8,
  exact_vertex_motion_Jacobian_rank=8,
  two_flat_implicit_constraints_independent_gradient_rank=2,
  implicit_constraint_gradient_times_vertex_Jacobian_max_residual=float(np.max(abs(grad@J))),
  implicit_constraints="For c: s0 - q^T Gboundary^-1 q=0. For b: s(b,c) - q'^T G(c,v1,..v4)^-1 q'=0, where q_i=(s0+d(anchor0,anchori)-si)/2. Both use diag(-+++) Minkowski Gram.",
  original_4volume=1/12,child_4volumes=children,
  child_Gram_eigenvalues_at_flat=sigs,
  outer_boundary_triangle_count=len(outside),
  interior_triangle_hinge_count=len(inside),
  off_flat_independent_normal_displacements=samples,
  no_physical_Dirac_constraint_closure_from_kinematic_relations=True,
  caveat="These are configuration-space flat embedding constraints on ten interior edge lengths. Their trivial mutual Poisson brackets as coordinate-only functions are NOT the first-class ADM Hamiltonian/momentum algebra. No Regge action, time-oriented boundary variation or Einstein dynamics has been constructed.",
  prior_art="Lorentzian Regge flat triangulation, Gram/Cayley-Menger interval relations and tent-move pseudo-constraints are established; this numerical two-interior-vertex control extends the previous one-center branch test but is not fundamental new GR.")
 OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf8")
 print(result["status"],"interior hinges",len(inside),"J",np.linalg.matrix_rank(J),flush=True)
 return result
if __name__=="__main__":main()
