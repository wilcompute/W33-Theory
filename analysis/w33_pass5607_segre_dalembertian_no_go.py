#!/usr/bin/env python3
"""Pass5607: finite Segre d'Alembertian and a full-symmetry no-go theorem.

On X=P1(q)xP1(q), PSL2(q) is 2-transitive on each ruling. Therefore the
commutant on one coordinate is span{I,J}; the full product commutant is at most
span{I⊗I,I⊗J,J⊗I,J⊗J}. Any linear operator preserving the complete independent
projective symmetry has at most four joint spectral sectors.

The most direct indefinite ruling operator uses L_K=nI-J on each P1, n=q+1:
    Box_q = L_K⊗I - I⊗L_K.
It has spectrum 0^(q^2+1), +(q+1)^q, -(q+1)^q. The mixed second derivative
L_K⊗L_K has only 0 and (q+1)^2. Thus exact full projective symmetry is too
restrictive to produce a dispersive continuum wave operator.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5607_SEGRE_DALEMBERTIAN_NO_GO.json'

def packet(q:int):
    n=q+1
    return {
      'q':q,'events':n*n,
      'box_spectrum':[{'eigenvalue':0,'multiplicity':q*q+1},{'eigenvalue':n,'multiplicity':q},{'eigenvalue':-n,'multiplicity':q}],
      'mixed_spectrum':[{'eigenvalue':0,'multiplicity':2*q+1},{'eigenvalue':n*n,'multiplicity':q*q}],
      'box_kernel_fraction':(q*q+1)/(n*n),
    }

def main():
    out={
      'status':'THEOREM_FULL_PROJECTIVE_SYMMETRY_NO_DISPERSIVE_DALEMBERTIAN',
      'commutant_theorem':'Because PSL2(q) is 2-transitive on P1(q), End_G(R[P1])=span{I,J}. Hence End_{GxG}(R[P1xP1]) is 4-dimensional, with at most four joint spectral sectors.',
      'canonical_operator':'Box_q=(nI-J) tensor I - I tensor (nI-J), n=q+1',
      'canonical_spectrum':'0^(q^2+1) + (q+1)^q + (-(q+1))^q',
      'mixed_operator':'(nI-J) tensor (nI-J)',
      'verdict':'A useful finite indefinite operator exists, but exact PGL/PSL product symmetry makes it massively degenerate and non-dispersive. A physical wave operator must add phase/holonomy, directed transport, chart order, defects, or symmetry breaking.',
      'samples':[packet(q) for q in (3,5,7,9,11,25,49)],
      'physics_firewall':'No Lorentzian continuum, speed of light, mass shell, or 3+1-dimensional wave equation is derived by this no-go theorem.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__': main()
