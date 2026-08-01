#!/usr/bin/env python3
"""Passes 1902--1903: exact U6 obstruction ledger and mixed-enumerator tensor reduction."""
from __future__ import annotations
import hashlib,itertools,json,math
from collections import Counter
from pathlib import Path
import networkx as nx
import numpy as np
ROOT=Path(__file__).resolve().parents[1];ROWS=ROOT/'data/w33_pass1876_rows45_hex.txt';DATA=ROOT/'data'
def canon(d):
 x=dict(d);x.pop('sha256_without_hash_field',None)
 return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':'),default=lambda o:bool(o) if isinstance(o,np.bool_) else int(o)).encode()).hexdigest()
def pass1902():
 A={4:540,6:9600,8:424170,10:17523360,12:891792940}
 terms={str(w):A[w]*math.comb(w,w//2)*math.comb(240-w,6-w//2)//2 for w in A}
 total=math.comb(240,6);edges=sum(terms.values());fixed12=A[12]*12//240;miss=fixed12*math.comb(11,5)
 checks={'total_weight6':total==249219381880,'collision_terms_sum':edges==1724138884380,'weight12_disjoint_edges':terms['12']==412008338280,'fixed_weight12_codewords':fixed12==44589647,'fixed_disjoint_incidence':miss==20600416914,'chart_visibility_formula':all(6-w//2>=0 for w in A)}
 out={'schema':'w33.pass1902.u6_component_reduction.v1','status':'PASS_WITH_GLOBAL_COMPONENT_BOUNDARY','checks':checks,'total_weight6_errors':total,'fixed_coordinate_weight6_errors':math.comb(239,5),'primal_coefficients':{str(k):v for k,v in A.items()},'equal_syndrome_collision_edges_by_difference_weight':terms,'equal_syndrome_collision_edges_total':edges,'chart_appearance_count_by_difference_weight':{str(w):6-w//2 for w in A},'weight12_disjoint_edges_invisible_to_every_coordinate_chart':terms['12'],'weight12_codewords_through_fixed_coordinate':fixed12,'fixed_coordinate_disjoint_partner_incidence_with_multiplicity':miss,'required_exact_pipeline':['sort all weight-six syndromes in one fixed-coordinate chart','remove weight-0/2/4 lower shadows','enumerate all weight-4/6/8/10/12 connecting codewords through the fixed coordinate','mark external partners, including 20,600,416,914 weight-12 incidences with multiplicity','deduplicate syndrome components before multiplying by 240/6=40'],'theorem':'The weight-six collision ledger is completely resolved by difference weight. The new terminal obstruction is the weight-12 shell: 412,008,338,280 disjoint collision edges, contributing 20,600,416,914 fixed-coordinate external-partner incidences with multiplicity, are invisible to every fixed-coordinate chart. The supplied external-memory workers are therefore necessary for U6; collision moments cannot close it.','boundary':'U6 itself is not claimed. The exact singleton-component count requires completion of the supplied chart sort and external-partner deduplication.'}
 assert all(checks.values());out['sha256_without_hash_field']=canon(out);return out
def read_rows():
 out=[]
 for line in ROWS.read_text().splitlines():
  z=[int(x,16) for x in line.split()];out.append(sum(x<<(64*i) for i,x in enumerate(z)))
 assert len(out)==45;return out
def pass1903():
 rows=read_rows();pair=[];phase=[];res=[];prof=Counter()
 for e in range(240):
  fs=[i for i in range(30) if rows[i]>>e&1];rs=[i-30 for i in range(30,45) if rows[i]>>e&1];prof[(len(fs),len(rs))]+=1
  if (len(fs),len(rs))==(2,1):pair.append((e,fs,rs[0]))
  elif (len(fs),len(rs))==(3,0):phase.append((e,fs))
  elif (len(fs),len(rs))==(0,3):res.append((e,rs))
  else:raise AssertionError((e,fs,rs))
 fps=list(itertools.combinations(range(6),2));fi={p:i for i,p in enumerate(fps)};M=np.zeros((15,15),dtype=np.int64)
 for _,fs,r in pair:M[fi[tuple(sorted((fs[0]//5,fs[1]//5)))],r]+=1
 Z=nx.Graph();Z.add_nodes_from(range(30))
 for i in range(15):
  for j in range(15):
   if M[i,j]==0:Z.add_edge(i,15+j)
 phase_mult=Counter(tuple(sorted(i//5 for i in fs)) for _,fs in phase)
 H=nx.Graph();H.add_nodes_from(range(15),bip=0);H.add_nodes_from(range(15,35),bip=1)
 for k,(_,rs) in enumerate(res):
  for r in rs:H.add_edge(r,15+k)
 nm=nx.algorithms.isomorphism.categorical_node_match('bip',None);haut=sum(1 for _ in nx.algorithms.isomorphism.GraphMatcher(H,H,node_match=nm).isomorphisms_iter())
 checks={'profiles_20_180_40':prof==Counter({(0,3):20,(2,1):180,(3,0):40}),'pair_matrix_binary':set(M.ravel())=={0,1},'pair_rows_cols12':set(M.sum(0))=={12} and set(M.sum(1))=={12},'zero_graph_tutte_coxeter':Z.number_of_edges()==45 and nx.is_connected(Z) and nx.girth(Z)==8 and nx.diameter(Z)==4,'phase_every_triple_twice':len(phase_mult)==20 and set(phase_mult.values())=={2},'residual_hypergraph_aut720':haut==720,'factor_count240':len(pair)+len(phase)+len(res)==240}
 out={'schema':'w33.pass1903.mixed_separator_tensor_reduction.v1','status':'PASS_WITH_EXHAUSTIVE_CONTRACTION_BOUNDARY','checks':checks,'variables':{'fiber_blocks':6,'bits_per_fiber_block':5,'residual_bits':15,'total_dimension':45},'coordinate_factors':{'residual_triples':20,'pair_factors':180,'phase_triples':40},'pair_factor_structure':'Each of the 15 fiber-block pairs has 12 coordinates, using 12 distinct residual variables. Each residual variable appears in 12 pair coordinates. The 45 absent pair-residual incidences form the cubic girth-8 Tutte-Coxeter graph.','phase_factor_structure':'Every 3-subset of the six fiber blocks occurs exactly twice among the 40 phase factors.','residual_factor_structure':'The 20 residual parity triples form the triangle hypergraph of K6 on its 15 duads; its color-preserving automorphism group has order 720.','exact_tensor_network':'Sum over six 32-state fiber variables and fifteen binary residual variables of 20 residual, 180 pair, and 40 phase parity monomials. This is the exact full trivariate enumerator; no marginal independence is used.','coordinate_profile_matrix':{'zeros':45,'ones':180,'row_sum':12,'column_sum':12},'theorem':'The unresolved 2^45 mixed enumerator is now reduced to a canonical finite tensor network controlled by the same Tutte-Coxeter complement as the voltage lift. The 180 pair coordinates are the ones of a 15x15 complement-incidence matrix, the 45 zeros are the Tutte-Coxeter edges, and the remaining factors are the complete 20-triple hypergraphs on the six separator blocks.','boundary':'The exact tensor network and chunkable exhaustive worker are closed. The final 155,841-bin contraction is not claimed until all 156 residual orbit chunks are run and merged.'}
 assert all(checks.values());out['sha256_without_hash_field']=canon(out);return out
def main():
 DATA.mkdir(exist_ok=True);a,b=pass1902(),pass1903();(DATA/'w33_pass1902_u6_component_reduction.json').write_text(json.dumps(a,sort_keys=True,separators=(',',':'))+'\n');(DATA/'w33_pass1903_mixed_separator_tensor_reduction.json').write_text(json.dumps(b,sort_keys=True,separators=(',',':'))+'\n');print(json.dumps({'1902':{'status':a['status'],'sha256':a['sha256_without_hash_field']},'1903':{'status':b['status'],'sha256':b['sha256_without_hash_field']}},indent=2))
if __name__=='__main__':main()
