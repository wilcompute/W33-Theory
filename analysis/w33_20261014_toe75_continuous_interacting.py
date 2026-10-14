"""TOE75: numerical continuous U(1)^2 interacting theta-graph ground
energy optimization and full fixed-N thermal traces; NOT global certification.

Native graph is 11-site W33 Theta(4,4,4), N=5 fermions, 12 hoppings.
Repulsive density interaction V. Pure free-fermion flat valleys and exact
S3 degeneracy of the 3 nontrivial Z2 corners are comparison controls.
"""
from __future__ import annotations
import json,sys
from pathlib import Path
import numpy as np
from scipy.optimize import minimize,minimize_scalar
from scipy.sparse.linalg import eigsh
from scipy.special import logsumexp
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261014_toe69_two_octagon_covariance import patch
from w33_20261014_toe74_u1_manybody_finite_t import H_phi,phases_for_chords
from w33_20261014_toe74_theta_friendship import theta_symmetry

def certificate():
    p=patch();s=theta_symmetry()
    assert s["all_three_nontrivial_Z2_corners_unitarily_equivalent"]
    out=[]
    for V in (0.,.2,1.,4.):
        calls=[0]
        def energy(t):
            calls[0]+=1
            phases=phases_for_chords(p,t)
            H=H_phi(p,phases,V)
            vals,vec=eigsh(H,k=1,which="SA",tol=3e-11,
                           maxiter=12000,v0=np.ones(462,dtype=complex)/np.sqrt(462))
            resid=float(np.linalg.norm(H@vec[:,0]-vals[0]*vec[:,0]))
            assert resid<1e-7
            return float(vals[0])
        baseline=energy((np.pi,0))
        # Numerically optimize a one-dimensional continuous boundary
        # valley phi1=pi. Physical angles unrestricted modulo 2pi.
        one=minimize_scalar(lambda x:energy((np.pi,float(x))),
                     bounds=(0,np.pi),method="bounded",
                     options={"xatol":3e-7,"maxiter":80})
        assert one.success
        best1=[float(np.pi),float(one.x)]
        # Multiple 2D starts; a local L-BFGS solve DOES NOT certify
        # global optimality over the phase torus.
        starts=[best1,[np.pi/2,np.pi],[.8*np.pi,.4*np.pi],
                [.4*np.pi,.8*np.pi]]
        attempts=[]
        for x in starts:
            res=minimize(lambda z:energy(z),x,
                method="L-BFGS-B",bounds=((0,2*np.pi),(0,2*np.pi)),
                options={"maxiter":65,"ftol":1e-12,"gtol":1e-7})
            attempts.append({"phase_pi_units":(res.x/np.pi).tolist(),
                "energy":float(res.fun),"solver_success":bool(res.success),
                "solver_message":str(res.message),"evaluations":int(res.nfev)})
        best=min(attempts,key=lambda z:z["energy"])
        # Full spectrum canonical Helmholtz free energies at the
        # 1D-optimized flux and a symmetry-equivalent Z2 control.
        spectra={}
        for name,angles in (("continuum_boundary_min",best1),
                            ("local_2D_best",np.asarray(best["phase_pi_units"])*np.pi),
                            ("nontrivial_Z2",(np.pi,0))):
            full=np.linalg.eigvalsh(H_phi(p,phases_for_chords(p,angles),V).toarray())
            spectra[name]={str(beta):float(-logsumexp(-beta*full)/beta)
                           for beta in (.5,1.,2.,8.)}
        thermal={str(beta):spectra["nontrivial_Z2"][str(beta)]-
                 spectra["continuum_boundary_min"][str(beta)]
                 for beta in (.5,1.,2.,8.)}
        thermal_local={str(beta):spectra["nontrivial_Z2"][str(beta)]-
                       spectra["local_2D_best"][str(beta)]
                       for beta in (.5,1.,2.,8.)}
        if V==0.:
            assert abs(baseline-one.fun)<1e-8
        else:
            assert baseline-float(one.fun)>-1e-7
        assert best["energy"]<=one.fun+1e-7
        out.append({"V":V,
          "Z2_three_equal_sector_ground":baseline,
          "one_dimensional_continuous_optimizer_phase_pi_units":[1.,float(one.x/np.pi)],
          "one_dimensional_continuous_min_energy":float(one.fun),
          "boundary_optimized_advantage_over_Z2":float(baseline-one.fun),
          "two_dimensional_multistart_runs":attempts,
          "best_local_two_dimensional_phase_pi_units":best["phase_pi_units"],
          "best_local_two_dimensional_energy":best["energy"],
          "best_local_advantage_over_Z2":float(baseline-best["energy"]),
          "finite_inverse_temperature_beta":[.5,1.,2.,8.],
          "beta_resolved_boundary_optimized_minus_Z2_free_energy_advantage":thermal,
          "beta_resolved_2D_local_best_minus_Z2_free_energy_advantage":thermal_local,
          "eigensolver_matrix_evaluation_count":calls[0]})
    return {"status":"PASS_TOE75_CONTINUOUS_INTERACTING_U1_FINITE_T_CONTROLS",
       "native_sites_edges_fermions":[11,12,5],
       "full_fixed_N_manybody_dimension":462,
       "theta_graph_three_nontrivial_Z2_sectors_exactly_isospectral":True,
       "interaction_scans":out,
       "scientific_scope":"Numerical 1D bounded and 2D multistart local optimization of 462-state static U1^2 interacting ground energy; exact canonical finite-dimensional spectra for thermal controls. No formal continuous global minimum, no spontaneous TR violation, no dynamical-gauge vacuum, no 80-site W33 TOE."}

if __name__=="__main__":
    c=certificate()
    (ROOT/"data/w33_20261014_toe75_continuous_interacting.json").write_text(
        json.dumps(c,indent=2)+"\n")
    print(c["status"],[(r["V"],r["one_dimensional_continuous_optimizer_phase_pi_units"],r["best_local_two_dimensional_phase_pi_units"],r["best_local_advantage_over_Z2"]) for r in c["interaction_scans"]])
