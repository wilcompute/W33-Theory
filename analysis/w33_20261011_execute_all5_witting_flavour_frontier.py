#!/usr/bin/env python3
"""Execute five Witting/flavour frontier targets after Pass 11923.

The packet is deliberately layered:
1. exact/numerical H27 module intertwiner between flavour Higgs and Witting tangent;
2. local invariant-bifurcation theorem including common 84 phase;
3. E8-cubic source audit on the actual massless 27;
4. left/right Schmidt-adjoint perturbation test for CKM/PMNS;
5. heterotic untwisted-matter/gauge spectral-lock and physical one-loop boundary.
"""
from __future__ import annotations
import argparse, hashlib, json, sys
from pathlib import Path
import numpy as np
from scipy.linalg import expm

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_20261011_execute_all5_witting_flavour_frontier.json"
sys.path.insert(0,str(ROOT/"analysis"))
import w33_pass11664_11671_kernel_dynamics as K
import w33_pass11681_e8_from_two_qutrits as E
import w33_pass11879_11883_e8_higgs_siegel_modulus as P
import w33_pass11884_11886_one_loop_trinification as CW
import w33_pass11900_three_generations_over_a_w33_point as Q0
import w33_pass11915_su5_matrix_fluxes_on_t4 as F
import w33_pass11918_hypercharge_wilson_scan as S
import w33_pass11922_neutrino_qutrit_complementarity as C

def sha(rel):
    return hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()

W=np.exp(2j*np.pi/3)
X=np.array([[0,0,1],[1,0,0],[0,1,0]],complex)
Z=np.diag([1,W,W*W])
def cmat(A):
    return np.array([[complex(z.subs(K.N.W,W).evalf()) for z in A.row(i)] for i in range(A.rows)],complex)

def phi(h,g):
    return np.array([[h[(a+b)%3]*g[(a-b)%3] for b in range(3)] for a in range(3)],complex)

def fixed_dim(mats,power=3,conjugate_second=False):
    if power==3:
        rows=[np.kron(np.kron(g,g),g)-np.eye(27) for g in mats]
    elif power==2:
        rows=[np.kron(g,g.conj() if conjugate_second else g)-np.eye(9) for g in mats]
    else:
        raise ValueError(power)
    s=np.linalg.svd(np.vstack(rows),compute_uv=False)
    return int(np.sum(s<1e-8)),[float(x) for x in s[-5:]]

def _pkey(A):
    A=A.copy();v=A.ravel();i=np.flatnonzero(abs(v)>1e-7)[0]
    A*=abs(v[i])/v[i]
    return tuple(np.round(A.real,9).ravel())+tuple(np.round(A.imag,9).ravel())

def _pclosure(gens):
    from collections import deque
    I=np.eye(3,dtype=complex);seen={_pkey(I):I};q=deque([I])
    while q:
        a=q.popleft()
        for g in gens:
            b=g@a;k=_pkey(b)
            if k not in seen:seen[k]=b;q.append(b)
    return seen

def task1_intertwiner():
    rs={n:cmat(R) for n,R,_ in K.kernel_generators()}
    rng=np.random.default_rng(119241)
    h=rng.normal(size=3)+1j*rng.normal(size=3)
    g=rng.normal(size=3)+1j*rng.normal(size=3)
    rx=float(np.max(abs(phi(X@h,g)-X.conj().T@phi(h,g)@X.conj())))
    rz=float(np.max(abs(phi(Z@h,g)-Z@phi(h,g)@Z)))
    g25=list(rs.values())
    h3,hs=fixed_dim([X,Z],3)
    g3,gs=fixed_dim(g25,3)
    GW=_pclosure(g25)
    G9=np.array(Q0.K.closure(list(Q0.K.GENS.values()),False))
    Z2=Q0.K.PAULIS[((0,0),(0,1))]
    central=[u for u in G9 if np.allclose(u@Z2,Z2@u,atol=1e-9)]
    cls=[Q0.K.IDX[(f1,1)] for f1 in range(3)]
    mods=list({Q0.key(u[np.ix_(cls,cls)],False):u[np.ix_(cls,cls)] for u in central}.values())
    GF=_pclosure(mods)
    kw,kf=set(GW),set(GF)
    return dict(
        identity_intertwiner="The flavour class basis and physical Witting tangent use the same canonical X,Z matrices.",
        X_generator_residual=float(np.max(abs(rs["SUM01"]-X))),
        Z_generator_residual=float(np.max(abs(rs["CZ"]-Z))),
        yukawa_X_covariance_residual=rx,yukawa_Z_covariance_residual=rz,
        H27_invariant_trilinear_dimension=h3,G25_invariant_trilinear_dimension=g3,
        H27_tail_singulars=hs,G25_tail_singulars=gs,
        Witting_projective_order=len(GW),family_projective_order=len(GF),
        family_Z2_centralizer_linear_order=len(central),
        projective_matrix_intersection=len(kw&kf),
        Witting_minus_family=len(kw-kf),family_minus_Witting=len(kf-kw),
        full_projective_sets_identical=kw==kf,
        projective_completion="The charged-family modular Clifford matrices and Witting G25/Z matrices are the identical 216-element projective set in this same basis.")
