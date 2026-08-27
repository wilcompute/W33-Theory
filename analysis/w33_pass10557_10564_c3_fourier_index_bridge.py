#!/usr/bin/env python3
"""Pass10557-10564: exact C3 Fourier/index bridge to the old Schlaefli-Steinberg lane.

Pass1147 proves that the three A2 color fibres form an intrinsic C3 torsor and
uses the integral color-Fourier basis

  [[1,1,0],[1,-1,1],[1,0,-1]]

with Smith diagonal (1,1,3).  Repeating it over the rank-81 within-color sector
gives index 3^81.

Pass10549-10556 proves that the new 27-state C105/C6 carrier factors as nine
C3 packets.  Therefore the identical integral qutrit Fourier basis, applied
packetwise, has block-diagonal Smith form with nine copies of (1,1,3), hence
index 3^9.  Over C both are simply multiplicity-space tensor C[C3].

This is an exact functor-level bridge, not an identification of the 9-dimensional
and 81-dimensional multiplicity spaces.
"""
from __future__ import annotations
import json
from pathlib import Path
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS10557_10564_C3_FOURIER_INDEX_BRIDGE.json'

def main():
    old=json.loads((ROOT/'data/w33_pass1147_schlaefli_steinberg_fourier_bridge.json').read_text())
    new=json.loads((ROOT/'data/PART_W33_PASS10549_10556_C105_INVARIANT_FOURIER.json').read_text())
    T=sp.Matrix([[1,1,0],[1,-1,1],[1,0,-1]])
    assert abs(int(T.det()))==3
    from sympy.matrices.normalforms import smith_normal_form
    from sympy.polys.domains import ZZ
    S=smith_normal_form(T,domain=ZZ)
    diag=[abs(int(S[i,i])) for i in range(3)]
    assert diag==[1,1,3]
    assert old['a2_color_torsor']['colors']==3
    assert old['a2_color_torsor']['complex_sector_ranks']==[81,81,81]
    assert old['integral_edge_lattice']['integral_color_fourier_split']['smith_diagonal']==[1,1,3]
    assert old['integral_edge_lattice']['integral_color_fourier_split']['rank81_index_factorization']=={'3':81}
    assert new['orbit_space']['packet_factorization']=='3 x 9'
    index9=3**9; index81=3**81
    assert index9==19683
    out={
      'schema':'w33.pass10557_10564.c3_fourier_index_bridge.v1','status':'PASS','passes':'10557-10564',
      'common_C3_transform':{'integral_basis':[[1,1,0],[1,-1,1],[1,0,-1]],'smith_diagonal':[1,1,3],'determinant_absolute':3,'complex_reading':'trivial plus the two nontrivial C3 Fourier characters'},
      'new_27_carrier':{'decomposition':'C^9 tensor C[C3]','C3_packets':9,'integral_fourier_index':index9,'index_factorization':'3^9'},
      'Pass1147_schlaefli_steinberg':{'decomposition':'C^81 tensor C[C3]','C3_color_multiplicity':81,'integral_fourier_index_decimal':str(index81),'index_factorization':'3^81'},
      'theorem':'The new C105/C6 27-state selector and the old Schlaefli-Steinberg A2-color construction use exactly the same C3/qutrit Fourier functor. Their only difference at this level is multiplicity: nine packets versus eighty-one rank-one color coordinates. The unavoidable integral denominator has prime 3 with exponent equal to the multiplicity, giving index 3^9 versus 3^81.',
      'boundary':'Exact Smith-normal-form and existing-certificate comparison. No canonical map between the 9-dimensional reduced C35 multiplicity space and the 81-dimensional Steinberg multiplicity space is claimed.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','new_index':index9,'old_index':'3^81','common':'C3 Fourier'}))
if __name__=='__main__':main()
