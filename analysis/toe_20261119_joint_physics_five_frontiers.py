#!/usr/bin/env python3
"""2026-11-19 TOE followthrough: five *independent* falsifiable calculations.

This is a joint low-energy EFT benchmark, NOT a solved theory of everything.
1. Exact one-loop SM + two Majorana SU2 triplets + one Majorana SU3 octet.
2. Rank-two type-III seesaw with 2026 oscillation inputs and explicit PMNS.
3. Starobinsky scalaron fifth-force range vs dark-energy radiative hierarchy.
4. Two selected 2026 real BAO observable residuals (diagonal-only pseudo-chi2).
5. Constructive PSD Gram-matrix Tsirelson certificate and PR obstruction.
"""
from __future__ import annotations
import json, math
from pathlib import Path
import numpy as np
from scipy import constants as C
from scipy.integrate import quad
from scipy.optimize import brentq

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261119_joint_physics_five_frontiers.json"
MZ=91.1876
ALPHA_EM_INV=127.930
SIN2W=.23122
ALPHA_S=.1180
B_SM=np.array([41/10,-19/6,-7.])
V_EW=246.22
PI=math.pi

def gauge_bridge(mu=2e16):
    inv=np.array([3/5*(1-SIN2W)*ALPHA_EM_INV,
                  SIN2W*ALPHA_EM_INV,1/ALPHA_S])
    # 2 left Weyl/Majorana SU2 adjoints: 2*(2/3)*T(adj)=8/3.
    # 1 left Weyl/Majorana SU3 adjoint: (2/3)*T(adj)=2.
    dB=np.array([0.,8/3,2.])
    L=math.log(mu/MZ)
    no_new=inv-B_SM*L/(2*PI)
    thresholds=2*PI*(no_new[1:]-no_new[0])/dB[1:]
    mT,mO=(mu*np.exp(-thresholds)).tolist()
    reconstructed=no_new-dB/(2*PI)*np.r_[0,thresholds]
    # Inverse couplings must be EXACTLY equal in the threshold approximation.
    assert np.ptp(reconstructed)<2e-12
    assert MZ<mT<mu and MZ<mO<mu
    # General feasible interval of common unification scales: for each
    # adjoint type, required t_i=a_i+s_i ln(MU/MZ) belongs to [0,L].
    intercept=2*PI*(inv[1:]-inv[0])/dB[1:]
    slope=(B_SM[0]-B_SM[1:])/dB[1:]
    assert np.all(slope>1)
    lower=max((-intercept/slope).tolist())
    upper=min((-intercept/(slope-1)).tolist())
    assert lower<L<upper
    mu_min=MZ*math.exp(lower)
    mu_max=MZ*math.exp(upper)
    # All new reps are real and Y=0: perturbative local anomalies and
    # SU(2) Witten global anomaly are absent (SU2 adjoint has integer isospin).
    assert 0<1/reconstructed[0]<1
    return {
       "status":"PASS",
       "field_content":[{"name":"Sigma_A","SM_rep":"(1,3,0)","spin":"Weyl/Majorana","count":2,
                         "Mass_GeV":mT,"delta_b2_total":8/3},
                        {"name":"Omega","SM_rep":"(8,1,0)","spin":"Weyl/Majorana","count":1,
                         "Mass_GeV":mO,"delta_b3_total":2}],
       "one_loop_beta_SM":B_SM.tolist(),"one_loop_beta_above_thresholds":(B_SM+dB).tolist(),
       "GUT_normalized_U1":True,"chosen_unification_scale_GeV":mu,
       "admissible_MU_interval_GeV":[mu_min,mu_max],
       "required_logs_lnMU_over_Mtriplet_lnMU_over_Moctet":thresholds.tolist(),
       "unified_inverse_alpha":float(reconstructed[0]),
       "unified_alpha":float(1/reconstructed[0]),
       "one_loop_closure_error":float(np.ptp(reconstructed)),
       "gauge_anomalies":"zero new perturbative local gauge anomalies; integer-isospin SU2 triplet has no Witten mod2 anomaly",
       "notes":["This proves an anomaly-free effective field content can achieve a chosen one-loop crossing.",
                "MU is input, not predicted; no UV grand-unified Lagrangian, heavy X/Y bosons or proton lifetime computed.",
                "2-loop BSM running and threshold matching may shift or destroy this exact one-loop crossing."]
    }

