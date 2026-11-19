#!/usr/bin/env python3
"""Five deeper physical TOE filters: UV adjoints, neutrino tuning, gravitational poles,
full published DESI DR2 covariance likelihood, and single-photon SSR limitations.

NO hypothesis of W33 or discrete TOE is required. This is a *falsifier suite*,
not a working grand unified model or a solution to fundamental quantum theory.
"""
from __future__ import annotations
import json
import math
from pathlib import Path
import numpy as np
from scipy.optimize import minimize
from numpy.polynomial.legendre import leggauss

import toe_20261119_joint_physics_five_frontiers as earlier

ROOT=Path(__file__).resolve().parents[1]
MEAN=ROOT/"data"/"desi_dr2_13_mean_20261119.txt"
COV=ROOT/"data"/"desi_dr2_13_cov_20261119.txt"
JSON=ROOT/"data"/"toe_20261119_five_physical_completion_gates.json"
MZ=91.1876
MU=2e16
PI=np.pi


def su5_adjoint_gate():
    """Tree-level SU5 adjoint 24F mass sum rule and one forced light X.
    For renormalizable tr(F^2) and tr(F^2 24H) with a single 24H
    aligned proportional to diag(2,2,2,-3,-3):
    M8=M+2K, M3=M-3K, MX=M-K/2=(M8+M3)/2.
    These are 2x2 complex symmetric fermion generation matrices.
    """
    b=earlier.gauge_bridge(MU)
    MT=b["field_content"][0]["Mass_GeV"]
    MO=b["field_content"][1]["Mass_GeV"]
    M3=np.diag([MT,MT]).astype(complex)
    M8=np.diag([MO,MU]).astype(complex)
    MX=(M8+M3)/2
    MX_mass=np.sort(np.linalg.svd(MX,compute_uv=False))
    bound=(MT+MO)/2
    assert MX_mass[0]<=bound*(1+1e-13)
    assert np.isclose(MX_mass[0],bound)
    # With arbitrary flavor mixing in the 2 adjoints:
    # s_min((M8+M3)/2) <= (s_min(M8)+||M3||_2)/2.
    rng=np.random.default_rng(2026111907)
    max_excess=0
    for _ in range(200):
        v=rng.standard_normal((2,2))+1j*rng.standard_normal((2,2))
        v,_=np.linalg.qr(v)
        # arbitrary complex symmetric fermion masses: Takagi congruence
        tri=v@np.diag([MT,MT])@v.T
        w=rng.standard_normal((2,2))+1j*rng.standard_normal((2,2))
        w,_=np.linalg.qr(w)
        octet=w@np.diag([MO,MU])@w.T
        x=(tri+octet)/2
        lim=(np.linalg.svd(tri,compute_uv=False)[0]+
             np.linalg.svd(octet,compute_uv=False)[-1])/2
        actual=np.linalg.svd(x,compute_uv=False)[-1]
        max_excess=max(max_excess,actual-lim)
        assert actual<=lim*(1+1e-10)
    # Leptoquark-like vectorlike (3,2,-5/6)+(3bar,2,5/6)
    # Weyl pair shifts all 3 couplings as a full 24F X block.
    dB_X=np.array([10/3,2,4/3])
    dB_T=np.array([0,4/3,0])
    dB_O=np.array([0,0,2])
    assert np.allclose(dB_X+dB_T+dB_O,[10/3]*3)
    # If introduced WITHOUT refitting the original 2T+1O toy solution,
    # the forced light X shifts the relative inverse couplings by O(1).
    invshift=-dB_X*np.log(MU/MX_mass[0])/(2*PI)
    # Second octet at MU, second X at MU/2 have additional, smaller,
    # differences, so this is only the first mandatory change, not a
    # complete alternative threshold fit.
    assert np.ptp(invshift)>4
    return {
        "status":"PASS",
        "toy_triplet_two_mass_GeV":MT,
        "toy_light_octet_mass_GeV":MO,
        "adjoined_heavy_octet_chosen_GeV":MU,
        "renormalizable_SU5_matrix_mass_relation":"2 MX = M8 + M3",
        "Takagi_light_X_analytic_upper_bound_GeV":bound,
        "explicit_commuting_example_X_Takagi_masses_GeV":MX_mass.tolist(),
        "random_complex_symmetric_mass_mixing_checks":200,
        "maximum_numerical_violation_of_upper_bound_GeV":max_excess,
        "full_24F_one_loop_shifts":{"triplet":dB_T.tolist(),"octet":dB_O.tolist(),
                                    "X_and_Xbar":dB_X.tolist()},
        "forced_light_X_inverse_coupling_shift_if_unretuned":invshift.tolist(),
        "forced_light_X_inverse_coupling_shift_spread_if_unretuned":float(np.ptp(invshift)),
        "source_hypothesis":"Two fermionic 24_F multiplets and only renormalizable mass operators from M and one 24_H spurion",
        "caveats":[
            "The min-singular-value bound holds only if all two triplets are <= the benchmark MT and at least one octet <= MO; it is not generic for arbitrary BSM models.",
            "Additional scalar representations, multiple 24_H VEVs, dimension-five operators, or exotic mixing can evade the matrix relation.",
            "An extra light X does not alone prove inconsistency: refit ALL thresholds and include every multiplet; no proton lifetime calculated.",
            "The benchmark low-energy field inventory is not a complete SU5 embedding."
        ]
    }


