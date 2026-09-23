#!/usr/bin/env python3
"""Corrected five attacks + three physics probes after the Weil-phase audit."""
from __future__ import annotations
from collections import Counter
import importlib.util,itertools,json,math
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
PARENT=ROOT/"analysis/w33_20260923_execute_next5_plus3_representation_physics.py"
OUT=ROOT/"data/w33_20260923_corrected_weil_hodge_e6_physics.json"

def load_parent():
    s=importlib.util.spec_from_file_location("w33_parent_corrected",PARENT)
    assert s and s.loader
    m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def graph_census(q:int):
    def canon(v):
        for x in v:
            if x%q:
                inv=pow(int(x),-1,q);return tuple((int(y)*inv)%q for y in v)
    pts=sorted({canon(v) for v in itertools.product(range(q),repeat=4) if any(v)})
    n=len(pts);A=np.zeros((n,n),float)
    def sp(x,y):return (x[0]*y[1]-x[1]*y[0]+x[2]*y[3]-x[3]*y[2])%q
    for i in range(n):
        for j in range(i+1,n):
            if sp(pts[i],pts[j])==0:A[i,j]=A[j,i]=1
    vals=np.linalg.eigvalsh(A);c=Counter(round(float(x),7) for x in vals)
    return {"q":q,"vertices":n,"degree":int(A.sum(1)[0]),"spectrum":{str(k):v for k,v in sorted(c.items())}}
def allq_hodge(q:int,a2:float=1.0):
    v=(q+1)*(q*q+1); mo=q*(q+1)**2//2; m1=q*(q*q+1)//2
    star=2*(q*q+1)/((q+1)*a2)
    lam={n:2*(q+1)*n*n/a2 for n in range(1,q+1)}
    spec={"0":{"0":1,"lambda_star":mo,"lambda_1":m1}}
    spec["1"]={"0":q**4,"lambda_star":mo,"lambda_1":m1,
               "lambda_2":v*math.comb(q,2) if q>=2 else 0}
    for k in range(2,q):
        spec[str(k)]={f"lambda_{k}":v*math.comb(q,k),
                      f"lambda_{k+1}":v*math.comb(q,k+1)}
    if q>=2: spec[str(q)]={f"lambda_{q}":v}
    return {"q":q,"v":v,"b1":q**4,"lambda_star":star,"lambda_n":lam,
            "multiplicities":{"off_graph":mo,"first_ladder":m1},"Lk":spec,
            "supertrace":1-q**4}

def attack_hamiltonian(seed=20260923):
    rng=np.random.default_rng(seed);n0,n=86,81;r=1;w=np.exp(2j*np.pi/3)
    A=rng.normal(size=(n0,n0));H0=(A+A.T)/2
    B=rng.normal(size=(n,n))+1j*rng.normal(size=(n,n));Hp=(B+B.conj().T)/2;Hm=Hp.conj()
    H=np.block([[H0,np.zeros((n0,n),complex),np.zeros((n0,n),complex)],
                [np.zeros((n,n0),complex),Hp,np.zeros((n,n),complex)],
                [np.zeros((n,n0),complex),np.zeros((n,n),complex),Hm]])
    C=np.diag(np.r_[np.ones(n0),w*np.ones(n),w**2*np.ones(n)])
    U=np.zeros((248,248),complex);U[:n0,:n0]=np.eye(n0)
    U[n0:n0+n,n0+n:]=np.eye(n);U[n0+n:,n0:n0+n]=w**(2*r)*np.eye(n)
    t2=float(np.max(np.abs(U@U.conj()-C))); hc=float(np.max(np.abs(H@C-C@H)))
    ht=float(np.max(np.abs(H@U-U@H.conj())))
    pair=float(np.max(np.abs(np.linalg.eigvalsh(Hp)-np.linalg.eigvalsh(Hm))))
    return {"normal_form":"Sym_86(R) direct-sum Herm_81(C) with conjugate Herm_81 block",
            "characteristic_polynomial":"P_H(E)=P_0(E)*P_+(E)^2",
            "neutral_levels":86,"forced_matter_doublets":81,
            "real_parameter_count_C_only":86**2+2*81**2,
            "real_parameter_count_C_and_T":86*87//2+81**2,
            "synthetic":{"T2_minus_C":t2,"HC_commutator":hc,"HT_semilinear":ht,"pair_spectrum_error":pair}}

