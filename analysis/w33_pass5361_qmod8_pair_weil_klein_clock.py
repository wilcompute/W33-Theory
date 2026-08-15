#!/usr/bin/env python3
"""Pass5361: q mod 8 Klein-four clock from local pair characters + global Weil descent.

Two independent existing structures carry complementary quadratic bits.

(1) Pass5360 / Darafsheh--Pournaki pair character:
    the exceptional pair xi_1,xi_2 (q=1 mod4) or eta_1,eta_2 (q=3 mod4)
    occurs in C[C(P^1(q),2)] exactly for q=1 or 3 mod8.
    This is the real Dirichlet character chi_{-2}(q): +1 for 1,3 and -1 for 5,7.

(2) Pass223 / Lataille--Sin--Tiep Weil descent:
    the characteristic-2 Weil pair is defined over F2 exactly for q=1 or 7 mod8,
    and requires F4 for q=3 or 5 mod8. This is chi_2(q): +1 for 1,7 and -1 for 3,5.

Their product is chi_{-1}(q), so the pair (chi_{-2},chi_2) separates all four
units modulo 8. This is an arithmetic compatibility theorem only: it does not
identify the complex exceptional pair with the modular Weil pair.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5361_QMOD8_PAIR_WEIL_KLEIN_CLOCK.json'

def row(r):
    assert r in (1,3,5,7)
    chi2=1 if r in (1,7) else -1
    chim2=1 if r in (1,3) else -1
    chim1=1 if r in (1,5) else -1
    assert chi2*chim2==chim1
    return {'q_mod_8':r,'chi_2':chi2,'chi_minus2':chim2,'chi_minus1':chim1,
      'complex_pair_exceptional_sector':'present' if chim2==1 else 'absent',
      'binary_Weil_field':'F2' if chi2==1 else 'F4'}

def main():
    table={str(r):row(r) for r in (1,3,5,7)}
    signatures={(x['chi_minus2'],x['chi_2']) for x in table.values()};assert len(signatures)==4
    # Multiplicativity on the unit group U(8).
    for a in (1,3,5,7):
      for b in (1,3,5,7):
        c=(a*b)%8
        assert row(c)['chi_2']==row(a)['chi_2']*row(b)['chi_2']
        assert row(c)['chi_minus2']==row(a)['chi_minus2']*row(b)['chi_minus2']
    out={'pass':5361,'status':'THEOREM_QMOD8_PAIR_WEIL_KLEIN_FOUR_CLOCK',
      'table':table,
      'group_statement':'The map U(8)->{+/-1}^2, r |-> (chi_-2(r),chi_2(r)), is an isomorphism C2 x C2 -> C2 x C2.',
      'product_character':'chi_-2 * chi_2 = chi_-1',
      'pair_input':'Pass5360: exceptional complex pair appears exactly for residues 1,3 mod8.',
      'weil_input':'Pass223: characteristic-2 Weil factors descend to F2 exactly for residues 1,7 mod8; residues 3,5 require F4.',
      'interpretation':'The local characteristic-zero pair module and the global characteristic-two rank-3 shadow carry complementary q-mod-8 bits.',
      'boundary':'Arithmetic/representation-theoretic compatibility only. No isomorphism is claimed between the complex exceptional characters and the characteristic-2 Weil modules; no footprint-rank theorem follows.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