def neutrino_complex_angle_gate():
    b=earlier.gauge_bridge(MU)
    M=b["field_content"][0]["Mass_GeV"]
    U=earlier.pmns(.3047,.0222,.4908,1.19*PI)
    m=np.array([0,np.sqrt(7.465e-5),np.sqrt(2.5093e-3)])*1e-9
    v=246.22
    target=U.conj()@np.diag(m)@U.conj().T
    rows=[]
    for z in [0,.35,.6,1j*.5,1j*1,1j*2,1j*3]:
        c=np.cos(z);s=np.sin(z)
        R=np.array([[0,c,s],[0,-s,c]],complex)
        assert np.linalg.norm(R@R.T-np.eye(2))<1e-12
        Y=1j*np.sqrt(2*M)/v*R@np.diag(np.sqrt(m))@U.conj().T
        predicted=-v*v/(2*M)*Y.T@Y
        residual=float(np.linalg.norm(predicted-target))
        assert residual<1e-22
        Ynorm2=float(np.linalg.norm(Y)**2)
        expected=(2*M/v**2)*(m[1]+m[2])*np.cosh(2*z.imag)
        assert np.isclose(Ynorm2,expected,rtol=1e-11)
        # Model-dependent one-loop threshold scale estimate, not
        # a renormalization-scheme-independent prediction.
        dmh2=3/(16*PI**2)*M*M*Ynorm2
        rows.append({"complex_z":str(z),
                     "Im_z":float(z.imag),"Y_frobenius_squared":Ynorm2,
                     "Y_max":float(np.max(np.abs(Y))),
                     "Higgs_threshold_estimate_GeV2":float(dmh2),
                     "threshold_over_125GeV_mass_squared":float(dmh2/125.25**2),
                     "mass_reconstruction_error_GeV":residual})
    assert rows[3]["Y_frobenius_squared"]>rows[0]["Y_frobenius_squared"]
    assert np.isclose(rows[0]["Y_frobenius_squared"],rows[1]["Y_frobenius_squared"])
    # This angle is unconstrained by the measured light mass matrix, and
    # can boost heavy Yukawa strengths exponentially by cosh(2 Im z).
    return {
        "status":"PASS","triplet_mass_GeV":M,
        "Casas_Ibarra_angle_samples":rows,
        "exact_trace_scaling":"Tr(Ydagger Y)=2M(m2+m3)/v^2 * cosh(2 Im z)",
        "light_mass_matrix_fixed":True,
        "tree_level_lightest_mass_eV":0,
        "warnings":[
           "Im z is free: low-energy mixing does not determine heavy Yukawas or naturalness.",
           "Higgs threshold formula 3 Tr(Ydagger M^2 Y)/(16 pi^2) is an explicitly conventional sensitivity scale; finite matching/logarithms depend on scheme.",
           "No loop leptogenesis, LFV prediction, or electroweak vacuum lifetime here.",
           "The 2-triplet truncation permits both light orderings, not a predicted neutrino ordering."
        ]
    }


def gravity_poles():
    # In Euclidean p²=q >=0, a Weyl-squared induced massive spin2
    # exchange factor 1/[q(1+q/M2²)] necessarily has negative residue
    # at the extra pole if treated as an exactly fundamental local kernel.
    M2=1e15
    q=np.geomspace(1e-12,1e4,41)*M2*M2
    exact=1/(q*(1+q/M2**2))
    split=1/q-1/(q+M2**2)
    assert np.allclose(exact,split,rtol=1e-12,atol=0)
    scal=earlier.gravity_bridge()
    return {
       "status":"PASS",
       "toy_Weyl_squared_mass_GeV":M2,
       "spin2_massless_pole_residue":1,
       "spin2_extra_pole_residue":-1,
       "partial_fraction_identity_max_relative_error":
         float(np.max(np.abs(exact-split)/exact)),
       "R2_scalaron_fifth_force_length_m":scal["scalaron_Compton_length_m"],
       "R2_no_new_spin2_ghost_at_quadratic_tree_level":True,
       "explanation":"Positive quadratic Weyl-type fourth-derivative spin2 pole has negative residue in local polynomial truncation",
       "limits":[
          "In EFT, a heavy higher-derivative pole beyond cutoff is not automatically a propagating physical ghost.",
          "A nonlocal or UV-completed gravity model may escape this specific polynomial structure.",
          "R² scalaron and a pole-identity test do not establish quantum gravity, graviton unitarity, cosmological constant, or black-hole entropy."
       ]
    }