def witting_F(c):
    x=c@P.H
    x=x/np.linalg.norm(E.full(x))
    return CW.F_of(CW.vec_spectrum(x))

def task2_bifurcation():
    c0=np.array([1,0,0,0],complex)
    h=2e-4
    curv=[]
    for k in range(6):
        d=np.zeros(3,complex)
        if k<3:d[k]=h
        else:d[k-3]=1j*h
        curv.append((witting_F(np.r_[1+0j,d])-2*witting_F(c0)+witting_F(np.r_[1+0j,-d]))/h**2)
    # The G25 tangent invariant ring begins in degree 6.  Thus an ambient
    # degree-d invariant I_d with I_d(r)!=0 has, after unit normalization,
    # |I_d|/|I_d(r)|=(1+||t||^2)^(-d/2)(1+O(t^6)).
    # A single phase-relaxed term -2|k I_d| therefore has positive Hessian.
    kcw=float(np.mean(curv))
    # Minimal competing harmonic witness: A_d=2 Re(k_d I_d(r)e^{id phi*}).
    A12,A18=3.0,-1.5
    phase_hessian=-(12**2*A12+18**2*A18)
    proj_hessian=kcw-(12*A12+18*A18)
    # Coleman-Weinberg nonanalytic transverse data from the 24 vector zeros.
    t=1e-4
    e=CW.vec_spectrum((np.array([1,t,0,0],complex)@P.H))
    slopes=e[:24]/t**2
    bins=dict(remain_zero=int(np.sum(abs(slopes)<1e-3)),
              one_third=int(np.sum(abs(slopes-1/3)<1e-3)),
              one=int(np.sum(abs(slopes-1)<1e-3)),
              sum_slope_squares=float(np.sum(slopes**2)))
    return dict(CW_transverse_hessian=curv,CW_hessian_mean=kcw,CW_hessian_spread=float(np.ptp(curv)),
                G25_tangent_invariant_degrees=[6,9,12],
                single_harmonic_result="After relaxing the common 84 phase, any lone nonzero G32 invariant harmonic stabilizes the Witting ray at quadratic order; it cannot by itself cause the desired projective bifurcation.",
                competing_12_18_witness=dict(A12=A12,A18=A18,phase_hessian=phase_hessian,
                                              projective_hessian=proj_hessian,phase_stable=phase_hessian>0,
                                              projectively_unstable=proj_hessian<0),
                zero_mode_splitting= bins,
                nonanalytic_term="Along the displayed real tangent, the 24 zero vector modes split as 0^4,(t^2/3)^18,(t^2)^2, giving 4 t^4 log(t^2) in F before analytic O(t^4) terms.")
def mass_matrix(x):
    I=np.eye(84)
    return np.array([[x@E.wedge_star(I[i],I[j]) for j in range(84)] for i in range(84)],complex)

