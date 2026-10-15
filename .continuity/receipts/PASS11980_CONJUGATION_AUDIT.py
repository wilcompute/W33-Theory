import sys,itertools,json,numpy as np
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'analysis'))
from w33_pass11980_heisenberg_fixed_holonomies import build_module,DIRECTIONS
from w33_20261015_toe82_native_H27_h1_character import mul
G=list(itertools.product(range(3),repeat=3));gi={g:i for i,g in enumerate(G)};e=(0,0,0)
def pw(x,n):
 r=e
 for _ in range(n):r=mul(r,x)
 return r
F=sorted({tuple(sorted(gi[mul(g,t)] for t in (e,d,pw(d,2)))) for g in G for d in DIRECTIONS})
E=sorted({a for f in F for a in itertools.combinations(f,2)});ei={a:i for i,a in enumerate(E)}
c=json.loads((ROOT/'data/w33_pass11980_heisenberg_fixed_holonomies.json').read_text())
p=c['explicit_holonomies_and_matter_probe'];selected=p['uniform_hopping_finite_free_fermion_fillings']['18']['continuous_flat_torus_audit']['selected_coefficients']
_,B,C=build_module();phase=sum((a*np.array(b) for a,b in zip(selected,p['character_generators_mod9'])),np.zeros(64,dtype=int))%9
links=phase@C%9
records=[];automorphisms=0
for X in G:
 for Y in G:
  if mul(X,Y)==mul(Y,X):continue
  automorphisms+=1
  Z=mul(mul(mul(X,Y),pw(X,2)),pw(Y,2))
  pm=[gi[mul(mul(pw(X,a),pw(Y,b)),pw(Z,z))] for a,b,z in G]
  if {tuple(sorted(pm[v] for v in f)) for f in F}!=set(F):continue
  pull=np.array([(1 if pm[a]<pm[b] else -1)*links[ei[tuple(sorted((pm[a],pm[b])))]] for a,b in E])%9
  # Sum is exact iff permutation pullback conjugates the connection up to gauge.
  delta=(pull+links)%9
  fixed=not ((delta@B)%9).any()
  record={'X':X,'Y':Y,'center_image':Z,'conjugate_up_to_gauge':fixed,'vertex_permutation':pm}
  if fixed:
   v={0:0}
   while len(v)<27:
    old=len(v)
    for j,(a,b) in enumerate(E):
     if a in v:v.setdefault(b,(v[a]+int(delta[j]))%9)
     if b in v:v.setdefault(a,(v[b]-int(delta[j]))%9)
    assert len(v)>old
   assert all((v[b]-v[a]-delta[j])%9==0 for j,(a,b) in enumerate(E))
   record['gauge_compensator_mod9']=[v[i] for i in range(27)]
  records.append(record)
result={'automorphisms_enumerated':automorphisms,'face_preserving_automorphisms':len(records),'selected_N18_character_coefficients':selected,'conjugating_map_count':sum(r['conjugate_up_to_gauge'] for r in records),'maps':records,'scope':'Exact native-compatible Heisenberg automorphism plus gauge conjugation check on one stable free-matter representative; not physical spacetime CP.'}
print(json.dumps(result,indent=2))