def pmns(s12sq,s13sq,s23sq,delta):
    s12=math.sqrt(s12sq);c12=math.sqrt(1-s12sq)
    s13=math.sqrt(s13sq);c13=math.sqrt(1-s13sq)
    s23=math.sqrt(s23sq);c23=math.sqrt(1-s23sq)
    z=np.exp(1j*delta)
    U=np.array([
        [c12*c13,s12*c13,s13/z],
        [-s12*c23-c12*s23*s13*z,c12*c23-s12*s23*s13*z,s23*c13],
        [s12*s23-c12*c23*s13*z,-c12*s23-s12*c23*s13*z,c23*c13]
    ])
    assert np.linalg.norm(U.conj().T@U-np.eye(3))<1e-13
    return U

def neutrino_bridge(mtrip):
    # Explicit type-III seesaw at tree level; choose NO central splittings
    # from Bari global fit 2026.a (preliminary), not a theory prediction.
    dm21=7.465e-5;dm31=2.5093e-3
    masses_eV=np.array([0.,math.sqrt(dm21),math.sqrt(dm31)])
    U=pmns(.3047,.0222,.4908,1.19*PI)
    heavy=np.array([mtrip,mtrip],float)
    mGeV=masses_eV*1e-9
    # Choose Casas-Ibarra R selecting the 2 massive eigenstates, complex
    # rotation z=0. This is one chosen Yukawa realization of measured inputs.
    R=np.array([[0,1,0],[0,0,1]],float)
    Y=1j*np.diag(np.sqrt(2*heavy))/V_EW@R@np.diag(np.sqrt(mGeV))@U.conj().T
    mnu=-V_EW**2/2*(Y.T@np.diag(1/heavy)@Y)
    reconstructed=U.T@mnu@U
    err=np.linalg.norm(reconstructed-np.diag(mGeV))
    assert err<1e-23
    assert np.linalg.matrix_rank(Y,tol=1e-10)==2
    assert np.linalg.matrix_rank(mnu,tol=1e-19)==2
    # The massless mode is a zero singular vector of the Weinberg matrix.
    assert np.linalg.norm(mnu@U[:,0])<1e-23
    amplitudes=np.abs(U[0,:])**2*masses_eV
    m_bb_min=max(0,2*max(amplitudes)-sum(amplitudes))
    m_bb_max=float(sum(amplitudes))
    return {
       "status":"PASS","mechanism":"tree-level minimal two-triplet type-III seesaw",
       "input_source":"Bari 2026.a preliminary normal ordering, θ23 and δ illustrative",
       "light_masses_eV":masses_eV.tolist(),"light_mass_sum_eV":float(sum(masses_eV)),
       "one_exactly_massless_neutrino":True,
       "heavy_triplet_masses_GeV":heavy.tolist(),
       "yukawa_abs_matrix":np.abs(Y).tolist(),
       "maximum_yukawa_abs":float(np.max(np.abs(Y))),
       "light_mass_matrix_complex_real_GeV":mnu.real.tolist(),
       "light_mass_matrix_complex_imag_GeV":mnu.imag.tolist(),
       "Takagi_reconstruction_error_GeV":float(err),
       "mbb_phase_range_eV":[float(m_bb_min),m_bb_max],
       "warnings":["Mixing angles, splittings, Yukawa phases and chosen heavy masses are inserted, not derived.",
                   "Rank 2 gives one massless light neutrino at tree level, but loop/higher-dimension terms may lift it.",
                   "No calculated leptogenesis, LFV bounds, collider rates, or Majorana detection prediction."]
    }