def _source_bao():
    assert MEAN.exists() and COV.exists(), "Published mean/cov fixtures not available"
    data=np.genfromtxt(MEAN,dtype=str,comments="#")
    cov=np.loadtxt(COV)
    z=data[:,0].astype(float)
    measured=data[:,1].astype(float)
    kind=data[:,2]
    assert len(measured)==13 and cov.shape==(13,13)
    assert np.max(np.abs(cov-cov.T))<1e-10
    assert np.linalg.eigvalsh(cov).min()>0
    assert abs(measured[3]-17.35069094)<1e-8
    assert abs(measured[4]-19.45534918)<1e-8
    return z,measured,kind,cov


def bao_covariance_fit():
    z,y,kind,C=_source_bao()
    nodes,weights=leggauss(64)
    Cinvy=np.linalg.solve(C,y)
    zs=np.unique(z)
    wmap={float(zi):i for i,zi in enumerate(zs)}
    grid=zs[:,None]*(nodes[None,:]+1)/2
    # DESI cosmology uses CMB-era effects in sound horizon; treat q=c/(H0*rd)
    # as a freely profiled positive amplitude. No independent H0/rd inferred.
    omega_r=9e-5
    def templates(om,w0,wa):
        def E(zp):
            a=1/(1+zp)
            Ode=1-om-omega_r
            density=Ode*a**(-3*(1+w0+wa))*np.exp(3*wa*(a-1))
            E2=om*a**-3+omega_r*a**-4+density
            if np.min(E2)<=0:return None
            return np.sqrt(E2)
        Integrals=zs/2*np.sum(weights[None,:]/E(grid),axis=1)
        Es=E(zs)
        tm=[]
        for zi,typ in zip(z,kind):
            idx=wmap[zi]
            I=Integrals[idx]
            e=Es[idx]
            if typ=="DM_over_rs":tm.append(I)
            elif typ=="DH_over_rs":tm.append(1/e)
            elif typ=="DV_over_rs":tm.append((zi*I*I/e)**(1/3))
            else:raise ValueError(typ)
        return np.array(tm)
    def profile(pars,is_cpl):
        om=pars[0]
        w0,wa=(pars[1],pars[2]) if is_cpl else (-1.,0.)
        t=templates(om,w0,wa)
        if t is None:return (np.inf,np.nan,None)
        Wt=np.linalg.solve(C,t)
        q=float((t@Cinvy)/(t@Wt))
        if q<=0:return (np.inf,q,t)
        diff=q*t-y
        chi=float(diff@np.linalg.solve(C,diff))
        return chi,q,t

    def optimize(is_cpl,extra_DES=False,wide_CPL=False):
        # Optional independent DES measurement, using already DESI-
        # excluded footprint and no DES/DESI cross-survey systematic cov.
        # This comparison is *independent Gaussian* only, NOT a joint
        # Stage-IV/Planck/SNe posterior.
        zz=.851;val=19.74;sig=.60
        def param_and_stats(p):
            chi,q,templ=profile(p,is_cpl)
            if not extra_DES or templ is None:return chi,q,templ
            om=p[0];w0,wa=(p[1],p[2]) if is_cpl else (-1.,0.)
            grid2=zz*(nodes+1)/2
            a=1/(1+grid2)
            Ode=1-om-omega_r
            E2=om*a**-3+omega_r*a**-4+Ode*a**(-3*(1+w0+wa))*np.exp(3*wa*(a-1))
            I=zz/2*np.sum(weights/np.sqrt(E2))
            # Profile common q jointly with DES datum, including 13x13
            # DESI block covariance + independent scalar variance.
            td=q*0+I
            Cinv_t=np.linalg.solve(C,templ)
            q=(templ@Cinvy+td*val/sig**2)/(templ@Cinv_t+td*td/sig**2)
            resid=q*templ-y
            chi=float(resid@np.linalg.solve(C,resid)+(q*td-val)**2/sig**2)
            return chi,float(q),templ
        bounds=[(.15,.5)]
        starts=[[.30],[.26],[.34]]
        if is_cpl:
            bounds+=[(-2.1,.5),(-6.,5.)] if wide_CPL else [(-2.1,-.25),(-3.5,3.5)]
            starts=[[.3,-1,0],[.30,-.84,-.53],[.26,-.7,-1.1],
                    [.36,-1.4,.8],[.27,-.5,-1.5],[.4,-1.2,.2]]
            if wide_CPL: starts += [[.38,0,-3.],[.44,.3,-4.5],[.3,-.1,-2.4]]
        results=[minimize(lambda p:param_and_stats(p)[0],start,bounds=bounds,
                          method="L-BFGS-B",options={"ftol":1e-12,
                                                    "maxiter":300})
                 for start in starts]
        feasible=[r for r in results if np.isfinite(r.fun)]
        best=min(feasible,key=lambda res:res.fun)
        chi,q,templ=param_and_stats(best.x)
        n=len(y)+int(extra_DES)
        k=(4 if is_cpl else 2) # Omega_m,q plus w0,wa when CPL
        return {
          "chi_squared":float(chi),
          "Omega_m":float(best.x[0]),
          "w0":float(best.x[1]) if is_cpl else -1.,
          "wa":float(best.x[2]) if is_cpl else 0.,
          "q_c_over_H0_rd":float(q),
          "H0_rd_km_s":float(299792.458/q),
          "AIC":float(chi+2*k),
          "BIC":float(chi+k*np.log(n)),
          "n_data":n,"n_parameters":k,
          "optimization_success":bool(best.success),
          "all_solution_chi2":[float(r.fun) for r in results],
          "predicted_desi_vector":(q*templ).tolist(),
          "residual_desi_vector":(q*templ-y).tolist()
        }

    lcdm=optimize(False)
    cpl=optimize(True)
    cpl_wide=optimize(True,wide_CPL=True)
    lcdm14=optimize(False,True)
    cpl14=optimize(True,True)
    assert cpl["chi_squared"]<=lcdm["chi_squared"]+1e-7
    assert cpl14["chi_squared"]<=lcdm14["chi_squared"]+1e-7
    assert np.isclose(y[3],17.35069094)
    return {
       "status":"PASS",
       "source_repo":"https://github.com/CobayaSampler/bao_data/tree/master/desi_bao_dr2",
       "source_mean_sha":"8aff444fdb42c0946342aa0011ab287eda097c4c",
       "source_cov_sha":"fd8e5697ab61379b07b52efb781ea6713417a4d9",
       "data_redshifts":z.tolist(),
       "data_types":kind.tolist(),
       "measurement_vector":y.tolist(),
       "covariance_eigenvalues":np.linalg.eigvalsh(C).tolist(),
       "n_desi_measurements":13,
       "LCDM_only_DESI13":lcdm,
       "CPL_only_DESI13":cpl,
       "CPL_only_DESI13_wide_bounds":cpl_wide,
       "DESI13_wide_vs_baseline_CPL_delta_chi2":cpl["chi_squared"]-cpl_wide["chi_squared"],
       "DESI13_delta_chi2_LCDM_minus_CPL":lcdm["chi_squared"]-cpl["chi_squared"],
       "DESI13_delta_AIC_CPL_minus_LCDM":cpl["AIC"]-lcdm["AIC"],
       "DESI13_delta_BIC_CPL_minus_LCDM":cpl["BIC"]-lcdm["BIC"],
       "LCDM_plus_overlap_removed_DES14":lcdm14,
       "CPL_plus_overlap_removed_DES14":cpl14,
       "warnings":[
         "This is a BAO-only Gaussian distance likelihood with the published 13x13 DESI DR2 covariance, not a full CMB/SNe/lensing likelihood.",
         "H0 and r_d enter only through their product; the early-Universe sound horizon is not derived.",
         "Omega_r fixed at 9e-5 and physical neutrino/radiation transfer effects approximated; use a Boltzmann code for precision.",
         "Adding DES Y6 independent-footprint point ignores potential residual cross-survey systematics.",
         "Delta chi² is not a discovery significance; AIC/BIC are approximate complexity diagnostics, not Bayesian evidence.",
         "Bounds in w0,wa and Omega_m restrict the fit; check likelihood contours and stability."
       ]
    }


