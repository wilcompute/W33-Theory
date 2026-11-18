"""B-alignment from gauge-invariant holomorphic F-term pinning, with
one-loop displacement checked against the split-E6 messenger CW loop.

At H_N,H_S vectorlike 27 singlet vevs and zero multipliers,
F_ZN=(v_N²/Lambda)*(psi-5chi - b_N),
F_ZS=(v_S²/Lambda)*(4psi - b_S).
Thus V_pin=lambda_pin*||Q b - b_target||² for equal
v_i^4/Lambda²=lambda_pin.

This is an actual E6-gauge-invariant EFT interaction, but assumes
the correctly aligned 27/27bar Higgs vevs and nonrenormalizable
operators. Other E6 78 directions are NOT checked. R-symmetry charge
R(Z_i)=2,H_i=0,B=0 makes these F terms allowed; choosing b_i
explicitly can break the independent B sign-exchange symmetry.
"""
import json,math,sys
from pathlib import Path
import numpy as np
from scipy.optimize import minimize
import mpmath as mp
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from toe_20261117_E6_FDflat_B_angle_scan import V0
from toe_20261117_E6_two_adjoint_split_27_threshold import IRREPS,threshold
OUT=ROOT/"data"/"toe_20261117_E6_B_Fterm_pinning_CW_stability.json"
Q=np.array([[1.,-5.],[4.,0.]])
bench=np.array([-.2,.2])
target=Q@bench
def Vpin(x,stiff=.1):
    v=Q@np.asarray(x)-target
    return stiff*float(v@v)
def fullV(x,stiff=.1):
    return Vpin(x,stiff)+V0(float(x[0]),float(x[1]),delta=.25)
def hessian(f,x,h=2e-5):
    n=len(x);ans=np.zeros((n,n))
    for i in range(n):
      for j in range(n):
        ei=np.eye(n)[i]*h;ej=np.eye(n)[j]*h
        ans[i,j]=(f(x+ei+ej)-f(x+ei-ej)-f(x-ei+ej)+f(x-ei-ej))/(4*h*h)
    return ans
def cw_gradient_mp():
    mp.mp.dps=45
    dim=[(dim,qp,qc) for _,dim,qp,qc,*_ in IRREPS]
    soft=mp.mpf(".25")
    def ff(q):return q*q*(mp.log(q)-mp.mpf("1.5"))
    def mm(p,c):
        tot=mp.mpf(0)
        for n,qp,qc in dim:
            B=qp*p+qc*c
            for t in (-1,1):
                v=(1+t*B)**2
                tot+=2*n*(ff(v+soft)-ff(v))/(16*mp.pi**2)
        return tot
    x=(mp.mpf("-.2"),mp.mpf(".2"))
    gradient=[float(mp.diff(lambda v:mm(v,x[1]),x[0])),
              float(mp.diff(lambda v:mm(x[0],v),x[1]))]
    return gradient