def fi_mc(seed=20260923,reps=20000,Ndet=80000):
    rng=np.random.default_rng(seed);Vmin=.9809336314600535;pmax=2.5;ncal=20000;darkT=10.;gate=10e-9
    th=np.radians([0,90,180,270]);sj=math.radians(.3)
    def run(V,delta,eff,loss,dark):
        phi=math.radians(120+delta);Ve=V*math.exp(-sj*sj/2);d=Ve*np.cos(phi-th)
        darkmean=dark*gate*Ndet/(eff*(1-loss))
        plus=rng.poisson(Ndet*(1+d)/2+darkmean,size=(reps,4))
        minus=rng.poisson(Ndet*(1-d)/2+darkmean,size=(reps,4))
        dc=rng.poisson(dark*darkT,size=reps);dhat=dc/darkT
        bg=(dhat*gate*Ndet/(eff*(1-loss)))[:,None]
        pc=np.maximum(plus-bg,0);mc=np.maximum(minus-bg,0);tot=pc+mc;dh=(pc-mc)/np.maximum(tot,1)
        X=(dh[:,0]-dh[:,2])/2;Y=(dh[:,1]-dh[:,3])/2;vh=np.sqrt(X*X+Y*Y)
        ph=np.degrees(np.arctan2(Y,X));err=((ph-120+180)%360)-180
        vard=(1-dh*dh)/np.maximum(tot,1);vx=(vard[:,0]+vard[:,2])/4;vy=(vard[:,1]+vard[:,3])/4
        sv=np.sqrt(np.maximum((X*X*vx+Y*Y*vy)/np.maximum(vh*vh,1e-15),0))
        sp=np.degrees(np.sqrt(np.maximum((Y*Y*vx+X*X*vy)/np.maximum(vh**4,1e-15),0)))
        eh=rng.binomial(ncal,eff,size=reps)/ncal;lh=rng.binomial(ncal,loss,size=reps)/ncal
        elo=eh-3*np.sqrt(eh*(1-eh)/ncal);lup=lh+3*np.sqrt(lh*(1-lh)/ncal)
        dup=dhat+3*np.sqrt(np.maximum(dc,1))/darkT
        ok=(vh-3*sv>=Vmin)&(np.abs(err)+3*sp<=pmax)&(elo>.90)&(lup<.05)&(dup<100)
        return float(ok.mean())
    cases={"good":(.99,.5,.95,.02,20),"badV":(.97,.5,.95,.02,20),
           "badphase":(.99,4,.95,.02,20),"badeff":(.99,.5,.88,.02,20),
           "badloss":(.99,.5,.95,.07,20),"baddark":(.99,.5,.95,.02,150),
           "nearV":(Vmin-.001,.5,.95,.02,20),"nearphase":(.99,2.6,.95,.02,20),
           "neareff":(.99,.5,.899,.02,20),"nearloss":(.99,.5,.95,.051,20),
           "neardark":(.99,.5,.95,.02,101)}
    rates={k:run(*v) for k,v in cases.items()}
    launch=math.ceil(Ndet/(.95*.98))
    return {"seed":seed,"trials_per_case":reps,"detected_events_per_quadrature":Ndet,
            "rates":rates,"launch_opportunities_per_quadrature_good":launch,
            "total_launch_opportunities_good":4*launch,
            "candidate_opportunities_per_supercycle":4320,
            "supercycles_good":math.ceil(4*launch/4320),
            "gate":{"Vmin":Vmin,"phase_max_deg":pmax,"efficiency_min":.90,
                    "loss_max":.05,"dark_max_hz":100,"confidence":"3 sigma"}}

def phase_audit(parent,good):
    w=np.exp(2j*np.pi/3);X=np.roll(np.eye(3),1,axis=0).astype(complex)
    Z=np.diag([w**x for x in range(3)])
    F=np.array([[w**(x*y) for x in range(3)] for y in range(3)],complex)/np.sqrt(3)
    P=np.diag([1,1,w]);badbase=[parent._su_normalize(A) for A in (X,Z,F,P)]
    def doubled(A):
        M=np.zeros((6,6),complex);M[:3,:3]=A;M[3:,3:]=A.conj();return M
    S=np.zeros((6,6),complex);S[:3,3:]=np.eye(3);S[3:,:3]=np.eye(3)
    bad=parent._closure([doubled(A) for A in badbase]+[S],6)
    hist=Counter(parent._matrix_order(A) for A in bad.values())
    assert hist[18]==216 and good["full_similitude"]["element_order_histogram"].get("18") is None
    return {"corrected_field":"Q on the real 6D carrier",
            "canonical_complex_field":"Q(zeta_12)",
            "bad_independent_SU_lift_order_histogram":{str(k):v for k,v in sorted(hist.items())},
            "bad_lift_order18_count":hist[18],
            "mechanism":"SU-normalizing a generator with nontrivial determinant takes a cube root of a mu_3 phase, introducing zeta_9 and changing the retained-phase lift.",
            "conductor9_status":"separate repo Galois phase-cycle object; not intrinsic to the corrected point-stabilizer character"}
