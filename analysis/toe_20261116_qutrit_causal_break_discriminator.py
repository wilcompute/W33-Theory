"""Causal-break qutrit experiment with matched one-step channels.

A classical latent h in F3 controls X^h on two successive time slots.
The independent-h reference is Markovian; persistent h is non-Markovian
despite *identical* one-slot shift-twirled CPTP maps and marginals.
The witness is classical temporal memory, not temporal entanglement.
"""
from fractions import Fraction as Q
from math import comb,log2
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261116_qutrit_causal_break_discriminator.json"

def joint(theta):
    t=Q(theta)
    if not 0<=t<=1:raise ValueError("theta must be in [0,1]")
    return [[(t/Q(3) if j==k else Q(0))+(1-t)/Q(9)
             for k in range(3)] for j in range(3)]

def witness(theta):
    P=joint(theta)
    p_same=sum(P[j][j] for j in range(3))
    assert all(sum(row)==Q(1,3) for row in P)
    assert all(sum(P[j][k] for j in range(3))==Q(1,3) for k in range(3))
    total=sum(map(sum,P),Q(0))
    assert total==1
    t=Q(theta)
    assert p_same==(1+2*t)/3
    info=sum(float(p)*log2(float(9*p)) for row in P for p in row if p)
    return {"persistent_memory_fraction":str(t),
      "joint_rational":[[str(x) for x in row] for row in P],
      "probability_matching_outcomes":str(p_same),
      "witness_excess_over_markov":str(p_same-Q(1,3)),
      "mutual_information_bits":info,
      "identical_one_slot_channel":"E(rho)=sum_h X^h rho X^-h/3 (Fourier-basis dephasing; entanglement-breaking)",
      "recorded_causal_break":"measure j at t1 in computational basis; reset independently to |0>; then measure k at t2"}

def pvalue_null(n:int,matches:int):
    if n<1 or not 0<=matches<=n:raise ValueError("invalid shot count")
    return sum((Q(comb(n,j))*Q(1,3)**j*Q(2,3)**(n-j)
                for j in range(matches,n+1)),Q(0))

def quantum_memory_bell_return():
    """Exact qutrit Bell-return witness after a genuine causal break.

    R:S starts |Phi3>; E starts |0>. SWAP(S,E), reprepare S=|0>,
    SWAP(S,E) restores the Bell pair; a measure/store/reprepare
    classical memory instead produces sum_j |jj><jj|/3.
    Both give the identical computational coincidence table.
    """
    n=9
    labels=[3*j+j for j in range(3)]
    bell=[[Q(0) for _ in range(n)] for _ in range(n)]
    classical=[[Q(0) for _ in range(n)] for _ in range(n)]
    for x in labels:
        classical[x][x]=Q(1,3)
        for y in labels:bell[x][y]=Q(1,3)
    def fid(state):
        return sum((bell[i][j]*state[j][i] for i in range(n)
                    for j in range(n)),Q(0))
    def pt_B(state):
        out=[[Q(0) for _ in range(n)] for _ in range(n)]
        for a in range(3):
            for b in range(3):
                for c in range(3):
                    for d in range(3):
                        out[3*a+d][3*c+b]=state[3*a+b][3*c+d]
        return out
    swap=[[Q(1) if i//3==j%3 and i%3==j//3 else Q(0)
           for j in range(n)] for i in range(n)]
    assert [[3*v for v in row] for row in pt_B(bell)]==swap
    assert pt_B(classical)==classical
    assert fid(bell)==1 and fid(classical)==Q(1,3)
    # Coherent SWAP memory basis amplitudes (overall 1/sqrt(3)):
    initial=[(j,j,0) for j in range(3)]   # (reference,system,env)
    after_first_swap=[(r,e,s) for r,s,e in initial]
    after_causal_break=[(r,0,e) for r,s,e in after_first_swap]
    final=[(r,e,s) for r,s,e in after_causal_break]
    assert final==initial
    # Bell partial transpose = SWAP/3: six +1/3 and three -1/3
    # eigenvalues; the classical memory's transpose is positive.
    return {"coherent_Bell_return_fidelity":str(fid(bell)),
            "classical_memory_Bell_return_fidelity":str(fid(classical)),
            "coherent_partial_transpose_negative_eigenvalues":3,
            "coherent_negativity":"1",
            "classical_partial_transpose_negative_eigenvalues":0,
            "computational_joint_probabilities_identical":True,
            "coherent_swap_support_initial":initial,
            "coherent_swap_support_final":final,
            "hardware_scope":"Requires reference qutrit, system qutrit, and coherent environment memory; no hardware data."}

def verify():
    for theta in (Q(0),Q(1,4),Q(1,2),Q(1)):
        witness(theta)
    assert witness(Q(0))["mutual_information_bits"]==0
    assert abs(witness(Q(1))["mutual_information_bits"]-log2(3))<1e-12
    assert pvalue_null(1,1)==Q(1,3)
    assert pvalue_null(9,9)==Q(1,3)**9
    assert float(pvalue_null(24,16))<.001
    # The single-slot shift twirl is dephasing in the X eigenbasis:
    # sum_{h=0}^2 omega^{h(k-l)} = 3 delta_{kl}.
    assert [sum(1 for h in range(3) if (h*d)%3==0) for d in range(3)]==[3,1,1]
    return {
      "status":"PASS_QUTRIT_CAUSAL_BREAK_MARKOV_VS_PERSISTENT_MEMORY",
      "hypotheses":{"H0":"fresh uniformly random h each slot",
                    "H1":"same uniformly random classical h both slots"},
      "one_slot_channels_identical":True,
      "one_slot_entanglement_breaking":True,
      "control_independent_repreparation":"|0> at intermediate slot",
      "exact_quantum_vs_classical_boundary":"Measured memory witness is classical process-tensor non-Markovianity; it does NOT certify multi-time quantum entanglement or indefinite causal order.",
      "witnesses":[witness(x) for x in (Q(0),Q(1,2),Q(1))],
      "coherent_quantum_memory_Bell_return":quantum_memory_bell_return(),
      "hypothetical_24_shots_16_matches_p_null_exact":str(pvalue_null(24,16)),
      "hypothetical_24_shots_16_matches_p_null_float":float(pvalue_null(24,16)),
      "hypothetical_9_shots_all_matches_p_null_exact":str(pvalue_null(9,9)),
      "hardware_status":"NO REAL PHOTON DATA; exact probability/control calculations only."
    }
if __name__=="__main__":
    cert=verify();OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(cert,indent=2)+"\n",encoding="utf-8")
    print(cert["status"],cert["hypothetical_24_shots_16_matches_p_null_float"])
