#!/usr/bin/env python3
"""Pass5616: couple the intrinsic q=3 magnetic lift to the repo's causal Dirac walk.

Pass4067 already supplied a local Clifford Dirac walk.  Pass5613 supplies a
canonical-on-vectors internal Hermitian magnetic operator H_mag.  Put

  H(p)=sum_j p_j alpha_j tensor I + beta tensor (m0 I + g H_mag).

Clifford anticommutation gives the exact identity

  H(p)^2 = |p|^2 I + I tensor (m0 I + g H_mag)^2,

and therefore internal band h has relativistic-form dispersion
  E_h,+/- = +/-sqrt(|p|^2 + (m0+g h)^2).

The coefficients m0,g remain free probe parameters; this pass does not fit masses.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5616_DIRAC_MAGNETIC_DISPERSION.json'

def pauli():
    I=np.eye(2,dtype=complex)
    X=np.array([[0,1],[1,0]],complex)
    Y=np.array([[0,-1j],[1j,0]],complex)
    Z=np.array([[1,0],[0,-1]],complex)
    return I,X,Y,Z

def main():
    I,X,Y,Z=pauli()
    beta=np.kron(Z,I)
    alphas=[np.kron(X,S) for S in (X,Y,Z)]
    I4=np.eye(4,dtype=complex)
    assert np.allclose(beta@beta,I4)
    for i,a in enumerate(alphas):
        assert np.allclose(a@a,I4)
        assert np.allclose(a@beta+beta@a,0)
        for j,b in enumerate(alphas):
            want=2*I4 if i==j else np.zeros((4,4),complex)
            assert np.allclose(a@b+b@a,want)

    bands=[(-6,6),(-3,7),(-1,3),(2,6),(3,5),(6,4),(9,1)]
    h=np.concatenate([np.full(m,x,float) for x,m in bands])
    Hmag=np.diag(h)
    m0=0.7;g=0.11;p=np.array([0.2,-0.3,0.4])
    M=m0*np.eye(32)+g*Hmag
    H=sum(p[j]*np.kron(alphas[j],np.eye(32)) for j in range(3))+np.kron(beta,M)
    lhs=H@H
    rhs=np.kron(I4,(float(p@p)*np.eye(32)+M@M))
    residual=float(np.max(np.abs(lhs-rhs)))
    assert residual<1e-12
    ev=np.linalg.eigvalsh(H)
    pred=[]
    p2=float(p@p)
    for x,m in bands:
        E=(p2+(m0+g*x)**2)**0.5
        pred.extend([-E]*(2*m));pred.extend([E]*(2*m))
    assert np.max(np.abs(np.sort(ev)-np.sort(np.array(pred))))<1e-10

    out={'pass':5616,'status':'EXACT_DIRAC_DISPERSION_WITH_INTRINSIC_MAGNETIC_INTERNAL_OPERATOR',
         'identity':'H(p)^2=|p|^2 I + (m0 I + g Hmag)^2',
         'dispersion':'E_h,+/- = +/-sqrt(|p|^2+(m0+g h)^2)',
         'q3_internal_bands':[{"h":x,"multiplicity":m} for x,m in bands],
         'numerical_probe':{'p':p.tolist(),'m0':m0,'g':g,'max_H2_residual':residual},
         'walk':'U_a=exp(-ia beta tensor M) prod_j exp(-ia p_j alpha_j tensor I), reusing the Pass4067 local operator-splitting construction',
         'physics_firewall':'The relativistic form is exact algebraically in lattice units, but c, m0, g, the assignment of magnetic bands to particles, and curved/gauge dynamics are not derived.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
