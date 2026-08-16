#!/usr/bin/env python3
"""Pass5629: try to turn the exact selected135 -> 270 cover into a connected refinement tower.

Pass4719 proves that the canonical six-sheet S3 closure is isomorphic to the
Kronecker/bipartite double cover of selected135, with 270 vertices, degree 12 and
spectrum
  12, 6, 3, 0, -3, -6, -12.

The obvious next refinement is another Kronecker C2 lift.  It fails structurally:
for every graph G,
  (G x K2) x K2 = G x (K2 x K2),
and K2 x K2 is two disjoint K2s.  Equivalently, once the first connected cover is
bipartite, the next bipartite double cover has top eigenvalue d with multiplicity
2 and is disconnected.  The spectrum merely duplicates; no new scale appears.

So the repo's existing C2 covers cannot be stacked naively into a connected Weyl
refinement tower.  A genuinely new nontrivial voltage/cohomology class is required
at every subsequent level.
"""
from __future__ import annotations
import json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'data/PART_W33_PASS4719_S3_REGULAR_CLOSURE.json'
OUT=ROOT/'data/PART_W33_PASS5629_CONNECTED_COVER_TOWER_OBSTRUCTION.json'

def parse_spec(d):
    out=Counter()
    for k,v in d.items():
        try: x=float(k)
        except ValueError: continue
        out[x]+=int(v)
    return out

def double_cover_spectrum(spec):
    out=Counter()
    for x,m in spec.items(): out[x]+=m;out[-x]+=m
    return out

def main():
    x=json.loads(SRC.read_text())
    r=x['regular_closure']; assert r['vertices']==270 and r['degree']==12 and r['bipartite'] is True
    spec=parse_spec(r['spectrum'])
    assert spec==Counter({12.0:1,6.0:30,3.0:44,0.0:120,-3.0:44,-6.0:30,-12.0:1})
    spec2=double_cover_spectrum(spec)
    assert sum(spec.values())==270 and sum(spec2.values())==540
    assert spec2[12.0]==2 and spec2[-12.0]==2
    # In a d-regular graph, multiplicity of eigenvalue d equals the number of
    # connected components. Hence the second double cover has two components.
    components=spec2[12.0]; assert components==2
    # Since the first spectrum is already sign-symmetric, the second level has
    # exactly the same distinct eigenvalue set.
    assert set(spec2)==set(spec)
    out={
      'pass':5629,'status':'NAIVE_C2_REFINEMENT_TOWER_DISCONNECTS_AFTER_FIRST_BIPARTITE_LIFT',
      'level1':{'vertices':270,'degree':12,'connected':True,'bipartite':True,'distinct_adjacency_eigenvalues':sorted(spec)},
      'level2_naive_C2':{'vertices':540,'degree':12,'components':components,'distinct_adjacency_eigenvalues':sorted(spec2),'top_eigenvalue_multiplicity':spec2[12.0]},
      'exact_identity':'(G x K2) x K2 = G x (K2 x K2), and K2 x K2 is 2 K2',
      'spectral_consequence':'the second lift duplicates the first spectrum and introduces no new eigenvalue scale; it cannot support a new Weyl exponent',
      'tower_boundary':'The repo has other exact covers such as the 810->1620 apartment C2 cover, but they are not a certified nested child of this 270 carrier. Fitting a dimension across unrelated carriers would be invalid.',
      'next_requirement':'A connected refinement tower needs a new nontrivial voltage/cohomology class on each current-level graph, rather than repeated use of the parity/Kronecker class.',
      'physics_boundary':'This is an exact graph-cover obstruction. It neither proves nor disproves continuum spacetime; it rules out the simplest existing C2 iteration as the mechanism.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