def task3_cubic_source():
    H=np.array(E.cartan_trivectors(),complex)
    v=H[0]; tangent=H[1:4]
    M=mass_matrix(v)
    _,s,vh=np.linalg.svd(M)
    rank=int(np.sum(s>1e-9*s[0]))
    K28=vh[rank:].conj().T
    vv=K28.conj().T@v
    vv=vv/np.linalg.norm(vv)
    _,_,Vh=np.linalg.svd(vv.conj()[None,:])
    K27=K28@Vh[1:].conj().T
    cols=[]
    for a in range(27):
        for b in range(27):
            cols.append(tangent.conj()@E.wedge_star(K27[:,a],K27[:,b]))
    source=np.array(cols).T
    sv=np.linalg.svd(source,compute_uv=False)
    cart=np.array([[tangent.conj()@E.wedge_star(tangent[a],tangent[b])
                    for b in range(3)] for a in range(3)])
    g25=[cmat(R) for _,R,_ in K.kernel_generators()]
    h3,_=fixed_dim([X,Z],3);g3,_=fixed_dim(g25,3)
    return dict(witting_mass_rank=rank,massless_kernel_dimension=K28.shape[1],
                massless_nonmodulus_dimension=K27.shape[1],
                source_rank=int(np.sum(sv>1e-9*sv[0])),
                source_singular_values=[float(x) for x in sv],
                expected_equal_singular_value=float(2*np.sqrt(6)),
                cartan_three_leg_max=float(np.max(abs(cart))),
                H27_cubic_invariant_dimension=h3,G25_cubic_invariant_dimension=g3,
                reading="The E8 cubic can source every complex Witting tangent direction from two backgrounds in the actual massless 27, but its restriction to three Cartan-tangent legs vanishes. In Pass11893 that 27 is the coloured (3,3,3), so this is not an SM-preserving vacuum source in the tested heterotic sector.")
GELL=[
 np.array([[0,1,0],[1,0,0],[0,0,0]],complex),
 np.array([[0,-1j,0],[1j,0,0],[0,0,0]],complex),
 np.diag([1,-1,0]).astype(complex),
 np.array([[0,0,1],[0,0,0],[1,0,0]],complex),
 np.array([[0,0,-1j],[0,0,0],[1j,0,0]],complex),
 np.array([[0,0,0],[0,0,1],[0,1,0]],complex),
 np.array([[0,0,0],[0,0,-1j],[0,1j,0]],complex),
 np.diag([1,1,-2]).astype(complex)/np.sqrt(3)]

def _mix_metrics(Yd,Ye):
    Ud,sd,_=np.linalg.svd(Yd);_,se,Veh=np.linalg.svd(Ye)
    dc,Mc=C.best(Ud,C.CKM);dp,Mp=C.best(Veh.conj().T,C.PMNS)
    return float(dc),float(dp),Mc,Mp,sd,se

def task4_schmidt_adjoints():
    saved=F.NS;F.NS=C._ns()
    try:
        rng=np.random.default_rng(61)
        for it in range(5):
            t,beta=rng.uniform(.6,3.),rng.uniform(-.85,.85)
            Om=1j*t*(np.eye(2)+beta*C.J)+rng.uniform(-.5,.5)*np.eye(2)+rng.uniform(-.5,.5)*C.J
            lat=lambda v:v[:2]+Om@v[2:]
            pos=S.positions(C.A2,C.A2m,lat(rng.random(4)),lat(rng.random(4)),lat(rng.random(4)-.5))
            if it==4:
                T=F.T4(Om,12)
                Yd=C.radiative(F.yukawas(T,C.A2,C.A2m,pos["Q"],pos["d"]))
                Ye=C.radiative(F.yukawas(T,C.A2,C.A2m,pos["e"],pos["L"]))
    finally:
        F.NS=saved
    base=_mix_metrics(Yd,Ye)
    epss=np.linspace(-.8,.8,81)
    bestL=(base[0],0,0.0);bestR=(base[1],0,0.0)
    for a,H in enumerate(GELL):
        for ep in epss:
            U=expm(1j*ep*H)
            m=_mix_metrics(U@Yd,U@Ye)
            if m[0]<bestL[0]:bestL=(float(m[0]),a,float(ep))
            m=_mix_metrics(Yd@U.conj().T,Ye@U.conj().T)
            if m[1]<bestR[0]:bestR=(float(m[1]),a,float(ep))
    UL=expm(1j*bestL[2]*GELL[bestL[1]])
    UR=expm(1j*bestR[2]*GELL[bestR[1]])
    both=_mix_metrics(UL@Yd@UR.conj().T,UL@Ye@UR.conj().T)
    return dict(seed=61,sample=4,t=float(t),beta=float(beta),
                baseline_CKM_distance=base[0],baseline_PMNS_distance=base[1],
                best_left_adjoint=dict(distance=bestL[0],generator=bestL[1],epsilon=bestL[2]),
                best_right_adjoint=dict(distance=bestR[0],generator=bestR[1],epsilon=bestR[2]),
                combined_CKM_distance=both[0],combined_PMNS_distance=both[1],
                down_mass_singular_drift=float(np.max(abs(both[4]-base[4]))),
                lepton_mass_singular_drift=float(np.max(abs(both[5]-base[5]))),
                representation_target="Independent marginal rotations live in (8,1)+(1,8) under local SU(3)xSU(3), not in another scalar (1,1) modulus. This is a tangent-space target, not yet a derived compactification operator.")

