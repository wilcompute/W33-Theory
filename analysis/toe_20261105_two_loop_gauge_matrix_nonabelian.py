#!/usr/bin/env python3
"""TOE front B: coupled TWO-LOOP gauge-only RGE, U1(Y)xU1(X)xSU2xSU3.

Noncanonical Lkin=-1/4 F^T K F; matter covariant derivative uses Q.A.
Weyl fermions have b^(1) 2/3 Q_iQ_j; complex scalar 1/3.
Two-loop (NO YUKAWA) for U1 K:
dK/dt=-B1/(8pi²) - [2 Sum_Weyl n QQ^T*(Q^T K^-1 Q+
                 C2_SU2*g2²+C2_SU3*g3²)
  +4 Sum_complex_scalar n QQ^T*(same)]/(128 pi^4).
Nonabelian beta g_a = (b_a g_a³)/(16pi²)
+g_a³ [Sum_{b=2,3} B_ab*g_b² + 2 Sum_f S_a qKq
           +4 Sum_s S_a qKq]/(16pi²)^2.
This is *gauge-only* two-loop, omits Yukawa contributions and heavy matching.
For generator/normalization verify exact SM two-loop published coefficient
B_YY=199/18 in raw Y units, B_Y2=9/2, B_Y3=44/3,
B_2Y=3/2 and B_3Y=11/6.

Vectorlike Q/antiQ included above full window; 1/2 generation scalar
S=-18 and T=-9 from preceding anomaly-free X=3(B-3Le) construction.
"""
from __future__ import annotations
import json,math,sys
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from toe_20261105_joint_flavor_u1_z9_seesaw_scalar_quality import spec
OUT=ROOT/"data/toe_20261105_full_u1matrix_su2_su3_gaugeonly_two_loop.json"
PI=math.pi;D16=(16*PI*PI)
def inventory(vectorlike=True):
    rows=[]
    for f in spec():
        typ=f["field"];ns=f["mult"]
        c2=3/4 if typ in ("Q","L") else 0.
        c3=4/3 if typ in ("Q","uc","dc") else 0.
        s2=(3/2 if typ=="Q" else (1/2 if typ=="L" else 0.))
        s3=(1 if typ=="Q" else (1/2 if typ in ("uc","dc") else 0.))
        rows.append((ns,np.array([float(f["y"]),float(f["x"])]),c2,c3,s2,s3,False))
    rows.extend([
       (2,np.array([.5,0.]),.75,0.,.5,0.,True),
       (1,np.array([0.,-9.]),0.,0.,0.,0.,True),
       (1,np.array([0.,-18.]),0.,0.,0.,0.,True)])
    if vectorlike:
        for sgn in (+1,-1):
            rows.append((6,np.array([sgn/6,sgn*1.]),.75,4/3,1.5,1.,False))
    return rows
def beta_one_mat(rows):
    B=np.zeros((2,2))
    for n,q,_,_,_,_,scalar in rows:
        B+=(1/3 if scalar else 2/3)*n*np.outer(q,q)
    return B
def two_loop_parts(rows,Ki,g2sq,g3sq):
    Kinv=np.linalg.inv(Ki)
    second=np.zeros((2,2))
    U1feedback=np.zeros(2)
    for n,q,c2,c3,s2,s3,scalar in rows:
        term=float(q@Kinv@q)
        # external abelian beta 2loop: 2 Weyl, 4 complex scalar
        second+=(4 if scalar else 2)*n*np.outer(q,q)*(term+c2*g2sq+c3*g3sq)
        # external non-Abelian two-loop beta: 2 Weyl,4 complex scalar
        U1feedback+=(4 if scalar else 2)*np.array([s2,s3])*term
    return second,U1feedback
B_NA_SM=np.array([[35/6,12.],[9/2,-26.]])
DELTA_NA=np.array([[24.5,8.],[3.,76/3]])
def delta_b(vectorlike):
    return np.array([-19/6,-7.])+ (np.array([2.,4/3]) if vectorlike else 0)
def check_SM_raw_Y():
    rows=inventory(False)
    B1=beta_one_mat(rows)
    assert abs(B1[0,0]-41/6)<1e-12
    sample=np.diag([1.,1e12])
    second,feedback=two_loop_parts(rows,sample,1.,1.)
    # evaluate individual gauge pieces by differencing
    bare,_=two_loop_parts(rows,sample,0,0)
    weak,_=two_loop_parts(rows,sample,1,0)
    strong,_=two_loop_parts(rows,sample,0,1)
    assert abs(bare[0,0]-199/18)<1e-9
    assert abs(weak[0,0]-bare[0,0]-9/2)<1e-9
    assert abs(strong[0,0]-bare[0,0]-44/3)<1e-9
    # Nonabelian external beta U1 coefficient for SU2,SU3
    def fb(K):
        return two_loop_parts(rows,K,0,0)[1]
    sample2=np.diag([1.,1e20])
    f=fb(sample2)
    assert abs(f[0]-1.5)<1e-9
    assert abs(f[1]-11/6)<1e-9
    return {"one_loop_bYY":float(B1[0,0]),"two_loop_YY_YY":float(bare[0,0]),
       "two_loop_YY_SU2":float(weak[0,0]-bare[0,0]),
       "two_loop_YY_SU3":float(strong[0,0]-bare[0,0]),
       "two_loop_SU2_YY":float(f[0]),"two_loop_SU3_YY":float(f[1])}
