#!/usr/bin/env python3
"""Pass8401-8408: the actual U3(3) Leech controller does NOT select one of the 336 W(3,2) sectors.

Dependencies / external theorem:
- Pass8241-8248 identifies the 336 closed anticommuting Pauli triangles in W(5,2)
  with the 336 nondegenerate 2-spaces, hence with the 336 embedded W(3,2) perps.
- ATLAS identifies the S6(2) degree-336 primitive action with non-isotropic lines,
  point stabilizer S3 x S6, order 4320.
- The finite-geometry result quoted in "Some Two-Character Sets" (and Cooperstein's
  underlying orbit theorem) states that for q=2 the index-two subgroup
  U ~= PSU(3,3) of G2(2) remains transitive on the non-isotropic lines of PG(5,2).

This file rechecks the finite symplectic 336-set and the orbit-stabilizer arithmetic.
The transitivity input is a published group-action theorem, not inferred from counts.
"""
from __future__ import annotations
import itertools, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS8401_8408_U33_BINARY_NO_SELECTION.json'
V=[tuple((n>>i)&1 for i in range(6)) for n in range(1,64)]
def om(a,b): return (a[0]*b[3]+a[1]*b[4]+a[2]*b[5]+a[3]*b[0]+a[4]*b[1]+a[5]*b[2])&1
def add(a,b): return tuple(x^y for x,y in zip(a,b))
def main():
    triangles=set()
    for a,b in itertools.combinations(V,2):
        if om(a,b): triangles.add(frozenset((a,b,add(a,b))))
    assert len(triangles)==336
    assert all(len(T)==3 and all(om(x,y) for x,y in itertools.combinations(T,2)) for T in triangles)
    # Each triangle is exactly the nonzero part of a nondegenerate F2^2: a projective non-isotropic line.
    perps=[]
    for T in triangles:
        W=frozenset(v for v in V if all(om(v,u)==0 for u in T))
        assert len(W)==15
        perps.append(W)
    assert len(set(perps))==336
    sp6=1451520; ambient_stab=4320; u33=6048
    assert sp6//ambient_stab==336
    assert u33%336==0 and u33//336==18
    out={
      'schema':'w33.pass8401_8408.u33_binary_no_selection.v1','status':'PASS','passes':'8401-8408',
      'ambient':'Leech W(5,2) = six-dimensional symplectic F2 carrier',
      'Pauli_triangles':336,'embedded_W32_sectors':336,
      'geometric_identification':'closed anticommuting triangles = nonzero vectors of nondegenerate F2^2 = projective non-isotropic lines',
      'Sp6(2)':{'order':sp6,'degree336_stabilizer_order':ambient_stab,'stabilizer':'S3 x S6'},
      'U3(3)':{'order':u33,'published_action':'transitive on all non-isotropic lines at q=2','orbit_size':336,'triangle_stabilizer_order':18},
      'external_sources':[
        'https://brauer.maths.qmul.ac.uk/Atlas/v3/clas/S62/',
        'https://brauer.maths.qmul.ac.uk/Atlas/v3/clas/U33/',
        'Some Two-Character Sets: q=2 index-two U ~= PSU(3,3) remains transitive on non-isotropic lines (citing Cooperstein orbit results)'
      ],
      'theorem':'The U3(3) controller associated with the pure order-8 Leech rung is transitive on the entire 336-set of closed anticommuting Pauli triangles / embedded W(3,2) sectors. Hence it does not canonically select an E8 two-qubit sector.',
      'claim_boundary':'Transitivity is a published finite-group action theorem combined with the exact Pass8241 object identification. This is a no-selection result; no physical subsystem claim follows.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','triangles':336,'U33_orbit':336,'stabilizer':18}))
if __name__=='__main__': main()