def _pt_b(rho):
    return rho.reshape((2,2,2,2)).transpose((0,3,2,1)).reshape((4,4))


def _horodecki_chsh(rho):
    X=np.array([[0,1],[1,0]],complex)
    Y=np.array([[0,-1j],[1j,0]],complex)
    Z=np.array([[1,0],[0,-1]],complex)
    ps=[X,Y,Z]
    T=np.array([[np.trace(rho@np.kron(a,b)).real for b in ps] for a in ps])
    eigen=np.linalg.eigvalsh(T.T@T)
    return float(2*np.sqrt(eigen[-1]+eigen[-2]))


def photon_superselection():
    psi=np.array([0,1,1,0],complex)/np.sqrt(2) # |01>+|10>
    rho=np.outer(psi,psi.conj())
    rho_twirl=np.diag(np.diag(rho))
    def negativity(mat):
        eigen=np.linalg.eigvalsh(_pt_b(mat))
        return float((np.sum(abs(eigen))-1)/2)
    Nraw=negativity(rho)
    Nt=negativity(rho_twirl)
    chraw=_horodecki_chsh(rho)
    cht=_horodecki_chsh(rho_twirl)
    assert abs(Nraw-.5)<1e-12
    assert abs(Nt)<1e-12
    assert abs(chraw-2*np.sqrt(2))<1e-12
    assert abs(cht-2)<1e-12
    rng=np.random.default_rng(2026111908)
    for _ in range(120):
        # Any local number-conserving local effect on a single-mode
        # zero/one occupation basis is diagonal; raw and twirled
        # states are operationally indistinguishable under SSR.
        a=np.diag(rng.uniform(-1,1,size=2))
        b=np.diag(rng.uniform(-1,1,size=2))
        op=np.kron(a,b)
        assert abs(np.trace(rho@op)-np.trace(rho_twirl@op))<1e-12
    return {
       "status":"PASS",
       "state":"single-photon two-mode occupation state (|10>+|01>)/sqrt2",
       "unrestricted_entanglement_negativity":Nraw,
       "locally_U1_twirl_entanglement_negativity":Nt,
       "unrestricted_max_CHSH":chraw,
       "locally_twirled_max_CHSH":cht,
       "locally_number_conserving_observables_checked":120,
       "operational_claim":"Without shared phase reference and under local particle-number superselection, single-photon coherence is not accessible to local CHSH",
       "caveats":[
         "With coherent ancillary reference frames the twirl assumption fails and operational Bell violations may be possible.",
         "A single photon with internal (path/polarization) degrees of freedom can exhibit contextuality, not necessarily spacelike Bell nonlocality.",
         "This does not refute single-photon qudit computation, though scalable arbitrary n-qubit encoding still needs >=2^n optical modes."
       ]
    }


