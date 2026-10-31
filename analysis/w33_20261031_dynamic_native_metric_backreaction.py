#!/usr/bin/env python3
"""Finite Hamiltonian conformal-metric backreaction on native W33 acoustic metric.

A conditional positive coupled scalar model, not Einstein gravity:
both time and spatial periodic cover are supplied.
"""
from __future__ import annotations
import json,math
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_20261031_dynamic_native_metric_backreaction.json"
Q=np.array([[5,2.5,-3,0],[2.5,5,0,-3],[-3,0,6,-3],[0,-3,-3,6]],float)
assert np.min(np.linalg.eigvalsh(Q))>0

def forward(u):
    return np.stack([np.roll(u,-1,axis=i)-u for i in range(4)],axis=-1)
def backward(v):
    return np.stack([v[...,i]-np.roll(v[...,i],1,axis=i) for i in range(4)],axis=-1)
def controls(u,phi,alpha,kappa,mu2):
    du=forward(u)
    density=np.einsum("...i,ij,...j->...",du,Q,du)
    eg=np.exp(2*alpha*phi)
    flux=eg[...,None]*np.einsum("ij,...j->...i",Q,du)
    au=np.sum(backward(flux),axis=-1)
    lap=sum(np.roll(phi,-1,axis=i)+np.roll(phi,1,axis=i)-2*phi for i in range(4))
    aphi=-alpha*eg*density+kappa*lap-mu2*phi
    return au,aphi
def energy(u,phi,pu,pp,alpha,kappa,mu2):
    d=forward(u);g=forward(phi)
    ed=np.exp(2*alpha*phi)*np.einsum("...i,ij,...j->...",d,Q,d)
    return .5*float(np.sum(pu**2+pp**2+ed+kappa*np.sum(g*g,axis=-1)+mu2*phi**2))
def initial(N):
    coord=np.indices((N,)*4)
    r2=np.zeros((N,)*4)
    for i in range(4):
        d=abs(coord[i]-N//2)
        r2+=np.minimum(d,N-d)**2
    return .12*np.exp(-r2/1.5)

def trajectory(N,alpha=.3,dt=.01,steps=160):
    kappa,mu2=.4,.3
    u=initial(N);phi=np.zeros_like(u)
    pu=np.zeros_like(u);pp=np.zeros_like(u)
    E0=energy(u,phi,pu,pp,alpha,kappa,mu2)
    _,aphi=controls(u,phi,alpha,kappa,mu2)
    initial_source=float(np.linalg.norm(aphi))
    if alpha:assert initial_source>0
    else:assert initial_source==0
    snapshots=[]
    for i in range(steps):
        au,ap=controls(u,phi,alpha,kappa,mu2)
        pu+=dt*.5*au;pp+=dt*.5*ap
        u+=dt*pu;phi+=dt*pp
        au,ap=controls(u,phi,alpha,kappa,mu2)
        pu+=dt*.5*au;pp+=dt*.5*ap
        if (i+1)%40==0:
            E=energy(u,phi,pu,pp,alpha,kappa,mu2)
            snapshots.append({"step":i+1,"energy":E,
                "relative_energy_drift":(E-E0)/E0,
                "metric_field_norm":float(np.linalg.norm(phi)),
                "physical_positivity_min_exp2alpha_phi":float(np.min(np.exp(2*alpha*phi)))})
    assert max(abs(s["relative_energy_drift"]) for s in snapshots)<.001
    if alpha:assert snapshots[-1]["metric_field_norm"]>1e-5
    else:assert snapshots[-1]["metric_field_norm"]<1e-12
    return {"N":N,"alpha":alpha,"dt":dt,"steps":steps,"initial_energy":E0,
            "initial_backreaction_source_norm":initial_source,
            "snapshots":snapshots}

def finite_differences():
    rng=np.random.default_rng(20261031);N=4
    u=.03*rng.normal(size=(N,)*4);phi=.03*rng.normal(size=(N,)*4)
    pu=np.zeros_like(u);pp=np.zeros_like(u)
    alpha,kappa,mu2=.3,.4,.3
    au,ap=controls(u,phi,alpha,kappa,mu2)
    e=1e-6
    spot=(1,2,0,3)
    v=u.copy();v[spot]+=e
    w=u.copy();w[spot]-=e
    du=(energy(v,phi,pu,pp,alpha,kappa,mu2)-energy(w,phi,pu,pp,alpha,kappa,mu2))/(2*e)
    v=phi.copy();v[spot]+=e
    w=phi.copy();w[spot]-=e
    dp=(energy(u,v,pu,pp,alpha,kappa,mu2)-energy(u,w,pu,pp,alpha,kappa,mu2))/(2*e)
    assert abs(du+au[spot])<1e-7
    assert abs(dp+ap[spot])<1e-7
    return {"finite_difference_force_u_error":abs(du+au[spot]),
        "finite_difference_force_phi_error":abs(dp+ap[spot])}

def build():
    trials=[trajectory(N,a) for N in (4,6) for a in (0.,.3)]
    controls_check=finite_differences()
    return {"status":"PASS_CONDITIONAL_DYNAMICAL_CONFORMAL_METRIC_BACKREACTION",
      "native_Q":Q.tolist(),
      "Hamiltonian":"H=1/2 sum_x [p_u^2+p_phi^2 + exp(2a phi) (D u)^T Q (D u) + kappa sum_mu(D_mu phi)^2 + mu^2 phi^2], with kappa=.4, mu2=.3",
      "discrete_gradient":"D_mu u(x)=u(x+e_mu)-u(x); D^dag is negative backward difference; coupled force from exact Hamiltonian derivative",
      "positivity":"Q positive definite, exp(2a phi)>0, kappa>0, mu2>0 => bounded-below positive classical Hamiltonian",
      "strict_locality":"Each explicit leapfrog step uses a spatial stencil with lattice L1 support <=2, and the conformal field responds locally to matter-gradient energy.",
      "force_gradient_verification":controls_check,
      "runs":trials,
      "physics_scope":"Externally chosen periodic four-dimensional spatial cover, continuous Hamiltonian time, conformal metric ansatz and kinetic couplings. This is not GR, no dynamical spin-2 graviton, Einstein constraints, Lorentz invariance derivation, or particle-spectrum prediction."}
if __name__=="__main__":
    d=build();OUT.write_text(json.dumps(d,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"status":d["status"],"runs":[
       {"N":r["N"],"alpha":r["alpha"],"drift":r["snapshots"][-1]["relative_energy_drift"],
       "metric_norm":r["snapshots"][-1]["metric_field_norm"]}for r in d["runs"]]},sort_keys=True))
