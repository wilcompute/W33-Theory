#!/usr/bin/env python3
"""Boundary-complete 9-simplex 4D Regge action: Euclidean exact flat test,
curvature and Lorentzian complex-angle continuation as a failure probe.

Nested 1->5 then 1->5 refinement (9 four-simplices, 2 interior points,
10 internal squared edge lengths, 20 internal triangle hinges).
True Euclidean Regge+GHY boundary action S=sum_int A(2π-Σθ)
+sum_outer A(π-Σθ), compute its first and second derivatives from
actual simplex Gram inverses. Verify Schlaefli finite-difference
gradient, eight flat vertex translation nulls, and curvature lifts.
Lorentzian analytic continuation uses principal complex angle and
area branches with subtractive flat calibration; measure failure,
do NOT assert a correct causal boundary action or ADM brackets.
"""
from __future__ import annotations
import itertools,math,json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261105_nine_simplex_regge_action_hessian_lorentz_diagnostic.json"
V0=np.vstack((np.zeros(4),np.eye(4)))
c0=V0.mean(axis=0);b0=np.mean(np.vstack((c0,V0[1:])),axis=0)
pos0=np.vstack((V0,c0,b0))
VL=np.vstack((np.zeros(4),np.diag([2.,1.,1.,1.])))
cL=VL.mean(axis=0);bL=np.mean(np.vstack((cL,VL[1:])),axis=0)
posL=np.vstack((VL,cL,bL))
parent=(5,1,2,3,4)
cells=[tuple([5]+[i for i in range(5) if i!=omit]) for omit in range(1,5)]+[
 tuple([6]+[i for i in parent if i!=omit]) for omit in parent]
assert len(cells)==9
in_edges=[(5,i) for i in range(5)]+[(6,i) for i in (5,1,2,3,4)]
assert len(in_edges)==10
all_tri=sorted({tuple(sorted(t)) for cell in cells for t in itertools.combinations(cell,3)})
interior=[t for t in all_tri if 5 in t or 6 in t]
boundary=[t for t in all_tri if 5 not in t and 6 not in t]
assert len(interior)==20 and len(boundary)==10
def sqdist(P,metric):
 return {(i,j):float((P[i]-P[j])@metric@(P[i]-P[j])) for i in range(len(P)) for j in range(i+1,len(P))}
def makeD(P,metric,s):
 D={k:v for k,v in sqdist(P,metric).items() if k[0]<5 and k[1]<5}
 D.update({tuple(sorted(e)):float(x) for e,x in zip(in_edges,s)})
 return D
def geometry(s,P,metric,euclidean=True):
 D=makeD(P,metric,s)
 def d(i,j):return 0 if i==j else D[tuple(sorted((i,j)))]
 sums={t:0+0j for t in all_tri}
 area={}
 for t in all_tri:
  i,j,k=t
  u=d(i,j);v=d(i,k);w=d(j,k)
  z=(u+v-w)/2
  discr=u*v-z*z
  if euclidean:
   assert discr>1e-9
   area[t]=math.sqrt(discr)/2
  else:
   assert abs(discr)>1e-8
   area[t]=np.sqrt(complex(discr))/2
 for cell in cells:
  others=list(cell[1:]);base=cell[0]
  G=np.array([[(d(base,i)+d(base,j)-d(i,j))/2 for j in others] for i in others])
  ev=np.linalg.eigvalsh(G)
  if euclidean:assert ev.min()>1e-9
  else: assert ev[0]<-1e-9 and ev[1]>1e-9
  Gi=np.linalg.inv(G)
  N=np.zeros((5,5))
  N[1:,1:]=Gi
  N[0,0]=Gi.sum()
  N[0,1:]=-Gi.sum(axis=0)
  N[1:,0]=-Gi.sum(axis=1)
  for t in itertools.combinations(cell,3):
   excluded=[i for i in range(5) if cell[i] not in t]
   a,b=excluded
   if euclidean:
    cos=-N[a,b]/math.sqrt(N[a,a]*N[b,b])
    theta=math.acos(float(np.clip(cos,-1.,1.)))
   else:
    cos=-N[a,b]/np.sqrt(complex(N[a,a]*N[b,b]))
    theta=np.arccos(complex(cos))
   sums[tuple(sorted(t))]+=theta
 return area,sums,D
def act_euclidean(s):
 A,Th,D=geometry(s,pos0,np.eye(4))
 delta={t:float((2*math.pi-Th[t]).real) for t in interior}
 S=float(sum(A[t]*delta[t] for t in interior)+sum(A[t]*(math.pi-Th[t].real) for t in boundary))
 g=np.zeros(10)
 for ei,(i,j) in enumerate(in_edges):
  for tri in interior:
   if i not in tri or j not in tri:continue
   k=next(z for z in tri if z not in (i,j))
   u=D[tuple(sorted((i,j)))];v=D[tuple(sorted((i,k)))];w=D[tuple(sorted((j,k)))]
   zz=(u+v-w)/2
   g[ei]+=delta[tri]*(v-zz)/(8*A[tri])
 return S,g,delta
def Jcoordinates(P):
 m=np.zeros((10,8));metric=np.eye(4)
 for n,(i,j) in enumerate(in_edges):
  p=P[i]-P[j]
  if i==5:m[n,:4]+=2*metric@p
  if i==6:
   m[n,4:]+=2*metric@p
   if j==5:m[n,:4]-=2*metric@p
 return m
def hessian(s,h=5e-6):
 F=np.eye(10)
 H=np.column_stack([(act_euclidean(s+h*z)[1]-act_euclidean(s-h*z)[1])/(2*h) for z in F])
 return (H+H.T)/2
