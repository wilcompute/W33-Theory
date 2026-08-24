#!/usr/bin/env python3
"""Pass10361-10368 outside-box: rank-six F4/F9 semisimple-vs-ramified clock duality.

Canonical V2 has 2^12=4^6 elements and, by Pass10345, a stabilizer containing
G2(4).  Independently, the ATLAS of finite group representations supplies the
natural six-dimensional representation of G2(4) over F4 and a 12-dimensional
F2 representation for G2(4):2.

On the prime-2 side:
  ord_13(4)=6,
so Phi_13 is degree six over F4.  A C13 clock on F4^6 is therefore semisimple
and irreducible at rank six; F4^6\{0} has 4095=13*315 vectors.

On the prime-3 side, the exact repo local-field construction gives
  O_L/3 ~= F9[t]/(t^6),  zeta9 = 1+t,
with U=1+N, N^6=0 and U of order nine.  This is a ramified/unipotent rank-six
clock over the other quadratic residue field F9.

Thus the project has a precise rank-six quadratic-extension mirror:

  characteristic 2: F4^6, semisimple C13 / Phi13 clock;
  characteristic 3: F9[t]/t^6, unipotent C9 / cyclotomic-uniformizer clock.

The theorem here is the arithmetic/representation architecture.  It does NOT
claim that the stored canonical V2 coordinate action has already been explicitly
conjugated to the ATLAS natural F4^6 matrices; that is the next module-level test.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS10361_10368_RANK6_F4_F9_CLOCK_DUALITY.json'

def ordmod(a,n):
    x=1
    for k in range(1,100):
        x=x*a%n
        if x==1:return k
    raise RuntimeError

def main():
    v2=json.loads((ROOT/'data/PART_W33_PASS10345_10352_CANONICAL_V2_GOOD_ORBIT7.json').read_text())
    loc=json.loads((ROOT/'data/PART_W33_PASS10009_10016_F9_RESIDUE_RING_UNITARY_LIFT.json').read_text())
    assert 2**12==4**6==4096
    assert 4**6-1==4095==13*315
    assert ordmod(4,13)==6
    assert ordmod(2,13)==12
    # Degree over F4 halves the F2 degree exactly because [F4:F2]=2.
    assert ordmod(2,13)==2*ordmod(4,13)
    assert v2['orbit7']['Stab_in_Co1']=='G2(4) x A4'
    assert v2['C13_closure']['exists_actual_C13_in_Stab_V2'] is True

    assert loc['exact_residue_ring']['isomorphism']=='O_L / 3 O_L ~= F9[t]/(t^6)'
    assert loc['exact_residue_ring']['F9_dimension']==6
    assert loc['regular_unitary_model']['N_nilpotency_index']==6
    assert loc['regular_unitary_model']['U_order']==9
    assert 9**6==3**12

    # cyclotomic identities giving the two sixes
    phi13=13-1
    assert phi13//2==6  # degree over F4 because ord_13(4)=6
    phi9=6
    assert phi9==6

    out={
      'schema':'w33.pass10361_10368.rank6_f4_f9_clock_duality.v1','status':'PASS','passes':'10361-10368','outside_box':True,
      'prime2_side':{
        'canonical_V2_cardinality':4096,'rewrite':'2^12 = 4^6','stabilizer_contains':'G2(4)',
        'external_ATLAS_representation_input':'G2(4) has a natural 6-dimensional representation over GF(4); G2(4):2 has a 12-dimensional representation over GF(2)',
        'clock':'C13','ord_13_4':6,'ord_13_2':12,'nonzero_vectors':4095,'C13_cycles_if_irreducible':315,
        'type':'semisimple / irreducible cyclotomic over F4'},
      'prime3_side':{
        'module':'F9[t]/(t^6)','F9_rank':6,'F3_dimension':12,'clock':'C9 via U=1+N','N_nilpotency_index':6,'U_order':9,
        'type':'totally ramified / unipotent cyclotomic over F9'},
      'rank6_mirror':{
        'common_rank':6,'quadratic_residue_fields':['F4/F2','F9/F3'],
        'contrast':'prime2 clock diagonalizes semisimply through Phi13 over F4; prime3 clock survives as nilpotent extension data through Phi9(1+t)=t^6 mod3'},
      'theorem':'The project contains two complementary six-dimensional quadratic-extension clock architectures. The characteristic-2 side naturally supports the G2(4) six-dimensional F4 module with an irreducible semisimple C13 clock because ord_13(4)=6; the characteristic-3 side is the exact F9[t]/t^6 local residue module carrying the unipotent order-9 clock U=1+N. Both have underlying prime-field dimension 12, but one is unramified/semisimple and the other ramified/unipotent.',
      'next_exact_target':'Conjugate the actual G2(4) action on canonical V2 to the restriction of scalars of the ATLAS natural F4^6 representation, thereby upgrading this representation-theoretic mirror to a coordinate theorem.',
      'boundary':'ATLAS supplies the existence of the natural GF(4)^6 representation; the repo supplies V2 cardinality/stabilizer and the F9^6 local module. This pass does not yet prove the stored V2 action is equivalent to the ATLAS natural representation.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','F4_rank':6,'F9_rank':6,'clock2':'C13 semisimple','clock3':'C9 unipotent'}))
    return 0
if __name__=='__main__':raise SystemExit(main())
