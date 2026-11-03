#!/usr/bin/env python3
"""Eight-front continuation, part B: noisy 216-port Naimark receiver, detector
gain twirling, and a six-outcome simplex coarse-grained POVM test."""
from __future__ import annotations
import sys,gzip,json,math
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261102_five_deeper_fronts import route_frame
from w33_20261102_route_216_cubic_tomography import geometry

def prepare():
  Z,N=route_frame()
  es,vt=np.linalg.eigh((Z.T@Z).astype(float))
  V=Z@vt[:,16:]/math.sqrt(360)
  for k in range(24):
    j=np.argmax(abs(V[:,k]))
    if V[j,k]<0:V[:,k]*=-1
  with gzip.open(ROOT/"data/w33_20261102_adjacent_givens_mesh.json.gz","rt") as f:j=json.load(f)
  assert len(j["rotations"])==4884
  S=3*V.T
  baseline=(V@S)**2
  assert np.max(abs(baseline.sum(axis=0)-1))<2e-12
  return Z,V,S,j["rotations"],baseline

def lossy_mesh(V,S,rotations,baseline):
  rng=np.random.default_rng(20261102)
  ret=[]
  settings=[
    ("ideal",1.,0.,0.,0.,1.,0.),
    ("loss_only",0.999,0.,0.,0.,.85,0.),
    ("calibration",.999,0.001,0.001,0.,.85,1e-6),
    ("phase_crosstalk",.999,0.001,0.001,0.0004,.85,1e-6),
    ("harsh_loss",.995,0.001,0.001,0.001,.85,1e-6),
  ]
  for name,eta,phase_sd,angle_sd,cross_sd,detect,dark in settings:
    scores=[]
    for k in range(3):
      X=np.zeros((216,24),dtype=np.complex128)
      X[:24]=np.eye(24)
      for a,c,s in reversed(rotations):
        theta=math.atan2(s,c)+rng.normal(0,angle_sd)
        cc,ss=math.cos(theta),math.sin(theta)
        a=int(a)
        u=X[a].copy();v=X[a+1].copy()
        X[a]=math.sqrt(eta)*(cc*u-ss*v)
        X[a+1]=math.sqrt(eta)*(ss*u+cc*v)*np.exp(1j*rng.normal(0,phase_sd))
        if cross_sd:
          phi=rng.normal(0,cross_sd)
          y=X[a].copy();z=X[a+1].copy()
          X[a]=math.cos(phi)*y+1j*math.sin(phi)*z
          X[a+1]=1j*math.sin(phi)*y+math.cos(phi)*z
      P=np.abs(X@S)**2
      eff=detect*P
      obs=eff+dark*(1-eff) # expected per-detector counts, NOT single-click probabilities
      cols=obs.sum(0)
      conditioned=obs/cols
      tv=0.5*np.abs(conditioned-baseline).sum(0)
      survival=P.sum(0)
      scores.append((float(survival.mean()),float(survival.min()),
          float(np.mean(tv)),float(np.max(tv)),float(cols.mean())))
      assert np.max(survival)<1+1e-8
    ret.append({"label":name,"per_active_two_rail_transmission":eta,"detector_efficiency":detect,
     "detector_dark_click_probability_per_output_per_shot":dark,"angle_sigma":angle_sd,"phase_sigma":phase_sd,
     "extra_crosstalk_sigma":cross_sd,"n_trials":3,
     "mean_single_photon_survival":float(np.mean([v[0] for v in scores])),
     "worst_case_single_photon_survival":float(min(v[1] for v in scores)),
     "mean_conditional_total_variation":float(np.mean([v[2] for v in scores])),
     "max_conditional_total_variation":float(max(v[3] for v in scores)),
     "mean_expected_detector_clicks_per_shot":float(np.mean([v[4] for v in scores]))})
  assert ret[0]["mean_conditional_total_variation"]<1e-10
  return {"scenarios":ret,"scope":"loss/phase/angle/crosstalk and dark counts are illustrative noise assumptions; normalized expected click counts NOT physical multi-click heralding or hardware characterization"}

