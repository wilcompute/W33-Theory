#!/usr/bin/env python3
"""Passes 3997-4004 exact W33 layout, delay tomography, and edge-memory constructions."""
from __future__ import annotations
import hashlib, itertools, json, random
from collections import Counter
from pathlib import Path
import numpy as np
import networkx as nx
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_3997_4004_LAYOUT_TOMOGRAPHY_EDGE_MEMORY.json'

def sha(x): return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def norm(v):
 v=tuple(x%3 for x in v)
 for x in v:
  if x:
   inv=1 if x==1 else 2
   return tuple(inv*y%3 for y in v)
 raise ValueError
def symp(x,y): return (x[0]*y[2]+x[1]*y[3]-x[2]*y[0]-x[3]*y[1])%3

def build():
 pts=sorted({norm(v) for v in itertools.product(range(3),repeat=4) if any(v)})
 A=np.zeros((40,40),dtype=int)
 for i,x in enumerate(pts):
  for j in range(i+1,40):
   if symp(x,pts[j])==0:A[i,j]=A[j,i]=1
 I=np.eye(40,dtype=int);J=np.ones((40,40),dtype=int)
 assert np.array_equal(A@A,8*I-2*A+4*J)
 G=nx.from_numpy_array(A)
 lines=sorted(tuple(sorted(c)) for c in nx.find_cliques(G) if len(c)==4)
 assert len(lines)==40
 N=np.zeros((40,40),dtype=int)
 for j,c in enumerate(lines):N[list(c),j]=1
 assert np.array_equal(N@N.T,4*I+A)
 return A,G,N

def one_factorization_direct(G):
 H=G.copy();rng=random.Random(0);factors=[]
 for _ in range(12):
  for u,v in H.edges():H[u][v]['weight']=rng.random()
  M=nx.max_weight_matching(H,maxcardinality=True,weight='weight');assert len(M)==20
  E=sorted((min(u,v),max(u,v)) for u,v in M);factors.append(E);H.remove_edges_from(E)
 assert H.number_of_edges()==0
 return factors

def one_factorization_incidence(N):
 B=nx.Graph();B.add_nodes_from(range(80))
 for i,j in zip(*np.where(N)):B.add_edge(int(i),40+int(j))
 H=B.copy();factors=[];top=set(range(40))
 for _ in range(4):
  M=nx.algorithms.bipartite.maximum_matching(H,top_nodes=top)
  E=sorted((min(u,v),max(u,v)) for u,v in M.items() if u<v);assert len(E)==40
  factors.append(E);H.remove_edges_from(E)
 assert H.number_of_edges()==0
 return B,factors

def factor_sha(f): return sha([[[int(u),int(v)] for u,v in layer] for layer in f])
def theta(w): return .31*w+.07*w*w-.013*w*w*w
def theta_prime(w): return .31+.14*w-.039*w*w
def scattering(w,E0,E10,E16):
 t=theta(w);return E0+np.exp(1j*10*t)*E10+np.exp(1j*16*t)*E16

