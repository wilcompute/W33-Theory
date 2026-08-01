#!/usr/bin/env python3
from __future__ import annotations
import collections,hashlib,itertools,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
 p=json.loads((ROOT/'data/w33_pass1837_middle_layer_compression.json').read_text())
 cols=[int(x) for x in (ROOT/'data/w33_pass1848_syndrome_columns.txt').read_text().split()]
 F=p['canonical_six_line_pack'];R=p['residual_vertices'];part={v:i for i,x in enumerate(F) for v in x};part.update({v:6 for v in R})
 duads=list(itertools.combinations(range(6),2));di={int(k):v for k,v in p['residual_to_duad_index'].items()};edges=[tuple(i for i in range(45)if c>>i&1)for c in cols]
 typ=collections.Counter(tuple(sorted(part[v]for v in e))for e in edges)
 residual=[e for e in edges if all(part[v]==6 for v in e)]
 residual_triangles=[]
 for e in residual:
  ds=tuple(sorted(duads[di[v]] for v in e));verts=sorted(set(itertools.chain.from_iterable(ds)));assert len(verts)==3
  residual_triangles.append(tuple(verts))
 assert set(residual_triangles)==set(itertools.combinations(range(6),3))
 allD=set(duads);syntheme_map={}
 for i,j in duads:
  inc=set()
  for e in edges:
   if sorted(part[v]for v in e)==[i,j,6]:inc.add(duads[di[next(v for v in e if part[v]==6)]])
  miss=tuple(sorted(allD-inc));assert len(miss)==3 and len(set(itertools.chain.from_iterable(miss)))==6
  syntheme_map[f'{i}{j}']=[list(x)for x in miss]
 synthemes={tuple(tuple(x)for x in v)for v in syntheme_map.values()};assert len(synthemes)==15
 triple={}
 for I in itertools.combinations(range(6),3):
  rows=[]
  for e in edges:
   if tuple(sorted(part[v]for v in e))==I:rows.append([F[k].index(next(v for v in e if part[v]==k))for k in I])
  assert len(rows)==2;triple[''.join(map(str,I))]=rows
 checks={'240_factorization':typ[(6,6,6)]==20 and all(typ[I+(6,)]==12 for I in duads) and all(typ[I]==2 for I in itertools.combinations(range(6),3)),
 'residual_all_K6_triangles':len(set(residual_triangles))==20,'duad_to_all_synthemes':len(synthemes)==15,'two_phase_each_fiber_triple':len(triple)==20}
 out={'schema':'w33.pass1848.duad_syntheme_transfer.v1','status':'PASS' if all(checks.values()) else 'FAIL','checks':checks,
 'check_factorization':{'residual_triangles':20,'fiber_pair_duad_checks':180,'fiber_triple_phase_checks':40,'identity':'240=20+15*12+20*2'},
 'duad_to_syntheme_outer_map':syntheme_map,'fiber_triple_phases':triple,
 'theorem':'The 15 fiber pairs (duads) map bijectively to the 15 missing perfect matchings (synthemes). The 20 residual checks are exactly the 20 K6 triangles, and every fiber triple carries two phase checks. This is the classical duad-syntheme realization of the exceptional outer automorphism of S6 inside the 6x5+KG(6,2) separator.',
 'boundary':'This freezes the exact transfer algebra and its S6 outer-automorphism carrier. A complete middle-layer weight enumerator still requires contracting the two phase tensors across all six fibers.'}
 raw=json.dumps(out,sort_keys=True,separators=(',',':')).encode();out['sha256']=hashlib.sha256(raw).hexdigest();print(json.dumps(out,sort_keys=True,separators=(',',':')));raise SystemExit(out['status']!='PASS')
if __name__=='__main__':main()
