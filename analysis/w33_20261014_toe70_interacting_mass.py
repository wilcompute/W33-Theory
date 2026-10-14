"""TOE70: L=3 native overlapping-octagon covariance and restricted CDW Hartree.

CDW solutions are in the *uniform sublattice Hartree channel* of local
nearest-neighbor density repulsion. They are NOT unrestricted HF minima,
exact many-body eigenstates, or a proof of spontaneous W33 mass in nature.
"""
from pathlib import Path
import json,sys
import numpy as np
from scipy.optimize import brentq
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_pass1081_1086_core import build_w33
from w33_20261014_toe69_two_octagon_covariance import patch,diagonalize

def interacting_two_loop():
    p=patch()
    old=[diagonalize(L,p) for L in (1,2)]
    new=diagonalize(3,p)
    assert [z["dimension"] for z in old+[new]]==[4158,11550,22638]
    assert all(z["numerical_ritz_residual"]<1e-7 for z in old+[new])
    assert old[0]["ground"]>old[1]["ground"]>new["ground"]
    assert new["flux_covariance"][0][1]<0
    assert new["flux_boundary_probability"]<2.1e-5
    rho=new["flux_covariance"][0][1]/np.sqrt(
        new["flux_covariance"][0][0]*new["flux_covariance"][1][1])
    return {
       "status":"PASS_TOE70_NATIVE_TWO_LOOP_L3_NUMERIC",
       "cutoff_sequence":old+[new],
       "flux_covariance_at_L3":new["flux_covariance"][0][1],
       "flux_correlation_at_L3":float(rho),
       "L2_to_L3_energy_change":new["ground"]-old[1]["ground"],
       "flux_boundary_L3":new["flux_boundary_probability"],
       "scope":"Actual native 11-site, 12-link, 5-fermion, 3-supported-octagon magnetic patch; finite three-cutoff Galerkin values, not certified untruncated bounds or full 80-site QFT. Prior Pass11974 studied this patch class."
    }

def cdw_channel():
    *_,flags,_=build_w33()
    B=np.zeros((40,40),dtype=float)
    for i,(p,l) in enumerate(flags):
        B[p,l]=-1 if i in (59,93,139) else 1
    sigma=np.linalg.svd(B,compute_uv=False)
    rank=int(sum(sigma>1e-9))
    assert rank==28 and len(sigma)==40
    solutions=[]
    for V in (.01,.05,.1,.2,.4,.8,1.6):
        # Hartree decoupling of V sum_<a,b>(n_a-1/2)(n_b-1/2),
        # restricted to uniform n_A=1/2-s, n_B=1/2+s.
        # Each native vertex has degree four; m=4Vs and
        # E_Hartree(m)=-sum_j sqrt(sigma_j²+m²)+10 m²/V.
        def derivative_equation(m):
            return 20/V-float(np.sum(1/np.sqrt(sigma*sigma+m*m)))
        m=float(brentq(derivative_equation,1e-12,8*V,xtol=1e-14))
        gain=float(np.sum(np.sqrt(sigma*sigma+m*m)-sigma)-10*m*m/V)
        assert m>0 and gain>0 and abs(derivative_equation(m))<1e-8
        H=np.block([[m*np.eye(40),B],[B.T,-m*np.eye(40)]])
        evals,evec=np.linalg.eigh(H)
        density=np.sum(abs(evec[:,:40])**2,axis=1)
        stagger_points=.5-density[:40]
        stagger_lines=density[40:]-.5
        local_dispersion=[float(np.std(stagger_points)),float(np.std(stagger_lines))]
        assert max(local_dispersion)>.001 if V<=.4 else True
        solutions.append({
            "V":V,"Hartree_mass_m":m,"uniform_channel_density_s":m/(4*V),
            "free_quasiparticle_gap_2m":2*m,
            "uniform_Hartree_energy_gain_vs_m0":gain,
            "local_point_line_density_stdev":local_dispersion,
            "stationary_gap_equation_residual":derivative_equation(m)})
    assert abs(solutions[0]["Hartree_mass_m"]/solutions[0]["V"]-.6)<.01
    # 12 singular zero modes force gap-equation RHS ~12/m, so every
    # V>0 admits a unique m>0 *within this one-parameter ansatz*.
    # Local density nonuniformity rejects unrestricted sitewise Hartree
    # self-consistency of that ansatz at the three-chord flux.
    return {
       "status":"PASS_TOE70_RESTRICTED_INTERACTION_DRIVEN_CDW",
       "native_vertices":80,"native_incidence_edges":160,
       "singular_zero_values_at_three_pi":40-rank,
       "local_density_repulsion_model":"V sum_native_edges (n_A-1/2)(n_B-1/2)",
       "Hartree_energy_functional":"E_H(m)=-sum_j sqrt(sigma_j^2+m^2)+10m^2/V",
       "Hartree_stationarity":"20/V=sum_j 1/sqrt(sigma_j^2+m^2)",
       "small_V_mass_over_V_limit":.6,
       "samples":solutions,
       "global_fixed_mass_flux_selection":"TOE67 uniform all-beta free determinant theorem holds at every common staggered mass; minimizing this uniform-channel Hartree functional over mass consequently retains three-pi.",
       "scope":"One-parameter uniform Hartree approximation to native nearest-neighbor repulsion; observed site-to-site density variations show it is NOT an unrestricted Hartree-Fock stationary state. Exchange corrections, dynamical gauge fields, actual interacting many-body gap, physical mass and parameter-free predictions are OPEN."
    }

def certificate():
    return {
       "status":"PASS_TOE70_TWO_LOOP_AND_RESTRICTED_MASS",
       "gauge":interacting_two_loop(),
       "mass":cdw_channel()
    }

if __name__=="__main__":
    c=certificate()
    (ROOT/"data/w33_20261014_toe70_interacting_mass.json").write_text(
         json.dumps(c,indent=2)+"\n")
    print(c["status"],c["gauge"]["flux_covariance_at_L3"])