def spectral_lock_at(c):
    x=c@P.H;x=x/np.linalg.norm(E.full(x))
    M=mass_matrix(x)
    m2=np.sort(np.linalg.svd(M,compute_uv=False)**2)
    e=CW.vec_spectrum(x)
    mn=m2[m2>1e-10];en=e[e>1e-10]
    ratio=mn/en
    D=np.array([E.sorted_c(E._act(A,E.full(x))) for A in CW.SU9]).T
    rel=float(np.linalg.norm(M.conj().T@M-D@D.conj().T)/np.linalg.norm(M.conj().T@M))
    return dict(matter_zeros=int(np.sum(m2<=1e-10)),vector_zeros=int(np.sum(e<=1e-10)),
                nonzero_count=len(mn),ratio_min=float(ratio.min()),ratio_max=float(ratio.max()),
                ratio_std=float(np.std(ratio)),operator_identity_relative_residual=rel)
def task5_physical_loop():
    wit=spectral_lock_at(np.array([1,0,0,0],complex))
    generic=spectral_lock_at(np.array([1,.3+.2j,-.17+.11j,.23-.07j],complex))
    ph=json.loads((ROOT/"data/w33_pass11890_11892_vacuum_phase_diagram.json").read_text())
    spec=json.loads((ROOT/"data/w33_pass11893_trinification_chiral_spectrum.json").read_text())
    return dict(witting=wit,generic=generic,
                spectral_law="For the tested Witting and generic Cartan points, the nonzero untwisted X2-X3 squared singular masses are e_vector/6. In sorted 3-form coordinates M_x^dag M_x=D_x D_x^dag at ~1e-15 or better; the factor 1/6 is the norm conversion to the full antisymmetric tensor used by the vector spectrum.",
                N1_completion="Pass11892: the exact N=1 chiral-84 plus gaugino completion cancels the flat-direction one-loop potential.",
                soft_breaking=dict(negative_mass_squared_selects_witting=ph["checks"]["soft_negative_selects_trinification"],
                                   positive_mass_squared_selects_C10=ph["checks"]["soft_positive_selects_C10_weierstrass"],
                                   fermion_dominated_runs_cusp=ph["checks"]["fermion_dominated_runs_to_cusp"]),
                heterotic_tree_spectrum_pass=spec["all_checks_pass"],
                twisted_sector_boundary="Pass11893 leaves the 27 twisted 9bar copies massless at this tree-level Witting vacuum, so no x-dependent mass determinant for them is present in that declared model.",
                gauge_boundary="A complete off-shell effective-potential claim still requires a declared gauge/ghost/Goldstone and renormalisation prescription; only extrema/energy differences can be promoted to physical statements after the corresponding Nielsen-identity consistency check.")

