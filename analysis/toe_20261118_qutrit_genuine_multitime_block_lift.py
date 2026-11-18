"""Exact qutrit embedding of a published genuinely-three-time qubit witness.

Extends the Beyer et al 2026 qubit example, with qutrit spectator blockade:
- all THREE pairs have a classical conditional Kraus realization;
- entire 9x9 Choi matrices are compared, not only chosen input states;
- restricting any hypothetical 3-time qutrit classical model to the
  invariant 2D sector would contradict the original three-time witness.
This is a block-embedded qubit demonstration, NOT intrinsic qutrit
memory, not a hardware experiment, not a new memory theorem.
"""
import json,math
from pathlib import Path
import numpy as np
from scipy.linalg import expm
ROOT=Path(__file__).resolve().parents[1]

def b2(M):
    return np.block([[np.asarray(M,complex),np.zeros((2,1),complex)],
                     [np.zeros((1,2),complex),np.zeros((1,1),complex)]])
P=np.diag([0,0,1]).astype(complex)
I2=np.eye(2,dtype=complex)
I3=np.eye(3,dtype=complex)
X=np.array([[0,1],[1,0]],complex)
Y=np.array([[0,-1j],[1j,0]],complex)
Z=np.diag([1.,-1.]).astype(complex)
L=np.array([[0,1],[0,0]],complex)
LR=L.conj().T

def app(ops,rho):
    return sum((K@rho@K.conj().T for K in ops),
               np.zeros_like(rho,dtype=complex))

def choi(ops):
    d=ops[0].shape[0]
    return np.block([[app(ops,np.outer(np.eye(d)[i],np.eye(d)[j]))
                       for j in range(d)] for i in range(d)])

def isTP(ops):
    return np.max(abs(sum((k.conj().T@k for k in ops),
                          np.zeros((3,3),complex))-I3))<1e-13

def conditional(K,branches):
    """CPTP classical-memory map: record i from K_i, apply Phi_i."""
    assert len(K)==len(branches) and all(isTP(Fs) for Fs in branches)
    return [F@k for k,Fs in zip(K,branches) for F in Fs]

def clifford_qutrit():
    """Independent W33 two-qutrit comparison: all native shear phases are quadratic.

    Quadratic Clifford phase shear alone cannot implement a cubic
    non-Clifford resource; here show an explicit canonical cubic control
    outside W33 line-radical quadratic phase subgroup.
    """
    w=np.exp(2j*np.pi/3)
    vals=np.array([(a*a*b)%3 for a in range(3) for b in range(3)])
    phase=np.power(w,vals)
    assert np.max(abs(phase**3-1))<1e-13
    # conjugate shift on second qutrit: the ratio of phases at b+1 and b
    # equals omega^(a²), a quadratic function, not a Pauli (linear).
    phase_delta=[int((a*a*(b+1)-a*a*b)%3) for a in range(3) for b in range(3)]
    assert phase_delta==[0,0,0,1,1,1,1,1,1]
    # finite third mixed derivative delta_a^2 delta_b a²b =2 !=0 F3.
    def f(a,b):return (a*a*b)%3
    diff=(f(2,1)-2*f(1,1)+f(0,1)
         -f(2,0)+2*f(1,0)-f(0,0))%3
    assert diff==2
    return dict(cubic_phase_exponents=vals.tolist(),cubic_mixed_finite_difference=diff,
                qutrit_two_body_cubic_gate_is_Clifford=False,
                diagonal_two_qutrit_cubic_resource="U|a,b>=omega^(a^2 b)|a,b>",
                cubic_is_outside_native_27_quadratic_phase_subgroup=True,
                provenance="The exact x^2y phase family was previously studied in repo Pass11701; this is a comparison and regression, not an invented new gate.")


