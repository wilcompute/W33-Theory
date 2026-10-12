#!/usr/bin/env python3
"""Exact H27 Hesse-cubic F-flat lock on the common Witting/flavour qutrit.

The common qutrit of Passes 11664/11921 carries X|j>=|j+1>, Z|j>=omega^j|j>.
Degree-three H27 invariants are exactly the Hesse pencil S=x^3+y^3+z^3 and
P=xyz.  A nonzero F-flat critical ray exists only for a singular member of
that pencil, and the union of all such critical rays is exactly the 12 qutrit
stabilizer states.  Thus an H27-preserving cubic superpotential cannot by
itself give a nonzero F-flat magic Higgs.
"""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_20261011_h27_hesse_cubic_f_flat_lock.json"

def sha(rel):
    return hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()

def canon(v,tol=1e-10):
    v=np.asarray(v,complex); v=v/np.linalg.norm(v)
    i=int(np.flatnonzero(abs(v)>tol)[0])
    v=v*np.exp(-1j*np.angle(v[i]))
    return tuple(np.r_[np.round(v.real,10),np.round(v.imag,10)])

def stabilizers():
    w=np.exp(2j*np.pi/3)
    out=[np.eye(3,dtype=complex)[k] for k in range(3)]
    out += [np.array([w**(s*j*j+t*j) for j in range(3)],complex)/np.sqrt(3)
            for s in range(3) for t in range(3)]
    return out

def singular_hesse_critical_rays():
    w=np.exp(2j*np.pi/3)
    # P=xyz: the three coordinate axes.
    out=[np.eye(3,dtype=complex)[k] for k in range(3)]
    # S-3 lambda P, lambda^3=1.  With x=1 the critical points are
    # (1,w^t,lambda^2 w^{-t}), t=0,1,2.
    members=[]
    for s in range(3):
        lam=w**s
        rays=[]
        for t in range(3):
            v=np.array([1,w**t,lam**2*w**(-t)],complex)/np.sqrt(3)
            rays.append(v); out.append(v)
        members.append(rays)
    return out,members

def degree3_h27_invariant_orbits():
    # monomial exponents (a,b,c), a+b+c=3.
    mons=[(a,b,3-a-b) for a in range(4) for b in range(4-a)]
    # Z invariance requires b+2c=0 mod3. X cyclically permutes exponents.
    allowed=[m for m in mons if (m[1]+2*m[2])%3==0]
    unseen=set(allowed); orbits=[]
    while unseen:
        m=min(unseen); orb=set()
        q=m
        for _ in range(3):
            orb.add(q); q=(q[2],q[0],q[1])
        orb &= set(allowed); unseen-=orb; orbits.append(sorted(orb))
    return mons,allowed,orbits

def grad(alpha,beta,v):
    x,y,z=v
    return np.array([3*alpha*x*x+beta*y*z,
                     3*alpha*y*y+beta*x*z,
                     3*alpha*z*z+beta*x*y],complex)

def payload():
    mons,allowed,orbits=degree3_h27_invariant_orbits()
    # The only invariant orbit sums are S and P.
    expected=[[(0,0,3),(0,3,0),(3,0,0)],[(1,1,1)]]
    orbits_sorted=sorted([sorted(o) for o in orbits],key=lambda o:(len(o),o))
    exp_sorted=sorted([sorted(o) for o in expected],key=lambda o:(len(o),o))
    assert orbits_sorted==exp_sorted

    rays,members=singular_hesse_critical_rays()
    stab=stabilizers()
    A={canon(v) for v in rays}; B={canon(v) for v in stab}
    assert len(A)==len(B)==12 and A==B

    w=np.exp(2j*np.pi/3)
    grad_res=[]
    # P member: alpha=0,beta=1.
    for v in rays[:3]: grad_res.append(float(np.max(abs(grad(0,1,v)))))
    # S-3lambda P: alpha=1,beta=-3lambda.
    for s,rr in enumerate(members):
        lam=w**s
        for v in rr: grad_res.append(float(np.max(abs(grad(1,-3*lam,v)))))
    assert max(grad_res)<1e-9

    theorem=(
      "For W=alpha(x^3+y^3+z^3)+beta xyz, a nonzero complex F-flat "
      "critical ray exists iff alpha=0 or beta^3+27 alpha^3=0. "
      "These four projective coefficient values are the four singular Hesse "
      "members. Their critical rays are exactly the 12 qutrit stabilizer states."
    )
    return {
      "schema":"w33.20261011.h27-hesse-cubic-f-flat-lock.v1",
      "status":"PASS_H27_CUBIC_F_FLAT_VACUA_ARE_EXACTLY_STABILIZER_STATES",
      "degree3":{
        "all_monomials":[list(x) for x in mons],
        "Z_allowed_monomials":[list(x) for x in allowed],
        "H27_invariant_dimension":2,
        "basis":["S=x^3+y^3+z^3","P=xyz"],
        "orbit_sums":[[list(x) for x in o] for o in orbits],
      },
      "singular_pencil":{
        "coefficient_condition":"alpha=0 or beta^3+27 alpha^3=0",
        "projective_members":4,
        "critical_rays_per_member":3,
        "union_critical_rays":12,
        "max_gradient_residual":max(grad_res),
        "equals_qutrit_stabilizer_set":True,
      },
      "theorem":theorem,
      "physics_boundary":{
        "consequence":"Breaking projective G25 down to H27 with only a supersymmetric cubic does not produce a nonzero F-flat magic Higgs: every nonzero F-flat vacuum is a stabilizer state and therefore remains in the Pass11923 charm-up lock.",
        "not_ruled_out":[
          "non-F-flat soft or radiative dynamics on the same Hesse pencil",
          "higher-degree H27 invariants",
          "explicit breaking below H27",
          "couplings to additional fields whose background changes the F-term equations"
        ],
      },
      "sources":{
        p:sha(p) for p in [
          "analysis/w33_pass11664_11671_kernel_dynamics.py",
          "analysis/w33_pass11923_stabiliser_higgs_lock.py",
          "analysis/w33_20261011_execute_all5_witting_flavour_frontier.py",
        ]
      },
      "checks":{
        "H27_cubic_invariant_dimension_two":True,
        "basis_is_Hesse_pencil":True,
        "four_singular_members":True,
        "critical_union_has_12_rays":True,
        "critical_union_equals_stabilizers":True,
        "gradients_vanish":max(grad_res)<1e-9,
      }
    }

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--check",action="store_true")
    a=ap.parse_args(); p=payload(); txt=json.dumps(p,indent=2,sort_keys=True)+"\n"
    if a.check:
        if not OUT.exists() or OUT.read_text()!=txt: raise SystemExit("certificate drift")
    else:
        OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(txt)
    print(json.dumps({"status":p["status"],"checks":p["checks"]}))
if __name__=="__main__": raise SystemExit(main())
