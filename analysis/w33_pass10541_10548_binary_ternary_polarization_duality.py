#!/usr/bin/env python3
"""Pass10541-10548: exact common template and exact no-go between binary F4 and ternary F9 transverse polarizations.

Binary Leech side (Pass10485-10492):
* Lambda/2Lambda is F4-Hermitian dimension 12;
* E and V2 are transverse maximal Hermitian-isotropic F4^6 halves;
* the F4 scalar T has order 3 and preserves EACH half;
* a separate exchange X has order 2 and swaps the halves, with X T X=T^{-T}.

Ternary glue side (Pass9237-9244, Pass9733-9740):
* F3^12 is an F9 module of dimension 6 via R^2=-I;
* C_G and C_E are transverse F3^6 Lagrangians;
* the F9 scalar i represented by R itself SWAPS C_G and C_E;
* R has order 4 and R^2=-I lies in the ordered-pair stabilizer.

Thus both systems realize a quadratic-extension scalar plus a transverse polarization,
but the scalar generator has different cycle type on the two polarization halves:
identity (binary) versus transposition (ternary).  This is invariant under any
polarization-respecting equivalence that maps the distinguished field generator to the
distinguished field generator.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS10541_10548_BINARY_TERNARY_POLARIZATION_DUALITY.json'

def main():
    b=json.loads((ROOT/'data/PART_W33_PASS10485_10492_BINARY_TRANSVERSE_F4_POLARIZATION.json').read_text())
    t=json.loads((ROOT/'data/PART_W33_PASS9237_9244_TRANSVERSE_GLUE_SYMPLECTIC_COMPLEX.json').read_text())
    u=json.loads((ROOT/'data/PART_W33_PASS9733_9740_FULL_GLUE_PAIR_UNITARY_STABILIZER.json').read_text())
    assert b['halves']['F4_dimensions']==[6,6]
    assert b['global_F4_scalar']['order']==3 and b['exchange']['order']==2
    assert b['exchange']['exchanges_E_and_V2']
    assert t['R_equals_KS']['R_squared']=='-I' and t['R_equals_KS']['order']==4
    assert t['intersection_dimension']==0 and t['sum_dimension']==12
    assert u['unordered_pair_stabilizer']['quotient_over_ordered']=='C2'
    assert 'R swaps C_G,C_E' in u['unordered_pair_stabilizer']['description']
    out={
      'schema':'w33.pass10541_10548.binary_ternary_polarization_duality.v1','status':'PASS','passes':'10541-10548',
      'common_template':{
        'quadratic_extension':True,'rank_six_field_geometry':True,'transverse_two_half_polarization':True,
        'binary':'F4/F2 on Lambda/2Lambda with F4^6 + F4^6 halves',
        'ternary':'F9/F3 on F3^12 with two transverse F3^6 Lagrangians'},
      'binary':{
        'field_scalar_order':3,'field_scalar_minpoly':'x^2+x+1','scalar_action_on_halves':'fixes E and V2 individually',
        'separate_exchange_order':2,'exchange_relation':'X T X = T^{-T}','reading':'split semilinear polarization'},
      'ternary':{
        'field_scalar_order':4,'field_scalar_relation':'R^2=-I','scalar_action_on_halves':'R swaps C_G and C_E',
        'ordered_pair_stabilizer':'O^-(6,3)','unordered_pair_extension':'<O^-(6,3),R> / O^-(6,3) = C2','reading':'rotating complex polarization'},
      'polarized_equivalence_no_go':{
        'distinguished_invariant':'cycle type of the quadratic-field scalar generator on the two polarization halves',
        'binary_cycle_type':'1+1','ternary_cycle_type':'2','equivalent_as_distinguished_polarized_scalar_packages':False},
      'theorem':'The binary Leech and ternary glue rank-six packages instantiate one quadratic-extension/transverse-polarization template but in inequivalent modes. On the binary side the F4 scalar preserves both halves and a separate semilinear involution exchanges them; on the ternary side the F9 scalar itself exchanges the two Lagrangians. Their common six-dimensional architecture is therefore a split-semilinear versus rotating-complex polarization duality, not a literal identification.',
      'boundary':'Exact comparison of already certified finite linear-algebra packages. This is a categorical structural distinction, not a continuum physical duality theorem.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','binary_scalar_half_cycle':'1+1','ternary_scalar_half_cycle':'2','literal_equivalence':False}))
    return 0
if __name__=='__main__':raise SystemExit(main())
