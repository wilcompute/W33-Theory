#!/usr/bin/env python3
"""Pass10345-10352: identify canonical V2 with good-sublattice orbit 7 and close C13 existence.

This pass combines one exact repo invariant with the published Nebe--Parker
classification of the 16 Aut(Leech)=2.Co1 orbits on good sublattices.

Repo input:
  canonical V2 = im((I-M)^2) for the unique pure order-8 element M, and
  |C_Co0(M)| = 48384 = 2^8 * 3^3 * 7.
Every element commuting with M preserves im((I-M)^2), hence

  C_Co0(M) <= Stab_Co0(V2).

External classification input (Nebe--Parker, Math. Comp. 83 (2014), table of
stabilisers/profiles of the 16 good-sublattice orbits): the 2.Co1 stabilizer
prime factorizations listed below.  Divisibility by 2^8*3^3*7 eliminates 15 of
16 rows.  The UNIQUE survivor is orbit 7, whose Co1 stabilizer is
G2(4) x A4 and whose good-sublattice profile is uniform 64^4095.

Consequences:
* canonical V2 lies in good-sublattice orbit 7;
* Stab_Co1(V2) ~= G2(4) x A4 (and the 2.Co1 preimage has twice that order);
* because 13 divides |G2(4)|, an ACTUAL order-13 element stabilizes canonical V2.

This resolves the existence question left open by Pass10049/10113.  It does not
yet give the explicit Co0 word conjugating the tested 13A representative onto
one that fixes the stored V2 basis.
"""
from __future__ import annotations
import json,math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS10345_10352_CANONICAL_V2_GOOD_ORBIT7.json'
SRC=ROOT/'data/PART_W33_PASS9985_9992_C13_V2_STABILIZER_GATE.json'

def val(f):
    n=1
    for p,e in f.items():n*=int(p)**int(e)
    return n

def main():
    src=json.loads(SRC.read_text())
    c=int(src['canonical_V2']['centralizer_order']);assert c==48384
    cf={2:8,3:3,7:1};assert val(cf)==c

    # Published |Stab(E)| in 2.Co1, encoded by prime factorization.
    # These are the table entries; only divisibility is used below.
    stabs={
      1:{2:5,3:1,5:2,13:1},
      2:{2:7,3:3,5:1,7:2},
      3:{2:4,3:2,7:1,13:1},
      4:{2:7,3:4,5:2},
      5:{2:7,3:2,7:2},
      6:{2:16,3:3,5:1},
      7:{2:15,3:4,5:2,7:1,13:1},
      8:{2:4,3:1,11:1,23:1},
      9:{2:12,3:1},
      10:{2:13,3:2},
      11:{2:9,3:1,7:1},
      12:{2:12,3:2},
      13:{2:5,3:3,5:1,7:1},
      14:{2:10,3:1,5:1},
      15:{2:9,3:1,7:1},
      16:{2:15,3:3},
    }
    def divisible(f,need):return all(f.get(p,0)>=e for p,e in need.items())
    survivors=[i for i,f in stabs.items() if divisible(f,cf)]
    assert survivors==[7],survivors

    # Independent order check from G2(4) x A4.
    g24=(4**6)*(4**6-1)*(4**2-1)
    assert g24==251_596_800
    A4=12;co1_stab=g24*A4;double_stab=2*co1_stab
    assert co1_stab==3_019_161_600 and double_stab==6_038_323_200
    assert double_stab%c==0 and co1_stab%c==0
    assert g24%13==0

    out={
      'schema':'w33.pass10345_10352.canonical_v2_good_orbit7.v1','status':'PASS','passes':'10345-10352',
      'repo_input':{'canonical_V2':'im((I-M)^2) for the unique pure order-8 M','C_Co0_M_order':c,'factorization':'2^8 * 3^3 * 7','inclusion':'C_Co0(M) <= Stab_Co0(V2)'},
      'published_good_sublattice_classification':{'orbits':16,'stabilizer_factorizations_2Co1':{str(i):{str(p):e for p,e in f.items()} for i,f in stabs.items()},'divisible_by_C_Co0_M':survivors},
      'orbit7':{'identified_as_canonical_V2_orbit':True,'Stab_in_Co1':'G2(4) x A4','Stab_Co1_order':co1_stab,'Stab_2Co1_order':double_stab,'profile':'64^4095','profile_meaning':'all 4095 nonzero quotient classes have bad-vector-set size 64'},
      'C13_closure':{'G2_4_order':g24,'13_divides_G2_4':True,'exists_actual_C13_in_Stab_V2':True,
                     'reconciliation':'Pass10049 tested one explicit Co1 class-13A representative and it did not fix the stored V2. Co1 has one 13A class, so a conjugate representative inside the orbit-7 stabilizer does fix V2.'},
      'theorem':'Canonical V2 is the unique good-sublattice orbit whose published 2.Co1 stabilizer can contain the exact repo centralizer C_Co0(M) of order 48384. Therefore V2 is Nebe--Parker good-sublattice orbit 7, with stabilizer G2(4) x A4 and uniform profile 64^4095. In particular an actual C13 <= G2(4) <= Stab_Co1(V2) exists, closing the C13-stabilizer existence question.',
      'next_exact_target':'Construct an explicit Co0/Co1 conjugating word carrying the stored tested 13A representative to one inside Stab(V2), and compare that G2(4) factor with the Hall--Janko/G2 controller already present elsewhere in the repo.',
      'boundary':'The centralizer/inclusion is exact repo mathematics. Identification of the unique orbit uses the published Nebe--Parker 16-orbit stabilizer/profile table as external classification input; the table itself is not recomputed here.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','survivor_orbit':7,'profile':'64^4095','C13_exists':True,'Stab_Co1':co1_stab}))
    return 0
if __name__=='__main__':raise SystemExit(main())