def make_results():
    parts={
      "physical_SU5_adjoint_mass_embedding":su5_adjoint_gate(),
      "neutrino_Yukawa_continuum_and_naturalness":neutrino_complex_angle_gate(),
      "higher_derivative_spin2_spectral_test":gravity_poles(),
      "full_DESI_DR2_Gaussian_covariance":bao_covariance_fit(),
      "single_photon_local_SSR_and_CHSH":photon_superselection()
    }
    assert all(v["status"]=="PASS" for v in parts.values())
    return {"date":"2026-11-19",
       "title":"TOE physical completion gates v3: no W33 assumptions",
       "status":"conditional physical no-go and observational likelihood diagnostics; not a TOE",
       "domains":parts}


def main():
    r=make_results()
    JSON.write_text(json.dumps(r,indent=2),encoding="utf-8")
    parts=r["domains"]
    g=parts["physical_SU5_adjoint_mass_embedding"]
    b=parts["full_DESI_DR2_Gaussian_covariance"]
    n=parts["neutrino_Yukawa_continuum_and_naturalness"]
    p=parts["single_photon_local_SSR_and_CHSH"]
    print(json.dumps({
       "status":"PASS",
       "forced_SU5_light_X_upper_GeV":g["Takagi_light_X_analytic_upper_bound_GeV"],
       "DESI13_LCDM_chi2":b["LCDM_only_DESI13"]["chi_squared"],
       "DESI13_CPL_chi2":b["CPL_only_DESI13"]["chi_squared"],
       "DESI13_delta_AIC":b["DESI13_delta_AIC_CPL_minus_LCDM"],
       "neutrino_yukawa_growth_Im_z_3":n["Casas_Ibarra_angle_samples"][-1]["Y_frobenius_squared"],
       "single_photon_CHSH_raw_and_SSR":[p["unrestricted_max_CHSH"],p["locally_twirled_max_CHSH"]],
       "json_path":str(JSON)}))


if __name__=="__main__":
    main()
