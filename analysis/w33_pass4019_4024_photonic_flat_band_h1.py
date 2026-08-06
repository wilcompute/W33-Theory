#!/usr/bin/env python3
"""Passes 4019-4024: photonic line-graph flat band from W33 Levi H1.

The 160 incidence links become the 160 sites of the Levi line graph X.  The
oriented boundary identity D^T D=A_X+2I makes the protected H1=81 cycle space
exactly the -2 flat band.  The 1620 Levi apartments give compact localized
8-link states spanning this band as a unit-norm tight frame of redundancy 20.
"""
from __future__ import annotations
import hashlib,itertools,json
from pathlib import Path
import networkx as nx
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_4019_4024_PHOTONIC_FLAT_BAND_H1.json'
MOD=3

def sha(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def norm(v):
 v=tuple(x%MOD for x in v)
 for a in v:
  if a:return tuple((1 if a==1 else 2)*x%MOD for x in v)
 raise ValueError
def sp(u,v):return (u[0]*v[2]+u[1]*v[3]-u[2]*v[0]-u[3]*v[1])%MOD

def build():
 pts=sorted({norm(v) for v in itertools.product(range(3),repeat=4) if any(v)})
 W=nx.Graph();W.add_nodes_from(range(40))
 for i,u in enumerate(pts):
  for j in range(i+1,40):
   if sp(u,pts[j])==0:W.add_edge(i,j)
 lines=sorted(tuple(sorted(c)) for c in nx.find_cliques(W) if len(c)==4);assert len(lines)==40
 L=nx.Graph();L.add_nodes_from(range(80))
 for j,line in enumerate(lines):
  for p in line:L.add_edge(p,40+j)
 edges=sorted(tuple(sorted(e)) for e in L.edges());idx={e:i for i,e in enumerate(edges)}
 D=np.zeros((80,160),dtype=np.int64)
 for j,(p,l) in enumerate(edges):D[p,j]=-1;D[l,j]=1
 X=nx.line_graph(L);AX=nx.to_numpy_array(X,nodelist=edges,dtype=np.int64)
 assert np.array_equal(D.T@D,AX+2*np.eye(160,dtype=np.int64))
 return W,L,edges,idx,D,AX

def canon_cycle(path):
 out=[]
 for seq in (path,list(reversed(path))):
  for i in range(len(seq)):out.append(tuple(seq[i:]+seq[:i]))
 return min(out)
def cycles_k(G,k):
 cycles=set()
 for start in G.nodes():
  stack=[(start,[start],{start})]
  while stack:
   u,path,seen=stack.pop()
   if len(path)==k:
    if G.has_edge(u,start):cycles.add(canon_cycle(path))
    continue
   for w in G.neighbors(u):
    if w!=start and w not in seen:stack.append((w,path+[w],seen|{w}))
 return sorted(cycles)

def main():
 W,L,edges,idx,D,AX=build();cycles=cycles_k(L,8);assert len(cycles)==1620
 C=np.zeros((160,1620),dtype=np.int64)
 for j,cyc in enumerate(cycles):
  for a,b in zip(cyc,cyc[1:]+cyc[:1]):
   e=tuple(sorted((a,b)));p,l=e;C[idx[e],j]=1 if (a,b)==(p,l) else -1
 assert np.array_equal(D@C,np.zeros((80,1620),dtype=np.int64))
 assert np.array_equal(AX@C,-2*C)
 rank=int(np.linalg.matrix_rank(C.astype(float)));assert rank==81
 Pn=C@C.T
 assert np.array_equal(Pn@Pn,160*Pn) and np.linalg.matrix_rank(Pn)==81
 assert set(np.diag(Pn))=={81}
 assert set(np.sum(C.astype(np.int64)**2,axis=0))=={8}
 assert np.array_equal(Pn@C,160*C)
 occupancy=np.sum(C!=0,axis=1);assert set(occupancy)=={81}
 spec=np.linalg.eigvalsh(AX.astype(float));spectrum={'-2':int(np.sum(np.isclose(spec,-2))),'2-sqrt(6)':int(np.sum(np.isclose(spec,2-np.sqrt(6)))),'2':int(np.sum(np.isclose(spec,2))),'2+sqrt(6)':int(np.sum(np.isclose(spec,2+np.sqrt(6)))),'6':int(np.sum(np.isclose(spec,6)))}
 assert spectrum=={'-2':81,'2-sqrt(6)':24,'2':30,'2+sqrt(6)':24,'6':1}
 I=np.eye(160,dtype=np.int64)
 poly=((AX-6*I)@(AX-2*I)@(AX@AX-4*AX-2*I))//2
 assert np.array_equal(poly,Pn)
 e0=np.zeros((160,160),dtype=np.int64);e0[0,0]=1
 local_num=Pn@e0@Pn
 assert np.linalg.matrix_rank(local_num)==1
 assert int(round(np.trace(local_num)))==81*160
 weights=np.arange(-80,80,dtype=np.int64);V=np.diag(weights)
 assert int(np.trace(Pn@V))==81*int(weights.sum())
 checks={'w33_40_240':W.number_of_nodes()==40 and W.number_of_edges()==240,'levi_80_160_degree4':L.number_of_nodes()==80 and L.number_of_edges()==160 and set(dict(L.degree()).values())=={4},'line_graph_160_480_degree6':AX.shape==(160,160) and int(AX.sum()//2)==480 and set(AX.sum(axis=1))=={6},'oriented_incidence_identity':np.array_equal(D.T@D,AX+2*I),'minus2_flat_band_rank81':spectrum['-2']==81 and rank==81,'apartments_1620':len(cycles)==1620,'apartments_are_compact_flat_states':np.array_equal(AX@C,-2*C) and set(np.sum(C.astype(np.int64)**2,axis=0))=={8},'apartments_span_flat_band':rank==81,'tight_frame_integer_identity':np.array_equal(Pn@C,160*C),'each_site_in_81_apartments':set(occupancy)=={81},'incidence_balance_12960':160*81==1620*8,'projector_polynomial_exact':np.array_equal(poly,Pn),'uniform_shift_preserves_flat_band':np.array_equal(Pn@I@Pn,160*Pn),'single_site_disorder_splits_rank1':np.linalg.matrix_rank(local_num)==1 and int(round(np.trace(local_num)))==81*160,'diagonal_disorder_trace_law':int(np.trace(Pn@V))==81*int(weights.sum())};checks={k:bool(v) for k,v in checks.items()};assert all(checks.values())
 x={'schema':'w33.pass4019_4024.photonic_flat_band_h1.v1','status':'PASS_EXACT_PHOTONIC_LINE_GRAPH_FLAT_BAND_H1','pass4019_coupler_as_site_line_graph':{'secondary_sites':160,'secondary_links':480,'degree':6,'identity':'A_X=D^T D-2I','spectrum':spectrum,'resource_boundary':'This secondary site Hamiltonian is not the same object as the primary 80-mode incidence Hamiltonian or passive link-current coordinates.'},'pass4020_h1_is_minus2_flat_band':{'flat_band_eigenvalue':-2,'multiplicity':81,'identity':'ker(D)=E_{-2}(A_X)','projector':'P_H1=(1/160) C C^T','integer_polynomial':'C C^T=1/2(A_X-6I)(A_X-2I)(A_X^2-4A_X-2I)'},'pass4021_apartment_compact_localized_states':{'apartments':1620,'support_per_state':8,'amplitudes':'alternating +/-1 around each Levi octagon','eigen_equation':'A_X c=-2c','span_rank':81,'reading':'Every Tits-building apartment supplies a compact flat-band state; all apartments together span the complete H1 band.'},'pass4022_apartment_unit_norm_tight_frame':{'unit_vectors':1620,'ambient_flat_band_dimension':81,'frame_bound':20,'redundancy':20,'integer_identity':'(C C^T) C=160 C','normalization':'columns have norm sqrt(8), so (C/sqrt(8))(C/sqrt(8))^T=20 P_H1'},'pass4023_local_address_law':{'apartments_per_secondary_site':81,'links_per_apartment':8,'double_count':'160*81=1620*8=12960','interpretation':'Each physical incidence-link address participates in exactly 81 compact apartment states.'},'pass4024_perturbation_boundary':{'uniform_onsite_shift':'delta I shifts the whole flat band rigidly and does not split it','single_site_onsite_perturbation':'P_H1 |e><e| P_H1 has rank 1 and nonzero eigenvalue 81/160','general_diagonal_trace_law':'Tr(P_H1 diag(v))=(81/160) sum_e v_e','honest_boundary':'The H1 flat band is exact in the symmetric Hamiltonian but is not generically immune to nonuniform onsite or coupling disorder.'},'external_context':{'flat_band_photonics':'Photonic flat bands and compact localized states are established consequences of destructive interference; the new repo result is the exact W33/Levi realization and its 1620-state H1 tight frame.','reviewed_sources':['Real et al., Scientific Reports 7, 15085 (2017)','Xia et al., arXiv:1810.12618','Yang et al., Nature Communications 15, 1484 (2024)']},'boundaries':['Exact finite graph, line-graph, eigenspace, cycle-frame, and first-order projected perturbation statements only.','No fabricated 160-site secondary lattice, measured localization, disorder tolerance, coupling synthesis, variable vacuum c, or laboratory performance is claimed.','The 160-site line-graph Hamiltonian, 80-mode incidence Hamiltonian, and 160-dimensional link-current space are related but distinct physical models.'],'checks':checks};x['semantic_sha256']=sha(x);OUT.write_text(json.dumps(x,indent=2,sort_keys=True)+'\n');print('PASS_4019_4024_PHOTONIC_FLAT_BAND_H1',x['semantic_sha256']);return x
if __name__=='__main__':main()
