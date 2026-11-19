#!/usr/bin/env python3
"""2026-11-19 physics-first TOE gate v2, no W33 assumptions.

Five independently reproducible phenomenology calculations and a GUT-threshold
theorem. All measured inputs are explicitly imported, not "predicted".
"""
from __future__ import annotations
import itertools
import json
import math
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp, quad
from scipy.optimize import brentq, linprog

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "toe_20261119_physics_first_five_frontiers_v2.json"
PI = np.pi
MZ = 91.1876
ALPHA_EM_INV = 127.930
S2W = 0.23122
ALPHA_S = 0.1180
SM_B = np.array([41/10, -19/6, -7.])
SM_B2 = np.array([[199/50,27/10,44/5],
                  [9/10,35/6,12.],
                  [11/10,9/2,-26.]],float)
TOP_C = np.array([17/10,3/2,2.])
GEV_REDUCED_PLANCK = 2.435e18


def gauge():
    """2-loop SM gauge + 1-loop top Yukawa, explicit no-threshold benchmark."""
    inv = np.array([.6*(1-S2W)*ALPHA_EM_INV,
                    S2W*ALPHA_EM_INV, 1/ALPHA_S])
    gs = np.sqrt(4*PI/inv)
    yt_mz = .94  # Illustrative MS-bar boundary at M_Z, NOT fitted.
    tmax = math.log(1e18/MZ)

    def rhs(t, y, two):
        g = y[:3]
        yt = y[3]
        term = SM_B
        if two:
            term = term + (SM_B2 @ (g*g)-TOP_C*(yt*yt))/(16*PI*PI)
        dg = (g**3)*term/(16*PI*PI)
        dyt = yt*((9/2)*yt*yt - (17/20)*g[0]**2
                  - (9/4)*g[1]**2-8*g[2]**2)/(16*PI*PI)
        return np.r_[dg,dyt]

    def solve(two):
        sol=solve_ivp(lambda t,y:rhs(t,y,two),(0,tmax),
              np.r_[gs,yt_mz],rtol=3e-11,atol=1e-13,dense_output=True)
        assert sol.success
        def inverses(t):
            g=sol.sol(t)[:3]
            return 4*PI/(g*g)
        t12=brentq(lambda t:inverses(t)[0]-inverses(t)[1],0,tmax)
        i12=inverses(t12)
        grid=np.linspace(0,tmax,3001)
        spreads=np.array([np.ptp(inverses(t)) for t in grid])
        best_t=float(grid[np.argmin(spreads)])
        return {
           "U1_SU2_crossing_GeV":float(MZ*np.exp(t12)),
           "inverse_couplings_at_crossing":i12.tolist(),
           "inverse_U1_minus_SU3_mismatch":float(i12[0]-i12[2]),
           "minimal_inverse_coupling_spread_on_grid":float(min(spreads)),
           "best_spread_scale_GeV":float(MZ*np.exp(best_t)),
           "top_Yukawa_at_crossing":float(sol.sol(t12)[3])
        }

    one=solve(False);two=solve(True)
    # A vectorlike SU(5) Dirac 5+5bar consists of (3,1,-1/3)
    # and (1,2,+1/2); for a complete degenerate threshold each
    # component of beta b_i shifts by 2/3. This changes the common
    # alpha_U but not differences at *one loop*.
    delta_d=np.array([4/15,0.,2/3])
    delta_l=np.array([2/5,2/3,0.])
    delta=delta_d+delta_l
    assert np.allclose(delta,[2/3]*3)
    tc=np.log(1e8/MZ)
    tprobe=np.log(1e14/MZ)
    plain=inv-SM_B*tprobe/(2*PI)
    complete=plain-delta*(tprobe-tc)/(2*PI)
    assert np.max(np.abs((plain-plain[0])-(complete-complete[0])))<1e-12
    assert one["inverse_U1_minus_SU3_mismatch"]>5
    assert two["inverse_U1_minus_SU3_mismatch"]>1  # nonzero, evaluated below
    # Even allowing the color-triplet D and weak-doublet L masses of ONE
    # Dirac SU5 5+5bar to split, exactly solve both one-loop crossing
    # equations when *both thresholds are assumed between MZ and MU*.
    # The common 2/3 shift cancels from differences; the sole relevant
    # threshold variable is ln(mL/mD). The unique formal solution cannot
    # satisfy physical threshold ordering since |ln(mL/mD)|>ln(MU/MZ).
    lhs=np.array([inv[0]-inv[1],inv[0]-inv[2]])
    matrix=np.array([[SM_B[0]-SM_B[1],delta_d[0]-delta_d[1]],
                     [SM_B[0]-SM_B[2],delta_d[0]-delta_d[2]]])/(2*PI)
    t_unif,split_log=np.linalg.solve(matrix,lhs)
    Mu=float(MZ*np.exp(t_unif))
    ratio=float(np.exp(split_log))
    physical=(0<=abs(split_log)<=t_unif)
    assert 1e13<Mu<1e14 and ratio<1e-15 and not physical
    return {
       "status":"PASS",
       "MSbar_MZ_inputs":{"alpha_em_inverse":ALPHA_EM_INV,
            "sin2thetaW":S2W,"alpha_s":ALPHA_S,"yt_at_MZ_assumed":yt_mz},
       "SM_one_loop":one,"SM_two_loop_topYukawa_at_one_loop":two,
       "beta_2loop_coefficients":SM_B2.tolist(),
       "vectorlike_Dirac_SU5_5_5bar_beta_shift":delta.tolist(),
       "complete_degenerate_SU5_multiplet_changes_one_loop_pairwise_differences":False,
       "split_5_fermion_D_shift":delta_d.tolist(),
       "split_5_fermion_L_shift":delta_l.tolist(),
       "one_split_Dirac_5_pair_formal_one_loop_full_unification":{
          "scale_GeV":Mu,"ln_MU_over_MZ":float(t_unif),
          "required_ln_mL_over_mD":float(split_log),
          "required_mL_over_mD":ratio,
          "feasible_with_MZ_le_mD_mL_le_MU":bool(physical),
          "reason":"Required absolute log mass splitting exceeds total MZ-to-MU window"
        },
       "limitations":["no 2-loop y_t or Higgs quartic RGEs",
                      "no heavy thresholds, matching, Planck-scale gravitational terms",
                      "not a realistic spectrum or precision MSSM fit"]
    }


