#!/usr/bin/env python3
"""Exact representation-level S3 bridge: heterotic defining doublet = W33 logical doublet.

Konopka Eq.(6.3) gives
  tau=[[1,-1],[0,-1]],
  sigma=[[0,-1],[1,-1]].

Let omega=exp(2pi i/3).  Choose the complex eigenbasis
  v_+ = (-omega^2, 1)^T,
  v_- = ( omega,   -1)^T.
With P=[v_+ v_-],
  P^-1 sigma P = diag(omega,omega^2),
  P^-1 tau   P = [[0,1],[1,0]].

These are exactly the W33 doubled central-character matrices
  z=diag(omega,omega^-1), X_L=swap.

Thus the two spaces are isomorphic as abstract complex S3-modules.  Moreover,
the Z3 centralizer character lines r_+,r_- in Konopka's Table 2 map directly
to the W33 r=1,r=2 center-character rails.

Boundary: this is a representation equivalence, not an identification of
microscopic operators.  The heterotic sigma is a geometric point-group action;
W33 z is a Heisenberg-center phase.  A physical bridge needs a heterotic
massless-state subspace carrying this defining irrep and a map of observables.
"""
from __future__ import annotations
import cmath,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_heterotic_s3_defining_irrep_intertwiner.json'

def mm(A,B):
    return [[sum(A[i][k]*B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
def inv2(A):
    d=A[0][0]*A[1][1]-A[0][1]*A[1][0]
    return [[A[1][1]/d,-A[0][1]/d],[-A[1][0]/d,A[0][0]/d]]
def close(A,B,tol=1e-9):
    return all(abs(A[i][j]-B[i][j])<tol for i in range(len(A)) for j in range(len(A[0])))

def main(write=True):
    w=cmath.exp(2j*cmath.pi/3)
    tau=[[1,-1],[0,-1]]
    sigma=[[0,-1],[1,-1]]
    P=[[-w*w,w],[1,-1]]
    Pinv=inv2(P)
    sig=mm(mm(Pinv,sigma),P)
    ta=mm(mm(Pinv,tau),P)
    z=[[w,0],[0,w*w]]
    X=[[0,1],[1,0]]
    assert close(sig,z) and close(ta,X)
    # characters on conjugacy classes e,tau,sigma are 2,0,-1
    chi={'e':2,'tau':ta[0][0]+ta[1][1],'sigma':sig[0][0]+sig[1][1]}
    assert abs(chi['tau'])<1e-9 and abs(chi['sigma']+1)<1e-9
    # centralizer projectors in diagonal basis
    Pplus=[[1,0],[0,0]];Pminus=[[0,0],[0,1]]
    out={'schema':'w33.heterotic_s3_defining_irrep_intertwiner.v1',
      'status':'PASS_EXACT_S3_MODULE_ISOMORPHISM',
      'source':'Konopka JHEP 07 (2013) 023 Eq.(6.3), Table 1-2',
      'heterotic_matrices':{'tau':tau,'sigma':sigma},
      'intertwiner_basis':{
        'v_plus':'(-omega^2,1)^T',
        'v_minus':'(omega,-1)^T',
        'P_columns':'[v_plus,v_minus]'},
      'normal_form':{
        'P^-1 sigma P':'diag(omega,omega^-1)',
        'P^-1 tau P':'[[0,1],[1,0]]'},
      'W33_identification':{
        'sigma':'logical center z',
        'tau':'outer logical swap X_L',
        'Z3_character_plus':'r=1 rail',
        'Z3_character_minus':'r=2 rail'},
      'character_match':{'e':2,'transposition':0,'three_cycle':-1},
      'projector_match':{
        'heterotic_Z3_rplus_to_W33_P1':'diag(1,0)',
        'heterotic_Z3_rminus_to_W33_P2':'diag(0,1)'},
      'conclusion':'The heterotic S3 defining representation and the W33 central-character logical doublet are isomorphic as complex S3-modules.',
      'physical_boundary':'No microscopic identification of heterotic geometric sigma with the Heisenberg center z is claimed. Need an actual heterotic state subspace/observable intertwiner.',
      'checks':{'sigma_diagonalized':True,'tau_becomes_swap':True,'character_table_matches':True}}
    if write:OUT.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2));return out
if __name__=='__main__':main(True)
