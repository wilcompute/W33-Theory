#!/usr/bin/env python3
"""Pass10621-10628: compare canonical Fourier square with E6 27/bar27 charge conjugation.

Pass10549 proves F^2 is negation on the 27 C6-orbit states of C105.  Under
C105 ~= C3 x C35, the C6 action is trivial on C3 and multiplication by 9 on
C35.  We compute the induced negation cycle type exactly: 3 fixed states and
12 transposed pairs.

E6 minuscule charge conjugation exchanges the 27 and bar27 weight sets.  On the
combined 54-state carrier it therefore has cycle type 2^27 and no fixed state.
Cycle type/trace is a conjugacy invariant, so F^2 cannot be identified with E6
charge conjugation by relabeling.  The two involutions must remain distinct:
internal harmonic negation versus external 27<->bar27 exchange.
"""
from __future__ import annotations
import json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS10621_10628_FOURIER_SQUARE_E6_CHARGE_CONJUGATION_NOGO.json'

def orbits35():
    seen=set();out=[]
    for s in range(35):
      if s in seen:continue
      O=[];x=s
      while x not in O:
        O.append(x);seen.add(x);x=(9*x)%35
      out.append(tuple(O))
    return out

def main():
    O=orbits35();assert len(O)==9
    oid={frozenset(x):i for i,x in enumerate(O)}
    neg35=[]
    for A in O:
      neg35.append(oid[frozenset((-x)%35 for x in A)])
    assert Counter(i==j for i,j in enumerate(neg35))==Counter({False:6,True:3})
    # 27 states = C3 x nine C35-orbits; negation sends (r,O)->(-r,-O).
    states=[(r,j) for r in range(3) for j in range(9)];si={x:i for i,x in enumerate(states)}
    p=[]
    for r,j in states:p.append(si[((-r)%3,neg35[j])])
    seen=set();lens=[]
    for i in range(27):
      if i in seen:continue
      C=[];x=i
      while x not in C:C.append(x);seen.add(x);x=p[x]
      lens.append(len(C))
    assert Counter(lens)==Counter({2:12,1:3})
    out={
      'schema':'w33.pass10621_10628.fourier_square_e6_charge_conjugation_nogo.v1','status':'PASS','passes':'10621-10628',
      'canonical_Fourier_square':{'action':'negation on C105/C6 orbit states','cycle_type':'1^3 2^12','trace_as_permutation_operator':3,'fixed_state_origin':'C3 coordinate 0 times the three self-negative C35/<9> orbits'},
      'E6_charge_conjugation':{'action':'exchange minuscule 27 and bar27','natural_carrier_size':54,'cycle_type':'2^27','fixed_states':0,'trace_as_permutation_operator':0},
      'direct_identification':False,
      'obstruction':'cycle type and trace are conjugacy invariants',
      'corrected_architecture':'retain two involutions: internal harmonic negation F^2 within a 27-state harmonic carrier, and an external E6 duality exchanging 27 with bar27',
      'theorem':'The canonical C105 Fourier square is not E6 charge conjugation. It is an internal negation involution with three fixed harmonic states, whereas E6 conjugation exchanges disjoint 27 and bar27 carriers without fixed weights. Any E6 bridge must therefore double the carrier and keep these operations distinct.',
      'boundary':'Exact finite orbit/cycle-type no-go plus standard minuscule-dual interpretation. No physical charge-conjugation operator is asserted.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','F2_cycle':'1^3 2^12','E6_cycle':'2^27','same':False}))
if __name__=='__main__':main()
