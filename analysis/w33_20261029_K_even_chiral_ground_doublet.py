#!/usr/bin/env python3
"""Time-reversal-even frustrated H27 Hamiltonian with two conjugate chiral
lowest-energy sectors. A ground manifold is not a dynamical choice of sign.
"""
import json
import numpy as np
G=[(a,b,c) for a in range(3) for b in range(3) for c in range(3)]
IX={g:i for i,g in enumerate(G)}
def mult(u,v):
 a,b,c=u;x,y,z=v
 return ((a+x)%3,(b+y)%3,(c+z+a*y)%3)
def left(g):
 U=np.zeros((27,27),complex)
 for j,h in enumerate(G):U[IX[mult(g,h)],j]=1
 return U
def verify(g=.25):
 X,Y,Z=[left(a) for a in ((1,0,0),(0,1,0),(0,0,1))]
 I=np.eye(27)
 assert np.max(np.abs(X@Y-Z@Y@X))<1e-12
 assert np.max(np.abs(Z@X-X@Z))<1e-12
 H0=X+X.conj().T+Y+Y.conj().T
 O=1j*(Z-Z.conj().T)
 O2=O@O
 assert np.max(np.abs(O-O.conj().T))<1e-12
 assert np.max(np.abs(H0@O-O@H0))<1e-12
 assert np.max(np.abs(O2-(2*I-Z-Z.conj().T)))<1e-12
 H=H0-g*O2
 assert np.max(np.abs(H-H.conj()))<1e-12
 assert np.max(np.abs(O+O.conj()))<1e-12
 ew,V=np.linalg.eigh(H)
 assert np.max(np.abs(ew[:6]-(-2-3*g)))<1e-12
 assert abs(ew[6]+2)<1e-12
 ch=np.linalg.eigvalsh(V[:,:6].conj().T@O@V[:,:6])
 assert np.max(np.abs(ch-np.array([-np.sqrt(3)]*3+[np.sqrt(3)]*3)))<1e-11
 return dict(status="PASS",n=27,free_positive_coupling=g,
    Hamiltonian="X+X^-1+Y+Y^-1-g*(i(Z-Z^-1))^2",
    equivalent="H0+g(Z+Z^-1)-2gI",
    real_K_even_H=True,imaginary_K_odd_chirality_operator=True,
    ground_energy=-2-3*g,ground_dimension=6,
    chiral_ground_expectations=[float(x) for x in ch],
    spectral_gap_above_ground=float(ew[6]-ew[0]),
    limit="Two exact K-exchanged chiral sectors, three states each; no intrinsic sign selection, no physical energy calibration, no infinite-volume SSB.")
if __name__=="__main__":print(json.dumps(verify(),indent=2))
