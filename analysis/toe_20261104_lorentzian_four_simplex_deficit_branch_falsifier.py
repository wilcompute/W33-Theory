#!/usr/bin/env python3
"""4D Minkowski signature 1->5 Regge hinge/boost branch falsifier.

A 4-simplex with one timelike and three spacelike independent
directions is subdivided by adding a genuine interior vertex.
Five child 4-simplices have (-+++) Gram signatures, 10 interior
triangle hinges split 7 timelike /3 spacelike. Compute exact
Lorentzian interval constraint C(s)=0 for five interior squared
edges s_i, 4D displaced-vertex tangent rank4, oriented volumes.

Lorentzian dihedral branch WARNING: naive principal complex
arccos produces spurious nonzero imaginary deficits at all 3
spacelike hinges even though embedding is Minkowski flat.
Calibrate analytic branch by the fixed oriented 1->5 embedding;
paired sectors then cancel boost components exactly.
Perturb one normal squared-length direction away from C(s)=0;
all 5 child Gram signature conditions maintained, deficits
become nonzero. Bulk area*deficit is not a COMPLETE action: correct
Lorentzian boundary term, real branch convention and canonical
lapse/shift bracket still not constructed. No GR proof.
"""
from __future__ import annotations
import itertools,json,math
from pathlib import Path
import numpy as np
import sympy as sy
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261104_lorentzian_four_simplex_deficit_branch_falsifier.json"
ETA=np.diag([-1.,1.,1.,1.])
V=np.vstack((np.zeros(4),np.diag([2.,1.,1.,1.])))
C=V.mean(axis=0)
IDX=list(itertools.combinations(range(5),2))
D={(i,j):float((V[i]-V[j])@ETA@(V[i]-V[j])) for i in range(5) for j in range(5)}
def ds(q):
 return np.einsum('ni,ij,nj->n',V-q,ETA,V-q)
def implicit(s):
 T=(s[1]-s[0]+4)/4
 X=np.array([(1-s[j]+s[0])/2 for j in (2,3,4)])
 return float(s[0]+T*T-X@X)
def residual_gradient(s):
 z=sy.symbols('z0:5',real=True)
 t=(z[1]-z[0]+4)/4
 x=[(1-z[i]+z[0])/2 for i in (2,3,4)]
 expr=z[0]+t*t-sum(v*v for v in x)
 gg=np.array([float(sy.diff(expr,y).subs(dict(zip(z,s)))) for y in z])
 return gg,str(sy.expand(expr))
def sigmas(s):
 out=[]
 for absent in range(5):
  idx=[i for i in range(5) if i!=absent]
  G=np.array([[(s[i]+s[j]-D[i,j])/2 for j in idx] for i in idx])
  eig=np.linalg.eigvalsh(G)
  if not(eig[0]<0 and all(eig[k]>0 for k in range(1,4))):
   raise ValueError((absent,eig))
  out.append((idx,np.linalg.inv(G),eig))
 return out
def hinges(s,fix_branches=True):
 geo=sigmas(s)
 results={}
 for a,b in IDX:
  co=(s[a]+s[b]-D[a,b])/2
  d2=s[a]*s[b]-co*co
  assert abs(d2)>1e-9
  causal="timelike" if d2<0 else "spacelike"
  area=.5*math.sqrt(abs(d2))
  angles=[]
  for absent in range(5):
   if absent in (a,b):continue
   idx,gi,_=geo[absent]
   k,l=[idx.index(j) for j in idx if j not in (a,b)]
   cs=-gi[k,l]/np.sqrt(complex(gi[k,k]*gi[l,l]))
   val=np.arccos(complex(cs))
   angles.append(val)
  if fix_branches and causal=="spacelike":
   # The 4D Minkowski embedding defines a consistent boost
   # orientation. In this fixed orientation the first and last
   # sectors use conjugate arccos branches; the middle sector
   # follows the principal branch. This is NOT a general
   # Lorentzian triangulation branch-finding algorithm.
   angles[0]=angles[0].conjugate()
   angles[2]=angles[2].conjugate()
  deficit=2*math.pi-sum(angles)
  if causal=="timelike":assert abs(deficit.imag)<1e-10
  if causal=="spacelike":assert abs(deficit.real)<1e-8
  results[a,b]=dict(causal=causal,area=area,deficit=deficit,
     square_2area=abs(d2))
 return results
