"""SU5-boundary octet projector and transparent 2-loop N=1 gauge running.

No 5D supersymmetric action, spectrum, proton lifetime or global G2 input.
"""
from pathlib import Path
import json
from math import pi,log
import numpy as np
from scipy.integrate import solve_ivp
from scipy.linalg import expm
import sympy as s
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261119_boundary_octet_two_loop_RG.json"
R=s.Rational

def projectors():
    H=np.diag([2,2,2,-3,-3]).astype(complex)
    P3=(H+3*np.eye(5))/5
    P2=(2*np.eye(5)-H)/5
    assert np.max(abs(P3@P3-P3))<1e-13
    assert np.max(abs(P2@P2-P2))<1e-13
    def p8(X):
        return P3@X@P3-np.trace(P3@X)/3*P3
    def p3(X):
        return P2@X@P2-np.trace(P2@X)/2*P2
    basis=[]
    for i in range(5):
        for j in range(i+1,5):
            X=np.zeros((5,5),complex);X[i,j]=X[j,i]=1
            Y=np.zeros((5,5),complex);Y[i,j]=1j;Y[j,i]=-1j
            basis.extend((X,Y))
    for i in range(4):
        X=np.zeros((5,5),complex);X[i,i]=1;X[i+1,i+1]=-1
        basis.append(X)
    assert len(basis)==24
    ranks=(np.linalg.matrix_rank(np.column_stack([p8(x).ravel() for x in basis])),
           np.linalg.matrix_rank(np.column_stack([p3(x).ravel() for x in basis])))
    assert ranks==(8,3),ranks
    # A color↔weak conjugation violates the octet-projector covariance
    # under full SU5 but not under the low-energy block SM gauge group.
    mix=np.zeros((5,5),complex);mix[0,3]=mix[3,0]=1.
    X=basis[0]
    # X=offdiag color generator, P8(X)=X, while rotation leaks X
    U=expm(1j*.37*mix)
    fullnorm=float(np.linalg.norm(p8(U@X@U.conj().T)-U@p8(X)@U.conj().T))
    assert fullnorm>.01
    # SU3xSU2 block conjugations commute with color/weak projectors.
    B=np.zeros((5,5),complex);B[0,1]=B[1,0]=1;B[3,4]=B[4,3]=1
    V=expm(1j*.17*B)
    smallnorm=float(np.linalg.norm(p8(V@X@V.conj().T)-V@p8(X)@V.conj().T))
    assert smallnorm<1e-13
    return {"SU5_adjoint_dimension":24,
      "SM_brane_color_projector_formula":"Pcolor=(H+3I)/5 with H=diag(2,2,2,-3,-3)",
      "octet_operator":"P8(X)=Pcolor*X*Pcolor-tr(Pcolor*X)/3*Pcolor",
      "triplet_operator":"P3(X)=Pweak*X*Pweak-tr(Pweak*X)/2*Pweak",
      "SM_octet_rank":ranks[0],"SM_weak_triplet_rank":ranks[1],
      "SU5_non_covariance_witness_norm":fullnorm,
      "SM_covariance_witness_norm":smallnorm,
      "effective_boundary_operator":"m8 tr((P8 Psi2)(P8 Psi2)) at the SU5-broken boundary; SM invariant, not SU5 invariant",
      "unbuilt":"Actual 5D supersymmetric adjoint Majorana boundary action, spinor parity/orbifold consistency, KK tower, UV-brane mass mechanism and anomaly inflow."}

def beta_for_vectorlike_pair(name):
    if name=="doublet":
        d3,d2,Y=1,2,R(1,2)
    elif name=="triplet":
        d3,d2,Y=3,1,R(1,3)
    else:raise ValueError(name)
    Ti=[2*R(3,5)*Y*Y*d3*d2,
        2*R(1,2)*d3 if d2>1 else R(0),
        2*R(1,2)*d2 if d3>1 else R(0)]
    Ci=[R(3,5)*Y*Y, R(3,4) if d2>1 else R(0),R(4,3) if d3>1 else R(0)]
    CG=[0,2,3]
    Bij=s.Matrix([[4*Ti[i]*Ci[j]+(2*CG[i]*Ti[i] if i==j else 0)
                   for j in range(3)] for i in range(3)])
    return s.Matrix(Ti),Bij

