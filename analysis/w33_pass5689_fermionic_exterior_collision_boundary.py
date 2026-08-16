#!/usr/bin/env python3
"""Pass5689 bonkers: can ordinary fermionic exclusion explain the E6 36/9 projector?

There are nine base fibers, each with three distinct Z3-resolved one-particle modes.
On the full 27-mode one-particle space W = direct_sum_b W_b, dim W_b=3, ordinary
fermionic antisymmetry uses Lambda^3 W.  A vertical cubic occupies the three distinct
modes in one W_b, so

    e_{b,0} wedge e_{b,1} wedge e_{b,2} != 0.

Therefore standard fermionic statistics DO NOT kill the vertical nine.

If one first projects each three-mode fiber to a single hard-core base mode e_b and
then uses Lambda^3 C^9, every vertical support maps to e_b wedge e_b wedge e_b=0,
while every horizontal support on three distinct base fibers survives.  Thus exterior
exclusion reproduces the collision projector only AFTER imposing the same one-mode-
per-fiber quotient/hard-core principle found in Pass5676.
"""
from __future__ import annotations
import itertools,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5689_FERMIONIC_EXTERIOR_COLLISION_BOUNDARY.json'

def wedge3_key(vs):
    # basis wedge is nonzero iff all one-particle basis labels are distinct
    return tuple(sorted(vs)) if len(set(vs))==3 else None

def main():
    full_vertical=[];base_vertical=[]
    for b in range(9):
        full=[(b,z) for z in range(3)]
        full_vertical.append(wedge3_key(full))
        base_vertical.append(wedge3_key([b,b,b]))
    assert all(x is not None for x in full_vertical)
    assert all(x is None for x in base_vertical)
    # AG(2,3) 12 lines, three fiber lifts each -> 36 horizontal supports.
    pts=[(x,y) for x in range(3) for y in range(3)];idx={p:i for i,p in enumerate(pts)}
    dirs=[(1,m) for m in range(3)]+[(0,1)];lines=set()
    for p in pts:
        for dx,dy in dirs:
            lines.add(tuple(sorted(idx[((p[0]+t*dx)%3,(p[1]+t*dy)%3)] for t in range(3))))
    assert len(lines)==12
    horizontal=[]
    for L in lines:
        for k in range(3):
            # one distinct internal mode per distinct base fiber; exact z-law is irrelevant to nonvanishing
            full=[(b,(k+i)%3) for i,b in enumerate(L)]
            horizontal.append((wedge3_key(full),wedge3_key(list(L))))
    assert len(horizontal)==36
    assert all(a is not None and b is not None for a,b in horizontal)
    out={
      'pass':5689,'status':'ORDINARY_FERMIONIC_STATISTICS_PRESERVES_VERTICAL9__BASE_HARDCORE_QUOTIENT_KILLS_IT',
      'full_one_particle_space':'W=direct_sum_{b=1}^9 W_b with dim W_b=3, total dim27',
      'full_fermionic_exterior':'Lambda^3 W',
      'vertical_full_fiber':'e_(b,0) wedge e_(b,1) wedge e_(b,2) is nonzero for all 9 fibers',
      'base_hardcore_projection':'W -> C^9 identifies the three internal fiber modes with one occupancy label e_b',
      'after_projection':'vertical maps to e_b wedge e_b wedge e_b=0; horizontal three-distinct-fiber supports remain nonzero',
      'counts':{'horizontal_survive_full':36,'vertical_survive_full':9,'horizontal_survive_base_hardcore':36,'vertical_survive_base_hardcore':0},
      'conclusion':'The collision projector is compatible with a fermionic/exterior interpretation only if a one-occupancy-per-fiber hard-core quotient is imposed before antisymmetrization. Ordinary Pauli exclusion on the full 27 resolved modes is insufficient.',
      'boundary':'This is a support-level exterior-algebra test. It neither proves that the E6 cubic fields are physical fermions nor derives the hard-core quotient from spin-statistics.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
