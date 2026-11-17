"""An independently motivated, gauge-invariant TWO-field vacuum selector.

A dynamical Hermitian rank-two projector Q (adjoint+singlet under SU5,
with a positive quartic pinning potential) and a traceless Hermitian
adjoint Phi have the gauge-invariant portal epsilon Tr(Phi Q).
At fixed TrPhi²=r² and rank(Q)=2, the global minimum over BOTH fields
is exactly Phi=-r*(Q-2I/5)/sqrt(6/5), eigenvalues proportional to
(2,2,2,-3,-3); this needs NO quartic TrPhi4 selection coefficient.

Q is a *separate dynamical adjoint-plus-singlet field*, NOT a VEV of
two fundamental SU5 fields (which could break weak SU2 gauge bosons).
The projector constraint is the strong-pinning/NLSM limit. It remains
to derive this potential and its SUSY/E6 embedding from first principles.
"""
import json,math
from pathlib import Path
import numpy as np
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261117_rank2_dynamical_projector_variational_selector.json"

def verify(m2=1.,lam=.35,eps=.2):
    assert m2>0 and lam>0 and eps>0
    Q=np.diag([0.,0.,0.,1.,1.])
    I=np.eye(5)
    C=Q-(2/5)*I
    assert np.allclose(Q@Q,Q)
    assert np.trace(Q)==2
    normC=np.linalg.norm(C,ord="fro")
    assert math.isclose(normC**2,6/5,abs_tol=1e-14)
    r=1.
    Phi=-r*C/normC
    assert np.trace(Phi)==0
    assert math.isclose(np.trace(Phi@Phi),r*r,abs_tol=1e-14)
    assert np.allclose(np.sort(np.linalg.eigvalsh(Phi)),
                       np.sort(np.array([2,2,2,-3,-3])/math.sqrt(30)),atol=1e-14)
    assert math.isclose(np.trace(Phi@Q),-math.sqrt(6/5),abs_tol=1e-14)
    q4=np.trace(Phi@Phi@Phi@Phi)/np.trace(Phi@Phi)**2
    assert math.isclose(q4,7/30,rel_tol=0,abs_tol=1e-14)
    # The trace-cyclic Rayleigh bound is exact because TrPhi=0:
    # Tr(Phi Q)=Tr(Phi(Q-2I/5)) >= -||Phi||_F ||Q-2I/5||_F.
    rng=np.random.default_rng(20261117)
    controls=[]
    for j in range(120):
        A=rng.standard_normal((5,5))
        A=(A+A.T)/2
        A-=np.trace(A)/5*I
        A/=np.linalg.norm(A,ord="fro")
        y=float(np.trace(A@Q))
        assert y>=-normC-1e-12
        controls.append(y)
    # With eps>0, the radial energy
    # -m2*r²+lambda*r⁴-eps*sqrt(6/5)*r has exactly one positive
    # stationary point (derivative crosses once on r>0).
    coeff=[4*lam,0,-2*m2,-eps*normC]
    roots=np.roots(coeff)
    rootspos=sorted(float(z.real) for z in roots if abs(z.imag)<1e-10 and z.real>0)
    assert len(rootspos)==1
    r0=rootspos[0]
    E=-m2*r0*r0+lam*r0**4-eps*normC*r0
    E0=-m2*(m2/(2*lam))+lam*(m2/(2*lam))**2
    assert E<E0
    # Quadratic portal misalignment eigen-gap for one frame rotation:
    # given Phi=(2,2,2,-3,-3)*r/sqrt(30) and Q_weak,
    # rotating one weak basis vector into a colour basis raises energy
    # DeltaV=(5 eps r/sqrt(30))*sin(theta)^2.
    phi_ref=np.array([2,2,2,-3,-3])/math.sqrt(30)*r0
    Eground=eps*sum(phi_ref[3:])
    gap=5*eps*r0/math.sqrt(30)
    for angle in (.1,.2,.4,.9,1.3):
        v=np.array([math.sin(angle),0,0,math.cos(angle),0])
        Qrot=np.outer(v,v)+np.diag([0.,0.,0.,0.,1.])
        shifted=eps*np.trace(np.diag(phi_ref)@Qrot)-Eground
        assert math.isclose(shifted,gap*math.sin(angle)**2,rel_tol=1e-11,abs_tol=1e-12)
    # Even letting Q readjust, the opposite-sign adjoint shape has
    # best portal -4eps*r/sqrt(30), vs desired -6eps*r/sqrt(30).
    sign_lift=2*eps*r0/math.sqrt(30)
    assert sign_lift>0
    return {"status":"PASS_INDEPENDENT_RANK2_PROJECTOR_SELECTS_3PLUS2_WITHOUT_TRPHI4_COEFFICIENT",
       "fields":"Phi Hermitian traceless SU5 adjoint; Q Hermitian SU5 adjoint-plus-singlet, Q^2=Q and TrQ=2",
       "rank2_pinning_effective_potential":"nu Tr[(Q²-Q)²]+chi(TrQ-2)², nu,chi>0; exact Q projector manifold only in strong-pinning limit or with constraint",
       "gauge_invariant_portal":"epsilon Tr(Phi Q), epsilon>0",
       "Cauchy_Schwarz_theorem":"For any rank2 Q, TrPhi=0, TrPhi²=r², min_Phi Tr(Phi Q)=-r sqrt(6/5), uniquely attained at Phi=-r(Q-2I/5)/sqrt(6/5)",
       "normalized_eigenvalues":"(2,2,2,-3,-3)/sqrt(30)",
       "fixed_norm_quartic_ratio":"7/30 arises without a TrPhi4 term",
       "radial_potential":"V_eff(r)=-m2 r²+lambda r⁴-epsilon r sqrt(6/5), lambda,m2,epsilon>0",
       "reference_parameters":{"m2":m2,"lambda":lam,"epsilon":eps,
         "selected_radial_norm":r0,"minimum_energy":E,
         "unbiased_quartic_energy":E0},
       "continuous_relative_rotation_cost":"DeltaV=(5 epsilon r/sqrt30) sin(theta)^2",
       "relative_orientation_gap":gap,"opposite_sign_relaxed_Q_energy_penalty":sign_lift,
       "random_traceless_matrix_controls":120,
       "physically_distinct_vs_gauge":"Simultaneous SU5 conjugations of Phi,Q are pure gauge. The portal fixes their RELATIVE orientation and lifts Phi sign, not an absolute labeling of the two weak indices.",
       "limits":"The projector manifold is assumed from a second dynamical sector; its UV origin, superpotential/Kähler, E6 representation, radiative and finite-temperature effects, proton decay, electroweak doublet-triplet splitting and observables have NOT been derived."}
if __name__=="__main__":
    x=verify();OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(x,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(x["status"],x["reference_parameters"]["selected_radial_norm"])
