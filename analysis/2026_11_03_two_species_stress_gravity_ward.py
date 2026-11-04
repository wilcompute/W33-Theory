#!/usr/bin/env python3
"""Two independent on-shell scalar matter species with separately conserved
stress tensors. Linearized hT gauge invariance alone allows nonuniversal
couplings; exact mixed massless/massive soft-graviton 2->2 Ward identity
forces universality. Necessary check, not interacting graviton emergence.
"""
from pathlib import Path
import sympy as s,json
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'2026_11_03_two_species_stress_spin2_ward.json'
t,x,y,z=s.symbols('t x y z',real=True)
coords=(t,x,y,z)
eta=s.diag(1,-1,-1,-1)
def stress(phi,m):
    grad=s.Matrix([s.diff(phi,u) for u in coords])
    term=(grad.T*eta*grad)[0]-m*m*phi*phi
    T=grad*grad.T-s.Rational(1,2)*eta*term
    divergence=[s.trigsimp(s.simplify(sum(eta[i,i]*s.diff(T[i,j],coords[i])
                  for i in range(4)))) for j in range(4)]
    return T,divergence
def dot(p,q):return (p.T*eta*q)[0]
def run():
    A=s.cos(t-x);B=s.cos(5*t-4*x)
    T0,d0=stress(A,0);T3,d3=stress(B,3)
    assert d0==[0]*4 and d3==[0]*4,(d0,d3)
    off,d_off=stress(s.cos(4*t-4*x),3)
    assert any(a!=0 for a in d_off)
    kA,kB=s.symbols('kA kB',real=True)
    dCombined=[s.simplify(kA*d0[i]+kB*d3[i]) for i in range(4)]
    assert dCombined==[0]*4 # linearized gauge Ward cannot fix kappas
    # Elastic A massless + B mass 3 scattering. All momenta exact.
    p1=s.Matrix([1,0,0,1])
    p2=s.Matrix([3,0,0,0])
    p3=s.Matrix([s.Rational(3,4),s.Rational(3,4),0,0])
    p4=s.Matrix([s.Rational(13,4),-s.Rational(3,4),0,1])
    assert p1+p2==p3+p4
    assert [dot(p,p) for p in (p1,p2,p3,p4)]==[0,9,0,9]
    # Gauge polarization shift eps_mu_nu -> eps_mu_nu+
    # q_mu xi_nu+xi_mu q_nu. Each eikonal soft leg contributes
    # (p^mu p^nu)/(p dot q) and signed external coupling.
    q=s.Matrix([5,3,4,0]);xi=s.Matrix([s.Rational(1,3),
        s.Rational(2,5),-s.Rational(1,7),s.Rational(3,11)])
    assert dot(q,q)==0
    assert all(dot(p,q)!=0 for p in (p1,p2,p3,p4))
    qc=eta*q;xic=eta*xi;shift=qc*xic.T+xic*qc.T
    ps=(p1,p2,p3,p4)
    signs=(-1,-1,1,1)
    co=(kA,kB,kA,kB)
    variation=s.factor(sum(signs[i]*co[i]*(ps[i].T*shift*ps[i])[0]/
                          dot(ps[i],q) for i in range(4)))
    predicted=2*(kA-kB)*dot(p3-p1,xi)
    assert s.simplify(variation-predicted)==0
    assert s.simplify(variation.subs({kA:1,kB:1}))==0
    assert s.simplify(variation.subs({kA:1,kB:2}))!=0
    # Universal soft condition is exact nullspace span (1,1)
    J=s.Matrix.hstack(p3-p1,p4-p2)
    assert J.rank()==1
    assert J.nullspace()==[s.Matrix([1,1])]
    out={"status":"PASS_TWO_ONSHELL_STRESS_TENSORS_SOFT_SPIN2_UNIVERSALITY",
      "matter_species":[{"field":"cos(t-x)","mass":0,"stress_divergence":[str(v) for v in d0]},
          {"field":"cos(5t-4x)","mass":3,"stress_divergence":[str(v) for v in d3]}],
      "off_shell_control_divergence":[str(v) for v in d_off],
      "linearized_coupling":"S_int=(1/2) integral h_mu_nu [kA T_A^mu_nu+kB T_B^mu_nu]. For separately on-shell free fields, divergence vanishes for arbitrary kA,kB; linearized hT gauge invariance alone cannot force equality.",
      "soft_mixed_mass_scattering_momenta":[[str(v) for v in p] for p in ps],
      "species_mass_squared":[0,9,0,9],
      "soft_null_q":[str(v) for v in q],
      "gauge_vector_xi":[str(v) for v in xi],
      "exact_soft_spin2_polarization_variation":str(variation),
      "universal_coupling_nullspace":[1,1],
      "logical_message":"Both freely chosen κ species preserve local source conservation, yet the massless-spin2 scattering Ward identity requires κ_A=κ_B for nonforward processes. Two helicities and a conserved hT coupling are not sufficient for gravitational universality.",
      "physics_boundary":"This checks two supplied flat-space scalar waves and an exact on-shell soft theorem kinematics; it does NOT include an interacting backreacting scalar-gravity Hamiltonian, nonlinear diffeomorphisms, quantum loops or a derived Newton constant.",
      "reference":"https://doi.org/10.1103/PhysRev.135.B1049"}
    OUT.write_text(json.dumps(out,indent=2)+"\n")
    print("TWO MATTER SPECIES","stress_onshell",d0,d3,"Ward",variation,flush=True)
if __name__=="__main__":run()
