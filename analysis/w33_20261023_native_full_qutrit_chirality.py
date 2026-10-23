#!/usr/bin/env python3
"""Full onsite two-qutrit Pauli chirality: explicit real mixing matrix and K symmetry.

No assumed abstract 2-state sector: use actual nine-dimensional H0, O, Rx.
Two-site spectrum from direct 81-dimensional Hermitian diagonalization.
"""
import json,sys
from pathlib import Path
import numpy as np

def run():
    zeta=np.exp(2j*np.pi/3)
    X=np.roll(np.eye(3,dtype=complex),1,axis=0)
    Z=np.diag([1,zeta,zeta**2])
    eye3=np.eye(3,dtype=complex); eye9=np.eye(9,dtype=complex)
    RX=(X+X.conj().T)/2
    RZ=(Z+Z.conj().T)/2
    J=np.kron((RX@RZ-RZ@RX)/(2j),eye3)
    mixing=np.kron(RX,eye3)
    Pi=np.zeros((9,9),complex)
    for a in range(3):
        for b in range(3):
            Pi[3*((-a)%3)+(-b)%3,3*a+b]=1
    H0=(eye9-9*Pi)/2
    assert np.allclose(H0,H0.conj())
    assert np.allclose(J.conj(),-J)
    assert np.allclose(mixing,mixing.conj())
    assert np.allclose(Pi@J@Pi,J)
    assert np.allclose(Pi@mixing@Pi,mixing)
    assert np.allclose(H0@J,J@H0)
    assert np.allclose(H0@mixing,mixing@H0)
    assert np.max(np.abs(J@mixing-mixing@J))>1e-3
    a=3*np.sqrt(2)/8
    Pplus=(J@J+a*J)/(2*a*a)
    Pminus=(J@J-a*J)/(2*a*a)
    norm=float(np.linalg.norm(Pplus@mixing@Pminus))
    assert norm>1e-5
    # A first-qutrit mixing leaves residual spectator degeneracy.
    # Add real parity-even second-qutrit operators to mix that sector.
    mixing_full=mixing+np.kron(eye3,RX)/3+np.kron(eye3,RZ)/5
    assert np.allclose(Pi@mixing_full@Pi,mixing_full)
    assert np.allclose(mixing_full,mixing_full.conj())
    rows=[]
    for name,M in (("first_only",mixing),("both_qutrits",mixing_full)):
     for h in (0.,.05,.1,.2):
        H=np.kron(H0,eye9)+np.kron(eye9,H0)-np.kron(J,J)
        H-=h*(np.kron(M,eye9)+np.kron(eye9,M))
        assert np.allclose(H,H.conj()) and np.allclose(H,H.conj().T)
        levels=np.linalg.eigvalsh(H)
        gap=float(levels[1]-levels[0])
        ground=int(np.count_nonzero(np.isclose(levels,levels[0],atol=1e-9)))
        rows.append({"mixing":name,"h":h,"E0":float(levels[0]),"gap":gap,
                     "ground_degeneracy":ground})
    return {"status":"FULL_NINE_DIMENSIONAL_TWO_QUTRIT_NATIVE_MIXING",
      "onsite_operator":"O=[Re(X_1),Re(Z_1)]/(2i), mixing=Re(X_1)",
      "H2":"H0 tensor I + I tensor H0 - O tensor O -h(mixing tensor I + I tensor mixing)",
      "K_symmetry":"H2 is entrywise real, hence invariant under computational-basis conjugation",
      "mixing_commutes_with_parity":True,
      "mixing_noncommutes_with_O":True,
      "positive_negative_chirality_overlap_norm":norm,
      "spectrum":rows,
      "physical_boundary":"Explicit full 9D on-site operator and 81D two-site spectrum, NOT a verified physical time reversal or thermodynamic spontaneous selection; residual spectator symmetries possible."}

if __name__=="__main__":
 d=json.dumps(run(),indent=2)+"\n"
 if len(sys.argv)>1:Path(sys.argv[1]).write_text(d,encoding="utf8")
 else:print(d)
