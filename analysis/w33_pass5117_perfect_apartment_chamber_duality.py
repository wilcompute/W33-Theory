#!/usr/bin/env python3
"""Pass5117 (bonkers): perfect duality of chamber gauge and apartment theta presentations."""
from __future__ import annotations
import json
from pathlib import Path
from analysis.w33_pass5074_gauge_active_chart_tester import build_W
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5117_PERFECT_APARTMENT_CHAMBER_DUALITY.json'

def rank2(rows):
    piv={}
    for r0 in rows:
        r=r0
        while r:
            p=r.bit_length()-1
            if p in piv:r^=piv[p]
            else:piv[p]=r;break
    return len(piv)

def anchor(q):
    G=build_W(q);E=len(G['flags']);V=len(G['pts'])+len(G['lines'])
    # Levi vertex-edge incidence rows as bitsets on chamber edges.
    rows=[0]*V
    for e,(p,l) in enumerate(G['flags']):rows[p]|=1<<e;rows[len(G['pts'])+l]|=1<<e
    r=rank2(rows);assert r==V-1
    cycle_dim=E-r;assert cycle_dim==q**4
    return {'q':q,'edge_space_dimension':E,'cut_dimension':r,'cycle_dimension':cycle_dim,
            'quotient_edge_mod_cut_dimension':E-r,'perfect_dual_dimension':q**4}

def main():
    out={'pass':5117,'status':'THEOREM_ALL_Q_PERFECT_PRESENTATION_DUALITY',
         'linear_algebra':'For the Levi incidence matrix B over F2, Cut=im(B^T)=(ker B)^perp=Z1^perp. Hence F2^E/Cut is canonically Z1^*.',
         'repo_identifications':['Pass5110: apartment code = chamber edge coefficients modulo Cut','Pass5066: apartment generators modulo theta = Z1(Levi;F2)'],
         'perfect_pairing':'<[g],[A]> = g dot boundary(A) mod 2; this is exactly the apartment coordinate of the chamber-generated codeword.',
         'conclusion':'Apartment code ~= Hom_F2(apartment/theta presentation,F2) canonically. The gauge/cohomology characters used in the Fourier formulation are literally the full character group of the theta presentation.',
         'anchors':{str(q):anchor(q) for q in (2,3,4,5)},
         'boundary':'Perfect finite-field duality does not imply that the cycle space is canonically self-dual as a subspace; the bicycle/radical intersection can be nonzero. The theorem is quotient-versus-dual, not an orthogonal direct-sum claim.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
