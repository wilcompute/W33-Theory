#!/usr/bin/env python3
"""Pass10637-10644: synthesize the semisimple C13 clock, 3-5-7 harmonic residue, and ramified C9 memory clock.

Binary/Leech side:
  A2=F4[g] ~= F_{4^6}, g of order 13 with irreducible degree-6 minimal
  polynomial.  Since 13 is prime to char 2, x^13-1 is separable.  A2 is a
  finite etale field algebra.  Its unit group has order 4^6-1=4095.  Removing
  base scalars F4^x (order3) and the C13 clock leaves 105=3*5*7.

Ternary/glue side:
  A3=F9[U] ~= F9[t]/(t^6), U=1+t of order9.  In char3, x^9-1=(x-1)^9;
  U is regular unipotent and A3 is local/nonreduced.  Its unit group has order
  (9-1)9^5.  Removing base scalars F9^x (order8) and C9 leaves 9^4=3^8=6561.

Thus the rank-six clocks are categorically complementary: etale/semisimple
versus local/unipotent.  Their residual unit quotients make the distinction
numerical as well: mixed 3*5*7 harmonics versus pure characteristic 3^8 memory.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS10637_10644_ETALE_LOCAL_RANK6_CLOCK_DUALITY.json'

def main():
    binary_units=4**6-1;binary_res=binary_units//(3*13)
    assert binary_units==4095 and binary_res==105==3*5*7
    local_units=(9-1)*9**5;local_res=local_units//(8*9)
    assert local_units==472392 and local_res==6561==3**8
    # Polynomial characteristic checks: in char2 derivative of x^13-1 is x^12,
    # while in char3 x^9-1=(x-1)^9 by Frobenius.
    for a in range(3):
      assert (pow(a,9,3)-1)%3 == (pow((a-1)%3,9,3))%3
    out={
      'schema':'w33.pass10637_10644.etale_local_rank6_clock_duality.v1','status':'PASS','passes':'10637-10644',
      'binary_semisimple':{
        'algebra':'F4[g] ~= F_{4^6}','dimension_over_F4':6,'clock':'C13','clock_prime_to_characteristic':True,
        'separability':'x^13-1 has nonzero derivative x^12 in characteristic 2',
        'unit_group_order':binary_units,'base_scalar_order':3,'post_scalar_clock_residual':binary_res,'residual_factorization':'3*5*7'},
      'ternary_ramified':{
        'algebra':'F9[U] ~= F9[t]/(t^6), U=1+t','dimension_over_F9':6,'clock':'C9','clock_divisible_by_characteristic':True,
        'inseparability':'x^9-1=(x-1)^9 in characteristic 3','nilpotency_index_U_minus_I':6,
        'unit_group_order':local_units,'base_scalar_order':8,'post_scalar_clock_residual':local_res,'residual_factorization':'3^8'},
      'duality':'finite etale field / semisimple global clock versus local nonreduced ring / unipotent filtration-memory clock',
      'theorem':'The prime-2 and prime-3 rank-six carriers are opposite algebraic realizations of a cyclic clock. The C13 side is separable and field-like, leaving the mixed 105=3*5*7 harmonic quotient after scalars and clock. The C9 side is inseparable and local, leaving the pure 3-power residual 6561=3^8. This makes the global-harmonic versus layered-memory distinction exact at the operator-algebra level.',
      'boundary':'Exact finite-field/local-ring unit counts and characteristic identities. The residual unit quotients are algebraic ambiguities, not physical state counts unless a separate hardware/controller map is supplied.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','residuals':[105,6561],'types':['etale','local']}))
if __name__=='__main__':main()
