#!/usr/bin/env python3
from __future__ import annotations
import cmath, itertools, json, math
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_20260924_temporal_maslov_mu12.json"
TOL=3e-10
omega=np.exp(2j*np.pi/3)
I3=np.eye(3,dtype=complex)

def phase_align(A,B):
    z=np.vdot(B.reshape(-1),A.reshape(-1))
    if abs(z)==0: return float("inf"),0j
    q=z/abs(z)
    return float(np.linalg.norm(A-q*B)),q

def root12_index(z):
    vals=[np.exp(2j*np.pi*k/12) for k in range(12)]
    ds=[abs(z-v) for v in vals]
    k=int(np.argmin(ds))
    assert ds[k]<TOL
    return k


def root12_exponent(z):
    return root12_index(z)


def rank2_mod3(S):
    S=np.asarray(S,dtype=int)%3
    if not np.any(S):
        return 0
    det=(int(S[0,0])*int(S[1,1])-int(S[0,1])*int(S[1,0]))%3
    return 2 if det else 1


def weil_phase(coords):
    a,b,c=map(int,coords)
    S=np.array([[a,b],[b,c]],dtype=int)%3
    rank=rank2_mod3(S)
    det=(a*c-b*b)%3
    total=0j
    for x,y in itertools.product(range(3),repeat=2):
        v=np.array([x,y],dtype=int)
        q=(2*int(v@S@v))%3
        total+=omega**q
    radical_factor=3**(2-rank)
    phase=total/(radical_factor*(3**(rank/2)))
    k=root12_index(phase)
    phase=np.exp(2j*np.pi*k/12)
    return phase,rank,det


def main():
    F=np.array([[omega**(j*k) for k in range(3)] for j in range(3)],
               dtype=complex)/math.sqrt(3)
    # G=diag(omega^(x^2)); it is one coordinate restriction of the
    # Bell-shell quadratic program with S_11=2 under the repo's 1/2 convention.
    G=np.diag([omega**((x*x)%3) for x in range(3)])
    X=np.zeros((3,3),dtype=complex)
    for x in range(3): X[(x+1)%3,x]=1
    Z=np.diag([omega**x for x in range(3)])

    assert np.linalg.norm(F.conj().T@F-I3)<TOL
    assert np.linalg.norm(G.conj().T@G-I3)<TOL
    assert np.linalg.norm(np.linalg.matrix_power(F,4)-I3)<TOL

    gauss=sum(omega**((x*x)%3) for x in range(3))/math.sqrt(3)
    assert abs(gauss-1j)<TOL

    # Explicit metaplectic/Maslov projective relation.
    lhs=np.linalg.matrix_power(F@G,3)
    rhs=1j*np.linalg.matrix_power(F,2)
    assert np.linalg.norm(lhs-rhs)<TOL
    # Weyl commutator phase and Maslov phase generate exactly mu_12.
    comm=Z@X@Z.conj().T@X.conj().T
    err,q=phase_align(comm,I3)
    assert err<TOL and (abs(q-omega)<TOL or abs(q-omega**2)<TOL)
    weyl=q

    phases={}
    for a in range(4):
        for b in range(3):
            z=(1j**a)*(weyl**b)
            phases[root12_index(z)]=z
    assert len(phases)==12 and set(phases)==set(range(12))

    # Antiunitary complex conjugation reverses both coherent orientations.
    assert abs(np.conj(gauss)-(-1j))<TOL
    assert abs(np.conj(weyl)-1/weyl)<TOL
    assert np.linalg.norm(np.conj(F)-F.conj())<TOL
    assert np.linalg.norm(np.conj(G)-G.conj())<TOL

    # Projective relation remains the same after reversal with inverse phase.
    rev_lhs=np.linalg.matrix_power(np.conj(F@G),3)
    rev_rhs=(-1j)*np.linalg.matrix_power(np.conj(F),2)
    assert np.linalg.norm(rev_lhs-rev_rhs)<TOL

    atlas=[]
    phase_hist={}
    class_hist={}
    for coords in itertools.product(range(3),repeat=3):
        ph,rank,det=weil_phase(coords)
        exp=root12_exponent(ph)
        phase_hist[str(exp)]=phase_hist.get(str(exp),0)+1
        key=f"rank{rank}_det{det}"
        class_hist[key]=class_hist.get(key,0)+1
        atlas.append({
          "coords":list(coords),"rank":rank,"determinant":det,
          "weil_phase_root12_exponent":exp,
        })
    assert phase_hist=={"0":13,"3":4,"6":6,"9":4}

    out={
      "schema":"w33.20260924.temporal_maslov_mu12.v2",
      "status":"PASS_HISTORY_QUADRATICS_GENERATE_THE_CLIFFORD_MU12_FIELD",
      "quadratic_gauss":{
        "sum":"(1/sqrt(3))*sum_x omega^(x^2)",
        "value":"i",
        "numeric":[float(gauss.real),float(gauss.imag)],
      },
      "operator_relation":{
        "F":"qutrit Fourier",
        "G":"diag(1,omega,omega), a Bell-shell quadratic chirp",
        "exact_projective_relation":"(F G)^3 = i F^2",
        "F_squared":"parity x -> -x",
        "interpretation":"the order-four phase is produced by composition of finite quadratic kernels",
      },
      "quadratic_history_atlas":{
        "size":27,
        "phase_exponent_histogram_mu12":phase_hist,
        "rank_determinant_histogram":class_hist,
        "rows":atlas,
        "reading":"rank-one histories carry the +/-i orientation pair; rank-two histories carry +/-1",
      },
      "phase_group":{
        "weyl_commutator_phase_root12_index":root12_index(weyl),
        "maslov_phase_root12_index":root12_index(1j),
        "generated_root12_indices":sorted(phases),
        "generated_group":"mu_12",
        "mechanism":"<omega,i> with orders 3 and 4",
      },
      "temporal_reversal":{
        "operation":"antiunitary complex conjugation",
        "omega_maps_to":"omega^-1",
        "i_maps_to":"-i",
        "reversed_relation":"(conj(FG))^3 = -i conj(F)^2",
        "reading":"coherent orientation is reversed without entropy production",
      },
      "repo_relation":{
        "prior_mu12":"repo already certified the qutrit Clifford scalar phase group mu_12 and an E8 Z12 character bridge",
        "new_content":"this packet supplies an explicit quadratic-Gauss/Maslov operator mechanism for the order-four factor inside the Bell-shell/Clifford lane",
        "history_program_parent":"analysis/w33_20260924_bell_shell_quadratic_clifford_programs.py",
      },
      "literature_boundary":(
        "Finite Weil/metaplectic representations acquire projective cocycles governed "
        "by quadratic Gauss/Maslov data. The executable claim here is the displayed "
        "qutrit matrix identity, not a continuum geometric-quantization theorem."
      ),
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({
      "status":out["status"],
      "gauss":out["quadratic_gauss"]["value"],
      "relation":out["operator_relation"]["exact_projective_relation"],
      "mu12":out["phase_group"]["generated_root12_indices"],
    },indent=2))

if __name__=="__main__":
    main()