def neutrinos():
    """Exact Majorana phase envelope + electron beta decay mass for both orders."""
    input_values={
      "NO":{"dm21":7.465e-5,"dm_atm":2.5093e-3,
            "s12sq":.3047,"s13sq":.0222},
      "IO":{"dm21":7.439e-5,"dm_atm":2.5182e-3,
            "s12sq":.3036,"s13sq":.0223}
    }
    def row(order,lightest):
        p=input_values[order]
        if order=="NO":
            masses=np.array([lightest,
                   np.sqrt(lightest*lightest+p["dm21"]),
                   np.sqrt(lightest*lightest+p["dm_atm"])])
        else:
            # |Delta m32²|=m2²-m3², m3 is lightest
            masses=np.array([np.sqrt(lightest**2+p["dm_atm"]-p["dm21"]),
                      np.sqrt(lightest**2+p["dm_atm"]),lightest])
        weights=np.array([(1-p["s12sq"])*(1-p["s13sq"]),
                    p["s12sq"]*(1-p["s13sq"]),p["s13sq"]])
        assert np.isclose(sum(weights),1)
        lengths=weights*masses
        # Exact triangle/polygon inequality for two free Majorana phases.
        maximum=float(sum(lengths))
        minimum=float(max(0.,2*max(lengths)-sum(lengths)))
        beta=float(np.sqrt(np.dot(weights,masses*masses)))
        return {"lightest_eV":float(lightest),"sum_eV":float(sum(masses)),
                "mbeta_eV":beta,"mbb_min_eV":minimum,"mbb_max_eV":maximum,
                "amplitudes_eV":lengths.tolist()}

    curves={}
    for ordering in ("NO","IO"):
        curves[ordering]=[row(ordering,m) for m in
                         [0,.001,.002,.004,.008,.01,.03,.05]]
    # In IO at exactly massless m3, phase cannot cancel 1/2 contributions:
    assert .015<curves["IO"][0]["mbb_min_eV"]<.023
    assert .001<curves["NO"][0]["mbb_min_eV"]<.002
    # At some small positive m1 the NO triangle can close.
    has_zero=any(row("NO",m)["mbb_min_eV"]<1e-13
               for m in np.linspace(0,.02,401))
    assert has_zero
    # Example exact symmetric Majorana mass matrix:
    # for ANY chosen PMNS unitary U, M=U* diag(m) U^dag (Takagi)
    # reconstructs an arbitrary 3x3 complex symmetric Majorana mass.
    p=input_values["NO"];s12=np.sqrt(p["s12sq"]);c12=np.sqrt(1-p["s12sq"])
    s13=np.sqrt(p["s13sq"]);c13=np.sqrt(1-p["s13sq"])
    s23=np.sqrt(.4908);c23=np.sqrt(1-.4908)
    delta=1.19*PI
    U=np.array([
      [c12*c13,s12*c13,s13*np.exp(-1j*delta)],
      [-s12*c23-c12*s23*s13*np.exp(1j*delta),
       c12*c23-s12*s23*s13*np.exp(1j*delta),s23*c13],
      [s12*s23-c12*c23*s13*np.exp(1j*delta),
       -c12*s23-s12*c23*s13*np.exp(1j*delta),c23*c13]
    ])
    m=np.array([.006,np.sqrt(.006**2+p["dm21"]),
                np.sqrt(.006**2+p["dm_atm"])])
    mass=U.conj()@np.diag(m)@U.conj().T
    assert np.linalg.norm(U.conj().T@U-np.eye(3))<1e-12
    assert np.linalg.norm(U.T@mass@U-np.diag(m))<1e-12
    assert np.linalg.norm(mass-mass.T)<1e-12
    return {
       "status":"PASS","input_source":"Bari 2026.a preliminary global fit",
       "input":input_values,"envelopes":curves,
       "NO_has_exact_phase_cancellation_for_some_nonzero_lightest_mass":has_zero,
       "IO_zero_lightest_mass_mbb_floor_eV":curves["IO"][0]["mbb_min_eV"],
       "NO_zero_lightest_mass_mbb_floor_eV":curves["NO"][0]["mbb_min_eV"],
       "PMNS_unitarity_error":float(np.linalg.norm(U.conj().T@U-np.eye(3))),
       "Majorana_Takagi_reconstruction_error":float(np.linalg.norm(U.T@mass@U-np.diag(m))),
       "limitations":["mass and Majorana phases are not derived",
           "IO minimum at fixed central angles is not a full confidence interval",
           "nuclear matrix elements needed to compare experiments",
           "Dirac neutrinos make m_beta_beta inapplicable as usual"]
    }


