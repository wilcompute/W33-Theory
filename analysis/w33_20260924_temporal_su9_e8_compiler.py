#!/usr/bin/env python3
from __future__ import annotations
import itertools, json, math, sys
from collections import Counter
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0,str(ROOT))
OUT=ROOT/"data/w33_20260924_temporal_su9_e8_compiler.json"

omega=np.exp(2j*np.pi/3)
TOL=2e-9

def qutrit_pauli(a,b):
    Z=np.diag([omega**j for j in range(3)])
    X=np.zeros((3,3),dtype=complex)
    for j in range(3):
        X[(j+1)%3,j]=1
    return np.linalg.matrix_power(Z,a)@np.linalg.matrix_power(X,b)

def liouville_weyl(x):
    a,b,c,d=x
    return np.kron(qutrit_pauli(a,b),np.conj(qutrit_pauli(c,d)))

def symp(x,y):
    a,b,c,d=x
    A,B,C,D=y
    return (a*B-b*A-c*D+d*C)%3

def canon_ray(v):
    v=tuple(int(x)%3 for x in v)
    for x in v:
        if x:
            s=1 if x==1 else 2
            return tuple((s*y)%3 for y in v)
    raise ValueError("zero")
def srg_check(A):
    deg=set(map(int,A.sum(axis=1)))
    lam=set()
    mu=set()
    for i,j in itertools.combinations(range(len(A)),2):
        cn=int(A[i]@A[j])
        (lam if A[i,j] else mu).add(cn)
    return deg,lam,mu

def main():
    labels=list(itertools.product(range(3),repeat=4))
    mats=[liouville_weyl(x) for x in labels]
    I=np.eye(9,dtype=complex)

    # Exact orthogonal operator basis numerically represented in C.
    G=np.array([[np.vdot(A,B) for B in mats] for A in mats])
    assert np.linalg.norm(G-9*np.eye(81))<1e-7
    assert np.linalg.matrix_rank(np.vstack([M.reshape(-1) for M in mats]),tol=1e-8)==81

    zero=(0,0,0,0)
    non=[x for x in labels if x!=zero]
    nonm=[liouville_weyl(x) for x in non]
    assert all(abs(np.trace(M))<TOL for M in nonm)
    assert np.linalg.matrix_rank(np.vstack([M.reshape(-1) for M in nonm]),tol=1e-8)==80

    # Verify the two-sided Weyl commutator form on all label pairs.
    for x,A in zip(labels,mats):
        for y,B in zip(labels,mats):
            phase=omega**symp(x,y)
            assert np.linalg.norm(A@B-phase*(B@A))<2e-8
    rays=sorted({canon_ray(x) for x in non})
    assert len(rays)==40
    rid={x:i for i,x in enumerate(rays)}
    A40=np.zeros((40,40),dtype=int)
    for i,x in enumerate(rays):
        for j,y in enumerate(rays[i+1:],start=i+1):
            if symp(x,y)==0:
                A40[i,j]=A40[j,i]=1
    deg,lam,mu=srg_check(A40)
    assert (deg,lam,mu)==({12},{2},{4})
    eig=Counter(int(round(x)) for x in np.linalg.eigvalsh(A40.astype(float)))
    assert eig==Counter({2:24,-4:15,12:1})

    # Independent standard traceless matrix basis has the same 80D space.
    std=[]
    for i in range(9):
        for j in range(9):
            if i!=j:
                E=np.zeros((9,9),dtype=complex)
                E[i,j]=1
                std.append(E)
    for i in range(8):
        H=np.zeros((9,9),dtype=complex)
        H[i,i]=1
        H[i+1,i+1]=-1
        std.append(H)
    assert len(std)==80
    assert np.linalg.matrix_rank(np.vstack([M.reshape(-1) for M in std]),tol=1e-8)==80
    joined=np.vstack([M.reshape(-1) for M in nonm+std])
    assert np.linalg.matrix_rank(joined,tol=1e-8)==80
    hesse=json.loads(
        (ROOT/"data/w33_20260924_temporal_hesse_4a2_a8_bridge.json").read_text()
    )
    process=json.loads(
        (ROOT/"data/w33_20260924_temporal_a8_e8_process_bracket.json").read_text()
    )
    assert hesse["status"]=="PASS_HESSE_12_IS_4A2_INSIDE_TEMPORAL_A8_E8"
    assert process["status"]=="PASS_NINE_HISTORY_CELLS_COMPILE_THE_A8_E8_ROOT_SUPPORT_BRACKETS"

    out={
      "schema":"w33.20260924.temporal_su9_e8_compiler.v1",
      "status":"PASS_NINE_QUTRIT_HISTORY_AMPLITUDES_COMPILE_W33_SL9_AND_E8_SUPPORT",
      "history_space":{
        "basis":"nine vectorized qutrit matrix units |i><j|",
        "dimension":9,
        "operator_algebra_dimension":81,
      },
      "two_sided_Weyl":{
        "operators":81,
        "identity":1,
        "nonidentity_traceless":80,
        "Hilbert_Schmidt_orthogonal":True,
        "nonidentity_span_rank":80,
        "same_space_as_standard_sl9_basis":True,
        "commutator_form":"aB-bA-cD+dC mod 3",
      },
      "W33_projectivization":{
        "nonzero_phase_space_labels":80,
        "projective_inverse_pairs":40,
        "adjacency":"two rays commute iff symplectic pairing is zero",
        "srg_parameters":[40,12,2,4],
        "spectrum":{"12":1,"2":24,"-4":15},
      },
      "E8_A8_completion":{
        "sl9_dimension":80,
        "Lambda3_dimension":84,
        "Lambda6_dimension":84,
        "identity":"248=80+84+84",
        "root_support_identity":"240=72+84+84 plus 8 Cartan",
        "Hesse_refinement":"84=12 Hesse lines +72 noncollinear triples; the 12+12 Hesse roots are 4A2",
        "process_bracket_certificate":"data/w33_20260924_temporal_a8_e8_process_bracket.json",
      },
      "theorem":(
        "Vectorizing one qutrit operator history gives a nine-dimensional "
        "history-amplitude space. Its 81 two-sided qutrit Weyl transformations "
        "are an orthogonal basis of End(C^9); the 80 nonidentity transformations "
        "are traceless, linearly independent, and span exactly sl9. Their F3^4 "
        "labels carry the two-sided Weyl symplectic commutator form, and pairing "
        "nonzero labels by sign gives the 40-ray W(3,3) commutation graph. Adding "
        "the 84 three-history and 84 dual six-history exterior sectors gives the "
        "standard 80+84+84 A8 decomposition of E8, with the temporal packet "
        "bracket supports certified separately. Thus the PDF's nine-history "
        "A8-to-E8 route is an explicit finite linear/root-support compiler."
      ),
      "boundary":(
        "The sl9 Weyl basis and the A8 root/Cartan basis are two bases of the "
        "same 80-dimensional algebra, not term-by-term identical vectors. The "
        "signed E8 structure constants remain owned by the frozen Chevalley "
        "artifact. No continuum gauge dynamics or Standard Model identification "
        "is inferred from this finite compiler."
      ),
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({
      "status":out["status"],
      "Weyl":out["two_sided_Weyl"],
      "W33":out["W33_projectivization"],
      "E8":out["E8_A8_completion"],
    },indent=2,sort_keys=True))

if __name__=="__main__":
    main()
