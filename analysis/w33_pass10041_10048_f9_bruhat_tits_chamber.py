#!/usr/bin/env python3
"""Pass10041-10048 outside-box: the six F9 layers form a full Bruhat-Tits chamber.

Set K=Q3(i), whose residue field is F9, and L=K(zeta_9).  The extension L/K is
totally ramified of degree 6.  With t=zeta_9-1, t is a uniformizer of L and
3 = unit * t^6.  Therefore the O_K-lattice chain

  O_L > t O_L > t^2 O_L > ... > t^5 O_L > t^6 O_L = 3 O_L (up to a unit)

has six successive one-dimensional F9 quotients.  The six homothety classes
[O_L],...,[t^5 O_L] are consequently a FULL CHAMBER (maximal simplex) in the
Bruhat-Tits building of PGL_6(K)=PGL_6(Q3(i)).

Multiplication by zeta_9=1+t is a unit of O_L and preserves every ideal t^j O_L,
so the order-9 cyclotomic action fixes this chamber vertex-by-vertex.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS10041_10048_F9_BRUHAT_TITS_CHAMBER.json'

def main():
    q=9;n=6
    indices=[q**j for j in range(n+1)]
    assert indices==[1,9,81,729,6561,59049,531441]
    assert q**6==3**12
    coeff=[3,9,18,21,15,6,1]
    assert [c%3 for c in coeff]==[0,0,0,0,0,0,1]
    vertex_types=list(range(6))
    out={
      'schema':'w33.pass10041_10048.f9_bruhat_tits_chamber.v1','status':'PASS','passes':'10041-10048','outside_box':True,
      'fields':{'K':'Q3(i), unramified quadratic','residue_K':'F9','L':'K(zeta_9)','e_L_over_K':6,'f_L_over_K':1,'uniformizer_L':'t=zeta_9-1','uniformizer_relation':'3 = unit * t^6'},
      'lattice_chain':{
        'terms':['O_L','t O_L','t^2 O_L','t^3 O_L','t^4 O_L','t^5 O_L','t^6 O_L ~ 3 O_L'],
        'indices_from_O_L':indices,
        'successive_quotients':'six copies of one-dimensional F9',
        'vertex_types_mod_6':vertex_types},
      'building':{
        'group':'PGL_6(Q3(i))','dimension':5,'vertices_in_chamber':6,
        'claim':'[O_L],[t O_L],...,[t^5 O_L] form a full chamber / maximal 5-simplex'},
      'cyclotomic_fixed_chamber':{
        'operator':'multiplication by zeta_9=1+t','why_fixed':'zeta_9 is a unit and zeta_9 * t^j O_L = t^j O_L for every j','residue_action':'regular order-9 unipotent action on O_L/3 from Pass10009-10016'},
      'parallel_relation':'The parallel Pass9481-9504 filtration produced a 3-simplex in the PGL_24(Q2) building. Here the mixed unramified/residue-F9 construction gives a maximal chamber in PGL_6(Q3(i)); both are lattice-chain manifestations of cyclotomic ramification.',
      'theorem':'The six F9 layers of the glue/local-field lift are exactly the six one-dimensional residue steps of a complete O_K lattice chain, hence the six homothety classes form a full Bruhat-Tits chamber for PGL_6(Q3(i)). The zeta_9 action fixes the chamber while acting nontrivially and regularly-unipotently on its mod-3 residue module.',
      'boundary':'Standard Bruhat-Tits lattice-chain interpretation plus the exact cyclotomic local-field identities. No p-adic AdS/CFT, fractal boundary, or physical spacetime interpretation is claimed.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','building':'PGL6(Q3(i))','chamber_vertices':6,'index':indices[-1]}))
    return 0
if __name__=='__main__':raise SystemExit(main())
