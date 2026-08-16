#!/usr/bin/env python3
"""Pass5619: test, rather than assume, the q=3 two-sheet lift as a spinor carrier.

There are two distinct finite quantum structures in the repo:
  (i) the standard two-qutrit 9-dimensional Weil/metaplectic representation of
      Sp(4,3), and
  (ii) the 32-state +/- vector lift of the 16 Segre events from Pass5613.

The central symplectic element -I acts in (i) as qutrit parity, with spectrum
+1^5,-1^4.  It is therefore NOT scalar -1 and the ordinary two-qutrit Weil
module is not, merely by this central element, a spin-1/2-like double-valued
module.

In (ii), the deck involution D swapping +/- lifts commutes with the intrinsic
magnetic Hamiltonian.  Its D=-1 sector is exactly 16-dimensional, and H_mag
there has spectrum -6^4,-3^4,3^4,6^4.  This is a genuine signed deck module, but
no equivariant identification with either D5 half-spin 16 is asserted.  The
repo's Pass346 chirality no-go remains in force: the outer PGSp controller swaps
the two D5 half-spin chiralities.
"""
from __future__ import annotations
import json
from collections import Counter
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5619_SPINOR_DECK_MODULE.json'

def p1(): return [(1,t) for t in range(3)]+[(0,1)]
def norm(v,q=3):
    for a in v:
        if a%q:
            z=pow(a%q,-1,q); return tuple(z*x%q for x in v)
    raise ValueError

def segre(u,v): return norm((u[0]*v[0],u[1]*v[1],u[0]*v[1],-u[1]*v[0]))
def B(x,y): return (x[0]*y[1]-x[1]*y[0]+x[2]*y[3]-x[3]*y[2])%3

def lifted_hamiltonian():
    reps=[segre(u,v) for u in p1() for v in p1()]
    vecs=[]; base=[]
    for i,v in enumerate(reps):
        for a in (1,2):
            vecs.append(tuple(a*x%3 for x in v)); base.append(i)
    w=np.exp(2j*np.pi/3); H=np.zeros((32,32),complex)
    for i in range(32):
        ri,ci=divmod(base[i],4)
        for j in range(i+1,32):
            rj,cj=divmod(base[j],4)
            if ri!=rj and ci!=cj:
                z=w**((2*B(vecs[i],vecs[j]))%3)
                H[i,j]=z; H[j,i]=np.conj(z)
    return H

def main():
    # Standard 2-qutrit Weil generators used in bt2768_metaplectic_lift_sensor.py.
    w=np.exp(2j*np.pi/3)
    F=np.array([[w**(j*k) for k in range(3)] for j in range(3)],complex)/np.sqrt(3)
    P=np.diag([w**((2*j*j)%3) for j in range(3)]).astype(complex)
    I3=np.eye(3,complex)
    Fp=np.kron(F,I3); Ff=np.kron(I3,F)
    Sp=np.kron(P,I3); Sf=np.kron(I3,P)
    CX=np.zeros((9,9),complex)
    for p in range(3):
        for f in range(3): CX[3*p+((f+p)%3),3*p+f]=1
    central_minus_I=Fp@Fp@Ff@Ff
    ev=np.linalg.eigvalsh(central_minus_I)
    cnt=Counter(float(x) for x in np.round(ev,8))
    assert cnt==Counter({-1.0:4,1.0:5})
    assert abs(np.trace(central_minus_I)-1)<1e-10
    assert np.max(abs(central_minus_I@central_minus_I-np.eye(9)))<1e-10
    commute={}
    for name,U in {'Fp':Fp,'Ff':Ff,'Sp':Sp,'Sf':Sf,'CX':CX}.items():
        r=float(np.max(abs(central_minus_I@U-U@central_minus_I))); commute[name]=r; assert r<1e-10

    H=lifted_hamiltonian()
    D=np.zeros((32,32),float)
    for i in range(16): D[2*i,2*i+1]=D[2*i+1,2*i]=1
    deck_comm=float(np.max(abs(D@H-H@D))); assert deck_comm<1e-10
    cols=[]
    for sign in (1,-1):
        for i in range(16):
            v=np.zeros(32); v[2*i]=1/np.sqrt(2); v[2*i+1]=sign/np.sqrt(2); cols.append(v)
    Q=np.column_stack(cols); T=Q.T@H@Q
    off=float(np.max(abs(T[:16,16:]))); assert off<1e-10
    even=np.linalg.eigvalsh(T[:16,:16]); odd=np.linalg.eigvalsh(T[16:,16:])
    ce=Counter(float(x) for x in np.round(even,8)); co=Counter(float(x) for x in np.round(odd,8))
    assert co==Counter({-6.0:4,-3.0:4,3.0:4,6.0:4})
    assert ce==Counter({-6.0:2,-3.0:3,-1.0:3,2.0:6,3.0:1,9.0:1})

    out={
      'pass':5619,'status':'SIGNED_16_DECK_MODULE_WITH_NAIVE_SPINOR_IDENTIFICATION_FALSIFIED',
      'two_qutrit_Weil_minus_I':{'spectrum':{'+1':5,'-1':4},'trace':1,'is_scalar_minus_one':False,'max_generator_commutator':max(commute.values())},
      'vector_lift':{'dimension':32,'deck_even_dimension':16,'deck_odd_dimension':16,'deck_commutator_residual':deck_comm,'off_block_residual':off,
                     'deck_even_spectrum':dict(sorted((str(k),v) for k,v in ce.items())),
                     'deck_odd_spectrum':dict(sorted((str(k),v) for k,v in co.items()))},
      'theorem':'The q=3 vector lift has a canonical 16-dimensional signed deck sector on which the sheet swap acts as -1, while the standard 9-dimensional two-qutrit Weil representation sends central -I to parity (+1^5,-1^4), not scalar -1.',
      'chirality_firewall':'Dimension 16 and central sign are insufficient to identify the deck-odd module with a D5 half-spin. Pass346 proves the substrate outer PGSp controller exchanges S+ and S-, so no intrinsic substrate invariant can choose one physical chirality.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__': main()