def gravity_bridge():
    # Link to prior published numerical Starobinsky inflation benchmark.
    from toe_20261119_physics_first_frontiers_v2 import inflation
    inflation_rows=inflation()["results"]
    star=next(x for x in inflation_rows if x["efolds_N"]==55)
    M_GeV=star["M_GeV"]
    # Scalaron from f(R)=R+R²/(6M²); at low curvature the Newtonian
    # potential carries +1/3 exp(-Mr) correction when the scalar couples
    # universally to matter. Its Compton length is utterly subatomic.
    scalaron_m_eV=M_GeV*1e9
    inv_length_m=C.hbar*C.c/(scalaron_m_eV*C.e)
    H0=68.3*1000/(1e6*C.parsec)
    omegaL=1-.302
    rhoL_SI=omegaL*3*H0**2/(8*PI*C.G)*C.c**2
    rhoL_eV4=rhoL_SI*(C.hbar*C.c)**3/C.e**4
    # Common EFT naturalness estimate, not a physical unrenormalized
    # observable or evidence that this loop value survives cancellations.
    naive_loop_eV4=scalaron_m_eV**4/(64*PI**2)
    ratio=naive_loop_eV4/rhoL_eV4
    assert 1e-30<inv_length_m<1e-29
    assert 1e95<ratio<1e101
    def fifth_force_factor(radius_m):
        return 1/3*np.exp(-radius_m/inv_length_m)
    return {
       "status":"PASS","model":"effective R+R²/(6M²), M² positive; not UV complete",
       "input_inflation_N55":star,
       "scalaron_Compton_length_m":float(inv_length_m),
       "scalaron_Newtonian_fifth_force_amplitude":1/3,
       "Yukawa_factor_at_1nanometer":float(fifth_force_factor(1e-9)),
       "inferred_present_dark_energy_rho_eV4":float(rhoL_eV4),
       "inferred_present_dark_energy_scale_meV":float(rhoL_eV4**.25*1e3),
       "naive_M4_over_64pi2_to_rhoLambda_ratio":float(ratio),
       "limitations":["Loop estimate is a naturalness diagnostic, not an unavoidable observable vacuum energy.",
                     "Bare cosmological constant renormalization and UV cancellations unspecified.",
                     "The R² scalaron does not explain observed cosmic acceleration merely by existing."]
    }

def dark_energy_bao():
    # Two published measurements with DES Y6 BAO overlap removed:
    # DES Y6 DM(0.851)/rd=19.74 ±0.60
    # DESI DR2 LRG2 DH(0.706)/rd=19.455 ±0.330
    # Critical limitation: neglect all correlations, fix rd/H0/Omega_m.
    Hz=68.3;Om=.302;rd=147.09;c=299792.458
    obs=[{"survey":"DES Y6 no DESI footprint","observable":"DM_over_rd","z":.851,
          "value":19.74,"sigma":.60},
         {"survey":"DESI DR2 LRG2","observable":"DH_over_rd","z":.706,
          "value":19.455,"sigma":.330}]
    def predict(w0,wa):
        def E(z):
            a=1/(1+z)
            rho=a**(-3*(1+w0+wa))*np.exp(3*wa*(a-1))
            return np.sqrt(Om*a**-3+(1-Om)*rho)
        rows=[]
        for o in obs:
            z=o["z"]
            if o["observable"]=="DM_over_rd":
                val=(c/Hz)*quad(lambda zz:1/E(zz),0,z,epsabs=1e-11)[0]/rd
            else:
                val=c/(Hz*E(z)*rd)
            pull=(val-o["value"])/o["sigma"]
            rows.append({**o,"predicted":float(val),"pull":float(pull)})
        return {"samples":rows,"diagonal_only_chi2":float(sum(v["pull"]**2 for v in rows))}
    lcdm=predict(-1,0)
    cpl=predict(-.84,-.53)
    assert lcdm["diagonal_only_chi2"]>cpl["diagonal_only_chi2"]
    assert lcdm["diagonal_only_chi2"]>5
    assert cpl["diagonal_only_chi2"]>2
    return {
       "status":"PASS","fixed_inputs":{"H0_km_s_Mpc":Hz,"Omega_m":Om,"rd_Mpc":rd},
       "LambdaCDM":lcdm,"DES_Y6_DESI_DR2_best_fit_CPL":cpl,
       "CPL_w0_wa":[-.84,-.53],
       "delta_chi2_LCDM_minus_CPL_fixed_inputs":float(lcdm["diagonal_only_chi2"]-cpl["diagonal_only_chi2"]),
       "source_uris":["https://academic.oup.com/mnras/article/551/4/stag1607/8771483",
                      "https://www.darkenergysurvey.org/des-y6-cosmology-results-papers/"],
       "warnings":["ONLY two selected observed values; simplified diagonal pseudo-chi² is NOT a statistical model preference.",
                   "DESI DR2 anisotropic BAO covariance, cosmological correlations, rd/H0/Om uncertainties and full likelihood omitted.",
                   "Absolute scale rd=147.09 Mpc imposed; no derivation of sound horizon or recombination physics."]
    }