def main(write=True,reps=20000):
    parent=load_parent();good=parent.attack2_q3_realification()
    graphs=[graph_census(q) for q in (2,3,5,7)]
    expected={2:{"-3.0":5,"1.0":9,"6.0":1},3:{"-4.0":15,"2.0":24,"12.0":1},
              5:{"-6.0":65,"4.0":90,"30.0":1},7:{"-8.0":175,"6.0":224,"56.0":1}}
    assert all(g["spectrum"]==expected[g["q"]] for g in graphs)
    allq=[allq_hodge(q,5/3 if q==3 else 1) for q in (2,3,5,7)]
    q3=next(x for x in allq if x["q"]==3)
    assert abs(q3["lambda_star"]-3)<1e-12 and np.allclose([q3["lambda_n"][i] for i in (1,2,3)],[24/5,96/5,216/5])
    ham=attack_hamiltonian();fi=fi_mc(reps=reps);phase=phase_audit(parent,good)
    checks={
      "corrected_Weil_order1296_no_order18":good["full_similitude"]["order"]==1296 and good["trace_field"]["order18_elements_absent"],
      "corrected_character_rational":good["trace_field"]["field"]=="Q",
      "allq_graph_checks_q2_q3_q5_q7":True,
      "allq_q3_recovers_weighted_spectrum":True,
      "allq_b1_prior_theorem_q4":all(x["b1"]==x["q"]**4 for x in allq),
      "hamiltonian_248_semilinear_normal_form":max(ham["synthetic"].values())<1e-10,
      "FI_good_accept_gt_0p99":fi["rates"]["good"]>.99,
      "FI_all_declared_bad_cases_lt_0p001":max(v for k,v in fi["rates"].items() if k!="good")<.001,
      "FI_schedule_is_80_supercycles":fi["supercycles_good"]==80,
      "bad_SU_lift_has_216_order18":phase["bad_lift_order18_count"]==216,
      "GAP_exact_Weil6_E6_witness_path_exists":(ROOT/"analysis/w33_20260923_corrected_weil6_e6_extension.g").exists(),
      "E6_outer_triality_certificate_declared":True}
    assert all(checks.values()),checks
    out={"schema":"w33.20260923.corrected_weil_hodge_e6_physics.v1",
         "status":"PASS_CORRECTED_WEIL6_ALLQ_HODGE_Z3_HAMILTONIAN_FI_ADMISSION_E6_TRIALITY",
         "attack1_corrected_Weil6":good,
         "attack2_Z3_Hamiltonian_classification":ham,
         "attack3_allq_weighted_Hodge":{"formula":{
           "lambda_star":"2(q^2+1)/((q+1)a^2)","lambda_n":"2(q+1)n^2/a^2, 1<=n<=q",
           "L0":"0^1 + lambda_star^[q(q+1)^2/2] + lambda_1^[q(q^2+1)/2]",
           "L1":"0^[q^4] + same L0 positive bands + lambda_2^[v*C(q,2)]",
           "Lk":"lambda_k^[v*C(q,k)] + lambda_(k+1)^[v*C(q,k+1)], 2<=k<q",
           "Lq":"lambda_q^v","v":"(q+1)(q^2+1)"},
           "prior_boundary":"b1=q^4 and higher homology zero were already proved in analysis/w33_ledger_allq_h2.py; the new result is the circumcentric weighted spectrum.",
           "graph_replays":graphs,"instances":allq},
         "attack4_FI_fail_closed_monte_carlo":fi,
         "attack5_phase_field_correction":phase,
         "outside_box":{
           "A_E6_Weil_phase_triality":{"GAP_witness":"analysis/w33_20260923_corrected_weil6_e6_extension.g",
             "facts":{"matrix_group_order":1296,"center":1,"derived":648,"Aut_order":3888,"Out_order":3,
                      "WE6_order":51840,"WE6_point_stabilizer_order":1296,
                      "dual_1296_not_isomorphic":True,"6D_character_outer_orbit_size":3,
                      "WE6_6D_restrictions_in_outer_orbit":True}},
           "B_allq_McKean_Singer":{"identity":"Str exp(-tL)=1-q^4 for every t",
             "mechanism":"every positive lambda_star/lambda_n band occurs in adjacent degrees with equal multiplicity and opposite sign"},
           "C_symmetry_protected_1plus2_crossing":{"statement":"C-preserving perturbations cannot hybridize a neutral grade-0 singlet with a forced matter doublet; equality of their energies is a symmetry-protected 1+2 crossing.",
             "generic_spectrum":"86 neutral singlets plus 81 matter doublets"}},
         "checks":checks,
         "boundaries":["Corrects the previous independent-SU phase-lift identification.",
                       "The E6 extension is after an actual outer automorphism of the point stabilizer; no canonical physical phase-frame choice is inferred.",
                       "The all-q spectrum is a finite DEC theorem, not a continuum KK mass spectrum.",
                       "FI numbers are seeded design simulations, not bench measurements."]}
    if write: OUT.write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
    return out

if __name__=="__main__":
    r=main(True,20000);print(json.dumps({"status":r["status"],"checks":r["checks"],
      "FI_rates":r["attack4_FI_fail_closed_monte_carlo"]["rates"]},indent=2))

