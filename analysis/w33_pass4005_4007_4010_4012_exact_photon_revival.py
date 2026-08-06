#!/usr/bin/env python3
"""Passes 4005-4007 and 4010-4012: exact finite-detuning W33 photon revival,
quadratic-form Wigner-Smith tomography, bright/dark write-hold-read memory,
revival arithmetic, spectral checksums, and synchronized tensor clocks.
"""
from __future__ import annotations
import hashlib,itertools,json,math
from pathlib import Path
import numpy as np
from scipy.linalg import expm,sinm
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_4005_4007_4010_4012_EXACT_PHOTON_REVIVAL.json'
def sha(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def norm(v):
 v=tuple(x%3 for x in v)
 for x in v:
  if x:
   inv=1 if x==1 else 2
   return tuple(inv*y%3 for y in v)
 raise ValueError

def sp(x,y):return (x[0]*y[2]+x[1]*y[3]-x[2]*y[0]-x[3]*y[1])%3
def geometry():
 pts=sorted({norm(v) for v in itertools.product(range(3),repeat=4) if any(v)});idx={p:i for i,p in enumerate(pts)};lines=set()
 for i,x in enumerate(pts):
  for y in pts[i+1:]:
   if sp(x,y):continue
   s={norm(tuple((a*x[j]+b*y[j])%3 for j in range(4))) for a,b in itertools.product(range(3),repeat=2) if a or b}
   if len(s)==4:lines.add(tuple(sorted(idx[p] for p in s)))
 assert len(pts)==len(lines)==40
 N=np.zeros((40,40))
 for j,line in enumerate(sorted(lines)):
  for i in line:N[i,j]=1
 A=N@N.T-4*np.eye(40);assert np.allclose(A.sum(1),12)
 return A,N
def projectors(N):
 I=np.eye(40);M=N@N.T
 E16=M@(M-6*I)/160;E6=M@(16*I-M)/60;E0=(M-16*I)@(M-6*I)/96
 F16=N.T@E16@N/16;F6=N.T@E6@N/6;F0=I-F16-F6
 for E,r in [(E16,1),(E6,24),(E0,15),(F16,1),(F6,24),(F0,15)]:assert np.allclose(E@E,E) and round(np.trace(E))==r
 return E16,E6,E0,F16,F6,F0
def revival(A,N,P):
 E16,E6,E0,F16,F6,F0=P;I=np.eye(40);Z=np.zeros((40,40));d=2*math.sqrt(2);t=math.pi/math.sqrt(2)
 H=np.block([[Z,N],[N.T,d*I]]);U=expm(-1j*t*H);Up=E16-E6+E0;Ul=F16-F6+F0;T=np.block([[Up,Z],[Z,Ul]])
 err=float(np.linalg.norm(U-T,2));leak=float(max(np.linalg.norm(U[:40,40:],2),np.linalg.norm(U[40:,:40],2)))
 assert err<2e-12 and leak<2e-12 and np.allclose(Up,-(I+A)/3+2*np.ones((40,40))/15)
 return {'hamiltonian':'H=g[[0,N],[N^T,(Delta/g)I]]','exact_ratio_Delta_over_g':'2*sqrt(2)','exact_interaction_g_t':'pi/sqrt(2)','sector_rabi_frequencies_over_g':{'sigma_4':'6*sqrt(2)','sigma_sqrt6':'4*sqrt(2)','bus_dark':'2*sqrt(2)'},'half_angle_windings':{'sigma_4':3,'sigma_sqrt6':2,'detuning':1},'point_action':'E16-E6+E0=I-2E6=-(I+A)/3+2J/15','line_action':'F16-F6+F0=I-2F6','off_block_leakage_operator_norm':leak,'full_unitary_operator_error':err,'claim':'Exact zero-leakage finite-detuning revival; no dispersive approximation is used.'}
def arithmetic(limit=600):
 out=[]
 for k in range(1,limit):
  for n6 in range(k+1,limit):
   q=8*n6*n6-5*k*k
   if q<=0 or q%3:continue
   n16=math.isqrt(q//3)
   if n16*n16!=q//3 or n16<=n6 or (n16+k)%2 or (n6+k)%2!=1 or math.gcd(math.gcd(n16,n6),k)!=1:continue
   d=n6*n6-k*k;out.append({'n16':n16,'n6':n6,'k':k,'Delta_over_g_squared':[24*k*k,d],'g_t_over_pi_squared':[d,6]})
 out.sort(key=lambda r:(r['n6']**2-r['k']**2,r['n16'],r['n6'],r['k']));assert out[0]=={'n16':3,'n6':2,'k':1,'Delta_over_g_squared':[24,3],'g_t_over_pi_squared':[3,6]}
 return {'integer_quadric':'3*n16^2-8*n6^2+5*k^2=0','phase_parities':'n16+k even; n6+k odd','parameter_map':'Delta/g=k*sqrt(24/(n6^2-k^2)); g*t=2*pi*sqrt((n6^2-k^2)/24)','smallest_positive_solution':out[0],'primitive_solutions_with_indices_below_600':out[:32],'primitive_solution_count_below_bound':len(out),'minimality':'n6^2-k^2 is at least 3 for positive n6>k; equality gives (n16,n6,k)=(3,2,1).'}
def tomography(A):
 L=12*np.eye(40)-A;Q=L.astype(complex);R=np.zeros_like(Q)
 for i in range(40):R[i,i]=Q[i,i]
 for i in range(40):
  for j in range(i+1,40):
   p=np.zeros(40,complex);p[i]=p[j]=1/math.sqrt(2);q=np.zeros(40,complex);q[i]=1/math.sqrt(2);q[j]=1j/math.sqrt(2)
   tp=float(np.real(p.conj()@Q@p));tq=float(np.real(q.conj()@Q@q));re=tp-(R[i,i].real+R[j,j].real)/2;im=(R[i,i].real+R[j,j].real)/2-tq;R[i,j]=re+1j*im;R[j,i]=re-1j*im
 err=float(np.max(np.abs(R-Q)));G=-np.real(R-np.trace(R).real*np.eye(40)/40);edges=int(np.sum(G>.5)//2);assert err<1e-13 and edges==240 and np.allclose(G,A)
 hs=[.12,.06,.03,.015];ce=[];re=[]
 for h in hs:
  Qh=sinm(h*L)/h;Q2=sinm(h*L/2)/(h/2);QR=(4*Q2-Qh)/3;ce.append(float(np.linalg.norm(Qh-L,2)));re.append(float(np.linalg.norm(QR-L,2)))
 return {'general_hermitian_quadratic_probe_count':1600,'reciprocal_real_symmetric_probe_count':820,'probe_formulas':{'diagonal':'Q_ii=tau(e_i)','real_offdiagonal':'Re Q_ij=tau((e_i+e_j)/sqrt(2))-(Q_ii+Q_jj)/2','imag_offdiagonal':'Im Q_ij=(Q_ii+Q_jj)/2-tau((e_i+i e_j)/sqrt(2))'},'ideal_reconstruction_max_error':err,'recovered_w33_edges':edges,'three_frequency_central_difference':{'linear_theta_exact_eigenvalue':'sin(h*theta_prime*lambda)/h','leading_bias':'-(h^2/6)*theta_prime^3*lambda^3','operator_bound':'||Q_h-Q|| <= (4096/6)*|theta_prime|^3*h^2+O(h^4)','step_sizes':hs,'central_errors':ce,'successive_central_error_ratios':[ce[i]/ce[i+1] for i in range(3)],'richardson_errors':re,'successive_richardson_error_ratios':[re[i]/re[i+1] for i in range(3)]},'causal_firewall':'Measure precursor/front arrival separately from Q; Q is dwell/group-delay memory and is subtracted before testing any mode-count-dependent front slope.'}
def memory(N,P):
 E16,E6,E0,F16,F6,F0=P;Pb=E16+E6;Fb=F16+F6;T=N.T@(E16/4+E6/math.sqrt(6));assert np.allclose(T.T@T,Pb) and np.allclose(T@T.T,Fb)
 Z=np.zeros((40,40));X=np.block([[Z,T.T],[T,Z]]);W=expm(-1j*math.pi*X/2);assert np.linalg.norm(W-(np.eye(80)-np.block([[Pb,Z],[Z,Fb]])-1j*X),2)<2e-12
 ph={'phi0':.37,'phi6':1.11,'phi16':-.42};H=np.block([[expm(-1j*ph['phi0']*E0),Z],[Z,expm(-1j*(ph['phi6']*F6+ph['phi16']*F16))]]);S=W.conj().T@H@W;target=np.exp(-1j*ph['phi0'])*E0+np.exp(-1j*ph['phi6'])*E6+np.exp(-1j*ph['phi16'])*E16
 err=float(np.linalg.norm(S[:40,:40]-target,2));leak=float(np.linalg.norm(S[40:,:40],2));R=W.conj().T@np.block([[np.eye(40),Z],[Z,F0+F16-F6]])@W;rerr=float(np.linalg.norm(R[:40,:40]-(E0+E16-E6),2));assert max(err,leak,rerr)<2e-12
 return {'polar_partial_isometry':'T=N^T(E16/4+E6/sqrt(6))','identities':['T^T T=E16+E6','T T^T=F16+F6'],'write_gate':'W=exp(-i*pi*X/2)=I-Pbright-Fbright-iX, X=[[0,T^T],[T,0]]','operation':'W sends the 25-dimensional point-bright sector to the line-bright sector and fixes both 15-dimensional dark sectors.','write_hold_read_point_action':'exp(-i phi0)E0+exp(-i phi6)E6+exp(-i phi16)E16','arbitrary_phase_test_operator_error':err,'arbitrary_phase_test_line_leakage':leak,'w33_reflection_hold_phases':{'phi0':0,'phi6':'pi','phi16':0},'w33_reflection_sequence_error':rerr,'boundary':'Exact controlled-Hamiltonian synthesis; engineering the polar coupling and fabricated performance are not claimed.'}
def checksum(A):
 L=12*np.eye(40)-A;I=np.eye(40);tau=np.trace(L)/480;C=L@(L-10*tau*I)@(L-16*tau*I);cn=float(np.linalg.norm(C,2));assert cn<1e-10 and np.allclose(-(L-np.trace(L)*I/40)/tau,A)
 rows=[]
 for m in range(1,9):rows.append({'m':m,'point_dimension':40**m,'plus_multiplicity':(40**m+(-8)**m)//2,'minus_multiplicity':(40**m-(-8)**m)//2})
 return {'basis_free_checksum':'Q(Q-10*tau I)(Q-16*tau I)=0 with tau=Tr(Q)/480','checksum_operator_norm_at_theta_prime_1':cn,'self_calibrating_projectors':{'E0':'(Q-10 tau I)(Q-16 tau I)/(160 tau^2)','E10':'Q(16 tau I-Q)/(60 tau^2)','E16':'Q(Q-10 tau I)/(96 tau^2)'},'geometry_recovery':'A=-(Q-Tr(Q)I/40)/tau','synchronized_tensor_clock':{'generator':'sum of m commuting copies of the exact 80-mode revival Hamiltonian','same_gate_time':'g*t=pi/sqrt(2) for every tensor depth','point_action':'U_point^tensor_m','point_plus_minus_multiplicities':rows,'closed_form':'m_plus=(40^m+(-8)^m)/2; m_minus=(40^m-(-8)^m)/2','boundary':'Parallel under m physical factors; literal hardware grows with factor count.'}}
def main():
 A,N=geometry();P=projectors(N);x={'schema':'w33.pass4005_4007_4010_4012.exact_photon_revival.v1','status':'PASS_EXACT_NONDISPERSIVE_REVIVAL_TOMOGRAPHY_MEMORY_AND_THREE_CONSTRUCTIONS','geometry':{'points':40,'lines':40,'incidences':int(N.sum()),'identity':'N N^T=4I+A_W33','singular_values':{'4':1,'sqrt(6)':24,'0':15}},'pass4005_exact_nondispersive_revival':revival(A,N,P),'pass4006_quadratic_form_wigner_smith_tomography':tomography(A),'pass4007_exact_bright_dark_write_hold_read':memory(N,P),'pass4010_bonkers_revival_arithmetic':arithmetic(),'pass4011_bonkers_spectral_checksum_and_geometry_oracle':checksum(A),'pass4012_bonkers_synchronized_tensor_clock':'Included under pass4011 checksum_and_tensor.synchronized_tensor_clock','boundary':'Exact finite-dimensional matrix, revival, tomography-inversion, and controlled-gate statements only. No fabricated device, measured Wigner-Smith matrix, variable vacuum c, literal photon-node ontology, hardware scaling advantage, Monster embedding, or laboratory performance is claimed.'};x['semantic_sha256']=sha(x);OUT.write_text(json.dumps(x,indent=2,sort_keys=True)+'\n');print('PASS_EXACT_PHOTON_REVIVAL',x['semantic_sha256'])
if __name__=='__main__':main()