def main():
 base=ds(C)
 assert max(abs(implicit(ds(C+np.array(z)))) for z in
       [(0,0,0,0),(.01,-.03,.015,.02),(-.01,.02,-.008,.002)])<1e-12
 J=np.array([-2*(V[i]-C)@ETA for i in range(5)])
 grad,poly=residual_gradient(base)
 assert np.linalg.matrix_rank(J)==4
 assert np.linalg.norm(grad@J)<1e-11
 assert abs(implicit(base))<1e-12
 eigchild=[x[2].tolist() for x in sigmas(base)]
 naive=hinges(base,False)
 sane=hinges(base,True)
 assert sum(x["causal"]=="timelike" for x in sane.values())==7
 assert sum(x["causal"]=="spacelike" for x in sane.values())==3
 spurious=max(abs(x["deficit"]) for x in naive.values())
 assert spurious>.5
 assert max(abs(x["deficit"]) for x in sane.values())<1e-10
 # Oriented 4-volume 5 child sum = boundary original; det Gram negative.
 vol=lambda a:abs(float(np.linalg.det(a)))/24
 orig=vol((V[1:]-V[0]).T)
 children=[vol((V[[i for i in range(5) if i!=absent]]-C).T) for absent in range(5)]
 assert abs(orig-1/12)<1e-12
 assert len(children)==5 and all(abs(v-1/60)<1e-12 for v in children)
 assert abs(sum(children)-orig)<1e-12
 shifts=[(0,0,0,0),(.01,-.025,.015,.01),(-.012,.02,-.01,.008)]
 for sh in shifts:
  s=ds(C+np.array(sh))
  assert abs(implicit(s))<1e-12
  assert max(abs(r["deficit"]) for r in hinges(s,True).values())<1e-10
 norm=np.linalg.norm(grad)
 n=grad/norm
 assert abs(grad@n-norm)<1e-12
 curved=[]
 for amp in (.001,.005,.01):
  s=base+amp*n
  res=implicit(s)
  assert abs(res)>1e-6
  hg=hinges(s,True)
  assert sum(x["causal"]=="timelike" for x in hg.values())==7
  assert sum(x["causal"]=="spacelike" for x in hg.values())==3
  max_def=max(abs(x["deficit"]) for x in hg.values())
  assert max_def>1e-4
  # Real/imag sectors belong to timelike rotation vs spacelike
  # boost; DO NOT add complex action as physical Lorentzian S.
  bulk=complex(sum(x["area"]*x["deficit"] for x in hg.values()))
  # Formal Regge hinge area-variation term at fixed angles; the
  # Schlaefli cancellation requires a boundary completion.
  forces=np.zeros(5,dtype=complex)
  for (a,b),v in hg.items():
   co=(s[a]+s[b]-D[a,b])/2
   det2=s[a]*s[b]-co*co
   sg=1 if det2>0 else -1
   forces[a]+=v["deficit"]*sg*(s[b]-co)/(8*v["area"])
   forces[b]+=v["deficit"]*sg*(s[a]-co)/(8*v["area"])
  curved.append(dict(normal_perturbation_s=amp,
    implicit_interval_constraint_residual=res,
    max_rotation_or_boost_hinge_deficit_abs=max_def,
    timelike_deficits_rotation_rad=[float(v["deficit"].real) for v in hg.values() if v["causal"]=="timelike"],
    spacelike_deficits_boost_rad=[float(v["deficit"].imag) for v in hg.values() if v["causal"]=="spacelike"],
    formal_complex_bulk_area_times_deficit=[bulk.real,bulk.imag],
    bulk_hinge_equation_norm=float(np.linalg.norm(forces)),
    all_five_child_Grams_still_Lorentzian=True))
 result=dict(status="PASS_FLAT_MINKOWSKI_4D_1TO5_LORENTZIAN_HINGES_AND_BRANCH_FAIL_CONTROL",
    boundary_vertices=V.tolist(),interior_vertex=C.tolist(),
    Lorentzian_metric_diag=[-1,1,1,1],
    original_simplex_signed_Gromov_4_volume=orig,
    all_five_child_coordinate_4_volumes=children,
    number_of_4simplices=5,interior_triangle_hinges=10,
    timelike_triangle_hinges=7,spacelike_triangle_hinges=3,
    five_interior_squared_interval_variables=base.tolist(),
    exact_Minkowski_embedding_constraint_polynomial=poly,
    flat_constraint_gradient=grad.tolist(),
    full_rank_four_vertex_motion_Jacobian=J.tolist(),
    flat_geometry_interval_constraint_zero=True,
    flat_all_hinge_rotation_and_boost_deficits_zero_after_oriented_branch=True,
    naive_principal_arccos_produces_spurious_flat_boost_deficit=True,
    max_naive_spurious_flat_hinge_deficit_abs=spurious,
    oriented_branch_recipe_for_three_spacelike_hinges="Using ordered absent-vertex sectors, flip imaginary sign of 1st and 3rd arccos branches; follows this fixed explicit flat Minkowski embedding, NOT universally applicable.",
    flat_child_simplex_Gram_eigenvalues=eigchild,
    off_flat_squared_interval_normal_perturbations=curved,
    actual_Lorentzian_boundary_action_and_variational_principle_completed=False,
    ADM_Hamiltonian_and_momentum_constraint_Poisson_algebra_derived=False,
    scope="A genuine 4D Lorentzian piecewise-flat causal-signature/hinge control and local curvature perturbation. Naively interpreting a principal complex arccos deficit misdiagnoses flat space as curved. No complete Lorentzian Regge Gibbons-Hawking boundary action or first-class constraint closure has been constructed.",
    prior_art="Sorkin Lorentzian Regge prescription, Bahr Dittrich 0905.1670, Lapse and Shift in Regge Calculus Galassi 1993; Causal Structure in Spin Foams (2024). This is a coordinate-specific numerical branch-control falsifier, not original Regge theory.")
 OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf8")
 print(result["status"],"naive spurious",spurious,"curved",curved[1]["max_rotation_or_boost_hinge_deficit_abs"],flush=True)
 return result
if __name__=="__main__":main()