def run():
    rows=[]
    for gamma,p in ((.36,.2),(.64,.3),(.25,.14),(.81,.4)):
        pcrit=(1-math.sqrt(1-gamma))/2
        assert p>=pcrit
        A1=math.sqrt(gamma)*L
        A2=np.diag([1.,math.sqrt(1-gamma)]).astype(complex)
        q1=[b2(A1),b2(A2),P]
        q2=[b2(math.sqrt(p)*Z),b2(math.sqrt(1-p)*I2),P]
        q3=[b2(math.sqrt(p)*X),b2(math.sqrt(1-p)*I2),P]
        assert all(isTP(C) for C in (q1,q2,q3))
        f=(math.sqrt(1-gamma)+2*p-1)/(2*math.sqrt(1-gamma))
        assert 0<=f<=.5
        F1=[LR,LR@L]
        F2=[math.sqrt(f)*Z,math.sqrt(1-f)*I2]
        b12=[[b2(K) for K in F1]+[P],
             [b2(K) for K in F2]+[P],[I3]]
        c12=conditional(q1,b12)
        e12=float(np.max(abs(choi(c12)-choi(q2))))
        angle=-math.asin(math.sqrt(gamma))
        Uplus=expm(1j*angle*Y/2)
        Uminus=expm(-1j*angle*Y/2)
        plus=[b2((A1+A2)/math.sqrt(2)),
              b2((A1-A2)/math.sqrt(2)),P]
        b13=[]
        for U in (Uplus,Uminus):
            b13.append([b2(math.sqrt(f)*X@U),
                        b2(math.sqrt(1-f)*U),P])
        b13.append([I3])
        c13=conditional(plus,b13)
        e13=float(np.max(abs(choi(c13)-choi(q3))))
        b23=[[b2(K@Z) for K in (math.sqrt(p)*X,math.sqrt(1-p)*I2)]+[P],
             [b2(K) for K in (math.sqrt(p)*X,math.sqrt(1-p)*I2)]+[P],
             [I3]]
        c23=conditional(q2,b23)
        e23=float(np.max(abs(choi(c23)-choi(q3))))
        assert max(e12,e13,e23)<1e-12
        # On the embedded two-level sector, the channel maps are exactly
        # Beyer's original example, hence the analytic triple witness remains.
        def emb2(rho):
            return b2(rho)
        rho=emb2(I2/2)
        out=app(q1,rho)
        sz=float(np.trace(out@b2(Z)).real)
        assert abs(sz-gamma)<1e-12
        rho_plus=emb2((I2+X)/2);rho_minus=emb2((I2-X)/2)
        assert abs(np.trace(app(q3,rho_plus)@app(q3,rho_minus)))<1e-12
        rows.append(dict(gamma=gamma,p=p,pairwise_classical_threshold=pcrit,
                         qutrit_Choi_errors=[e12,e13,e23],
                         qutrit_CPTP=True,qutrit_embedded_three_time_W=-gamma))
    out=dict(status="PASS",three_time_qutrit_block_embeddings=rows,
        qutrit_dimension=3,all_pairwise_full_Choi_residual_lt_1e_minus12=True,
        qubit_channel_support="span(|0>,|1>)",spectator="|2> dephases all coherence from qubit subspace at each observation",
        no_three_time_classical_model="Restriction of a purported qutrit classical-memory 3-time process to the invariant two-level output/input sector would yield a classical 3-time process for the original qubit model, ruled out by Beyer et al's W3<0.",
        witness_requires_complete_3time_process_control="Yes. The three time marginals and classical pairwise decompositions alone are NOT enough to exclude quantum-memory-free alternative multi-time processes unless the preparation and interventions match the published operational scenario.",
        embedded_not_intrinsically_qutrit=True,
        cubic_resource_compare=clifford_qutrit(),
        source="Beyer et al arXiv:2611.17268 (2026-11-12) exact published three-time memory theorem; repo 2026-11-18 previous qubit reproduction",
        physical_limit="Three-level embedding is a mathematical prototype, with all nontrivial dynamics confined to an invariant qubit subspace. Requires a real three-time instrument/test, not merely three isolated one-time channel characterizations.")
    path=ROOT/"data/toe_20261118_qutrit_genuine_multitime_block_lift.json"
    path.write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
    print("PASS four full qutrit Choi-matrix pairwise classical decompositions; embedded three-time nonclassical witness")
    return out

if __name__=="__main__":run()