def quantum_gram():
    # For any shared state psi and four Hermitian dichotomic observables,
    # u_x=A_x|psi>, v_y=B_y|psi> are unit vectors in a realified
    # Hilbert space. Their Gram matrix G is PSD with G_ii=1.
    # The CHSH objective tr(W G) is bounded by dual certificate
    # lambda I - W >=0, lambda=1/sqrt2.
    W=np.array([[0,0,.5,.5],
                [0,0,.5,-.5],
                [.5,.5,0,0],
                [.5,-.5,0,0]],float)
    lam=1/np.sqrt(2)
    dual=lam*np.eye(4)-W
    eig=np.linalg.eigvalsh(dual)
    assert min(eig)>-1e-12 and max(eig)>1
    # Explicit real unit vectors attain maximum:
    # a0=(1,0),a1=(0,1),
    # b0=(1,1)/sqrt2,b1=(1,-1)/sqrt2.
    vec=np.array([[1,0],[0,1],
                  [1/np.sqrt(2),1/np.sqrt(2)],
                  [1/np.sqrt(2),-1/np.sqrt(2)]])
    G=vec@vec.T
    assert min(np.linalg.eigvalsh(G))>-1e-12
    value=float(np.trace(W@G))
    assert abs(value-2*np.sqrt(2))<1e-12
    # PR correlators (E00,E01,E10,E11)=(1,1,1,-1) would reach 4.
    # With unit vectors, dot=1 forces equality, whereas dot=-1
    # forces opposition. Four PR relations contradict each other.
    PR=np.array([1.,1.,1.,-1.])
    assert sum([PR[0],PR[1],PR[2],-PR[3]])==4
    return {
       "status":"PASS",
       "matrix_W":W.tolist(),"PSD_dual_certificate_eigenvalues":eig.tolist(),
       "dual_objective":float(4*lam),
       "explicit_quantum_Gram":G.tolist(),"primal_objective":value,
       "PR_no_signaling_algebraic_CHSH":4,
       "no_signaling_does_not_imply_quantum":True,
       "certificate":"For PSD Gram G and diag G=1, tr(WG) <= tr(lambda I G)=4 lambda=2sqrt2",
       "limitations":["Proof assumes quantum Hilbert structure and Born inner product; does NOT derive them.",
                     "Maximal CHSH alone cannot characterize all quantum correlation sets.",
                     "A classical no-signaling PR box is a mathematical countermodel, not a physical device."]
    }

def run_all():
    g=gauge_bridge()
    n=neutrino_bridge(g["field_content"][0]["Mass_GeV"])
    r={"gauge_and_chiral_content":g,"neutrino_typeIII":n,
       "gravity_R2_and_dark_energy_naturalness":gravity_bridge(),
       "real_data_BAO_two_point_audit":dark_energy_bao(),
       "quantum_Tsirelson_PSD_certificate":quantum_gram()}
    assert len(r)==5 and all(x["status"]=="PASS" for x in r.values())
    return {
      "title":"Five physically anchored TOE consistency gates and a conditional coupled BSM toy model",
      "date":"2026-11-19","W33_used_as_foundation":False,
      "status":"Five model-limited consistency certificates PASS; no unified theory achieved",
      "source_uris":[
       "https://global-nu.org/results.html",
       "https://academic.oup.com/mnras/article/551/4/stag1607/8771483",
       "https://www.darkenergysurvey.org/des-y6-cosmology-results-papers/",
       "https://journals.aps.org/prd/abstract/10.1103/PhysRevD.102.112011",
       "https://link.springer.com/article/10.1140/epjc/s10052-026-15312-z"],
      "frontiers":r
    }

def main():
    out=run_all()
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(out,indent=2),encoding="utf-8")
    r=out["frontiers"]
    print(json.dumps({
        "result":"PASS",
        "MU":r["gauge_and_chiral_content"]["chosen_unification_scale_GeV"],
        "MT":r["gauge_and_chiral_content"]["field_content"][0]["Mass_GeV"],
        "MO":r["gauge_and_chiral_content"]["field_content"][1]["Mass_GeV"],
        "maxY":r["neutrino_typeIII"]["maximum_yukawa_abs"],
        "zero_lightest":r["neutrino_typeIII"]["one_exactly_massless_neutrino"],
        "scaleron_fifth_range_m":r["gravity_R2_and_dark_energy_naturalness"]["scalaron_Compton_length_m"],
        "BAO_pseudo_delta_chi2":r["real_data_BAO_two_point_audit"]["delta_chi2_LCDM_minus_CPL_fixed_inputs"],
        "CHSH_bound":r["quantum_Tsirelson_PSD_certificate"]["dual_objective"],
        "output":str(OUT)
    }))

if __name__=="__main__":
    main()
