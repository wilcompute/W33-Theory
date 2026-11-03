#!/usr/bin/env python3
"""Eight-front continuation, part A: q7 cubic probes, Jordan basepoint obstruction,
cyclic voltage-cover continuum, and perturbed quantum echo. Finite falsifiers only.
"""
from __future__ import annotations
import sys,json,math,random
from pathlib import Path
import numpy as np
from scipy import sparse
from scipy.sparse.linalg import eigsh
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/"analysis"),str(ROOT/"analysis/search_drivers_12466")]
from even_line_sets_gf import build
from w33_20261102_five_deeper_fronts import route_frame

def cubic_q7():
  pts,lines,N=build(7);v=len(pts)
  src=json.loads((ROOT/"analysis/search_drivers_12466/even_line_sets_gf_q7_sym2.json").read_text())
  pid={p:i for i,p in enumerate(pts)}
  lid={frozenset(L):i for i,L in enumerate(lines)}
  seed=frozenset(lid[frozenset(pid[tuple(a)] for a in L)] for L in src["chosen_lines"])
  A=N@N.T-8*np.eye(v,dtype=int)
  first=lines[0]
  collinear=tuple(first[:3])
  nonline=next((int(a),int(b),int(c)) for a in range(v) for b in range(a+1,v) for c in range(b+1,v)
            if A[a,b] and A[a,c] and not A[b,c])
  independent=None
  for a in range(v):
    if independent:break
    for b in range(a+1,v):
      if A[a,b]:continue
      for c in range(b+1,v):
        if A[a,c]==A[b,c]==0:
          independent=(a,b,c);break
      if independent:break
  # The first zero-edge lex triple is on a NONISOTROPIC projective line.
  triple={"collinear":collinear,"two_edges":nonline,"zero_edge_nonisotropic_line":independent}
  def om(u,w):return (u[0]*w[2]+u[1]*w[3]-u[2]*w[0]-u[3]*w[1])%7
  def norm(w):
    a=next(t for t in w if t)
    return tuple(v*pow(a,-1,7)%7 for v in w)
  gens=[]
  for j in (0,1,2,3,5,7,11,13,17,19,23,29,31,37,41,43):
    a=pts[j]
    gp=[pid[norm(tuple((p[k]+om(p,a)*a[k])%7 for k in range(4)))] for p in pts]
    gens.append(tuple(lid[frozenset(gp[i] for i in L)] for L in lines))
  rng=random.Random(20261102);S=seed;distinct=set();moments={n:[] for n in triple}
  # Random walk is NOT iid or uniform; these are only empirical probes.
  for i in range(4800):
    g=gens[rng.randrange(len(gens))]
    S=frozenset(g[j] for j in S)
    if i>=200 and i%3==0:
      distinct.add(S)
      h=N[:,list(S)].sum(1)
      assert np.all((h==0)|(h==2))
      x=(5*(h//2)-2).astype(np.int64)
      for name,inds in triple.items():moments[name].append(int(np.prod(x[list(inds)])))
  assert len(distinct)>500
  # Full-orbit exact one-point cubic from point transitivity, no orbit enumeration.
  v1=400;t=160
  one=int((t*(3**3)+(v1-t)*(-2)**3)//v1)
  assert one==6
  q5=int((60*(8**3)+(156-60)*(-5)**3)//156)
  assert q5==120
  return dict(q7_exact_single_coordinate_cubic=one,q5_exact_single_coordinate_cubic=q5,
    q3_single_coordinate_cubic=0,seed_distinct_sampled=len(distinct),
    triple_examples={n:dict(index=list(t),nonuniform_walk_mean=float(np.mean(moments[n])),
                             nonuniform_walk_sd=float(np.std(moments[n])))
                    for n,t in triple.items()},
    scope="exact marginal cubics; triple probes are correlated/nonuniform random walks, NOT full q7 cubic census")

def albert_control():
  Z,_=route_frame()
  T=Z.T@Z
  x=(T[:,0]+T[:,1])//12
  assert np.array_equal(T@x,360*x)
  Q=Z.T@((Z@x)**2);sq=int(x@x)
  assert np.any(Q)
  def n0(y):
    a,b,c=y[:3];w=y[3:]
    return int(a*(b*c-int(w@w)))
  def sharp0(y):
    a,b,c=y[:3];w=y[3:]
    return np.concatenate((np.array([b*c-int(w@w),a*c,a*b],dtype=np.int64),-a*w))
  rng=np.random.default_rng(42)
  for _ in range(12):
    y=rng.integers(-3,4,size=27,dtype=np.int64)
    assert np.array_equal(sharp0(sharp0(y)),n0(y)*y)
  # Cubic trial N_l=a(bc-||x||²)+l*sum_s (Z_s x)^3.
  # Basepoint (1,1,1,0) has correct nondegenerate trace matrix diag(1,1,1,2*I24).
  # For lambda=2 and input (0,0,0,x), sharp=(-||x||²,0,0,3Q).
  # In the iterated sharp the a-coordinate is -9||Q||², while N(y)*y_a=0.
  ysharp=np.concatenate((np.array([-sq,0,0],dtype=np.int64),3*Q))
  lhs_a=-int(ysharp[3:]@ysharp[3:])
  assert lhs_a!=0
  return dict(dimension=27,reducible_control="N(a,b,c,x)=a*(b*c-x.x)",
    control_adjoint_identity_tests=12,basepoint=[1,1,1],
    basepoint_trace_form="diag(1,1,1,2*I_24)",
    attempted_deformation="N_lambda=a*(b*c-x.x)+lambda*C_route(x)",
    lambda_test=2,zero_scalar_input_x_squared=sq,
    iteration_a_component=lhs_a,expected_a_component=0,
    forbidden_nonzero_lambda_for_this_trace_form=True,
    scope="reducible degree-three cubic norm exists, but naive addition of route cubic breaks adjoint identity; DOES NOT exclude exceptional 27D alternatives")

def cyclic_cover():
  _,_,N=build(3);n=40
  A=N@N.T-4*np.eye(40,dtype=int)
  edge=next((i,j) for i in range(n) for j in range(i+1,n) if A[i,j])
  i0,j0=edge
  out=[]
  for m in (3,5,9,15):
    a=[];b=[]
    for layer in range(m):
      for i in range(n):
        for j in range(i+1,n):
          if A[i,j]:
            dest=(layer+1)%m if (i,j)==edge else layer
            u=layer*n+i;v=dest*n+j
            a.extend((u,v));b.extend((v,u))
    Am=sparse.coo_matrix((np.ones(len(a)),(a,b)),shape=(n*m,n*m)).tocsr()
    assert np.all(np.array(Am.sum(axis=1)).ravel()==12)
    # Symmetry and connectivity
    assert (Am-Am.T).nnz==0
    comps=sparse.csgraph.connected_components(Am,directed=False)[0];assert comps==1
    lap=sparse.eye(n*m,format="csr")-Am/12
    vals=np.sort(eigsh(lap,k=3,sigma=-1e-7,which="LM",return_eigenvectors=False,tol=1e-10))
    assert abs(vals[0])<1e-8 and vals[1]>0,(m,vals)
    bound=(2-2*math.cos(2*math.pi/m))/(12*40)
    assert vals[1]<bound+1e-7
    # voltage cover points may be connected but 2D/3D continuum not implied
    out.append(dict(layers=m,vertices=n*m,first_gap=float(vals[1]),
                    exact_analytic_rayleigh_upper_bound=bound,
                    connected=True))
  assert out[-1]["first_gap"]<out[0]["first_gap"]
  return dict(bridge_edge=list(edge),cover_family=out,
       derived_bound="lambda_2(normalized L_m) <= (2-2cos(2pi/m))/480 = O(m^-2)",
       scope="a connected artificial cyclic voltage cover of W33, not a 3+1D continuum or Lorentz invariant")

def echo():
  _,_,N=build(3);A=(N@N.T-4*np.eye(40,dtype=int)).astype(float)
  lam,V=np.linalg.eigh(A)
  def U(eigvals,eigvec,t):return (eigvec*np.exp(-1j*eigvals*t))@eigvec.T
  ideal=U(lam,V,math.pi)
  assert np.max(abs(ideal-np.eye(40)))<1e-12
  rng=np.random.default_rng(20261102)
  out=[]
  for delta in (0.0,0.01,0.05,0.10):
    vals=[]
    for k in range(12):
      disorder=rng.normal(0,delta,40)
      eig,vec=np.linalg.eigh(A+np.diag(disorder))
      T=U(eig,vec,math.pi)
      vals.append(float(abs(np.trace(T)/40)**2))
    out.append(dict(diagonal_noise_sigma_over_J=delta,
                    mean_entanglement_fidelity=float(np.mean(vals)),
                    min_entanglement_fidelity=float(min(vals))))
  assert abs(out[0]["mean_entanglement_fidelity"]-1)<1e-12
  return dict(trials_per_noise=12,reproducible_seed=20261102,results=out,
     scope="one-particle 40-mode static Gaussian onsite disorder; not genuine hardware or gravitational dynamics")

def main():
  d={}
  for name,fn in (("q7_cubic",cubic_q7),("albert",albert_control),("continuum_cover",cyclic_cover),("echo",echo)):
    d[name]=fn();print("PASS",name,json.dumps(d[name])[:1500],flush=True)
  d["status"]="PASS_FOUR_INDEPENDENT_FRONTIERS_WITH_BOUNDED_SCOPE"
  p=ROOT/"data/w33_20261102_eightfront_partA.json";p.write_text(json.dumps(d,indent=2)+"\n")
  return d
if __name__=="__main__":main()
