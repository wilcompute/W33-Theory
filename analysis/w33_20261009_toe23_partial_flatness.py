"""Round23: geometric partial flatness qutrit code surviving on native W33.
Subsets of the 1620 oriented 8-cycles are selected by a distinguished
vertex or edge, and preserve that geometry's stabilizer.
"""
from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261009_toe_integral_clique_levi_bridge import chain
from w33_20261009_round18_chirality_plaquette_audit import cycles_touching
from w33_20261009_round19_gauge_cycle_frustration import modrank
OUT=ROOT/'data/w33_20261009_toe23_partial_flatness.json'
def run():
 pts,ix,lines,li,edges,tris,flags,fi,E,T,D,M,R=chain()
 oriented=[(p,40+l) for p,l in flags]
 cycles=set()
 for j in range(160):cycles.update(cycles_touching(oriented,j))
 cycles=sorted(cycles)
 assert len(cycles)==1620
 eidx={tuple(sorted(e)):i for i,e in enumerate(oriented)}
 rows=[];vset=[];eset=[]
 for cyc in cycles:
  r={}
  for a,b in zip(cyc,cyc[1:]+cyc[:1]):
   k=eidx[tuple(sorted((a,b)))]
   r[k]=1 if a<b else -1
  assert len(r)==8
  rows.append(r);vset.append(set(cyc));eset.append(set(r))
 def summary(name,selected):
  rank=modrank([rows[i] for i in selected],3)
  assert 0<=rank<=81
  return dict(selector=name,checked_8cycles=len(selected),cycle_rank_mod3=rank,
    physical_link_qutrits=160,gauss_rank=79,
    encoded_logical_qutrits=81-rank,
    stabilizer_rank=79+rank,
    encoded_hilbert_dimension=f'3^{81-rank}')
 all_set=summary('all 1620 cycles',list(range(1620)))
 assert all_set['cycle_rank_mod3']==81
 e0=next(j for j,(a,b) in enumerate(oriented) if a==0)
 root_a,root_b=oriented[e0]
 nonincident=next(v for v in range(40,80) if v not in {w for a,w in oriented if a==0})
 labels=[
  ('cycles through point 0',[i for i,v in enumerate(vset) if 0 in v]),
  ('cycles through line endpoint '+str(root_b),[i for i,v in enumerate(vset) if root_b in v]),
  ('cycles through incidence edge '+str(e0),[i for i,e in enumerate(eset) if e0 in e]),
  ('cycles touching point 0 or incident line',[i for i,v in enumerate(vset) if (0 in v or root_b in v)]),
  ('cycles touching point 0 AND incident line',[i for i,v in enumerate(vset) if (0 in v and root_b in v)]),
  ('cycles touching point 0 AND nonincident line',[i for i,v in enumerate(vset) if (0 in v and nonincident in v)]),
  ('cycles avoiding point 0',[i for i,v in enumerate(vset) if 0 not in v]),
  ('cycles avoiding incidence edge',[i for i,e in enumerate(eset) if e0 not in e])]
 res=[summary(name,idx) for name,idx in labels]
 for q in res:print('FLATNESS',q['selector'],'cycles',q['checked_8cycles'],'rank',q['cycle_rank_mod3'],'logical',q['encoded_logical_qutrits'],flush=True)
 assert len(res)==8
 assert res[0]['cycle_rank_mod3']==res[1]['cycle_rank_mod3']
 assert res[0]['checked_8cycles']==res[1]['checked_8cycles']
 assert res[2]['cycle_rank_mod3']<=res[0]['cycle_rank_mod3']
 # Native flag-transitivity suggests a theorem; check every one of 160
 # incidence edges independently, both the through-edge and avoiding ranks.
 each_edge=[]
 for edge_id in range(160):
  through=[rows[i] for i,es in enumerate(eset) if edge_id in es]
  outside=[rows[i] for i,es in enumerate(eset) if edge_id not in es]
  ranks=(len(through),modrank(through,3),modrank(outside,3))
  each_edge.append(ranks)
 assert set(each_edge)=={(81,81,80)}
 print('ALL 160 FLAGS',set(each_edge),flush=True)
 out=dict(status='PASS',all_160_edge_checks=dict(eightcycles_through_each_edge=81,rank_through_each_edge=81,rank_avoiding_each_edge=80,independently_checked_edges=160),graph='native Levi W(3,3) 80 vertices 160 edges',gauge_rank_F3=79,full_flatness=all_set,selector_profiles=res,
   theorem='Choose vertex- or incidence-edge-selected local Wilson eight-cycle constraints together with all 80 native vertex Gauss X stabilizers. Each selected Wilson Z operator commutes with Gauss because oriented cycle is closed; the independent Wilson rank r leaves exactly 160-79-r=81-r logical qutrits. These geometrically chosen families respect the stabilizer subgroup of their selector, unlike arbitrary cycle subsets. They yield many exactly soluble commuting Hamiltonians with nontrivial surviving qutrit logical sectors.',
   important_boundary='The Wilson constraints are controlled assumptions of a finite graph Hamiltonian. Logical rank does not establish nonzero code distance, robust topological order, a physical excitation gap in the thermodynamic limit, or Standard Model gauge forces. Selection of a vertex/edge explicitly breaks full symplectic symmetry.')
 OUT.write_text(json.dumps(out,indent=2)+'\n')
 return out
if __name__=='__main__':run()
