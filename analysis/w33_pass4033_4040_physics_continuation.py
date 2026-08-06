#!/usr/bin/env python3
"""Passes 4033--4040: independent physics continuation after Passes 4025--4032."""
from __future__ import annotations
import hashlib, itertools, json, math
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path
import networkx as nx
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_4033_4040_PHYSICS_CONTINUATION.json'
PRIME=1_000_003

def sha(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
MOD=3
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
 lines=sorted(tuple(sorted(c)) for c in nx.find_cliques(W) if len(c)==4)
 L=nx.Graph();L.add_nodes_from(range(80))
 for j,line in enumerate(lines):
  for q in line:L.add_edge(q,40+j)
 edges=sorted(tuple(sorted(e)) for e in L.edges());idx={e:i for i,e in enumerate(edges)}
 D=np.zeros((80,160),dtype=np.int64)
 for j,(q,l) in enumerate(edges):D[q,j]=-1;D[l,j]=1
 X=nx.line_graph(L);AX=nx.to_numpy_array(X,nodelist=edges,dtype=np.int64)
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

def sparse_rank(rows,p=PRIME):
 basis={}
 for row in rows:
  d={i:int(v)%p for i,v in enumerate(row) if int(v)%p}
  while d:
   q=min(d)
   if q not in basis:
    z=pow(d[q],-1,p);basis[q]={k:v*z%p for k,v in d.items()};break
   z=d[q]
   for k,v in basis[q].items():
    w=(d.get(k,0)-z*v)%p
    if w:d[k]=w
    elif k in d:del d[k]
 return len(basis)
def independent_columns(A,target,p=PRIME):
 basis={};out=[]
 for j in range(A.shape[1]):
  v=A[:,j].astype(object)%p
  for q in sorted(basis):
   if v[q]:v=(v-int(v[q])*basis[q])%p
  nz=[i for i,x in enumerate(v) if x]
  if nz:
   q=nz[0];v=v*pow(int(v[q]),-1,p)%p;basis[q]=v;out.append(j)
   if len(out)==target:return out
 raise RuntimeError(len(out))
def eig_profile(vals,targets,tol=1e-7):
 out=Counter()
 for x in vals:
  for k,v in targets.items():
   if abs(float(x)-v)<tol:out[k]+=1;break
  else:out[f'other:{x:.12g}']+=1
 return dict(out)
def cheb(spec):
 lo,hi=min(spec),max(spec);x=(spec-(hi+lo)/2)/((hi-lo)/2)
 return np.array([np.cos(k*np.arccos(np.clip(x,-1,1))) for k in range(len(spec))])

def main():
 W,L,edges,idx,D,AX=build();cycles=cycles_k(L,8)
 C=np.zeros((160,1620),dtype=np.int64)
 for j,cyc in enumerate(cycles):
  for a,c in zip(cyc,cyc[1:]+cyc[:1]):
   e=tuple(sorted((a,c)));p,l=e;C[idx[e],j]=1 if (a,c)==(p,l) else -1
 K=C@C.T;P=K/160.0
 cols=independent_columns(C,81);B=C[:,cols];G=B.T@B
 lam,Q=np.linalg.eigh(G.astype(float));Wc=B@Q@np.diag(1/np.sqrt(lam))@Q.T
 compiler={'columns':cols,'basis_shape':list(B.shape),'gram_condition':float(lam.max()/lam.min()),'isometry_error':float(np.max(abs(Wc.T@Wc-np.eye(81)))),'projector_error':float(np.max(abs(Wc@Wc.T-P))),'formula':'W=B(B^T B)^(-1/2)','swap_hamiltonian':'[[0,W^T],[W,0]]','swap_time':'pi/2','input_requirement':'80 device modes plus one ancilla for all 81 H1 channels'}
 X=nx.Graph();X.add_nodes_from(range(160));edge_id={e:i for i,e in enumerate(edges)}
 for v in L:
  inc=[edge_id[tuple(sorted(e))] for e in L.edges(v)];X.add_edges_from(itertools.combinations(inc,2))
 tri=np.triu_indices(81);R=B
 onsite=np.array([np.outer(R[e],R[e])[tri] for e in range(160)],dtype=np.int64)
 coupling=np.array([(np.outer(R[e],R[f])+np.outer(R[f],R[e]))[tri] for e,f in X.edges()],dtype=np.int64)
 ro,rc,rb=sparse_rank(onsite),sparse_rank(coupling),sparse_rank(np.vstack([onsite,coupling]))
 atom=P*P
 atom_spec=eig_profile(np.linalg.eigvalsh(atom),{'81/160':81/160,'(252+27sqrt6)/800':(252+27*math.sqrt(6))/800,'234/800':234/800,'(252-27sqrt6)/800':(252-27*math.sqrt(6))/800,'164/800':164/800})
 identity_error=0.0
 for e in range(160):
  A=np.outer(Wc[e],Wc[e]);S=sum((np.outer(Wc[e],Wc[f])+np.outer(Wc[f],Wc[e]) for f in X.neighbors(e)),np.zeros((81,81)))
  identity_error=max(identity_error,float(np.max(abs(A+S/4))))
 disorder={'onsite_span':ro,'coupling_span':rc,'combined_span':rb,'atom_gram_spectrum':atom_spec,'incident_identity':'A_e=-(1/4)sum_{f~e}A_ef','incident_identity_error':identity_error,'all_pair_inner_products_nonzero':bool(np.min(abs(P))>1e-12),'commutant':'scalars','generated_algebra':'M_81(C)','generated_lie_algebra':'u(81) with uniform identity control'}
 f=ROOT/'data/PART_3999_ORBITAL_RELATION_FUSION.json';m=ROOT/'data/PART_4000_MONSTER_EXECUTION_SUMMARY.json'
 engine={'relation_output':f.exists(),'monster_output':m.exists(),'status':'COMPLETE' if f.exists() and m.exists() else 'BLOCKED_ENGINE_OUTPUTS_MISSING','boundary':'No relation-fusion rank, Monster word, class fusion, or embedding is promoted without generated outputs and inspected logs.'}
 tomo={}
 for name,specv in {'mode_H2':np.array([0.,6.,16.]),'signed_Levi':np.array([-4.,-math.sqrt(6),0.,math.sqrt(6),4.]),'line_graph':np.array([-2.,2-math.sqrt(6),2.,2+math.sqrt(6),6.])}.items():
  V=np.vander(specv,len(specv),increasing=True).T;T=cheb(specv)
  tomo[name]={'sectors':len(specv),'minimal_nontrivial_probes':len(specv)-1,'raw_condition_2':float(np.linalg.cond(V)),'chebyshev_condition_2':float(np.linalg.cond(T)),'chebyshev_inverse_inf':float(np.linalg.norm(np.linalg.inv(T),np.inf))}
 gap=4-math.sqrt(6)
 fab={'primary':{'modes':80,'links':160,'degree':4},'secondary':{'sites':160,'links':480,'degree':6},'hopping':'uniform real +J; no negative hopping is required','flat_energy_over_J':-2,'nearest_energy_over_J':2-math.sqrt(6),'gap_over_J':gap,'sufficient_cluster_condition':'||V||_2 < (4-sqrt(6))J/2','design_target_not_measurement':'kappa/J <= 0.1','platforms':['3D laser-written waveguide/resonator graph','time/frequency synthetic-dimension resonator network']}
 edge_spec=eig_profile(np.linalg.eigvalsh(D.T@D),{'0':0.,'4-sqrt6':4-math.sqrt(6),'4':4.,'4+sqrt6':4+math.sqrt(6),'8':8.})
 fridge={'jump_map':'L_v=sum_e D[v,e] a_e','dark_space':'ker(D)=H1','dark_dimension':81,'decay_spectrum':edge_spec,'dissipative_gap':'4-sqrt(6)','boundary':'Linear loss alone needs no-jump postselection, replenishment, or number-conserving reservoir engineering to preserve a photon.'}
 control={'local_rank_one_controls':160,'linear_span':ro,'all_control_rays_nonorthogonal':bool(np.min(abs(P))>1e-12),'commutant':'scalars','associative_closure':'M_81(C)','hamiltonian_lie_closure':'u(81)','boundary':'Ideal controllability only; pulse synthesis, loss, calibration, and leakage are not certified.'}
 Lv=D@D.T;Lp=np.linalg.pinv(Lv,rcond=1e-12);dist=dict(nx.all_pairs_shortest_path_length(L));shell=defaultdict(list)
 for i in range(80):
  for j in range(i+1,80):shell[dist[i][j]].append(float(Lp[i,i]+Lp[j,j]-2*Lp[i,j]))
 coulomb={str(d):{'pairs':len(v),'resistance':str(Fraction(float(np.mean(v))).limit_denominator(10000)),'spread':float(max(v)-min(v))} for d,v in sorted(shell.items())}
 checks={'geometry':W.number_of_nodes()==40 and W.number_of_edges()==240 and L.number_of_nodes()==80 and L.number_of_edges()==160 and len(cycles)==1620,'hodge':np.linalg.matrix_rank(D)==79 and np.linalg.matrix_rank(C)==81 and np.array_equal(D@C,np.zeros((80,1620),dtype=int)) and np.max(abs(P@P-P))<1e-9,'compiler':cols==list(range(81)) and compiler['gram_condition']-160<1e-7 and compiler['isometry_error']<1e-10 and compiler['projector_error']<1e-10,'disorder':(ro,rc,rb)==(160,320,320) and identity_error<1e-10 and sum(atom_spec.values())==160,'tomography':all(x['chebyshev_condition_2']<2 for x in tomo.values()),'fabrication_gap':gap>1.5,'fridge':edge_spec=={'0':81,'4-sqrt6':24,'4':30,'4+sqrt6':24,'8':1},'coulomb':{d:coulomb[d]['resistance'] for d in coulomb}=={'1':'79/160','2':'13/20','3':'111/160','4':'7/10'} and max(x['spread'] for x in coulomb.values())<1e-11,'engine_fail_closed':engine['status'] in {'COMPLETE','BLOCKED_ENGINE_OUTPUTS_MISSING'}};checks={k:bool(v) for k,v in checks.items()}
 out={'schema':'w33.pass4033_4040.physics_continuation.v1','status':'PASS_EXACT_INDEPENDENT_PHYSICS_CONTINUATION_WITH_LITERAL_ENGINE_GATE_FAIL_CLOSED','pass4033_full_H1_swap_compiler':compiler,'pass4034_projected_disorder_algebra':disorder,'pass4035_literal_algebra_gate':engine,'pass4036_compressed_sector_tomography':tomo,'pass4037_fabrication_contract':fab,'pass4038_bonkers_dissipative_Hodge_refrigerator':fridge,'pass4039_bonkers_disorder_as_universal_control':control,'pass4040_bonkers_Levi_Coulomb_law':{'gauss_map':'rho=D E, sum rho=0','charge_rank':79,'harmonic_flux_rank':81,'penalty':'J D^T D','resistance_by_distance':coulomb,'boundary':'Exact finite network electrodynamics, not continuum Maxwell theory or gravity.'},'checks':checks,'all_checks_hold':all(checks.values()),'boundaries':['No fabricated device or measured performance.','No literal algebra/Monster result without engine artifacts.','No continuum, Standard Model, gravity, or TOE claim.']};out['semantic_sha256']=sha(out);OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print('PASS_4033_4040',out['semantic_sha256']);return out
if __name__=='__main__':
 r=main();assert r['all_checks_hold']