def inflation():
    """Starobinsky f(R)=R+R^2/(6M^2), Einstein-frame slow-roll tests."""
    As=2.1e-9
    y_end=1+2/np.sqrt(3)
    def N_of_y(y):
        return .75*(y-y_end-np.log(y/y_end))
    def slow(N):
        y=brentq(lambda y:N_of_y(y)-N,y_end+1e-9,1e4,
                 xtol=1e-12)
        eps=4/(3*(y-1)**2)
        eta=4*(2-y)/(3*(y-1)**2)
        ns=1-6*eps+2*eta
        r=16*eps
        MoverMp=np.sqrt(32*PI**2*As*eps)/(1-1/y)
        # Exact parameter-independent field-space prediction
        assert abs(N_of_y(y)-N)<1e-10
        assert 0<MoverMp<1e-4
        return {"efolds_N":N,"exp_sqrt_2over3_phi":float(y),
                "epsilon":float(eps),"eta":float(eta),
                "scalar_tilt_ns":float(ns),"tensor_ratio_r":float(r),
                "M_over_reduced_Mplanck":float(MoverMp),
                "M_GeV":float(MoverMp*GEV_REDUCED_PLANCK)}
    rows=[slow(N) for N in (50,55,60)]
    assert all(.95<x["scalar_tilt_ns"]<.97 for x in rows)
    assert all(.002<x["tensor_ratio_r"]<.005 for x in rows)
    assert rows[0]["tensor_ratio_r"]>rows[-1]["tensor_ratio_r"]
    return {
       "status":"PASS",
       "model":"Mpl²/2 * integral sqrt(-g) [R + R²/(6M²)]",
       "Einstein_potential":"3/4 Mpl² M² [1-exp(-sqrt(2/3) phi/Mpl)]²",
       "slowroll_scalar_amplitude_assumed":As,
       "results":rows,
       "negative_R2_coefficient":"tachyonic scalaron mass squared, excludes this healthy benchmark",
       "observational_reference":"arXiv:2512.10613: ns_CMB=.9682±.0032; with_DESI=.9728±.0029; r<.034 (95%)",
       "limitations":["R² inflation is a low-energy effective model, not a UV complete quantum gravity",
           "N uncertain due reheating and unknown thermal history",
           "slow roll only and first-order spectrum; no precision Boltzmann CMB likelihood",
           "not a derivation of dark energy or standard model masses"]
    }