def main():
 euclidean_s=np.array([sqdist(pos0,np.eye(4))[tuple(sorted(e))] for e in in_edges])
 S0,g,delta=act_euclidean(euclidean_s)
 assert max(abs(z) for z in delta.values())<1e-10
 assert np.linalg.norm(g)<1e-10
 S_expected=3*math.pi/2+4*math.pi*math.sqrt(3)/3
 assert abs(S0-S_expected)<1e-9
 J=Jcoordinates(pos0);assert np.linalg.matrix_rank(J)==8
 H=hessian(euclidean_s)
 ev=np.linalg.eigvalsh(H)
 assert sum(abs(z)<1e-2 for z in ev)==8,(ev,H)
 assert np.linalg.norm(H@J)<1e-2
 assert np.linalg.norm(H-H.T)<1e-10
 # Action itself must differentiate to Schlaefli hinge gradient.
 rng=np.random.default_rng(20261105)
 finite=[]
 for amp in (0,.001,.004):
  _,sv,Vh=np.linalg.svd(J.T,full_matrices=True)
  n=Vh[-1]
  trial=euclidean_s+amp*n
  S,gr,de=act_euclidean(trial)
  fd=np.array([(act_euclidean(trial+1e-6*z)[0]-act_euclidean(trial-1e-6*z)[0])/(2e-6) for z in np.eye(10)])
  err=float(np.max(abs(fd-gr)))
  assert err<1e-5,(amp,err)
  vals=np.linalg.eigvalsh(hessian(trial))
  finite.append(dict(amp=amp,action_change=S-S0,gradient_norm=float(np.linalg.norm(gr)),
   maximum_hinge_deficit=max(abs(x) for x in de.values()),
   Hessian_eigenvalues=vals.tolist(),Schlafli_FD_gradient_residual=err))
 for _ in range(5):
  P=pos0.copy()
  # Keep both nested vertices strictly inside their respective parents;
  # moving b outside the narrow child can create overlapping simplices
  # and false apparent deficits despite flat ambient R4.
  P[5]+=rng.normal(size=4)*.001
  P[6]+=rng.normal(size=4)*.001
  ss=np.array([sqdist(P,np.eye(4))[tuple(sorted(e))] for e in in_edges])
  S,gg,dd=act_euclidean(ss)
  assert abs(S-S0)<1e-9
  assert np.linalg.norm(gg)<1e-6,np.linalg.norm(gg)
  assert max(abs(z) for z in dd.values())<1e-6
 # Lorentzian complex principal branch: diagnose, do not substitute
 # an invented 2pi angle reference in spacelike-boost sectors.
 SL=np.array([sqdist(posL,np.diag([-1.,1.,1.,1.]))[tuple(sorted(e))] for e in in_edges])
 AL,T0,_=geometry(SL,posL,np.diag([-1.,1.,1.,1.]),False)
 def Lrelative(ss):
  A,th,_=geometry(ss,posL,np.diag([-1.,1.,1.,1.]),False)
  return complex(sum(A[t]*(T0[t]-th[t]) for t in all_tri))
 dL=np.array([(Lrelative(SL+1e-6*z)-Lrelative(SL-1e-6*z))/(2e-6) for z in np.eye(10)])
 flatmoves=[]
 for _ in range(5):
  P=posL.copy()
  P[5]+=rng.normal(size=4)*.002
  P[6]+=rng.normal(size=4)*.002
  sl=np.array([sqdist(P,np.diag([-1.,1.,1.,1.]))[tuple(sorted(e))] for e in in_edges])
  flatmoves.append(abs(Lrelative(sl)))
 result=dict(status="PASS_NINE_SIMPLEX_EUCLIDEAN_REGGE_ACTION_8_FLAT_GAUGE_HESSIAN_ZERO_MODES_AND_LORENTZ_DIAGNOSTIC",
  interior_vertices=2,four_simplices=9,interior_hinges=20,boundary_hinges=10,interior_squared_edge_variables=10,
  Euclidean_boundary_complete_S_flat=S0,Euclidean_S_flat_known_outer_value=S_expected,
  Euclidean_flat_Hessian_eigenvalues=ev.tolist(),Euclidean_flat_Hessian_8_tangent_near_null=True,
  Euclidean_flat_internal_vertex_Jacobian_rank=8,Euclidean_flat_Hessian_times_J_norm=float(np.linalg.norm(H@J)),
  off_flat_normal_curvature_and_Hessian=finite,
  Lorentzian_principal_branch_relative_flat_action_gradient_norm=float(np.linalg.norm(dL)),
  Lorentzian_principal_branch_max_flat_vertex_motion_action_residual=float(max(flatmoves)),
  Lorentzian_action_physically_verified=False,
  ADM_Hamiltonian_momentum_constraint_closure_derived=False,
  warning="Euclidean action is genuine Regge+GHY, not Lorentzian causal gravity. Lorentzian complex principal angle branch calibrated by subtracting flat value is only a diagnostic; a correct Lorentzian boundary term, causal boosts and first-class Dirac algebra are NOT established by its residuals.",
  known_prior_art="Regge action variation/Schlafli, flat vertex gauge/null modes and curved pseudo-constraints (Bahr Dittrich 2009); numerical 9-simplex nested control builds on 2026-11-04 one-vertex Euclidean repo action.")
 OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
 print(result["status"],"Euclidean flat Hessian",ev,"Lorentz branch FD",float(np.linalg.norm(dL)),flush=True)
 return result
if __name__=="__main__":main()
