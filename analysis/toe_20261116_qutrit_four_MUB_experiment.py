"""Four-MUB qutrit Bell-return witness, calibrated optical readout and shot bounds.

Reference/system state |Phi_3>, environment implements coherent SWAP storage.
Four MUB coincidence projectors satisfy sum_b P_match(b)=I+3|Phi><Phi|.
Hence F_Bell=(sum C_b-1)/3 and separable states obey sum C_b<=2.
Noise and shot claims are conditional on calibrated IID heralded trials.
"""
from __future__ import annotations
import cmath
import json
import math
from fractions import Fraction as F
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261116_qutrit_four_MUB_experiment.json"
D=3
OMEGA=cmath.exp(2j*math.pi/D)

def matmul(A,B):
    n=len(A)
    return [[sum(A[i][k]*B[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
def eye(n):
    return [[complex(i==j) for j in range(n)] for i in range(n)]
def conj(A):return [[x.conjugate() for x in row] for row in A]
def kron(A,B):
    return [[A[i//len(B)][j//len(B)] * B[i%len(B)][j%len(B)]
            for j in range(len(A)*len(B))] for i in range(len(A)*len(B))]
def mubs_identity_error():
    X=[[complex(i==(j+1)%3) for j in range(3)] for i in range(3)]
    Z=[[OMEGA**i if i==j else 0j for j in range(3)] for i in range(3)]
    U=[Z,X,matmul(X,Z),matmul(X,matmul(Z,Z))]
    S=[[0j for _ in range(9)] for _ in range(9)]
    I=eye(9)
    for u in U:
        T=kron(u,conj(u))
        T2=matmul(T,T)
        for i in range(9):
            for j in range(9):
                S[i][j]+=(I[i][j]+T[i][j]+T2[i][j])/3
    phi=[(1/math.sqrt(3) if i in (0,4,8) else 0) for i in range(9)]
    target=[[I[i][j]+3*phi[i]*phi[j] for j in range(9)] for i in range(9)]
    return max(abs(S[i][j]-target[i][j]) for i in range(9) for j in range(9))

def model(v):
    """Isotropic coherent-return noise: rho=v Phi + (1-v) I9/9."""
    v=F(v)
    if not 0<=v<=1:raise ValueError("v must be a probability")
    p_each=(1+2*v)/3
    s4=4*p_each
    fidelity=(1+8*v)/9
    assert fidelity==(s4-1)/3
    return {"visibility":str(v),"each_MUB_matching_probability":str(p_each),
            "sum_4MUB_matching":str(s4),
            "Bell_fidelity":str(fidelity),
            "separable_4MUB_bound":"2",
            "entanglement_certified_by_4MUB_ideal_mean":s4>2,
            "entanglement_certified_by_2MUB_ideal_mean":2*p_each>F(4,3)}

def shots_for_power(v,alpha=.01,beta=.1):
    """Hoeffding plan: independent n trials in each of four bases.

    Reject separability if S_hat>2+sqrt(2 ln(1/alpha)/n).
    Under isotropic v, P(fail to reject) <= beta whenever the
    true gap exceeds sum of the alpha and beta Hoeffding radii.
    """
    if not(0<alpha<1 and 0<beta<1):raise ValueError("alpha,beta in (0,1)")
    v=float(F(v))
    gap=4*(1+2*v)/3-2
    if gap<=0:return {"visibility":v,"certifiable_with_4MUB":False}
    a=math.sqrt(2*math.log(1/alpha))
    b=math.sqrt(2*math.log(1/beta))
    n=math.ceil((a+b)**2/gap**2)
    while (a+b)/math.sqrt(n)>gap+1e-12:n+=1
    return {"visibility":v,"alpha":alpha,"miss_probability_bound":beta,
            "shots_per_MUB":n,"total_heralded_detected_pairs":4*n,
            "required_gap":gap,
            "test":"reject if S_hat>2+sqrt(2*ln(1/alpha)/n)",
            "assumptions":"IID fixed isotropic visibility, properly matched conjugate MUBs, loss-independent heralding; calibration and detection loopholes excluded by assumption"}

def verify():
    err=mubs_identity_error()
    assert err<1e-12,err
    for v in (F(0),F(1,4),F(1,2),F(3,4),F(1)):
        model(v)
    assert model(F(1,4))["entanglement_certified_by_4MUB_ideal_mean"] is False
    assert model(F(1,2))["entanglement_certified_by_4MUB_ideal_mean"] is True
    assert model(F(1,2))["entanglement_certified_by_2MUB_ideal_mean"] is False
    assert shots_for_power(F(3,4))["shots_per_MUB"]==16
    assert shots_for_power(F(3,5))["shots_per_MUB"]==31
    return {"status":"PASS_FOUR_MUB_QUTRIT_BELL_WITNESS_AND_FINITE_SHOT_CONTROL",
            "operator_identity":"Sum of four matched conjugate-MUB projectors = I9 + 3*Phi3",
            "identity_max_matrix_entry_error":err,
            "exact_fidelity_relation":"F_Bell=(sum_b C_b-1)/3",
            "separable_bound":"sum_b C_b<=2 (equivalently F_Bell<=1/3)",
            "isotropic_entanglement_threshold":"v>1/4 for four MUBs; v>1/2 for two MUBs",
            "isotropic_cases":[model(v) for v in (F(0),F(1,4),F(2,5),F(3,5),F(3,4),F(9,10),F(1))],
            "conditional_power_plans":[shots_for_power(v) for v in (F(3,10),F(2,5),F(1,2),F(3,5),F(3,4),F(9,10))],
            "hardware_data":"NONE; device-dependent witness and mathematical design only",
            "physical_measurement_note":"4 settings: Z and eigenbases of X, XZ, XZ^2 on reference; complex-conjugate partner bases on system. Three time-bin rails, coherent memory and phase-stable Fourier multiports are proposed, not built."
    }

if __name__=="__main__":
    cert=verify()
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(cert,indent=2)+"\n",encoding="utf-8")
    print(cert["status"],"max error",cert["identity_max_matrix_entry_error"])
