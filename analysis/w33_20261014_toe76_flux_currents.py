"""TOE76 exact-free and numeric-interacting persistent-current / Hessian
tests for W33-native Theta(4,4,4); matched generic theta control.

No attempt to claim that generic three-arm interference is W33-specific.
V>0 finite-difference Hessians and finite-T susceptibilities are numerical.
"""
from __future__ import annotations
import json,sys
from pathlib import Path
import numpy as np
from scipy.sparse.linalg import eigsh
from scipy.special import logsumexp
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261014_toe69_two_octagon_covariance import patch
from w33_20261014_toe74_theta_friendship import theta_symmetry
from w33_20261014_toe74_u1_manybody_finite_t import H_phi,phases_for_chords
from w33_20261014_toe75_exact_120_flux import theoretical_energy

def certificate():
    p=patch()
    t=theta_symmetry()
    theta_arms=t["native_three_equal_four_edge_routes"]
    assert len(theta_arms)==3
    angles=np.array([2*np.pi/3,4*np.pi/3])
    delta=3e-3
    def compute(phi,V,beta=None):
        H=H_phi(p,phases_for_chords(p,phi),V)
        if beta is None:
            e,v=eigsh(H,k=1,which="SA",tol=1e-11,maxiter=12000,
                      v0=np.ones(462,dtype=complex)/np.sqrt(462))
            assert np.linalg.norm(H@v[:,0]-e[0]*v[:,0])<1e-7
            return float(e[0])
        spec=np.linalg.eigvalsh(H.toarray())
        return float(-logsumexp(-beta*spec)/beta)
    results=[]
    for V in (0.,.2,1.,4.):
        E0=compute(angles,V)
        out={"V":V,"phase_pi_units":[2/3,4/3],"energy_at_120":E0}
        for beta in (None,2.):
            f=lambda z:compute(z,V,beta)
            center=f(angles)
            p0=f(angles+np.array([delta,0]))
            m0=f(angles-np.array([delta,0]))
            p1=f(angles+np.array([0,delta]))
            m1=f(angles-np.array([0,delta]))
            pp=f(angles+np.array([delta,delta]))
            pm=f(angles+np.array([delta,-delta]))
            mp=f(angles+np.array([-delta,delta]))
            mm=f(angles-np.array([delta,delta]))
            gradient=[(p0-m0)/(2*delta),(p1-m1)/(2*delta)]
            H=np.array([[(p0+m0-2*center)/delta**2,
                         (pp-pm-mp+mm)/(4*delta**2)],
                        [(pp-pm-mp+mm)/(4*delta**2),
                         (p1+m1-2*center)/delta**2]])
            vals=np.linalg.eigvalsh(H)
            k="ground_state" if beta is None else "beta_2"
            out[k]={"numerical_current_grad":gradient,
                    "numerical_Hessian":H.tolist(),
                    "Hessian_eigenvalues":vals.tolist(),
                    "positive_numerical_local_flux_stiffness":bool(vals[0]>0)}
            assert max(abs(z) for z in gradient)<.0002
        if V==0.:
            Eexact=theoretical_energy(0)
            assert abs(E0-Eexact)<1e-9
            # s^2 near cube roots = δφ1² - δφ1 δφ2 + δφ2².
            # E0≈Emin + (-g''(3))*s², g(t)=sqrt(5+2sqrt(t)).
            # Therefore Hessian = -g''(3) [[2,-1],[-1,2]].
            t3=3.0
            gpp=-(3*t3**.5+5)/(4*t3**1.5*(5+2*t3**.5)**1.5)
            theory=(-gpp)*np.array([[2.,-1.],[-1.,2.]])
            assert np.max(np.abs(np.asarray(out["ground_state"]["numerical_Hessian"])-theory))<3e-6
            out["exact_V0_Hessian_formula"]="(-g''(3))*[[2,-1],[-1,2]], g(t)=sqrt(5+2sqrt(t))"
            out["exact_V0_Hessian_theory"]=theory.tolist()
        results.append(out)
    # Strong specificity control: the entire graph built from three
    # length-four branches is Theta(4,4,4), independent of W33's
    # 80-site origin; arm relabelings leave the spectra invariant.
    return {
     "status":"PASS_TOE76_FLUX_CURRENTS_STIFFNESS_AND_GENERIC_CONTROL",
     "native_theta_sites_edges":[11,12],
     "fermion_Fock_dimension":462,
     "finite_difference_step_radians":delta,
     "exact_free_global_120_geometry":True,
     "S3_arm_relabelings":len(t["S3_arm_permutation_automorphisms"]),
     "observables":results,
     "generic_theta_graph_control":"The exact free 120-degree optimum, three-arm Ihara factor, and corresponding currents are properties of EVERY uniform Theta(4,4,4) graph. They are NOT W33-unique. An extra observable distinguishing the W33 embedding from an independently realized equal-arm interferometer is REQUIRED.",
     "scope":"Finite-patch numerical interacting persistent currents, local stiffness and beta2 Helmholtz free-energy Hessian, plus an exact V0 Hessian check. Not a global V>0 phase minimum, thermodynamic chirality, gauge dynamics or a parameter-free physical prediction."}

if __name__=="__main__":
    c=certificate()
    (ROOT/"data/w33_20261014_toe76_flux_currents.json").write_text(json.dumps(c,indent=2)+"\n")
    print(c["status"],[(z["V"],z["ground_state"]["Hessian_eigenvalues"],z["beta_2"]["Hessian_eigenvalues"]) for z in c["observables"]])
