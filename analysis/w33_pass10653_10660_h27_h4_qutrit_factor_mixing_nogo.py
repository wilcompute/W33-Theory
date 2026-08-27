#!/usr/bin/env python3
"""Pass10653-10660: compare the genuine H27 central-qutrit factor with the C3 factor of the H4 3-5-7 harmonic basis.

H27 adjacency commutes with its center C3.  In the central Fourier basis its
three 9x9 blocks have spectra
  chi0: 8^1,(-1)^8
  chi1: 2^6,(-4)^3
  chi2: 2^6,(-4)^3,
so every diagonal block has Frobenius norm squared 72 and every off-diagonal
C3 block vanishes.  Any polynomial f(H27) remains C3-block-diagonal.

Pass10645 computes the actual H4 harmonic operator T.  Its C3 block Frobenius
squared table is
  [[504,48,48],[48,57,72],[48,72,57]].
Thus qutrit-changing blocks carry total norm squared 336 out of total954,
namely 56/159 of the operator Frobenius power.

Therefore no factor-preserving unitary I_3 tensor U_9 can realize the H27/H4
spectral transport.  The required nonlocal transform necessarily entangles the
genuine qutrit C3 index with the arithmetic nine-state factor.
"""
from __future__ import annotations
from fractions import Fraction
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS10653_10660_H27_H4_QUTRIT_FACTOR_MIXING_NOGO.json'

def main():
    h_diag=[8**2+8*((-1)**2),6*(2**2)+3*((-4)**2),6*(2**2)+3*((-4)**2)]
    assert h_diag==[72,72,72]
    h_total=sum(h_diag);assert h_total==216
    B=[[504,48,48],[48,57,72],[48,72,57]]
    h4_total=sum(sum(r) for r in B);assert h4_total==954
    h4_off=sum(B[i][j] for i in range(3) for j in range(3) if i!=j);assert h4_off==336
    frac=Fraction(h4_off,h4_total);assert frac==Fraction(56,159)
    out={
      'schema':'w33.pass10653_10660.h27_h4_qutrit_factor_mixing_nogo.v1','status':'PASS','passes':'10653-10660',
      'H27_central_qutrit':{
        'block_dimensions':[9,9,9],'block_Frobenius_squared_diagonal':h_diag,'off_diagonal':0,'total_Frobenius_squared':h_total,
        'meaning':'H27 and every polynomial in H27 conserve the central C3 Fourier character exactly'},
      'H4_harmonic_C3':{
        'block_Frobenius_squared':B,'total_Frobenius_squared':h4_total,'off_diagonal_total':h4_off,'qutrit_changing_fraction':'56/159'},
      'factor_preserving_transporter':'IMPOSSIBLE: no U=I_3 tensor U_9 can conjugate the H27 radial transport to the H4 harmonic transport',
      'required_transport':'must mix/entangle the C3 qutrit index with the C5xC7 arithmetic nine-state sector',
      'theorem':'The canonical C3 factor is a conserved central quantum number for H27 but an interacting coordinate for the H4/(13:6) harmonic transport. Exactly 56/159 of the H4 operator Frobenius power changes the C3 harmonic sector. Hence the missing H27-to-H4 Fourier/Steinberg map is necessarily qutrit-arithmetic entangling, not a local transform on the nine-state multiplicity space.',
      'boundary':'Exact H27 block norms and exact rational summary of the Pass10645 verified H4 block norms. Frobenius mixing is an operator-coordinate statement, not a physical transition probability.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','mixing_fraction':'56/159','local_qutrit_transporter':False}))
if __name__=='__main__':main()