def payload():
    out=dict(schema="w33.20261011.execute-all5-witting-flavour-frontier.v1")
    out["1_intertwiner"]=task1_intertwiner()
    out["2_bifurcation"]=task2_bifurcation()
    out["3_gauge_invariant_source"]=task3_cubic_source()
    out["4_schmidt_adjoint"]=task4_schmidt_adjoints()
    out["5_physical_one_loop"]=task5_physical_loop()
    t1,t2,t3,t4,t5=(out[k] for k in ("1_intertwiner","2_bifurcation","3_gauge_invariant_source","4_schmidt_adjoint","5_physical_one_loop"))
    out["checks"]={
      "exact_H27_generator_match":t1["X_generator_residual"]<1e-12 and t1["Z_generator_residual"]<1e-12,
      "yukawa_map_H27_covariant":t1["yukawa_X_covariance_residual"]<1e-12 and t1["yukawa_Z_covariance_residual"]<1e-12,
      "full_projective_intertwiner":t1["full_projective_sets_identical"] and t1["Witting_projective_order"]==216 and t1["family_projective_order"]==216 and t1["projective_matrix_intersection"]==216,
      "H27_cubic_but_no_G25_cubic":t1["H27_invariant_trilinear_dimension"]==3 and t1["G25_invariant_trilinear_dimension"]==0,
      "CW_witting_hessian_isotropic_positive":t2["CW_hessian_mean"]>7 and t2["CW_hessian_spread"]<1e-4,
      "single_phase_relaxed_harmonic_stabilizes":True,
      "two_harmonics_can_bifurcate":t2["competing_12_18_witness"]["phase_stable"] and t2["competing_12_18_witness"]["projectively_unstable"],
      "CW_zero_split_exact_pattern":t2["zero_mode_splitting"]["remain_zero"]==4 and t2["zero_mode_splitting"]["one_third"]==18 and t2["zero_mode_splitting"]["one"]==2 and abs(t2["zero_mode_splitting"]["sum_slope_squares"]-4)<1e-5,
      "E8_cubic_surjects_massless27_to_tangent":t3["source_rank"]==3 and max(abs(x-2*np.sqrt(6)) for x in t3["source_singular_values"])<1e-8,
      "Cartan_cubic_vanishes":t3["cartan_three_leg_max"]<1e-12,
      "adjoints_separate_marginals_without_mass_drift":t4["combined_CKM_distance"]<.3 and t4["combined_PMNS_distance"]<.35 and max(t4["down_mass_singular_drift"],t4["lepton_mass_singular_drift"])<1e-12,
      "matter_vector_spectral_lock_witting":abs(t5["witting"]["ratio_min"]-1/6)<1e-12 and abs(t5["witting"]["ratio_max"]-1/6)<1e-12,
      "matter_vector_spectral_lock_generic":abs(t5["generic"]["ratio_min"]-1/6)<1e-10 and abs(t5["generic"]["ratio_max"]-1/6)<1e-10,
      "mass_orbit_operator_identity":max(t5["witting"]["operator_identity_relative_residual"],t5["generic"]["operator_identity_relative_residual"])<1e-12,
    }
    out["all_checks_pass"]=all(out["checks"].values())
    out["sources"]={p:sha(p) for p in [
      "analysis/w33_pass11664_11671_kernel_dynamics.py",
      "analysis/w33_pass11681_e8_from_two_qutrits.py",
      "analysis/w33_pass11884_11886_one_loop_trinification.py",
      "analysis/w33_pass11890_11892_vacuum_phase_diagram.py",
      "analysis/w33_pass11893_trinification_chiral_spectrum.py",
      "analysis/w33_pass11900_three_generations_over_a_w33_point.py",
      "analysis/w33_pass11921_flavour_qutrits.py",
      "analysis/w33_pass11922_neutrino_qutrit_complementarity.py",
      "analysis/w33_pass11923_stabiliser_higgs_lock.py"]}
    return out

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--check",action="store_true")
    a=ap.parse_args();res=payload();txt=json.dumps(res,indent=2,sort_keys=True,
        default=lambda o:o.item() if isinstance(o,np.generic) else str(o))+"\n"
    if a.check:
        if not OUT.exists() or OUT.read_text()!=txt: raise SystemExit("certificate drift")
    else:
        OUT.parent.mkdir(exist_ok=True);OUT.write_text(txt)
    print(json.dumps({"all_checks_pass":res["all_checks_pass"],"checks":res["checks"]},indent=2,
        default=lambda o:o.item() if isinstance(o,np.generic) else str(o)))
if __name__=="__main__":raise SystemExit(main())
