#!/usr/bin/env python3
"""Pass 2968: exact [45,9,9]_2 curvature route code."""
from __future__ import annotations
import collections,itertools,json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'data/PART_BT2968_CURVATURE_ROUTE_CODE_results.json'
V=tuple(range(10));E=list(itertools.combinations(V,2));T=list(itertools.combinations(V,3));Q=list(itertools.combinations(V,4));EI={e:i for i,e in enumerate(E)};TI={t:i for i,t in enumerate(T)}
def rref(m):
 a=np.asarray(m,dtype=np.uint8).copy()%2;rows,cols=a.shape;p=[];r=0
 for c in range(cols):
  q=next((i for i in range(r,rows) if a[i,c]),None)
  if q is None:continue
  a[[r,q]]=a[[q,r]]
  for i in range(rows):
   if i!=r and a[i,c]:a[i]^=a[r]
  p.append(c);r+=1
  if r==rows:break
 return a,p
def rank(m):return len(rref(m)[1])
H=np.zeros((120,45),dtype=np.uint8)
for i,t in enumerate(T):
 for e in itertools.combinations(t,2):H[i,EI[tuple(sorted(e))]]=1
B=np.zeros((210,120),dtype=np.uint8)
for i,q in enumerate(Q):
 for f in itertools.combinations(q,3):B[i,TI[tuple(sorted(f))]]=1
def cut(s):
 s=set(s);return np.array([int((u in s)^(v in s)) for u,v in E],dtype=np.uint8)
def key(v):return bytes(np.packbits(v))
def main():
 rh=rank(H);assert rh==36 and np.count_nonzero((B@H)%2)==0
 cuts={}
 for mask in range(1<<10):
  v=cut([i for i in V if mask>>i&1]);cuts[key(v)]=v
 assert len(cuts)==512 and all(np.count_nonzero((H@v)%2)==0 for v in cuts.values()) and 45-rh==9
 weights=collections.Counter(int(np.count_nonzero(v)) for v in cuts.values());assert dict(sorted(weights.items()))=={0:1,9:10,16:45,21:120,24:210,25:126};d=9
 _,piv=rref(H.T);H36=H[piv];assert len(piv)==rank(H36)==36
 cw=[int(np.count_nonzero(H[:,j])) for j in range(45)];assert set(cw)=={8} and len({key(H[:,j]) for j in range(45)})==45
 pw=collections.Counter(int(np.count_nonzero(H[:,a]^H[:,b])) for a,b in itertools.combinations(range(45),2));assert pw==collections.Counter({14:360,16:630})
 checks={'triangle_edge_matrix_shape_120x45':H.shape==(120,45),'triangle_coboundary_rank_36':rh==36,'kernel_dimension_9':45-rh==9,'kernel_equals_512_vertex_switching_cuts':len(cuts)==512,'cut_code_parameters_45_9_9':d==9,'tetrahedral_bianchi_BH_zero':np.count_nonzero((B@H)%2)==0,'all_single_edge_faults_have_unique_weight8_syndromes':set(cw)=={8} and len({key(H[:,j]) for j in range(45)})==45,'all_weight_at_most_8_nongauge_faults_detected':d==9,'all_weight_at_most_4_faults_correctable_modulo_gauge':d>=9,'36_independent_triangle_checks_suffice':rank(H36)==36};assert all(checks.values())
 result={'schema':'w33.pass2968.curvature_route_code.v1','status':'COMPLETE_EXACT_BINARY_GAUGE_CODE','checks':{k:bool(v) for k,v in checks.items()},'check_count':10,'raw_registers':{'spread_modes':10,'transport_edges':45,'triangle_curvature_checks':120,'independent_syndrome_bits':36,'tetrahedral_bianchi_relations':210},'code':{'kernel':'vertex-switching cut space of K10','parameters':'[45,9,9]_2','weight_enumerator':{str(k):v for k,v in sorted(weights.items())},'minimum_undetectable_weight':9,'correctable_fault_weight_modulo_gauge':4,'detectable_nongauge_fault_weight':8},'syndromes':{'single_edge_syndrome_weight':8,'single_edge_syndromes_unique':True,'two_edge_syndrome_weight_histogram':{str(k):v for k,v in sorted(pw.items())},'independent_triangle_indices':[int(i) for i in piv]},'decoder_statement':'Subtract the Pass-2967 baseline and decode H e to a minimum-weight edge-fault coset.','headline':'The spread router parity curvature is an exact [45,9,9]_2 gauge code with 36 independent checks and correction through four odd faults modulo gauge.','claim_boundary':'Parity only: even S4 errors, loss, drift and detector faults require the pilot/channel layers.'}
 OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print('PASS 10 / 10',result['headline'])
if __name__=='__main__':main()