def main():
 A,G,N=build();direct=one_factorization_direct(G);B,incidence=one_factorization_incidence(N)
 assert Counter(int(round(x)) for x in np.linalg.eigvalsh(A.astype(float)))==Counter({12:1,2:24,-4:15})
 layout={
  'direct_40_mode':{'modes':40,'links':240,'degree':12,'perfect_matching_layers':12,'factorization_sha256':factor_sha(direct),'balanced_cut_spectral_lower_bound':100},
  'incidence_80_mode':{'modes':80,'links':160,'degree':4,'girth':nx.girth(B),'perfect_matching_layers':4,'factorization_sha256':factor_sha(incidence),'balanced_cut_spectral_lower_bound':'20*(4-sqrt(6))'},
  'linear_cost_boundary':{'direct_minus_incidence':'-40*alpha+80*beta+8*gamma','direct_preferred_iff':'5*alpha>10*beta+gamma','incidence_preferred_iff':'5*alpha<10*beta+gamma'},
  'interpretation':'The direct device minimizes modes; the incidence lift minimizes degree, links, and disjoint coupling layers. The exact phase boundary exposes which fabrication resource dominates.'}
 I40=np.eye(40);J40=np.ones((40,40));L=12*I40-A
 E0=J40/40;E10=(4*I40+A)/6-J40/15;E16=I40-E0-E10
 assert np.allclose(E10@E10,E10) and np.allclose(E16@E16,E16)
 w0=.4;qp=theta_prime(w0);Q=qp*L;hs=[.1,.05,.025,.0125];errs=[];S0=scattering(w0,E0,E10,E16)
 for h in hs:
  dS=(scattering(w0+h,E0,E10,E16)-scattering(w0-h,E0,E10,E16))/(2*h)
  Qe=-1j*S0.conj().T@dS;Qe=(Qe+Qe.conj().T)/2
  errs.append(float(np.linalg.norm(Qe-Q)/np.linalg.norm(Q)))
 ratios=[errs[i]/errs[i+1] for i in range(len(errs)-1)];assert all(3.8<r<4.2 for r in ratios)
 p=np.array([.17,.51,.32]);m1=10*p[1]+16*p[2];m2=100*p[1]+256*p[2]
 rec=np.array([1-(16*m1-m2)/60-(m2-10*m1)/96,(16*m1-m2)/60,(m2-10*m1)/96]);assert np.allclose(p,rec)
 Qc=Q-np.trace(Q)/40*I40;assert np.allclose(Qc,-qp*A)
 recovered=np.rint(-Qc/qp).astype(int);np.fill_diagonal(recovered,0);assert np.array_equal(recovered,A)
 tomography={'operator':'Q(omega)=-i S^dagger dS/domega=theta_prime L_W33','three_sector_moment_inverse':{'p16':'(m2-10*m1)/96','p10':'(16*m1-m2)/60','p0':'1-p10-p16'},'synthetic_population':[float(x) for x in p],'recovered_population':[float(x) for x in rec],'central_difference_h':hs,'relative_frobenius_errors':errs,'successive_error_ratios':ratios,'common_delay_gauge_theorem':'Q-(Tr Q/40)I=-theta_prime A_W33','geometry_recovery':'After common-delay subtraction, thresholding the off-diagonal delay kernel reconstructs all 240 W33 edges exactly.','full_transfer_tomography_ledger':{'frequencies':3,'coherent_input_probes':40,'complex_transfer_amplitudes_per_frequency':1600,'real_scalar_data_before_gauge_reduction':9600}}
 edges=sorted((u,v) for u,v in G.edges());D=np.zeros((40,240),dtype=int)
 for e,(u,v) in enumerate(edges):D[u,e]=1;D[v,e]=-1
 K=D.T@D;assert Counter(int(round(x)) for x in np.linalg.eigvalsh(K.astype(float)))==Counter({0:201,10:24,16:15})
 edge_memory={'modes':240,'oriented_incidence_rank':39,'dark_cycle_dimension':201,'generator_spectrum':{'0':201,'10':24,'16':15},'exact_half_flight':'exp(-i*pi*D^T D/2)=I-2E_10','boundary':'The 201-dimensional kernel is the raw graph cycle space, not the previously certified 81-dimensional Hodge/CSS logical space.'}
 qfi={'localized_vertex_qfi':'48*theta_prime^2','optimal_0_16_cat_qfi':'256*theta_prime^2','cramer_rao':'delta_omega >= 1/sqrt(nu*F_Q)','proof':'For a pure probe F_Q=4 Var(Q); a vertex has Laplacian moments 12 and 156, while the spectral diameter is 16.'}
 payload={'schema':'w33.pass3997_4004.layout_tomography_edge_memory.v1','status':'PASS_EXACT_LAYOUT_TOMOGRAPHY_AND_THREE_PHOTON_CONSTRUCTIONS','layout_competition':layout,'wigner_smith_tomography':tomography,'bonkers_centered_delay_geometry':{'identity':'Q_centered=-theta_prime A_W33','spectrum_in_units_theta_prime':{'-12':1,'-2':24,'4':15}},'bonkers_edge_carrier_memory':edge_memory,'bonkers_delay_metrology':qfi,'boundary':'Exact finite graph, matrix, scheduling, synthetic noiseless tomography, and QFI statements. No fabricated layout, measured delay, device loss model, variable vacuum c, or laboratory sensitivity is claimed.'}
 payload['semantic_sha256']=sha(payload);OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(payload,indent=2,sort_keys=True)+'\n')
 print('PASS_LAYOUT_TOMOGRAPHY_EDGE_MEMORY',payload['semantic_sha256'])
if __name__=='__main__':main()