def cosmology():
    """CPL expansion, comoving distances and linear growth in GR."""
    Om=.302
    H0=68.3
    c_kms=299792.458
    def model(w0,wa):
        ode=1-Om
        def rho(a):
            return a**(-3*(1+w0+wa))*np.exp(3*wa*(a-1))
        def E2(a):
            return Om*a**-3+ode*rho(a)
        def dle(a):
            de=ode*rho(a)
            w=w0+wa*(1-a)
            return (-3*Om*a**-3-3*(1+w)*de)/(2*E2(a))
        def omega_m_a(a):
            return Om*a**-3/E2(a)
        def rhs(x,y):
            a=np.exp(x)
            return [y[1],-(2+dle(a))*y[1]+1.5*omega_m_a(a)*y[0]]
        ai=.001
        sol=solve_ivp(rhs,(np.log(ai),0),[ai,ai],rtol=1e-10,
                      atol=1e-12,dense_output=True)
        assert sol.success
        norm=sol.sol(0)[0]
        assert norm>0
        def at_z(z):
            a=1/(1+z)
            D,Dp=sol.sol(np.log(a))
            E=np.sqrt(E2(a))
            chi=c_kms/H0*quad(lambda zz: 1/np.sqrt(E2(1/(1+zz))),
                             0,z,epsabs=2e-9)[0]
            return {"z":z,"E":float(E),
                 "H_km_s_Mpc":float(H0*E),
                 "comoving_distance_Mpc":float(chi),
                 "growth_D_over_D_today":float(D/norm),
                 "growth_f":float(Dp/D),
                 "f_sigma8_if_sigma8_today_0p8":float(Dp/D*D/norm*.8)}
        return [at_z(z) for z in (.1,.3,.5,.7,1,2)]
    lcdm=model(-1,0)
    cpl=model(-.84,-.53)
    diffs=[]
    for a,b in zip(lcdm,cpl):
        diffs.append({"redshift":a["z"],
           "H_CPL_over_LCDM_minus1":b["E"]/a["E"]-1,
           "chi_CPL_over_LCDM_minus1":b["comoving_distance_Mpc"]/a["comoving_distance_Mpc"]-1,
           "fSigma8_CPL_over_LCDM_minus1":
                b["f_sigma8_if_sigma8_today_0p8"]/a["f_sigma8_if_sigma8_today_0p8"]-1})
    assert max(abs(x["H_CPL_over_LCDM_minus1"]) for x in diffs)>.005
    # From continuity: w(a) crossing -1 implies rho_de extremum at a_c.
    ac=1-( -1-(-.84))/(-.53)
    zc=1/ac-1
    assert abs(zc-.43243243243243)<1e-12
    return {
       "status":"PASS",
       "background":"flat GR with smooth homogeneous CPL dark energy, zero radiation/neutrinos",
       "Om0":Om,"H0_km_s_Mpc":H0,
       "DES_Y6_DESI_DR2_lowz_best_fit":{"w0":-.84,"wa":-.53,
          "rough_preference_sigma":2.3},
       "phantom_crossing_redshift":float(zc),
       "LCDM":lcdm,"CPL":cpl,"CPL_fractional_shifts":diffs,
       "growth_ODE":"D''+[2+dlnH/dlna]D'-(3/2)Omega_m(a)D=0, derivatives ln(a)",
       "limitations":["CPL best fit not itself statistically established",
           "no full data covariance, parameter variation or radiation",
           "linear scale-independent growth, no clustering dark energy",
           "same normalized sigma8(today) imposed, not CMB-normalized growth",
           "H0 and Om fixed across models for controlled differential test"]
    }