def detector_twirling(Z):
  pts,lines,N,idx,norm,omega=geometry()
  signs={tuple(int(x) for x in z):i for i,z in enumerate(Z)}
  generators=[]
  for a in pts:
    gp=[idx[norm(tuple((x[k]+omega(x,a)*a[k])%3 for k in range(4)))] for x in pts]
    p=np.array([signs[tuple(int(z[gp.index(i)]) for i in range(40))] for z in Z],dtype=int)
    # verify each generator is a permutation and preserves the 216x216 geometry
    assert len(set(map(int,p)))==216
    assert np.array_equal(Z[p],Z[:,np.argsort(gp)])
    generators.append(p)
  rng=np.random.default_rng(20261103)
  gain=1+0.08*rng.normal(size=216)
  gain=np.maximum(gain,0.6)
  walk=np.arange(216)
  av=np.zeros(216)
  counts=0
  for i in range(3000):
    g=generators[int(rng.integers(len(generators)))]
    walk=g[walk]
    if i%4==0:
      av+=gain[walk];counts+=1
  av/=counts
  return {"systematic_detector_gain_std_before":float(np.std(gain)),
    "mean_gain":float(np.mean(gain)),"symmetry_twirl_gain_std_after":float(np.std(av)),
    "number_of_symmetry_walk_samples":counts,
    "max_residual_gain_offset":float(np.max(abs(av-gain.mean()))),
    "scope":"hypothetical reconfigurable physical output switching by route automorphisms; mere software relabeling cannot remove detector bias"}

def simplex_spectral_test(Z):
  G=Z@Z.T
  # Every row has exactly five other vectors with -8 inner product within its
  # own known simplex, but many external -8 partners as well.
  deg=int(np.sum(G[0]==-8))
  assert deg>5
  # Check that every regular 6-simplex block *would* yield a 5D projector
  # and six equally weighted rank-one conditional outcomes.
  # Explicit partition is owned by Pass 12526; this is a local numerical
  # six-vector existence witness, not a full 36-group reconstruction.
  from itertools import combinations
  neigh=np.flatnonzero(G[0]==-8)
  six=None
  for a in neigh:
    cand=[int(v) for v in neigh if v>a and G[a,v]==-8]
    for b in cand:
      cand2=[v for v in cand if v>b and G[b,v]==-8]
      for c in cand2:
        cand3=[v for v in cand2 if v>c and G[c,v]==-8]
        for d in cand3:
          for e in cand3:
            if e>d and G[d,e]==-8:
              possible=[0,int(a),int(b),int(c),int(d),int(e)]
              small=Z[possible]
              if np.all(small@small.T==48*np.eye(6,dtype=np.int64)-8*np.ones((6,6),dtype=np.int64)):
                six=possible;break
          if six:break
        if six:break
      if six:break
    if six:break
  if six is None: return {"status":"EXPLICIT_SIX_NOT_FOUND","search_scope":"greedy local limited clique search"}
  W=Z[six].astype(float)
  es=np.linalg.eigvalsh(W@W.T)
  assert np.max(abs(es[0]))<1e-8 and np.max(abs(es[1:]-48))<1e-8
  # u_s=Z_s / sqrt(40) in 40D; E_s=(1/9)u_s u_s.T
  # sum E_s across simplex = (48/360) P5 = 2/15 P5
  return {"status":"EXPLICIT_6_VECTOR_SIMPLEX_WITNESS","route_indices":six,
    "simplex_gram_diagonal":40,"simplex_gram_offdiag":-8,
    "simplex_sum_POVM": "sum_{six} E_s = (2/15) P5",
    "simplex_projector_rank":5,
    "scope":"local six-frame verification, distinct from pre-existing full 36-simplex partition; sequential coarse-fine instrument still requires implementation"}

def main():
 Z,V,S,rot,B=prepare()
 out={}
 for name,fn in (("optical_noise",lambda:lossy_mesh(V,S,rot,B)),
                 ("detector_twirling",lambda:detector_twirling(Z)),
                 ("simplex_coarse_fine",lambda:simplex_spectral_test(Z))):
  out[name]=fn();print("DONE",name,json.dumps(out[name])[:1800],flush=True)
 out["status"]="PASS_MESH_TWIRL_AND_SIMPLEX_EXPLORATION"
 p=ROOT/"data/w33_20261102_eightfront_partB.json"
 p.write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
 return out
if __name__=="__main__":main()
