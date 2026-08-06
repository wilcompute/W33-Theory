#!/usr/bin/env python3
"""Passes 4013-4018: exact W33 incidence-link H1 memory bridge.

This verifier reconciles the 80-mode point-line incidence dynamics with the
160-link Levi Hodge theorem.  Its central result is that the same 160 physical
incidence couplers carry the protected H1=81 sector exactly as boundaryless
link-current memory.  It also verifies a distinct A_Levi^2 sign-fold revival,
signed four-moment tomography, and ideal centered-delay incidence recovery.
"""
from __future__ import annotations
import hashlib,itertools,json
from collections import Counter
from fractions import Fraction
from pathlib import Path
import networkx as nx
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_4013_4018_INCIDENCE_LINK_H1_MEMORY.json'
MOD=3

def sha(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def norm(v):
 v=tuple(x%MOD for x in v)
 for a in v:
  if a:
   inv=1 if a==1 else 2
   return tuple(inv*x%MOD for x in v)
 raise ValueError('zero vector')
def sp(u,v):return (u[0]*v[2]+u[1]*v[3]-u[2]*v[0]-u[3]*v[1])%MOD
def frac(x):return str(x.numerator) if x.denominator==1 else f'{x.numerator}/{x.denominator}'

def geometry():
 pts=sorted({norm(v) for v in itertools.product(range(MOD),repeat=4) if any(v)});assert len(pts)==40
 A=np.zeros((40,40),dtype=np.int64)
 for i,u in enumerate(pts):
  for j in range(i+1,40):
   if sp(u,pts[j])==0:A[i,j]=A[j,i]=1
 G=nx.from_numpy_array(A);lines=sorted(tuple(sorted(c)) for c in nx.find_cliques(G) if len(c)==4);assert len(lines)==40
 N=np.zeros((40,40),dtype=np.int64)
 for j,line in enumerate(lines):N[list(line),j]=1
 I=np.eye(40,dtype=np.int64);J=np.ones((40,40),dtype=np.int64)
 assert np.array_equal(A@A,8*I-2*A+4*J) and np.array_equal(N@N.T,4*I+A)
 AL=np.block([[np.zeros((40,40),dtype=np.int64),N],[N.T,np.zeros((40,40),dtype=np.int64)]])
 return A,N,AL,G

def signed_tomography():
 p=[Fraction(1,10),Fraction(3,10),Fraction(1,10),Fraction(1,5),Fraction(3,10)]
 pm4,pms,p0,pps,pp4=p;a=pp4+pm4;b=pps+pms;d=pp4-pm4;e=pps-pms
 m1=(4*d,e);m2=16*a+6*b;m3=(64*d,6*e);m4=256*a+36*b
 ar=(m4-6*m2)/160;br=(16*m2-m4)/60;dr=(m3[0]-6*m1[0])/40;er=(16*m1[1]-m3[1])/10
 r=[(ar-dr)/2,(br-er)/2,1-ar-br,(br+er)/2,(ar+dr)/2];assert r==p
 return {'sector_order':['-4','-sqrt(6)','0','+sqrt(6)','+4'],'synthetic_populations':[frac(x) for x in p],'moments':{'m1':{'rational':frac(m1[0]),'sqrt6_coefficient':frac(m1[1])},'m2':frac(m2),'m3':{'rational':frac(m3[0]),'sqrt6_coefficient':frac(m3[1])},'m4':frac(m4)},'inverse':{'a=p(+4)+p(-4)':'(m4-6*m2)/160','b=p(+sqrt6)+p(-sqrt6)':'(16*m2-m4)/60','d=p(+4)-p(-4)':'(m3-6*m1)/40','e=p(+sqrt6)-p(-sqrt6)':'(16*m1-m3)/(10*sqrt6)','p0':'1-a-b','p(+/-4)':'(a+/-d)/2','p(+/-sqrt6)':'(b+/-e)/2'},'recovered_populations':[frac(x) for x in r]}

def main():
 A,N,AL,G=geometry();L=nx.from_numpy_array(AL);assert nx.is_connected(L) and set(dict(L.degree()).values())=={4}
 I80=np.eye(80,dtype=np.int64);H2=AL@AL
 raw=Counter(np.round(np.linalg.eigvalsh(AL.astype(float)),10));hs=Counter(np.rint(np.linalg.eigvalsh(H2.astype(float))).astype(int))
 target_raw=Counter({-4.0:1,-round(6**.5,10):24,0.0:30,round(6**.5,10):24,4.0:1})
 assert raw==target_raw and hs==Counter({0:30,6:48,16:2})
 P0=(H2-6*I80)@(H2-16*I80);P6=H2@(16*I80-H2);P16=H2@(H2-6*I80);Z80=np.zeros((80,80),dtype=np.int64)
 pc={'96E0_squared':np.array_equal(P0@P0,96*P0),'60E6_squared':np.array_equal(P6@P6,60*P6),'160E16_squared':np.array_equal(P16@P16,160*P16),'E0E6_zero':np.array_equal(P0@P6,Z80),'E0E16_zero':np.array_equal(P0@P16,Z80),'E6E16_zero':np.array_equal(P6@P16,Z80),'partition':np.array_equal(5*P0+8*P6+3*P16,480*I80)};pc={k:bool(v) for k,v in pc.items()};assert all(pc.values())
 assert [np.linalg.matrix_rank(x) for x in (P0,P6,P16)]==[30,48,2]
 half=60*I80-2*P6;quarter=(60*I80-P6+1j*P6)/60
 assert np.array_equal(half@half,60**2*I80) and np.allclose(quarter@quarter,half/60) and np.allclose(np.linalg.matrix_power(quarter,4),I80)
 Q=7*I80+5*AL;centered=Q-(np.trace(Q)//80)*I80;recovered=(centered//5).astype(np.int64);assert np.array_equal(recovered,AL) and int(recovered.sum()//2)==160
 edges=sorted(tuple(sorted(e)) for e in L.edges());assert len(edges)==160
 D=np.zeros((80,160),dtype=np.int64)
 for j,(u,v) in enumerate(edges):D[u,j]=-1;D[v,j]=1
 K=D.T@D;I160=np.eye(160,dtype=np.int64);Km4=K-4*I160
 Pcyc=(K-8*I160)@Km4@(Km4@Km4-6*I160)
 assert np.array_equal(Pcyc@Pcyc,320*Pcyc) and np.linalg.matrix_rank(Pcyc)==81 and np.array_equal(D@Pcyc,np.zeros((80,160),dtype=np.int64)) and set(np.diag(Pcyc))=={162} and np.linalg.matrix_rank(D)==79
 R=320*I160-2*Pcyc;assert np.array_equal(R@R,320**2*I160) and abs(np.trace(R)/320+2)<1e-12
 ev=np.linalg.eigvalsh(K.astype(float));es={'0':int(np.sum(np.isclose(ev,0))),'8':int(np.sum(np.isclose(ev,8))),'4':int(np.sum(np.isclose(ev,4))),'4-sqrt(6)':int(np.sum(np.isclose(ev,4-np.sqrt(6)))),'4+sqrt(6)':int(np.sum(np.isclose(ev,4+np.sqrt(6))))};assert es=={'0':81,'8':1,'4':30,'4-sqrt(6)':24,'4+sqrt(6)':24}
 p0,p6,p16=Fraction(17,100),Fraction(51,100),Fraction(32,100);m1=6*p6+16*p16;m2=36*p6+256*p16;rp16=(m2-6*m1)/160;rp6=(16*m1-m2)/60;rp0=1-rp6-rp16;assert (rp0,rp6,rp16)==(p0,p6,p16)
 checks={'w33_40_points_240_edges':A.shape==(40,40) and G.number_of_edges()==240,'incidence_40_by_40_160_flags':N.shape==(40,40) and int(N.sum())==160,'levi_80_modes_160_links_degree4':L.number_of_nodes()==80 and L.number_of_edges()==160 and set(dict(L.degree()).values())=={4},'raw_levi_spectrum':raw==target_raw,'two_step_integer_spectrum':hs==Counter({0:30,6:48,16:2}),'mode_projectors_exact':all(pc.values()),'mode_half_gate_involution':np.array_equal(half@half,60**2*I80),'mode_quarter_gate_order4':np.allclose(np.linalg.matrix_power(quarter,4),I80),'centered_delay_recovers_160_flags':np.array_equal(recovered,AL),'link_boundary_rank79':np.linalg.matrix_rank(D)==79,'link_cycle_rank81':160-80+1==81,'link_projector_exact_rank81':np.array_equal(Pcyc@Pcyc,320*Pcyc) and np.linalg.matrix_rank(Pcyc)==81,'link_projector_boundaryless':np.array_equal(D@Pcyc,np.zeros((80,160),dtype=np.int64)),'link_reflection_involution_trace_minus2':np.array_equal(R@R,320**2*I160) and abs(np.trace(R)/320+2)<1e-12,'three_sector_tomography_exact':(rp0,rp6,rp16)==(p0,p6,p16)};checks={k:bool(v) for k,v in checks.items()};assert all(checks.values())
 x={'schema':'w33.pass4013_4018.incidence_link_h1_memory.v1','status':'PASS_EXACT_INCIDENCE_LINK_H1_MEMORY_BRIDGE','pass4013_physical_incidence_link_h1_projector':{'incidence_layout':{'modes':80,'physical_links':160,'degree':4},'oriented_link_boundary_shape':[80,160],'boundary_rank':79,'cycle_rank':81,'edge_laplacian_spectrum':es,'projector_polynomial':'320P_H1=(K-8I)(K-4I)(((K-4I)^2)-6I)','projector_rank':81,'projector_diagonal':'81/160','proof_of_identification':'P_H1 is symmetric idempotent, im(P_H1) subset ker(D), and both spaces have dimension 81; therefore P_H1 is the canonical Hodge/Kirchhoff cycle projector.'},'pass4014_exact_link_memory_reflection':{'gate':'R_H1=I-2P_H1','eigenspaces':{'+1_cut':79,'-1_cycle':81},'trace':-2,'scaled_integral_form':'320R_H1=320I-2(320P_H1)','interpretation':'An exact reflection distinguishes physical link currents that are pure cuts from boundaryless cycle-memory currents.'},'pass4015_independent_two_step_incidence_revival':{'raw_Levi_spectrum':{'-4':1,'-sqrt(6)':24,'0':30,'+sqrt(6)':24,'+4':1},'raw_global_period':'none for t>0 because 4/sqrt(6) is irrational','sign_fold_generator':'H2=A_Levi^2','H2_spectrum':{'0':30,'6':48,'16':2},'minimal_full_revival_time':'pi','half_period_gate':'exp(-i*pi*H2/2)=I-2E6','quarter_period_gate':'exp(-i*pi*H2/4)=I+(i-1)E6','quarter_period_order':4,'relation_to_pass4005':'This polynomial sign-fold gate uses A_Levi^2. It is distinct from the exact finite-detuning block Hamiltonian certified in Pass 4005, although both use the same incidence matrix N.'},'pass4016_sign_resolved_four_moment_tomography':signed_tomography(),'pass4017_full_incidence_delay_recovery':{'ideal_model':'Q=tau_common I+theta_prime A_Levi','identity':'Q-(Tr Q/80)I=theta_prime A_Levi','recovered_vertices':80,'recovered_point_line_flags':160,'boundary':'Ideal-model inverse only; no measured scattering matrix or noise robustness is claimed.'},'pass4018_mode_memory_vs_link_memory_separation':{'mode_space':{'dimension':80,'H2_sector_ranks':[30,48,2]},'link_current_space':{'dimension':160,'cut_rank':79,'cycle_H1_rank':81},'bridge':'The 80-mode/160-link incidence architecture simultaneously hosts point-line bright/dark mode dynamics and a distinct protected H1=81 link-current memory sector.','nonconflation':'The 48-dimensional mode middle sector, the 30-dimensional mode kernel, and the 81-dimensional link cycle sector are different vector spaces and are not identified by dimension numerology.'},'three_sector_even_tomography':{'sector_order':['0','6','16'],'synthetic_populations':[frac(x) for x in (p0,p6,p16)],'moments':{'m1':frac(m1),'m2':frac(m2)},'inverse':{'p16':'(m2-6*m1)/160','p6':'(16*m1-m2)/60','p0':'1-p6-p16'},'recovered':[frac(x) for x in (rp0,rp6,rp16)]},'boundaries':['Exact finite graph and matrix statements only.','No fabricated coupler network, loss model, disorder tolerance, laboratory delay, variable vacuum c, literal hidden photon nodes, or hardware performance is claimed.','The raw Levi adjacency is not periodic; the exact polynomial revival belongs to A_Levi^2.','This packet does not claim the pending literal 48-orbital relation fusion or a Monster embedding.'],'checks':checks};x['semantic_sha256']=sha(x);OUT.write_text(json.dumps(x,indent=2,sort_keys=True)+'\n');print('PASS_4013_4018_INCIDENCE_LINK_H1_MEMORY',x['semantic_sha256'])
if __name__=='__main__':main()
