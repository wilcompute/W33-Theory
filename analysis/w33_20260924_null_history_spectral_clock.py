#!/usr/bin/env python3
from __future__ import annotations
import itertools, json, math
from collections import Counter
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_20260924_null_history_spectral_clock.json"
P=3
W=np.exp(2j*np.pi/3)
TOL=3e-10

V=list(itertools.product(range(3),repeat=3))
VID={v:i for i,v in enumerate(V)}

def q(v): return (v[0]*v[2]-v[1]*v[1])%3

NULL=[v for v in V if v!=(0,0,0) and q(v)==0]

def adjacency():
    A=np.zeros((27,27),dtype=int)
    for s in V:
        for n in NULL:
            t=tuple((s[i]+n[i])%3 for i in range(3))
            A[VID[s],VID[t]]=1
    return A
def fourier_vector(k):
    return np.array([
        W**(sum(k[i]*s[i] for i in range(3))%3)/math.sqrt(27)
        for s in V
    ],dtype=complex)

def fourier_eigenvalue(k):
    z=sum(W**(sum(k[i]*n[i] for i in range(3))%3) for n in NULL)
    assert abs(z.imag)<TOL
    return int(round(z.real))

def projective_gl2():
    mats={}
    for z in itertools.product(range(3),repeat=4):
        G=np.array(z,dtype=int).reshape(2,2)
        if int(round(np.linalg.det(G)))%3==0: continue
        a=tuple(int(x) for x in G.reshape(-1))
        b=tuple(int(x) for x in ((-G)%3).reshape(-1))
        key=min(a,b)
        mats[key]=np.array(key,dtype=int).reshape(2,2)
    assert len(mats)==24
    return list(mats.values())
def sym2_rep(G):
    B=[
      np.array([[1,0],[0,0]],dtype=int),
      np.array([[0,1],[1,0]],dtype=int),
      np.array([[0,0],[0,1]],dtype=int),
    ]
    cols=[]
    for S in B:
        R=(G@S@G.T)%3
        cols.append([int(R[0,0]),int(R[0,1]),int(R[1,1])])
    return np.array(cols,dtype=int).T%3

def inv3(A):
    out=None
    for z in itertools.product(range(3),repeat=9):
        B=np.array(z,dtype=int).reshape(3,3)
        if np.array_equal((A@B)%3,np.eye(3,dtype=int)%3):
            out=B; break
    assert out is not None
    return out

def dual_action(M,k):
    return tuple(int(x) for x in (inv3(M).T@np.array(k,dtype=int))%3)
def sl2():
    out=[]
    for z in itertools.product(range(3),repeat=4):
        G=np.array(z,dtype=int).reshape(2,2)
        if int(round(np.linalg.det(G)))%3==1:
            out.append(G%3)
    assert len(out)==24
    return out