def verify():
    gradient=np.array(cw_gradient_mp())
    assert np.linalg.norm(gradient)>1e-5
    pinH=2*.1*Q.T@Q
    assert np.allclose(np.linalg.eigvalsh(pinH),[.2*(21-math.sqrt(41)),.2*(21+math.sqrt(41))])
    rows=[]
    for stiff in (.02,.05,.1,.2,.5,1.,2.,5.,10.):
        fun=lambda x:fullV(x,stiff)
        res=minimize(fun,bench,method="BFGS",
                     options={"gtol":2e-10,"maxiter":1200})
        x=np.asarray(res.x,dtype=float)
        H=hessian(fun,x)
        eig=np.linalg.eigvalsh(H)
        k=threshold(float(x[0]),float(x[1]),.25)
        mass=min(y["min_fermion_mass_abs"] for y in k["irrep"])
        assert min(eig)>0
        rows.append({"pin_stiffness":stiff,"minimizer_psi_chi":x.tolist(),
           "displacement_norm":float(np.linalg.norm(x-bench)),
           "B_pinned_plus_CW_energy":float(fun(x)),
           "gradient_norm_at_displaced_minimum":float(np.linalg.norm(
            (np.array([fun(x+np.eye(2)[i]*1e-5)-fun(x-np.eye(2)[i]*1e-5) for i in range(2)])/(2e-5)))),
           "local_Hessian_eigenvalues":eig.tolist(),
           "remaining_SU5_shape_kappa":k["kappa_SU5_TrPhi4"],
           "minimum_heavy_messenger_fermion_mass":mass})
    assert rows[-1]["displacement_norm"]<rows[0]["displacement_norm"]
    assert rows[0]["remaining_SU5_shape_kappa"]<0
    assert rows[-1]["remaining_SU5_shape_kappa"]>0
    assert rows[5]["remaining_SU5_shape_kappa"]>0 and rows[5]["minimum_heavy_messenger_fermion_mass"]<.15
    assert rows[6]["remaining_SU5_shape_kappa"]>0 and rows[6]["minimum_heavy_messenger_fermion_mass"]>.15
    def at(stiff):
        res=minimize(lambda z:fullV(z,stiff),bench,method="BFGS",
                 options={"gtol":1e-9,"maxiter":1200})
        pos=res.x
        z=threshold(float(pos[0]),float(pos[1]),.25)
        return min(v["min_fermion_mass_abs"] for v in z["irrep"]),z["kappa_SU5_TrPhi4"],pos
    lo,hi=1.,2.
    for _ in range(28):
        mid=(lo+hi)/2
        mass,kappa,pos=at(mid)
        if mass <.15:lo=mid
        else:hi=mid
    mass,kappa,pos=at(hi)
    assert abs(mass-.15)<1e-6 and kappa>0
    minpin={"pin_stiffness_at_benchmark_mass_floor_0p15":hi,
         "one_loop_psi_chi":list(map(float,pos)),
         "kappa_at_mass_floor":kappa,"mass_floor":mass,
         "not_universal":"Threshold depends on chosen F-term coefficient, messenger mass M, soft Delta, renormalization scheme, and the stipulated 0.15M cutoff; it is not an observable or UV theorem."}
    return {"status":"PASS_E6_B_GAUGE_INVARIANT_FTERM_ALIGNMENT_CW_LOCAL_MINIMA",
        "pin_mass_floor_threshold":minpin,
       "E6_operator":"W contains S_i(barH_i H_i-v_i²)+Z_i/Lambda[barH_i B H_i -b_i barH_i H_i], i=N^c, S; with aligned 27+bar27 VEVs it produces V_F=sum_i(v_i^4/Lambda²)(q_i dot B-b_i)².",
       "Q_integer":[[1,-5],[4,0]],
       "target_B_eigenvalues":target.tolist(),
       "benchmark_B_psi_chi":bench.tolist(),
       "unpinned_CW_gradient_at_benchmark":gradient.tolist(),
       "pinned_tree_Hessian_eigenvalues_at_stiff_0p1":np.linalg.eigvalsh(pinH).tolist(),
       "one_loop_local_minima":rows,
       "B_background_no_longer_stationary_after_CW":True,
       "R_parity":"With Higgs R=0, Lagrange singlets R=2 and B R=0, operators have superpotential R=2. Constant b_i can explicitly break the separate t/B mirror parity; the s/A mirror remains intact.",
       "scope":"Existence of an E6-covariant EFT F-term angular pin and numerically stable 2D B(psi,chi) local minima with messenger loop; not a global E6 scalar, D-term, temperature or proton-stability analysis. Vacuum shift is scheme-dependent unless full counterterm matching is specified."}
if __name__=="__main__":
    z=verify();OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(z,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(z["status"],z["unpinned_CW_gradient_at_benchmark"],
       z["one_loop_local_minima"][2]["minimizer_psi_chi"],
       z["one_loop_local_minima"][2]["remaining_SU5_shape_kappa"])