def integrate(M=np.eye(2),two=True):
    # Fiducial symmetry-unbroken toy window, all listed fields active:
    # no physical claim about scalar vevs, Yukawas, thresholds.
    mu0=1e10;muU=1.3163003690605982e15
    N=inventory(True)
    N2=[(n,M.T@q,c2,c3,s2,s3,scalar) for n,q,c2,c3,s2,s3,scalar in N]
    B=beta_one_mat(N2)
    kn=np.diag([1/.36**2,1/.045**2]);k0=M.T@kn@M
    y0=np.r_[k0[0,0],k0[0,1],k0[1,1],.56**2,.67**2]
    ba=delta_b(True)
    bNA=B_NA_SM+DELTA_NA
    def rhs(t,y):
        K=np.array([[y[0],y[1]],[y[1],y[2]]])
        g2sq,g3sq=y[3:]
        if np.min(np.linalg.eigvalsh(K))<=0 or min(g2sq,g3sq)<=0:
            raise ArithmeticError("Unphysical kinetic matrix")
        betaK=-B/(8*PI*PI)
        ufeedback=np.zeros(2)
        if two:
            extra,ufeedback=two_loop_parts(N2,K,g2sq,g3sq)
            betaK=betaK-extra/(128*PI**4)
        gb=np.array([g2sq,g3sq])
        dy=2*gb**2*ba/D16
        if two: dy+=2*gb**2*(bNA@gb+ufeedback)/(D16**2)
        return np.r_[betaK[0,0],betaK[0,1],betaK[1,1],dy]
    sol=solve_ivp(rhs,(0,math.log(muU/mu0)),y0,rtol=2e-10,atol=2e-11,dense_output=True)
    assert sol.success,sol.message
    y=sol.y[:,-1]
    K=np.array([[y[0],y[1]],[y[1],y[2]]])
    ev=np.linalg.eigvalsh(K)
    assert min(ev)>0
    return {"K_high":K.tolist(),"K_eigenvalues":ev.tolist(),
        "g2_high":float(math.sqrt(y[3])),"g3_high":float(math.sqrt(y[4])),
        "K_initial":k0.tolist(),"initial_mu_GeV":mu0,"end_mu_GeV":muU,
        "full_beta_one_loop":B.tolist()}
def main():
    sm=check_SM_raw_Y()
    one=integrate(two=False)
    two=integrate(two=True)
    assert abs(np.array(two["K_high"])[0,0]-np.array(one["K_high"])[0,0])>.002
    MM=np.array([[2.,1.],[1.,1.]])
    cov=integrate(MM,True)
    A=MM.T@np.array(two["K_high"])@MM
    err=float(np.max(abs(A-np.array(cov["K_high"]))))
    assert err<3e-8,err
    for q in ([1/6,1],[-.5,-9],[0,9]):
        a=np.array(q)
        v=a@np.linalg.solve(two["K_high"],a)
        vp=(MM.T@a)@np.linalg.solve(cov["K_high"],MM.T@a)
        assert abs(v-vp)<5e-11
    out={"status":"PASS_GAUGEONLY_TWO_LOOP_COUPLED_NONABELIAN_AND_TWO_U1",
      "reproduced_exact_SM_rawY_two_loop_coefficients":sm,
      "one_loop_whole_gauge_4factor":one,
      "two_loop_gauge_only_whole_4factor":two,
      "basis_transformed_two_loop":cov,
      "basis_covariance_error_K_infinity":err,
      "beta_formula":"dK/dt=-B/(8pi²)-[2SumWeyl n QQT(QK^-1Q + sum C2*g²)+4SumComplexScalar n QQT(same)]/(128pi^4). Nonabelian two-loop beta has established SM B_nonabelian, added Dirac (3,2) index terms, and 2SumWeyl S2 QK^-1Q + 4SumScalar S2 QK^-1Q.",
      "critical_missing":"Not the full two-loop EFT: top, neutrino, heavy quark Yukawa terms and scalar/Yukawa RGEs OMITTED; no matching or decoupling, no generated heavy fields at threshold and no running below U1X breaking. Gauge-only two-loop does not imply complete two-loop unification.",
      "physical_scope":"One unbroken high-scale window with all specified fields active and arbitrarily selected K,g2,g3 at 1e10GeV. X=3(B-3Le), S=-18,T=-9, one vectorlike Q; no Higgs vev or physical prediction.",
      "prior_art":["Davidson Gorbahn PRD114 055020 2026 doi:10.1103/cjy8-36vv",
        "Luo Xiao Phys Lett B555 279 2003","Machacek Vaughan general gauge beta formulas"]}
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print("GAUGE_TWOLOOP_PASS","SM",sm,"B1",one["full_beta_one_loop"],"deltaK",
          (np.array(two["K_high"])-np.array(one["K_high"])).tolist(),
          "basis_error",err,flush=True)
    return out
if __name__=="__main__":main()