def main():
    A=adjacency()
    assert set(map(int,A.sum(axis=1)))=={8}
    L=8*np.eye(27)-A

    rows=[]
    for k in V:
        fv=fourier_vector(k)
        lamA=fourier_eigenvalue(k)
        err=float(np.linalg.norm(A@fv-lamA*fv))
        assert err<TOL
        rows.append({"k":list(k),"q":q(k),"A_eigenvalue":lamA,
                     "L_eigenvalue":8-lamA,"fourier_error":err})
    ac=Counter(r["A_eigenvalue"] for r in rows)
    lc=Counter(r["L_eigenvalue"] for r in rows)
    assert ac==Counter({2:12,-1:8,-4:6,8:1})
    assert lc==Counter({6:12,9:8,12:6,0:1})
    # The order-three clock at t*=2*pi/9.
    tstar=2*math.pi/9
    phases={lam:complex(np.exp(-1j*tstar*lam)) for lam in lc}
    assert abs(phases[0]-1)<TOL and abs(phases[9]-1)<TOL
    assert abs(phases[6]-W)<TOL and abs(phases[12]-W**2)<TOL

    evals,evecs=np.linalg.eigh(L)
    U=evecs@np.diag(np.exp(-1j*tstar*evals))@evecs.conj().T
    assert np.linalg.norm(np.linalg.matrix_power(U,3)-np.eye(27))<1e-8

    fixed=[tuple(r["k"]) for r in rows if r["L_eigenvalue"] in (0,9)]
    assert len(fixed)==9
    assert (0,0,0) in fixed
    fixed_nonzero=[k for k in fixed if k!=(0,0,0)]
    assert set(fixed_nonzero)==set(NULL)

    # Bell S4 acts on dual null shell as two tetrahedra.
    reps={tuple(sym2_rep(G).reshape(-1)):sym2_rep(G) for G in projective_gl2()}
    nullset=set(NULL); orbits=[]
    while nullset:
        x=min(nullset)
        O={dual_action(M,x) for M in reps.values()}
        orbits.append(sorted(O)); nullset-=O
    assert sorted(map(len,orbits))==[4,4]
    # Single-qutrit projective Pauli labels are F3^2, and SL2(3) is transitive
    # on the eight nonzero labels. Hence no quotient-equivariant identification
    # with the S4 4+4 null shell exists.
    p2=[v for v in itertools.product(range(3),repeat=2) if v!=(0,0)]
    x=p2[0]
    pauli_orbit={
        tuple(int(y) for y in (G@np.array(x,dtype=int))%3)
        for G in sl2()
    }
    assert len(pauli_orbit)==8

    out={
      "schema":"w33.20260924.null_history_spectral_clock.v1",
      "status":"PASS_ORDER3_NULL_HISTORY_CLOCK_WITH_QUTRIT_MODULE_NOGO",
      "graph":{"vertices":27,"degree":8,"edges":108,
               "adjacency_spectrum":dict(ac),"laplacian_spectrum":dict(lc)},
      "fourier_duality":{
        "translation_group":"F3^3",
        "null_connection_set_size":len(NULL),
        "eigenvalue_by_dual_quadratic_type":{
          "zero":8,"det0_nonzero":-1,"det1":-4,"det2":2
        },
      },
      "clock":{
        "t_star":"2*pi/9",
        "phase_by_laplacian_eigenvalue":{
          "0":"1","6":"omega","9":"1","12":"omega^2"
        },
        "U_cubed_identity":True,
        "fixed_dimension":len(fixed),
        "fixed_fourier_support":"{0} union nonzero null cone",
        "fixed_support_count":"1+8=9",
      },
      "qutrit_operator_intertwiner_test":{
        "dimension_match":True,
        "Bell_S4_orbits_on_eight_nonzero_fixed_modes":sorted(map(len,orbits)),
        "SL23_orbit_on_eight_nonidentity_projective_Paulis":len(pauli_orbit),
        "equivariant_identification_under_these_actions":False,
        "conclusion":(
          "The nine-dimensional clock-fixed space has the same 1+8 count as "
          "M3(C), but its natural Bell-line S4 symmetry splits the eight null "
          "modes as 4+4, unlike the transitive SL(2,3) action on nonzero qutrit "
          "Pauli labels. A canonical qutrit-operator identification is therefore "
          "not supplied by these symmetry actions."
        ),
      },
      "boundary":(
        "Exact finite Fourier/symmetry theorem. The 9-dimensional fixed sector "
        "is dynamical and canonical for the null-history Laplacian, but it is not "
        "promoted to the physical qutrit operator module without a different "
        "common subgroup/intertwiner."
      ),
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({
      "status":out["status"],
      "spectra":[dict(ac),dict(lc)],
      "fixed":out["clock"]["fixed_support_count"],
      "S4_orbits":out["qutrit_operator_intertwiner_test"]["Bell_S4_orbits_on_eight_nonzero_fixed_modes"],
      "Pauli_orbit":len(pauli_orbit),
    },indent=2,sort_keys=True))

if __name__=="__main__":
    main()