def solve_RGE():
    dbl,BD=beta_for_vectorlike_pair("doublet")
    tri,BT=beta_for_vectorlike_pair("triplet")
    assert dbl==s.Matrix([R(3,5),1,0])
    assert tri==s.Matrix([R(2,5),0,1])
    assert BD==s.Matrix([[R(9,25),R(9,5),0],[R(3,5),7,0],[0,0,0]])
    assert BT==s.Matrix([[R(8,75),0,R(32,15)],[0,0,0],[R(4,15),0,R(34,3)]])
    assert dbl+tri==s.ones(3,1)
    mZ=91.1876;msusy=1000.;MU=2.e16
    aem=1/127.95;sin2=.23122;alphas=.1181
    a1=(5/3)*aem/(1-sin2);a2=aem/sin2
    inva_mz=np.array([1/a1,1/a2,1/alphas])
    bSM=np.array([41/10,-19/6,-7],float)
    inv0=inva_mz-bSM/(2*pi)*log(msusy/mZ)
    bm=np.array([33/5,1,-3],float)
    BM=np.array([[199/25,27/5,88/5],[9/5,25,24],[11/5,9,14]],float)
    bD=np.array(dbl,float).reshape(3);bT=np.array(tri,float).reshape(3)
    D=np.array(BD,float);T=np.array(BT,float)
    def run_scenario(tensor,MT):
        # Selected one-loop threshold and full N=1 gauge-gauge two-loop
        # coefficients above msusy; no heavy GUT matching or Yukawa terms.
        if tensor=="MSSM only":
            blocks=[(msusy,MU,bm,BM)]
        elif tensor=="extra light doublet at 1TeV / heavy triplet":
            blocks=[(msusy,MT,bm+bD,BM+D),(MT,MU,bm+bD+bT,BM+D+T)]
        elif tensor=="MSSM plus heavy triplet at MT":
            blocks=[(msusy,MT,bm,BM),(MT,MU,bm+bT,BM+T)]
        else:raise ValueError(tensor)
        a=inv0.copy()
        for lo,hi,b,B in blocks:
            if hi<=lo:continue
            def rhs(t,inv):
                assert min(inv)>1e-3
                alpha=1/np.array(inv)
                return -b/(2*pi)-(B@alpha)/(8*pi*pi)
            sol=solve_ivp(rhs,(log(lo),log(hi)),a,method="DOP853",
                          rtol=2e-11,atol=2e-12)
            assert sol.success
            a=sol.y[:,-1]
        return {"description":tensor,"triplet_threshold_GeV":MT,
           "alpha_inverse_at_MU":a.tolist(),
           "unification_mismatch_at_MU_12_13_23":[float(a[0]-a[1]),float(a[0]-a[2]),float(a[1]-a[2])]}
    cases=[run_scenario("MSSM only",MU),
           run_scenario("MSSM plus heavy triplet at MT",1e14),
           run_scenario("MSSM plus heavy triplet at MT",1e16),
           run_scenario("extra light doublet at 1TeV / heavy triplet",1e14),
           run_scenario("extra light doublet at 1TeV / heavy triplet",1e16)]
    return {"gauge_boundary":projectors(),
       "N1_two_loop_extra_doublet_B": [[str(z) for z in row] for row in BD.tolist()],
       "N1_two_loop_extra_triplet_B": [[str(z) for z in row] for row in BT.tolist()],
       "extra_complete_SU5_5_b":[str(z) for z in list(dbl+tri)],
       "input_SM_at_MZ":{"alphaEM_inverse":127.95,"sin2theta":sin2,"alphaS":alphas,"mZ_GeV":mZ},
       "simplified_matching_scale_GeV":msusy,"fixed_evaluation_scale_GeV":MU,
       "MSSM_b2loop_gauge_matrix":BM.tolist(),
       "scenarios":cases,
       "colored_triplet_d5_proton_amplitude_relative_if_mass_1e14_vs_1e16":100.,
       "colored_triplet_d5_proton_rate_relative_if_mass_1e14_vs_1e16":10000.,
       "illustrative_proton_decay_experimental_reference":"Super-K p->e+pi0 partial lifetime >2.4e34 years (90% CL), Phys Rev D102 112011 (2020), a dimension-six channel, NOT a direct numerical limit on this dimension-five triplet amplitude.",
       "limitations":"Simplified 1-loop SM MZ->1TeV, two-loop N=1 gauge-gauge terms, sharp thresholds; no MSSM Yukawas, threshold matching at SUSY and GUT, 5D KK spectrum, Planck operators, physical proton matrix elements, dimension-five wino/higgsino dressing or experimentally fit unification scale. No actual 5D/G2 compact vacuum."}

def run():
    r=solve_RGE()
    OUT.write_text(json.dumps(r,indent=2,default=lambda x:x.item() if isinstance(x,np.generic) else str(x))+"\n",encoding="utf8")
    for c in r["scenarios"]:print(c["description"],c["triplet_threshold_GeV"],np.round(c["unification_mismatch_at_MU_12_13_23"],4))
    print("PASS octet projector 8, weak triplet 3; derived extra two-loop SUSY B")
    print(OUT)
    return r
if __name__=="__main__":run()
