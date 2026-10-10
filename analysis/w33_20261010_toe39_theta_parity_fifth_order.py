"""TOE39: parity block and fifth-order determinant law for level-3 genus-2 theta-nulls.

Independently reconstructs the theta series; never treats singular values as
modular-invariant masses. The exact statements are proved in the paired note.
"""
from __future__ import annotations
import json
import math
from pathlib import Path
import numpy as np

P = np.array([[1,0,0],[0,0,1],[0,1,0]], dtype=int)
U = np.array([[1,0,0],[0,2**-.5,2**-.5],[0,2**-.5,-2**-.5]], dtype=float)

def theta(tau1: complex, tau2: complex, eps: complex, N: int = 14):
    n = np.arange(-N, N+1, dtype=float)
    x = [n+c/3 for c in range(3)]
    out = np.zeros((3,3),dtype=complex)
    for a in range(3):
        for b in range(3):
            u,v = x[a][:,None],x[b][None,:]
            out[a,b] = np.exp(3j*np.pi*(tau1*u*u+2*eps*u*v+tau2*v*v)).sum()
    return out

def moments(tau: complex, N: int = 14):
    n = np.arange(-N,N+1,dtype=float)
    a=np.empty((3,3),dtype=complex)
    for c in range(3):
        x=n+c/3
        w=np.exp(3j*np.pi*tau*x*x)
        for r in range(3): a[c,r]=np.sum(x**r*w)
    return a

def run():
    cases=[(.173+1.07j,.286+1.29j),
           (.113+1.31j,-.21+1.19j),
           (1j, .5+1.05j)]
    rows=[]
    for t1,t2 in cases:
        e=.04
        T=theta(t1,t2,e)
        Tminus=theta(t1,t2,-e)
        parity=max(np.max(abs(P@T-Tminus)),
                   np.max(abs(T@P-Tminus)),np.max(abs(P@T@P-T)))
        block=U.T@T@U
        offblock=max(np.max(abs(block[2,:2])),np.max(abs(block[:2,2])))
        odd_det=abs(np.linalg.det(T)+np.linalg.det(Tminus))
        Tzero=U.T@theta(t1,t2,0)@U
        even0_rank2_det=abs(np.linalg.det(Tzero[:2,:2]))
        odd0=abs(Tzero[2,2])
        c=(6j*np.pi)**3*np.linalg.det(moments(t1))*np.linalg.det(moments(t2))/2
        assert abs(c)>1e-9
        es=[.08,.04,.02,.01]
        errors=[float(abs(np.linalg.det(theta(t1,t2,z))/(c*z**3)-1)) for z in es]
        assert parity<1e-12 and offblock<1e-12 and odd_det<1e-12
        assert even0_rank2_det<1e-12 and odd0<1e-12
        assert max(errors)<.2 and all(errors[j+1]<.30*errors[j] for j in range(3)),errors
        rows.append(dict(tau1=str(t1),tau2=str(t2),parity_residual=float(parity),
                         off_block_residual=float(offblock),
                         odd_determinant_residual=float(odd_det),
                         split_even_det_residual=float(even0_rank2_det),
                         split_odd_residual=float(odd0),
                         epsilons=es,leading_cubic_relative_errors=errors,
                         halving_error_ratios=[errors[i+1]/errors[i] for i in range(3)]))
    return dict(status="PASS",cases=rows,
                theorem="P Theta(e)=Theta(-e)=Theta(e) P; P Theta(e) P=Theta(e); det Theta(-e)=-det Theta(e).",
                block="In P-parity coordinates Theta(e)=Theta_even(e**2) direct_sum e*Theta_odd(e**2), with a 2x2 even block and 1x1 odd block.",
                determinant="det Theta(e)=C*e**3+O(e**5); C=(6*pi*i)**3/2*det(u0,u1,u2)*det(v0,v1,v2).",
                boundary="Exact analytic theta-series parity plus numerical truncation tests. Does not fix a modulus, assign Yukawa couplings, or derive measured masses.")

if __name__=="__main__":
    result=run()
    output=Path(__file__).resolve().parents[1]/"data"/"w33_20261010_toe39_theta_parity_fifth_order.json"
    output.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"status":result["status"],"case_count":len(result["cases"]),"certificate":str(output)},indent=2))
