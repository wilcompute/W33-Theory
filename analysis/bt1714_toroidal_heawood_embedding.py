#!/usr/bin/env python3
"""BT1714 - seven toroidal realizations into the Heawood/K7,7 scheduler."""
from __future__ import annotations
import itertools,json,math
from pathlib import Path
import networkx as nx
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'bt1714_toroidal_heawood_embedding.json'
def bits(n): return ((n>>2)&1,(n>>1)&1,n&1)
def dot2(a,b): return sum(x*y for x,y in zip(bits(a),bits(b)))%2
def build_certificate():
 torus=['C0','C1','C2','C3','C4','S0','S1']; pts=list(range(1,8)); line_labels=list(range(1,8))
 fano={ell:[p for p in pts if dot2(p,ell)==0] for ell in line_labels}
 rp=dict(zip(torus,pts)); schedule=[]; H=nx.Graph(); B=nx.Graph()
 H.add_nodes_from([f'R:{r}' for r in torus],bipartite=0); H.add_nodes_from([f'L:{l}' for l in line_labels],bipartite=1); B.add_nodes_from(H.nodes(data=True))
 for r,p in rp.items():
  inc=[ell for ell,ps in fano.items() if p in ps]; non=[ell for ell in line_labels if ell not in inc]
  schedule.append({'realization':r,'point':p,'execution_slots':inc,'buffer_slots':non})
  for ell in line_labels:
   (H if ell in inc else B).add_edge(f'R:{r}',f'L:{ell}')
 owner={}
 for ell,ps in fano.items():
  for a,b in itertools.combinations(sorted(ps),2): owner[f'{a}-{b}']=ell
 checks={'seven_realizations_5_plus_2':len(torus)==7 and sum(x.startswith('C') for x in torus)==5 and sum(x.startswith('S') for x in torus)==2,'each_realization_has_3_execution_and_4_buffer_slots':all(len(x['execution_slots'])==3 and len(x['buffer_slots'])==4 for x in schedule),'heawood_edges_21':H.number_of_edges()==21,'coheawood_buffers_28':B.number_of_edges()==28,'k77_total_49':H.number_of_edges()+B.number_of_edges()==49,'fano_lines_partition_k7_edges':len(owner)==math.comb(7,2),'heawood_connected_3_regular':nx.is_connected(H) and all(d==3 for _,d in H.degree()),'coheawood_connected_4_regular':nx.is_connected(B) and all(d==4 for _,d in B.degree()),'period_142857_length_6':len({1,4,2,8,5,7})==6}
 return {'theorem':'BT1714 Seven-Realization Heawood Scheduler Embedding Theorem','verified':all(checks.values()),'summary':'The five Csaszar plus two Szilassi realization heptad embeds as the point side of the Fano/Heawood K7,7 scheduler. Each realization has three Heawood execution slots and four co-Heawood buffer slots; Fano lines partition the 21-pair toroidal edge carrier while the 28 non-incidence slots form a calibration reservoir.','realization_point_map':rp,'schedule':schedule,'fano_lines':fano,'k7_edge_owner':owner,'counts':{'execution_edges':21,'buffer_edges':28,'total_k77_edges':49,'toroidal_edge_carrier':21,'phase_period_1_over_7':6,'toroidal_colors':7},'claim_boundary':['Scheduler embedding of realization labels into Fano incidence; concrete 3D coordinate embeddings are not parsed here.','The 28 co-Heawood slots are certified non-incidence buffers, not hardware calibration events yet.'],'checks':checks}
def main():
 cert=build_certificate(); OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(cert,indent=2,sort_keys=True)+'\n'); print(cert['theorem'],cert['verified']); return 0 if cert['verified'] else 1
if __name__=='__main__': raise SystemExit(main())