def bell():
    """Full four conditional distributions, LP local polytope threshold."""
    X=np.array([[0,1],[1,0]],complex)
    Z=np.diag([1,-1])
    id2=np.eye(2)
    A=[Z,X]
    B=[(Z+X)/np.sqrt(2),(Z-X)/np.sqrt(2)]
    psi=np.array([1,0,0,1],complex)/np.sqrt(2)
    rho=np.outer(psi,psi.conj())
    outcomes=(-1,1)
    combos=list(itertools.product(range(2),range(2),outcomes,outcomes))
    # p(a,b|x,y) convention: x,y setting indices then outcomes a,b
    P=[]
    for x,y,a,b in combos:
        Pa=(id2+a*A[x])/2
        Pb=(id2+b*B[y])/2
        prob=np.trace(rho@np.kron(Pa,Pb)).real
        P.append(prob)
    P=np.array(P)
    assert min(P)>0
    def pr(x,y,a,b):return .5 if a*b==((-1)**(x*y)) else 0.
    PR=np.array([pr(*row) for row in combos])
    White=np.full(16,.25)
    local=[]
    for ax0,ax1,by0,by1 in itertools.product(outcomes,repeat=4):
        local.append([1. if a==[ax0,ax1][x] and b==[by0,by1][y]
                      else 0. for x,y,a,b in combos])
    Aeq=np.array(local).T
    def local_feasible(p):
        result=linprog(np.zeros(16),A_eq=Aeq,b_eq=p,
                      bounds=(0,None),method="highs")
        return bool(result.success),result
    # Isotropic quantum correlator visibility v is local exactly
    # for v<=1/sqrt2 under these four binary measurements.
    for v in (0.,.50,.70,1/np.sqrt(2)):
        feasible,_=local_feasible(v*P+(1-v)*White)
        assert feasible, v
    for v in (.72,.85,1.):
        feasible,_=local_feasible(v*P+(1-v)*White)
        assert not feasible,v
    feasible_pr,_=local_feasible(PR)
    assert not feasible_pr
    def marginal_no_signaling(p):
        arr=p.reshape(2,2,2,2) # index ordering -1,+1
        for x,a in itertools.product(range(2),repeat=2):
            assert abs(arr[x,0,a,:].sum()-arr[x,1,a,:].sum())<1e-12
        for y,b in itertools.product(range(2),repeat=2):
            assert abs(arr[0,y,:,b].sum()-arr[1,y,:,b].sum())<1e-12
    marginal_no_signaling(P);marginal_no_signaling(PR)
    def E(p,x,y):
        return sum(a*b*p[i] for i,(xx,yy,a,b) in enumerate(combos)
                   if (xx,yy)==(x,y))
    def chsh(p):return E(p,0,0)+E(p,0,1)+E(p,1,0)-E(p,1,1)
    assert abs(chsh(P)-2*np.sqrt(2))<1e-12
    assert abs(chsh(PR)-4)<1e-12
    return {
       "status":"PASS",
       "quantum_distribution":P.tolist(),
       "PR_distribution":PR.tolist(),
       "quantum_CHSH":float(chsh(P)),
       "PR_nosignaling_CHSH":float(chsh(PR)),
       "critical_isotropic_visibility":float(1/np.sqrt(2)),
       "critical_isotropic_white_noise_fraction":float(1-1/np.sqrt(2)),
       "LP_local_at_visibility_0p70":True,
       "LP_nonlocal_at_visibility_0p72":True,
       "PR_nosignaling":True,
       "conclusion":"No-signaling does not imply Tsirelson or Born probabilities",
       "limitations":["ideal quantum state and measurements", "CHSH scenario not all quantum phenomena",
                      "independent source/detection loopholes not modeled",
                      "not a derivation of quantum mechanics"]
    }


def certify():
    sections={
      "two_loop_GUT_and_complete_multiplet":gauge(),
      "Majorana_phase_envelopes":neutrinos(),
      "healthy_R2_inflationary_EFT":inflation(),
      "CPL_distances_and_linear_growth":cosmology(),
      "Bell_local_polytope_and_nosignaling":bell()
    }
    assert all(x["status"]=="PASS" for x in sections.values())
    return {
      "date":"2026-11-19","claim_level":"phenomenological and analytic consistency tests, NOT solved TOE",
      "assumptions":"W33 and repo finite geometry excluded by design",
      "source_urls":[
        "https://global-nu.org/results.html",
        "https://www.darkenergysurvey.org/des-y6-cosmology-results-papers/",
        "https://link.springer.com/article/10.1140/epjc/s10052-017-4683-2",
        "https://arxiv.org/abs/2512.10613",
        "https://csnsdoc.ihep.ac.cn/article/doi/10.1088/1674-1137/ae8cf2"
      ],
      "sections":sections
    }


def main():
    result=certify()
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(result,indent=2),encoding="utf-8")
    s=result["sections"]
    print(json.dumps({
       "status":"PASS",
       "SM_two_loop_mismatch":s["two_loop_GUT_and_complete_multiplet"]["SM_two_loop_topYukawa_at_one_loop"]["inverse_U1_minus_SU3_mismatch"],
       "IO_mbb_min_meV":1000*s["Majorana_phase_envelopes"]["IO_zero_lightest_mass_mbb_floor_eV"],
       "Starobinsky_r_N55":s["healthy_R2_inflationary_EFT"]["results"][1]["tensor_ratio_r"],
       "CPL_H_fractional_z1":s["CPL_distances_and_linear_growth"]["CPL_fractional_shifts"][4]["H_CPL_over_LCDM_minus1"],
       "Bell_visibility":s["Bell_local_polytope_and_nosignaling"]["critical_isotropic_visibility"],
       "output":str(OUT)
    }))

if __name__=="__main__":
    main()
